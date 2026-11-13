#!/usr/bin/env python3
"""Exploratory probes for the W6 terminality addendum brief (BRIEF.md).

By Claude (Fable 5.2), November 12, 2026. Planning aid; zero recurrence credit.
Not a result. Standard library only. Usage: python3 probe.py

1. Recomputes R6.12's two-state example exactly: retained behaviour far from
   the assessment of a fixed end does not depend on the end.
2. Checks R6.4 Proposition 2 on a grid: with a constant advantage, the growth
   factor falls as the revision rate rises.
3. One toy with a heritable revision rate under a permanent advantage.
"""
from fractions import Fraction as F
import math

# --- 1. R6.12, equations (8)-(11) -------------------------------------------
K = [[F(3, 5), F(2, 5)], [F(1, 10), F(3, 5)]]
h, v, lam = [F(2), F(1)], [F(1), F(2)], F(4, 5)
assert [sum(K[i][j] * h[j] for j in range(2)) for i in range(2)] == [lam * x for x in h]
assert [sum(v[i] * K[i][j] for i in range(2)) for j in range(2)] == [lam * x for x in v]
Q = [[K[i][j] * h[j] / (lam * h[i]) for j in range(2)] for i in range(2)]
assert Q == [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]


def retained_rule(u, n):
    """Next-state law among retained paths, n transitions before the end weight u."""
    hs = [u]
    for _ in range(n):
        hs.append([sum(K[i][j] * hs[-1][j] for j in range(2)) for i in range(2)])
    return [[K[i][j] * hs[n - 1][j] / hs[n][i] for j in range(2)] for i in range(2)]


print("1. distance of retained behaviour from the common pattern (max over rows)")
for u in ([F(9), F(1)], [F(1), F(9)], [F(1), F(0)], [F(0), F(1)]):
    row = []
    for n in (1, 3, 10):
        q = retained_rule(u, n)
        err = max(abs(q[i][0] - Q[i][0]) for i in range(2))
        assert err <= F(3, 4) * F(1, 2 ** n) / (1 - F(1, 2 ** n))
        row.append(f"n={n}: {float(err):.6f}")
    print("   end weight", tuple(int(x) for x in u), " ".join(row))

# --- 2. R6.4 Proposition 2 ---------------------------------------------------
R = 2.0


def growth(mu):
    a, b, c, d = 1 - mu, mu, R * mu, R * (1 - mu)  # diag(1,R) @ [[1-mu,mu],[mu,1-mu]]
    tr, det = a + d, a * d - b * c
    return (tr + math.sqrt(tr * tr - 4 * det)) / 2


grid = [k / 100 for k in range(0, 51)]
vals = [growth(m) for m in grid]
assert all(x > y for x, y in zip(vals, vals[1:]))
print(f"2. growth factor falls from {vals[0]:.4f} (never revise) to {vals[-1]:.4f} (revise at rate 1/2)")

# --- 3. heritable revision rate, permanent advantage R -----------------------
mus = [0.0, 0.001, 0.01, 0.05, 0.2]
eps = 1e-3  # chance per update of moving to a neighbouring revision rate
x = [[1 / (2 * len(mus))] * 2 for _ in mus]  # x[k] = (mass without priority, mass with)
print("3. share of the population at each revision rate", mus)
for t in range(1, 20001):
    y = []
    for k, m in enumerate(mus):
        lo, hi = x[k][0], R * x[k][1]
        y.append([lo * (1 - m) + hi * m, lo * m + hi * (1 - m)])
    z = [row[:] for row in y]
    for k in range(len(mus)):
        for d in (-1, 1):
            if 0 <= k + d < len(mus):
                for c in range(2):
                    z[k][c] -= eps * y[k][c]
                    z[k + d][c] += eps * y[k][c]
    tot = sum(map(sum, z))
    x = [[c / tot for c in row] for row in z]
    if t in (100, 1000, 20000):
        shares = " ".join(f"{sum(row):.4f}" for row in x)
        print(f"   after {t:>5} updates: {shares}   priority held by {sum(r[1] for r in x):.4f}")
