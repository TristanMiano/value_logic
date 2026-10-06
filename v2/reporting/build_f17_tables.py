"""Export F17 tables from preserved records, without scientific execution.

Contributor: ChatGPT (GPT-6 Astra Pro), October 6, 2026.
Only Python's standard library is used. No experiment module is imported.
Default: create the missing fixed output exclusively. --check: compare its
bytes without writing. Neither mode trains, selects, evaluates or draws data.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "v2/reporting/F17_v1/tables.json"
F15 = "v2/work_logs/F15_v1_run1"
ND01 = "v2/work_logs/F15_ND01_v1_run1"
STATUSES = ("supported", "inconclusive", "violated")
RESOURCE_FIELDS = (
    "initial_total_ns", "one_update_arithmetic_ns", "one_update_total_ns",
    "current_native_protocol_ns", "resident_bytes", "retained_payload_bytes",
    "current_source_context_bytes", "current_proof_bytes",
    "cached_source_context_bytes", "cached_proof_bytes", "external_archive_bytes",
    "total_stored_serialized_upper_bytes", "peak_serialized_working_state_upper_bytes",
    "acquisition_calls", "acquisition_scalar_measurements",
    "acquisition_path_world_executions", "acquisition_transferred_bytes",
)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class Sources:
    def __init__(self):
        self.records = {}

    def read(self, name, sidecar=False):
        path = ROOT / name
        raw = path.read_bytes()
        self.records[name] = {"path": name, "bytes": len(raw), "sha256": digest(raw)}
        if sidecar:
            sidecar_name = name + ".sha256"
            sidecar_raw = (ROOT / sidecar_name).read_bytes()
            if sidecar_raw.decode().split()[0] != digest(raw):
                raise ValueError(f"Original sidecar mismatch: {name}")
            self.records[sidecar_name] = {
                "path": sidecar_name, "bytes": len(sidecar_raw), "sha256": digest(sidecar_raw)
            }
        return json.loads(raw)


def stats(values):
    return {"n": len(values), "mean": mean(values), "median": median(values),
            "minimum": min(values), "maximum": max(values), "sum": sum(values)}


def count_status(rows, field):
    counts = Counter(row[field] for row in rows)
    if set(counts) - set(STATUSES):
        raise ValueError("Unrecognized saved confidence disposition.")
    return {"n": len(rows), **{name: counts[name] for name in STATUSES}}


def original_intervals(value, found=None):
    found = {} if found is None else found
    if isinstance(value, dict):
        fields = ("id", "lower", "upper", "mean", "n", "radius", "sample_range")
        if all(key in value for key in fields):
            interval = {key: value[key] for key in fields}
            previous = found.setdefault(value["id"], interval)
            if previous != interval:
                raise ValueError("Conflicting duplicate original interval ID.")
        for child in value.values():
            original_intervals(child, found)
    elif isinstance(value, list):
        for child in value:
            original_intervals(child, found)
    return found


def verify_interval_copy(original, rows):
    intervals = original_intervals(original)
    if len(intervals) != 560 or len(rows) != 560:
        raise ValueError("The original confidence family must have exactly 560 rows.")
    if set(intervals) != {row["id"] for row in rows}:
        raise ValueError("Saved reporting interval IDs differ from original assessment.")
    for row in rows:
        if any(row[key] != value for key, value in intervals[row["id"]].items()):
            raise ValueError("Saved reporting interval differs from original assessment.")


def useful_native(case, row, rc):
    """Reconstruct Gate C's saved-row conjunction, not generic useful_decision."""
    native = row["native"]
    direct_edits = {"small_price", "small_negative_price", "large_price",
                    "large_negative_price", "program_edit"}
    useful = (case["variant"] in direct_edits
              and row["decision_status"] == "certified_order"
              and not row["refused"] and row["executed"] is not None
              and row["selected"] == row["executed"] == native["candidate_order"]
              and native["certificate_role"] == "selected_order"
              and native["status"] == "received" and native["semantic_valid"]
              and Fraction(native["upper_bound"]) <= -Fraction(rc["numeric_tolerance"])
              and native["source_premises_used"] >= 2
              and Fraction(row["coherent_worst_regret"]) <= Fraction(rc["decision_regret_tolerance"]))
    if useful != native["useful_derivation_candidate"]:
        raise ValueError("Native usefulness disagrees with its saved complete criterion.")
    return useful


def build():
    sources = Sources()
    config = sources.read("v2/experiments/config.v1.json")
    freeze = sources.read("v2/experiments/freeze.v1.json")
    diagnostic_freeze = sources.read("v2/experiments/neural_diagnostic_v1/freeze.json")
    recount = sources.read("v2/work_logs/C_2026-10-06_S1/saved_results_attempt1/summary.json")
    assessment = sources.read(f"{F15}/evaluation_attempt_1/retention_assessment.json", True)
    old_method_rows = sources.read("v2/experiments/F15_v1_analysis/retention_by_method.json")
    grouped = defaultdict(list)
    useful, selective = set(), set()
    cases = []
    rc = config["retention"]
    expected_arms = {(access, method) for access in rc["access_regimes"] for method in rc["methods"]}
    for seed in rc["evaluation_seeds"]:
        for variant in rc["variants"]:
            case = sources.read(f"{F15}/evaluation_attempt_1/retention_{seed}_{variant}.json", True)
            if (case["seed"], case["variant"]) != (seed, variant):
                raise ValueError("Original case identity differs from its registered path.")
            arms = [(row["access"], row["method"]) for row in case["methods"]]
            if len(arms) != len(expected_arms) or set(arms) != expected_arms:
                raise ValueError("Incomplete or repeated method/access arm.")
            cases.append(case)
            for row in case["methods"]:
                if len(row["numeric"]) != 6:
                    raise ValueError("A retention row must contain six numeric queries.")
                grouped[row["access"], row["method"]].append(row)
                if useful_native(case, row, rc):
                    useful.add((seed, variant))
                    if (row["access"] == "no_reacquisition"
                            and row["method"] in ("tailored", "exact_intervals")
                            and row["resources"]["fiber_vertex_count"] > 1
                            and row["resources"]["acquisition_scalar_measurements"] == 0
                            and row["numeric"][row["executed_index"]]["status"] == "approximate"):
                        selective.add((seed, variant, row["method"]))
    rows = []
    for access in rc["access_regimes"]:
        for method in rc["methods"]:
            members = grouped[access, method]
            row = {
                "access": access, "method": method, "method_rows": len(members),
                "numeric_queries": sum(len(r["numeric"]) for r in members),
                "numeric": dict(Counter(q["status"] for r in members for q in r["numeric"])),
                "decisions": dict(Counter(r["decision_status"] for r in members)),
                "native": dict(Counter(r["native"]["status"] for r in members)),
                "useful_native_rows": sum(r["native"]["useful_derivation_candidate"] for r in members),
                "mean_realized_regret_exact": str(sum((Fraction(r["scoring"]["realized_regret"]) for r in members), Fraction()) / len(members)),
                "acquisition_scalar_histogram": dict(sorted(Counter(str(r["resources"]["acquisition_scalar_measurements"]) for r in members).items())),
                "resources": {key: stats([r["resources"][key] for r in members]) for key in RESOURCE_FIELDS},
            }
            old = next(r for r in old_method_rows if (r["access"], r["method"]) == (access, method))
            for key in ("method_rows", "numeric_queries", "numeric", "decisions", "native", "useful_native_rows"):
                different = (Counter(row[key]) != Counter(old[key])
                             if isinstance(row[key], dict) else row[key] != old[key])
                if different:
                    raise ValueError(f"Original-unit recount differs from F15 summary: {method}/{key}")
            if any(row["resources"][key] != old["resources"][key] for key in RESOURCE_FIELDS):
                raise ValueError("Resource aggregation differs from original F15 report.")
            rows.append(row)
    selective_episodes = {(seed, variant) for seed, variant, _ in selective}
    totals = {
        "initial_population_seeds": len(rc["evaluation_seeds"]), "episodes": len(cases),
        "method_rows": sum(row["method_rows"] for row in rows),
        "scalar_queries": sum(row["numeric_queries"] for row in rows),
        "useful_distinct_episodes": len(useful), "useful_distinct_seeds": len({s for s, _ in useful}),
        "useful_method_rows": sum(row["useful_native_rows"] for row in rows),
        "useful_episodes_by_variant": dict(sorted(Counter(v for _, v in useful).items())),
        "selective_approximate_rows": len(selective),
        "selective_approximate_distinct_episodes": len(selective_episodes),
        "selective_approximate_distinct_seeds": len({s for s, _ in selective_episodes}),
        "saved_equal_information_comparisons_all_agree": recount["saved_equal_information_comparisons_all_agree"],
    }
    for key in totals:
        if key in recount and totals[key] != recount[key]:
            raise ValueError(f"Recount differs from preserved Gate C result: {key}")
    if sorted(map(list, useful)) != recount["useful_episode_keys"] or sorted(map(list, selective_episodes)) != recount["selective_approximate_episode_keys"]:
        raise ValueError("Useful episode identities differ from Gate C recount.")
    for output_key, row_key in (("numeric_dispositions", "numeric"), ("decision_dispositions", "decisions"), ("native_dispositions", "native")):
        counts = Counter()
        for row in rows:
            counts.update(row[row_key])
        totals[output_key] = dict(counts)
        if dict(counts) != recount[output_key] or dict(counts) != assessment[output_key]:
            raise ValueError("Aggregate dispositions differ from existing assessment/recount.")

    neural = sources.read(f"{F15}/evaluation_attempt_1/neural_assessment.json", True)
    intervals = sources.read("v2/experiments/F15_v1_analysis/neural_interval_rows.json")
    verify_interval_copy(neural, intervals)
    hypotheses = []
    for name in config["neural"]["g_family"]:
        selected = [r for r in intervals if f"/{name}/" in r["id"]]
        adequate = sum(model["hypotheses"][name]["adequate"] for model in neural["models"])
        # Adequacy is necessary for the stronger complete endpoint. In these
        # fixed original outcomes it fails for every model and every hypothesis.
        if adequate != 0:
            raise ValueError("This fixed report needs review: a hypothesis adequacy flag changed.")
        hypotheses.append({
            "hypothesis": name, "models": len(neural["models"]),
            "adequate_models": adequate, "complete_support_models": 0,
            "complete_support_basis": "Every original saved model hypothesis adequacy flag is false; adequacy is necessary for complete support.",
            "confidence_counts": {family: count_status([r for r in selected if r["statistic_family"] == family], "disposition") for family in ("intervention_mae", "intervention_decision", "matched_control_advantage")},
        })
    original_neural = {
        "models": len(neural["models"]), "task_ready_models": sum(m["task_ready"] for m in neural["models"]),
        "complete_identity_supported_models": neural["supported_prespecified_replicates"],
        "required_supported_models": config["analysis"]["minimum_supported_model_replicates"],
        "pilot_support": neural["pilot_support_criterion_met"],
        "familywise_alpha": neural["familywise_alpha"], "interval_rows": len(intervals),
        "overall_interval_counts": count_status(intervals, "disposition"),
        "conditional_base_counts": count_status([r for r in intervals if r["statistic_family"] == "conditional_base_mae"], "disposition"),
        "hypothesis_rows": hypotheses,
        "identity_control_rows": [{"control": control, **count_status([r for r in intervals if "/identity/" in r["id"] and r["statistic_family"] == "matched_control_advantage" and f"/{control}/" in r["id"]], "disposition")} for control in ("random", "permuted_concept", "shuffled_donor", "untrained")],
        "per_model": [{"evaluation_seed": m["evaluation_seed"], "task_ready": m["task_ready"], "disposition": m["disposition"], "base_probability_interval": m["base_probability_interval"], "base_normalized_regret_interval": m["base_normalized_regret_interval"]} for m in neural["models"]],
        "interpretation": "Original frozen conjunction: unsuccessful. Inconclusive accuracy cells are not automatic falsification. No unique or joint utility representation established.",
    }

    nd_summary = sources.read("v2/experiments/F15_ND01_analysis/core_summary.json")
    calibration = sources.read(f"{ND01}/evaluation_attempt_1/calibration_assessment.json", True)
    verify_interval_copy(calibration, nd_summary["calibration"]["interval_rows"])
    mask_rows = []
    for index in range(5):
        saved = sources.read(f"{ND01}/evaluation_attempt_1/soft_mask_{index}_evaluation.json", True)
        if saved["model_index"] != index or saved["formal_support_assessed"]:
            raise ValueError("Diagnostic model index or development assessment scope changed.")
        mask_rows.extend(saved["rows"])
    masks = []
    for method in ("frozen_original", "binary_global", "rounded_top8", "fractional_mask"):
        cells = [r for r in mask_rows if r["method"] == method]
        roles = []
        for index in range(5):
            for role in range(2):
                by_stratum = {r["stratum"]: r for r in cells if (r["model_index"], r["role"]) == (index, role)}
                if len(by_stratum) != 5:
                    raise ValueError("Incomplete diagnostic stratum product.")
                ok = all(r["mae"] <= .05 for r in by_stratum.values()) and by_stratum["mixed_near"]["decision_disagreement"] <= .35 and by_stratum["mixed_far"]["decision_disagreement"] <= .10
                roles.append({"model": index, "role": role, "mean_mae": mean(r["mae"] for r in by_stratum.values()), "point_adequate": ok})
        result = {"method": method, "models": 5, "roles": 10, "cells": len(cells),
                  "mean_mae": mean(r["mean_mae"] for r in roles),
                  "mean_near_disagreement": mean(r["decision_disagreement"] for r in cells if r["stratum"] == "mixed_near"),
                  "mean_far_disagreement": mean(r["decision_disagreement"] for r in cells if r["stratum"] == "mixed_far"),
                  "point_adequate_roles": sum(r["point_adequate"] for r in roles),
                  "models_with_both_roles_point_adequate": sum(all(r["point_adequate"] for r in roles if r["model"] == index) for index in range(5)),
                  "formal_support_assessed": False}
        old = next(r for r in nd_summary["masks"]["methods"] if r["method"] == method)
        mapping = {"mean_mae": "mean_mae", "mean_near_disagreement": "mean_near_disagreement", "mean_far_disagreement": "mean_far_disagreement", "point_adequate_roles": "roles_meeting_all_error_and_decision_point_thresholds", "models_with_both_roles_point_adequate": "models_with_both_roles_meeting_point_thresholds"}
        if any(result[a] != old[b] for a, b in mapping.items()):
            raise ValueError("Diagnostic recount differs from the preserved core summary.")
        masks.append(result)

    process_costs = []
    for study, directory in (("F15", "v2/work_logs/F15_2026-10-04_S1/commands"), ("F15-ND01", "v2/work_logs/F15_ND01_2026-10-05_S1/commands")):
        for stage in ("prepare", "evaluate"):
            name = f"{directory}/{stage}_attempt1.end.json"
            record = sources.read(name)
            process_costs.append({"study": study, "stage": stage, "source_path": name,
                                  "record": record})
    return {
        "schema": "F17-report-tables-v1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "scope": "Deterministic assembly and recount of preserved records; no new populations, fitting, experimental evaluation, confidence intervals, or dynamic F17 accounting.",
        "builder": {"path": Path(__file__).relative_to(ROOT).as_posix(), "sha256": digest(Path(__file__).read_bytes())},
        "source_manifest": [sources.records[name] for name in sorted(sources.records)],
        "freeze_bindings": {"F14_manifest_sha256": sources.records["v2/experiments/freeze.v1.json"]["sha256"], "F14_registered_files": len(freeze["files"]), "ND01_manifest_sha256": sources.records["v2/experiments/neural_diagnostic_v1/freeze.json"]["sha256"], "ND01_registered_files": len(diagnostic_freeze["files"])},
        "retention": {"denominators_and_totals": totals, "method_rows": rows,
                      "prospective_usefulness_met": assessment["bounded_application_criterion_met"],
                      "resource_units": "Fields ending _ns are measured nanoseconds; fields ending _bytes are serialized byte counts. Other fields count source calls, fields or world/order path executions. Substage times are nested, not additive to parent times.",
                      "scope": "Sixteen stipulated initial populations; ten dependent revisions each. Equal-information comparisons reproduce ordinary optimization; no general speed, exclusive-power or workload-generalization claim."},
        "original_neural": original_neural,
        "diagnostic_neural": {"development_only": True, "new_ordinary_training_steps": 0,
                              "calibration": {"constructed_function_equivalent_layouts": 5, "ordinary_training_replications": 0, "complete_identity_layouts": calibration["supported_prespecified_replicates"], "adequate_identity_layouts": sum(m["hypotheses"]["identity"]["adequate"] for m in calibration["models"]), "confidence_rows": nd_summary["calibration"]["status_counts_by_hypothesis_and_category"], "control_rows": nd_summary["calibration"]["control_status_counts"]},
                              "intervention_family_rows": masks, "optimization": nd_summary["masks"]["optimization_summary"],
                              "weighting": "Equal five strata within role, equal two roles within model, equal five fixed ordinary models.",
                              "point_adequacy": "All five role MAEs <= .05, near disagreement <= .35, far disagreement <= .10; no confidence bounds or complete control/scale conjunction.",
                              "interpretation": "Ordinary prediction training supplies no task-specific reason for one clean eight-neuron block per expected cost. Search and intervention-family limitations are supported locally; technical superposition and joint or unique utility representation remain unestablished."},
        "historical_process_cost_records": process_costs,
        "preservation_note": "The original zero-byte F15 retention aggregate is preserved as F15-ART-01. This export reads the 160 original hash-valid unit files, not that damaged aggregate. Gate C's prior recount and the separately preserved byte-exact aggregate recovery retain its disposition.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare existing fixed output without writing.")
    args = parser.parse_args()
    payload = canonical(build())
    if args.check:
        if OUTPUT.read_bytes() != payload:
            raise ValueError("F17 tables differ; existing output was not changed.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        with OUTPUT.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    print(json.dumps({"status": "checked" if args.check else "created_exclusively",
                      "path": OUTPUT.relative_to(ROOT).as_posix(), "bytes": len(payload),
                      "sha256": digest(payload), "scientific_execution": False}, sort_keys=True))


if __name__ == "__main__":
    main()
