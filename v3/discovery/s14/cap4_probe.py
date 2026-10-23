"""DEVELOPMENT: cheap falsification of one cap-four potential proposal.

Three unknown coordinates and a fourth known padding coordinate. Enumerate
all maps realizable by a distinct-coordinate tree and terminal padding to 4.
All 255 nonempty sources are screened. No all-size optimality claim.
Budget: one bounded enumeration, no parameter tuning or heavy solver.
"""
from datetime import datetime, timezone
from functools import lru_cache
from itertools import product
from math import log2
from pathlib import Path
import hashlib
import json
import platform
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'cap4_probe.json'
assert not OUT.exists()
started=datetime.now(timezone.utc).isoformat()
start=time.perf_counter_ns()

@lru_cache(None)
def maps(worlds, remaining, depth):
    ans={tuple([c]*len(worlds)) for c in range(max(1,depth),5)}
    for bit in remaining:
        rem=tuple(i for i in remaining if i!=bit)
        lo=tuple(x for x in worlds if not (x>>bit)&1)
        hi=tuple(x for x in worlds if (x>>bit)&1)
        for left,right in product(maps(lo,rem,depth+1),maps(hi,rem,depth+1)):
            d=dict(zip(lo,left));d.update(zip(hi,right))
            ans.add(tuple(d[x] for x in worlds))
    return tuple(sorted(ans))

def edges(w):
    return sum(bool(w&(1<<x)) and bool(w&(1<<(x^(1<<i))))
               for x in range(8) for i in range(3) if not (x>>i)&1)

functions=maps(tuple(range(8)),(0,1,2),0)
ec=[edges(w) for w in range(256)]
elog=[s*log2(s) if s else 0.0 for s in range(9)]
fees=(0.25,0.5,1,2,5,10,100)
worst={f:dict(margin=float('inf')) for f in fees}
count=0
for fn in functions:
    cells=tuple(sum(1<<x for x,t in enumerate(fn) if t==j) for j in range(1,5))
    for w in range(1,256):
        m=w.bit_count()
        parts=[w&cell for cell in cells]
        ns=[p.bit_count() for p in parts]
        e=ec[w]-sum(ec[p] for p in parts)
        h=elog[m]-sum(elog[s] for s in ns)
        q=sum(j*s for j,s in enumerate(ns,1))
        for f in fees:
            a,b=(16+2*f)/7,(6*f-1)/14
            margin=q+f*m-a*e-b*h
            if margin<worst[f]['margin']:
                worst[f]=dict(margin=margin,source=[x for x in range(8) if w&(1<<x)],
                              invoice_map=fn,cell_sizes=ns,crossed_edges=e,
                              entropy_mass=h,query_mass=q,a=a,b=b)
            count+=1

result=dict(status='COMPLETED',label='DEVELOPMENT finite falsification screen',
            contributor='Codex (GPT-6)',started_utc=started,
            ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,python=sys.version,
            platform=platform.platform(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            maps=len(functions),sources=255,comparisons=count,panels=worst,
            scope='Necessary local screens for proposed coefficients only; float entropy.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,indent=2))
