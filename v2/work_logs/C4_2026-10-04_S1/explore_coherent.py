"""Development search only; floating LP findings require exact validation."""
from fractions import Fraction as Q
from itertools import combinations
from scipy.optimize import linprog
from v2.verification.c4_price_revision import equal_price_geometry

largest = (0.0, None)
count = 0
for k in range(3, 11):
    for m in (Q(0), Q(1, 10), Q(1), Q(4), Q(20)):
        g, f = equal_price_geometry(k, m)
        for a in range(k):
            for step in range(1, 5):
                b = g[a]+Q(step, 5)*(g[a+1]-g[a])
                levels = []
                for i, j in combinations(range(k+1), 2):
                    if g[i] <= b <= g[j]:
                        left = (g[j]-b)/(g[j]-g[i])
                        levels.append(tuple(left*row[i]+(1-left)*row[j] for row in f[1:]))
                lows = [min(v[r] for v in levels) for r in range(k-1)]
                highs = [max(v[r] for v in levels) for r in range(k-1)]
                unconstrained = max(u-l for l, u in zip(lows, highs))/2
                constraints, bounds = [], []
                for row, low, high in zip(f[1:], lows, highs):
                    constraints.extend([list(row)+[-1], [-x for x in row]+[-1]])
                    bounds.extend([low, -high])
                fit = linprog([0]*(k+1)+[1], A_ub=constraints, b_ub=bounds,
                              A_eq=[[1]*(k+1)+[0], list(g)+[0]], b_eq=[1, b],
                              bounds=[(0, None)]*(k+2), method='highs')
                if not fit.success:
                    raise RuntimeError(fit.message)
                count += 1
                gap = fit.fun-float(unconstrained)
                if gap > largest[0]:
                    largest = (gap, (k, str(m), str(b), str(unconstrained),
                                     fit.fun, list(fit.x), list(fit.ineqlin.marginals),
                                     list(fit.eqlin.marginals)))
                if gap > 1e-8:
                    print('STRICT_GAP', largest, flush=True)
                    print('evaluated', count, flush=True)
                    raise SystemExit
print('No gap above floating tolerance in', count, 'conditional fibers; maximum', largest)
