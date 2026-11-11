#!/usr/bin/env python3
"""Finite transfer witness: exact expectations and comparison to classical HSIC.

Codex (GPT-6), November 10, 2026. Uses only the standard library, plus the
explicit worlds from this session's unflagged_assignment.py. No sampling
or floating-point arithmetic enters the identities.
"""
from fractions import Fraction as F
from itertools import permutations, product
import argparse
import json
from pathlib import Path

from unflagged_assignment import sharp_world, world


def signed_difference(a, b, outcomes):
    xa, ya = a
    xb, yb = b
    orientation = int(xa == 0 and xb == 1) - int(xa == 1 and xb == 0)
    return [F(orientation * (int(ya == y) - int(yb == y)), 2)
            for y in range(outcomes)]


def witness(episode, outcomes=2):
    answer = F(0)
    for i, j, k, l in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)):
        a = signed_difference(episode[i], episode[j], outcomes)
        b = signed_difference(episode[k], episode[l], outcomes)
        answer += sum(x * y for x, y in zip(a, b))
    return answer / 3


def song_hsic_kernel(episode):
    """Song et al. (2012), Theorem 3, eq. 11, binary linear X / delta Y."""
    answer = 0
    for s, t, u, v in permutations(range(4)):
        kst = int(episode[s][0] == 0 and episode[t][0] == 0)
        lst = int(episode[s][1] == episode[t][1])
        luv = int(episode[u][1] == episode[v][1])
        lsu = int(episode[s][1] == episode[u][1])
        answer += kst * (lst + luv - 2 * lsu)
    return F(answer, 24)


def expectations(q, f, prior):
    ny = len(f[0][0])
    observations = list(product(range(2), range(ny)))
    empirical = F(0)
    distribution = {}
    for episode in product(observations, repeat=4):
        value = witness(episode, ny)
        probability = F(0)
        for t, mass in enumerate(prior):
            for x, y in episode:
                mass *= q[t][x] * f[t][x][y]
            probability += mass
        empirical += probability * value
        distribution[value] = distribution.get(value, F(0)) + probability
    direct = sum(prior[t] * q[t][0] ** 2 * q[t][1] ** 2
                 * sum((f[t][0][y] - f[t][1][y]) ** 2 for y in range(ny))
                 for t in range(len(q)))
    assert sum(distribution.values()) == 1
    assert empirical == direct
    return {'expectation': str(direct), 'decimal': float(direct),
            'distribution': {str(k): str(v) for k, v in sorted(distribution.items()) if v}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    values = set()
    checked = 0
    # Four possible outcomes represent every equality pattern among four draws.
    for episode in product(list(product(range(2), range(4))), repeat=4):
        v = witness(episode, 4)
        assert v == song_hsic_kernel(episode)
        values.add(v)
        checked += 1
    assert min(values) == F(-1, 6) and max(values) == F(1, 3)
    prior, q, f, _ = sharp_world()
    sharp = expectations(q, f, prior)
    states, q, f = world()
    two_history = expectations(q, f, [F(1, len(states))] * len(states))
    # Same sharply varying assignment with true twins: witness is exactly zero.
    twins = [[[F(1, 2), F(1, 2)]] * 2 for _ in states]
    null = expectations(q, twins, [F(1, len(states))] * len(states))
    assert null['expectation'] == '0'
    answer = {'author': 'Codex (GPT-6)', 'status': 'passed',
              'kernel_comparisons': checked, 'range': [str(min(values)), str(max(values))],
              'sharp_three_history_world': sharp, 'two_history_world': two_history,
              'twin_null': null,
              'interpretation': 'The binary-task witness is exactly the classical unbiased HSIC kernel; no new statistic is claimed.'}
    encoded = json.dumps(answer, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded, encoding='utf-8', newline='\n')
    print(encoded)


if __name__ == '__main__':
    main()
