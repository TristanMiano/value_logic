#!/usr/bin/env python3
"""Project the successful saved observer output into complete exact tables.

This is table production after observer completion. It does not execute an
observer, import experiment code, or open any final public/private payload.
Every output is created exclusively. The original observer output is unchanged.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path


W = Path(__file__).resolve().parent
RPATH = W / "attempt_A1_01/reconstructed.json"
SPATH = W / "attempt_A1_01/summary.json"
D = json.loads(RPATH.read_text())
SUMMARY = json.loads(SPATH.read_text())
THRESHOLD = Fraction(1, 100)


def rational(value):
    return Fraction(*value)


def pair(value):
    return [value.numerator, value.denominator]


def exact(value):
    return "unavailable" if value is None else str(rational(value))


def decimal(value):
    return "unavailable" if value is None else f"{float(rational(value)):.10f}"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def configuration(family, identifier):
    return next(c for c in D["configuration_means"]
                if c["family"] == family and c["configuration_id"] == identifier)


def slice_row(c, s):
    return {"family": c["family"], "configuration_id": c["configuration_id"],
            "method_kind": c["method_kind"], "stakes": c["stakes"], **s}


def table(lines, headers, rows):
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(v).replace("|", "\\|") for v in row) + " |")
    lines.append("")


assert SUMMARY["status"] == "PASS" and SUMMARY["mismatch_count"] == 0
assert len(D["configuration_means"]) == 76
assert len(D["independent_per_unit_metrics"]) == 336
assert len(D["catalogue_comparisons"]) == 54
assert len(D["paired_configuration_effects"]) == 25
assert len(D["paired_records"]) == 150
candidate_comparisons = [c for row in D["catalogue_comparisons"] for c in row["candidate_comparisons"]]
assert len(candidate_comparisons) == 120
assert all(rational(c["distinct_ordinary_minus_candidate"]) < 0 for c in candidate_comparisons)
assert all(c["complete_primary_denominator"] for c in D["configuration_means"])

main = []
main_slices = []
all_slices = []
for c in D["configuration_means"]:
    all_slices.extend(slice_row(c, s) for s in c["prespecified_slices"])
for family in ["mixed", "cheap_null", "gate_transfer"]:
    for selector in ["uniform", "tickets"]:
        c = configuration(family, f"value_{selector}_cold")
        cached = configuration(family, f"value_{selector}_cached_hashed")
        for field in ["brier_mean", "base_brier_mean", "uniform_brier_mean", "action_loss_mean"]:
            assert c["means"][field] == cached["means"][field]
        main.append({
            "family": family, "selector": selector,
            "configuration_ids": [c["configuration_id"], cached["configuration_id"]],
            "complete_primary_denominator": c["complete_primary_denominator"],
            "planned_executions_per_configuration": c["planned_executions"],
            "uniform_brier_mean": c["means"]["uniform_brier_mean"],
            "base_brier_mean": c["means"]["base_brier_mean"],
            "issued_brier_mean": c["means"]["brier_mean"],
            "uniform_minus_base_brier": c["uniform_minus_base_brier"],
            "practical_learning_effect": c["practical_learning_effect"],
            "action_loss_mean": c["means"]["action_loss_mean"],
            "cold_mean_units": c["means"]["cold_units"],
            "cached_mean_units": cached["means"]["cold_units"],
        })
        main_slices.extend(slice_row(c, s) for s in c["prespecified_slices"])

catalogue_by_cell = defaultdict(dict)
for c in D["catalogue_comparisons"]:
    key = (c["family"], json.dumps(c["stakes"], sort_keys=True),
           tuple(c["price_normalized_per_unit"]))
    catalogue_by_cell[key][c["selection"]] = c
native_fixed_differences = []
for (family, stakes, price), selections in catalogue_by_cell.items():
    fixed = selections["fixed_record_repricing"]["distinct_ordinary_minimum"]
    native = selections["native_price_catalogue"]["distinct_ordinary_minimum"]
    if fixed != native:
        native_fixed_differences.append({"family": family,
                                        "stakes": json.loads(stakes),
                                        "price": list(price),
                                        "fixed_record": fixed,
                                        "native_price": native})

dominance = []
for family, ordinary in [("mixed", "proof_dpll_fallback1"),
                         ("cheap_null", "exact_dpll"),
                         ("gate_transfer", "probability_cost")]:
    o = configuration(family, ordinary)
    for c in D["configuration_means"]:
        if c["family"] != family or c["method_kind"] != "candidate":
            continue
        delta_a = rational(c["means"]["action_loss_mean"]) - rational(o["means"]["action_loss_mean"])
        delta_b = rational(c["mean_cold_units_per_request"]) - rational(o["mean_cold_units_per_request"])
        assert c["stakes"] == o["stakes"]
        assert c["complete_primary_denominator"] and o["complete_primary_denominator"]
        assert delta_a > 0 and delta_b > 0
        dominance.append({
            "scope": "Derived fixed-record action-plus-cold-cost inequality; not a new deployed policy or a replacement endpoint",
            "family": family, "ordinary": ordinary, "candidate": c["configuration_id"],
            "ordinary_action_loss_mean": o["means"]["action_loss_mean"],
            "ordinary_mean_cold_units_per_request": o["mean_cold_units_per_request"],
            "candidate_minus_ordinary_action": pair(delta_a),
            "candidate_minus_ordinary_cold_per_request": pair(delta_b),
            "strict_ordinary_objective_advantage_all_nonnegative_prices": True,
            "complete_outer_attempt_economic_claim_permitted": False,
        })

reports = []
report_endpoint_rows = []
fees_by_family = Counter()
signs = defaultdict(Counter)
ranges = defaultdict(list)
for c in D["configuration_means"]:
    r = c["paid_reporting"]
    if not r["requested"]:
        continue
    reports.append({"family": c["family"], "configuration_id": c["configuration_id"], **r})
    fees_by_family[c["family"]] += r["known_total_additional_units"]
    for endpoint, value in r["endpoints"].items():
        report_endpoint_rows.append({"family": c["family"],
                                     "configuration_id": c["configuration_id"],
                                     "endpoint": endpoint, **value})
for unit in D["independent_per_unit_metrics"]:
    r = unit["score"].get("paid_report_comparison", {})
    if r.get("status") != "success":
        continue
    for endpoint, value in r["endpoints"].items():
        for metric in ["normalized_width_reduction", "normalized_lower_endpoint_gain",
                       "normalized_upper_endpoint_gain"]:
            q = rational(value[metric])
            signs[(endpoint, metric)]["negative" if q < 0 else "zero" if q == 0 else "positive"] += 1
            ranges[(endpoint, metric)].append(q)
report_sign_rows = []
for (endpoint, metric), counts in sorted(signs.items()):
    values = ranges[(endpoint, metric)]
    report_sign_rows.append({"endpoint": endpoint, "metric": metric,
                             "counts": dict(counts), "minimum": pair(min(values)),
                             "maximum": pair(max(values)),
                             "individual_reports_at_least_001": sum(v >= THRESHOLD for v in values),
                             "individual_counts_are_not_configuration_primary_effects": True})

out = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "contributor": "ChatGPT (GPT-6 Astra Pro)",
    "reviewer_agent": "/root/freeze_review",
    "task": "P3-10",
    "amendment_id": "P3-10-A1",
    "amendment_manifest_sha256": SUMMARY["amendment_manifest_sha256"],
    "principal_research_minutes_claimed": 0,
    "source_reconstructed_sha256": sha(RPATH),
    "source_summary_sha256": sha(SPATH),
    "projector_sha256": sha(Path(__file__)),
    "rational_encoding": "[integer numerator, positive integer denominator]; no decimal is authoritative",
    "mean_hierarchy": "For each whole fixed configuration: equal prescribed seed-slot weight within each population, then equal prescribed population weight. Each slice uses its parent hierarchy and complete planned denominator.",
    "positive_action_or_learning_threshold": [1, 100],
    "equal_output_cost_maximum_ratio": [19, 20],
    "complete_outer_attempt_economic_claim_permitted": False,
    "source_observer_summary": SUMMARY,
    "main_candidate_whole": main,
    "main_candidate_slices": main_slices,
    "all_configuration_summaries": D["configuration_means"],
    "all_configuration_slices": all_slices,
    "paired_configuration_effects": D["paired_configuration_effects"],
    "paired_records": D["paired_records"],
    "pair_relation_counts": dict(Counter(x["relation"] for x in D["paired_records"])),
    "catalogue_comparisons": D["catalogue_comparisons"],
    "native_fixed_catalogue_differences": native_fixed_differences,
    "derived_fixed_record_ordinary_dominance": dominance,
    "report_configuration_summaries": reports,
    "report_endpoint_rows": report_endpoint_rows,
    "report_individual_endpoint_sign_counts": report_sign_rows,
    "known_total_report_fees_by_family": dict(fees_by_family),
    "known_total_report_fees": sum(fees_by_family.values()),
}
assert len(all_slices) == 200 and len(main_slices) == 16
assert len(reports) == 21 and len(report_endpoint_rows) == 63
assert len(native_fixed_differences) == 5
assert len(dominance) == 12
assert sum(fees_by_family.values()) == 65_407_686

lines = ["# P3-10-A1 exact broker interpretation tables", "",
         "Contributor: **ChatGPT (GPT-6 Astra Pro)**, agent `/root/freeze_review`.", "",
         "These tables project the single successful independent saved-JSON observer run. They do not constitute another observer attempt or any paid replay. Exact fractions are authoritative; the companion JSON preserves every configuration denominator, paired record, fixed expert readout, catalogue tie, report endpoint and fee.", "",
         "All means use the frozen equal-seed-within-population, then equal-population hierarchy. The global end-to-end economic gate is false because the original failed public prefix has unknown cost. Zero-price action effects remain separate from cost claims. Agent time adds zero principal Research90 minutes.", "",
         f"Reconstructed source SHA-256: `{sha(RPATH)}`.", "",
         "## Main candidate whole means", "",
         "Each row has a cold and cached configuration with exactly equal issued/base Brier and action means; the two bills are retained separately below.", ""]
table(lines, ["Family", "Selector", "Equal Brier", "Base Brier", "Issued Brier", "Equal − base", "Action W", "A2 ≥ .01"],
      [[r["family"], r["selector"], exact(r["uniform_brier_mean"]), exact(r["base_brier_mean"]),
        exact(r["issued_brier_mean"]), exact(r["uniform_minus_base_brier"]),
        exact(r["action_loss_mean"]), r["practical_learning_effect"]] for r in main])
lines += ["## All main candidate slices", "",
          "These are all 16 selector/family/slice cells. Cached variants have the same mathematical paths. Position totals below are executed denominators, not independent observations.", ""]
table(lines, ["Family", "Configuration", "Slice", "Positions", "Equal Brier", "Base Brier", "Issued Brier", "Equal − base", "W", "A2 ≥ .01"],
      [[r["family"], r["configuration_id"], r["slice"], r["known_scheduled_positions"],
        exact(r["means"]["uniform_brier_mean"]), exact(r["means"]["base_brier_mean"]),
        exact(r["means"]["brier_mean"]), exact(r["uniform_minus_base_brier"]),
        exact(r["means"]["action_loss_mean"]), r["practical_learning_effect"]] for r in main_slices])
lines += ["## Original expert and readout retention", "",
          "The six experts are retained in their frozen index order. Same-hard-mask values are descriptive readouts of the recorded history.", ""]
table(lines, ["Family", "Configuration", "Slice", "Experts 0–5", "Half", "Dyadic equal", "Same hard equal", "Same hard half"],
      [[r["family"], r["configuration_id"], r["slice"],
        "; ".join(exact(v) for v in r["forecast_readout_means"]["expert_brier_means"]),
        exact(r["forecast_readout_means"]["constant_half_brier_mean"]),
        exact(r["forecast_readout_means"]["dyadic_equal_mixture_brier_mean"]),
        exact(r["forecast_readout_means"]["same_hard_mask_equal_mixture_brier_mean"]),
        exact(r["forecast_readout_means"]["same_hard_mask_half_brier_mean"])] for r in main_slices])
lines += ["## All 76 whole configuration means", "",
          "The JSON retains native price, stakes, group/seed slots, complete denominators, total executed bills and report details. N/A fields remain unavailable instead of becoming zero.", ""]
table(lines, ["Family", "Configuration", "Kind", "Episodes", "Brier", "Base Brier", "W", "Cold units", "Cold/T", "Equal − base", "Report units"],
      [[c["family"], c["configuration_id"], c["method_kind"], c["planned_executions"],
        exact(c["means"]["brier_mean"]), exact(c["means"]["base_brier_mean"]),
        exact(c["means"]["action_loss_mean"]), exact(c["means"]["cold_units"]),
        exact(c["mean_cold_units_per_request"]), exact(c["uniform_minus_base_brier"]),
        exact(c["means"]["optional_reporting_units"])] for c in D["configuration_means"]])
lines += ["## All 200 prespecified configuration slices", "",
          "All per-episode planned and closed denominators, original experts and readouts are in the JSON. No incomplete parent was omitted; all were complete and valid.", ""]
table(lines, ["Family", "Configuration", "Slice", "Positions", "Brier", "Base Brier", "W", "Equal − base", "A2 ≥ .01"],
      [[r["family"], r["configuration_id"], r["slice"], r["known_scheduled_positions"],
        exact(r["means"]["brier_mean"]), exact(r["means"]["base_brier_mean"]),
        exact(r["means"]["action_loss_mean"]), exact(r["uniform_minus_base_brier"]),
        r["practical_learning_effect"]] for r in all_slices])
lines += ["## All 25 paired configuration effects", "",
          "Differences are target minus current under current common stakes and common normalized price. The cost ratio is the ratio of hierarchical mean bills, current/target. Complete-path threshold flags and globally admissible cost flags are distinct; see the exact JSON for both.", ""]
table(lines, ["Family", "Current configuration", "Relation", "Pairs", "ΔW", "Current/target cost", "ΔJ", "Equal output", "Completed ΔJ ≥ .01", "Allowed ΔJ claim"],
      [[r["family"], r["configuration_id"], r["relation"], r["paired_executions"],
        exact(r["mean_action_improvement"]), exact(r["mean_cold_cost_ratio"]),
        exact(r["mean_common_objective_improvement"]), r["every_pair_equal_delivered_output"],
        r["completed_path_priced_threshold_met"], r["practical_priced_effect"]]
       for r in D["paired_configuration_effects"]])
lines += ["## All 54 catalogue minima and ties", "",
          "Whole fixed configurations are averaged before minimization. Native-price and fixed-record catalogues remain separate; ties are exact. All 120 candidate comparisons across the 30 applicable rows have negative distinct-ordinary-minus-candidate differences. The other 24 asymmetric rows schedule no candidate.", ""]
table(lines, ["Family", "(fp, fn)", "Selection", "Price", "Distinct minimum", "Tied ordinary configurations", "Candidate comparisons"],
      [[r["family"], f"({exact(r['stakes']['fp'])}, {exact(r['stakes']['fn'])})", r["selection"],
        exact(r["price_normalized_per_unit"]), exact(r["distinct_ordinary_minimum"]["value"]),
        ", ".join(r["distinct_ordinary_minimum"]["ties"]), len(r["candidate_comparisons"])]
       for r in D["catalogue_comparisons"]])
lines += ["## Supplemental fixed-record ordinary dominance", "",
          "Each exact row has positive a and b in J(candidate) − J(ordinary) = a + λb, hence the ordinary path has strictly smaller terminal priced objective for every λ ≥ 0. This is a derived path comparison under the declared tariff, not a new controller, forecast-field dominance, or an end-to-end economic claim.", ""]
table(lines, ["Family", "Ordinary", "Candidate", "a: candidate − ordinary W", "b: candidate − ordinary cold/T"],
      [[r["family"], r["ordinary"], r["candidate"], exact(r["candidate_minus_ordinary_action"]),
        exact(r["candidate_minus_ordinary_cold_per_request"])] for r in dominance])
lines += ["## All 63 report configuration endpoints", "",
          "126 scheduled reports all succeeded. Width differences and endpoint gains are normalized by full scheduled horizon. These 63 rows cover F/V/Z for all 21 configurations, including the executed identity mirror. They do not estimate confidence coverage.", ""]
table(lines, ["Family", "Configuration", "Quantity", "Deterministic width/T", "Delivered width/T", "Width gain/T", "Lower gain/T", "Upper gain/T", "Gain ≥ .01"],
      [[r["family"], r["configuration_id"], r["endpoint"],
        exact(r["means"]["deterministic_width_per_horizon"]),
        exact(r["means"]["width_per_horizon"]), exact(r["means"]["normalized_width_reduction"]),
        exact(r["means"]["normalized_lower_endpoint_gain"]),
        exact(r["means"]["normalized_upper_endpoint_gain"]), r["practical_width_reduction"]]
       for r in report_endpoint_rows])
lines += ["## Report fees", "",
          "These fees are additional to terminal-answer bills. Summing fee totals counts actual executions, including mirrors, and does not add statistical replication.", ""]
table(lines, ["Family", "Configuration", "Scheduled reports", "Mean additional units", "Total additional units"],
      [[r["family"], r["configuration_id"], r["planned_reports"], exact(r["mean_additional_units"]),
        r["known_total_additional_units"]] for r in reports])
lines += [f"All actual report fees: **{sum(fees_by_family.values()):,} units**.", "",
          "## Individual-report endpoint signs", "",
          "These counts disclose all zero/positive/adverse endpoint results. Individual threshold hits are descriptive and do not replace a fixed configuration mean.", ""]
table(lines, ["Quantity", "Metric", "Negative", "Zero", "Positive", "Individual ≥ .01", "Minimum", "Maximum"],
      [[r["endpoint"], r["metric"], r["counts"].get("negative", 0), r["counts"].get("zero", 0),
        r["counts"].get("positive", 0), r["individual_reports_at_least_001"],
        exact(r["minimum"]), exact(r["maximum"])] for r in report_sign_rows])

with (W / "findings_tables_A1.json").open("x") as handle:
    json.dump(out, handle, indent=2, sort_keys=True)
    handle.write("\n")
with (W / "findings_tables_A1.md").open("x") as handle:
    handle.write("\n".join(lines) + "\n")
print(json.dumps({"status": "TABLES_WRITTEN", "configuration_rows": 76,
                  "slice_rows": 200, "pair_aggregates": 25, "catalogue_rows": 54,
                  "report_endpoint_rows": 63,
                  "json_sha256": sha(W / "findings_tables_A1.json"),
                  "markdown_sha256": sha(W / "findings_tables_A1.md")}))
