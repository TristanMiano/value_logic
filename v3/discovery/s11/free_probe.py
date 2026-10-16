"""DEVELOPMENT exact expectation checks for execution-only feedback."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import math
from matching_core import matching_orders,sparse_delta
from free_core import EventTree
from local_feedback import stopping


def event(order,edges,world,stop):
    receipts={};edge_set=set(edges)
    for i in order:
        receipts[i]=world[i]
        if stop(receipts):
            if i-1 in edge_set:return i-1,'edge'
            if i in edge_set:return None,None
            return (i,'singleton') if i<len(world)-1 else (None,None)
    return None,None


def case(index):
    n=(4,5,6,7)[index];mode=('sum','sum','dnf','two_sided')[index];threshold=(1,3,0,4)[index]
    family=matching_orders(n);fees=[1+(j*3%7) for j in range(n)]
    stop=lambda r:stopping(r,mode,threshold,n);gamma=F(1,5)
    counts={'world_weight_panels':0,'execution_events':0,'mean_coordinates':0,
            'event_probability_checks':0,'variance_checks':0,'uniform_lower_checks':0}
    for scheme in range(3):
        weights=[F(1) if scheme==0 else F(1+(j*7+scheme)%9,1+(j*2+scheme)%5) for j in range(n-1)]
        masses=[]
        for _,edges in family:
            mass=F(1)
            for j in edges:mass*=weights[j]
            masses.append(mass)
        total=sum(masses,F(0));Q=[v/total for v in masses];P=[(1-gamma)*q+gamma/F(len(family)) for q in Q]
        qe=[sum((q for q,(_,e) in zip(Q,family) if j in e),F(0)) for j in range(n-1)]
        qs=[sum((q for q,(_,e) in zip(Q,family) if j not in e and j-1 not in e),F(0)) for j in range(n-1)]
        pe=[sum((p for p,(_,e) in zip(P,family) if j in e),F(0)) for j in range(n-1)]
        ps=[sum((p for p,(_,e) in zip(P,family) if j not in e and j-1 not in e),F(0)) for j in range(n-1)]
        tree=EventTree(n)
        for j,w in enumerate(weights):tree.update(j,math.log(float(w)))
        for j in range(n-1):
            assert abs(tree.event_probability(j,'edge')-float(qe[j]))<1e-12
            assert abs(tree.event_probability(j,'singleton')-float(qs[j]))<1e-12
            counts['event_probability_checks']+=2
            if scheme==0:
                assert qe[j]>=F(1,5) and qs[j]>=F(1,3);counts['uniform_lower_checks']+=2
        for world in product((0,1),repeat=n):
            expected=[F(0)]*(n-1);variance=F(0)
            for p,(order,edges) in zip(P,family):
                j,kind=event(order,edges,world,stop);counts['execution_events']+=1
                if kind:
                    estimate=F(-fees[j],pe[j]) if kind=='edge' else F(fees[j+1],ps[j])
                    expected[j]+=p*estimate;variance+=p*qe[j]*estimate*estimate
            true,_,_=sparse_delta(dict(enumerate(world)),n,fees,stop)
            assert expected==[true.get(j,F(0)) for j in range(n-1)],(n,world,expected,true)
            assert variance<=max(fees)**2*(3/gamma+2/(1-gamma))
            counts['world_weight_panels']+=1;counts['mean_coordinates']+=n-1;counts['variance_checks']+=1
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'n':n,'mode':mode,
      'threshold':threshold,'policies':len(family),'counts':counts,'gamma':str(gamma),
      'hashes':{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in
      ('free_core.py','free_probe.py','matching_core.py','local_feedback.py')},
      'scope':'Exact finite mean and variance identities; numerical partition probability checks. Not confirmation.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
