"""Read-only selection-gap and fixed-control-ceiling diagnostics for F15-ND01.

Creates selection_diagnostics.json and selection_diagnostics.md from already
saved statistics. No populations, models, fitting, selection, or evaluation.
Contributor: ChatGPT (GPT-6 Astra Pro). Use --check for nonmutating reproduction.
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
from collections import defaultdict
from pathlib import Path
from statistics import mean

import summarize as S


COMPONENTS = (*S.STRATA, "mixed_near_disagreement", "mixed_far_disagreement")
TOLERANCE = 1e-12


def sign(value):
    return "positive" if value > TOLERANCE else "negative" if value < -TOLERANCE else "tie"


def phase_record(selected, evaluated, role, discovery):
    if discovery:
        score = selected["roles"][role]["selection_score"]
        strata = score["per_stratum"]
        components = score["robust_normalized_components"]
        return {
            "worst_normalized_objective": score["robust_max_normalized_error"],
            "mean_probability_mse": score["probability_mse"],
            "near_disagreement": strata["mixed_near"]["decision_disagreement"],
            "far_disagreement": strata["mixed_far"]["decision_disagreement"],
            "equal_target_output_effect_rms": score["equal_target_output_effect_rms"],
            "maximizing_components": [name for name, value in zip(COMPONENTS, components)
                                      if abs(value - max(components)) <= TOLERANCE],
            "normalized_components": dict(zip(COMPONENTS, components)),
        }
    summary, strata = evaluated["role_summaries"][role], evaluated["roles"][role]
    components = summary["robust_normalized_components"]
    return {
        "worst_normalized_objective": summary["robust_max_normalized_error"],
        "mean_probability_mse": summary["equal_stratum_mean_mse"],
        "mean_probability_mae": summary["equal_stratum_mean_mae"],
        "near_disagreement": strata["mixed_near"]["decision_disagreement"],
        "far_disagreement": strata["mixed_far"]["decision_disagreement"],
        "equal_target_output_effect_rms": summary["unchanged_target_output_effect_rms"],
        "maximizing_components": [name for name, value in zip(COMPONENTS, components)
                                  if abs(value - max(components)) <= TOLERANCE],
        "normalized_components": dict(zip(COMPONENTS, components)),
    }


def summarize_group(rows):
    changes = [r for r in rows if r["selected_subset_changed"]]
    metric_names = ("worst_normalized_objective", "mean_probability_mse", "near_disagreement",
                    "far_disagreement", "equal_target_output_effect_rms")
    result = {"comparisons": len(rows), "selected_subset_changes": len(changes),
              "strict_improvement_tolerance": TOLERANCE,
              "mean_differences": {
                  phase: {metric: mean(r["improvement_of_robust_over_frozen_mse"][phase][metric]
                                       for r in rows) for metric in metric_names}
                  for phase in ("discovery", "validation")}}
    for phase in ("discovery", "validation"):
        for metric in ("worst_normalized_objective", "near_disagreement"):
            values = [r["improvement_of_robust_over_frozen_mse"][phase][metric] for r in rows]
            result[f"{phase}_{metric}_sign_counts"] = {category: sum(sign(v) == category for v in values)
                                                        for category in ("positive", "negative", "tie")}
    for metric in ("worst_normalized_objective", "near_disagreement"):
        result[f"strict_discovery_gain_and_validation_loss_{metric}"] = sum(
            r["improvement_of_robust_over_frozen_mse"]["discovery"][metric] > TOLERANCE and
            r["improvement_of_robust_over_frozen_mse"]["validation"][metric] < -TOLERANCE for r in rows)
    result["mean_validation_mae_change_robust_minus_frozen_mse"] = mean(
        r["validation"]["robust"]["mean_probability_mae"] -
        r["validation"]["frozen_mse"]["mean_probability_mae"] for r in rows)
    result["mean_worst_objective_validation_minus_discovery"] = {
        selector: mean(r["validation"][selector]["worst_normalized_objective"] -
                       r["discovery"][selector]["worst_normalized_objective"] for r in rows)
        for selector in ("frozen_mse", "robust")}
    return result


def build(repo, run):
    inputs = S.Inputs(repo)
    complete = inputs.read(run / "evaluation_complete.json")
    if complete["status"] != "evaluation_complete" or len(complete["units"]) != 15:
        raise ValueError("The complete diagnostic evaluation is required before reporting.")
    prepared_manifest = inputs.read(run / "preparation_complete.json")
    cfg = inputs.read(repo / "v2/experiments/neural_diagnostic_v1/config.json", False)
    evaluation_paths = {(r["kind"], r["index"]): run / r["file"] for r in complete["units"]}
    preparation_paths = {(r["kind"], r["index"]): run / r["file"] for r in prepared_manifest["units"]}
    assessment_path = run / complete["calibration_assessment"]["file"]
    assessment = inputs.read(assessment_path)
    search_rows, ceiling_rows = [], []
    grouped = defaultdict(list)
    for i in range(5):
        preparation = inputs.read(preparation_paths[("search", i)])
        evaluation = inputs.read(evaluation_paths[("search", i)])
        if evaluation["prepared_artifact_hash"] != preparation["artifact_hash"]:
            raise ValueError("Search preparation/evaluation binding mismatch.")
        for family, budget, role in itertools.product(
                preparation["effective_settings"]["proposal_families"], (128, 1024), (0, 1)):
            names = {selector: f"{family}/budget_{budget}/{selector}" for selector in ("frozen_mse", "robust")}
            discovery = {selector: phase_record(preparation["alignments"][name], evaluation["evaluated"][name], role, True)
                         for selector, name in names.items()}
            validation = {selector: phase_record(preparation["alignments"][name], evaluation["evaluated"][name], role, False)
                          for selector, name in names.items()}
            improvements = {phase: {metric: record["frozen_mse"][metric] - record["robust"][metric]
                                    for metric in ("worst_normalized_objective", "mean_probability_mse",
                                                   "near_disagreement", "far_disagreement", "equal_target_output_effect_rms")}
                            for phase, record in (("discovery", discovery), ("validation", validation))}
            # This checks already saved scores; it does not rerun the selection.
            if improvements["discovery"]["worst_normalized_objective"] < -TOLERANCE:
                raise ValueError("Saved robust choice has worse discovery primary objective than the saved MSE choice.")
            subsets = {selector: preparation["alignments"][name]["roles"][role]["subset"] for selector, name in names.items()}
            row = {"model_index": i, "model_seed": preparation["source_model_seed"], "role": role,
                   "family": family, "budget": budget,
                   "source_preparation": inputs.source(preparation_paths[("search", i)]),
                   "source_evaluation": inputs.source(evaluation_paths[("search", i)]),
                   "selected_subsets": subsets, "selected_subset_changed": subsets["frozen_mse"] != subsets["robust"],
                   "discovery": discovery, "validation": validation,
                   "improvement_of_robust_over_frozen_mse": improvements,
                   "positive_improvement_means_lower_error_with_robust": True}
            search_rows.append(row)
            grouped[(family, budget)].append(row)
        calibration = inputs.read(evaluation_paths[("calibration", i)])
        model = assessment["models"][i]
        for hypothesis, role, control in itertools.product(S.HYPOTHESES, (0, 1), S.CONTROLS[1:]):
            aligned_cells = calibration["alignments"][f"{hypothesis}/aligned"]["roles"][role]
            control_cells = calibration["alignments"][f"{hypothesis}/{control}"]["roles"][role]
            aligned_mae = mean(aligned_cells[s]["mae"] for s in S.STRATA)
            control_mae = mean(control_cells[s]["mae"] for s in S.STRATA)
            interval = model["hypotheses"][hypothesis]["roles"][role]["control_advantages"][control]
            S.close(control_mae - aligned_mae, interval["mean"], "Observed control minus aligned means differ from saved paired mean.")
            radius, margin = interval["radius"], .01
            ceiling_lower = max(interval["sample_range"][0], control_mae - radius)
            ceiling_rows.append({
                "layout_index": i, "hypothesis": hypothesis, "role": role, "control": control,
                **inputs.source(evaluation_paths[("calibration", i)]),
                "recorded_advantage_interval_id": interval["id"],
                "mean_aligned_mae": aligned_mae, "mean_control_mae": control_mae,
                "observed_mean_paired_advantage": interval["mean"],
                "recorded_advantage_lower_bound": interval["lower"],
                "frozen_pooled_pair_count": interval["n"], "frozen_advantage_radius": radius,
                "frozen_required_advantage": margin,
                "hypothetical_zero_aligned_error_mean_advantage_ceiling": control_mae,
                "hypothetical_zero_aligned_error_lower_bound_ceiling": ceiling_lower,
                "control_error_needed_for_zero_error_aligned_to_clear_margin": radius + margin,
                "allowable_aligned_mean_error_for_fixed_control_and_radius": control_mae - radius - margin,
                "fixed_control_ceiling_below_required_lower_bound": ceiling_lower < margin,
                "calculation": "For these observed controls and the frozen radius: mean improvement=MAE_control-MAE_aligned<=MAE_control; lower bound<=MAE_control-radius.",
                "new_support_assessment": False,
            })
    if len(search_rows) != 100 or len(ceiling_rows) != 160:
        raise ValueError("Expected all 100 selector comparisons and 160 calibration-control ceilings.")
    grouped_summary = [{"family": family, "budget": budget, **summarize_group(rows)}
                       for (family, budget), rows in sorted(grouped.items())]
    ceiling_summary = []
    for hypothesis, control in itertools.product(S.HYPOTHESES, S.CONTROLS[1:]):
        rows = [r for r in ceiling_rows if r["hypothesis"] == hypothesis and r["control"] == control]
        ceiling_summary.append({"hypothesis": hypothesis, "control": control, "roles": len(rows),
                                "mean_control_mae": mean(r["mean_control_mae"] for r in rows),
                                "fixed_control_ceiling_below_margin_count": sum(r["fixed_control_ceiling_below_required_lower_bound"] for r in rows),
                                "minimum_zero_error_lower_bound_ceiling": min(r["hypothetical_zero_aligned_error_lower_bound_ceiling"] for r in rows),
                                "maximum_zero_error_lower_bound_ceiling": max(r["hypothetical_zero_aligned_error_lower_bound_ceiling"] for r in rows)})
    layout_ceilings = []
    for i, hypothesis in itertools.product(range(5), S.HYPOTHESES):
        rows = [r for r in ceiling_rows if r["layout_index"] == i and r["hypothesis"] == hypothesis]
        blocked = [{"role": r["role"], "control": r["control"],
                    "mean_control_mae": r["mean_control_mae"],
                    "lower_bound_ceiling": r["hypothetical_zero_aligned_error_lower_bound_ceiling"]}
                   for r in rows if r["fixed_control_ceiling_below_required_lower_bound"]]
        layout_ceilings.append({"layout_index": i, "hypothesis": hypothesis,
                                "at_least_one_fixed_control_blocks_margin_even_at_zero_aligned_error": bool(blocked),
                                "blocking_fixed_controls": blocked})
    summary = {
        "schema": "f15-nd01-selection-diagnostics-v1", "development_only": True,
        "author": "ChatGPT (GPT-6 Astra Pro)", "no_new_population_model_fit_selection_or_evaluation": True,
        "original_F15_result_unchanged": True,
        "inputs": [inputs.records[k] for k in sorted(inputs.records)],
        "reporting_scripts": [{"file": p.relative_to(repo).as_posix(), "sha256": S.digest(p.read_bytes())}
                              for p in (Path(__file__).resolve(), Path(S.__file__).resolve())],
        "selection_comparison": {"rows": search_rows, "family_budget_summaries": grouped_summary,
                                 "overall_descriptive_summary": summarize_group(search_rows),
                                 "comparison_count_is_not_independent_replicate_count": True,
                                 "scope": "same fixed networks and validation arrays; families, nested budgets, and selectors reuse information"},
        "calibration_fixed_control_ceilings": {"rows": ceiling_rows, "by_hypothesis_and_control": ceiling_summary,
                                               "by_layout_and_hypothesis": layout_ceilings,
                                               "new_support_assessment": False,
                                               "scope": "algebraic ceiling conditional on the saved control errors, pair counts, and original fixed interval radius"},
        "reporting_failures": [],
    }
    summary_bytes = (json.dumps(summary, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    overall = summary["selection_comparison"]["overall_descriptive_summary"]
    identity = [r for r in ceiling_summary if r["hypothesis"] == "identity"]
    identity_layouts = [r for r in layout_ceilings if r["hypothesis"] == "identity"]
    note = [
        "# F15-ND01: selection generalization and fixed-control ceilings", "",
        "Contributor: ChatGPT (GPT-6 Astra Pro). Development diagnostics from saved statistics only.", "",
        "No population, model, fit, alignment choice, or evaluation was generated by this analysis. "
        "The complete original F15 assessment and the registered ND01 outputs remain unchanged.", "",
        "## Robust selection: discovery gains versus validation", "",
        f"Across the 100 family/budget/model/role comparisons, the robust selector changed "
        f"{overall['selected_subset_changes']} selected subsets. Its saved discovery maximum normalized "
        f"objective strictly improved in {overall['discovery_worst_normalized_objective_sign_counts']['positive']} "
        f"comparisons and tied in {overall['discovery_worst_normalized_objective_sign_counts']['tie']}, "
        f"using the registered 1e-12 tie band. Validation improved in "
        f"{overall['validation_worst_normalized_objective_sign_counts']['positive']}, worsened in "
        f"{overall['validation_worst_normalized_objective_sign_counts']['negative']}, and tied in "
        f"{overall['validation_worst_normalized_objective_sign_counts']['tie']}.", "",
        f"Strict discovery improvement reversed into validation loss in "
        f"{overall['strict_discovery_gain_and_validation_loss_worst_normalized_objective']} comparisons. "
        "These are paired settings, not 100 independent model replicates: the five networks, "
        "shared populations, nested candidate pools, and overlapping proposals create dependence.", "",
        "Positive numbers in the gain columns below favor robust selection. Each row averages "
        "the ten model/role pairs for one family and budget.", "",
        "| Family | Budget | Discovery worst-objective gain | Validation worst-objective gain | Discovery near-disagreement gain | Validation near-disagreement gain | Strict discovery gains reversing in validation |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in grouped_summary:
        d, v = r["mean_differences"]["discovery"], r["mean_differences"]["validation"]
        note.append(f"| {r['family']} | {r['budget']} | {d['worst_normalized_objective']:.6f} | {v['worst_normalized_objective']:.6f} | {d['near_disagreement']:.6f} | {v['near_disagreement']:.6f} | {r['strict_discovery_gain_and_validation_loss_worst_normalized_objective']}/10 |")
    note += ["", "The objective is the maximum of five MAE/.05 values, near disagreement/.35, "
             "and far disagreement/.10. It differs from average probability MSE, and the maximum "
             "and thresholded disagreement terms can react strongly to the 128 discovery pairs "
             "per stratum. A discovery-versus-validation reversal is consistent with selection "
             "on a noisy criterion. It does not isolate overfitting from finite-sample variation, "
             "objective tradeoffs, or the candidate pool's available interventions. No statistical "
             "test, new interval family, or new support disposition is introduced here.", "",
             "## Fixed-control advantage ceilings in constructed calibration", "",
             "For a saved control and an aligned intervention on the same rows,", "",
             "\\[\\Delta=\\operatorname{MAE}_{control}-\\operatorname{MAE}_{aligned}"
             "\\leq\\operatorname{MAE}_{control}.\\]", "",
             "The frozen matched-control radius is 0.022115658601168407. Thus an observed control "
             "must have MAE at least 0.03211565860116841 for even a hypothetical zero-error aligned "
             "intervention to attain a lower bound of 0.01 under that same radius. This keeps the "
             "original sample-range and multiplicity rule; it does not tighten the interval by "
             "assuming a new error distribution.", "",
             "| Identity control | Roles with a ceiling below the required lower bound | Mean control MAE | Range of zero-aligned-error lower-bound ceilings |",
             "|---|---:|---:|---:|"]
    for r in identity:
        note.append(f"| {r['control']} | {r['fixed_control_ceiling_below_margin_count']}/10 | {r['mean_control_mae']:.6f} | {r['minimum_zero_error_lower_bound_ceiling']:.6f} to {r['maximum_zero_error_lower_bound_ceiling']:.6f} |")
    note += ["", f"All {sum(r['at_least_one_fixed_control_blocks_margin_even_at_zero_aligned_error'] for r in identity_layouts)}/5 "
             "constructed layouts contain at least one such control. For these exact observed "
             "controls and this frozen radius, improving only the aligned error cannot meet "
             "every required control margin—even if that error were driven to zero.", "",
             "This diagnoses a limitation of interpreting the complete endpoint as a test for "
             "the presence of useful structure. The endpoint also requires an extraction "
             "advantage over capable competing searches. Its failure on this calibration does "
             "not negate the supported absolute correspondence checks. Nor does this calculation "
             "claim that every future control search, larger sample count, or different endpoint "
             "has the same ceiling. Passing the algebraic ceiling would be necessary, not "
             "sufficient, for full endpoint completion.", "",
             "The JSON includes all 160 hypothesis/role/control ceiling records, all 100 paired "
             "selector comparisons, original source paths and hashes, and the code hashes. "
             "The report can be reproduced without mutating outputs:", "",
             "```bash", "python v2/experiments/F15_ND01_analysis/selection_diagnostics.py --check", "```", "",
             f"Summary JSON SHA256: `{S.digest(summary_bytes)}`.", "",
             "Reporting failures in this analysis: none.", ""]
    return {"selection_diagnostics.json": summary_bytes,
            "selection_diagnostics.md": "\n".join(note).encode()}


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
        print(json.dumps({"status": "selection_diagnostics_byte_exact", "outputs": len(outputs)}))
        return
    if any((directory / name).exists() for name in outputs):
        raise FileExistsError("Refusing to overwrite selection diagnostics; use --check.")
    for name, data in outputs.items():
        with (directory / name).open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    print(json.dumps({"status": "selection_diagnostics_created", "outputs": [
        {"file": name, "bytes": len(data), "sha256": S.digest(data)} for name, data in outputs.items()]}))


if __name__ == "__main__":
    main()
