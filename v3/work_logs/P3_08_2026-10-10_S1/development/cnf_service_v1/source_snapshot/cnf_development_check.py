"""Focused source-bound DEVELOPMENT checks for the new P3-08 CNF service."""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "v3/experiments"))
import p308_cnf as N
from p308_common import C


def dump(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference(query):
    # A separate finite Boolean definition, never a controller input.
    return int(any(
        all(any((values[abs(lit) - 1] == 1) == (lit > 0) for lit in clause)
            for clause in query.clauses)
        for values in itertools.product((0, 1), repeat=query.variables)
    ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise RuntimeError("Preserve existing output; choose a prospectively versioned new run.")
    args.out.mkdir(parents=True)
    paths = [REPO / "v3/experiments/p308_cnf.py",
             REPO / "v3/experiments/p308_common.py",
             REPO / "v3/checks/07_selective_feedback.py",
             REPO / "v3/checks/07_selective_feedback_service.py",
             REPO / "v3/checks/07_computation_adapter.py",
             Path(__file__).resolve(),
             Path(__file__).with_name("cnf_input_plan.json")]
    initial = {str(p.relative_to(REPO)): sha(p) for p in paths}
    dump(args.out / "started.json", {
        "stage": "DEVELOPMENT", "schema": "value_logic.p308.cnf.checks.v1",
        "sources": initial, "python": sys.version, "argv": sys.argv,
        "overlapping_agent_principal_credit_ns": 0,
        "wall_start_ns": time.time_ns()
    })

    # Persist every public generated formula before either solver or reference.
    cohort = N.make_development_queries()
    dump(args.out / "public_cohort.json", [q.record() for q in cohort])
    checks = []
    catalogue = [()] + [(x,) for x in (-2, -1, 1, 2)]
    catalogue += [tuple(sorted((a, b))) for a in (-1, 1) for b in (-2, 2)]
    counts = {"exhaustive_formulas": 0, "service_calls": 0, "max_total": 0,
              "false_answers": 0, "true_answers": 0}
    for index in range(1 << len(catalogue)):
        query = N.make_query(f"exhaustive-two-{index}", 2,
                             [c for j, c in enumerate(catalogue) if index & (1 << j)])
        expected = reference(query)
        counts["exhaustive_formulas"] += 1
        for solver in ("enumeration", "dpll"):
            receipt = N.checked_purchase(query, N.service_cap(query, solver), solver)
            assert receipt.successful and receipt.checked and receipt.answer == expected
            assert receipt.claim_key == query.claim_key and receipt.query_id == query.query_id
            assert receipt.resources.total <= N.service_cap(query, solver)
            counts["service_calls"] += 1
            counts["max_total"] = max(counts["max_total"], receipt.resources.total)
            counts["true_answers" if expected else "false_answers"] += 1
    checks.append({"name": "all_subsets_two_variable_clause_catalogue", **counts})

    boundary = [
        N.make_query("empty-formula", 1, []),
        N.make_query("empty-clause", 1, [()]),
        N.make_query("duplicates", 2, [(1, 1), (-1, 2), (-1, 2)]),
        N.make_query("tautology", 2, [(1, -1), (2, -2)]),
        N.make_query("opposing-units", 12, [(1,), (-1,)]),
        N.make_query("disconnected", 6, [(1, 2), (-1, 2), (3, -4), (-3, -4), (5, 6)]),
        N.make_query("maximum-shape", 12, [(1, -2, 3, -4)] * 64),
    ]
    for query in boundary:
        expected = reference(query)
        for solver in ("enumeration", "dpll"):
            receipt = N.checked_purchase(query, N.service_cap(query, solver), solver)
            assert receipt.successful and receipt.answer == expected
    checks.append({"name": "boundary_duplicates_tautologies_empty_and_max_shape",
                   "queries": [q.query_id for q in boundary],
                   "max_admitted_cap": N.service_cap(boundary[-1], "dpll")})

    rejected_shapes = [
        lambda: N.Query("bad-bool", True, ()),
        lambda: N.Query("bad-zero", 0, ()),
        lambda: N.Query("bad-over", 13, ()),
        lambda: N.Query("bad-width", 4, ((1, 2, 3, 4, 4),)),
        lambda: N.Query("bad-count", 1, ((1,),) * 65),
        lambda: N.Query("bad-zero-literal", 1, ((0,),)),
        lambda: N.Query("bad-bool-literal", 1, ((True,),)),
        lambda: N.Query("bad-literal", 2, ((3,),)),
        lambda: N.Query("bad-mutable", 1, [(1,)]),
        lambda: N.Query("bad-order", 2, ((2, 1),)),
        lambda: N.Query("bad-version", 1, (), semantics_version="other"),
    ]
    for call in rejected_shapes:
        try:
            call()
        except N.Rejected:
            pass
        else:
            raise AssertionError("Malformed query admitted.")
    checks.append({"name": "exact_immutable_admission", "rejections": len(rejected_shapes)})

    # No direct contradictory units: false checking exercises full enumeration.
    hard_false = N.make_query("full-cube-unsat", 3, [
        tuple((j + 1) * signs[j] for j in range(3))
        for signs in itertools.product((-1, 1), repeat=3)])
    full = N.checked_purchase(hard_false)
    assert full.answer == 0 and "all assignments" in full.detail
    finish = sum(units for category, operation, units in full.resources.operations
                 if category == "admission" or operation in (
                     "cnf_final_response_prepaid", "cnf_final_cleanup_prepaid"))
    budgets = sorted(set([0, 1, finish - 1, finish, finish + 1,
                          full.resources.total // 2, full.resources.total - 1,
                          full.resources.total, full.resources.total + 1]))
    budget_rows = []
    for budget in budgets:
        receipt = N.checked_purchase(hard_false, budget)
        assert receipt.resources.total <= budget
        if budget < full.resources.total:
            assert receipt.status == "budget_exhausted"
            assert receipt.answer is None and not receipt.checked
        else:
            assert receipt.answer == 0 and receipt.checked
        budget_rows.append({"budget": budget, **receipt.record()})
    dump(args.out / "budget_failure_receipts.json", budget_rows)
    checks.append({"name": "prepaid_output_production_checker_and_release_denials",
                   "full_cost": full.resources.total, "budgets": budgets})

    # Corrupt producer outputs; the trusted checker must suppress release.
    original_dpll = N._dpll
    corrupt_rows = []
    true_query = N.make_query("corrupt-false-on-sat", 2, [(1, 2)])
    try:
        for candidate in ((0, None), (1, 0), (0.0, None)):
            N._dpll = lambda q, m, result=candidate: result
            receipt = N.checked_purchase(true_query)
            assert receipt.status == "rejected" and receipt.answer is None
            assert not receipt.checked and receipt.resources.total > 0
            corrupt_rows.append(receipt.record())
    finally:
        N._dpll = original_dpll
    dump(args.out / "rejected_producer_receipts.json", corrupt_rows)
    checks.append({"name": "corrupted_producer_is_not_hard_evidence",
                   "rejections": len(corrupt_rows)})

    cache = N.ExactCache(capacity=1)
    meter = C.CostMeter()
    q1 = N.make_query("cache-1", 2, [(1, 2)])
    q2 = replace(q1, query_id="cache-reissued")
    r1 = N.checked_purchase(q1)
    assert cache.lookup(q1, meter) is None
    assert cache.remember(q1, r1, meter)
    hit = cache.lookup(q2, meter)
    assert hit is not None and hit.query_id == q2.query_id and hit.answer == r1.answer
    assert cache.lookup(replace(q2, source_version="cnf-input-v2"), meter) is None
    assert cache.lookup(N.make_query(q2.query_id, 2, [(1,), (-1,)]), meter) is None
    before_entries = cache.entries
    for forged in (replace(r1, query_id="unrelated"),
                   replace(r1, provider="not-this-provider"),
                   replace(r1, answer=True),
                   replace(r1, claim_key=("changed",))):
        try:
            cache.remember(q1, forged, meter)
        except N.Rejected:
            pass
        else:
            raise AssertionError("Malformed/misbound receipt entered cache.")
        assert cache.entries == before_entries
    assert cache.remember(hard_false, full, meter)
    assert cache.lookup(q1, meter) is None and cache.entries == 1
    dump(args.out / "cache_invoice.json", meter.snapshot())
    checks.append({"name": "cache_content_version_request_rebinding_and_fifo",
                   "entries": cache.entries, "retained_words": cache.retained_words,
                   "invoice_total": meter.total})

    original_functions = {name: getattr(N, name) for name in
                          ("_dpll", "_enumeration", "_verify_unsat", "_verify_witness")}
    def truth_forbidden(*args, **kwargs):
        raise AssertionError("Public advice tried to execute truth.")
    try:
        for name in original_functions:
            setattr(N, name, truth_forbidden)
        for query in cohort:
            feature_meter = C.CostMeter(N.EXPERT_CAP)
            predictions = N.expert_predictions(query, feature_meter)
            assert len(predictions) == len(N.EXPERT_NAMES) and predictions[:2] == (0, 1)
            assert all(type(v) is int and v in (0, 1) for v in predictions)
            assert feature_meter.total <= N.EXPERT_CAP
            proxy_meter = C.CostMeter(N.EXPERT_CAP)
            assert N.cost_proxy(query, proxy_meter) >= 1
    finally:
        for name, function in original_functions.items():
            setattr(N, name, function)
    checks.append({"name": "stateless_features_and_public_cost_proxy",
                   "queries": len(cohort), "expert_names": N.EXPERT_NAMES})

    comparison = []
    for query in cohort:
        expected = reference(query)
        results = {}
        for solver in ("enumeration", "dpll"):
            receipt = N.checked_purchase(query, N.service_cap(query, solver), solver)
            assert receipt.successful and receipt.answer == expected
            results[solver] = receipt.record()
        comparison.append({"query": query.record(), "private_reference_answer": expected,
                           "solvers": results})
    dump(args.out / "development_solver_comparison.json", comparison)
    summary = {
        "queries": len(cohort), "positive": sum(row["private_reference_answer"] for row in comparison),
        "negative": sum(1 - row["private_reference_answer"] for row in comparison),
        "enumeration_units": sum(row["solvers"]["enumeration"]["resources"]["total"] for row in comparison),
        "dpll_units": sum(row["solvers"]["dpll"]["resources"]["total"] for row in comparison),
    }
    checks.append({"name": "unbalanced_public_development_cohort_retained", **summary})

    final_hashes = {str(p.relative_to(REPO)): sha(p) for p in paths}
    assert final_hashes == initial, "Source changed during the bounded check run."
    result = {"stage": "DEVELOPMENT", "status": "PASS",
              "scope": "Enumerated two-variable clause catalogue plus declared finite development/boundary cases; not a general correctness proof.",
              "sources": initial, "checks": checks,
              "service_comparison": summary, "wall_end_ns": time.time_ns(),
              "principal_clock_credit_ns": 0}
    dump(args.out / "result.json", result)
    print(json.dumps({"status": "PASS", "checks": len(checks), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
