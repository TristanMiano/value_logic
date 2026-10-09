"""Bounded rational witness check, ChatGPT (GPT-6 Astra Pro), 2026-10-09.

No forecasting selection routine or transcendental approximation is imported.
The infinite sums and BRIA nonimplication are proved in 06_bria_boundary.md.
This probe preserves the declared 127-round fixture and refuses replacement.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def main():
    target = HERE / 'result.json'
    if target.exists():
        raise SystemExit('Preserve the existing development result.')
    start, utc = time.perf_counter_ns(), datetime.now(timezone.utc).isoformat()
    plan = json.loads((HERE / 'plan.json').read_text())
    checks = Counter()

    def check(value, name):
        checks[name] += 1
        if not value:
            raise AssertionError(name)

    rates = tuple(map(F, plan['rates']))
    total_e = total_e2 = overestimate = F(0)
    losses = [F(0), F(0), F(0)]
    exponents = {(j, r): F(0) for j in range(7) for r in rates}
    records = []
    for t in range(1, plan['horizon'] + 1):
        k = t.bit_length()  # ceil(log2(t+1)) for integer t >= 1.
        eps = F(1, 1 << (2 * k + 3))
        p, y = 1 - eps, F(1)
        total_e += eps
        total_e2 += eps * eps
        check(total_e <= F(1, 16) and total_e2 <= F(1, 896), 'prefix geometric bounds')
        check(p.denominator.bit_length() == 2 * k + 4, 'report denominator bits')
        check(p.numerator.bit_length() <= 2 * k + 3, 'report numerator bits')
        if t + 1 == 1 << k:
            check(total_e == F(1 - F(1, 1 << k), 16), 'exact first moment at block end')
            check(total_e2 == F(1 - F(1, 1 << (3 * k)), 896), 'exact second moment at block end')
        costs_p = ((1 - p) / 2, 1 - p)
        actual_costs = ((1 - y) / 2, 1 - y)
        estimate = 1 - costs_p[0]
        overestimate += estimate - 1
        check(costs_p[0] <= costs_p[1], 'constant action is forecast optimal')
        check(actual_costs == (0, 0), 'zero realized fixed and oracle regret')
        check(estimate < 1 and F(0) <= estimate <= 1, 'strict outpromise in reward range')
        check(1 - 1 == 0, 'always matched kept-promise record')
        check(overestimate == -total_e / 2 and overestimate < 0, 'no overestimation identity')
        qs = (F(1), F(1, 2), F(t % 2))
        for i, q in enumerate(qs):
            losses[i] += (q - y) ** 2
            regret = total_e2 - losses[i]
            check(regret <= total_e2, 'regret to each supplied expert')
            check(2 * regret <= F(1, 448), 'unit-cap expert exponent bound')
        coeffs = tuple(max(F(0), 1 - abs(4 * p - j)) for j in range(5))
        coeffs += (F(1, 2), F((-1) ** t * (t + 1)))
        check(sum(coeffs[:5]) == 1, 'tent partition')
        for j, a in enumerate(coeffs):
            for rate in rates:
                z = rate * a
                inc = z * eps - z * z / 8
                check(inc == 2 * eps * eps - (z - 4 * eps) ** 2 / 8,
                      'local completed square identity')
                check(inc <= 2 * eps * eps, 'local centered exponent bound')
                exponents[j, rate] += inc
                check(exponents[j, rate] <= 2 * total_e2 <= F(1, 448),
                      'cumulative centered exponent bound')
        records.append({'t': t, 'k': k, 'epsilon': str(eps), 'forecast': str(p),
            'reward_estimate': str(estimate), 'outcome': 1, 'actual_reward': 1,
            'action': 0, 'hypothesis_action': 0, 'promise': 1,
            'matched_test_increment': 0, 'sum_error': str(total_e),
            'sum_squared_error': str(total_e2)})
    result = {'status': 'PASS', 'stage': plan['stage'], 'started_utc': utc,
        'elapsed_wall_ns': time.perf_counter_ns() - start,
        'checks': dict(checks), 'assertions': sum(checks.values()),
        'horizon': plan['horizon'], 'infinite_error_bound': '1/16',
        'infinite_squared_error_bound': '1/896', 'exponent_upper': '1/448',
        'capital_upper_rational': '448/447', 'records': records,
        'capital_scope': 'Actual-path monitor bound; no issued allowance or algorithm trajectory claim.',
        'source_sha256': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                          for name in ('plan.json', 'probe.py')}}
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'horizon', 'assertions', 'elapsed_wall_ns')}))


if __name__ == '__main__':
    main()
