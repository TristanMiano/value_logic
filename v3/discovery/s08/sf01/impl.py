"""Shared-cost paired-component frontiers. Codex (GPT-6), DEVELOPMENT."""
from itertools import product
from pathlib import Path
import json
import random
import sys
import replacement_frontier as rf
g01=rf.g01;Meter=rf.Meter;HERE=Path(__file__).resolve().parent

def bounded(weights,tau,meter):
    W=sum(weights)
    if tau<W:return None
    table={0:()}
    for w in weights:
        nxt={}
        for value,count in table.items():
            for k in(0,1,2):
                q=value+w*k;proposal=count+(k,)
                if q<=tau and(q not in nxt or proposal<nxt[q]):nxt[q]=proposal
                meter.pay('planning','two_copy_subset_sum_transition',5+len(count))
        table=nxt
    K=max(table);return dict(count=list(table[K]),coefficient=K,regret=max(K,2*W-K),upper=4*W-K,reachable=sorted(table))

def group_metrics(group,count):
    lo,hi=group['interval'];weights=group['weights'];centers=group['centers']
    a=sum(k*w*(c-lo) for k,w,c in zip(count,weights,centers))
    b=sum((2-k)*w*(hi-c) for k,w,c in zip(count,weights,centers))
    upper=sum(w*(k*c+(2-k)*hi) for k,w,c in zip(count,weights,centers))
    return max(a,b),upper,a,b

def pareto(points):
    # Retain one concrete witness at each decreasing upper-cost level.
    best={}
    for R,U,count in points:
        if R not in best or(U,count)<best[R]:best[R]=(U,count)
    answer=[];last=None
    for R,(U,count) in sorted(best.items()):
        if last is None or U<last:answer.append((R,U,count));last=U
    return answer

def finite(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes());(directory/'declaration.md').write_bytes((HERE/'shared_frontier.md').read_bytes())
    rng=random.Random(8141630);cases=[]
    for d in range(1,9):
        for j in range(3):cases.append(dict(name=f'd{d}r{j}',weights=[1]*d if j==0 else [rng.randrange(1,8) for _ in range(d)]))
    cases.append(dict(name='signed_boundary',weights=[3,5]));groups=[]
    for j in range(20):
        degree=1+j%5;lo=rng.randrange(0,7);hi=rng.randrange(lo+1,9)
        groups.append(dict(name=f'g{j}',interval=[lo,hi],weights=[rng.randrange(1,8) for _ in range(degree)],centers=[rng.randrange(lo,hi+1) for _ in range(degree)]))
    g01.save(directory/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases,groups=groups,source_sha256=g01.sha(__file__),physical_audits=0));result=[]
    for case in cases:
        weights=case['weights'];W=sum(weights);meter=Meter();all_points=[]
        for count in product((0,1,2),repeat=len(weights)):
            values=[]
            for z in(0,1,2):
                cost=sum(w*(k+(2-k)*z) for w,k in zip(weights,count));opt=2*W*min(1,z);values.append((cost-opt,cost))
            K=sum(w*k for w,k in zip(weights,count));R=max(x for x,y in values);U=max(y for x,y in values)
            assert(R,U)==(max(K,2*W-K),4*W-K);all_points.append((R,U,count))
        rows=[]
        for tau in range(2*W+1):
            answer=bounded(weights,tau,meter);feasible=[p for p in all_points if p[0]<=tau]
            if not feasible:assert answer is None;continue
            assert answer['upper']==min(p[1] for p in feasible)
            restricted=rf.subset(weights,tau-W,Meter());upper=3*W-restricted['value']
            rows.append(dict(tau=tau,answer=answer,restricted_upper=upper,strict=answer['upper']<upper))
        record=dict(name=case['name'],count_actions=len(all_points),targets=len(rows),strict_targets=sum(r['strict'] for r in rows),frontier=pareto(all_points),rows=rows,invoice=meter.record())
        g01.save(directory/f"{case['name']}.json",record);result.append({k:v for k,v in record.items() if k not in('rows','frontier','invoice')});print(case['name'],len(all_points),record['strict_targets'],flush=True)
    group_results=[]
    for group in groups:
        points=[];world_checks=0
        for count in product((0,1,2),repeat=len(group['weights'])):
            R,U,a,b=group_metrics(group,count);costs=[];regrets=[]
            for z in range(group['interval'][0],group['interval'][1]+1):
                cost=sum(w*(k*c+(2-k)*z) for w,k,c in zip(group['weights'],count,group['centers']))
                opt=sum(2*w*min(c,z) for w,c in zip(group['weights'],group['centers']));costs.append(cost);regrets.append(cost-opt);world_checks+=1
            assert R==max(regrets) and U==max(costs) and U==2*sum(w*c for w,c in zip(group['weights'],group['centers']))+b
            points.append((R,U,count))
        group_results.append(dict(name=group['name'],count_actions=len(points),world_checks=world_checks,frontier=pareto(points)))
    boundary=json.loads((directory/'signed_boundary.json').read_text());point=next(r for r in boundary['rows'] if r['tau']==10)
    assert point['answer']['count']==[0,2] and point['answer']['upper']==22 and point['restricted_upper']==24
    g01.save(directory/'results.json',dict(status='complete',cases=result,groups=group_results,physical_audits=0))

if __name__=='__main__':finite(Path(sys.argv[1]))
