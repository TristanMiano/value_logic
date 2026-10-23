"""Finite numerical development screen; no formal numerical certification."""
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from time import perf_counter_ns

start=perf_counter_ns()
def h(x):
    assert -1e-14<=x<=1+1e-14
    x=max(0,min(1,x))
    return -(x*math.log(x) if x else 0)-((1-x)*math.log1p(-x) if x<1 else 0)
def information(pi,q,b):
    if q==0:
        return 0.
    r=(pi-q*b)/(1-q)
    return h(pi)-q*h(b)-(1-q)*h(r)
def frontier(pi,epsilon,kappa):
    lo=0.
    hi=(1-pi)/(1-epsilon)
    if information(pi,hi,epsilon)<=kappa:
        return hi
    for _ in range(70):
        mid=(lo+hi)/2
        if information(pi,mid,epsilon)<=kappa:
            lo=mid
        else:
            hi=mid
    return (lo+hi)/2

cases=0
smallest_slack=0.
for pi in (.1,.25,.5,.75,.9):
    for epsilon in (0,.01,.05,.2,.4):
        if epsilon>=pi:
            continue
        qmax=(1-pi)/(1-epsilon)
        for i in range(1,31):
            q=qmax*i/30
            bound=information(pi,q,epsilon)
            for j in range(31):
                b=epsilon*j/30
                r=(pi-q*b)/(1-q)
                if r>1+1e-14:
                    continue
                slack=information(pi,q,b)-bound
                smallest_slack=min(smallest_slack,slack)
                assert slack>=-1e-12
                cases+=1

left=.8*math.log(9)
right=2*(math.log(2)-h(.1))
assert left>right
examples=[dict(base_error=pi,target_error=eps,information_ceiling=k,
               maximum_coverage=frontier(pi,eps,k))
          for pi,eps in ((.1,.01),(.5,0),(.5,.05)) for k in (.01,.05,.1)]
result=dict(status='PASS',model='Codex (GPT-6)',python=platform.python_version(),
    source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
    feasible_joint_laws=cases,minimum_numerical_slack=smallest_slack,
    source_counterexample=dict(pairwise_KL=left,twice_mutual_information=right),
    examples=examples,elapsed_ns=perf_counter_ns()-start,
    scope='Floating-point finite joint-law screen and illustrative roots; analytic proof is separate, no measured workload benefit.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
