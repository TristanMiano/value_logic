"""Actual goal coverage versus an imposed score; Codex (GPT-6), 2026-11-12."""
from itertools import product
import json
from pathlib import Path

import numpy as np

from goal_geometry import partitions, determines
from observed_goals import (SEEDS, TRAIN, KAPPA, JOINT_WEIGHTS, observations,
                            fit, validation_scores, population_predictions,
                            population_value)

GAP_LAW = ((0.0, 0.1, 5.0), (0.9, 1.0, 5.0))


def integrated_validation(predictions, observed, law):
    x, goal, y, _ = observed
    total = np.zeros(len(predictions))
    for raw in range(8):
        for j in range(3):
            selected = (x == raw) & (goal == j)
            count, successes = selected.sum(), y[selected].sum()
            for low, high, density in law:
                end = np.clip(predictions[:, raw, j], low, high)
                total += density*(2*(end-low)*successes-(end**2-low**2)*count)
    return total/len(x)


def actual_population(predictions, means, law):
    value = np.zeros_like(predictions)
    for low, high, density in law:
        end = np.clip(predictions, low, high)
        value += density*(means*(end-low)-(end**2-low**2)/2)
    return (value*JOINT_WEIGHTS).sum(axis=2).mean(axis=1)


def main():
    labels = np.array(list(partitions(8)))
    cells = labels.max(axis=1)+1
    charge = KAPPA*(cells-1)
    rows, mixtures = [], []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        hidden = np.array(list(product((0, 1), repeat=3)))[rng.permutation(8)]
        means = 0.2+0.6*hidden
        fitted = fit(labels, observations(rng, means, TRAIN))
        validation = observations(rng, means, 8192)
        x, goal, y, uniform = validation
        prices = np.where(uniform < 0.5, uniform/5, 0.9+(uniform-0.5)/5)
        assert fitted.min() > 0.1 and fitted.max() < 0.9
        population = actual_population(fitted, means, GAP_LAW)-charge
        assert np.allclose(population, 0.45-charge, atol=1e-14)
        for count in (512, 8192):
            sample = tuple(a[:count] for a in (x, goal, y, prices))
            direct, wrong_uniform = validation_scores(fitted, sample)
            correct = integrated_validation(fitted, sample, GAP_LAW)
            assert np.allclose(direct, direct[0], atol=1e-13)
            assert np.allclose(correct, correct[0], atol=1e-13)
            for name, score in (('realized', direct), ('actual_law', correct),
                                ('wrong_uniform_law', wrong_uniform)):
                index = int(np.argmax(score-charge))
                rows.append({'seed': seed, 'validation_n': count, 'judge': name,
                             'cells': int(cells[index]),
                             'actual_population_net': float(population[index]),
                             'exact_hazard': bool(cells[index] == 2 and
                                                  determines(labels[index], hidden[:, 0]))})
        if seed == 0:
            oracle = population_predictions(labels, means)
            uniform_value = population_value(oracle, means)
            gap_value = actual_population(oracle, means, GAP_LAW)
            for epsilon in (0.0, 0.25, 4/9, 0.5, 0.75, 1.0):
                for uses in (1, 2, 4):
                    net = uses*(epsilon*uniform_value+(1-epsilon)*gap_value)-charge
                    best = np.flatnonzero(np.isclose(net, net.max(), atol=1e-12, rtol=0))
                    mixtures.append({'uniform_fraction': epsilon, 'uses': uses,
                                     'optimal_cells': sorted(set(int(cells[i]) for i in best)),
                                     'best_net': float(net.max()),
                                     'constant_net': float(net[0])})
    summary = []
    for count in (512, 8192):
        for name in ('realized', 'actual_law', 'wrong_uniform_law'):
            group = [r for r in rows if r['validation_n'] == count and r['judge'] == name]
            summary.append({'validation_n': count, 'judge': name,
                            'seeds': len(group), 'constant_count': sum(r['cells'] == 1 for r in group),
                            'exact_hazard_count': sum(r['exact_hazard'] for r in group),
                            'mean_actual_population_net': float(np.mean([
                                r['actual_population_net'] for r in group]))})
    result = {'status': 'passed', 'summary': summary, 'mixture_frontier': mixtures,
              'rows': rows, 'interpretation': 'Independent price coverage is changed; learning data access is fixed.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n',
                                                  encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
