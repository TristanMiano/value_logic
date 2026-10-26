"""Frozen finite closure/receipt comparison. No external solver or arithmetic noise."""
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import hashlib
import json
import platform
import random
import time

started = time.perf_counter_ns()
stats = dict(core_cases=0, source_checks=0, target_checks=0,
             least_iterations=0, affine_cases=0, affine_selectors=0,
             separating_tests=0)
d, top = 3, 7


def points(mask):
    return tuple(x for x in range(8) if mask >> x & 1)


def closed_sources(operation, arity):
    ans = []
    for mask in range(1, 256):
        xs = points(mask)
        if all(mask >> operation(*ys) & 1
               for ys in combinations_with_replacement(xs, arity)):
            ans.append(mask)
    return ans


meet_sources = closed_sources(lambda a, b: a & b, 2)
majority_sources = closed_sources(lambda a, b, c: (a & b) | (a & c) | (b & c), 3)


def actual_core(regions, sources):
    core = 255
    compatible = 0
    for f in sources:
        stats['source_checks'] += 1
        if all(f & t for t in regions):
            compatible += 1
            core &= f
    assert compatible
    return core


def meet_predicted(regions, z):
    if z == top:
        return any(t == (1 << top) for t in regions)
    return all(any(all((x & z) == z and not(x >> j & 1) for x in points(t))
                       for t in regions)
               for j in range(d) if not(z >> j & 1))


projections = (1, 2, 4, 3, 5, 6)


def majority_predicted(regions, z):
    return all(any(all((x & j) == (z & j) for x in points(t)) for t in regions)
               for j in projections)


def least_cube(cubes):
    z = 0
    while True:
        stats['least_iterations'] += 1
        covered = 0
        for p, n in cubes:
            if z & p == z:
                covered |= n
        next_z = top ^ covered
        assert z & next_z == z
        if next_z == z:
            break
        z = next_z
    if z != top or any(p == top for p, n in cubes):
        return z
    return None


def check(regions, cubes=None):
    meet = actual_core(regions, meet_sources)
    maj = actual_core(regions, majority_sources)
    for z in range(8):
        stats['target_checks'] += 2
        assert bool(meet >> z & 1) == meet_predicted(regions, z), (regions, z, 'meet')
        assert bool(maj >> z & 1) == majority_predicted(regions, z), (regions, z, 'majority')
    if cubes is not None:
        least = least_cube(cubes)
        if meet:
            expected = top
            for x in points(meet):
                expected &= x
            assert meet >> expected & 1
            assert least == expected, (cubes, least, expected)
        else:
            assert least is None
    stats['core_cases'] += 1
    return dict(meet_core=points(meet), majority_core=points(maj))


cubes = []
for states in product((-1, 0, 1), repeat=d):
    p = sum(1 << j for j, s in enumerate(states) if s == 1)
    n = sum(1 << j for j, s in enumerate(states) if s == 0)
    t = sum(1 << x for x in range(8) if (x & p) == p and not(x & n))
    cubes.append((p, n, t))
assert len(cubes) == 27
for cube in cubes:
    check((cube[2],), (cube[:2],))
for a, b in combinations(cubes, 2):
    check((a[2], b[2]), (a[:2], b[:2]))
rng = random.Random(20261025)
for _ in range(80):
    check(tuple(rng.randrange(1, 256) for _ in range(3)))
for b in range(8):
    check((255, 1 << b), ((0, 0), (b, top ^ b)))
pair_zero = tuple(sum(1 << x for x in range(8) if not(x & pair))
                  for pair in (3, 5, 6))
majority_example = check(pair_zero, ((0, 3), (0, 5), (0, 6)))
assert majority_example['majority_core'] == (0,)


def affine_contains_zero(generators):
    base = generators[0]
    basis = {}
    for v in generators[1:]:
        v ^= base
        while v:
            pivot = v.bit_length()-1
            if pivot in basis:
                v ^= basis[pivot]
            else:
                basis[pivot] = v
                break
    v = base
    while v:
        pivot = v.bit_length()-1
        if pivot not in basis:
            return False
        v ^= basis[pivot]
    return True


def affine_contacts(clauses):
    # e0 at bit0; X_j at1+j; N_j at5+j.
    out = [(1,)]
    out += [((1 << (1+j)) ^ (1 << (5+j)),) for j in range(4)]
    for clause in clauses:
        out.append((sum(1 << (1+j) for j in clause),))
        for p, q in combinations(clause, 2):
            out.append((1 << (5+p), (1 << (5+p)) ^ (1 << (5+q))))
    assert all(len(t) == 1 or (t[0] ^ t[1]).bit_count() == 1 for t in out)
    return out


triples = tuple(combinations(range(4), 3))
affine_results = []
for mask in range(1, 16):
    clauses = tuple(triples[j] for j in range(4) if mask >> j & 1)
    sat = any(all(sum((x >> j) & 1 for j in c) == 1 for c in clauses)
              for x in range(16))
    contacts = affine_contacts(clauses)
    separators = []
    for h in range(512):
        stats['separating_tests'] += 1
        if all(any((h & x).bit_count() % 2 for x in t) for t in contacts):
            separators.append(h)
    excluding = 0
    total = 0
    for selected in product(*contacts):
        total += 1
        stats['affine_selectors'] += 1
        if not affine_contains_zero(selected):
            excluding += 1
    assert sat == bool(separators) == bool(excluding), (clauses, sat, separators, excluding)
    stats['affine_cases'] += 1
    affine_results.append(dict(clauses=clauses, satisfiable=sat,
                               separators=len(separators), selectors=total,
                               excluding_selectors=excluding))

source = Path(__file__)
result = dict(status='PASS', contributor='Codex (GPT-6)',
              python=platform.python_version(),
              source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              elapsed_ns=time.perf_counter_ns()-started, counts=stats,
              meet_sources=len(meet_sources), majority_sources=len(majority_sources),
              majority_example=majority_example, affine_results=affine_results)
source.with_name('closure_result.json').write_text(json.dumps(result, indent=2)+'\n',
                                                 encoding='utf-8')
print(json.dumps(result))
