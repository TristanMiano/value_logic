"""Exact folded sampling laws; source independence of deletion; reset scope."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import math
import platform
import time

start=time.perf_counter_ns()
def C(n,k): return math.comb(n,k) if 0<=k<=n else 0
def law(n,d,a):
    m=n//2
    den=C(n,d)
    out={}
    for t in range(d//2+1):
        num=C(m+a,t)*C(m-a,d-t)
        if 2*t!=d: num+=C(m+a,d-t)*C(m-a,t)
        out[t]=F(num,den)
    return out
def div(p,q):
    if any(v and not q[k] for k,v in p.items()): return math.inf
    return sum(float(v)*math.log(float(v/q[k])) for k,v in p.items() if v)

laws=deletions=direct=0
table=[]
for n in range(4,18,2):
    previous=-1e-12
    for d in range(1,n+1):
        for a in range(n//2+1):
            p=law(n,d,a)
            assert sum(p.values())==1
            laws+=1
            if d>1:
                smaller=defaultdict(F)
                for t,prob in p.items():
                    if t: smaller[min(t-1,d-t)]+=prob*F(t,d)
                    if t<d: smaller[min(t,d-1-t)]+=prob*F(d-t,d)
                assert all(smaller[k]==v for k,v in law(n,d-1,a).items())
                deletions+=1
            if n<=8:
                x=[1]*(n//2+a)+[0]*(n//2-a)
                observed=defaultdict(int)
                for I in combinations(range(n),d):
                    k=sum(x[i] for i in I)
                    observed[min(k,d-k)]+=1
                assert all(F(observed[k],C(n,d))==v for k,v in p.items())
                direct+=1
        p,q=law(n,d,0),law(n,d,1)
        if d<n: assert all(not v or q[k]>0 for k,v in p.items())
        D=div(p,q)
        assert D>=previous-1e-12
        previous=D
        if n==8:
            table.append(dict(cap=d+1,comparison_queries=d,kl_01=(D if math.isfinite(D) else 'infinity'),
                              expected_episodes_lower=(.98*math.log(99)/D if 0<D<math.inf else None),
                              note='Comparison experiment may require more count symbols than this cap permits.'))

channels={}
for x in product((0,1),repeat=2):
    distribution=defaultdict(F)
    for r in (0,1): distribution[(x[0]^r,x[1]^r)]+=F(1,2)
    q=x[0]^x[1]
    if q in channels: assert channels[q]==distribution
    channels[q]=distribution
    assert all(a^b==q for a,b in distribution)

out=dict(status='PASS',exact_laws=laws,exact_deletion_relations=deletions,
         direct_subset_checks=direct,n8_comparison=table,shared_coin_inputs_checked=4,
         source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         python=platform.python_version(),elapsed_perf_counter_ns=time.perf_counter_ns()-start,
         scope='Finite exact laws and scope counterexample; no measured fee savings or optimal count-channel construction at every cap.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
