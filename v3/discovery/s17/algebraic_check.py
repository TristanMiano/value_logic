"""Exact univariate degree/root screen; Codex (GPT-6), DEVELOPMENT."""
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
import sympy as s

HERE=Path(__file__).resolve().parent
OUT=HERE/'algebraic_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
start=perf_counter_ns()
t=s.symbols('t')
C=s.diag(s.Rational(1,10),s.Rational(9,10))
V=s.ones(2)/2
E=s.Rational(1,100)
h=(E+s.sqrt(E*E+4*E))/2
I=s.eye(2)
Dl=(I-C)*t*t+(I+E*C)*t+E*C
Du=C*t*t+(I-E*C)*t-E*C
rows=[]
for name,D,factor in [('lower',Dl,t),('upper',Du,t*(t+1))]:
    n=s.expand(factor*s.trace(V*C*D.adjugate()))
    d=s.expand(D.det())
    f=s.cancel(n/d)
    direct=s.trace(V*C*((1+t)*I-(t-E-E/t)*C).inv()) if name=='lower' else s.trace(V*(1+t)*C*(I+(t-E-E/t)*C).inv())
    assert s.cancel(f-direct)==0
    der=s.Poly(s.fraction(s.cancel(s.diff(f,t)))[0],t).clear_denoms()[1].primitive()[1]
    assert der.degree()==6 and der.is_irreducible
    intervals=s.polys.polytools.intervals(der,eps=s.Rational(1,10**12))
    admissible=[]
    for (a,b),mult in intervals:
        assert not (a<=h<=b)
        if a>h:
            admissible.append((a,b,mult))
    assert len(admissible)==1
    a,b,mult=admissible[0]
    mid=(a+b)/2
    sign_left=s.sign(der.eval(a)/s.denom(s.cancel(s.diff(f,t))).subs(t,a))
    sign_right=s.sign(der.eval(b)/s.denom(s.cancel(s.diff(f,t))).subs(t,b))
    assert (sign_left,sign_right)==((1,-1) if name=='lower' else (-1,1))
    tau=s.Rational(539,1000)
    strict_poly=s.Poly(s.expand(tau*d-n if name=='upper' else n-tau*d),t)
    assert strict_poly.degree()<=4
    if name=='upper':
        assert f.subs(t,mid)<tau and strict_poly.eval(mid)>0
    rows.append(dict(endpoint=name,derivative_coefficients=[str(x) for x in der.all_coeffs()],
                     derivative_degree=der.degree(),irreducible_over_rationals=True,
                     admissible_real_root_count=1,root_interval=[str(a),str(b)],
                     rational_parameter=str(mid),value=str(f.subs(t,mid)),
                     value_decimal=str(s.N(f.subs(t,mid),18)),
                     threshold_polynomial_degree=strict_poly.degree(),
                     threshold_coefficients=[str(x) for x in strict_poly.all_coeffs()]))
record=dict(status='PASS',cases=rows,elapsed_ns=perf_counter_ns()-start,
            python=platform.python_version(),sympy=s.__version__,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='Exact formula identity, degree6 irreducibility, one admissible critical root, correct extremum signs and degree4 strict upper decision; one fixed rational block only.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',values=[r['value_decimal'] for r in rows],elapsed_ns=record['elapsed_ns'])))
