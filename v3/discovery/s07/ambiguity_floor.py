#!/usr/bin/env python3
"""Checked source-ambiguity floors for a fixed-action repair duty.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12.
A mixture is an adversarial lower-bound certificate, not a learned belief.
All logical profiles must first be admitted from raw source-bound evidence.
This calculation purchases no new proof, witness or source observation.
"""
from __future__ import annotations

from fractions import Fraction as F

VERSION = 's07-source-ambiguity-floor-v1'


def source_floor(row, bank, costs, price, *, cap=6):
    """Use at most cap compatible configurations and all equal-weight pairs.

    A result above tolerance proves that no fixed action, including any
    as-yet undiscovered feasible repair, can meet that uniform duty without
    narrowing the cost source. It does not prove that a logical purchase
    cannot improve later work or another request. A zero floor is inconclusive.
    The finite pair search is a heuristic, not the optimal minimax dual.
    """
    if type(cap) is not int or cap < 1 or F(price) < 0:
        raise ValueError('Positive integral scenario cap and nonnegative price required')
    meter = costs.meter
    if bank.meter is not meter:
        raise ValueError('One common meter required')
    start = meter.total
    price = F(price)
    possible = tuple(tuple(p) for p in costs.possible)
    if (len(possible) != costs.n or not possible
            or any(not p or len(set(p)) != len(p)
                   or any(type(k) is not int or not 0 <= k < len(costs.modes) for k in p)
                   for p in possible)):
        raise ValueError('Nonempty admitted finite mode sets required')
    if any(len(m) != costs.m or any(F(w) < 0 for w in m) for m in costs.modes):
        raise ValueError('Nonnegative source weights required')
    meter.pay('ambiguity_admission', 'source_possible_and_public_mode_words',
              sum(map(len, possible)) + costs.n + costs.m * len(costs.modes) + 12)
    assignments = []
    # Each configuration is actually compatible, not an arbitrary point of
    # an unrelated coordinate box. All choices use only public mode sets.
    for k in range(min(cap, len(costs.modes))):
        assignment = tuple(k if k in p else min(p) for p in possible)
        meter.pay('ambiguity_scenarios', 'compatible_configuration_construction',
                  sum(map(len, possible)) + 2 * costs.n)
        if assignment not in assignments:
            assignments.append(assignment)
    scenarios = []
    for assignment in assignments:
        weights = [sum(costs.modes[k][j] for k in assignment) for j in range(costs.m)]
        meter.pay('ambiguity_scenarios', 'configuration_objective_sum', 2 * costs.n * costs.m)
        bank.set_weights(weights)
        point = bank.bounds(row)
        scenarios.append(dict(assignment=list(assignment), weights=weights,
                              upper=min(price, F(point['upper'])),
                              witness_id=point['witness_id'], model=point['model'],
                              upper_action='replace' if price < point['upper'] else 'repair'))
    best = dict(bound=F(0), pair=None, mixture_lower=F(0), average_upper=None,
                lower_proof_id='nonnegative_objective')
    pairs = []
    for i, a in enumerate(scenarios):
        for j in range(i + 1, len(scenarios)):
            b = scenarios[j]
            summed = [x + y for x, y in zip(a['weights'], b['weights'])]
            meter.pay('ambiguity_mixture', 'two_scenario_objective_sum', 2 * costs.m)
            bank.set_weights(summed)
            point = bank.bounds(row)
            # The repair optimum is positively homogeneous; replacement is
            # clipped only after division, because its price remains p.
            lower = min(price, F(point['lower'], 2))
            upper = (a['upper'] + b['upper']) / 2
            bound = max(F(0), lower - upper)
            candidate = dict(bound=bound, pair=[i, j], mixture_lower=lower,
                             average_upper=upper, lower_proof_id=point['proof_id'])
            pairs.append(candidate)
            meter.pay('ambiguity_mixture', 'exact_clipping_gap_and_receipt', 16)
            if bound > best['bound']:
                best = candidate
    meter.pay('ambiguity_output', 'bound_scenario_and_dependency_record',
              24 + len(scenarios) * (costs.n + costs.m + 6) + 6 * len(pairs))
    return dict(version=VERSION, row=row, source_id=costs.source_id,
                logical_source_id=bank.rows[row]['source_identity'],
                possible_modes=[list(p) for p in possible], price=price,
                scenario_cap=cap, scenarios=scenarios, pairs=pairs,
                **best, invoice_units=meter.total - start,
                new_acquisitions=0,
                meaning='Lower bound on the best possible uniform fixed-action regret over the admitted finite cost source; source-bound raw logical admission is a premise')


def verify_floor(receipt, row, bank, costs, price):
    """Reconstruct all arithmetic from an independently admitted current bank."""
    got = source_floor(row, bank, costs, price, cap=receipt['scenario_cap'])
    for name in ('version', 'row', 'source_id', 'logical_source_id', 'possible_modes',
                 'price', 'scenarios', 'pairs', 'bound', 'pair', 'mixture_lower',
                 'average_upper', 'lower_proof_id'):
        if got[name] != receipt[name]:
            raise ValueError('Source-ambiguity receipt mismatch: ' + name)
    return True
