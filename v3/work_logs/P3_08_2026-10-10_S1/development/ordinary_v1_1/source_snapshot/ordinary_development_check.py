"""Focused handwritten-tape DEVELOPMENT checks; no full cohort comparison."""
from __future__ import annotations

import argparse
import ast
from dataclasses import replace
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "v3/experiments"))
import p308_cnf as S
import p308_ordinary as O
from p308_common import C


def dump(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def truth(query):
    return int(any(all(any((bits[abs(lit) - 1] == 1) == (lit > 0) for lit in clause)
                       for clause in query.clauses)
                   for bits in itertools.product((0, 1), repeat=query.variables)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise RuntimeError("Retain existing development output; use a versioned new directory.")
    args.out.mkdir(parents=True)
    sources = [REPO / "v3/experiments" / filename for filename in
               ("p308_ordinary.py", "p308_cnf.py", "p308_common.py", "p308_broker.py")]
    sources += [Path(__file__).resolve(), Path(__file__).with_name("ordinary_input_plan.json"),
                REPO / "v3/checks/07_selective_feedback.py"]
    hashes = {str(p.relative_to(REPO)): sha(p) for p in sources}
    dump(args.out / "started.json", {
        "stage": "DEVELOPMENT", "sources": hashes, "argv": sys.argv,
        "python": sys.version, "wall_start_ns": time.time_ns(),
        "principal_clock_credit_ns": 0,
        "selection": "Handwritten focused tapes and predeclared edge cases only; no full generated comparison."
    })
    full3 = [tuple((i + 1) * signs[i] for i in range(3))
             for signs in itertools.product((-1, 1), repeat=3)]
    tape = (
        S.make_query("q0", 3, [(1,), (-1,)]),
        S.make_query("q1", 3, [(1, 2), (-1, 3), (2, 3)]),
        S.make_query("q2", 3, full3),
        S.make_query("q3", 4, [(1,), (-2,), (3, 4)]),
        S.make_query("q4", 3, [(1,), (-1,)]),
        S.make_query("q5", 3, [(1, 2), (-1, 3), (2, 3)]),
        S.make_query("q6", 3, [(1,), (-1,)], source_version="cnf-input-v2"),
        S.make_query("q7", 3, [(1,)]),
    )
    full4 = [tuple((i + 1) * signs[i] for i in range(4))
             for signs in itertools.product((-1, 1), repeat=4)]
    censored = tuple(S.make_query(f"c{i}", 12, full4, source_version=f"cnf-source-{i}")
                     for i in range(4))
    repeated = tuple(S.make_query(f"r{i}", 3, [(1,)]) for i in range(8))
    dump(args.out / "public_focused_tapes.json", {
        "basic": [q.record() for q in tape],
        "censored": [q.record() for q in censored],
        "repeated": [q.record() for q in repeated]
    })
    checks = []
    private_truth = {q.query_id: truth(q) for q in tape + censored + repeated}
    dump(args.out / "private_reference_answers.json", private_truth)

    # The policy's cheap exact arithmetic is checked against ordinary rational
    # algebra, including ties, zero stakes and asymmetric high-width stakes.
    values = (F(0), F(1), F(1, 2), F(3, 7),
              F((1 << 63) - 1), F(1, (1 << 63) - 1))
    readout_rows = []
    for fp, fn, numerator in itertools.product(values, values, (0, 1, 12345, 32768, 65535, 65536)):
        meter = C.CostMeter()
        action, loss = O._greedy(numerator, 65536, fp, fn, meter)
        q = F(numerator, 65536)
        exact0, exact1 = fn * q, fp * (1 - q)
        assert action == int(exact1 < exact0)
        assert F(*loss) == min(exact0, exact1)
        readout_rows.append(meter.total)
    one_word_meter = C.CostMeter()
    O._greedy(32768, 65536, F(1), F(1), one_word_meter)
    assert one_word_meter.total == 30
    checks.append({"name": "specialized_integer_greedy_equals_fraction_cost",
                   "cases": len(readout_rows), "min_units": min(readout_rows),
                   "max_units": max(readout_rows), "one_word_units": one_word_meter.total})

    method_runs = {}
    for method in O.METHODS:
        result = O.run_method(tape, method, seed=3081001,
                              proof_cap=0 if method == "proof_only" else 2048,
                              error_price=1, unit_price=0)
        assert result["status"] == "success" and len(result["trace"]) == len(tape)
        assert result["expectation_theorem_eligible"] is False
        assert result["successful_quota_contract"] is False
        assert result["meter"]["total"] == sum(result["meter"]["by_category"].values())
        for row in result["trace"]:
            assert row["forecast_immutable"] and row["claim_key"] == tape[row["index"]].claim_key
            if row["hard_after"]["status"] == "checked":
                assert row["terminal_action"] == private_truth[row["query_id"]]
            if method == "proof_only":
                assert row["terminal_action"] == 0 and row["hard_after"]["status"] == "unresolved"
        if method in ("exact_dpll", "exact_cache", "ordinary_combo"):
            assert result["known_terminal_rounds"] == len(tape)
        method_runs[method] = result
    assert method_runs["exact_dpll"]["purchases"] == 8
    assert method_runs["exact_cache"]["purchases"] == 6
    assert method_runs["exact_cache"]["cache_hits"] == 2
    assert method_runs["probability_cost"]["purchases"] == 2
    assert method_runs["probability_cost"]["feedback_updates"] == 2
    dump(args.out / "tiny_method_runs.json", method_runs)
    checks.append({"name": "five_methods_with_distinct_service_and_cache_history",
                   "methods": list(method_runs),
                   "exact_cache_purchases": 6, "same_source_cache_hits": 2})

    # All base forecasts are reconstructed from each block's pre-feedback state.
    probability = O.run_method(tape, "probability_cost", seed=3081001,
                               false_positive_price=3, false_negative_price=1)
    for block in probability["blocks"]:
        weights = block["weights_before"]
        for row in probability["trace"][block["block"] * 4:(block["block"] + 1) * 4]:
            num, den = row["base_q"]
            assert num == (den * sum(w * a for w, a in zip(weights, row["advice"]))) // sum(weights)
            q = F(*row["emitted_q"])
            assert row["prospective_action"] == int(3 * (1 - q) < q)
    dump(args.out / "asymmetric_probability_run.json", probability)
    checks.append({"name": "frozen_block_forecasts_and_greedy_asymmetric_action", "rows": 8})

    failed = O.run_method(tape, "probability_cost", provider_limit=100)
    assert failed["status"] == "success" and failed["provider_failures"] == 2
    assert failed["successful_purchases"] == 0 and failed["feedback_updates"] == 0
    assert all(row["purchased_label"] is None for row in failed["trace"])
    assert all(inv["resources"]["total"] > 0 and inv["status"] == "budget_exhausted"
               for inv in failed["invoices"])
    interrupted = O.run_method(tape, "probability_cost", unit_limit=4000)
    assert interrupted["status"] == "failed"
    assert interrupted["meter"]["total"] <= 4000
    assert interrupted.get("rounds_issued", 0) == len(interrupted.get("issued_trace", []))
    for invalid in ("1e999999999", "-1", "1/0"):
        rejected = O.run_method(tape, "ordinary_combo", unit_price=invalid)
        assert rejected["status"] == "failed" and not rejected["trace"]
    dump(args.out / "budget_and_input_failure_runs.json", {
        "failed_children": failed, "global_interruption": interrupted
    })
    checks.append({"name": "failed_child_costs_no_labels_no_update_and_global_partial",
                   "failed_children": 2, "global_spent": interrupted["meter"]["total"]})

    completion = O.run_method(censored, "ordinary_combo", seed=3081001,
                              error_price=1, unit_price=0)
    assert completion["status"] == "success" and completion["known_terminal_rounds"] == 4
    failed_probes = [r for r in completion["invoices"]
                     if r["purpose"] == "optional_capped_probe" and r["status"] != "success"]
    assert failed_probes and all(r["resources"]["total"] > 0 for r in failed_probes)
    full_receipts = [r for r in completion["invoices"]
                     if r["purpose"] in ("optional_full", "selected_full") and r["status"] == "success"]
    assert sum(row["successful_full_total"] for row in completion["cost_history"]) == sum(
        row["resources"]["total"] for row in full_receipts)
    assert sum(row["successful_full_count"] for row in completion["cost_history"]) == len(full_receipts)
    assert completion["failed_full_calls_censored"] == 0
    dump(args.out / "censored_probe_then_full_run.json", completion)
    checks.append({"name": "paid_failed_prefix_not_treated_as_cheap_completed_profile",
                   "failed_probes": len(failed_probes), "successful_full_calls": len(full_receipts)})

    # Same easy repeated service is an intentionally adverse economic control.
    cache_run = O.run_method(repeated, "exact_cache", unit_price=1, error_price=0)
    combo_run = O.run_method(repeated, "ordinary_combo", unit_price=1, error_price=0)
    assert cache_run["status"] == combo_run["status"] == "success"
    assert all(r["terminal_action"] == 1 for r in cache_run["trace"] + combo_run["trace"])
    adverse_delta = combo_run["meter"]["total"] - cache_run["meter"]["total"]
    assert adverse_delta > 0
    dump(args.out / "adverse_repeated_tiny_control.json",
         {"exact_cache": cache_run, "ordinary_combo": combo_run,
          "combo_minus_cache_units": adverse_delta,
          "scope": "One declared tiny diagnostic, not a full-cohort comparison or global economic result."})
    checks.append({"name": "retained_adverse_equal_terminal_repeated_control",
                   "combo_minus_cache_units": adverse_delta})

    old_service = S.checked_purchase
    try:
        def misbound(query, *args, **kwargs):
            receipt = old_service(query, *args, **kwargs)
            return replace(receipt, query_id="wrong-request")
        S.checked_purchase = misbound
        misbound_run = O.run_method(tape, "exact_cache")
        assert misbound_run["status"] == "failed" and misbound_run["purchases"] == 1
        assert misbound_run["successful_purchases"] == 0
        assert misbound_run["invoices"][0]["resources"]["total"] > 0
        assert not misbound_run["trace"]
    finally:
        S.checked_purchase = old_service
    dump(args.out / "misbound_provider_failure.json", misbound_run)
    tree = ast.parse((REPO / "v3/experiments/p308_ordinary.py").read_text())
    private_calls = [node.attr for node in ast.walk(tree)
                     if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
                     and node.value.id == "S" and node.attr.startswith("_")]
    assert not private_calls
    checks.append({"name": "owned_provider_binding_and_no_private_solver_attribute",
                   "misbound_invoice_retained": True})

    final_hashes = {str(p.relative_to(REPO)): sha(p) for p in sources}
    assert final_hashes == hashes, "Source changed during these source-bound checks."
    result = {
        "stage": "DEVELOPMENT", "status": "PASS", "version": O.VERSION,
        "sources": hashes, "checks": checks, "wall_end_ns": time.time_ns(),
        "principal_clock_credit_ns": 0,
        "full_cohort_comparison_run": False,
        "economic_scope": "Tiny adverse diagnostic only; no superiority claim."
    }
    dump(args.out / "result.json", result)
    print(json.dumps({"status": "PASS", "checks": len(checks),
                      "greedy_one_word_units": 30,
                      "adverse_combo_minus_cache": adverse_delta}, sort_keys=True))


if __name__ == "__main__":
    main()
