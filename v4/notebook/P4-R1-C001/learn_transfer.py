#!/usr/bin/env python3
"""Observed-data transfer recovery with the four-performance witness.

Codex (GPT-6), November 10, 2026. The learner receives task and result
arrays only. Hidden states and the truth partition are used by the generator
and final evaluation, never by the estimator or confidence calculation.
Requires NumPy. This deliberately simple estimator has no optimality claim.
"""
from fractions import Fraction as F
from itertools import combinations
import argparse
import json
from math import log, sqrt
from pathlib import Path

import numpy as np


def generate(n, seed):
    rng = np.random.default_rng(seed)
    state = rng.integers(0, 2, n)
    q = np.array([[.3, .2, .2, .3], [.2, .3, .3, .2]])
    uniforms = rng.random((n, 4))
    tasks = np.zeros((n, 4), dtype=np.int8)
    for cutoff in np.cumsum(q, axis=1)[:, :-1].T:
        tasks += uniforms > cutoff[state, None]
    first_kind_success = np.where(state == 0, .9, .1)[:, None]
    probabilities = np.where(tasks < 2, first_kind_success, 1 - first_kind_success)
    results = (rng.random((n, 4)) < probabilities).astype(np.int8)
    return tasks, results


def recover(tasks, results, alphabet_size, checkpoints, alpha=.05):
    """Estimate each pair's witness; conservative components may under-refine."""
    pairs = list(combinations(range(alphabet_size), 2))
    sums = {}
    for a, b in pairs:
        is_a, is_b = tasks == a, tasks == b
        eligible = (is_a.sum(axis=1) == 2) & (is_b.sum(axis=1) == 2)
        positive_a = (is_a * results).sum(axis=1)
        positive_b = (is_b * results).sum(axis=1)
        plus = eligible & (((positive_a == 2) & (positive_b == 0))
                           | ((positive_a == 0) & (positive_b == 2)))
        minus = eligible & (positive_a == 1) & (positive_b == 1)
        # Six times K, exactly integer valued for binary outcomes.
        scaled = 2 * plus.astype(np.int64) - minus.astype(np.int64)
        cumulative = np.cumsum(scaled)
        sums[(a, b)] = {n: int(cumulative[n - 1]) for n in checkpoints}
    records = []
    for n in checkpoints:
        radius = sqrt((n + 1) * log((n + 1) * len(pairs) ** 2 / alpha ** 2)) / (4 * n)
        estimates = {pair: sums[pair][n] / (6 * n) for pair in pairs}
        separated = {pair for pair, value in estimates.items() if value > radius}
        # A true twin edge remains on the confidence event. Components of
        # remaining edges therefore never split twins, but can delay using
        # already-certified distinctions until intervening edges disappear.
        parent = list(range(alphabet_size))
        def root(a):
            while a != parent[a]:
                a = parent[a]
            return a
        for a, b in pairs:
            if (a, b) not in separated:
                parent[root(b)] = root(a)
        labels = [root(a) for a in range(alphabet_size)]
        mapping = {v: i for i, v in enumerate(dict.fromkeys(labels))}
        labels = [mapping[x] for x in labels]
        records.append({'independent_episodes': n, 'raw_performances': 4 * n,
                        'simultaneous_radius': radius,
                        'estimates': {f'{a},{b}': value for (a, b), value in estimates.items()},
                        'certified_distinctions': [list(pair) for pair in sorted(separated)],
                        'conservative_partition': labels})
    return records


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path); args = p.parse_args()
    seed = 20261110
    checkpoints = [1000, 10000, 100000, 500000]
    tasks, results = generate(checkpoints[-1], seed)
    records = recover(tasks, results, 4, checkpoints)
    q = [[F(3, 10), F(2, 10), F(2, 10), F(3, 10)],
         [F(2, 10), F(3, 10), F(3, 10), F(2, 10)]]
    truth = [0, 0, 1, 1]
    target = {}
    for a, b in combinations(range(4), 2):
        target[f'{a},{b}'] = (sum((qt[a] * qt[b]) ** 2 for qt in q) * F(16, 25)
                              if truth[a] != truth[b] else F(0))
    minimum = min(x for x in target.values() if x)
    covered = all(abs(row['estimates'][pair] - float(value)) <= row['simultaneous_radius']
                  for row in records for pair, value in target.items())
    assert records[-1]['conservative_partition'] == truth
    assert 2 * records[-1]['simultaneous_radius'] < float(minimum)
    answer = {'author': 'Codex (GPT-6)', 'status': 'passed', 'seed': seed,
              'learner_inputs': ['task labels in four-performance groups', 'binary outcomes', 'alphabet size', 'confidence level'],
              'simultaneous_confidence': .95,
              'population_pair_values_for_evaluation': {k: str(v) for k, v in target.items()},
              'minimum_positive_pair_value': str(minimum),
              'coverage_at_recorded_checkpoints': covered, 'records': records,
              'scope': 'Fixed finite alphabet; grouped conditionally iid observations. No latent-state estimation, general ontology invention, or optimal sample-cost claim.'}
    encoded = json.dumps(answer, indent=2) + '\n'
    if args.output: args.output.write_text(encoded, encoding='utf-8', newline='\n')
    print(encoded)


if __name__ == '__main__': main()
