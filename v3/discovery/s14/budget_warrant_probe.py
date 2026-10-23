"""Finite affine-fiber screen of budget warrants; DEVELOPMENT, Codex (GPT-6)."""
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import random
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'budget_warrant_probe.json'
assert not OUT.exists()
start=time.perf_counter_ns()
started=datetime.now(timezone.utc).isoformat()
rng=random.Random(2026102218)

def parity(x):return x.bit_count()%2
def span(rows):
    s={0}
    for r in rows:s|={x^r for x in s}
    return s

panels=0
world_checks=0
strict_relaxations=0
for n in (2,3,4,5,6):
    for case in range(8):
        dual=span(rng.randrange(1,1<<n) for _ in range(rng.randrange(n+1)))
        x0=rng.randrange(1<<n)
        source=[x for x in range(1<<n) if all(parity((x^x0)&h)==0 for h in dual)]
        prices=[rng.randrange(1,5) for _ in range(n)]
        for B in (0,1,2,4,8):
            affordable=[]
            for h in dual-{0}:
                costs=[prices[i] for i in range(n) if (h>>i)&1]
                if sum(costs)-max(costs)<=B:affordable.append(h)
            W={x for x in range(1<<n) if all(not parity((x^x0)&h) for h in affordable)}
            direct=set(range(1<<n))
            for S in range(1<<n):
                if sum(prices[i] for i in range(n) if (S>>i)&1)>B:continue
                fibers={}
                for x in source:fibers.setdefault(x&S,[]).append(x)
                for x in list(direct):
                    fiber=fibers.get(x&S)
                    if not fiber:continue
                    for j in range(n):
                        if (S>>j)&1:continue
                        values={(y>>j)&1 for y in fiber}
                        if len(values)==1 and ((x>>j)&1) not in values:
                            direct.remove(x)
                            break
            assert W==direct,(n,case,B,prices,dual,W,direct)
            assert set(source)<=W
            strict_relaxations+=len(W)>len(source)
            panels+=1
            world_checks+=1<<n

def graph_panel(n,edges):
    m=len(edges)
    even=[]
    for mask in range(1<<m):
        degrees=[0]*n
        for j,(a,b) in enumerate(edges):
            if (mask>>j)&1:degrees[a]^=1;degrees[b]^=1
        if not any(degrees):even.append(mask)
    # Greedy over the entire tiny cycle space; no claim of a scalable algorithm.
    basis=[]
    current={0}
    for c in sorted(even,key=lambda x:(x.bit_count(),x)):
        if c not in current:
            basis.append(c)
            current|={x^c for x in current}
    assert current==set(even)
    thresholds=[]
    for k in range(m):
        full=span(c for c in even if c.bit_count()<=k+1)
        short=span(c for c in basis if c.bit_count()<=k+1)
        assert full==short
        thresholds.append(dict(k=k,rank=len(full).bit_length()-1,warrant_worlds=2**m//len(full)))
    return dict(vertices=n,edges=edges,basis=basis,basis_lengths=[c.bit_count() for c in basis],thresholds=thresholds)

graphs=[graph_panel(7,[(0,1),(1,2),(2,0),(0,3),(3,4),(4,5),(5,6),(6,0)]),
        graph_panel(4,list(combinations(range(4),2))),
        graph_panel(4,[(0,1),(1,2),(2,0),(1,3),(3,2)])]
assert graphs[0]['basis_lengths']==[3,5]
assert graphs[0]['thresholds'][2]['warrant_worlds']==128
assert graphs[0]['thresholds'][4]['warrant_worlds']==64
result=dict(status='PASS',label='DEVELOPMENT small exact screen; not independent confirmation',
            contributor='Codex (GPT-6)',started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            python=sys.version,platform=platform.platform(),affine_panels=panels,world_checks=world_checks,
            strict_relaxations=strict_relaxations,graph_panels=graphs)
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='graph_panels'},indent=2))
