#!/usr/bin/env python3
"""Objective-lattice strengthening of the checked source-ambiguity floor.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. Reuses the same admitted
pair scenarios and retained raw-proof projection as ambiguity_floor v1.
No new logical or source acquisitions; no logical model enumeration.
"""
from fractions import Fraction as F
from functools import reduce
from math import gcd
import ambiguity_floor as base

VERSION = 's07-discrete-source-ambiguity-floor-v1'


def source_floor(row, bank, costs, price, *, cap=6):
    meter = costs.meter
    start = meter.total
    simple = base.source_floor(row, bank, costs, price, cap=cap)
    price = F(price)
    scale = price.denominator
    scenarios = simple['scenarios']
    if any(type(w) is not int for scenario in scenarios for w in scenario['weights']):
        raise ValueError('Discrete obstruction requires nonnegative integer scenario objectives')
    best = dict(bound=F(0), pair=None, repair_floor=F(0), replacement_floor=F(0))
    pairs = []
    for i, a in enumerate(scenarios):
        for j in range(i + 1, len(scenarios)):
            b = scenarios[j]
            q = [x + y for x, y in zip(a['weights'], b['weights'])]
            bank.set_weights(q)
            point = bank.bounds(row)
            lower = F(point['lower'])
            if lower.denominator != 1:
                raise ValueError('Current retained integer tree minima must be integral')
            target = int(scale * lower)
            gs = [scale * reduce(gcd, s['weights'], 0) for s in (a, b)]
            ups = [scale * s['upper'] for s in (a, b)]
            if any(v.denominator != 1 for v in ups):
                raise ValueError('Scenario upper left the declared price lattice')
            ups = list(map(int, ups))
            meter.pay('discrete_ambiguity', 'pair_objective_gcd_and_lattice_scaling', 8 * costs.m + 16)

            def allowed(r):
                meter.pay('discrete_ambiguity', 'rounded_pair_necessary_budget_test', 12)
                return sum(g * ((u + r) // g) if g else 0 for g, u in zip(gs, ups)) >= target

            low, high = -1, scale * max(sum(a['weights']), sum(b['weights']))
            if not allowed(high):
                raise ValueError('Admitted lower contradicts the Boolean objective ceiling')
            while low + 1 < high:
                middle = (low + high) // 2
                if allowed(middle):
                    high = middle
                else:
                    low = middle
            repair = F(high, scale)
            replacement = max(F(0), price - min(a['upper'], b['upper']))
            floor = min(repair, replacement)
            candidate = dict(bound=floor, pair=[i, j], repair_floor=repair,
                replacement_floor=replacement, summed_objective=q,
                checked_raw_lower=lower, lower_proof_id=point['proof_id'],
                price_lattice_scale=scale, objective_gcd_scaled=gs,
                scenario_uppers_scaled=ups,
                first_allowed_regret_scaled=high,
                previous_regret_scaled=low,
                previous_is_infeasible=low >= 0 and not allowed(low))
            pairs.append(candidate)
            meter.pay('discrete_ambiguity', 'pair_receipt_and_best_lower', 28 + costs.m)
            if floor > best['bound']:
                best = candidate
    # The simple mixture bound remains useful when its scenario menu differs;
    # retaining the maximum is safe even if the discrete pair bound is looser.
    floor = max(simple['bound'], best['bound'])
    meter.pay('discrete_ambiguity', 'source_bound_result_record', 24 + 10 * len(pairs))
    return dict(version=VERSION, row=row, source_id=costs.source_id,
        logical_source_id=bank.rows[row]['source_identity'], price=price,
        possible_modes=simple['possible_modes'], scenario_cap=cap,
        scenarios=scenarios, pairs=pairs, best_discrete_pair=best,
        simple_mixture_floor=simple['bound'], bound=floor,
        simple_mixture_receipt=simple, invoice_units=meter.total - start,
        new_acquisitions=0,
        meaning='Lower bound on best possible uniform fixed-action regret, with objective lattices and separately treated replacement; complete raw proof admission is a premise')


def verify_floor(receipt, row, bank, costs, price):
    got = source_floor(row, bank, costs, price, cap=receipt['scenario_cap'])
    for name in ('version', 'row', 'source_id', 'logical_source_id', 'price',
                 'possible_modes', 'scenarios', 'pairs', 'best_discrete_pair',
                 'simple_mixture_floor', 'bound'):
        if got[name] != receipt[name]:
            raise ValueError('Discrete ambiguity receipt mismatch: ' + name)
    return True
