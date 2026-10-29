"""Finite DEVELOPMENT screen, independent of LP and range implementations."""
import gzip
import hashlib
import itertools
import json
import math
import platform
import sys
import time
import traceback
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def hereditary_families(k):
    families = []
    for encoded in range(1 << (1 << k)):
        good = True
        for subset in range(1 << k):
            if not (encoded >> subset) & 1:
                continue
            for j in range(k):
                if subset >> j & 1 and not (encoded >> (subset ^ (1 << j))) & 1:
                    good = False
                    break
            if not good:
                break
        if good:
            families.append(frozenset(s for s in range(1 << k) if encoded >> s & 1))
    return families


def partitions(k, n):
    answer = []
    for assignment in itertools.product(range(n), repeat=k):
        masks = [0] * n
        for j, i in enumerate(assignment):
            masks[i] |= 1 << j
        answer.append(tuple(masks))
    return answer


def bound(k, n):
    q, r = divmod(k, n)
    return math.factorial(k) // (math.factorial(q + 1) ** r * math.factorial(q) ** (n - r))


def first_fit(order, families):
    masks = [0] * len(families)
    for j in order:
        for i, family in enumerate(families):
            enlarged = masks[i] | (1 << j)
            if enlarged in family:
                masks[i] = enlarged
                break
        else:
            return None
    return tuple(masks)


def inspect(k, families, candidates):
    n = len(families)
    feasible = {p for p in candidates if all(s in family for s, family in zip(p, families))}
    edges = {}
    terminals = []
    for p in feasible:
        neighbours = []
        lower = False
        for i, subset in enumerate(p):
            for j in range(k):
                bit = 1 << j
                if not subset & bit:
                    continue
                for destination in range(n):
                    if destination == i:
                        continue
                    next_p = list(p)
                    next_p[i] ^= bit
                    next_p[destination] |= bit
                    next_p = tuple(next_p)
                    if next_p in feasible:
                        neighbours.append(next_p)
                        lower |= destination < i
        edges[p] = neighbours
        if not lower:
            terminals.append(p)
    unseen = set(feasible)
    components = 0
    while unseen:
        components += 1
        todo = [unseen.pop()]
        while todo:
            p = todo.pop()
            for other in edges[p]:
                if other in unseen:
                    unseen.remove(other)
                    todo.append(other)
    weighted = 0
    for p in terminals:
        weighted += math.prod(math.factorial(s.bit_count()) for s in p)
        order = [j for s in p for j in range(k) if s >> j & 1]
        assert first_fit(order, families) == p, ('first fit', k, families, p)
    maximum = bound(k, n)
    assert components <= len(terminals) <= maximum, ('count', k, families)
    assert weighted <= math.factorial(k), ('weight', k, families)
    return dict(vertices=len(feasible), components=components, terminals=len(terminals),
                weight=weighted, factorial=math.factorial(k), bound=maximum)


def main():
    result_path = HERE / 'component_result.json'
    records_path = HERE / 'component_records.jsonl.gz'
    failure_path = HERE / 'component_failure.json'
    for p in [result_path, records_path, failure_path]:
        if p.exists():
            raise RuntimeError(f'Refusing to replace exposed output: {p.name}')
    freeze = json.loads((HERE / 'component_freeze.json').read_text(encoding='utf-8'))
    for name, digest in freeze['sha256'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, name
    began = time.monotonic_ns()
    count = 0
    panels = []
    cases_digest = hashlib.sha256()
    try:
        with gzip.GzipFile(filename=str(records_path), mode='wb', mtime=0) as output:
            for k, n in [(3, 3), (4, 2)]:
                families = hereditary_families(k)
                assert len(families) == {3: 20, 4: 168}[k]
                candidates = partitions(k, n)
                histogram = Counter()
                panel_count = 0
                for family_ids in itertools.product(range(len(families)), repeat=n):
                    if time.monotonic_ns() - began > 120_000_000_000:
                        raise TimeoutError('Prospective 120-second run cap reached')
                    selected = [families[i] for i in family_ids]
                    row = dict(k=k, n=n, families=list(family_ids),
                               **inspect(k, selected, candidates))
                    encoded = (json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n').encode()
                    output.write(encoded)
                    cases_digest.update(encoded)
                    histogram[row['components']] += 1
                    count += 1
                    panel_count += 1
                panels.append(dict(k=k, n=n, cases=panel_count,
                                   component_histogram=dict(sorted(histogram.items()))))
            fixtures = []
            for k, n in [(0, 1), (1, 3), (3, 3), (4, 3), (6, 3), (6, 4), (7, 2)]:
                q, r = divmod(k, n)
                capacities = [q + (i < r) for i in range(n)]
                families = [frozenset(s for s in range(1 << k) if s.bit_count() <= size)
                            for size in capacities]
                row = dict(k=k, n=n, capacities=capacities,
                           **inspect(k, families, partitions(k, n)))
                assert row['components'] == row['terminals'] == row['vertices'] == bound(k, n)
                assert row['weight'] == math.factorial(k)
                fixtures.append(row)
        result = dict(status='PASS', scope='finite development; no independent confirmation',
                      cases=count, panels=panels, fixtures=fixtures,
                      uncompressed_records_sha256=cases_digest.hexdigest(),
                      records_sha256=hashlib.sha256(records_path.read_bytes()).hexdigest(),
                      runtime_ns=time.monotonic_ns() - began, python=sys.version,
                      platform=platform.platform(), freeze=freeze)
        result_path.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(dict(status='PASS', cases=count, fixtures=len(fixtures),
                              runtime_ns=result['runtime_ns'], panels=panels)))
    except BaseException:
        failure_path.write_text(json.dumps(dict(status='FAIL', completed_cases=count,
                                                traceback=traceback.format_exc()), indent=2) + '\n',
                                encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
