"""Exact small-law rank-stopping screen; Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from math import comb,log
import hashlib
import json
import time

out=Path(__file__).with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()

def extend(span,z):
    return span|sum(1<<(x^z) for x in range(4) if span>>x&1)

def rank(span):
    return span.bit_count().bit_length()-1

def binomial_tail(n,k,e):
    return sum(F(comb(n,j))*e**j*(1-e)**(n-j) for j in range(k+1))

laws=[tuple(F(a,4) for a in counts) for counts in
      ((a,b,c,4-a-b-c) for a in range(5) for b in range(5-a) for c in range(5-a-b))]
laws += [(F(9,10),F(1,10),F(0),F(0)),(F(8,10),F(1,10),F(1,10),F(0))]
epsilons=(F(1,10),F(1,4),F(1,2),F(3,4))
deltas=(F(1,2),F(1,4),F(1,10))
joint_checks=sequential_checks=0
positive_crossings=0
max_failure_ratio=F(0)
for law in laws:
    miss={span:sum(p for z,p in enumerate(law) if not(span>>z&1)) for span in (1,3,5,9,15)}
    distribution={1:F(1)}
    for n in range(1,31):
        next_distribution=defaultdict(F)
        for span,p in distribution.items():
            for z,q in enumerate(law):
                if q:
                    next_distribution[extend(span,z)]+=p*q
        distribution=next_distribution
        assert sum(distribution.values())==1
        for e in epsilons:
            for k in (0,1):
                actual=sum(p for span,p in distribution.items() if miss[span]>e and rank(span)<=k)
                assert actual<=binomial_tail(n,k,e)
                joint_checks+=1
    for e in epsilons:
        A=(1-e/2)/(1-e)
        for delta in deltas:
            distribution={(1,False):F(1)}
            for n in range(1,31):
                next_distribution=defaultdict(F)
                for (span,failed),p in distribution.items():
                    for z,q in enumerate(law):
                        if q:
                            s=extend(span,z)
                            j=rank(s)
                            m=A**(n-j)/2**j
                            fail=failed or (miss[s]>e and m>=1/delta)
                            next_distribution[(s,fail)]+=p*q
                distribution=next_distribution
                failure=sum(p for (span,failed),p in distribution.items() if failed)
                assert failure<=delta
                positive_crossings+=failure>0
                max_failure_ratio=max(max_failure_ratio,failure/delta)
                sequential_checks+=1

fixed=[]
n=200
delta=F(1,20)
denominator=1_000_000
for k in (0,1,20):
    target=delta/F((k+1)*(k+2))
    lo,hi=0,denominator
    while hi-lo>1:
        mid=(hi+lo)//2
        if binomial_tail(n,k,F(mid,denominator))>target:
            lo=mid
        else:
            hi=mid
    assert binomial_tail(n,k,F(lo,denominator))>target
    assert binomial_tail(n,k,F(hi,denominator))<=target
    old=2/(n-2*k)*(k*log(4)+log((k+1)*(k+2)/float(delta)))
    fixed.append({'n':n,'k_bar':k,'delta':delta,
                  'new_root_lower':F(lo,denominator),'new_root_upper':F(hi,denominator),
                  'new_upper_float':hi/denominator,'stable_compression_comparator_float':old,
                  'bound_reduction_percent_float':100*(1-hi/denominator/old)})
A=F(39,38)
assert A**199>=40
first=next(n for n in range(1,300) if A**(n-1)>=40)
result={'status':'PASS','contributor':'Codex (GPT-6)',
        'scope':'exact laws on F2^2, horizons1..30, fixed targets; no measured acquisition gain',
        'laws':len(laws),'joint_tail_checks':joint_checks,
        'sequential_unsafe_crossing_checks':sequential_checks,
        'positive_crossing_panels':positive_crossings,
        'max_unsafe_probability_over_delta':max_failure_ratio,
        'fixed_cohort_comparisons':fixed,
        'k_bar1_target_risk_005_delta_005_first_certified_N':first,
        'ordinary_equivalent':'same binomial coupling / rank certificate / Ville test ties',
        'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
        'elapsed_ns':time.perf_counter_ns()-clock,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2,default=str))
