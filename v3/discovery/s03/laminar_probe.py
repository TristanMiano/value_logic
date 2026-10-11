"""Finite constructive checks and charged kernel timing, not confirmation."""
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import time
from datetime import datetime,timezone
from laminar import CountTree,Conflict,endpoints


def exhaustive(tree,pairs,weights):
    vals=[];xs=[];worlds=0
    for world in product(*pairs):
        x=tuple(p[0] for p in world)
        if not tree.feasible(x):
            continue
        worlds+=1;xs.append(x)
        vals.append(sum((w*p[1] for w,p in zip(weights,world)),Fraction()))
    return (min(vals),max(vals)) if vals else None,worlds,xs


def run():
    rng=random.Random(91351);cases=[];total_worlds=0;conflicts=0;projections=0
    all_pairs=((0,0),(0,1),(1,0),(1,1))
    for case in range(360):
        n=rng.randint(1,7);shape=CountTree(n)
        bounds={}
        for v,node in enumerate(shape.nodes):
            if rng.random()<.65:
                a,b=sorted((rng.randrange(node.size+1),rng.randrange(node.size+1)))
                bounds[v]=(a,b)
        pairs=[tuple(p for p in all_pairs if rng.random()<.8) for _ in range(n)]
        allowed=[{0,1} if rng.random()<.8 else {rng.randrange(2)} for _ in range(n)]
        weights=[Fraction(rng.randint(-7,7),rng.randint(1,5)) for _ in range(n)]
        tree=CountTree(n,bounds,allowed)
        expected,worlds,xs=exhaustive(tree,pairs,weights);total_worlds+=worlds
        try:
            lo,hi=endpoints(tree,pairs,weights)
            actual=(lo[0],hi[0])
        except Conflict:
            actual=None;conflicts+=1
        assert actual==expected,(case,actual,expected)
        # Projection uses only the count/allowed-bit source, not pair restrictions.
        plain=[x for x in product((0,1),repeat=n) if tree.feasible(x)]
        for v in range(len(tree.nodes)):
            try:
                a,b,_=tree.interval(v)
                ds=tree.descendants(v)
                want=[sum(x[i] for i in ds) for x in plain]
                assert want and (a,b)==(min(want),max(want))
            except Conflict:
                assert not plain
            projections+=1
        cases.append({'case':case,'n':n,'worlds':worlds,'endpoints':None if actual is None else list(map(str,actual))})

    # Dynamic receipts and restoration, including statistical-source conflicts.
    dynamic=[]
    for case in range(90):
        n=rng.randint(2,8);shape=CountTree(n)
        truth=[rng.randrange(2) for _ in range(n)]
        bounds={}
        for v,node in enumerate(shape.nodes):
            k=sum(truth[i] for i in shape.descendants(v))
            bounds[v]=(max(0,k-rng.randrange(3)),min(node.size,k+rng.randrange(3)))
        tree=CountTree(n,bounds);order=rng.sample(range(n),n);steps=0
        for i in order:
            steps+=tree.set_allowed(i,{truth[i]},tree.version)
            plain=[x for x in product((0,1),repeat=n) if tree.feasible(x)]
            for v in range(len(tree.nodes)):
                ds=tree.descendants(v);want=[sum(x[j] for j in ds) for x in plain]
                assert tree.interval(v)[:2]==(min(want),max(want))
        for i in reversed(order):
            steps+=tree.set_allowed(i,{0,1},tree.version)
        assert tree.interval(0)[:2]==CountTree(n,bounds).interval(0)[:2]
        dynamic.append({'case':case,'n':n,'updates':2*n,'path_steps':steps})
    conflict_tree=CountTree(4,{0:(3,4)})
    conflict_tree.set_allowed(0,{0},0);conflict_tree.set_allowed(1,{0},1)
    try:
        conflict_tree.interval(0)
        raise AssertionError('conflict was hidden')
    except Conflict:
        pass
    # One bad-domain and stale update leave state unchanged.
    before=(conflict_tree.version,list(map(set,conflict_tree.allowed)))
    for args in [(2,[0,False],2),(2,{1},0)]:
        try:
            conflict_tree.set_allowed(*args)
            raise AssertionError('invalid update accepted')
        except ValueError:
            assert before==(conflict_tree.version,conflict_tree.allowed)

    timings=[]
    for n in (1024,8192):
        truth=[rng.randrange(2) for _ in range(n)]
        shape=CountTree(n);bounds={}
        for v,node in enumerate(shape.nodes):
            if node.leaf is None:
                k=sum(truth[i] for i in shape.descendants(v))
                bounds[v]=(max(0,k-2),min(node.size,k+2))
        pairs=[all_pairs if rng.random()<.1 else ((0,0),(1,1)) for _ in range(n)]
        weights=[Fraction(rng.randint(-20,20),rng.randint(1,7)) for _ in range(n)]
        start=time.perf_counter_ns();tree=CountTree(n,bounds);build=time.perf_counter_ns()-start
        start=time.perf_counter_ns();lo,hi=endpoints(tree,pairs,weights);optim=time.perf_counter_ns()-start
        changes=rng.sample(range(n),min(n,1000));queries=[rng.randrange(len(tree.nodes)) for _ in range(1000)]
        start=time.perf_counter_ns();update_steps=sum(tree.set_allowed(i,{truth[i]},tree.version) for i in changes);update_ns=time.perf_counter_ns()-start
        start=time.perf_counter_ns();answers=[tree.interval(v) for v in queries];query_ns=time.perf_counter_ns()-start
        assert all(a<=sum(truth[i] for i in tree.descendants(v))<=b for v,(a,b,_) in zip(queries,answers))
        timings.append({'n':n,'nodes':len(tree.nodes),'build_ns':build,'both_weighted_endpoints_ns':optim,
                        'weighted_merge_items':lo[3]+hi[3],'updates':len(changes),'updates_ns':update_ns,'update_path_steps':update_steps,
                        'queries':len(queries),'queries_ns':query_ns,'query_path_steps':sum(r[2] for r in answers),
                        'endpoints':[str(lo[0]),str(hi[0])]})
    return {'status':'complete','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)',
            'utc':datetime.now(timezone.utc).isoformat(),'cases':cases,'feasible_pair_worlds':total_worlds,
            'infeasible_cases':conflicts,'static_node_projection_checks':projections,'dynamic_cases':dynamic,
            'explicit_conflict_cases':1,'invalid_update_cases':2,'timings':timings,
            'timing_scope':'Prepared input. Build includes tree/bounds validation; optimizer includes witnesses and checks. Timings exclude input generation, separate reference checks and serialization. Count bounds in these fixtures are supplied, not statistically acquired.',
            'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(__file__).with_name('laminar.py'))}}


if __name__=='__main__':
    out=Path(__file__).with_name('laminar01.json')
    assert not out.exists(),'Do not overwrite an exposed run'
    result=run();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','dynamic_cases')}))
