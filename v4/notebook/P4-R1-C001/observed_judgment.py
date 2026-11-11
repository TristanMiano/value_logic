#!/usr/bin/env python3
"""Implemented W1 composition: discover a partition, validate, fit, predict.

Codex (GPT-6), November 10, 2026. NumPy/SciPy. Independent data stages
separate concept proposal, witness validation, and conditional forecasting.
Includes a full-label count baseline with the same total observations and
a favorable two-component grouped-mixture EM comparator. True laws are used
only for exact finite-world evaluation after fitting.
"""
from collections import defaultdict
from itertools import product
import argparse
import json
from math import log, sqrt
from pathlib import Path

import numpy as np
from scipy.special import logsumexp

from learn_transfer import generate, recover


def input_codes(tasks, results, partition):
    labels = np.asarray(partition)[tasks]
    k = max(partition) + 1
    codes = np.zeros(len(tasks), dtype=np.int64)
    for j in range(3): codes = codes * (2 * k) + 2 * labels[:, j] + results[:, j]
    return codes * k + labels[:, 3], k ** 4 * 8


def fit_table(tasks, results, partition):
    codes, size = input_codes(tasks, results, partition)
    counts = np.bincount(2 * codes + results[:, 3], minlength=2 * size).reshape(size, 2)
    probabilities = (counts + 1) / (counts.sum(axis=1, keepdims=True) + 2)
    return probabilities, counts


def grouped_counts(tasks, results):
    observations = 2 * tasks + results
    counts = np.zeros((len(tasks), 8), dtype=np.int8)
    for j in range(4): counts[np.arange(len(tasks)), observations[:, j]] += 1
    patterns, multiplicity = np.unique(counts, axis=0, return_counts=True)
    return patterns.astype(float), multiplicity.astype(float)


def fit_grouped_mixture(tasks, results, components=2):
    patterns, multiplicity = grouped_counts(tasks, results)
    n = len(tasks)
    fits = []
    for seed in range(6):
        rng = np.random.default_rng(8100 + seed)
        g = rng.dirichlet(np.ones(8), size=components)
        weights = np.full(components, 1 / components)
        old = -np.inf
        for iteration in range(1000):
            log_joint = patterns @ np.log(g).T + np.log(weights)
            log_mass = logsumexp(log_joint, axis=1)
            likelihood = float(multiplicity @ log_mass)
            assert likelihood >= old - 1e-6
            if iteration and likelihood - old < 1e-10 * max(1, abs(likelihood)):
                break
            old = likelihood
            responsibilities = np.exp(log_joint - log_mass[:, None]) * multiplicity[:, None]
            weights = responsibilities.sum(axis=0) / n
            g = responsibilities.T @ patterns
            g = np.maximum(g, 1e-12)
            g /= g.sum(axis=1, keepdims=True)
        fits.append((likelihood, weights.copy(), g.copy(), iteration + 1))
    best = max(fits, key=lambda x: x[0])
    return best, {'components_supplied': components, 'independent_parameters': components * 7 + components - 1,
                  'unordered_group_patterns': len(patterns),
                  'initializations': len(fits), 'iterations': [x[3] for x in fits],
                  'log_likelihoods': [x[0] for x in fits],
                  'scope': 'Correct two-component iid mixture class supplied; no proof of a global EM optimum.'}


def population():
    q = np.array([[.3, .2, .2, .3], [.2, .3, .3, .2]])
    success = np.array([[.9, .9, .1, .1], [.1, .1, .9, .9]])
    g = np.stack((q * (1 - success), q * success), axis=2)
    observations = list(product(range(4), range(2)))
    tasks, results, mass = [], [], []
    for episode in product(observations, repeat=4):
        xs, ys = zip(*episode)
        probability = .5 * sum(np.prod([g[t, x, y] for x, y in episode]) for t in range(2))
        tasks.append(xs); results.append(ys); mass.append(probability)
    assert abs(sum(mass) - 1) < 1e-12
    return np.array(tasks), np.array(results), np.array(mass), g


def evaluate_table(probabilities, partition, tasks, results, mass):
    codes, _ = input_codes(tasks, results, partition)
    return float(mass @ np.log(probabilities[codes, results[:, 3]]))


def oracle_table(partition, tasks, results, mass):
    codes, size = input_codes(tasks, results, partition)
    joint = np.bincount(2 * codes + results[:, 3], weights=mass, minlength=2 * size).reshape(size, 2)
    probabilities = joint / joint.sum(axis=1, keepdims=True)
    return probabilities


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path); args = p.parse_args()
    selection = generate(100000, 20261120)
    proposal_record = recover(*selection, 4, [100000], alpha=.025)[0]
    partition = proposal_record['conservative_partition']
    # This outcome is checked, not supplied to the recovery algorithm.
    assert partition == [0, 0, 1, 1]
    validation = generate(5000, 20261121)
    compressed_tasks = np.asarray(partition)[validation[0]]
    validation_record = recover(compressed_tasks, validation[1], 2, [5000], alpha=.025)[0]
    mean = validation_record['estimates']['0,1']
    lower = max(0., mean - validation_record['simultaneous_radius'])
    oracle_gain_lower = 2 * lower ** 2
    training = generate(20000, 20261122)
    learned, learned_counts = fit_table(*training, partition)
    inputs = len(learned)
    expected_estimation_bound = inputs / (len(training[0]) + 1)
    forecast_gain_certificate = oracle_gain_lower - expected_estimation_bound
    all_tasks = np.concatenate([d[0] for d in (selection, validation, training)])
    all_results = np.concatenate([d[1] for d in (selection, validation, training)])
    full_partition, coarse_partition = list(range(4)), [0] * 4
    full_equal_training, _ = fit_table(*training, full_partition)
    full_equal_total, full_counts = fit_table(all_tasks, all_results, full_partition)
    coarse, _ = fit_table(all_tasks, all_results, coarse_partition)
    mixture, mixture_metadata = fit_grouped_mixture(all_tasks, all_results)
    tasks, results, mass, true_g = population()
    oracle_full = oracle_table(full_partition, tasks, results, mass)
    oracle_learned = oracle_table(partition, tasks, results, mass)
    oracle_coarse = oracle_table(coarse_partition, tasks, results, mass)
    base_score = evaluate_table(oracle_coarse, coarse_partition, tasks, results, mass)
    values = {}
    for name, probs, part in (
            ('coarse_all_data', coarse, coarse_partition),
            ('learned_partition_independent_training', learned, partition),
            ('full_labels_equal_training_only', full_equal_training, full_partition),
            ('full_labels_equal_total_data', full_equal_total, full_partition),
            ('oracle_learned_partition', oracle_learned, partition),
            ('oracle_full_labels', oracle_full, full_partition)):
        score = evaluate_table(probs, part, tasks, results, mass)
        values[name] = {'expected_log_score': score, 'gain_over_oracle_coarse_nats': score - base_score,
                        'conditional_table_entries': int(probs.size)}
    _, weights, flat_g, _ = mixture
    fitted_g = flat_g.reshape(2, 4, 2)
    history_log = np.log(weights)[None, :] + sum(np.log(fitted_g[:, tasks[:, j], results[:, j]]).T for j in range(3))
    # History posterior times the target's joint task/outcome probabilities.
    target_logs = history_log + np.log(fitted_g[:, tasks[:, 3], results[:, 3]]).T
    target_input_logs = history_log + np.log(fitted_g.sum(axis=2)[:, tasks[:, 3]]).T
    mixture_score = float(mass @ (logsumexp(target_logs, axis=1) - logsumexp(target_input_logs, axis=1)))
    values['grouped_two_component_em_equal_total_data'] = {
        'expected_log_score': mixture_score, 'gain_over_oracle_coarse_nats': mixture_score - base_score,
        'metadata': mixture_metadata, 'fitted_weights': weights.tolist(),
        'fitted_joint_laws': flat_g.tolist()}
    assert values['learned_partition_independent_training']['gain_over_oracle_coarse_nats'] > 0
    assert forecast_gain_certificate > 0
    answer = {'author': 'Codex (GPT-6)', 'status': 'passed',
              'stage_sizes_episodes': {'proposal': len(selection[0]), 'validation': len(validation[0]), 'training': len(training[0])},
              'total_raw_performances': 4 * len(all_tasks),
              'selected_partition': partition, 'proposal_record': proposal_record,
              'independent_validation': validation_record,
              'validated_witness_lower_bound': lower,
              'oracle_gain_lower_bound_nats': oracle_gain_lower,
              'expected_training_regret_bound': expected_estimation_bound,
              'gain_lower_bound_in_expectation_over_independent_training': forecast_gain_certificate,
              'confidence_scope': 'Witness bound has 97.5% coverage conditional on the proposal; the training term is an expectation, not a confidence claim for one fitted table.',
              'comparisons': values,
              'marginal_success_rates': (true_g[:, :, 1].mean(axis=0) / true_g.sum(axis=2).mean(axis=0)).tolist(),
              'scope': 'Finite alphabet, four-attempt episodes. The grouped-mixture comparator uses additional correct latent-class assumptions. All acquisition counts are explicit.'}
    encoded = json.dumps(answer, indent=2) + '\n'
    if args.output: args.output.write_text(encoded, encoding='utf-8', newline='\n')
    print(encoded)


if __name__ == '__main__': main()
