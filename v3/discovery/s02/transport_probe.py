"""DEVELOPMENT: exact aggregate-count/product-relation value bounds.

Codex (GPT-6), 2026-10-11. Supplied relations are assumptions at this kernel
boundary; a caller must justify them for its actual mathematical sources.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import random
import sys
import time
import traceback

PAIRS=((0,0),(0,1),(1,0),(1,1))
STATES=tuple(tuple(c) for k in range(1,5) for c in combinations(PAIRS,k))


class Conflict(ValueError):pass


def endpoint(L,U,states,weights,constant=F(0),upper=False):
    N=len(states)
    if type(L) is not int or type(U) is not int or len(weights)!=N or not 0<=L<=U<=N:
        raise ValueError('Malformed count/value input')
    x=[None]*N;y=[None]*N;free=[];forced_ones=0
    for i,(allowed,w) in enumerate(zip(states,weights)):
        if not allowed:raise Conflict('Empty coordinate relation')
        if any(type(a) is not int or type(b) is not int or (a,b) not in PAIRS for a,b in allowed):
            raise ValueError('Malformed bit pair')
        choices={}
        for a in (0,1):
            values=[(w*b,b) for aa,b in allowed if aa==a]
            if values:choices[a]=(max if upper else min)(values)
        if len(choices)==1:
            a=next(iter(choices));x[i]=a;y[i]=choices[a][1];forced_ones+=a
        else:
            delta=choices[1][0]-choices[0][0]
            free.append((delta,i,choices))
    lo=max(0,L-forced_ones);hi=min(len(free),U-forced_ones)
    if lo>hi:raise Conflict('Count interval conflicts with coordinate evidence')
    free.sort(key=lambda item:((-item[0] if upper else item[0]),item[1]))
    preferred=sum(delta>0 if upper else delta<0 for delta,_,_ in free)
    k=max(lo,min(hi,preferred))
    for j,(_,i,choices) in enumerate(free):
        a=int(j<k);x[i]=a;y[i]=choices[a][1]
    value=constant+sum((w*b for w,b in zip(weights,y)),F(0))
    assert L<=sum(x)<=U and all((a,b) in S for a,b,S in zip(x,y,states))
    return dict(value=value,base=x,edited=y,selected_free_ones=k,free_coordinates=len(free))


def bounds(L,U,states,weights,constant=F(0)):
    try:
        lower=endpoint(L,U,states,weights,constant)
        upper=endpoint(L,U,states,weights,constant,True)
        assert lower['value']<=upper['value']
        return dict(status='bounded',lower=lower,upper=upper)
    except Conflict as exc:
        return dict(status='source_conflict',reason=str(exc))


def small_screen():
    rng=random.Random(8601);cases=0;conflicts=0;worlds=0
    for n in range(7):
        for trial in range(50):
            states=[rng.choice(STATES) for _ in range(n)]
            weights=[F(rng.randrange(-9,10),rng.randrange(1,6)) for _ in range(n)]
            L,U=sorted((rng.randrange(n+1),rng.randrange(n+1)))
            constant=F(rng.randrange(-3,4),3)
            values=[]
            for pairs in product(*states):
                worlds+=1
                if L<=sum(a for a,b in pairs)<=U:
                    values.append(constant+sum((w*b for w,(a,b) in zip(weights,pairs)),F(0)))
            result=bounds(L,U,states,weights,constant)
            if not values:
                assert result['status']=='source_conflict';conflicts+=1
            else:
                assert result['status']=='bounded'
                assert (result['lower']['value'],result['upper']['value'])==(min(values),max(values))
            cases+=1
    closed_forms=0
    n=6
    for mask in range(1<<n):
        A=[i for i in range(n) if mask>>i&1];B=[i for i in range(n) if not mask>>i&1]
        states=[PAIRS if i in A else ((0,0),(1,1)) for i in range(n)]
        q=[F(i+1,n*(n+1)//2) for i in range(n)]
        for L,U in ((0,6),(2,4),(3,3),(5,6)):
            r=bounds(L,U,states,q)
            lower=sum(sorted(q[i] for i in B)[:max(0,L-len(A))],F(0))
            upper=sum((q[i] for i in A),F(0))+sum(sorted((q[i] for i in B),reverse=True)[:min(U,len(B))],F(0))
            assert r['lower']['value']==lower and r['upper']['value']==upper
            closed_forms+=1
    assert bounds(1,1,[((0,0),)],[F(1)])['status']=='source_conflict'
    assert bounds(0,1,[()],[F(1)])['status']=='source_conflict'
    return dict(random_cases=cases,enumerated_pair_worlds=worlds,source_conflicts=conflicts,
                local_edit_closed_forms=closed_forms,explicit_conflicts=2)


def main(output):
    assert not output.exists()
    result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='Exact rational kernel on a supplied product relation and one count interval. Finite enumeration is limited to N<=6; larger timings exclude common input generation and serialization, include both endpoints/witness construction/local feasibility checks. No arbitrary coupled-CNF or novelty claim.')
    start=time.monotonic_ns()
    try:
        result['checks']=small_screen()
        rows=[]
        for N in (1000,10000):
            rng=random.Random(8601+N)
            states=[rng.choice(STATES) for _ in range(N)]
            weights=[F(rng.randrange(-20,21),20) for _ in range(N)]
            # This interval is deliberately broad; random forced receipts can
            # be present, and endpoint witnesses still have to be feasible.
            L,U=N//4,3*N//4
            before=time.perf_counter_ns();r=bounds(L,U,states,weights);elapsed=time.perf_counter_ns()-before
            row=dict(N=N,seed=8601+N,L=L,U=U,elapsed_ns=elapsed,status=r['status'])
            if r['status']=='bounded':
                row.update(lower=r['lower']['value'],upper=r['upper']['value'],
                           endpoint_sha256=hashlib.sha256(json.dumps(r,default=str).encode()).hexdigest())
            rows.append(row)
        result.update(status='complete',rows=rows)
    except Exception:
        result.update(status='failed',failure=traceback.format_exc());raise
    finally:
        result.update(elapsed_ns=time.monotonic_ns()-start,end_utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps(result,default=str))


if __name__=='__main__':main(Path(sys.argv[1]))
