"""New norm-capped upper choice and rational lower decision; Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import time

out=Path(__file__).with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()

def two_upper(s,m,e):
    if m-s*s<1e-13:
        x=math.sqrt((1-s)/s)
        if e>=x:
            return 1.0
        if e*(x-e)<=1:
            return 1/(1+(x-e)**2)
        return (1+e*e)/(x*x)
    q=math.sqrt(s-m)
    b=1-2*s+m
    if e>=(1-s)/q:
        return 1.0
    def derivative(alpha):
        r=math.sqrt(max(0,1-2*alpha*(1-s)+alpha*alpha*b))
        return 2*(r+alpha*e*q)*((alpha*b-(1-s))/r+e*q)+2*alpha*q*q
    lo,hi=0.0,1/q
    for _ in range(70):
        mid=(lo+hi)/2
        if derivative(mid)<0:
            lo=mid
        else:
            hi=mid
    alpha=(lo+hi)/2
    r=math.sqrt(max(0,1-2*alpha*(1-s)+alpha*alpha*b))
    return (r+alpha*e*q)**2+alpha*alpha*q*q

checks=0
panels=0
examples=[]
for K in (.2,.5,1,2,3,4,10):
    l=1/(1+K*K)
    for mix in (0,.01,.1,.5,.9):
        s=l+mix*(1-l)
        mmax=max(s*s,(1+l)*s-l)
        for e in (.1,.5,1,3):
            a=(math.sqrt(e*e+4)+e)/2
            mopt=min(mmax,max(s*s,s/(1+a*a)))
            upper=two_upper(s,mopt,e)
            for j in range(101):
                m=s*s+(mmax-s*s)*j/100
                assert two_upper(s,m,e)<=upper+2e-11
                checks+=1
            # All one-receipt feasible moments must meet the exact norm constraint.
            assert (1-2*s+mopt)/(s-mopt)<=K*K+1e-9
            panels+=1
for K in (3,3.1,3.2,3.4,4):
    s,e=.1,1
    l=1/(1+K*K)
    a=(math.sqrt(5)+1)/2
    mmax=max(s*s,(1+l)*s-l)
    mopt=min(mmax,max(s*s,s/(1+a*a)))
    examples.append({'s':s,'K':K,'edit':e,'m_opt':mopt,
                     'capped_upper':two_upper(s,mopt,e),'uncapped_upper':a*a*s})

# Exact decision: no floating-point output is used for these assertions.
c_upper,d_lower=F(489,125),F(209,250)
assert c_upper*c_upper>=F(153,10)
assert d_lower*d_lower<=F(7,10)
assert F(4,5)**2+F(3,5)**2==1
b=1+(4*c_upper-3*d_lower)/5
assert b==F(907,250)
certificate=F(16,25)/(1+b*b)
assert certificate==F(40000,885149)
threshold=F(9,200)
assert min(certificate,F(9,170))>threshold
s,t=F(1,10),F(1,25)
m=s*s/(s+t)
q2=s*t/(s+t)
y2=m-s*s
oldnorm=((1-s)**2+y2)/q2
newnorm=((1-t)**2+(t/s)**2*y2)/q2
oldvalue=(1+y2/q2)/(1+oldnorm)
newvalue=(1+(t/s)**2*y2/q2)/(1+newnorm)
edit2=((s-t)**2+(1-t/s)**2*y2)/q2
assert oldvalue==s and newvalue==t<threshold
assert oldnorm==F(61,2)>16 and edit2==F(9,10)<=1
assert F(1,26)<threshold
exact={'lower':str(certificate),'lower_float':float(certificate),
       'threshold':str(threshold),'margin':str(certificate-threshold),
       'old_value_only_counterexample':{'old':str(s),'new':str(t),
             'old_norm_squared':str(oldnorm),'edit_squared':str(edit2)},
       'norm_only_counterexample_new':str(F(1,26)),
       'new_operator_applications_after_receipts':0}
result={'status':'PASS','contributor':'Codex (GPT-6)',
        'scope':'floating capped-upper selection screen plus EXACT rational threshold certificate',
        'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
        'upper_panels':panels,'moment_grid_comparisons':checks,'examples':examples,
        'exact_decision':exact,'complete_cost_or_cpu_gain':False,
        'elapsed_ns':time.perf_counter_ns()-clock,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
