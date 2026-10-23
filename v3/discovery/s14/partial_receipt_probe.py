"""Rational partial-receipt decision certificate; DEVELOPMENT, Codex (GPT-6)."""
from datetime import datetime, timezone
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import hashlib
import json
import platform
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'partial_receipt_probe.json'
assert not OUT.exists()
started=datetime.now(timezone.utc).isoformat()
start=time.perf_counter_ns()
sqrt_calls=0

def sqrt_bounds(x,scale=10**12):
    global sqrt_calls
    assert x>=0
    sqrt_calls+=1
    z=isqrt(x.numerator*scale*scale//x.denominator)
    low=F(z,scale)
    high=low if low*low==x else F(z+1,scale)
    assert low*low<=x<=high*high
    return low,high

def receipt_band(l,u,A,B,e,alpha):
    assert 0<l<=u<1 and 0<=A<=B and e>=0 and alpha>=0
    rlo=max(l,A/u)
    rhi=min(F(1),B/l)
    assert rlo<=rhi
    rp=min(max(F(1,2),rlo),rhi)
    _,root=sqrt_bounds(rp*(1-rp))
    Cbox=1+2*e*root+e*e*rhi
    _,aroot=sqrt_bounds(e*e+4)
    Cglobal=1+e*e/2+e*aroot/2
    lower=max(l/min(Cbox,Cglobal),l/Cglobal)
    coefficient=2*alpha*(1-alpha)
    Abar=(1-alpha)**2+coefficient*(u if coefficient>=0 else l)+alpha*alpha*B
    Qbar=u-A
    _,ra=sqrt_bounds(Abar)
    _,rq=sqrt_bounds(Qbar)
    upper=min(F(1),Cglobal*u,(ra+alpha*e*rq)**2+alpha*alpha*Qbar)
    return lower,upper,dict(r_interval=[rlo,rhi],Cbox=Cbox,Cglobal=Cglobal,
                            Abar=Abar,Qbar=Qbar,alpha=alpha,one_scalar_band=[l/Cglobal,min(F(1),u*Cglobal)])

l,u=F(999,10000),F(1001,10000)
A,B=F(999,100000),F(1001,100000)
e,alpha,threshold=F(1),F(10,9),F(6,25)
lower,upper,certificate=receipt_band(l,u,A,B,e,alpha)
assert lower<upper<threshold
assert certificate['one_scalar_band'][1]>threshold

def moments(column):
    den=1+sum(x*x for x in column)
    w=[1-column[0]*column[0]/den,-column[0]*column[1]/den]
    return w[0],sum(x*x for x in w)

panels=0
for x in (F(5999,2000),F(3),F(6001,2000)):
    for y in (F(-1,200),F(0),F(1,200)):
        M=[x,y]
        s,m=moments(M)
        assert l<=s<=u and A<=m<=B
        for length in (F(0),F(1,10),F(1,2),F(1)):
            for direction in ((F(1),F(0)),(F(-1),F(0)),(F(3,5),F(4,5)),(F(-3,5),F(4,5))):
                assert sum(z*z for z in direction)==1
                N=[M[i]+length*direction[i] for i in range(2)]
                new,_=moments(N)
                assert lower<=new<=upper
                panels+=1

# One-scalar insufficiency witness, using the exact finite-extremizer theorem.
old,new=F(1,10),F(32,125)
distance=F(39,40)
assert distance*distance==(new-old)**2/(old*new)
assert old+new<1 and distance<e and new>threshold
omitted_moment=old*old/(old+new)
assert omitted_moment>B

result=dict(status='PASS',label='DEVELOPMENT rational certificate and finite panels',
            contributor='Codex (GPT-6)',started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            python=sys.version,platform=platform.platform(),value_interval=[l,u],moment_interval=[A,B],
            edit_norm_bound=e,threshold=threshold,certified_band=[lower,upper],
            displayed_band=[float(lower),float(upper)],certificate=certificate,
            outward_sqrt_calls=sqrt_calls,new_matrix_operator_applications=0,exact_matrix_panels=panels,
            one_scalar_counterexample=dict(old=old,new=new,distance=distance,second_moment=omitted_moment))
OUT.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('certificate','certified_band')},indent=2,default=str))
