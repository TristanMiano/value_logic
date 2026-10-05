"""F15 saved-statistics arithmetic audit; no experimental modules or generation.

Contributor: delegated ChatGPT (GPT-6 Astra Pro), F15 analysis audit.
This collaborating verification is not F16 or independent peer review.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "v2/work_logs/F15_v1_run1"
HERE = Path(__file__).resolve().parent
G = ("identity", "inv_eta", "inv_one_minus_eta", "inv_total_cost")
ARMS = ("aligned", "random", "permuted_concept", "shuffled_donor", "untrained")
STRATA = ("mixed_near", "mixed_far", "preserve_other", "equal_target", "scale_separating")
N, FAMILY, ALPHA = 8192, 560, 0.05
checks, failures, file_hashes = Counter(), [], {}
started_wall, started_cpu = time.perf_counter(), time.process_time()


def check(condition, name, group):
    checks[group] += 1
    if not condition:
        failures.append(name)


def close(a, b):
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-14)


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def read(path, sidecar=False):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    file_hashes[str(path.relative_to(ROOT))] = digest
    if sidecar:
        check(Path(str(path)+".sha256").read_text().strip() == digest,
              str(path)+" sidecar", "artifact_hashes")
    return json.loads(data)


config = read(ROOT / "v2/experiments/config.v1.json")
assessment = read(RUN / "evaluation_attempt_1/neural_assessment.json", True)
prep_manifest = read(RUN / "preparation_complete.json", True)
exposure = read(RUN / "evaluation_start.json", True)
check(config["analysis"]["maximum_interval_rows"] == FAMILY and config["analysis"]["familywise_alpha"] == ALPHA,
      "fixed interval family", "configuration")
check(config["neural"]["evaluation_pairs_per_stratum"] == N and config["neural"]["task_evaluation_samples"] == N,
      "fixed evaluation counts", "configuration")
check(prep_manifest["completed_utc"] < exposure["started_utc"], "all-model preparation before exposure", "artifact_binding")
check(exposure["preparation_manifest_sha256"] == file_hashes[str((RUN/"preparation_complete.json").relative_to(ROOT))],
      "exposure preparation digest", "artifact_binding")

# Recover all unique stored confidence rows. Conditional-base rows recur in
# each hypothesis; identical IDs must have identical recorded arithmetic.
stored = {}


def collect(value):
    if isinstance(value, dict):
        if {"id", "sample_range", "radius", "lower", "upper", "mean", "n"} <= value.keys():
            if value["id"] in stored:
                check(stored[value["id"]] == value, value["id"]+" repeated row", "stored_consistency")
            stored[value["id"]] = value
        for child in value.values():
            collect(child)
    elif isinstance(value, list):
        for child in value:
            collect(child)


collect(assessment)
intervals = {}


def interval(key, mean, n=N, bounds=(0.0, 1.0)):
    lower, upper = bounds
    # Direct independent arithmetic from the saved sample mean/count, without
    # importing or calling the frozen analysis implementation.
    radius = math.sqrt(math.log((2/ALPHA)*FAMILY)/(2*n)) * (upper-lower)
    result = {"id": key, "mean": mean, "n": n, "sample_range": list(bounds),
              "radius": radius, "lower": max(lower, mean-radius), "upper": min(upper, mean+radius)}
    record = stored.get(key)
    check(record is not None, key+" present", "intervals")
    if record is not None:
        check(record["n"] == n and record["sample_range"] == list(bounds)
              and all(close(record[k], result[k]) for k in ("mean", "radius", "lower", "upper")),
              key+" arithmetic", "intervals")
    intervals[key] = result
    return result


def all_finite(value):
    if isinstance(value, dict):
        return all(all_finite(v) for v in value.values())
    if isinstance(value, list):
        return all(all_finite(v) for v in value)
    return not isinstance(value, float) or math.isfinite(value)


models, raw_cells = [], []
for i in range(5):
    prepared_path = RUN / f"preparation_attempt_1/model_{i}_prepared.json"
    prepared = read(prepared_path, True)
    result = read(RUN / f"evaluation_attempt_1/model_{i}_evaluation.json", True)
    expected = assessment["models"][i]
    prefix = f"model{i}"
    prepared_hash = canonical({k: v for k, v in prepared.items() if k != "artifact_hash"})
    check(prepared_hash == prepared["artifact_hash"] == result["discovery_artifact_hash"], prefix+" internal hash", "artifact_binding")
    check(prepared["config_hash"] == canonical(config["neural"]) and prepared["config"] == config["neural"],
          prefix+" config binding", "artifact_binding")
    check(prep_manifest["models"][i]["sha256"] == file_hashes[str(prepared_path.relative_to(ROOT))],
          prefix+" preparation manifest file", "artifact_binding")
    check(prepared["discovery_seed"] == 1500401+i and result["evaluation_seed"] == 1500491+i
          and prepared["evaluation_generated"] is False, prefix+" split", "artifact_binding")
    check(all_finite(prepared) and all_finite(result), prefix+" finite artifacts", "artifact_binding")
    train = prepared["training"]
    check((train["steps"], train["batch_size"], train["stochastic_outcome_labels"], train["expected_cost_training_labels"], train["parameter_count"])
          == (3000, 256, 768000, 0, 193), prefix+" ordinary training contract", "budgets")
    for name in ("network", "untrained_network"):
        net = prepared[name]
        check(len(net["w"]) == 4 and all(len(row) == 32 for row in net["w"])
              and len(net["b"]) == len(net["v"]) == 32 and isinstance(net["beta"], (int, float)),
              prefix+" "+name+" shape", "budgets")
    for name, alignment in prepared["alignments"].items():
        for role in alignment["roles"]:
            pool, scores, selected = role["candidate_pool"], role["candidate_scores"], role["selected_index"]
            check(len(pool) == len(scores) == role["candidate_evaluations"] == role["decoder_fits"] == 128,
                  prefix+" "+name+" candidates", "budgets")
            check(all(len(s) == len(set(s)) == 8 and all(type(k) is int and 0 <= k < 32 for k in s) for s in pool),
                  prefix+" "+name+" proper subsets", "budgets")
            check(role["subset"] == pool[selected] == role["decoder"]["subset"]
                  and role["selection_score"] == scores[selected] and len(role["decoder"]["coefficient"]) == 8,
                  prefix+" "+name+" saved selection", "budgets")
            # Independently verify the declared sequential lexicographic tie rule.
            winner = 0
            for candidate, score in enumerate(scores[1:], 1):
                significant = [(score[k], scores[winner][k]) for k in ("probability_mse", "effect_mse", "decoder_nmse")
                               if abs(score[k]-scores[winner][k]) > 1e-12]
                if significant and significant[0][0] < significant[0][1]:
                    winner = candidate
            check(winner == selected, prefix+" "+name+" discovery ranking", "budgets")
    check(set(prepared["alignments"]) == set(result["alignments"]) == {f"{g}/{arm}" for g in G for arm in ARMS},
          prefix+" complete arms", "budgets")
    for generation in (result["pair_generation"], result["wrong_donor_generation"]):
        check(len(generation) == 2 and all(set(role) == set(STRATA) for role in generation)
              and all(cell["accepted"] == N and N <= cell["proposals_generated"] <= 4000*N
                      for role in generation for cell in role.values()), prefix+" pair counts", "budgets")
    task = result["task"]
    base = interval(prefix+"/base_mae", task["mae"])
    regret = interval(prefix+"/base_normalized_regret", task["mean_normalized_decision_regret"])
    check(task["n"] == N and task["decision_regret_bound"] == 1.375
          and close(task["mean_decision_regret"], 1.375*task["mean_normalized_decision_regret"]),
          prefix+" task normalizer", "saved_statistics")
    task_ready = base["upper"] <= .05 and regret["upper"]*1.375 <= .05
    conditional = {}
    for role in range(2):
        for stratum in STRATA:
            metric = result["alignments"]["identity/aligned"]["roles"][role][stratum]["base_prediction"]
            conditional[role, stratum] = interval(f"{prefix}/conditional_base/{role}/{stratum}/mae", metric["mae"])
    hypotheses = {}
    for g in G:
        role_results = []
        for role in range(2):
            absolute, decisions, advantages = {}, {}, {}
            for stratum in STRATA:
                cell = result["alignments"][g+"/aligned"]["roles"][role][stratum]
                absolute[stratum] = interval(f"{prefix}/{g}/{role}/{stratum}/mae", cell["mae"])
                check(cell["n"] == N, prefix+" cell count", "budgets")
                if stratum in ("mixed_near", "mixed_far"):
                    decisions[stratum] = interval(f"{prefix}/{g}/{role}/{stratum}/disagreement", 1-cell["decision_agreement"])
                raw_cells.append({"model_index": i, "g": g, "role": role, "stratum": stratum,
                    "arm_mae": {arm: result["alignments"][g+"/"+arm]["roles"][role][stratum]["mae"] for arm in ARMS},
                    "whole_layer_mae": cell["whole_layer_swap"]["mae"], "no_swap_mae": cell["no_swap"]["mae"]})
            for control in ARMS[1:]:
                cells = [result["matched_control_comparisons_by_g"][g][control][f"{role}/{s}"] for s in STRATA]
                for stratum, cell in zip(STRATA, cells):
                    metric_difference = (result["alignments"][g+"/"+control]["roles"][role][stratum]["mae"]
                                         -result["alignments"][g+"/aligned"]["roles"][role][stratum]["mae"])
                    check(cell["n"] == N and close(cell["sum"]/N, cell["mean_paired_absolute_error_improvement"])
                          and close(metric_difference, cell["mean_paired_absolute_error_improvement"]),
                          prefix+" control moment/MAE identity", "saved_statistics")
                # Pool independent equal-sized strata from their saved totals.
                mean = math.fsum(cell["sum"] for cell in cells)/(5*N)
                advantages[control] = interval(f"{prefix}/{g}/{role}/{control}/advantage", mean, 5*N, (-1.0, 1.0))
            effects = {s: min(2.0, absolute[s]["upper"]+conditional[role, s]["upper"]) for s in STRATA}
            adequate = (max(x["upper"] for x in absolute.values()) <= .05
                and max(conditional[role, s]["upper"] for s in STRATA) <= .05
                and max(effects.values()) <= .10 and decisions["mixed_far"]["upper"] <= .10
                and decisions["mixed_near"]["upper"] <= .35)
            selective = min(x["lower"] for x in advantages.values()) >= .01
            falsified = any(x["lower"] > .05 for x in absolute.values())
            original = expected["hypotheses"][g]["roles"][role]
            for field, value in (("absolute_and_decision_criteria", adequate), ("matched_control_specificity", selective),
                                 ("mae_tolerance_falsified_in_a_stratum", falsified)):
                check(original[field] is value, f"{prefix}/{g}/{role}/{field}", "support_booleans")
            check(all(close(effects[s], original["derived_adjusted_effect_mae_upper"][s]) for s in STRATA),
                  prefix+" adjusted effects", "derived_bounds")
            role_results.append({"role": role, "adequate": adequate, "selective": selective,
                "intervention_mae_support_strata": [s for s in STRATA if absolute[s]["upper"] <= .05],
                "intervention_mae_falsified_strata": [s for s in STRATA if absolute[s]["lower"] > .05],
                "intervention_mae_inconclusive_strata": [s for s in STRATA if absolute[s]["lower"] <= .05 < absolute[s]["upper"]],
                "conditional_base_support_strata": [s for s in STRATA if conditional[role, s]["upper"] <= .05],
                "near_decision_supported": decisions["mixed_near"]["upper"] <= .35,
                "far_decision_supported": decisions["mixed_far"]["upper"] <= .10,
                "absolute": absolute, "decisions": decisions, "matched_controls": advantages})
        hypotheses[g] = {"roles": role_results, "adequate": all(x["adequate"] for x in role_results),
                         "selective": all(x["selective"] for x in role_results)}
        check(all(expected["hypotheses"][g][field] is hypotheses[g][field] for field in ("adequate", "selective")),
              prefix+" "+g+" hypothesis", "support_booleans")
    scale_tests = []
    for g in G[1:]:
        for role in range(2):
            cell = result["alternative_comparisons"][g][f"{role}/scale_separating"]
            comparison = cell["same_identity_subset_comparison"]
            frequency = interval(f"{prefix}/{g}/{role}/separating_frequency", cell["separating_pairs"]/cell["total_pairs"])
            advantage = interval(f"{prefix}/{g}/{role}/same_identity_subset_advantage", comparison["sum"]/comparison["n"], N, (-1.0, 1.0))
            check(cell["separating_pairs"] == cell["total_pairs"] == comparison["n"] == N
                  and close(comparison["sum"]/N, comparison["mean_paired_absolute_error_improvement"]),
                  prefix+" separating counts and moments", "saved_statistics")
            distinguished = frequency["lower"] >= .9 and advantage["lower"] >= .01
            check(expected["same_subset_scale_tests"][g][role]["distinguished"] is distinguished,
                  prefix+" scale support", "support_booleans")
            scale_tests.append({"g": g, "role": role, "distinguished": distinguished,
                                "frequency": frequency, "advantage": advantage})
    gauge_errors = {g: result["gauges_by_g"][g]["errors"] for g in G}
    numerical = True
    for gauge in result["gauges_by_g"].values():
        numerical &= (set(gauge["errors"]) == {"observational_probability", "intervention_probability", "decoder_value"}
            and all(0 <= error <= 1e-10 for error in gauge["errors"].values()) and gauge["refits"] == 0
            and gauge["tolerance"] == 1e-10 and sorted(gauge["permutation"]) == list(range(32))
            and len(gauge["scales"]) == 32 and all(.125 <= s <= 8 for s in gauge["scales"]))
        check(gauge["passed"] is bool(all(error <= 1e-10 for error in gauge["errors"].values())),
              prefix+" gauge flag", "support_booleans")
    witness = result["unused_duplicate_witness"]
    numerical &= (set(result["gauges_by_g"]) == set(G) and result["resource"]["alignment_refits"] == 0
        and 0 <= result["global_scale_prediction_error"] <= 1e-10
        and 0 <= result["global_scale_decoder_error"] <= 1e-10
        and 0 <= witness["decoder_max_error"] <= 1e-10 and 0 <= witness["unused_logit_effect_max"] <= 1e-10
        and witness["used_logit_effect_max"] > 1e-10 and witness["decoding_passes_and_unused_causal_use_fails"] is True)
    scale_specific = all(x["distinguished"] for x in scale_tests)
    identity = hypotheses["identity"]
    disposition = ("numerical_or_protocol_failure" if not numerical else
        "task_underlearned_at_frozen_criterion" if not task_ready else
        "expected_cost_interchange_supported_at_declared_scope" if identity["adequate"] and identity["selective"] and scale_specific else
        "interchange_adequate_but_not_discriminated_from_controls_or_scales" if identity["adequate"] else
        "competing_cost_scale_supported_original_not_supported" if any(hypotheses[g]["adequate"] and hypotheses[g]["selective"] for g in G[1:]) else
        "specified_subset_hypothesis_not_supported_at_frozen_thresholds")
    check(expected["task_ready"] is task_ready and expected["numerical_controls_valid"] is bool(numerical)
          and expected["disposition"] == disposition, prefix+" model disposition", "support_booleans")
    overlap = sorted(set(prepared["alignments"]["identity/aligned"]["roles"][0]["subset"])
                     & set(prepared["alignments"]["identity/aligned"]["roles"][1]["subset"]))
    check(len(overlap) == result["composition"]["overlap_size"] and result["composition"]["primary_claim"] is False,
          prefix+" secondary composition", "saved_statistics")
    if not overlap:
        check(result["composition"]["order_probability_max_difference"] == 0,
              prefix+" disjoint composition commutes", "saved_statistics")
    models.append({"index": i, "discovery_seed": prepared["discovery_seed"], "evaluation_seed": result["evaluation_seed"],
        "task": task, "task_mae_interval": base, "task_regret_interval_normalized": regret,
        "task_ready": task_ready, "hypotheses": hypotheses, "same_subset_scale_tests": scale_tests,
        "scale_specific": scale_specific, "numerical_controls_valid": bool(numerical),
        "gauges": gauge_errors, "global_scale_errors": [result["global_scale_prediction_error"], result["global_scale_decoder_error"]],
        "unused_duplicate_witness": witness, "composition": result["composition"], "identity_subset_overlap": overlap,
        "selected_alternative": prepared["selected_alternative"], "disposition": disposition,
        "identity_decoder_nrmse": result["alignments"]["identity/aligned"]["observational_decoder_nrmse"],
        "identity_log_contribution_rmse": result["alignments"]["identity/aligned"]["log_contribution_rmse"]})

supported = sum(m["disposition"] == "expected_cost_interchange_supported_at_declared_scope" for m in models)
pilot = supported >= 4 and all(m["numerical_controls_valid"] for m in models)
check(set(intervals) == set(stored) and len(intervals) == assessment["actual_interval_rows"] == FAMILY,
      "complete 560-row family", "intervals")
check(assessment["supported_prespecified_replicates"] == supported and assessment["pilot_support_criterion_met"] is pilot,
      "full pilot support", "support_booleans")
identity_rows = [r for r in raw_cells if r["g"] == "identity"]
summary = {
    "ordinary_task_ready_models": sum(m["task_ready"] for m in models),
    "numerical_controls_valid_models": sum(m["numerical_controls_valid"] for m in models),
    "identity_supported_models": supported, "pilot_support_criterion_met": pilot,
    "by_hypothesis": {g: {"adequate_models": sum(m["hypotheses"][g]["adequate"] for m in models),
        "selective_models": sum(m["hypotheses"][g]["selective"] for m in models),
        "supported_mae_cells": sum(len(r["intervention_mae_support_strata"]) for m in models for r in m["hypotheses"][g]["roles"]),
        "falsified_mae_cells": sum(len(r["intervention_mae_falsified_strata"]) for m in models for r in m["hypotheses"][g]["roles"]),
        "inconclusive_mae_cells": sum(len(r["intervention_mae_inconclusive_strata"]) for m in models for r in m["hypotheses"][g]["roles"])} for g in G},
    "identity_matched_control_supported_roles": {arm: sum(r["matched_controls"][arm]["lower"] >= .01
        for m in models for r in m["hypotheses"]["identity"]["roles"]) for arm in ARMS[1:]},
    "identity_raw_pooled_mae_ranges_by_arm": {arm: [min(math.fsum(r["arm_mae"][arm] for r in identity_rows if r["model_index"] == i and r["role"] == role)/5
        for i in range(5) for role in range(2)), max(math.fsum(r["arm_mae"][arm] for r in identity_rows if r["model_index"] == i and r["role"] == role)/5
        for i in range(5) for role in range(2))] for arm in ARMS},
    "same_subset_scale_supported_model_roles": {g: sum(s["distinguished"] for m in models for s in m["same_subset_scale_tests"] if s["g"] == g) for g in G[1:]},
    "largest_recorded_gauge_error": max(e for m in models for gauge in m["gauges"].values() for e in gauge.values()),
    "composition_overlap_sizes": [len(m["identity_subset_overlap"]) for m in models],
    "composition_order_max_differences": [m["composition"]["order_probability_max_difference"] for m in models]}
output = {"schema": "f15-delegated-neural-saved-output-audit-v1",
    "contributor": "delegated ChatGPT (GPT-6 Astra Pro), F15 analysis audit",
    "generated_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
    "experimental_generation_or_training_performed": False,
    "new_inferential_claims_added": False, "independent_peer_review_or_F16": False,
    "scope": "independent standard-library recalculation of frozen intervals and predicates from saved statistics; underlying forwards/pair arrays are not regenerated",
    "input_sha256": file_hashes, "audit_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "checks_by_group": dict(checks), "failures": failures, "passed": not failures,
    "unique_interval_rows_recomputed": len(intervals), "summary": summary,
    "models": models, "descriptive_per_cell_baselines": raw_cells, "intervals": list(intervals.values()),
    "audit_compute_wall_seconds": time.perf_counter()-started_wall,
    "audit_compute_cpu_seconds": time.process_time()-started_cpu,
    "additional_principal_engaged_minutes_claimed": 0}
path = HERE / "neural_output_audit.json"
path.write_text(json.dumps(output, indent=2, sort_keys=True, allow_nan=False)+"\n")
print(json.dumps({"output": str(path.relative_to(ROOT)), "passed": output["passed"], "failures": failures,
                  "checks_by_group": dict(checks), "intervals_recomputed": len(intervals), "summary": summary}, indent=2))
if failures:
    raise SystemExit(1)
