"""Directed concepts: exact projections, information and birth dynamics.

Codex (GPT-6), November 11, 2026. Population checks, not an online
estimator of a general adaptively controlled Markov chain.
"""
from fractions import Fraction as Q
from itertools import product
from math import log
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import expit
from coalition_recovery import partitions


def project(matrix, left, right):
    n = len(matrix)
    answer = []
    for x in range(n):
        row = []
        for y in range(n):
            xs = [u for u in range(n) if left[u] == left[x]]
            ys = [v for v in range(n) if right[v] == right[y]]
            row.append(sum((matrix[u][v] for u in xs for v in ys), Q(0))/(len(xs)*len(ys)))
        answer.append(row)
    return answer


def information(matrix):
    n = len(matrix)
    return sum(float(t)*log(float(t)) if t else 0.
               for row in matrix for t in row)/(n*n)


def norm2(matrix):
    n = len(matrix)
    return sum((x*x for row in matrix for x in row), Q(0))/(n*n)


def decision_accuracy(matrix, observed, target):
    """Optimal 0/1 prediction of a fixed target from the observed label."""
    n = len(matrix)
    return sum(max(sum((matrix[x][y]
                        for x in range(n) if observed[x] == left
                        for y in range(n) if target[y] == right), Q(0))
                   for right in set(target))
               for left in set(observed))/(n*n)


def goal_family_gap(matrix, observed):
    """Exact uniform-price decision integral versus predictive squared error."""
    n = len(matrix)
    conditional = [[value/n for value in row] for row in matrix]
    coarse = [[sum((conditional[u][y] for u in range(n)
                   if observed[u] == observed[x]), Q(0))
               /sum(observed[u] == observed[x] for u in range(n))
               for y in range(n)] for x in range(n)]
    squared = sum(((conditional[x][y]-coarse[x][y])**2
                   for x in range(n) for y in range(n)), Q(0))/n
    # Integral_0^1 (p-t)_+ dt = p^2/2. Uniform x and uniform target y.
    value_gap = sum((conditional[x][y]**2-coarse[x][y]**2
                     for x in range(n) for y in range(n)), Q(0))/(2*n*n)
    assert value_gap == squared/(2*n)
    menus = []
    for count in (1, 2, 4, 8, 16):
        prices = [Q(2*j-1, 2*count) for j in range(1, count+1)]
        def payoff(p):
            return sum((max(Q(0), p-price) for price in prices), Q(0))/count
        gap = sum((payoff(conditional[x][y])-payoff(coarse[x][y])
                   for x in range(n) for y in range(n)), Q(0))/(n*n)
        allowance = Q(1, 8*count*count)
        assert gap >= 0 and abs(gap-value_gap) <= allowance
        assert squared <= 2*n*gap + Q(n, 4*count*count)
        menus.append({'prices_per_event': count, 'decision_value_gap': str(gap),
                      'integration_error_bound': str(allowance)})
    return {'partition': observed, 'average_goal_value_gap': str(value_gap),
            'predictive_squared_error': str(squared), 'finite_menus': menus}


def dynamics(a, e, end):
    def derivative(t, state):
        b, odds = state
        w = expit(odds)
        q = e*a+(1-e)*w*b
        return [q-b, (2/3)*(2*b*q-b*b)]
    solution = solve_ivp(derivative, (0., end), [0., log(.01/.99)],
                         method='DOP853', rtol=2e-11, atol=2e-13,
                         dense_output=True, max_step=5.)
    assert solution.success
    samples = []
    for t in sorted(set([0., 100., 500., 1000., end])):
        if t > end:
            continue
        b, odds = solution.sol(t)
        w = expit(odds)
        q = e*a+(1-e)*w*b
        samples.append({'time_after_birth': t, 'b': float(b), 'fine_weight': float(w),
                        'aggregate_correlation': float(w*b),
                        'actual_correlation': float(q),
                        'squared_environment_error': float(2/3*(q-a)**2)})
    assert abs(samples[-1]['b']-a) < 1e-7
    assert samples[-1]['fine_weight'] > 1-1e-7
    return {'environment': a, 'share': e, 'initial_fine_weight': .01,
            'calibration_rate': 1., 'samples': samples}


def main():
    k = [[Q(0), Q(1), Q(-1)], [Q(-1), Q(0), Q(1)], [Q(1), Q(-1), Q(0)]]
    v = [Q(1), Q(-1), Q(0)]
    checks, decisions, goal_checks, decompositions = [], [], [], 0
    for a in (Q(1, 10), Q(3, 5), Q(9, 10), Q(-3, 5)):
        matrix = [[1+a*k[x][y] for y in range(3)] for x in range(3)]
        assert all(sum(row) == 3 and min(row) > 0 for row in matrix)
        assert all(sum(matrix[x][y] for x in range(3)) == 3 for y in range(3))
        full = information(matrix)
        formula = (float(1+a)*log(float(1+a))+float(1-a)*log(float(1-a)))/3
        assert abs(full-formula) < 1e-14
        rows = []
        for c in partitions(3):
            pc = project(matrix, c, c)
            value = information(pc)
            divergence = sum(float(matrix[x][y])*log(float(matrix[x][y]/pc[x][y]))
                             for x in range(3) for y in range(3))/9
            assert abs(full-value-divergence) < 1e-14
            decompositions += 1
            if len(set(c)) < 3:
                assert pc == [[Q(1)]*3 for _ in range(3)] and abs(value) < 1e-14
            rows.append({'partition': c, 'information': value})
            goal_checks.append({'a': str(a), **goal_family_gap(matrix, c)})
        role = project(matrix, (0, 1, 1), (1, 0, 1))
        role_value = information(role)
        assert 0 < role_value < full
        checks.append({'a': str(a), 'full_information': full,
                       'common_partition_values': rows, 'role_binary_information': role_value})
        full_accuracy = decision_accuracy(matrix, (0, 1, 2), (0, 1, 2))
        input_binary_accuracy = decision_accuracy(matrix, (0, 1, 1), (0, 1, 2))
        assert full_accuracy == (1+abs(a))/3
        assert input_binary_accuracy == Q(1, 3)+2*abs(a)/9
        role_accuracy = decision_accuracy(matrix, (0, 1, 1), (1, 0, 1))
        if a > 0:
            assert role_accuracy == max(Q(2, 3), (5+2*a)/9)
        decisions.append({'a': str(a), 'no_context_next_symbol_accuracy': str(Q(1, 3)),
                          'binary_input_full_target_accuracy': str(input_binary_accuracy),
                          'full_input_full_target_accuracy': str(full_accuracy),
                          'role_target_no_context_accuracy': str(Q(2, 3)),
                          'role_target_binary_input_accuracy': str(role_accuracy)})
    robustness = []
    for a, delta in product((Q(1, 5), Q(3, 5)), (Q(1, 100), Q(1, 20))):
        assert delta < a and a+delta < 1
        matrix = [[1+a*k[x][y]+delta*v[x]*v[y] for y in range(3)] for x in range(3)]
        binary_values = [information(project(matrix, c, c))
                         for c in partitions(3) if len(set(c)) == 2]
        upper, lower = Q(4, 9)*delta**2, Q(2, 9)*a**2
        assert max(binary_values) <= float(upper)+1e-14
        assert information(matrix) >= float(lower)-1e-14
        robustness.append({'a': str(a), 'delta': str(delta),
                           'max_binary_information': max(binary_values),
                           'binary_upper_bound': float(upper),
                           'full_information': information(matrix), 'full_lower_bound': float(lower)})
    # General directed projection identity with rational doubly stochastic
    # matrices obtained as mixtures of permutation matrices.
    import itertools
    general_count = 0
    for weights in ((1, 2, 3, 4, 5, 6), (5, 1, 1, 2, 1, 1), (1, 3, 2, 5, 4, 8)):
        matrix = [[Q(0)]*3 for _ in range(3)]
        for weight, permutation in zip(weights, itertools.permutations(range(3))):
            for x, y in enumerate(permutation):
                matrix[x][y] += Q(3*weight, sum(weights))
        for c, d in product(partitions(3), repeat=2):
            projected = project(matrix, c, d)
            gap = information(matrix)-information(projected)
            divergence = sum(float(matrix[x][y])*log(float(matrix[x][y]/projected[x][y]))
                             for x in range(3) for y in range(3))/9
            assert abs(gap-divergence) < 1e-14 and gap >= -1e-14
            assert all(sum(row) == 3 for row in projected)
            assert all(sum(projected[x][y] for x in range(3)) == 3 for y in range(3))
            general_count += 1
    result = {'author': 'Codex (GPT-6)', 'status': 'passed',
              'scope': 'finite population proof checks; no adaptive-chain convergence claim',
              'cycle_information_checks': checks, 'decomposition_count': decompositions,
              'general_role_projection_checks': general_count, 'robustness_checks': robustness,
              'decision_comparisons_exact': decisions,
              'uniform_goal_family_checks_exact': goal_checks,
              'fine_concept_birth': [dynamics(.6, .2, 2000.), dynamics(.6, .05, 30000.)],
              'binary_only_population': 'all projected forecasts remain uniform if initialized there'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'status': 'passed', 'decomposition_count': decompositions,
                      'general_role_projection_checks': general_count,
                      'example': checks[1], 'robustness_checks': robustness,
                      'final_birth_states': [row['samples'][-1] for row in result['fine_concept_birth']]}))


if __name__ == '__main__':
    main()
