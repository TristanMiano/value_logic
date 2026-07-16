"""Block-oriented, data-only evaluator for implementation version 1.1.

The frozen generator still creates rich records once.  This adapter immediately
projects them into fixed numeric arrays.  Every fit seed then reuses those
arrays, batches neural inference, and calls the exact semantic kernel once per
panel rather than constructing millions of short-lived Python objects.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Mapping, Sequence

import numpy as np

from experiments.cpp_kernel import CppKernel, KernelInputs, KernelOutputs, OPEN
from experiments.implementation import (
    BOUNDARY_CONDITIONS,
    FEATURE_NAMES,
    SCHEMA_SCALE,
    TRANSFER_OFFSETS,
    CalibrationBundle,
    CalibrationGroup,
    boundary_status_cases,
    encode_probe,
    encode_request_atom,
    probe_target_weight,
    request_target_weight,
    tolerance_transfer_cases,
)
from experiments.learner import ReluMLP, WorldPanelData, predict
from experiments.protocol import (
    FIT_SEEDS,
    AtomRecord,
    EvidenceMode,
    GeneratedWorld,
    Plan,
    RequestAtom,
    RequestRecord,
    Role,
    Schema,
    generate_world,
    ALPHA_CAL,
)
from verification.kernel import AtomValue, Outcome
from verification.losses import proposed_calibration_radius


PROBE_ROWS = 80
BOUNDARY_ROWS = 320
TRANSFER_ROWS = 320
REQUEST_ROWS = 120
REQUEST_COUNT = 40
TOTAL_ROWS = PROBE_ROWS + BOUNDARY_ROWS + TRANSFER_ROWS + REQUEST_ROWS
# Batched and one-world-at-a-time PyTorch matrix multiplication can differ by a
# few float32 ULPs.  Converting normalized latency outputs back to milliseconds
# magnifies the largest observed pilot difference to 7.63e-6.  Discrete states,
# masks, routes, feature arrays, and C++/NumPy outputs remain exact.
FLOAT_TRACE_EQUIVALENCE_ATOL = 1e-5

PLAN_INDEX = {plan: index for index, plan in enumerate(Plan)}
SCHEMA_INDEX = {Schema.LOSS: 0, Schema.LATENCY: 1}
MODE_INDEX = {
    (True, True): 0,
    (True, False): 1,
    (False, True): 2,
    (False, False): 3,
}
OUTCOME_INDEX = {outcome: index for index, outcome in enumerate(Outcome)}


@dataclass(frozen=True)
class PanelArrays:
    features: np.ndarray
    schema: np.ndarray
    threshold: np.ndarray
    evidence_present: np.ndarray
    evidence_valid: np.ndarray
    can_support: np.ndarray
    can_refute: np.ndarray
    reference: np.ndarray
    weights: np.ndarray
    group: np.ndarray
    stage: np.ndarray

    @property
    def rows_per_world(self) -> int:
        return int(self.features.shape[1])


@dataclass(frozen=True)
class PreparedEvaluationBlock:
    role: Role
    start: int
    probe: PanelArrays
    boundary: PanelArrays
    transfer: PanelArrays
    request: PanelArrays
    probe_oracle_target: np.ndarray
    probe_target_present: np.ndarray
    request_well_formed: np.ndarray
    request_reference_outcome: np.ndarray
    request_plan: np.ndarray
    request_weights: np.ndarray

    @property
    def world_count(self) -> int:
        return int(self.probe.features.shape[0])

    def combined_features(self) -> np.ndarray:
        return np.concatenate(
            (
                self.probe.features,
                self.boundary.features,
                self.transfer.features,
                self.request.features,
            ),
            axis=1,
        ).reshape(-1, len(FEATURE_NAMES))


@dataclass(frozen=True)
class BlockEvaluation:
    metrics: tuple[Mapping[str, Any], ...]
    traces: tuple[Mapping[str, np.ndarray], ...]


def _write_feature(
    output: np.ndarray,
    *,
    x: float,
    complexity: float,
    difficulty: float,
    stage: int,
    threshold: float,
    delta: float,
    fallback: float,
    well_formed: bool,
    evidence_present: bool,
    evidence_valid: bool,
    can_support: bool,
    can_refute: bool,
    plan: Plan,
    schema: Schema,
) -> None:
    """Write the frozen 25-coordinate vector without constructing a mapping."""

    output.fill(0.0)
    scale = SCHEMA_SCALE[schema]
    output[:15] = (
        x,
        complexity,
        difficulty,
        stage / 3.0,
        threshold / scale,
        delta / SCHEMA_SCALE[Schema.LOSS],
        fallback / SCHEMA_SCALE[Schema.LOSS],
        float(well_formed),
        float(evidence_present),
        float(evidence_valid),
        1.0,
        1.0,
        float(can_support),
        float(can_refute),
        1.0,
    )
    output[15 + PLAN_INDEX[plan]] = 1.0
    output[19 + SCHEMA_INDEX[schema]] = 1.0
    output[21 + MODE_INDEX[(can_support, can_refute)]] = 1.0


def _probe_feature(probe: AtomRecord, output: np.ndarray) -> None:
    _write_feature(
        output,
        x=probe.x,
        complexity=probe.complexity,
        difficulty=probe.difficulty,
        stage=probe.stage,
        threshold=probe.threshold,
        delta=0.0,
        fallback=0.0,
        well_formed=True,
        evidence_present=probe.evidence_present,
        evidence_valid=probe.evidence_valid,
        can_support=probe.can_support,
        can_refute=probe.can_refute,
        plan=probe.plan,
        schema=probe.schema,
    )


def _request_feature(request: RequestRecord, atom: RequestAtom, output: np.ndarray) -> None:
    _write_feature(
        output,
        x=request.x,
        complexity=request.complexity,
        difficulty=request.difficulty,
        stage=request.stage,
        threshold=atom.threshold,
        delta=request.delta if atom.name == "I" else 0.0,
        fallback=request.fallback_loss if atom.name == "I" else 0.0,
        well_formed=request.well_formed,
        evidence_present=atom.evidence_present,
        evidence_valid=atom.evidence_valid,
        can_support=atom.can_support,
        can_refute=atom.can_refute,
        plan=request.plan,
        schema=atom.schema,
    )


def _decode_reference(
    lower: float,
    upper: float,
    threshold: float,
    present: bool,
    valid: bool,
    can_support: bool,
    can_refute: bool,
) -> int:
    if not (present and valid):
        return int(AtomValue.OPEN)
    if upper <= threshold and can_support:
        return int(AtomValue.SUPPORTED)
    if lower > threshold and can_refute:
        return int(AtomValue.REFUTED)
    return int(AtomValue.OPEN)


def _empty_panel(worlds: int, rows: int) -> dict[str, np.ndarray]:
    return {
        "features": np.empty((worlds, rows, len(FEATURE_NAMES)), dtype=np.float32),
        "schema": np.empty((worlds, rows), dtype=np.int8),
        "threshold": np.empty((worlds, rows), dtype=np.float64),
        "evidence_present": np.empty((worlds, rows), dtype=np.uint8),
        "evidence_valid": np.empty((worlds, rows), dtype=np.uint8),
        "can_support": np.empty((worlds, rows), dtype=np.uint8),
        "can_refute": np.empty((worlds, rows), dtype=np.uint8),
        "reference": np.empty((worlds, rows), dtype=np.int8),
        "weights": np.empty((worlds, rows), dtype=np.float64),
        "group": np.empty((worlds, rows), dtype=np.int16),
        "stage": np.empty((worlds, rows), dtype=np.int8),
    }


def _freeze_panel(storage: Mapping[str, np.ndarray]) -> PanelArrays:
    return PanelArrays(**storage)


def _prepare_world(
    world: GeneratedWorld,
    local: int,
    probe: Mapping[str, np.ndarray],
    boundary: Mapping[str, np.ndarray],
    transfer: Mapping[str, np.ndarray],
    request_panel: Mapping[str, np.ndarray],
    probe_oracle_target: np.ndarray,
    probe_target_present: np.ndarray,
    request_well_formed: np.ndarray,
    request_reference_outcome: np.ndarray,
    request_plan: np.ndarray,
    request_weights: np.ndarray,
) -> None:
    if len(world.probes) != PROBE_ROWS or len(world.requests) != REQUEST_COUNT:
        raise ValueError("the frozen world shape changed")

    for row, atom in enumerate(world.probes):
        _probe_feature(atom, probe["features"][local, row])
        schema = SCHEMA_INDEX[atom.schema]
        weight = probe_target_weight(atom)
        probe["schema"][local, row] = schema
        probe["threshold"][local, row] = atom.threshold
        probe["evidence_present"][local, row] = atom.evidence_present
        probe["evidence_valid"][local, row] = atom.evidence_valid
        probe["can_support"][local, row] = atom.can_support
        probe["can_refute"][local, row] = atom.can_refute
        probe["reference"][local, row] = int(atom.value)
        probe["weights"][local, row] = weight
        probe["group"][local, row] = schema * 3 + int(atom.value)
        probe["stage"][local, row] = atom.stage
        probe_oracle_target[local, row] = atom.oracle_target
        probe_target_present[local, row] = atom.learning_target is not None

        base = probe["features"][local, row]
        schema_scale = SCHEMA_SCALE[atom.schema]
        boundary_scale = atom.oracle_scale
        boundary_start = 4 * row
        boundary_stop = boundary_start + 4
        boundary["features"][local, boundary_start:boundary_stop] = base
        boundary_thresholds = np.asarray(
            (
                atom.reference_region.upper + 0.25 * boundary_scale,
                atom.reference_region.upper,
                (atom.reference_region.lower + atom.reference_region.upper) / 2.0,
                atom.reference_region.lower - 0.25 * boundary_scale,
            ),
            dtype=np.float64,
        )
        boundary["features"][local, boundary_start:boundary_stop, 4] = (
            boundary_thresholds / schema_scale
        ).astype(np.float32)
        boundary["features"][local, boundary_start:boundary_stop, 8:14] = 1.0
        boundary["features"][local, boundary_start:boundary_stop, 21:25] = 0.0
        boundary["features"][local, boundary_start:boundary_stop, 21] = 1.0
        boundary["schema"][local, boundary_start:boundary_stop] = schema
        boundary["threshold"][local, boundary_start:boundary_stop] = boundary_thresholds
        boundary["evidence_present"][local, boundary_start:boundary_stop] = 1
        boundary["evidence_valid"][local, boundary_start:boundary_stop] = 1
        boundary["can_support"][local, boundary_start:boundary_stop] = 1
        boundary["can_refute"][local, boundary_start:boundary_stop] = 1
        boundary["reference"][local, boundary_start:boundary_stop] = (2, 2, 1, 0)
        boundary["weights"][local, boundary_start:boundary_stop] = weight
        boundary["group"][local, boundary_start:boundary_stop] = schema * 4 + np.arange(4)
        boundary["stage"][local, boundary_start:boundary_stop] = atom.stage

        transfer_start = 4 * row
        transfer_stop = transfer_start + 4
        transfer["features"][local, transfer_start:transfer_stop] = base
        transfer_thresholds = atom.threshold + np.asarray(TRANSFER_OFFSETS) * atom.oracle_scale
        transfer["features"][local, transfer_start:transfer_stop, 4] = (
            transfer_thresholds / schema_scale
        ).astype(np.float32)
        transfer["schema"][local, transfer_start:transfer_stop] = schema
        transfer["threshold"][local, transfer_start:transfer_stop] = transfer_thresholds
        transfer["evidence_present"][local, transfer_start:transfer_stop] = atom.evidence_present
        transfer["evidence_valid"][local, transfer_start:transfer_stop] = atom.evidence_valid
        transfer["can_support"][local, transfer_start:transfer_stop] = atom.can_support
        transfer["can_refute"][local, transfer_start:transfer_stop] = atom.can_refute
        references = np.asarray(
            [
                _decode_reference(
                    atom.reference_region.lower,
                    atom.reference_region.upper,
                    float(threshold),
                    atom.evidence_present,
                    atom.evidence_valid,
                    atom.can_support,
                    atom.can_refute,
                )
                for threshold in transfer_thresholds
            ],
            dtype=np.int8,
        )
        transfer["reference"][local, transfer_start:transfer_stop] = references
        transfer["weights"][local, transfer_start:transfer_stop] = weight
        transfer["group"][local, transfer_start:transfer_stop] = (
            (schema * 3 + references.astype(np.int16)) * 4 + np.arange(4)
        )
        transfer["stage"][local, transfer_start:transfer_stop] = atom.stage

    cursor = 0
    for request_index, request in enumerate(world.requests):
        if tuple(atom.name for atom in request.atoms) != ("A", "I", "C"):
            raise ValueError("request atoms are no longer ordered A, I, C")
        request_well_formed[local, request_index] = request.well_formed
        request_reference_outcome[local, request_index] = OUTCOME_INDEX[request.outcome]
        request_plan[local, request_index] = PLAN_INDEX[request.plan]
        request_weights[local, request_index] = request_target_weight(request)
        for atom in request.atoms:
            _request_feature(request, atom, request_panel["features"][local, cursor])
            schema = SCHEMA_INDEX[atom.schema]
            request_panel["schema"][local, cursor] = schema
            request_panel["threshold"][local, cursor] = atom.threshold
            request_panel["evidence_present"][local, cursor] = atom.evidence_present
            request_panel["evidence_valid"][local, cursor] = atom.evidence_valid
            request_panel["can_support"][local, cursor] = atom.can_support
            request_panel["can_refute"][local, cursor] = atom.can_refute
            request_panel["reference"][local, cursor] = int(atom.value)
            request_panel["weights"][local, cursor] = request_weights[local, request_index]
            request_panel["group"][local, cursor] = request_index
            request_panel["stage"][local, cursor] = request.stage
            cursor += 1


def prepare_evaluation_block(
    role: Role,
    start: int,
    count: int,
    *,
    allow_final: bool = False,
) -> PreparedEvaluationBlock:
    if start < 0 or count <= 0:
        raise ValueError("evaluation block range is invalid")
    stores = {
        "probe": _empty_panel(count, PROBE_ROWS),
        "boundary": _empty_panel(count, BOUNDARY_ROWS),
        "transfer": _empty_panel(count, TRANSFER_ROWS),
        "request": _empty_panel(count, REQUEST_ROWS),
    }
    probe_oracle_target = np.empty((count, PROBE_ROWS), dtype=np.float64)
    probe_target_present = np.empty((count, PROBE_ROWS), dtype=np.uint8)
    request_well_formed = np.empty((count, REQUEST_COUNT), dtype=np.uint8)
    request_reference_outcome = np.empty((count, REQUEST_COUNT), dtype=np.int8)
    request_plan = np.empty((count, REQUEST_COUNT), dtype=np.int8)
    request_weights = np.empty((count, REQUEST_COUNT), dtype=np.float64)
    for local, index in enumerate(range(start, start + count)):
        _prepare_world(
            generate_world(role, index, allow_final=allow_final),
            local,
            stores["probe"],
            stores["boundary"],
            stores["transfer"],
            stores["request"],
            probe_oracle_target,
            probe_target_present,
            request_well_formed,
            request_reference_outcome,
            request_plan,
            request_weights,
        )
    return PreparedEvaluationBlock(
        role,
        start,
        _freeze_panel(stores["probe"]),
        _freeze_panel(stores["boundary"]),
        _freeze_panel(stores["transfer"]),
        _freeze_panel(stores["request"]),
        probe_oracle_target,
        probe_target_present,
        request_well_formed,
        request_reference_outcome,
        request_plan,
        request_weights,
    )


def materialize_training_panel_fast(
    role: Role,
    start: int,
    count: int,
    *,
    allow_final: bool = False,
) -> WorldPanelData:
    """Project the 80 learning probes per world directly into numeric arrays."""

    if start < 0 or count <= 0:
        raise ValueError("training panel range is invalid")
    features = np.empty((count, PROBE_ROWS, len(FEATURE_NAMES)), dtype=np.float32)
    targets = np.empty((count, PROBE_ROWS), dtype=np.float32)
    schemas = np.empty((count, PROBE_ROWS), dtype=np.int8)
    states = np.empty((count, PROBE_ROWS), dtype=np.int8)
    weights = np.empty((count, PROBE_ROWS), dtype=np.float32)
    for local, index in enumerate(range(start, start + count)):
        world = generate_world(role, index, allow_final=allow_final)
        if len(world.probes) != PROBE_ROWS:
            raise ValueError("the frozen world does not contain 80 learning probes")
        for row, atom in enumerate(world.probes):
            _probe_feature(atom, features[local, row])
            scale = SCHEMA_SCALE[atom.schema]
            targets[local, row] = (
                np.nan if atom.learning_target is None else atom.learning_target / scale
            )
            schemas[local, row] = SCHEMA_INDEX[atom.schema]
            states[local, row] = int(atom.value)
            weights[local, row] = probe_target_weight(atom)
    return WorldPanelData(features, targets, schemas, states, weights)


def assert_training_adapter_equivalence(role: Role = Role.PILOT, worlds: int = 8) -> None:
    from experiments.implementation import materialize_panel

    legacy = materialize_panel(role, 0, worlds)
    repaired = materialize_training_panel_fast(role, 0, worlds)
    for name in (
        "features",
        "statistic_targets",
        "schemas",
        "state_targets",
        "weights",
    ):
        if not np.array_equal(getattr(legacy, name), getattr(repaired, name), equal_nan=True):
            raise AssertionError(f"fast training adapter differs from v1 in {name}")


def calibrate_structured_pair(
    model: ReluMLP,
    data: WorldPanelData,
    *,
    scorer_parameter_hash: str,
    training_manifest_hash: str,
    calibration_manifest_hash: str,
) -> tuple[CalibrationBundle, CalibrationBundle]:
    """Compute full and center-only calibration from one batched prediction."""

    raw = predict(model, data.features.reshape(-1, data.feature_count)).reshape(
        data.world_count, PROBE_ROWS, -1
    )

    def build(center_only: bool) -> CalibrationBundle:
        groups: dict[Schema, CalibrationGroup] = {}
        for schema, schema_index, center_index, radius_index in (
            (Schema.LOSS, 0, 0, 1),
            (Schema.LATENCY, 1, 2, 3),
        ):
            residuals: list[float] = []
            for world_index in range(data.world_count):
                eligible = np.flatnonzero(
                    (data.schemas[world_index] == schema_index)
                    & ~np.isnan(data.statistic_targets[world_index])
                )
                if len(eligible) == 0:
                    continue
                local_weights = data.weights[world_index, eligible].astype(np.float64)
                local_weights /= local_weights.sum()
                token = sha256(
                    f"calibration-row-v1|{world_index}|{schema.value}".encode("utf-8")
                ).digest()
                unit = int.from_bytes(token[:8], "big") / 2**64
                selected_position = min(
                    len(eligible) - 1,
                    int(np.searchsorted(np.cumsum(local_weights), unit, side="right")),
                )
                row = int(eligible[selected_position])
                center = float(raw[world_index, row, center_index])
                radius = (
                    0.0
                    if center_only
                    else max(0.0, float(raw[world_index, row, radius_index]))
                )
                target = float(data.statistic_targets[world_index, row])
                residuals.append(max(abs(target - center) - radius, 0.0))
            proposal = proposed_calibration_radius(
                tuple(float(value) for value in residuals),
                ALPHA_CAL,
            )
            groups[schema] = CalibrationGroup(
                schema,
                proposal.radius,
                data.world_count,
                len(residuals),
                proposal.rank,
            )
        variant = "center_only" if center_only else "structured"
        digest = sha256(
            json.dumps(
                {
                    "scorer": scorer_parameter_hash,
                    "variant": variant,
                    "training": training_manifest_hash,
                    "calibration": calibration_manifest_hash,
                    "groups": {
                        schema.value: asdict(group)
                        for schema, group in groups.items()
                    },
                },
                sort_keys=True,
                default=str,
            ).encode("utf-8")
        ).hexdigest()
        return CalibrationBundle(
            scorer_parameter_hash,
            variant,
            training_manifest_hash,
            calibration_manifest_hash,
            groups,
            f"calibration:{digest}",
        )

    return build(False), build(True)


def assert_fast_adapter_equivalence(role: Role = Role.PILOT, worlds: int = 8) -> None:
    """Prove on pilot records that the direct array projection matches v1."""

    prepared = prepare_evaluation_block(role, 0, worlds)
    for local in range(worlds):
        world = generate_world(role, local)
        expected_probe = np.stack([encode_probe(atom) for atom in world.probes])
        if not np.array_equal(expected_probe, prepared.probe.features[local]):
            raise AssertionError("fast probe feature adapter differs from v1")
        expected_boundary = [
            case.feature
            for atom in world.probes
            for case in boundary_status_cases(atom)
        ]
        expected_transfer = [
            case.feature
            for atom in world.probes
            for case in tolerance_transfer_cases(atom)
        ]
        if not np.array_equal(np.stack(expected_boundary), prepared.boundary.features[local]):
            raise AssertionError("fast boundary feature adapter differs from v1")
        if not np.array_equal(np.stack(expected_transfer), prepared.transfer.features[local]):
            raise AssertionError("fast transfer feature adapter differs from v1")
        expected_request = np.stack(
            [encode_request_atom(request, atom) for request in world.requests for atom in request.atoms]
        )
        if not np.array_equal(expected_request, prepared.request.features[local]):
            raise AssertionError("fast request feature adapter differs from v1")


def _binding_vectors(
    panel: PanelArrays,
    calibration: CalibrationBundle,
) -> tuple[np.ndarray, np.ndarray]:
    eta_by_schema = np.asarray(
        [
            calibration.groups[Schema.LOSS].eta_normalized * SCHEMA_SCALE[Schema.LOSS],
            calibration.groups[Schema.LATENCY].eta_normalized * SCHEMA_SCALE[Schema.LATENCY],
        ],
        dtype=np.float64,
    )
    count_ok = np.asarray(
        [
            calibration.groups[Schema.LOSS].calibration_worlds >= 200,
            calibration.groups[Schema.LATENCY].calibration_worlds >= 200,
        ],
        dtype=bool,
    )
    eta = eta_by_schema[panel.schema]
    ok = count_ok[panel.schema] & np.isfinite(eta) & (panel.stage >= 0) & (panel.stage <= 3)
    return eta, ok.astype(np.uint8)


def _decode_panel(
    panel: PanelArrays,
    structured_raw: np.ndarray,
    ce_raw: np.ndarray,
    calibration: CalibrationBundle,
    center_calibration: CalibrationBundle,
    kernel: CppKernel,
) -> KernelOutputs:
    eta, binding = _binding_vectors(panel, calibration)
    center_eta, center_binding = _binding_vectors(panel, center_calibration)
    shape = panel.schema.shape
    return kernel.decode(
        KernelInputs(
            structured_raw.reshape(-1, 4),
            ce_raw.reshape(-1, 3),
            panel.schema.reshape(-1),
            panel.threshold.reshape(-1),
            panel.evidence_present.reshape(-1),
            panel.evidence_valid.reshape(-1),
            panel.can_support.reshape(-1),
            panel.can_refute.reshape(-1),
            eta.reshape(-1),
            center_eta.reshape(-1),
            binding.reshape(-1),
            center_binding.reshape(-1),
        )
    )


def _reshape_kernel(output: KernelOutputs, worlds: int, rows: int) -> KernelOutputs:
    return KernelOutputs(
        *(getattr(output, name).reshape(worlds, rows) for name in output.__dataclass_fields__)
    )


def _macro_accuracy(
    reference: np.ndarray,
    prediction: np.ndarray,
    group: np.ndarray,
    weights: np.ndarray,
) -> np.ndarray:
    worlds = reference.shape[0]
    scores = np.zeros(worlds, dtype=np.float64)
    group_counts = np.zeros(worlds, dtype=np.int16)
    correct = reference == prediction
    for group_id in range(int(group.max()) + 1):
        selected = group == group_id
        total = np.sum(np.where(selected, weights, 0.0), axis=1)
        present = total > 0.0
        numerator = np.sum(np.where(selected & correct, weights, 0.0), axis=1)
        scores[present] += numerator[present] / total[present]
        group_counts[present] += 1
    if np.any(group_counts == 0):
        raise ValueError("macro accuracy has a world with no groups")
    return scores / group_counts


def _request_outcomes(states: np.ndarray, well_formed: np.ndarray) -> np.ndarray:
    atoms = states.reshape(states.shape[0], REQUEST_COUNT, 3)
    aggregate = atoms.min(axis=2)
    outcomes = np.where(aggregate == 2, 3, np.where(aggregate == 0, 1, 2)).astype(np.int8)
    outcomes[~well_formed.astype(bool)] = 0
    return outcomes


def _request_accuracy(
    reference: np.ndarray,
    prediction: np.ndarray,
    weights: np.ndarray,
) -> np.ndarray:
    return np.sum(weights * (reference == prediction), axis=1) / np.sum(weights, axis=1)


def _fallback_mass(prediction: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return np.sum(weights * (prediction != 3), axis=1) / np.sum(weights, axis=1)


def evaluate_model_on_block(
    block: PreparedEvaluationBlock,
    structured_model: ReluMLP,
    ce_model: ReluMLP,
    structured_hash: str,
    calibration: CalibrationBundle,
    center_calibration: CalibrationBundle,
    kernel: CppKernel,
    *,
    fit_seed: int,
    combined_features: np.ndarray | None = None,
) -> BlockEvaluation:
    if calibration.scorer_parameter_hash != structured_hash:
        raise ValueError("calibration bundle is not bound to the structured model")
    if center_calibration.scorer_parameter_hash != structured_hash:
        raise ValueError("center calibration is not bound to the structured model")
    worlds = block.world_count
    features = block.combined_features() if combined_features is None else combined_features
    if features.shape != (worlds * TOTAL_ROWS, len(FEATURE_NAMES)):
        raise ValueError("combined evaluation features have the wrong shape")
    structured_all = predict(structured_model, features).reshape(worlds, TOTAL_ROWS, 4)
    ce_all = predict(ce_model, features).reshape(worlds, TOTAL_ROWS, 3)
    slices = {
        "probe": slice(0, PROBE_ROWS),
        "boundary": slice(PROBE_ROWS, PROBE_ROWS + BOUNDARY_ROWS),
        "transfer": slice(PROBE_ROWS + BOUNDARY_ROWS, PROBE_ROWS + BOUNDARY_ROWS + TRANSFER_ROWS),
        "request": slice(PROBE_ROWS + BOUNDARY_ROWS + TRANSFER_ROWS, TOTAL_ROWS),
    }
    decoded = {
        name: _reshape_kernel(
            _decode_panel(
                getattr(block, name),
                structured_all[:, local_slice],
                ce_all[:, local_slice],
                calibration,
                center_calibration,
                kernel,
            ),
            worlds,
            getattr(block, name).rows_per_world,
        )
        for name, local_slice in slices.items()
    }

    probe = decoded["probe"]
    boundary = decoded["boundary"]
    transfer = decoded["transfer"]
    request = decoded["request"]
    open_probe = np.full_like(probe.structured_state, OPEN)
    open_request = np.full_like(request.structured_state, OPEN)

    request_structured = _request_outcomes(request.structured_state, block.request_well_formed)
    request_ce = _request_outcomes(request.ce_state, block.request_well_formed)
    request_center = _request_outcomes(request.center_state, block.request_well_formed)
    request_unaccepted = _request_outcomes(open_request, block.request_well_formed)
    request_self = _request_outcomes(request.self_confidence_state, block.request_well_formed)

    eta, _ = _binding_vectors(block.probe, calibration)
    rows = np.arange(PROBE_ROWS)[None, :]
    scales = np.where(block.probe.schema == 0, 0.1, 10.0)
    raw_probe = structured_all[:, slices["probe"]]
    centers = np.where(
        block.probe.schema == 0,
        raw_probe[:, :, 0],
        raw_probe[:, :, 2],
    ).astype(np.float64) * scales
    radii = np.maximum(
        np.where(block.probe.schema == 0, raw_probe[:, :, 1], raw_probe[:, :, 3]),
        0.0,
    ).astype(np.float64) * scales + eta
    contains = (
        (centers - radii <= block.probe_oracle_target)
        & (block.probe_oracle_target <= centers + radii)
        & block.probe_target_present.astype(bool)
    )

    metric_columns = {
        "E_in_structured": _macro_accuracy(block.probe.reference, probe.structured_state, block.probe.group, block.probe.weights),
        "E_in_ce": _macro_accuracy(block.probe.reference, probe.ce_state, block.probe.group, block.probe.weights),
        "E_in_center_only": _macro_accuracy(block.probe.reference, probe.center_state, block.probe.group, block.probe.weights),
        "E_in_unaccepted_radius_shadow": _macro_accuracy(block.probe.reference, probe.shadow_state, block.probe.group, block.probe.weights),
        "E_in_unaccepted_radius_production": _macro_accuracy(block.probe.reference, open_probe, block.probe.group, block.probe.weights),
        "E_in_self_confidence_invalid": _macro_accuracy(block.probe.reference, probe.self_confidence_state, block.probe.group, block.probe.weights),
        "E_boundary_structured": _macro_accuracy(block.boundary.reference, boundary.structured_state, block.boundary.group, block.boundary.weights),
        "E_boundary_ce": _macro_accuracy(block.boundary.reference, boundary.ce_state, block.boundary.group, block.boundary.weights),
        "E_boundary_center_only": _macro_accuracy(block.boundary.reference, boundary.center_state, block.boundary.group, block.boundary.weights),
        "E_boundary_unaccepted_radius_shadow": _macro_accuracy(block.boundary.reference, boundary.shadow_state, block.boundary.group, block.boundary.weights),
        "E_boundary_self_confidence_invalid": _macro_accuracy(block.boundary.reference, boundary.self_confidence_state, block.boundary.group, block.boundary.weights),
        "E_transfer_structured": _macro_accuracy(block.transfer.reference, transfer.structured_state, block.transfer.group, block.transfer.weights),
        "E_transfer_ce": _macro_accuracy(block.transfer.reference, transfer.ce_state, block.transfer.group, block.transfer.weights),
        "E_transfer_center_only": _macro_accuracy(block.transfer.reference, transfer.center_state, block.transfer.group, block.transfer.weights),
        "E_transfer_unaccepted_radius_shadow": _macro_accuracy(block.transfer.reference, transfer.shadow_state, block.transfer.group, block.transfer.weights),
        "E_transfer_self_confidence_invalid": _macro_accuracy(block.transfer.reference, transfer.self_confidence_state, block.transfer.group, block.transfer.weights),
        "query_outcome_structured": _request_accuracy(block.request_reference_outcome, request_structured, block.request_weights),
        "query_outcome_ce": _request_accuracy(block.request_reference_outcome, request_ce, block.request_weights),
        "query_outcome_center_only": _request_accuracy(block.request_reference_outcome, request_center, block.request_weights),
        "query_outcome_unaccepted_radius_production": _request_accuracy(block.request_reference_outcome, request_unaccepted, block.request_weights),
        "query_outcome_self_confidence_invalid": _request_accuracy(block.request_reference_outcome, request_self, block.request_weights),
        "fallback_mass_structured": _fallback_mass(request_structured, block.request_weights),
        "fallback_mass_ce": _fallback_mass(request_ce, block.request_weights),
        "inactive_selection_rate_structured": np.zeros(worlds),
        "inactive_selection_rate_ce": np.zeros(worlds),
    }
    for schema_index, name in ((0, "coverage_J"), (1, "coverage_T")):
        eligible = (block.probe.schema == schema_index) & block.probe_target_present.astype(bool)
        metric_columns[name] = np.sum(contains & eligible, axis=1) / np.sum(eligible, axis=1)

    metrics = tuple(
        {
            "fit_seed": fit_seed,
            "world_index": block.start + world,
            **{name: float(values[world]) for name, values in metric_columns.items()},
        }
        for world in range(worlds)
    )

    traces = []
    for world in range(worlds):
        traces.append(
            {
                "probe_structured_raw": structured_all[world, slices["probe"]].astype(np.float32),
                "probe_ce_raw": ce_all[world, slices["probe"]].astype(np.float32),
                "probe_reference": block.probe.reference[world].astype(np.int8),
                "probe_structured_K3": probe.structured_state[world].astype(np.int8),
                "probe_ce_K3": probe.ce_state[world].astype(np.int8),
                "probe_center_only_K3": probe.center_state[world].astype(np.int8),
                "probe_unaccepted_shadow_K3": probe.shadow_state[world].astype(np.int8),
                "probe_unaccepted_production_K3": open_probe[world].astype(np.int8),
                "probe_self_confidence_K3": probe.self_confidence_state[world].astype(np.int8),
                "probe_support_margin": probe.support_margin[world].astype(np.float32),
                "probe_refutation_margin": probe.refutation_margin[world].astype(np.float32),
                "probe_support_relu": probe.support_relu[world].astype(np.float32),
                "probe_refutation_relu": probe.refutation_relu[world].astype(np.float32),
                "boundary_structured_raw": structured_all[world, slices["boundary"]].astype(np.float32),
                "boundary_ce_raw": ce_all[world, slices["boundary"]].astype(np.float32),
                "boundary_reference": block.boundary.reference[world].astype(np.int8),
                "boundary_structured_K3": boundary.structured_state[world].astype(np.int8),
                "boundary_ce_K3": boundary.ce_state[world].astype(np.int8),
                "boundary_center_only_K3": boundary.center_state[world].astype(np.int8),
                "boundary_unaccepted_shadow_K3": boundary.shadow_state[world].astype(np.int8),
                "boundary_self_confidence_K3": boundary.self_confidence_state[world].astype(np.int8),
                "boundary_support_margin": boundary.support_margin[world].astype(np.float32),
                "boundary_refutation_margin": boundary.refutation_margin[world].astype(np.float32),
                "boundary_support_relu": boundary.support_relu[world].astype(np.float32),
                "boundary_refutation_relu": boundary.refutation_relu[world].astype(np.float32),
                "transfer_structured_raw": structured_all[world, slices["transfer"]].astype(np.float32),
                "transfer_ce_raw": ce_all[world, slices["transfer"]].astype(np.float32),
                "transfer_reference": block.transfer.reference[world].astype(np.int8),
                "transfer_structured_K3": transfer.structured_state[world].astype(np.int8),
                "transfer_ce_K3": transfer.ce_state[world].astype(np.int8),
                "transfer_center_only_K3": transfer.center_state[world].astype(np.int8),
                "transfer_unaccepted_shadow_K3": transfer.shadow_state[world].astype(np.int8),
                "transfer_self_confidence_K3": transfer.self_confidence_state[world].astype(np.int8),
                "transfer_support_margin": transfer.support_margin[world].astype(np.float32),
                "transfer_refutation_margin": transfer.refutation_margin[world].astype(np.float32),
                "transfer_support_relu": transfer.support_relu[world].astype(np.float32),
                "transfer_refutation_relu": transfer.refutation_relu[world].astype(np.float32),
                "request_structured_raw": structured_all[world, slices["request"]].astype(np.float32),
                "request_ce_raw": ce_all[world, slices["request"]].astype(np.float32),
                "request_reference_outcome": block.request_reference_outcome[world].astype(np.int8),
                "request_structured_outcome": request_structured[world].astype(np.int8),
                "request_ce_outcome": request_ce[world].astype(np.int8),
                "request_structured_active_mask": (request_structured[world] == 3).astype(np.int8),
                "request_ce_active_mask": (request_ce[world] == 3).astype(np.int8),
                "request_structured_route": np.where(request_structured[world] == 3, block.request_plan[world], 3).astype(np.int8),
                "request_ce_route": np.where(request_ce[world] == 3, block.request_plan[world], 3).astype(np.int8),
                "request_center_only_outcome": request_center[world].astype(np.int8),
                "request_unaccepted_production_outcome": request_unaccepted[world].astype(np.int8),
                "request_self_confidence_outcome": request_self[world].astype(np.int8),
                "request_atom_structured_K3": request.structured_state[world].astype(np.int8),
                "request_atom_support_margin": request.support_margin[world].astype(np.float32),
                "request_atom_refutation_margin": request.refutation_margin[world].astype(np.float32),
                "request_atom_support_relu": request.support_relu[world].astype(np.float32),
                "request_atom_refutation_relu": request.refutation_relu[world].astype(np.float32),
            }
        )
    return BlockEvaluation(metrics, tuple(traces))


def assert_evaluation_equivalence(
    legacy_metrics: Mapping[str, Any],
    legacy_trace: Mapping[str, np.ndarray],
    repaired_metrics: Mapping[str, Any],
    repaired_trace: Mapping[str, np.ndarray],
) -> None:
    if set(legacy_metrics) | {"fit_seed"} != set(repaired_metrics):
        raise AssertionError("legacy and repaired metric schemas differ")
    for name, value in legacy_metrics.items():
        candidate = repaired_metrics[name]
        if isinstance(value, (int, np.integer)):
            if int(value) != int(candidate):
                raise AssertionError(f"metric {name} differs")
        elif not np.isclose(float(value), float(candidate), rtol=0.0, atol=2e-12):
            raise AssertionError(f"metric {name} differs: {value} != {candidate}")
    if set(legacy_trace) != set(repaired_trace):
        raise AssertionError("legacy and repaired trace schemas differ")
    for name, value in legacy_trace.items():
        candidate = repaired_trace[name]
        if value.dtype.kind in "iu":
            if not np.array_equal(value, candidate):
                raise AssertionError(f"trace {name} differs")
        elif not np.allclose(
            value,
            candidate,
            rtol=0.0,
            atol=FLOAT_TRACE_EQUIVALENCE_ATOL,
            equal_nan=True,
        ):
            maximum = float(np.max(np.abs(value.astype(np.float64) - candidate.astype(np.float64))))
            raise AssertionError(f"trace {name} differs; max_abs={maximum}")
