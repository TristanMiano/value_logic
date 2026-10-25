"""Frozen rational segment prototype for conditional linear optimum receipts."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import random
import time

started = time.perf_counter_ns()
stats = Counter()


def dot(h, x):
    return sum(a*b for a, b in zip(h, x))


def point(segment, t):
    a, b = segment
    return tuple(x+t*(y-x) for x, y in zip(a, b))


def face(segment, old, values, h, mask):
    stats['face_regions'] += 1
    a, b = segment
    delta = tuple(y-x for x, y in zip(a, b))
    lo, hi = Q(0), Q(1)
    for j, (g, value) in enumerate(zip(old, values)):
        alpha, beta = dot(g, a), dot(g, delta)
        stats['face_constraint_tests'] += 1
        if not beta:
            if alpha < value or (mask >> j & 1 and alpha != value):
                return None
            continue
        threshold = Q(value-alpha, beta)
        if mask >> j & 1:
            lo, hi = max(lo, threshold), min(hi, threshold)
        elif beta > 0:
            lo = max(lo, threshold)
        else:
            hi = min(hi, threshold)
        if lo > hi:
            return None
    xlo, xhi = point(segment, lo), point(segment, hi)
    vlo, vhi = dot(h, xlo), dot(h, xhi)
    if vlo <= vhi:
        return vlo, vhi, lo, hi
    return vhi, vlo, hi, lo


def solve(segments, old, values, h):
    k, n = len(old), len(segments)
    full = (1 << k)-1
    cap = 1+max(abs(dot(h, endpoint)) for s in segments for endpoint in s)
    table = [[face(s, old, values, h, t) for t in range(1 << k)] for s in segments]
    lower, upper = {0: (cap, ())}, {0: (cap, ())}
    for i in range(n):
        next_l, next_u = {}, {}
        assert lower.keys() == upper.keys()
        for s in lower:
            remaining = full ^ s
            t = remaining
            while True:
                stats['dp_transitions_considered'] += 1
                f = table[i][t]
                if f is not None:
                    lv, uv, lt, ut = f
                    dest = s | t
                    cand_l = (min(lower[s][0], lv), lower[s][1]+(lt,))
                    cand_u = (min(upper[s][0], uv), upper[s][1]+(ut,))
                    if dest not in next_l or cand_l[0] < next_l[dest][0]:
                        next_l[dest] = cand_l
                    if dest not in next_u or cand_u[0] > next_u[dest][0]:
                        next_u[dest] = cand_u
                if t == 0:
                    break
                t = (t-1) & remaining
        lower, upper = next_l, next_u
        stats['dp_reached_states'] += len(lower)
    if full not in lower:
        return None
    result = lower[full], upper[full]
    for value, parameters in result:
        assert all(0 <= t <= 1 for t in parameters)
        xs = tuple(point(s, t) for s, t in zip(segments, parameters))
        assert tuple(min(dot(g, x) for x in xs) for g in old) == tuple(values)
        assert min(dot(h, x) for x in xs) == value
        stats['endpoint_witness_checks'] += 1
    return result


def enumerate_candidates(segments, old, values, h):
    candidates = []
    for a, b in segments:
        ts = {Q(0), Q(1)}
        for g, v in zip(old, values):
            aa, bb = dot(g, a), dot(g, b)
            if aa != bb:
                t = Q(v-aa, bb-aa)
                if 0 <= t <= 1:
                    ts.add(t)
        xs = [point((a, b), t) for t in sorted(ts)]
        candidates.append([x for x in xs if all(dot(g, x) >= v for g, v in zip(old, values))])
    low = high = None
    for xs in product(*candidates):
        stats['enumerated_configurations'] += 1
        if any(min(dot(g, x) for x in xs) != v for g, v in zip(old, values)):
            continue
        value = min(dot(h, x) for x in xs)
        low = value if low is None else min(low, value)
        high = value if high is None else max(high, value)
        stats['consistent_configurations'] += 1
    return None if low is None else (low, high)


def check(segments, old, values, h):
    result = solve(segments, old, values, h)
    actual = None if result is None else (result[0][0], result[1][0])
    expected = enumerate_candidates(segments, old, values, h)
    assert actual == expected, (segments, old, values, h, actual, expected)
    stats['segment_cases'] += 1
    stats['consistent_cases' if result is not None else 'inconsistent_cases'] += 1
    return result


rng = random.Random(20261025)


def direction(d):
    while True:
        h = tuple(rng.randrange(-2, 3) for _ in range(d))
        if any(h):
            return h


for case in range(200):
    d, n, k = rng.randrange(1, 5), rng.randrange(1, 6), rng.randrange(5)
    segments = tuple((tuple(Q(rng.randrange(-3, 4)) for _ in range(d)),
                      tuple(Q(rng.randrange(-3, 4)) for _ in range(d))) for _ in range(n))
    old = tuple(direction(d) for _ in range(k))
    xs = tuple(point(s, rng.choice((Q(0), Q(1, 3), Q(1, 2), Q(2, 3), Q(1)))) for s in segments)
    values = [min(dot(g, x) for x in xs) for g in old]
    if k and case % 5 == 0:
        values[0] += rng.choice((Q(-1, 2), Q(1, 2)))
    check(segments, old, values, direction(d))

example = check((((Q(-2),), (Q(0),)), ((Q(0),), (Q(2),))),
                ((1,),), (Q(0),), (-1,))
assert example[0][0] == -2 and example[1][0] == 0

formula_panel = [((1,), (-1,)), ((1, 2), (-1, 3), (-2, -3)),
                 ((1,), (2,), (3,)), ((1,), (-1, 2), (-2, 3), (-3,))]
clauses = []
for pattern in product((-1, 0, 1), repeat=3):
    clause = tuple((j+1)*v for j, v in enumerate(pattern) if v)
    if clause:
        clauses.append(clause)
formula_panel += [tuple(rng.sample(clauses, rng.randrange(1, 7))) for _ in range(20)]
for formula in formula_panel:
    k = len(formula)
    segments = []
    for var in range(1, 4):
        a = tuple(Q(int(-var not in c)) for c in formula)
        b = tuple(Q(int(var not in c)) for c in formula)
        segments.append((a, b))
    old = tuple(tuple(int(j == l) for l in range(k)) for j in range(k))
    result = solve(segments, old, (Q(0),)*k, (1,)*k)
    satisfiable = any(all(any((assignment[abs(lit)-1] == (lit > 0)) for lit in c)
                          for c in formula) for assignment in product((False, True), repeat=3))
    assert (result is not None) == satisfiable, formula
    stats['sat_adapter_cases'] += 1
    stats['sat_adapter_sat' if satisfiable else 'sat_adapter_unsat'] += 1

source = Path(__file__)
result = dict(status='PASS', contributor='Codex (GPT-6)', python=platform.python_version(),
              source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              elapsed_ns=time.perf_counter_ns()-started, counts=dict(stats),
              example=dict(lower=str(example[0][0]), upper=str(example[1][0]),
                           lower_parameters=[str(x) for x in example[0][1]],
                           upper_parameters=[str(x) for x in example[1][1]]),
              scope='Exact finite segment/DP and SAT-adapter checks; no novelty or full-cost claim')
source.with_name('attainer_result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result))
