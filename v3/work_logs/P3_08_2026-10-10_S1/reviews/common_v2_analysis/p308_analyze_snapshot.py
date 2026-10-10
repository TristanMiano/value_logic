"""Offline, exact DEVELOPMENT analysis of the sealed common-v2 comparison.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
This private evaluator reads completed score records. It is not a deployed
selector, future performance predictor, price-tuning rule, or coverage study.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json


def pair(q):
    return [q.numerator, q.denominator]


def run(source, out):
    source, out = Path(source), Path(out)
    out.mkdir(parents=True, exist_ok=False)
    data = json.loads(source.read_text())
    rows = data["runs"]
    assert len(rows) == 186 and all(r["status"] == "success" and r["full_horizon"] for r in rows)
    scenarios = sorted({r["scenario"] for r in rows})
    prices = [F(0), F(1,100000), F(1,10000), F(1,1000), F(1,100)]
    seeds = (11,29,47)

    def find(scenario, method, seed, price=None):
        candidates = [r for r in rows if r["scenario"] == scenario
                      and r["configuration"]["method"] == method
                      and r["configuration"]["seed"] == seed
                      and (price is None or F(r["configuration"].get("unit_price", "0")) == price)]
        assert len(candidates) == 1
        return candidates[0]

    index_pairs, hard_pairs = [], []
    for scenario in scenarios:
        for seed in seeds:
            for selector in ("uniform", "tickets"):
                base = find(scenario, "finite_"+selector, seed)
                linear = find(scenario, "value_"+selector, seed)
                hashed = find(scenario, "value_"+selector+"_hashed", seed)
                assert linear["terminal_errors"] == hashed["terminal_errors"]
                assert linear["issued_brier"] == hashed["issued_brier"]
                assert linear["purchases"] == hashed["purchases"]
                assert linear["optional_reporting_units"] == hashed["optional_reporting_units"]
                index_pairs.append({"scenario": scenario, "seed": seed, "selector": selector,
                                    "linear_minus_hashed_units": linear["local_units"]-hashed["local_units"],
                                    "identical_performance": True})
                for candidate in (linear, hashed):
                    saved_errors = base["terminal_errors"]-candidate["terminal_errors"]
                    extra_units = candidate["local_units"]-base["local_units"]
                    assert saved_errors >= 0 and extra_units > 0
                    # This is a repricing threshold on two fixed realized
                    # paths, not a new price-sensitive controller run.
                    hard_pairs.append({"scenario": scenario, "seed": seed,
                                       "method": candidate["configuration"]["method"],
                                       "saved_errors": saved_errors, "extra_units": extra_units,
                                       "strict_fixed_record_benefit_if_lambda_below": pair(F(saved_errors, extra_units)),
                                       "zero_price_tie_if_no_saved_errors": saved_errors == 0})
    ordinary_hash_pairs = []
    for scenario in scenarios:
        pairs = [(find(scenario,"exact_cache",11), find(scenario,"exact_cache_hashed",11))]
        pairs += [(find(scenario,"ordinary_combo",seed,price), find(scenario,"ordinary_combo_hashed",seed,price))
                  for seed in seeds for price in prices]
        for linear, hashed in pairs:
            assert linear["terminal_errors"] == hashed["terminal_errors"]
            assert linear["issued_brier"] == hashed["issued_brier"]
            assert linear["purchases"] == hashed["purchases"]
            ordinary_hash_pairs.append({"scenario": scenario,
                "configuration": linear["configuration"],
                "linear_minus_hashed_units": linear["local_units"]-hashed["local_units"],
                "identical_performance": True})

    native_price_comparisons = []
    for scenario in scenarios:
        for seed in seeds:
            for price in prices:
                eligible = [r for r in rows if r["scenario"] == scenario and (
                    r["configuration"]["seed"] == seed
                    or (r["configuration"]["seed"] == 11 and r["configuration"]["method"] in (
                        "proof_enumeration","proof_dpll","exact_enumeration","exact_dpll",
                        "exact_cache","exact_cache_hashed","no_compute_0","no_compute_1")))]
                eligible = [r for r in eligible if not r["configuration"]["method"].startswith("ordinary_combo")
                            or F(r["configuration"]["unit_price"]) == price]
                costs = {r["run_id"]: F(r["terminal_errors"])+price*r["cold_units"] for r in eligible}
                minimum = min(costs.values())
                best = [r["run_id"] for r in eligible if costs[r["run_id"]] == minimum]
                ordinary = [r for r in eligible if r["configuration"]["kind"] == "ordinary"]
                ordinary_min = min(costs[r["run_id"]] for r in ordinary)
                ordinary_best = [r["run_id"] for r in ordinary if costs[r["run_id"]] == ordinary_min]
                native_price_comparisons.append({"scenario":scenario,"seed":seed,"price":pair(price),
                    "best_catalogue_cost":pair(minimum),"best_catalogue_records":best,
                    "best_distinct_ordinary_cost":pair(ordinary_min),"best_distinct_ordinary_records":ordinary_best,
                    "ordinary_mirrors_can_equal_each_broker_record":True,
                    "posthoc_best_is_deployed_policy":False,
                    "each_combo_uses_its_native_price":True})
    summaries = []
    groups = {}
    for row in rows:
        key = (row["scenario"],row["configuration"]["method"],row["configuration"].get("unit_price","fixed"))
        groups.setdefault(key,[]).append(row)
    for (scenario,method,price), group in sorted(groups.items()):
        summaries.append({"scenario":scenario,"method":method,"policy_price":price,"run_count":len(group),
            "mean_errors":pair(F(sum(r["terminal_errors"] for r in group),len(group))),
            "min_errors":min(r["terminal_errors"] for r in group),"max_errors":max(r["terminal_errors"] for r in group),
            "mean_local_units":pair(F(sum(r["local_units"] for r in group),len(group))),
            "min_local_units":min(r["local_units"] for r in group),"max_local_units":max(r["local_units"] for r in group),
            "mean_issued_brier":pair(sum((F(*r["issued_brier"]) for r in group),F(0))/len(group)),
            "seed_means_establish_coverage_or_generalization":False})
    record = {"stage":"DEVELOPMENT","created_utc":datetime.now(timezone.utc).isoformat(),
        "score_source":str(source),"score_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
        "analysis_source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_units":sorted({r["source_units"] for r in rows}),
        "candidate_index_pairs":index_pairs,"ordinary_index_pairs":ordinary_hash_pairs,
        "hard_path_repricing_thresholds":hard_pairs,"native_price_catalogue_comparisons":native_price_comparisons,
        "seed_summaries":summaries,
        "interpretation":"Retrospective exact analysis of completed exposed development records. Catalogue minima are not implementable oracles. No deployment work is priced here; report service remains optional and separate."}
    (out/"result.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    print(json.dumps({"rows":len(rows),"candidate_hash_pairs":len(index_pairs),"ordinary_hash_pairs":len(ordinary_hash_pairs),
                      "native_price_comparisons":len(native_price_comparisons),"seed_summary_groups":len(summaries)}))


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--scores",required=True)
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    run(args.scores,args.out)
