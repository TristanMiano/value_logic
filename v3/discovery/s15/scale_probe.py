"""Finite floating screen of relative_scale.md; not outward certification."""
import hashlib
import json
from pathlib import Path
from time import perf_counter_ns

HERE = Path(__file__).resolve().parent
OUT = HERE/'scale_probe.json'
assert not OUT.exists(), 'Preserve exposed outputs.'
started = perf_counter_ns()


def ell(k, p):
    return (1+k**(p/(p-1)))**(1-p)


def bounds(s, p, scale, e, eta):
    q, a = p/(p-1), s**(1/p)
    t = max(0., s**(-1/(p-1))-1)**(1/q)
    def objective(k, direction):
        amp = a*(1+k**q)**(1/q)
        if direction == 'lower':
            return max(0.,amp-eta)**p*ell(scale*k+e,p)
        return (amp+eta)**p*ell(max(0.,scale*k-e),p)
    if scale == 0:
        return max(0.,1-eta)**p*ell(e,p), (1+eta)**p, None, None, t, objective
    if e == 0:
        if eta >= a or scale <= 1:
            kl = 0.
        elif eta == 0:
            kl = t
        else:
            ratio = (1-scale**(-q))*a/eta
            kl = min(t, max(0.,ratio**p-1)**(1/q))
        if scale >= 1:
            ku = 0.
        elif eta == 0:
            ku = t
        else:
            ratio = (scale**(-q)-1)*a/eta
            ku = min(t, max(0.,ratio**p-1)**(1/q))
    else:
        if eta >= a:
            kl = 0.
        else:
            def gl(k):
                return (scale-(k/(scale*k+e))**(q-1)-e*k**(q-1))/(1+k**q)**((q-1)/q)
            lo, hi = 0., 1.
            while gl(hi) > scale*eta/a:
                hi *= 2
            for _ in range(90):
                mid = (lo+hi)/2
                if gl(mid) > scale*eta/a:
                    lo = mid
                else:
                    hi = mid
            kl = min(t,(lo+hi)/2)
        boundary = e/scale
        def gu(k):
            return ((k/(scale*k-e))**(q-1)-scale-e*k**(q-1))/(1+k**q)**((q-1)/q)
        lo, hi = boundary, boundary+1
        while gu(hi) > scale*eta/a:
            hi = boundary+2*(hi-boundary)
        for _ in range(90):
            mid = (lo+hi)/2
            if mid == boundary or scale*mid-e <= 0 or gu(mid) > scale*eta/a:
                lo = mid
            else:
                hi = mid
        ku = min(t,(lo+hi)/2)
    return objective(kl,'lower'),objective(ku,'upper'),kl,ku,t,objective


rows = []
checks = 0
for p in [4/3, 1.5, 2., 3., 4.]:
    for scale in [.1,.5,1.,2.,10.]:
        for e in [0.,.25,1.]:
            for eta in [0.,.03,.2,.7]:
                previous = (-1.,-1.)
                for s in [.03,.1,.6,1.]:
                    lower,upper,kl,ku,t,obj = bounds(s,p,scale,e,eta)
                    assert -1e-12 <= lower <= upper+1e-11
                    assert upper <= (1+eta)**p+1e-10
                    assert lower >= previous[0]-1e-11 and upper >= previous[1]-1e-11
                    previous = (lower,upper)
                    for i in range(101):
                        k = t*i/100
                        assert lower <= obj(k,'lower')+1e-10, (p,scale,e,eta,s,'lower')
                        assert upper >= obj(k,'upper')-1e-10, (p,scale,e,eta,s,'upper')
                        checks += 2
                    witnesses = {}
                    for direction,k,endpoint in [('lower',kl,lower),('upper',ku,upper)]:
                        gaps = []
                        for K in [100.,1000.,10000.]:
                            tail = ell(K,p)
                            weight = (s-tail)/(ell(k,p)-tail)
                            assert -1e-12 <= weight <= 1+1e-12
                            weight = min(1.,max(0.,weight))
                            c = weight**(1/p)
                            assert abs(weight*ell(k,p)+(1-weight)*tail-s)<1e-11
                            if direction == 'lower':
                                val = max(c-eta,0.)**p*ell(scale*k+e,p)+(1-weight)*ell(scale*K,p)
                                gap = val-endpoint
                            else:
                                val = (c+eta)**p*ell(max(scale*k-e,0.),p)+(1-weight)*ell(scale*K,p)
                                gap = endpoint-val
                            assert gap >= -1e-10, (p,scale,e,eta,s,direction,gap)
                            gaps.append(gap)
                        assert gaps[-1] <= gaps[0]+1e-10
                        witnesses[direction] = gaps
                    if e == eta == 0:
                        endpoints = sorted([s,ell(scale*t,p)])
                        assert max(abs(a-b) for a,b in zip(endpoints,[lower,upper])) < 1e-11
                    rows.append(dict(p=p,scale=scale,e=e,eta=eta,s=s,
                                     bounds=[lower,upper],optimizing_k=[kl,ku],witness_gaps=witnesses))

zero_scale = []
for p in [4/3,2.,4.]:
    for s in [.03,.6,1.]:
        for e in [0.,.25,1.]:
            for eta in [0.,.2,1.,2.]:
                lower,upper,*_ = bounds(s,p,0.,e,eta)
                assert abs(lower-max(0.,1-eta)**p*ell(e,p))<1e-12
                assert abs(upper-(1+eta)**p)<1e-12
                zero_scale.append(dict(p=p,s=s,e=e,eta=eta,bounds=[lower,upper]))

result = dict(status='PASS',classification='DEVELOPMENT; floating finite checks',
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              elapsed_ns=perf_counter_ns()-started,parameter_cases=len(rows),
              scalar_grid_inequalities=checks,zero_scale_cases=len(zero_scale),
              regularization_example=list(bounds(.1,2.,.5,0.,0.)[:2]),
              rows=rows,zero_scale=zero_scale)
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('rows','zero_scale')},indent=2))
