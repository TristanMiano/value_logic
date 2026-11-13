"""Observed-data goal judgment; Codex (GPT-6), November 12, 2026.

All experiment choices were recorded in explore.md before the first run.
Only the generator/evaluator sees the hidden context meanings. Fitting and
selection receive raw context labels, sampled goals, outcomes and prices.
Requires NumPy; no training framework or external dataset.
"""
from itertools import product
import json
from pathlib import Path
import platform

import numpy as np

from goal_geometry import partitions, determines

SEEDS = list(range(32))
TRAIN = 8192
VALIDATION = (128, 512, 2048, 8192)
KAPPA = 0.02
GOAL_PROB = np.array([0.5, 0.25, 0.25])
JOINT_WEIGHTS = 2 * GOAL_PROB


def observations(rng, means, count):
    x = rng.integers(0, 8, count)
    goal = rng.choice(3, count, p=GOAL_PROB)
    y = (rng.random(count) < means[x, goal]).astype(float)
    price = rng.random(count)
    return x, goal, y, price


def fit(labels, observed):
    """Return predictions indexed by candidate, raw context and goal."""
    x, goal, y, _ = observed
    count = np.bincount(3*x + goal, minlength=24).reshape(8, 3)
    successes = np.bincount(3*x + goal, weights=y, minlength=24).reshape(8, 3)
    same = labels[:, :, None] == labels[:, None, :]
    cell_count = np.einsum('mxy,yj->mxj', same, count)
    cell_success = np.einsum('mxy,yj->mxj', same, successes)
    return (1 + cell_success)/(2 + cell_count)


def validation_scores(predictions, observed):
    """Two unbiased judges of the same achieved practical payoff."""
    x, goal, y, price = observed
    direct = np.zeros(len(predictions))
    integrated = np.zeros(len(predictions))
    for raw in range(8):
        for j in range(3):
            selected = (x == raw) & (goal == j)
            ys, prices = y[selected], price[selected]
            order = np.argsort(prices)
            sorted_prices = prices[order]
            prefix = np.concatenate(([0.0], np.cumsum(ys[order]-sorted_prices)))
            q = predictions[:, raw, j]
            position = np.searchsorted(sorted_prices, q, side='left')
            direct += 2 * prefix[position]
            integrated += 2*q*ys.sum() - q*q*len(ys)
    return direct/len(x), integrated/len(x)


def population_value(predictions, means):
    return ((means[None, :, :]*predictions - predictions**2/2)
            * JOINT_WEIGHTS[None, None, :]).sum(axis=2).mean(axis=1)


def population_predictions(labels, means):
    same = labels[:, :, None] == labels[:, None, :]
    return np.einsum('mxy,yj->mxj', same, means)/same.sum(axis=2)[:, :, None]


def summarize(rows, name, count):
    subset = [r for r in rows if r['judge'] == name and r['validation_n'] == count]
    net = [r['population_net'] for r in subset]
    return {'judge': name, 'validation_n': count, 'seeds': len(subset),
            'mean_population_net': float(np.mean(net)),
            'min_population_net': float(np.min(net)),
            'max_population_net': float(np.max(net)),
            'mean_population_regret_to_oracle': float(np.mean([
                r['oracle_net']-r['population_net'] for r in subset])),
            'exact_common_hazard_count': sum(r['exact_common_hazard'] for r in subset),
            'retains_hazard_count': sum(r['retains_hazard'] for r in subset),
            'cell_histogram': {str(k): sum(r['cells'] == k for r in subset)
                               for k in range(1, 9)}}


def main():
    labels = np.array(list(partitions(8)), dtype=np.int64)
    cells = labels.max(axis=1)+1
    charges = KAPPA*(cells-1)
    rows, baseline = [], []
    checks = {'candidates': len(labels), 'training_uses_hidden_mean': False,
              'selection_uses_hidden_mean': False, 'direct_formula_spotchecks': 0}
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        hidden = np.array(list(product((0, 1), repeat=3)))[rng.permutation(8)]
        means = 0.2 + 0.6*hidden
        train = observations(rng, means, TRAIN)
        validation = observations(rng, means, max(VALIDATION))
        fitted = fit(labels, train)
        oracle_predictions = population_predictions(labels, means)
        oracle_net = population_value(oracle_predictions, means)-charges
        oracle_index = int(np.argmax(oracle_net))
        assert cells[oracle_index] == 2
        assert determines(labels[oracle_index], hidden[:, 0])
        assert np.isclose(oracle_net[oracle_index], 0.275, atol=1e-14)
        fitted_net = population_value(fitted, means)-charges
        baseline.append({'seed': seed,
                         'constant_population_net': float(fitted_net[0]),
                         'full_population_net': float(fitted_net[-1]),
                         'best_trained_population_net': float(fitted_net.max()),
                         'oracle_net': float(oracle_net.max())})
        for count in VALIDATION:
            sample = tuple(a[:count] for a in validation)
            scores = validation_scores(fitted, sample)
            # Independent literal evaluation of several candidate rules verifies
            # the sorted-prefix acceleration and the integrated-score formula.
            x, goal, y, price = sample
            for index in (0, 1, oracle_index, len(labels)-1):
                q = fitted[index, x, goal]
                literal = np.mean(2*(q > price)*(y-price))
                rb_literal = np.mean(2*q*y-q*q)
                assert np.isclose(scores[0][index], literal, atol=1e-13)
                assert np.isclose(scores[1][index], rb_literal, atol=1e-13)
                checks['direct_formula_spotchecks'] += 1
            for name, score in zip(('realized', 'integrated'), scores):
                index = int(np.argmax(score-charges))
                keeps = determines(labels[index], hidden[:, 0])
                rows.append({'seed': seed, 'judge': name, 'validation_n': count,
                             'partition': labels[index].tolist(), 'cells': int(cells[index]),
                             'retains_hazard': bool(keeps),
                             'exact_common_hazard': bool(keeps and cells[index] == 2),
                             'validation_net': float(score[index]-charges[index]),
                             'population_net': float(fitted_net[index]),
                             'oracle_net': float(oracle_net.max())})
    result = {'status': 'passed', 'contributor': 'Codex (GPT-6)',
              'python': platform.python_version(), 'numpy': np.__version__,
              'contract': {'seeds': SEEDS, 'training_n': TRAIN,
                           'validation_n': VALIDATION, 'kappa': KAPPA,
                           'goal_probabilities': GOAL_PROB.tolist(),
                           'candidate_partitions': len(labels),
                           'observed_labels_when_declining': True,
                           'context_hidden_bits_given_to_learner': False},
              'checks': checks,
              'summary': [summarize(rows, name, count) for count in VALIDATION
                          for name in ('realized', 'integrated')],
              'baseline_summary': {name: float(np.mean([r[name] for r in baseline]))
                                   for name in baseline[0] if name != 'seed'},
              'baselines_by_seed': baseline, 'rows': rows}
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('rows', 'baselines_by_seed')}, indent=2))


if __name__ == '__main__':
    main()
