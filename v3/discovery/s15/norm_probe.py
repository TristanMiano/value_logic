"""Small floating developmental screen; not an outward or independent proof."""
from pathlib import Path
import hashlib, json, math, time

HERE=Path(__file__).resolve().parent
OUT=HERE/'norm_probe.json'
assert not OUT.exists(), 'Preserve outputs; use an isolated replay directory.'
start=time.perf_counter_ns()

def ell(t,p):
    q=p/(p-1)
    return (1+t**q)**(1-p)

def params(p,e):
    q=p/(p-1)
    def f(t):return t**(-(q-1))-(t+e)**(-(q-1))-e
    lo,hi=1e-16,1.
    while f(hi)>0:hi*=2
    for _ in range(100):
        mid=(lo+hi)/2
        if f(mid)>0:lo=mid
        else:hi=mid
    t=(lo+hi)/2
    ratio=((1+(t+e)**q)/(1+t**q))**(p-1)
    assert abs(ratio-(t+e)/t)<2e-12*ratio
    return t,ratio,ell(t,p),ell(t+e,p)

def envelope(s,p,e):
    t,r,a,b=params(p,e);q=p/(p-1)
    inv=max(0,s**(-1/(p-1))-1)**(1/q)
    lower=s/r if s<=a else ell(inv+e,p)
    upper=s*r if s<=b else ell(max(inv-e,0),p)
    return lower,upper

def grad(x,p):return math.copysign(abs(x)**(p-1),x) if x else 0.

def objective(A,v,x,p):
    residual=[b-sum(a*z for a,z in zip(row,x)) for row,b in zip(A,v)]
    return sum(abs(z)**p for z in residual)+sum(abs(z)**p for z in x)

def certificate(A,v,x,p):
    residual=[b-sum(a*z for a,z in zip(row,x)) for row,b in zip(A,v)]
    w=[grad(z,p) for z in residual];q=p/(p-1)
    adj=[sum(row[j]*z for row,z in zip(A,w)) for j in range(len(x))]
    denominator=sum(abs(z)**q for z in w+adj)
    dual=abs(sum(a*b for a,b in zip(w,v)))**p/denominator**(p-1)
    primal=objective(A,v,x,p)
    return dual,primal

def solve(A,v,x,p):
    x=x[:]
    for sweep in range(2000):
        for j in range(len(x)):
            residual=[b-sum(row[k]*x[k] for k in range(len(x)) if k!=j)
                      for row,b in zip(A,v)]
            def derivative(z):
                return grad(z,p)-sum(row[j]*grad(r-row[j]*z,p)
                                     for row,r in zip(A,residual))
            lo,hi=-1.,1.
            while derivative(lo)>0:lo*=2
            while derivative(hi)<0:hi*=2
            for _ in range(60):
                mid=(lo+hi)/2
                if derivative(mid)>0:hi=mid
                else:lo=mid
            x[j]=(lo+hi)/2
        lower,upper=certificate(A,v,x,p)
        if upper-lower<5e-11:return lower,upper,sweep+1
    raise AssertionError(('Primal-dual convergence budget exceeded',p,lower,upper))

scalar_checks=0;mixture_checks=0;rows=[];mixtures=[]
for p in (4/3,1.5,2.,3.,4.):
    for e in (.25,1.,2.):
        t,r,a,b=params(p,e)
        for factor in (1.,1.25,2.,4.):
            old=ell(t/factor,p);new=ell(t/factor+e,p)
            l,u=envelope(old,p,e)
            assert abs(new-l)<2e-12
            l2,u2=envelope(new,p,e)
            assert abs(old-u2)<2e-12
            scalar_checks+=2
        s=a/2;gaps=[]
        for K in (20.,200.,2000.):
            old_tail=ell(K,p)
            if old_tail>=s:continue
            weight=(s-old_tail)/(a-old_tail)
            new=weight*b+(1-weight)*old_tail
            assert new>=s/r-1e-12
            assert abs(weight*a+(1-weight)*old_tail-s)<1e-12
            gaps.append(new-s/r);mixture_checks+=1
        assert all(y<x for x,y in zip(gaps,gaps[1:]))
        mixtures.append(dict(p=p,e=e,t_star=t,ratio=r,lower_join=a,
                             upper_join=b,limiting_gaps=gaps))
    raw_x=[1.,8.] if p==4/3 else ([1.,4.] if p==1.5 else [1.,2.])
    targets=[grad(z,p) for z in raw_x]
    for seed in range(4):
        A=[[.25+seed/4, -.5+seed/8],[-.75+seed/8, .5]]
        A.append([targets[j]-A[0][j]-A[1][j] for j in range(2)])
        raw_v=[1+sum(a*x for a,x in zip(row,raw_x)) for row in A]
        scale=sum(abs(z)**p for z in raw_v)**(1/p)
        v=[z/scale for z in raw_v];old_x=[z/scale for z in raw_x]
        old=(3+sum(abs(z)**p for z in raw_x))/scale**p
        dl,du=certificate(A,v,old_x,p)
        assert abs(dl-old)<2e-12 and abs(du-old)<2e-12
        e=.25+.25*seed;N=[row[:] for row in A]
        N[seed%3][seed%2]+=e # One-entry edit has induced l_p norm exactly e.
        lower,upper,sweeps=solve(N,v,old_x,p)
        l,u=envelope(old,p,e)
        assert l<=lower+1e-10 and upper<=u+1e-10,(p,seed,l,lower,upper,u)
        rows.append(dict(p=p,seed=seed,old_value=old,e=e,envelope=[l,u],
                         target_primal_dual=[lower,upper],sweeps=sweeps))

result=dict(status='PASS',classification='DEVELOPMENT; floating finite screen',
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            elapsed_ns=time.perf_counter_ns()-start,
            scalar_equalities=scalar_checks,diagonal_mixture_checks=mixture_checks,
            nonsymmetric_primal_dual_cases=len(rows),
            maximum_primal_dual_gap=max(x['target_primal_dual'][1]-x['target_primal_dual'][0] for x in rows),
            mixtures=mixtures,rows=rows)
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('rows','mixtures')},indent=2))
