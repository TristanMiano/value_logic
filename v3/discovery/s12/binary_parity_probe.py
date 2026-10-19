"""Finite DEVELOPMENT checks of the binary-source adapter, not independent review."""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys
import time
from reachable_probe import binary_sources

HERE = Path(__file__).resolve().parent


def rank(rows):
    basis = {}
    for row in rows:
        while row:
            p = row.bit_length()-1
            if p in basis:
                row ^= basis[p]
            else:
                basis[p] = row
                break
    return len(basis)


def check_sources():
    panels = []
    for n in range(1, 5):
        checks = 0
        sources = binary_sources(n)
        for w in sources:
            if not w:
                continue
            worlds = [x for x in range(1 << n) if w >> x & 1]
            a = worlds[0]
            rows = [x ^ a for x in worlds]
            signatures = [sum(((x >> i) & 1) << j for j, x in enumerate(rows))
                          for i in range(n)]
            blocks = {}
            for i, signature in enumerate(signatures):
                if signature:
                    blocks[signature] = blocks.get(signature, 0) | (1 << i)
            assert rank(rows) == len(blocks), (n, w, blocks)
            for s in range(1 << n):
                truth = {(x & s).bit_count() % 2 for x in worlds}
                predicted_constant = all((b & s).bit_count() % 2 == 0
                                         for b in blocks.values())
                assert (len(truth) == 1) == predicted_constant, (n, w, s)
                if predicted_constant:
                    assert truth == {(a & s).bit_count() % 2}
                checks += 1
        panels.append(dict(n=n, nonempty_sources=len(sources)-1, parity_checks=checks))
    return panels


def chain_panel():
    # Enumerate threshold choices and both invoice orientations, not the
    # Fibonacci capacity recursion. Offset changes parity values, not costs.
    @lru_cache(None)
    def oracle(k):
        if k == 1:
            return 0
        return min(max(c0+oracle(split), c1+oracle(k-split))
                   for split in range(1, k) for c0, c1 in [(1, 2), (2, 1)])

    @lru_cache(None)
    def balanced(k):
        if k == 1:
            return 0
        a, b = balanced(k//2), balanced(k-k//2)
        return min(max(1+a, 2+b), max(2+a, 1+b))

    capacities = [1, 1]
    while capacities[-1] < 128:
        capacities.append(capacities[-1]+capacities[-2])
    rows = []
    for k in range(1, 129):
        predicted = next(b for b, leaves in enumerate(capacities) if leaves >= k)
        assert oracle(k) == predicted, (k, oracle(k), predicted)
        if k in [2, 3, 4, 8, 16, 32, 64, 128]:
            rows.append(dict(positions=k, optimal_invoice_fee=oracle(k),
                             balanced_invoice_fee=balanced(k)))
    return dict(comparisons=128, rows=rows,
                limitation='Initial source, controller computation and resets excluded; '
                           'ordinary optimal unequal-cost search ties.')


def main():
    started = time.perf_counter_ns()
    result = dict(status='PASS', scope='DEVELOPMENT', contributor='Codex (GPT-6)',
                  python=sys.version, sources=check_sources(), chain=chain_panel())
    result['elapsed_ns'] = time.perf_counter_ns()-started
    result['hashes'] = {p: hashlib.sha256((HERE/p).read_bytes()).hexdigest()
                        for p in ['binary_parity_probe.py', 'reachable_probe.py',
                                  'parity_price_probe.py']}
    (HERE/'binary_parity_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
