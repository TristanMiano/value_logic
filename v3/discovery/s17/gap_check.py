"""Exact quantitative two-edit information gap; Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'gap_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
prior=json.loads((HERE/'pair_radius_result.json').read_text())
r=next(x for x in prior['radii'] if x['radius']=='1')
start=perf_counter_ns()
al,ah=map(F,r['a_interval'])
ql,qh=map(F,r['q_interval'])
gl,gh=map(F,r['coefficient_interval'])
kl,kh=1+al-qh,1+ah-ql
ll,lh=ql+al-1,qh+ah-1
Klo=gl*kl*ll/((ah-1+kh)*(ah+1+lh))
assert Klo>F(3,20)
K=F(3,20)
lo,hi=F(28714,100000),F(28715,100000)
assert lo<1/(1+qh)<1/(1+ql)<hi
rows=[]
for name,diag,weights in [
    ('equal_moments_A',[F(1,10),F(3,10)],[F(1,2),F(1,2)]),
    ('equal_moments_B',[F(14,75),F(19,20)],[F(225,229),F(4,229)]),
    ('uniform_target_strict',[F(1,10),F(2,5)],[F(1,2),F(1,2)])]:
    sv=sum(w*x for w,x in zip(weights,diag))
    m=sum(w*x*x for w,x in zip(weights,diag))
    b0=sum(w*x/(1-x) for w,x in zip(weights,diag))
    eta=(1-hi)*b0-sv
    Fmin=(1-hi)*eta
    dmax=max(sum(w*((2*z-1-x)/(1-x))**2 for w,x in zip(weights,diag)) for z in (lo,hi))
    gap=K*Fmin**2/dmax if eta>0 else F(0)
    momentgap=K*max(F(0),m-hi*sv)**2/sv
    if name=='equal_moments_A':
        assert (1-lo)*b0<sv and sv==F(1,5) and m==F(1,20)
    else:
        assert gap>0
    if name=='equal_moments_B':
        assert sv==F(1,5) and m==F(1,20) and b0==F(34,61) and momentgap==0
    rows.append(dict(case=name,diagonal=list(map(str,diag)),weights=list(map(str,weights)),
                     old_value=str(sv),second_block_moment=str(m),inverse_statistic=str(b0),
                     gap_at_least=str(gap),gap_decimal=float(gap),
                     simpler_moment_gap=str(momentgap),
                     absolute_upper=str(gh*sv-gap)))
record=dict(status='PASS',K_lower_bound=str(K),contact_interval=[str(lo),str(hi)],cases=rows,
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            dependency_sha256=hashlib.sha256((HERE/'pair_radius_result.json').read_bytes()).hexdigest(),
            scope='Exact arithmetic instantiation of pair_gap.md, conditional on its analytic inequality; no SDP approximation.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',gaps=[r['gap_decimal'] for r in rows],elapsed_ns=record['elapsed_ns'])))
