"""Changed relevance, reused facts, and a failed invariance. Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

import numpy as np

from goal_geometry import partitions,determines
from learned_concepts import KAPPA,PartitionLearner,net_population,mean_se

NEW_LABELS=(0,128,512,2048,8192,16384)


def counts(x,g,y):
    n=np.bincount(2*x+g,minlength=16).reshape(8,2)
    s=np.bincount(2*x+g,weights=y,minlength=16).reshape(8,2)
    return n,s


def purchased(rng,means,n,common):
    x=rng.integers(0,8,n)
    g=rng.choice(2,n,p=[common,1-common])
    price=rng.random(n)
    outcome=(rng.random(n) < means[x,g]).astype(float)
    payoff=outcome-price
    decoded=payoff+price
    assert np.max(np.abs(decoded-np.rint(decoded))) < 1e-12
    return x,g,decoded


def factorized_choice(labels,same,n,s,weights):
    estimated=np.divide(s,n,out=np.full((8,2),.5),where=n > 0)
    cell_mass=np.einsum('mxy,yj->mxj',same,weights)
    cell_success=np.einsum('mxy,yj->mxj',same,weights*estimated)
    q=np.divide(cell_success,cell_mass,out=np.full_like(cell_success,.5),where=cell_mass > 0)
    score=np.einsum('xj,mxj->m',weights,q*q)/2-KAPPA*labels.max(axis=1)
    winner=int(np.argmax(score))
    return labels[winner],q[winner]


def exact_envelope(labels):
    bits=list(product((0,1),repeat=3))
    checked=0
    for alpha in (F(0),F(1,2),F(1)):
        best={k:None for k in range(1,9)}
        for partition in labels.tolist():
            k=max(partition)+1
            gross=F(0)
            for j,weight in ((0,alpha),(1,1-alpha)):
                for c in range(k):
                    members=[i for i,l in enumerate(partition) if l == c]
                    numerator=sum(1+3*bits[i][j] for i in members)
                    gross += weight*F(numerator*numerator,400*len(members))
            value=gross-F(k-1,50)
            best[k]=value if best[k] is None else max(best[k],value)
            checked+=1
        assert best[1] == F(1,8)
        assert best[2] == F(21,200)+F(9,200)*max(alpha,1-alpha)
        assert best[3] == F(13,100)-F(9,400)*min(alpha,1-alpha)
        assert best[4] == F(11,100)
        for k in range(5,9):
            assert best[k] <= F(17,100)-F(k-1,50)
    # Every candidate value and each proposed envelope segment are affine;
    # their endpoint inequalities cover the entire two intervals.
    return {'rational_partition_endpoint_checks':checked,
            'frequency_intervals_certified':['[0,1/2]','[1/2,1]'],
            'pooled_switch_requires_new_over_old_greater_than':3}


def main():
    labels=np.array(list(partitions(8)),dtype=np.int64)
    same=labels[:,:,None] == labels[:,None,:]
    rows=[]
    for replica in range(32):
        seed=61701+replica
        rng=np.random.default_rng(seed)
        bits=np.array(list(product((0,1),repeat=3)))[rng.permutation(8)]
        old_means=.2+.6*bits[:,[0,1]]
        old=purchased(rng,old_means,2048,.8)
        # Input-only observations carry no labels, prices, outcomes or oracle
        # means into the relevance estimate. All methods may inspect them.
        current_x=rng.integers(0,8,4096)
        current_g=rng.choice(2,4096,p=[.4,.6])
        weights=np.bincount(2*current_x+current_g,minlength=16).reshape(8,2)/4096
        for flip in (False,True):
            current=old_means.copy()
            if flip:
                current[:,1]=1-current[:,1]
            # Paired potential draws differ only in the changed outcome law.
            fresh=purchased(np.random.default_rng(seed+100000),current,max(NEW_LABELS),.4)
            for size in NEW_LABELS:
                joined=tuple(np.concatenate((past,new[:size])) for past,new in zip(old,fresh))
                n,s=counts(*joined)
                pooled=PartitionLearner(labels)
                pooled.count,pooled.success=n,s
                pc,pq,_=pooled.choose()
                all_c,all_q=factorized_choice(labels,same,n,s,weights)
                rn,rs=counts(*(a[-512:] for a in joined))
                recent_c,recent_q=factorized_choice(labels,same,rn,rs,weights)
                for method,c,q in (('pooled_joint',pc,pq),('reuse_conditionals',all_c,all_q),
                                   ('recent_conditionals',recent_c,recent_q)):
                    net=net_population(q,current,np.array([.4,.6]),int(c.max())+1)
                    rows.append({'replica':replica,'conditional_law_reversed':flip,
                                 'new_purchased_outcomes':size,'method':method,
                                 'population_net':net,'cells':int(c.max())+1,
                                 'retains_common':bool(determines(c,bits[:,0])),
                                 'retains_private':bool(determines(c,bits[:,1])),
                                 'private_forecast_mse':float(((q[:,1]-current[:,1])**2).mean())})
    summary=[]
    for flip,size,method in product((False,True),NEW_LABELS,
                                    ('pooled_joint','reuse_conditionals','recent_conditionals')):
        group=[r for r in rows if r['conditional_law_reversed']==flip and r['new_purchased_outcomes']==size
               and r['method']==method]
        summary.append({'conditional_law_reversed':flip,'new_purchased_outcomes':size,'method':method,
                        'population_net':mean_se([r['population_net'] for r in group]),
                        'retains_common_count':sum(r['retains_common'] for r in group),
                        'retains_private_count':sum(r['retains_private'] for r in group),
                        'constant_count':sum(r['cells']==1 for r in group),
                        'private_forecast_mse':mean_se([r['private_forecast_mse'] for r in group])})
    out={'status':'passed','contract':{'replicas':32,'first_seed':61701,'old_purchases':2048,
           'new_purchases':NEW_LABELS,'current_input_only_observations':4096,
           'current_weights_available_to_all_methods':True,'recent_label_window':512,
           'comparison':'diagnostic deployed-value comparison; no total acquisition-cost advantage'},
         'envelope':exact_envelope(labels),'summary':summary,
         'final_runs':[r for r in rows if r['new_purchased_outcomes']==max(NEW_LABELS)]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'passed','envelope':out['envelope']},indent=2))
    for r in summary:
        print(r['conditional_law_reversed'],r['new_purchased_outcomes'],r['method'],
              round(r['population_net']['mean'],6),r['retains_private_count'])


if __name__ == '__main__':
    main()
