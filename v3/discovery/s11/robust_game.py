"""DEVELOPMENT minimax query/flip synthesis; Codex (GPT-6).

An ordinary matrix LP proposes mixtures. Two exact oracles certify their gap.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import random
import time
import numpy as np
from scipy.optimize import linprog

from query_flip import compact_plan, source
from robust_flip import summarize_policy, point_source, policy_value, regret_oracle


def distribution(raw):
    values=[max(F(0),F(float(x)).limit_denominator(1000000)) for x in raw]
    total=sum(values,F(0))
    assert total>0
    return [x/total for x in values]


def matrix_game(matrix):
    nr,nc=len(matrix),len(matrix[0])
    M=np.array([[float(x) for x in row] for row in matrix])
    A=np.concatenate((M.T,-np.ones((nc,1))),axis=1)
    result=linprog([0]*nr+[1],A_ub=A,b_ub=[0]*nc,A_eq=[[1]*nr+[0]],b_eq=[1],bounds=[(0,None)]*nr+[(None,None)],method='highs')
    assert result.success,result.message
    raw_alpha=list(map(float,result.x[:nr]))
    raw_beta=list(map(float,-result.ineqlin.marginals))
    return distribution(raw_alpha),distribution(raw_beta),{'alpha_raw':raw_alpha,'beta_raw':raw_beta,'numeric_value':result.fun}


def policy_key(rows):
    return tuple((fee,tuple(coeff)) for fee,coeff in rows)


def run(src,w,f,q,H,box,cap=40,tolerance=F(1,100000)):
    m,r=src['m'],src['r']
    midpoint=[[(lo+hi)/2 for lo,hi in row] for row in box]
    policies=[];pkeys=set();scenarios=[];skeys=set();history=[]
    def make_policy(mu):
        planned=compact_plan(point_source(src,mu),w,f,q,H)
        rows=summarize_policy(src,planned[4],f,q,H)
        return planned[0],{'rows':rows,'plan':planned[2]}
    def add_policy(pol):
        key=policy_key(pol['rows'])
        if key in pkeys:return False
        pkeys.add(key);policies.append(pol);return True
    def add_scenario(mu):
        key=tuple(tuple(row) for row in mu)
        if key in skeys:return False
        skeys.add(key)
        opt,pol=make_policy(mu)
        scenarios.append({'means':mu,'optimum':opt})
        return True
    nominal_value,nominal=make_policy(midpoint)
    add_policy(nominal)
    zero={'rows':[(F(0),(0,)*m) for _ in src['cells']],'plan':{'?'*r+':'+str(H):{'value':'0','action':['terminal_0']}}}
    add_policy(zero)
    add_scenario(midpoint)
    add_scenario([[lo for lo,hi in row] for row in box])
    add_scenario([[hi for lo,hi in row] for row in box])
    nominal_regret=regret_oracle(src,nominal['rows'],w,f,q,H,box)[0]
    zero_regret=regret_oracle(src,zero['rows'],w,f,q,H,box)[0]
    status='iteration_cap'
    start=time.perf_counter_ns()
    for iteration in range(cap):
        matrix=[[policy_value(src,pol['rows'],w,sc['means'])-sc['optimum'] for sc in scenarios] for pol in policies]
        alpha,beta,proposal=matrix_game(matrix)
        mixed=[]
        for z in range(len(src['cells'])):
            fee=sum((a*pol['rows'][z][0] for a,pol in zip(alpha,policies)),F(0))
            coeff=tuple(sum((a*pol['rows'][z][1][i] for a,pol in zip(alpha,policies)),F(0)) for i in range(m))
            mixed.append((fee,coeff))
        U,_,worst,_,ucount=regret_oracle(src,mixed,w,f,q,H,box)
        worst_opt,_=make_policy(worst)
        assert policy_value(src,mixed,w,worst)-worst_opt==U
        average=[[sum((b*sc['means'][z][i] for b,sc in zip(beta,scenarios)),F(0)) for i in range(m-r)] for z in range(len(src['cells']))]
        best,responding_policy=make_policy(average)
        L=best-sum((b*sc['optimum'] for b,sc in zip(beta,scenarios)),F(0))
        L=max(F(0),L)
        assert L<=U,(L,U)
        history.append({'iteration':iteration,'policies':len(policies),'scenarios':len(scenarios),
                        'upper':str(U),'lower':str(L),'gap':str(U-L),
                        'alpha':list(map(str,alpha)),'beta':list(map(str,beta)),
                        'lp_proposal':proposal,'oracle_work':ucount,
                        'worst_means':[[str(x) for x in row] for row in worst]})
        if U-L<=tolerance:
            status='certified_gap';break
        newp=add_policy(responding_policy)
        news=add_scenario(worst)
        if not newp and not news:
            status='stalled_existing_responses';break
    # The last alpha/beta refer to the bank lengths recorded in the last row.
    return {'status':status,'nominal_regret':str(nominal_regret),'zero_regret':str(zero_regret),
            'history':history,'elapsed_ns':time.perf_counter_ns()-start,
            'policies':[{'rows':[{'fee':str(fee),'coefficients':list(map(str,coeff))} for fee,coeff in pol['rows']],'plan':pol['plan']} for pol in policies],
            'scenarios':[{'means':[[str(x) for x in row] for row in sc['means']],'optimum':str(sc['optimum'])} for sc in scenarios]}


def case(index):
    m,r,H=[(1,0,0),(3,1,2),(5,2,3),(31,3,5)][index]
    src=source(m,r,1400+index)
    rng=random.Random(1500+index)
    w=tuple(F(rng.choice((-2,-1,1,2))) for _ in range(m))
    f=tuple(F(rng.randrange(1,5),4) for _ in range(m))
    q=(F(1,8),)*r
    box=[[(max(F(-1),v/p-F(1,2)),min(F(1),v/p+F(1,2))) for v in row] for p,row in zip(src['mass'],src['moments'])]
    if index==0:
        w=(F(1),);box=[[(F(-1),F(1))]]
    result=run(src,w,f,q,H,box)
    if index==0:
        assert result['history'][-1]['upper']==result['history'][-1]['lower']=='1/2'
    return {'case':index,'m':m,'r':r,'H':H,'mass':list(map(str,src['mass'])),
            'weights':list(map(str,w)),'flip_fee':list(map(str,f)),'query_fee':list(map(str,q)),
            'box':[[[str(lo),str(hi)] for lo,hi in row] for row in box],**result,
            'scope':'Expected minimax regret over privately randomized admissible policies; known masses and valid rectangular conditional mean source. No acquisition bill or broad novelty claim.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case)
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['dependencies']={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('query_flip.py','robust_flip.py')}
    with args.out.open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    last=result['history'][-1]
    print(json.dumps({k:result[k] for k in ('case','m','r','H','status','nominal_regret','zero_regret','elapsed_ns')}|{k:last[k] for k in ('iteration','policies','scenarios','upper','lower','gap')}))


if __name__=='__main__':main()
