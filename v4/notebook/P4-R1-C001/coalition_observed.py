"""Observed approvals for R1.14 Proposition 31; Codex (GPT-6).

The learner receives raw approvals, task labels and a stated feature catalogue.
Latent traits and the hidden duplicate mapping are simulator/evaluation only.
The asserted separation is a declared model assumption for the finite certificate.
"""
from dataclasses import dataclass
from math import log, sqrt
from pathlib import Path
import json
import numpy as np


@dataclass
class MomentLearner:
    tasks: int
    features: tuple

    def __post_init__(self):
        self.sums = np.zeros((len(self.features), self.tasks, self.tasks))
        self.counts = np.zeros((self.tasks, self.tasks), dtype=int)
        self.individual_sums = np.zeros(6)
        self.global_features = np.zeros(len(self.features))
        self.episodes = 0

    def observe(self, x, xp, approvals0, approvals1):
        n = len(approvals0)
        assert approvals0.shape == approvals1.shape == (n, 6)
        assert np.all(np.isin(approvals0, [-1, 1]))
        assert np.all(np.isin(approvals1, [-1, 1]))
        z0 = np.stack([np.prod(approvals0[:, s], axis=1) for s in self.features], axis=1)
        z1 = np.stack([np.prod(approvals1[:, s], axis=1) for s in self.features], axis=1)
        totals = np.sum(z0*z1, axis=0)
        self.sums[:, x, xp] += totals
        self.counts[x, xp] += n
        self.individual_sums += np.sum(approvals0*approvals1, axis=0)
        self.global_features += totals
        self.episodes += n

    def infer(self, alpha, separation):
        assert np.all(self.counts == self.counts[0, 0])
        n = int(self.counts[0, 0])
        gram = self.sums / self.counts[None, :, :]
        diagonal = np.diagonal(gram, axis1=1, axis2=2)
        distance = diagonal[:, :, None] + diagonal[:, None, :] - gram - gram.transpose(0, 2, 1)
        radius = sqrt(2*log(2*len(self.features)*self.tasks**2/alpha)/n)
        assert 4*radius < separation/2
        distinct = np.max(distance, axis=0) > separation/2
        # On the simultaneous event these are true equivalence classes.
        # Off that event, do not silently force a contradictory graph into a partition.
        same = ~distinct
        assert np.array_equal(same, same.T) and np.all(np.diag(same))
        assert all(not same[x, y] or np.array_equal(same[x], same[y])
                   for x in range(self.tasks) for y in range(self.tasks))
        patterns = {}
        labels = [patterns.setdefault(tuple(row), len(patterns)) for row in same]
        return {'partition': labels, 'gram': gram, 'distance': distance,
                'radius_gram': radius, 'radius_distance': 4*radius,
                'certified_distinct': np.max(distance, axis=0) - 4*radius > 0,
                'global_feature_reappearance': self.global_features/self.episodes,
                'global_individual_reappearance': self.individual_sums/self.episodes}


def generate_reports(rng, traits, signs):
    means = .5 * traits * signs
    outcomes = np.where(rng.random(means.shape) < (1+means)/2, 1, -1)
    fresh = rng.choice([-1, 1], size=means.shape)
    approvals = np.empty((len(traits), 6), dtype=np.int8)
    approvals[:, ::2] = fresh
    approvals[:, 1::2] = fresh * outcomes
    return approvals


def main():
    seed, n, alpha, separation = 20261125, 2000, .05, 1.0
    rng = np.random.default_rng(seed)
    # Unrelated label order, with two copies of each hidden response profile.
    profile = np.array([[1, -1, 1], [1, 1, -1], [1, -1, -1], [1, 1, 1],
                        [1, 1, -1], [1, -1, 1], [1, 1, 1], [1, -1, -1]])
    learner = MomentLearner(8, ((0, 1), (2, 3), (4, 5)))
    first_order_sums = np.zeros((8, 6))
    first_order_counts = np.zeros(8)
    for x in range(8):
        for xp in range(8):
            traits = rng.choice([-1, 1], size=(n, 3))
            a0 = generate_reports(rng, traits, profile[x])
            a1 = generate_reports(rng, traits, profile[xp])
            learner.observe(x, xp, a0, a1)
            first_order_sums[x] += a0.sum(axis=0)
            first_order_sums[xp] += a1.sum(axis=0)
            first_order_counts[x] += n
            first_order_counts[xp] += n
    result = learner.infer(alpha, separation)
    expected = np.all(profile[:, None, :] == profile[None, :, :], axis=2)
    actual = np.equal.outer(result['partition'], result['partition'])
    assert np.array_equal(actual, expected)
    true_gram = .25 * np.einsum('xf,yf->fxy', profile, profile)
    max_error = float(np.max(np.abs(result['gram']-true_gram)))
    assert max_error <= result['radius_gram']
    assert np.array_equal(result['certified_distinct'], ~expected)
    pairwise = []
    for x in range(8):
        for xp in range(x+1, 8):
            observed = float(np.max(result['distance'][:, x, xp]))
            pairwise.append({'tasks': [x, xp], 'estimated_max_distance': observed,
                             'lower': observed-result['radius_distance'],
                             'upper': observed+result['radius_distance'],
                             'same_true_profile': bool(expected[x, xp])})
    output = {'author': 'Codex (GPT-6)', 'status': 'passed', 'seed': seed,
              'episodes': learner.episodes, 'performances': 2*learner.episodes,
              'binary_reports': 12*learner.episodes, 'ordered_task_pairs': 64,
              'episodes_per_ordered_pair': n, 'confidence': 1-alpha,
              'declared_separation': separation,
              'separation_scope': 'known construction/model assumption, not inferred exact gap',
              'partition': result['partition'], 'max_gram_error': max_error,
              'radius_gram': result['radius_gram'], 'radius_distance': result['radius_distance'],
              'global_feature_reappearance': result['global_feature_reappearance'].tolist(),
              'global_individual_reappearance': result['global_individual_reappearance'].tolist(),
              'max_absolute_first_order_mean': float(np.max(np.abs(first_order_sums/first_order_counts[:, None]))),
              'first_order_population_law': 'uniform full approval vector on every task',
              'pairwise_certificates': pairwise,
              'comparison': 'same estimator is a conventional repeated-measurement moment method',
              'limitations': ['one seeded construction', 'controlled assignments',
                              'known interaction feature catalogue', 'known separation for exact merges',
                              'no independent confirmation']}
    Path(__file__).with_suffix('.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'pairwise_certificates'}))


if __name__ == '__main__':
    main()
