"""DEVELOPMENT stopped-invoice coupling LP, Codex (GPT-6).

HiGHS proposes solutions. Exact rational checks establish certificate validity.
The mathematical flow is an adaptation of established marginal coupling LPs.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import random
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def rat(x):
    return F(float(x)).limit_denominator(1000000)


def solve_flow(p, fees, C, Q):
    n,K = len(p),len(p[0])-1
    assert n and Q>0 and all(sum(row)==1 for row in p)
    states = [list(range(min(Q,i*K)+1)) for i in range(n+1)]
    balance = {}
    marginal = {}
    rhs=[]
    for i in range(n):
        for s in states[i]:
            balance[i,s]=len(rhs)
            rhs.append(F(int(i==0 and s==0)))
    for i in range(n):
        for x in range(K+1):
            marginal[i,x]=len(rhs)
            rhs.append(p[i][x])
    arcs=[]
    columns=[]
    objective=[]
    rr,cc,vv=[],[],[]
    for i in range(n):
        for s in states[i]:
            for x in range(K+1):
                t=min(Q,s+x)
                arc=(i,s,x,t)
                col={balance[i,s]:1,marginal[i,x]:1}
                if i+1<n:
                    col[balance[i+1,t]]=-1
                j=len(arcs)
                arcs.append(arc)
                columns.append(col)
                objective.append(fees[i]*int(s<Q)+C*int(i==n-1 and t<Q))
                for row,val in col.items():
                    rr.append(row);cc.append(j);vv.append(val)
    A=coo_matrix((vv,(rr,cc)),shape=(len(rhs),len(arcs))).tocsr()
    start=time.perf_counter_ns()
    result=linprog(-np.array(list(map(float,objective))),A_eq=A,b_eq=np.array(list(map(float,rhs))),bounds=(0,None),method='highs')
    elapsed=time.perf_counter_ns()-start
    assert result.success,result.message
    flow=list(map(rat,result.x))
    checked=[F(0)]*len(rhs)
    for val,col in zip(flow,columns):
        for row,coef in col.items():
            checked[row]+=coef*val
    primal_valid=all(x>=0 for x in flow) and checked==rhs
    lower=sum((a*b for a,b in zip(objective,flow)),F(0)) if primal_valid else None
    prices=[[rat(-result.eqlin.marginals[marginal[i,x]]) for x in range(K+1)] for i in range(n)]
    potential=[{} for _ in range(n+1)]
    potential[n]={s:C*int(s<Q) for s in states[n]}
    for i in reversed(range(n)):
        potential[i]={s:max(fees[i]*int(s<Q)+potential[i+1][min(Q,s+x)]-prices[i][x] for x in range(K+1)) for s in states[i]}
    for i,s,x,t in arcs:
        assert potential[i][s]+prices[i][x]>=fees[i]*int(s<Q)+potential[i+1][t]
    upper=potential[0][0]+sum((p[i][x]*prices[i][x] for i in range(n) for x in range(K+1)),F(0))
    if primal_valid:
        assert lower<=upper
    return {'upper':str(upper),'lower':None if lower is None else str(lower),'exact':lower==upper,
            'primal_valid':primal_valid,'variables':len(arcs),'equations':len(rhs),'solver_ns':elapsed,
            'numeric_objective':-result.fun,'simplex_iterations':result.nit,
            'flow':[[i,s,x,str(v)] for (i,s,x,t),v in zip(arcs,flow) if v],
            'prices':[[str(v) for v in row] for row in prices],
            'potential':[{str(s):str(v) for s,v in row.items()} for row in potential]}


def bill(xs,fees,C,Q):
    s,total=0,F(0)
    for x,c in zip(xs,fees):
        if s<Q:
            total+=c
        s+=x
    return total+C*int(s<Q)


def full_law_lp(p,fees,C,Q):
    n,K=len(p),len(p[0])-1
    xs=list(product(range(K+1),repeat=n))
    A=np.array([[int(row[i]==x) for row in xs] for i in range(n) for x in range(K+1)])
    b=[v for row in p for v in row]
    costs=[bill(row,fees,C,Q) for row in xs]
    result=linprog(-np.array(list(map(float,costs))),A_eq=A,b_eq=np.array(list(map(float,b))),bounds=(0,None),method='highs')
    assert result.success,result.message
    weights=list(map(rat,result.x))
    assert all(w>=0 for w in weights)
    for i in range(n):
        for x in range(K+1):
            assert sum((w for w,row in zip(weights,xs) if row[i]==x),F(0))==p[i][x]
    value=sum((w*c for w,c in zip(weights,costs)),F(0))
    # The compact dual is an independent upper certificate for this full law.
    return {'value':str(value),'world_variables':len(xs),
            'witness':[[list(row),str(w)] for row,w in zip(xs,weights) if w]}


def case(index):
    n=3+index%4 if index<12 else (24 if index==12 else 80)
    rng=random.Random(1100+index)
    Q=2+index%max(2,n)
    fees=[F(rng.randrange(1,4)) for _ in range(n)]
    C=F(sum(fees))
    p=[]
    for i in range(n):
        raw=[rng.randrange(1,8) for _ in range(3)] if index%3 else [3,3,2]
        p.append([F(x,sum(raw)) for x in raw])
    start=time.perf_counter_ns()
    compact=solve_flow(p,fees,C,Q)
    assert compact['exact'],compact
    full=None
    if index<12:
        full=full_law_lp(p,fees,C,Q)
        assert full['value']==compact['upper']
    tails=[F(1)]
    if index<12:
        for k in range(1,n+1):
            tail=solve_flow(p[:k],[F(0)]*k,F(1),Q)
            assert tail['exact']
            tails.append(F(tail['upper']))
        separate=sum((c*u for c,u in zip(fees,tails)),F(0))+C*tails[-1]
        assert separate>=F(compact['upper'])
    else:
        separate=None
    return {'case':index,'n':n,'K':2,'Q':Q,'marginals':[[str(x) for x in row] for row in p],
            'fees':list(map(str,fees)),'fallback':str(C),'compact':compact,'full':full,
            'separate_prefix_bound':None if separate is None else str(separate),
            'separate_gap':None if separate is None else str(separate-F(compact['upper'])),
            'elapsed_ns':time.perf_counter_ns()-start,
            'scope':'Analytical stopped-invoice bound; no paid service or learning measurement.'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--case',type=int,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    assert not args.out.exists()
    result=case(args.case)
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':args.case,'n':result['n'],'Q':result['Q'],'bound':result['compact']['upper'],
                      'gap':result['separate_gap'],'variables':result['compact']['variables'],
                      'solver_ns':result['compact']['solver_ns']}))


if __name__=='__main__':
    main()
