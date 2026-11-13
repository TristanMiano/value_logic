"""Plastic priorities across changing goals; Codex (GPT-6), 2026-11-12.

Exact finite checks validate the conditional-odds argument. Numerical
trajectories illustrate its population model and two different persistence
mechanisms. No simulated trajectory is an empirical study of human motives.
"""
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import random

import numpy as np


def scalar(q, ratio, up, down):
    return ((1-down)*ratio*q+up*(1-q))/(ratio*q+1-q)


def fixed(ratio, up, down):
    if abs(ratio-1) < 1e-14:
        return up/(up+down)
    a = ratio-1
    b = 1+up-(1-down)*ratio
    roots = ((-b+math.sqrt(b*b+4*a*up))/(2*a),
             (-b-math.sqrt(b*b+4*a*up))/(2*a))
    return next(q for q in roots if 0 < q < 1)


def step_exact(pop, base, ratio, goal_zero, goal_one, up, down):
    """Explicit offspring/retention flow by parent goal, type, next goal/type."""
    size = len(pop)
    new = [[Q(0), Q(0)] for _ in range(size)]
    for g in range(size):
        for kind in (0, 1):
            weight = pop[g][kind]*base[g]*(ratio[g] if kind else 1)
            kernel = goal_one if kind else goal_zero
            for h in range(size):
                for child in (0, 1):
                    mutation = (1-down if child else down) if kind else (up if child else 1-up)
                    new[h][child] += weight*kernel[g][h]*mutation
    total = sum(sum(row) for row in new)
    return [[value/total for value in row] for row in new]


def stochastic_matrix(rng, size):
    rows = [[Q(rng.randint(1, 9)) for _ in range(size)] for _ in range(size)]
    return [[x/sum(row) for x in row] for row in rows]


def exact_checks():
    rng = random.Random(60401)
    count = 0
    for _ in range(400):
        size = rng.choice((2, 3, 4))
        pop = [[Q(rng.randint(1, 9)) for _ in (0, 1)] for _ in range(size)]
        base = [Q(rng.randint(1, 20), 10) for _ in range(size)]
        ratio = [Q(rng.randint(11, 30), 10) for _ in range(size)]
        k0 = stochastic_matrix(rng, size)
        k1 = stochastic_matrix(rng, size)
        overlap = min(k1[g][h]/k0[g][h] for g in range(size) for h in range(size))
        up, down = Q(1, 30), Q(1, 20)
        minimum = min(row[1]/sum(row) for row in pop)
        bound = scalar(minimum, overlap*min(ratio), up, down)
        new = step_exact(pop, base, ratio, k0, k1, up, down)
        assert all(row[1]/sum(row) >= bound for row in new)
        same = step_exact(pop, base, ratio, k0, k0, up, down)
        stronger = scalar(minimum, min(ratio), up, down)
        assert all(row[1]/sum(row) >= stronger for row in same)
        count += 2*size
    return {'random_rational_instances': 400, 'conditional_inequalities': count}


def step(pop, base, ratio, kernel, mu, second_kernel=None):
    selected = pop*base[:, None]
    selected[:, 1] *= ratio
    second_kernel = kernel if second_kernel is None else second_kernel
    migrated = np.column_stack((kernel.T @ selected[:, 0],
                               second_kernel.T @ selected[:, 1]))
    new = np.empty_like(migrated)
    new[:, 0] = (1-mu)*migrated[:, 0]+mu*migrated[:, 1]
    new[:, 1] = mu*migrated[:, 0]+(1-mu)*migrated[:, 1]
    return new/new.sum()


def main():
    checks = exact_checks()
    mu = 0.02
    base = np.array([1.0, 1.2, 0.8])
    ratios = np.array([1.1, 1.4, 2.0])
    kernel = np.array([[0.8, 0.1, 0.1], [0.15, 0.7, 0.15], [0.2, 0.1, 0.7]])
    pop = np.full((3, 2), 1/6)
    for _ in range(2000):
        pop = step(pop, base, ratios, kernel, mu)
    # Compare iterated normalized reproduction with the independently assembled
    # positive transition/retention matrix's Perron eigenvector.
    matrix = np.zeros((6, 6))
    for g in range(3):
        for kind in (0, 1):
            for h in range(3):
                for child in (0, 1):
                    matrix[2*g+kind, 2*h+child] = (base[g]*(ratios[g] if kind else 1)
                        * kernel[g, h]*(1-mu if kind == child else mu))
    eigenvalues, eigenvectors = np.linalg.eig(matrix.T)
    vector = eigenvectors[:, np.argmax(eigenvalues.real)].real
    vector /= vector.sum()
    assert np.max(np.abs(vector.reshape(3, 2)-pop)) < 1e-12
    conditional = pop[:, 1]/pop.sum(axis=1)
    assert conditional.min() >= fixed(ratios.min(), mu, mu)-1e-12
    stationary = {'goal_masses': pop.sum(axis=1).tolist(),
                  'conditional_priority': conditional.tolist(),
                  'overall_priority': float(pop[:, 1].sum()),
                  'uniform_lower_limit': fixed(ratios.min(), mu, mu),
                  'matrix_eigenvector_error': float(np.max(np.abs(vector.reshape(3, 2)-pop)))}

    # Goal fitness and goal-revision kernels change every round. They are shared
    # by the two priority types; the priority ratios stay above 1.1.
    rng = np.random.default_rng(60402)
    pop = np.array([[0.2, 0.01], [0.3, 0.09], [0.1, 0.3]])
    lower = min(pop[:, 1]/pop.sum(axis=1))
    trajectory = []
    for t in range(600):
        base = rng.uniform(0.05, 3, 3)
        ratios = rng.uniform(1.1, 2.5, 3)
        kernel = rng.uniform(0.01, 1, (3, 3))
        kernel /= kernel.sum(axis=1, keepdims=True)
        pop = step(pop, base, ratios, kernel, mu)
        lower = scalar(lower, 1.1, mu, mu)
        conditional = pop[:, 1]/pop.sum(axis=1)
        assert conditional.min() >= lower-1e-12
        trajectory.append({'round': t+1, 'goal_masses': pop.sum(axis=1).tolist(),
                           'conditional_priority': conditional.tolist(),
                           'comparison_lower_bound': lower})

    # A capability favored in nine of ten contexts can still lose on cumulative
    # multiplicative retention. This is a deterministic, exactly checked cycle.
    q_exact = Q(1, 2)
    cycle_ratios = [Q(2)]*9+[Q(1, 1024)]
    for ratio in cycle_ratios:
        q_exact = scalar(q_exact, ratio, Q(0), Q(0))
    assert q_exact == Q(1, 3)
    reversal = {'favorable_context_fraction': '9/10', 'retention_product': '1/2',
                'initial_priority': '1/2', 'after_one_cycle': str(q_exact)}

    # Goal revision that sorts the priority types into different environments
    # can overwhelm their within-goal advantage. Restore overlap as a repair.
    sorting = []
    for overlap in (0.0, 0.8, 1.0):
        pop = np.full((2, 2), 0.25)
        k0 = np.array([[1.0, 0.0], [1.0, 0.0]])
        k1 = np.array([[overlap, 1-overlap], [overlap, 1-overlap]])
        for _ in range(2000):
            pop = step(pop, np.array([100.0, 1.0]), np.array([2.0, 2.0]), k0, mu, k1)
        occupied = pop.sum(axis=1) > 0
        conditional = pop[occupied, 1]/pop[occupied].sum(axis=1)
        lower_limit = fixed(2*overlap, mu, mu) if overlap > 0 else None
        if lower_limit is not None:
            assert conditional.min() >= lower_limit-1e-12
        sorting.append({'goal_overlap': overlap, 'goal_masses': pop.sum(axis=1).tolist(),
                        'conditional_priority_occupied': conditional.tolist(),
                        'overall_priority': float(pop[:, 1].sum()),
                        'guaranteed_lower_limit': lower_limit})

    # Compare revision rates by actual long-run retention. The fixed-advantage
    # case favors reduced revision; switching advantage can favor flexibility.
    mutation_grid = (0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5)
    growth = []
    for revision in mutation_grid:
        mutation = np.array([[1-revision, revision], [revision, 1-revision]])
        forward = np.diag([1.0, 4.0]) @ mutation
        reverse = np.diag([4.0, 1.0]) @ mutation
        constant = float(np.linalg.eigvals(forward).real.max())
        growth.append({'revision': revision, 'environment': 'constant', 'per_round_growth': constant})
        for length in (1, 5, 20, 100):
            cycle = np.linalg.matrix_power(forward, length) @ np.linalg.matrix_power(reverse, length)
            rate = float(np.linalg.eigvals(cycle).real.max()**(1/(2*length)))
            growth.append({'revision': revision, 'environment': f'alternating_blocks_{length}',
                           'per_round_growth': rate})
    constant_rates = [r['per_round_growth'] for r in growth if r['environment'] == 'constant']
    assert all(a > b for a, b in zip(constant_rates, constant_rates[1:]))
    best_rates = [max((r for r in growth if r['environment'] == environment),
                      key=lambda r: r['per_round_growth'])
                  for environment in ('constant', 'alternating_blocks_1', 'alternating_blocks_5',
                                      'alternating_blocks_20', 'alternating_blocks_100')]

    # Neutral intervention: remove every priority-dependent retention advantage.
    initial = fixed(2.0, mu, mu)
    neutral = []
    q = initial
    for t in range(201):
        assert abs(q-(0.5+(initial-0.5)*(1-2*mu)**t)) < 1e-12
        if t in (0, 10, 25, 50, 100, 200):
            neutral.append({'round': t, 'priority': q})
        q = scalar(q, 1.0, mu, mu)

    # Frequency-dependent reinforcement can preserve either convention after
    # an initiating advantage is removed. Values are still revisable.
    feedback = []
    for strength in (0.04, 0.5):
        for start in (0.1, 0.499, 0.5, 0.501, 0.9):
            q = start
            for _ in range(3000):
                q = scalar(q, math.exp(strength*(2*q-1)), mu, mu)
            feedback.append({'coordination_strength': strength, 'initial': start, 'limit': q})
    result = {'status': 'passed', 'checks': checks, 'mutation': mu,
              'stationary': stationary,
              'changing_goals': {'rounds': len(trajectory), 'last': trajectory[-1],
                                 'minimum_slack': min(min(r['conditional_priority'])-
                                                       r['comparison_lower_bound'] for r in trajectory)},
              'majority_reversal': reversal,
              'goal_sorting': sorting,
              'revision_comparison': growth, 'best_tested_revision': best_rates,
              'asymmetric_revision': {'ratio': 2.0, 'up': 0.01, 'down': 0.4,
                                      'fixed_priority': fixed(2.0, 0.01, 0.4)},
              'neutral_intervention': neutral,
              'neutral_half_life': math.log(0.5)/math.log(1-2*mu),
              'coordination_threshold': 4*mu/(1-2*mu), 'coordination': feedback,
              'trajectory': trajectory[::10]+[trajectory[-1]]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n',
                                                  encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'trajectory'}, indent=2))


if __name__ == '__main__':
    main()
