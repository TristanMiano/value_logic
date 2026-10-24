"""Exact rational partial-moment threshold checks; DEVELOPMENT, no overwrite."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'threshold_probe.json'
assert not OUT.exists(), 'Preserve original output; replay in an isolated directory.'
started=perf_counter_ns()


def upper_remainder(s,m,E,u,mu):
    assert 0<s<1 and s*s<=m<=s and E>=0 and 0<u<1 and mu>1-u
    a=1-s; q=s-m; B=m-s*s
    return (u*a*a-(1-u)*(q+B)-mu*E*q
            -u*u*a*a/(mu+u)-(1-u)**2*B/(mu-1+u))


def lower_interval(s,E,ell,l,h):
    assert 0<s<1 and 0<ell<=1 and s*s<=l<=h<=s and E>=0
    K=s*s-ell*(s+E*h)
    if E==0:
        return dict(valid=ell<=s,strict=ell<s,K=str(K),min_squared=str(K*K))
    vertex=(s*s+ell*s)/(ell*(E+4))
    x=max(l,min(vertex,h))
    P=(ell*ell*E*(E+4)*x*x-2*ell*E*(s*s+ell*s)*x+(s*s-ell*s)**2)
    # Check the independent unsimplified expression at the same minimizer.
    assert P==(s*s-ell*(s+E*x))**2-4*ell*ell*E*x*(s-x)
    return dict(valid=K>=0 and P>=0,strict=K>=0 and P>0,K=str(K),
                vertex=str(vertex),minimizer=str(x),min_squared=str(P))


s=F(1,2);E=F(1,100);l=F(41,100);h=s;u=F(539,1000);mu=F(11)
remainders=[upper_remainder(s,m,E,u,mu) for m in (l,h)]
assert min(remainders)>0
lower=lower_interval(s,E,F(288,625),l,h)
assert lower['strict']
# A rejected threshold is not called mathematically impossible: this
# certificate check can fail even where a different witness would work.
rejected=[upper_remainder(s,m,E,F(53,100),mu) for m in (l,h)]
assert min(rejected)<0
assert lower_interval(s,F(0),s,l,h)['valid']
assert not lower_interval(s,F(0),s,l,h)['strict']

# Compare interval widths with the sharp one-scalar receipt envelope.
# sqrt(4.01)>2.0024 implies old_lower<.45244.
root_lower=F(2503,1250)
assert root_lower*root_lower<F(401,100)
old_lower_upper=F(201,400)-root_lower/40
assert old_lower_upper==F(11311,25000)
old_width_lower=F(100,181)-old_lower_upper
new_width=u-F(288,625)
reduction_lower=1-new_width/old_width_lower
assert reduction_lower>F(218,1000)

result=dict(status='PASS',contributor='Codex (GPT-6)',classification='DEVELOPMENT',
    python=platform.python_version(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    receipts=dict(s=str(s),edit_squared=str(E),moment_interval=[str(l),str(h)]),
    upper=dict(threshold=str(u),witness=str(mu),endpoint_remainders=list(map(str,remainders))),
    lower=dict(threshold='288/625',**lower),new_width=str(new_width),
    old_width_strict_lower=str(old_width_lower),width_reduction_strict_lower=str(reduction_lower),
    elapsed_ns=perf_counter_ns()-started,
    limits='The >21.8% narrower certified band uses richer paid receipts; no fee or CPU saving, ordinary identical checker ties.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','source_sha256','width_reduction_strict_lower','elapsed_ns')}))
