"""Exact small spectral and policy checks. Not independent confirmation."""
from fractions import Fraction as F
from itertools import combinations,product
from math import comb
from pathlib import Path
import hashlib,json,random,sys,time
from flip_values import advise,cost,regret


def walsh(v):
    a=list(v);step=1
    while step<len(a):
        for start in range(0,len(a),step*2):
            for j in range(start,start+step):
                u,v=a[j],a[j+step];a[j],a[j+step]=u+v,u-v
        step*=2
    return [F(x,len(a)) for x in a]


def plans(m,H):return [None]+[J for n in range(H+1) for J in combinations(range(m),n)]


def main(out):
    assert not out.exists();start=time.perf_counter_ns();spectra=[];rng=random.Random(11512)
    for m in range(1,12,2):
        S=[m-2*x.bit_count() for x in range(1<<m)]
        absolute=walsh([abs(s) for s in S]);r0=walsh([max(0,-s) for s in S]);r1=walsh([max(0,s) for s in S])
        support={i for i in range(1<<m) if r0[i] or r1[i]}|{0};n=(m-1)//2;C=F(comb(2*n,n),1<<(2*n))
        for mask,v in enumerate(absolute):
            degree=mask.bit_count()
            expected=F(0) if degree%2 else (m*C if degree==0 else C*((-1)**(degree//2-1))*F(comb(n,degree//2-1),comb(2*n,degree-2)))
            assert v==expected
        assert len(support)==(1<<(m-1))+m
        spectra.append({'variables':m,'states':1<<m,'reference_dimension':m+1,'regret_dimension':len(support),
                        'absolute_coefficients_by_degree':{str(k):str(absolute[(1<<k)-1]) for k in range(m+1)}})
    cases=[];corner_pairs=policy_checks=0
    for case in range(72):
        m=rng.randrange(1,7);H=rng.randrange(m+1);menu=plans(m,H)
        prices=tuple(F(rng.randrange(0,9),4) for _ in range(m))
        counts=[rng.randrange(1,10) for _ in range(1<<m)];total=sum(counts)
        means=tuple(sum(F(w,total)*(1 if not x&(1<<i) else -1) for x,w in enumerate(counts)) for i in range(m))
        J=advise(means,prices,H);best=min(cost(means,prices,K) for K in menu)
        assert cost(means,prices,J)==best;policy_checks+=1
        lower=[];upper=[]
        for _ in range(m):
            a,b=sorted((rng.randrange(-4,5),rng.randrange(-4,5)));lower.append(F(a,4));upper.append(F(b,4))
        selected=list(dict.fromkeys([None,(),J,rng.choice(menu)]));finite={K:F(0) for K in selected}
        for corner in product(*zip(lower,upper)):
            costs={K:cost(corner,prices,K) for K in menu};minimum=min(costs.values());corner_pairs+=len(menu)
            for K in selected:finite[K]=max(finite[K],costs[K]-minimum)
        witnesses=[]
        for K in selected:
            R,alternative,corner=regret(lower,upper,prices,H,K)
            assert R==finite[K]
            assert cost(corner,prices,K)-cost(corner,prices,alternative)==R
            witnesses.append({'plan':K,'regret':str(R),'competitor':alternative,'means':list(map(str,corner))})
        cases.append({'variables':m,'horizon':H,'prices':list(map(str,prices)),'prior_counts':counts,'means':list(map(str,means)),
                      'advised_plan':J,'optimal_cost':str(best),'lower':list(map(str,lower)),'upper':list(map(str,upper)),'regret_witnesses':witnesses})
    result={'status':'complete','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','seed':11512,'python':sys.version,
            'sources':{p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ('flip_values.py','baseline_probe.py')},
            'spectra':spectra,'cases':cases,'policy_checks':policy_checks,'corner_plan_pairs':corner_pairs,'elapsed_ns':time.perf_counter_ns()-start}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k] for k in ('status','spectra','policy_checks','corner_plan_pairs','elapsed_ns')}))


if __name__=='__main__':main(Path(sys.argv[1]))
