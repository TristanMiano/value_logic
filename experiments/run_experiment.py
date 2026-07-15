"""Single frozen entry point for Task 20 preflight and Task 21 execution.

Task 20 uses the default ``--preflight`` and ``--smoke`` paths, which never
materialize production roles.  The final path requires the literal Task 21
authorization token and generates confirmation worlds only after model
selection, eight paired fits, calibration, model serialization, and a
completion marker have all succeeded.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys
import time
from typing import Any, Mapping, Sequence

import numpy as np

from experiments.implementation import (
    BOUNDARY_CONDITIONS,
    FEATURE_NAMES,
    TRANSFER_OFFSETS,
    CalibrationBundle,
    boundary_status_cases,
    calibrate_structured,
    decode_cross_entropy,
    decode_request,
    decode_structured,
    encode_probe,
    encode_request_atom,
    implementation_preflight,
    materialize_panel,
    probe_target_weight,
    request_target_weight,
    self_confidence_ablation,
    tolerance_transfer_cases,
)
from experiments.learner import (
    FitConfig,
    FitSummary,
    JointSelection,
    ReluMLP,
    TrialScore,
    WorldPanelData,
    choose_joint_capacity,
    fit_cross_entropy,
    fit_structured,
    frozen_grid,
    matched_architectures,
    predict,
    state_dict_arrays,
)
from experiments.protocol import (
    FIT_SEEDS,
    Plan,
    Role,
    Schema,
    generate_world,
)
from experiments.system_witness import deterministic_system_witness
from verification.kernel import AtomValue, Outcome


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "experiments" / "protocol_v1.json"
MANIFESTS_PATH = ROOT / "experiments" / "manifests_v1.json"
IMPLEMENTATION_PATH = ROOT / "experiments" / "implementation_v1.json"
RESULTS_PATH = ROOT / "experiments" / "raw_results_v1.json"
MODELS_PATH = ROOT / "experiments" / "model_states_v1.npz"
TRACE_DIRECTORY = ROOT / "experiments" / "trace_shards_v1"
FIT_MARKER_PATH = ROOT / "experiments" / "fit_complete_v1.json"
TASK21_TOKEN = "RUN-VALUE-LOGIC-FINAL-V1"


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _json(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _subpanel(data: WorldPanelData, start: int, stop: int) -> WorldPanelData:
    return WorldPanelData(
        data.features[start:stop],
        data.statistic_targets[start:stop],
        data.schemas[start:stop],
        data.state_targets[start:stop],
        data.weights[start:stop],
    )


def _summary(summary: FitSummary) -> Mapping[str, Any]:
    return {
        "arm": summary.arm,
        "seed": summary.seed,
        "architecture": asdict(summary.architecture),
        "config": asdict(summary.config),
        "phases": [asdict(phase) for phase in summary.phases],
        "parameter_hash": summary.parameter_hash,
        "wall_seconds": summary.wall_seconds,
    }


def _selection(selection: JointSelection) -> Mapping[str, Any]:
    return {
        "parameter_budget": selection.parameter_budget,
        "normalized_joint_regret": selection.normalized_joint_regret,
        "structured": {
            "config": asdict(selection.structured.config),
            "validation_loss": selection.structured.validation_loss,
        },
        "cross_entropy": {
            "config": asdict(selection.cross_entropy.config),
            "validation_loss": selection.cross_entropy.validation_loss,
        },
    }


def verify_frozen_sources() -> Mapping[str, Any]:
    contract = _json(IMPLEMENTATION_PATH)
    expected = contract["source_sha256"]
    observed = {
        "learner.py": _sha256(ROOT / "experiments" / "learner.py"),
        "implementation.py": _sha256(ROOT / "experiments" / "implementation.py"),
        "system_witness.py": _sha256(ROOT / "experiments" / "system_witness.py"),
        "run_experiment.py": _sha256(ROOT / "experiments" / "run_experiment.py"),
    }
    mismatches = {
        name: {"expected": expected[name], "observed": value}
        for name, value in observed.items()
        if expected.get(name) != value
    }
    if mismatches:
        raise RuntimeError(f"frozen implementation source drift: {mismatches}")
    if contract["protocol_sha256"] != _sha256(PROTOCOL_PATH):
        raise RuntimeError("frozen protocol hash drift")
    if contract["manifests_sha256"] != _sha256(MANIFESTS_PATH):
        raise RuntimeError("frozen manifest hash drift")
    return contract


def run_preflight() -> Mapping[str, Any]:
    contract = verify_frozen_sources()
    result = dict(implementation_preflight(PROTOCOL_PATH, MANIFESTS_PATH))
    result.update(
        {
            "implementation_version": contract["implementation_version"],
            "source_hashes_verified": True,
            "system_witness": deterministic_system_witness(),
        }
    )
    return result


def run_smoke() -> Mapping[str, Any]:
    """Pilot-role neural smoke test; no result is an empirical endpoint."""

    run_preflight()
    panel = materialize_panel(Role.PILOT, 0, 16)
    train = _subpanel(panel, 0, 12)
    selection = _subpanel(panel, 12, 16)
    structured_spec, ce_spec = matched_architectures(len(FEATURE_NAMES), 12000)
    config = FitConfig(
        0.001,
        0.0,
        12000,
        batch_worlds=8,
        max_epochs=4,
        patience_epochs=2,
        validation_cadence=1,
        center_epochs=2,
        radius_epochs=2,
    )
    structured, structured_summary = fit_structured(
        train, selection, structured_spec, config, FIT_SEEDS[0]
    )
    ce, ce_summary = fit_cross_entropy(train, selection, ce_spec, config, FIT_SEEDS[0])
    structured_repeat, repeat_summary = fit_structured(
        train, selection, structured_spec, config, FIT_SEEDS[0]
    )
    deterministic = (
        structured_summary.parameter_hash == repeat_summary.parameter_hash
        and np.array_equal(
            predict(structured, selection.features.reshape(-1, len(FEATURE_NAMES))),
            predict(structured_repeat, selection.features.reshape(-1, len(FEATURE_NAMES))),
        )
    )
    if not deterministic:
        raise AssertionError("paired smoke fit is not exactly reproducible")
    return {
        "status": "pass",
        "evidence_grade": "pilot_role_implementation_smoke_only",
        "worlds": 16,
        "production_payloads_generated": False,
        "final_payloads_generated": False,
        "structured": _summary(structured_summary),
        "cross_entropy": _summary(ce_summary),
        "deterministic_repeat": deterministic,
    }


def _fit_grid(
    fit_data: WorldPanelData,
    selection_data: WorldPanelData,
    protocol: Mapping[str, Any],
) -> tuple[JointSelection, list[Mapping[str, Any]]]:
    optimization = protocol["optimization"]
    configs = frozen_grid(
        optimization["learning_rate_grid"],
        optimization["weight_decay_grid"],
        optimization["parameter_budget_grid"],
    )
    scores: list[TrialScore] = []
    records: list[Mapping[str, Any]] = []
    selection_seed = FIT_SEEDS[0]
    for config in configs:
        structured_spec, ce_spec = matched_architectures(
            len(FEATURE_NAMES), config.parameter_budget
        )
        _, structured_summary = fit_structured(
            fit_data, selection_data, structured_spec, config, selection_seed
        )
        _, ce_summary = fit_cross_entropy(
            fit_data, selection_data, ce_spec, config, selection_seed
        )
        scores.extend(
            (
                TrialScore("structured", config, structured_summary.selection_loss),
                TrialScore("cross_entropy", config, ce_summary.selection_loss),
            )
        )
        records.append(
            {
                "config": asdict(config),
                "structured": _summary(structured_summary),
                "cross_entropy": _summary(ce_summary),
            }
        )
    return choose_joint_capacity(scores), records


def _save_models(
    structured: Sequence[ReluMLP],
    ce: Sequence[ReluMLP],
    summaries: Sequence[tuple[FitSummary, FitSummary]],
) -> str:
    arrays: dict[str, np.ndarray] = {}
    for seed, structured_model, ce_model in zip(FIT_SEEDS, structured, ce):
        for name, value in state_dict_arrays(structured_model).items():
            arrays[f"structured_{seed}_{name}"] = value
        for name, value in state_dict_arrays(ce_model).items():
            arrays[f"cross_entropy_{seed}_{name}"] = value
    np.savez_compressed(MODELS_PATH, **arrays)
    return _sha256(MODELS_PATH)


def _fit_final_models(
    fit_data: WorldPanelData,
    selection_data: WorldPanelData,
    selection: JointSelection,
) -> tuple[list[ReluMLP], list[ReluMLP], list[tuple[FitSummary, FitSummary]]]:
    structured_models: list[ReluMLP] = []
    ce_models: list[ReluMLP] = []
    summaries: list[tuple[FitSummary, FitSummary]] = []
    structured_spec, ce_spec = matched_architectures(
        len(FEATURE_NAMES), selection.parameter_budget
    )
    for seed in FIT_SEEDS:
        structured_model, structured_summary = fit_structured(
            fit_data,
            selection_data,
            structured_spec,
            selection.structured.config,
            seed,
        )
        ce_model, ce_summary = fit_cross_entropy(
            fit_data,
            selection_data,
            ce_spec,
            selection.cross_entropy.config,
            seed,
        )
        structured_models.append(structured_model)
        ce_models.append(ce_model)
        summaries.append((structured_summary, ce_summary))
    return structured_models, ce_models, summaries


def _macro_accuracy(
    references: Sequence[AtomValue],
    predictions: Sequence[AtomValue],
    groups: Sequence[tuple[Any, ...]],
    weights: Sequence[float],
) -> float:
    grouped: dict[tuple[Any, ...], list[tuple[bool, float]]] = {}
    for reference, prediction, group, weight in zip(references, predictions, groups, weights):
        grouped.setdefault(group, []).append((prediction is reference, float(weight)))
    if not grouped:
        raise ValueError("macro accuracy has no groups")
    cell_scores = []
    for records in grouped.values():
        total = sum(weight for _, weight in records)
        cell_scores.append(sum(float(correct) * weight for correct, weight in records) / total)
    return sum(cell_scores) / len(cell_scores)


def _evaluate_one_world_seed(
    world_index: int,
    structured_model: ReluMLP,
    ce_model: ReluMLP,
    structured_hash: str,
    calibration: CalibrationBundle,
    center_calibration: CalibrationBundle,
    *,
    role: Role = Role.FINAL_CONFIRMATION,
    allow_final: bool = False,
) -> tuple[Mapping[str, Any], Mapping[str, np.ndarray]]:
    world = generate_world(role, world_index, allow_final=allow_final)
    # The adapter, not the learner, sees generator records.
    probe_features = np.stack([encode_probe(probe) for probe in world.probes])
    structured_raw = predict(structured_model, probe_features)
    ce_raw = predict(ce_model, probe_features)
    structured_values: list[AtomValue] = []
    ce_values: list[AtomValue] = []
    center_values: list[AtomValue] = []
    unaccepted_shadow_values: list[AtomValue] = []
    unaccepted_production_values: list[AtomValue] = []
    self_confidence_values: list[AtomValue] = []
    support_margins: list[float] = []
    refutation_margins: list[float] = []
    support_relus: list[float] = []
    refutation_relus: list[float] = []
    coverage = {Schema.LOSS: [], Schema.LATENCY: []}
    references = [probe.value for probe in world.probes]
    weights = [probe_target_weight(probe) for probe in world.probes]
    in_groups = [(probe.schema.value, probe.value.name) for probe in world.probes]
    for probe, raw_s, raw_c in zip(world.probes, structured_raw, ce_raw):
        structured = decode_structured(
            atom_address=probe.atom_id,
            schema=probe.schema,
            plan=probe.plan,
            stage=probe.stage,
            threshold=probe.threshold,
            evidence_present=probe.evidence_present,
            evidence_valid=probe.evidence_valid,
            can_support=probe.can_support,
            can_refute=probe.can_refute,
            raw=raw_s,
            scorer_parameter_hash=structured_hash,
            calibration=calibration,
        )
        ce = decode_cross_entropy(
            atom_address=probe.atom_id,
            logits=raw_c,
            evidence_present=probe.evidence_present,
            evidence_valid=probe.evidence_valid,
            can_support=probe.can_support,
            can_refute=probe.can_refute,
        )
        center = decode_structured(
            atom_address=probe.atom_id,
            schema=probe.schema,
            plan=probe.plan,
            stage=probe.stage,
            threshold=probe.threshold,
            evidence_present=probe.evidence_present,
            evidence_valid=probe.evidence_valid,
            can_support=probe.can_support,
            can_refute=probe.can_refute,
            raw=raw_s,
            scorer_parameter_hash=structured_hash,
            calibration=center_calibration,
            variant="center_only",
        )
        unaccepted = decode_structured(
            atom_address=probe.atom_id,
            schema=probe.schema,
            plan=probe.plan,
            stage=probe.stage,
            threshold=probe.threshold,
            evidence_present=probe.evidence_present,
            evidence_valid=probe.evidence_valid,
            can_support=probe.can_support,
            can_refute=probe.can_refute,
            raw=raw_s,
            scorer_parameter_hash=structured_hash,
            calibration=calibration,
            variant="unaccepted_radius",
        )
        self_confidence = self_confidence_ablation(probe.atom_id, raw_c)
        structured_values.append(structured.value)
        ce_values.append(ce.value)
        center_values.append(center.value)
        unaccepted_shadow_values.append(
            unaccepted.shadow_value
            if unaccepted.shadow_value is not None
            else AtomValue.OPEN
        )
        unaccepted_production_values.append(unaccepted.value)
        self_confidence_values.append(self_confidence.value)
        support_margins.append(float(structured.support_margin))
        refutation_margins.append(float(structured.refutation_margin))
        support_relus.append(structured.support_relu)
        refutation_relus.append(structured.refutation_relu)
        if probe.learning_target is not None and structured.region is not None:
            coverage[probe.schema].append(structured.region.contains(probe.oracle_target))

    boundary_cases = [case for probe in world.probes for case in boundary_status_cases(probe)]
    boundary_features = np.stack([case.feature for case in boundary_cases])
    boundary_s_raw = predict(structured_model, boundary_features)
    boundary_c_raw = predict(ce_model, boundary_features)
    boundary_s_values: list[AtomValue] = []
    boundary_c_values: list[AtomValue] = []
    boundary_center_values: list[AtomValue] = []
    boundary_shadow_values: list[AtomValue] = []
    boundary_confidence_values: list[AtomValue] = []
    boundary_support_margins: list[float] = []
    boundary_refutation_margins: list[float] = []
    boundary_support_relus: list[float] = []
    boundary_refutation_relus: list[float] = []
    boundary_refs = [case.reference for case in boundary_cases]
    boundary_groups = []
    for case, probe, raw_s, raw_c in zip(
        boundary_cases,
        (probe for probe in world.probes for _ in BOUNDARY_CONDITIONS),
        boundary_s_raw,
        boundary_c_raw,
    ):
        boundary_structured = decode_structured(
            atom_address=case.atom_address,
            schema=probe.schema,
            plan=probe.plan,
            stage=probe.stage,
            threshold=case.threshold,
            evidence_present=True,
            evidence_valid=True,
            can_support=True,
            can_refute=True,
            raw=raw_s,
            scorer_parameter_hash=structured_hash,
            calibration=calibration,
        )
        boundary_s_values.append(boundary_structured.value)
        boundary_support_margins.append(float(boundary_structured.support_margin))
        boundary_refutation_margins.append(float(boundary_structured.refutation_margin))
        boundary_support_relus.append(boundary_structured.support_relu)
        boundary_refutation_relus.append(boundary_structured.refutation_relu)
        boundary_c_values.append(
            decode_cross_entropy(
                atom_address=case.atom_address,
                logits=raw_c,
                evidence_present=True,
                evidence_valid=True,
                can_support=True,
                can_refute=True,
            ).value
        )
        boundary_center_values.append(
            decode_structured(
                atom_address=case.atom_address,
                schema=probe.schema,
                plan=probe.plan,
                stage=probe.stage,
                threshold=case.threshold,
                evidence_present=True,
                evidence_valid=True,
                can_support=True,
                can_refute=True,
                raw=raw_s,
                scorer_parameter_hash=structured_hash,
                calibration=center_calibration,
                variant="center_only",
            ).value
        )
        shadow = decode_structured(
            atom_address=case.atom_address,
            schema=probe.schema,
            plan=probe.plan,
            stage=probe.stage,
            threshold=case.threshold,
            evidence_present=True,
            evidence_valid=True,
            can_support=True,
            can_refute=True,
            raw=raw_s,
            scorer_parameter_hash=structured_hash,
            calibration=calibration,
            variant="unaccepted_radius",
        )
        boundary_shadow_values.append(
            shadow.shadow_value if shadow.shadow_value is not None else AtomValue.OPEN
        )
        boundary_confidence_values.append(
            self_confidence_ablation(case.atom_address, raw_c).value
        )
        boundary_groups.append((probe.schema.value, case.condition))

    transfer_cases = [case for probe in world.probes for case in tolerance_transfer_cases(probe)]
    transfer_features = np.stack([case.feature for case in transfer_cases])
    transfer_s_raw = predict(structured_model, transfer_features)
    transfer_c_raw = predict(ce_model, transfer_features)
    transfer_s_values: list[AtomValue] = []
    transfer_c_values: list[AtomValue] = []
    transfer_center_values: list[AtomValue] = []
    transfer_shadow_values: list[AtomValue] = []
    transfer_confidence_values: list[AtomValue] = []
    transfer_support_margins: list[float] = []
    transfer_refutation_margins: list[float] = []
    transfer_support_relus: list[float] = []
    transfer_refutation_relus: list[float] = []
    transfer_refs = [case.reference for case in transfer_cases]
    transfer_groups = []
    transfer_weights = []
    for case, probe, raw_s, raw_c in zip(
        transfer_cases,
        (probe for probe in world.probes for _ in TRANSFER_OFFSETS),
        transfer_s_raw,
        transfer_c_raw,
    ):
        transfer_structured = decode_structured(
            atom_address=case.atom_address,
            schema=probe.schema,
            plan=probe.plan,
            stage=probe.stage,
            threshold=case.threshold,
            evidence_present=probe.evidence_present,
            evidence_valid=probe.evidence_valid,
            can_support=probe.can_support,
            can_refute=probe.can_refute,
            raw=raw_s,
            scorer_parameter_hash=structured_hash,
            calibration=calibration,
        )
        transfer_s_values.append(transfer_structured.value)
        transfer_support_margins.append(float(transfer_structured.support_margin))
        transfer_refutation_margins.append(float(transfer_structured.refutation_margin))
        transfer_support_relus.append(transfer_structured.support_relu)
        transfer_refutation_relus.append(transfer_structured.refutation_relu)
        transfer_c_values.append(
            decode_cross_entropy(
                atom_address=case.atom_address,
                logits=raw_c,
                evidence_present=probe.evidence_present,
                evidence_valid=probe.evidence_valid,
                can_support=probe.can_support,
                can_refute=probe.can_refute,
            ).value
        )
        transfer_center_values.append(
            decode_structured(
                atom_address=case.atom_address,
                schema=probe.schema,
                plan=probe.plan,
                stage=probe.stage,
                threshold=case.threshold,
                evidence_present=probe.evidence_present,
                evidence_valid=probe.evidence_valid,
                can_support=probe.can_support,
                can_refute=probe.can_refute,
                raw=raw_s,
                scorer_parameter_hash=structured_hash,
                calibration=center_calibration,
                variant="center_only",
            ).value
        )
        shadow = decode_structured(
            atom_address=case.atom_address,
            schema=probe.schema,
            plan=probe.plan,
            stage=probe.stage,
            threshold=case.threshold,
            evidence_present=probe.evidence_present,
            evidence_valid=probe.evidence_valid,
            can_support=probe.can_support,
            can_refute=probe.can_refute,
            raw=raw_s,
            scorer_parameter_hash=structured_hash,
            calibration=calibration,
            variant="unaccepted_radius",
        )
        transfer_shadow_values.append(
            shadow.shadow_value if shadow.shadow_value is not None else AtomValue.OPEN
        )
        transfer_confidence_values.append(
            self_confidence_ablation(case.atom_address, raw_c).value
        )
        transfer_groups.append((probe.schema.value, case.reference.name, case.offset))
        transfer_weights.append(probe_target_weight(probe))

    request_features = np.stack(
        [encode_request_atom(request, atom) for request in world.requests for atom in request.atoms]
    )
    request_s_raw = predict(structured_model, request_features)
    request_c_raw = predict(ce_model, request_features)
    structured_outcomes: list[Outcome] = []
    ce_outcomes: list[Outcome] = []
    center_outcomes: list[Outcome] = []
    unaccepted_outcomes: list[Outcome] = []
    self_confidence_outcomes: list[Outcome] = []
    request_structured_decisions = []
    cursor = 0
    for request in world.requests:
        structured_atoms = []
        ce_atoms = []
        center_atoms = []
        unaccepted_atoms = []
        confidence_atoms = []
        for atom in request.atoms:
            address = f"{request.request_id}:{atom.name}"
            structured_atom = decode_structured(
                atom_address=address,
                schema=atom.schema,
                plan=request.plan,
                stage=request.stage,
                threshold=atom.threshold,
                evidence_present=atom.evidence_present,
                evidence_valid=atom.evidence_valid,
                can_support=atom.can_support,
                can_refute=atom.can_refute,
                raw=request_s_raw[cursor],
                scorer_parameter_hash=structured_hash,
                calibration=calibration,
            )
            structured_atoms.append(structured_atom)
            request_structured_decisions.append(structured_atom)
            ce_atoms.append(
                decode_cross_entropy(
                    atom_address=address,
                    logits=request_c_raw[cursor],
                    evidence_present=atom.evidence_present,
                    evidence_valid=atom.evidence_valid,
                    can_support=atom.can_support,
                    can_refute=atom.can_refute,
                )
            )
            center_atoms.append(
                decode_structured(
                    atom_address=address,
                    schema=atom.schema,
                    plan=request.plan,
                    stage=request.stage,
                    threshold=atom.threshold,
                    evidence_present=atom.evidence_present,
                    evidence_valid=atom.evidence_valid,
                    can_support=atom.can_support,
                    can_refute=atom.can_refute,
                    raw=request_s_raw[cursor],
                    scorer_parameter_hash=structured_hash,
                    calibration=center_calibration,
                    variant="center_only",
                )
            )
            unaccepted_atoms.append(
                decode_structured(
                    atom_address=address,
                    schema=atom.schema,
                    plan=request.plan,
                    stage=request.stage,
                    threshold=atom.threshold,
                    evidence_present=atom.evidence_present,
                    evidence_valid=atom.evidence_valid,
                    can_support=atom.can_support,
                    can_refute=atom.can_refute,
                    raw=request_s_raw[cursor],
                    scorer_parameter_hash=structured_hash,
                    calibration=calibration,
                    variant="unaccepted_radius",
                )
            )
            confidence_atoms.append(self_confidence_ablation(address, request_c_raw[cursor]))
            cursor += 1
        structured_outcomes.append(decode_request(request, structured_atoms).outcome)
        ce_outcomes.append(decode_request(request, ce_atoms).outcome)
        center_outcomes.append(decode_request(request, center_atoms).outcome)
        unaccepted_outcomes.append(decode_request(request, unaccepted_atoms).outcome)
        self_confidence_outcomes.append(decode_request(request, confidence_atoms).outcome)

    boundary_weights = [
        probe_target_weight(probe)
        for probe in world.probes
        for _ in BOUNDARY_CONDITIONS
    ]
    request_weights = [request_target_weight(request) for request in world.requests]
    request_weight_sum = sum(request_weights)

    def request_accuracy(predictions: Sequence[Outcome]) -> float:
        return sum(
            weight * float(predicted is request.outcome)
            for predicted, request, weight in zip(
                predictions, world.requests, request_weights
            )
        ) / request_weight_sum

    def fallback_mass(predictions: Sequence[Outcome]) -> float:
        return sum(
            weight * float(predicted is not Outcome.GRANTED)
            for predicted, weight in zip(predictions, request_weights)
        ) / request_weight_sum

    metrics = {
        "world_index": world_index,
        "E_in_structured": _macro_accuracy(references, structured_values, in_groups, weights),
        "E_in_ce": _macro_accuracy(references, ce_values, in_groups, weights),
        "E_in_center_only": _macro_accuracy(references, center_values, in_groups, weights),
        "E_in_unaccepted_radius_shadow": _macro_accuracy(references, unaccepted_shadow_values, in_groups, weights),
        "E_in_unaccepted_radius_production": _macro_accuracy(references, unaccepted_production_values, in_groups, weights),
        "E_in_self_confidence_invalid": _macro_accuracy(references, self_confidence_values, in_groups, weights),
        "E_boundary_structured": _macro_accuracy(boundary_refs, boundary_s_values, boundary_groups, boundary_weights),
        "E_boundary_ce": _macro_accuracy(boundary_refs, boundary_c_values, boundary_groups, boundary_weights),
        "E_boundary_center_only": _macro_accuracy(boundary_refs, boundary_center_values, boundary_groups, boundary_weights),
        "E_boundary_unaccepted_radius_shadow": _macro_accuracy(boundary_refs, boundary_shadow_values, boundary_groups, boundary_weights),
        "E_boundary_self_confidence_invalid": _macro_accuracy(boundary_refs, boundary_confidence_values, boundary_groups, boundary_weights),
        "E_transfer_structured": _macro_accuracy(transfer_refs, transfer_s_values, transfer_groups, transfer_weights),
        "E_transfer_ce": _macro_accuracy(transfer_refs, transfer_c_values, transfer_groups, transfer_weights),
        "E_transfer_center_only": _macro_accuracy(transfer_refs, transfer_center_values, transfer_groups, transfer_weights),
        "E_transfer_unaccepted_radius_shadow": _macro_accuracy(transfer_refs, transfer_shadow_values, transfer_groups, transfer_weights),
        "E_transfer_self_confidence_invalid": _macro_accuracy(transfer_refs, transfer_confidence_values, transfer_groups, transfer_weights),
        "coverage_J": sum(coverage[Schema.LOSS]) / len(coverage[Schema.LOSS]),
        "coverage_T": sum(coverage[Schema.LATENCY]) / len(coverage[Schema.LATENCY]),
        "query_outcome_structured": request_accuracy(structured_outcomes),
        "query_outcome_ce": request_accuracy(ce_outcomes),
        "query_outcome_center_only": request_accuracy(center_outcomes),
        "query_outcome_unaccepted_radius_production": request_accuracy(unaccepted_outcomes),
        "query_outcome_self_confidence_invalid": request_accuracy(self_confidence_outcomes),
        "fallback_mass_structured": fallback_mass(structured_outcomes),
        "fallback_mass_ce": fallback_mass(ce_outcomes),
        "inactive_selection_rate_structured": 0.0,
        "inactive_selection_rate_ce": 0.0,
    }
    trace = {
        "probe_structured_raw": structured_raw.astype(np.float32),
        "probe_ce_raw": ce_raw.astype(np.float32),
        "probe_reference": np.asarray([int(value) for value in references], dtype=np.int8),
        "probe_structured_K3": np.asarray([int(value) for value in structured_values], dtype=np.int8),
        "probe_ce_K3": np.asarray([int(value) for value in ce_values], dtype=np.int8),
        "probe_center_only_K3": np.asarray([int(value) for value in center_values], dtype=np.int8),
        "probe_unaccepted_shadow_K3": np.asarray([int(value) for value in unaccepted_shadow_values], dtype=np.int8),
        "probe_unaccepted_production_K3": np.asarray([int(value) for value in unaccepted_production_values], dtype=np.int8),
        "probe_self_confidence_K3": np.asarray([int(value) for value in self_confidence_values], dtype=np.int8),
        "probe_support_margin": np.asarray(support_margins, dtype=np.float32),
        "probe_refutation_margin": np.asarray(refutation_margins, dtype=np.float32),
        "probe_support_relu": np.asarray(support_relus, dtype=np.float32),
        "probe_refutation_relu": np.asarray(refutation_relus, dtype=np.float32),
        "boundary_structured_raw": boundary_s_raw.astype(np.float32),
        "boundary_ce_raw": boundary_c_raw.astype(np.float32),
        "boundary_reference": np.asarray([int(value) for value in boundary_refs], dtype=np.int8),
        "boundary_structured_K3": np.asarray([int(value) for value in boundary_s_values], dtype=np.int8),
        "boundary_ce_K3": np.asarray([int(value) for value in boundary_c_values], dtype=np.int8),
        "boundary_center_only_K3": np.asarray([int(value) for value in boundary_center_values], dtype=np.int8),
        "boundary_unaccepted_shadow_K3": np.asarray([int(value) for value in boundary_shadow_values], dtype=np.int8),
        "boundary_self_confidence_K3": np.asarray([int(value) for value in boundary_confidence_values], dtype=np.int8),
        "boundary_support_margin": np.asarray(boundary_support_margins, dtype=np.float32),
        "boundary_refutation_margin": np.asarray(boundary_refutation_margins, dtype=np.float32),
        "boundary_support_relu": np.asarray(boundary_support_relus, dtype=np.float32),
        "boundary_refutation_relu": np.asarray(boundary_refutation_relus, dtype=np.float32),
        "transfer_structured_raw": transfer_s_raw.astype(np.float32),
        "transfer_ce_raw": transfer_c_raw.astype(np.float32),
        "transfer_reference": np.asarray([int(value) for value in transfer_refs], dtype=np.int8),
        "transfer_structured_K3": np.asarray([int(value) for value in transfer_s_values], dtype=np.int8),
        "transfer_ce_K3": np.asarray([int(value) for value in transfer_c_values], dtype=np.int8),
        "transfer_center_only_K3": np.asarray([int(value) for value in transfer_center_values], dtype=np.int8),
        "transfer_unaccepted_shadow_K3": np.asarray([int(value) for value in transfer_shadow_values], dtype=np.int8),
        "transfer_self_confidence_K3": np.asarray([int(value) for value in transfer_confidence_values], dtype=np.int8),
        "transfer_support_margin": np.asarray(transfer_support_margins, dtype=np.float32),
        "transfer_refutation_margin": np.asarray(transfer_refutation_margins, dtype=np.float32),
        "transfer_support_relu": np.asarray(transfer_support_relus, dtype=np.float32),
        "transfer_refutation_relu": np.asarray(transfer_refutation_relus, dtype=np.float32),
        "request_structured_raw": request_s_raw.astype(np.float32),
        "request_ce_raw": request_c_raw.astype(np.float32),
        "request_reference_outcome": np.asarray([list(Outcome).index(r.outcome) for r in world.requests], dtype=np.int8),
        "request_structured_outcome": np.asarray([list(Outcome).index(value) for value in structured_outcomes], dtype=np.int8),
        "request_ce_outcome": np.asarray([list(Outcome).index(value) for value in ce_outcomes], dtype=np.int8),
        "request_structured_active_mask": np.asarray(
            [int(value is Outcome.GRANTED) for value in structured_outcomes],
            dtype=np.int8,
        ),
        "request_ce_active_mask": np.asarray(
            [int(value is Outcome.GRANTED) for value in ce_outcomes],
            dtype=np.int8,
        ),
        "request_structured_route": np.asarray(
            [
                list(Plan).index(request.plan if outcome is Outcome.GRANTED else Plan.FALLBACK)
                for request, outcome in zip(world.requests, structured_outcomes)
            ],
            dtype=np.int8,
        ),
        "request_ce_route": np.asarray(
            [
                list(Plan).index(request.plan if outcome is Outcome.GRANTED else Plan.FALLBACK)
                for request, outcome in zip(world.requests, ce_outcomes)
            ],
            dtype=np.int8,
        ),
        "request_center_only_outcome": np.asarray([list(Outcome).index(value) for value in center_outcomes], dtype=np.int8),
        "request_unaccepted_production_outcome": np.asarray([list(Outcome).index(value) for value in unaccepted_outcomes], dtype=np.int8),
        "request_self_confidence_outcome": np.asarray([list(Outcome).index(value) for value in self_confidence_outcomes], dtype=np.int8),
        "request_atom_structured_K3": np.asarray(
            [int(decision.value) for decision in request_structured_decisions],
            dtype=np.int8,
        ),
        "request_atom_support_margin": np.asarray(
            [float(decision.support_margin) for decision in request_structured_decisions],
            dtype=np.float32,
        ),
        "request_atom_refutation_margin": np.asarray(
            [float(decision.refutation_margin) for decision in request_structured_decisions],
            dtype=np.float32,
        ),
        "request_atom_support_relu": np.asarray(
            [decision.support_relu for decision in request_structured_decisions],
            dtype=np.float32,
        ),
        "request_atom_refutation_relu": np.asarray(
            [decision.refutation_relu for decision in request_structured_decisions],
            dtype=np.float32,
        ),
    }
    return metrics, trace


def _write_trace_shard(
    start: int,
    stop: int,
    seed: int,
    traces: Sequence[Mapping[str, np.ndarray]],
) -> str:
    TRACE_DIRECTORY.mkdir(exist_ok=True)
    keys = set(traces[0])
    if any(set(trace) != keys for trace in traces):
        raise ValueError("trace shard rows do not share one frozen schema")
    combined = {
        key: np.concatenate([trace[key] for trace in traces], axis=0)
        for key in sorted(keys)
    }
    path = TRACE_DIRECTORY / f"worlds_{start:05d}_{stop - 1:05d}_seed_{seed}.npz"
    np.savez_compressed(path, **combined)
    return _sha256(path)


def run_task21_final(token: str) -> Mapping[str, Any]:
    if token != TASK21_TOKEN:
        raise PermissionError("the exact Task 21 final-authorization token is required")
    if RESULTS_PATH.exists() or FIT_MARKER_PATH.exists() or MODELS_PATH.exists():
        raise FileExistsError("frozen run artifacts already exist; automatic rerun is forbidden")
    contract = verify_frozen_sources()
    protocol = _json(PROTOCOL_PATH)
    started = time.perf_counter()

    # No confirmation payload exists before all selection, fitting, and
    # calibration decisions have been serialized and hashed.
    train = materialize_panel(Role.TRAIN, 0, 20000)
    fit_data = _subpanel(train, 0, 16000)
    selection_data = _subpanel(train, 16000, 20000)
    selection, trials = _fit_grid(fit_data, selection_data, protocol)
    structured_models, ce_models, summaries = _fit_final_models(
        fit_data, selection_data, selection
    )
    model_hash = _save_models(structured_models, ce_models, summaries)
    calibration_data = materialize_panel(Role.CALIBRATION, 0, 5000)
    calibrations = []
    for model, summary in zip(structured_models, summaries):
        common = {
            "scorer_parameter_hash": summary[0].parameter_hash,
            "training_manifest_hash": protocol["roles"][Role.TRAIN.value]["manifest_hash"],
            "calibration_manifest_hash": protocol["roles"][Role.CALIBRATION.value]["manifest_hash"],
        }
        calibrations.append(
            (
                calibrate_structured(model, calibration_data, **common),
                calibrate_structured(model, calibration_data, center_only=True, **common),
            )
        )
    fit_record = {
        "status": "fit_and_calibration_complete_before_final_materialization",
        "implementation_version": contract["implementation_version"],
        "selection": _selection(selection),
        "trials": trials,
        "fits": [
            {"structured": _summary(structured), "cross_entropy": _summary(ce)}
            for structured, ce in summaries
        ],
        "calibrations": [
            {
                variant.arm_variant: {
                    "calibration_id": variant.calibration_id,
                    "scorer_parameter_hash": variant.scorer_parameter_hash,
                    "groups": {
                        schema.value: asdict(group)
                        for schema, group in variant.groups.items()
                    },
                }
                for variant in pair
            }
            for pair in calibrations
        ],
        "models_sha256": model_hash,
        "final_payloads_generated": False,
    }
    FIT_MARKER_PATH.write_text(json.dumps(fit_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fit_marker_hash = _sha256(FIT_MARKER_PATH)

    world_seed_metrics: list[Mapping[str, Any]] = []
    trace_hashes: list[Mapping[str, Any]] = []
    for seed, structured_model, ce_model, summary, calibration_pair in zip(
        FIT_SEEDS, structured_models, ce_models, summaries, calibrations
    ):
        for block_start in range(0, 5000, 100):
            block_stop = min(5000, block_start + 100)
            block_traces = []
            for world_index in range(block_start, block_stop):
                metrics, trace = _evaluate_one_world_seed(
                    world_index,
                    structured_model,
                    ce_model,
                    summary[0].parameter_hash,
                    calibration_pair[0],
                    calibration_pair[1],
                    role=Role.FINAL_CONFIRMATION,
                    allow_final=True,
                )
                world_seed_metrics.append({"fit_seed": seed, **metrics})
                block_traces.append(trace)
            trace_hashes.append(
                {
                    "world_start": block_start,
                    "world_stop_exclusive": block_stop,
                    "fit_seed": seed,
                    "sha256": _write_trace_shard(
                        block_start, block_stop, seed, block_traces
                    ),
                }
            )
    result = {
        "status": "raw_frozen_run_complete_unadjudicated",
        "implementation_version": contract["implementation_version"],
        "protocol_version": protocol["protocol_version"],
        "fit_marker_sha256": fit_marker_hash,
        "models_sha256": model_hash,
        "world_seed_metrics": world_seed_metrics,
        "trace_shards": trace_hashes,
        "trace_schema": contract["trace_schema"],
        "system_witness": deterministic_system_witness(),
        "hard_moe": "omitted_prospectively",
        "elapsed_seconds": time.perf_counter() - started,
        "adjudication": None,
    }
    RESULTS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "status": result["status"],
        "results_path": str(RESULTS_PATH),
        "results_sha256": _sha256(RESULTS_PATH),
        "trace_shards": len(trace_hashes),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preflight", action="store_true", help="verify the frozen implementation without fitting")
    mode.add_argument("--smoke", action="store_true", help="run a pilot-role implementation smoke test")
    mode.add_argument("--task21-final", metavar="TOKEN", help="execute the single frozen final run")
    args = parser.parse_args(argv)
    try:
        if args.task21_final is not None:
            result = run_task21_final(args.task21_final)
        elif args.smoke:
            result = run_smoke()
        else:
            result = run_preflight()
    except Exception as error:
        print(f"frozen experiment entry point failed: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
