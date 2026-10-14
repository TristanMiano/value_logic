"""Ordinary primal-dual ternary graph audit certificates. Codex (GPT-6)."""
from itertools import product
from pathlib import Path
import copy
import json
import random
import sys
import g01
import action_audits as aa
import star_learning as base

HERE=Path(__file__).resolve().parent
Meter=base.Meter
VERSION='s08-graph-audits-v1'

def source(costs,edges):
    data=aa.original([[a,b,1] for a,b in edges],costs)
    data.pop('identity');data['bit_source']='all ternary vectors; no stochastic premise'
    data['alphabet']=[0,1,2]
    return g01.seal(data)

def admit(data,meter):
    costs=data['audit_costs'];n=len(costs);edges=data['edges']
    if any(type(c)is not int or c<=0 for c in costs):raise ValueError('Positive integer fees required')
    if any(len(e)!=3 or any(type(v)is not int for v in e) or not 0<=e[0]<e[1]<n or e[2]!=1 for e in edges):raise ValueError('Invalid simple unit-weight graph')
    if len({tuple(e) for e in edges})!=len(edges):raise ValueError('Duplicate graph edge')
    if data!=source(costs,[(a,b) for a,b,w in edges]):raise ValueError('Original source binding mismatch')
    meter.pay('source','original_clauses_features_graph_alphabet_and_fees',20+n+sum(1+len(c) for c in data['hard'])+5*len(data['features']))

def primal_dual(data,meter):
    residual=list(data['audit_costs']);cover=set();dual=[]
    for a,b,w in data['edges']:
        value=0
        if a not in cover and b not in cover:
            value=min(residual[a],residual[b]);residual[a]-=value;residual[b]-=value
            for i in(a,b):
                if residual[i]==0:cover.add(i)
        dual.append(value);meter.pay('planning','uncovered_edge_dual_raise_and_tight_vertices',12)
    meter.pay('planning','emit_cover_and_dual',len(dual)+len(cover))
    return dict(source=data['identity'],cover=sorted(cover),dual=dual)

def check_dual(data,plan,meter,require_cover=True):
    if plan['source']!=data['identity']:raise ValueError('Wrong dual source')
    if len(plan['dual'])!=len(data['edges']):raise ValueError('Wrong dual dimension')
    loads=[0]*data['n']
    for (a,b,w),value in zip(data['edges'],plan['dual']):
        if type(value)is not int or value<0:raise ValueError('Invalid dual value')
        loads[a]+=value;loads[b]+=value;meter.pay('dual_check','nonnegative_edge_and_endpoint_loads',6)
    if any(v>c for v,c in zip(loads,data['audit_costs'])):raise ValueError('Infeasible dual')
    meter.pay('dual_check','all_vertex_capacity_checks',2*data['n'])
    if require_cover:
        cover=set(plan['cover'])
        if len(cover)!=len(plan['cover']) or any(type(i)is not int or not 0<=i<data['n'] for i in cover):raise ValueError('Invalid cover')
        if any(loads[i]!=data['audit_costs'][i] for i in cover):raise ValueError('Untight cover vertex')
        if any(a not in cover and b not in cover for a,b,w in data['edges']):raise ValueError('Uncovered edge')
        meter.pay('dual_check','tight_cover_and_complete_edge_coverage',3*len(cover)+3*len(data['edges']))
    return loads

def two_pass(data,plan,get,meter):
    known={}
    for i in plan['cover']:known[i]=get(i)
    forced=set()
    for a,b,w in data['edges']:
        if known.get(a)==1 and b not in known:forced.add(b)
        if known.get(b)==1 and a not in known:forced.add(a)
        meter.pay('execution','identify_unqueried_mandatory_neighbor',6)
    for i in sorted(forced):known[i]=get(i)
    meter.pay('execution','dispatch_cover_and_forced_queries',len(known))
    return known

def lower_certificate(data,plan,known,meter):
    mandatory=set()
    for a,b,w in data['edges']:
        if known.get(a)==1:mandatory.add(b)
        if known.get(b)==1:mandatory.add(a)
        meter.pay('bound','observed_middle_mandatory_neighbors',4)
    residual=sum(y for (a,b,w),y in zip(data['edges'],plan['dual']) if a not in mandatory and b not in mandatory)
    bound=sum(data['audit_costs'][i] for i in mandatory)+residual
    meter.pay('bound','mandatory_fee_and_remaining_dual',data['n']+4*len(data['edges']))
    return dict(source=data['identity'],mandatory=sorted(mandatory),lower_fee=bound)

def check_lower(data,plan,receipts,request,cert,meter):
    check_dual(data,plan,meter,False);known={}
    for r in receipts:
        if r['identity']!=g01.kernel.digest({k:v for k,v in r.items() if k!='identity'}):raise ValueError('Invalid receipt hash')
        i=r['node']
        if r['source']!=data['identity'] or r['request']!=request or type(i)is not int or not 0<=i<data['n']:raise ValueError('Wrong receipt scope')
        if i in known or r['sequence']!=len(known) or r['value'] not in (0,1,2) or r['base_fee']!=data['audit_costs'][i]:raise ValueError('Invalid receipt')
        known[i]=r['value'];meter.pay('bound_check','independent_receipt_binding',17)
    adjacency=[[] for _ in range(data['n'])]
    for a,b,w in data['edges']:adjacency[a].append(b);adjacency[b].append(a)
    mandatory={v for u,value in known.items() if value==1 for v in adjacency[u]}
    meter.pay('bound_check','independent_adjacency_mandatory_expansion',data['n']+4*len(data['edges'])+sum(len(adjacency[u]) for u,v in known.items() if v==1))
    if cert['source']!=data['identity'] or cert['mandatory']!=sorted(mandatory):raise ValueError('Invalid mandatory assertion')
    lower=sum(data['audit_costs'][v] for v in mandatory)
    for j,(a,b,w) in enumerate(data['edges']):
        if a not in mandatory and b not in mandatory:lower+=plan['dual'][j]
    if lower!=cert['lower_fee']:raise ValueError('Invalid lower bound arithmetic')
    meter.pay('bound_check','sum_mandatory_cost_and_residual_dual',data['n']+3*len(data['edges']))
    return lower

def sufficient(edges,world,mask):
    return all((mask>>a&1 and world[a]!=1) or(mask>>b&1 and world[b]!=1) or(mask>>a&1 and mask>>b&1) for a,b,w in edges)

def offline(data,world):
    costs=data['audit_costs'];edges=data['edges'];n=data['n']
    mandatory={v for a,b,w in edges for v,u in ((a,b),(b,a)) if world[u]==1}
    direct=min(sum(c for i,c in enumerate(costs) if mask>>i&1) for mask in range(1<<n) if sufficient(edges,world,mask))
    rest=[(a,b) for a,b,w in edges if a not in mandatory and b not in mandatory]
    cover=min(sum(c for i,c in enumerate(costs) if mask>>i&1 and i not in mandatory) for mask in range(1<<n)
              if all(mask>>a&1 or mask>>b&1 for a,b in rest))
    formula=sum(costs[i] for i in mandatory)+cover
    assert direct==formula
    return direct

def finite(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    (directory/'declaration.md').write_bytes((HERE/'graph_audits.md').read_bytes())
    rng=random.Random(8141560);cases=[]
    for n in range(2,9):
        options=dict(path=[(i,i+1) for i in range(n-1)],star=[(0,i) for i in range(1,n)],
            cycle=sorted(set([(i,i+1) for i in range(n-1)]+[(0,n-1)])),
            clique=[(i,j) for i in range(n) for j in range(i+1,n)],
            sparse=[(i,j) for i in range(n) for j in range(i+1,n) if rng.randrange(3)==0])
        for shape,edges in options.items():cases.append(dict(name=f'n{n}_{shape}',costs=[rng.randrange(1,10) for i in range(n)],edges=edges))
    cases.append(dict(name='tight_edge',costs=[1,1],edges=[(0,1)]))
    g01.save(directory/'design.json',dict(stage='DEVELOPMENT',cases=cases,source_sha256=g01.sha(__file__),physical_audits=0))
    results=[]
    for case in cases:
        data=source(case['costs'],case['edges']);meter=Meter();admit(data,meter)
        plan=primal_dual(data,meter);check_dual(data,plan,meter);worlds=[]
        for bits in product((0,1),repeat=data['n']):
            world=[1 if b else 2*(i%2) for i,b in enumerate(bits)];receipts=[];request=case['name']+'-'+''.join(map(str,bits))
            def get(i):
                receipts.append(g01.seal(dict(source=data['identity'],request=request,node=i,value=world[i],base_fee=case['costs'][i],sequence=len(receipts))))
                return world[i]
            known=two_pass(data,plan,get,meter);action=base.construct(data,receipts,request,meter);base.check(data,receipts,action,meter)
            cert=lower_certificate(data,plan,known,meter);lower=check_lower(data,plan,receipts,request,cert,meter)
            optimum=offline(data,world);fee=sum(case['costs'][i] for i in known)
            assert lower<=optimum<=fee<=2*lower
            worlds.append(dict(bits=bits,fee=fee,optimum=optimum,lower=lower,mandatory=cert['mandatory']))
        bad=copy.deepcopy(plan);bad['dual'][0:1]=[sum(case['costs'])+1]
        rejects=[]
        for label,fun in [('dual',lambda:check_dual(data,bad,Meter())),('source',lambda:check_dual(dict(data,identity='wrong'),plan,Meter())),
                          ('bound',lambda:check_lower(data,plan,receipts,request,dict(cert,lower_fee=cert['lower_fee']+1),Meter()))]:
            try:fun()
            except ValueError:rejects.append(label)
            else:raise AssertionError('Negative control accepted '+label)
        if receipts:
            altered=copy.deepcopy(receipts);altered[0]['request']='wrong';altered[0]=g01.seal({k:v for k,v in altered[0].items() if k!='identity'})
            try:check_lower(data,plan,altered,request,cert,Meter())
            except ValueError:rejects.append('receipt')
            else:raise AssertionError('Wrong-scope receipt accepted')
        result=dict(name=case['name'],plan=plan,worlds=worlds,negative_controls=rejects,invoice=meter.record(),physical_audits=0)
        g01.save(directory/f"{case['name']}.json",result);results.append(dict(name=case['name'],worlds=len(worlds),max_ratio=max((__import__('fractions').Fraction(w['fee'],w['optimum']) for w in worlds if w['optimum']),default=0)))
        print(case['name'],len(worlds),flush=True)
    g01.save(directory/'results.json',dict(status='complete',cases=results,worlds=sum(x['worlds'] for x in results),physical_audits=0))

if __name__=='__main__':finite(Path(sys.argv[1]))
