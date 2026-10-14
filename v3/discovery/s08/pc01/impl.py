#!/usr/bin/env python3
"""Checked supplied path policies. DEVELOPMENT, Codex (GPT-6), 2026-10-14."""
from functools import lru_cache
from fractions import Fraction as F
from datetime import datetime,timezone
from pathlib import Path
import copy
import json
import random
import sys
import g01

HERE=Path(__file__).resolve().parent
VERSION='s08-path-policy-certs-v1'
Meter=g01.kernel.Meter


def identity(costs,boxes):
    return g01.kernel.digest(json.loads(json.dumps(dict(costs=costs,boxes=boxes,
        kind='independent exactly-one ternary path action source; conditional probability boxes'),default=g01.encode)))


def admit(costs,boxes,meter):
    if not costs or len(costs)!=len(boxes):raise ValueError('Source dimensions')
    if any(type(c) not in (int,F) or c<=0 for c in costs):raise ValueError('Invalid fee')
    if any(len(q)!=2 or any(type(p) not in (int,F) for p in q) or not 0<=q[0]<=q[1]<=1 for q in boxes):raise ValueError('Invalid probability box')
    meter.pay('admission','bind_positive_fees_and_conditional_boxes',8*len(costs))


def propose(costs,boxes,rule):
    meter=Meter();n=len(costs);roots={}
    for a in range(n):
        for b in range(a+1,n):
            if rule=='left':i=a;units=1
            elif rule=='middle':i=(a+b)//2;units=2
            elif rule=='ratio':
                i=max(range(a,b+1),key=lambda j:((boxes[j][0]+boxes[j][1])/(2*costs[j]),-j));units=5*(b-a+1)
            else:raise ValueError('Unknown proposer')
            roots[a,b]=i;meter.pay('proposal','choose_interval_root',units)
    return roots,meter.record()


def upper(costs,boxes,roots):
    meter=Meter();admit(costs,boxes,meter);n=len(costs);tables={k:{} for k in ('ordinary','left','right')}
    def at(kind,a,b):return tables[kind][a,b] if a<=b else F(0)
    def combine(i,e,m):
        meter.pay('production','two_endpoint_affine_maximum',9)
        return costs[i]+max(p*e+(1-p)*m for p in boxes[i])
    for length in range(1,n+1):
        for a in range(n-length+1):
            b=a+length-1
            tables['left'][a,b]=combine(a,at('ordinary',a+1,b),at('left',a+1,b))
            tables['right'][a,b]=combine(b,at('ordinary',a,b-1),at('right',a,b-1))
            if a==b:tables['ordinary'][a,b]=F(0)
            else:
                i=roots[a,b]
                if not a<=i<=b:raise ValueError('Policy root outside interval')
                tables['ordinary'][a,b]=combine(i,at('ordinary',a,i-1)+at('ordinary',i+1,b),at('right',a,i-1)+at('left',i+1,b))
            meter.pay('production','retain_three_bounds',3)
    return dict(source=identity(costs,boxes),roots=roots,tables=tables,bound=tables['ordinary'][0,n-1],invoice=meter.record())


def check(costs,boxes,certificate):
    meter=Meter();admit(costs,boxes,meter);n=len(costs)
    if certificate['source']!=identity(costs,boxes):raise ValueError('Wrong source or probability box')
    states={(a,b) for a in range(n) for b in range(a,n)}
    if set(certificate['roots'])!={(a,b) for a,b in states if a<b}:raise ValueError('Policy scope mismatch')
    tables=certificate['tables']
    if set(tables)!= {'ordinary','left','right'}:raise ValueError('Table scope')
    for row in tables.values():
        if set(row)!=states or any(type(v) not in (int,F) or v<0 for v in row.values()):raise ValueError('Invalid upper entries')
    def at(kind,a,b):return tables[kind][a,b] if a<=b else F(0)
    for a,b in states:
        obligations=[('left',a,at('ordinary',a+1,b),at('left',a+1,b)),
            ('right',b,at('ordinary',a,b-1),at('right',a,b-1))]
        if a==b:
            if tables['ordinary'][a,b]!=0:raise ValueError('Ordinary singleton should stop')
        else:
            i=certificate['roots'][a,b]
            if type(i)is not int or not a<=i<=b:raise ValueError('Invalid selected root')
            obligations.append(('ordinary',i,at('ordinary',a,i-1)+at('ordinary',i+1,b),at('right',a,i-1)+at('left',i+1,b)))
        for kind,i,e,m in obligations:
            for p in boxes[i]:
                if tables[kind][a,b]<costs[i]+p*e+(1-p)*m:raise ValueError('Underestimated continuation')
                meter.pay('checking','individual_endpoint_upper_inequality',7)
    if certificate['bound']!=tables['ordinary'][0,n-1]:raise ValueError('Root bound mismatch')
    return meter.record()


def next_query(state,roots):
    """Replay the supplied policy using only known extreme/middle outcomes."""
    class Missing(Exception):pass
    def ask(i):
        if state[i]<0:raise Missing(i)
        return state[i]
    def go(a,b,mode='ordinary'):
        if a>b or (a==b and mode=='ordinary'):return
        if mode=='left':go(a+1,b,'left' if ask(a)==1 else 'ordinary')
        elif mode=='right':go(a,b-1,'right' if ask(b)==1 else 'ordinary')
        else:
            i=roots[a,b];middle=ask(i)==1
            go(a,i-1,'right' if middle else 'ordinary');go(i+1,b,'left' if middle else 'ordinary')
    try:go(0,len(state)-1)
    except Missing as exc:return exc.args[0]
    return None


def adversary(costs,boxes,roots):
    """Explicit history-state maximum; extreme labels collapse only in query order."""
    calls=0
    @lru_cache(None)
    def visit(state):
        nonlocal calls
        calls+=1;i=next_query(state,roots)
        if i is None:return F(0)
        extreme=list(state);extreme[i]=0;middle=list(state);middle[i]=1
        e=visit(tuple(extreme));m=visit(tuple(middle))
        return costs[i]+max(p*e+(1-p)*m for p in boxes[i])
    return dict(value=visit((-1,)*len(costs)),states=calls)


def export(certificate):
    return dict(source=certificate['source'],bound=certificate['bound'],invoice=certificate['invoice'],
        roots={f'{a},{b}':v for (a,b),v in certificate['roots'].items()},
        tables={kind:{f'{a},{b}':v for (a,b),v in table.items()} for kind,table in certificate['tables'].items()})


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(8141424);cases=[]
    for n in range(2,8):
        for repeat in range(4):
            boxes=[]
            for _ in range(n):
                a,b=sorted([rng.randrange(5),rng.randrange(5)]);boxes.append([F(a,4),F(b,4)])
            cases.append(dict(costs=[rng.randrange(1,9) for _ in range(n)],boxes=boxes))
    large=[dict(costs=[rng.randrange(1,9) for _ in range(n)],boxes=[[F(1,4),F(3,4)] for _ in range(n)]) for n in (32,128)]
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        created_utc=datetime.now(timezone.utc).isoformat(),small=cases,large=large,rules=['left','middle','ratio'],
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'path_policy_certs.md'),actual_new_audits=0))
    result=dict(status='running',small=[],large=[],negative_controls=[])
    for index,case in enumerate(cases+large):
        for rule in ('left','middle','ratio'):
            roots,proposal=propose(**case,rule=rule);certificate=upper(**case,roots=roots);checking=check(**case,certificate=certificate)
            record=dict(case=index,n=len(case['costs']),rule=rule,proposal=proposal,certificate=export(certificate),checking=checking)
            if index<len(cases):
                actual=adversary(**case,roots=roots);assert actual['value']==certificate['bound'];record['adversary']=actual
                result['small'].append(record)
            else:result['large'].append(record)
            g01.save(directory/'results.json',result)
    special=dict(costs=[10,1,1,1],boxes=[[F(0),F(0)],[F(1),F(1)],[F(0),F(1)],[F(0),F(0)]])
    roots,_=propose(**special,rule='left');roots[0,3]=3
    certificate=upper(**special,roots=roots);check(**special,certificate=certificate)
    lower_only=dict(special,boxes=[[a,a] for a,b in special['boxes']])
    wrong=upper(**lower_only,roots=roots)
    result['monotonicity_counterexample']=dict(source=special,correct=certificate['bound'],invalid_lower_only=wrong['bound'],
        ordinary_01=certificate['tables']['ordinary'][0,1],forced_right_01=certificate['tables']['right'][0,1])
    assert certificate['bound']==13 and wrong['bound']==3
    for name in ('wrong_source','invalid_root','negative_entry','underestimated_bound'):
        bad=copy.deepcopy(certificate)
        if name=='wrong_source':bad['source']='0'*64
        if name=='invalid_root':bad['roots'][0,3]=4
        if name=='negative_entry':bad['tables']['left'][0,0]=-1
        if name=='underestimated_bound':bad['tables']['ordinary'][0,3]-=1;bad['bound']-=1
        try:check(**special,certificate=bad)
        except ValueError as exc:result['negative_controls'].append(dict(name=name,rejected=True,reason=str(exc)))
        else:raise AssertionError(f'{name} accepted')
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat(),
        summary=dict(checked_small_policies=len(result['small']),adversary_states=sum(r['adversary']['states'] for r in result['small']),
            large_policies=len(result['large']),actual_new_audits=0))
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status=result['status'],summary=result['summary'],counterexample=result['monotonicity_counterexample'],
        large=[dict(n=r['n'],rule=r['rule'],proposal=r['proposal']['total'],production=r['certificate']['invoice']['total'],checking=r['checking']['total']) for r in result['large']]),default=g01.encode))


if __name__=='__main__':run(Path(sys.argv[1]))
