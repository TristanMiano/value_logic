"""DEVELOPMENT: small source-reduction and scalar hard-case witness screen."""
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import math
import platform
import numpy as np
import scipy
from scipy.optimize import brentq, minimize

here=Path(__file__).resolve().parent
out=here/'minrank_probe.json'
assert not out.exists(), 'Preserve original evidence.'
started=perf_counter_ns()


def fixed_minimum(M,v,e):
    E=e*e
    b,V=np.linalg.eigh(M.T@M)
    g=V.T@M.T@v
    bmin=float(b[0])
    tm=2*E/(bmin+1+E+math.sqrt((bmin+1+E)**2-4*bmin*E))
    kernel=np.abs(b-bmin)<1e-10
    finite=np.linalg.norm(g[kernel])<1e-10

    def values(t,endpoint=False):
        den=(1-t)*b+1+E-E/t
        x=np.zeros(len(b))
        active=~kernel if endpoint else np.ones(len(b),dtype=bool)
        x[active]=(1-t)*g[active]/den[active]
        physical=V@x
        R=float(np.linalg.norm(v-M@physical)**2)
        a=float(physical@physical)
        derivative=-R+E*a/(t*t)
        h=(1-t)*R+(1+E-E/t)*a
        return h,derivative,x,R,a

    hard=False
    if finite and values(tm,True)[1]<=0:
        hard=True
        h,deriv,x,R,a=values(tm,True)
        extra=(R-E*a/(tm*tm))/(E/(tm*tm)-bmin)
        assert extra>=-1e-10
        x[np.flatnonzero(kernel)[0]]=math.sqrt(max(0,extra))
        t=tm
    else:
        lo=tm+max(1e-13,(1-tm)*1e-12)
        hi=1-1e-12
        assert values(lo)[1]>0 and values(hi)[1]<0
        t=brentq(lambda q:values(q)[1],lo,hi,xtol=2e-14)
        h,deriv,x,R,a=values(t)
    x=V@x
    residual=v-M@x
    Delta=e*np.outer(residual/np.linalg.norm(residual),x/np.linalg.norm(x))
    direct=float(v@np.linalg.solve(np.eye(len(v))+(M+Delta)@(M+Delta).T,v))
    primal=float(x@x+np.linalg.norm(v-(M+Delta)@x)**2)
    assert abs(direct-h)<2e-8,(direct,h,t,hard)
    assert abs(primal-h)<2e-8,(primal,h,t,hard)
    assert abs(np.linalg.norm(Delta,2)-e)<1e-9
    return h,{'t':float(t),'tmin':tm,'hard_case':hard,'direct_value':direct}


rows=[]
for lambdas in ([.5],[.2,.8],[.1,.4,.7]):
    r=len(lambdas)
    C0=np.array(lambdas)
    for mass in (0,.2,.8,1):
        # Unequal nonzero components, plus a zero g hard case at mass=1.
        direction=np.arange(1,r+1,dtype=float)
        direction/=np.linalg.norm(direction)
        c=np.r_[math.sqrt(mass),math.sqrt(1-mass)*direction]
        C=np.diag(np.r_[1,C0]);k=len(c)
        M0=np.vstack([np.zeros((1,r)),np.diag(np.sqrt(1/C0-1))])
        s=float(c@C@c);m0=float(c@C@C@c)
        for e in (.1,.7,2):
            E=e*e;cap=(E+math.sqrt(E*E+4*E))/2
            u=1/(2+cap);bstar=1/(1+cap)
            canonical,detail=fixed_minimum(M0,c,e)
            iscap=s-m0>=u*s-1e-12
            if iscap:
                z=np.sqrt(1-C0)*c[1:]
                Q=float(z@(C0*z))
                scale=u*s/Q
                B=scale*C0
                X=np.vstack([np.zeros((1,r)),np.diag(np.sqrt(1-C0)),
                             np.diag(np.sqrt(C0-B))])
                M=X@np.diag(1/np.sqrt(B))
                v=np.r_[c,np.zeros(r)]
                old=np.linalg.inv(np.eye(len(v))+M@M.T)
                assert np.max(np.abs(old[:k,:k]-C))<2e-10
                x=np.sqrt(B)*z
                residual=v-M@x
                Delta=e*np.outer(residual/np.linalg.norm(residual),x/np.linalg.norm(x))
                got=float(v@np.linalg.solve(np.eye(len(v))+(M+Delta)@(M+Delta).T,v))
                answer=bstar*s
                assert abs(got-answer)<2e-9,(got,answer)
                assert canonical>=answer-2e-8
            else:
                answer=canonical
            rows.append({'C0':lambdas,'protected_target_mass':mass,'e':e,
                         'case':'cap' if iscap else 'canonical','value':float(answer),
                         'canonical_value':float(canonical),'scalar':detail})

# Additional endpoint with a nonzero g outside the least-eigenvalue space.
C0=np.array([.2,.8]);c=np.array([math.sqrt(.99),.1,0.])
M=np.vstack([np.zeros((1,2)),np.diag(np.sqrt(1/C0-1))])
special,detail=fixed_minimum(M,c,1)
assert detail['hard_case']

# A few direct primal minimizations for information, not a global certificate.
checks=[]
for lambdas,c,e in [([.2,.8],np.array([math.sqrt(.8),math.sqrt(.1),math.sqrt(.1)]),.7),
                    ([.5],np.array([1.,0.]),1.)]:
    C0=np.array(lambdas);r=len(C0)
    M=np.vstack([np.zeros((1,r)),np.diag(np.sqrt(1/C0-1))])
    expected,detail=fixed_minimum(M,c,e)
    def primal(x):
        return float(x@x+max(np.linalg.norm(c-M@x)-e*np.linalg.norm(x),0)**2)
    attempts=[minimize(primal,start,method='BFGS',options={'gtol':1e-9})
              for start in (np.zeros(r),np.ones(r)*.2,-np.ones(r)*.2)]
    best=min(float(a.fun) for a in attempts)
    assert best>=expected-2e-8
    assert abs(best-expected)<2e-7
    checks.append({'expected':float(expected),'best_primal':best,
                   'optimizer_success':[bool(a.success) for a in attempts]})

result={'status':'PASS','scope':'36 compatible-source cases plus one nonzero-g hard case and two local-primal screens; DEVELOPMENT only',
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'elapsed_ns':perf_counter_ns()-started,'cases':rows,
        'nonzero_g_hard_case':{'value':float(special),**detail},'primal_checks':checks}
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','cases':len(rows),'cap':sum(x['case']=='cap' for x in rows),
                  'scalar_hard':sum(x['scalar']['hard_case'] for x in rows),
                  'nonzero_g_hard_case':result['nonzero_g_hard_case'],
                  'elapsed_ns':result['elapsed_ns']}))
