"""Reproduce descriptive F15 report tables from saved, hash-checked outputs.

Contributor: ChatGPT (GPT-6 Astra Pro), October 4/5, 2026.
This reporting program is outside F14-v1's immutable experimental closure.
It generates no populations, trains no model, selects no alignment, and adds
no confirmatory confidence intervals. All inferential rows are the original
560 frozen rows; added summaries and economic contrasts are descriptive.

Run: python -m v2.experiments.summarize_f15
Check an existing report: python -m v2.experiments.summarize_f15 --check
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import statistics

from . import analysis as A
from . import freeze as F


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUN = ROOT / "v2/work_logs/F15_v1_run1"
DEFAULT_OUT = ROOT / "v2/experiments/F15_v1_analysis"


def read_checked(path):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert Path(str(path) + ".sha256").read_text().strip() == digest, path
    return F.load_json(path)


def exact_mean(values):
    values = list(values)
    return str(sum((Q(x) for x in values), Q(0)) / len(values)) if values else None


def numeric_stats(values):
    values = list(values)
    if not values:
        return {"n": 0}
    return {"n": len(values), "minimum": min(values), "maximum": max(values),
            "sum": sum(values), "mean": statistics.mean(values),
            "median": statistics.median(values)}


def interval_rows(assessment, config):
    rows = {}

    def visit(value):
        if isinstance(value, dict):
            if {"id", "mean", "n", "sample_range", "lower", "upper", "radius"} <= value.keys():
                if value["id"] in rows:
                    assert rows[value["id"]] == value
                rows[value["id"]] = value
            for item in value.values():
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(assessment)
    assert len(rows) == config["analysis"]["maximum_interval_rows"] == 560
    output = []
    for key, original in sorted(rows.items()):
        row = dict(original)
        if key.endswith("separating_frequency"):
            kind, threshold, family = "minimum", .90, "separating_frequency"
        elif key.endswith("advantage"):
            kind, threshold = "minimum", .01
            family = "same_subset_scale_advantage" if "same_identity_subset" in key else "matched_control_advantage"
        elif key.endswith("base_normalized_regret"):
            kind, threshold, family = "maximum", .05 / 1.375, "ordinary_task_regret"
        elif key.endswith("disagreement"):
            kind, threshold, family = "maximum", (.35 if "/mixed_near/" in key else .10), "intervention_decision"
        else:
            kind, threshold = "maximum", .05
            family = "conditional_base_mae" if "/conditional_base/" in key else (
                "ordinary_task_mae" if key.endswith("/base_mae") else "intervention_mae")
        support = row["upper"] <= threshold if kind == "maximum" else row["lower"] >= threshold
        violation = row["lower"] > threshold if kind == "maximum" else row["upper"] < threshold
        row.update(criterion_kind=kind, threshold=threshold, statistic_family=family,
                   support=support, violation=violation,
                   disposition="supported" if support else "violated" if violation else "inconclusive")
        output.append(row)
    return output


RESOURCE_FIELDS = (
    "retained_payload_bytes", "resident_bytes", "cached_source_context_bytes", "cached_proof_bytes",
    "external_archive_bytes", "resident_plus_archive_bytes", "current_source_context_bytes",
    "current_proof_bytes", "current_update_metadata_bytes", "schema_bytes",
    "active_serialized_upper_bytes", "total_stored_serialized_upper_bytes",
    "initial_with_supplied_source_serialized_upper_bytes", "peak_serialized_working_state_upper_bytes",
    "initial_production_ns", "initial_native_production_and_check_ns", "initial_total_ns",
    "source_archive_production_ns", "acquisition_ns", "update_and_solve_ns", "decision_ns",
    "current_context_production_ns", "current_native_protocol_ns", "one_update_arithmetic_ns",
    "one_update_total_ns", "one_case_method_plus_common_ns", "acquisition_calls",
    "acquisition_scalar_measurements", "acquisition_path_world_executions", "acquisition_transferred_bytes",
    "basis_checks", "fiber_equation_rank", "fiber_vertex_count", "peak_basis_candidates",
    "stored_feasible_basis_count", "inverse_rational_cells_per_basis", "native_source_rows",
)


def summarize_retention(rows, paired):
    numeric = Counter(a["status"] for r in rows for a in r["numeric"])
    decisions = Counter(r["decision_status"] for r in rows)
    resources = {key: numeric_stats(r["resources"][key] for r in rows) for key in RESOURCE_FIELDS}
    means = {}
    for charge in ("0", "1/20", "1/2"):
        cells = [next(x for x in r["acquisition_sensitivity"] if x["per_scalar_measurement_cost"] == charge) for r in rows]
        means[charge] = {
            "decision_plus_current_acquisition": exact_mean(x["decision_plus_acquisition_loss"] for x in cells),
            "initial_plus_decision_plus_current_acquisition": exact_mean(x["horizon_decision_plus_source_loss"]["1"] for x in cells),
            "initial_common_source_charge": exact_mean(x["initial_common_source_loss"] for x in cells),
            "current_common_source_charge": exact_mean(x["current_common_source_loss"] for x in cells),
            "method_specific_acquisition_charge": exact_mean(x["method_specific_acquisition_loss"] for x in cells),
            "horizon_means": {str(h): exact_mean(x["horizon_decision_plus_source_loss"][str(h)] for x in cells) for h in (1, 4, 16, 64)},
        }
    quality_keys = ("quality_vector_equal_to_fresh", "both_admit_all_numeric_queries_and_certify_decision",
                    "both_receive_selected_order_proof", "both_admit_numeric_decision_and_selected_order_proof")
    return {
        "method_rows": len(rows), "numeric_queries": len(rows)*6,
        "numeric": {s: numeric[s] for s in ("exact", "approximate", "refused")},
        "decisions": {s: decisions[s] for s in ("certified_order", "certified_fallback", "refusal_to_fallback")},
        "native": dict(Counter(r["native"]["status"] for r in rows)),
        "cache": dict(Counter(r["native"]["cache"] for r in rows)),
        "useful_native_rows": sum(r["native"]["useful_derivation_candidate"] for r in rows),
        "full_law_valid_but_retained_fiber_invalid": sum(r["scoring"]["full_source_semantic_valid"] and not r["native"]["semantic_valid"] for r in rows),
        "approximate_selected_cost_with_certified_order": sum(r["decision_status"] == "certified_order" and r["numeric"][r["executed_index"]]["status"] == "approximate" for r in rows),
        "mean_actual_cost": exact_mean(r["scoring"]["actual_executed_cost"] for r in rows),
        "mean_actual_regret": exact_mean(r["scoring"]["realized_regret"] for r in rows),
        "max_actual_regret": str(max(Q(r["scoring"]["realized_regret"]) for r in rows)),
        "actual_regret_exceeds_tolerance": sum(Q(r["scoring"]["realized_regret"]) > Q(1,20) for r in rows),
        "acquisition_scalar_histogram": dict(Counter(str(r["resources"]["acquisition_scalar_measurements"]) for r in rows)),
        "resources": resources, "acquisition_sensitivity_mean": means,
        "paired_quality_counts": {key: sum(r[key] for r in paired) for key in quality_keys},
    }


def analyze(run):
    config = F.load_json(F.DEFAULT_CONFIG)
    freeze = F.bound_configuration(config)
    preparation = read_checked(run / "preparation_complete.json")
    evaluation = read_checked(run / "evaluation_complete.json")
    assert preparation["freeze"] == evaluation["freeze"] == freeze
    assert evaluation["preparation_manifest_sha256"] == F.file_digest(run / "preparation_complete.json")
    assert preparation["completed_utc"] < evaluation["started_utc"]
    assert evaluation["status"] == "evaluation_complete"
    folder = run / f"evaluation_attempt_{evaluation['attempt']}"
    # A post-run integrity audit found this one aggregate empty. All 160
    # exclusive per-case artifacts remain valid, and their canonical assembly
    # reproduces the aggregate's ORIGINAL sidecar exactly. Preserve the damaged
    # primary file; use the original units, with the recovery explicitly reported.
    aggregate = folder / "retention_results.json"
    cases = [read_checked(next(run.glob(f"evaluation_attempt_*/retention_{seed}_{variant}.json")))
             for seed in config["retention"]["evaluation_seeds"]
             for variant in config["retention"]["variants"]]
    original_aggregate_sha256 = Path(str(aggregate)+".sha256").read_text().strip()
    assert F.digest_bytes(F.canonical_bytes(cases)) == original_aggregate_sha256
    aggregate_intact = F.file_digest(aggregate) == original_aggregate_sha256
    if not aggregate_intact:
        assert aggregate.stat().st_size == 0, "Unexpected additional aggregate corruption"
    recovery = {"original_file":str(aggregate.relative_to(ROOT)),
                "original_file_intact":aggregate_intact,"observed_bytes":aggregate.stat().st_size,
                "observed_sha256":F.file_digest(aggregate),
                "original_sidecar_sha256":original_aggregate_sha256,
                "reconstructed_bytes":len(F.canonical_bytes(cases)),
                "all_160_individual_units_hash_valid":True,
                "exact_reconstruction_matches_original_sidecar":True,
                "original_file_overwritten":False,"new_generation_or_stage_retry":False}
    ra = read_checked(run / evaluation["retention_assessment_file"])
    neural = [read_checked(next(run.glob(f"evaluation_attempt_*/model_{i}_evaluation.json"))) for i in range(5)]
    na = read_checked(run / evaluation["neural_assessment_file"])
    models = [read_checked(run / m["file"]) for m in preparation["models"]]
    for i, model in enumerate(models):
        F.validate_prepared(model, config, config["neural"]["model_seeds"][i])
        assert neural[i]["discovery_artifact_hash"] == model["artifact_hash"]
    # Reanalysis, not repeated evaluation: the functions consume saved statistics.
    assert F.canonical_bytes(A.retention_assessment(cases, config)) == F.canonical_bytes(ra)
    assert F.canonical_bytes(A.neural_assessment(neural, config)) == F.canonical_bytes(na)
    assert len(cases) == 160
    rows = [dict(item, seed=case["seed"], variant=case["variant"]) for case in cases for item in case["methods"]]
    assert len(rows) == 1920
    paired = ra["paired_resource_and_decision_comparisons"]
    by_method, by_variant = [], []
    for access in config["retention"]["access_regimes"]:
        for method in config["retention"]["methods"]:
            selected = [r for r in rows if (r["access"], r["method"]) == (access, method)]
            comparisons = [r for r in paired if (r["access"], r["method"]) == (access, method)]
            by_method.append(dict(access=access, method=method, **summarize_retention(selected, comparisons)))
            for variant in config["retention"]["variants"]:
                by_variant.append(dict(access=access, method=method, variant=variant,
                    **summarize_retention([r for r in selected if r["variant"] == variant],
                                         [r for r in comparisons if r["variant"] == variant])))
    # Honest accounting: common generation appears once physically, while each
    # hypothetical method service receives the same common charge in comparisons.
    physical_common_ns = sum(c["common_input_accounting"]["observed_common_production_ns"] for c in cases)
    method_stage_ns = sum(r["resources"]["initial_total_ns"] + r["resources"]["one_update_total_ns"] for r in rows)
    for case in cases:
        common = case["common_input_accounting"]["observed_common_production_ns"]
        for r in case["methods"]:
            q = r["resources"]
            assert q["one_case_method_plus_common_ns"] == common + q["initial_total_ns"] + q["one_update_total_ns"]
            assert q["one_update_total_ns"] == q["one_update_arithmetic_ns"] + q["current_context_production_ns"] + q["current_native_protocol_ns"]
            assert q["resident_bytes"] == q["retained_payload_bytes"] + q["cached_source_context_bytes"] + q["cached_proof_bytes"]
            assert q["resident_plus_archive_bytes"] == q["resident_bytes"] + q["external_archive_bytes"]
    lookup = {(r["seed"], r["variant"], r["method"], r["access"]): r for r in rows}
    pair_lookup = {(r["seed"], r["variant"], r["method"], r["access"]): r for r in paired}
    economics, projections = [], []
    for case in cases:
        seed, variant = case["seed"], case["variant"]
        for method in config["retention"]["methods"]:
            no = lookup[seed,variant,method,"no_reacquisition"]
            yes = lookup[seed,variant,method,"adaptive_reacquisition"]
            fields = yes["resources"]["acquisition_scalar_measurements"]
            gain = Q(no["scoring"]["actual_executed_cost"]) - Q(yes["scoring"]["actual_executed_cost"])
            economics.append({"seed":seed,"variant":variant,"method":method,
                "acquired_scalar_fields":fields,"observed_decision_loss_reduction":str(gain),
                "observed_decision_only_break_even_price_per_scalar":str(gain/fields) if fields else None,
                "retained_decision_was_already_certified":not no["refused"],
                "retained_numeric_refusals":no["pre_repair"]["numeric_refusals"],
                "executed_order_changed":no["executed"] != yes["executed"],
                "net_reduction_at_registered_prices":{p:str(gain-Q(p)*fields) for p in config["retention"]["acquisition_costs"]},
                "scope":"descriptive paired action losses and registered charges; numerical-answer utility and archive/CPU cost not monetized"})
        for b in case["break_even"]:
            row = lookup[seed,variant,b["method"],b["access"]]
            fresh = lookup[seed,variant,"fresh",b["access"]]
            quality = pair_lookup[seed,variant,b["method"],b["access"]]
            projections.append(dict(b, seed=seed, variant=variant,
                quality_vector_equal_to_fresh=quality["quality_vector_equal_to_fresh"],
                both_admit_numeric_decision_and_selected_order_proof=quality["both_admit_numeric_decision_and_selected_order_proof"],
                arithmetic_horizon_wins={str(h):row["resources"]["horizon_arithmetic_ns"][str(h)] < fresh["resources"]["horizon_arithmetic_ns"][str(h)] for h in config["retention"]["horizons"]}))
    intervals = interval_rows(na, config)
    model_summary, interventions = [], []
    for i,(prepared,result,assessed) in enumerate(zip(models,neural,na["models"])):
        local = [r for r in intervals if r["id"].startswith(f"model{i}/")]
        identity_mae = [r for r in local if r["statistic_family"] == "intervention_mae" and "/identity/" in r["id"]]
        model_summary.append({"index":i,"discovery_seed":prepared["discovery_seed"],"evaluation_seed":result["evaluation_seed"],
            "disposition":assessed["disposition"],"task_ready":assessed["task_ready"],
            "numerical_controls_valid":assessed["numerical_controls_valid"],"task":result["task"],
            "base_probability_interval":assessed["base_probability_interval"],
            "base_regret_upper_task_units":assessed["base_normalized_regret_interval"]["upper"]*1.375,
            "identity_mae_mean_range":[min(x["mean"] for x in identity_mae),max(x["mean"] for x in identity_mae)],
            "identity_mae_interval_dispositions":dict(Counter(x["disposition"] for x in identity_mae)),
            "identity_selected_subsets":[r["subset"] for r in prepared["alignments"]["identity/aligned"]["roles"]],
            "discovery_selected_alternative":result["selected_alternative"],"hypotheses":assessed["hypotheses"],
            "same_subset_scale_tests":assessed["same_subset_scale_tests"],"composition":result["composition"],
            "gauges":result["gauges_by_g"],"evaluation_data_hashes":result["evaluation_data_hashes"],
            "training_resource":prepared["training"],"discovery_resource":prepared["resource"],"evaluation_resource":result["resource"]})
        for name, alignment in result["alignments"].items():
            for role, cells in enumerate(alignment["roles"]):
                for stratum, metrics in cells.items():
                    interventions.append(dict(model=i,discovery_seed=prepared["discovery_seed"],evaluation_seed=result["evaluation_seed"],
                        alignment=name,role=role,stratum=stratum,subset_overlap=alignment["overlap"],
                        observational_decoder_nrmse=alignment["observational_decoder_nrmse"][role],
                        log_contribution_rmse=alignment["log_contribution_rmse"][role],**metrics))
    assert len(interventions) == 1000
    summary = {
        "schema":"F15-descriptive-summary-v1","freeze":freeze,
        "primary_run":str(run.relative_to(ROOT)),"evaluation_completed_utc":evaluation["completed_utc"],
        "saved_assessments_reproduce_exactly":True,"new_population_generation":False,
        "new_confirmatory_intervals":0,"original_interval_rows":len(intervals),
        "aggregate_recovery":recovery,
        "retention":{k:v for k,v in ra.items() if k not in ("paired_resource_and_decision_comparisons","equal_information_control_comparisons")},
        "retention_aggregate":summarize_retention(rows,paired),
        "retention_physical_common_generation_seconds":physical_common_ns/1e9,
        "retention_method_stage_seconds":method_stage_ns/1e9,
        "neural":{"supported_models":na["supported_prespecified_replicates"],"pilot_support":na["pilot_support_criterion_met"],
            "task_ready_models":sum(m["task_ready"] for m in na["models"]),
            "numerically_valid_models":sum(m["numerical_controls_valid"] for m in na["models"]),
            "all_interval_dispositions":dict(Counter(r["disposition"] for r in intervals)),
            "original_task_examples":sum(n["task"]["n"] for n in neural),
            "intended_intervention_pairs":sum(n["resource"]["pair_examples"] for n in neural),
            "incorrect_donor_pairs":sum(n["resource"]["pair_examples"] for n in neural),
            "alignment_role_pair_evaluations":sum(n["resource"]["alignment_role_pair_evaluations"] for n in neural),
            "binary_training_labels":sum(m["training"]["stochastic_outcome_labels"] for m in models),
            "expected_cost_training_labels":sum(m["training"]["expected_cost_training_labels"] for m in models),
            "candidate_evaluations":sum(m["resource"]["candidate_evaluations"] for m in models)},
        "primary_stage_resources":{"preparation":{k:preparation[k] for k in ("attempt","observed_wall_seconds","observed_cpu_seconds")},
                                   "evaluation":{k:evaluation[k] for k in ("attempt","observed_wall_seconds","observed_cpu_seconds")}},
        "interpretation":"Task execution and reporting, scoped application support, neural support, and contribution distinctiveness are separate dispositions."
    }
    outputs = {"summary.json":summary,"retention_by_method.json":by_method,"retention_by_variant.json":by_variant,
               "retention_acquisition_economics.json":economics,"retention_horizon_comparisons.json":projections,
               "neural_models.json":model_summary,"neural_interventions.json":interventions,"neural_interval_rows.json":intervals}
    inputs = []
    for path in sorted(run.rglob("*.json")):
        if path != aggregate or aggregate_intact:
            read_checked(path)
        inputs.append({"file":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,"sha256":F.file_digest(path),
                       "integrity":"empty; recovered exactly from original units" if path == aggregate and not aggregate_intact else "sidecar_verified"})
    outputs["input_manifest.json"] = {"schema":"F15-report-input-manifest-v1","freeze":freeze,"files":inputs}
    return outputs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run",type=Path,default=DEFAULT_RUN)
    parser.add_argument("--out",type=Path,default=DEFAULT_OUT)
    parser.add_argument("--check",action="store_true")
    args = parser.parse_args(argv)
    outputs = analyze(args.run.resolve())
    args.out.mkdir(parents=True,exist_ok=True)
    manifest = {"schema":"F15-derived-output-manifest-v1",
                "reporting_code_sha256":F.file_digest(Path(__file__)),
                "files":{name:{"bytes":len(F.canonical_bytes(value)),"sha256":F.digest_bytes(F.canonical_bytes(value))} for name,value in outputs.items()}}
    outputs["output_manifest.json"] = manifest
    for name,value in outputs.items():
        path = args.out/name
        if args.check or path.exists():
            assert path.read_bytes() == F.canonical_bytes(value), f"Derived report differs: {path}"
        else:
            F.write_json(path,value,exclusive=True)
    print(json.dumps({"status":"checked" if args.check else "written","files":len(outputs),
                      "retention_application":outputs["summary.json"]["retention"]["bounded_application_criterion_met"],
                      "neural_pilot_support":outputs["summary.json"]["neural"]["pilot_support"],
                      "new_generation":False,"out":str(args.out)},indent=2))


if __name__ == "__main__":
    main()
