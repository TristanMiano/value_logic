"""One-case conventional control for second-block/norm bounds; DEVELOPMENT.

Codex (GPT-6). Approximate screen: 1e-6 reference error, 5e-7 constraint
violation. No solver output is an exact certificate or timing comparison.
"""
from fractions import Fraction
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
OUT=HERE/'norm_sdp_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
number=lambda s:float(Fraction(s))
old=json.loads((HERE/'second_result.json').read_text())
extra=json.loads((HERE/'norm_result.json').read_text())
C=np.array([[number(s) for s in row] for row in old['C']])
Q=np.array([[number(s) for s in row] for row in old['Q']])
c=np.array([number(row[0]) for row in old['unnormalized_c']])
c=c/np.linalg.norm(c)
k=len(c); E=1.; K2=number(extra['K_squared_warrant'])
T=C-Q; H0=np.eye(k)-C; B0=np.eye(k)-2*C+Q

def upper(r):
    if r==0:
        return 1.
    a,b=1/(1-r),1+E/r
    return float(a-a*a*c@H0@np.linalg.solve(a*B0+b*T,H0@c))

opt=minimize_scalar(upper,bounds=(1e-10,1-1e-10),method='bounded',
                    options={'xatol':1e-12})
reference_upper=min(1.,upper(float(opt.x)))

def solve(norm_bound):
    G=cp.Variable((2*k+2,2*k+2),symmetric=True)
    H=cp.Variable((k+2,k+2),symmetric=True)
    r,u,x,z=2*k,2*k+1,k,k+1
    f=c@G[:k,r]
    cons=[G>>0,H>>0,G[:k,:k]==np.eye(k),G[:k,k:2*k]==C,
          G[k:2*k,k:2*k]==Q,H[:k,:k]==T,
          G[k:2*k,:k]@c-G[k:2*k,r]-G[k:2*k,u]==H[:k,x],
          G[:k,r]-G[k:2*k,r]==H[:k,x]-H[:k,z],
          f==G[r,r]+H[x,x],G[r,u]==H[x,z],
          G[u,u]<=E*H[x,x],H[z,z]<=E*G[r,r]]
    if norm_bound:
        Ac=np.zeros((k+2,k+1)); Ac[:k,:k]=np.eye(k); Ac[x,k]=1
        Fc=Ac.copy(); Fc[z,k]=-1
        Bc=np.zeros((2*k+2,k+1))
        Bc[:k,:k]=np.eye(k); Bc[k:2*k,:k]=-np.eye(k)
        Bc[:k,k]=c; Bc[r,k]=-1; Bc[u,k]=-1
        Dc=np.zeros_like(Bc); Dc[k:2*k,:k]=np.eye(k); Dc[r,k]=1
        cons.extend([K2*(Ac.T@H@Ac)-Bc.T@G@Bc>>0,
                     K2*(Dc.T@G@Dc)-Fc.T@H@Fc>>0])
    rows={}
    for side,objective in [('lower',cp.Minimize(f)),('upper',cp.Maximize(f))]:
        problem=cp.Problem(objective,cons)
        begin=perf_counter_ns()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            value=problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,
                                tol_gap_rel=1e-9,tol_feas=1e-9,max_iter=300)
        violation=max(float(np.max(q.violation())) for q in cons)
        rows[side]=dict(value=float(value),status=problem.status,
                       violation=violation,elapsed_ns=perf_counter_ns()-begin,
                       warnings=[str(w.message) for w in caught],
                       gram_output=G.value.tolist(),gram_input=H.value.tolist())
    return rows

start=perf_counter_ns()
unbounded=solve(False)
bounded=solve(True)
discrepancy=max(abs(unbounded['lower']['value']-number(old['lower_infimum'])),
                abs(unbounded['upper']['value']-reference_upper))
rows=list(unbounded.values())+list(bounded.values())
passed=(bool(opt.success) and discrepancy<=1e-6 and
        all(r['status']=='optimal' and r['violation']<=5e-7 for r in rows) and
        bounded['lower']['value']>=number(extra['improved'])-1e-7 and
        bounded['lower']['value']<=number(extra['actual'])+1e-7 and
        bounded['upper']['value']<=unbounded['upper']['value']+1e-7)
record=dict(status='PASS' if passed else 'FAIL',C=C.tolist(),Q=Q.tolist(),
            c=c.tolist(),E=E,K_squared=K2,unbounded=unbounded,bounded=bounded,
            scalar_upper=reference_upper,upper_r=float(opt.x),
            max_reference_discrepancy=discrepancy,
            explicit_lower=number(extra['improved']),
            elapsed_ns=perf_counter_ns()-start,
            versions=dict(python=platform.python_version(),numpy=np.__version__,
                          scipy=scipy.__version__,cvxpy=cp.__version__),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            inputs={p:hashlib.sha256((HERE/p).read_bytes()).hexdigest()
                    for p in ('second_result.json','norm_result.json')},
            scope='One noncommuting case with and without a known source norm; approximate conventional control only.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status=record['status'],unbounded=[unbounded[s]['value'] for s in ('lower','upper')],
                     bounded=[bounded[s]['value'] for s in ('lower','upper')],
                     discrepancy=discrepancy,elapsed_ns=record['elapsed_ns'])))
if not passed:
    raise SystemExit(1)
