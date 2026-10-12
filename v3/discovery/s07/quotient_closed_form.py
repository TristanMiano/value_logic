#!/usr/bin/env python3
"""Exact constant-arithmetic quote for the S29 homogeneous audit family.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. Same conditional source,
pure-action, paid-geometry and tariff premises as quotient_plan.py.
This does not establish those premises or purchase observations.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import time
import quotient_plan as dp

VERSION = 's07-quotient-closed-form-v1'


def ceil(q):
    return -((-q.numerator) // q.denominator)


def floor(q):
    return q.numerator // q.denominator


def quote(n, a, decision_gap, fixed_cost, price, tolerance,
          mandatory_audit_price=1, decision_audit_price=1):
    if type(n) is not int or n < 0:
        raise ValueError('Nonnegative integral number of mandatory features required')
    a, gap, fixed, price, tau, audit, decision = map(F, (
        a, decision_gap, fixed_cost, price, tolerance,
        mandatory_audit_price, decision_audit_price))
    if a <= 0 or fixed < 0 or price < 0 or not 0 <= tau < gap or audit <= 0 or decision <= 0:
        raise ValueError('Same positive-tariff, fixed-action source premises as the count DP required')
    low, high = fixed + n*a, fixed + 2*n*a
    if low >= price-tau:
        kind, cost, steps, highs, lows = 'replace', F(0), 0, None, None
    elif high <= price+tau:
        kind, cost, steps, highs, lows = 'decision_audit_then_repair', decision, 0, None, None
    else:
        highs = ceil((price-tau-fixed-n*a)/a)
        lows = n-floor((price+tau-fixed-n*a)/a)
        if not highs > 0 or not lows > 0 or not highs+lows-1 <= n:
            raise AssertionError('Positive complete stopping thresholds must fit the source')
        steps = highs+lows-1
        kind, cost = 'audit_until_high_or_low_threshold', steps*audit+decision
    return dict(version=VERSION, parameters=dict(n=n, a=a, decision_gap=gap,
        fixed_cost=fixed, price=price, tolerance=tau,
        mandatory_audit_price=audit, decision_audit_price=decision),
        kind=kind, observation_tariff_bound=cost, maximum_mandatory_audits=steps,
        replacement_high_threshold=highs, repair_low_threshold=lows,
        compiled_count_states=0, scalar_plan_records=1,
        source_premise='Exactly the homogeneous independent mandatory/decision source and checked fixed-cost/proof premises of quotient_plan; quote() does not admit them.',
        cost_scope='Observation tariff only. Constant many exact rational arithmetic operations, not constant bit cost; source/proof admission, compiler/checker execution and all remaining actual costs are additional.')


def run(output):
    if output.exists():
        raise FileExistsError('Preserve closed-form development evidence')
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    previous_path = Path(dp.__file__).with_name('quotient_plan_results.json')
    previous = json.loads(previous_path.read_text())
    if previous['implementation_sha256'] != hashlib.sha256(Path(dp.__file__).read_bytes()).hexdigest():
        raise ValueError('The original DP snapshot changed')
    cases = []
    for old in previous['small_independent_comparisons']:
        p = old['parameters']
        got = quote(**p)
        if got['observation_tariff_bound'] != F(old['exact_tariff']):
            raise AssertionError('Closed-form quote differs from independent literal audit-tree optimum')
        cases.append(dict(parameters=p, exact_tariff=got['observation_tariff_bound'],
                          literal_states=old['literal_states'], old_count_states=old['count_states'],
                          closed_form=got))
    examples = []
    for old in previous['examples']:
        got = quote(**old['parameters'])
        if got['observation_tariff_bound'] != F(old['observation_tariff_bound']):
            raise AssertionError('Closed-form quote differs from saved larger count DP')
        examples.append(dict(closed_form=got, previous_count_states=old['compiled_states'],
                              previous_planning_named_units=old['planning_named_units']))
    huge = quote(10**12, 2, 8, 2, 3*10**12+2, 1, 1, 1)
    if huge['observation_tariff_bound'] != 10**12:
        raise AssertionError('Symbolic scale family arithmetic mismatch')
    result = dict(status='passed', evidence='DEVELOPMENT conditional closed-form complete tariff quote',
        contributor='ChatGPT (GPT-6 Astra Pro)', created_utc=datetime.now(timezone.utc).isoformat(),
        implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        original_dp_sha256=previous['implementation_sha256'],
        original_dp_result_sha256=hashlib.sha256(previous_path.read_bytes()).hexdigest(),
        prior_literal_minimax_comparisons=cases, larger_dp_comparisons=examples,
        huge_arithmetic_example=huge, actual_new_acquisitions=0,
        timing=dict(process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-wall))
    output.write_text(json.dumps(result, indent=2, default=dp.encode)+'\n')
    print(json.dumps(dict(status='passed', independent_literal_comparisons=len(cases),
        larger_dp_comparisons=len(examples), actual_new_acquisitions=0,
        largest_saved_middle_case=dict(n=128, previous_states=4224, new_scalar_plan_records=1,
                                      same_worst_audit_tariff=128),
        huge_arithmetic_example_tariff=huge['observation_tariff_bound']), default=dp.encode))


if __name__ == '__main__':
    run(Path(sys.argv[1]))
