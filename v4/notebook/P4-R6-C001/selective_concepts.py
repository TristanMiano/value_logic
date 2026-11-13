"""Learning common concepts with nonanticipating purchases. Codex (GPT-6)."""
from itertools import product
import json
import math
from pathlib import Path

import numpy as np

from goal_geometry import partitions,determines
from learned_concepts import BLOCKS,KAPPA,REPLICAS,opportunity_batch,net_population,oracle,mean_se


class SelectiveLearner:
    def __init__(self,labels,purchased_weights=False):
        self.labels=labels
        self.same=labels[:,:,None] == labels[:,None,:]
        self.cells=labels.max(axis=1)+1
        self.inputs=np.zeros((8,2),dtype=np.int64)
        self.count=np.zeros((8,2),dtype=np.int64)
        self.success=np.zeros((8,2))
        self.purchased_weights=purchased_weights

    def observe(self,x,g,t,payoff,q):
        bought=t <= q[x,g]
        self.inputs+=np.bincount(2*x+g,minlength=16).reshape(8,2)
        observed=payoff[bought]+t[bought]
        assert np.max(np.abs(observed-np.rint(observed)),initial=0) < 1e-12
        self.count+=np.bincount(2*x[bought]+g[bought],minlength=16).reshape(8,2)
        self.success+=np.bincount(2*x[bought]+g[bought],weights=observed,minlength=16).reshape(8,2)
        return int(bought.sum())

    def choose(self):
        raw_mean=np.clip((self.success+1)/(self.count+2),.1,.9)
        weights=self.count if self.purchased_weights else self.inputs
        weights=weights/weights.sum() if weights.sum() else np.full((8,2),1/16)
        mass=np.einsum('mxy,yj->mxj',self.same,weights)
        success=np.einsum('mxy,yj->mxj',self.same,weights*raw_mean)
        q=np.divide(success,mass,out=np.full_like(success,.5),where=mass > 0)
        scores=np.einsum('xj,mxj->m',weights,q*q)/2-KAPPA*(self.cells-1)
        selected=int(np.argmax(scores))
        return self.labels[selected],q[selected]


def replica_stats(group,key):
    """Average the two agents before computing the across-replica SE."""
    values=[np.mean([r[key] for r in group if r['replica']==rep]) for rep in range(REPLICAS)]
    return mean_se(values)


def main():
    labels=np.array(list(partitions(8)),dtype=np.int64)
    baseline=json.loads(Path(__file__).with_name('learned_concepts.json').read_text())
    forced={(r['common_goal_probability'],r['replica'],r['agent']):r for r in baseline['final_runs']}
    rows=[]
    for environment,common in enumerate((.8,.4)):
        probabilities=np.array([common,1-common])
        for replica in range(REPLICAS):
            seed=61601+replica
            perm_rng=np.random.default_rng(np.random.SeedSequence([seed,environment,0]))
            hidden=np.array(list(product((0,1),repeat=3)))[perm_rng.permutation(8)]
            for agent,biased in product((1,2),(False,True)):
                rng=np.random.default_rng(np.random.SeedSequence([seed,environment,agent]))
                means=.2+.6*hidden[:,[0,agent]]
                best,best_value,_=oracle(labels,means,probabilities)
                learner=SelectiveLearner(labels,biased)
                total,training_total,purchased,regret,earned=0,0,0,0.,0.
                q=np.full((8,2),.5)
                for length in BLOCKS:
                    training=int(math.ceil(length**(2/3)-1e-9))
                    x,g,t,payoff,bought=opportunity_batch(rng,means,probabilities,training,q)
                    purchased+=learner.observe(x,g,t,payoff,q)
                    training_total+=training
                    training_net=net_population(q,means,probabilities,8)
                    regret+=training*(best_value-training_net)
                    earned+=float(payoff.sum())-training*KAPPA*7
                    partition,q=learner.choose()
                    assert np.min(q) >= .1-1e-12 and np.max(q) <= .9+1e-12
                    cells=int(partition.max())+1
                    deployment=net_population(q,means,probabilities,cells)
                    exploitation=length-training
                    _,_,_,payoff,_=opportunity_batch(rng,means,probabilities,exploitation,q)
                    regret+=exploitation*(best_value-deployment)
                    earned+=float(payoff.sum())-exploitation*KAPPA*(cells-1)
                    total+=length
                    assert learner.inputs.sum()==training_total
                    assert learner.count.sum()==purchased
                    record={'common_goal_probability':common,'replica':replica,'agent':agent,
                        'method':'purchased_input_weights' if biased else 'all_input_weights',
                        'horizon':total,'training_opportunities':training_total,
                        'purchased_training_outcomes':purchased,'cells':cells,
                        'optimal_partition':bool(np.array_equal(partition,best)),
                        'retains_common':bool(determines(partition,hidden[:,0])),
                        'retains_private':bool(determines(partition,hidden[:,agent])),
                        'current_population_net':deployment,'oracle_net':best_value,
                        'whole_run_population_net':best_value-regret/total,
                        'realized_net_per_opportunity':earned/total,
                        'common_forecast_mse':float(((q[:,0]-means[:,0])**2).mean()),
                        'private_forecast_mse':float(((q[:,1]-means[:,1])**2).mean()),
                        'minimum_raw_purchase_count':int(learner.count.min()),
                        'partition':partition.tolist()}
                    if total==sum(BLOCKS):
                        old=forced[(common,replica,agent)]
                        record['paired_gain_over_forced']=record['whole_run_population_net']-(best_value-old['mean_population_regret'])
                        record['paired_realized_gain_over_forced']=record['realized_net_per_opportunity']-old['realized_net_per_opportunity']
                    rows.append(record)
    summary=[]
    for common,method,horizon in product((.8,.4),('all_input_weights','purchased_input_weights'),
                                         sorted(set(r['horizon'] for r in rows))):
        group=[r for r in rows if r['common_goal_probability']==common and r['method']==method and r['horizon']==horizon]
        keys=['current_population_net','whole_run_population_net','realized_net_per_opportunity',
              'purchased_training_outcomes','common_forecast_mse','private_forecast_mse']
        if horizon==sum(BLOCKS):
            keys+=['paired_gain_over_forced','paired_realized_gain_over_forced']
        summary.append({'common_goal_probability':common,'method':method,'horizon':horizon,
            'agent_runs':len(group),'se_unit':'32 replica means, each averaging two agents',
            'optimal_partition_count':sum(r['optimal_partition'] for r in group),
            'retains_common_count':sum(r['retains_common'] for r in group),
            'retains_private_count':sum(r['retains_private'] for r in group),
            **{key:replica_stats(group,key) for key in keys}})
    out={'status':'passed','contract':{'replicas':REPLICAS,'first_seed':61601,
        'paired_to':'learned_concepts.json','blocks':BLOCKS,'candidate_partitions':4140,
        'training_cells_charged':8,'all_training_opportunities_charged':True,
        'conditional_mean_clip':[.1,.9],'learning_uses_exploitation':False,
        'current_goal_seen_before_action':True,'outcome_revealed_after_decline':False,
        'input_weight_comparison':'same raw-mean estimator, different observed frequency weights'},
        'summary':summary,'final_runs':[r for r in rows if r['horizon']==sum(BLOCKS)]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'passed','final_summary':[r for r in summary if r['horizon']==sum(BLOCKS)]},indent=2))


if __name__=='__main__':
    main()
