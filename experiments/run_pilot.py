"""Run the Task 19A generator-only pilot and freeze protocol artifacts.

This entry point may materialize only ``Role.PILOT`` worlds.  It writes no
learned-arm result and never calls ``generate_world`` for a production role.
Production manifests contain deterministic lineage identifiers and digests,
not generated targets or oracle outcomes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, is_dataclass
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path
import sys
from time import perf_counter
from typing import Any

from experiments.protocol import (
    ALPHA_CAL,
    BOOTSTRAP_SEED,
    CELL_DESIGN_COUNTS,
    CELL_DESIGN_MASS,
    CELL_TARGET_MASS,
    FINAL_WORLD_CAP,
    FINAL_WORLD_FLOOR,
    FIT_SEEDS,
    GENERATOR_VERSION,
    ORACLE_VERSION,
    OUTCOME_DESIGN_COUNTS,
    OUTCOME_DESIGN_MASS,
    OUTCOME_TARGET_MASS,
    PILOT_WORLD_COUNT,
    PRODUCTION_ROLES,
    PROTOCOL_VERSION,
    REQUIRED_BINDING_FIELDS,
    ROLE_SEEDS,
    SCORER_INPUT_WHITELIST,
    STRATUM_DESIGN_COUNTS,
    STRATUM_DESIGN_MASS,
    STRATUM_TARGET_MASS,
    AtomStratum,
    ContextCell,
    Role,
    Schema,
    audit_manifest_disjointness,
    bootstrap_sd_upper,
    generate_world,
    manifest_summary,
    paired_sample_size,
    round_world_count,
    succession_fixture,
    worst_case_paired_sd,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS_PATH = HERE / "pilot_results_v1.json"
MANIFESTS_PATH = HERE / "manifests_v1.json"
PROTOCOL_PATH = HERE / "protocol_v1.json"


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(_jsonable(key)): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_jsonable(item) for item in value]
    return value


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _counter(counter: Counter[Any]) -> dict[str, int]:
    return {str(_jsonable(key)): value for key, value in sorted(counter.items(), key=lambda x: str(x[0]))}


def _validate_world(world: Any) -> None:
    if len(world.probes) != 80 or len(world.requests) != 40:
        raise AssertionError("world panel cardinality changed")
    for schema in Schema:
        records = [probe for probe in world.probes if probe.schema is schema]
        if Counter(probe.stratum for probe in records) != Counter(STRATUM_DESIGN_COUNTS):
            raise AssertionError(f"{schema.value} atom quota changed")
        if Counter(probe.cell for probe in records) != Counter(CELL_DESIGN_COUNTS):
            raise AssertionError(f"{schema.value} context quota changed")
    if Counter(request.outcome for request in world.requests) != Counter(OUTCOME_DESIGN_COUNTS):
        raise AssertionError("public-outcome quota changed")
    if Counter(request.cell for request in world.requests) != Counter(CELL_DESIGN_COUNTS):
        raise AssertionError("request context quota changed")
    if sum(request.boundary_case for request in world.requests) != 8:
        raise AssertionError("request boundary quota changed")
    by_outcome: dict[Any, Counter[str]] = defaultdict(Counter)
    for request in world.requests:
        by_outcome[request.outcome][request.focal_atom] += 1
        if request.delta <= 0:
            raise AssertionError("fallback-improvement delta must remain positive")
    for outcome in OUTCOME_DESIGN_COUNTS:
        if outcome.value == "Undefined":
            continue
        if by_outcome[outcome] != Counter({"A": 4, "I": 4, "C": 4}):
            raise AssertionError(f"focal-atom balance changed for {outcome.value}")


def run_pilot() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    start = perf_counter()
    worlds = []
    for index in range(PILOT_WORLD_COUNT):
        world = generate_world(Role.PILOT, index)
        _validate_world(world)
        worlds.append(world)
    elapsed = perf_counter() - start

    all_probes = [probe for world in worlds for probe in world.probes]
    all_requests = [request for world in worlds for request in world.requests]
    coverage_by_schema: dict[str, float] = {}
    world_coverages: dict[str, list[float]] = {schema.value: [] for schema in Schema}
    for schema in Schema:
        schema_records = [probe for probe in all_probes if probe.schema is schema]
        coverage_by_schema[schema.value] = sum(
            probe.reference_region.contains(probe.oracle_target)
            for probe in schema_records
        ) / len(schema_records)
        for world in worlds:
            records = [probe for probe in world.probes if probe.schema is schema]
            world_coverages[schema.value].append(
                sum(
                    probe.reference_region.contains(probe.oracle_target)
                    for probe in records
                )
                / len(records)
            )

    coverage_sd = {
        schema: bootstrap_sd_upper(values)
        for schema, values in world_coverages.items()
    }
    coverage_pilot_band_ok = all(
        0.885 <= value <= 0.915 for value in coverage_by_schema.values()
    )

    fixture = succession_fixture()
    fixture_ok = (
        len(fixture.simultaneous_active) == 2
        and fixture.gap_uses_fallback
        and fixture.lapse_outcome.value == "Withheld"
        and fixture.rebuttal_outcome.value == "Refused"
        and fixture.irrelevant_before == fixture.irrelevant_after
        and fixture.tolerance_old.name == "OPEN"
        and fixture.tolerance_successor.name == "SUPPORTED"
        and len(fixture.later_dominates) == 2
    )

    # Task 20's learners do not exist, so a generator-only pilot cannot observe
    # their paired endpoint SD.  Freeze conservative worst-coupling bounds at
    # the registered design alternatives instead of presenting proxy-arm
    # variance as data.  Pilot coverage SD remains a generator diagnostic; the
    # coverage power bound assumes worst clustering at p=.90 (SD=.30).
    superiority_sd_bound = worst_case_paired_sd(0.90, 0.80)
    in_regime_sd_bound = worst_case_paired_sd(0.90, 0.90)
    coverage_sd_bound = max(0.30, *coverage_sd.values())
    power_counts = {
        "tolerance_transfer": paired_sample_size(
            superiority_sd_bound, 0.05, alpha=0.025
        ),
        "boundary_status": paired_sample_size(
            superiority_sd_bound, 0.05, alpha=0.025
        ),
        "in_regime_noninferiority": paired_sample_size(
            in_regime_sd_bound, 0.02, alpha=0.05
        ),
        "coverage_J": paired_sample_size(
            coverage_sd_bound, 0.02, alpha=0.025
        ),
        "coverage_T": paired_sample_size(
            coverage_sd_bound, 0.02, alpha=0.025
        ),
    }
    unrounded_final = max(FINAL_WORLD_FLOOR, *power_counts.values())
    final_worlds = round_world_count(unrounded_final)
    if final_worlds > FINAL_WORLD_CAP:
        raise RuntimeError(
            f"core power rule requires {final_worlds} worlds, above cap {FINAL_WORLD_CAP}"
        )
    role_counts = {
        Role.TRAIN: max(4 * final_worlds, 2000),
        Role.CALIBRATION: max(final_worlds, 1000),
        Role.VALIDATION: final_worlds,
        Role.SYSTEM_AUDIT: final_worlds,
        Role.FINAL_CONFIRMATION: final_worlds,
    }

    pilot_manifest = manifest_summary(
        Role.PILOT, PILOT_WORLD_COUNT, payloads_generated=True
    )
    production_manifests = [
        manifest_summary(role, role_counts[role], payloads_generated=False)
        for role in PRODUCTION_ROLES
    ]
    all_manifests = [pilot_manifest, *production_manifests]
    audit_manifest_disjointness(all_manifests)
    if any(
        manifest.payloads_generated
        for manifest in production_manifests
    ):
        raise AssertionError("production payload was generated during pilot")

    manifest_payload = {
        "protocol_version": PROTOCOL_VERSION,
        "implicit_manifest_rule": (
            "IDs are SHA-256(protocol_version|role_seed|kind|index); exact ordered "
            "membership is recoverable from seed_label and count; digests bind every ID"
        ),
        "manifests": all_manifests,
        "disjointness_audit": {
            "world_roots": "pass",
            "trajectory_roots": "pass",
            "provenance_roots": "pass",
            "plan_family_roots": "pass",
        },
    }
    _write_json(MANIFESTS_PATH, manifest_payload)

    pilot_results: dict[str, Any] = {
        "protocol_version": PROTOCOL_VERSION,
        "pilot_role": Role.PILOT,
        "pilot_worlds": PILOT_WORLD_COUNT,
        "production_world_payloads_generated": False,
        "runtime_seconds": elapsed,
        "runtime_worlds_per_second": PILOT_WORLD_COUNT / elapsed,
        "panel": {
            "probes_per_world": 80,
            "requests_per_world": 40,
            "probe_strata": _counter(Counter(probe.stratum for probe in all_probes)),
            "probe_states": _counter(Counter(probe.value.name for probe in all_probes)),
            "request_outcomes": _counter(Counter(request.outcome.value for request in all_requests)),
            "request_cells": _counter(Counter(request.cell for request in all_requests)),
            "boundary_probes": sum(probe.boundary for probe in all_probes),
            "boundary_requests": sum(request.boundary_case for request in all_requests),
            "missing_learning_targets": sum(
                probe.learning_target is None for probe in all_probes
            ),
        },
        "oracle_reference_coverage": coverage_by_schema,
        "oracle_world_coverage_sd_upper_95_bootstrap": coverage_sd,
        "oracle_coverage_balance_band_0.885_0.915": coverage_pilot_band_ok,
        "fixture_acceptance": fixture_ok,
        "manifest_disjointness": "pass",
        "power": {
            "status": "planning bounds; not observed learner effects",
            "structured_design_accuracy": 0.90,
            "ce_superiority_design_accuracy": 0.80,
            "ce_in_regime_design_accuracy": 0.90,
            "superiority_sd_worst_coupling": superiority_sd_bound,
            "in_regime_sd_worst_coupling": in_regime_sd_bound,
            "coverage_sd_worst_clustered_at_p_0.90": coverage_sd_bound,
            "endpoint_world_counts": power_counts,
            "unrounded_maximum": unrounded_final,
            "block_size": 100,
            "final_worlds": final_worlds,
            "role_world_counts": role_counts,
        },
        "optional_extensions": {
            "hard_moe": {
                "decision": "omit_prospectively",
                "reason": (
                    "no independent conforming/mismatched seam generator or paired "
                    "interaction-variance estimate exists without displacing the core"
                ),
            },
            "system_certificate": {
                "decision": "deterministic_integration_witness_only",
                "reason": (
                    "root-count gate passes, but no learned-grade adapter or powered "
                    "false-grant variance exists before Task 20"
                ),
            },
            "activation_alignment": "exploratory_only",
        },
    }
    _write_json(RESULTS_PATH, pilot_results)

    protocol_payload: dict[str, Any] = {
        "protocol_version": PROTOCOL_VERSION,
        "status": "frozen_after_generator_only_pilot",
        "frozen_date": "2026-07-14",
        "generator_version": GENERATOR_VERSION,
        "oracle_version": ORACLE_VERSION,
        "alpha_cal": ALPHA_CAL,
        "design_sha256": _file_sha256(HERE / "01_design.md"),
        "generator_source_sha256": _file_sha256(HERE / "protocol.py"),
        "pilot_runner_sha256": _file_sha256(HERE / "run_pilot.py"),
        "pilot_results_sha256": _file_sha256(RESULTS_PATH),
        "manifests_sha256": _file_sha256(MANIFESTS_PATH),
        "python_runtime": sys.version,
        "roles": {
            role.value: {
                "count": role_counts[role],
                "seed_label": ROLE_SEEDS[role],
                "manifest_hash": next(
                    manifest.manifest_hash
                    for manifest in production_manifests
                    if manifest.role is role
                ),
                "payloads_generated": False,
                "embargoed": role is Role.FINAL_CONFIRMATION,
            }
            for role in PRODUCTION_ROLES
        },
        "pilot": {
            "count": PILOT_WORLD_COUNT,
            "seed_label": ROLE_SEEDS[Role.PILOT],
            "manifest_hash": pilot_manifest.manifest_hash,
            "payloads_generated": True,
        },
        "fit_seeds": FIT_SEEDS,
        "analysis_bootstrap": {
            "seed": BOOTSTRAP_SEED,
            "replicates": 10000,
            "unit": "world_root",
            "fit_seed_handling": "average fixed eight paired fits within world",
        },
        "sampling": {
            "context_target_mass": CELL_TARGET_MASS,
            "context_design_mass": CELL_DESIGN_MASS,
            "atom_target_mass": STRATUM_TARGET_MASS,
            "atom_design_mass": STRATUM_DESIGN_MASS,
            "outcome_target_mass": OUTCOME_TARGET_MASS,
            "outcome_design_mass": OUTCOME_DESIGN_MASS,
            "importance_weight": "target_mass/design_mass",
        },
        "minimum_core": {
            "F35": {
                "superiority_margin": 0.05,
                "design_alternative_difference": 0.10,
                "in_regime_noninferiority_margin": -0.02,
                "holm_familywise_alpha": 0.05,
                "endpoint_world_counts": power_counts,
            },
            "F36": {
                "nominal_coverage": 0.90,
                "null_lower_margin": 0.88,
                "groups": [Schema.LOSS.value, Schema.LATENCY.value],
                "infinite_proposal_counts_as_covered_but_is_not_usable": True,
            },
        },
        "endpoint_contract": {
            "E_transfer": (
                "target-weighted K3 accuracy; macro J/T x Supported/Open/Refuted "
                "x offsets -2,-1.5,1.5,2; structured minus CE"
            ),
            "E_boundary": (
                "macro K3 accuracy on near-support, exact boundary support, "
                "crossing open, near-refutation within normalized distance .25"
            ),
            "E_in": "target-weighted in-regime macro K3 accuracy",
            "coverage": (
                "per pre-outcome-eligible target indicator t in U_prop; infinity "
                "counts covered but is unusable evidence"
            ),
            "key_secondary": [
                "false_support_rate",
                "false_refutation_rate",
                "atom_K3_fidelity",
                "query_quotient_fidelity",
                "four_way_public_outcome_fidelity",
                "simultaneous_license_fidelity",
                "empty_active_set_fidelity",
                "lapse_rebuttal_update_tolerance_dominator_fidelity",
                "finite_width_infinity_rejection_rates",
                "inactive_selection_rate_exactly_zero",
                "selected_deployed_fallback_and_misroute_loss",
                "CE_class_probability_calibration_separate_from_region_coverage",
            ],
            "target_reweighting": "fixed target_mass/design_mass within world",
        },
        "inference": {
            "primary_unit": "world_root",
            "within_world": "compute weighted metric then average eight paired fit seeds",
            "primary_bootstrap_replicates": 10000,
            "primary_bootstrap_seed": BOOTSTRAP_SEED,
            "primary_bootstrap": "paired world-cluster centered at registered null margin",
            "F35_multiplicity": "Holm one-sided family alpha .05; E_in intersection gate alpha .05",
            "F36_multiplicity": "Holm one-sided J/T family alpha .05",
            "secondary_intervals": "world-clustered 95%; descriptive",
        },
        "role_permissions": {
            Role.TRAIN.value: "fit plus frozen 80/20 internal scorer selection only",
            Role.CALIBRATION.value: "fit eta_cal for frozen scorer only",
            Role.VALIDATION.value: "fit reject/router thresholds only",
            Role.SYSTEM_AUDIT.value: "construct lower-ranked audit evidence only",
            Role.FINAL_CONFIRMATION.value: "single frozen evaluation; no fitting or tuning",
        },
        "sample_size": {
            "final_worlds": final_worlds,
            "floor": FINAL_WORLD_FLOOR,
            "cap": FINAL_WORLD_CAP,
            "rounding_block": 100,
            "role_world_counts": role_counts,
        },
        "scorer_firewall": {
            "whitelist": sorted(SCORER_INPUT_WHITELIST),
            "closed_world": True,
            "taint_provenance_required_for_transforms": True,
        },
        "proposal_binding": {
            "required_fields": REQUIRED_BINDING_FIELDS,
            "minimum_calibration_worlds_per_group": 200,
            "mismatch_result": "Open",
            "infinity_result": "Open",
        },
        "learned_factorization": {
            "structured": (
                "shared ReLU trunk; one vector head emitting "
                "center_J,radius_J,center_T,radius_T"
            ),
            "cross_entropy": "shared ReLU trunk family; three logits per atom slot",
            "deterministic_decoder_channels_are_not_learned_heads": True,
            "capacity_rule": (
                "two hidden ReLU layers; choose the smallest integer widths meeting "
                "the selected trainable-parameter budget and <=2% arm mismatch; "
                "tie-break by lower inference FLOPs"
            ),
        },
        "optimization": {
            "optimizer": "AdamW",
            "batch_size": 512,
            "max_epochs": 200,
            "patience_epochs": 20,
            "minimum_validation_improvement": 1e-5,
            "gradient_norm_clip": 1.0,
            "learning_rate_grid": [0.0003, 0.001, 0.003],
            "weight_decay_grid": [0.0, 0.0001, 0.001],
            "parameter_budget_grid": [12000, 20000],
            "trial_budget": 18,
            "selection_role": "train_internal_selection_partition",
            "train_internal_selection_fraction": 0.20,
            "train_partition_blocked_by_world_root": True,
            "train_partition_rule": (
                "indices 0..15999 fit; indices 16000..19999 internal selection"
            ),
            "center_then_radius": True,
            "center_mapping_frozen_during_radius_fit": True,
            "final_optional_stopping": False,
        },
        "required_ablations": {
            "1": "direct independent atom K3 cross-entropy baseline",
            "2": "center-only with common accepted calibration convention",
            "3": "predicted radius without accepted held-out expansion; shadow path only",
            "5": "self-confidence incorrectly treated as grant; never production active mask",
        },
        "deterministic_witness": "F18 sign/boundary/masking regression",
        "trace_required_fields": [
            "protocol_and_manifest_hashes",
            "world_trajectory_provenance_plan_family_roots_and_role",
            "allowed_input_field_names_and_firewall_result",
            "request_profile_units_thresholds_scope_stage_event_prefix",
            "arm_parameter_hash_factorization_fit_seed_capacity_compute",
            "raw_center_radius_or_logits",
            "binding_checker_polarity_validity",
            "signed_margins_paired_relu_K3_WF_public_outcome_active_mask",
            "router_fallback_and_dependency_footprint",
            "access_control_separated_oracle_namespace",
            "target_design_weights_stratum_metric_contribution_failure_flags",
        ],
        "optional_extensions": pilot_results["optional_extensions"],
        "amendments": [
            {
                "id": "19A-A1",
                "kind": "clarification",
                "decision": (
                    "later finite dominance requires registered paired-difference "
                    "certificates; overlapping marginal intervals are insufficient"
                ),
            },
            {
                "id": "19A-A2",
                "kind": "power-planning repair",
                "decision": (
                    "learner paired SD cannot be observed before Task 20; use frozen "
                    "worst-coupling design-alternative bounds rather than proxy effects"
                ),
            },
        ],
        "embargo": {
            "final_payloads_generated": False,
            "final_manifest_ids_and_hashes_only": True,
            "materialization_requires_explicit_Task21_allow_final": True,
            "rerun_rule": "same seed/config only for unread infrastructure failure",
        },
    }
    _write_json(PROTOCOL_PATH, protocol_payload)
    return pilot_results, manifest_payload, protocol_payload


def main() -> int:
    if PROTOCOL_PATH.exists() and "--force-refreeze" not in sys.argv[1:]:
        print(
            "frozen Task 19A artifacts already exist; refusing to overwrite them. "
            "Use --force-refreeze only for a prospective versioned repair before "
            "production generation.",
            file=sys.stderr,
        )
        return 2
    pilot, _, protocol = run_pilot()
    print(
        json.dumps(
            {
                "pilot_worlds": pilot["pilot_worlds"],
                "runtime_seconds": pilot["runtime_seconds"],
                "oracle_reference_coverage": pilot["oracle_reference_coverage"],
                "final_worlds": protocol["sample_size"]["final_worlds"],
                "hard_moe": protocol["optional_extensions"]["hard_moe"]["decision"],
                "system_certificate": protocol["optional_extensions"]["system_certificate"]["decision"],
                "final_payloads_generated": protocol["embargo"]["final_payloads_generated"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
