#!/usr/bin/env python3
"""Independent finite checks for the S6 review and quantitative extensions.

Codex (GPT-6), November 10, 2026. Uses no earlier research checker.
Joint probabilities and comparisons of kernels are rational; logarithms use
50-digit Decimal arithmetic. Ordered histories, rather than the earlier
multinomial implementation, provide a separate computation route.
Run: python audit_s6.py --output audit_s6.json
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
import random


def dec(x):
    if isinstance(x, F):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x)


def labels(n):
    if n == 0:
        yield ()
        return
    for previous in labels(n - 1):
        for new in range(max(previous, default=-1) + 2):
            yield previous + (new,)


def refines(c, d):
    return all(c[i] != c[j] or d[i] == d[j]
               for i in range(len(c)) for j in range(i))


def canonical(signatures):
    seen = {}
    return tuple(seen.setdefault(s, len(seen)) for s in signatures)


def information(joint):
    left = [sum(row) for row in joint]
    right = [sum(row[j] for row in joint) for j in range(len(joint[0]))]
    ans = Decimal(0)
    for i, row in enumerate(joint):
        for j, mass in enumerate(row):
            if mass:
                ans += dec(mass) * dec(mass / (left[i] * right[j])).ln()
    return ans


def collapse(joint, c):
    size = max(c) + 1
    out = [[F(0) for _ in range(size)] for _ in range(size)]
    for i, row in enumerate(joint):
        for j, mass in enumerate(row):
            out[c[i]][c[j]] += mass
    return out


def fine_episodes(p, q, f, n):
    """Return rational P(ordered history, target type, target outcome)."""
    nt, nz, ny = len(p), len(q), len(f[0][0])
    obs = tuple(product(range(nz), range(ny)))
    result = []
    for history in product(obs, repeat=n):
        skill_mass = list(p)
        for z, y in history:
            for t in range(nt):
                skill_mass[t] *= q[z] * f[t][z][y]
        for target in range(nz):
            row = tuple(sum(skill_mass[t] * q[target] * f[t][target][y]
                            for t in range(nt)) for y in range(ny))
            result.append((history, target, row))
    assert sum(sum(row) for _, _, row in result) == 1
    return result


def score(episodes, c, local=False):
    grouped = {}
    for history, target, row in episodes:
        cell = c[target]
        shown = (tuple(y for z, y in history if c[z] == cell) if local
                 else tuple((c[z], y) for z, y in history))
        dest = grouped.setdefault((shown, cell), [F(0)] * len(row))
        for y, mass in enumerate(row):
            dest[y] += mass
    ans = Decimal(0)
    for row in grouped.values():
        total = sum(row)
        for mass in row:
            if mass:
                ans += dec(mass) * dec(mass / total).ln()
    return ans


def bern(p):
    return (1 - p, p)


def transfer_checks():
    worlds = [
        ("opposite skills", [F(1, 2)] * 2, [F(1, 2)] * 2,
         [[bern(F(9, 10)), bern(F(1, 10))],
          [bern(F(1, 10)), bern(F(9, 10))]], 5),
        ("twins", [F(2, 5), F(3, 5)], [F(1, 5), F(2, 5), F(2, 5)],
         [[bern(F(4, 5)), bern(F(4, 5)), bern(F(1, 5))],
          [bern(F(1, 5)), bern(F(1, 5)), bern(F(4, 5))]], 3),
        ("unequal masses", [F(1, 3), F(2, 3)],
         [F(1, 6), F(1, 3), F(1, 2)],
         [[bern(F(1, 4)), bern(F(1, 2)), bern(F(4, 5))],
          [bern(F(3, 4)), bern(F(1, 3)), bern(F(2, 5))]], 4),
        ("difficulty only", [F(1)], [F(1, 2)] * 2,
         [[bern(F(1, 5)), bern(F(4, 5))]], 3),
    ]
    rows, checked, bound_checked = [], 0, 0
    smallest_ratio = Decimal('Infinity')
    for name, p, q, f, nmax in worlds:
        nz, ny = len(q), len(f[0][0])
        parts = list(labels(nz))
        twin = canonical(tuple(f[t][z] for t in range(len(p))) for z in range(nz))
        marginal = canonical(tuple(sum(p[t] * f[t][z][y] for t in range(len(p)))
                                   for y in range(ny)) for z in range(nz))
        gaps = []
        for n in range(nmax + 1):
            episodes = fine_episodes(p, q, f, n)
            values = {c: score(episodes, c) for c in parts}
            target = marginal if n == 0 else twin
            best = values[tuple(range(nz))]
            for c, val in values.items():
                assert (abs(best - val) < Decimal('1e-42')) == refines(c, target)
                checked += 1
                if n:
                    for a, b in combinations(range(nz), 2):
                        if c[a] != c[b] or twin[a] == twin[b]:
                            continue
                        k = q[a] * q[b] / (q[a] + q[b])
                        moments = [sum(p[t] * (f[t][a][y] - f[t][b][y]) ** 2
                                       for t in range(len(p))) for y in range(ny)]
                        bound = k * k * sum(d * d for d in moments) / 2
                        assert best - val >= dec(bound) - Decimal('1e-42')
                        bound_checked += 1
                        smallest_ratio = min(smallest_ratio, (best - val) / dec(bound))
            gaps.append(str(best - values[(0,) * nz]))
        rows.append({"world": name, "n_max": nmax, "coarsest_gaps_nats": gaps})
    return {"worlds": rows, "partition_history_checks": checked,
            "uniform_history_bound_checks": bound_checked,
            "smallest_gap_to_bound_ratio": str(smallest_ratio)}


def diagnostic_checks():
    rng = random.Random(20261110)
    worlds = []
    for index in range(24):
        raw = [[rng.randint(1, 12) for _ in range(4)] for _ in range(3)]
        if index % 2 == 0:
            for row in raw:
                row[1] = 2 * row[0]
        likelihood = [[F(v, sum(row)) for v in row] for row in raw]
        worlds.append(([F(1, 6), F(1, 3), F(1, 2)], likelihood))
    checked = bounds = 0
    minimum_ratio = Decimal('Infinity')
    for prior, likelihood in worlds:
        nw = len(likelihood[0])
        mu = [sum(prior[t] * likelihood[t][w] for t in range(len(prior))) for w in range(nw)]
        joint = [[sum(prior[t] * likelihood[t][a] * likelihood[t][b]
                      for t in range(len(prior))) for b in range(nw)] for a in range(nw)]
        target = canonical(tuple(likelihood[t][w] / mu[w] for t in range(len(prior)))
                           for w in range(nw))
        optimum = information(joint)
        parts = list(labels(nw))
        values = {c: information(collapse(joint, c)) for c in parts}
        for c, val in values.items():
            assert (abs(optimum - val) < Decimal('1e-42')) == refines(c, target)
            for fine in parts:
                if refines(fine, c):
                    assert values[fine] >= val - Decimal('1e-42')
            checked += 1
            for a, b in combinations(range(nw), 2):
                if c[a] != c[b] or target[a] == target[b]:
                    continue
                d = sum(prior[t] * (likelihood[t][a] / mu[a] - likelihood[t][b] / mu[b]) ** 2
                        for t in range(len(prior)))
                k = mu[a] * mu[b] / (mu[a] + mu[b])
                bound = 2 * k ** 3 * d ** 2
                assert optimum - val >= dec(bound) - Decimal('1e-42')
                bounds += 1
                minimum_ratio = min(minimum_ratio, (optimum - val) / dec(bound))
    sharpness = []
    for denominator in (2, 4, 8, 16, 32, 64):
        e = F(1, denominator)
        likelihood = [[(1 + e) / 2, (1 - e) / 2],
                      [(1 - e) / 2, (1 + e) / 2]]
        joint = [[sum(likelihood[t][a] * likelihood[t][b] / 2 for t in range(2))
                  for b in range(2)] for a in range(2)]
        actual = information(joint)
        bound = e ** 4 / 2
        sharpness.append({"epsilon": str(e), "information_nats": str(actual),
                          "bound_nats": str(dec(bound)), "ratio": str(actual / dec(bound))})
    return {"worlds": len(worlds), "partition_checks": checked,
            "diagnostic_bound_checks": bounds,
            "smallest_gap_to_bound_ratio": str(minimum_ratio), "balanced_binary_sharpness": sharpness}


def support_checks():
    """Exact panel kernels; direct covariance test does not use the proof shortcut."""
    cases = []
    for name, rates, fashion in [
        ("specialists and occasion fashion", [[F(9, 10), F(1, 10)], [F(1, 10), F(9, 10)]], True),
        ("general trait and occasion fashion", [[F(9, 10), F(7, 10)], [F(2, 10), F(1, 10)]], True),
        ("trait on only one task", [[F(9, 10), F(1, 2)], [F(1, 10), F(1, 2)]], False),
    ]:
        m = 3 if fashion else 1
        approvals = list(product((0, 1), repeat=m))
        kernel = {}
        for t, x, a in product(range(2), range(2), approvals):
            mass = rates[t][x] if a[0] else 1 - rates[t][x]
            if fashion:
                mass *= F(1, 2) if a[1] == a[2] else 0
            kernel[t, x, a] = mass
        cases.append((name, m, approvals, kernel))
    m = 2
    approvals = list(product((0, 1), repeat=m))
    kernel = {(t, x, a): F(1, 2) if a[0] ^ a[1] == t ^ x else F(0)
              for t, x, a in product(range(2), range(2), approvals)}
    cases.append(("joint-only signal", m, approvals, kernel))
    rows = []
    for name, m, approvals, kernel in cases:
        sets = [frozenset(j for j in range(m) if mask & (1 << j)) for mask in range(1 << m)]

        def delineation(s):
            sub = list(product((0, 1), repeat=len(s)))
            return canonical(tuple(sum(kernel[t, x, a] for a in approvals
                                       if tuple(a[j] for j in sorted(s)) == b)
                                   for t in range(2) for b in sub) for x in range(2))

        def sigma(c):
            nc = max(c) + 1
            kc = {}
            for t, cell, a in product(range(2), range(nc), approvals):
                xs = [x for x in range(2) if c[x] == cell]
                kc[t, cell, a] = sum(kernel[t, x, a] for x in xs) / len(xs)
            found, self_found = set(), set()
            for j, cell in product(range(m), range(nc)):
                u = [sum(kc[t, cell, a] for a in approvals if a[j]) for t in range(2)]
                if u[0] != u[1]:
                    self_found.add(j)
                for other, a in product(range(nc), approvals):
                    v = [kc[t, other, a] for t in range(2)]
                    covariance = sum(u[t] * v[t] for t in range(2)) / 2 - sum(u) * sum(v) / 4
                    if covariance:
                        found.add(j)
            assert found == self_found
            return frozenset(found)

        phi = {s: sigma(delineation(s)) for s in sets}
        tracking = sigma((0, 1))
        for s in sets:
            assert phi[s] <= tracking
            if s <= tracking:
                assert s <= phi[s]
            for larger in sets:
                if s <= larger:
                    assert phi[s] <= phi[larger]
        assert phi[tracking] == tracking
        fixed = [sorted(s) for s in sets if phi[s] == s]
        start, chain = frozenset(), [[]]
        while phi[start] != start:
            start = phi[start]
            chain.append(sorted(start))
        rows.append({"world": name, "fixed_supports": fixed,
                     "trait_tracking": sorted(tracking), "bottom_iteration": chain})
    return rows


def repair_examples():
    p, q = [F(1)], [F(1, 2)] * 2
    f = [[bern(F(1, 5)), bern(F(4, 5))]]
    episode = fine_episodes(p, q, f, 1)
    fine, coarse = score(episode, (0, 1)), score(episode, (0, 0))
    # No persistent heterogeneity, hence independent whole observations.
    marginal = [q[x] * f[0][x][y] for x, y in product(range(2), range(2))]
    whole_information = information([[a * b for b in marginal] for a in marginal])
    assert whole_information == 0 and fine > coarse
    fa, fb = [F(1, 10), F(9, 10)], [F(4, 10), F(6, 10)]
    assert sum(fa) == sum(fb)
    ka = [F(19, 32) + F(1, 16) * x for x in fa]
    kb = [F(1, 2) + F(1, 4) * x for x in fb]
    assert ka == kb
    return {
        "different_objectives": {"difficulty_score_gain_nats": str(fine - coarse),
                                 "whole_observation_information_nats": str(whole_information)},
        "calibration": {"success_profiles": [[str(x) for x in fa], [str(x) for x in fb]],
                        "both_mean_success": "1/2", "transfer_correlation": 1,
                        "identical_approval_profiles": [str(x) for x in ka]},
        "tied_perron_components": {"matrix_up_to_positive_scale": [[1, 0], [0, 1]],
                                   "start_and_limit": ["1/4", "3/4"]},
        "neutral_replicator_tie": {"beta": 0, "equal_environment_alignment": True,
                                  "weight_derivative_for_every_weight": 0},
        "nonneutral_replicator_tie": {"beta": 1, "inner_product": 0, "environment_advantage": 1,
                                     "invader_payoff_advantage_at_mass_x": "2*x"},
        "full_plane_exemplars": {"exemplar_count": "hull_vertex_count",
                                 "original_arc_formula_excess": 1},
        "low_rank_many_exemplars": "N distinct positive quarter-circle points; rank 2; all N uniquely exposed",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    with localcontext() as ctx:
        ctx.prec = 50
        result = {"author": "Codex (GPT-6)", "cycle": "P4-R1-C001", "session": 6,
                  "method": "rational probabilities; ordered histories; 50-digit decimal logarithms",
                  "transfer": transfer_checks(), "diagnostic": diagnostic_checks(),
                  "support": support_checks(), "repair_examples": repair_examples()}
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded, encoding='utf-8', newline='\n')
        print(json.dumps({"output": str(args.output), "status": "passed",
                          "partition_history_checks": result['transfer']['partition_history_checks'],
                          "uniform_history_bound_checks": result['transfer']['uniform_history_bound_checks'],
                          "diagnostic_bound_checks": result['diagnostic']['diagnostic_bound_checks'],
                          "support_worlds": len(result['support'])}))
    else:
        print(encoded, end='')


if __name__ == '__main__':
    main()
