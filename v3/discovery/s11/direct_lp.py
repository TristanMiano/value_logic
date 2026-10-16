"""DEVELOPMENT direct minimax query/flip LP; Codex (GPT-6).

Numerical advice is checked by exact feasible-policy and weak-duality bounds.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from query_flip import signs, matches, compact_plan
from robust_flip import point_source, policy_value, regret_oracle
from policy_flow import architecture, realize


def plus(target, source, multiplier=F(1)):
    for j,v in source.items():
        target[j]=target.get(j,F(0))+multiplier*v
        if not target[j]:del target[j]
    return target


def build(src,w,f,q,H,box):
    arch=architecture(src['m'],src['r'],H)
    states,ids,variables,options,flipids,Aeq,beq,Aub=arch
    n=len(variables);names=list(variables);bounds=[(F(0),F(1))]*n
    def new(name,lo,hi):
        j=len(names);names.append(name);bounds.append((F(lo),F(hi)));return j
    def convert(A):
        rows=[{} for _ in range(A.shape[0])]
        for i,j,v in zip(A.tocoo().row,A.tocoo().col,A.tocoo().data):
            assert j<n
            rows[int(i)][int(j)]=F(int(v))
        return rows
    eq=convert(Aeq);beq=list(map(F,beq));ub=convert(Aub);bub=[F(0)]*len(ub)
    def inequality(row,b=F(0)):
        ub.append(row);bub.append(F(b))
    cell_fee=[];cell_coeff=[]
    for z in src['cells']:
        fee={};coeff=[{} for _ in w]
        for h in states:
            if not matches(z,h):continue
            for i in range(src['m']):
                plus(coeff[i],{ids[h,'stop1',-1]:1,flipids[h][i]:-2})
                plus(fee,{flipids[h][i]:f[i]})
            for j in range(src['r']):
                if (h,'query',j) in ids:plus(fee,{ids[h,'query',j]:q[j]})
        cell_fee.append(fee);cell_coeff.append(coeff)
    ds={}
    for zidx,z in enumerate(src['cells']):
        for i,weight in enumerate(w):
            endpoints=(F(z[i]),) if i<src['r'] else tuple(sorted(set(box[zidx][i-src['r']])))
            for a in (-1,0,1):
                d=new(('support',zidx,i,a),-2*abs(weight),2*abs(weight));ds[zidx,i,a]=d
                for mu in endpoints:
                    row=plus({d:F(-1)},cell_coeff[zidx][i],weight*mu)
                    inequality(row,weight*a*mu)
    cap=H*max(tuple(f)+tuple(q)+(F(0),))+2*sum(map(abs,w),F(0))
    B={h:new(('adversary_value',h),-cap,cap) for h in states}
    for h in states:
        compatible=[t for t,z in enumerate(src['cells']) if matches(z,h)]
        mass=sum((src['mass'][t] for t in compatible),F(0))
        fee={}
        for t in compatible:plus(fee,cell_fee[t],src['mass'][t])
        W={(i,a):{ds[t,i,a]:src['mass'][t] for t in compatible if src['mass'][t]} for i in range(src['m']) for a in (-1,0,1)}
        zero=plus({B[h]:F(-1)},fee)
        for i in range(src['m']):plus(zero,W[i,0])
        inequality(zero)
        k=H-sum(v!=0 for v in h)
        threshold=new(('top_k_threshold',h),0,4*max(map(abs,w),default=F(0)))
        one=plus({B[h]:F(-1),threshold:F(k)},fee)
        for i in range(src['m']):
            excess=new(('top_k_excess',h,i),0,4*abs(w[i]))
            row=plus({excess:F(-1),threshold:F(-1)},W[i,-1])
            plus(row,W[i,1],F(-1));inequality(row,f[i]*mass)
            plus(one,W[i,1]);one[excess]=F(1)
        inequality(one)
        if k:
            for j in range(src['r']):
                if h[j]:continue
                children=[tuple(o if a==j else h[a] for a in range(src['r'])) for o in (-1,1)]
                inequality({B[h]:F(-1),B[children[0]]:F(1),B[children[1]]:F(1)},q[j]*mass)
    objective=[F(0)]*len(names);objective[B[(0,)*src['r']]]=F(1)
    return arch,eq,beq,ub,bub,bounds,objective,names


def sparse(rows,n):
    rr=[];cc=[];vv=[]
    for i,row in enumerate(rows):
        for j,v in row.items():rr.append(i);cc.append(j);vv.append(float(v))
    return coo_matrix((vv,(rr,cc)),shape=(len(rows),n)).tocsr()


def dual_bound(eq,beq,ub,bub,bounds,c,raw_lambda,raw_nu):
    lam=[min(F(0),F(float(v)).limit_denominator(1000000)) for v in raw_lambda]
    nu=[F(float(v)).limit_denominator(1000000) for v in raw_nu]
    residual=list(c)
    for row,v in zip(ub,lam):
        for j,a in row.items():residual[j]-=a*v
    for row,v in zip(eq,nu):
        for j,a in row.items():residual[j]-=a*v
    base=sum((v*b for v,b in zip(lam,bub)),F(0))+sum((v*b for v,b in zip(nu,beq)),F(0))
    correction=sum((min(a*lo,a*hi) for a,(lo,hi) in zip(residual,bounds)),F(0))
    return base+correction,{'lambda':list(map(str,lam)),'nu':list(map(str,nu)),
                            'box_infimum_correction':str(correction),'base':str(base),
                            'residual_l1':str(sum(map(abs,residual),F(0)))}


def case(index):
    root=Path(__file__).resolve().parent
    path=root/'rg01'/('c%02da0.json'%index)
    old=json.loads(path.read_text(encoding='utf-8'))
    m,r,H=old['m'],old['r'],old['H']
    src={'m':m,'r':r,'cells':signs(r),'mass':list(map(F,old['mass']))}
    w,f,q=(tuple(map(F,old[key])) for key in ('weights','flip_fee','query_fee'))
    box=[[(F(lo),F(hi)) for lo,hi in row] for row in old['box']]
    start=time.perf_counter_ns()
    arch,eq,beq,ub,bub,bounds,c,names=build(src,w,f,q,H,box)
    lp=linprog(list(map(float,c)),A_ub=sparse(ub,len(c)),b_ub=list(map(float,bub)),
               A_eq=sparse(eq,len(c)),b_eq=list(map(float,beq)),
               bounds=[(float(lo),float(hi)) for lo,hi in bounds],method='highs')
    assert lp.success,lp.message
    realization,rows,local=realize(src,f,q,H,lp.x,arch)
    U,action,worst,_,counts=regret_oracle(src,rows,w,f,q,H,box)
    assert U==policy_value(src,rows,w,worst)-compact_plan(point_source(src,worst),w,f,q,H)[0]
    lower,certificate=dual_bound(eq,beq,ub,bub,bounds,c,lp.ineqlin.marginals,lp.eqlin.marginals)
    L=max(F(0),lower);assert L<=U,(L,U)
    oldlower=max(F(v['lower']) for v in old['history'])
    oldupper=min(F(v['upper']) for v in old['history'])
    assert L<=oldupper and oldlower<=U,(L,U,oldlower,oldupper)
    return {'case':index,'input':path.relative_to(root).as_posix(),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'm':m,'r':r,'H':H,'variables':len(c),'equalities':len(eq),'inequalities':len(ub),
            'nonzeros':sum(map(len,eq))+sum(map(len,ub)),'numeric_value':float(lp.fun),
            'upper':str(U),'lower':str(L),'gap':str(U-L),'old_upper':str(oldupper),'old_lower':str(oldlower),
            'nominal_regret':old['nominal_regret'],'iterations':lp.nit,
            'raw_primal_advice':list(map(float,lp.x)),'raw_dual_advice':{'lambda':list(map(float,lp.ineqlin.marginals)),'nu':list(map(float,lp.eqlin.marginals))},
            'dual_certificate':certificate,'final_local_policy':local,'final_realization':list(map(str,realization)),
            'final_rows':[{'fee':str(fee),'coefficients':list(map(str,coeff))} for fee,coeff in rows],
            'worst_means':[[str(v) for v in row] for row in worst],'oracle_work':counts,
            'elapsed_ns':time.perf_counter_ns()-start,
            'scope':'Bounded-variable weak-duality lower and exact-oracle upper for repaired admissible policy. Development only.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case)
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['dependencies']={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('policy_flow.py','query_flip.py','robust_flip.py','robust_game.py','robust_game_grid.py')}
    with args.out.open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','m','variables','inequalities','nonzeros','numeric_value','lower','upper','gap','iterations','elapsed_ns')}))


if __name__=='__main__':main()
