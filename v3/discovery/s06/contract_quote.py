#!/usr/bin/env python3
"""Finite complete-call tariff and two-outcome regret quotations.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12.
These are declared-operation ceilings for the bound source implementation,
not CPU, wall-clock, machine-survival or scalable-solver guarantees.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s05"))
import maxsat_repair as source
import maxsat_reprice as compilation


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def finite_call_quote(instance):
    """Bound the actual provider/checker/compilation Meter operations.

    The procedure branches once per previously unassigned variable, so its
    execution/proof tree has <= 2**(n+1)-1 nodes and <= 2**n leaves. Every
    clause/weight inspection is bounded by the admitted source lengths.
    """
    n, hard, soft = instance["variables"], instance["hard"], instance["soft"]
    if type(n) is not int or n < 1:
        raise ValueError("Positive finite variable universe required")
    for clause in hard + [s["clause"] for s in soft]:
        if any(type(v) is not int or not 1 <= abs(v) <= n for v in clause):
            raise ValueError("Malformed source clause")
    if any(type(s["weight"]) is not int or s["weight"] < 0 for s in soft):
        raise ValueError("Nonnegative integral query weights required")
    m, leaves = len(soft), 1 << n
    nodes = 2 * leaves - 1
    h = sum(1 + len(c) for c in hard)
    s = sum(2 + len(v["clause"]) for v in soft)
    provider_per_node = 2 + h + s + max(2, 1 + m, n)
    negative_per_node = 1 + max(
        [0] + [1 + len(c) for c in hard]
        + [sum(3 + len(v["clause"]) for v in soft)]
    )
    witness_check = h + 1 + s
    witness_compile = (
        h + 1 + sum(1 + len(v["clause"]) for v in soft)
        + 2 * m + n + 2
    )
    negative_check = nodes * negative_per_node
    tree_compile = nodes * (m + 2) + leaves + 1
    raw_proof_words = 2 * (leaves - 1) + leaves * max(2, m + 1)
    # New source admission and objective update are explicit wrapper tariffs.
    admission = 8 + h + sum(2 + len(v["clause"]) for v in soft)
    objective_update = 2 * m + 2
    wrapper_response = 16
    witness_retention = n + 8
    proof_retention = 8 + raw_proof_words
    positive_processing = witness_check + witness_compile + witness_retention
    negative_processing = negative_check + tree_compile + proof_retention
    return dict(
        source_id=source.digest(instance), variables=n, soft_clauses=m,
        maximum_tree_nodes=nodes, maximum_tree_leaves=leaves,
        provider_per_node=provider_per_node,
        provider_units=nodes * provider_per_node,
        negative_check_units=negative_check,
        witness_check_units=witness_check,
        tree_compile_units=tree_compile,
        witness_compile_units=witness_compile,
        raw_proof_words=raw_proof_words,
        admission_units=admission, objective_update_units=objective_update,
        response_units=wrapper_response,
        witness_retention_units=witness_retention,
        proof_retention_units=proof_retention,
        complete_wrapper_units=(
            admission + witness_check + objective_update + nodes * provider_per_node
            + max(positive_processing, negative_processing) + wrapper_response
        ),
        provider_sha256=sha(source.__file__),
        compilation_sha256=sha(compilation.__file__),
        meter_contract="Named operation tariff only; all Python execution is also measured as CPU/wall time.",
        cpu_max_seconds=None, wall_max_seconds=None,
    )


def execute_complete(instance, budget):
    """Execute one separately paid finite branching query and check its result.

    This does not call native IHS/MaxSAT. A process/host interruption still
    prevents completion; the quote only rules out the code's Meter cap on a
    normal terminating execution with these bound bytes and admitted inputs.
    """
    if type(budget) is not int:
        raise ValueError("Integral query budget required")
    wall, cpu = time.perf_counter_ns(), time.process_time_ns()
    quote = finite_call_quote(instance)
    meter = source.Meter()
    meter.pay("contract_admission", "source_words", quote["admission_units"])
    source.checked_objective(instance, instance["public_incumbent"], meter)
    meter.pay("objective_update", "query_weight_words", quote["objective_update_units"])
    response = source.budget_provider(instance, budget, quote["provider_units"])
    if response["status"] == "UNRESOLVED":
        raise AssertionError("Proved provider-operation ceiling was insufficient")
    receipt = dict(source_id=quote["source_id"], budget=budget,
                   provider_response=response, quote=quote)
    if response["status"] == "SAT":
        value = source.checked_objective(instance, response["model"], meter)
        if value > budget:
            raise ValueError("Witness does not answer the requested bound")
        receipt["witness"] = compilation.compile_witness(instance, response["model"], meter)
        meter.pay("storage", "complete_witness", quote["witness_retention_units"])
    else:
        source.check_negative(instance, budget, response["proof"], meter)
        receipt["leaf_masks"] = compilation.compile_tree(response["proof"], meter)
        receipt["checked_lower"] = budget + 1
        meter.pay("storage", "complete_negative", 8 + source.proof_words(response["proof"]))
    meter.pay("output", "complete_query_response", quote["response_units"])
    total = meter.total + response["invoice"]["total"]
    if total > quote["complete_wrapper_units"]:
        raise AssertionError("Complete declared-operation quote was exceeded")
    receipt.update(wrapper_invoice=meter.record(), total_operation_units=total,
                   timing=dict(process_ns=time.process_time_ns()-cpu,
                               wall_ns=time.perf_counter_ns()-wall))
    receipt["receipt_id"] = source.digest(receipt)
    return receipt


def transfer_margins(costs, q):
    """Exact all-Boolean objective transfer using common source supports.

    This enumerates 2**m objective masks, not feasible logical models or
    unobserved cohort outcomes. Every support query uses the caller's meter.
    """
    if len(q) != costs.m or any(type(x) is not int or x < 0 for x in q):
        raise ValueError("Nonnegative integral query vector required")
    alpha = delta = 0
    alpha_mask = delta_mask = 0
    for mask in range(1 << costs.m):
        z = tuple((mask >> j) & 1 for j in range(costs.m))
        qz = sum(a*b for a, b in zip(q, z))
        hi, _ = costs.support(z)
        negative_lo, _ = costs.support(tuple(-a for a in z))
        a, d = hi-qz, qz+negative_lo
        if a > alpha:
            alpha, alpha_mask = a, mask
        if d > delta:
            delta, delta_mask = d, mask
        costs.meter.pay("contract_quote", "mask_objective_and_transfer_comparison", 2*costs.m+4)
    return dict(alpha=alpha, delta=delta, alpha_mask=alpha_mask, delta_mask=delta_mask,
                objective_masks=1 << costs.m)


def two_outcome_quote(upper, lower, price, tolerance, alpha, delta, budget=None):
    """Sufficient complete-call interval and safe per-outcome regret bounds."""
    upper, lower, price, tolerance, alpha, delta = map(
        Fraction, (upper, lower, price, tolerance, alpha, delta)
    )
    if not 0 <= lower <= upper or min(price, tolerance, alpha, delta) < 0:
        raise ValueError("Invalid admitted scalar envelope or margins")
    u, ell = min(upper, price), min(lower, price)
    # ceil(U + delta - tau - 1), floor(ell + tau - alpha).
    low_value, high_value = u+delta-tolerance-1, ell+tolerance-alpha
    low = -((-low_value.numerator)//low_value.denominator)
    high = high_value.numerator//high_value.denominator
    result = dict(integer_budget_low=low, integer_budget_high=high,
                  nonempty_budget_interval=low <= high,
                  current_scalar_bound=max(Fraction(0), u-ell))
    if budget is not None:
        if type(budget) is not int:
            raise ValueError("Integral budget required")
        sat = max(Fraction(0), min(u, Fraction(budget)+alpha)-ell)
        unsat = max(Fraction(0), u-min(price, max(lower, Fraction(budget+1)-delta)))
        result.update(budget=budget, sat_bound=sat, checked_unsat_bound=unsat,
                      complete_worst_bound=max(sat, unsat),
                      guaranteed_scalar_reduction=max(Fraction(0), u-ell-max(sat,unsat)),
                      cap_timeout_worst_bound=max(Fraction(0),u-ell))
    return result


def audit_price_threshold(audit_gain, logic_gain, audit_software, logic_software,
                          audit_cpu, logic_cpu, software_price, cpu_price):
    """Largest audit price with >= local guaranteed reduction per price.

    CPU arguments must be valid prospective cost quotations for a guaranteed
    decision, or explicitly retrospective measurements for a realized region.
    """
    ga, gl, ka, kl, ta, tl, sigma, rho = map(Fraction, (
        audit_gain, logic_gain, audit_software, logic_software,
        audit_cpu, logic_cpu, software_price, cpu_price,
    ))
    if gl <= 0 or min(ga, ka, kl, ta, tl, sigma, rho) < 0:
        raise ValueError("Positive logical gain and nonnegative resources required")
    return ga*(sigma*kl+rho*tl)/gl - sigma*ka-rho*ta
