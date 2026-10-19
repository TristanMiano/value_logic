"""Codex (GPT-6), s12 DEVELOPMENT randomized invoice controller.

DP selects declared block/prefix modes. A separate execution simulator decodes
only invoices and used random bits, then checks every small input/random tape.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def scale(p, a):
    return tuple(p*x for x in a)


def total(metrics, overhead, coin_price):
    queries, coins, episodes = metrics
    return queries + coin_price*coins + overhead*episodes


def compile_policy(n, cap, overhead, coin_price):
    values = [(F(0), F(0), F(0))]
    policy = [None]
    choices = 0
    for k in range(1, n+1):
        candidates = []
        accumulator = (F(0), F(0), F(0))
        probability = F(1)
        for m in range(1, min(k, cap-1)+1):
            probability /= 2
            accumulator = add(accumulator, scale(probability, values[k-m]))
            block = add((F(m)+F(1, 2), F(1), F(1)), values[k-m])
            mu = 2*(1-probability)
            prefix = add((mu+probability, mu, F(1)),
                         add(accumulator, scale(probability, values[k-m])))
            candidates.extend([(block, ('B', m)), (prefix, ('P', m))])
            choices += 2
        metrics, action = min(candidates, key=lambda z:
            (total(z[0], overhead, coin_price), z[0][1], z[0][2], z[0][0], z[1][0], -z[1][1]))
        values.append(metrics)
        policy.append(action)
    return values, policy, choices


def execute(n, cap, policy, hidden, tape):
    pending = list(range(n))
    output_parity = 0
    queries = coins = episodes = 0
    while pending:
        kind, m = policy[len(pending)]
        data = pending[:m]
        marker = next(i for i in range(n) if i not in data)
        assert m+1 <= cap and marker not in data
        episodes += 1
        if kind == 'B':
            private_parity = sum((hidden >> i) & 1 for i in data) % 2
            public_bit = (tape >> coins) & 1
            coins += 1
            invoice = m + (private_parity ^ public_bit)
            # The public decoder does not use private_parity.
            output_parity ^= (invoice-m) ^ public_bit
            pending = pending[m:]
        else:
            used_bits = []
            invoice = None
            for j, i in enumerate(data, 1):
                bit = (tape >> coins) & 1
                coins += 1
                used_bits.append(bit)
                transformed = ((hidden >> i) & 1) ^ bit
                if transformed == 0:
                    invoice = j
                    break
            if invoice is None:
                invoice = m+1
            learned = min(invoice, m)
            public_transformed = ([1]*(learned-1)+[0]) if invoice <= m else [1]*m
            assert len(used_bits) == learned
            for bit, transformed in zip(used_bits, public_transformed):
                output_parity ^= bit ^ transformed
            pending = pending[learned:]
        queries += invoice
    assert coins <= n
    assert output_parity == hidden.bit_count() % 2
    return queries, coins, episodes


def metrics_json(metrics, overhead, coin_price):
    return dict(queries=str(metrics[0]), random_choices=str(metrics[1]), episodes=str(metrics[2]),
                declared_bill=str(total(metrics, overhead, coin_price)))


def main():
    started = time.perf_counter_ns()
    panels, large = [], []
    executions = conditional_means = candidates = 0
    for n, cap in [(3, 3), (4, 3), (5, 4)]:
        for overhead in [F(0), F(1, 4), F(1)]:
            for coin_price in [F(0), F(1, 8), F(1, 4)]:
                values, policy, count = compile_policy(n, cap, overhead, coin_price)
                candidates += count
                worst = F(0)
                for hidden in range(1 << n):
                    sums = [0, 0, 0]
                    for tape in range(1 << n):
                        measured = execute(n, cap, policy, hidden, tape)
                        for i, value in enumerate(measured):
                            sums[i] += value
                        worst = max(worst, total(measured, overhead, coin_price))
                        executions += 1
                    actual = tuple(F(s, 1 << n) for s in sums)
                    assert actual == values[n], (n, cap, overhead, coin_price, hidden, actual, values[n])
                    conditional_means += 1
                blocks = (n+cap-2)//(cap-1)
                fixed = (F(n)+F(blocks, 2), F(blocks), F(blocks))
                assert total(values[n], overhead, coin_price) <= total(fixed, overhead, coin_price)
                panels.append(dict(n=n, cap=cap, overhead=str(overhead), coin_price=str(coin_price),
                                   hybrid=metrics_json(values[n], overhead, coin_price),
                                   fixed=metrics_json(fixed, overhead, coin_price),
                                   exhaustive_worst_declared_bill=str(worst), policy=policy))
    for cap in [3, 4, 8]:
        for overhead, coin_price in [(F(0),F(0)),(F(1,4),F(0)),(F(0),F(1,8)),(F(1),F(1,4))]:
            n = 100
            values, policy, count = compile_policy(n, cap, overhead, coin_price)
            candidates += count
            blocks = (n+cap-2)//(cap-1)
            fixed = (F(n)+F(blocks, 2), F(blocks), F(blocks))
            assert total(values[n], overhead, coin_price) <= total(fixed, overhead, coin_price)
            large.append(dict(n=n, cap=cap, overhead=str(overhead), coin_price=str(coin_price),
                              hybrid=metrics_json(values[n], overhead, coin_price),
                              fixed=metrics_json(fixed, overhead, coin_price),
                              improvement_fraction=str(1-total(values[n],overhead,coin_price)/total(fixed,overhead,coin_price)),
                              first_action=policy[n]))
    result = dict(status='PASS', contributor='Codex (GPT-6)', scope='DEVELOPMENT', python=sys.version,
                  elapsed_ns=time.perf_counter_ns()-started,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  totals=dict(executions=executions, every_input_mean_checks=conditional_means,
                              dp_candidate_evaluations=candidates, small_panels=len(panels), large_dp_panels=len(large)),
                  small=panels, large=large,
                  limitations='All small input/tape pairs only at named n/caps/prices. Large panels are exact '
                  'DP calculations in the restricted hybrid class, not unrestricted oracles. '
                  'Declared bill prices queries, episodes and random choices, not all controller work.')
    (HERE/'hybrid_probe.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:result[k] for k in ('status','elapsed_ns','totals')},indent=2))
    for panel in large:
        print(json.dumps(dict(cap=panel['cap'], overhead=panel['overhead'], coin_price=panel['coin_price'],
                              improvement_percent=float(F(panel['improvement_fraction'])*100),
                              first_action=panel['first_action'])))


if __name__ == '__main__':
    main()
