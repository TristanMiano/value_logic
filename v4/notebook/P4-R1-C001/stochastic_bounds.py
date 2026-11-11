#!/usr/bin/env python3
"""Sufficient observation budgets for the proved binary online construction.

Codex (GPT-6), November 10, 2026. These are conservative analytic bounds,
not executed simulation horizons or minimax sample complexity estimates.
"""
import argparse
import json
from math import exp, log, sqrt
from pathlib import Path


def logistic(x):
    if x >= 0: return 1 / (1 + exp(-x))
    v = exp(x); return v / (1 + v)


def bounds(n, a, exposure, w0=.01, b0=-.5, eta=1., alpha=.025, beta=.025):
    k = n // 2
    # gamma_t=(t+25)^(-.6), t starts at zero.
    square_sum_upper = 25 ** -1.2 + 5 * 25 ** -.2
    gk_lower = ((k + 25) ** .4 - 25 ** .4) / .4
    window_lower = ((n + 25) ** .4 - (k + 25) ** .4) / .4
    maximum_window_step = (k + 25) ** -.6
    martingale_cap = sqrt(2 * square_sum_upper * log(2 / alpha))
    c = 2 / eta + martingale_cap
    energy_lower = max(0., exposure * abs(a) * gk_lower - c) ** 2 / gk_lower if gk_lower else 0.
    log_odds_lower = log(w0 / (1 - w0)) - b0 * b0 / eta - 4 * eta * square_sum_upper + energy_lower
    missing_upper = logistic(-log_odds_lower)
    transient = 2 * exp(-eta * exposure * window_lower)
    feedback_bias = (1 - exposure) * missing_upper / exposure
    noise = sqrt(2 * eta * maximum_window_step / exposure * log(2 / beta))
    return {'observations': n, 'midpoint': k, 'joint_failure_bound': alpha + beta,
            'squared_step_sum_upper': square_sum_upper,
            'fine_weight_lower_from_midpoint_onward': logistic(log_odds_lower),
            'forecast_absolute_error_upper': transient + feedback_bias + noise,
            'error_terms': {'initial_transient': transient, 'residual_coarse_influence': feedback_bias,
                            'martingale_noise': noise}}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path); args = p.parse_args()
    records = []
    for exposure in (.5, .2, .05):
        def satisfied(n):
            b = bounds(n, .6, exposure)
            return b['fine_weight_lower_from_midpoint_onward'] >= .99 and b['forecast_absolute_error_upper'] <= .1
        upper = 2
        while not satisfied(upper): upper *= 2
        lower = upper // 2
        while lower + 1 < upper:
            middle = (lower + upper) // 2
            if satisfied(middle): upper = middle
            else: lower = middle
        records.append({'a': .6, 'environmental_share': exposure,
                        'sufficient_budget': bounds(upper, .6, exposure),
                        'at_one_million': bounds(1000000, .6, exposure)})
    answer = {'author': 'Codex (GPT-6)', 'status': 'calculated',
              'initial_forecast': -.5, 'initial_weight': .01,
              'step_rule': 'gamma_t=(t+25)^(-0.6), eta=1', 'records': records,
              'scope': 'Conservative sufficient budgets at specified model parameters; not necessary budgets or observed performance.'}
    encoded = json.dumps(answer, indent=2) + '\n'
    if args.output: args.output.write_text(encoded, encoding='utf-8', newline='\n')
    print(encoded)


if __name__ == '__main__': main()
