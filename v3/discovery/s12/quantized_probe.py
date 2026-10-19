"""Codex (GPT-6), s12 DEVELOPMENT quantized public-invoice screen.

The observer sees only floor(C/Delta). Feasibility retains the remaining
budget for every possible world; C need not be constant inside a bucket.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys
import time
from parity_price_probe import all_invoice_functions

HERE = Path(__file__).resolve().parent


def exact_oracle(n, functions, delta, overhead, target):
    labels = tuple((x & target).bit_count() % 2 for x in range(1 << n))
    programs = [(cost, tuple(c // delta for c in cost)) for cost in functions]
    stats = dict(states=0, choices=0, heterogeneous_buckets=0)
    for cost, observed in programs:
        for bucket in set(observed):
            if len({cost[x] for x, o in enumerate(observed) if o == bucket}) > 1:
                stats['heterogeneous_buckets'] += 1

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
                new_budget = [-1] * (1 << n)
                for x in group:
                    new_budget[x] = budgets[x] - cost[x] - overhead
                if not feasible(tuple(new_budget)):
                    possible = False
                    break
            if possible:
                return True
        return False

    if not target:
        return 0, stats
    if all(len(set(observed)) == 1 for _, observed in programs):
        return None, stats
    # Independent baseline: encode each target bit using one visible threshold.
    high = target.bit_count() * (max(2, delta) + overhead)
    assert feasible((high,) * (1 << n))
    low = -1
    while high - low > 1:
        middle = (low + high) // 2
        if feasible((middle,) * (1 << n)):
            high = middle
        else:
            low = middle
    return high, stats


def predicted(k, cap, delta, overhead):
    if not k:
        return 0
    b = delta * (cap // delta)
    if b <= 1:
        return None
    q = (k + b - 2) // (b - 1)
    return delta * max(q, (k + q + delta - 1) // delta) + q * overhead


def main():
    start = time.perf_counter_ns()
    n = 3
    totals = dict(comparisons=0, states=0, choices=0, heterogeneous_buckets=0)
    panels = []
    for cap in [2, 3]:
        functions = sorted(all_invoice_functions((1,) * n, cap))
        for delta in [1, 2, 3, 4]:
            for overhead in [0, 1, 3]:
                values = []
                for target in range(8):
                    actual, stats = exact_oracle(n, functions, delta, overhead, target)
                    expected = predicted(target.bit_count(), cap, delta, overhead)
                    assert actual == expected, (cap, delta, overhead, target, actual, expected)
                    totals['comparisons'] += 1
                    for key, value in stats.items():
                        totals[key] += value
                    values.append(actual)
                panels.append(dict(cap=cap, delta=delta, overhead=overhead,
                                   functions=len(functions), prices_by_target_mask=values))
    result = dict(status='PASS', contributor='Codex (GPT-6)', scope='DEVELOPMENT',
                  python=sys.version, elapsed_ns=time.perf_counter_ns()-start,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependency_sha256=hashlib.sha256((HERE/'parity_price_probe.py').read_bytes()).hexdigest(),
                  totals=totals, panels=panels,
                  limitations='Three-bit finite oracle. Per-world budgets preserve hidden actual costs. '
                  'No all-size independent proof, noisy readout, unequal-price theorem or application benchmark.')
    (HERE/'quantized_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps({k: result[k] for k in ('status','elapsed_ns','totals')}, indent=2))


if __name__ == '__main__':
    main()
