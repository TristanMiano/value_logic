"""Ordinary DIRECT control on explicitly expanded source worlds, DEVELOPMENT."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys
import observation_policy as op
import policy_safety as safe
g01=op.g01;Meter=op.Meter;HERE=Path(__file__).resolve().parent

def words(integer):return max(1,(integer.bit_length()+63)//64)

def matrix(case,price,tau,meter):
    data=op.source(case);worlds=list(product(*data['supports']));n=len(case['weights']);actions=[dict(kind='replace',count=None)]+[dict(kind='repair',count=list(k)) for k in product((0,1,2),repeat=n)]
    regions=[0]*len(actions);tests=[{v:0 for v in support} for support in data['supports']]
    for h,row in enumerate(worlds):
        opt=min(price,row[-1]+sum(2*w*min(row[0],row[i]) for i,w in enumerate(case['weights'],1)))
        for i,v in enumerate(row):tests[i][v]|=1<<h;meter.pay('region_build','world_query_signature_words',4+words(1<<h))
        for a,action in enumerate(actions):
            cost=price if a==0 else row[-1]+sum(w*(k*row[i]+(2-k)*row[0]) for i,(w,k) in enumerate(zip(case['weights'],action['count']),1))
            if cost-opt<=tau:regions[a]|=1<<h
            meter.pay('region_build','source_action_world_loss_and_region_bit',10+10*n+words(1<<h))
    kept=[]
    for i,region in enumerate(regions):
        if not region:continue
        dominated=False
        for j,other in enumerate(regions):
            meter.pay('region_build','bitset_region_containment',4+max(words(region),words(other)))
            if i!=j and region&~other==0 and(region!=other or j<i):dominated=True;break
        if not dominated:kept.append(i)
    actions=[actions[i] for i in kept];regions=[regions[i] for i in kept];classes={};members=[]
    for h,row in enumerate(worlds):
        mask=sum(1<<i for i,region in enumerate(regions) if region>>h&1)
        if not mask:raise AssertionError('Action regions do not cover a supported world')
        classes[mask]=classes.get(mask,0)|(1<<h);members.append(mask)
        meter.pay('region_build','membership_signature_and_class_bitset',5+len(regions)+words(1<<h))
    return dict(source=data['identity'],worlds=worlds,actions=actions,regions=regions,classes=classes,members=members,tests=tests,full=(1<<len(worlds))-1)

class Score:
    def __init__(self,table,meter):self.table=table;self.meter=meter;self.cache={};self.max_bits=0
    def get(self,V):
        if not V:raise ValueError('Empty supported version set')
        if V in self.cache:self.meter.pay('scoring','cached_version_bitset_lookup',2+words(V));return self.cache[V]
        table=self.table;N=V.bit_count();counts=[]
        for mask,bits in table['classes'].items():
            count=(V&bits).bit_count()
            if count:counts.append((mask,count))
            self.meter.pay('scoring','class_mass_bitset_intersection',3+words(V))
        edges=[];q=1
        for a in range(len(table['regions'])):
            inside=sum(count for mask,count in counts if mask>>a&1)
            outside_squares=sum(count*count for mask,count in counts if not(mask>>a&1))
            e=(N*N-inside*inside-outside_squares)//2
            self.meter.pay('scoring','ecd_mass_square_and_sum',8+8*len(counts))
            self.meter.pay('scoring','residual_product_word_operations',2+words(q)*words(e));q*=e;edges.append(e)
        self.cache[V]=(q,edges);self.max_bits=max(self.max_bits,q.bit_length());return q,edges
    def gains(self,V,unknown,case):
        q,_=self.get(V);N=V.bit_count();result=[]
        for i in unknown:
            remaining=0
            for bits in self.table['tests'][i].values():
                child=V&bits;self.meter.pay('scoring','query_response_bitset',3+words(V))
                if child:
                    qq,_=self.get(child);mass=child.bit_count();remaining+=mass*qq
                    self.meter.pay('scoring','response_expectation_word_operations',3+words(mass)*words(qq))
            gain=N*q-remaining
            if gain<0:raise AssertionError('Negative direct gain')
            result.append((gain,case['fees'][i],i));self.meter.pay('scoring','exact_query_gain',4+words(N*q))
        return result

def decision(case,state,price,tau,action,meter):
    known={i:v for i,v in enumerate(state[:-1]) if v is not None};a=state[-1];loA,hiA=(0,case['A']) if a is None else(a,a)
    count=action['count'] if action['kind']=='repair' else [1]*len(case['weights'])
    R,U,L=op.ps.endpoint_metrics(case['weights'],case['H'],known,count,meter)
    bound=max(R,U+hiA-price) if action['kind']=='repair' else max(0,price-L-loA)
    if bound>tau:raise AssertionError('Region action fails source endpoint check')
    return dict(kind=action['kind'],count=action['count'],bound=bound)

def compile_policy(case,price,tau,geometry):
    data=op.source(case);meter=Meter();op.admit(case,data,geometry,meter);root=(None,)*len(data['supports']);first=op.terminal(case,root,price,tau,meter)
    if first is not None:
        policy=dict(source=data['identity'],price=price,tau=tau,root=op.state_key(root),value=0,nodes={op.state_key(root):dict(value=0,action=first)})
        return policy,None,dict(invoice=meter.record(),fast_root=True,expanded_worlds=0,retained_regions=0,classes=0,expected_fee=0,scored_versions=0,max_product_bits=0)
    table=matrix(case,price,tau,meter);score=Score(table,meter);nodes={};expected={}
    def visit(state,V):
        key=op.state_key(state)
        if key in nodes:return nodes[key]['value'],expected[key]
        for a,region in enumerate(table['regions']):
            meter.pay('selection','region_containment_terminal',3+words(V))
            if V&~region==0:
                action=decision(case,state,price,tau,table['actions'][a],meter);nodes[key]=dict(value=0,action=action);expected[key]=F(0);return 0,F(0)
        gains=score.gains(V,[i for i,v in enumerate(state) if v is None],case);chosen=None
        for gain,fee,i in gains:
            if chosen is None or gain*chosen[1]>chosen[0]*fee or(gain*chosen[1]==chosen[0]*fee and i<chosen[2]):chosen=(gain,fee,i)
            meter.pay('selection','rational_gain_cross_product_comparison',6+words(gain)*words(fee))
        _,fee,i=chosen;children=[];average=F(0);N=V.bit_count()
        for value,bits in table['tests'][i].items():
            child=list(state);child[i]=value;VV=V&bits
            if not VV:continue
            worst,mean=visit(tuple(child),VV);children.append(worst);average+=F(VV.bit_count(),N)*mean
            meter.pay('selection','chosen_policy_branch_and_expected_fee',10+len(state))
        worst=fee+max(children);average+=fee;nodes[key]=dict(query=i,value=worst);expected[key]=average;return worst,average
    V,average=visit(root,table['full']);policy=dict(source=data['identity'],price=price,tau=tau,root=op.state_key(root),value=V,nodes=nodes)
    return policy,table,dict(invoice=meter.record(),fast_root=False,expanded_worlds=len(table['worlds']),retained_regions=len(table['regions']),classes=len(table['classes']),expected_fee=average,scored_versions=len(score.cache),max_product_bits=score.max_bits)

def screen(case,price,tau,table):
    meter=Meter()
    if table is None:table=matrix(case,price,tau,meter)
    score=Score(table,meter);states={};identities=pair_checks=adaptive_checks=0
    supports=op.source(case)['supports']
    for state in product(*[(None,*s) for s in supports]):
        V=table['full']
        for i,v in enumerate(state):
            if v is not None:V&=table['tests'][i][v]
        common=any(V&~r==0 for r in table['regions']);exact=op.terminal(case,state,price,tau,Meter()) is not None
        q,edges=score.get(V);assert common==exact==(q==0);identities+=1
        # Explicit class pairs, independently of the sum-of-squares formula.
        counts=Counter(table['members'][h] for h in range(len(table['worlds'])) if V>>h&1)
        for a,e in enumerate(edges):
            classes=Counter()
            for mask,count in counts.items():classes[-1 if mask>>a&1 else mask]+=count
            masses=list(classes.values());brute=sum(x*y for j,x in enumerate(masses) for y in masses[j+1:]);assert brute==e;pair_checks+=1
        gains={i:F(gain,V.bit_count()) for gain,fee,i in score.gains(V,[i for i,v in enumerate(state) if v is None],case)}
        states[state]=(V,gains)
    for state,(V,gains) in states.items():
        for j,v in enumerate(state):
            if v is not None:continue
            for response in supports[j]:
                child=list(state);child[j]=response;_,child_gains=states[tuple(child)]
                for i,gain in child_gains.items():
                    assert gains[i]>=gain,(state,j,response,i,gains[i],gain);adaptive_checks+=1
    return dict(partial_states=len(states),terminal_equivalences=identities,edge_pair_checks=pair_checks,adaptive_comparisons=adaptive_checks,invoice=meter.record())

def run(root,case,price,tau):
    old=HERE/'op01';geometry=json.loads((old/f"{case['name']}_geometry.json").read_text());directory=root/f"{case['name']}_{price}_{tau}";directory.mkdir(exist_ok=False)
    policy,table,preparation=compile_policy(case,price,tau,geometry);(directory/'policy.json').write_text(json.dumps(policy,separators=(',',':'))+'\n');g01.save(directory/'preparation.json',preparation)
    meter=Meter();checked=safe.check(case,policy,geometry,meter);g01.save(directory/'checking.json',dict(**checked,invoice=meter.record()))
    if len(case['weights'])==2:g01.save(directory/'screen.json',screen(case,price,tau,table))
    print(case['name'],price,tau,len(policy['nodes']),preparation['invoice']['total'],preparation['expected_fee'],flush=True)

if __name__=='__main__':
    root=Path(sys.argv[1]);design=json.loads((root/'design.json').read_text())
    if g01.sha(__file__)!=design['source_sha256']:raise ValueError('Changed implementation')
    case=next(c for c in design['cases'] if c['name']==sys.argv[2]);run(root,case,int(sys.argv[3]),int(sys.argv[4]))
