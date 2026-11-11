#!/usr/bin/env python3
"""Checks of coupled forecasts, conceptual partitions, and recurrence feedback.

Codex (GPT-6), November 10, 2026. Requires NumPy and SciPy. This integrates
the population ODE; it does not simulate or certify a finite-sample learner.
No prior Fable research implementation is used. Run from this directory:
python coupled_reappearance.py --output coupled_reappearance.json
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import expit

from audit_s6 import labels


def projection(mu, c):
    c = np.asarray(c)
    match = c[:, None] == c[None, :]
    matrix = match * mu[None, :]
    return matrix / matrix.sum(axis=1, keepdims=True)


class Community:
    def __init__(self, mu, environmental, partitions, share, reserve=None):
        self.mu = np.asarray(mu, float)
        self.F = np.asarray(environmental, float)
        self.parts = list(partitions)
        self.e = share
        self.m, self.n = len(self.parts), len(mu)
        self.P = np.asarray([projection(self.mu, c) for c in self.parts])
        self.measure = np.outer(self.mu, self.mu)
        self.reserve = reserve
        self.layout = []
        offset = self.m
        for c in self.parts:
            nc = max(c) + 1
            mass = np.array([sum(self.mu[x] for x in range(self.n) if c[x] == a)
                             for a in range(nc)])
            reps = [c.index(a) for a in range(nc)]
            pairs = list(combinations(range(nc), 2))
            self.layout.append((offset, mass, reps, pairs, np.asarray(c)))
            offset += len(pairs)
        self.projected = self.project(self.F)
        self.delta = np.einsum('cij,cij,ij->c', self.projected - self.F,
                               self.projected - self.F, self.measure)
        self.full = self.parts.index(tuple(range(self.n))) if tuple(range(self.n)) in self.parts else None
        assert np.all(self.F >= 0)
        assert np.max(np.abs(self.F @ self.mu - 1)) < 1e-12
        assert np.max(np.abs(self.F - self.F.T)) < 1e-12

    def project(self, matrix):
        return self.P @ matrix @ self.P.transpose(0, 2, 1)

    def split(self, state):
        logits = state[:self.m]
        weights = np.exp(logits - np.max(logits))
        weights /= weights.sum()
        forecasts = []
        for offset, mass, reps, pairs, c in self.layout:
            joint = np.zeros((len(mass), len(mass)))
            for value, (a, b) in zip(state[offset:offset + len(pairs)], pairs):
                joint[a, b] = joint[b, a] = value
            np.fill_diagonal(joint, mass - joint.sum(axis=1))
            density = joint / np.outer(mass, mass)
            forecasts.append(density[c[:, None], c[None, :]])
        return weights, np.asarray(forecasts)

    def pack(self, weights, forecasts):
        if np.any(weights <= 0):
            raise ValueError('simulation logits require positive initial weights')
        coordinates = list(np.log(weights))
        for forecast, (_, mass, reps, pairs, _) in zip(forecasts, self.layout):
            coordinates.extend(mass[a] * mass[b] * forecast[reps[a], reps[b]] for a, b in pairs)
        return np.asarray(coordinates)

    def rates(self, weights):
        if self.reserve is None:
            return np.ones(self.m)
        # Fixed total learning-rate budget m, with reserve*m spread uniformly.
        return self.reserve + (1 - self.reserve) * self.m * weights

    def quantities(self, state):
        weights, forecasts = self.split(state)
        mean = np.einsum('c,cij->ij', weights, forecasts)
        generated = self.e * self.F + (1 - self.e) * mean
        norms = np.einsum('cij,cij,ij->c', forecasts, forecasts, self.measure)
        scores = 2 * np.einsum('cij,ij,ij->c', forecasts, generated, self.measure) - norms
        potential = (2 * self.e * np.sum(self.F * mean * self.measure)
                     + (1 - self.e) * np.sum(mean ** 2 * self.measure) - weights @ norms)
        return weights, forecasts, mean, generated, scores, potential

    def rhs(self, _time, state):
        weights, forecasts, _, generated, scores, _ = self.quantities(state)
        # Log-weight coordinates preserve the simplex at every evaluation.
        dlogw = scores - weights @ scores
        dr = self.rates(weights)[:, None, None] * (self.project(generated) - forecasts)
        coordinates = list(dlogw)
        for derivative, (_, mass, reps, pairs, _) in zip(dr, self.layout):
            coordinates.extend(mass[a] * mass[b] * derivative[reps[a], reps[b]] for a, b in pairs)
        return np.asarray(coordinates)

    def potential_derivative(self, state):
        weights, forecasts, _, generated, scores, _ = self.quantities(state)
        residual = self.project(generated) - forecasts
        return (weights @ ((scores - weights @ scores) ** 2)
                + 2 * np.sum(weights * self.rates(weights)
                             * np.einsum('cij,cij,ij->c', residual, residual, self.measure)))

    def initial(self, seed=20261110, weights=None):
        rng = np.random.default_rng(seed)
        forecasts = []
        for index in range(self.m):
            a = rng.normal(size=self.n)
            a -= self.mu @ a
            a *= 0.65 / max(abs(a))
            raw = np.ones((self.n, self.n)) + np.outer(a, a)
            forecasts.append(self.P[index] @ raw @ self.P[index].T)
        if weights is None:
            weights = np.full(self.m, .2 / (self.m - 1))
            weights[0] = .8
        return self.pack(np.asarray(weights), np.asarray(forecasts))

    def simulate(self, horizon, initial=None, tolerance=1e-9):
        if initial is None:
            initial = self.initial()
        sol = solve_ivp(self.rhs, (0., horizon), initial, method='DOP853',
                        rtol=tolerance, atol=tolerance / 100,
                        t_eval=np.linspace(0, horizon, 301))
        assert sol.success, sol.message
        quantities = [self.quantities(y) for y in sol.y.T]
        final = quantities[-1]
        weights, forecasts, mean, generated, _, potential = final
        good = self.delta < 1e-13
        potentials = np.asarray([q[-1] for q in quantities])
        assert min(np.min(q[0]) for q in quantities) > -1e-8
        assert max(abs(q[0].sum() - 1) for q in quantities) < 1e-8
        assert min(np.min(q[1]) for q in quantities) > -1e-8
        assert max(np.max(abs(q[1] @ self.mu - 1)) for q in quantities) < 1e-8
        return {
            'environment_share': self.e, 'learning_reserve_per_type': self.reserve,
            'horizon': horizon, 'solver_relative_tolerance': tolerance,
            'function_evaluations': sol.nfev,
            'partitions': self.parts, 'sufficient_partitions': [c for c, yes in zip(self.parts, good) if yes],
            'final_weights': weights.tolist(), 'nonsufficient_mass': float(weights[~good].sum()),
            'mean_forecast_max_error': float(abs(mean - self.F).max()),
            'actual_recurrence_max_error': float(abs(generated - self.F).max()),
            'calibrated_forecasts_max_error': float(abs(forecasts - self.projected).max()),
            'potential_gap': float(self.e * np.sum(self.F ** 2 * self.measure) - potential),
            'minimum_sampled_potential_increment': float(np.diff(potentials).min()),
            'initial_potential': float(potentials[0]), 'final_potential': float(potential),
        }, sol.y[:, -1]


def check_potential_identity():
    rng = np.random.default_rng(20261111)
    max_relative = 0.
    for n in (3, 4):
        mu = np.arange(1, n + 1, dtype=float)
        mu /= mu.sum()
        a = rng.normal(size=n)
        a -= mu @ a
        a *= .8 / max(abs(a))
        F = np.ones((n, n)) + np.outer(a, a)
        for e in (0., .05, .3, 1.):
            for reserve in (None, .1):
                comm = Community(mu, F, list(labels(n)), e, reserve)
                state = comm.initial(seed=int(rng.integers(1, 1000000)))
                direction = comm.rhs(0, state)
                step = 1e-5
                difference = (comm.quantities(state + step * direction)[-1]
                              - comm.quantities(state - step * direction)[-1]) / (2 * step)
                formula = comm.potential_derivative(state)
                relative = abs(difference - formula) / max(1., abs(formula))
                max_relative = max(max_relative, relative)
                assert relative < 2e-8
    return {'cases': 16, 'largest_scaled_derivative_error': max_relative}


def binary_rhs(a, e, reserve):
    def rhs(_, state):
        logit, b = state
        w = expit(logit)
        q = e * a + (1 - e) * w * b
        eta = 1. if reserve is None else reserve + (1 - 2 * reserve) * w
        return [2 * b * q - b * b, eta * (q - b)]
    return rhs


def binary_checks():
    checks = []
    for reserve in (0., .05, None):
        horizon = 3000.
        sol = solve_ivp(binary_rhs(.5, .5, reserve), (0., horizon), [np.log(.01 / .99), -.5],
                        method='DOP853', rtol=1e-11, atol=1e-13)
        assert sol.success
        logit, b = sol.y[:, -1]
        w = expit(logit)
        checks.append({'case': 'rare initially mistaken fine model', 'reserve': reserve,
                       'total_rate_budget': 1 if reserve is not None else 2,
                       'final_fine_weight': float(w), 'final_correlation_forecast': float(b),
                       'horizon': horizon})
        if reserve == 0:
            assert w < 1e-9 and -.5 <= b <= -.4594
        else:
            assert w > 1 - 1e-8 and abs(b - .5) < 1e-8
    exposure = []
    for e in (.5, .2, .1, .05):
        def half_weight(_, state):
            return expit(state[0]) - .5
        half_weight.terminal = True
        half_weight.direction = 1
        a = .7
        sol = solve_ivp(binary_rhs(a, e, None), (0., 50 / (e * e * a * a)), [np.log(.01 / .99), 0.],
                        method='DOP853', rtol=1e-10, atol=1e-12, events=half_weight)
        assert sol.success and len(sol.t_events[0]) == 1
        time = float(sol.t_events[0][0])
        exposure.append({'environment_share': e, 'time_to_half_influence': time,
                         'linearized_invasion_rate': e * e * a * a,
                         'time_times_share_squared': time * e * e})
    return {'allocation_comparison': checks, 'weak_exposure': exposure}


def common_worlds():
    cases = []
    mu = np.full(4, .25)
    a = np.array([.7, .7, -.7, -.7])
    F = np.ones((4, 4)) + np.outer(a, a)
    for e, reserve in ((1., None), (.2, None), (.2, .1)):
        comm = Community(mu, F, list(labels(4)), e, reserve)
        result, _ = comm.simulate(1200.)
        result['world'] = 'two recurring kinds, four observable symbols'
        assert result['nonsufficient_mass'] < 2e-7
        assert result['mean_forecast_max_error'] < 2e-7
        cases.append(result)
    mu = np.array([.1, .2, .3, .4])
    a = np.array([-.6, -.6, .2, .3])
    F = np.ones((4, 4)) + np.outer(a, a)
    comm = Community(mu, F, list(labels(4)), .3)
    early, state = comm.simulate(12000.)
    early['world'] = 'unequal reference frequencies and near-twin distinctions'
    early['minimum_positive_score_gap'] = float(min(comm.delta[comm.delta > 1e-12]))
    # A first trial at this horizon retained about 9.5% nonsufficient mass.
    # Keep that adverse finite-horizon evidence rather than treating an
    # asymptotic theorem as a uniform finite-time certificate.
    cases.append(early)
    result, _ = comm.simulate(48000., initial=state)
    result['world'] = 'same near-twin world continued to time 60000'
    result['elapsed_from_original_start'] = 60000.
    result['minimum_positive_score_gap'] = early['minimum_positive_score_gap']
    assert result['nonsufficient_mass'] < early['nonsufficient_mass']
    assert result['mean_forecast_max_error'] < early['mean_forecast_max_error']
    cases.append(result)
    mu = np.full(4, .25)
    a = np.array([1., 1., -1., -1.])
    F = np.ones((4, 4)) - .5 * np.outer(a, a)
    comm = Community(mu, F, list(labels(4)), .2)
    result, _ = comm.simulate(1200.)
    result['world'] = 'alternating kinds: reversible but not conditional-iid Gram'
    assert result['nonsufficient_mass'] < 2e-7
    assert result['mean_forecast_max_error'] < 2e-7
    cases.append(result)
    # At zero environmental exposure, arbitrary common predictions sustain themselves.
    comm = Community(mu, F, list(labels(4)), 0.)
    state = comm.pack(np.full(comm.m, 1 / comm.m), np.ones((comm.m, 4, 4)))
    assert np.max(abs(comm.rhs(0., state))) < 1e-14
    limits = {'zero_exposure_stationary_nonfactual_error': float(abs(comm.quantities(state)[3] - F).max()),
              'missing_concepts': 'coarse-only catalogue remains coarse even with positive environmental exposure'}
    coarse = Community(mu, F, [(0, 0, 0, 0)], .2)
    state = coarse.pack(np.ones(1), np.ones((1, 4, 4)))
    assert np.max(abs(coarse.rhs(0., state))) < 1e-14
    limits['coarse_only_forecast_error'] = float(abs(coarse.quantities(state)[2] - F).max())
    return cases, limits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--part', choices=('all', 'identity', 'binary', 'worlds'), default='all')
    args = parser.parse_args()
    result = {'author': 'Codex (GPT-6)', 'cycle': 'P4-R1-C001', 'session': 6,
              'evidence': 'population ODE integration; no finite-sample learning claim'}
    if args.part in ('all', 'identity'):
        result['potential_identity'] = check_potential_identity()
        print('potential identity checks passed', flush=True)
    if args.part in ('all', 'binary'):
        result['binary'] = binary_checks()
        print('binary allocation and exposure checks passed', flush=True)
    if args.part in ('all', 'worlds'):
        result['worlds'], result['limiting_cases'] = common_worlds()
        print('shared-world convergence checks passed', flush=True)
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded, encoding='utf-8', newline='\n')
        print(json.dumps({'output': str(args.output), 'status': 'passed'}))
    else:
        print(encoded, end='')


if __name__ == '__main__':
    main()
