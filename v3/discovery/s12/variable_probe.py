"""s12 DEVELOPMENT variable-invoice construction. Codex (GPT-6).

Exact execution over small full cubes; bounded unrestricted expected oracle.
All costs in the oracle are integer quarter-units, not floating approximations.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys
import time
from parity_price_probe import all_invoice_functions, partitions

HERE = Path(__file__).resolve().parent


def prefix_run(n, cap, world):
    unknown = list(range(n))
    public = {}
    purchases = episodes = markers = 0
    while unknown:
        m = min(len(unknown), cap - 1)
        data = unknown[:m]
        private_purchases = []
        for i in data:
            private_purchases.append(i)
            if not ((world >> i) & 1):
                break
        else:
            marker = next(i for i in range(n) if i not in data)
            private_purchases.append(marker)
            markers += 1
        assert len(set(private_purchases)) == len(private_purchases) <= cap
        invoice = len(private_purchases)
        learned = min(invoice, m)
        for j, i in enumerate(data[:learned]):
            public[i] = int(invoice > m or j < invoice - 1)
        unknown = unknown[learned:]
        purchases += invoice
        episodes += 1
    assert sum(bit << i for i, bit in public.items()) == world
    assert purchases == n + markers
    return purchases, episodes


def recurrence(n, cap):
    r, e = [F(0)], [F(0)]
    for k in range(1, n + 1):
        m = min(k, cap - 1)
        r.append(sum(F(1, 2**j) * r[k-j] for j in range(1, m+1))
                 + F(1, 2**m) * (1 + r[k-m]))
        e.append(1 + sum(F(1, 2**j) * e[k-j] for j in range(1, m+1))
                 + F(1, 2**m) * e[k-m])
        assert e[k] == F(k, 2) + r[k]
        if cap == 3:
            assert r[k] == F(k, 6) + F(2, 9) * (1 - F(-1, 2)**k)
    return r[n], e[n]


class StateCap(Exception):
    pass


def expected_oracle(n, cap, fee_quarters, full_vector, state_cap=20000):
    bank = partitions(all_invoice_functions((1,) * n, cap))
    ones = sum(1 << x for x in range(1 << n) if x.bit_count() % 2)
    stats = dict(states=0, program_choices=0, programs=len(bank))

    @lru_cache(None)
    def value(w):
        done = w.bit_count() == 1 if full_vector else (not w & ones or w & ones == w)
        if done:
            return 0
        stats['states'] += 1
        if stats['states'] > state_cap:
            raise StateCap
        best = None
        for program in bank:
            groups = [(cost, w & s) for cost, s in program if w & s]
            if len(groups) < 2:
                continue
            stats['program_choices'] += 1
            total = sum((4 * c + fee_quarters) * s.bit_count() + value(s)
                        for c, s in groups)
            best = total if best is None else min(best, total)
        assert best is not None
        return best
    try:
        answer = F(value((1 << (1 << n)) - 1), 4 * (1 << n))
        return dict(status='exact', value=str(answer), stats=stats)
    except StateCap:
        return dict(status='state_cap', cap=state_cap, stats=stats)


def main():
    start = time.perf_counter_ns()
    world_checks = formula_checks = 0
    examples = []
    for n in range(2, 12):
        for cap in range(2, n + 1):
            outcomes = [prefix_run(n, cap, world) for world in range(1 << n)]
            world_checks += len(outcomes)
            r, e = recurrence(n, cap)
            assert F(sum(p for p, _ in outcomes), len(outcomes)) == n + r
            assert F(sum(a for _, a in outcomes), len(outcomes)) == e
            d = cap - 1
            for f in map(F, [0, F(1, 4), F(1, 2), 1, 2]):
                maximum = max(p + f * a for p, a in outcomes)
                predicted = n + 1 + f*n + ((n-1)//d) * max(0, 1 - f*(d-1))
                assert maximum == predicted, (n, cap, f, maximum, predicted)
                formula_checks += 1
            if (n, cap) in [(3, 3), (4, 3), (10, 3), (10, 10)]:
                examples.append(dict(n=n, cap=cap, prefix_mean=str(n+r),
                                     fixed_parity_blocks_mean=str(F(n) + F((n+d-1)//d, 2)),
                                     prefix_episodes=str(e), prefix_worst=n+(n+d-1)//d))
    oracle_rows = []
    for n, cap in [(3, 2), (3, 3), (4, 3)]:
        for fee_quarters in [0, 1, 2, 4, 8]:
            r, e = recurrence(n, cap)
            upper = n + r + F(fee_quarters, 4)*e
            for full_vector in [False, True]:
                row = expected_oracle(n, cap, fee_quarters, full_vector)
                row.update(n=n, cap=cap, overhead=str(F(fee_quarters, 4)),
                           target='full_vector' if full_vector else 'parity',
                           prefix_mean=str(upper))
                if row['status'] == 'exact':
                    assert F(row['value']) <= upper
                    if n == 3 and cap == 3 and fee_quarters == 0:
                        assert F(row['value']) == F(15, 4)
                oracle_rows.append(row)
    result = dict(status='PASS', contributor='Codex (GPT-6)', scope='DEVELOPMENT',
                  python=sys.version, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependency_sha256=hashlib.sha256((HERE/'parity_price_probe.py').read_bytes()).hexdigest(),
                  elapsed_ns=time.perf_counter_ns()-start, world_checks=world_checks,
                  hard_cost_formula_checks=formula_checks, examples=examples,
                  oracle=oracle_rows, limitations='Finite screens and constructed prior; no general expected-optimality or empirical task gain.')
    (HERE/'variable_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps({k: result[k] for k in ('status','elapsed_ns','world_checks',
                                             'hard_cost_formula_checks','examples','oracle')}, indent=2))


if __name__ == '__main__':
    main()
