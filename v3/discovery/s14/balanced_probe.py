"""Exact small balanced-edit and SDP-necessity screen; Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import random
import time

OUT = Path(__file__).with_suffix('.json')
assert not OUT.exists(), 'Preserve executed evidence; use a fresh replay directory.'


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def transpose(a):
    return list(map(list, zip(*a)))


def mv(a, x):
    return [dot(row, x) for row in a]


def sub(a, b):
    return [x-y for x, y in zip(a, b)]


def solve(a, v):
    n = len(a)
    b = [list(row)+[v[i]] for i, row in enumerate(a)]
    for j in range(n):
        k = next(k for k in range(j, n) if b[k][j])
        b[j], b[k] = b[k], b[j]
        scale = b[j][j]
        b[j] = [x/scale for x in b[j]]
        for i in range(n):
            if i != j:
                scale = b[i][j]
                b[i] = [x-scale*y for x, y in zip(b[i], b[j])]
    x = [row[-1] for row in b]
    assert mv(a, x) == v
    return x


def receipt(a, v):
    operator = [[F(i == j)+dot(row, other) for j, other in enumerate(a)]
                for i, row in enumerate(a)]
    w = solve(operator, v)
    z = mv(transpose(a), w)
    s, m = dot(v, w), dot(w, w)
    assert s-m == dot(z, z)
    return s, m, w, z


def bounds(s, m, e2):
    return s*s/(s+e2*m), (F(1) if s == 1 else
                           1-(1-s)**2/(1-s+e2*(s-m)))


def psd2(a):
    assert a[0][1] == a[1][0]
    assert a[0][0] >= 0 and a[1][1] >= 0
    assert a[0][0]*a[1][1] >= a[0][1]**2


def interpolate_necessary(x, y, u, v, cap2):
    for xi, yi in zip(x, y):
        for uj, vj in zip(u, v):
            assert dot(xi, vj) == dot(yi, uj)
    psd2([[cap2*dot(xi, xj)-dot(yi, yj)
           for xj, yj in zip(x, y)] for xi, yi in zip(x, y)])
    psd2([[cap2*dot(ui, uj)-dot(vi, vj)
           for uj, vj in zip(u, v)] for ui, vi in zip(u, v)])


started = datetime.now(timezone.utc).isoformat()
clock = time.perf_counter_ns()
rng = random.Random(1430001)
panels = interpolation_panels = 0
for rows, columns in ((1, 1), (2, 1), (2, 2), (2, 3), (3, 2)):
    for case in range(12):
        a = [[F(rng.randrange(-5, 6), 3) for j in range(columns)]
             for i in range(rows)]
        v = [F(i == 0) for i in range(rows)]
        left = [F(i == case % rows) for i in range(rows)]
        right = [F(j == case % columns) for j in range(columns)]
        if rows > 1 and case % 2:
            left = [F(3, 5), F(4, 5)] + [F(0)]*(rows-2)
        if columns > 1 and case % 3:
            right = [F(5, 13), F(12, 13)] + [F(0)]*(columns-2)
        s, m, w, z = receipt(a, v)
        for e in (F(0), F(1, 10), F(1), F(3)):
            h = [[e*x*y for y in right] for x in left]
            plus = [[x+y for x, y in zip(ar, hr)] for ar, hr in zip(a, h)]
            minus = [[x-y for x, y in zip(ar, hr)] for ar, hr in zip(a, h)]
            tp, mp, u, p = receipt(plus, v)
            tm = receipt(minus, v)[0]
            lower, upper = bounds(s, m, e*e)
            assert lower <= (tp+tm)/2 <= upper
            ap, c = mv(a, p), mv(transpose(a), u)
            b, d = sub(sub(v, u), ap), sub(p, c)
            assert b == mv(h, p) and d == mv(transpose(h), u)
            assert dot(p, d) == dot(b, u)
            assert dot(b, b) <= e*e*dot(p, p)
            assert dot(d, d) <= e*e*dot(u, u)
            cap2 = sum(dot(row, row) for row in a)
            interpolate_necessary([z, p], [sub(v, w), ap], [w, u], [z, c], cap2)
            panels += 1
            interpolation_panels += 1

upper_equalities = lower_equalities = 0
for x in (F(1, 4), F(1), F(3), F(10)):
    for y in (F(0), F(1, 2), F(2)):
        a = [[x], [y], [F(0)]]
        v = [F(1), F(0), F(0)]
        s, m, _, _ = receipt(a, v)
        for e in (F(0), F(1, 10), F(1), F(3)):
            n = [[x], [y], [e]]
            assert receipt(n, v)[0] == bounds(s, m, e*e)[1]
            upper_equalities += 1
            old = [[x, F(0)]]
            new = [[x, e]]
            ss, mm, _, _ = receipt(old, [F(1)])
            assert receipt(new, [F(1)])[0] == bounds(ss, mm, e*e)[0]
            lower_equalities += 1

limits = []
for s, m, e in ((F(1,10),F(1,50),F(1)), (F(1,4),F(1,8),F(2)),
                (F(1,2),F(3,8),F(1,2))):
    gaps = []
    for k in (10, 100, 1000):
        q = F(1, 1+k*k)
        x = (m-s*q)/(s-q)
        weight = (s-q)/(x-q)
        assert weight*x+(1-weight)*q == s
        assert weight*x*x+(1-weight)*q*q == m
        value = weight*x/(1+e*e*x)+(1-weight)*q/(1+e*e*q)
        gap = value-bounds(s, m, e*e)[0]
        assert gap > 0
        gaps.append(gap)
    assert all(a > b for a, b in zip(gaps, gaps[1:]))
    limits.append({'s': s, 'm': m, 'e': e, 'exact_positive_gaps': gaps})

result = {
    'contributor': 'Codex (GPT-6)', 'status': 'PASS',
    'scope': 'exact tiny screens, not independent review or an SDP solver',
    'started_utc': started, 'ended_utc': datetime.now(timezone.utc).isoformat(),
    'balanced_pair_panels': panels, 'interpolation_necessity_panels': interpolation_panels,
    'upper_equality_cases': upper_equalities, 'lower_boundary_equality_cases': lower_equalities,
    'lower_limiting_sequences': limits,
    'example_balanced_interval': [F(1,11), F(2,11)],
    'example_individual_interval': [F(1,17), F(2,9)],
    'elapsed_ns': time.perf_counter_ns()-clock,
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
}
OUT.write_text(json.dumps(result, indent=2, default=str)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2, default=str))
