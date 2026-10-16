"""DEVELOPMENT chain-constrained logical regret oracle, Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import argparse
import hashlib
import json
import random
import time

SIGNS=(-1,1)
ALL=set(product(SIGNS,repeat=2))


def admissible(x,relations):
    return all((x[i],x[i+1]) in relation for i,relation in enumerate(relations))


def chain_max(coefficients,weights,flip_fee,H,relations,clamp,mode):
    """Max sum w_i(s_i-mode+2b_i)x_i - f_i b_i, chain x, sum b<=H."""
    m=len(weights);H=min(H,m) if mode else 0
    values={(None,0):F(0)};history=[]
    counts={'states':0,'extensions':0,'relation_checks':0,'retained_backpointers':0}
    for i in range(m):
        nxt={};back={}
        for (previous,k),value in values.items():
            counts['states']+=1
            for x in SIGNS:
                if i in clamp and x!=clamp[i]:continue
                if i:
                    counts['relation_checks']+=1
                    if (previous,x) not in relations[i-1]:continue
                for b in range(1+int(bool(mode) and k<H)):
                    counts['extensions']+=1
                    candidate=value+weights[i]*(coefficients[i]-mode+2*b)*x-flip_fee[i]*b
                    key=x,k+b
                    if key not in nxt or candidate>nxt[key]:
                        nxt[key]=candidate;back[key]=((previous,k),b)
        values=nxt;history.append(back);counts['retained_backpointers']+=len(back)
        if not values:return None,None,None,counts
    key=max(values,key=values.get);answer=values[key];truth=[];flips=[]
    for i in range(m-1,-1,-1):
        truth.append(key[0]);previous,b=history[i][key]
        if b:flips.append(i)
        key=previous
    return answer,tuple(reversed(truth)),tuple(reversed(flips)),counts


def oracle(rows,weights,flip_fee,H,relations):
    best=None;witness=None;total={k:0 for k in ('states','extensions','relation_checks','retained_backpointers')}
    for z,(fee,coefficients) in rows.items():
        for mode in (0,1):
            value,truth,flips,counts=chain_max(coefficients,weights,flip_fee,H,relations,dict(enumerate(z)),mode)
            for k,v in counts.items():total[k]+=v
            if value is None:continue
            value+=fee
            if best is None or value>best:
                best=value;witness={'truth':truth,'flips':flips,'terminal':mode,'cell':z}
    assert best is not None,'Empty logical source'
    return best,witness,total


def mixed_controller(m,r,H,flip_fee,query_fee,seed):
    rng=random.Random(seed);policies=[]
    states=sorted(product((-1,0,1),repeat=r),key=lambda h:sum(v!=0 for v in h))
    for policy_index in range(3):
        policy={}
        for h in states:
            k=H-sum(v!=0 for v in h)
            if k<0:continue
            query=[j for j in range(r) if h[j]==0] if k else []
            options=['stop0','stop1']+[('query',j) for j in query]
            action=rng.choice(options)
            if policy_index==0 and not any(h) and query:action=('query',query[0])
            if action=='stop1':
                chosen=tuple(sorted(rng.sample(range(m),rng.randrange(min(k,m)+1))))
                action=('stop1',chosen)
            policy[h]=action
        policies.append(policy)
    probabilities=(F(1,2),F(1,3),F(1,6));rows={}
    for z in product(SIGNS,repeat=r):
        total_fee=F(0);coefficients=[F(0)]*m
        for probability,policy in zip(probabilities,policies):
            h=[0]*r;fee=F(0);used=0
            while True:
                action=policy[tuple(h)]
                if isinstance(action,tuple) and action[0]=='query':
                    j=action[1];h[j]=z[j];fee+=query_fee[j];used+=1
                elif action=='stop0':break
                else:
                    flips=action[1];used+=len(flips)
                    fee+=sum((flip_fee[i] for i in flips),F(0))
                    for i in range(m):coefficients[i]+=probability*(-1 if i in flips else 1)
                    break
            assert used<=H
            total_fee+=probability*fee
        rows[z]=(total_fee,tuple(coefficients))
    return rows,policies,probabilities


def brute(rows,weights,flip_fee,H,relations):
    m=len(weights);r=len(next(iter(rows)));best=None;worlds=0;comparisons=0
    for x in product(SIGNS,repeat=m):
        if not admissible(x,relations):continue
        worlds+=1;fee,coefficients=rows[x[:r]]
        cost=fee+sum((w*s*y for w,s,y in zip(weights,coefficients,x)),F(0))
        optimal=F(0)
        for k in range(min(m,H)+1):
            for flipped in combinations(range(m),k):
                comparisons+=1
                value=sum((w*y*(-1 if i in flipped else 1) for i,(w,y) in enumerate(zip(weights,x))),F(0))
                value+=sum((flip_fee[i] for i in flipped),F(0))
                optimal=min(optimal,value)
        regret=cost-optimal
        if best is None or regret>best:best=regret
    return best,worlds,comparisons


def case(index):
    m,r,H=[(4,0,0),(5,1,1),(6,2,3),(7,2,8),(6,0,2),(257,4,8)][index]
    relation_menu=[ALL,{(-1,-1),(1,1)},{(-1,1),(1,-1)},ALL-{(1,-1)},ALL-{(1,1)}]
    relations=[relation_menu[(i+index)%len(relation_menu)] for i in range(m-1)]
    rng=random.Random(19000+index)
    weights=tuple(F(rng.randrange(-3,4)) for _ in range(m))
    flip_fee=tuple(F(rng.randrange(5),4) for _ in range(m))
    query_fee=tuple(F(rng.randrange(3),8) for _ in range(r))
    rows,policies,probabilities=mixed_controller(m,r,H,flip_fee,query_fee,20000+index)
    start=time.perf_counter_ns();value,witness,counts=oracle(rows,weights,flip_fee,H,relations)
    elapsed=time.perf_counter_ns()-start
    relaxed,_,relaxedcounts=oracle(rows,weights,flip_fee,H,[ALL]*(m-1))
    assert value<=relaxed
    x=tuple(witness['truth']);z=x[:r];fee,s=rows[z]
    actual=fee+sum((a*b*c for a,b,c in zip(weights,s,x)),F(0))
    if witness['terminal']:
        actual-=sum((w*y*(-1 if i in witness['flips'] else 1) for i,(w,y) in enumerate(zip(weights,x))),F(0))
        actual-=sum((flip_fee[i] for i in witness['flips']),F(0))
    assert actual==value and admissible(x,relations)
    checked=None
    if m<10:
        exact,worlds,comparisons=brute(rows,weights,flip_fee,H,relations)
        assert exact==value,(index,exact,value)
        checked={'admissible_worlds':worlds,'truth_flip_comparisons':comparisons,'value':str(exact)}
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'m':m,'r':r,'H':H,
       'weights':list(map(str,weights)),'flip_fee':list(map(str,flip_fee)),'query_fee':list(map(str,query_fee)),
       'relations':[sorted(x) for x in relations],'controller_seed':20000+index,
       'mixture':list(map(str,probabilities)),'policies':[{str(k):v for k,v in p.items()} for p in policies],
       'rows':[{'cell':z,'fee':str(fee),'coefficients':list(map(str,s))} for z,(fee,s) in rows.items()],
       'exact_regret':str(value),'unconstrained_regret':str(relaxed),'witness':witness,
       'counts':counts,'unconstrained_counts':relaxedcounts,'elapsed_ns':elapsed,'enumeration':checked,
       'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'scope':'Fixed-controller exact chain separator, not an optimized controller or paid source acquisition.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','m','r','H','exact_regret','unconstrained_regret','counts','enumeration')}))
