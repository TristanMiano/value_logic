#!/usr/bin/env python3
"""Check the n = 1 stability bound and probe monotonicity of deficits in n.

P4-R1-C001. Written by Claude (Fable 5.2), 2026-11-09.
Bound: if a delineation merges two types A, B with sampling masses a, b, then
V_1(finest) - V_1(c) >= 0.5 * (ab/(a+b))**2 * sum_y (E[(f_A(y)-f_B(y))**2])**2.
"""
import json, sys
import numpy as np
from exact_scores import value, canon, indep

rng = np.random.default_rng(20261109)
worst_ratio, viol, pairs, nonmono = float("inf"), 0, 0, 0
tightest = None
for i in range(400):
    k, nt = 3, int(rng.integers(2, 5))
    ny = 2 if i % 2 else 3
    p = rng.dirichlet(np.ones(nt))
    q = rng.dirichlet(np.ones(k) * 2)
    scale = 10 ** rng.uniform(-2, 0)            # include nearly-twin types
    base = rng.dirichlet(np.ones(ny), size=(nt, 1))
    f = (1 - scale) * np.repeat(base, k, axis=1) + scale * rng.dirichlet(np.ones(ny), size=(nt, k))
    P, Q, F = p.tolist(), indep(q.tolist(), nt), f.tolist()
    finest = tuple(range(k))
    for A in range(k):
        for B in range(A):
            lab = list(range(k)); lab[A] = lab[B]
            c = canon(lab)
            d = [value(P, Q, F, finest, n) - value(P, Q, F, c, n) for n in (1, 2, 3)]
            delta2 = np.einsum("t,ty->y", p, (f[:, A, :] - f[:, B, :]) ** 2)
            bound = 0.5 * (q[A] * q[B] / (q[A] + q[B])) ** 2 * float((delta2 ** 2).sum())
            pairs += 1
            viol += d[0] < bound - 1e-13
            if bound > 0 and d[0] / bound < worst_ratio:
                worst_ratio, tightest = d[0] / bound, {"deficit_n1": d[0], "bound": bound}
            nonmono += not (d[0] <= d[1] + 1e-12 and d[1] <= d[2] + 1e-12)
json.dump({"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001", "merged_pairs_checked": pairs,
           "bound_violations": int(viol), "smallest_deficit_to_bound_ratio": worst_ratio, "tightest_case": tightest,
           "pairs_with_deficit_not_increasing_over_n_1_2_3": int(nonmono)}, sys.stdout, indent=1)
