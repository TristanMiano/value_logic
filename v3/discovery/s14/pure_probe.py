"""Tiny Fourier/decision-tree screen; Codex (GPT-6), DEVELOPMENT."""
from pathlib import Path
from functools import lru_cache
from datetime import datetime, timezone
import hashlib
import json
import time

out=Path(__file__).with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()

def parity(x):
    return x.bit_count()%2

def walsh(values):
    values=list(values)
    step=1
    while step<len(values):
        for start in range(0,len(values),2*step):
            for j in range(start,start+step):
                a,b=values[j],values[j+step]
                values[j],values[j+step]=a+b,a-b
        step*=2
    return values

@lru_cache(None)
def depth(values):
    if min(values)==max(values):
        return 0
    n=(len(values)-1).bit_length()
    best=n
    for i in range(n):
        children=tuple(tuple(v for j,v in enumerate(values) if ((j>>i)&1)==b) for b in (0,1))
        best=min(best,1+max(depth(child) for child in children))
    return best

panels=[]
fourier_checks=0
for r in (2,3,4):
    g,h=2**r-1,2**(r-1)
    dual={sum(parity(a&i)<<(i-1) for i in range(1,g+1)) for a in range(2**r)}
    assert {d.bit_count() for d in dual}=={0,h}
    todo=set(range(2**g))
    reps=[]
    degrees=[]
    while todo:
        w=min(todo)
        coset={w^d for d in dual}
        todo-=coset
        weights=[v.bit_count() for v in coset]
        assert 2*sum(weights)==len(dual)*g
        assert 4*sum(a*a for a in weights)==len(dual)*(g*g+g)
        degree=max(v.bit_count() for v in coset if v.bit_count()!=h)
        assert degree==0 if w==0 else degree>=h+1
        reps.append(w)
        degrees.append(degree)
    assert min(degrees[1:])==h+1
    chars=[]
    if r<=3:
        quantizer=[]
        for x in range(2**g):
            syndrome=0
            for i in range(1,g+1):
                if x>>(i-1)&1:
                    syndrome^=i
            quantizer.append(x^(1<<(syndrome-1) if syndrome else 0))
        for w,degree in zip(reps,degrees):
            values=tuple(1-2*parity(w&c) for c in quantizer)
            spectrum=walsh(values)
            for v,coefficient in enumerate(spectrum):
                expected=(2**g)*(h-v.bit_count())//h if (v^w) in dual else 0
                assert coefficient==expected
                fourier_checks+=1
            d=depth(values)
            assert d>=degree
            chars.append({'representative':w,'representative_weight':w.bit_count(),
                          'fourier_degree':degree,'exact_decision_depth':d})
    panels.append({'r':r,'block':g,'cosets':len(reps),
                   'minimum_nonconstant_degree':min(degrees[1:]),
                   'characters':chars})

result={'status':'PASS','contributor':'Codex (GPT-6)',
        'scope':'all dual cosets for blocks 3,7,15; exact spectra and character depths for blocks 3,7 only',
        'panels':panels,'fourier_checks':fourier_checks,
        'depth_cache':str(depth.cache_info()),
        'not_checked':'minimum decision depth over arbitrary nonlinear codeword functions; all-protocol cap optimum',
        'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
        'elapsed_ns':time.perf_counter_ns()-clock,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
