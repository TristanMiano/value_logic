"""Exact partial-receipt certificate, DEVELOPMENT, Codex (GPT-6).

Bernstein positivity proves the fixed coefficient bound on entire intervals.
Finite spectral panels separately screen the evaluator and residual identity.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform
import random
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'receipt_probe.json'
assert not OUT.exists()
started=datetime.now(timezone.utc).isoformat()
start=time.perf_counter_ns()

def mul(p,q):
    ans=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):ans[i+j]+=a*b
    return ans

def roots(rs):
    p=[F(1)]
    for r in rs:p=mul(p,[-r,F(1)])
    return p

def at(p,t):
    out=F(0)
    for c in p[::-1]:out=out*t+c
    return out

def bernstein(p,left,right):
    n=len(p)-1
    shifted=[sum(p[i]*comb(i,k)*left**(i-k)*(right-left)**k
                 for i in range(k,n+1)) for k in range(n+1)]
    return [sum(shifted[k]*F(comb(j,k),comb(n,k)) for k in range(j+1))
            for j in range(n+1)]

nodes=list(map(F,[1,2,8,16]))
den=roots([-t for t in nodes])
bn=roots(nodes)
nums=[]
for i,t in enumerate(nodes):
    p=roots(nodes[:i]+nodes[i+1:])
    scale=at(den,t)/at(p,t)
    nums.append([scale*c for c in p])

certificate=[]
for left,right in zip(nodes,nodes[1:]):
    midpoint=(left+right)/2
    signs=[1 if at(p,midpoint)>0 else -1 for p in nums]
    poly=[F(9,4)*c for c in den]
    for s,p in zip(signs,nums):
        for k,c in enumerate(p):poly[k]-=s*c
    pending=[(left,right,0)]
    while pending:
        a,b,depth=pending.pop()
        bs=bernstein(poly,a,b)
        if min(bs)>=0:
            certificate.append(dict(left=str(a),right=str(b),signs=signs,
                                    polynomial=list(map(str,poly)),
                                    bernstein_coefficients=list(map(str,bs))))
        else:
            assert depth<12,('Could not certify',a,b,bs)
            mid=(a+b)/2
            pending.extend([(mid,b,depth+1),(a,mid,depth+1)])
certificate.sort(key=lambda row:F(row['left']))
assert F(certificate[0]['left'])==1 and F(certificate[-1]['right'])==16
assert all(F(a['right'])==F(b['left']) for a,b in zip(certificate,certificate[1:]))

def weights(t):return [at(p,t)/at(den,t) for p in nums]
def product(values):
    result=F(1)
    for v in values:result*=v
    return result
def response(t,law):return sum(w/(1+t*lam) for w,lam in law)
def band(t,intervals):
    ws=weights(t)
    low=sum(w*(lo if w>=0 else hi) for w,(lo,hi) in zip(ws,intervals))
    high=sum(w*(hi if w>=0 else lo) for w,(lo,hi) in zip(ws,intervals))
    b=at(bn,t)/at(den,t)
    return max(F(0),low+min(-b/25,b)),min(F(1),high+max(-b/25,b))

identity_checks=0
for t in [F(i,4) for i in range(4,65)]:
    assert sum(map(abs,weights(t)))<=F(9,4)
    assert abs(at(bn,t)/at(den,t))<=F(1,25)
    for lam in [F(0),F(1,100),F(1,16),F(1,8),F(1,2),F(1),F(7),F(100)]:
        actual=1/(1+lam*t)-sum(w/(1+lam*s) for w,s in zip(weights(t),nodes))
        expected=at(bn,t)/at(den,t)/(1+lam*t)*product((1-lam*s)/(1+lam*s) for s in nodes)
        assert actual==expected
        identity_checks+=1

rng=random.Random(22015)
checks=0
max_width=F(0)
for _ in range(50):
    masses=[rng.randrange(1,11) for _ in range(4)]
    law=[(F(w,sum(masses)),F(rng.randrange(51),rng.randrange(1,21))) for w in masses]
    intervals=[(max(F(0),response(t,law)-F(1,1000)),
                min(F(1),response(t,law)+F(1,1000))) for t in nodes]
    for t in [F(i,4) for i in range(4,65)]:
        lo,hi=band(t,intervals)
        y=response(t,law)
        assert lo<=y<=hi
        assert hi-lo<=F(461,10000)
        max_width=max(max_width,hi-lo)
        checks+=1

result=dict(status='PASS',label='DEVELOPMENT, same-model exact certificate and finite screen',
            contributor='Codex (GPT-6)',started_utc=started,
            ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            python=sys.version,platform=platform.platform(),
            nodes=list(map(str,nodes)),coefficient_bound='9/4',
            residual_bound='1/25',receipt_radius='1/1000',uniform_width='461/10000',
            exact_identity_checks=identity_checks,spectral_panel_checks=checks,
            maximum_screened_width=str(max_width),bernstein_certificate=certificate,
            scope='Uniform coefficient bound is polynomial-certified; spectral panel is finite.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='bernstein_certificate'},indent=2))
print('Certified intervals:',len(certificate))
