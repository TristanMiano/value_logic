"""DEVELOPMENT: a cheap exact certificate and numerical attainment screen."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import math
import platform
import numpy as np

HERE=Path(__file__).resolve().parent
OUT=HERE/'matrix_probe.json'
assert not OUT.exists(), 'Do not overwrite original evidence.'
start=perf_counter_ns()


def exact_g(spectrum,weights,E,eta):
    assert eta>0 and eta*eta<=E*(1+eta)
    a=1+eta; k=E+E/eta-eta
    z=[a/(a+k*l) for l in spectrum]
    A=1-sum(2*p*(1-l)*x for p,l,x in zip(weights,spectrum,z))
    A+=sum(p*(1-l)*x*x for p,l,x in zip(weights,spectrum,z))
    Q=sum(p*l*(1-l)*x*x for p,l,x in zip(weights,spectrum,z))
    answer=a*A+k*Q
    independently=sum(p*a*(1+E+E/eta)*l/(a+k*l) for p,l in zip(weights,spectrum))
    assert answer==independently
    return answer,z


spectrum=[F(1,10),F(9,10)];weights=[F(1,2)]*2;E=F(1,100)
choices=[(exact_g(spectrum,weights,E,F(j,10000))[0],F(j,10000)) for j in range(1,1052)
         if F(j,10000)**2<=E*(1+F(j,10000))]
best,eta=min(choices)
assert best<F(539,1000)
exact=dict(spectrum=list(map(str,spectrum)),weights=list(map(str,weights)),
           eta=str(eta),bound=str(best),decimal_illustration=float(best))


def golden_min(f,lo,hi):
    phi=(math.sqrt(5)-1)/2
    x=hi-phi*(hi-lo);y=lo+phi*(hi-lo);fx=f(x);fy=f(y)
    for _ in range(120):
        if fx<fy:
            hi=y;y=x;fy=fx;x=hi-phi*(hi-lo);fx=f(x)
        else:
            lo=x;x=y;fx=fy;y=lo+phi*(hi-lo);fy=f(y)
    return (lo+hi)/2


def positive_root(A):
    values,basis=np.linalg.eigh(A)
    assert values.min()>-1e-10
    return (basis*np.sqrt(np.maximum(values,0)))@basis.T


def evaluate(lambdas,probabilities,e):
    lam=np.array(lambdas,float);p=np.array(probabilities,float)
    C=np.diag(lam);c=np.sqrt(p);size=len(lam);E=e*e
    s=float(p@lam);m0=float(p@(lam*lam));cap=(E+math.sqrt(E*E+4*E))/2
    def g(eta):
        if eta==0:return 1.0
        a=1+eta;k=E+E/eta-eta
        return float(p@(a*(1+E+E/eta)*lam/(a+k*lam)))
    eta=golden_min(g,max(1e-12,cap*1e-10),cap)
    choices=[(g(eta),eta,'interior'),(g(cap),cap,'upper'),(1.,0.,'zero')]
    value,eta,case=min(choices)
    # Avoid misclassifying a numerically almost-boundary minimizer.
    if abs(g(cap)-value)<1e-11:value,eta,case=g(cap),cap,'upper'
    if abs(1-value)<1e-11:value,eta,case=1.,0.,'zero'
    if case=='zero':
        M=np.diag(np.sqrt(1/lam-1));v=c
        N=M-np.outer(v,M.T@v)
    elif case=='upper':
        qstar=s/(1+E/(cap*cap));mstar=s-qstar
        tau=(mstar-m0)/(s-m0)
        assert -1e-8<=tau<1
        tau=max(0,tau)
        B=np.diag(np.sqrt(tau*lam*(1-lam)))
        S=np.block([[C,B],[B,np.eye(size)-C]])
        M=positive_root(np.linalg.inv(S)-np.eye(2*size))
        v=np.concatenate([c,np.zeros(size)])
        w=S@v;x=M.T@w
        N=M-e*np.outer(w/np.linalg.norm(w),x/np.linalg.norm(x))
    else:
        M=np.diag(np.sqrt(1/lam-1));v=c
        a=1+eta;k=E+E/eta-eta
        z=a*c/(a+k*lam);x=M.T@C@z;r=v-M@x
        N=M-e*np.outer(r/np.linalg.norm(r),x/np.linalg.norm(x))
    identity=np.eye(len(v))
    source=np.linalg.solve(identity+M@M.T,identity)
    compression=source[:size,:size]
    actual=float(v@np.linalg.solve(identity+N@N.T,v))
    edit=float(np.linalg.norm(N-M,2))
    discrepancy=abs(actual-value)
    assert np.max(np.abs(compression-C))<1e-8
    assert edit<=e+1e-8
    assert discrepancy<2e-7, (lambdas,probabilities,e,case,value,actual,eta)
    return dict(lambdas=lambdas,probabilities=probabilities,e=e,case=case,
                eta=eta,bound=value,actual=actual,discrepancy=discrepancy,edit_norm=edit)


panel=[]
for lam,p in [([.1,.9],[.5,.5]),([.1,.2],[.5,.5]),([.8,.9],[.25,.75]),
              ([.05,.4,.95],[.2,.3,.5]),([.25],[1.])]:
    for e in [.01,.1,.5,1.,3.]:panel.append(evaluate(lam,p,e))
assert {row['case'] for row in panel}=={'interior','upper','zero'}
result=dict(status='PASS',contributor='Codex (GPT-6)',classification='DEVELOPMENT',
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            python=platform.python_version(),numpy=np.__version__,exact=exact,panel=panel,
            elapsed_ns=perf_counter_ns()-start,
            limits='Only the rational selected certificate is exact. Numerical matching checks are a small same-model screen, not independent proof or complete-cost comparison.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status=result['status'],exact=exact,cases={c:sum(r['case']==c for r in panel) for c in ('interior','upper','zero')},elapsed_ns=result['elapsed_ns'])))
