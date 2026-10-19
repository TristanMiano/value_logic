"""Codex (GPT-6), s12 DEVELOPMENT stronger randomized invoice controls.

New source and outputs preserve the earlier hybrid probe unchanged.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time
from variable_probe import prefix_run, recurrence

HERE = Path(__file__).resolve().parent


def fixed_run(n, cap, hidden, bit):
    parity = queries = episodes = 0
    for start in range(0, n, cap-1):
        block = list(range(start, min(n, start+cap-1)))
        marker = next(i for i in range(n) if i not in block)
        assert marker not in block and len(block)+1 <= cap
        private = sum((hidden >> i) & 1 for i in block) % 2
        invoice = len(block) + (private ^ bit)
        parity ^= (invoice-len(block)) ^ bit
        queries += invoice
        episodes += 1
    assert parity == hidden.bit_count() % 2
    return queries, episodes


def main():
    started = time.perf_counter_ns()
    prefix_executions = fixed_executions = conditional_checks = 0
    for n in range(2, 8):
        masks = [seed | ((seed.bit_count() % 2) << (n-1)) for seed in range(1 << (n-1))]
        for cap in range(2, n+1):
            surcharge, episodes = recurrence(n, cap)
            q = (n+cap-2)//(cap-1)
            for hidden in range(1 << n):
                outcomes = [prefix_run(n, cap, hidden ^ mask) for mask in masks]
                actual = tuple(F(sum(row[i] for row in outcomes), len(outcomes)) for i in range(2))
                assert actual == (n+surcharge, episodes), (n, cap, hidden, actual)
                prefix_executions += len(outcomes)
                conditional_checks += 1
                fixed = [fixed_run(n, cap, hidden, bit) for bit in [0, 1]]
                actual_fixed = tuple(F(sum(row[i] for row in fixed), 2) for i in range(2))
                assert actual_fixed == (F(n)+F(q, 2), F(q))
                fixed_executions += 2
                conditional_checks += 1
    source_result = json.loads((HERE/'hybrid_probe.json').read_text())
    comparisons = []
    erased = 0
    for panel in source_result['large']:
        n, cap = panel['n'], panel['cap']
        f, gamma = F(panel['overhead']), F(panel['coin_price'])
        q = (n+cap-2)//(cap-1)
        surcharge, episodes = recurrence(n, cap)
        bills = dict(shared_fixed=F(n)+F(q, 2)+q*f+gamma,
                     even_prefix=n+surcharge+f*episodes+(n-1)*gamma,
                     fresh_hybrid=F(panel['hybrid']['declared_bill']))
        choice = min(bills, key=lambda name: bills[name])
        gain = 1-bills[choice]/bills['shared_fixed']
        old_gain = F(panel['improvement_fraction'])
        lost = old_gain > 0 and gain == 0
        erased += lost
        comparisons.append(dict(n=n, cap=cap, overhead=str(f), coin_price=str(gamma),
                                bills={k:str(v) for k,v in bills.items()}, selected=choice,
                                gain_against_shared_fixed=str(gain),
                                earlier_fresh_coin_gain=str(old_gain), earlier_gain_erased=lost))
    result = dict(status='PASS', contributor='Codex (GPT-6)', scope='DEVELOPMENT',
                  python=sys.version, elapsed_ns=time.perf_counter_ns()-started,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependencies={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                                for name in ['variable_probe.py','parity_price_probe.py','hybrid_probe.json']},
                  totals=dict(prefix_input_mask_executions=prefix_executions,
                              fixed_input_coin_executions=fixed_executions,
                              every_input_mean_checks=conditional_checks,
                              large_comparisons=len(comparisons), earlier_positive_gains_erased=erased),
                  large=comparisons,
                  limitations='Finite every-input checks n=2..7. Large comparisons use exact recurrences '
                  'and the frozen restricted DP; no all-in runtime claim or unrestricted optimum.')
    (HERE/'shared_coin_probe.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:result[k] for k in ('status','elapsed_ns','totals')},indent=2))
    for panel in comparisons:
        print(json.dumps(dict(cap=panel['cap'], overhead=panel['overhead'], coin_price=panel['coin_price'],
                              selected=panel['selected'], improvement_percent=float(F(panel['gain_against_shared_fixed'])*100),
                              earlier_gain_erased=panel['earlier_gain_erased'])))


if __name__ == '__main__':
    main()
