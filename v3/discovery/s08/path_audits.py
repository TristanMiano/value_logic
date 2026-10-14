#!/usr/bin/env python3
"""Exact product-source path planner; DEVELOPMENT, Codex (GPT-6), 2026-10-14."""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
from datetime import datetime,timezone
from pathlib import Path
import json
import random
import sys
import time
import g01

HERE=Path(__file__).resolve().parent
VERSION='s08-path-audits-v1'
Meter=g01.kernel.Meter


def plan(costs,probabilities):
    if not costs or len(costs)!=len(probabilities) or any(c<=0 for c in costs) or any(not 0<=p<=1 for p in probabilities):
        raise ValueError('Nonempty positive fees and admitted probability vector required')
    n=len(costs);values={};left={};right={};roots={};meter=Meter()
    def at(table,a,b):return table[(a,b)] if a<=b else F(0)
    for length in range(1,n+1):
        for a in range(n-length+1):
            b=a+length-1
            left[a,b]=costs[a]+probabilities[a]*at(values,a+1,b)+(1-probabilities[a])*at(left,a+1,b)
            right[a,b]=costs[b]+probabilities[b]*at(values,a,b-1)+(1-probabilities[b])*at(right,a,b-1)
            meter.pay('planning','two_forced_endpoint_recurrences',12)
            if a==b:values[a,b]=F(0);roots[a,b]=None
            else:
                options=[]
                for i in range(a,b+1):
                    v=costs[i]+probabilities[i]*(at(values,a,i-1)+at(values,i+1,b))
                    v+=(1-probabilities[i])*(at(right,a,i-1)+at(left,i+1,b))
                    options.append((v,i));meter.pay('planning','elective_root_candidate',10)
                values[a,b],roots[a,b]=min(options)
            assert left[a,b]>=values[a,b] and right[a,b]>=values[a,b]
            meter.pay('planning','retain_interval_values_and_root',4)
    return dict(n=n,values=values,left=left,right=right,roots=roots,invoice=meter.record())


def evaluate_policy(costs,probabilities,policy):
    n=len(costs);v={};l={};r={}
    def at(table,a,b):return table[(a,b)] if a<=b else F(0)
    for length in range(1,n+1):
        for a in range(n-length+1):
            b=a+length-1
            l[a,b]=costs[a]+probabilities[a]*at(v,a+1,b)+(1-probabilities[a])*at(l,a+1,b)
            r[a,b]=costs[b]+probabilities[b]*at(v,a,b-1)+(1-probabilities[b])*at(r,a,b-1)
            if a==b:v[a,b]=F(0)
            else:
                i=policy['roots'][a,b]
                v[a,b]=costs[i]+probabilities[i]*(at(v,a,i-1)+at(v,i+1,b))
                v[a,b]+=(1-probabilities[i])*(at(r,a,i-1)+at(l,i+1,b))
    return v[0,n-1]


def explicit(costs,probabilities):
    """All three-value observation histories, no interval or forced-state rule."""
    calls=options=0;n=len(costs)
    @lru_cache(None)
    def value(state):
        nonlocal calls,options
        calls+=1;safe=True
        for i in range(n-1):
            qa=[state[i]] if state[i]>=0 else [0,1,2]
            qb=[state[i+1]] if state[i+1]>=0 else [0,1,2]
            if not (max(qa)<=min(qb) or max(qb)<=min(qa)):safe=False;break
        if safe:return F(0)
        choices=[]
        for i,x in enumerate(state):
            if x>=0:continue
            options+=1;v=F(costs[i]);law=(probabilities[i]/2,1-probabilities[i],probabilities[i]/2)
            for outcome,p in enumerate(law):
                child=list(state);child[i]=outcome;v+=p*value(tuple(child))
            choices.append(v)
        return min(choices)
    answer=value((-1,)*n)
    return dict(value=answer,states=calls,options=options)


def execute(costs,hidden,policy):
    """Conditional policy probe: actual auditing service is not claimed here."""
    seen={};queries=[]
    def ask(i):
        if i in seen:raise AssertionError('Repeated query')
        seen[i]=hidden[i];queries.append(i);return seen[i]
    def go(a,b,mode='ordinary'):
        if a>b or (a==b and mode=='ordinary'):return
        if mode=='left':
            middle=ask(a)==1;go(a+1,b,'left' if middle else 'ordinary')
        elif mode=='right':
            middle=ask(b)==1;go(a,b-1,'right' if middle else 'ordinary')
        else:
            i=policy['roots'][a,b];middle=ask(i)==1
            go(a,i-1,'right' if middle else 'ordinary');go(i+1,b,'left' if middle else 'ordinary')
    go(0,len(costs)-1)
    choices=[]
    for i in range(len(costs)-1):
        qa=[seen[i]] if i in seen else [0,1,2];qb=[seen[i+1]] if i+1 in seen else [0,1,2]
        if max(qa)<=min(qb):choices.append(i)
        elif max(qb)<=min(qa):choices.append(i+1)
        else:raise AssertionError('Policy terminated without a source-uniform exact action')
        assert hidden[choices[-1]]==min(hidden[i],hidden[i+1])
    return dict(queries=queries,cost=sum(costs[i] for i in queries),choices=choices)


def export(policy):
    result={k:v for k,v in policy.items() if k not in ('values','left','right','roots')}
    for key in ('values','left','right','roots'):
        result[key]={f'{a},{b}':v for (a,b),v in policy[key].items()}
    return result


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(8141417);cases=[]
    for n in range(2,8):
        for repeat in range(4):
            cases.append(dict(costs=[rng.randrange(1,8) for _ in range(n)],
                probabilities=[F(rng.randrange(5),4) for _ in range(n)]))
    large=[dict(costs=[rng.randrange(1,8) for _ in range(n)],probabilities=[F(rng.randrange(1,10),10) for _ in range(n)]) for n in (16,32,64)]
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        created_utc=datetime.now(timezone.utc).isoformat(),small=cases,large=large,
        declaration_sha256=g01.sha(HERE/'path_audits.md'),source_sha256=g01.sha(__file__),
        actual_new_audits=0,scope='Conditional policy reconstruction only; runtime includes exhaustive diagnostics'))
    result=dict(status='running',small=[],large=[]);start=time.perf_counter_ns()
    for case in cases:
        costs=list(map(F,case['costs']));p=case['probabilities'];policy=plan(costs,p);bellman=explicit(costs,p)
        assert policy['values'][0,len(costs)-1]==bellman['value']
        mean=F(0);count=0;maxqueries=0
        for hidden in product((0,1,2),repeat=len(costs)):
            outcome=execute(costs,hidden,policy);prob=F(1)
            for x,pi in zip(hidden,p):prob*=1-pi if x==1 else pi/2
            mean+=prob*outcome['cost'];count+=1;maxqueries=max(maxqueries,len(outcome['queries']))
        assert mean==bellman['value']
        # A lower-probability policy must meet its original upper invoice at all larger endpoints.
        lower=[pi/2 for pi in p];robust=plan(costs,lower);checks=0
        for endpoints in product((0,1),repeat=len(costs)):
            q=[li if e==0 else F(1) for li,e in zip(lower,endpoints)]
            assert evaluate_policy(costs,q,robust)<=robust['values'][0,len(costs)-1];checks+=1
        result['small'].append(dict(case=case,policy=export(policy),bellman=bellman,
            source_outcomes=count,mean_invoice=mean,max_queries=maxqueries,robust_endpoint_checks=checks))
        g01.save(directory/'results.json',result)
    for case in large:
        costs=list(map(F,case['costs']));p=case['probabilities'];t=time.perf_counter_ns();policy=plan(costs,p)
        elapsed=time.perf_counter_ns()-t
        result['large'].append(dict(n=len(costs),value=policy['values'][0,len(costs)-1],
            planning_ns=elapsed,policy=export(policy),source='Known product parameters, not learned'))
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat(),wall_ns=time.perf_counter_ns()-start,
        summary=dict(small_cases=len(cases),bellman_states=sum(r['bellman']['states'] for r in result['small']),
            source_outcomes=sum(r['source_outcomes'] for r in result['small']),
            robust_endpoint_checks=sum(r['robust_endpoint_checks'] for r in result['small']),actual_new_audits=0))
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status=result['status'],summary=result['summary'],large=[{k:r[k] for k in ('n','value','planning_ns')} for r in result['large']]),default=g01.encode))


if __name__=='__main__':run(Path(sys.argv[1]))
