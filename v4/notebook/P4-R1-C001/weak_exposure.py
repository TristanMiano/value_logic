#!/usr/bin/env python3
"""W1 checks for grounding with weakening environmental exposure.

Codex (GPT-6), November 10, 2026. ODE checks use finite calibration speed.
The long-horizon probe calculation is an exact event-driven simulation of
the accepted Bernoulli stream, NOT execution of trillions of physical trials.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import json
from math import exp, log, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import expit


def logit(w):
    return log(w / (1 - w))


def dynamics(a, e0, power, eta, w0, horizon):
    initial_logit = logit(w0)

    def rhs(t, state):
        b, ell, integral = state
        w, missing = expit(ell), expit(-ell)
        exposure = e0 * (1 + t) ** -power
        q = exposure * a + (1 - exposure) * w * b
        return [eta * (exposure * a - (missing + exposure * w) * b),
                2 * b * q - b * b, b * b]

    times = np.unique(np.r_[0., np.geomspace(.01, horizon, 400), [1., 10., 100., 1000., 10000.], horizon])
    times = times[times <= horizon]
    solution = solve_ivp(rhs, [0., horizon], [0., initial_logit, 0.],
                         method='Radau', t_eval=times, rtol=2e-9, atol=2e-11)
    assert solution.success, solution.message
    b, ell, integral = solution.y
    residual = ell - initial_logit - integral - b * b / eta
    max_identity_error = float(np.max(np.abs(residual)))
    assert max_identity_error < 1e-6
    assert np.min(b * np.sign(a)) >= -1e-10
    assert np.max(np.abs(b)) <= abs(a) + 1e-8
    snapshots = []
    for t in (100., 10000., horizon):
        ix = int(np.argmin(abs(times - t)))
        exposure = e0 * (1 + times[ix]) ** -power
        w = float(expit(ell[ix]))
        snapshots.append({'time': float(times[ix]), 'fine_weight': w,
                          'fine_forecast': float(b[ix]), 'environmental_share': exposure,
                          'actual_recurrence': float(exposure * a + (1 - exposure) * w * b[ix]),
                          'missing_weight_over_exposure': float(expit(-ell[ix]) / exposure)})
    result = {'a': a, 'e0': e0, 'power': power, 'eta': eta, 'initial_weight': w0,
              'horizon': horizon, 'max_logit_identity_error': max_identity_error,
              'solver_function_evaluations': solution.nfev, 'snapshots': snapshots}
    if power > .5 and w0 < .5:
        c = .5
        energy = a * a * e0 * e0 / ((1 - c) ** 2 * (2 * power - 1))
        threshold = logit(c) - initial_logit
        result['failure_certificate'] = {'barrier': c, 'energy_bound': energy,
                                         'logit_distance': threshold,
                                         'condition_satisfied': energy < threshold,
                                         'uniform_weight_upper_bound': float(expit(initial_logit + energy))}
        if energy < threshold:
            assert np.max(expit(ell)) <= expit(initial_logit + energy) + 1e-9
    return result


def noisy_probe_checks():
    records = []
    for a, exposure, beta in product((F(-3, 5), F(0), F(3, 5)),
                                     (F(1, 20), F(1, 5), F(4, 5)),
                                     (F(1, 2), F(9, 10), F(1))):
        moments = [F(0)] * 4
        fisher = [[F(0), F(0)], [F(0), F(0)]]
        for action, outcome in product((-1, 1), repeat=2):
            probability = (1 + outcome * (exposure * a + (1 - exposure) * beta * action)) / 4
            x = outcome - beta * action
            d = 1 - action * outcome / beta
            moments[0] += probability * x
            moments[1] += probability * d
            moments[2] += probability * (x - a * d) ** 2
            moments[3] += probability * (x - a * d)
            gradient = [F(outcome, 4) * exposure, F(outcome, 4) * (a - beta * action)]
            for i, j in product(range(2), repeat=2):
                fisher[i][j] += gradient[i] * gradient[j] / probability
        assert moments[0] == exposure * a and moments[1] == exposure and moments[3] == 0
        variance = (1 - beta ** 2) * (1 + a * a / beta ** 2) + 2 * exposure * (beta ** 2 - a * a)
        assert moments[2] == variance
        efficient = fisher[0][0] - fisher[0][1] ** 2 / fisher[1][1]
        denominator = (a * a + beta * beta) * (1 - exposure ** 2 * a * a - (1 - exposure) ** 2 * beta ** 2)
        denominator -= 4 * exposure * (1 - exposure) * a * a * beta * beta
        formula = exposure ** 2 * beta ** 2 / denominator
        assert efficient == formula
        records.append({'a': str(a), 'share': str(exposure), 'control_precision': str(beta),
                        'moment_variance': str(variance), 'efficient_information': str(efficient)})
    return records


def accepted_stream(a, e0, power, horizon, seed):
    """Exact thinning of decreasing independent Bernoulli acceptance hazards.

    At time t the future hazard is bounded by its value at t. Draw the next
    proposal by a geometric wait at this bound, retain with actual/bound,
    and tighten the bound at every proposal. Marks are independent of the
    acceptance time. Rejected physical trials are not instantiated.
    """
    rng = np.random.default_rng(seed)
    t, accepted, total, proposals = 0, 0, 0, 0
    bound = e0 / 2
    checkpoints = [10 ** 6, 10 ** 9, horizon]
    records = []
    next_checkpoint = 0
    while t < horizon:
        candidate = t + int(rng.geometric(bound))
        while next_checkpoint < len(checkpoints) and candidate > checkpoints[next_checkpoint]:
            n = checkpoints[next_checkpoint]
            radius = sqrt((accepted + 1) * log((accepted + 1) / .05 ** 2)) / accepted if accepted else None
            # Integral lower/upper bounds for sum_{t=1}^n e0/2*(1+t)^-power.
            def integral(lo, hi):
                if power == 1: return log((1 + hi) / (1 + lo))
                return ((1 + hi) ** (1 - power) - (1 + lo) ** (1 - power)) / (1 - power)
            lower = e0 / 2 * integral(1, n + 1)
            upper = e0 / 2 * (2 ** -power + integral(1, n))
            records.append({'raw_observation_horizon': n, 'accepted_marks': accepted,
                            'accepted_mean': total / accepted if accepted else None,
                            'confidence_radius': radius,
                            'expected_acceptances_interval': [lower, upper]})
            next_checkpoint += 1
        if candidate > horizon: break
        actual = e0 / 2 * (1 + candidate) ** -power
        proposals += 1
        if rng.random() < actual / bound:
            accepted += 1
            total += 1 if rng.random() < (1 + a) / 2 else -1
        t, bound = candidate, actual
    return {'seed': seed, 'a': a, 'e0': e0, 'power': power, 'proposal_events_simulated': proposals,
            'snapshots': records,
            'scope': 'Exact accepted-process simulation by thinning; raw horizons are hypothetical observation counts, not executed trials.'}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path); args = p.parse_args()
    cases = [(.6, .2, .25, 1., .01, 1e6),
             (.8, .8, .5, .7, .2, 1e6),
             (.6, .2, .5, 1., .01, 1e6),
             (.6, .2, .75, 1., .01, 1e6),
             (.6, .2, .75, 1., .99, 1e6),
             (-.6, .2, .25, .1, .01, 1e6)]
    ode = [dynamics(*case) for case in cases]
    # Checks of the individual conditional KL bound, independent of policy.
    kl_checks = 0
    for a0, beta in product((.1, .4, .8), (.2, .6, .9)):
        for exposure, feedback in product((.001, .01, .1, .7, 1.), (-beta, 0., beta)):
            pp = (1 + (1 - exposure) * feedback + exposure * a0) / 2
            pm = (1 + (1 - exposure) * feedback - exposure * a0) / 2
            divergence = pp * log(pp / pm) + (1 - pp) * log((1 - pp) / (1 - pm))
            bound = 4 * a0 * a0 * exposure * exposure / (1 - max(beta, a0) ** 2)
            assert divergence <= bound + 1e-14
            kl_checks += 1
    moments = noisy_probe_checks()
    probes = accepted_stream(.6, .2, .75, 10 ** 12, 20261123)
    result = {'author': 'Codex (GPT-6)', 'status': 'passed',
              'simultaneous_learning_cases': ode, 'conditional_kl_checks': kl_checks,
              'exact_noisy_probe_checks': len(moments), 'noisy_probe_records': moments,
              'weak_exposure_probe': probes,
              'scope': 'Finite ODE checks and exact identities support the stated proofs, not general multi-concept or strategic-agent claims.'}
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output: args.output.write_text(encoded, encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'noisy_probe_records'}, indent=2))


if __name__ == '__main__': main()
