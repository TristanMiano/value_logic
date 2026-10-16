"""DEVELOPMENT finite certified-repair regret on existing CNFs, Codex (GPT-6)."""
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
from repair_core import integer_distribution

GRID=2**20


def case(index):
    root=Path(__file__).resolve().parent;path=root/'cr02'/('c%02da0.json'%index);data=json.loads(path.read_text(encoding='utf-8'))
    n=data['n'];worlds=data['source_models'];query=data['query_variables'];weights=[((5*i+3)%9)-4 for i in range(n)]
    fee_query=F(1,4);fee_flip=F(1,8)
    histories=sorted(product((-1,0,1),repeat=2),key=lambda h:(sum(v!=0 for v in h),h));menus={}
    for row in data['arms'][0]['histories']:
        literals=set(row['history']);h=tuple(1 if j in literals else -1 if -j in literals else 0 for j in query)
        menus[h]=row.get('valid_masks',[])
    root_menu=set(menus[(0,0)])
    matches=lambda x,h:all(not v or (1 if x&(1<<(query[j]-1)) else -1)==v for j,v in enumerate(h))
    def terminal_cost(x,mask):
        return sum(w*(1 if (x^mask)&(1<<i) else -1) for i,w in enumerate(weights))+fee_flip*mask.bit_count()
    comparator={x:min([F(0)]+[fee_query*sum(v!=0 for v in h)+terminal_cost(x,mask)
                for h in histories if matches(x,h) for mask in menus[h]]) for x in worlds}
    outputs=[]
    for arm in ('full','static_menu','no_query'):
        start=time.perf_counter_ns();names=[];ids={};options={}
        for h in histories:
            actions=[('stop0',0)]+[('mask',mask) for mask in menus[h] if arm!='static_menu' or mask in root_menu]
            actions += [('query',j) for j,v in enumerate(h) if not v]
            options[h]=[]
            for kind,a in actions:
                j=len(names);names.append((h,kind,a));ids[h,kind,a]=j;options[h].append(j)
        beta=len(names);size=beta+1;bounds=[(F(0),F(1))]*beta+[(F(0),2*sum(map(abs,weights))+F(7,4))]
        if arm=='no_query':
            for (h,kind,a),j in ids.items():
                if kind=='query':bounds[j]=(F(0),F(0))
        eq=[];beq=[]
        for h in histories:
            row={j:F(1) for j in options[h]}
            for j,v in enumerate(h):
                if v:
                    parent=tuple(0 if k==j else h[k] for k in range(2));plus(row,{ids[parent,'query',j]:F(-1)})
            eq.append(row);beq.append(F(not any(h)))
        costs={};ub=[];bub=[]
        for x in worlds:
            row={}
            for j,(h,kind,a) in enumerate(names):
                if matches(x,h) and kind!='stop0':row[j]=fee_query if kind=='query' else terminal_cost(x,a)
            costs[x]=row;ub.append(plus({beta:F(-1)},row));bub.append(comparator[x])
        objective=[F(0)]*beta+[F(1)]
        lp=linprog(list(map(float,objective)),A_ub=sparse(ub,size),b_ub=list(map(float,bub)),
            A_eq=sparse(eq,size),b_eq=list(map(float,beq)),bounds=[tuple(map(float,b)) for b in bounds],
            method='highs',options={'time_limit':45})
        assert lp.success,(lp.status,lp.message)
        realization=[F(0)]*beta;local=[]
        for h in histories:
            reach=F(1) if not any(h) else sum((realization[ids[tuple(0 if k==j else h[k] for k in range(2)),'query',j]] for j,v in enumerate(h) if v),F(0))
            permitted=[j for j in options[h] if arm!='no_query' or names[j][1]!='query']
            units=integer_distribution([lp.x[j] for j in permitted],GRID)
            for j,u in zip(permitted,units):realization[j]=reach*F(u,GRID)
            local.append({'history':h,'reach':str(reach),'option_ids':permitted,'units':units})
        for row,b in zip(eq,beq):assert sum((a*realization[j] for j,a in row.items()),F(0))==b
        realized_cost={x:sum((a*realization[j] for j,a in row.items()),F(0)) for x,row in costs.items()}
        regrets={x:realized_cost[x]-comparator[x] for x in worlds};assert min(regrets.values())>=0
        upper=max(regrets.values());lower,certificate=lower_bound(eq,beq,ub,bub,bounds,objective,lp.ineqlin.marginals,lp.eqlin.marginals)
        lower=max(F(0),lower);assert lower<=upper
        metrics=[]
        for x in worlds:
            qcount=F(0);fcount=F(0);enabled=F(0);terminal=F(0)
            for j,(h,kind,a) in enumerate(names):
                if not matches(x,h):continue
                if kind=='query':qcount+=realization[j]
                if kind=='mask':
                    terminal+=realization[j];fcount+=a.bit_count()*realization[j]
                    if a not in root_menu:enabled+=realization[j]
            metrics.append({'world':x,'cost':str(realized_cost[x]),'regret':str(regrets[x]),
                'expected_queries':str(qcount),'expected_flips':str(fcount),'new_menu_use_probability':str(enabled),'terminal_one_probability':str(terminal)})
        outputs.append({'arm':arm,'numeric':float(lp.fun),'lower':str(lower),'upper':str(upper),'gap':str(upper-lower),
            'variables':size,'equalities':len(eq),'world_inequalities':len(ub),'nonzeros':sum(map(len,eq))+sum(map(len,ub)),
            'raw_primal_advice':list(map(float,lp.x)),'raw_dual_advice':{'lambda':list(map(float,lp.ineqlin.marginals)),'nu':list(map(float,lp.eqlin.marginals))},
            'dual_certificate':certificate,'policy_option_names':names,'realization':list(map(str,realization)),
            'local_policy':local,'world_metrics':metrics,'elapsed_ns':time.perf_counter_ns()-start})
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'name':data['name'],'n':n,'queries':query,
        'query_fee':str(fee_query),'flip_fee':str(fee_flip),'weights':weights,'query_cap':2,'flip_cap':2,'total_cap':4,
        'input':path.relative_to(root).as_posix(),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'comparator':[{'world':x,'optimum':str(comparator[x])} for x in worlds],'results':outputs,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependencies':{s:hashlib.sha256((root/s).read_bytes()).hexdigest() for s in ('direct_lp.py','lp_certificate.py','repair_core.py')},
        'scope':'Exact finite regret enclosures conditional on inherited source completeness and selected two-query/two-flip menu. Acquisition/preparation/computation prices remain outside the objective.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':a.case,'name':result['name'],'results':[{k:v[k] for k in ('arm','lower','upper','gap','variables','world_inequalities','elapsed_ns')} for v in result['results']]}))
