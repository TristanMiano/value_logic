"""Frozen developmental check of fault-budget closure adapters, on exact bits."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import hashlib
import json
import platform
import random
import time

started = time.perf_counter_ns()
stats = Counter()
d = 3
points = tuple(range(1 << d))
universe = (1 << len(points))-1
members = {s: tuple(x for x in points if s >> x & 1) for s in range(universe+1)}


def closure(s, kind):
    while True:
        old = s
        xs = members[s]
        if kind == 'meet':
            for x in xs:
                for y in xs:
                    s |= 1 << (x & y)
        else:
            for x in xs:
                for y in xs:
                    for z in xs:
                        out = ((x & y) | (y & z) | (x & z)
                               if kind == 'majority' else x ^ y ^ z)
                        s |= 1 << out
        if s == old:
            return s


hulls = {kind: tuple(closure(s, kind) for s in range(universe+1))
         for kind in ('meet', 'majority', 'affine')}
closed = {kind: tuple(s for s in range(1, universe+1) if hs[s] == s)
          for kind, hs in hulls.items()}
projections = tuple(combinations(range(d), 1))+tuple(combinations(range(d), 2))


def project(x, js):
    return sum(((x >> j) & 1) << k for k, j in enumerate(js))


def predicted(contacts, b, r, kind):
    result = 0
    for z in points:
        if kind == 'meet':
            tests = [(1 << z)] if z == 7 else [
                sum(1 << x for x in points if x & z == z and not(x >> j & 1))
                for j in range(d) if not(z >> j & 1)]
        else:
            tests = [sum(1 << x for x in points if project(x, js) == project(z, js))
                     for js in projections]
        if all(b & t or sum(not(c & ~t) for c in contacts) > r for t in tests):
            result |= 1 << z
    return result


def source_core(contacts, b, r, kind):
    result = universe
    for f in closed[kind]:
        stats['source_checks'] += 1
        if not(b & ~f) and sum(not(f & t) for t in contacts) <= r:
            result &= f
    return result


rng = random.Random(20261025)
for case in range(400):
    contacts = tuple(rng.randrange(1, 256) for _ in range(rng.randrange(1, 8)))
    b = (0 if case % 3 else sum(1 << x for x in rng.sample(points, 2)))
    for r in range(len(contacts)):
        for kind in ('meet', 'majority'):
            got = predicted(contacts, b, r, kind)
            want = source_core(contacts, b, r, kind)
            assert got == want, (kind, contacts, b, r, got, want)
            stats['contact_core_cases'] += 1


def robust_cores(reports, r):
    counts = Counter(reports)
    support = sum(1 << x for x in counts)
    eligible = tuple(x for x in counts if counts[x] <= r)
    remaining = [support]
    for k in range(1, min(r, len(eligible))+1):
        for deleted in combinations(eligible, k):
            if sum(counts[x] for x in deleted) <= r:
                remaining.append(support & ~sum(1 << x for x in deleted))
    out = {}
    for kind, hs in hulls.items():
        result = universe
        for s in remaining:
            result &= hs[s]
            stats['deletion_hull_lookups'] += 1
        out[kind] = result
    return out


def affine_stream(reports, bits, r):
    banks = [dict() for _ in range(r)]
    for index, x in enumerate(reports):
        y = x | (1 << bits)
        supports = []
        for bank in banks:
            v, coeff = y, 0
            for pivot in sorted(bank, reverse=True):
                stats['stream_pivot_checks'] += 1
                if v >> pivot & 1:
                    row, support = bank[pivot]
                    v ^= row
                    coeff ^= support
            if v:
                bank[v.bit_length()-1] = (v, coeff ^ (1 << index))
                break
            supports.append(coeff)
        else:
            supports.append(1 << index)
            used = 0
            for support in supports:
                assert support and not(support & used)
                used |= support
                total = 0
                for j in range(index+1):
                    if support >> j & 1:
                        total ^= reports[j] | (1 << bits)
                        stats['certificate_row_xors'] += 1
                assert total == y and support.bit_count() % 2 == 1
            assert len(supports) == r+1
            assert used.bit_count() <= r*(bits+1)+1
            stats['stream_certificates'] += 1
            return x, index+1, supports
    return None


for size in range(2, 10):
    for reports in combinations_with_replacement(points, size):
        for r in (1, 2):
            if r >= size:
                continue
            result = robust_cores(reports, r)
            stats['full_point_cases'] += 1
            for kind, threshold in (('meet', 4*r), ('majority', 6*r), ('affine', 4*r)):
                if size > threshold:
                    assert result[kind], (kind, reports, r)
                    stats['existence_implications'] += 1
            if size > 4*r:
                cert = affine_stream(reports, d, r)
                assert cert and result['affine'] >> cert[0] & 1
                stats['stream_exact_core_comparisons'] += 1

sharp = {'meet': (7, 6, 5, 3), 'majority': (0, 7, 1, 6, 3, 4),
         'affine': (0, 1, 2, 4)}
for kind, pattern in sharp.items():
    for r in (1, 2):
        reports = tuple(x for x in pattern for _ in range(r))
        assert robust_cores(reports, r)[kind] == 0
        assert robust_cores(reports+(0,), r)[kind] != 0
        stats['sharp_boundary_cases'] += 1

pairs = tuple(combinations(range(d), 2))
b = sum(1 << x for x in (7, 6, 5, 3))
encoded = set()
for counts in product(range(4), repeat=len(pairs)):
    contacts = [1 << 7]*3
    for js, copies in zip(pairs, counts):
        contact = sum(1 << x for x in points if project(x, js) == 0)
        contacts += [contact]*copies
    answers = []
    for r in range(3):
        core = predicted(contacts, b, r, 'majority')
        assert core == source_core(contacts, b, r, 'majority')
        for js, copies in zip(pairs, counts):
            z = 7 & ~sum(1 << j for j in js)
            answer = bool(core >> z & 1)
            assert answer == (copies > r)
            answers.append(answer)
            stats['summary_answers'] += 1
    encoded.add(tuple(answers))
assert len(encoded) == 4**3

for case in range(100):
    bits = rng.randrange(4, 33)
    r = rng.randrange(0, 5)
    reports = tuple(rng.getrandbits(bits) for _ in range(r*(bits+1)+1))
    cert = affine_stream(reports, bits, r)
    assert cert and cert[1] <= r*(bits+1)+1
    stats['larger_stream_cases'] += 1

source = Path(__file__)
result = dict(status='PASS', contributor='Codex (GPT-6)', python=platform.python_version(),
              source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              elapsed_ns=time.perf_counter_ns()-started, counts=dict(stats),
              closed_source_counts={k: len(v) for k, v in closed.items()},
              scope='Finite adapter checks only; same-model DEVELOPMENT, not novelty or confirmation')
source.with_name('fault_result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result))
