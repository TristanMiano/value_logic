#!/usr/bin/env python3
"""Exact unflagged-assignment counterexample and longer-history repair.

Codex (GPT-6), November 10, 2026. Rational joint laws, decimal logarithms.
No earlier Fable implementation is imported. Ordered histories are explicit.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
import argparse
import json
from math import lcm
from pathlib import Path

from audit_s6 import dec, score


def world(share=F(1, 2), amplitude=F(1, 10)):
    states = list(product((-1, 1), repeat=3))
    t = (1 - share) / 2
    q, outcomes = [], []
    for u, v, w in states:
        qa = F(1, 2) + t * u
        qb = 1 - qa
        fa = F(1, 2) + amplitude * (v / F(2) + t * w) / qa
        fb = F(1, 2) + amplitude * (v / F(2) - t * w) / qb
        assert 0 < fa < 1 and 0 < fb < 1
        q.append([qa, qb])
        outcomes.append([[1 - fa, fa], [1 - fb, fb]])
    return states, q, outcomes


def episodes(q, f, n, prior=None):
    if prior is None:
        prior = [F(1, len(q))] * len(q)
    observations = list(product(range(2), range(2)))
    result = []
    for hist in product(observations, repeat=n):
        posterior_mass = []
        for t in range(len(q)):
            mass = prior[t]
            for x, y in hist:
                mass *= q[t][x] * f[t][x][y]
            posterior_mass.append(mass)
        for target in range(2):
            row = [sum(posterior_mass[t] * q[t][target] * f[t][target][y]
                       for t in range(len(q))) for y in range(2)]
            result.append((hist, target, row))
    assert sum(sum(row) for _, _, row in result) == 1
    return result


def sharp_world():
    """Match independent task/result sequence moments through three views."""
    prior, q, f, latent = [], [], [], []
    for r, probability in ((F(1, 2), F(5, 8)), (F(3, 2), F(3, 8))):
        for su, sv in product((-1, 1), repeat=2):
            u, v, w = su * r / 4, sv * r / 4, F(su * sv, 16)
            joint = [[(1 + x * u + y * v + x * y * w) / 4
                      for y in (-1, 1)] for x in (-1, 1)]
            qt = [sum(row) for row in joint]
            ft = [[p / qt[x] for p in joint[x]] for x in range(2)]
            assert all(p > 0 for row in joint for p in row)
            prior.append(probability / 4)
            q.append(qt)
            f.append(ft)
            latent.append([str(z) for z in (r, su, sv, u, v, w)])
    return prior, q, f, latent


def entropy(row):
    return -sum((dec(x) * dec(x).ln() for x in row if x), Decimal(0))


def exact_tie(q, f, n, prior=None):
    """Conditional probabilities compared by integer cross-products, no logs."""
    if prior is None:
        prior = [F(1, len(q))] * len(q)
    values = [q[t][x] * f[t][x][y]
              for t, x, y in product(range(len(q)), range(2), range(2))]
    denominator = lcm(*(v.denominator for v in values))
    g = [[[int(q[t][x] * f[t][x][y] * denominator) for y in range(2)]
          for x in range(2)] for t in range(len(q))]
    pd = lcm(*(p.denominator for p in prior))
    weights = [int(p * pd) for p in prior]
    marg = [[sum(g[t][x][y] for x in range(2)) for y in range(2)] for t in range(len(q))]
    for ys in product(range(2), repeat=n):
        cm = weights.copy()
        for y in ys:
            cm = [a * marg[t][y] for t, a in enumerate(cm)]
        coarse = [sum(cm[t] * marg[t][y] for t in range(len(q))) for y in range(2)]
        for xs in product(range(2), repeat=n):
            fm = weights.copy()
            for x, y in zip(xs, ys):
                fm = [a * g[t][x][y] for t, a in enumerate(fm)]
            for x in range(2):
                row = [sum(fm[t] * g[t][x][y] for t in range(len(q))) for y in range(2)]
                if row[0] * sum(coarse) != coarse[0] * sum(row):
                    return False
    return True


def support_boundary_grid():
    checked = observable = 0
    first_gaps = dict.fromkeys(('0', '1', '2', '3', 'none'), 0)
    for qa0, qa1 in product((F(0), F(1, 4), F(1, 2), F(3, 4), F(1)), repeat=2):
        q = [[qa0, 1 - qa0], [qa1, 1 - qa1]]
        for rates in product((F(0), F(1, 2), F(1)), repeat=4):
            f = [[[1 - rates[2 * t + x], rates[2 * t + x]] for x in range(2)]
                 for t in range(2)]
            joint_difference = any(q[t][0] * q[t][1] * (f[t][0][1] - f[t][1][1])
                                   for t in range(2))
            checked += 1
            if not joint_difference:
                continue
            observable += 1
            first = 'none'
            for n in range(4):
                if not exact_tie(q, f, n):
                    first = str(n)
                    break
            assert not exact_tie(q, f, 3)
            first_gaps[first] += 1
    return {'worlds': checked, 'jointly_observable_nontwins': observable,
            'first_strict_gap_counts': first_gaps,
            'n3_violations': 0,
            'boundary_scope': 'zero and positive assignment/outcome probabilities; two latent states'}


def flagged_gap(share, q, f):
    """One history; both judges observe independent-assignment flags."""
    obs = list(product(range(2), range(2), range(2)))  # x, assigned, outcome
    fine, coarse = {}, {}
    for x, assigned, y in obs:
        for target, target_assigned in product(range(2), repeat=2):
            row = [F(0), F(0)]
            for t in range(len(q)):
                qh = share / 2 if assigned else q[t][x] - share / 2
                qt = share / 2 if target_assigned else q[t][target] - share / 2
                for out in range(2):
                    row[out] += qh * qt * f[t][x][y] * f[t][target][out] / len(q)
            fine[x, assigned, y, target, target_assigned] = row
            key = (assigned, y, target_assigned)
            coarse.setdefault(key, [F(0), F(0)])
            coarse[key] = [a + b for a, b in zip(coarse[key], row)]
    def value(table):
        result = Decimal(0)
        for row in table.values():
            mass = sum(row)
            if mass:
                result -= dec(mass) * entropy([p / mass for p in row])
        return result
    return value(fine) - value(coarse)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    with localcontext() as ctx:
        ctx.prec = 50
        states, q, f = world()
        rows = []
        for n in range(6):
            data = episodes(q, f, n)
            vf, vc = score(data, (0, 1)), score(data, (0, 0))
            gap = vf - vc
            assert gap >= Decimal('-1e-45')
            if n <= 1:
                assert abs(gap) < Decimal('1e-45')
            assert exact_tie(q, f, n) == (n <= 1)
            rows.append({'n_history': n, 'fine_score': str(vf),
                         'coarse_score': str(vc), 'gap_nats': str(gap)})
        limiting = Decimal(0)
        separation = F(0)
        exact_weighted_bound = F(0)
        for t in range(len(q)):
            mixture = [sum(q[t][x] * f[t][x][y] for x in range(2)) for y in range(2)]
            limiting += (entropy(mixture) - sum(dec(q[t][x]) * entropy(f[t][x])
                                                for x in range(2))) / len(q)
            difference = sum(abs(f[t][0][y] - f[t][1][y]) for y in range(2))
            separation += difference ** 2 / len(q)
            exact_weighted_bound += q[t][0] * q[t][1] * difference ** 2 / (2 * len(q))
        exposure_bound = F(1, 2) * F(1, 4) * separation / 2
        assert limiting >= dec(exact_weighted_bound) >= dec(exposure_bound) > 0
        flag_gap = flagged_gap(F(1, 2), q, f)
        assert flag_gap > 0
        # The equality mechanism survives arbitrarily large (but not full)
        # independent assignment shares; this is not a zero-support artifact.
        high_share = []
        for share in (F(9, 10), F(99, 100), F(999, 1000)):
            _, qs, fs = world(share)
            data = episodes(qs, fs, 1)
            gap = score(data, (0, 1)) - score(data, (0, 0))
            assert abs(gap) < Decimal('1e-45')
            assert any(fs[t][0] != fs[t][1] for t in range(len(qs)))
            high_share.append({'assignment_share': str(share), 'n1_gap_nats': str(gap)})
        prior2, q2, f2, latent2 = sharp_world()
        sharp_rows = []
        for n in range(6):
            data = episodes(q2, f2, n, prior2)
            gap = score(data, (0, 1)) - score(data, (0, 0))
            if n <= 2:
                assert abs(gap) < Decimal('1e-44')
            else:
                assert gap > 0
            assert exact_tie(q2, f2, n, prior2) == (n <= 2)
            sharp_rows.append({'n_history': n, 'gap_nats': str(gap)})
        result = {'author': 'Codex (GPT-6)', 'cycle': 'P4-R1-C001', 'session': 6,
                  'states_U_V_W': states, 'assignment_share': '1/2',
                  'assignment_laws': [[str(x) for x in row] for row in q],
                  'success_laws': [[str(f[t][x][1]) for x in range(2)] for t in range(len(q))],
                  'finite_history': rows, 'limiting_gap_nats': str(limiting),
                  'mean_L1_separation_squared': str(separation),
                  'weighted_limit_lower_bound': str(exact_weighted_bound),
                  'exposure_only_limit_lower_bound': str(exposure_bound),
                  'flagged_n1_gap_nats': str(flag_gap), 'high_assignment_shares': high_share,
                  'support_boundary_grid': support_boundary_grid(),
                  'sharp_three_history_world': {'latent_R_signs_u_v_w': latent2,
                      'prior': [str(x) for x in prior2], 'independent_assignment_share': '5/8',
                      'joint_kernel_minimum': str(min(q2[t][x] * f2[t][x][y]
                          for t, x, y in product(range(len(q2)), range(2), range(2)))),
                      'finite_history': sharp_rows}}
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded, encoding='utf8', newline='\n')
        print(json.dumps({'output': str(args.output), 'status': 'passed',
                          'gaps': [r['gap_nats'] for r in rows], 'limit': str(limiting)}))
    else:
        print(encoded, end='')


if __name__ == '__main__':
    main()
