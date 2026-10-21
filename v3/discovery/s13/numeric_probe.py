"""Finite exact screen of joint_edit_gap.md; expected under30 seconds."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent


def solve(a,b):
    n=len(a)
    x=[list(map(F,row))+[F(v)] for row,v in zip(a,b)]
    for k in range(n):
        pivot=next(i for i in range(k,n) if x[i][k])
        x[k],x[pivot]=x[pivot],x[k]
        d=x[k][k]
        x[k]=[v/d for v in x[k]]
        for i in range(n):
            if i!=k:
                d=x[i][k]
                x[i]=[v-d*w for v,w in zip(x[i],x[k])]
    return [row[-1] for row in x]


def inverse(a):
    n=len(a)
    cols=[solve(a,[int(i==j) for i in range(n)]) for j in range(n)]
    return [list(row) for row in zip(*cols)]


def positive(a):
    a=[list(map(F,row)) for row in a]
    n=len(a)
    assert all(a[i][j]==a[j][i] for i in range(n) for j in range(n))
    for k in range(n):
        assert a[k][k]>0
        for i in range(k+1,n):
            for j in range(k+1,n):
                a[i][j]-=a[i][k]*a[k][j]/a[k][k]


def matrices(r,sign):
    v=[[F(2 if i==j else 0) for j in range(r)] for i in range(r)]
    for i in range(r):
        j=(i+1)%r
        v[i][j]=v[j][i]=F(sign if i==r-1 else 1,2)
    big=[[F(10)]+[F(i==0) for i in range(r)]]
    big += [[F(i==0)]+v[i] for i in range(r)]
    positive(v)
    positive(big)
    a=inverse(big)
    positive(a)
    return v,a


def main():
    began=time.perf_counter_ns()
    counts=dict(panels=0,edit_vectors=0,proper_equalities=0,full_differences=0,
                direct_solves=0,port_solves=0)
    examples=[]
    for r in range(3,7):
        models=[matrices(r,s) for s in (1,-1)]
        for strengths in product((0,1,2),repeat=r):
            values=[]
            for v,a in models:
                edited=[row[:] for row in a]
                for i,t in enumerate(strengths):
                    edited[i+1][i+1]+=t
                y=solve(edited,[1]+[0]*r)[0]
                counts['direct_solves']+=1
                active=[i for i,t in enumerate(strengths) if t]
                if active:
                    port=[[v[i][j]+(F(1,strengths[i]) if i==j else 0)
                           for j in active] for i in active]
                    g=[int(i==0) for i in active]
                    d=sum(F(x)*z for x,z in zip(g,solve(port,g)))
                    counts['port_solves']+=1
                else:
                    d=F(0)
                assert y==10-d
                values.append(y)
            counts['edit_vectors']+=1
            if len(active)<r:
                assert values[0]==values[1]
                counts['proper_equalities']+=1
            else:
                assert values[0]!=values[1]
                counts['full_differences']+=1
            if all(t==1 for t in strengths):
                examples.append(dict(r=r,plus=str(values[0]),minus=str(values[1])))
        counts['panels']+=1
    assert examples[0]['plus']=='193/20'
    assert examples[0]['minus']=='135/14'
    out=dict(status='PASS',contributor='Codex (GPT-6)',counts=counts,examples=examples,
             elapsed_ns=time.perf_counter_ns()-began,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scope='exact finite development; no performance or independent confirmation claim')
    (HERE/'numeric_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':
    main()
