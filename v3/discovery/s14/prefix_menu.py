"""Exact small prefix-profile envelope, DEVELOPMENT, Codex (GPT-6)."""
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'prefix_menu.json'
assert not OUT.exists()
start=time.perf_counter_ns()
started=datetime.now(timezone.utc).isoformat()
profiles={1:{(0,)}}
for leaves in range(2,13):
    profiles[leaves]=set()
    for left in range(1,leaves//2+1):
        for p,q in product(profiles[left],profiles[leaves-left]):
            profiles[leaves].add(tuple(sorted(d+1 for d in p+q)))

def data(depths):
    counts=[]
    for d in depths:counts.append(max(d,counts[-1]+1 if counts else d))
    probs=[F(1,2**d) for d in depths]
    assert sum(probs)==1
    return dict(depths=depths,counts=counts,
                D=sum(p*d for p,d in zip(probs,depths)),
                Q=sum(p*t for p,t in zip(probs,counts)))

def fee(row,f):return (row['Q']+f)/row['D']

panels=[]
checks=0
for H in range(2,13):
    rows=[data(p) for L in range(2,H+1) for p in sorted(profiles[L])]
    rows=[r for r in rows if r['counts'][-1]<=H]
    by_D={}
    for r in rows:
        if r['D'] not in by_D or r['Q']<by_D[r['D']]['Q']:by_D[r['D']]=r
    hull=[]
    for r in sorted(by_D.values(),key=lambda x:x['D']):
        while hull:
            prev,prev_start=hull[-1]
            cross=(r['Q']/r['D']-prev['Q']/prev['D'])/(1/prev['D']-1/r['D'])
            if prev_start is None or cross>prev_start:break
            hull.pop()
        hull.append((r,cross if hull else None))
    active=0
    for j,(_,s) in enumerate(hull):
        if s is None or s<=0:active=j
    hull=hull[active:]
    starts=[F(0)]+[s for _,s in hull[1:]]
    assert all(s>=0 for s in starts)
    probes={F(0),F(1),F(10),F(100),starts[-1]+1}
    for s in starts:probes.add(s)
    for a,b in zip(starts,starts[1:]):probes.add((a+b)/2)
    for f in probes:
        j=max(i for i,s in enumerate(starts) if s<=f)
        assert fee(hull[j][0],f)==min(fee(r,f) for r in rows)
        checks+=len(rows)
    baseline=data(tuple(range(1,H-1))+(H-1,H-1))
    assert baseline['D']==2-F(1,2**(H-2))
    assert baseline['Q']==2-F(1,2**(H-1))
    panels.append(dict(H=H,feasible_profiles=len(rows),distinct_progress=len(by_D),
                       phases=[dict(start=s,**r) for s,(r,_) in zip(starts,hull)],
                       selected=[dict(reset=f,best=min(fee(r,f) for r in rows),
                                      prefix=fee(baseline,f)) for f in (F(0),F(1),F(10),F(100))]))

def encode(x):
    if isinstance(x,F):return str(x)
    raise TypeError(type(x).__name__)

result=dict(status='PASS',label='DEVELOPMENT exact finite menu, not all-protocol optimum',
            contributor='Codex (GPT-6)',started_utc=started,
            ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,python=sys.version,platform=platform.platform(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            profile_counts={L:len(p) for L,p in profiles.items()},
            envelope_comparisons=checks,panels=panels)
OUT.write_text(json.dumps(result,indent=2,default=encode)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status=result['status'],runtime_ns=result['runtime_ns'],
                      profiles=result['profile_counts'],envelope_comparisons=checks,
                      panels=[dict(H=p['H'],phases=len(p['phases']),selected=p['selected']) for p in panels]),
                 indent=2,default=encode))
