"""Small DEVELOPMENT panel for local_contrasts.md; Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
import numpy as np

here=Path(__file__).resolve().parent
out=here/'local_contrast_probe.json'
assert not out.exists(), 'Preserve original evidence.'
t0=perf_counter_ns()
rng=np.random.default_rng(1651)
max_ratio=0.
cases=0
for n,m,k in [(2,2,2),(3,2,2),(4,3,3),(6,5,4)]:
    for _ in range(30):
        M=rng.normal(size=(n,m))*10**rng.uniform(-1,1)
        W=np.linalg.qr(rng.normal(size=(n,k)))[0]
        H=rng.normal(size=(k,k)); H=(H+H.T)/2
        S=np.linalg.inv(np.eye(n)+M@M.T)
        C=W.T@S@W; D=W.T@S@S@W
        P=S@W; Q=M.T@P
        G=P@H@Q.T
        assert np.allclose(np.sum(G*G),np.trace(H@D@H@(C-D)),atol=1e-10)
        e=10**rng.uniform(-4,-1)
        edit=rng.normal(size=(n,m)); edit*=e/np.linalg.norm(edit)
        N=M+edit; SN=np.linalg.inv(np.eye(n)+N@N.T)
        linear=-2*np.sum(G*edit)
        actual=np.trace(H@(W.T@SN@W-C))
        bound=np.linalg.svd(H,compute_uv=False).sum()*e*e
        residual=abs(actual-linear)
        assert residual<=bound+1e-10
        max_ratio=max(max_ratio,float(residual/bound))
        cases+=1

limit_cases=[]
H=np.diag([1.,-1.]); u=np.ones(2)/np.sqrt(2)
for c in [.1,.25,.4,.5,.7,.9]:
    limit=2*c*np.sqrt(1-c) if c<=.5 else 2*c*np.sqrt(2*c*(1-c))
    if c<.5:
        slopes=[]
        for tau in [.9,.99,.999,.9999]:
            S=np.zeros((3,3)); S[:2,:2]=c*np.eye(2)
            S[:2,2]=S[2,:2]=np.sqrt(tau*c*(1-c))*u
            S[2,2]=1-tau*c
            assert np.linalg.eigvalsh(S)[0]>0
            assert np.linalg.eigvalsh(np.eye(3)-S)[0]>-1e-12
            assert np.linalg.matrix_rank(np.eye(3)-S,tol=1e-10)==2
            D=(S@S)[:2,:2]
            slope=2*np.sqrt(np.trace(H@D@H@(c*np.eye(2)-D)))
            assert slope<=limit+1e-12
            slopes.append(float(slope))
        assert all(a<b for a,b in zip(slopes,slopes[1:]))
        assert limit-slopes[-1]<1e-4
    else:
        D=c*c*np.eye(2)
        slope=2*np.sqrt(np.trace(H@D@H@(c*np.eye(2)-D)))
        assert abs(slope-limit)<1e-12
        slopes=[float(slope)]
    limit_cases.append(dict(c=c,limit=float(limit),slopes=slopes))

# A rational outward bound for the stated strict percentage, no floating proof.
sqrt_upper=F(77459667,100000000)
assert sqrt_upper**2>F(3,5)
radius_upper=sqrt_upper/F(125)+F(1,5000)
separate_lower=F(1,125)
gain_lower=1-radius_upper/separate_lower
assert gain_lower>F(2004,10000)
result=dict(status='PASS',seed=1651,random_cases=cases,
            max_remainder_bound_ratio=max_ratio,limit_cases=limit_cases,
            exact_radius_upper=str(radius_upper),exact_gain_lower=str(gain_lower),
            elapsed_ns=perf_counter_ns()-t0,python=platform.python_version(),
            numpy=np.__version__,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='Finite floating sanity checks plus an exact rational percentage certificate; no independent confirmation.')
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
