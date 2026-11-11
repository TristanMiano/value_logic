#!/usr/bin/env python3
"""Observed online calibration and concept selection, with no hidden inputs.

Codex (GPT-6), November 10, 2026. Known environmental parameters are used
only in the simulator and evaluation. The learner update receives Z only.
The conventional full-representation comparator sees its own controlled
stream, at the same raw observation count, coupled by common uniforms.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.special import expit


class Learner:
    def __init__(self, b, weight, eta):
        self.b = np.array(b, dtype=float)
        self.log_odds = np.log(np.array(weight) / (1 - np.array(weight)))
        self.initial_b = self.b.copy()
        self.initial_log_odds = self.log_odds.copy()
        self.eta = eta
        self.energy = np.zeros_like(self.b)
        self.noise_correction = np.zeros_like(self.b)

    def influence(self):
        return expit(self.log_odds)

    def step(self, observed, gamma):
        old = self.b.copy()
        self.log_odds += gamma * (2 * old * observed - old * old)
        self.b += self.eta * gamma * (observed - old)
        self.energy += gamma * old * old
        self.noise_correction += self.eta * gamma * gamma * (observed - old) ** 2

    def identity_error(self):
        return self.log_odds - self.initial_log_odds - self.energy - (self.b ** 2 - self.initial_b ** 2) / self.eta + self.noise_correction


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path)
    p.add_argument('--steps', type=int, default=1000000); args = p.parse_args()
    specifications = [
        {'name': 'informative_wrong_sign', 'a': .6, 'share': .2, 'b0': -.5, 'w0': .01},
        {'name': 'stronger_exposure', 'a': .6, 'share': .5, 'b0': -.5, 'w0': .01},
        {'name': 'weak_exposure', 'a': .6, 'share': .05, 'b0': -.5, 'w0': .01},
        {'name': 'negative_environment', 'a': -.6, 'share': .2, 'b0': .5, 'w0': .01},
        {'name': 'no_distinction', 'a': 0., 'share': .2, 'b0': -.5, 'w0': .01}]
    replicates = 12
    a = np.repeat([s['a'] for s in specifications], replicates)
    exposure = np.repeat([s['share'] for s in specifications], replicates)
    b0 = np.repeat([s['b0'] for s in specifications], replicates)
    w0 = np.repeat([s['w0'] for s in specifications], replicates)
    learner = Learner(b0, w0, eta=1.)
    full_predictor = b0.copy()
    rng = np.random.default_rng(20261124)
    checkpoints = sorted(set([n for n in (1000, 10000, 100000, args.steps) if n <= args.steps]))
    records, max_identity = [], 0.
    step_sum = 0.
    for start in range(0, args.steps, 2000):
        stop = min(args.steps, start + 2000)
        uniforms = rng.random((stop - start, len(a)))
        for offset, uniform in enumerate(uniforms):
            t = start + offset
            gamma = (t + 25) ** -.6
            step_sum += gamma
            q = exposure * a + (1 - exposure) * learner.influence() * learner.b
            observed = np.where(uniform < (1 + q) / 2, 1., -1.)
            # The learner sees neither q nor a nor the environmental share.
            learner.step(observed, gamma)
            q_full = exposure * a + (1 - exposure) * full_predictor
            full_observed = np.where(uniform < (1 + q_full) / 2, 1., -1.)
            full_predictor += gamma * (full_observed - full_predictor)
            if t + 1 in checkpoints:
                error = float(np.max(np.abs(learner.identity_error())))
                max_identity = max(max_identity, error)
                for case_index, spec in enumerate(specifications):
                    indices = slice(case_index * replicates, (case_index + 1) * replicates)
                    weights = learner.influence()[indices]
                    forecasts = learner.b[indices]
                    full = full_predictor[indices]
                    records.append({'case': spec['name'], 'observations_per_run': t + 1,
                                    'cumulative_step': step_sum,
                                    'fine_weight_range': [float(weights.min()), float(weights.max())],
                                    'fine_weight_mean': float(weights.mean()),
                                    'forecast_mean': float(forecasts.mean()),
                                    'environment_forecast_mse': float(np.mean((forecasts - spec['a']) ** 2)),
                                    'single_fine_predictor_mse': float(np.mean((full - spec['a']) ** 2)),
                                    'individual_weights': weights.tolist(),
                                    'individual_forecasts': forecasts.tolist()})
    assert max_identity < 1e-7
    assert np.max(np.abs(learner.b)) <= 1
    answer = {'author': 'Codex (GPT-6)', 'status': 'passed', 'seed': 20261124,
              'parameters': specifications, 'independent_runs_per_case': replicates,
              'steps_per_run': args.steps, 'step_rule': 'gamma_t=(t+25)^(-0.6), eta=1',
              'raw_observations_per_method': len(a) * args.steps,
              'max_pathwise_identity_error': max_identity, 'checkpoints': records,
              'scope': 'One fixed two-concept model. Finite paths illustrate a consistency proof; weak exposure may require far more observations. No expected-score oracle is used by either learner.'}
    encoded = json.dumps(answer, indent=2) + '\n'
    if args.output: args.output.write_text(encoded, encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in answer.items() if k != 'checkpoints'}, indent=2))
    for row in records:
        if row['observations_per_run'] == args.steps:
            print(json.dumps({k: v for k, v in row.items() if not k.startswith('individual')}))


if __name__ == '__main__': main()
