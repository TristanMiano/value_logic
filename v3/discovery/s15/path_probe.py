"""Exact rational comparison of rank-one value profiles and interpolation."""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import platform
from random import Random
from time import perf_counter_ns

start=perf_counter_ns()
rng=Random(20261023)
def dot(x,y):
    return sum((a*b for a,b in zip(x,y)),F(0))
def mv(A,x):
    return [dot(row,x) for row in A]
def solve(A,b):
    cols=len(A[0])
    rows=[[F(x) for x in a]+[F(y)] for a,y in zip(A,b)]
    pivot=[]
    at=0
    for j in range(cols):
        hit=next((i for i in range(at,len(rows)) if rows[i][j]),None)
        if hit is None:
            continue
        rows[at],rows[hit]=rows[hit],rows[at]
        v=rows[at][j]
        rows[at]=[x/v for x in rows[at]]
        for i in range(len(rows)):
            if i!=at:
                v=rows[i][j]
                rows[i]=[x-v*y for x,y in zip(rows[i],rows[at])]
        pivot.append(j)
        at+=1
    assert not any(not any(row[:cols]) and row[-1] for row in rows)
    x=[F(0)]*cols
    for i,j in enumerate(pivot):
        x[j]=rows[i][-1]
    return x,len(pivot)
def gram(M):
    return [[dot(a,b)+int(i==j) for j,b in enumerate(M)] for i,a in enumerate(M)]

checks=0
interpolation_checks=0
ranks={}
removable=0
for n in range(1,4):
    for m in range(1,4):
        for _ in range(5):
            M=[[F(rng.randrange(-2,3)) for j in range(m)] for i in range(n)]
            u=[F(rng.randrange(-2,3)) for i in range(n)]
            z=[F(rng.randrange(-2,3)) for j in range(m)]
            v=[F(int(i==0)) for i in range(n)]
            Q=gram(M)
            w=mv(M,z)
            iv,_=solve(Q,v)
            iu,_=solve(Q,u)
            iw,_=solve(Q,w)
            s=dot(v,iv)
            a,b,c,d,e,gamma=dot(u,iu),dot(u,iw),dot(w,iw),dot(u,iv),dot(w,iv),dot(z,z)
            def direct(t):
                N=[[M[i][j]+t*u[i]*z[j] for j in range(m)] for i in range(n)]
                x,_=solve(gram(N),v)
                return dot(v,x)
            for t in map(F,(-3,-2,-1,0,1,2,3)):
                D=1+2*b*t+(b*b+a*(gamma-c))*t*t
                R=2*d*e*t+((gamma-c)*d*d+2*b*d*e-a*e*e)*t*t
                assert D>0
                assert s-R/D==direct(t)
                checks+=1
            rows=[]
            rhs=[]
            for t in map(F,(-2,-1,1,2)):
                f=direct(t)
                rows.append([t,t*t,-t*f,-t*t*f])
                rhs.append(f-s)
            coeff,rank=solve(rows,rhs)
            ranks[str(rank)]=ranks.get(str(rank),0)+1
            for t in (F(-5,2),F(-1,2),F(0),F(1,2),F(5,2)):
                numerator=s+coeff[0]*t+coeff[1]*t*t
                denominator=1+coeff[2]*t+coeff[3]*t*t
                assert direct(t)*denominator==numerator
                removable+=denominator==0
                interpolation_checks+=1
result=dict(status='PASS',model='Codex (GPT-6)',python=platform.python_version(),
    source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
    matrix_cases=45,exact_profile_checks=checks,exact_interpolation_checks=interpolation_checks,
    interpolation_system_ranks=ranks,removable_zero_denominators=removable,
    elapsed_ns=perf_counter_ns()-start,
    scope='Exact rational finite development cases, including degenerate interpolation; not an independent proof or cost benchmark.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
