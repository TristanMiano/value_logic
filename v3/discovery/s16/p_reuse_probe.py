"""Finite DEVELOPMENT checks of nonquadratic_reuse.md; Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
import numpy as np

here=Path(__file__).resolve().parent
out=here/'p_reuse_probe.json'
assert not out.exists(), 'Preserve original evidence.'
start=perf_counter_ns()
exact=[]
for p,q in [(F(3,2),F(3)),(F(2),F(2)),(F(3),F(3,2))]:
    for denom in [2,5,10,100]:
        # e is a rational square, so all displayed e powers are exact.
        root=F(1,denom); e=root*root
        def power(exponent):
            z=2*exponent
            assert z.denominator==1
            return root**int(z)
        eq=power(q); eq1=power(q-1); ep=power(p); m22=power(2-q)
        B=1+eq/2
        x=[1/B,-eq1/B]
        residual=[2-(x[0]-e*x[1]),-(e*x[0]+m22*x[1])]
        assert residual==[1/B,0]
        # After multiplication by B^(p-1), stationarity is [1,-e]=[1,-e].
        assert power((q-1)*(p-1))==e
        assert (q-1)*p==q
        assert 2+eq==2*B
        ratio_base=1+ep/2
        # Record the exact square when p=3/2; otherwise the exact ratio.
        ratio_power=2 if p==F(3,2) else 1
        ratio=ratio_base**ratio_power*B**int((p-1)*ratio_power)
        assert ratio>1
        exact.append(dict(p=str(p),e=str(e),ratio_power=ratio_power,ratio_exact=str(ratio)))

rng=np.random.default_rng(1654)
checks=0
max_fraction=0.
def norm(x,p): return float(np.sum(abs(x)**p)**(1/p))
def jmap(x,p): return np.sign(x)*abs(x)**(p-1)
def remainder(s,t):
    if s<=2: return 2**(2-s)*t**s
    return s*(s-1)/2*(1+t)**(s-2)*t*t
for p in [1.25,1.5,2.,3.,4.]:
    q=p/(p-1)
    for _ in range(40):
        n,m=3,4
        r=rng.normal(size=m); x=rng.normal(size=n)
        scale=(norm(r,p)**p+norm(x,p)**p)**(1/p)
        r/=scale; x/=scale
        a=norm(r,p); b=norm(x,p)
        jr=jmap(r,p); jx=jmap(x,p)
        Z=rng.normal(size=(n,m))
        M=np.outer(jx,jr)/(jr@jr)+Z@(np.eye(m)-np.outer(jr,jr)/(jr@jr))
        y=M.T@x+r
        assert np.allclose(M@jr,jx)
        edit=rng.normal(size=(n,m))
        e=10**rng.uniform(-4,-.1)
        # Induced q norm bound, equivalent to the transpose p norm bound.
        norm_bound=np.linalg.norm(edit,1)**(1/q)*np.linalg.norm(edit,np.inf)**(1-1/q)
        edit*=e/norm_bound
        N=M+edit
        wp=np.concatenate([r-edit.T@x,x])
        h=np.concatenate([jr,N@jr])
        product=norm(wp,p)*norm(h,q)
        bound=1+remainder(p,e*b)/p+remainder(q,e*a**(p-1))/q
        assert product<=bound+1e-10
        z=rng.normal(size=n)
        assert abs(h@np.concatenate([y-N.T@z,z])-1)<1e-9
        assert norm(wp,p)**p<=(a+e*b)**p+b**p+1e-10
        max_fraction=max(max_fraction,(product-1)/(bound-1))
        if p==2:
            assert abs(bound-(1+e*e/2))<1e-12
        checks+=1
result=dict(status='PASS',exact_family_cases=exact,random_cases=checks,seed=1654,
            max_fraction_of_smoothness_excess=float(max_fraction),
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),numpy=np.__version__,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='Exact displayed family algebra and finite floating inequality sanity checks; no independent confirmation.')
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
