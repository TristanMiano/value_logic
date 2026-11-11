#!/usr/bin/env python3
"""Exact catalogue geometry and ODE boundary checks for R1.9 extensions.

Codex (GPT-6), November 10, 2026. The two binary partitions have one free
contrast each. Exact arithmetic checks their invasion and calibration
identities; numerical solutions only illustrate attraction and repair.
"""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import expit

from coupled_reappearance import Community


def exact_boundary(a, r, e):
    x = a * (e + (1 - e) * r * r)
    y = a * r
    advantage = x * x - y * y
    critical = r / (1 + r)
    unstable_threshold = (critical - e) / (1 - e) if e < critical else F(0)
    return {'amplitude': str(a), 'projection_overlap': str(r), 'exposure': str(e),
            'good_forecast_contrast': str(x), 'bad_forecast_contrast': str(y),
            'good_invasion_advantage': str(advantage), 'advantage_float': float(advantage),
            'critical_exposure': str(critical),
            'quasistatic_good_weight_threshold': str(unstable_threshold),
            'linearization_eigenvalues': [str(advantage), '-1', str(-e)]}


def trajectory(a, r, e, horizon=3000, initial_weight=.001):
    x0 = a * (e + (1 - e) * r * r)
    y0 = a * r
    def rhs(_time, z):
        w, x, y = expit(z[0]), z[1], z[2]
        qg = e * a + (1 - e) * (w * x + (1 - w) * r * y)
        qc = e * a * r + (1 - e) * (w * r * x + (1 - w) * y)
        return [2 * x * qg - x * x - (2 * y * qc - y * y), qg - x, qc - y]
    sol = solve_ivp(rhs, (0, horizon), [np.log(initial_weight / (1 - initial_weight)), x0, y0],
                    method='DOP853', rtol=1e-10, atol=1e-12)
    assert sol.success
    return {'exposure': e, 'initial_weight': initial_weight, 'horizon': horizon,
            'final_good_weight': float(expit(sol.y[0, -1])),
            'final_good_contrast': float(sol.y[1, -1]),
            'final_bad_contrast': float(sol.y[2, -1]), 'function_evaluations': sol.nfev}


def identity_checks():
    # Fully represented densities check the reduced formulas independently.
    mu = np.full(3, 1 / 3)
    v = np.array([1., 1., -2.])
    environmental = np.ones((3, 3)) + .2 * np.outer(v, v)
    c = Community(mu, environmental, [(0, 0, 1), (0, 1, 1)], .1)
    bad = c.projected[1]
    generated = .1 * environmental + .9 * bad
    good = c.project(generated)[0]
    norm = lambda x: np.sum(c.measure * x * x)
    advantage = norm(good) - norm(bad)
    assert abs(advantage - float(F(-39, 6400))) < 1e-14
    max_residual = 0.
    for e in (.01, .1, .2, .5, .9, 1.):
        c.e = e
        for w in (.0, .01, .2, .6, 1.):
            weights = np.array([w, 1 - w])
            # Solve simultaneous projected calibration as a linear system.
            operator = np.zeros((9, 9))
            for j in range(9):
                basis = np.zeros((3, 3)); basis.flat[j] = 1
                operator[:, j] = np.einsum('c,cij->ij', weights, c.project(basis)).ravel()
            q = np.linalg.solve(np.eye(9) - (1 - e) * operator, e * environmental.ravel()).reshape(3, 3)
            forecasts = c.project(q)
            mean = np.einsum('c,cij->ij', weights, forecasts)
            d = environmental - mean
            parallel = c.project(d)[0]
            perpendicular = d - parallel
            variance = sum(weights[i] * norm(forecasts[i] - mean) for i in range(2))
            scores = np.array([2 * np.sum(c.measure * r * q) - norm(r) for r in forecasts])
            predicted = e * e * norm(parallel) + (2 * e - 1) * norm(perpendicular) + variance
            max_residual = max(max_residual, abs(scores[0] - weights @ scores - predicted))
            if e >= .5 and norm(d) > 1e-10:
                assert predicted > 0
    assert max_residual < 1e-12
    return {'calibrated_profiles': 30, 'maximum_advantage_identity_error': max_residual,
            'uniform_three_symbol_boundary_advantage': advantage}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path); args = p.parse_args()
    sharp_family = []
    for epsilon in (F(1, 4), F(1, 10), F(1, 100), F(1, 1000)):
        r = (F(1, 2) - epsilon) / (F(1, 2) + epsilon)
        critical = r / (1 + r)
        assert critical == F(1, 2) - epsilon
        case = exact_boundary(F(1, 2), r, critical / 2)
        assert F(case['good_invasion_advantage']) < 0
        case['reference_masses'] = [str(F(1, 2) - epsilon), str(epsilon), '1/2']
        sharp_family.append(case)
    trials = [trajectory(.4, .25, e, horizon=30000 if e == .21 else 3000, initial_weight=w)
              for e, w in ((.1, .001), (.1, .4), (.21, .001), (.5, .001))]
    assert trials[0]['final_good_weight'] < 1e-8
    assert all(t['final_good_weight'] > 1 - 1e-7 for t in trials[1:])
    result = {'author': 'Codex (GPT-6)', 'status': 'passed',
              'exact_uniform_example': exact_boundary(F(2, 5), F(1, 4), F(1, 10)),
              'sharp_half_exposure_family': sharp_family, 'projection_checks': identity_checks(),
              'trajectories': trials,
              'scope': 'Population calibration and selection, not strategic forecast choice or finite-sample learning.'}
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output: args.output.write_text(encoded, encoding='utf-8', newline='\n')
    print(encoded)


if __name__ == '__main__': main()
