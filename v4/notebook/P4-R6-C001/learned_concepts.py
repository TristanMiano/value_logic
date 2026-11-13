"""Purchased evidence selects common or private concepts. Codex (GPT-6).

The learner receives raw contexts, goal labels, prices and action payoffs.
Hidden meanings/probabilities occur only in environment and evaluator code.
"""
from itertools import product
from fractions import Fraction as F
import json
import math
from pathlib import Path

import numpy as np

from goal_geometry import partitions, determines

KAPPA = .02
BLOCKS = tuple(2**k for k in range(9,17))
REPLICAS = 32


class PartitionLearner:
    def __init__(self, labels):
        self.labels = labels
        self.cells = labels.max(axis=1)+1
        self.same = labels[:, :, None] == labels[:, None, :]
        self.count = np.zeros((8,2),dtype=np.int64)
        self.success = np.zeros((8,2))

    def observe_purchased(self, x, goal, price, payoff):
        outcome = payoff+price
        assert np.max(np.abs(outcome-np.rint(outcome))) < 1e-12
        self.count += np.bincount(2*x+goal,minlength=16).reshape(8,2)
        self.success += np.bincount(2*x+goal,weights=outcome,minlength=16).reshape(8,2)

    def choose(self):
        count = np.einsum('mxy,yj->mxj',self.same,self.count)
        success = np.einsum('mxy,yj->mxj',self.same,self.success)
        q = np.divide(success,count,out=np.full_like(success,.5),where=count > 0)
        score = np.einsum('xj,mxj->m',self.count,q*q)/(2*self.count.sum())
        score -= KAPPA*(self.cells-1)
        index = int(np.argmax(score))
        return self.labels[index], q[index], float(score[index])


def opportunity_batch(rng, means, probabilities, size, q=None):
    """Only action payoff is returned; unbought outcomes stay in this function."""
    x = rng.integers(0,8,size)
    goal = rng.choice(2,size,p=probabilities)
    price = rng.random(size)
    outcome = rng.random(size) < means[x,goal]
    bought = np.ones(size,dtype=bool) if q is None else price <= q[x,goal]
    payoff = bought*(outcome-price)
    return x,goal,price,payoff,int(bought.sum())


def net_population(q, means, probabilities, cells):
    return float(((means*q-q*q/2)*probabilities).sum(axis=-1).mean()-KAPPA*(cells-1))


def oracle(labels, means, probabilities):
    same = labels[:, :, None] == labels[:, None, :]
    q = np.einsum('mxy,yj->mxj',same,means)/same.sum(axis=2)[:, :, None]
    cells = labels.max(axis=1)+1
    values = ((means[None,:,:]*q-q*q/2)*probabilities).sum(axis=2).mean(axis=1)-KAPPA*(cells-1)
    winners = np.flatnonzero(np.abs(values-values.max()) < 1e-12)
    assert len(winners) == 1
    index = int(winners[0])
    return labels[index],float(values[index]),{
        'constant_known_law':float(values[0]),'full_known_law':float(values[-1])}


def mean_se(values):
    a = np.array(values,dtype=float)
    return {'mean':float(a.mean()),'standard_error':float(a.std(ddof=1)/np.sqrt(len(a)))}


def rational_oracle(labels):
    """Independent exact check of the common-feature premise in Corollary 1."""
    hidden = list(product((0,1),repeat=3))
    reports=[]
    for common in (F(4,5),F(2,5)):
        values=[]
        for partition in labels.tolist():
            k=max(partition)+1
            gross=F(0)
            for goal,weight in ((0,common),(1,1-common)):
                for cell in range(k):
                    members=[i for i,label in enumerate(partition) if label == cell]
                    numerator=sum(1+3*hidden[i][goal] for i in members)
                    gross += weight*F(numerator*numerator,400*len(members))
            values.append(gross-F(k-1,50))
        maximum=max(values)
        winners=[i for i,v in enumerate(values) if v == maximum]
        assert len(winners) == 1
        target=np.array(hidden)[:,0 if common == F(4,5) else 1]
        assert determines(labels[winners[0]],target)
        gap=maximum-max(v for v in values if v < maximum)
        reports.append({'common_probability':str(common),'optimum':str(maximum),
                        'gap_to_next_partition':str(gap),'optimal_partition_count':len(winners),
                        'all_partitions_checked':len(values),
                        'best_by_cells':{str(k):str(max(v for p,v in zip(labels,values) if p.max()+1 == k))
                                         for k in range(1,9)}})
    return reports


def main():
    labels = np.array(list(partitions(8)),dtype=np.int64)
    assert len(labels) == 4140
    rows,agreements = [],[]
    for environment,common in enumerate((.8,.4)):
        probabilities = np.array([common,1-common])
        for replica in range(REPLICAS):
            seed = 61601+replica
            permutation_rng = np.random.default_rng(np.random.SeedSequence([seed,environment,0]))
            hidden = np.array(list(product((0,1),repeat=3)))[permutation_rng.permutation(8)]
            final_q = []
            for agent in (1,2):
                rng = np.random.default_rng(np.random.SeedSequence([seed,environment,agent]))
                means = .2+.6*hidden[:,[0,agent]]
                best_partition,best_value,baselines = oracle(labels,means,probabilities)
                target = hidden[:,0 if common == .8 else agent]
                assert determines(best_partition,target)
                assert abs(best_value-(.141 if common == .8 else .132)) < 1e-12
                learner = PartitionLearner(labels)
                total,explored,regret,earned = 0,0,0.0,0.0
                for length in BLOCKS:
                    training = int(math.ceil(length**(2/3)-1e-9))
                    x,g,t,payoff,bought = opportunity_batch(rng,means,probabilities,training)
                    assert bought == training
                    learner.observe_purchased(x,g,t,payoff)
                    explored += training
                    # Across uniform contexts every goal outcome has mean .5;
                    # forced purchases therefore earn zero in population,
                    # before the full eight-cell training cost of .14.
                    regret += training*(best_value+KAPPA*7)
                    earned += float(payoff.sum())-training*KAPPA*7
                    partition,q,empirical = learner.choose()
                    cells = int(partition.max())+1
                    exploitation = length-training
                    _,_,_,payoff,bought = opportunity_batch(rng,means,probabilities,exploitation,q)
                    net = net_population(q,means,probabilities,cells)
                    assert net <= best_value+1e-12
                    regret += exploitation*(best_value-net)
                    earned += float(payoff.sum())-exploitation*KAPPA*(cells-1)
                    total += length
                    assert learner.count.sum() == explored
                    rows.append({'common_goal_probability':common,'replica':replica,'agent':agent,
                                 'horizon':total,'exploration_attempts':explored,'cells':cells,
                                 'retains_common':bool(determines(partition,hidden[:,0])),
                                 'retains_private':bool(determines(partition,hidden[:,agent])),
                                 'optimal_partition':bool(np.array_equal(partition,best_partition)),
                                 'current_population_net':net,'oracle_net':best_value,
                                 'cumulative_population_regret':regret,
                                 'mean_population_regret':regret/total,
                                 'realized_net_per_opportunity':earned/total,
                                 'common_forecast_mse':float(((q[:,0]-means[:,0])**2).mean()),
                                 'private_forecast_mse':float(((q[:,1]-means[:,1])**2).mean()),
                                 'partition':partition.tolist(),**baselines})
                final_q.append(q[:,0])
            agreements.append({'common_goal_probability':common,'replica':replica,
                               'shared_forecast_squared_difference':float(((final_q[0]-final_q[1])**2).mean())})
    summary=[]
    horizons=sorted(set(row['horizon'] for row in rows))
    for common,horizon in product((.8,.4),horizons):
        group=[r for r in rows if r['common_goal_probability'] == common and r['horizon'] == horizon]
        summary.append({'common_goal_probability':common,'horizon':horizon,'runs':len(group),
                        'exploration_attempts_per_run':group[0]['exploration_attempts'],
                        'optimal_partition_count':sum(r['optimal_partition'] for r in group),
                        'retains_common_count':sum(r['retains_common'] for r in group),
                        'retains_private_count':sum(r['retains_private'] for r in group),
                        **{key:mean_se([r[key] for r in group]) for key in (
                            'current_population_net','mean_population_regret','realized_net_per_opportunity',
                            'common_forecast_mse','private_forecast_mse')}})
    out={'status':'passed','contract':{'replicas':REPLICAS,'first_seed':61601,
          'block_lengths':BLOCKS,'candidates':4140,'kappa':KAPPA,
          'outcome_revealed_after_decline':False,'learner_given_semantic_bits':False,
          'learning_uses_exploration_only':True,'exploration_cells_charged':8},
         'rational_oracle':rational_oracle(labels),
         'summary':summary,'final_runs':[r for r in rows if r['horizon'] == horizons[-1]],
         'agreement':[{ 'common_goal_probability':common,
             **mean_se([r['shared_forecast_squared_difference'] for r in agreements
                        if r['common_goal_probability'] == common])} for common in (.8,.4)]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'passed','final_summary':[r for r in summary if r['horizon'] == horizons[-1]],
                      'agreement':out['agreement']},indent=2))


if __name__ == '__main__':
    main()
