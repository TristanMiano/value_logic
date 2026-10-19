"""Structurally bounded DEVELOPMENT extension; no old artifact is overwritten."""
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys
import time
from parity_price_probe import all_invoice_functions, partitions

HERE = Path(__file__).resolve().parent


class Budget(Exception):
    pass


def panel(bank, full):
    begin = time.perf_counter_ns()
    stats = dict(states=0, program_choices=0, programs=len(bank))
    ones = sum(1 << x for x in range(32) if x.bit_count() % 2)
    reason = ''
    @lru_cache(None)
    def value(w):
        done = w.bit_count() == 1 if full else (not w & ones or w & ones == w)
        if done:
            return 0
        stats['states'] += 1
        if stats['states'] > 225000:
            raise Budget('state_cap')
        if stats['states'] % 256 == 0 and time.perf_counter_ns()-begin > 150_000_000_000:
            raise Budget('time_cap')
        if stats['states'] % 32768 == 0:
            print(json.dumps(dict(target='vector' if full else 'parity', progress=stats)), flush=True)
        best = None
        for program in bank:
            groups = [(c, w & s) for c, s in program if w & s]
            if len(groups) < 2:
                continue
            stats['program_choices'] += 1
            total = sum(c*s.bit_count()+value(s) for c, s in groups)
            best = total if best is None else min(best, total)
        assert best is not None
        return best
    try:
        answer = str(Fraction(value((1 << 32)-1), 32))
        status = 'exact'
    except Budget as error:
        answer, status = None, str(error)
    return dict(target='full_vector' if full else 'parity', status=status, value=answer,
                stats=stats, state_cap=225000, time_cap_ns=150_000_000_000,
                elapsed_ns=time.perf_counter_ns()-begin, prefix_mean='95/16')


def main():
    begin = time.perf_counter_ns()
    bank = partitions(all_invoice_functions((1,)*5, 3))
    rows = [panel(bank, False)]
    if rows[0]['status'] == 'exact':
        rows.append(panel(bank, True))
    result = dict(status='COMPLETED', scope='DEVELOPMENT', contributor='Codex (GPT-6)',
                  n=5, episode_cap=3, overhead=0, python=sys.version, panels=rows,
                  elapsed_ns=time.perf_counter_ns()-begin,
                  hashes={name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                          for name in ['prefix_complete.py', 'parity_price_probe.py']},
                  limitation='One finite extension justified by a reachable-source bound; '
                             'no independent confirmation or all-size optimality.')
    (HERE/'prefix_complete.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
