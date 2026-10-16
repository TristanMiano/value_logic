"""DEVELOPMENT compact private-query and certified-repair LP, Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import time
from scipy.optimize import linprog
from direct_lp import plus,sparse
from lp_certificate import lower_bound
from repair_core import (SIGNS,ALL,compatible,admissible,compile_menu,mask_network,
    joint_network,point_comparator,separator,integer_distribution)

GRID=2**20


def architecture(m,r,H,source,target):
    histories=sorted((h for h in product((-1,0,1),repeat=r) if sum(v!=0 for v in h)<=H),
                     key=lambda h:(sum(v!=0 for v in h),h))
    names=[];ids={};options={};menus={};networks={};network_ids={}
    eq=[];beq=[];bounds=[]
    def new(key):
        j=len(names);names.append(key);bounds.append((F(0),F(1)));return j
    for h in histories:
        options[h]=[]
        for act,j in [('stop0',-1),('stop1',-1)]+([('query',j) for j in range(r) if not h[j]] if sum(v!=0 for v in h)<H else []):
            ids[h,act,j]=new(('policy',h,act,j));options[h].append(ids[h,act,j])
        menus[h]=compile_menu(source,target,h)
        network=mask_network(m,menus[h],H-sum(v!=0 for v in h));networks[h]=network
        if network is None:
            bounds[ids[h,'stop1',-1]]=(F(0),F(0));network_ids[h]=[]
        else:network_ids[h]=[new(('mask',h,e)) for e in range(len(network['edges']))]
    for h in histories:
        row={j:F(1) for j in options[h]}
        for j,v in enumerate(h):
            if v:
                parent=tuple(0 if i==j else h[i] for i in range(r))
                plus(row,{ids[parent,'query',j]:F(-1)})
        eq.append(row);beq.append(F(not any(h)))
        network=networks[h]
        if network is None:continue
        incoming={key:[] for key in network['nodes']}
        for e,(_,child,_,_) in enumerate(network['edges']):incoming[child].append(e)
        for key in network['nodes']:
            if not network['out'][key]:continue
            row={network_ids[h][e]:F(1) for e in network['out'][key]}
            for e in incoming[key]:plus(row,{network_ids[h][e]:F(-1)})
            if key==network['root']:plus(row,{ids[h,'stop1',-1]:F(-1)})
            eq.append(row);beq.append(F(0))
    return {'histories':histories,'ids':ids,'options':options,'menus':menus,
            'networks':networks,'network_ids':network_ids,'names':names,'eq':eq,'beq':beq,'bounds':bounds}


def cost_rows(arch,m,r,w,f,q):
    rows={}
    for z in product(SIGNS,repeat=r):
        fee={};coeff=[{} for _ in range(m)]
        for h in arch['histories']:
            if not compatible(z,h):continue
            u=arch['ids'][h,'stop1',-1]
            for i in range(m):plus(coeff[i],{u:F(1)})
            network=arch['networks'][h]
            if network is not None:
                for e,(_,_,i,b) in enumerate(network['edges']):
                    if b:
                        j=arch['network_ids'][h][e]
                        plus(coeff[i],{j:F(-2)});plus(fee,{j:f[i]})
            for j in range(r):
                key=h,'query',j
                if key in arch['ids']:plus(fee,{arch['ids'][key]:q[j]})
        rows[z]=(fee,coeff)
    return rows


def build(m,r,H,w,f,q,source,target,no_queries,enumerate_worlds=False):
    arch=architecture(m,r,H,source,target)
    n=len(arch['names']);names=list(arch['names']);bounds=list(arch['bounds'])
    eq=list(arch['eq']);beq=list(arch['beq']);ub=[];bub=[]
    if no_queries:
        for key,j in arch['ids'].items():
            if key[1]=='query':bounds[j]=(F(0),F(0))
    def new(name,lo,hi):
        j=len(names);names.append(name);bounds.append((F(lo),F(hi)));return j
    fee_cap=H*max(tuple(f)+tuple(q)+(F(0),))
    score_cap=2*sum(map(abs,w),F(0))+H*max(f,default=F(0))+1
    beta=new(('regret',),0,fee_cap+2*sum(map(abs,w),F(0))+1)
    rowmap=cost_rows(arch,m,r,w,f,q)
    if enumerate_worlds:
        for x in product(SIGNS,repeat=m):
            if not admissible(x,source):continue
            value,_=point_comparator(x,w,f,q,H,arch['menus'],arch['networks'])
            fee,coeff=rowmap[x[:r]];row={beta:F(-1)};plus(row,fee)
            for i in range(m):plus(row,coeff[i],w[i]*x[i])
            ub.append(row);bub.append(value)
    else:
        for zi,(z,(fee,coeff)) in enumerate(rowmap.items()):
            if joint_network(source,None,z,0,0) is None:continue
            feeid=new(('fee',zi),0,fee_cap);eq.append(plus({feeid:F(1)},fee,F(-1)));beq.append(F(0))
            coeffids=[]
            for i in range(m):
                j=new(('response',zi,i),-1,1);coeffids.append(j)
                eq.append(plus({j:F(1)},coeff[i],F(-1)));beq.append(F(0))
            choices=[(None,None,0,0,F(0))]
            choices += [(h,menu,1,H-sum(v!=0 for v in h),sum((q[j] for j,v in enumerate(h) if v),F(0)))
                        for h,menu in arch['menus'].items() if menu is not None and compatible(z,h)]
            for hi,(h,menu,mode,cap,query_fee) in enumerate(choices):
                network=joint_network(source,menu,z,cap,mode)
                if network is None:continue
                nodeids={key:new(('adversary',zi,hi,key),-score_cap,score_cap)
                         for key in network['nodes'] if network['out'][key]}
                ub.append({feeid:F(1),nodeids[network['root']]:F(1),beta:F(-1)});bub.append(query_fee)
                for key,child,i,x,b in network['edges']:
                    row={nodeids[key]:F(-1),coeffids[i]:w[i]*x}
                    if child in nodeids:plus(row,{nodeids[child]:F(1)})
                    constant=w[i]*(-mode+2*b)*x-f[i]*b
                    ub.append(row);bub.append(-constant)
    c=[F(0)]*len(names);c[beta]=F(1)
    return arch,eq,beq,ub,bub,bounds,c,names,rowmap


def realize(arch,m,r,H,raw,no_queries):
    x=[F(0)]*len(arch['names']);local=[]
    for h in arch['histories']:
        reach=F(1) if not any(h) else sum((x[arch['ids'][tuple(0 if i==j else h[i] for i in range(r)),'query',j]]
                                          for j,v in enumerate(h) if v),F(0))
        allowed=[]
        for j in arch['options'][h]:
            _,_,action,coordinate=arch['names'][j]
            if action=='stop1' and arch['networks'][h] is None:continue
            if action=='query' and no_queries:continue
            allowed.append(j)
        units=integer_distribution([raw[j] for j in allowed],GRID)
        for j,p in zip(allowed,units):x[j]=reach*F(p,GRID)
        network=arch['networks'][h];edge_units=[]
        if network is not None:
            incoming={key:0 for key in network['nodes']};incoming[network['root']]=GRID
            edge_units=[0]*len(network['edges'])
            for key in network['nodes']:
                outgoing=network['out'][key]
                if not outgoing:continue
                allocated=integer_distribution([raw[arch['network_ids'][h][e]] for e in outgoing],incoming[key])
                for e,p in zip(outgoing,allocated):
                    edge_units[e]=p;incoming[network['edges'][e][1]]+=p
                    x[arch['network_ids'][h][e]]=x[arch['ids'][h,'stop1',-1]]*F(p,GRID)
            assert sum(incoming[key] for key in network['nodes'] if not network['out'][key])==GRID
        local.append({'history':h,'reach':str(reach),'choice_ids':allowed,'choice_units':units,'mask_edge_units':edge_units})
    for row,b in zip(arch['eq'],arch['beq']):assert sum((a*x[j] for j,a in row.items()),F(0))==b
    assert all(lo<=v<=hi for v,(lo,hi) in zip(x,arch['bounds']))
    for z in product(SIGNS,repeat=r):
        total=sum((x[arch['ids'][h,a,-1]] for h in arch['histories'] if compatible(z,h) for a in ('stop0','stop1')),F(0))
        assert total==1
    return x,local


def brute_upper(rows,w,f,q,H,source,target):
    m=len(w);r=len(q);worlds=[x for x in product(SIGNS,repeat=m) if admissible(x,source)]
    best=None;comparisons=0
    for x in worlds:
        optimum=F(0)
        for h in product((-1,0,1),repeat=r):
            used=sum(v!=0 for v in h)
            if used>H or not compatible(x,h):continue
            compatible_worlds=[y for y in worlds if compatible(y,h)]
            for mask in range(2**m):
                if mask.bit_count()>H-used:continue
                if not all(admissible(tuple(v*(-1 if mask&(1<<i) else 1) for i,v in enumerate(y)),target) for y in compatible_worlds):continue
                comparisons+=1
                cost=sum((w[i]*x[i]*(-1 if mask&(1<<i) else 1)+f[i]*bool(mask&(1<<i)) for i in range(m)),F(0))
                cost+=sum((q[j] for j,v in enumerate(h) if v),F(0));optimum=min(optimum,cost)
        fee,coeff=rows[x[:r]];value=fee+sum((w[i]*x[i]*coeff[i] for i in range(m)),F(0))-optimum
        best=value if best is None else max(best,value)
    return best,{'worlds':len(worlds),'valid_mask_comparisons':comparisons}


def solve(m,r,H,w,f,q,source,target,no_queries):
    start=time.perf_counter_ns()
    arch,eq,beq,ub,bub,bounds,c,names,rowmap=build(m,r,H,w,f,q,source,target,no_queries)
    lp=linprog(list(map(float,c)),A_ub=sparse(ub,len(c)),b_ub=list(map(float,bub)),
       A_eq=sparse(eq,len(c)),b_eq=list(map(float,beq)),bounds=[tuple(map(float,b)) for b in bounds],
       method='highs',options={'time_limit':45})
    assert lp.success,(lp.status,lp.message)
    x,local=realize(arch,m,r,H,lp.x,no_queries)
    evaluate=lambda row:sum((a*x[j] for j,a in row.items()),F(0))
    rows={z:(evaluate(fee),tuple(map(evaluate,coeff))) for z,(fee,coeff) in rowmap.items()}
    upper,witness,counts=separator(rows,w,f,q,H,source,arch['menus'])
    lower,certificate=lower_bound(eq,beq,ub,bub,bounds,c,lp.ineqlin.marginals,lp.eqlin.marginals)
    lower=max(F(0),lower);assert lower<=upper,(lower,upper)
    truth=tuple(witness['truth']);point,_=point_comparator(truth,w,f,q,H,arch['menus'],arch['networks'])
    fee,coeff=rows[truth[:r]]
    assert upper==fee+sum((w[i]*truth[i]*coeff[i] for i in range(m)),F(0))-point
    check=None
    if m<=6:
        explicit,check=brute_upper(rows,w,f,q,H,source,target);assert explicit==upper
        _,ee,eb,eu,ev,bounds2,c2,_,_=build(m,r,H,w,f,q,source,target,no_queries,True)
        enumerated=linprog(list(map(float,c2)),A_ub=sparse(eu,len(c2)),b_ub=list(map(float,ev)),
            A_eq=sparse(ee,len(c2)),b_eq=list(map(float,eb)),bounds=[tuple(map(float,b)) for b in bounds2],method='highs')
        assert enumerated.success and abs(enumerated.fun-lp.fun)<1e-7,(enumerated.message,enumerated.fun,lp.fun)
        check['enumerated_lp']=float(enumerated.fun)
    return {'no_queries':no_queries,'numeric':float(lp.fun),'lower':str(lower),'upper':str(upper),'gap':str(upper-lower),
        'variables':len(c),'equalities':len(eq),'inequalities':len(ub),'nonzeros':sum(map(len,eq))+sum(map(len,ub)),
        'histories':len(arch['histories']),'empty_terminal_menus':sum(n is None for n in arch['networks'].values()),
        'raw_primal_advice':list(map(float,lp.x)),'raw_dual_advice':{'lambda':list(map(float,lp.ineqlin.marginals)),'nu':list(map(float,lp.eqlin.marginals))},
        'dual_certificate':certificate,'realization':list(map(str,x)),'local_policy':local,
        'rows':[{'cell':z,'fee':str(fee),'coefficients':list(map(str,s))} for z,(fee,s) in rows.items()],
        'witness':witness,'oracle_counts':counts,'small_control':check,'elapsed_ns':time.perf_counter_ns()-start}


def case(index):
    root=Path(__file__).resolve().parent
    oldindex=[0,2,3,0,0,5,5][index]
    path=root/'sr01'/('c%02da0.json'%oldindex);old=json.loads(path.read_text(encoding='utf-8'))
    m,r,H=old['m'],old['r'],old['H']
    w,f,q=(tuple(map(F,old[k])) for k in ('weights','flip_fee','query_fee'))
    source=[set(map(tuple,s)) for s in old['relations']];target=[set(s) for s in source]
    if index==3:
        m,r,H=4,2,3;w=(F(1),F(2),F(-1),F(1));f=(F(1,4),)*m;q=(F(1,4),F(1,2))
        source=[set(ALL) for _ in range(m-1)];target=[ALL-{(1,-1)},set(ALL),set(ALL)]
    if index==4:H=0
    if index==6:target[0]={(-1,-1),(1,1)}
    outputs=[solve(m,r,H,w,f,q,source,target,no_queries) for no_queries in (False,True)]
    if index==0:assert F(outputs[0]['lower'])<=F(65,64)<=F(outputs[0]['upper']) and abs(outputs[0]['numeric']-65/64)<1e-7
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'m':m,'r':r,'H':H,
       'input':path.relative_to(root).as_posix(),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
       'weights':list(map(str,w)),'flip_fee':list(map(str,f)),'query_fee':list(map(str,q)),
       'source_relations':[sorted(s) for s in source],'target_relations':[sorted(s) for s in target],
       'results':outputs,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'dependencies':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ('repair_core.py','direct_lp.py','lp_certificate.py')},
       'scope':'Finite safe-revision compact LP, rational realized upper and residual-corrected dual lower. Computation and source acquisition unpriced.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':a.case,'m':result['m'],'results':[{k:v[k] for k in ('no_queries','lower','upper','gap','variables','inequalities','nonzeros','empty_terminal_menus','elapsed_ns')} for v in result['results']]}))
