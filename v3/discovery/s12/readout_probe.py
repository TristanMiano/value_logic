"""Codex (GPT-6), s12 DEVELOPMENT: general readouts and affine sources.

All partitions of the positive counts 1..H are enumerated at n=3. Monotone
partitions test the derived theorem; nonmonotone partitions are exploratory.
Actual costs stay in a per-world remaining-budget vector after each invoice.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys
import time
from parity_price_probe import all_invoice_functions, affine_sources, equivalent_characters

HERE = Path(__file__).resolve().parent


def partitions(length, prefix=(0,)):
    if len(prefix) == length:
        yield prefix
    else:
        for label in range(max(prefix) + 2):
            yield from partitions(length, prefix + (label,))


def cover(k, jumps, overhead):
    if not k:
        return 0
    if not jumps:
        return None
    values = [0]
    for size in range(1, k + 1):
        values.append(min(b + overhead + values[max(0, size - b + 1)] for b in jumps))
    return values[k]


def oracle(n, functions, readout, overhead, target):
    labels = tuple((x & target).bit_count() % 2 for x in range(1 << n))
    programs = [(cost, tuple(readout[c] for c in cost)) for cost in functions]
    stats = dict(states=0, choices=0)

    @lru_cache(None)
    def feasible(budgets):
        worlds = [x for x, b in enumerate(budgets) if b >= 0]
        if len({labels[x] for x in worlds}) <= 1:
            return True
        stats['states'] += 1
        for cost, observed in programs:
            if any(cost[x] + overhead > budgets[x] for x in worlds):
                continue
            groups = {}
            for x in worlds:
                groups.setdefault(observed[x], []).append(x)
            if len(groups) <= 1:
                continue
            stats['choices'] += 1
            possible = True
            for group in groups.values():
                remaining = [-1] * (1 << n)
                for x in group:
                    remaining[x] = budgets[x] - cost[x] - overhead
                if not feasible(tuple(remaining)):
                    possible = False
                    break
            if possible:
                return True
        return False

    def solve(source, upper):
        worlds = [x for x in range(1 << n) if source >> x & 1]
        if len({labels[x] for x in worlds}) <= 1:
            return 0
        if upper is None:
            assert all(len({o[x] for x in worlds}) == 1 for _, o in programs)
            return None
        def budgets(amount):
            return tuple(amount if source >> x & 1 else -1 for x in range(1 << n))
        assert feasible(budgets(upper)), (readout, source, target, upper)
        low, high = -1, upper
        while high - low > 1:
            middle = (low + high) // 2
            if feasible(budgets(middle)):
                high = middle
            else:
                low = middle
        return high
    return solve, stats


def main():
    started = time.perf_counter_ns()
    n = 3
    sources = affine_sources(n)
    totals = dict(monotone_comparisons=0, nonmonotone_comparisons=0, states=0, choices=0)
    panels, counterexamples = [], []
    for cap in [2, 3]:
        functions = sorted(all_invoice_functions((1,) * n, cap))
        for positive in partitions(cap):
            readout = (0,) + positive
            monotone = all(a <= b for a, b in zip(positive, positive[1:]))
            jumps = [b for b in range(2, cap + 1) if readout[b] != readout[b - 1]]
            panel = dict(cap=cap, readout=readout, monotone=monotone, jumps=jumps,
                         programs=len(functions), full_cube=[])
            for overhead in [0, 1, 5]:
                full = []
                for target in range(1 << n):
                    solve, stats = oracle(n, functions, readout, overhead, target)
                    for source in sources:
                        weight = min(t.bit_count() for t in equivalent_characters(n, source, target))
                        expected = cover(weight, jumps, overhead)
                        actual = solve(source, expected)
                        key = 'monotone_comparisons' if monotone else 'nonmonotone_comparisons'
                        totals[key] += 1
                        if monotone:
                            assert actual == expected, (cap, readout, overhead, source, target, actual, expected)
                        elif actual != expected:
                            counterexamples.append(dict(cap=cap, readout=readout, overhead=overhead,
                                                        source=source, target=target, actual=actual,
                                                        jump_cover=expected))
                        if source == (1 << (1 << n)) - 1:
                            full.append(actual)
                    for key, value in stats.items():
                        totals[key] += value
                panel['full_cube'].append(dict(overhead=overhead, values_by_target=full))
            panels.append(panel)
    result = dict(status='PASS', contributor='Codex (GPT-6)', scope='DEVELOPMENT',
                  python=sys.version, elapsed_ns=time.perf_counter_ns()-started,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependency_sha256=hashlib.sha256((HERE/'parity_price_probe.py').read_bytes()).hexdigest(),
                  totals=totals, panels=panels, nonmonotone_counterexamples=counterexamples,
                  limitations='All n=3 affine sources, count partitions and listed overheads only. '
                  'Nonmonotone readout is exploratory; finite agreement would not establish its theorem.')
    (HERE/'readout_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps({k: result[k] for k in ('status', 'elapsed_ns', 'totals')}, indent=2))
    print('Nonmonotone counterexamples:', len(counterexamples))


if __name__ == '__main__':
    main()
