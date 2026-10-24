"""Exact rounded-scalar decision under a source-norm warrant; DEVELOPMENT.

Codex (GPT-6). This screens the separate formulas, not the unchanged s16 checker.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'bounded_decision_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start=perf_counter_ns()
E=F(1); K2=F(9); beta=1/(1+K2)
s=F(21,200); eps=F(1,1000)
lo,hi=s-eps,s+eps
tl,tu=F(1,3),F(13,10)
def constants(t):
    return 1+t,t-E-E/t
a,d=constants(tl)
assert d<0 and a-d>0 and a-beta*d>0
lower=(a*lo-beta*d)/((a-d)*(a-beta*d))
a,d=constants(tu)
assert E<tu and -1<d<0 and 1+beta*d>0
upper=a*(hi+beta*d)/((1+d)*(1+beta*d))
assert beta<lo<hi<1
assert F(1,20)<lower<upper<F(27,100)
root_low,root_high=F(559,250),F(2237,1000)
assert root_low**2<5<root_high**2
h_low,h_high=(1+root_low)/2,(1+root_high)/2
m0=(F(1,10)**2+F(11,100)**2)/2
assert m0<s*(1+h_low)/(2+h_low)
assert m0<s/(2+h_high)
core_lower_upper=s/(1+h_low)
core_upper_lower=s*(1+h_low)
assert core_lower_upper<F(1,20) and core_upper_lower>F(27,100)
record=dict(status='PASS',C_diagonal=['1/10','11/100'],E=str(E),K_squared=str(K2),
            beta=str(beta),exact_target_value=str(s),scalar_interval=[str(lo),str(hi)],
            lower_t=str(tl),upper_t=str(tu),lower=str(lower),upper=str(upper),
            thresholds=['1/20','27/100'],
            core_lower_upper_enclosure=str(core_lower_upper),
            core_upper_lower_enclosure=str(core_upper_lower),
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='One exact conditional scalar-plus-norm decision, compared with sharp C-only caps; no acquisition price or empirical speedup.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status=record['status'],lower=str(lower),upper=str(upper),
                     decimals=[float(lower),float(upper)],elapsed_ns=record['elapsed_ns'])))
