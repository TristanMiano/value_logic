#!/usr/bin/env python3
"""Checked joint map-error guards on tree cost sources. DEVELOPMENT.
Codex (GPT-6), 2026-10-13. Guard witnesses are worst cases, not acquired truth.
"""
from collections import Counter
from datetime import datetime,timezone
from itertools import product
from pathlib import Path
import copy
import json
import random
import sys
import time
import g01

HERE=Path(__file__).resolve().parent
VERSION='s08-joint-guard-v1'
Meter=g01.kernel.Meter


def tree(edges,supports,meter):
    n=len(supports)
    if n<1 or len(edges)!=n-1 or any(not q or sorted(set(q))!=list(q) or any(type(v)is not int or v not in (0,1) for v in q) for q in supports):
        raise ValueError('Nonempty binary supports and n-1 tree edges required')
    adjacency=[[] for _ in range(n)]
    seen=set()
    for a,b,w in edges:
        if any(type(v)is not int for v in (a,b,w)) or not 0<=a<n or not 0<=b<n or a==b or w<0:
            raise ValueError('Malformed nonnegative edge')
        key=tuple(sorted((a,b)))
        if key in seen:raise ValueError('Duplicate edge')
        seen.add(key);adjacency[a].append((b,w));adjacency[b].append((a,w))
        meter.pay('admission','edge_endpoints_weight_and_duplicate_check',8)
    parents=[None]*n;parents[0]=-1
    order=[0]
    for a in order:
        for b,w in adjacency[a]:
            if b==parents[a]:continue
            if parents[b] is not None:raise ValueError('Cycle')
            parents[b]=a;order.append(b)
    if len(order)!=n:raise ValueError('Disconnected source')
    meter.pay('admission','supports_and_connected_tree_check',3*n+2*len(edges))
    return adjacency,parents,order


def produce(edges,supports):
    meter=Meter()
    adjacency,parent,order=tree(edges,supports,meter)
    node={};messages={};choices={}
    for i in reversed(order):
        children=[(j,w) for j,w in adjacency[i] if parent[j]==i]
        node[i]={v:sum(messages[j][v] for j,w in children) for v in supports[i]}
        meter.pay('produce','combine_child_messages',len(supports[i])*(1+len(children)))
        if i:
            weight=next(w for j,w in adjacency[i] if j==parent[i])
            messages[i]={};choices[i]={}
            for u in supports[parent[i]]:
                values=[(weight*abs(u-v)+node[i][v],v) for v in supports[i]]
                value,arg=max(values)
                messages[i][u]=value;choices[i][u]=arg
                meter.pay('produce','edge_factor_add_and_max',4*len(supports[i]))
    bound,root=max((value,v) for v,value in node[0].items())
    assignment=[None]*len(supports);assignment[0]=root
    for i in order[1:]:assignment[i]=choices[i][assignment[parent[i]]]
    meter.pay('produce','root_and_attaining_assignment',2*len(supports))
    return dict(bound=bound,messages=messages,witness=assignment,
                source=g01.kernel.digest(dict(edges=edges,supports=supports)),invoice=meter.record())


def check(edges,supports,certificate):
    """Check local upper inequalities rather than replay the max producer."""
    meter=Meter()
    adjacency,parent,order=tree(edges,supports,meter)
    if certificate['source']!=g01.kernel.digest(dict(edges=edges,supports=supports)):
        raise ValueError('Certificate has another source/refinement')
    messages={int(i):{int(v):value for v,value in row.items()} for i,row in certificate['messages'].items()}
    if set(messages)!=set(range(1,len(supports))):raise ValueError('Wrong message scope')
    for i in range(1,len(supports)):
        if set(messages[i])!=set(supports[parent[i]]):raise ValueError('Wrong parent-value message support')
        weight=next(w for j,w in adjacency[i] if j==parent[i])
        children=[j for j,w in adjacency[i] if parent[j]==i]
        for u in supports[parent[i]]:
            for v in supports[i]:
                rhs=weight*abs(u-v)+sum(messages[j][v] for j in children)
                if messages[i][u]<rhs:raise ValueError('Message is not an upper bound')
                meter.pay('check','local_message_upper_inequality',5+len(children))
    for root in supports[0]:
        if certificate['bound']<sum(messages[j][root] for j,w in adjacency[0]):
            raise ValueError('Root is not an upper bound')
        meter.pay('check','root_upper_inequality',2+len(adjacency[0]))
    witness=certificate['witness']
    if len(witness)!=len(supports) or any(v not in q for v,q in zip(witness,supports)):
        raise ValueError('Worst-case witness outside the admitted cost source')
    achieved=sum(w*abs(witness[a]-witness[b]) for a,b,w in edges)
    if achieved!=certificate['bound']:raise ValueError('Worst-case witness does not attain the bound')
    meter.pay('check','attaining_witness_cost',len(supports)+4*len(edges))
    return meter.record()


def exhaustive(edges,supports):
    return max(sum(w*abs(t[a]-t[b]) for a,b,w in edges) for t in product(*supports))


def independent_bounds(edges,supports):
    oriented=pair=0
    for a,b,w in edges:
        oriented+=w*(max(max(0,u-v) for u in supports[a] for v in supports[b])
                    +max(max(0,v-u) for u in supports[a] for v in supports[b]))
        pair+=w*max(abs(u-v) for u in supports[a] for v in supports[b])
    return dict(separate_orientations=oriented,separate_edges=pair)


def generate(rng,n):
    edges=[[i,rng.randrange(i),rng.randrange(1,5)] for i in range(1,n)]
    supports=[[[0],[1],[0,1]][rng.randrange(3)] for _ in range(n)]
    return dict(edges=edges,supports=supports)


def run(directory):
    directory.mkdir(exist_ok=False)
    (directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(261013)
    cases=[generate(rng,2+i%8) for i in range(32)]
    large=[generate(rng,n) for n in (32,128,512)]
    g01.save(directory/'design.json',dict(version=VERSION,contributor='Codex (GPT-6)',stage='DEVELOPMENT',
        created_utc=datetime.now(timezone.utc).isoformat(),small=cases,large=large,
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'joint_guard.md'),
        actual_new_cost_audits=0,actual_logical_provider_calls=0))
    result=dict(version=VERSION,status='running',small=[],large=[],negative_controls=[])
    for index,case in enumerate(cases):
        edges,supports=case['edges'],case['supports']
        cert=produce(edges,supports);invoice=check(edges,supports,cert)
        assert cert['bound']==exhaustive(edges,supports)
        refinements=[]
        for i,values in enumerate(supports):
            if len(values)<2:continue
            for value in values:
                q=copy.deepcopy(supports);q[i]=[value]
                child=produce(edges,q);checked=check(edges,q,child)
                assert child['bound']==exhaustive(edges,q) and child['bound']<=cert['bound']
                refinements.append(dict(node=i,value=value,bound=child['bound'],production=child['invoice'],checking=checked))
        result['small'].append(dict(index=index,certificate=cert,checking=invoice,
            **independent_bounds(edges,supports),refinements=refinements))
    for case in large:
        cert=produce(**case);checked=check(case['edges'],case['supports'],cert)
        result['large'].append(dict(n=len(case['supports']),certificate=cert,checking=checked,
            **independent_bounds(**case),scope='Upper inequalities and attaining witness; no enumeration'))
    triangle=[[0,1,1],[1,2,1],[2,0,1]];q=[[0,1]]*3
    result['triangle']=dict(**independent_bounds(triangle,q),exact=exhaustive(triangle,q))
    edges=[[0,1,1],[1,2,2]];q=[[0,1]]*3
    valid=produce(edges,q)
    for name in ('message_underestimate','nonattaining_witness','wrong_source'):
        bad=copy.deepcopy(valid)
        if name=='message_underestimate':bad['messages'][2][0]=-1
        if name=='nonattaining_witness':bad['witness']=[0,0,0]
        if name=='wrong_source':bad['source']='0'*64
        try:check(edges,q,bad)
        except ValueError as exc:result['negative_controls'].append(dict(name=name,rejected=True,reason=str(exc)))
        else:raise AssertionError('Tampered guard accepted')
    try:produce(triangle,[[0,1]]*3)
    except ValueError as exc:result['negative_controls'].append(dict(name='cycle',rejected=True,reason=str(exc)))
    else:raise AssertionError('Cycle accepted')
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat())
    result['summary']=dict(small_initial_cases=len(cases),single_audit_refinements=sum(len(r['refinements']) for r in result['small']),
        joint_strictly_better_than_edgewise=sum(r['certificate']['bound']<r['separate_edges'] for r in result['small']),
        joint_strictly_better_than_orientations=sum(r['certificate']['bound']<r['separate_orientations'] for r in result['small']),
        large_cases=len(large),rejected_negative_controls=len(result['negative_controls']),actual_new_audits=0)
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status=result['status'],summary=result['summary'],triangle=result['triangle'],large=[
        dict(n=r['n'],bound=r['certificate']['bound'],edgewise=r['separate_edges'],orientation=r['separate_orientations'],
             produce_units=r['certificate']['invoice']['total'],check_units=r['checking']['total']) for r in result['large']])))


if __name__=='__main__':run(Path(sys.argv[1]))
