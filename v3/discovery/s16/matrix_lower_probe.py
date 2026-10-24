"""DEVELOPMENT: exact lower certificate and small numerical matching screen."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import math
import platform
import numpy as np

HERE=Path(__file__).resolve().parent
OUT=HERE/'matrix_lower_probe.json'
assert not OUT.exists(), 'Preserve original evidence.'
started=perf_counter_ns()


def exact_lower(lam,p,E,eta):
    assert eta>0 and eta*eta>=E*(1+eta)
    a=1+eta;k=E+E/eta-eta
    z=[1/(a+k*l) for l in lam]
    answer=sum(w*l/(a+k*l) for w,l in zip(p,lam))
    check=sum(w*(2*l*x-l*(a+k*l)*x*x) for w,l,x in zip(p,lam,z))
    assert answer==check
    return answer


lam=[F(1,10),F(9,10)];p=[F(1,2)]*2;E=F(1,100)
choices=[(exact_lower(lam,p,E,F(j,10000)),F(j,10000)) for j in range(1052,5001)
         if F(j,10000)**2>=E*(1+F(j,10000))]
best,eta=max(choices)
assert best>F(4613,10000)
upper=F(867127945275459,1611861132384100)
new_width=upper-best
old_width_lower=F(100,181)-F(11311,25000)
reduction=1-new_width/old_width_lower
assert reduction>F(234,1000)


def golden_max(f,lo,hi):
    phi=(math.sqrt(5)-1)/2
    x=hi-phi*(hi-lo);y=lo+phi*(hi-lo);fx=f(x);fy=f(y)
    for _ in range(130):
        if fx>fy:
            hi=y;y=x;fy=fx;x=hi-phi*(hi-lo);fx=f(x)
        else:
            lo=x;x=y;fx=fy;y=lo+phi*(hi-lo);fy=f(y)
    return (lo+hi)/2


def root(A):
    vals,basis=np.linalg.eigh(A)
    assert vals.min()>-1e-9
    return (basis*np.sqrt(np.maximum(vals,0)))@basis.T


def evaluate(lambdas,probabilities,e):
    l=np.array(lambdas,float);p=np.array(probabilities,float);C=np.diag(l)
    c=np.sqrt(p);n=len(c);E=e*e;cap=(E+math.sqrt(E*E+4*E))/2
    s=float(p@l);m0=float(p@(l*l))
    def objective(eta):
        a=1+eta;k=E+E/eta-eta
        return float(p@(l/(a+k*l)))
    candidate=math.exp(golden_max(lambda t:objective(math.exp(t)),math.log(cap),math.log(100*cap)))
    if objective(candidate)<=objective(cap)+1e-11:
        eta=cap;case='boundary';value=objective(cap)
        mstar=s*(1+cap)/(2+cap);tau=(mstar-m0)/(s-m0)
        assert -1e-8<=tau<1
        B=np.diag(np.sqrt(max(tau,0)*l*(1-l)))
        S=np.block([[C,B],[B,np.eye(n)-C]])
        M=root(np.linalg.inv(S)-np.eye(2*n));v=np.concatenate([c,np.zeros(n)])
        w=S@v;x=M.T@w
    else:
        eta=candidate;case='interior';value=objective(eta)
        M=np.diag(np.sqrt(1/l-1));v=c
        a=1+eta;k=E+E/eta-eta
        z=c/(a+k*l);w=C@z;x=M.T@w
    N=M+e*np.outer(w/np.linalg.norm(w),x/np.linalg.norm(x))
    eye=np.eye(len(v));source=np.linalg.solve(eye+M@M.T,eye)
    actual=float(v@np.linalg.solve(eye+N@N.T,v))
    discrepancy=abs(actual-value);edit=float(np.linalg.norm(N-M,2))
    assert np.max(np.abs(source[:n,:n]-C))<1e-8
    assert edit<=e+1e-8
    assert discrepancy<2e-7,(lambdas,e,eta,case,value,actual)
    return dict(lambdas=lambdas,probabilities=probabilities,e=e,case=case,
                eta=eta,bound=value,actual=actual,discrepancy=discrepancy,edit_norm=edit)


panel=[]
for l,p in [([.1,.9],[.5,.5]),([.1,.2],[.5,.5]),([.8,.9],[.25,.75]),
            ([.05,.4,.95],[.2,.3,.5]),([.25],[1.])]:
    for e in [.01,.1,.5,1.,3.]:panel.append(evaluate(l,p,e))
assert {r['case'] for r in panel}=={'boundary','interior'}
result=dict(status='PASS',contributor='Codex (GPT-6)',classification='DEVELOPMENT',
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    python=platform.python_version(),numpy=np.__version__,panel=panel,
    exact=dict(eta=str(eta),lower=str(best),lower_decimal=float(best),upper=str(upper),
               new_width=str(new_width),width_reduction_strict_lower=str(reduction),
               width_reduction_decimal=float(reduction)),elapsed_ns=perf_counter_ns()-started,
    limits='Selected rational certificate exact; numerical panel and optimizer are developmental, not independent confirmation or an economic benchmark.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='PASS',exact=result['exact'],cases={c:sum(r['case']==c for r in panel) for c in ('boundary','interior')},elapsed_ns=result['elapsed_ns'])))
