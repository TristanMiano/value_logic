"""Frozen small rational probe for relative_demo.md; ordinary vertex control."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import time

start = time.perf_counter_ns()
counts = dict(line_pairs=0, feasible_intersections=0)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def vertices(q, tau):
    lines = [(a, F(1)) for a in q]
    lines += [(tuple(-x for x in a), tau) for a in q]
    found = set()
    for (a, b), (c, d) in combinations(lines, 2):
        counts['line_pairs'] += 1
        det = a[0]*c[1]-a[1]*c[0]
        if not det:
            continue
        r = ((b*c[1]-a[1]*d)/det, (a[0]*d-b*c[0])/det)
        vals = [dot(r, x) for x in q]
        if all(-tau <= v <= 1 for v in vals) and max(vals) == 1:
            counts['feasible_intersections'] += 1
            found.add(r)
    return sorted(found)


def mapped(a, x):
    return tuple(dot(row, x) for row in a)


def strings(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, dict):
        return {k: strings(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)):
        return [strings(x) for x in v]
    return v


q = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(-1))]
sharp = vertices(q, F(1, 2))
expected = sorted([(F(1), F(-1, 2)), (F(-1, 2), F(1)),
                   (F(-1, 2), F(-1, 2))])
assert sharp == expected
assert all(sum(r[j] for r in sharp) == 0 for j in range(2))
assert vertices(q, F(49, 100)) == []

xi = (F(7, 8), F(1, 16))
p = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
q2 = [tuple(a-b for a, b in zip(xi, x)) for x in p]
c = tuple(sum(x[j] for x in q2)/3 for j in range(2))
for i, a in enumerate(q2):
    reflected = tuple(c[j]-(a[j]-c[j])/2 for j in range(2))
    other_mean = tuple(sum(q2[k][j] for k in range(3) if k != i)/2
                       for j in range(2))
    assert reflected == other_mean
tau = F(1, 4)
h = vertices(q2, tau)
assert h
v = tuple(2*x for x in c)
bound = min(dot(r, v) for r in h)
assert bound > tau
assert min(dot(r, c) for r in h) >= (1-2*tau)/3
for x in p:
    direction = tuple(a-b for a, b in zip(x, xi))
    assert min(dot(r, direction) for r in h) <= tau

a = [(F(2), F(1)), (F(1), F(1))]
ainvt = [(F(1), F(-1)), (F(-1), F(2))]
transformed = vertices([mapped(a, x) for x in q2], tau)
assert transformed == sorted(mapped(ainvt, r) for r in h)
assert min(dot(r, mapped(a, v)) for r in transformed) == bound

diamond = [(F(1), F(0)), (F(-1), F(0)),
           (F(0), F(1)), (F(0), F(-1))]
symmetric = vertices(diamond, F(1))
assert len(symmetric) == 4
assert all(sum(r[j] for r in symmetric) == 0 for j in range(2))
assert vertices(diamond, F(99, 100)) == []

one_reward = F(5, 9)
one_tau = F(1, 5)
one_boundary = F(4, 5) + one_tau/one_reward
assert one_boundary == F(29, 25)
assert (F(6, 5)-F(4, 5))*one_reward > one_tau
assert dot((one_reward,), (F(9, 5),)) == 1
assert -one_tau <= dot((one_reward,), (F(-1, 5),)) <= 1

source = Path(__file__)
result = dict(status='PASS', contributor='Codex (GPT-6)',
              scope='Finite arithmetic; ordinary vertex enumeration; same-model',
              python=platform.python_version(), source_sha256=hashlib.sha256(
                  source.read_bytes()).hexdigest(),
              elapsed_ns=time.perf_counter_ns()-start,
              counts=counts, sharp_triangle_rewards=sharp,
              interior_demo=dict(point=xi, contrast_center=c, tau=tau,
                                 rewards=h, proposed_direction=v,
                                 worst_normalized_advantage=bound),
              symmetric_rewards=symmetric, one_dimensional_boundary=one_boundary,
              affine_covariance=True)
source.with_name('demo_result.json').write_text(
    json.dumps(strings(result), indent=2)+'\n', encoding='utf-8')
print(json.dumps(strings(result)))
