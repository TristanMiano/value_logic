"""Exact finite checks for arrival-order evidence with partial proof receipts."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math
import platform
import time

start=time.monotonic_ns()
def maxprefix(factors):
    p=m=F(1)
    for f in factors:
        p*=f
        m=max(m,p)
    return p,m

n=12
valid=invalid=0
for ys in product((0,1), repeat=n):
    valid += maxprefix([F(3,2) if y==0 else F(1,2) for y in ys])[1]>=4
    invalid += F(3,2)**ys.count(0)>=4
assert F(valid,2**n)<=F(1,4)
assert F(invalid,2**n)>F(9,10)

partial_cases=0
for states in product(range(3), repeat=8):
    ys=[int(s==0) for s in states] # 0=bad,1=unresolved good,2=proved good
    us=[int(s!=2) for s in states]
    a=b=F(1)
    for y,u in zip(ys,us):
        a*=F(3,2)-u
        b*=F(3,2)-y
        assert a<=b
    partial_cases+=1

class Tree:
    def __init__(self, values):
        self.size=1
        while self.size<len(values): self.size*=2
        self.nodes=[(F(1),F(1)) for _ in range(2*self.size)]
        self.updates=0
        for i,x in enumerate(values): self.set(i,x)
    def set(self,i,x):
        j=self.size+i
        self.nodes[j]=(x,max(F(1),x))
        j//=2
        while j:
            p,m=self.nodes[2*j]
            q,r=self.nodes[2*j+1]
            self.nodes[j]=(p*q,max(m,p*r))
            self.updates+=1
            j//=2

tree_checks=0
for length in (7,16,65,128):
    factors=[F(1,2)]*length
    tr=Tree(factors)
    assert tr.nodes[1]==maxprefix(factors)
    previous=tr.nodes[1][1]
    # Nonchronological, deterministic proof order; every third case stays pending.
    order=list(range(length-1,-1,-2))+list(range(0,length,2))
    seen=set()
    for i in order:
        if i in seen or i%3==0: continue
        seen.add(i)
        factors[i]=F(3,2)
        before=tr.updates
        tr.set(i,factors[i])
        assert tr.updates-before==int(math.log2(tr.size))
        assert tr.nodes[1]==maxprefix(factors)
        assert tr.nodes[1][1]>=previous
        previous=tr.nodes[1][1]
        tree_checks+=1

examples=[]
for n,g in ((1500,1470),(5000,4900),(100,100)):
    u=n-g
    theta=.5
    delta=.05
    A=math.exp((math.log(1/delta)-u*math.log1p(-theta))/g)
    upper=(A-1)/(A-1+theta)
    examples.append(dict(cases=n,proved_good=g,unresolved_or_bad=u,
                         theta=theta,delta=delta,upper_risk=upper))

out=dict(status='PASS',null_sequences=2**12,
         valid_ever_cross= str(F(valid,2**12)),
         completed_only_false_cross=str(F(invalid,2**12)),
         partial_states=partial_cases,tree_updates_checked=tree_checks,
         fixed_prefix_examples=examples,
         source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         python=platform.python_version(),elapsed_ns=time.monotonic_ns()-start,
         scope='Exact finite enumeration at p0=p=.5, theta=.5, delta=.25; not a universal proof, cost experiment or empirical risk estimate.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
