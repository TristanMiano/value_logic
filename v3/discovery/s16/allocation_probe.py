"""Exact two-target feasible/tangent bounds; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform
import time
t0=time.perf_counter_ns()
e=F(1,10); E=e*e
def f(x): return 1/(1+x*x)
def point(t):
    a=e*(1-t*t)/(1+t*t); b=e*2*t/(1+t*t)
    x=1-a; y=1+b
    d1=x/(a*(1+x*x)**2); d2=y/(b*(1+y*y)**2)
    return a,b,d1,d2
lo=F(0); hi=F(1)
for _ in range(35):
    mid=(lo+hi)/2
    _,_,d1,d2=point(mid)
    if d1<d2: lo=mid
    else: hi=mid
t=(lo+hi)/2
a,b,d1,d2=point(t)
assert a*a+b*b==E
lower=f(1-a)-f(1+b)
upper=lower+max(d1,d2)*E-d1*a*a-d2*b*b
assert upper>=lower and upper-lower<F(1,10**10)
separate=F(4000,40001)
gain=1-upper/separate
assert gain>F(29,100)

# Symbolic-sign reductions at rational points, including the sharp scale boundary.
concavity_checks=0
for alpha in [F(1,10),F(1,2),F(1),F(2)]:
    for j in range(1,100):
        x=alpha*F(j,100)
        assert alpha*(3*x*x-1)-4*x*x*x<=0
        z=alpha+F(j,10)
        assert 4*z*z*z-3*alpha*z*z+alpha>0
        concavity_checks+=2
assert F(21,10)*(3-1)-4>0 # alpha>2 loses global positive-branch concavity.
result={'status':'PASS','e':str(e),'rational_parameter':str(t),
        'a':str(a),'b':str(b),'a_float':float(a),'b_float':float(b),
        'lower':str(lower),'upper':str(upper),
        'lower_float':float(lower),'upper_float':float(upper),
        'certified_reduction':str(gain),'reduction_float':float(gain),
        'concavity_grid_checks':concavity_checks,
        'elapsed_ns':time.perf_counter_ns()-t0,'python':platform.python_version(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Exact rational feasible and tangent certificates, conditional on the concavity derivation; no empirical cost claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
