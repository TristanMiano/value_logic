#!/usr/bin/env python3
"""Rational-probability checks of selected-task quantitative recovery.

Codex (GPT-6), November 10, 2026. Independent ordered episode enumeration
and decimal conditional entropy. Checks do not substitute for the proof.
"""
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
import argparse
import json
from pathlib import Path
import random

from audit_s6 import dec


def joint_tables(q, f, prior, history):
    ny = len(f[0][0])
    observations = list(product(range(2), range(ny)))
    fine, coarse = defaultdict(lambda: [F(0)] * ny), defaultdict(lambda: [F(0)] * ny)
    for hist in product(observations, repeat=history):
        masses = list(prior)
        for x, y in hist:
            masses = [p * q[t][x] * f[t][x][y] for t, p in enumerate(masses)]
        for target in range(2):
            row = [sum(p * q[t][target] * f[t][target][y] for t, p in enumerate(masses))
                   for y in range(ny)]
            fine[(hist, target)] = row
            coarse_key = tuple(y for x, y in hist)
            for y, value in enumerate(row): coarse[coarse_key][y] += value
    return fine, coarse


def gap(q, f, prior, history):
    fine, coarse = joint_tables(q, f, prior, history)
    def conditional_score(table):
        result = Decimal(0)
        for row in table.values():
            mass = sum(row)
            if mass:
                result += sum((dec(v) * (dec(v) / dec(mass)).ln() for v in row if v), Decimal(0))
        return result
    return conditional_score(fine) - conditional_score(coarse)


def witness_mean(q, f, prior):
    return sum(prior[t] * q[t][0] ** 2 * q[t][1] ** 2
               * sum((a - b) ** 2 for a, b in zip(f[t][0], f[t][1])) for t in range(len(q)))


def interpolation_check(q, f, prior):
    """Check the exact inverse-forecast moment bound used in the proof."""
    ny = len(f[0][0])
    g = [[[q[t][x] * f[t][x][y] for y in range(ny)] for x in range(2)] for t in range(len(q))]
    # Here K contains both task types, so q_K=1; keep the generic formula.
    qk = [sum(qt) for qt in q]
    gk = [[g[t][0][y] + g[t][1][y] for y in range(ny)] for t in range(len(q))]
    factor = F(0)
    for y, v in product(range(ny), repeat=2):
        if y == v: continue
        den = sum(prior[t] * gk[t][y] ** 2 * gk[t][v] * qk[t] for t in range(len(q)))
        num = sum(prior[t] * gk[t][y] ** 3 * gk[t][v] for t in range(len(q)))
        cv = sum(prior[t] * gk[t][v] * qk[t] ** 3 for t in range(len(q)))
        assert den ** 3 <= num ** 2 * cv
        selected_mass = F(0)
        for t in range(len(q)):
            h = g[t][0][y] * g[t][1][v] + g[t][1][y] * g[t][0][v]
            selected_mass += prior[t] * h * (g[t][0][y] * q[t][1] + g[t][1][y] * q[t][0])
        assert selected_mass <= den
        if den:
            assert num > 0
            factor += selected_mass * den ** 2 / num ** 2
        else:
            assert selected_mass == 0
    assert factor <= ny - 1
    return factor


def sharp_family(h):
    prior, q, f = [], [], []
    for r, probability in ((1 - h, F(1, 2) + h / 4), (1 + h, F(1, 2) - h / 4)):
        for s, t in product((-1, 1), repeat=2):
            u, v, w = s * r / 4, t * r / 4, F(s * t, 16)
            joint = [[(1 + x * u + y * v + x * y * w) / 4 for y in (-1, 1)] for x in (-1, 1)]
            qt = [sum(row) for row in joint]
            ft = [[p / qt[x] for p in joint[x]] for x in range(2)]
            prior.append(probability / 4); q.append(qt); f.append(ft)
    return prior, q, f


def exact_quadratic_coefficient():
    p0, q0, f0 = sharp_family(F(0))
    ph, qh, fh = sharp_family(F(1, 2))
    base = joint_tables(q0, f0, p0, 3)
    perturbed = joint_tables(qh, fh, ph, 3)
    tau = F(15, 16)
    curvature = F(0)
    for sign, t0, th in zip((1, -1), base, perturbed):
        for key, row0 in t0.items():
            row1 = [(b - a) / tau for a, b in zip(row0, th[key])]
            curvature += sign * (sum(b * b / a for a, b in zip(row0, row1))
                                 - sum(row1) ** 2 / sum(row0))
    # delta=tau/2048; KL has half the second derivative as its coefficient.
    coefficient = 2048 ** 2 * curvature / 2
    assert coefficient > 2
    return coefficient


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path); args = p.parse_args()
    rng = random.Random(20261110)
    records, sharp = [], []
    with localcontext() as context:
        context.prec = 60
        for index in range(36):
            ny = 3 if index % 3 == 0 else 2
            states = 3
            prior = [F(1, states)] * states
            q, f = [], []
            for t in range(states):
                qa = F(rng.randrange(5), 4)
                q.append([qa, 1 - qa])
                rows = []
                for x in range(2):
                    counts = [rng.randrange(4) for _ in range(ny)]
                    if not sum(counts): counts[0] = 1
                    rows.append([F(z, sum(counts)) for z in counts])
                f.append(rows)
            delta = witness_mean(q, f, prior)
            factor = interpolation_check(q, f, prior)
            gamma = min(p for ft in f for row in ft for p in row)
            for n in (3, 4) if ny == 2 else (3,):
                gain = gap(q, f, prior, n)
                bound = F(2, ny - 1) * delta ** 2
                positive_bound = 16 * gamma ** 2 * delta ** 2
                assert gain + Decimal('1e-50') >= dec(max(bound, positive_bound))
                records.append({'world': index, 'outcomes': ny, 'history': n,
                                'witness': str(delta), 'gain_nats': str(gain),
                                'universal_bound': str(bound), 'positive_outcome_bound': str(positive_bound),
                                'inverse_forecast_mass_factor': str(factor)})
        for power in range(1, 9):
            h = F(1, 2 ** power)
            prior, q, f = sharp_family(h)
            delta = witness_mean(q, f, prior)
            assert delta == (4 * h ** 2 - h ** 4) / 2048
            gain = gap(q, f, prior, 3)
            assert gain >= dec(2 * delta * delta)
            sharp.append({'h': str(h), 'witness': str(delta), 'gain_nats': str(gain),
                          'gain_over_witness_squared': str(gain / dec(delta * delta))})
    coefficient = exact_quadratic_coefficient()
    result = {'author': 'Codex (GPT-6)', 'status': 'passed',
              'rational_worlds': 36, 'history_bound_comparisons': len(records),
              'includes_zero_assignments_and_outcomes': True,
              'checks': records, 'sharp_order_family': sharp,
              'exact_limit_gain_over_witness_squared': str(coefficient),
              'exact_limit_decimal': float(coefficient),
              'scope': 'Quadratic order is proved using an interior perturbation; these numbers only check its consequences.'}
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output: args.output.write_text(encoded, encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))


if __name__ == '__main__': main()
