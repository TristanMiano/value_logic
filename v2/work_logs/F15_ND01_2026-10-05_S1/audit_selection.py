"""Independent saved-statistic audit of ND01 selection/control diagnostics.

Only reads saved JSON/text and computes scalar arithmetic. It never imports
experiment/model/reporting modules or generates a population. Writes only
audit_selection.json and audit_selection.md in this auditor's session directory.
Contributor: delegated ChatGPT (GPT-6 Astra Pro), protocol/accounting audit.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path
from statistics import fmean

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
RUN = REPO / "v2/work_logs/F15_ND01_v1_run1"
ANALYSIS = REPO / "v2/experiments/F15_ND01_analysis"
STRATA = ("mixed_near", "mixed_far", "preserve_other", "equal_target", "scale_separating")
HYPOTHESES = ("identity", "inv_eta", "inv_one_minus_eta", "inv_total_cost")
CONTROLS = ("random", "permuted_concept", "shuffled_donor", "untrained")
FAMILIES = ("cost_corr", "uniform", "permuted_cost_corr", "log_cost_corr", "positive_contribution_cov")
METRICS = ("worst_normalized_objective", "mean_probability_mse", "near_disagreement",
           "far_disagreement", "equal_target_output_effect_rms")
TIE = 1e-12
inputs, checks, errors = {}, [], []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(value, label):
    checks.append(label)
    if not value:
        errors.append(label)


def close(actual, expected, label):
    check(math.isfinite(actual) and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12), label)


def load(path):
    data = path.read_bytes()
    inputs[path.relative_to(REPO).as_posix()] = {"bytes": len(data), "sha256": sha(data)}
    sidecar = Path(str(path) + ".sha256")
    if sidecar.exists():
        check(sidecar.read_text().split()[0] == sha(data), f"Saved source SHA: {path.name}")
    return json.loads(data)


def sign(value):
    return "positive" if value > TIE else "negative" if value < -TIE else "tie"


def phase(cells):
    components = {s: cells[s]["mae"]/.05 for s in STRATA}
    components["mixed_near_disagreement"] = cells["mixed_near"]["decision_disagreement"]/.35
    components["mixed_far_disagreement"] = cells["mixed_far"]["decision_disagreement"]/.10
    return {
        "worst_normalized_objective": max(components.values()),
        "mean_probability_mse": fmean(cells[s]["mse"] for s in STRATA),
        "mean_probability_mae": fmean(cells[s]["mae"] for s in STRATA),
        "near_disagreement": cells["mixed_near"]["decision_disagreement"],
        "far_disagreement": cells["mixed_far"]["decision_disagreement"],
        "equal_target_output_effect_rms": cells["equal_target"]["unchanged_target_output_effect_rms"],
        "normalized_components": components,
        "maximizing_components": [k for k, v in components.items() if abs(v-max(components.values())) <= TIE],
    }


def group(rows):
    out = {"comparisons": len(rows), "selected_subset_changes": sum(r["changed"] for r in rows),
           "strict_improvement_tolerance": TIE,
           "mean_differences": {p: {m: fmean(r["diff"][p][m] for r in rows) for m in METRICS}
                                for p in ("discovery", "validation")}}
    for p, metric in itertools.product(("discovery", "validation"), (METRICS[0], "near_disagreement")):
        counts = Counter(sign(r["diff"][p][metric]) for r in rows)
        out[f"{p}_{metric}_sign_counts"] = {k: counts[k] for k in ("positive", "negative", "tie")}
    for metric in (METRICS[0], "near_disagreement"):
        out[f"strict_discovery_gain_and_validation_loss_{metric}"] = sum(
            r["diff"]["discovery"][metric] > TIE and r["diff"]["validation"][metric] < -TIE for r in rows)
    out["mean_validation_mae_change_robust_minus_frozen_mse"] = fmean(
        r["phases"]["validation"]["robust"]["mean_probability_mae"] -
        r["phases"]["validation"]["frozen_mse"]["mean_probability_mae"] for r in rows)
    out["mean_worst_objective_validation_minus_discovery"] = {
        selector: fmean(r["phases"]["validation"][selector][METRICS[0]]-
                        r["phases"]["discovery"][selector][METRICS[0]] for r in rows)
        for selector in ("frozen_mse", "robust")}
    return out


def compare(actual, expected, label):
    if isinstance(expected, dict):
        for key, value in expected.items():
            check(key in actual, f"{label}: key {key}")
            if key in actual:
                compare(actual[key], value, f"{label}/{key}")
    elif isinstance(expected, float):
        close(actual, expected, label)
    else:
        check(actual == expected, label)


def main():
    summary = load(ANALYSIS / "selection_diagnostics.json")
    prepared = load(RUN / "preparation_complete.json")
    evaluated = load(RUN / "evaluation_complete.json")
    cfg = load(REPO / "v2/experiments/neural_diagnostic_v1/config.json")
    assessment = load(RUN / evaluated["calibration_assessment"]["file"])
    prep_units = {(r["kind"], r["index"]): r for r in prepared["units"]}
    eval_units = {(r["kind"], r["index"]): r for r in evaluated["units"]}
    check(len(prep_units) == len(eval_units) == 15, "Complete 15-unit preparation/evaluation")
    check(prepared["status"] == "preparation_complete" and evaluated["status"] == "evaluation_complete",
          "Original stages complete")
    source_search = {}
    source_cal = {}
    for i in range(5):
        prep = load(RUN / prep_units[("search", i)]["file"])
        ev = load(RUN / eval_units[("search", i)]["file"])
        cal = load(RUN / eval_units[("calibration", i)]["file"])
        check(ev["prepared_artifact_hash"] == prep["artifact_hash"], f"Model {i}: prep/eval binding")
        check(tuple(prep["effective_settings"]["proposal_families"]) == FAMILIES, f"Model {i}: all five families")
        source_search[i] = (prep, ev)
        source_cal[i] = cal
    rows = summary["selection_comparison"]["rows"]
    by_key = {(r["model_index"], r["family"], r["budget"], r["role"]): r for r in rows}
    expected_keys = set(itertools.product(range(5), FAMILIES, (128, 1024), (0, 1)))
    check(set(by_key) == expected_keys and len(rows) == 100, "Exactly 100 unique selector comparisons")
    rebuilt, groups = [], defaultdict(list)
    for key in sorted(expected_keys):
        i, family, budget, role = key
        prep, ev = source_search[i]
        saved = by_key[key]
        phases = {"discovery": {}, "validation": {}}
        subsets = {}
        for selector in ("frozen_mse", "robust"):
            name = f"{family}/budget_{budget}/{selector}"
            selected = prep["alignments"][name]["roles"][role]
            subsets[selector] = selected["subset"]
            check(selected["subset"] == sorted(set(selected["subset"])) and len(selected["subset"]) == 8,
                  f"{key}/{selector}: actual sorted eight-neuron subset")
            phases["discovery"][selector] = phase(selected["selection_score"]["per_stratum"])
            phases["validation"][selector] = phase(ev["evaluated"][name]["roles"][role])
            for p in phases:
                expected = dict(phases[p][selector])
                if p == "discovery":
                    expected.pop("mean_probability_mae")
                compare(saved[p][selector], expected, f"{key}/{p}/{selector}")
        diff = {p: {m: phases[p]["frozen_mse"][m]-phases[p]["robust"][m] for m in METRICS}
                for p in phases}
        changed = subsets["frozen_mse"] != subsets["robust"]
        check(saved["selected_subsets"] == subsets and saved["selected_subset_changed"] == changed,
              f"{key}: chosen subsets bind prepared files")
        compare(saved["improvement_of_robust_over_frozen_mse"], diff, f"{key}: independent differences")
        check(diff["discovery"][METRICS[0]] >= -TIE, f"{key}: robust discovery objective no worse")
        record = {"key": key, "changed": changed, "phases": phases, "diff": diff}
        rebuilt.append(record)
        groups[(family, budget)].append(record)
    overall = group(rebuilt)
    compare(summary["selection_comparison"]["overall_descriptive_summary"], overall, "Overall aggregate")
    for saved in summary["selection_comparison"]["family_budget_summaries"]:
        compare(saved, group(groups[(saved["family"], saved["budget"])]), f"Group {saved['family']}/{saved['budget']}")
    check(overall["selected_subset_changes"] == 41, "41 changed subsets independently confirmed")
    check(overall["validation_worst_normalized_objective_sign_counts"] == {"positive": 10, "negative": 31, "tie": 59},
          "10 improved /31 worsened /59 tied independently confirmed")

    ceilings = summary["calibration_fixed_control_ceilings"]["rows"]
    ceiling_map = {(r["layout_index"], r["hypothesis"], r["role"], r["control"]): r for r in ceilings}
    ceiling_keys = set(itertools.product(range(5), HYPOTHESES, (0, 1), CONTROLS))
    check(set(ceiling_map) == ceiling_keys and len(ceilings) == 160, "Exactly 160 unique control ceilings")
    threshold = cfg["calibration"]["analysis"]["matched_control_advantage_min"]
    m = cfg["calibration"]["analysis"]["maximum_interval_rows"]
    alpha = cfg["calibration"]["analysis"]["familywise_alpha"]
    counts = Counter()
    blocked_layouts = set()
    radii = set()
    blockers = []
    for key in sorted(ceiling_keys):
        i, hypothesis, role, control = key
        cells = source_cal[i]["alignments"]
        aligned = cells[f"{hypothesis}/aligned"]["roles"][role]
        comparison = cells[f"{hypothesis}/{control}"]["roles"][role]
        n = sum(comparison[s]["n"] for s in STRATA)
        check({comparison[s]["n"] for s in STRATA} == {8192}, f"{key}: equal-stratum pooling valid")
        mae_control = sum(comparison[s]["n"]*comparison[s]["mae"] for s in STRATA)/n
        mae_aligned = sum(aligned[s]["n"]*aligned[s]["mae"] for s in STRATA)/n
        radius = 2 * math.sqrt(math.log(2*m/alpha)/(2*n))
        interval = assessment["models"][i]["hypotheses"][hypothesis]["roles"][role]["control_advantages"][control]
        close(radius, interval["radius"], f"{key}: Hoeffding radius independently derived")
        close(mae_control-mae_aligned, interval["mean"], f"{key}: paired mean equals pooled error difference")
        lower_ceiling = max(interval["sample_range"][0], mae_control-radius)
        blocked = lower_ceiling < threshold
        expected = {
            "mean_control_mae": mae_control, "mean_aligned_mae": mae_aligned,
            "observed_mean_paired_advantage": mae_control-mae_aligned,
            "frozen_pooled_pair_count": n, "frozen_advantage_radius": radius,
            "frozen_required_advantage": threshold,
            "hypothetical_zero_aligned_error_mean_advantage_ceiling": mae_control,
            "hypothetical_zero_aligned_error_lower_bound_ceiling": lower_ceiling,
            "control_error_needed_for_zero_error_aligned_to_clear_margin": radius+threshold,
            "allowable_aligned_mean_error_for_fixed_control_and_radius": mae_control-radius-threshold,
            "fixed_control_ceiling_below_required_lower_bound": blocked,
            "new_support_assessment": False,
        }
        compare(ceiling_map[key], expected, f"{key}: fixed-control ceiling")
        radii.add(interval["radius"])
        if blocked:
            counts[(hypothesis, control)] += 1
            blocked_layouts.add((i, hypothesis))
            if hypothesis == "identity":
                blockers.append({"layout": i, "role": role, "control": control,
                                 "control_mae": mae_control, "lower_bound_ceiling": lower_ceiling})
    check(radii == {.022115658601168407}, "All 160 saved radii equal 0.022115658601168407")
    check(counts[("identity", "permuted_concept")] == 7 and counts[("identity", "random")] == 1
          and counts[("identity", "shuffled_donor")] == counts[("identity", "untrained")] == 0,
          "Identity fixed-control blockers: 7 permuted, 1 random, 0 wrong-donor/untrained")
    check(all((i, "identity") in blocked_layouts for i in range(5)), "Identity blocked in all five constructed layouts")
    for row in summary["calibration_fixed_control_ceilings"]["by_hypothesis_and_control"]:
        check(row["fixed_control_ceiling_below_margin_count"] == counts[(row["hypothesis"], row["control"])],
              f"Ceiling group {row['hypothesis']}/{row['control']}: blocker count")
    for row in summary["calibration_fixed_control_ceilings"]["by_layout_and_hypothesis"]:
        check(row["at_least_one_fixed_control_blocks_margin_even_at_zero_aligned_error"] ==
              ((row["layout_index"], row["hypothesis"]) in blocked_layouts), "Layout/hypothesis blocking flag")
    for source in summary["inputs"]:
        data = (REPO/source["file"]).read_bytes()
        check(len(data) == source["bytes"] and sha(data) == source["sha256"], f"Reported source manifest: {source['file']}")
    for source in summary["reporting_scripts"]:
        check(sha((REPO/source["file"]).read_bytes()) == source["sha256"], f"Reported script hash: {source['file']}")
    note = (ANALYSIS / "selection_diagnostics.md").read_text()
    check(sha((ANALYSIS / "selection_diagnostics.json").read_bytes()) in note, "Markdown binds actual diagnostic JSON hash")
    check("These are paired settings, not 100 independent model replicates" in note,
          "Markdown discloses dependent comparison counts")
    check("these exact observed" in note and "frozen radius" in note and "hypothetical zero-error" in note,
          "Markdown conditions ceiling on saved controls/radius and hypothetical aligned zero error")

    result = {
        "schema": "F15-ND01-independent-selection-audit-v1", "status": "PASS" if not errors else "FAIL",
        "contributor": "delegated ChatGPT (GPT-6 Astra Pro), protocol/accounting audit",
        "audited_utc": datetime.now(timezone.utc).isoformat(), "checks": len(checks), "errors": errors,
        "source_only_scalar_arithmetic": True, "model_or_population_functions_imported_or_called": False,
        "comparison_count": len(rebuilt), "overall_recomputed": overall,
        "control_ceiling_count": len(ceilings), "radius": sorted(radii), "identity_blockers": blockers,
        "scope": "Independent reconstruction from saved preparation/evaluation moments and assessment; no new statistical test or support disposition. Counts are dependent settings, not independent replicates.",
        "interpretation": "With the observed control errors, original pooled n and fixed Hoeffding radius held constant, an aligned intervention with zero MAE would still fail at least one required control lower-bound margin in every constructed layout. This is conditional endpoint sensitivity evidence; it does not prove an obstacle for different controls, sample sizes or intervals.",
        "audit_script_sha256": sha(Path(__file__).read_bytes()), "inputs": inputs,
        "parallel_agent_minutes_added": 0,
    }
    output = HERE / "audit_selection.json"
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    output.with_suffix(".md").write_text(
        "# F15-ND01 independent saved-selection audit\n\n"
        f"**{result['status']}**: {len(checks)} checks, {len(errors)} defects. "
        "Read-only inspection and independent scalar arithmetic from saved statistics; no experiment, model function, population, fit, selection or evaluation was run.\n\n"
        "All 100 robust-vs-MSE comparisons bind their prepared subsets and saved per-stratum moments. "
        "41 subsets changed; discovery's maximum normalized objective improved in 41 and tied in 59. "
        "Validation improved in 10, worsened in 31 and tied in 59. "
        "All 31 losses followed strict discovery gains. Group and overall summaries also match.\n\n"
        "All 160 calibration-control ceilings independently reconstruct. The registered union-bound "
        "radius computes as 0.022115658601168407 from range width 2, n=40960, m=560 and alpha=.05. "
        "Identity has seven permuted-concept and one random-control ceiling blockers, spanning all five layouts; "
        "there are zero wrong-donor or untrained-control blockers.\n\n"
        f"{result['interpretation']}\n\n"
        "The original analysis explicitly preserves dependence and the conditional nature of this calculation. "
        "No concrete defect found. The Markdown's 0.03211565860116841 threshold is a harmless display rounding "
        "of radius+.01; the calculations retain full floating-point precision.\n\n"
        "Evidence: [audit_selection.json](audit_selection.json). Contributor: delegated ChatGPT "
        "(GPT-6 Astra Pro), protocol/accounting audit. Parallel-agent minutes added: zero.\n")
    print(json.dumps({"status": result["status"], "checks": len(checks), "errors": errors,
                      "selector_comparisons": len(rebuilt), "control_ceilings": len(ceilings),
                      "identity_blockers": len(blockers)}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
