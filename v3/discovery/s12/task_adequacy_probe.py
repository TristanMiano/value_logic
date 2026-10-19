"""Small DEVELOPMENT check of the task/observation source envelope."""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent


def value(x, scope):
    return tuple(x >> i & 1 for i in scope)


def projection(worlds, scope):
    return {value(x, scope) for x in worlds}


def restrict(worlds, receipt):
    return {x for x in worlds if all((x >> i & 1) == b for i, b in receipt.items())}


def main():
    begin = time.perf_counter_ns()
    rng = random.Random(121933)
    counts = dict(sources=0, binary_sources=0, conditional_projections=0,
                  enlarged_sources=0, added_worlds=0, outside_witnesses=0,
                  conflicting_full_receipts=0, unsafe_outside_actions=0,
                  binary_representations=0)
    for n in range(2, 7):
        universe = set(range(1 << n))
        small_scopes = [(i,) for i in range(n)]+list(combinations(range(n), 2))
        for rep in range(30):
            binary = rep % 2 == 0
            if binary:
                witness = rng.randrange(1 << n)
                clauses = []
                for _ in range(n*3):
                    scope = rng.choice(small_scopes)
                    forbidden = tuple(rng.randrange(2) for _ in scope)
                    if value(witness, scope) != forbidden:
                        clauses.append((scope, forbidden))
                f = {x for x in universe if all(value(x, s) != a for s, a in clauses)}
                counts['binary_sources'] += 1
            else:
                f = {x for x in universe if rng.random() < .35}
                f.add(rng.randrange(1 << n))
            q = tuple(sorted(rng.sample(range(n), rng.randrange(min(3, n)+1))))
            scopes = [tuple(sorted(rng.sample(range(n), rng.randrange(1, min(3, n)+1))))
                      for _ in range(3)]
            joint = {tuple(sorted(set(q) | set(j))) for j in scopes}
            tables = {s: projection(f, s) for s in joint}
            h = {x for x in universe if all(value(x, s) in table for s, table in tables.items())}
            assert f <= h
            counts['enlarged_sources'] += (f != h)
            counts['added_worlds'] += len(h-f)
            for pattern in product((-1, 0, 1), repeat=len(q)):
                receipt = {i: b for i, b in zip(q, pattern) if b != -1}
                fp, hp = restrict(f, receipt), restrict(h, receipt)
                assert bool(fp) == bool(hp)
                for j in scopes:
                    assert projection(fp, j) == projection(hp, j)
                    counts['conditional_projections'] += 1
            for x in universe-h:
                receipt = dict(zip(q, value(x, q)))
                fp = restrict(f, receipt)
                if not fp:
                    counts['conflicting_full_receipts'] += 1
                else:
                    scope = next(j for j in scopes if value(x, j) not in projection(fp, j))
                    # Target is OR of these coordinates; choose the local mask
                    # that sends actual x to its all-zero falsifying assignment.
                    mask = sum((x >> i & 1) << i for i in scope)
                    assert all(any((w ^ mask) >> i & 1 for i in scope) for w in fp)
                    assert not any((x ^ mask) >> i & 1 for i in scope)
                    counts['unsafe_outside_actions'] += 1
                counts['outside_witnesses'] += 1
            if binary:
                retained = set()
                for s in joint:
                    for k in (1, 2):
                        retained.update(combinations(s, k))
                constraints = [(s, projection(f, s)) for s in retained]
                h2 = {x for x in universe if all(value(x, s) in table for s, table in constraints)}
                assert h == h2
                counts['binary_representations'] += 1
            counts['sources'] += 1
    # q->z->a may be globally false while its observed/acted-on interface is right.
    f = {x for x in range(8) if (not x & 1 or x & 2) and (not x & 2 or x & 4)}
    h = {x for x in range(8) if not x & 1 or x & 4}
    assert f == {0, 4, 6, 7} and h == {0, 2, 4, 5, 6, 7}
    actual = 5
    assert actual not in f and actual in h
    assert all(not ((w ^ 4) & 4) for w in restrict(f, {0: 1}))
    assert not ((actual ^ 4) & 4)
    result = dict(status='PASS', scope='DEVELOPMENT', contributor='Codex (GPT-6)',
                  python=sys.version, counts=counts, worked_example=dict(
                      source_worlds=sorted(f), envelope_worlds=sorted(h), actual=actual),
                  elapsed_ns=time.perf_counter_ns()-begin,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  limitation='Synthetic exact semantic checks; no model calibration, '
                             'application audit saving or independent confirmation.')
    (HERE/'task_adequacy_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
