"""Mixed-goal priority dynamics. Codex (GPT-6), November 12, 2026.

Checks finite identities and inequalities independently of the stated proofs;
Monte Carlo summaries illustrate invariant distributions, not human data.
"""
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import random

import numpy as np


def update(q, ratio, mu):
    selected = ratio*q/(ratio*q+1-q)
    return mu+(1-2*mu)*selected


def logit(q):
    return np.log(q)-np.log1p(-q)


def exact_checks():
    rng = random.Random(61101)
    count = 0
    for _ in range(800):
        mu = Q(rng.randint(1, 49), 100)
        s = Q(rng.randint(1, 99), 100)
        c = 1-2*mu
        out = mu+c*s
        assert out*(1-out)-s*(1-s) == mu*(1-mu)*(2*s-1)**2
        assert 0 < c*s*(1-s)/(out*(1-out)) <= c
        q = Q(rng.randint(1, 99), 100)
        r = Q(rng.randint(1, 20), rng.randint(1, 20))
        after = update(q, r, Q(0))
        assert after/(1-after) == r*q/(1-q)
        assert update(1-q, 1/r, mu) == 1-update(q, r, mu)
        count += 4
    return {'rational_instances': 800, 'identities_and_inequalities': count}


def coupling_checks():
    rng = np.random.default_rng(61102)
    checked = 0
    results = []
    for mu in (0.005, 0.02, 0.1):
        c = 1-2*mu
        for delta in (0.0, 0.01, 0.1):
            q, other = 0.01, 0.99
            bound = abs(float(logit(q)-logit(other)))
            for _ in range(1000):
                lr = float(rng.uniform(-1.5, 1.5))
                change = float(rng.uniform(-delta, delta))
                q = update(q, math.exp(lr), mu)
                other = update(other, math.exp(lr+change), mu)
                bound = c*(bound+delta)
                assert abs(float(logit(q)-logit(other))) <= bound+3e-12
                checked += 1
            results.append({'mu': mu, 'log_advantage_tolerance': delta,
                            'final_log_odds_gap': abs(float(logit(q)-logit(other))),
                            'proved_bound': bound})
    return {'checked_steps': checked, 'settings': results}


def invariant_examples():
    # Common uniforms provide the monotone comparison across p. Independent
    # copies at the same p test distributional versus pathwise agreement.
    rng = np.random.default_rng(61103)
    ps = np.array([0.4, 0.5, 0.6])
    replicas, burn, rounds = 32, 2000, 24000
    rows = []
    for mu in (0.005, 0.02, 0.1):
        qs = np.full((len(ps), replicas), 0.5)
        private = np.full(replicas, 0.5)
        total = np.zeros_like(qs)
        per_replica_square = np.zeros_like(qs)
        below = np.zeros_like(qs)
        disagreement = 0.0
        # Sparse samples keep this checker and its committed output small.
        samples = [[] for _ in ps]
        for t in range(burn+rounds):
            u = rng.random(replicas)
            ratio = np.where(u[None, :] < ps[:, None], 2.0, 0.5)
            qs = update(qs, ratio, mu)
            private = update(private, np.where(rng.random(replicas) < 0.6, 2.0, 0.5), mu)
            assert np.all(qs[0] <= qs[1]+1e-14) and np.all(qs[1] <= qs[2]+1e-14)
            if t >= burn:
                total += qs
                per_replica_square += qs**2
                below += qs > 0.5
                disagreement += float(np.abs(qs[2]-private).mean())
                if t % 40 == 0:
                    for j in range(len(ps)):
                        samples[j].extend(qs[j].tolist())
        for j, p in enumerate(ps):
            means = total[j]/rounds
            mean = float(means.mean())
            rows.append({'mu': mu, 'favorable_goal_probability': float(p),
                         'mean_priority': mean,
                         'replicate_mean_standard_error': float(means.std(ddof=1)/math.sqrt(replicas)),
                         'fraction_priority_above_half': float(below[j].mean()/rounds),
                         'sd_priority': math.sqrt(float(per_replica_square[j].mean()/rounds)-mean**2),
                         'sampled_quantiles_10_50_90': np.quantile(samples[j], [0.1, 0.5, 0.9]).tolist(),
                         'independent_stream_mean_absolute_gap_at_p_06': disagreement/rounds if p == 0.6 else None})
    return {'seed': 61103, 'replicas': replicas, 'burn_in': burn,
            'sample_rounds': rounds, 'ratio_pair': [2.0, 0.5], 'settings': rows}


def population_examples():
    rho = np.array([0.4, 0.6])
    kernel = np.tile(rho, (2, 1))
    multipliers = np.array([[1.0, 2.0], [1.0, 0.5]])
    matrix_rows = []
    for mu in (0.1, 0.02, 0.005, 0.001, 0.0001):
        matrix = np.empty((4, 4))
        for g in range(2):
            for kind in range(2):
                for h in range(2):
                    for child in range(2):
                        matrix[2*g+kind, 2*h+child] = (multipliers[g, kind]*kernel[g, h]
                            * (1-mu if kind == child else mu))
        ev, vectors = np.linalg.eig(matrix.T)
        k = np.argmax(ev.real)
        vector = vectors[:, k].real
        vector /= vector.sum()
        pop = np.full(4, 0.25)
        for _ in range(1000):
            pop = pop @ matrix
            pop /= pop.sum()
        assert np.max(np.abs(pop-vector)) < 1e-11
        conditional = vector.reshape(2, 2)[:, 1]/vector.reshape(2, 2).sum(axis=1)
        matrix_rows.append({'mu': mu, 'growth': float(ev[k].real),
                            'overall_priority': float(vector[1::2].sum()),
                            'conditional_priority': conditional.tolist()})
    assert matrix_rows[-1]['overall_priority'] > 0.998
    assert Q(2, 5)*2+Q(3, 5)*Q(1, 2) == Q(11, 10)
    # Five shared goals with two favorable and three unfavorable give a
    # multiplier 1/2, rather than the population average multiplier 11/10.
    q = Q(1, 2)
    for r in (Q(2), Q(2), Q(1, 2), Q(1, 2), Q(1, 2)):
        q = update(q, r, Q(0))
    assert q == Q(1, 3)
    return {'shared_cycle_odds_multiplier': '1/2',
            'distributed_type_1_growth_without_revision': '11/10',
            'distributed_type_0_growth_without_revision': '1',
            'small_revision_limit': matrix_rows}


def main():
    out = {'exact': exact_checks(), 'coupling': coupling_checks(),
           'population': population_examples(), 'invariant': invariant_examples()}
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n', encoding='utf-8',newline='\n')
    print(json.dumps({'passed': True, 'output': path.name,
                      'rational_checks': out['exact']['identities_and_inequalities'],
                      'coupling_steps': out['coupling']['checked_steps'],
                      'invariant_settings': len(out['invariant']['settings'])}))


if __name__ == '__main__':
    main()
