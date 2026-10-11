"""Observer-only certificate aggregate reconstruction from 13 saved toys.

Original v1 paid invoices remain unchanged. The three separate direct reserve
probes have no standardized history score and are not invented as catalogue rows.
No scientific worker, generator, receiver or private scorer is imported/called.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11. Principal credit: zero.
"""
from collections import Counter
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
SOURCE = HERE / "amended_v1/source/v3/experiments"
sys.path.insert(0, str(SOURCE))
spec = importlib.util.spec_from_file_location("_p309_alignment_certificate_analyzer", SOURCE / "p309_analyze.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
count = 0


def check(label, actual, expected):
    global count
    count += 1
    if actual != expected:
        raise AssertionError(repr((label, actual, expected)))


def pair(value):
    return [value.numerator, value.denominator]


def main():
    path = REPO / "v3/work_logs/P3_09_2026-10-11_S1/reviews/structural_design/development_smoke_v1/results.json"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    check("saved input hash", digest, "819dce1ed0e4f44f43a062ae683c1a4f56e2263bc567b951e839692e3eaf5c0c")
    saved = json.loads(path.read_text())
    check("standardized history denominator", len(saved["histories"]), 13)
    check("original paid attempt count", sum(len(h["paid_rows"]) for h in saved["histories"]), 52)
    rows, groups = [], {}
    for history in saved["histories"]:
        score = history["score"]
        check("original score version retained", score["version"], "p309-certificates-v1")
        total = consumer = source = 0
        raw = Counter()
        delivered = []
        for row in history["paid_rows"]:
            local_total = local_consumer = 0
            for stage, categories in row["invoice"]["by_stage"].items():
                amount = sum(categories.values())
                local_total += amount
                if stage.startswith("receiver_") or stage in ("terminal", "failure_terminal", "common_source"):
                    local_consumer += amount
                if stage == "common_source":
                    source += amount
                raw.update(categories)
            check("request full invoice", local_total, row["invoice"]["total_units"])
            check("request consumer invoice", local_consumer, row["invoice"]["consumer_units"])
            total += local_total
            consumer += local_consumer
            if row["status"] == "DELIVERED":
                delivered.append(row["shared_request_id"])
        partition = {"producer": total - consumer, "consumer": consumer,
                     "output": sum(v for k, v in raw.items() if k.endswith("_output_bytes") or k == "terminal_bytes"),
                     "storage": raw.get("live_serialized_byte_periods", 0), "source": source}
        check("complete history total", score["total_units"], total)
        check("complete history consumer", score["consumer_units"], consumer)
        check("primitive categories", score["tariff_category_totals"], dict(raw))
        check("partition and diagnostics", score["category_totals"], partition)
        check("delivered request identities", sorted(score["delivered_request_ids"]), sorted(delivered))
        check("three expected valid deliveries", len(delivered), 3)
        rows.append({"unit": score["unit"], "score": score})
        groups[score["group_id"]] = {"recipe": {"family": score["population_recipe"]["family"]}}
    config = {"analysis": {"saving_ratio_threshold": [19, 20]}}
    output = A.certificate_analysis(config, groups, rows)
    lookup = {(r["scope"], r["recipient"], r["budget_condition"], r["method"]): r
              for r in output["complete_histories"]}
    for comparison in output["coverage_cost_comparisons"]:
        base = (comparison["scope"], comparison["recipient"], comparison["budget_condition"])
        left, right = lookup[base + (comparison["left"],)], lookup[base + (comparison["right"],)]
        lset, rset = set(left["delivered_request_ids"]), set(right["delivered_request_ids"])
        admissible = left["validity_pass"] and right["validity_pass"] and left["total_units"] is not None and right["total_units"] is not None
        service = bool(lset) and lset >= rset
        ratio = F(left["total_units"], right["total_units"])
        check("exact cost ratio", comparison["left_to_right_total_cost_ratio"], pair(ratio))
        check("coverage subset relation", comparison["coverage_superset"], lset >= rset)
        check("whole service identity", comparison["identical_coverage"], lset == rset)
        check("complete-service qualifier", comparison["both_complete"], left["complete_service"] and right["complete_service"])
        check("inclusive five percent cost predicate", comparison["left_practical_cost_dominance"], bool(admissible and service and ratio <= F(19, 20)))
        check("weak cost predicate", comparison["left_weakly_dominates"], bool(admissible and service and ratio <= 1))
        # Each fixture supplies complete vectors; missing primitive keys denote
        # genuine zero counts, not an omitted invoice or missing observation.
        stage_dom = all(left["category_totals"][k] <= right["category_totals"][k] for k in left["category_totals"])
        keys = set(left["tariff_category_totals"]) | set(right["tariff_category_totals"])
        primitive_dom = all(left["tariff_category_totals"].get(k, 0) <= right["tariff_category_totals"].get(k, 0) for k in keys)
        check("named stage diagnostic vector order", comparison["componentwise_named_diagnostic_dominance"], bool(admissible and service and stage_dom))
        check("primitive tariff vector order", comparison["componentwise_primitive_tariff_dominance"], bool(admissible and service and primitive_dom))
    # Reuse the original price-order counterexample under the newly separated
    # field names. These are hand-written observer dictionaries, not paid runs.
    def toy(method, bill, raw):
        return {"unit": {"group_id": "dev-resource-vector", "recipient": "fresh", "budget_condition": "development",
                         "method": method, "method_kind": "ordinary"},
                "score": {"all_request_ids": ["dev-request"], "delivered_request_ids": ["dev-request"],
                          "request_count": 1, "total_units": bill, "validity_pass": True,
                          "category_totals": {"producer": 0, "consumer": bill, "output": 0, "storage": 0, "source": 0},
                          "tariff_category_totals": raw, "category_totals_complete": True}}
    synthetic = A.certificate_analysis(config, {"dev-resource-vector": {"recipe": {"family": "DEVELOPMENT_vector"}}},
                                       [toy("a", 90, {"native_calls": 90}), toy("b", 100, {"opcode_events": 100})])
    row = next(r for r in synthetic["coverage_cost_comparisons"] if r["left"] == "a")
    check("aggregate stage vector still ordered", row["componentwise_named_diagnostic_dominance"], True)
    check("primitive price counterexample now distinguished", row["componentwise_primitive_tariff_dominance"], False)
    return {"stage": "P3-09-DEVELOPMENT-OBSERVER-RECONSTRUCTION", "status": "PASS", "checks": count,
            "principal_clock_credit": 0, "worker_generator_receiver_private_score_calls": 0,
            "source_data_sha256": digest, "histories": 13, "paid_attempts_in_histories": 52,
            "direct_reserve_probes_excluded_from_catalogue": 3,
            "saved_v1_invoices_repriced": False,
            "analyzer_sha256": hashlib.sha256((SOURCE / "p309_analyze.py").read_bytes()).hexdigest(),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "analysis": output, "synthetic_resource_comparison": row,
            "scope": "One exposed two-bit DEVELOPMENT family, full condition only, seven fresh and six resident methods. All methods correctly decline the deliberately false second bound. No final transfer or cap claim."}


if __name__ == "__main__":
    try:
        result = main()
    except Exception as error:
        result = {"stage": "P3-09-DEVELOPMENT-OBSERVER-RECONSTRUCTION", "status": "FAIL",
                  "checks_completed": count, "error": repr(error), "traceback": traceback.format_exc(),
                  "principal_clock_credit": 0, "worker_or_final_endpoint_calls": 0}
    out = HERE / "amended_v1/certificate_results.json"
    with out.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": result["status"], "checks": count,
                      "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "error": result.get("error")}))
