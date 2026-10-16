"""DEVELOPMENT compact chain-source minimax query/revision LP, Codex (GPT-6)."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import time
from scipy.optimize import linprog
from policy_flow import architecture,realize
from direct_lp import plus,sparse
from lp_certificate import lower_bound
from logical_chain import SIGNS,admissible,oracle,brute
from query_flip import matches,signs


def build(m,r,H,w,f,q,relations,no_queries=False):
    arch=architecture(m,r,H)
    states,ids,variables,options,flipids,Aeq,beq,Aub=arch
    n=len(variables);names=list(variables);bounds=[(F(0),F(1))]*n
    if no_queries:
        for key,j in ids.items():
            if key[1]=='query':bounds[j]=(F(0),F(0))
    def convert(A):
        result=[{} for _ in range(A.shape[0])];coo=A.tocoo()
        for i,j,v in zip(coo.row,coo.col,coo.data):
            assert j<n
            result[int(i)][int(j)]=F(int(v))
        return result
    eq=convert(Aeq);beq=list(map(F,beq));ub=convert(Aub);bub=[F(0)]*len(ub)
    def new(name,lo,hi):
        j=len(names);names.append(name);bounds.append((F(lo),F(hi)));return j
    fee_cap=H*max(tuple(f)+tuple(q)+(F(0),))
    score_cap=2*sum(map(abs,w),F(0))+H*max(f,default=F(0))+1
    beta=new(('regret',),0,fee_cap+2*sum(map(abs,w),F(0))+1)
    allcells=signs(r);cells_kept=0
    for zi,z in enumerate(allcells):
        @lru_cache(None)
        def can(i,previous):
            if i==m:return True
            return any((i>=r or x==z[i]) and (not i or (previous,x) in relations[i-1])
                       and can(i+1,x) for x in SIGNS)
        if not can(0,0):continue
        cells_kept+=1
        fee_row={};coeff_rows=[{} for _ in w]
        for h in states:
            if not matches(z,h):continue
            for i in range(m):
                plus(coeff_rows[i],{ids[h,'stop1',-1]:1,flipids[h][i]:-2})
                plus(fee_row,{flipids[h][i]:f[i]})
            for j in range(r):
                if (h,'query',j) in ids:plus(fee_row,{ids[h,'query',j]:q[j]})
        feeid=new(('cell_fee',zi),0,fee_cap)
        eq.append(plus({feeid:F(1)},fee_row,F(-1)));beq.append(F(0))
        coeffids=[]
        for i in range(m):
            s=new(('cell_response',zi,i),-1,1);coeffids.append(s)
            eq.append(plus({s:F(1)},coeff_rows[i],F(-1)));beq.append(F(0))
        for mode in (0,1):
            nodes={};pending=[]
            def node(key):
                if key not in nodes:
                    nodes[key]=new(('adversary',zi,mode)+key,-score_cap,score_cap)
                    pending.append(key)
                return nodes[key]
            root=node((0,0,0));ub.append({feeid:F(1),root:F(1),beta:F(-1)});bub.append(F(0))
            for i,previous,k in pending:
                parent=nodes[i,previous,k]
                for x in SIGNS:
                    if i<r and x!=z[i]:continue
                    if i and (previous,x) not in relations[i-1]:continue
                    if not can(i+1,x):continue
                    for b in range(1+int(bool(mode) and k<min(H,m))):
                        row={parent:F(-1)};plus(row,{coeffids[i]:w[i]*x})
                        if i+1<m:plus(row,{node((i+1,x,k+b)):F(1)})
                        const=w[i]*(-mode+2*b)*x-f[i]*b
                        ub.append(row);bub.append(-const)
    assert cells_kept>0
    objective=[F(0)]*len(names);objective[beta]=F(1)
    return arch,eq,beq,ub,bub,bounds,objective,names,cells_kept


def solve(m,r,H,w,f,q,relations,no_queries):
    start=time.perf_counter_ns()
    arch,eq,beq,ub,bub,bounds,c,names,cells=build(m,r,H,w,f,q,relations,no_queries)
    lp=linprog(list(map(float,c)),A_ub=sparse(ub,len(c)),b_ub=list(map(float,bub)),
        A_eq=sparse(eq,len(c)),b_eq=list(map(float,beq)),
        bounds=[tuple(map(float,b)) for b in bounds],method='highs',options={'time_limit':45})
    assert lp.success,(lp.status,lp.message)
    src={'m':m,'r':r,'cells':signs(r)};advice=list(lp.x)
    if no_queries:
        for key,j in arch[1].items():
            if key[1]=='query':advice[j]=0.
    realization,rawrows,local=realize(src,f,q,H,advice,arch)
    rows=dict(zip(src['cells'],rawrows))
    U,witness,counts=oracle(rows,w,f,H,relations)
    L,certificate=lower_bound(eq,beq,ub,bub,bounds,c,lp.ineqlin.marginals,lp.eqlin.marginals)
    L=max(F(0),L);assert L<=U,(L,U)
    if no_queries:assert all(realization[j]==0 for key,j in arch[1].items() if key[1]=='query')
    enum=None
    if m<=7:
        exact,worlds,comparisons=brute(rows,w,f,H,relations);assert exact==U
        enum={'worlds':worlds,'comparisons':comparisons,'upper':str(exact)}
    return {'no_queries':no_queries,'numeric':float(lp.fun),'lower':str(L),'upper':str(U),'gap':str(U-L),
       'variables':len(c),'equalities':len(eq),'inequalities':len(ub),'nonzeros':sum(map(len,eq))+sum(map(len,ub)),
       'feasible_query_cells':cells,'histories':len(arch[0]),'iterations':lp.nit,
       'raw_primal_advice':list(map(float,lp.x)),
       'raw_dual_advice':{'lambda':list(map(float,lp.ineqlin.marginals)),'nu':list(map(float,lp.eqlin.marginals))},
       'dual_certificate':certificate,'realization':list(map(str,realization)),'local_policy':local,
       'rows':[{'cell':z,'fee':str(fee),'coefficients':list(map(str,s))} for z,(fee,s) in rows.items()],
       'witness':witness,'oracle_counts':counts,'enumeration':enum,'elapsed_ns':time.perf_counter_ns()-start}


def enumerated_lp(m,r,H,w,f,q,relations,no_queries):
    arch=architecture(m,r,H);states,ids,variables,options,flipids,Aeq,beq,Aub=arch;n=len(variables)
    bounds=[(0.,1.)]*n+[(0.,None)]
    if no_queries:
        for key,j in ids.items():
            if key[1]=='query':bounds[j]=(0.,0.)
    ub=[];coo=Aub.tocoo()
    for _ in range(Aub.shape[0]):ub.append({})
    for i,j,v in zip(coo.row,coo.col,coo.data):ub[int(i)][int(j)]=F(int(v))
    bub=[F(0)]*len(ub);worlds=0
    for x in product(SIGNS,repeat=m):
        if not admissible(x,relations):continue
        worlds+=1;row={n:F(-1)}
        for h in states:
            if not matches(x[:r],h):continue
            plus(row,{ids[h,'stop1',-1]:sum((w[i]*x[i] for i in range(m)),F(0))})
            for i in range(m):plus(row,{flipids[h][i]:f[i]-2*w[i]*x[i]})
            for j in range(r):
                if (h,'query',j) in ids:plus(row,{ids[h,'query',j]:q[j]})
        gains=sorted((2*w[i]*x[i]-f[i] for i in range(m)),reverse=True)
        optimal=min(F(0),sum((w[i]*x[i] for i in range(m)),F(0))-sum((v for v in gains[:H] if v>0),F(0)))
        ub.append(row);bub.append(optimal)
    lp=linprog([0.]*n+[1.],A_ub=sparse(ub,n+1),b_ub=list(map(float,bub)),
        A_eq=Aeq,b_eq=beq,bounds=bounds,method='highs')
    assert lp.success,lp.message
    return {'numeric_value':float(lp.fun),'worlds':worlds}


def case(index):
    root=Path(__file__).resolve().parent;path=root/'lc01'/('c%02da0.json'%index)
    old=json.loads(path.read_text(encoding='utf-8'))
    m,r,H=(31,3,4) if index==5 else (old['m'],old['r'],old['H'])
    w,f=(tuple(map(F,old[k][:m])) for k in ('weights','flip_fee'))
    q=tuple(map(F,old['query_fee'][:r]));relations=[set(map(tuple,x)) for x in old['relations'][:m-1]]
    outputs=[]
    for no_queries in (False,True):
        result=solve(m,r,H,w,f,q,relations,no_queries)
        if m<=7:
            control=enumerated_lp(m,r,H,w,f,q,relations,no_queries)
            assert abs(control['numeric_value']-result['numeric'])<1e-7
            result['enumerated_lp']=control
        outputs.append(result)
    assert F(outputs[0]['lower'])<=F(outputs[1]['upper'])
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'m':m,'r':r,'H':H,
       'input':path.relative_to(root).as_posix(),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
       'weights':list(map(str,w)),'flip_fee':list(map(str,f)),'query_fee':list(map(str,q)),
       'relations':[sorted(x) for x in relations],'results':outputs,
       'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'dependencies':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in
         ('logical_chain.py','policy_flow.py','direct_lp.py','lp_certificate.py','query_flip.py',
          'robust_flip.py','robust_game_grid.py','robust_game.py')},
       'scope':'Rational bounded-dual lower and exact-chain upper for repaired feasible private controller. No general novel-optimization or economic claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':a.case,'m':result['m'],'results':[{k:v[k] for k in
       ('no_queries','lower','upper','gap','variables','inequalities','nonzeros','elapsed_ns')} for v in result['results']]}))
