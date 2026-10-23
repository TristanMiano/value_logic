"""Revised exact small four-receipt design certificate, DEVELOPMENT, Codex (GPT-6)."""
from datetime import datetime, timezone
from fractions import Fraction as F
from math import comb, sqrt
from pathlib import Path
import hashlib
import json
import platform
import random
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'receipt_design_probe_v2.json'
assert not OUT.exists()
started=datetime.now(timezone.utc).isoformat()
start=time.perf_counter_ns()

def mul(p,q):
    a=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):a[i+j]+=x*y
    return a

def roots(xs):
    p=[F(1)]
    for x in xs:p=mul(p,[-x,F(1)])
    return p

def at(p,t):
    a=F(0)
    for x in p[::-1]:a=a*t+x
    return a

def bernstein(p,a,b):
    n=len(p)-1
    shifted=[sum(p[i]*comb(i,k)*a**(i-k)*(b-a)**k for i in range(k,n+1)) for k in range(n+1)]
    return [sum(shifted[k]*F(comb(j,k),comb(n,k)) for k in range(j+1)) for j in range(n+1)]

nodes=[F(8,7),F(5,2),F(32,5),F(14)]
delta=F(117,6475)
Lambda=F(12,5)
eps=F(1,1000)
width=(1+delta)*delta+2*eps*Lambda
den=roots([-x for x in nodes])
num=roots(nodes)
card=[]
for i,x in enumerate(nodes):
    p=roots(nodes[:i]+nodes[i+1:])
    card.append([at(den,x)/at(p,x)*a for a in p])

A,B=F(106,7),F(89,10)
S,P=A+B,A*B
positive=[(delta-1)*P,(delta+1)*S,delta-1]
negative=[(delta+1)*P,(delta-1)*S,delta+1]
assert positive[-1]<0 and at(positive,F(8))>=0 and at(positive,F(17))==0
discriminant=negative[1]**2-4*negative[0]*negative[2]
assert negative[-1]>0 and discriminant<0

certificate=[]
breaks=[F(1)]+nodes+[F(16)]
for left,right in zip(breaks,breaks[1:]):
    signs=[1 if at(p,(left+right)/2)>0 else -1 for p in card]
    p=[Lambda*x for x in den]
    for sg,q in zip(signs,card):
        for j,x in enumerate(q):p[j]-=sg*x
    stack=[(left,right,0)]
    while stack:
        a,b,depth=stack.pop()
        bs=bernstein(p,a,b)
        if min(bs)>=0:
            certificate.append(dict(left=a,right=b,signs=signs,polynomial=p,bernstein=bs))
        else:
            assert depth<12,('failed declared coefficient bound',a,b,bs)
            mid=(a+b)/2
            stack.extend(((mid,b,depth+1),(a,mid,depth+1)))
certificate.sort(key=lambda row:row['left'])
assert certificate[0]['left']==1 and certificate[-1]['right']==16
assert all(a['right']==b['left'] for a,b in zip(certificate,certificate[1:]))

def weights(t):return [at(p,t)/at(den,t) for p in card]
def product(xs):
    a=F(1)
    for x in xs:a*=x
    return a
def response(t,law):return sum(w/(1+t*l) for w,l in law)
def band(t,intervals):
    w=weights(t)
    lo=sum(x*(a if x>=0 else b) for x,(a,b) in zip(w,intervals))
    hi=sum(x*(b if x>=0 else a) for x,(a,b) in zip(w,intervals))
    beta=at(num,t)/at(den,t)
    return max(F(0),lo+min(-delta*beta,beta)),min(F(1),hi+max(-delta*beta,beta))

points=sorted(set([F(1)+F(15*j,120) for j in range(121)]+nodes))
identities=0
max_lebesgue=F(0)
for t in points:
    w=weights(t)
    max_lebesgue=max(max_lebesgue,sum(map(abs,w)))
    assert sum(map(abs,w))<=Lambda
    assert abs(at(num,t)/at(den,t))<=delta
    for l in (F(0),F(1,100),F(1,16),F(1,4),F(1),F(7),F(100)):
        actual=1/(1+l*t)-sum(a/(1+l*x) for a,x in zip(w,nodes))
        expected=at(num,t)/at(den,t)/(1+l*t)*product((1-l*x)/(1+l*x) for x in nodes)
        assert actual==expected
        identities+=1
rng=random.Random(2026102216)
panels=0
max_width=F(0)
for _ in range(20):
    masses=[rng.randrange(1,11) for _ in range(4)]
    law=[(F(w,sum(masses)),F(rng.randrange(0,40),rng.randrange(1,20))) for w in masses]
    intervals=[(max(F(0),response(t,law)-eps),min(F(1),response(t,law)+eps)) for t in nodes]
    for t in points:
        lo,hi=band(t,intervals)
        assert lo<=response(t,law)<=hi
        assert hi-lo<=width
        max_width=max(max_width,hi-lo)
        panels+=1

sopt=10*34**.25
aopt=(sopt+sqrt(sopt*sopt-544))/2
bopt=(sopt-sqrt(sopt*sopt-544))/2
design=dict(sum=sopt,product=136,delta=(25-sopt)/(25+sopt),
            nodes=sorted([(u-sqrt(u*u-64))/2 for u in (aopt,bopt)]+
                         [(u+sqrt(u*u-64))/2 for u in (aopt,bopt)]))
result=dict(status='PASS',label='DEVELOPMENT exact interval certificate and finite spectral screens',
            contributor='Codex (GPT-6)',started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,python=sys.version,platform=platform.platform(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            nodes=nodes,residual_bound=delta,coefficient_bound=Lambda,receipt_radius=eps,
            uniform_width=width,previous_width=F(461,10000),
            relative_width_reduction=1-width/F(461,10000),
            residual_positive_polynomial=positive,residual_negative_polynomial=negative,
            negative_discriminant=discriminant,bernstein_certificate=certificate,
            identities=identities,spectral_panels=panels,maximum_screened_width=max_width,
            maximum_screened_lebesgue=max_lebesgue,symmetric_analytic_design=design)
OUT.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='bernstein_certificate'},indent=2,default=str))
print('Certified coefficient intervals:',len(certificate))
