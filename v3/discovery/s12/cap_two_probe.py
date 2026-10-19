"""Codex (GPT-6), s12 DEVELOPMENT cap-two interface reduction screen.

Compare unrestricted private-program invoices with coordinate recursions.
Expected costs use unnormalized integer prior mass for exact arithmetic.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys
import time
from parity_price_probe import all_invoice_functions, partitions

HERE = Path(__file__).resolve().parent


def solvers(fees, overhead, bank, ones, weights):
    n = len(fees)
    splits = [sum(1 << x for x in range(1 << n) if x & (1 << i))
              for i in range(n)]
    marker = [min(c for j, c in enumerate(fees) if j != i) for i in range(n)]
    stats = dict(private_states=0, private_choices=0,
                 reduced_states=0, reduced_choices=0)

    @lru_cache(None)
    def mass(w):
        return sum(weight for x, weight in enumerate(weights) if w & (1 << x))

    def terminal(w):
        return not (w & ones) or (w & ones) == w

    @lru_cache(None)
    def oracle(w):
        if terminal(w):
            return (0, 0)
        stats['private_states'] += 1
        worst, expected_mass = float('inf'), float('inf')
        for program in bank:
            groups = [(cost, w & s) for cost, s in program if w & s]
            if len(groups) < 2:
                continue
            stats['private_choices'] += 1
            children = [(c, s, oracle(s)) for c, s in groups]
            worst = min(worst, max(c + overhead + v[0] for c, s, v in children))
            expected_mass = min(expected_mass, sum(
                (c + overhead) * mass(s) + v[1] for c, s, v in children))
        assert worst < float('inf')
        return worst, expected_mass

    @lru_cache(None)
    def reduced(w):
        if terminal(w):
            return (0, 0, 0)
        stats['reduced_states'] += 1
        worst, expected_mass, depth = float('inf'), float('inf'), float('inf')
        for i, mask in enumerate(splits):
            w1, w0 = w & mask, w & ~mask
            if not w0 or not w1:
                continue
            stats['reduced_choices'] += 1
            a, b = reduced(w0), reduced(w1)
            low, high = sorted((a[0], b[0]))
            worst = min(worst, fees[i] + overhead + max(high, low + marker[i]))
            expected_mass = min(expected_mass,
                (fees[i] + overhead) * mass(w) + marker[i] * min(mass(w0), mass(w1))
                + a[1] + b[1])
            depth = min(depth, 1 + max(a[2], b[2]))
        return worst, expected_mass, depth

    return oracle, reduced, stats


def main():
    began = time.perf_counter_ns()
    totals = dict(worst_comparisons=0, expected_comparisons=0,
                  depth_bound_comparisons=0, private_states=0, private_choices=0,
                  reduced_states=0, reduced_choices=0)
    panels = []
    for fees in [(1, 1, 1), (1, 2, 7), (1, 1, 100)]:
        bank = partitions(all_invoice_functions(fees, 2))
        panels.append(dict(fees=fees, private_invoice_functions=len(bank)))
        for overhead in [0, 3]:
            for weights in [(1,) * 8, (1, 3, 2, 11, 7, 4, 19, 5)]:
                for ones in range(256):
                    oracle, reduced, stats = solvers(fees, overhead, bank, ones, weights)
                    for w in range(1, 256):
                        actual, predicted = oracle(w), reduced(w)
                        assert actual == predicted[:2], (fees, overhead, weights, ones, w,
                                                         actual, predicted)
                        totals['worst_comparisons'] += 1
                        totals['expected_comparisons'] += 1
                        if fees == (1, 1, 1) and overhead == 0 and predicted[2]:
                            depth = predicted[2]
                            assert depth + 1 <= actual[0] <= 2 * depth
                            totals['depth_bound_comparisons'] += 1
                    for key, value in stats.items():
                        totals[key] += value
    result = dict(status='PASS', contributor='Codex (GPT-6)', scope='DEVELOPMENT',
                  python=sys.version, elapsed_ns=time.perf_counter_ns() - began,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependency_sha256=hashlib.sha256((HERE / 'parity_price_probe.py').read_bytes()).hexdigest(),
                  totals=totals, panels=panels,
                  limitations='Finite three-bit check; exact rational weighted expectations. '
                  'No measured application or end-to-end computation advantage.')
    (HERE / 'cap_two_probe.json').write_bytes((json.dumps(result, indent=2) + '\n').encode())
    print(json.dumps({k: result[k] for k in ('status', 'elapsed_ns', 'totals', 'panels')}, indent=2))


if __name__ == '__main__':
    main()
