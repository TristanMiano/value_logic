"""Independent P3-06 checks of native-cost normalization and stake obstruction.

Development evidence only. No output-transport comparison, P3-07 policy or
principal research-time credit. Contributor: ChatGPT (GPT-6 Astra Pro).
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import importlib.util
import json
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'v3/checks/06_defensive_forecasting.py'


def run():
    spec = importlib.util.spec_from_file_location('p306_native_stake_target', SOURCE)
    target = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = target
    spec.loader.exec_module(target)
    checks = 0

    def check(statement, message):
        nonlocal checks
        checks += 1
        if not statement:
            raise AssertionError(message)

    def upper_power_two(value):
        # Exact integer comparison; no floating logarithm is used.
        value = max(F(1), value)
        exponent = max(0, value.numerator.bit_length()-value.denominator.bit_length())
        result = 1 << exponent
        if result*value.denominator < value.numerator:
            result <<= 1
        check(result >= value and result < 2*value, 'Exact power-of-two envelope.')
        return F(result)

    def odd_part(n):
        while n % 2 == 0:
            n //= 2
        return n

    alpha, beta, gamma = F(2, 3), F(3, 5), F(5, 7)
    names, forecasts = ('zero', 'half', 'one'), {'zero': 0, 'half': F(1, 2), 'one': 1}
    norm_constant = 3*alpha*alpha+beta*beta+gamma*gamma
    traces = []
    for outcomes in product((0, 1), repeat=6):
        base = target.Forecaster(names, bins=2, alpha=alpha, beta=beta,
                                 decision_features=True, gamma=gamma)
        shifted = target.Forecaster(names, bins=2, alpha=alpha, beta=beta,
                                    decision_features=True, gamma=gamma)
        native_mix, native_actions = F(0), [F(0), F(0)]
        original_offset, sum_m2, native_slack = F(0), F(0), F(0)
        trace = []
        for t, y in enumerate(outcomes, 1):
            diameter = F(t*t, 3)
            stake = upper_power_two(diameter)
            eta = target.dyadic_eta(t)
            rows = ((F(0), diameter/2), (diameter/2, F(0)))
            common = (F(t*t, 7), -F((t+2)**3, 7))
            changed = tuple(tuple(row[z]+common[z] for z in (0, 1)) for row in rows)
            normalized = tuple(tuple(x/stake for x in row) for row in rows)
            normalized_changed = tuple(tuple(x/stake for x in row) for row in changed)
            for row, norm_row in zip(changed, normalized_changed):
                for x, nx in zip(row, norm_row):
                    check(odd_part(x.denominator) == odd_part(nx.denominator),
                          'Normalization introduces no fresh odd denominator factor.')
            pred = base.issue(str(t), forecasts, stake, tolerance=F(1, 256),
                              actions=target.ActionTable(normalized, eta))
            other = shifted.issue(str(t), forecasts, stake, tolerance=F(1, 256),
                                  actions=target.ActionTable(normalized_changed, eta))
            check((pred.probability, pred.features, pred.score, pred.allowance,
                   pred.action_one_probability, pred.bisections)
                  == (other.probability, other.features, other.score, other.allowance,
                      other.action_one_probability, other.bisections),
                  'Outcome-dependent common offsets leave forecasting dynamics unchanged.')
            p, s = pred.probability, pred.action_one_probability
            b0, b1 = rows[0][0], rows[1][0]
            d0, d1 = rows[0][1]-b0, rows[1][1]-b1
            delta = b1-b0+(d1-d0)*p
            expected_s = min(F(1), max(F(0), F(1, 2)-delta/(2*stake*eta)))
            mean_slope = d0+s*(d1-d0)
            check(s == expected_s and pred.features[-2:]
                  == (gamma*(mean_slope-d0), gamma*(mean_slope-d1)),
                  'Native smooth action and residual-coordinate identity.')
            phi2 = sum((x*x for x in pred.features), F(0))
            check(phi2 <= stake*stake*norm_constant, 'Unbounded-stake feature norm envelope.')
            native_mix += (1-s)*rows[0][y]+s*rows[1][y]
            for i in (0, 1):
                native_actions[i] += rows[i][y]
            original_offset += common[y]
            sum_m2 += stake*stake
            native_slack += stake*eta/8
            base.reveal(str(t), y, scope=base.settings.scope)
            shifted.reveal(str(t), y, scope=shifted.settings.scope)
            acc, changed_acc = base.accumulator, shifted.accumulator
            check(acc.mixed_action_loss == native_mix and acc.action_losses == tuple(native_actions),
                  'Weighted normalized costs equal original native costs exactly.')
            check(changed_acc.mixed_action_loss == native_mix+original_offset
                  and changed_acc.action_losses == tuple(x+original_offset for x in native_actions),
                  'Common offsets change absolute totals but cancel regret.')
            check(acc.residual == changed_acc.residual and acc.bound == changed_acc.bound,
                  'Common-offset potential invariance.')
            check(acc.smoothing_slack == native_slack, 'Native smoothing slack.')
            check(acc.bound <= norm_constant*sum_m2/4+acc.allowance,
                  'Native accumulated potential envelope.')
            for i in (0, 1):
                excess = native_mix-native_actions[i]-native_slack
                check(excess <= 0 or gamma*gamma*excess*excess <= acc.bound,
                      'Native fixed-action regret certificate.')
            trace.append({'t': t, 'diameter': str(diameter), 'stake': str(stake),
                          'p': str(p), 's': str(s), 'native_mix': str(native_mix),
                          'native_action_losses': list(map(str, native_actions)),
                          'native_slack': str(native_slack), 'bound_squared': str(acc.bound)})
        traces.append({'outcomes': outcomes, 'trace': trace})

    # All four-step reports in this rational grid, including the threshold tie.
    geometric = []
    for ratio in (F(9, 2), F(6), F(8)):
        minimum_ratio = None
        sequences = 0
        for ps in product((F(0), F(1, 4), F(1, 2), F(3, 4), F(1)), repeat=4):
            total = own = F(0)
            expert = [F(0), F(0)]
            for t, p in enumerate(ps, 1):
                previous_total = total
                weight = ratio**t
                y = int(p < F(1, 2))
                total += weight
                own += weight*(y-p)**2
                expert[0] += weight*y
                expert[1] += weight*(1-y)
                regret = own-min(expert)
                check(own >= total/4 and min(expert) <= previous_total,
                      'Geometric-adversary component lower bounds.')
                check(previous_total*ratio < total, 'Latest geometric weight dominance.')
                check(regret >= total*(ratio-4)/(4*ratio), 'Sharpened geometric lower bound.')
                if ratio > 5:
                    check(regret >= total*(ratio-5)/(4*ratio), 'Original conservative lower bound.')
                value = regret/total
                minimum_ratio = value if minimum_ratio is None else min(minimum_ratio, value)
            sequences += 1
        geometric.append({'r': str(ratio), 'sequences': sequences,
                          'proved_lower_bound': str((ratio-4)/(4*ratio)),
                          'minimum_observed_regret_ratio': str(minimum_ratio)})

    dense, sparse = [], []
    for power in (0, 1, 2, 3):
        for horizon in (32, 128, 256):
            stakes = [upper_power_two(F(t**power)) for t in range(1, horizon+1)]
            total = sum(stakes, F(0))
            squares = sum((x*x for x in stakes), F(0))
            check(horizon*squares <= 4*(power+1)**2*total*total,
                  'Dense polynomial dispersion envelope.')
            dense.append({'power': power, 'rounds': horizon,
                          'sum_squares_over_total_squared': str(squares/(total*total))})
    spike_times = [2**(2**k) for k in range(5)]
    for horizon in spike_times[1:]:
        active = [t for t in spike_times if t <= horizon]
        total = horizon+sum(t*t-1 for t in active)
        squares = horizon+sum(t**4-1 for t in active)
        sparse.append({'rounds': horizon, 'largest_stake': horizon*horizon,
                       'sum_squares_over_total_squared': str(F(squares, total*total))})
    check(F(squares, total*total) > F(999, 1000), 'Sparse polynomial-envelope obstruction observed.')
    return {'status': 'PASS', 'assertions': checks, 'production_version': target.VERSION,
            'normalization_binary_sequences': len(traces), 'normalization_traces': traces,
            'geometric_lower_bound': geometric, 'dense_polynomial_examples': dense,
            'sparse_polynomial_examples': sparse,
            'scope': 'Exact finite development checks; asymptotic claims use the separate written proof.'}


if __name__ == '__main__':
    start_utc = datetime.now(timezone.utc).isoformat()
    start_ns = time.monotonic_ns()
    reviewed = sha256(SOURCE.read_bytes()).hexdigest()
    try:
        result = run()
    except Exception:
        result = {'status': 'FAIL', 'traceback': traceback.format_exc()}
    after = sha256(SOURCE.read_bytes()).hexdigest()
    if reviewed != after:
        result['status'] = 'SOURCE_CHANGED_DURING_REVIEW'
    result.update(start_utc=start_utc, end_utc=datetime.now(timezone.utc).isoformat(),
                  execution_ns=time.monotonic_ns()-start_ns,
                  source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  reviewed_production_sha256=reviewed, production_sha256_after=after,
                  principal_research_time_credit_ns=0, subagent_research_effort='unmeasured')
    out = Path(__file__).with_name('unbounded_stakes_review_result.json')
    if out.exists():
        raise SystemExit('Refusing to overwrite review evidence.')
    out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result.get(k) for k in ('status', 'assertions', 'production_version',
                                              'reviewed_production_sha256', 'execution_ns')}))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
