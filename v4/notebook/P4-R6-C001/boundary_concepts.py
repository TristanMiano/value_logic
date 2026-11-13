"""Finite shared/private learning near indifference. Codex (GPT-6)."""
from itertools import product
import json
import math
from pathlib import Path

import numpy as np

from goal_geometry import partitions, determines
from learned_concepts import KAPPA, opportunity_batch, net_population, mean_se
from selective_concepts import SelectiveLearner

COMMON = (.45, .49, .5, .51, .55)
BLOCKS = tuple(2**k for k in range(9, 21))
CHECKPOINTS = (sum(BLOCKS[:8]), sum(BLOCKS))
REPLICAS = 32


def category(partition, hidden, agent):
    if int(partition.max()) + 1 != 2:
        return 'other'
    if determines(partition, hidden[:, 0]):
        return 'common'
    if determines(partition, hidden[:, agent]):
        return 'private'
    return 'other'


def check_population(labels):
    hidden = np.array(list(product((0, 1), repeat=3)))
    means = .2 + .6*hidden[:, [0, 1]]
    same = labels[:, :, None] == labels[:, None, :]
    q = np.einsum('mxy,yj->mxj', same, means)/same.sum(axis=2)[:, :, None]
    cells = labels.max(axis=1)+1
    out = []
    for common in COMMON:
        probabilities = np.array([common, 1-common])
        values = ((means[None, :, :]*q-q*q/2)*probabilities).sum(axis=2).mean(axis=1)-KAPPA*(cells-1)
        maximum = .105 + .045*max(common, 1-common)
        assert abs(float(values.max())-maximum) < 1e-12
        winners = np.flatnonzero(abs(values-maximum) < 1e-12)
        kinds = sorted(category(labels[i], hidden, 1) for i in winners)
        assert kinds == (['common', 'private'] if common == .5 else ['common' if common > .5 else 'private'])
        out.append({'common_goal_probability': common, 'oracle_net': maximum,
                    'optimal_categories': kinds, 'common_private_gap': .045*abs(2*common-1),
                    'partitions_checked': len(labels)})
    return out


def main():
    labels = np.array(list(partitions(8)), dtype=np.int64)
    population = check_population(labels)
    rows = []
    for environment, common in enumerate(COMMON):
        probabilities = np.array([common, 1-common])
        optimum = .105 + .045*max(common, 1-common)
        for replica in range(REPLICAS):
            seed = 62001 + replica
            perm_rng = np.random.default_rng(np.random.SeedSequence([seed, environment, 0]))
            hidden = np.array(list(product((0, 1), repeat=3)))[perm_rng.permutation(8)]
            for agent in (1, 2):
                rng = np.random.default_rng(np.random.SeedSequence([seed, environment, agent]))
                means = .2 + .6*hidden[:, [0, agent]]
                learner = SelectiveLearner(labels)
                q = np.full((8, 2), .5)
                total = training_total = purchased = 0
                regret = earned = 0.
                for length in BLOCKS:
                    training = int(math.ceil(length**(2/3)-1e-9))
                    x, g, t, payoff, _ = opportunity_batch(rng, means, probabilities, training, q)
                    purchased += learner.observe(x, g, t, payoff, q)
                    training_total += training
                    training_net = net_population(q, means, probabilities, 8)
                    regret += training*(optimum-training_net)
                    earned += float(payoff.sum())-training*KAPPA*7
                    partition, q = learner.choose()
                    cells = int(partition.max())+1
                    deployment = net_population(q, means, probabilities, cells)
                    assert deployment <= optimum+1e-12
                    exploitation = length-training
                    _, _, _, payoff, _ = opportunity_batch(rng, means, probabilities, exploitation, q)
                    regret += exploitation*(optimum-deployment)
                    earned += float(payoff.sum())-exploitation*KAPPA*(cells-1)
                    total += length
                    assert learner.inputs.sum() == training_total
                    assert learner.count.sum() == purchased
                    if total in CHECKPOINTS:
                        kind = category(partition, hidden, agent)
                        optimal = kind in ('common', 'private') if common == .5 else kind == ('common' if common > .5 else 'private')
                        rows.append({'common_goal_probability': common, 'replica': replica, 'agent': agent,
                                     'horizon': total, 'training_opportunities': training_total,
                                     'purchased_outcomes': purchased, 'category': kind,
                                     'optimal_partition': optimal, 'deployment_regret': optimum-deployment,
                                     'whole_run_net': optimum-regret/total,
                                     'realized_net': earned/total, 'cells': cells})
    summary = []
    for common, horizon in product(COMMON, CHECKPOINTS):
        group = [r for r in rows if r['common_goal_probability'] == common and r['horizon'] == horizon]
        pairs = {}
        for replica in range(REPLICAS):
            kinds = sorted(r['category'] for r in group if r['replica'] == replica)
            key = '/'.join(kinds)
            pairs[key] = pairs.get(key, 0)+1
        keys = ('deployment_regret', 'whole_run_net', 'realized_net', 'purchased_outcomes')
        stats = {key: mean_se([np.mean([r[key] for r in group if r['replica'] == rep]) for rep in range(REPLICAS)]) for key in keys}
        summary.append({'common_goal_probability': common, 'horizon': horizon,
                        'training_opportunities': group[0]['training_opportunities'],
                        'agent_runs': len(group), 'optimal_partition_count': sum(r['optimal_partition'] for r in group),
                        'category_counts': {k: sum(r['category'] == k for r in group) for k in ('common', 'private', 'other')},
                        'pair_counts': pairs, 'se_unit': '32 replica means, each averaging two agents', **stats})
    output = {'status': 'passed', 'contract': {'common_probabilities': COMMON, 'blocks': BLOCKS,
              'replicas': REPLICAS, 'first_seed': 62001, 'candidate_partitions': len(labels),
              'training_price': KAPPA*7, 'feedback': 'purchased payoffs only; all training inputs',
              'learns_from_exploitation': False, 'checkpoints_nested': True},
              'population_checks': population, 'summary': summary, 'runs': rows}
    Path(__file__).with_suffix('.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8',newline='\n')
    print(json.dumps({'status': 'passed', 'summary': summary}, indent=2))


if __name__ == '__main__':
    main()
