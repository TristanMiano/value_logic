"""Summarize completed F15-ND01 artifacts without generating inputs or fitting.

Contributor: ChatGPT (GPT-6 Astra Pro). Uses only Python's standard library.
Default execution creates the four derived outputs exclusively. ``--check``
recomputes their bytes from saved inputs and checks equality without writing.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean


STRATA = ("mixed_near", "mixed_far", "preserve_other", "equal_target", "scale_separating")
HYPOTHESES = ("identity", "inv_eta", "inv_one_minus_eta", "inv_total_cost")
CONTROLS = ("aligned", "random", "permuted_concept", "shuffled_donor", "untrained")
MASK_METHODS = ("fractional_mask", "rounded_top8", "binary_global", "frozen_original")
DEVELOPMENT = "F15-ND01 development diagnostic; original F15 result unchanged"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def close(a, b, message):
    if not math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12):
        raise ValueError(message)


class Inputs:
    def __init__(self, repo):
        self.repo = repo
        self.records = {}

    def read(self, path, require_sidecar=True):
        path = path.resolve()
        data = path.read_bytes()
        identifier = path.relative_to(self.repo).as_posix()
        actual = digest(data)
        sidecar = path.with_suffix(path.suffix + ".sha256")
        if sidecar.exists():
            registered = sidecar.read_text().split()[0]
            if actual != registered:
                raise ValueError(f"Input sidecar mismatch: {identifier}")
            sidecar_record = {"file": sidecar.relative_to(self.repo).as_posix(),
                              "sha256": digest(sidecar.read_bytes())}
        elif require_sidecar:
            raise ValueError(f"Missing input sidecar: {identifier}")
        else:
            sidecar_record = None
        result = json.loads(data)
        if "artifact_hash" in result:
            unhashed = {k: v for k, v in result.items() if k != "artifact_hash"}
            if result["artifact_hash"] != digest(canonical(unhashed)):
                raise ValueError(f"Input internal artifact hash mismatch: {identifier}")
        self.records[identifier] = {"file": identifier, "sha256": actual,
                                    "bytes": len(data), "sidecar": sidecar_record}
        return result

    def source(self, path):
        key = path.resolve().relative_to(self.repo).as_posix()
        return {"source_file": key, "source_sha256": self.records[key]["sha256"]}


def metric_row(metric):
    row = {k: metric.get(k) for k in (
        "n", "mae", "mse", "rmse", "max_absolute_error", "decision_agreement",
        "adjusted_effect_rmse", "expected_effect_rms", "observed_effect_rms",
        "unchanged_target_output_effect_rms", "logit_mse", "logit_rmse")}
    row["decision_disagreement"] = metric.get("decision_disagreement", 1 - metric["decision_agreement"])
    for name in ("base_prediction", "no_swap", "whole_layer_swap"):
        baseline = metric.get(name, {})
        for field in ("mae", "mse", "decision_agreement"):
            row[f"{name}_{field}"] = baseline.get(field)
    return row


def group_metric_rows(rows, method_field):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[method_field]].append(row)
    result = []
    for name, members in sorted(grouped.items()):
        by_role = defaultdict(dict)
        for row in members:
            key = (row["model_index"], row["role"])
            if row["stratum"] in by_role[key]:
                raise ValueError("Duplicate model/role/stratum in a summary group.")
            by_role[key][row["stratum"]] = row
        if len(members) != 50 or len(by_role) != 10:
            raise ValueError("Each method requires all five models, two roles, and five strata.")
        role_rows = []
        for (model, role), strata in sorted(by_role.items()):
            if set(strata) != set(STRATA):
                raise ValueError("Incomplete stratum product.")
            mae_ok = all(strata[s]["mae"] <= .05 for s in STRATA)
            near_ok = strata["mixed_near"]["decision_disagreement"] <= .35
            far_ok = strata["mixed_far"]["decision_disagreement"] <= .10
            normalized = [strata[s]["mae"] / .05 for s in STRATA] + [
                strata["mixed_near"]["decision_disagreement"] / .35,
                strata["mixed_far"]["decision_disagreement"] / .10]
            role_rows.append({
                "model_index": model, "role": role,
                "mean_mae": mean(strata[s]["mae"] for s in STRATA),
                "mean_mse": mean(strata[s]["mse"] for s in STRATA),
                "near_disagreement": strata["mixed_near"]["decision_disagreement"],
                "far_disagreement": strata["mixed_far"]["decision_disagreement"],
                "equal_target_effect_rms": strata["equal_target"]["unchanged_target_output_effect_rms"],
                "worst_stratum_mae": max(strata[s]["mae"] for s in STRATA),
                "max_normalized_error": max(normalized),
                "all_five_mae_point_thresholds_met": mae_ok,
                "near_point_threshold_met": near_ok, "far_point_threshold_met": far_ok,
                "error_and_decision_point_thresholds_met": mae_ok and near_ok and far_ok,
            })
        role_pass = {(r["model_index"], r["role"]): r["error_and_decision_point_thresholds_met"] for r in role_rows}
        record = {
            "method": name, "model_count": 5, "role_count": 10, "cell_count": 50,
            "weighting": "equal five strata within role, equal two roles within model, equal five fixed models",
            "mean_mae": mean(r["mean_mae"] for r in role_rows),
            "mean_mse": mean(r["mean_mse"] for r in role_rows),
            "mean_near_disagreement": mean(r["near_disagreement"] for r in role_rows),
            "mean_far_disagreement": mean(r["far_disagreement"] for r in role_rows),
            "mean_role_equal_target_output_effect_rms": mean(r["equal_target_effect_rms"] for r in role_rows),
            "pooled_role_equal_target_output_effect_rms": math.sqrt(mean(r["equal_target_effect_rms"] ** 2 for r in role_rows)),
            "mean_role_worst_stratum_mae": mean(r["worst_stratum_mae"] for r in role_rows),
            "mean_role_max_normalized_error": mean(r["max_normalized_error"] for r in role_rows),
            "mae_cells_at_most_0_05": sum(r["mae"] <= .05 for r in members),
            "near_roles_at_most_0_35": sum(r["near_point_threshold_met"] for r in role_rows),
            "far_roles_at_most_0_10": sum(r["far_point_threshold_met"] for r in role_rows),
            "roles_meeting_all_error_and_decision_point_thresholds": sum(role_pass.values()),
            "models_with_both_roles_meeting_point_thresholds": sum(role_pass[(m, 0)] and role_pass[(m, 1)] for m in range(5)),
            "role_rows": role_rows,
            "by_stratum": [{"stratum": s,
                            "mean_mae": mean(r["mae"] for r in members if r["stratum"] == s),
                            "mean_mse": mean(r["mse"] for r in members if r["stratum"] == s),
                            "mean_decision_disagreement": mean(r["decision_disagreement"] for r in members if r["stratum"] == s)} for s in STRATA],
            "formal_support_assessed": False,
            "point_thresholds_are_not_complete_F15_endpoint": True,
        }
        if all(r.get("logit_mse") is not None for r in members):
            record["mean_logit_mse"] = mean(r["logit_mse"] for r in members)
        result.append(record)
    return result


def summarize_comparisons(records):
    """Aggregate already saved paired moments; retain every model/role.

    ``records`` is [(model_index, source_identifier, saved_comparison), ...].
    """
    candidate, reference = records[0][2]["candidate"], records[0][2]["reference"]
    roles, cells = [], []
    for model, source, comparison in records:
        if (comparison["candidate"], comparison["reference"]) != (candidate, reference):
            raise ValueError("Mixed comparison identities.")
        for role in comparison["roles"]:
            pooled = role["pooled_equal_strata"]
            close(pooled["sum"] / pooled["n"], pooled["mean_paired_absolute_error_improvement"], "Paired moments mismatch")
            roles.append({"model_index": model, "role": role["role"],
                          "source_file": source, **pooled})
            for s, stats in role["strata"].items():
                cells.append({"model_index": model, "role": role["role"], "stratum": s, **stats})
    if len(roles) != 10 or len(cells) != 50:
        raise ValueError("A paired comparison must retain ten roles and fifty cells.")
    means = [r["mean_paired_absolute_error_improvement"] for r in roles]
    return {
        "candidate": candidate, "reference": reference,
        "positive_improvement_favors": "candidate", "role_count": len(roles),
        "mean_role_paired_mae_improvement": mean(means),
        "minimum_role_mean_improvement": min(means), "maximum_role_mean_improvement": max(means),
        "positive_role_means": sum(v > 0 for v in means),
        "negative_role_means": sum(v < 0 for v in means), "zero_role_means": sum(v == 0 for v in means),
        "role_means_at_least_0_01": sum(v >= .01 for v in means),
        "role_rows": roles,
        "by_stratum": [{"stratum": s,
                        "mean_paired_mae_improvement": mean(r["mean_paired_absolute_error_improvement"] for r in cells if r["stratum"] == s),
                        "positive_role_means": sum(r["mean_paired_absolute_error_improvement"] > 0 for r in cells if r["stratum"] == s)} for s in STRATA],
        "formal_support_assessed": False,
        "scope": "descriptive comparisons of fixed-model development results; no original F15 familywise inference applied",
    }


def pooled_moments(cells):
    n, total, squares = sum(c["n"] for c in cells), sum(c["sum"] for c in cells), sum(c["sum_squares"] for c in cells)
    return {"n": n, "sum": total, "sum_squares": squares,
            "mean_paired_absolute_error_improvement": total / n,
            "sample_variance": max(0., (squares - total * total / n) / (n - 1)),
            "minimum": min(c["minimum"] for c in cells), "maximum": max(c["maximum"] for c in cells)}


def calibration_intervals(assessment):
    records = {}

    def add(row, direction, threshold, category, layout, hypothesis=None, role=None, stratum=None, control=None):
        status = ("supported" if row["upper"] <= threshold else "violated" if row["lower"] > threshold else "inconclusive") if direction == "at_most" else (
            "supported" if row["lower"] >= threshold else "violated" if row["upper"] < threshold else "inconclusive")
        value = {**row, "layout_index": layout, "hypothesis": hypothesis, "role": role,
                 "stratum": stratum, "control": control, "direction": direction,
                 "threshold": threshold, "category": category, "status": status,
                 "development_only": True, "ordinary_trained_evidence": False}
        if row["id"] in records and records[row["id"]] != value:
            raise ValueError("Duplicate calibration interval has inconsistent interpretation.")
        records[row["id"]] = value

    for i, model in enumerate(assessment["models"]):
        add(model["base_probability_interval"], "at_most", .05, "base_probability", i)
        add(model["base_normalized_regret_interval"], "at_most", .05 / 1.375, "base_normalized_regret", i)
        for role, r in enumerate(model["hypotheses"]["identity"]["roles"]):
            for stratum, row in r["conditional_base"].items():
                add(row, "at_most", .05, "conditional_base", i, role=role, stratum=stratum)
        for hypothesis, h in model["hypotheses"].items():
            for role, r in enumerate(h["roles"]):
                for stratum, row in r["absolute"].items():
                    add(row, "at_most", .05, "intervention_mae", i, hypothesis, role, stratum)
                for stratum, row in r["decisions"].items():
                    add(row, "at_most", .35 if stratum == "mixed_near" else .10,
                        "decision_disagreement", i, hypothesis, role, stratum)
                for control, row in r["control_advantages"].items():
                    add(row, "at_least", .01, "matched_control_advantage", i, hypothesis, role, control=control)
        for hypothesis, roles in model["same_subset_scale_tests"].items():
            for role, r in enumerate(roles):
                add(r["frequency"], "at_least", .90, "same_subset_scale_frequency", i, hypothesis, role)
                add(r["advantage"], "at_least", .01, "same_subset_scale_advantage", i, hypothesis, role)
    if len(records) != 560 or assessment["actual_interval_rows"] != 560:
        raise ValueError("Expected exactly the original 560 calibration interval rows.")
    return [records[k] for k in sorted(records)]


def status_counts(rows):
    counts = Counter(r["status"] for r in rows)
    return {"n": len(rows), **{s: counts[s] for s in ("supported", "inconclusive", "violated")}}


def csv_bytes(rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=keys, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: json.dumps(v, separators=(",", ":"), allow_nan=False)
                         if isinstance(v, (dict, list)) else v for k, v in row.items()})
    return output.getvalue().encode()


def build(repo, run):
    inputs = Inputs(repo)
    evaluation_complete = inputs.read(run / "evaluation_complete.json")
    if evaluation_complete.get("status") != "evaluation_complete" or len(evaluation_complete["units"]) != 15:
        raise ValueError("All fifteen evaluations must be complete before this reporting script reads their outcomes.")
    preparation_complete = inputs.read(run / "preparation_complete.json")
    exposure = inputs.read(run / "evaluation_exposure.json")
    cfg = inputs.read(repo / "v2/experiments/neural_diagnostic_v1/config.json", False)
    freeze = inputs.read(repo / "v2/experiments/neural_diagnostic_v1/freeze.json", False)
    old_assessment = inputs.read(repo / "v2/work_logs/F15_v1_run1/evaluation_attempt_1/neural_assessment.json")
    eval_paths = {(u["kind"], u["index"]): run / u["file"] for u in evaluation_complete["units"]}
    prep_paths = {(u["kind"], u["index"]): run / u["file"] for u in preparation_complete["units"]}
    evaluations, preparations = {}, {}
    for kind, i in itertools.product(("calibration", "search", "soft_mask"), range(5)):
        evaluations[(kind, i)] = inputs.read(eval_paths[(kind, i)])
        preparations[(kind, i)] = inputs.read(prep_paths[(kind, i)])
        expected_prep = evaluations[(kind, i)].get("prepared_artifact_hash", evaluations[(kind, i)].get("discovery_artifact_hash"))
        if expected_prep != preparations[(kind, i)]["artifact_hash"]:
            raise ValueError("Evaluation/preparation binding mismatch.")
    assessment_path = run / evaluation_complete["calibration_assessment"]["file"]
    assessment = inputs.read(assessment_path)
    search_rows, mask_rows, calibration_rows = [], [], []
    search_comparison_groups = {k: defaultdict(list) for k in ("matched_controls", "budgets", "selectors", "families")}
    mask_comparison_groups = defaultdict(list)
    optimization_rows, task_rows, calibration_oracle_rows, provenance_checks = [], [], [], []
    original_mask_lookup = {}
    for i in range(5):
        search, mask = evaluations[("search", i)], evaluations[("soft_mask", i)]
        sp, mp = preparations[("search", i)], preparations[("soft_mask", i)]
        if search["validation_data_hashes"]["role_pairs"] != mask["validation_pair_hashes"]:
            raise ValueError("Search and mask diagnostics must use identical validation arrays.")
        if sp["selection_data_hashes"]["role_pairs"] != mp["discovery_pair_hashes"]:
            raise ValueError("Search and mask diagnostics must use identical discovery arrays.")
        if search["network_hash"] != mask["original_network_hash"]:
            raise ValueError("Search and mask diagnostics must retain the identical original network.")
        provenance_checks.append({"model_index": i, "identical_search_mask_discovery_pairs": True,
                                  "identical_search_mask_validation_pairs": True, "identical_original_network": True})
        source = inputs.source(eval_paths[("search", i)])
        task_rows.append({"model_index": i, "model_seed": search["source_model_seed"], **source,
                          "new_development_task_metrics": search["task"],
                          "original_F15_task_ready": old_assessment["models"][i]["task_ready"],
                          "original_F15_disposition": old_assessment["models"][i]["disposition"],
                          "new_development_point_task_mae_and_regret_thresholds_met": search["task"]["mae"] <= .05 and search["task"]["mean_decision_regret"] <= .05,
                          "no_new_task_confidence_assessment": True})
        for name, evaluated in sorted(search["evaluated"].items()):
            selected = sp["alignments"][name]
            for role in (0, 1):
                for stratum in STRATA:
                    metric = evaluated["roles"][role][stratum]
                    row = {"evidence": DEVELOPMENT, **source, "model_index": i,
                           "model_seed": search["source_model_seed"], "validation_seed": search["validation_seed"],
                           "variant": name, "family": evaluated["family"], "budget": evaluated["budget"],
                           "selector": evaluated["selector"], "role": role, "stratum": stratum,
                           **metric_row(metric), "selected_subset": selected["roles"][role]["subset"],
                           "selected_candidate_index": selected["roles"][role]["selected_index"],
                           "discovery_probability_mse": selected["roles"][role]["selection_score"]["probability_mse"],
                           "discovery_robust_max_normalized_error": selected["roles"][role]["selection_score"]["robust_max_normalized_error"],
                           "observational_decoder_nrmse": evaluated["observational_decoder_nrmse"][role],
                           "observational_log_contribution_rmse": evaluated["observational_log_contribution_rmse"][role]}
                    search_rows.append(row)
        for name, controls in search["matched_control_comparisons"].items():
            for control, comparison in controls.items():
                search_comparison_groups["matched_controls"][f"{name}/versus_{control}"].append((i, source["source_file"], comparison))
        for source_key, category in (("budget_comparisons", "budgets"), ("selector_comparisons", "selectors"), ("family_comparisons", "families")):
            for name, comparison in search[source_key].items():
                search_comparison_groups[category][name].append((i, source["source_file"], comparison))
        mask_source = inputs.source(eval_paths[("soft_mask", i)])
        for row in mask["rows"]:
            mask_rows.append({"evidence": DEVELOPMENT, **mask_source,
                              "model_index": i, "model_seed": mp["original_model_seed"],
                              "validation_seed": mask["validation_seed"], "method": row["method"],
                              "role": row["role"], "stratum": row["stratum"], **metric_row(row),
                              "output_hash": row["output_hash"]})
            if row["method"] == "frozen_original":
                original_mask_lookup[(i, row["role"], row["stratum"])] = row
        for comparator in ("rounded_top8", "binary_global", "frozen_original"):
            roles = []
            for role in (0, 1):
                cells = {r["stratum"]: r for r in mask["paired_comparisons"] if r["comparator"] == comparator and r["role"] == role}
                roles.append({"role": role, "strata": cells, "pooled_equal_strata": pooled_moments(list(cells.values()))})
            comparison = {"candidate": "fractional_mask", "reference": comparator, "roles": roles}
            mask_comparison_groups[comparator].append((i, mask_source["source_file"], comparison))
        for role, fitted in enumerate(mp["roles"]):
            binary, cert, optimizer = fitted["binary_global"], fitted["certificate"], fitted["optimizer"]
            optimization_rows.append({
                "model_index": i, "role": role, **inputs.source(prep_paths[("soft_mask", i)]),
                "fractional_mask": fitted["mask"], "rounded_subset": fitted["rounded_subset"],
                "original_subset": fitted["original_subset"], "binary_subset": binary["subset"],
                "fractional_discovery_logit_mse": fitted["discovery_objective"],
                "fractional_numerical_lower_bound": cert["relaxed_optimum_lower_bound"],
                "fractional_numerical_upper_bound": cert["relaxed_optimum_upper_bound"],
                "fractional_duality_gap": cert["duality_gap"],
                "optimizer_iterations": optimizer["iterations"],
                "optimizer_converged_to_declared_gap": optimizer["duality_gap_converged"],
                "binary_discovery_logit_mse": binary["direct_discovery_logit_mse"],
                "binary_minus_fractional_discovery_logit_mse": binary["direct_discovery_logit_mse"] - fitted["discovery_objective"],
                "binary_enumerated_subsets": binary["enumerated_subsets"],
                "binary_unpruned_full_enumeration": binary["unpruned_full_enumeration"],
                "binary_recomputation_discrepancy": binary["maximum_objective_recomputation_discrepancy"],
                "discovery_matrix_hash": fitted["discovery_matrix_hash"],
                "binary_native_resource": binary["resource"],
                "scope": "finite discovery logit objective in float64; neither a probability-error optimum nor an unseen-population bound",
            })
        calibration = evaluations[("calibration", i)]
        cal_source = inputs.source(eval_paths[("calibration", i)])
        for name, alignment in sorted(calibration["alignments"].items()):
            for role in (0, 1):
                for stratum in STRATA:
                    calibration_rows.append({"evidence": "constructed calibration development; no ordinary-trained replicate claim",
                                             **cal_source, "row_type": "searched_alignment", "layout_index": i,
                                             "evaluation_seed": calibration["evaluation_seed"], "alignment": name,
                                             "hypothesis": alignment["g_id"], "control": alignment["control"],
                                             "role": role, "stratum": stratum,
                                             **metric_row(alignment["roles"][role][stratum])})
        for oracle in calibration["oracle_known_subset_accuracy"]["rows"]:
            record = {"evidence": "known-by-construction subset oracle; complete endpoint not assessed",
                      **cal_source, "row_type": "known_subset_oracle", "layout_index": i,
                      "evaluation_seed": calibration["evaluation_seed"], "alignment": "identity/known_subset_oracle",
                      "hypothesis": "identity", "control": "known_subset_oracle", "role": oracle["role"],
                      "stratum": oracle["stratum"], **metric_row(oracle["metrics"]),
                      "known_subset": oracle["known_subset"],
                      "uniform_probability_error_bound": oracle["uniform_probability_error_bound"],
                      "uniform_bound_satisfied": oracle["uniform_bound_satisfied"],
                      "searched_subset_matches_known_subset": oracle["searched_subset_matches_known_subset"],
                      "searched_minus_oracle_mae": oracle["searched_minus_oracle_mae"]}
            record["unchanged_target_output_effect_rms"] = oracle["unchanged_target_output_effect_rms"]
            calibration_rows.append(record)
            calibration_oracle_rows.append(record)
    if (len(search_rows), len(mask_rows), len(calibration_rows)) != (1000, 200, 1050):
        raise ValueError("Unexpected complete Cartesian row counts.")
    search_summary, mask_summary = group_metric_rows(search_rows, "variant"), group_metric_rows(mask_rows, "method")
    search_vs_original = []
    for summary in search_summary:
        role_differences = []
        for i, role in itertools.product(range(5), (0, 1)):
            selected_rows = [r for r in search_rows if r["variant"] == summary["method"] and r["model_index"] == i and r["role"] == role]
            differences = {r["stratum"]: original_mask_lookup[(i, role, r["stratum"])]["mae"] - r["mae"] for r in selected_rows}
            for row in selected_rows:
                original = original_mask_lookup[(i, role, row["stratum"])]
                for baseline in ("base_prediction", "no_swap", "whole_layer_swap"):
                    close(row[f"{baseline}_mae"], original[baseline]["mae"], "Shared-array baseline mismatch")
            role_differences.append({"model_index": i, "role": role, "mean_paired_mae_improvement": mean(differences.values()),
                                     "stratum_mean_differences": differences})
        improvements = [r["mean_paired_mae_improvement"] for r in role_differences]
        search_vs_original.append({"candidate": summary["method"], "reference": "frozen_original_on_same_ND01_validation_arrays",
                                   "mean_role_paired_mae_improvement": mean(improvements),
                                   "positive_role_means": sum(v > 0 for v in improvements),
                                   "negative_role_means": sum(v < 0 for v in improvements),
                                   "role_rows": role_differences,
                                   "available_statistic": "paired mean from differences of saved means; no paired variance reconstructed",
                                   "formal_support_assessed": False})
    intervals = calibration_intervals(assessment)
    calibration_models = []
    for i, model in enumerate(assessment["models"]):
        calibration_models.append({"layout_index": i, "evaluation_seed": model["evaluation_seed"],
            "task_ready": model["task_ready"], "numerical_controls_valid": model["numerical_controls_valid"],
            "disposition": model["disposition"],
            "hypotheses": {g: {"adequate": h["adequate"], "selective": h["selective"],
                                "roles": [{"absolute_and_decision_criteria": r["absolute_and_decision_criteria"],
                                           "matched_control_specificity": r["matched_control_specificity"]} for r in h["roles"]]}
                           for g, h in model["hypotheses"].items()},
            "scale_distinguished": {g: [r["distinguished"] for r in roles] for g, roles in model["same_subset_scale_tests"].items()},
            "composition": model["composition"],
            "task": evaluations[("calibration", i)]["task"]})
    baseline_rows = []
    for i, role, stratum in itertools.product(range(5), (0, 1), STRATA):
        row = original_mask_lookup[(i, role, stratum)]
        baseline_rows.append({"model_index": i, "role": role, "stratum": stratum,
                              **{name: row[name] for name in ("base_prediction", "no_swap", "whole_layer_swap")}})
    baseline_summary = {name: {"mean_mae": mean(r[name]["mae"] for r in baseline_rows),
                               "by_stratum": [{"stratum": s, "mean_mae": mean(r[name]["mae"] for r in baseline_rows if r["stratum"] == s)} for s in STRATA]}
                        for name in ("base_prediction", "no_swap", "whole_layer_swap")}
    csv_outputs = {"search_rows.csv": csv_bytes(search_rows), "mask_rows.csv": csv_bytes(mask_rows),
                   "calibration_rows.csv": csv_bytes(calibration_rows)}
    summary = {
        "schema": "f15-nd01-complete-saved-output-summary-v1", "development_only": True,
        "author": "ChatGPT (GPT-6 Astra Pro)", "original_F15_result_unchanged": True,
        "no_population_generation_or_model_fitting": True,
        "counts": {"search_rows": len(search_rows), "search_variants": len(search_summary),
                   "mask_rows": len(mask_rows), "mask_methods": len(mask_summary),
                   "calibration_searched_rows": 1000, "calibration_oracle_rows": 50,
                   "calibration_interval_rows": len(intervals), "fixed_ordinary_models": 5,
                   "constructed_function_equivalent_layouts": 5},
        "input_manifest": [inputs.records[k] for k in sorted(inputs.records)],
        "script": {"file": Path(__file__).resolve().relative_to(repo).as_posix(), "sha256": digest(Path(__file__).read_bytes())},
        "table_manifest": [{"file": name, "bytes": len(data), "sha256": digest(data)} for name, data in sorted(csv_outputs.items())],
        "provenance_checks": provenance_checks,
        "ordinary_task_rows": task_rows,
        "ordinary_task_summary": {"original_F15_ready_count": sum(r["original_F15_task_ready"] for r in task_rows),
                                   "new_development_mean_task_mae": mean(r["new_development_task_metrics"]["mae"] for r in task_rows),
                                   "new_development_task_mae_range": [min(r["new_development_task_metrics"]["mae"] for r in task_rows), max(r["new_development_task_metrics"]["mae"] for r in task_rows)],
                                   "formal_new_readiness_assessed": False},
        "ordinary_conditional_baselines": {"rows": baseline_rows, "summary": baseline_summary,
                                            "conditional_base_point_mae_cells_at_most_0_05": sum(r["base_prediction"]["mae"] <= .05 for r in baseline_rows)},
        "search": {"variants": search_summary,
                   "paired_comparisons": {category: {key: summarize_comparisons(records) for key, records in sorted(groups.items())}
                                          for category, groups in search_comparison_groups.items()},
                   "comparisons_to_original_F15_selected_subsets_on_common_arrays": search_vs_original,
                   "no_new_confirmatory_support_assessment": True},
        "masks": {"methods": mask_summary,
                  "paired_comparisons": {key: summarize_comparisons(records) for key, records in sorted(mask_comparison_groups.items())},
                  "optimizer_rows": optimization_rows,
                  "optimization_summary": {"roles": 10,
                      "converged_to_declared_duality_gap": sum(r["optimizer_converged_to_declared_gap"] for r in optimization_rows),
                      "total_optimizer_iterations": sum(r["optimizer_iterations"] for r in optimization_rows),
                      "duality_gap_range": [min(r["fractional_duality_gap"] for r in optimization_rows), max(r["fractional_duality_gap"] for r in optimization_rows)],
                      "fractional_coordinate_count_range": [min(r["fractional_mask"]["fractional_count"] for r in optimization_rows), max(r["fractional_mask"]["fractional_count"] for r in optimization_rows)],
                      "total_binary_subsets_enumerated": sum(r["binary_enumerated_subsets"] for r in optimization_rows),
                      "binary_unpruned_complete_count": sum(r["binary_unpruned_full_enumeration"] for r in optimization_rows),
                      "binary_minus_fractional_discovery_logit_mse_range": [min(r["binary_minus_fractional_discovery_logit_mse"] for r in optimization_rows), max(r["binary_minus_fractional_discovery_logit_mse"] for r in optimization_rows)]},
                  "no_new_confirmatory_support_assessment": True,
                  "technical_superposition_established": False},
        "calibration": {
            "complete_endpoint_layouts": assessment["diagnostic"]["calibration_complete_endpoint_layouts"],
            "complete_endpoint_met": assessment["diagnostic"]["calibration_complete_endpoint_met"],
            "same_constructed_function_across_layouts": True, "ordinary_trained_evidence": False,
            "models": calibration_models, "interval_rows": intervals,
            "all_interval_status_counts": status_counts(intervals),
            "status_counts_by_hypothesis_and_category": [{"hypothesis": h, "category": c, **status_counts([r for r in intervals if r["hypothesis"] == h and r["category"] == c])}
                for h in (None, *HYPOTHESES) for c in sorted({r["category"] for r in intervals})
                if any(r["hypothesis"] == h and r["category"] == c for r in intervals)],
            "control_status_counts": [{"hypothesis": h, "control": control,
                                       **status_counts([r for r in intervals if r["hypothesis"] == h and r["control"] == control])}
                                      for h in HYPOTHESES for control in CONTROLS[1:]],
            "hypothesis_outcome_counts": [{"hypothesis": g,
                "adequate_layouts": sum(m["hypotheses"][g]["adequate"] for m in assessment["models"]),
                "selective_layouts": sum(m["hypotheses"][g]["selective"] for m in assessment["models"]),
                "adequate_and_selective_layouts": sum(m["hypotheses"][g]["adequate"] and m["hypotheses"][g]["selective"] for m in assessment["models"])} for g in HYPOTHESES],
            "oracle": {"complete_endpoint_assessed": False, "known_subsets_selected_by_construction": True,
                       "uniform_error_bounds_satisfied": sum(r["uniform_bound_satisfied"] for r in calibration_oracle_rows),
                       "mean_mae": mean(r["mae"] for r in calibration_oracle_rows),
                       "max_absolute_error": max(r["max_absolute_error"] for r in calibration_oracle_rows),
                       "searched_exact_known_subset_roles": sum(r["searched_subset_matches_known_subset"] for r in calibration_oracle_rows if r["stratum"] == "mixed_near"),
                       "mean_searched_minus_oracle_mae": mean(r["searched_minus_oracle_mae"] for r in calibration_oracle_rows)},
        },
        "resources": {
            "stage_records": {name: {k: record.get(k) for k in (
                "attempt", "started_utc", "completed_utc", "wall_seconds", "cpu_seconds", "native_child_cpu_seconds", "parent_plus_child_cpu_seconds",
                "preserved_partial_units", "reused_units", "retry_reason", "automatic_retry")}
                for name, record in (("preparation", preparation_complete), ("evaluation", evaluation_complete))},
            "per_unit": [{"kind": kind, "index": i, "preparation": preparations[(kind, i)]["resource"],
                          "evaluation": evaluations[(kind, i)]["resource"]} for kind, i in itertools.product(("calibration", "search", "soft_mask"), range(5))],
            "new_ordinary_training_steps": 0,
            "actual_search_candidate_scores": sum(preparations[("search", i)]["resource"]["candidate_evaluations_actual"] for i in range(5)),
            "logical_search_candidate_scores_without_shared_score_reuse": sum(preparations[("search", i)]["resource"]["candidate_evaluations_logical_without_shared_scores"] for i in range(5)),
            "actual_search_decoder_fits": sum(preparations[("search", i)]["resource"]["decoder_fits_actual"] for i in range(5)),
            "calibration_candidate_scores": sum(preparations[("calibration", i)]["resource"]["candidate_evaluations"] for i in range(5)),
            "task_time_ledger_not_modified_by_reporting_script": True,
        },
    }
    # Keep these read bindings explicit: their complete hashes are in the input manifest.
    summary["execution_binding"] = {"diagnostic_config_schema": cfg.get("schema"),
                                    "diagnostic_freeze_protocol": freeze.get("protocol_id", freeze.get("schema")),
                                    "exposure_record": exposure,
                                    "evaluation_completion_utc": evaluation_complete["completed_utc"]}
    return {"core_summary.json": (json.dumps(summary, sort_keys=True, indent=2, allow_nan=False) + "\n").encode(), **csv_outputs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--run", type=Path, default=Path("v2/work_logs/F15_ND01_v1_run1"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    run = args.run.resolve() if args.run.is_absolute() else (repo / args.run).resolve()
    outputs = build(repo, run)
    directory = Path(__file__).resolve().parent
    if args.check:
        for name, data in outputs.items():
            if (directory / name).read_bytes() != data:
                raise ValueError(f"Derived output differs: {name}")
        print(json.dumps({"status": "byte_exact_saved_output_summary_verified", "outputs": len(outputs)}))
        return
    existing = [name for name in outputs if (directory / name).exists()]
    if existing:
        raise FileExistsError(f"Refusing to overwrite derived outputs {existing}; use --check for verification.")
    for name, data in outputs.items():
        with (directory / name).open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    print(json.dumps({"status": "complete_saved_output_summary_created", "outputs": [
        {"file": name, "bytes": len(data), "sha256": digest(data)} for name, data in outputs.items()]}))


if __name__ == "__main__":
    main()
