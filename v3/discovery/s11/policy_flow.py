"""DEVELOPMENT compact randomized query/flip policy flow, Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack, csr_matrix
from query_flip import signs,matches,compact_plan
from robust_flip import point_source,policy_value,regret_oracle
from robust_game_grid import grid_distribution,DENOMINATOR


def architecture(m,r,H):
    states=sorted((h for h in product((-1,0,1),repeat=r) if sum(x!=0 for x in h)<=H),key=lambda h:(sum(x!=0 for x in h),h))
    ids={};variables=[];options={};flipids={}
    def new(key):
        ids[key]=len(variables);variables.append(key);return ids[key]
    for h in states:
        k=H-sum(x!=0 for x in h)
        options[h]=[new((h,'stop0',-1)),new((h,'stop1',-1))]
        if k:
            options[h]+=[new((h,'query',j)) for j in range(r) if h[j]==0]
        flipids[h]=[new((h,'flip',i)) for i in range(m)]
    size=len(variables)+1
    eq=[];rhs=[];ub=[]
    for h in states:
        row={idx:1 for idx in options[h]}
        for j in range(r):
            if h[j]:
                parent=tuple(0 if i==j else h[i] for i in range(r))
                row[ids[parent,'query',j]]=row.get(ids[parent,'query',j],0)-1
        eq.append(row);rhs.append(int(not any(h)))
        u=ids[h,'stop1',-1]
        for v in flipids[h]:ub.append({v:1,u:-1})
        ub.append({**{v:1 for v in flipids[h]},u:-(H-sum(x!=0 for x in h))})
    def sparse(rows):
        rr=[];cc=[];vv=[]
        for i,row in enumerate(rows):
            for j,x in row.items():rr.append(i);cc.append(j);vv.append(x)
        return coo_matrix((vv,(rr,cc)),shape=(len(rows),size)).tocsr()
    return states,ids,variables,options,flipids,sparse(eq),rhs,sparse(ub)


def source_cost(src,mu,w,f,q,arch):
    states,ids,variables,options,flipids,*_=arch
    result=[F(0)]*len(variables)
    for h in states:
        mass=F(0);moments=[F(0)]*src['m']
        for z,p,row in zip(src['cells'],src['mass'],mu):
            if matches(z,h):
                mass+=p
                for i,x in enumerate(z+tuple(row)):moments[i]+=p*x
        result[ids[h,'stop1',-1]]=sum((a*b for a,b in zip(w,moments)),F(0))
        for i,v in enumerate(flipids[h]):result[v]=f[i]*mass-2*w[i]*moments[i]
        for j in range(src['r']):
            key=h,'query',j
            if key in ids:result[ids[key]]=q[j]*mass
    return result


def realize(src,f,q,H,raw,arch):
    states,ids,variables,options,flipids,*_=arch
    x=[F(0)]*len(variables)
    local=[]
    for h in states:
        reach=F(1) if not any(h) else sum((x[ids[tuple(0 if i==j else h[i] for i in range(src['r'])),'query',j]] for j in range(src['r']) if h[j]),F(0))
        raw_choices=[max(0.,float(raw[j])) for j in options[h]]
        probs=grid_distribution(raw_choices) if sum(raw_choices)>1e-14 else [F(1)]+[F(0)]*(len(raw_choices)-1)
        for j,p in zip(options[h],probs):x[j]=reach*p
        raw_stop=max(0.,float(raw[ids[h,'stop1',-1]]))
        units=[int(min(1.,max(0.,float(raw[j])/raw_stop))*DENOMINATOR) if raw_stop>1e-14 else 0 for j in flipids[h]]
        k=H-sum(o!=0 for o in h)
        if sum(units)>k*DENOMINATOR:
            total=sum(units);units=[u*k*DENOMINATOR//total for u in units]
        marginals=[F(u,DENOMINATOR) for u in units]
        assert all(0<=v<=1 for v in marginals) and sum(marginals)<=k
        stop=x[ids[h,'stop1',-1]]
        for j,p in zip(flipids[h],marginals):x[j]=stop*p
        local.append({'history':h,'reach':str(reach),'outgoing':list(map(str,probs)),'flip_marginals':list(map(str,marginals))})
    rows=[]
    for z in src['cells']:
        fee=F(0);coeff=[F(0)]*src['m'];total=F(0)
        for h in states:
            if not matches(z,h):continue
            u0=x[ids[h,'stop0',-1]];u1=x[ids[h,'stop1',-1]]
            total+=u0+u1
            for i,j in enumerate(flipids[h]):
                coeff[i]+=u1-2*x[j];fee+=f[i]*x[j]
            for j in range(src['r']):
                key=h,'query',j
                if key in ids:fee+=q[j]*x[ids[key]]
        assert total==1,total
        assert all(-1<=v<=1 for v in coeff)
        rows.append((fee,tuple(coeff)))
    return x,rows,local


def case(index):
    root=Path(__file__).resolve().parent
    path=root/'rg01'/('c%02da0.json'%index)
    old=json.loads(path.read_text(encoding='utf-8'))
    m,r,H=old['m'],old['r'],old['H']
    src={'m':m,'r':r,'cells':signs(r),'mass':list(map(F,old['mass']))}
    w,f,q=(tuple(map(F,old[key])) for key in ('weights','flip_fee','query_fee'))
    box=[[(F(lo),F(hi)) for lo,hi in row] for row in old['box']]
    arch=architecture(m,r,H)
    states,ids,variables,options,flipids,Aeq,beq,Aub=arch
    scenarios=[];keys=set()
    def add(mu):
        key=tuple(tuple(row) for row in mu)
        if key in keys:return False
        keys.add(key)
        opt=compact_plan(point_source(src,mu),w,f,q,H)[0]
        scenarios.append({'means':mu,'optimum':opt,'cost':source_cost(src,mu,w,f,q,arch)})
        return True
    add([[(lo+hi)/2 for lo,hi in row] for row in box])
    add([[lo for lo,hi in row] for row in box])
    add([[hi for lo,hi in row] for row in box])
    history=[];status='iteration_cap';start=time.perf_counter_ns()
    for iteration in range(40):
        cuts=csr_matrix(np.array([[float(v) for v in sc['cost']]+[-1.] for sc in scenarios]))
        A=vstack((Aub,cuts),format='csr')
        b=[0.]*Aub.shape[0]+[float(sc['optimum']) for sc in scenarios]
        lp=linprog([0.]*len(variables)+[1.],A_ub=A,b_ub=b,A_eq=Aeq,b_eq=beq,bounds=(0,None),method='highs')
        assert lp.success,lp.message
        x,rows,local=realize(src,f,q,H,lp.x,arch)
        for sc in scenarios:
            assert sum((a*b for a,b in zip(x,sc['cost'])),F(0))==policy_value(src,rows,w,sc['means'])
        U,_,worst,_,counts=regret_oracle(src,rows,w,f,q,H,box)
        worst_opt=compact_plan(point_source(src,worst),w,f,q,H)[0]
        assert U==policy_value(src,rows,w,worst)-worst_opt
        raw_beta=list(map(float,-lp.ineqlin.marginals[-len(scenarios):]))
        beta=grid_distribution(raw_beta) if sum(max(0,x) for x in raw_beta)>1e-14 else [F(1)]+[F(0)]*(len(scenarios)-1)
        average=[[sum((p*sc['means'][z][i] for p,sc in zip(beta,scenarios)),F(0)) for i in range(m-r)] for z in range(2**r)]
        meanopt=compact_plan(point_source(src,average),w,f,q,H)[0]
        L=max(F(0),meanopt-sum((p*sc['optimum'] for p,sc in zip(beta,scenarios)),F(0)))
        assert L<=U,(L,U)
        history.append({'iteration':iteration,'scenarios':len(scenarios),'upper':str(U),'lower':str(L),'gap':str(U-L),
                        'numeric_value':lp.fun,'raw_realization_advice':list(map(float,lp.x[:-1])),
                        'beta_raw':raw_beta,'beta':list(map(str,beta)),
                        'worst_means':[[str(x) for x in row] for row in worst],'oracle_work':counts})
        if U-L<=F(1,100000):status='certified_gap';break
        if not add(worst):status='stalled_existing_response';break
    return {'case':index,'input':path.relative_to(root).as_posix(),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'm':m,'r':r,'H':H,'variables':len(variables),'histories':len(states),'status':status,
            'history':history,'final_local_policy':local,
            'final_realization':list(map(str,x)),
            'final_rows':[{'fee':str(fee),'coefficients':list(map(str,coeff))} for fee,coeff in rows],
            'scenarios':[{'means':[[str(x) for x in row] for row in sc['means']],'optimum':str(sc['optimum'])} for sc in scenarios],
            'elapsed_ns':time.perf_counter_ns()-start,'probability_grid':DENOMINATOR,
            'scope':'Exact gap for an admissible grid-repaired randomized controller; known masses. Numerical master optimum not trusted.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case);result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['dependencies']={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('query_flip.py','robust_flip.py','robust_game.py','robust_game_grid.py')}
    with args.out.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(result,indent=2)+'\n')
    last=result['history'][-1]
    print(json.dumps({k:result[k] for k in ('case','m','r','H','variables','histories','status','elapsed_ns')}|{k:last[k] for k in ('iteration','scenarios','upper','lower','gap')}))


if __name__=='__main__':main()
