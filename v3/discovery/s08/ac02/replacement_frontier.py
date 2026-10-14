"""Replacement-aware paired-star action frontier. DEVELOPMENT, Codex (GPT-6)."""
from itertools import product
from pathlib import Path
import json
import random
import sys
import g01
HERE=Path(__file__).resolve().parent;Meter=g01.kernel.Meter

def subset(weights,limit,meter):
    if limit<0:return None
    states={0:()}
    for i,w in enumerate(weights):
        nxt=dict(states)
        for value,chosen in states.items():
            if value+w<=limit:
                proposal=chosen+(i,)
                if value+w not in nxt or proposal<nxt[value+w]:nxt[value+w]=proposal
            meter.pay('planning','subset_sum_transition',5+len(chosen))
        states=nxt
    value=max(states);meter.pay('planning','select_largest_attainable_bias',len(states))
    return dict(value=value,chosen=list(states[value]),attainable=sorted(states))

def propose(weights,known,tau,meter):
    remaining=[i for i in range(len(weights)) if i not in known];W=sum(weights[i] for i in remaining)
    C=sum(2*weights[i]*min(1,v) for i,v in known.items());result=subset([weights[i] for i in remaining],tau-W,meter)
    meter.pay('planning','known_cost_unknown_weight_and_tolerance',4*len(weights))
    if result is None:return None
    biased={remaining[j] for j in result['chosen']};count=[(2 if known[i]>=1 else 0) if i in known else (2 if i in biased else 1) for i in range(len(weights))]
    return dict(count=count,repair_regret=W+result['value'],local_upper=C+3*W-result['value'],unknown_weight=W,
        known_cost=C,bias_weight=result['value'],subset=result)

def metrics(weights,known,count):
    R=U=0
    for i,(w,k) in enumerate(zip(weights,count)):
        options=[known[i]] if i in known else [0,1,2]
        R+=w*max(k+(2-k)*v-2*min(1,v) for v in options)
        U+=w*max(k+(2-k)*v for v in options)
    return R,U

def finite(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes());(directory/'declaration.md').write_bytes((HERE/'replacement_frontier.md').read_bytes())
    rng=random.Random(8141600);cases=[]
    for n in range(1,7):
        for shape in('unit','weighted'):cases.append(dict(name=f'n{n}_{shape}',weights=[1]*n if shape=='unit' else [rng.randrange(1,6) for _ in range(n)]))
    g01.save(directory/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases,source_sha256=g01.sha(__file__),physical_audits=0));results=[]
    for case in cases:
        weights=case['weights'];n=len(weights);states=choices=queries=world_checks=0;meter=Meter();max_frontier=0
        for state in product((-1,0,1,2),repeat=n):
            known={i:v for i,v in enumerate(state) if v!=-1};unknown=[i for i in range(n) if i not in known];W=sum(weights[i] for i in unknown)
            points=[]
            for values in product((0,1,2),repeat=len(unknown)):
                count=[2 if known.get(i,0)>=1 else 0 for i in range(n)]
                for i,k in zip(unknown,values):count[i]=k
                R,U=metrics(weights,known,count);points.append((R,U,tuple(count)));choices+=1
                if n<=3:
                    worlds=[]
                    for vals in product((0,1,2),repeat=len(unknown)):
                        world=[known.get(i,0) for i in range(n)]
                        for i,v in zip(unknown,vals):world[i]=v
                        cost=sum(w*(k+(2-k)*v) for w,k,v in zip(weights,count,world))
                        optimum=sum(2*w*min(1,v) for w,v in zip(weights,world));worlds.append((cost-optimum,cost));world_checks+=1
                    assert R==max(x for x,y in worlds) and U==max(y for x,y in worlds)
            unique=sorted(set((r,u) for r,u,k in points));pareto=[p for p in unique if not any(q[0]<=p[0] and q[1]<=p[1] and q!=p for q in unique)]
            max_frontier=max(max_frontier,len(pareto))
            for tau in range(2*W+1):
                ans=propose(weights,known,tau,meter);feasible=[p for p in points if p[0]<=tau]
                if not feasible:assert ans is None
                else:
                    assert ans['local_upper']==min(u for r,u,k in feasible)
                    assert metrics(weights,known,ans['count'])==(ans['repair_regret'],ans['local_upper'])
                queries+=1
            states+=1
        result=dict(name=case['name'],states=states,count_action_checks=choices,tolerance_queries=queries,explicit_world_checks=world_checks,max_frontier=max_frontier,invoice=meter.record())
        results.append(result);g01.save(directory/f"{case['name']}.json",result);print(case['name'],states,choices,queries,flush=True)
    # Exact original five-variable boundary, with an entailed mandatory feature.
    hard=[[1,2],[-1,-2],[3,4],[-3,-4],[1,5],[-1,5]]
    feasible=[mask for mask in range(32) if all(any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in clause) for clause in hard)]
    assert len(feasible)==4 and all(mask>>4&1 for mask in feasible)
    def cost(mask,leaf,anchor):return sum((1 if i in(0,2) else leaf if i in(1,3) else anchor) for i in range(5) if mask>>i&1)
    boundary=[]
    for mask in feasible:
        r=0
        for leaf,anchor in product((0,1,2),(0,100)):
            optimum=min(100,min(cost(m,leaf,anchor) for m in feasible));r=max(r,cost(mask,leaf,anchor)-optimum)
        boundary.append(dict(mask=mask,combined_regret=r))
    assert next(x['combined_regret'] for x in boundary if x['mask']==21)==2
    assert next(x['combined_regret'] for x in boundary if x['mask']==25)==3
    g01.save(directory/'results.json',dict(status='complete',cases=results,boundary=dict(hard=hard,feasible=feasible,repairs=boundary,replacement_regret=100),physical_audits=0))

if __name__=='__main__':finite(Path(sys.argv[1]))
