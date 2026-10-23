"""Exact finite transport screen, DEVELOPMENT, Codex (GPT-6).

Rational matrix inverses and squared-radical comparisons establish each panel
without floating-point tolerances. Floating point is used only to compare
the earlier Phi/additive adapters and to display widths.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import platform
import random
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'transport_probe.json'
assert not OUT.exists()
started=datetime.now(timezone.utc).isoformat()
start=time.perf_counter_ns()
rng=random.Random(2026102214)

def inv(A):
    n=len(A)
    B=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next(k for k in range(j,n) if B[k][j])
        B[j],B[k]=B[k],B[j]
        z=B[j][j]
        B[j]=[x/z for x in B[j]]
        for i in range(n):
            if i!=j:
                z=B[i][j]
                B[i]=[x-z*y for x,y in zip(B[i],B[j])]
    return [r[n:] for r in B]

def value(M,v):
    n=len(M)
    A=[[F(i==j)+sum(a*b for a,b in zip(M[i],M[j])) for j in range(n)] for i in range(n)]
    R=inv(A)
    assert all(sum(A[i][k]*R[k][j] for k in range(n))==int(i==j)
               for i in range(n) for j in range(n))
    return sum(v[i]*R[i][j]*v[j] for i in range(n) for j in range(n))

def unit(n):
    if n==1:return [F(1)]
    u=[F(0)]*n
    j,k=rng.sample(range(n),2)
    a,b=rng.choice(((F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(0),F(1))))
    u[j],u[k]=rng.choice((-1,1))*a,rng.choice((-1,1))*b
    assert sum(x*x for x in u)==1
    return u

def lower_holds(s,t,a):
    # Is t >= L_e(s)? a>=1 rational and e=a-1/a.
    e=a-1/a
    if s<=a*a/(1+a*a):return t>=s/(a*a)
    z=s/t-1-e*e*s
    return z<=0 or z*z<=4*e*e*s*(1-s)

def low(s,e):
    a=(math.sqrt(e*e+4)+e)/2
    if s<=a*a/(1+a*a):return s/(a*a)
    return 1/(1+(math.sqrt((1-s)/s)+e)**2)

def high(s,e):
    a=(math.sqrt(e*e+4)+e)/2
    if s<=1/(1+a*a):return s*a*a
    return 1/(1+max(0,math.sqrt((1-s)/s)-e)**2)

def phi(s):
    return math.log(2*s) if s<=.5 else 1-math.sqrt((1-s)/s)

def unphi(r):
    return .5*math.exp(r) if r<=0 else 1/(1+(1-r)**2) if r<1 else 1.

alphas=[F(1),F(101,100),F(5,4),F(2),F(4),F(10)]
matrix_panels=0
for n,m in ((1,1),(2,1),(2,2),(2,3),(3,2),(3,3)):
    for seed in range(30):
        M=[[F(rng.randrange(-12,13),rng.choice((1,2,5))) for j in range(m)] for i in range(n)]
        v,u,z=unit(n),unit(n),unit(m)
        s=value(M,v)
        for a in alphas:
            e=a-1/a
            N=[[M[i][j]+e*u[i]*z[j] for j in range(m)] for i in range(n)]
            t=value(N,v)
            assert 0<s<=1 and 0<t<=1
            assert lower_holds(s,t,a),('lower',n,m,seed,a,s,t)
            assert lower_holds(t,s,a),('upper',n,m,seed,a,s,t)
            matrix_panels+=1

scalar_equalities=0
for a in alphas:
    e=a-1/a
    for j in range(11):
        m=F(j,10)/a
        s=1/(1+m*m)
        t=1/(1+(m+e)**2)
        assert s>=a*a/(1+a*a)
        z=s/t-1-e*e*s
        assert z>=0 and z*z==4*e*e*s*(1-s)
        scalar_equalities+=1

limits=[]
for a in alphas[1:]:
    sp=a*a/(1+a*a)
    s=sp/3
    gaps=[]
    for K in (10,100,1000,10000):
        r=F(1,1+K*K)
        w=(s-r)/(sp-r)
        assert 0<w<1
        t=w/(1+a*a)+(1-w)*r
        assert w*sp+(1-w)*r==s
        gap=t-s/(a*a)
        assert gap>0
        gaps.append(gap)
    assert all(x>y for x,y in zip(gaps,gaps[1:]))
    limits.append(dict(a=a,s=s,gaps=gaps))

adapter_panels=0
max_roundoff=0.
for a in alphas:
    e=float(a-1/a)
    for j in range(1,1001):
        s=j/1000
        l,u=low(s,e),high(s,e)
        pl,pu=unphi(phi(s)-e),unphi(phi(s)+e)
        al,au=max(0,s-3*math.sqrt(3)*e/8),min(1,s+3*math.sqrt(3)*e/8)
        err=max(pl-l,u-pu,al-l,u-au)
        max_roundoff=max(max_roundoff,err)
        assert err<1e-12,(a,s,l,u,pl,pu,al,au)
        adapter_panels+=1

examples=[dict(s=s,e=e,sharp=[low(s,e),high(s,e)],
               phi=[unphi(phi(s)-e),unphi(phi(s)+e)],
               additive=[max(0,s-3*math.sqrt(3)*e/8),min(1,s+3*math.sqrt(3)*e/8)])
          for s,e in ((.1,.5),(.9,.5),(1.,2.),(.5,1.),(.1,2.))]
result=dict(status='PASS',label='DEVELOPMENT exact finite panels; not independent confirmation',
            contributor='Codex (GPT-6)',started_utc=started,
            ended_utc=datetime.now(timezone.utc).isoformat(),runtime_ns=time.perf_counter_ns()-start,
            python=sys.version,platform=platform.platform(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            matrix_panels=matrix_panels,exact_one_sided_bounds=2*matrix_panels,
            scalar_equalities=scalar_equalities,limiting_examples=limits,
            adapter_panels=adapter_panels,maximum_adapter_roundoff=max_roundoff,examples=examples)
OUT.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:result[k] for k in ('status','runtime_ns','source_sha256','matrix_panels',
                  'exact_one_sided_bounds','scalar_equalities','adapter_panels','maximum_adapter_roundoff','examples')},indent=2))
