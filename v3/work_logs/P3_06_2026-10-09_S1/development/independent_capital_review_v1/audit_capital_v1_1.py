"""Independent exact-rational capital/enclosure audit; development only.

The reference exponential has a geometric Taylor-tail bound and exact powers
after reduction by ceil(abs(x)); it never uses production dyadic squaring.
Log upper bounds are checked by this reference exponential, not by duplicating
the logarithm implementation. Finite probes accompany a separate proof review.
"""
from dataclasses import asdict, is_dataclass
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import importlib.util
from itertools import product
import json
from math import isqrt
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source_snapshot_v1_1/06_capital_forecasting.py'
SPEC = importlib.util.spec_from_file_location('independent_capital_v11', SOURCE)
CORE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CORE
SPEC.loader.exec_module(CORE)
CHECKS = 0


def check(condition, detail):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(detail)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if is_dataclass(value):
        return encode(asdict(value))
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (set, frozenset)):
        return sorted(encode(v) for v in value)
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def fingerprint(learner):
    return hashlib.sha256(json.dumps(encode(vars(learner)), sort_keys=True).encode()).hexdigest()


@lru_cache(maxsize=8192)
def reference_exp(x, precision=112):
    """Rational interval for exp(x), with a distinct exact tail/rounding path."""
    if x == 0:
        return F(1), F(1)
    copies = max(1, -((-abs(x).numerator) // abs(x).denominator))
    z = abs(x) / copies
    target = F(1, 1 << (precision + 32 + copies.bit_length()))
    partial, term, degree = F(1), F(1), 0
    while True:
        next_term = term * z / (degree + 1)
        tail = next_term / (1 - z / (degree + 2))
        if tail <= target:
            break
        term = next_term
        partial += term
        degree += 1
    lower, upper = partial ** copies, (partial + tail) ** copies
    if x < 0:
        return 1 / upper, 1 / lower
    return lower, upper


def test_enclosures():
    xs = {F(0), F(1), F(-1), F(2), F(-2), F(3), F(8), F(-8),
          F(63, 2), F(-63, 2), F(1024), F(-1024), F(1, 1 << 100),
          -F(1, 1 << 100), F(1) - F(1, 1 << 18), F(1) + F(1, 1 << 18),
          F(2) - F(1, 1 << 18), F(2) + F(1, 1 << 18)}
    xs.update(F(n, d) for n in range(-7, 8) for d in (3, 7))
    exp_cases, max_numerator_bits, max_denominator_bits = 0, 0, 0
    for bits, x in product((8, 16, 48, 96), sorted(xs)):
        lower, upper = CORE.exp_interval(x, bits)
        ref_lower, ref_upper = reference_exp(x, bits + 80)
        check(0 <= lower <= ref_lower <= ref_upper <= upper, ('exp enclosure', x, bits))
        check((lower * (1 << bits)).denominator == (upper * (1 << bits)).denominator == 1,
              ('dyadic endpoints', x, bits))
        exp_cases += 1
        max_numerator_bits = max(max_numerator_bits, lower.numerator.bit_length(), upper.numerator.bit_length())
        max_denominator_bits = max(max_denominator_bits, lower.denominator.bit_length(), upper.denominator.bit_length())
    log_xs = (F(1), F(1) + F(1, 1 << 16), F(9, 8), F(3, 2),
              F(2) - F(1, 1 << 24), F(2), F(2) + F(1, 1 << 24),
              F(7, 3), F(4), F(31, 2), F(1 << 200))
    log_cases, greatest_reference_precision = 0, 0
    for bits, x in product((8, 16, 48, 96), log_xs):
        upper = CORE.log_upper(x, bits)
        error_budget = F(1, 1 << bits)
        precision = bits + 80
        while True:
            exp_upper_lower = reference_exp(upper, precision)[0]
            exp_lower_upper = reference_exp(upper - error_budget, precision)[1]
            if exp_upper_lower >= x and exp_lower_upper <= x:
                break
            precision *= 2
            check(precision <= 4096, ('log reference precision', x, bits))
        check(exp_upper_lower >= x, ('log upper via exp inversion', x, bits))
        check(exp_lower_upper <= x, ('log error via exp inversion', x, bits))
        log_cases += 1
        greatest_reference_precision = max(greatest_reference_precision, precision)
    return {'exp_cases': exp_cases, 'log_cases': log_cases,
            'largest_exp_endpoint_numerator_bits': max_numerator_bits,
            'largest_exp_endpoint_denominator_bits': max_denominator_bits,
            'maximum_log_reference_precision': greatest_reference_precision,
            'positive_1024_interval_bits16': CORE.exp_interval(F(1024), 16),
            'negative_1024_interval_bits16': CORE.exp_interval(F(-1024), 16)}


def require_rejection(call, learner=None):
    before = fingerprint(learner) if learner is not None else None
    try:
        call()
    except (ValueError, TypeError, AttributeError) as error:
        if learner is not None:
            check(before == fingerprint(learner), ('rejection mutated state', type(error).__name__))
        check(True, 'rejected')
        return type(error).__name__
    raise AssertionError('Malformed input or immutable assignment was accepted')


def replace_first(sequence):
    sequence[0] = F(999)


def test_inputs_and_immutability():
    count = 0
    CORE.log_upper(F(2), 16)
    CORE.log_upper(F(1), 16)
    for value, bits in ((2.0, 16), (True, 16), (F(2), 16.0), (F(2), True),
                        (F(2), 7), (F(0), 16), (F(-1), 16), ('1/0', 16), ([], 16)):
        require_rejection(lambda value=value, bits=bits: CORE.log_upper(value, bits)); count += 1
    for value, bits in ((2.0, 16), (True, 16), (F(2), 16.0), (F(2), True),
                        (F(2), 7), ('1/0', 16), (None, 16)):
        require_rejection(lambda value=value, bits=bits: CORE.exp_interval(value, bits)); count += 1
    for kwargs in ({'experts': 'ab'}, {'experts': []}, {'experts': ['a', 'a']},
                   {'experts': [[]]}, {'experts': [1]}, {'horizon': True},
                   {'horizon': 0}, {'max_weight': 0}, {'max_slope_range': 0},
                   {'total_numeric_budget': 0}, {'max_bisections': -1},
                   {'initial_bits': 15}, {'max_bits': 16}, {'bins': 65}, {'scope': False}):
        args = {'experts': ['a'], 'horizon': 4}; args.update(kwargs)
        require_rejection(lambda args=args: CORE.CapitalForecaster(**args)); count += 1
    names = ['a', 'b']
    learner = CORE.CapitalForecaster(names, 2, scope='input-audit', initial_bits=24, max_bits=48)
    names.append('not-a-member')
    check(learner.settings.experts == ('a', 'b'), 'expert name input detached')
    for args, kwargs in (
        (('', {'a': 0, 'b': 1}), {}), ((True, {'a': 0, 'b': 1}), {}),
        (('x', {'a': 0}), {}), (('x', {'a': 0, 'b': 1, 'c': 0}), {}),
        (('x', ['a', 'b']), {}), (('x', {'a': True, 'b': 1}), {}),
        (('x', {'a': 0.0, 'b': 1}), {}), (('x', {'a': -1, 'b': 1}), {}),
        (('x', {'a': 0, 'b': 2}), {}), (('x', {'a': 0, 'b': 1}), {'weight': -1}),
        (('x', {'a': 0, 'b': 1}), {'weight': F(1001, 1000)}),
        (('x', {'a': 0, 'b': 1}), {'eta': 0}),
        (('x', {'a': 0, 'b': 1}), {'rows': [[0, 1]]}),
        (('x', {'a': 0, 'b': 1}), {'rows': [[0, 4], [0, 0]]}),
    ):
        require_rejection(lambda args=args, kwargs=kwargs: learner.issue(*args, **kwargs), learner); count += 1
    experts, rows = {'a': F(1, 3), 'b': F(2, 3)}, [[0, 1], [1, 0]]
    pred = learner.issue('valid', experts, rows=rows)
    experts['a'], rows[0][0] = F(100), 100
    check(pred.expert_values[0] == F(1, 3) and pred.actions.rows[0][0] == 0, 'issued inputs detached')
    for field in ('state', 'pending', 'history', 'settings', 'priors', 'expert_rate', 'calibration_rate', 'action_rate'):
        require_rejection(lambda field=field: setattr(learner, field, None), learner); count += 1
    for call in (lambda: setattr(learner.settings, 'horizon', 999),
                 lambda: setattr(pred, 'probability', F(0)),
                 lambda: setattr(pred.actions, 'eta', F(0)),
                 lambda: replace_first(pred.expert_values),
                 lambda: replace_first(pred.actions.rows[0]),
                 lambda: replace_first(learner.priors),
                 lambda: setattr(learner.state, 'capital_bound', F(999))):
        require_rejection(call, learner); count += 1
    report = learner.audit(); before = fingerprint(learner)
    report['state']['logs'] = (F(999),); report['settings']['horizon'] = 999
    check(before == fingerprint(learner), 'audit is detached')
    for outcome in (True, False, F(0), F(1), 0.0, 1.0, '1', -1, 2, None):
        require_rejection(lambda outcome=outcome: learner.reveal('valid', outcome, scope='input-audit'), learner); count += 1
    require_rejection(lambda: learner.reveal('wrong', 1, scope='input-audit'), learner); count += 1
    require_rejection(lambda: learner.reveal('valid', 1, scope='wrong'), learner); count += 1
    require_rejection(lambda: learner.issue('other', {'a': 0, 'b': 1}), learner); count += 1
    learner.reveal('valid', 1, scope='input-audit')
    check(pred.probability == learner.history[0][0].probability, 'old report retained')
    require_rejection(lambda: learner.reveal('valid', 1, scope='input-audit'), learner); count += 1
    require_rejection(lambda: learner.issue('valid', {'a': 0, 'b': 1}), learner); count += 1
    learner.issue('last', {'a': 0, 'b': 1}, weight=0)
    learner.reveal('last', 0, scope='input-audit')
    require_rejection(lambda: learner.issue('too-many', {'a': 0, 'b': 1}), learner); count += 1
    return {'rejection_or_immutable_assignment_cases': count, 'final_fingerprint': fingerprint(learner)}


def reconstruct(history, settings):
    n, m = len(settings.experts), settings.bins
    own, experts, cal, calv = F(0), [F(0)] * n, [F(0)] * (m + 1), [F(0)] * (m + 1)
    acts, actv, fixed, mixed, slack, weight = [F(0)] * 2, [F(0)] * 2, [F(0)] * 2, F(0), F(0), F(0)
    for pred, y in history:
        p, w, rows, eta = pred.probability, pred.weight, pred.actions.rows, pred.actions.eta
        costs = tuple((1 - p) * row[0] + p * row[1] for row in rows)
        s = min(F(1), max(F(0), F(1, 2) - (costs[1] - costs[0]) / (2 * eta)))
        check(s == pred.action_one_probability, 'independent smoothing reconstruction')
        d = tuple(row[1] - row[0] for row in rows)
        own += w * (p - y) ** 2
        for k, q in enumerate(pred.expert_values):
            experts[k] += w * (q - y) ** 2
        for j in range(m + 1):
            v = w * max(F(0), 1 - m * abs(p - F(j, m)))
            cal[j] += v * (y - p); calv[j] += v * v
        for i in (0, 1):
            v = w * ((1 - s) * d[0] + s * d[1] - d[i])
            acts[i] += v * (y - p); actv[i] += v * v
            fixed[i] += w * rows[i][y]
        mixed += w * ((1 - s) * rows[0][y] + s * rows[1][y])
        slack += w * eta / 8; weight += w
    root = isqrt(settings.horizon)
    if root * root < settings.horizon:
        root += 1
    rates = (F(2) / settings.max_weight, F(4, root) / settings.max_weight,
             F(4, root) / (settings.max_weight * settings.max_slope_range))
    logs = tuple(rates[0] * (own - other) for other in experts)
    for residual, variance in zip(cal, calv):
        logs += (rates[1] * residual - rates[1] ** 2 * variance / 8,
                 -rates[1] * residual - rates[1] ** 2 * variance / 8)
    logs += tuple(rates[2] * r - rates[2] ** 2 * v / 8 for r, v in zip(acts, actv))
    return {'logs': logs, 'own_loss': own, 'expert_losses': tuple(experts),
            'calibration_residuals': tuple(cal), 'calibration_variances': tuple(calv),
            'action_residuals': tuple(acts), 'action_variances': tuple(actv),
            'mixed_loss': mixed, 'fixed_losses': tuple(fixed), 'smoothing_slack': slack,
            'weight': weight, 'settled': len(history)}


def reference_capital(logs, priors):
    pairs = [reference_exp(log, 112) for log in logs]
    return tuple(sum((prior * pair[edge] for prior, pair in zip(priors, pairs)), F(0)) for edge in (0, 1))


def test_round(learner, pred, y):
    before = learner.state
    previous = reference_capital(before.logs, learner.priors)
    lo, hi = pred.capital_before_interval
    check(lo <= previous[0] <= previous[1] <= hi, 'old capital enclosure')
    after = []
    for branch in (0, 1):
        expected = reconstruct(learner.history + ((pred, branch),), learner.settings)
        check(expected['logs'] == pred.logs_by_outcome[branch], 'counterfactual exact log identity')
        pair = reference_capital(expected['logs'], learner.priors)
        saved = pred.capital_after_intervals[branch]
        check(saved[0] <= pair[0] <= pair[1] <= saved[1], 'counterfactual capital enclosure')
        check(pair[1] <= before.capital_bound + pred.capital_allowance, 'certified branch allowance')
        check(all(expected['mixed_loss'] - f <= expected['smoothing_slack'] + z
                  for f, z in zip(expected['fixed_losses'], expected['action_residuals'])),
              'centered residual transports actual action regret')
        after.append(pair)
    p = pred.probability
    check((1 - p) * after[0][1] + p * after[1][1] <= previous[0]
          or pred.weight == 0, 'independent supermartingale mean')
    check(pred.allowance_met == (pred.capital_allowance <= pred.requested_allowance), 'budget status accurate')
    learner.reveal(pred.query, y, scope=learner.settings.scope)
    expected = reconstruct(learner.history, learner.settings)
    for key, value in expected.items():
        check(getattr(learner.state, key) == value, ('settled history reconstruction', key))
    check(learner.state.capital_bound == before.capital_bound + pred.capital_allowance, 'retained additive allowance')
    report = learner.audit()
    check(all(expected['own_loss'] - value <= report['expert_regret_upper'] for value in expected['expert_losses']), 'expert bound')
    check(all(abs(value) <= bound for value, bound in zip(expected['calibration_residuals'], report['calibration_absolute_upper'])), 'calibration bound')
    check(all(expected['mixed_loss'] - value <= bound for value, bound in zip(expected['fixed_losses'], report['mixed_action_regret_upper'])), 'action bound')


def test_capital_traces():
    rounds, missed = 0, 0
    weights = (F(3, 2), F(1, 3), F(0), F(1))
    tables = (((0, 1), (1, 0)), ((7, 9), (8, 7)), ((0, -2), (1, -3)), ((0, 3), (2, 1)))
    summaries = []
    for outcomes in product((0, 1), repeat=4):
        learner = CORE.CapitalForecaster(('zero', 'one', 'history'), 4, max_weight=F(3, 2),
            max_slope_range=5, bins=2, initial_bits=24, max_bits=48,
            max_bisections=20, scope='counterfactual-audit')
        check(sum(learner.priors) == 1 and all(prior > 0 for prior in learner.priors), 'positive normalized priors')
        for t, y in enumerate(outcomes):
            experts = {'zero': F(0), 'one': F(1), 'history': F(1 + sum(outcomes[:t]), t + 2)}
            pred = learner.issue(str(t), experts, weights[t], rows=tables[t], eta=F(1, 4 * (t + 1)))
            test_round(learner, pred, y)
            rounds += 1; missed += not pred.allowance_met
        summaries.append({'outcomes': outcomes, 'capital_bound': learner.state.capital_bound,
                          'own_loss': learner.state.own_loss, 'pending': learner.pending is not None})
    return {'sequences': 16, 'rounds': rounds, 'binary_counterfactuals': 2 * rounds,
            'requested_allowance_misses': missed, 'summaries': summaries}


def test_caps_and_offsets():
    cases = []
    for label, kwargs, q, rows in (
        ('large_horizon_precision_exhaustion', {'horizon': 10 ** 12, 'initial_bits': 16,
          'max_bits': 16, 'max_bisections': 4, 'total_numeric_budget': F(1, 1 << 40)},
         F(0), ((0, -1), (1, 2))),
        ('zero_bisection_actual_growth', {'horizon': 8, 'initial_bits': 24,
          'max_bits': 48, 'max_bisections': 0, 'total_numeric_budget': F(1, 1 << 60)},
         F(3, 8), ((0, 1), (1, 0))),
    ):
        learner = CORE.CapitalForecaster(('only',), bins=2, scope=label, **kwargs)
        pred = learner.issue('boundary', {'only': q}, rows=rows)
        exact_pairs = tuple(reference_capital(logs, learner.priors) for logs in pred.logs_by_outcome)
        test_round(learner, pred, 0)
        check(not pred.allowance_met and pred.capital_allowance > 0, (label, 'honest exhaustion'))
        cases.append({'case': label, 'probability': pred.probability,
                      'requested_allowance': pred.requested_allowance, 'actual_allowance': pred.capital_allowance,
                      'allowance_met': pred.allowance_met,
                      'both_outcomes_strictly_decrease_actual_capital': all(pair[1] < 1 for pair in exact_pairs),
                      'some_outcome_strictly_increases_actual_capital': any(pair[0] > 1 for pair in exact_pairs)})
    left = CORE.CapitalForecaster(('a', 'b'), 4, scope='offset-audit', bins=2, initial_bits=24, max_bits=48)
    right = CORE.CapitalForecaster(('a', 'b'), 4, scope='offset-audit', bins=2, initial_bits=24, max_bits=48)
    for t, y in enumerate((1, 0, 0, 1)):
        a, b = F(10 ** 35 * (t + 1)), F((-1) ** t * (10 ** 40 + t))
        rows = ((a, a + 1 + b), (a + 1, a + b))
        qs = {'a': F(t, 4), 'b': F(3, 4)}
        pred0 = left.issue(str(t), qs, eta=F(1, 7)); pred1 = right.issue(str(t), qs, rows=rows, eta=F(1, 7))
        check(pred0.probability == pred1.probability, 'large common offset forecast invariance')
        check(pred0.logs_by_outcome == pred1.logs_by_outcome, 'large common offset capital invariance')
        test_round(left, pred0, y); test_round(right, pred1, y)
        check(left.state.mixed_loss - left.state.fixed_losses[0] == right.state.mixed_loss - right.state.fixed_losses[0], 'exact cancellation of large absolute cost offset')
    return {'capped_cases': cases, 'common_offset_rounds': 4}


def main():
    result = {'status': 'PASS', 'version': CORE.VERSION,
              'reviewer': 'ChatGPT (GPT-6 Astra Pro), independent implementation reviewer',
              'principal_research90_seconds': 0,
              'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
    result['enclosures'] = test_enclosures()
    result['api'] = test_inputs_and_immutability()
    result['capital_traces'] = test_capital_traces()
    result['caps_and_offsets'] = test_caps_and_offsets()
    result['checks'] = CHECKS
    with (HERE / 'audit_capital_v1_1_result.json').open('x') as handle:
        json.dump(encode(result), handle, indent=2, sort_keys=True); handle.write('\n')
    print(json.dumps({'status': result['status'], 'checks': CHECKS,
                      'source_sha256': result['source_sha256'],
                      'exp_cases': result['enclosures']['exp_cases'],
                      'log_cases': result['enclosures']['log_cases'],
                      'api_cases': result['api']['rejection_or_immutable_assignment_cases'],
                      'counterfactuals': result['capital_traces']['binary_counterfactuals']}))


if __name__ == '__main__':
    main()
