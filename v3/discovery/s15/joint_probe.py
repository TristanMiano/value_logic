"""Cheap floating screen of joint_target.md; no outward proof claimed."""
import ast
import hashlib
import json
import math
from pathlib import Path
from time import perf_counter_ns

HERE = Path(__file__).resolve().parent
OUT = HERE / 'joint_probe.json'
assert not OUT.exists(), 'Preserve exposed results; replay in an isolated directory.'
started = perf_counter_ns()

# Reuse exactly the prior elementary optimizer functions, without rerunning
# that exposed probe or mutating its output. The dependency bytes are hashed.
dependency = HERE / 'norm_probe.py'
tree = ast.parse(dependency.read_text(encoding='utf-8'))
names = {'grad', 'objective', 'certificate', 'solve'}
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
assert {n.name for n in functions} == names
exec(compile(ast.Module(body=functions, type_ignores=[]), str(dependency), 'exec'))


def ell(k, p):
    return (1 + k**(p/(p-1)))**(1-p)


def bounds(s, p, e, eta):
    q, a = p/(p-1), s**(1/p)
    t = max(0., s**(-1/(p-1))-1)**(1/q)
    def objective(k, direction):
        amplitude = a*(1+k**q)**(1/q)
        if direction == 'lower':
            return max(0., amplitude-eta)**p*ell(k+e, p)
        return (amplitude+eta)**p*ell(max(0.,k-e), p)
    if e == 0:
        kl = ku = 0.
    else:
        if eta >= a:
            kl = 0.
        else:
            def g(k):
                return (1-e*k**(q-1)-(k/(k+e))**(q-1))/(1+k**q)**((q-1)/q)
            lo, hi = 0., 1.
            while g(hi) > eta/a:
                hi *= 2
            for _ in range(90):
                mid = (lo+hi)/2
                if g(mid) > eta/a:
                    lo = mid
                else:
                    hi = mid
            kl = min(t,(lo+hi)/2)
        def g(k):
            return ((k/(k-e))**(q-1)-1-e*k**(q-1))/(1+k**q)**((q-1)/q)
        lo, hi = e, e+1
        while g(hi) > eta/a:
            hi = e+2*(hi-e)
        for _ in range(90):
            mid = (lo+hi)/2
            if mid == e or g(mid) > eta/a:
                lo = mid
            else:
                hi = mid
        ku = min(t,(lo+hi)/2)
    return objective(kl,'lower'), objective(ku,'upper'), kl, ku, t, objective


rows = []
grid_checks = 0
for p in [4/3, 1.5, 2., 3., 4.]:
    for s in [.03, .1, .6, 1.]:
        for e in [0., .25, 1.]:
            for eta in [0., .03, .2, .7]:
                lower, upper, kl, ku, t, obj = bounds(s,p,e,eta)
                assert lower >= 0 and upper <= (1+eta)**p + 1e-11
                assert lower <= upper+1e-12
                for i in range(101):
                    k = t*i/100
                    assert lower <= obj(k,'lower')+1e-11
                    assert upper >= obj(k,'upper')-1e-11
                    grid_checks += 2
                witnesses = {}
                for direction, k, endpoint in [('lower',kl,lower),('upper',ku,upper)]:
                    gaps = []
                    for K in [100.,1000.,10000.]:
                        tail = ell(K,p)
                        weight = (s-tail)/(ell(k,p)-tail)
                        assert -1e-12 <= weight <= 1+1e-12
                        weight = min(1.,max(0.,weight))
                        c = weight**(1/p)
                        assert abs(weight*ell(k,p)+(1-weight)*tail-s)<1e-11
                        if direction == 'lower':
                            value = max(c-eta,0.)**p*ell(k+e,p)+(1-weight)*tail
                            gap = value-endpoint
                        else:
                            value = (c+eta)**p*ell(max(k-e,0.),p)+(1-weight)*tail
                            gap = endpoint-value
                        assert gap >= -1e-10, (p,s,e,eta,direction,gap)
                        gaps.append(gap)
                    assert gaps[-1] <= gaps[0]+1e-10
                    witnesses[direction] = gaps
                rows.append(dict(p=p,s=s,e=e,eta=eta,bounds=[lower,upper],
                                 optimizing_k=[kl,ku],witness_gaps=witnesses))

matrices = []
for p in [4/3,1.5,2.,3.,4.]:
    raw_x = [1.,8.] if p==4/3 else ([1.,4.] if p==1.5 else [1.,2.])
    targets = [grad(x,p) for x in raw_x]
    for seed in range(4):
        A = [[.25+seed/4,-.5+seed/8],[-.75+seed/8,.5]]
        A.append([targets[j]-A[0][j]-A[1][j] for j in range(2)])
        rv = [1+sum(a*x for a,x in zip(row,raw_x)) for row in A]
        scale = sum(abs(x)**p for x in rv)**(1/p)
        v, x = [z/scale for z in rv], [z/scale for z in raw_x]
        s = (3+sum(abs(z)**p for z in raw_x))/scale**p
        e, eta = .25+.25*seed, .05+.025*seed
        N = [row[:] for row in A]
        N[seed%3][seed%2] += e
        w = v[:]
        w[(seed+1)%3] += eta*(-1 if seed%2 else 1)
        dl,du,sweeps = solve(N,w,x,p)
        lower,upper,*_ = bounds(s,p,e,eta)
        assert lower <= dl+1e-10 and du <= upper+1e-10
        matrices.append(dict(p=p,seed=seed,e=e,eta=eta,old=s,
                             bounds=[lower,upper],primal_dual=[dl,du],sweeps=sweeps))

example = bounds(.1,2.,1.,.05)
result = dict(status='PASS',classification='DEVELOPMENT; floating finite checks',
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              dependency_path='v3/discovery/s15/norm_probe.py',
              dependency_sha256=hashlib.sha256(dependency.read_bytes()).hexdigest(),
              elapsed_ns=perf_counter_ns()-started, parameter_cases=len(rows),
              scalar_grid_inequalities=grid_checks, nonsymmetric_cases=len(matrices),
              example_s01_e1_eta005=list(example[:4]),
              maximum_primal_dual_gap=max(r['primal_dual'][1]-r['primal_dual'][0] for r in matrices),
              rows=rows, matrices=matrices)
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('rows','matrices')},indent=2))
