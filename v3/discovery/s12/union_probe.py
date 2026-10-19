"""Codex (GPT-6), DEVELOPMENT finite joint-adequacy screen; stdlib only."""
import hashlib
import itertools
import json
import random
import time
from pathlib import Path


def envelope(source, worlds, q, scopes):
    tables = [(q | j, {x & (q | j) for x in source}) for j in scopes]
    return {x for x in worlds if all(x & mask in vals for mask, vals in tables)}


def project(source, mask):
    return {x & mask for x in source}


def main():
    started = time.perf_counter()
    rng = random.Random(3441)
    counts = dict(panels=0, conditional_projections=0, strictly_larger_panels=0,
                  extra_joint_worlds=0, outside_global_union_worlds=0)
    for n in range(3, 6):
        worlds = set(range(1 << n))
        for _ in range(30):
            branches = [set(rng.sample(sorted(worlds), rng.randint(1, len(worlds))))
                        for _ in range(rng.randint(2, 4))]
            qbits = rng.sample(range(n), rng.randint(0, min(3, n)))
            q = sum(1 << i for i in qbits)
            scopes = [sum(1 << i for i in rng.sample(range(n), rng.randint(1, 2)))
                      for _ in range(rng.randint(1, 4))]
            union = set().union(*branches)
            joint = envelope(union, worlds, q, scopes)
            one = set().union(*(envelope(b, worlds, q, scopes) for b in branches))
            assert union <= one <= joint
            counts['panels'] += 1
            counts['strictly_larger_panels'] += bool(joint - one)
            counts['extra_joint_worlds'] += len(joint - one)
            counts['outside_global_union_worlds'] += len(joint - union)
            for receipt in itertools.product((-1, 0, 1), repeat=len(qbits)):
                compatible = lambda x: all(v == -1 or ((x >> i) & 1) == v
                                           for i, v in zip(qbits, receipt))
                actual = {x for x in joint if compatible(x)}
                retained = [{x for x in b if compatible(x)} for b in branches]
                merged = set().union(*retained)
                assert bool(actual) == bool(merged)
                for j in scopes:
                    assert project(actual, j) == project(merged, j)
                    counts['conditional_projections'] += 1
    worlds = set(range(16))
    f1 = {x for x in worlds if not x & 1 or (x & 2 and not x & 4 and x & 8)}
    f2 = {x for x in worlds if not x & 1 or (not x & 2 and x & 4 and x & 8)}
    joint = envelope(f1 | f2, worlds, 1, [2, 4, 8])
    one = envelope(f1, worlds, 1, [2, 4, 8]) | envelope(f2, worlds, 1, [2, 4, 8])
    assert len(joint) == 12 and len(one) == 10 and 15 in joint - one
    assert 15 not in envelope(f1 | f2, worlds, 1, [6, 8])
    assert project({x for x in f1 | f2 if x & 1}, 8) == {8}
    out = dict(contributor='Codex (GPT-6)', classification='DEVELOPMENT',
               status='PASS', seed=3441, counts=counts,
               example=dict(joint_worlds=12, one_branch_worlds=10,
                            actual=15, pair_scope_excludes_actual=True),
               elapsed_seconds=time.perf_counter()-started,
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               scope='Finite semantic checks; no end-to-end service or coverage calibration.')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
