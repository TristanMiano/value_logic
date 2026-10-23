"""Bounded exact lossy Bellman screen; Codex (GPT-6), DEVELOPMENT."""
from pathlib import Path
from itertools import product
from functools import lru_cache
from datetime import datetime, timezone
import hashlib
import json
import time

out=Path(__file__).with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()

def maps(n):
    worlds=range(1<<n)
    result=set()
    for i in range(n):
        children={tuple([1]*(1<<n))}
        for j in range(n):
            if j!=i:
                for labels in product((2,3),repeat=2):
                    children.add(tuple(labels[(x>>j)&1] for x in worlds))
        for left,right in product(children,repeat=2):
            result.add(tuple((right if x>>i&1 else left)[x] for x in worlds))
    return sorted(result)

panels=[]
for n in (3,4):
    bank=maps(n)
    masks=[tuple(sum(1<<x for x,label in enumerate(m) if label==t) for t in (1,2,3)) for m in bank]
    bitmasks=[sum(1<<x for x in range(1<<n) if x>>i&1) for i in range(n)]
    @lru_cache(None)
    def risk(w):
        size=w.bit_count()
        return sum(min((w&mask).bit_count(),size-(w&mask).bit_count()) for mask in bitmasks)
    @lru_cache(None)
    def transitions(w):
        result=[]
        for triple in masks:
            parts=tuple(w&a for a in triple)
            if w in parts:
                continue
            q=sum(t*p.bit_count() for t,p in enumerate(parts,1))
            result.append((q,tuple(p for p in parts if p)))
        return tuple(result)
    for fee in (1,10,100):
        t0=time.perf_counter_ns()
        states=0
        improving_states=0
        @lru_cache(None)
        def value(w):
            global states,improving_states
            states+=1
            if states>10000 or time.perf_counter_ns()-t0>30_000_000_000:
                raise TimeoutError((states,time.perf_counter_ns()-t0))
            size=w.bit_count()
            stop=(7+4*fee)*risk(w)
            best=stop
            for q,parts in transitions(w):
                cost=3*(q+fee*size)+sum(value(p) for p in parts)
                best=min(best,cost)
            improving_states+=best<stop
            return best
        root=(1<<(1<<n))-1
        try:
            optimum=value(root)
            stop=(7+4*fee)*n*(1<<(n-1))
            status='COUNTEREXAMPLE' if optimum<stop else 'NO_COUNTEREXAMPLE'
            assert optimum<=stop
            panel={'n':n,'fee':fee,'status':status,'scaled_optimum_mass':optimum,
                   'scaled_stop_mass':stop,'scaling':'multiply objective fee+2*gamma*error by3 and by2^n',
                   'states':states,'locally_improving_states':improving_states,
                   'count_maps':len(bank),'elapsed_ns':time.perf_counter_ns()-t0}
        except TimeoutError as exc:
            panel={'n':n,'fee':fee,'status':'INCONCLUSIVE_CAP','detail':str(exc),
                   'states':states,'elapsed_ns':time.perf_counter_ns()-t0}
        panels.append(panel)
        print(json.dumps(panel),flush=True)
result={'status':'COMPLETE','contributor':'Codex (GPT-6)','panels':panels,
        'scope':'finite exact source panels only, no general optimality claim',
        'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
        'elapsed_ns':time.perf_counter_ns()-clock,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
