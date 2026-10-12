#!/usr/bin/env python3
"""Conditional complete count-state audit quotations for the S29 family.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. This is a pure planning
component, not a complete admitted repair service. Its caller must supply
the independently checked product-source geometry and exact R-block cost.
Audit prices cover the declared observation tariff only. Planning, proof,
admission, checking and other resource costs remain additional.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import hashlib
import json
from pathlib import Path
import sys
import time

VERSION = 's07-quotient-count-planner-v1'


def encode(value):
    if isinstance(value, F):
        return value.numerator if value.denominator == 1 else str(value)
    raise TypeError(type(value).__name__)


def compile_plan(n, a, decision_gap, fixed_cost, price, tolerance,
                 mandatory_audit_price=1, decision_audit_price=1):
    if type(n) is not int or not 0 <= n <= 512:
        raise ValueError('This component supports zero to512 mandatory features')
    a, gap, fixed, price, tau, audit, decision = map(F, (
        a, decision_gap, fixed_cost, price, tolerance,
        mandatory_audit_price, decision_audit_price))
    if a <= 0 or fixed < 0 or price < 0 or not 0 <= tau < gap or audit <= 0 or decision <= 0:
        raise ValueError('Require positive source/tariffs, nonnegative costs, and tolerance below the decision gap')
    operations = dict(state_evaluation=0, branch_comparison=0, state_storage=0)
    records = {}

    @lru_cache(None)
    def value(k, h):
        tmin = n * a + a * h
        tmax = tmin + a * (n - k)
        operations['state_evaluation'] += 16
        if fixed + tmin >= price - tau:
            # Nonnegative future charges make a free terminal optimal.
            result = dict(kind='replace', cost=F(0), children=[])
        else:
            options = []
            if fixed + tmax <= price + tau:
                options.append(dict(kind='decision_audit_then_repair', cost=decision, children=[]))
            # If one decision audit is already cheapest possible and a
            # mandatory audit alone costs at least as much, no expansion
            # can improve this observation-tariff quote.
            if k < n and not (options and audit >= decision):
                children = [value(k + 1, h), value(k + 1, h + 1)]
                options.append(dict(kind='mandatory_audit', cost=audit + max(children),
                                    children=[[k + 1, h], [k + 1, h + 1]]))
            if not options:
                raise AssertionError('Finite complete audit menu lost its terminal')
            operations['branch_comparison'] += 3 * len(options)
            result = min(options, key=lambda item: (item['cost'], item['kind']))
        result.update(k=k, h=h, mandatory_min=tmin, mandatory_max=tmax)
        records[k, h] = result
        operations['state_storage'] += 12
        return result['cost']

    bound = value(0, 0)
    return dict(version=VERSION, parameters=dict(n=n, a=a, decision_gap=gap,
        fixed_cost=fixed, price=price, tolerance=tau,
        mandatory_audit_price=audit, decision_audit_price=decision),
        observation_tariff_bound=bound,
        states=[records[key] for key in sorted(records)],
        compiled_states=len(records), maximum_count_states=(n + 1) * (n + 2) // 2,
        full_latent_identification_tariff=n * audit + decision,
        planning_operations=operations, planning_named_units=sum(operations.values()),
        source_premise='Independent binary mandatory costs a/2a, one symmetric unknown decision bit with gap H, globally checked mandatory/equal-choice geometry, checked exact fixed R-block cost and feasible repair. These are premises, not established by this numerical planner.',
        cost_scope='Worst observation tariffs only; add actual proof/geometry acquisition, source admission, table compilation, execution/checking, host and storage costs.')


def literal_minimax(n, a, gap, fixed, price, tau, audit, decision):
    """Separate small full-information-state DP including early bit audits."""
    calls = 0

    @lru_cache(None)
    def visit(known, bit):
        nonlocal calls
        calls += 1
        unknown = [i for i, v in enumerate(known) if v < 0]
        totals = [fixed + sum(a * (1 + (v if v >= 0 else fill[unknown.index(i)]))
                              for i, v in enumerate(known))
                  for fill in product((0, 1), repeat=len(unknown))]
        bits = (0, 1) if bit < 0 else (bit,)
        actions = ['replace', 0, 1]
        def regret(action):
            return max((price if action == 'replace' else t + (0 if action == b else gap))
                       - min(price, t) for t in totals for b in bits)
        if any(regret(action) <= tau for action in actions):
            return F(0)
        options = []
        for i in unknown:
            children = []
            for outcome in (0, 1):
                updated = list(known); updated[i] = outcome
                children.append(visit(tuple(updated), bit))
            options.append(audit + max(children))
        if bit < 0:
            options.append(decision + max(visit(known, 0), visit(known, 1)))
        if not options:
            raise AssertionError('Fully observed source must have an optimal fixed action')
        return min(options)

    answer = visit(tuple([-1] * n), -1)
    return answer, calls


def run(output):
    if output.exists():
        raise FileExistsError('Preserve conditional planning evidence')
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    checks = []
    for n in range(5):
        for tau in (F(0), F(1, 2), F(1)):
            for audit, decision in ((F(1), F(1)), (F(1), F(4)), (F(3), F(1))):
                for price in (F(2 + 2*n), F(2 + 3*n, 1) + F(1, 2), F(3 + 4*n)):
                    args = (n, F(2), F(8), F(2), price, tau, audit, decision)
                    plan = compile_plan(*args)
                    exact, states = literal_minimax(*args)
                    if plan['observation_tariff_bound'] != exact:
                        raise AssertionError('Count-state quotation disagrees with literal minimax audit tree')
                    checks.append(dict(parameters=plan['parameters'], count_states=plan['compiled_states'],
                                       literal_states=states, exact_tariff=exact))
    examples = [compile_plan(n, 2, 8, 2, price, 1, 1, 1)
                for n in (8, 32, 128)
                for price in (2 + 2*n, 2 + 3*n, 3 + 4*n)]
    result = dict(status='passed', evidence='DEVELOPMENT conditional complete planning component',
        contributor='ChatGPT (GPT-6 Astra Pro)', created_utc=datetime.now(timezone.utc).isoformat(),
        implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        small_independent_comparisons=checks, examples=examples, actual_new_acquisitions=0,
        timing=dict(process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-wall))
    output.write_text(json.dumps(result, indent=2, default=encode) + '\n')
    print(json.dumps(dict(status='passed', comparisons=len(checks), actual_new_acquisitions=0,
        examples=[dict(n=e['parameters']['n'], price=e['parameters']['price'],
            tariff=e['observation_tariff_bound'], states=e['compiled_states'],
            full_identification_tariff=e['full_latent_identification_tariff'],
            planning_named_units=e['planning_named_units']) for e in examples]), default=encode))


if __name__ == '__main__':
    run(Path(sys.argv[1]))
