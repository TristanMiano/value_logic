"""R1.14: exact finite kernels/credit operators and numerical score checks.

Codex (GPT-6), November 10, 2026. Run from any working directory.
No hidden traits are provided to a fitted learner: this script checks
population constructions, not an implemented finite-sample estimator.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, exp, log, prod, sqrt
from pathlib import Path
import json
import numpy as np


def subsets(r, maximum):
    return [s for k in range(1, maximum + 1)
            for s in combinations(range(r), k)]


def partitions(n):
    if n == 0:
        yield ()
        return
    for previous in partitions(n - 1):
        for label in range(max(previous, default=-1) + 2):
            yield previous + (label,)


def canonical(keys):
    found = {}
    return tuple(found.setdefault(k, len(found)) for k in keys)


def marginal(world, r, coalition):
    vectors = list(product((-1, 1), repeat=r))
    outputs = list(product((-1, 1), repeat=len(coalition)))
    indices = {a: i for i, a in enumerate(outputs)}
    result = []
    for theta_rows in world:
        rows = []
        for row in theta_rows:
            out = [F(0)] * len(outputs)
            for a, value in zip(vectors, row):
                out[indices[tuple(a[j] for j in coalition)]] += value
            assert sum(out) == 1
            rows.append(tuple(out))
        result.append(tuple(rows))
    return tuple(result)


def factor_partition(marginals, active):
    nx = len(marginals[0][0])
    nt = len(marginals[0])
    return canonical(tuple(tuple(marginals[s][t][x])
                           for s in active for t in range(nt))
                     for x in range(nx))


def credit(marginals, partition):
    result = []
    cells = [[x for x, cell in enumerate(partition) if cell == k]
             for k in sorted(set(partition))]
    for i, kernel in enumerate(marginals):
        varying = False
        for cell in cells:
            rows = [tuple(sum((theta[x][a] for x in cell), F(0)) / len(cell)
                          for a in range(len(theta[0]))) for theta in kernel]
            varying |= len(set(rows)) > 1
        if varying:
            result.append(i)
    return tuple(result)


def operator_report(marginals):
    count = len(marginals)
    fixed = []
    for mask in range(1 << count):
        active = tuple(i for i in range(count) if mask & (1 << i))
        part = factor_partition(marginals, active)
        if credit(marginals, part) == active:
            fixed.append({'active': active, 'partition': part})
    active, path = (), []
    while True:
        part = factor_partition(marginals, active)
        path.append({'active': active, 'partition': part})
        new = credit(marginals, part)
        if new == active:
            break
        assert set(active) <= set(new)
        active = new
    return {'fixed_points': fixed, 'bottom_iteration': path}


def score(kernel, partition):
    """Own-coalition one-history optimal prediction; population probabilities."""
    p = np.array(kernel, dtype=float)
    nt, nx, ny = p.shape
    cells = sorted(set(partition))
    # Joint of (history cell, history approval, target cell, target approval).
    cell_p = np.stack([p[:, np.array(partition) == c, :].sum(axis=1) / nx
                       for c in cells], axis=1)
    joint = np.einsum('tcu,tdv->cudv', cell_p, cell_p) / nt
    # Target cell is supplied before prediction, so sum over target approval only.
    base = joint.sum(axis=3, keepdims=True)
    assert abs(joint.sum() - 1) < 1e-12
    return float(np.sum(joint * np.log(joint / base)))


def six_judge_world():
    world = []
    for theta in product((-1, 1), repeat=3):
        rows = []
        for s, t in product((-1, 1), repeat=2):
            means = (F(theta[0], 2), F(theta[1] * s, 2), F(theta[2] * t, 2))
            row = tuple(prod((1 + means[j] * a[2*j] * a[2*j+1]) / 4
                             for j in range(3))
                        for a in product((-1, 1), repeat=6))
            assert sum(row) == 1 and min(row) > 0
            rows.append(row)
        world.append(rows)
    return world


def parity_world(r, rho=F(1, 2)):
    world = []
    for anchor_theta, theta in product((-1, 1), repeat=2):
        rows = []
        for x in (-1, 1):
            row = tuple((1 + F(anchor_theta, 2)*a[0]*a[1])/4
                        * (1 + rho*theta*x*prod(a[2:])) / (2**r)
                        for a in product((-1, 1), repeat=r+2))
            assert sum(row) == 1 and min(row) > 0
            rows.append(row)
        world.append(rows)
    return world


def quantitative_checks():
    rng = np.random.default_rng(20261124)
    rows = []
    for r in (3, 4, 6):
        support = subsets(r, 2)
        vectors = np.array(list(product((-1, 1), repeat=r)))
        features = np.array([np.prod(vectors[:, s], axis=1) for s in support]).T
        for _ in range(30):
            lam = rng.uniform(-.6, .6, len(support))
            mup = rng.uniform(-.6, .6, len(support))
            logits = features @ np.stack([lam, mup], axis=1)
            probabilities = np.exp(logits - logits.max(axis=0))
            probabilities /= probabilities.sum(axis=0)
            p, q = probabilities.T
            moment_difference = (p-q) @ features
            epsilon = float(np.max(np.abs(moment_difference)))
            bound_norm = max(float(np.abs(lam).sum()), float(np.abs(mup).sum()))
            sym_kl = float(np.sum((p-q) * np.log(p/q)))
            identity = float((lam-mup) @ moment_difference)
            tv = float(np.abs(p-q).sum()/2)
            assert abs(sym_kl-identity) < 1e-12
            bound = min(sqrt(bound_norm*epsilon/2),
                        exp(bound_norm)*sqrt(len(support))*epsilon/2)
            assert tv <= bound + 1e-12
            rows.append({'r': r, 'tv': tv, 'bound': bound,
                         'identity_residual': abs(sym_kl-identity)})
    approximate = []
    for rho in (F(1, 10), F(1, 2), F(9, 10)):
        delta = float((1+rho)/2)*log(float(1+rho)) + float((1-rho)/2)*log(float(1-rho))
        # Two opposite parity laws, both moment-matched by the uniform law.
        tv = float(rho)
        bound = 2*sqrt(delta/2)
        assert tv <= bound + 1e-12
        approximate.append({'rho': str(rho), 'tv': tv,
                            'each_projection_kl': delta, 'bound': bound})
    return {'count': len(rows), 'max_identity_residual': max(x['identity_residual'] for x in rows),
            'max_tv_over_bound': max(x['tv']/x['bound'] for x in rows),
            'approximate_parity': approximate}


def main():
    world = six_judge_world()
    edges = ((0, 1), (2, 3), (4, 5))
    anchored = ((0, 1), (0, 1, 2, 3), (0, 1, 4, 5))
    singles = [marginal(world, 6, (i,)) for i in range(6)]
    assert credit(singles, (0, 1, 2, 3)) == ()
    # One full observation is uniform for every task, before seeing any same-performer history.
    for x in range(4):
        assert all(sum(world[t][x][a] for t in range(8))/8 == F(1, 64)
                   for a in range(64))
    edge_kernels = [marginal(world, 6, s) for s in edges]
    anchor_kernels = [marginal(world, 6, s) for s in anchored]
    edge_report = operator_report(edge_kernels)
    anchor_report = operator_report(anchor_kernels)
    assert len(edge_report['fixed_points']) == 4
    assert edge_report['bottom_iteration'][-1]['partition'] == (0, 0, 0, 0)
    assert len(anchor_report['fixed_points']) == 1
    assert anchor_report['bottom_iteration'][-1]['partition'] == (0, 1, 2, 3)
    assert factor_partition([tuple(tuple(x) for x in world)], (0,)) == (0, 1, 2, 3)
    score_rows = []
    for partition in partitions(4):
        score_rows.append({'partition': partition,
                           'anchored_score': sum(score(k, partition) for k in anchor_kernels),
                           'pair_score': sum(score(k, partition) for k in edge_kernels)})
    for key in ('anchored_score', 'pair_score'):
        winners = [x['partition'] for x in score_rows
                   if abs(x[key] - max(y[key] for y in score_rows)) < 1e-12]
        assert winners == [(0, 1, 2, 3)]
    parity_rows = []
    for r in (3, 4, 6):
        pw = parity_world(r)
        groups = [tuple(sorted({0, 1} | set(s)))
                  for s in subsets(r+2, min(2, r-1))]
        groups = sorted(set(groups))
        kernels = [marginal(pw, r+2, s) for s in groups]
        assert factor_partition(kernels, range(len(groups))) == (0, 0)
        assert credit(kernels, (0, 0)) == tuple(range(len(groups)))
        full = marginal(pw, r+2, tuple(range(r+2)))
        assert factor_partition([full], (0,)) == (0, 1)
        parity_rows.append({'parity_judges': r, 'anchored_groups': len(groups),
                            'factor_partition': [0, 0], 'full_partition': [0, 1]})
    counts = []
    for r in (6, 20):
        group_sizes = [2] + [3]*(r-2) + [4]*comb(r-2, 2)
        counts.append({'judges': r, 'all_pairwise_anchored_groups': len(group_sizes),
                       'marginal_entries': sum(2**s for s in group_sizes),
                       'full_entries': 2**r,
                       'known_disjoint_edges_entries': 4+(r//2-1)*16})
    output = {'author': 'Codex (GPT-6)', 'status': 'passed',
              'scope': 'population construction checks, not a fitted learner or independent review',
              'single_performance_full_law': 'uniform on all four tasks',
              'individual_judges_credited': [], 'unanchored_pairs': edge_report,
              'anchored_groups': anchor_report, 'partition_score_checks': score_rows,
              'parity_boundaries': parity_rows, 'representation_counts': counts,
              'quantitative_checks': quantitative_checks()}
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({key: output[key] for key in ('status', 'single_performance_full_law',
                                                 'representation_counts', 'quantitative_checks')}))


if __name__ == '__main__':
    main()
