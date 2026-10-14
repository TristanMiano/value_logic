"""Ordinary stochastic cover for one exact duty. Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys
import observation_policy as op
import policy_safety as safe
g01=op.g01;Meter=op.Meter;HERE=Path(__file__).resolve().parent

def utility(case,state,meter):
    H=case['H'];Q=H*sum(case['weights'])
    if state[-1] is not None:meter.pay('cover','observed_anchor_covers',2);return Q
    center=0 if state[0] is None else H-state[0];value=0
    for i,w in enumerate(case['weights'],1):
        leaf=0 if state[i] is None else H-state[i];value+=2*w*max(center,leaf);meter.pay('cover','weighted_edge_maximum_score',7)
    return min(Q,value)

def choose(case,state,meter):
    H=case['H'];Q=H*sum(case['weights']);score=utility(case,state,meter)
    if score==Q:return None
    supports=op.source(case)['supports'];best=None
    for i,v in enumerate(state):
        if v is not None:continue
        gain=0
        for response in supports[i]:
            child=list(state);child[i]=response;gain+=utility(case,child,meter)-score
        candidate=F(gain,len(supports[i])*case['fees'][i]);meter.pay('selection','expected_cover_gain_per_fee',10+len(supports[i]))
        if best is None or candidate>best[0]:best=(candidate,i)
    if best is None or best[0]<=0:raise AssertionError('No useful query before full cover')
    return best[1]

def action(case,state,meter):
    H=case['H'];tau=H*sum(case['weights']);price=case['A'];n=len(case['weights'])
    if case['A']!=10*tau:raise ValueError('Specialized anchor-price/tolerance relation changed')
    if utility(case,state,meter)<tau:raise ValueError('Duty uncovered')
    if state[-1]==price:return dict(kind='replace',count=None,bound=0)
    if state[-1]==0:count=[1]*n
    else:
        upper=H if state[0] is None else state[0]
        count=[2 if(v is not None and v<upper) else 0 for v in state[1:-1]]
    known={i:v for i,v in enumerate(state[:-1]) if v is not None};R,U,L=op.ps.endpoint_metrics(case['weights'],H,known,count,meter)
    hiA=price if state[-1] is None else state[-1];bound=max(R,U+hiA-price)
    if bound>tau:raise AssertionError('Cover does not warrant action')
    return dict(kind='repair',count=count,bound=bound)

def compile_policy(case,geometry):
    data=op.source(case);meter=Meter();op.admit(case,data,geometry,meter);supports=data['supports'];nodes={};means={};tau=case['H']*sum(case['weights'])
    def visit(state):
        key=op.state_key(state)
        if key in nodes:return nodes[key]['value'],means[key]
        query=choose(case,state,meter)
        if query is None:nodes[key]=dict(value=0,action=action(case,state,meter));means[key]=F(0);return 0,F(0)
        children=[];averages=[]
        for v in supports[query]:
            child=list(state);child[query]=v;worst,mean=visit(tuple(child));children.append(worst);averages.append(mean)
            meter.pay('compilation','selected_cover_policy_response',7+len(state))
        value=case['fees'][query]+max(children);mean=case['fees'][query]+sum(averages,F())/len(averages)
        nodes[key]=dict(value=value,query=query);means[key]=mean;return value,mean
    root=op.state_key((None,)*len(supports));value,mean=visit((None,)*len(supports));policy=dict(source=data['identity'],price=case['A'],tau=tau,root=root,value=value,nodes=nodes)
    return policy,dict(expected_fee=mean,invoice=meter.record(),states=len(nodes))

def finite(case):
    supports=op.source(case)['supports'];tau=case['H']*sum(case['weights']);utilities={};checks=0
    for state in product(*[(None,*s) for s in supports]):
        g=utility(case,state,Meter());exact=op.terminal(case,state,case['A'],tau,Meter());assert (g==tau)==(exact is not None);utilities[state]=g
        if g==tau:action(case,state,Meter())
    for state,g in utilities.items():
        unseen=[i for i,v in enumerate(state) if v is None]
        for ii,i in enumerate(unseen):
            for j in unseen[ii+1:]:
                for a in supports[i]:
                    left=list(state);left[i]=a
                    for b in supports[j]:
                        right=list(state);right[j]=b;both=left.copy();both[j]=b
                        assert utilities[tuple(left)]+utilities[tuple(right)]>=g+utilities[tuple(both)];checks+=1
    return dict(partial_states=len(utilities),terminal_equivalences=len(utilities),pointwise_submodular_comparisons=checks,physical_audits=0)

def run(root,case):
    directory=root/case['name'];directory.mkdir(exist_ok=False);geometry=json.loads((HERE/'op01'/f"{case['name']}_geometry.json").read_text())
    policy,prep=compile_policy(case,geometry);meter=Meter();checked=safe.check(case,policy,geometry,meter)
    (directory/'policy.json').write_text(json.dumps(policy,separators=(',',':'))+'\n');g01.save(directory/'preparation.json',prep);g01.save(directory/'checking.json',dict(**checked,invoice=meter.record()));g01.save(directory/'screen.json',finite(case));print(case['name'],prep['expected_fee'],policy['value'],prep['invoice']['total'],meter.total,flush=True)

if __name__=='__main__':
    root=Path(sys.argv[1]);design=json.loads((root/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==sys.argv[2]);run(root,case)
