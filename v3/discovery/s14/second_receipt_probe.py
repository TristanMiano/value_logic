"""Small DEVELOPMENT screen of the two-scalar lower envelope; Codex (GPT-6)."""
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
OUT=HERE/'second_receipt_probe.json'
assert not OUT.exists()
started=datetime.now(timezone.utc).isoformat()
start=time.perf_counter_ns()
rng=random.Random(2026102217)

def inv(A):
    n=len(A)
    B=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next(k for k in range(j,n) if B[k][j])
        B[j],B[k]=B[k],B[j]
        q=B[j][j]
        B[j]=[x/q for x in B[j]]
        for i in range(n):
            if i!=j:
                q=B[i][j]
                B[i]=[x-q*y for x,y in zip(B[i],B[j])]
    return [r[n:] for r in B]

def moments(M,v):
    n=len(M)
    A=[[F(i==j)+sum(a*b for a,b in zip(M[i],M[j])) for j in range(n)] for i in range(n)]
    R=inv(A)
    w=[sum(row[j]*v[j] for j in range(n)) for row in R]
    assert all(sum(A[i][j]*w[j] for j in range(n))==v[i] for i in range(n))
    s=sum(x*y for x,y in zip(v,w))
    m=sum(x*x for x in w)
    assert s*s<=m<=s
    return s,m

def unit(n):
    if n==1:return [F(1)]
    u=[F(0)]*n
    j,k=rng.sample(range(n),2)
    u[j],u[k]=F(3,5),F(4,5)
    return u

panels=0
for n,k in ((1,1),(2,1),(2,2),(2,3),(3,2)):
    for case in range(12):
        M=[[F(rng.randrange(-8,9),rng.choice((1,2,3))) for _ in range(k)] for _ in range(n)]
        v,u,z=unit(n),unit(n),unit(k)
        s,m=moments(M,v)
        for e in (F(0),F(1,10),F(1),F(3)):
            N=[[M[i][j]+e*u[i]*z[j] for j in range(k)] for i in range(n)]
            t,_=moments(N,v)
            lower_residual=s*s/t-s-e*e*m
            upper_residual=t-s-e*e*(s-m)
            radicand=4*e*e*m*(s-m)
            assert lower_residual<=0 or lower_residual**2<=radicand
            assert upper_residual<=0 or upper_residual**2<=radicand
            panels+=1

equalities=0
for x in (F(0),F(1,4),F(1),F(3),F(10)):
    s=1/(1+x*x)
    m=s*s
    for e in (F(0),F(1,10),F(1),F(3)):
        t=1/(1+(x+e)**2)
        assert t==s*s/(s+2*e*x*s*s+e*e*m)
        equalities+=1

limits=[]
for s,m,e in ((F(1,10),F(1,50),F(1,2)),(F(1,4),F(1,8),F(1)),(F(1,2),F(3,8),F(2))):
    r=m/s
    bound=float(s)/(1+2*float(e)*math.sqrt(float(r*(1-r)))+float(e*e*r))
    gaps=[]
    rows=[]
    for K in (10,100,1000,10000):
        q=F(1,1+K*K)
        x=(m-s*q)/(s-q)
        p=(s-q)/(x-q)
        assert 0<q<x<1 and 0<p<1
        assert p*x+(1-p)*q==s
        assert p*x*x+(1-p)*q*q==m
        t=float(p)/(1+(math.sqrt(float((1-x)/x))+float(e))**2)+float((1-p)*q)
        gap=t-bound
        assert gap>0
        gaps.append(gap)
        rows.append(dict(K=K,old_response=s,old_second_moment=m,low_spectral_response=q,
                         high_spectral_response=x,weight=p,new_response_float=t,gap_float=gap))
    assert all(a>b for a,b in zip(gaps,gaps[1:]))
    limits.append(dict(s=s,m=m,e=e,lower_bound_float=bound,rows=rows))

result=dict(status='PASS',label='DEVELOPMENT finite screen, not independent confirmation',
            contributor='Codex (GPT-6)',started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,python=sys.version,platform=platform.platform(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            exact_matrix_panels=panels,exact_inequalities=2*panels,scalar_equalities=equalities,
            exact_moment_constructions=12,limiting_sequences=limits)
OUT.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='limiting_sequences'},indent=2))
