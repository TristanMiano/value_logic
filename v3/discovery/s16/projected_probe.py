"""Exact finite DEVELOPMENT screen of projected receipts; refuses overwrite."""
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'projected_probe.json'
assert not OUT.exists(), 'Preserve the original evidence; replay in an isolated directory.'
start=perf_counter_ns()

def roots(x, scale=10**12):
    assert x>=0
    n=isqrt(x.numerator*scale*scale//x.denominator)
    lo=F(n,scale); hi=lo if lo*lo==x else F(n+1,scale)
    assert lo*lo<=x<=hi*hi
    return lo,hi

def value(M):
    # Unit target (1,1)/sqrt(2); its quadratic form is rational.
    a=1+sum(x*x for x in M[0])
    b=sum(x*y for x,y in zip(*M))
    d=1+sum(x*x for x in M[1])
    det=a*d-b*b
    assert det>0
    return (a+d-2*b)/(2*det)

M=[[F(3),F(0)],[F(0),F(1,3)]]
assert value(M)==F(1,2)
assert F(193,10)**2>369
lower=F(2500,5427);upper=F(1079,2000)
assert lower>F(23,50) and upper<F(27,50)
assert F(100,181)>F(27,50)
# These 625 perturbations have Frobenius norm <=1/10, hence op norm <=1/10.
values=[]
for hs in product(range(-2,3),repeat=4):
    H=[[F(hs[0],40),F(hs[1],40)],[F(hs[2],40),F(hs[3],40)]]
    assert sum(x*x for row in H for x in row)<=F(1,100)
    N=[[M[i][j]+H[i][j] for j in range(2)] for i in range(2)]
    v=value(N);assert lower<v<upper
    values.append(v)

# A fully rational matrix edit refutes the proposed spectral scalar bound.
delta=F(1,1000)
N=[[F(3)-delta,-delta],[-9*delta,F(1,3)-9*delta]]
e2=164*delta*delta
e_lo,e_hi=roots(e2)
_,r_hi=roots(e2+4)
assert e_hi<F(1,3) and e_hi<F(8,3)
scalar_upper_01=F(1,10)*(r_hi+e_hi)**2/4
scalar_upper_09=1/(1+(F(1,3)-e_hi)**2)
spectral_upper=(scalar_upper_01+scalar_upper_09)/2
actual=value(N)
assert actual>spectral_upper
assert F(369,2500)>F(8,25)**2

result=dict(status='PASS',contributor='Codex (GPT-6)',classification='DEVELOPMENT',
    python=platform.python_version(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    exact_perturbation_cases=len(values),certificate_lower=str(lower),certificate_upper=str(upper),
    observed_value_min=str(min(values)),observed_value_max=str(max(values)),
    single_receipt_adverse_value='100/181',
    spectral_counterexample=dict(delta=str(delta),edit_norm_squared=str(e2),
        edit_norm_interval=[str(e_lo),str(e_hi)],actual_response=str(actual),
        spectral_claim_outward_upper=str(spectral_upper),strict_gap=str(actual-spectral_upper)),
    elapsed_ns=perf_counter_ns()-start,
    scope='Finite exact checks and one exact counterexample; no independent confirmation, universal probe proof or runtime advantage.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
