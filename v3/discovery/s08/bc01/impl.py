"""bc01 exact model policy-improvement screens; no cost acquisition."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import sys
import anchor_cover as ac
import graph_cover_service as gs
HERE=Path(__file__).resolve().parent;g01=ac.g01;Meter=ac.Meter

class Planner:
    def __init__(self,supports,fees,quota,utility,depth):
        self.supports=supports;self.fees=fees;self.quota=quota;self.utility=utility;self.depth=depth;self.C=fees[-1];self.meter=Meter()
        self.value=lru_cache(None)(self._value)
    def _value(self,state,budget,depth):
        self.meter.pay('lookahead','state_and_terminal',4+len(state))
        if self.utility(state,self.meter)==self.quota:return F(0),None
        if depth==0:return F(self.C),len(state)-1
        best=(F(self.C),len(state)-1)
        for i,old in enumerate(state[:-1]):
            if old is not None or self.fees[i]>budget:continue
            mean=F(self.fees[i]);parts=[]
            for v in self.supports[i]:
                child=list(state);child[i]=v
                parts.append(self.value(tuple(child),budget-self.fees[i],depth-1)[0]);self.meter.pay('lookahead','response_and_rational_mean',10+len(state))
            mean+=sum(parts,F())/len(parts)
            if mean<best[0]:best=(mean,i)
        return best
    def choose(self,state,budget):return self.value(tuple(state),budget,self.depth)[1]

def stars(root):
    design=json.loads((HERE/'ac01/design.json').read_text());records=[]
    for case in design['cases']:
        data=ac.op.source(case);supports=data['supports'];Q=case['H']*sum(case['weights']);case_rows=[]
        for depth in(1,2):
            p=Planner(supports,case['fees'],Q,lambda s,m:ac.utility(case,s,m),depth);initial=(None,)*len(supports);bound=p.value(initial,p.C,depth)[0];total=F();saving=F();worst=0;worlds=0;queries=0
            for world in product(*supports):
                state=list(initial);budget=p.C;paid=0;credits=F()
                while True:
                    i=p.choose(state,budget)
                    if i is None:break
                    if i<len(state)-1:
                        completion=0
                        for v in supports[i]:
                            child=state.copy();child[i]=v;completion+=ac.utility(case,child,Meter())==Q
                        credits+=F(p.C*completion,len(supports[i]))-case['fees'][i];budget-=case['fees'][i]
                    state[i]=world[i];paid+=case['fees'][i];queries+=1
                assert ac.utility(case,state,Meter())==Q and paid<=2*p.C
                ac.action(case,state,Meter());total+=paid;saving+=credits;worst=max(worst,paid);worlds+=1
            mean=total/worlds;assert mean<=bound<=p.C and mean==p.C-saving/worlds
            case_rows.append(dict(depth=depth,expected_fee=mean,initial_upper=bound,anchor_fee=p.C,worst_fee=worst,worlds=worlds,diagnostic_queries=queries,states=p.value.cache_info().currsize,invoice=p.meter.record()))
        records.append(dict(name=case['name'],policies=case_rows))
    g01.save(root/'stars.json',dict(status='complete',physical_audits=0,cases=records))

def graph(root,name):
    design=json.loads((HERE/'gc02/design.json').read_text());case=next(c for c in design['cases'] if c['name']==name);e=json.loads((HERE/'gc02'/f'{name}_evidence.json').read_text());data=e['source'];K=e['cut']['bound'];Q=data['H']*(2*sum(w for a,b,w in data['edges'])-K);state=(None,)*len(data['supports']);values=[]
    for depth in(1,2):
        p=Planner(data['supports'],data['audit_costs'],Q,lambda s,m:gs.gc.utility(data,s,K,m),depth);bound,query=p.value(state,p.C,depth)
        values.append(dict(depth=depth,initial_upper=bound,anchor_fee=p.C,initial_query=query,strict_improvement=bound<p.C,states=p.value.cache_info().currsize,invoice=p.meter.record()))
    g01.save(root/f'{name}.json',dict(status='complete',physical_audits=0,values=values))

if __name__=='__main__':
    root=HERE/'bc01';root.mkdir(exist_ok=True)
    if sys.argv[1]=='stars':stars(root)
    else:graph(root,sys.argv[1])
