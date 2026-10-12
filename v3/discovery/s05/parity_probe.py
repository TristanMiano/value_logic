"""Small constructive check, not confirmation; ChatGPT (GPT-6 Astra Pro).

Question: does reusable minimum-T-join closure agree with direct finite-world
optimization under only pair-disagreement upper bounds? Also expose the
single-target / joint-value distinction and a correlated cancellation example.
Run from repository root: python v3/discovery/s05/parity_probe.py
"""
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random
import time

import numpy as np
import scipy
from scipy.optimize import linprog

from parity_closure import PairClosure, boundary


def world_lp(n, pairs, targets):
    """Separate optimization directly over all 2^(n-1) rooted bit worlds."""
    worlds = [tuple([0, *bits]) for bits in itertools.product((0, 1), repeat=n-1)]
    a = np.array([[int(w[x] != w[y]) for w in worlds] for x, y, _ in pairs], float)
    objective = np.array([sum(sum(w[v] for v in t) % 2 for t in targets)
                          for w in worlds], float)
    result = linprog(-objective, A_ub=a if len(pairs) else None,
                     b_ub=[p for _, _, p in pairs] if len(pairs) else None,
                     A_eq=np.ones((1, len(worlds))), b_eq=[1],
                     bounds=(0, None), method='highs')
    if not result.success:
        raise RuntimeError(result.message)
    witness = [{'negative_vertices': [i for i, v in enumerate(w) if v],
                'mass': float(x)} for w, x in zip(worlds, result.x) if x > 1e-10]
    residual = max([0.0, *([float(v) for v in a @ result.x - np.array([p for _, _, p in pairs])]
                          if len(pairs) else [])])
    return dict(optimum=float(-result.fun), witness=witness,
                max_constraint_residual=residual)


def main():
    started = time.perf_counter_ns()
    rng = random.Random(2026101201)
    rows = []
    # A modest source-bound development screen across sparse/dense, clipped,
    # zero-bound, disconnected, empty-target and nonempty-target cases.
    for n in range(2, 8):
        all_pairs = list(itertools.combinations(range(n), 2))
        for graph_index in range(8):
            pairs = [(a, b, rng.choice([0, .01, .08, .2, .4, .8, 1]))
                     for a, b in all_pairs if rng.random() < (graph_index + 1) / 9]
            closure = PairClosure(n, pairs)
            choices = [t for k in range(0, n+1, 2)
                       for t in itertools.combinations(range(n), k)]
            targets = [(), *rng.sample(choices[1:], min(3, len(choices)-1))]
            for target in targets:
                cert = closure.certificate(target)
                lp = world_lp(n, pairs, [target])
                delta = abs(cert['error_upper'] - lp['optimum'])
                rows.append(dict(n=n, graph_index=graph_index, pairs=pairs,
                                 target=target, certificate=cert, lp=lp,
                                 absolute_difference=delta))
                assert delta < 1e-8

    edge_graph = [(0, 1, .2), (1, 2, .2), (2, 3, .2), (3, 4, .2)]
    blocks = edge_graph + [(0, 2, 0), (2, 4, 0)]
    cancellation = dict(
        construction='Z1=Z2=A, Z3=Z4=B; Pr(A=-1)=Pr(B=-1)=.2. No independence needed.',
        target=[0, 4], edge_only=PairClosure(5, edge_graph).certificate([0, 4]),
        with_blocks=PairClosure(5, blocks).certificate([0, 4]),
        direct_target_error=0,
        acquired_vertices_per_row=dict(edge_marginals=[1, 2, 3, 4],
                                       two_blocks=[2, 4], direct_target=[4]),
        scope='Population illustration; empirical error bounds are not supplied for free.')

    cross = [(a, b, .2) for a in (0, 1) for b in (2, 3, 4)]
    targets = list(itertools.combinations(range(5), 2))
    closure = PairClosure(5, cross)
    joint_gap = dict(graph=cross, targets=targets,
                     sum_individual_sharp_bounds=sum(closure.bound(t) for t in targets),
                     joint=world_lp(5, cross, targets),
                     scope='Individual sharpness does not imply sharp sum-of-targets value.')
    assert abs(joint_gap['sum_individual_sharp_bounds'] - 2.8) < 1e-8
    assert abs(joint_gap['joint']['optimum'] - 2.4) < 1e-8
    here = Path(__file__).resolve().parent
    result = dict(status='DEVELOPMENT', contributor='ChatGPT (GPT-6 Astra Pro)',
                  generated_utc=datetime.now(timezone.utc).isoformat(), seed=2026101201,
                  source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in [Path(__file__), here/'parity_closure.py']},
                  environment=dict(python=platform.python_version(), numpy=np.__version__,
                                   scipy=scipy.__version__),
                  check_count=len(rows),
                  max_absolute_difference=max(row['absolute_difference'] for row in rows),
                  max_constraint_residual=max(row['lp']['max_constraint_residual'] for row in rows),
                  elapsed_ns=time.perf_counter_ns()-started,
                  cancellation=cancellation, joint_gap=joint_gap, cases=rows)
    (here/'parity_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['check_count','max_absolute_difference',
                                          'max_constraint_residual','elapsed_ns']}))
    print(json.dumps({'cancellation':cancellation,'joint_gap':joint_gap}))


if __name__ == '__main__':
    main()
