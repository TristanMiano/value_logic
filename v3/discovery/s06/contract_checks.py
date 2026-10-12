#!/usr/bin/env python3
"""Small constructive arithmetic checks for contract_quote.py, no native calls.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. The small example was
specified before execution and is an illustration, not held-out validation.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
from fractions import Fraction
import json
from pathlib import Path
import sys
import time

import contract_quote as cq
from joint_repair import CostState, certificate


def jsonable(value):
    if isinstance(value, Fraction):
        return dict(numerator=value.numerator, denominator=value.denominator)
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(v) for v in value]
    return value


def run(output):
    if output.exists():
        raise FileExistsError("Preserve executed constructive evidence")
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    source = cq.source
    # Declared independent illustration: x1 OR x2; soft penalties for x1,x2.
    # Only the both-true witness is initially retained. Cost 2 is always 3;
    # cost 1 belongs to {3,4}. No distribution over these values is supplied.
    tiny = dict(row="contract_example", variables=2, hard=[[1, 2]],
                soft=[dict(weight=3, clause=[-1]), dict(weight=3, clause=[-2])],
                public_incumbent=3, objective_max=6)
    tiny["identity"] = source.digest(tiny)
    cost_contract = dict(possible_cost_modes=[[3,3],[4,3]], cohort_size=1,
                         target="The single fixed row; unknown realized mode, no outcome law.")
    cost_source_id = source.digest(cost_contract)
    meter = source.Meter()
    costs = CostState(cost_contract["possible_cost_modes"], 1, cost_source_id, meter)
    # The setup lower proof is an actual paid call and checked receipt.
    initial_negative = cq.execute_complete(tiny, 2)
    assert initial_negative["provider_response"]["status"] == "UNSAT"
    initial_witness = cq.compilation.compile_witness(tiny, 3, meter)
    profile = dict(witnesses=[initial_witness], trees=[dict(
        leaf_masks=initial_negative["leaf_masks"], receipt_id=initial_negative["receipt_id"]
    )])
    before = certificate(profile, costs, 8)
    margins = cq.transfer_margins(costs, [3,3])
    quote = cq.two_outcome_quote(upper=7, lower=3, price=8, tolerance=2,
                                alpha=margins["alpha"], delta=margins["delta"], budget=4)
    assert (before["bound"], margins["alpha"], margins["delta"]) == (4, 1, 0)
    assert (quote["integer_budget_low"], quote["integer_budget_high"]) == (4, 4)
    assert quote["complete_worst_bound"] == 2
    # Complete public audit menu: evaluating hypothetical possibilities is
    # billed software; these are not observations of a hidden source.
    audit_outcomes = []
    for value in [3,4]:
        prospective = CostState(cost_contract["possible_cost_modes"], 1, cost_source_id, meter)
        prospective.possible[0] = tuple(k for k,v in enumerate(prospective.modes) if v[0] == value)
        meter.pay("audit_quote", "prospective_mode_filter", len(prospective.modes))
        audit_outcomes.append(dict(value=value, bound=certificate(profile,prospective,8)["bound"]))
    audit_worst = max(r["bound"] for r in audit_outcomes)
    assert audit_worst == 4
    bought = cq.execute_complete(tiny, 4)
    assert bought["provider_response"]["status"] == "SAT"
    profile["witnesses"].append(bought["witness"])
    after = certificate(profile, costs, 8)
    assert after["bound"] == 0
    # Check margins over every objective mask and every public extreme mode.
    # This is not a logical-optimum calculation and does not guide a purchase.
    margin_checks = 0
    for mode in cost_contract["possible_cost_modes"]:
        for mask in range(4):
            z = [(mask >> j)&1 for j in range(2)]
            real = sum(a*b for a,b in zip(mode,z))
            nominal = sum(3*a for a in z)
            assert real-nominal <= margins["alpha"]
            assert nominal-real <= margins["delta"]
            margin_checks += 1
            meter.pay("constructive_check", "objective_transfer_case", 8)
    # Dependency-preserving W can improve both margins relative to its box.
    anticorrelated = CostState([[0,2],[2,0]], 1, "analytical-anticorrelation", meter)
    joint_margin = cq.transfer_margins(anticorrelated,[1,1])
    box = CostState([[0,2],[2,0]], 1, "analytical-anticorrelation", meter,"box")
    box_margin = cq.transfer_margins(box,[1,1])
    assert (joint_margin["alpha"],joint_margin["delta"]) == (1,1)
    assert (box_margin["alpha"],box_margin["delta"]) == (2,2)
    # Symbolic price-region arithmetic; CPU values here are explicit invented
    # quotation examples, not measured or inferred native timing forecasts.
    threshold = cq.audit_price_threshold(3,2,10,30,1,2,1,5)
    assert threshold == 45
    # Bind and price the public s05 sources, without opening hidden cost modes
    # or searching the original source models again.
    archive_path = cq.HERE.parent/"s05"/"maxsat_repair_results.json"
    archive = json.loads(archive_path.read_text())
    public_quotes = [cq.finite_call_quote(v) for v in archive["instances"]]
    assert max(q["provider_units"] for q in public_quotes) == 66941
    assert max(q["negative_check_units"] for q in public_quotes) == 16863
    assert max(q["tree_compile_units"] for q in public_quotes) == 5367
    assert all(q["provider_units"] <= 1_000_000 for q in public_quotes)
    result = dict(
        version="s06-complete-acquisition-contract-v1", evidence="DEVELOPMENT",
        contributor="ChatGPT (GPT-6 Astra Pro)", created_utc=datetime.now(timezone.utc).isoformat(),
        implementation_sha256=cq.sha(cq.__file__), checks_sha256=cq.sha(__file__),
        source_archive_sha256=cq.sha(archive_path), new_native_calls=0,
        new_complete_branch_calls=2, new_external_cost_observations=0,
        tiny_source=tiny, tiny_cost_contract=cost_contract,
        tiny=dict(before=before, transfer_margins=margins, complete_quote=quote,
                  proposed_audit_outcomes=audit_outcomes, audit_worst_bound=audit_worst,
                  audit_guaranteed_reduction=before["bound"]-audit_worst,
                  logical_guaranteed_reduction=quote["guaranteed_scalar_reduction"],
                  initial_paid_lower_receipt=initial_negative, paid_query=bought,
                  after=after, checked_objective_transfer_cases=margin_checks),
        common_source_margin_example=dict(joint=joint_margin,box=box_margin),
        illustrative_price_threshold=threshold,
        price_scope="Invented prospective tariff example only; no native runtime-law or economic claim.",
        public_source_complete_quotes=public_quotes,
        declared_checks_operations=meter.record(),
        measured_total_timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall),
        result="PASS at the finite arithmetic and source-bound callable illustration scope",
        limitations="No guaranteed CPU/wall bound, no native completion guarantee, no hidden-source fixture optimization, no held-out validation.",
    )
    output.write_text(json.dumps(jsonable(result),indent=2)+"\n")
    print(json.dumps(dict(result=result["result"], new_complete_branch_calls=2,
        quoted_provider_max=max(q["provider_units"] for q in public_quotes),
        quoted_complete_wrapper_max=max(q["complete_wrapper_units"] for q in public_quotes),
        actual_tiny_call_units=[initial_negative["total_operation_units"],bought["total_operation_units"]],
        tiny_initial_bound=before["bound"],tiny_final_bound=after["bound"])))


if __name__ == "__main__":
    run(Path(sys.argv[1]))
