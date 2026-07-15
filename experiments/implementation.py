"""Frozen Task 20 adapter and exact neural-symbolic execution boundary.

The generator/oracle remains in :mod:`experiments.protocol`.  This module
constructs a closed, audited pre-outcome feature vector, hands only numeric
arrays to :mod:`experiments.learner`, and joins reference values only after a
prediction trace has been frozen.  Learned outputs are proposals; exact
well-formedness, evidence usability, polarity, ``K_3``, profile aggregation,
active masking, and fallback remain symbolic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import exp
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np

from experiments.learner import ReluMLP, WorldPanelData, predict
from experiments.protocol import (
    ALPHA_CAL,
    CELL_DESIGN_MASS,
    CELL_TARGET_MASS,
    MODE_POLARITY,
    ORACLE_VERSION,
    PROTOCOL_VERSION,
    AtomRecord,
    EvidenceMode,
    GeneratedWorld,
    Plan,
    Proposal,
    RequestAtom,
    RequestRecord,
    Role,
    Schema,
    TaintedValue,
    check_proposal_binding,
    decode_evidence,
    exact_active_set,
    f18_witness,
    generate_world,
    reference_binding_record,
    select_or_fallback,
    validate_scorer_payload,
)
from verification.kernel import AtomValue, Interval, Outcome
from verification.losses import derive_public_outcome, proposed_calibration_radius


NORMALIZATION_ID = "task20-fixed-units-v1"
SCHEMA_SCALE: Mapping[Schema, float] = {Schema.LOSS: 0.1, Schema.LATENCY: 10.0}
TRANSFER_OFFSETS = (-2.0, -1.5, 1.5, 2.0)
WIDTH_TRANSFERS = (0.5, 1.5)
BOUNDARY_CONDITIONS = (
    "near_support",
    "exact_boundary_support",
    "crossing_open",
    "near_refutation",
)

FEATURE_NAMES = (
    "x",
    "complexity",
    "difficulty",
    "stage_scaled",
    "threshold_scaled",
    "delta_scaled",
    "fallback_scaled",
    "well_formed",
    "evidence_present",
    "evidence_valid",
    "evidence_current",
    "checker_accepted",
    "can_support",
    "can_refute",
    "evidence_width_design",
    "plan_O",
    "plan_S",
    "plan_N",
    "plan_F",
    "schema_J",
    "schema_T",
    "mode_two_sided",
    "mode_upper_only",
    "mode_lower_only",
    "mode_empirical_only",
)

if len(FEATURE_NAMES) != 25:
    raise AssertionError("the frozen feature vector must have 25 coordinates")


def _mode_from_polarity(can_support: bool, can_refute: bool) -> EvidenceMode:
    pair = (can_support, can_refute)
    for mode, allowed in MODE_POLARITY.items():
        if allowed == pair:
            return mode
    raise ValueError(f"unregistered evidence polarity {pair!r}")


def _units(schema: Schema) -> str:
    return "loss" if schema is Schema.LOSS else "ms"


def _safe_payload(
    *,
    atom_address: str,
    schema: Schema,
    plan: Plan,
    x: float,
    complexity: float,
    difficulty: float,
    stage: int,
    threshold: float,
    delta: float,
    fallback: float,
    profile_slot: str,
    well_formed: bool,
    evidence_present: bool,
    evidence_valid: bool,
    evidence_current: bool,
    checker_accepted: bool,
    can_support: bool,
    can_refute: bool,
    evidence_width: float = 1.0,
) -> dict[str, Any]:
    mode = _mode_from_polarity(can_support, can_refute)
    threshold_field = "epsilon_a" if schema is Schema.LOSS else "epsilon_c"
    payload: dict[str, Any] = {
        "atom_address": atom_address,
        "plan_template": plan.value,
        "plan_features": ("declared-plan-role", plan.value),
        "x": x,
        "complexity": complexity,
        "difficulty": difficulty,
        "scope": "core-target-law",
        "stage_prefix": stage,
        "statistic_schema": schema.value,
        "units": _units(schema),
        "normalization_id": NORMALIZATION_ID,
        "evidence_mode": mode.value,
        "can_support": can_support,
        "can_refute": can_refute,
        "profile_slot": profile_slot,
        "profile_role": "required-atom" if profile_slot in {"A", "I", "C"} else "probe",
        threshold_field: TaintedValue(threshold, (threshold_field,), "unit-normalization"),
        "delta": delta,
        "fallback_threshold_inputs": fallback,
        "candidate_library_id": "candidate-registry-v1",
        "evaluated_set_id": "finite-core-set-v1",
        "evidence_design": evidence_width,
        "well_formed": well_formed,
        "missingness": not evidence_present,
        "validity": evidence_valid,
        "expiry": evidence_current,
        "checker_status": "accepted" if checker_accepted else "rejected",
    }
    validate_scorer_payload(payload)
    return payload


def _encode_payload(payload: Mapping[str, Any]) -> np.ndarray:
    schema = Schema(str(payload["statistic_schema"]))
    plan = Plan(str(payload["plan_template"]))
    mode = EvidenceMode(str(payload["evidence_mode"]))
    threshold_key = "epsilon_a" if schema is Schema.LOSS else "epsilon_c"
    threshold_value = payload[threshold_key]
    if isinstance(threshold_value, TaintedValue):
        threshold_value = threshold_value.value
    scale = SCHEMA_SCALE[schema]
    plan_order = (Plan.OLD, Plan.SUCCESSOR, Plan.NEW, Plan.FALLBACK)
    schema_order = (Schema.LOSS, Schema.LATENCY)
    mode_order = (
        EvidenceMode.TWO_SIDED,
        EvidenceMode.UPPER_ONLY,
        EvidenceMode.LOWER_ONLY,
        EvidenceMode.EMPIRICAL_ONLY,
    )
    values = (
        float(payload["x"]),
        float(payload["complexity"]),
        float(payload["difficulty"]),
        float(payload["stage_prefix"]) / 3.0,
        float(threshold_value) / scale,
        float(payload["delta"]) / SCHEMA_SCALE[Schema.LOSS],
        float(payload["fallback_threshold_inputs"]) / SCHEMA_SCALE[Schema.LOSS],
        float(bool(payload["well_formed"])),
        float(not bool(payload["missingness"])),
        float(bool(payload["validity"])),
        float(bool(payload["expiry"])),
        float(payload["checker_status"] == "accepted"),
        float(bool(payload["can_support"])),
        float(bool(payload["can_refute"])),
        float(payload["evidence_design"]),
        *(float(plan is item) for item in plan_order),
        *(float(schema is item) for item in schema_order),
        *(float(mode is item) for item in mode_order),
    )
    vector = np.asarray(values, dtype=np.float32)
    if vector.shape != (len(FEATURE_NAMES),) or not np.isfinite(vector).all():
        raise ValueError("feature encoding is incomplete or nonfinite")
    return vector


def probe_payload(
    probe: AtomRecord,
    *,
    threshold: float | None = None,
    evidence_width: float = 1.0,
) -> dict[str, Any]:
    return _safe_payload(
        atom_address=probe.atom_id,
        schema=probe.schema,
        plan=probe.plan,
        x=probe.x,
        complexity=probe.complexity,
        difficulty=probe.difficulty,
        stage=probe.stage,
        threshold=probe.threshold if threshold is None else threshold,
        delta=0.0,
        fallback=0.0,
        profile_slot="probe",
        well_formed=True,
        evidence_present=probe.evidence_present,
        evidence_valid=probe.evidence_valid,
        evidence_current=True,
        checker_accepted=True,
        can_support=probe.can_support,
        can_refute=probe.can_refute,
        evidence_width=evidence_width,
    )


def request_atom_payload(request: RequestRecord, atom: RequestAtom) -> dict[str, Any]:
    return _safe_payload(
        atom_address=f"{request.request_id}:{atom.name}",
        schema=atom.schema,
        plan=request.plan,
        x=request.x,
        complexity=request.complexity,
        difficulty=request.difficulty,
        stage=request.stage,
        threshold=atom.threshold,
        delta=request.delta if atom.name == "I" else 0.0,
        fallback=request.fallback_loss if atom.name == "I" else 0.0,
        profile_slot=atom.name,
        well_formed=request.well_formed,
        evidence_present=atom.evidence_present,
        evidence_valid=atom.evidence_valid,
        evidence_current=True,
        checker_accepted=True,
        can_support=atom.can_support,
        can_refute=atom.can_refute,
    )


def encode_probe(probe: AtomRecord, *, threshold: float | None = None) -> np.ndarray:
    return _encode_payload(probe_payload(probe, threshold=threshold))


def encode_request_atom(request: RequestRecord, atom: RequestAtom) -> np.ndarray:
    return _encode_payload(request_atom_payload(request, atom))


def world_panel(world: GeneratedWorld) -> WorldPanelData:
    if len(world.probes) != 80:
        raise ValueError("the frozen world does not contain 80 probes")
    features = np.stack([encode_probe(probe) for probe in world.probes])[None, :, :]
    targets = np.asarray(
        [
            np.nan if probe.learning_target is None else probe.learning_target / SCHEMA_SCALE[probe.schema]
            for probe in world.probes
        ],
        dtype=np.float32,
    )[None, :]
    schemas = np.asarray(
        [0 if probe.schema is Schema.LOSS else 1 for probe in world.probes], dtype=np.int8
    )[None, :]
    states = np.asarray([int(probe.value) for probe in world.probes], dtype=np.int8)[None, :]
    weights = np.asarray(
        [probe_target_weight(probe) for probe in world.probes],
        dtype=np.float32,
    )[None, :]
    return WorldPanelData(features, targets, schemas, states, weights)


def probe_target_weight(probe: AtomRecord) -> float:
    """Joint stratum/context target-to-design ratio for one atom probe."""

    return (
        probe.importance_weight
        * CELL_TARGET_MASS[probe.cell]
        / CELL_DESIGN_MASS[probe.cell]
    )


def request_target_weight(request: RequestRecord) -> float:
    """Joint public-outcome/context target-to-design ratio for a request."""

    return (
        request.importance_weight
        * CELL_TARGET_MASS[request.cell]
        / CELL_DESIGN_MASS[request.cell]
    )


def materialize_panel(
    role: Role,
    start: int,
    count: int,
    *,
    allow_final: bool = False,
) -> WorldPanelData:
    """Materialize a contiguous role block without retaining oracle objects."""

    if start < 0 or count <= 0:
        raise ValueError("panel range is invalid")
    feature_blocks: list[np.ndarray] = []
    target_blocks: list[np.ndarray] = []
    schema_blocks: list[np.ndarray] = []
    state_blocks: list[np.ndarray] = []
    weight_blocks: list[np.ndarray] = []
    for index in range(start, start + count):
        panel = world_panel(generate_world(role, index, allow_final=allow_final))
        feature_blocks.append(panel.features)
        target_blocks.append(panel.statistic_targets)
        schema_blocks.append(panel.schemas)
        state_blocks.append(panel.state_targets)
        weight_blocks.append(panel.weights)
    return WorldPanelData(
        np.concatenate(feature_blocks),
        np.concatenate(target_blocks),
        np.concatenate(schema_blocks),
        np.concatenate(state_blocks),
        np.concatenate(weight_blocks),
    )


@dataclass(frozen=True)
class CalibrationGroup:
    schema: Schema
    eta_normalized: float
    calibration_worlds: int
    score_count: int
    rank: int


@dataclass(frozen=True)
class CalibrationBundle:
    scorer_parameter_hash: str
    arm_variant: str
    training_manifest_hash: str
    calibration_manifest_hash: str
    groups: Mapping[Schema, CalibrationGroup]
    calibration_id: str


def calibrate_structured(
    model: ReluMLP,
    data: WorldPanelData,
    *,
    scorer_parameter_hash: str,
    training_manifest_hash: str,
    calibration_manifest_hash: str,
    center_only: bool = False,
) -> CalibrationBundle:
    raw = predict(model, data.features.reshape(-1, data.feature_count)).reshape(
        data.world_count, 80, -1
    )
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
        proposal = proposed_calibration_radius(tuple(float(value) for value in residuals), ALPHA_CAL)
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
                    schema.value: asdict(group) for schema, group in groups.items()
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


def binding_record(
    *,
    atom_address: str,
    schema: Schema,
    plan: Plan,
    scorer_parameter_hash: str,
    calibration: CalibrationBundle,
    can_support: bool,
    can_refute: bool,
    current_stage: int,
    checker_accepted: bool = True,
) -> dict[str, Any]:
    group = calibration.groups[schema]
    mode = _mode_from_polarity(can_support, can_refute)
    return reference_binding_record(
        record_id=f"binding:{atom_address}:{calibration.calibration_id}",
        atom_address=atom_address,
        statistic_schema=schema.value,
        target_constructor_version=ORACLE_VERSION,
        plan_template=plan.value,
        units=_units(schema),
        normalization_id=NORMALIZATION_ID,
        scorer_architecture_id="two-hidden-relu-single-vector-head-v1",
        scorer_parameter_hash=scorer_parameter_hash,
        learned_head_factorization_id="centerJ-radiusJ-centerT-radiusT-v1",
        training_manifest_hash=calibration.training_manifest_hash,
        calibration_procedure_id="pooled-additive-residual-expansion-v1",
        calibration_manifest_hash=calibration.calibration_manifest_hash,
        calibration_group=schema.value,
        eta_cal_or_infinity=group.eta_normalized * SCHEMA_SCALE[schema],
        calibration_count=group.calibration_worlds,
        certificate_mode=mode.value,
        can_support=can_support,
        can_refute=can_refute,
        valid_from_stage=0,
        valid_through_stage=3,
        checker_result="accepted" if checker_accepted else "rejected",
        provenance_root=f"calibration-provenance:{calibration.calibration_id}",
        created_stage=0,
    )


@dataclass(frozen=True)
class AtomDecision:
    atom_address: str
    arm: str
    value: AtomValue
    diagnostic: str
    region: Interval | None
    support_margin: float | None
    refutation_margin: float | None
    support_relu: float
    refutation_relu: float
    positive_surplus: float
    binding_accepted: bool
    binding_reasons: tuple[str, ...]
    shadow_value: AtomValue | None = None
    self_confidence: float | None = None
    production_active: bool = True


def _structured_coordinates(raw: Sequence[float], schema: Schema) -> tuple[float, float]:
    if len(raw) != 4:
        raise ValueError("structured head must emit four coordinates")
    scale = SCHEMA_SCALE[schema]
    if schema is Schema.LOSS:
        return float(raw[0]) * scale, max(0.0, float(raw[1])) * scale
    return float(raw[2]) * scale, max(0.0, float(raw[3])) * scale


def decode_structured(
    *,
    atom_address: str,
    schema: Schema,
    plan: Plan,
    stage: int,
    threshold: float,
    evidence_present: bool,
    evidence_valid: bool,
    can_support: bool,
    can_refute: bool,
    raw: Sequence[float],
    scorer_parameter_hash: str,
    calibration: CalibrationBundle,
    variant: str = "structured",
) -> AtomDecision:
    center, learned_radius = _structured_coordinates(raw, schema)
    group = calibration.groups[schema]
    if variant == "center_only":
        learned_radius = 0.0
    eta = group.eta_normalized * SCHEMA_SCALE[schema]
    accepted_path = variant in {"structured", "center_only"}
    total_radius = learned_radius + (eta if accepted_path else 0.0)
    region = Interval(center - total_radius, center + total_radius)
    record = binding_record(
        atom_address=atom_address,
        schema=schema,
        plan=plan,
        scorer_parameter_hash=scorer_parameter_hash,
        calibration=calibration,
        can_support=can_support,
        can_refute=can_refute,
        current_stage=stage,
        checker_accepted=accepted_path,
    )
    proposal = Proposal(
        region.lower,
        region.upper,
        scorer_parameter_hash,
        NORMALIZATION_ID,
        schema.value,
        plan.value,
        "core-target-law",
    )
    decision = check_proposal_binding(record, proposal, current_stage=stage)
    usable = decision.accepted and evidence_present and evidence_valid
    value = decode_evidence(
        region,
        threshold,
        evidence_present=usable,
        evidence_valid=usable,
        can_support=can_support,
        can_refute=can_refute,
    )
    support_margin = threshold - region.upper
    refutation_margin = region.lower - threshold
    scale = SCHEMA_SCALE[schema]
    support_relu = max(0.0, support_margin / scale)
    refutation_relu = max(0.0, refutation_margin / scale)
    surplus = support_relu if value is AtomValue.SUPPORTED else 0.0
    diagnostic = (
        "accepted_supported_region"
        if value is AtomValue.SUPPORTED
        else "accepted_refuting_region"
        if value is AtomValue.REFUTED
        else "binding_or_region_open"
    )
    shadow_value = None
    if variant == "unaccepted_radius":
        shadow_value = decode_evidence(
            region,
            threshold,
            evidence_present=evidence_present,
            evidence_valid=evidence_valid,
            can_support=can_support,
            can_refute=can_refute,
        )
        value = AtomValue.OPEN
        diagnostic = "unaccepted_uncertainty_proposal"
    return AtomDecision(
        atom_address,
        variant,
        value,
        diagnostic,
        region,
        support_margin,
        refutation_margin,
        support_relu,
        refutation_relu,
        surplus,
        decision.accepted,
        decision.reasons,
        shadow_value,
        None,
        accepted_path,
    )


def _softmax(logits: Sequence[float]) -> tuple[float, ...]:
    maximum = max(float(value) for value in logits)
    values = [exp(float(value) - maximum) for value in logits]
    total = sum(values)
    return tuple(value / total for value in values)


def decode_cross_entropy(
    *,
    atom_address: str,
    logits: Sequence[float],
    evidence_present: bool,
    evidence_valid: bool,
    can_support: bool,
    can_refute: bool,
) -> AtomDecision:
    if len(logits) != 3:
        raise ValueError("CE arm must emit exactly three K3 logits")
    probabilities = _softmax(logits)
    predicted = AtomValue(int(np.argmax(np.asarray(logits))))
    diagnostic = "direct_ce_prediction"
    if not evidence_present:
        predicted = AtomValue.OPEN
        diagnostic = "missing_evidence_exact_override"
    elif not evidence_valid:
        predicted = AtomValue.OPEN
        diagnostic = "invalid_evidence_exact_override"
    elif predicted is AtomValue.SUPPORTED and not can_support:
        predicted = AtomValue.OPEN
        diagnostic = "support_polarity_exact_override"
    elif predicted is AtomValue.REFUTED and not can_refute:
        predicted = AtomValue.OPEN
        diagnostic = "refutation_polarity_exact_override"
    return AtomDecision(
        atom_address,
        "cross_entropy",
        predicted,
        diagnostic,
        None,
        None,
        None,
        0.0,
        0.0,
        0.0,
        True,
        (),
        None,
        max(probabilities),
        True,
    )


def self_confidence_ablation(atom_address: str, logits: Sequence[float]) -> AtomDecision:
    probabilities = _softmax(logits)
    confidence = max(probabilities)
    value = AtomValue.SUPPORTED if confidence >= 0.5 else AtomValue.OPEN
    return AtomDecision(
        atom_address,
        "self_confidence_invalid",
        value,
        "invalid_self_confidence_as_authorization",
        None,
        None,
        None,
        0.0,
        0.0,
        0.0,
        False,
        ("self_confidence_is_not_external_evidence",),
        None,
        confidence,
        False,
    )


@dataclass(frozen=True)
class RequestDecision:
    request_id: str
    well_formed: bool
    atoms: Mapping[str, AtomDecision]
    outcome: Outcome
    active_mask: int


def decode_request(
    request: RequestRecord,
    decisions: Iterable[AtomDecision],
) -> RequestDecision:
    indexed = {decision.atom_address.rsplit(":", 1)[-1]: decision for decision in decisions}
    if set(indexed) != {"A", "I", "C"}:
        raise ValueError("request diagnostics must be indexed by exactly A, I, and C")
    outcome = derive_public_outcome(
        well_formed=request.well_formed,
        required_atom_values=(indexed[name].value for name in ("A", "I", "C")),
    )
    return RequestDecision(
        request.request_id,
        request.well_formed,
        indexed,
        outcome,
        int(outcome is Outcome.GRANTED),
    )


@dataclass(frozen=True)
class RouteDecision:
    selected: Plan
    active: tuple[Plan, ...]
    mask: Mapping[Plan, int]
    inactive_selection_probability: float
    used_fallback: bool


def route_with_exact_mask(
    outcomes: Mapping[Plan, Outcome],
    scores: Mapping[Plan, float],
) -> RouteDecision:
    active = exact_active_set(outcomes)
    selected = select_or_fallback(outcomes, scores)
    if selected is not Plan.FALLBACK and selected not in active:
        raise AssertionError("an inactive score reactivated a plan")
    mask = {plan: int(plan in active) for plan in (Plan.OLD, Plan.SUCCESSOR, Plan.NEW)}
    return RouteDecision(selected, active, mask, 0.0, selected is Plan.FALLBACK)


@dataclass(frozen=True)
class TransferCase:
    atom_address: str
    offset: float
    feature: np.ndarray
    threshold: float
    reference: AtomValue


@dataclass(frozen=True)
class BoundaryCase:
    atom_address: str
    condition: str
    feature: np.ndarray
    threshold: float
    reference: AtomValue


def tolerance_transfer_cases(probe: AtomRecord) -> tuple[TransferCase, ...]:
    cases = []
    for offset in TRANSFER_OFFSETS:
        threshold = probe.threshold + offset * probe.oracle_scale
        reference = decode_evidence(
            probe.reference_region,
            threshold,
            evidence_present=probe.evidence_present,
            evidence_valid=probe.evidence_valid,
            can_support=probe.can_support,
            can_refute=probe.can_refute,
        )
        cases.append(
            TransferCase(
                f"{probe.atom_id}:transfer:{offset:+.1f}",
                offset,
                encode_probe(probe, threshold=threshold),
                threshold,
                reference,
            )
        )
    return tuple(cases)


def boundary_status_cases(probe: AtomRecord) -> tuple[BoundaryCase, ...]:
    """Construct the four registered near-boundary cells before scoring.

    The ordinary random strict strata have probability zero of landing at the
    exact ``.25`` cutoff.  The endpoint therefore uses this deterministic
    query panel over the same world/plan/statistic law.  All four records are
    present, valid, and two-sided so the condition—not missingness or
    polarity—determines the reference state.
    """

    lower = probe.reference_region.lower
    upper = probe.reference_region.upper
    scale = probe.oracle_scale
    thresholds = (
        upper + 0.25 * scale,
        upper,
        (lower + upper) / 2.0,
        lower - 0.25 * scale,
    )
    references = (
        AtomValue.SUPPORTED,
        AtomValue.SUPPORTED,
        AtomValue.OPEN,
        AtomValue.REFUTED,
    )
    cases: list[BoundaryCase] = []
    for condition, threshold, reference in zip(
        BOUNDARY_CONDITIONS, thresholds, references
    ):
        payload = _safe_payload(
            atom_address=f"{probe.atom_id}:boundary:{condition}",
            schema=probe.schema,
            plan=probe.plan,
            x=probe.x,
            complexity=probe.complexity,
            difficulty=probe.difficulty,
            stage=probe.stage,
            threshold=threshold,
            delta=0.0,
            fallback=0.0,
            profile_slot="probe",
            well_formed=True,
            evidence_present=True,
            evidence_valid=True,
            evidence_current=True,
            checker_accepted=True,
            can_support=True,
            can_refute=True,
        )
        computed = decode_evidence(
            probe.reference_region,
            threshold,
            evidence_present=True,
            evidence_valid=True,
            can_support=True,
            can_refute=True,
        )
        if computed is not reference:
            raise AssertionError("boundary query constructor has the wrong K3 state")
        cases.append(
            BoundaryCase(
                str(payload["atom_address"]),
                condition,
                _encode_payload(payload),
                threshold,
                reference,
            )
        )
    return tuple(cases)


def width_transfer_reference(probe: AtomRecord, multiplier: float) -> tuple[Interval, AtomValue]:
    if multiplier not in WIDTH_TRANSFERS:
        raise ValueError("width transfer multiplier is not frozen")
    center = (probe.reference_region.lower + probe.reference_region.upper) / 2.0
    half_width = (probe.reference_region.upper - probe.reference_region.lower) * multiplier / 2.0
    region = Interval(center - half_width, center + half_width)
    return region, decode_evidence(
        region,
        probe.threshold,
        evidence_present=probe.evidence_present,
        evidence_valid=probe.evidence_valid,
        can_support=probe.can_support,
        can_refute=probe.can_refute,
    )


def frozen_prediction_trace(
    *,
    world: GeneratedWorld,
    atom_address: str,
    role: Role,
    allowed_payload: Mapping[str, Any],
    arm: str,
    fit_seed: int,
    parameter_hash: str,
    raw_output: Sequence[float],
    decision: AtomDecision,
    manifest_hashes: Mapping[str, str],
    request_context: Mapping[str, Any],
    router: RouteDecision | None = None,
) -> dict[str, Any]:
    validate_scorer_payload(allowed_payload)
    trace = {
        "protocol_and_manifest_hashes": {
            "protocol_version": PROTOCOL_VERSION,
            **dict(manifest_hashes),
        },
        "lineage": {
            "world_root": world.identity.world_root,
            "trajectory_root": world.identity.trajectory_root,
            "provenance_root": world.identity.provenance_root,
            "plan_family_root": world.identity.plan_family_root,
            "role": role.value,
        },
        "allowed_input_field_names_and_firewall_result": {
            "fields": sorted(allowed_payload),
            "result": "pass",
            "feature_names": FEATURE_NAMES,
        },
        "request_profile_units_thresholds_scope_stage_event_prefix": dict(request_context),
        "arm_parameter_hash_factorization_fit_seed_capacity_compute": {
            "arm": arm,
            "fit_seed": fit_seed,
            "parameter_hash": parameter_hash,
            "factorization": (
                "centerJ-radiusJ-centerT-radiusT"
                if arm.startswith("structured")
                else "three-K3-logits"
            ),
        },
        "raw_center_radius_or_logits": [float(value) for value in raw_output],
        "binding_checker_polarity_validity": {
            "accepted": decision.binding_accepted,
            "reasons": decision.binding_reasons,
            "diagnostic": decision.diagnostic,
        },
        "signed_margins_paired_relu_K3_WF_public_outcome_active_mask": {
            "support_margin": decision.support_margin,
            "refutation_margin": decision.refutation_margin,
            "support_relu": decision.support_relu,
            "refutation_relu": decision.refutation_relu,
            "positive_surplus": decision.positive_surplus,
            "K3": decision.value.name,
            "production_active": decision.production_active,
        },
        "router_fallback_and_dependency_footprint": (
            None
            if router is None
            else {
                "selected": router.selected.value,
                "active": [plan.value for plan in router.active],
                "mask": {plan.value: value for plan, value in router.mask.items()},
                "fallback": router.used_fallback,
            }
        ),
        "access_control_separated_oracle_namespace": {
            "joined": False,
            "prediction_hash_frozen_before_join": True,
        },
        "target_design_weights_stratum_metric_contribution_failure_flags": None,
        "atom_address": atom_address,
    }
    json.dumps(trace, sort_keys=True)
    return trace


def prediction_hash(trace: Mapping[str, Any]) -> str:
    if trace["access_control_separated_oracle_namespace"]["joined"]:
        raise ValueError("prediction hash must be frozen before evaluation join")
    return sha256(json.dumps(trace, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def join_evaluation_namespace(
    trace: Mapping[str, Any],
    *,
    reference: AtomValue,
    target_weight: float,
    design_weight: float,
    stratum: str,
) -> dict[str, Any]:
    frozen_hash = prediction_hash(trace)
    joined = json.loads(json.dumps(trace))
    joined["access_control_separated_oracle_namespace"] = {
        "joined": True,
        "prediction_hash": frozen_hash,
    }
    predicted = AtomValue[joined["signed_margins_paired_relu_K3_WF_public_outcome_active_mask"]["K3"]]
    joined["target_design_weights_stratum_metric_contribution_failure_flags"] = {
        "evaluation_namespace": {
            "reference_K3": reference.name,
            "target_weight": target_weight,
            "design_weight": design_weight,
            "stratum": stratum,
            "correct": predicted is reference,
            "false_support": predicted is AtomValue.SUPPORTED and reference is not AtomValue.SUPPORTED,
            "false_refutation": predicted is AtomValue.REFUTED and reference is not AtomValue.REFUTED,
        }
    }
    return joined


def write_trace_jsonl(path: Path, traces: Iterable[Mapping[str, Any]]) -> str:
    """Write replayable full-precision traces and return their SHA-256 hash."""

    digest = sha256()
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for trace in traces:
            line = json.dumps(trace, sort_keys=True, separators=(",", ":")) + "\n"
            handle.write(line)
            digest.update(line.encode("utf-8"))
    return digest.hexdigest()


def f18_implementation_witness() -> Mapping[str, Any]:
    witness = dict(f18_witness())
    outcomes = {
        Plan.OLD: Outcome.GRANTED,
        Plan.SUCCESSOR: Outcome.WITHHELD,
        Plan.NEW: Outcome.REFUSED,
    }
    # The inactive successor receives an arbitrarily high raw score and still
    # cannot beat the sole exact license.
    route = route_with_exact_mask(
        outcomes,
        {Plan.OLD: 1.0, Plan.SUCCESSOR: 1_000_000.0, Plan.NEW: 2.0},
    )
    empty = route_with_exact_mask(
        {Plan.OLD: Outcome.WITHHELD, Plan.SUCCESSOR: Outcome.REFUSED},
        {Plan.OLD: 10.0, Plan.SUCCESSOR: 20.0},
    )
    witness.update(
        {
            "selected_with_inactive_high_score": route.selected.value,
            "inactive_selection_probability": route.inactive_selection_probability,
            "empty_selected": empty.selected.value,
            "positive_means": "positive preactivation or named margin only; never grant by itself",
            "zero_means": "no unique logical state",
        }
    )
    return witness


def implementation_preflight(protocol_path: Path, manifests_path: Path) -> Mapping[str, Any]:
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    manifests = json.loads(manifests_path.read_text(encoding="utf-8"))
    if protocol["protocol_version"] != PROTOCOL_VERSION:
        raise ValueError("implementation/protocol version mismatch")
    final = protocol["roles"][Role.FINAL_CONFIRMATION.value]
    if final["payloads_generated"] or not final["embargoed"]:
        raise ValueError("final-confirmation embargo is not intact")
    if protocol["optional_extensions"]["hard_moe"]["decision"] != "omit_prospectively":
        raise ValueError("Task 20 must not reactivate hard MoE")
    witness = f18_implementation_witness()
    if witness["selected_with_inactive_high_score"] != Plan.OLD.value:
        raise AssertionError("F18 exact mask witness failed")
    if witness["empty_selected"] != Plan.FALLBACK.value:
        raise AssertionError("empty active set did not use fallback")
    return {
        "status": "pass",
        "protocol_version": PROTOCOL_VERSION,
        "feature_count": len(FEATURE_NAMES),
        "manifest_roles": len(manifests["manifests"]),
        "final_payloads_generated": False,
        "hard_moe": "omitted",
        "F18": witness,
    }
