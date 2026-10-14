#!/usr/bin/env python3
"""Independent finite reconstructions; no actual source acquisitions.
Codex (GPT-6), 2026-10-14. DEVELOPMENT, not confirmation.
"""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
from datetime import datetime,timezone
import json
import random
import sys
import time
import g01

HERE=Path(__file__).resolve().parent
VERSION='s08-star-check-v1'


def closed_form(costs,probabilities):
    center=costs[0];p0=probabilities[0]
    order=sorted(range(1,len(costs)),key=lambda i:(probabilities[i]==1,
        costs[i]/(1-probabilities[i]) if probabilities[i]<1 else F(0),i))
    survival=F(1);attempt=F(0)
    for i in order:
        attempt+=survival*costs[i];survival*=probabilities[i]
    gain=center*survival-p0*attempt
    baseline=center+(1-p0)*sum(costs[1:])
    return dict(order=order,gain=gain,baseline=baseline,value=baseline-max(F(0),gain))


def safe_star(state):
    """Directly check whether a fixed endpoint choice can minimize each edge."""
    for i in range(1,len(state)):
        a=[state[0]] if state[0]>=0 else [0,1,2]
        b=[state[i]] if state[i]>=0 else [0,1,2]
        if not (all(x<=y for x in a for y in b) or all(y<=x for x in a for y in b)):
            return False
    return True


def explicit_bellman(costs,probabilities):
    n=len(costs);calls=0;queries=0
    @lru_cache(None)
    def evaluate(state):
        nonlocal calls,queries
        calls+=1
        if safe_star(state):return F(0)
        choices=[]
        for i,x in enumerate(state):
            if x>=0:continue
            value=F(costs[i]);queries+=1
            law=(probabilities[i]/2,1-probabilities[i],probabilities[i]/2)
            for outcome,probability in enumerate(law):
                nxt=list(state);nxt[i]=outcome
                value+=probability*evaluate(tuple(nxt))
            choices.append(value)
        return min(choices)
    value=evaluate((-1,)*n)
    return dict(value=value,states=calls,query_options=queries)


def binary_minimax(edges,n):
    records=[];action_evaluations=0
    for state in product((-1,0,1),repeat=n):
        worlds=list(product(*([x] if x>=0 else [0,1] for x in state)))
        best=None
        for counts in product((0,1,2),repeat=len(edges)):
            worst=max(sum(w*(k*t[a]+(2-k)*t[b]-2*min(t[a],t[b]))
                for (a,b,w),k in zip(edges,counts)) for t in worlds)
            best=worst if best is None else min(best,worst)
            action_evaluations+=1
        residual=max(sum(w*abs(t[a]-t[b]) for a,b,w in edges if state[a]<0 and state[b]<0) for t in worlds)
        assert best==residual
        records.append(dict(state=state,minimax=best,residual_maxcut=residual))
    return dict(n=n,edges=edges,states=len(records),action_evaluations=action_evaluations,records=records)


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(8141026)
    cases=[]
    for n in range(2,7):
        for repeat in range(5):
            cases.append(dict(costs=[rng.randrange(1,11) for _ in range(n)],
                probabilities=[F(rng.randrange(5),4) for _ in range(n)]))
    cases.append(dict(costs=[10,1,1,1,1],probabilities=[F(1,2)]+[F(9,10)]*4))
    graphs=[dict(n=2,edges=[[0,1,1]]),dict(n=3,edges=[[0,1,1],[1,2,2]]),
        dict(n=3,edges=[[0,1,1],[1,2,1],[2,0,1]]),
        dict(n=4,edges=[[0,1,2],[1,2,1],[2,3,3],[0,3,1]])]
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT',
        contributor='Codex (GPT-6)',created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,graphs=graphs,
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'star_audits.md'),
        actual_new_audits=0,scope='Read-only finite Bellman and minimax reconstruction, no service timing claim'))
    start=time.perf_counter_ns();result=dict(status='running',stars=[],binary=[])
    for case in cases:
        probabilities=case['probabilities'];costs=list(map(F,case['costs']))
        formula=closed_form(costs,probabilities);exact=explicit_bellman(costs,probabilities)
        assert formula['value']==exact['value']
        best_gain=None;orders=0
        for order in permutations(range(1,len(costs))):
            survival=F(1);attempt=F(0)
            for i in order:attempt+=survival*costs[i];survival*=probabilities[i]
            gain=costs[0]*survival-probabilities[0]*attempt
            best_gain=gain if best_gain is None else max(best_gain,gain);orders+=1
        assert best_gain==formula['gain']
        result['stars'].append(dict(case=case,formula=formula,bellman=exact,orders_compared=orders))
        g01.save(directory/'results.json',result)
    for graph in graphs:
        result['binary'].append(binary_minimax(**graph));g01.save(directory/'results.json',result)
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat(),
        wall_ns=time.perf_counter_ns()-start,
        summary=dict(stars=len(cases),bellman_states=sum(x['bellman']['states'] for x in result['stars']),
            leaf_orders=sum(x['orders_compared'] for x in result['stars']),
            strict_improvements=sum(x['formula']['value']<x['formula']['baseline'] for x in result['stars']),
            binary_information_states=sum(x['states'] for x in result['binary']),
            binary_action_evaluations=sum(x['action_evaluations'] for x in result['binary']),actual_new_audits=0))
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status=result['status'],summary=result['summary'],worked=result['stars'][-1]),default=g01.encode))


if __name__=='__main__':run(Path(sys.argv[1]))
