"""P3-09 observer reconstruction of preserved DEVELOPMENT score records.

No adapters, generators, policies, providers, reporters or private scorers run.
The amended analyzer is loaded from the source snapshot beside this script.
Old actual paid invoices remain unchanged. A5 enrichments are observer-only.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11. Principal credit: zero.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
SOURCE = HERE / "amended_v1" / "source" / "v3" / "experiments"
sys.path.insert(0, str(SOURCE))
spec = importlib.util.spec_from_file_location("_p309_alignment_amended_analyzer", SOURCE / "p309_analyze.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
REVIEWS = REPO / "v3/work_logs/P3_09_2026-10-11_S1/reviews"
checks = 0


def p(value):
    if value is None:
        return None
    value = F(value)
    return [value.numerator, value.denominator]


def f(value):
    return F(*value) if isinstance(value, (list, tuple)) else F(value)


def avg(values):
    return None if not values or any(v is None for v in values) else sum(map(f, values), F()) / len(values)


def hmean(rows, value):
    groups = {}
    for row in rows:
        groups.setdefault(row["unit"]["group_id"], []).append(value(row))
    return avg([avg(values) for values in groups.values()])


def eq(name, actual, expected):
    global checks
    checks += 1
    if actual != expected:
        raise AssertionError(json.dumps({"check": name, "actual": actual, "expected": expected}, sort_keys=True))


def read_bound(path, digest):
    data = path.read_bytes()
    eq("input source hash " + str(path), hashlib.sha256(data).hexdigest(), digest)
    return json.loads(data)


def common_loss(score, stakes):
    if score.get("full_horizon") is not True or score.get("validity_pass") is not True:
        return None
    fp, fn = f(stakes["fp"]), f(stakes["fn"])
    return (fp * score["false_positives"] + fn * score["false_negatives"]) / (score["horizon"] * max(fp, fn))


def main():
    config = {"analysis": {"loss_improvement_threshold": [1, 100],
                           "saving_ratio_threshold": [19, 20],
                           "report_width_improvement_threshold": [1, 100],
                           "repricing_grid": [[0, 1], [1, 100000], [1, 10000], [1, 1000], [1, 100]]}}
    saved = read_bound(REVIEWS / "broker_design/development_v1/run/results.json",
                       "7a2d6d7eba3699008f6d31a05eeb07fa0a02518bf11601f0ae630382022585e7")
    enriched = read_bound(REVIEWS / "broker_design/a5_observer_v1/run/results.json",
                          "6ac07c9920c79e68b6357d7f9366932134c259c8509bdb780f3f50ce5c022c78")
    comparisons = {row["id"]: row for row in enriched["results"] if not row["synthetic_observer_input"]}
    scores = {row["unit_id"]: deepcopy(row) for row in saved["scores"]}
    records = {row["unit"]["id"]: row for row in saved["public_records"]}
    eq("all broker records preserved", len(records), 30)
    eq("all score identities", sorted(scores), sorted(records))
    eq("all A5 identities", sorted(comparisons), sorted(records))
    rows = []
    quantity_count = 0
    for identifier, result in records.items():
        score = scores[identifier]
        extra = comparisons[identifier]
        # Real A5 rows reference the hash-bound original; only synthetic rows
        # embed an optional report. Reconstruct against the original below.
        eq("A5 record horizon binding", extra["horizon"], score["horizon"])
        eq("A5 real record is a reference", extra["optional_report"], None)
        score["paid_report_comparison"] = deepcopy(extra["comparison"])
        eq("original source units retained", score["source_units"], 65114)
        eq("source invoice agrees", result["common_source_invoice"]["total"], 65114)
        eq("terminal invoice agrees", score["local_units"], result["episode"]["meter"]["total"])
        eq("complete cold invoice", score["cold_units"], 65114 + score["local_units"])
        optional = result["optional_reporting"]
        optional_units = 0 if optional is None else optional["source_invoice"]["total"] + optional["report"]["meter"]["total"]
        eq("optional invoice retained", score["optional_reporting_units"], optional_units)
        eq("comparison separate fee", extra["comparison"]["additional_units"], optional_units)
        if optional is not None and optional["report"]["status"] == "success":
            report = optional["report"]
            for name, endpoint in report["intervals"].items():
                actual = extra["comparison"]["endpoints"][name]
                lo, hi = f(endpoint["lower"]), f(endpoint["upper"])
                dlo, dhi = map(f, report["deterministic_envelopes"][name])
                conflict = endpoint.get("confidence_conflict", False) or hi < lo
                gain = None if conflict else (dhi - dlo - hi + lo) / score["horizon"]
                eq("A5 independent width", actual["width"], None if conflict else p(hi - lo))
                eq("A5 independent envelope", actual["deterministic_width"], p(dhi - dlo))
                eq("A5 independent gain", actual["normalized_width_reduction"], p(gain))
                eq("A5 lower gain", actual["normalized_lower_endpoint_gain"], p((lo - dlo) / score["horizon"]))
                eq("A5 upper gain", actual["normalized_upper_endpoint_gain"], p((dhi - hi) / score["horizon"]))
                eq("A5 inclusive practical threshold", actual["practical_width_reduction"], gain is not None and gain >= F(1, 100))
                quantity_count += 1
        rows.append({"unit": deepcopy(result["unit"]), "score": score})
    eq("saved report quantity denominator", quantity_count, 21)
    group_ids = {row["unit"]["group_id"] for row in rows}
    eq("explicit development group", group_ids, {"development_broker_toy"})
    groups = {name: {"id": name, "recipe": {"family": "observer_DEVELOPMENT_toy",
                                            "horizon": 16, "prefix_length": 0}} for name in group_ids}
    output = A.broker_analysis(config, groups, rows)
    by_id = {row["unit"]["id"]: row for row in rows}
    for summary in output["configuration_means"]:
        bucket = [row for row in rows if row["unit"]["configuration_id"] == summary["configuration_id"]
                  and row["unit"]["stakes"] == summary["stakes"]]
        eq("configuration denominator", summary["planned_executions"], len(bucket))
        eq("cold cost denominator", summary["known_total_executed_cold_units"], sum(row["score"]["cold_units"] for row in bucket))
        complete = all(row["score"]["full_horizon"] is True and row["score"]["validity_pass"] is True for row in bucket)
        eq("complete configuration gate", summary["complete_primary_denominator"], complete)
        for name, actual in summary["means"].items():
            eq("configuration mean " + name, actual, p(hmean(bucket, lambda row: row["score"].get(name))))
        for sliced in summary["prespecified_slices"]:
            name = sliced["slice"]
            def values(row):
                return row["score"].get("first_occurrence") if name == "first_occurrence" else row["score"].get("segments", {}).get(name)
            def usable(row):
                return row["score"].get("full_horizon") is True and row["score"].get("validity_pass") is True and values(row) and values(row).get("full_horizon") is True
            eq("slice complete gate", sliced["complete_primary_denominator"], bool(all(usable(row) for row in bucket)))
            eq("slice exact denominator sum", sliced["known_scheduled_positions"], sum(values(row)["horizon"] for row in bucket if values(row)))
            eq("slice episode denominator", sliced["planned_episodes"], len(bucket))
            for metric, actual in sliced["means"].items():
                eq("slice mean " + metric, actual, p(hmean(bucket, lambda row: values(row).get(metric) if usable(row) else None)))
        reported = summary["paid_reporting"]
        requested = [row for row in bucket if row["unit"]["engine"] in ("broker", "mirror")]
        eq("A5 requested denominator", reported["planned_reports"], len(requested))
        if requested:
            eq("A5 aggregate complete bill", reported["known_total_additional_units"], sum(row["score"]["optional_reporting_units"] for row in requested))
            for name, reported_endpoint in reported["endpoints"].items():
                def report_usable(row):
                    rep = row["score"]["paid_report_comparison"]
                    return (row["score"]["full_horizon"] is True and row["score"]["validity_pass"] is True
                            and rep["status"] == "success" and rep.get("endpoints", {}).get(name, {}).get("status") == "success")
                eq("A5 full scheduled report gate", reported_endpoint["complete_report_denominator"], all(report_usable(row) for row in requested))
                for field, actual in reported_endpoint["means"].items():
                    expected = hmean(requested, lambda row: row["score"]["paid_report_comparison"]["endpoints"][name].get(field) if report_usable(row) else None)
                    eq("A5 aggregate mean " + field, actual, p(expected))
    for paired in output["paired_records"]:
        current, target = by_id[paired["unit_id"]], by_id[paired["target_id"]]
        left, right = current["score"], target["score"]
        cl, tl = common_loss(left, current["unit"]["stakes"]), common_loss(right, current["unit"]["stakes"])
        delta = None if cl is None or tl is None else tl - cl
        eq("paired common stakes action", paired["differences"]["action_loss_mean_target_minus_current"], p(delta))
        price = f(left["native_price_normalized"]) if left["native_price_normalized"] is not None else F()
        objective = None if delta is None else delta + price * F(right["cold_units"] - left["cold_units"], left["horizon"])
        eq("paired common objective", paired["differences"]["common_native_objective_target_minus_current"], p(objective))
        full = cl is not None and tl is not None
        ratio = F(left["cold_units"], right["cold_units"]) if full and right["cold_units"] > 0 else None
        eq("paired complete cold ratio", paired["cold_cost_ratio_current_to_target"], p(ratio))
        same = (full and left["delivered_path_sha256"] == right["delivered_path_sha256"]
                and left["action_path_sha256"] == right["action_path_sha256"]
                and left["brier_mean"] == right["brier_mean"] and delta == 0)
        eq("paired output eligibility", paired["equal_delivered_output"], same)
        eq("paired five percent predicate", paired["practical_equal_output_cost_saving"], bool(same and ratio is not None and ratio <= F(19, 20)))
    eq("all planned toy pair links", len(output["paired_records"]), 11)

    # The initial false improvement witness, reconstructed under the new helper.
    unchanged = {"full_horizon": True, "validity_pass": True, "horizon": 2,
                 "false_positives": 1, "false_negatives": 0}
    eq("unchanged actions under one asymmetric objective", p(A.common_stakes_action_loss(unchanged, {"fp": [1, 2], "fn": [3, 2]})), [1, 6])
    eq("unchanged paired decision gain is zero", p(A.common_stakes_action_loss(unchanged, {"fp": [1, 2], "fn": [3, 2]}) - A.common_stakes_action_loss(unchanged, {"fp": [1, 2], "fn": [3, 2]})), [0, 1])

    # A1 failure injection affects a copied observer dictionary only. Every
    # public record and original score stays byte-for-byte unchanged on disk.
    mirror = next(row for row in rows if row["unit"]["pairing"].get("identity_of"))
    changed = deepcopy(rows)
    changed_row = next(row for row in changed if row["unit"]["id"] == mirror["unit"]["id"])
    changed_row["score"]["cold_units"] += 1
    changed_row["score"]["local_units"] += 1
    negative = A.broker_analysis(config, groups, changed)
    pair_record = next(row for row in negative["paired_records"] if row["unit_id"] == mirror["unit"]["id"] and row["relation"] == "identity_of")
    eq("mirror paid identity failure detected", pair_record["ordinary_identity_pass"], False)
    eq("mirror failure enters combined A1 list", mirror["unit"]["id"] in negative["coupling_violations"], True)

    result = {"stage": "P3-09-DEVELOPMENT-OBSERVER-RECONSTRUCTION", "principal_clock_credit": 0,
              "adapter_endpoint_calls": 0, "policy_calls": 0, "reporter_calls": 0,
              "private_truth_calls": 0, "final_generation_calls": 0,
              "checks": checks, "status": "PASS", "public_records": len(rows),
              "pair_links": len(output["paired_records"]), "report_quantities": quantity_count,
              "original_source_units_per_episode": 65114,
              "prospective_source_units_not_substituted": 66076,
              "input_scope": "One old DEVELOPMENT toy and two deliberate denials. One development seed. Whole-only segment data; not a balanced final panel, transfer result, or new source-cost execution.",
              "observer_enrichment": "Paid-report comparisons were attached to copies of preserved scores and independently reconstructed from the saved paid report envelopes.",
              "analyzer_sha256": hashlib.sha256((SOURCE / "p309_analyze.py").read_bytes()).hexdigest(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "broker_analysis": output,
              "synthetic_mirror_invoice_failure": pair_record}
    return result


if __name__ == "__main__":
    try:
        result = main()
    except Exception as error:
        result = {"stage": "P3-09-DEVELOPMENT-OBSERVER-RECONSTRUCTION", "principal_clock_credit": 0,
                  "status": "FAIL", "checks_completed": checks, "error": repr(error),
                  "traceback": traceback.format_exc(), "no_worker_or_final_endpoint_calls": True}
    target = HERE / "amended_v1" / "replay_results_v2.json"
    with target.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": result["status"], "checks": checks,
                      "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                      "error": result.get("error")}))
