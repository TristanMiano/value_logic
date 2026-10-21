"""Exact finite matrix-edit screen, no physical measurement-cost claim."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
from math import isqrt
import hashlib
import importlib.util
import json
import random
import time

HERE=Path(__file__).resolve().parent
DEP=HERE/'numeric_probe.py'
spec=importlib.util.spec_from_file_location('matrix_helpers',DEP)
H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)
RNG=random.Random(202610212)


def root(q):
    a,b=isqrt(q.numerator),isqrt(q.denominator)
    assert a*a==q.numerator and b*b==q.denominator
    return F(a,b)


def reduce(v,g,d):
    active=[i for i,x in enumerate(d) if x]
    if not active:return F(0)
    mat=[[v[i][j]+(1/d[i] if i==j else 0) for j in active] for i in active]
    z=H.solve(mat,[g[i] for i in active])
    return sum(g[i]*x for i,x in zip(active,z))


def main():
    began=time.perf_counter_ns()
    counts=dict(recovery_panels=0,singleton_values=0,pair_values=0,
                joint_predictions=0,m_matrix_panels=0,omission_checks=0,noise_pairs=0)
    for r in range(2,6):
        for _ in range(5):
            v=[[F(0) for j in range(r)] for i in range(r)]
            for i,j in combinations(range(r),2):v[i][j]=v[j][i]=F(RNG.randrange(-2,3))
            for i in range(r):v[i][i]=2+sum(abs(x) for x in v[i])
            g=[F(RNG.choice((-1,1))*RNG.randrange(1,4)) for i in range(r)]
            y0=1+sum(a*b for a,b in zip(g,H.solve(v,g)))
            big=[[y0]+g]+[[g[i]]+v[i] for i in range(r)]
            H.positive(big);a=H.inverse(big)
            def measure(d):
                edited=[row[:] for row in a]
                for i,t in enumerate(d):edited[i+1][i+1]+=t
                return y0-H.solve(edited,[1]+[0]*r)[0]
            recovered=[[F(0) for j in range(r)] for i in range(r)]
            gg=[]
            for i in range(r):
                ds=[]
                for t in (F(1),F(2)):
                    d=[F(0)]*r;d[i]=t;ds.append(measure(d))
                inva=2*(1/ds[0]-1/ds[1]);aa=1/inva
                bb=aa/ds[0]-1
                assert aa==g[i]**2 and bb==v[i][i]
                gg.append(root(aa));recovered[i][i]=bb
                counts['singleton_values']+=2
            for i,j in combinations(range(r),2):
                vi,vj=recovered[i][i],recovered[j][j]
                gi,gj=gg[i],gg[j]
                t=min(gi/gj,gj/gi)/(2*(vi+vj))
                d=[F(0)]*r;d[i]=d[j]=t
                obs=measure(d)
                qa=obs;qb=-2*gi*gj
                qc=(gi**2*(1+t*vj)+gj**2*(1+t*vi))/t-obs*(1+t*vi)*(1+t*vj)/t**2
                disc=root(qb*qb-4*qa*qc)
                roots={(-qb+disc)/(2*qa),(-qb-disc)/(2*qa)}
                admissible=[u for u in roots if u*u<vi*vj]
                assert len(admissible)==1
                recovered[i][j]=recovered[j][i]=admissible[0]
                assert admissible[0]==v[i][j]*(1 if g[i]*g[j]>0 else -1)
                counts['pair_values']+=1
            for d in product((F(0),F(1),F(3)),repeat=r):
                assert reduce(recovered,gg,d)==measure(d)
                counts['joint_predictions']+=1
            counts['recovery_panels']+=1
    for n in range(2,6):
        for _ in range(4):
            a=[[F(0) for j in range(n)] for i in range(n)]
            for i,j in combinations(range(n),2):a[i][j]=a[j][i]=-F(RNG.randrange(4))
            for i in range(n):a[i][i]=RNG.randrange(1,4)+sum(abs(x) for x in a[i])
            b=[F(RNG.randrange(4)) for _ in range(n)]
            H.positive(a)
            y0=sum(x*z for x,z in zip(b,H.solve(a,b)))
            values={}
            for d in product((F(0),F(1),F(2)),repeat=n):
                edited=[row[:] for row in a]
                for i,t in enumerate(d):edited[i][i]+=t
                values[d]=y0-sum(x*z for x,z in zip(b,H.solve(edited,b)))
            for d,f in values.items():
                for mask in range(1<<n):
                    kept=tuple(F(0) if mask>>i&1 else d[i] for i in range(n))
                    bound=sum(values[tuple(d[i] if j==i else F(0) for j in range(n))]
                              for i in range(n) if mask>>i&1)
                    assert 0<=f-values[kept]<=bound
                    counts['omission_checks']+=1
            counts['m_matrix_panels']+=1
    v=[[F(2),F(1,2)],[F(1,2),F(2)]];g=[F(1),F(0)]
    assert reduce(v,g,[F(1),F(1)])-reduce(v,g,[F(1),F(0)])==F(1,105)
    gaps=[]
    for eps in (F(1,10),F(1,100),F(1,1000),F(1,10000)):
        matrices=[];g=[F(1),eps,eps]
        for sign in (1,-1):
            v=[[F(2) if i==j else F(1,2) for j in range(3)] for i in range(3)]
            v[1][2]=v[2][1]=F(sign,2)
            H.positive([[F(10)]+g]+[[g[i]]+v[i] for i in range(3)])
            matrices.append(v)
        for t in map(F,(1,2,10,100)):
            pair=abs(reduce(matrices[0],g,[F(0),t,t])-reduce(matrices[1],g,[F(0),t,t]))
            assert pair<=F(8,15)*eps**2
            counts['noise_pairs']+=1
        joint=abs(reduce(matrices[0],g,[F(1)]*3)-reduce(matrices[1],g,[F(1)]*3))
        if eps<=F(1,1000):assert joint>F(1,280)
        gaps.append(dict(epsilon=str(eps),pair_upper=str(F(8,15)*eps**2),joint_gap=str(joint)))
    out=dict(status='PASS',contributor='Codex (GPT-6)',seed=202610212,
             counts=counts,noise_examples=gaps,elapsed_ns=time.perf_counter_ns()-began,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             dependency_sha256={DEP.name:hashlib.sha256(DEP.read_bytes()).hexdigest()},
             scope='Exposed finite exact algebra; no independent confirmation or physical saving')
    (HERE/'ports_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
