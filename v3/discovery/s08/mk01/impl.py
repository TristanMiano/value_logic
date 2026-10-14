#!/usr/bin/env python3
"""Exact Markov source evidence and path acquisition. DEVELOPMENT.
Codex (GPT-6), 2026-10-14. Indicators: 0=extreme, 1=middle.
"""
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
import path_policy_certs as pc

HERE=Path(__file__).resolve().parent
VERSION='s08-markov-path-v1'
Meter=g01.kernel.Meter
MENU=(1,3,5,7,9)


def likelihood(n,r,observed,meter=None):
    """Integer numerator over the common denominator 2*10**(n-1)."""
    if type(n)is not int or n<1 or type(r)is not int or not 0<r<10:raise ValueError('Invalid finite Markov source')
    if any(type(i)is not int or not 0<=i<n or type(v)is not int or v not in (0,1) for i,v in observed.items()):raise ValueError('Invalid observed pattern')
    weights=[1,1]
    if 0 in observed:weights[1-observed[0]]=0
    for i in range(1,n):
        weights=[weights[0]*r+weights[1]*(10-r),weights[0]*(10-r)+weights[1]*r]
        if i in observed:weights[1-observed[i]]=0
    if meter:meter.pay('inference','forward_integer_transition_and_observation',8*n+len(observed))
    return sum(weights)


def world_probability(bits,r):
    result=F(1,2)
    for x,y in zip(bits,bits[1:]):result*=F(r if x==y else 10-r,10)
    return result


def bridge(n,r,a,b,mode,i,meter=None):
    """P(indicator_i=0) conditional on the relevant observed boundaries."""
    if not 0<=a<=i<=b<n or mode not in ('ordinary','left','right'):raise ValueError('Invalid boundary state')
    left=None if a==0 else int(mode=='left')
    right=None if b==n-1 else int(mode=='right')
    def potential(distance,label):
        if label is None:return (1,1)
        same=(10**distance+(2*r-10)**distance)//2
        different=(10**distance-(2*r-10)**distance)//2
        return (same,different) if label==0 else (different,same)
    l=potential(i-a+1,left);q=potential(b-i+1,right)
    weights=[l[0]*q[0],l[1]*q[1]]
    if meter:meter.pay('inference','bridge_powers_products_and_rational_normalization',18)
    return F(weights[0],sum(weights))


def plan(costs,r,roots=None):
    """Optimal for a known model, or evaluate a supplied root policy."""
    if not costs or any(type(c) not in (int,F) or c<=0 for c in costs):raise ValueError('Invalid costs')
    n=len(costs);meter=Meter();tables={k:{} for k in ('ordinary','left','right')};chosen={}
    def at(mode,a,b):return tables[mode][a,b] if a<=b else F(0)
    for length in range(1,n+1):
        for a in range(n-length+1):
            b=a+length-1
            p=bridge(n,r,a,b,'left',a,meter)
            tables['left'][a,b]=costs[a]+p*at('ordinary',a+1,b)+(1-p)*at('left',a+1,b)
            p=bridge(n,r,a,b,'right',b,meter)
            tables['right'][a,b]=costs[b]+p*at('ordinary',a,b-1)+(1-p)*at('right',a,b-1)
            meter.pay('planning','forced_endpoint_values',12)
            if a==b:tables['ordinary'][a,b]=F(0)
            else:
                options=[]
                for i in ([roots[a,b]] if roots is not None else range(a,b+1)):
                    p=bridge(n,r,a,b,'ordinary',i,meter)
                    value=costs[i]+p*(at('ordinary',a,i-1)+at('ordinary',i+1,b))
                    value+=(1-p)*(at('right',a,i-1)+at('left',i+1,b))
                    options.append((value,i));meter.pay('planning','elective_root_value',10)
                tables['ordinary'][a,b],chosen[a,b]=min(options)
            meter.pay('planning','retain_three_tables_and_root',4)
    return dict(n=n,r=r,roots=chosen,tables=tables,bound=tables['ordinary'][0,n-1],invoice=meter.record())


def explicit(costs,r):
    n=len(costs);calls=0
    @lru_cache(None)
    def evaluate(state):
        nonlocal calls
        calls+=1
        if all(state[i]==0 or state[i+1]==0 or (state[i]>=0 and state[i+1]>=0) for i in range(n-1)):return F(0)
        observed={i:x for i,x in enumerate(state) if x>=0};den=likelihood(n,r,observed);choices=[]
        for i,x in enumerate(state):
            if x>=0:continue
            obs=dict(observed);obs[i]=0;p=F(likelihood(n,r,obs),den)
            e=list(state);e[i]=0;m=list(state);m[i]=1
            choices.append(costs[i]+p*evaluate(tuple(e))+(1-p)*evaluate(tuple(m)))
        return min(choices)
    return dict(value=evaluate((-1,)*n),states=calls)


def conditional_trace(bits,roots):
    state=[-1]*len(bits);queries=[]
    while True:
        i=pc.next_query(state,roots)
        if i is None:break
        state[i]=bits[i];queries.append(i)
    assert all(state[i]==0 or state[i+1]==0 or (state[i]>=0 and state[i+1]>=0) for i in range(len(bits)-1))
    return tuple(state),queries


def export(policy):
    return dict(n=policy['n'],r=policy['r'],bound=policy['bound'],invoice=policy['invoice'],
        roots={f'{a},{b}':i for (a,b),i in policy['roots'].items()},
        tables={name:{f'{a},{b}':v for (a,b),v in table.items()} for name,table in policy['tables'].items()})


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(8141435)
    cases=[dict(costs=[rng.randrange(1,10) for _ in range(n)],r=MENU[(n+repeat)%len(MENU)]) for n in range(2,8) for repeat in range(4)]
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,menu=list(MENU),
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'correlated_models.md'),actual_new_audits=0,
        likelihood_scope='All partial indicator patterns for n=1..6, all five menu models; bridge scopes n=2..7'))
    result=dict(status='running',likelihood_checks=0,bridge_checks=0,cases=[],negative_controls=[])
    for n in range(1,7):
        for r in MENU:
            worlds=[(bits,world_probability(bits,r)) for bits in product((0,1),repeat=n)]
            for state in product((-1,0,1),repeat=n):
                obs={i:x for i,x in enumerate(state) if x>=0}
                exact=sum(prob for bits,prob in worlds if all(bits[i]==x for i,x in obs.items()))
                assert F(likelihood(n,r,obs),2*10**(n-1))==exact;result['likelihood_checks']+=1
    for case in cases:
        n=len(case['costs']);r=case['r'];policy=plan(case['costs'],r);bellman=explicit(case['costs'],r)
        assert policy['bound']==bellman['value']
        for a in range(n):
            for b in range(a,n):
                for mode in ('ordinary','left','right'):
                    obs={}
                    if a:obs[a-1]=int(mode=='left')
                    if b<n-1:obs[b+1]=int(mode=='right')
                    base=likelihood(n,r,obs)
                    for i in range(a,b+1):
                        probe=dict(obs);probe[i]=0
                        assert bridge(n,r,a,b,mode,i)==F(likelihood(n,r,probe),base)
                        result['bridge_checks']+=1
        means={q:F(0) for q in MENU};patterns=set()
        for bits in product((0,1),repeat=n):
            pattern,queries=conditional_trace(bits,policy['roots']);patterns.add(pattern)
            fee=sum(case['costs'][i] for i in queries)
            for q in MENU:means[q]+=world_probability(bits,q)*fee
        for q in MENU:assert plan(case['costs'],q,policy['roots'])['bound']==means[q]
        # The adaptively selected terminal patterns partition the whole source.
        normalizers={q:sum(F(likelihood(n,q,{i:x for i,x in enumerate(s) if x>=0}),2*10**(n-1)) for s in patterns) for q in MENU}
        assert all(v==1 for v in normalizers.values())
        result['cases'].append(dict(case=case,policy=export(policy),bellman=bellman,cross_model_fee=means,
            terminal_patterns=len(patterns),terminal_likelihood_normalization=normalizers))
        g01.save(directory/'results.json',result)
    for name,args in [('bad_parameter',(4,10,{})),('unknown_indicator',(4,5,{1:2})),('outside_node',(4,5,{4:0}))]:
        try:likelihood(*args)
        except ValueError as exc:result['negative_controls'].append(dict(name=name,rejected=True,reason=str(exc)))
        else:raise AssertionError('Bad model source accepted')
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat(),
        summary=dict(likelihood_checks=result['likelihood_checks'],bridge_checks=result['bridge_checks'],
            cases=len(cases),bellman_states=sum(c['bellman']['states'] for c in result['cases']),
            cross_model_values=len(cases)*len(MENU),actual_new_audits=0))
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status=result['status'],summary=result['summary'],negative_controls=result['negative_controls'])))


if __name__=='__main__':run(Path(sys.argv[1]))
