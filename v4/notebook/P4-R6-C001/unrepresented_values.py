"""Survival filtering and actual policy cloning; Codex (GPT-6), W6.

Learners see first actions and end-of-trial retention flags only. The exact
model is reserved for evaluation and finite mathematical checks.
"""
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path

import numpy as np


K = [[F(3, 5), F(2, 5)], [F(1, 10), F(3, 5)]]


def matvec(k, v):
    return [sum(x*y for x, y in zip(row, v)) for row in k]


def exact_messages(goal, n):
    h = [list(map(F, goal))]
    for _ in range(n):
        h.append(matvec(K, h[-1]))
    return h


def exact_conditioned(goal, n):
    h = exact_messages(goal, n)
    return [[K[i][j]*h[n-1][j]/h[n][i] for j in range(2)] for i in range(2)]


def finite_checks():
    limit = [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]
    inequalities = 0
    for a, b in product(range(5), repeat=2):
        if a+b == 0:
            continue
        for n in (1, 2, 4, 8, 16):
            q = exact_conditioned((a, b), n)
            bound = F(3, 4)*F(1, 2)**n/(1-F(1, 2)**n)
            for i in range(2):
                assert sum(q[i]) == 1
                assert sum(abs(q[i][j]-limit[i][j]) for j in range(2))/2 <= bound
                inequalities += 1
    enumerated = 0
    for goal in ((1, 1), (9, 1), (1, 9)):
        for n in (2, 4, 8):
            q = exact_conditioned(goal, n)
            h = exact_messages(goal, n)
            for initial in (0, 1):
                by_first = [F(0), F(0)]
                for tail in product(range(2), repeat=n):
                    path = (initial,)+tail
                    weight = F(goal[tail[-1]])
                    for i, j in zip(path, path[1:]):
                        weight *= K[i][j]
                    by_first[tail[0]] += weight
                    enumerated += 1
                assert sum(by_first) == h[n][initial]
                assert [x/sum(by_first) for x in by_first] == q[initial]
    return {'terminal_bias_bound_checks': inequalities,
            'exact_paths_enumerated': enumerated,
            'ten_step_bound': str(F(3, 4)*F(1, 2)**10/(1-F(1, 2)**10))}


def gibbs_check():
    rng = np.random.default_rng(61201)
    p = np.array([[0.6, 0.4], [1/7, 6/7]])
    survival = np.array([1.0, 0.7])
    paths = [(0,)+x for x in product(range(2), repeat=5)]
    baseline, weights = [], []
    for path in paths:
        baseline.append(math.prod(p[i, j] for i, j in zip(path, path[1:])))
        weights.append(math.prod(survival[i] for i in path[:-1])*(9 if path[-1] == 0 else 1))
    baseline, weights = np.array(baseline), np.array(weights)
    z = float(baseline @ weights)
    selected = baseline*weights/z
    max_error = 0.0
    for _ in range(200):
        q = rng.dirichlet(np.ones(len(paths)))
        lhs = q @ np.log(weights)-q @ np.log(q/baseline)
        rhs = math.log(z)-q @ np.log(q/selected)
        max_error = max(max_error, abs(lhs-rhs))
        assert abs(lhs-rhs) < 5e-14 and lhs <= math.log(z)+1e-14
    return {'path_variational_checks': 200, 'maximum_identity_error': max_error}


def learn_by_retaining_first_actions(rng, goal, horizon, attempts):
    p_a = np.array([0.6, 1/7])
    survival = np.array([1.0, 0.7])
    learned, counts = [], []
    for initial in (0, 1):
        state = np.full(attempts, initial, dtype=np.int8)
        alive = np.ones(attempts, dtype=bool)
        first = None
        for t in range(horizon):
            alive &= rng.random(attempts) < survival[state]
            state = (rng.random(attempts) >= p_a[state]).astype(np.int8)
            if t == 0:
                first = state.copy()
        terminal_accept = np.asarray(goal, dtype=float)/max(goal)
        alive &= rng.random(attempts) < terminal_accept[state]
        c = np.bincount(first[alive], minlength=2)
        learned.append((c+1)/(c.sum()+2))
        counts.append(c.tolist())
    return np.array(learned), counts


def survival_at(policy, horizon):
    killed = np.array([1.0, 0.7])[:, None]*policy
    return (np.linalg.matrix_power(killed, horizon) @ np.ones(2)).tolist()


def clone_experiment():
    attempts, repetitions, deployment = 65536, 16, 32
    limit = np.array([[0.75, 0.25], [0.25, 0.75]])
    rows = []
    for horizon in (2, 4, 8, 12):
        for goal in ((1, 1), (9, 1), (1, 9)):
            target = np.array(exact_conditioned(goal, horizon), dtype=float)
            runs = []
            for seed in range(61210, 61210+repetitions):
                # Distinct independent training randomness across settings.
                rng = np.random.default_rng(np.random.SeedSequence([seed, horizon, *goal]))
                learned, counts = learn_by_retaining_first_actions(rng, goal, horizon, attempts)
                err = np.abs(learned-target).sum(axis=1).max()/2
                runs.append({'seed': seed, 'accepted_first_actions': counts,
                             'learned_policy': learned.tolist(),
                             'max_row_tv_to_finite_target': float(err),
                             'survival': survival_at(learned, deployment)})
            mean_policy = np.mean([r['learned_policy'] for r in runs], axis=0)
            viability = np.array([r['survival'] for r in runs])
            rows.append({'training_horizon': horizon, 'terminal_weight': list(goal),
                         'finite_selected_policy': target.tolist(),
                         'mean_learned_policy': mean_policy.tolist(),
                         'finite_target_tv_to_limit': float(np.abs(target-limit).sum(axis=1).max()/2),
                         'mean_max_row_tv_estimation_error': float(np.mean([r['max_row_tv_to_finite_target'] for r in runs])),
                         'mean_survival': viability.mean(axis=0).tolist(),
                         'survival_standard_error': (viability.std(axis=0, ddof=1)/math.sqrt(repetitions)).tolist(),
                         'mean_accepted_per_start': np.mean([[sum(c) for c in r['accepted_first_actions']] for r in runs], axis=0).tolist(),
                         'runs': runs})
    baseline = np.array([[0.6, 0.4], [1/7, 6/7]])
    optimal = np.array([[1.0, 0.0], [1.0, 0.0]])
    return {'attempted_trials_per_start_per_setting_per_seed': attempts,
            'replicas': repetitions, 'deployment_horizon': deployment,
            'total_attempted_training_trials': attempts*2*len(rows)*repetitions,
            'baseline_survival': survival_at(baseline, deployment),
            'limit_controller_survival': survival_at(limit, deployment),
            'unconstrained_survival_optimum': survival_at(optimal, deployment),
            'settings': rows}


def main():
    out = {'status': 'passed', 'finite': finite_checks(), 'gibbs': gibbs_check(),
           'cloning': clone_experiment()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8',newline='\n')
    print(json.dumps({'status': out['status'], 'finite': out['finite'], 'gibbs': out['gibbs'],
                      'training_trials': out['cloning']['total_attempted_training_trials']}))


if __name__ == '__main__':
    main()
