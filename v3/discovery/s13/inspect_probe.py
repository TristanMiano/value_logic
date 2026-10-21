"""Small development screen; exact rational fees, no fitted performance claim."""
from pathlib import Path
from itertools import product
from collections import deque
from functools import lru_cache
from fractions import Fraction as F
import ast
import hashlib
import json
import random
import time

HERE=Path(__file__).resolve().parent
DEP=HERE/'edge_extension.py'
ns={'deque':deque}
tree=ast.parse(DEP.read_text(encoding='utf-8'))
exec(compile(ast.Module(body=[v for v in tree.body if isinstance(v,ast.ClassDef)
                             and v.name=='Flow'],type_ignores=[]),str(DEP),'exec'),ns)
Flow=ns['Flow']
RNG=random.Random(202610211)
COUNTS=dict(cuts=0,panels=0,certificate_checks=0,prediction_worlds=0,
            adaptive_panels=0,adaptive_strict=0,reoptimized_strict=0)


def valid(signs,edges,units):
    return all(signs[i]==0 or signs[j]==1 for i,j in edges) and all(signs[i]==b for i,b in units)


def solve(d,edges,units):
    n=len(d);s,t=2*n,2*n+1
    graph=Flow(t+1)
    inf=1+sum(sum(row) for row in d)
    for i,(d0,d1) in enumerate(d):
        graph.add(s,2*i,d0)
        graph.add(2*i+1,t,d1)
        graph.add(2*i+1,2*i,inf)
    for i,j in edges:graph.add(2*i,2*j+1,inf)
    for i,b in units:
        if b:graph.add(s,2*i+1,inf)
        else:graph.add(2*i,t,inf)
    cost,reach=graph.maxflow(s,t)
    COUNTS['cuts']+=1
    if cost>=inf:return None,None
    signs=tuple(0 if 2*i not in reach else 1 if 2*i+1 in reach else -1 for i in range(n))
    assert valid(signs,edges,units)
    assert cost==sum(d[i][b] for i,b in enumerate(signs) if b!=-1)
    return cost,signs


def plan(w,q,p,edges,units):
    d=[tuple(min(w[i][b],q[i]+(1-(p[i] if b else 1-p[i]))*w[i][b]) for b in (0,1))
       for i in range(len(w))]
    cost,signs=solve(d,edges,units)
    modes=tuple('none' if b==-1 else 'write' if d[i][b]==w[i][b] else 'query'
                for i,b in enumerate(signs))
    return cost,signs,modes,d


def execution(w,q,signs,modes,x,edges,units):
    Q=sum(q[i] for i,m in enumerate(modes) if m=='query')
    W=sum(w[i][signs[i]] for i,m in enumerate(modes) if m=='write')
    R=sum(w[i][signs[i]] for i,m in enumerate(modes) if m=='query' and x[i]!=signs[i])
    h=tuple(x[i] if modes[i]=='query' else -1 for i in range(len(w)))
    remaining,chosen=solve([tuple(0 if h[i]==b else w[i][b] for b in (0,1)) for i in range(len(w))],edges,units)
    final=tuple(x[i] if chosen[i]==-1 else chosen[i] for i in range(len(w)))
    assert valid(final,edges,units)
    return Q+W+R,Q+remaining


def adaptive(w,q,law,edges,units):
    n=len(w)
    @lru_cache(None)
    def value(h):
        selected=[(x,mass) for x,mass in law.items() if all(a==-1 or a==b for a,b in zip(h,x))]
        mass=sum(m for _,m in selected)
        best,_=solve([tuple(0 if h[i]==b else w[i][b] for b in (0,1)) for i in range(n)],edges,units)
        if mass==0:return best
        for i,a in enumerate(h):
            if a!=-1:continue
            c=q[i]
            for b in (0,1):
                part=sum(m for x,m in selected if x[i]==b)
                if part:c+=part/mass*value(h[:i]+(b,)+h[i+1:])
            best=min(best,c)
        return best
    return value((-1,)*n)


def panel(w,q,law,edges,units):
    n=len(w);worlds=list(product((0,1),repeat=n))
    p=[sum(m for x,m in law.items() if x[i]) for i in range(n)]
    cost,signs,modes,d=plan(w,q,p,edges,units)
    if cost is None:return
    certificates=[s for s in product((-1,0,1),repeat=n) if valid(s,edges,units)]
    assert cost==min(sum(d[i][b] for i,b in enumerate(s) if b!=-1) for s in certificates)
    COUNTS['certificate_checks']+=len(certificates)
    B,_=solve(w,edges,units)
    assert cost<=B
    direct=F(0);reopt=F(0)
    for x in worlds:
        c,r=execution(w,q,signs,modes,x,edges,units)
        assert r<=c and r<=2*B
        direct+=law.get(x,0)*c
        reopt+=law.get(x,0)*r
    assert direct==cost
    if reopt<direct:COUNTS['reoptimized_strict']+=1
    for y in RNG.sample(worlds,min(3,len(worlds))):
        pc,ps,pm,_=plan(w,q,list(y),edges,units)
        assert pc<=B
        for x in worlds:
            c,r=execution(w,q,ps,pm,x,edges,units)
            assert r<=c and r<=2*B
            if x==y:assert r==pc
            COUNTS['prediction_worlds']+=1
    if n<=4:
        optimum=adaptive(w,q,law,edges,units)
        assert optimum<=reopt<=direct
        COUNTS['adaptive_panels']+=1
        if optimum<reopt:COUNTS['adaptive_strict']+=1
    COUNTS['panels']+=1


def main():
    began=time.perf_counter_ns()
    for n in range(2,6):
        for case in range(8):
            edges=sorted({tuple(RNG.sample(range(n),2)) for _ in range(RNG.randrange(1,2*n))})
            units=[] if case%3 else [(RNG.randrange(n),RNG.randrange(2))]
            w=[(F(RNG.randrange(1,10)),F(RNG.randrange(1,10))) for _ in range(n)]
            q=[F(RNG.randrange(5)) for _ in range(n)]
            worlds=list(product((0,1),repeat=n))
            masses=[RNG.randrange(1,10) for _ in worlds]
            total=sum(masses)
            law={x:F(m,total) for x,m in zip(worlds,masses)}
            panel(w,q,law,edges,units)
    # A small independent case where buying a check only after another result helps.
    w=[(F(1),F(10)),(F(1),F(10)),(F(10),F(3,2))]
    q=[F(3,10),F(3,10),F(10)]
    law={(a,b,0):F(1,4) for a,b in product((0,1),repeat=2)}
    edges=[(0,2),(1,2)]
    pc,_,_,_=plan(w,q,[F(1,2),F(1,2),F(0)],edges,[])
    ac=adaptive(w,q,law,edges,[])
    assert pc==F(3,2) and ac==F(29,20)
    # Correlation can make the ratio unbounded as epsilon tends to zero.
    eps=F(1,100)
    w=[(F(1),F(1)),(F(1),F(1))];q=[eps,eps]
    law={(0,0):F(1,2),(1,1):F(1,2)}
    pc2,_,_,_=plan(w,q,[F(1,2)]*2,[(0,1)],[])
    ac2=adaptive(w,q,law,[(0,1)],[])
    assert pc2==F(51,100) and ac2==F(3,200)
    out=dict(status='PASS',contributor='Codex (GPT-6)',seed=202610211,
             counts=COUNTS,independent_gap={'fixed':str(pc),'adaptive':str(ac)},
             correlated_gap={'fixed':str(pc2),'adaptive':str(ac2),'ratio':str(pc2/ac2)},
             elapsed_ns=time.perf_counter_ns()-began,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             dependency_sha256={DEP.name:hashlib.sha256(DEP.read_bytes()).hexdigest()},
             scope='Finite rational identities and ordinary adaptive control; no empirical deployment claim')
    (HERE/'inspect_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
