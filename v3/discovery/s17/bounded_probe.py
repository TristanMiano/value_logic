"""Bounded-source piecewise endpoints versus exact-form SDP; DEVELOPMENT.

Codex (GPT-6). Seven specified branch cases; 1e-6 endpoint discrepancy and
5e-7 feasibility tolerance. Numerical solutions are not exact certificates.
"""
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
import warnings
import cvxpy as cp
import numpy as np
import scipy
from scipy.optimize import minimize_scalar

HERE=Path(__file__).resolve().parent
OUT=HERE/'bounded_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')

def endpoints(C,c,e,K):
    lam,V=np.linalg.eigh(C)
    weights=(V.T@c)**2
    E=e*e; beta=1/(1+K*K); s=float(c@C@c)
    assert min(lam)>=beta-1e-12
    p=(s-beta)/(1-beta)
    if abs(p)<1e-13:
        p=0.
    h=(E+np.sqrt(E*E+4*E))/2
    lr,ur=1/(1+h),h/(1+h)
    def low(r):
        if r in (0.,1.):
            return 0.
        if r<=lr:
            return float(weights@(1/(1+(1/lam-1)/r+E/(1-r))))
        return float(p/(1+E/(1-r))+(1-p)/(1+(1/beta-1)/r+E/(1-r)))
    def up(r):
        if r==0:
            return 1.
        if r==1:
            return (1+E)/(K*K) if p==0 else np.inf
        a,b=1/(1-r),1+E/r
        if r<=ur:
            return float(weights@(a*b*lam/(a+(b-a)*lam)))
        return float(p*a+(1-p)*a*b*beta/(a+(b-a)*beta))
    results={}
    success=True
    for side,fun,cap,sign in [('lower',low,lr,-1),('upper',up,ur,1)]:
        pts=[0.,cap,1.]
        for left,right in [(0.,cap),(cap,1.)]:
            opt=minimize_scalar(lambda r:sign*fun(r),bounds=(left,right),
                                method='bounded',options={'xatol':1e-13})
            success=success and bool(opt.success)
            pts.append(float(opt.x))
        value,r=min([(sign*fun(r),r) for r in pts])
        results[side]=dict(value=sign*value,r=r,
                           branch='core' if r<cap else 'chord' if r>cap else 'cap')
    results['success']=success
    return results

def solve(C,c,e,K):
    k=len(c)
    G=cp.Variable((2*k+2,2*k+2),symmetric=True)
    H=cp.Variable((k+2,k+2),symmetric=True)
    r,u,x,z=2*k,2*k+1,k,k+1
    f=c@G[:k,r]
    cons=[G>>0,H>>0,G[:k,:k]==np.eye(k),G[:k,k:2*k]==C,
          G[k:2*k,k:2*k]+H[:k,:k]==C,
          G[k:2*k,:k]@c-G[k:2*k,r]-G[k:2*k,u]==H[:k,x],
          G[:k,r]-G[k:2*k,r]==H[:k,x]-H[:k,z],
          f==G[r,r]+H[x,x],G[r,u]==H[x,z],
          G[u,u]<=e*e*H[x,x],H[z,z]<=e*e*G[r,r]]
    Ac=np.zeros((k+2,k+1)); Ac[:k,:k]=np.eye(k); Ac[x,k]=1
    Fc=Ac.copy(); Fc[z,k]=-1
    Bc=np.zeros((2*k+2,k+1))
    Bc[:k,:k]=np.eye(k); Bc[k:2*k,:k]=-np.eye(k)
    Bc[:k,k]=c; Bc[r,k]=-1; Bc[u,k]=-1
    Dc=np.zeros_like(Bc); Dc[k:2*k,:k]=np.eye(k); Dc[r,k]=1
    cons.extend([K*K*(Ac.T@H@Ac)-Bc.T@G@Bc>>0,
                 K*K*(Dc.T@G@Dc)-Fc.T@H@Fc>>0])
    results={}
    for side,objective in [('lower',cp.Minimize(f)),('upper',cp.Maximize(f))]:
        problem=cp.Problem(objective,cons)
        begin=perf_counter_ns()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            value=problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,
                                tol_gap_rel=1e-9,tol_feas=1e-9,max_iter=400)
        results[side]=dict(value=float(value),status=problem.status,
                           elapsed_ns=perf_counter_ns()-begin,
                           violation=max(float(np.max(q.violation())) for q in cons),
                           warnings=[str(w.message) for w in caught],
                           gram_output=G.value.tolist(),gram_input=H.value.tolist())
    return results

rot=np.array([[.6,-.8],[.8,.6]])
cases=[('scalar_rotation',np.array([[.1]]),np.array([1.]),1.,3.),
       ('scalar_chord',np.array([[.25]]),np.array([1.]),.1,np.sqrt(3)),
       ('two_chords',np.diag([.1,.11]),np.ones(2)/np.sqrt(2),1.,3.),
       ('core_interiors',rot@np.diag([.1,.9])@rot.T,rot@(np.ones(2)/np.sqrt(2)),1.,3.),
       ('upper_cap',np.diag([.1,.2]),np.ones(2)/np.sqrt(2),1.,3.),
       ('cancellation',np.diag([.8,.9]),np.array([.6,.8]),1.,1.),
       ('both_caps',np.diag([.1,.2]),np.ones(2)/np.sqrt(2),1.,10.)]
start=perf_counter_ns()
rows=[]
for name,C,c,e,K in cases:
    reference=endpoints(C,c,e,K)
    sdp=solve(C,c,e,K)
    error=max(abs(reference[s]['value']-sdp[s]['value']) for s in ('lower','upper'))
    passed=(reference['success'] and error<=1e-6 and
            all(sdp[s]['status'] in ('optimal','optimal_inaccurate') and
                sdp[s]['violation']<=5e-7 for s in ('lower','upper')))
    rows.append(dict(case=name,C=C.tolist(),c=c.tolist(),e=e,K=K,
                     reference=reference,sdp=sdp,discrepancy=error,passed=passed))
    print(json.dumps(dict(case=name,passed=passed,error=error,
                          lower=reference['lower'],upper=reference['upper'])))
record=dict(status='PASS' if all(r['passed'] for r in rows) else 'FAIL',
            cases=rows,elapsed_ns=perf_counter_ns()-start,
            versions=dict(python=platform.python_version(),numpy=np.__version__,
                          scipy=scipy.__version__,cvxpy=cp.__version__),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='Seven specified branch cases against the conventional bounded-operator SDP; no exact certificate or speedup claim.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status=record['status'],elapsed_ns=record['elapsed_ns'])))
if record['status']!='PASS':
    raise SystemExit(1)
