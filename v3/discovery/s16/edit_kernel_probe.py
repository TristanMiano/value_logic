"""Exact DEVELOPMENT screen for joint structured-edit receipts; no speed claim."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import hashlib
import json
import platform
import random
import time

t0=time.perf_counter_ns()
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def tr(A): return list(map(list,zip(*A)))
def add(A,B): return [[a+b for a,b in zip(x,y)] for x,y in zip(A,B)]
def neg(A): return [[-x for x in row] for row in A]
def sub(A,B): return add(A,neg(B))
def mul(A,B): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def hcat(A,B): return [x+y for x,y in zip(A,B)]
def invdet(A):
    n=len(A); R=hcat([row[:] for row in A],eye(n)); det=F(1)
    for j in range(n):
        pivot=next(i for i in range(j,n) if R[i][j])
        if pivot!=j: R[pivot],R[j]=R[j],R[pivot]; det=-det
        v=R[j][j]; det*=v; R[j]=[x/v for x in R[j]]
        for i in range(n):
            if i!=j:
                v=R[i][j]; R[i]=[x-v*y for x,y in zip(R[i],R[j])]
    return [row[n:] for row in R],det
def quad(x,A): return mul(tr(x),mul(A,x))[0][0]
def gram(A): return mul(A,tr(A))

rng=random.Random(1644)
def mat(n,m): return [[F(rng.randrange(-3,4),rng.choice([1,2,3])) for _ in range(m)] for _ in range(n)]
cases=0
for n,m,r,s in [(2,2,1,1),(3,2,2,1),(2,3,1,2),(3,3,2,2)]:
    for variant in range(6):
        M=mat(n,m); P=mat(n,r)
        if variant==0: P=[[F(0)]*r for _ in range(n)] # Singular G is allowed.
        Q=[row[:s] for row in eye(m)]
        W=[row[:min(2,n)] for row in eye(n)]; y=mat(m,1)
        S,detold=invdet(add(eye(n),gram(M)))
        mu=mul(S,mul(M,y)); r0=quad(y,eye(m))-mul(tr(mul(M,y)),mu)[0][0]
        U=hcat(P,mul(M,Q)); G=mul(tr(U),mul(S,U)); B=mul(tr(U),mul(S,W))
        C=mul(tr(W),mul(S,W)); g=mul(tr(U),mu); h=mul(tr(W),mu); q=mul(tr(Q),y)
        GP=[row[:r] for row in G]; GPP=[row[:r] for row in G[:r]]
        for scale in [F(0),F(1,10),F(1),F(3)]:
            A=[[scale*x for x in row] for row in mat(r,s)]
            K=hcat(gram(A),A)+hcat(tr(A),[[F(0)]*s for _ in range(s)])
            inverse,det_ratio=invdet(add(eye(r+s),mul(K,G))); D=mul(inverse,K)
            assert D==tr(D) and det_ratio>0
            a=mul(A,q); t=add(g,mul(GP,a))
            Cnew=sub(C,mul(tr(B),mul(D,B)))
            hnew=sub(add(h,mul(tr(B[:r]),a)),mul(tr(B),mul(D,t)))
            rnew=r0-2*mul(tr(a),g[:r])[0][0]-quad(a,GPP)+quad(t,D)
            N=add(M,mul(P,mul(A,tr(Q))))
            SN,detnew=invdet(add(eye(n),gram(N)))
            muN=mul(SN,mul(N,y))
            assert Cnew==mul(tr(W),mul(SN,W))
            assert hnew==mul(tr(W),muN)
            assert rnew==quad(y,eye(m))-mul(tr(mul(N,y)),muN)[0][0]
            assert det_ratio==detnew/detold
            cases+=1

# Fixed-catalogue all-zero paths from pass43, exact crossing counts.
crossings={}
for N,S0,name in [(1000,90,'with_aggregate_proof'),(2000,100,'uniform_full_catalogue')]:
    wealth=F(1)
    for t in range(1,N-S0+2):
        wealth*=F(N-t+1,N-S0-t+1)
        if wealth>=20:
            crossings[name]={'queries':t,'wealth':str(wealth),'wealth_float':float(wealth)}
            break
assert crossings['with_aggregate_proof']['queries']==32
result={'status':'PASS','exact_edit_cases':cases,'catalogue_zero_paths':crossings,
        'elapsed_ns':time.perf_counter_ns()-t0,'python':platform.python_version(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Finite exact algebra screen, not independent proof or empirical resource advantage.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
