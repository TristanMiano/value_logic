"""Exact conditional coherent-center search; finite development evidence only."""
from fractions import Fraction as Q
from itertools import combinations
from v2.verification.c4_price_revision import equal_price_geometry


def solve(rows, values):
    n = len(values)
    a = [list(map(Q, row))+[Q(value)] for row, value in zip(rows, values)]
    for col in range(n):
        selected = next((i for i in range(col, n) if a[i][col]), None)
        if selected is None:
            return None
        a[col], a[selected] = a[selected], a[col]
        divisor = a[col][col]
        a[col] = [x/divisor for x in a[col]]
        for i in range(n):
            if i != col and a[i][col]:
                factor = a[i][col]
                a[i] = [x-factor*y for x, y in zip(a[i], a[col])]
    return tuple(row[-1] for row in a)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def feasible_center(g, f, b, lows, highs, radius):
    n = len(g)
    constraints = [(tuple(-int(i == j) for i in range(n)), Q(0)) for j in range(n)]
    for row, low, high in zip(f[1:], lows, highs):
        constraints.extend([(row, low+radius), (tuple(-x for x in row), radius-high)])
    for active in combinations(constraints, n-2):
        rows = [(1,)*n, g]+[row for row, _ in active]
        values = [1, b]+[value for _, value in active]
        point = solve(rows, values)
        if point is not None and all(dot(row, point) <= value for row, value in constraints):
            return point
    return None


if __name__ == '__main__':
    count = 0
    for k in range(3, 7):
        for m in (Q(0), Q(1, 10), Q(4)):
            g, f = equal_price_geometry(k, m)
            for a in range(k):
                b = (g[a]+g[a+1])/2
                vertices = []
                for i, j in combinations(range(k+1), 2):
                    if g[i] <= b <= g[j]:
                        left = (g[j]-b)/(g[j]-g[i])
                        vertices.append(tuple(left*row[i]+(1-left)*row[j] for row in f[1:]))
                lows = tuple(min(v[r] for v in vertices) for r in range(k-1))
                highs = tuple(max(v[r] for v in vertices) for r in range(k-1))
                radius = max(u-l for l, u in zip(lows, highs))/2
                center = feasible_center(g, f, b, lows, highs, radius)
                count += 1
                print('fiber', k, m, b, 'radius', radius, 'center', center, flush=True)
                if center is None:
                    print('STRICT GAP; exact vertex exhaustion. Evaluated:', count, flush=True)
                    raise SystemExit
    print('No coherence penalty in', count, 'exact fibers. No universal claim.', flush=True)
