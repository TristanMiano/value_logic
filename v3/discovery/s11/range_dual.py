"""DEVELOPMENT dual range tradeoff, Codex (GPT-6). Frozen input certificates."""
from pathlib import Path
from fractions import Fraction as F
import argparse
import hashlib
import json
import time
import math
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def optimize(data,eta,cap=None):
    p=[[F(x) for x in row] for row in data['marginals']]
    fees=list(map(F,data['fees']))
    C=F(data['fallback'])
    n,Q,K=data['n'],data['Q'],len(p[0])-1
    hids={};lids={};lowids={};upids={};bounds=[]
    def add(bound=(None,None)):
        bounds.append(bound)
        return len(bounds)-1
    states=[list(range(min(Q,i*K)+1)) for i in range(n+1)]
    for i in range(n):
        for s in states[i]:
            hids[i,s]=add()
    for i in range(n):
        for x in range(K+1):
            lids[i,x]=add((0,0) if x==0 else (None,None))
        lowids[i]=add()
        upids[i]=add()
    objective=[F(0)]*len(bounds)
    model={hids[0,0]:F(1)}
    for i in range(n):
        for x in range(K+1):
            model[lids[i,x]]=p[i][x]
    if cap is None:
        for j,v in model.items():
            objective[j]=v
    for i in range(n):
        objective[lowids[i]]=-eta
        objective[upids[i]]=eta
    rr,cc,vv,b=[],[],[],[]
    def constraint(row,rhs):
        idx=len(b)
        b.append(rhs)
        for j,v in row.items():
            rr.append(idx);cc.append(j);vv.append(float(v))
    for i in range(n):
        for s in states[i]:
            for x in range(K+1):
                t=min(Q,s+x)
                row={hids[i,s]:-1,lids[i,x]:-1}
                rhs=-fees[i]*int(s<Q)
                if i+1<n:
                    row[hids[i+1,t]]=1
                else:
                    rhs-=C*int(t<Q)
                constraint(row,rhs)
        for x in range(K+1):
            constraint({lids[i,x]:1,upids[i]:-1},0)
            constraint({lowids[i]:1,lids[i,x]:-1},0)
    if cap is not None:
        constraint(model,cap)
    A=coo_matrix((vv,(rr,cc)),shape=(len(b),len(bounds))).tocsr()
    start=time.perf_counter_ns()
    result=linprog(np.array(list(map(float,objective))),A_ub=A,b_ub=np.array(list(map(float,b))),bounds=bounds,method='highs')
    elapsed=time.perf_counter_ns()-start
    assert result.success,result.message
    prices=[[F(float(result.x[lids[i,x]])).limit_denominator(1000000) for x in range(K+1)] for i in range(n)]
    h=[{} for _ in range(n+1)]
    h[n]={s:C*int(s<Q) for s in states[n]}
    for i in reversed(range(n)):
        h[i]={s:max(fees[i]*int(s<Q)+h[i+1][min(Q,s+x)]-prices[i][x] for x in range(K+1)) for s in states[i]}
    checks=0
    for i in range(n):
        for s in states[i]:
            for x in range(K+1):
                assert h[i][s]+prices[i][x]>=fees[i]*int(s<Q)+h[i+1][min(Q,s+x)]
                checks+=1
    U=h[0][0]+sum((p[i][x]*prices[i][x] for i in range(n) for x in range(K+1)),F(0))
    ranges=[max(row)-min(row) for row in prices]
    R=sum(ranges,F(0))
    average_fee=sum((r*c for r,c in zip(ranges,fees)),F(0))/R if R else F(0)
    margin=C-U
    N=math.ceil(float(2*R*R/(margin*margin))*math.log(20)) if margin>0 and R else None
    return {'eta':str(eta),'sharp_cap':None if cap is None else str(cap),'cap_met_exactly':cap is None or U<=cap,
            'upper':str(U),'range':str(R),'penalized':str(U+eta*R),'positive_ranges':sum(x>0 for x in ranges),
            'expected_sample_fee':str(average_fee),'fixed_N_half_margin':N,
            'predicted_sample_fee':None if N is None else str(N*average_fee),
            'solver_ns':elapsed,'arc_checks':checks,'lp_variables':len(bounds),'lp_constraints':len(b),
            'prices':[[str(x) for x in row] for row in prices],
            'potential':[{str(s):str(x) for s,x in row.items()} for row in h]}


def case(index):
    root=Path(__file__).resolve().parent
    relative=['if01/c07a0.json','if01/c10a0.json','if02/c13_upper_only.json'][index]
    path=root/relative
    data=json.loads(path.read_text(encoding='utf-8'))
    cert=data.get('compact',data.get('proposal'))
    cap=F(cert['upper'])
    rows=[optimize(data,F(1),cap)]
    rows += [optimize(data,eta) for eta in (F(0),F(1,100),F(1,20),F(1,10),F(1,4),F(1,2))]
    return {'case':index,'source':relative,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'n':data['n'],'fallback':data['fallback'],'rows':rows,
            'scope':'Obtained exact upper certificates, not an independently verified optimal regularization frontier or an executed calibration trial.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case)
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**result,'rows':[{k:v for k,v in row.items() if k not in ('prices','potential')} for row in result['rows']]}))


if __name__=='__main__':main()
