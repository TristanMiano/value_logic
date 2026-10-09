"""Independent P3-06 algebra probe for rationally smoothed terminal decisions.

This file imports no project forecaster. It is development evidence for the
review theorem, not an implementation claim about the preserved checkpoint.
Contributor: ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer.
"""
from __future__ import annotations

from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import platform
import time
import traceback


def clip(z):
    return min(F(1), max(F(0), z))


def norm2(v):
    return sum((x * x for x in v), F(0))


def run():
    checks = 0

    def check(statement, message):
        nonlocal checks
        checks += 1
        if not statement:
            raise AssertionError(message)

    # Direct exhaustive rational checks of the local inequality, including
    # every equality case Delta = +/- eta/2 in this finite grid.
    local_cases = 0
    for eta in (F(1, 7), F(1), F(3)):
        for k in range(-32, 33):
            delta = k * eta / 16
            s = clip(F(1, 2) - delta / (2 * eta))
            slack = s * delta - min(F(0), delta)
            check(F(0) <= slack <= eta / 8, 'Local smoothing slack.')
            if abs(k) == 8:
                check(slack == eta / 8, 'Sharp eta/8 constant.')
            local_cases += 1

    alpha, beta, gamma = F(2, 3), F(3, 5), F(5, 7)
    qs = (F(0), F(1, 2), F(1))
    bins = 2
    tables = (
        ((F(0), F(1)), (F(1), F(-1))),
        ((F(2), F(-1)), (F(0), F(2))),
        ((F(1), F(3)), (F(4), F(-2))),
        ((F(0), F(0)), (F(1), F(0))),
        ((F(-2), F(4)), (F(3), F(-3))),
    )
    weights = (F(1, 2), F(1), F(3, 2), F(0), F(2))
    traces = []
    max_rational_bits = 0

    def features(p, t):
        w = weights[t]
        (b0, d0), (b1, d1) = tables[t]
        eta = F(1, t + 2)
        delta = b1 - b0 + (d1 - d0) * p
        s = clip(F(1, 2) - delta / (2 * eta))
        dbar = d0 + s * (d1 - d0)
        phi = tuple(w * alpha * (q - p) for q in qs)
        phi += tuple(w * beta * max(F(0), 1 - bins * abs(p - F(j, bins)))
                     for j in range(bins + 1))
        phi += tuple(w * gamma * (dbar - di) for di in (d0, d1))
        return phi, s

    def score(p, t, residual):
        phi, s = features(p, t)
        value = sum((r * f for r, f in zip(residual, phi)), F(0))
        value += (1 - 2 * p) * norm2(phi) / 2
        return value, phi, s

    def score_lipschitz(t, residual):
        w = weights[t]
        eta = F(1, t + 2)
        diameter = abs(tables[t][1][1] - tables[t][0][1])
        bounds = [(w * alpha, w * alpha)] * len(qs)
        bounds += [(w * beta, w * beta * bins)] * (bins + 1)
        bounds += [(w * gamma * diameter,
                    w * gamma * diameter * diameter / (2 * eta))] * 2
        return sum((abs(r) * lip + maximum**2 + maximum * lip
                    for r, (maximum, lip) in zip(residual, bounds)), F(0))

    for ys in product((0, 1), repeat=5):
        residual = [F(0)] * (len(qs) + bins + 1 + 2)
        variance, allowance = F(0), F(0)
        own_square = F(0)
        other_square, distances = [F(0)] * len(qs), [F(0)] * len(qs)
        mixture_loss = F(0)
        action_losses, action_forecast_gaps = [F(0)] * 2, [F(0)] * 2
        slack_total = F(0)
        trace = []
        for t, y in enumerate(ys):
            tolerance = F(1, 256)
            lipschitz = score_lipschitz(t, residual)
            budget = 0
            while lipschitz / (2 ** (budget + 1)) > tolerance:
                budget += 1
            s0, phi0, action0 = score(F(0), t, residual)
            boundary = False
            steps = 0
            if s0 <= 0:
                p, value, phi, s = F(0), s0, phi0, action0
                boundary = True
            else:
                s1, phi1, action1 = score(F(1), t, residual)
                if s1 >= 0:
                    p, value, phi, s = F(1), s1, phi1, action1
                    boundary = True
                else:
                    low, high = F(0), F(1)
                    p = F(1, 2)
                    value, phi, s = score(p, t, residual)
                    while abs(value) > tolerance and steps < budget:
                        if value > 0:
                            low = p
                        else:
                            high = p
                        p = (low + high) / 2
                        value, phi, s = score(p, t, residual)
                        steps += 1
            check(boundary or abs(value) <= tolerance,
                  'Analytic Lipschitz bisection budget terminates.')
            allowed = 2 * max(F(0), (1 - p) * value, -p * value)
            check(allowed <= 2 * tolerance, 'Successful root allowance.')
            if boundary:
                check(allowed == 0, 'Endpoint allowance.')
            for possible_y in (0, 1):
                error = possible_y - p
                trial = [r + error * f for r, f in zip(residual, phi)]
                increment = norm2(trial) - norm2(residual) - p * (1 - p) * norm2(phi)
                check(increment == 2 * error * value, 'Binary potential identity.')
                check(increment <= allowed, 'Both-outcomes issue-time allowance.')

            w, eta = weights[t], F(1, t + 2)
            (b0, d0), (b1, d1) = tables[t]
            diameter = abs(d1 - d0)
            check(norm2(phi) <= w*w * (len(qs)*alpha*alpha + beta*beta
                                       + gamma*gamma*diameter*diameter),
                  'Sharper joint two-action feature norm bound.')
            error = y - p
            residual = [r + error * f for r, f in zip(residual, phi)]
            variance += p * (1 - p) * norm2(phi)
            allowance += allowed
            bound = variance + allowance
            check(norm2(residual) <= bound, 'Extended common-vector potential.')
            own_square += w * error * error
            for i, q in enumerate(qs):
                other_square[i] += w * (q - y)**2
                distances[i] += w * (q - p)**2
                check(own_square - other_square[i]
                      == 2 * residual[i] / alpha - distances[i],
                      'Existing expert identity retained.')
            mixture_y = (1 - s)*(b0 + d0*y) + s*(b1 + d1*y)
            mixture_p = (1 - s)*(b0 + d0*p) + s*(b1 + d1*p)
            mixture_loss += w * mixture_y
            slack_total += w * eta / 8
            for i, (bi, di) in enumerate(tables[t]):
                action_losses[i] += w * (bi + di*y)
                action_forecast_gaps[i] += w * (mixture_p - bi - di*p)
                regret = mixture_loss - action_losses[i]
                feature_index = len(qs) + bins + 1 + i
                check(regret == action_forecast_gaps[i] + residual[feature_index]/gamma,
                      'Changing-loss-table action identity.')
                check(action_forecast_gaps[i] <= slack_total,
                      'Accumulated local decision slack.')
                excess = regret - slack_total
                check(excess <= 0 or gamma*gamma*excess*excess <= bound,
                      'Finite mixed-action regret bound.')
            for z in (*residual, variance, allowance, p, value):
                max_rational_bits = max(max_rational_bits,
                                        abs(z.numerator).bit_length(),
                                        z.denominator.bit_length())
            trace.append({'round': t, 'p': str(p), 'y': y, 'action_one_probability': str(s),
                          'weight': str(w), 'eta': str(eta), 'root_steps': steps,
                          'root_budget': budget, 'score_lipschitz_bound': str(lipschitz),
                          'allowance': str(allowed), 'bound_squared': str(bound),
                          'mixture_regrets': [str(mixture_loss-z) for z in action_losses],
                          'slack_total': str(slack_total)})
        traces.append({'outcomes': ys, 'trace': trace})

    # The hard-threshold witness satisfies both finite-tent calibration and
    # good square loss, yet has linear external 0/1 decision regret.
    witness = []
    for pairs in (16, 64, 256):
        errors = [F(0)] * 3
        learner_square, expert_half_square = F(0), F(0)
        hard_loss, fixed_losses = F(0), [F(0), F(0)]
        epsilon_sum, epsilon2_sum = F(0), F(0)
        for n in range(1, pairs + 1):
            epsilon = F(1, 8*n)
            epsilon_sum += epsilon
            epsilon2_sum += epsilon*epsilon
            for p, y in ((F(1, 2)-epsilon, 1), (F(1, 2)+epsilon, 0)):
                for j in range(3):
                    errors[j] += max(F(0), 1 - 2*abs(p-F(j, 2))) * (y-p)
                learner_square += (y-p)**2
                expert_half_square += (F(1, 2)-y)**2
                action = int(p > F(1, 2))
                hard_loss += int(action != y)
                for i in (0, 1):
                    fixed_losses[i] += int(i != y)
        expected_edge = epsilon_sum + 2*epsilon2_sum
        check(errors == [expected_edge, F(0), -expected_edge], 'Exact hard-decision witness bins.')
        check(learner_square-expert_half_square == 2*epsilon_sum+2*epsilon2_sum,
              'Exact hard-decision witness square regret.')
        check(hard_loss-min(fixed_losses) == pairs, 'Linear hard-decision external regret.')
        witness.append({'rounds': 2*pairs, 'bin_residuals': list(map(str, errors)),
                        'square_regret_to_half': str(learner_square-expert_half_square),
                        'hard_action_regret': str(hard_loss-min(fixed_losses))})

    return {'status': 'PASS', 'assertions': checks, 'local_slack_cases': local_cases,
            'binary_sequences': len(traces), 'traces': traces,
            'hard_threshold_witness': witness, 'max_rational_component_bits': max_rational_bits,
            'scope': 'Independent finite development probe; general claims rest on the review proofs.'}


if __name__ == '__main__':
    started = datetime.now(timezone.utc).isoformat()
    start_ns = time.monotonic_ns()
    try:
        result = run()
    except Exception:
        result = {'status': 'FAIL', 'traceback': traceback.format_exc()}
    result.update(start_utc=started, end_utc=datetime.now(timezone.utc).isoformat(),
                  execution_ns=time.monotonic_ns()-start_ns, python=platform.python_version(),
                  contributor='ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer',
                  principal_research_time_credit_ns=0, subagent_research_effort='unmeasured',
                  source_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    target = Path(__file__).with_name('decision_extension_probe_result.json')
    if target.exists():
        raise SystemExit('Refusing to overwrite an existing review probe result.')
    target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in
                     ('status', 'assertions', 'execution_ns', 'source_sha256') if key in result}))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
