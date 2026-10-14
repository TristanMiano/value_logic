"""Exact expected/worst physical-fee frontier, Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys
import observation_policy as op
import policy_safety as safe
g01=op.g01;Meter=op.Meter;HERE=Path(__file__).resolve().parent

def build(case,original,meter):
    nodes=original['nodes'];fees=case['fees'];supports=op.source(case)['supports'];maxB=sum(fees);values={};choices={}
    for key in sorted(nodes,key=lambda x:x.count('_')):
        node=nodes[key];state=op.state_from(key)
        if 'action' in node:
            for B in range(maxB+1):values[key,B]=F(0)
            continue
        options=[i for i,v in enumerate(state) if v is None]
        for B in range(maxB+1):
            candidates=[]
            for i in options:
                if fees[i]>B:continue
                means=[]
                for v in supports[i]:
                    child=list(state);child[i]=v;means.append(values[op.state_key(child),B-fees[i]])
                    meter.pay('tradeoff','budget_child_value_and_probability',10+len(state))
                if any(m is None for m in means):continue
                expect=fees[i]+sum(means,F(0))/len(means);candidates.append((expect,i))
                meter.pay('tradeoff','exact_expected_query_candidate',10+sum(max(1,m.denominator.bit_length()//64+1) for m in means))
            if candidates:
                mean,i=min(candidates);values[key,B]=mean;choices[key,B]=i
            else:values[key,B]=None
    root=original['root'];curve=[dict(cap=B,expected=values[root,B],query=choices.get((root,B))) for B in range(maxB+1) if values[root,B] is not None]
    assert curve[0]['cap']==original['value']
    def extract(B):
        selected={};reached={}
        def visit(key,budget):
            # A query path can reach one observation state with the same total spent
            # irrespective of order, since fees are fixed and each coordinate is unique.
            if key in selected:
                assert reached[key]==budget;return selected[key]['value']
            reached[key]=budget;node=nodes[key]
            if 'action' in node:selected[key]=dict(node);return 0
            i=choices[key,budget];state=op.state_from(key);worsts=[]
            for v in supports[i]:
                child=list(state);child[i]=v;worsts.append(visit(op.state_key(child),budget-fees[i]))
            worst=fees[i]+max(worsts);selected[key]=dict(query=i,value=worst);return worst
        worst=visit(root,B)
        return dict(source=original['source'],price=original['price'],tau=original['tau'],root=root,value=worst,nodes=selected)
    return curve,extract(curve[0]['cap']),extract(maxB),len(values)

def evaluate(case,policy):
    supports=op.source(case)['supports'];fees=[]
    for world in product(*supports):
        state=[None]*len(supports);cost=0
        while True:
            node=policy['nodes'][op.state_key(state)]
            if 'action' in node:break
            i=node['query'];assert state[i] is None;state[i]=world[i];cost+=case['fees'][i]
        fees.append(cost)
    assert max(fees)==policy['value']
    return dict(expected=F(sum(fees),len(fees)),worst=max(fees),worlds=len(fees),total_fee=sum(fees))

def cheapest(case,original):
    supports=op.source(case)['supports'];nodes={}
    def visit(key):
        if key in nodes:return nodes[key]['value']
        node=original['nodes'][key]
        if 'action' in node:nodes[key]=dict(node);return 0
        state=op.state_from(key);i=min((i for i,v in enumerate(state) if v is None),key=lambda i:(case['fees'][i],i));children=[]
        for v in supports[i]:
            child=list(state);child[i]=v;children.append(visit(op.state_key(child)))
        worst=case['fees'][i]+max(children);nodes[key]=dict(value=worst,query=i);return worst
    value=visit(original['root']);return dict(source=original['source'],price=original['price'],tau=original['tau'],root=original['root'],value=value,nodes=nodes)

def run(root,case,price,tau):
    label=f"{case['name']}_{price}_{tau}";old=HERE/'op01'/(label+'_policy');original=json.loads((old/'policy.json').read_text());geometry=json.loads((HERE/'op01'/f"{case['name']}_geometry.json").read_text());directory=root/label;directory.mkdir(exist_ok=False)
    meter=Meter();curve,lex,mean,states=build(case,original,meter);policies=dict(original_minimax=safe.extract(case,original,Meter()),lexicographic=lex,expected=mean,cheapest=cheapest(case,original),direct=json.loads((HERE/'dr01'/label/'policy.json').read_text()));scores={}
    for name,policy in policies.items():
        cm=Meter();checked=safe.check(case,policy,geometry,cm);score=evaluate(case,policy);scores[name]=dict(**score,safety_units=cm.total,states=checked['reachable_states'])
        if name in('lexicographic','expected'):(directory/(name+'.json')).write_text(json.dumps(policy,separators=(',',':'))+'\n')
    assert scores['lexicographic']['expected']==curve[0]['expected'] and scores['expected']['expected']==curve[-1]['expected']
    assert scores['lexicographic']['worst']==scores['original_minimax']['worst']
    assert scores['lexicographic']['expected']<=scores['original_minimax']['expected']
    for a,b in zip(curve,curve[1:]):assert a['expected']>=b['expected']
    g01.save(directory/'results.json',dict(curve=curve,scores=scores,budget_states=states,invoice=meter.record(),parent_policy_sha256=g01.sha(old/'policy.json'),physical_audits=0,status='complete'))
    print(label,{k:str(v['expected']) for k,v in scores.items()},flush=True)

if __name__=='__main__':
    root=Path(sys.argv[1]);design=json.loads((root/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==sys.argv[2]);run(root,case,int(sys.argv[3]),int(sys.argv[4]))
