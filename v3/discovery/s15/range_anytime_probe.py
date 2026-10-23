"""Exact finite stopping-law checks; complete sequential evaluations only."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import platform
import time

start=time.monotonic_ns()
def cap(rank,zeta,theta,delta):
    a=theta/zeta
    b=(1-theta)/(1-zeta)
    R=0
    while a**R*b**rank<1/delta: R+=1
    return rank+R

def false_probability(probs,zeta,theta,delta):
    a=theta/zeta
    b=(1-theta)/(1-zeta)
    rank=len(probs)
    @lru_cache(None)
    def walk(j,R):
        if j==rank: return F(0)
        if a**R*b**j>=1/delta: return F(1)
        p=probs[j]
        return p*walk(j,R+1)+(1-p)*walk(j+1,R)
    return walk(0,0)

checks=[]
for rank in range(8):
    for delta in (F(1,10),F(1,100)):
        probs=[F(1,2**(rank-j)) for j in range(rank)]
        p=false_probability(probs,F(1,2),F(3,4),delta)
        assert p<=delta
        checks.append(dict(source='uniform_F2_image',rank=rank,delta=str(delta),
                           false_probability=str(p),cap=cap(rank,F(1,2),F(3,4),delta)))

# F3 map (x,y)->(x,x*y): exact masses of zero and each possible observed line.
points=[(x,x*y%3) for x in range(3) for y in range(3)]
assert points.count((0,0))==3
for y in range(3):
    line={(a,a*y%3) for a in range(3)}
    assert sum(p in line for p in points)==5
poly=false_probability([F(1,3),F(5,9)],F(2,3),F(5,6),F(1,10))
assert poly<=F(1,10)

caps=[]
z=F(4,257)
delta=F(1,1000)
for rank in (0,1,4,16,128):
    R=0
    while sum(F(1,2)*(theta/z)**R*((1-theta)/(1-z))**rank
              for theta in (F(1,2),F(1,10)))<1/delta:
        R+=1
    caps.append(dict(rank=rank,theta_half_cap=cap(rank,z,F(1,2),delta),
                     theta_tenth_cap=cap(rank,z,F(1,10),delta),mixture_cap=rank+R,
                     earlier_consecutive_three_cap=3*(rank+1)))
assert caps[2]['theta_half_cap']==7

stale_count=0
while F(3,2)**stale_count<10: stale_count+=1
assert stale_count==6 and stale_count<8
out=dict(status='PASS',linear_cases=checks,
         polynomial_case=dict(source='F3:(x,y)->(x,x*y)',false_probability=str(poly),
                              delta='1/10',cap=cap(2,F(2,3),F(5,6),F(1,10))),
         cap_examples=caps,
         stale_span_counterexample=dict(source='identity_F2_dimension8',
             probes_before_false_certificate=stale_count,false_certificate_probability='1',
             reason='Reclassifying each probe as belonging to the span after adding it makes every indicator one; six vectors cannot span dimension eight.'),
         source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         python=platform.python_version(),elapsed_ns=time.monotonic_ns()-start,
         scope='Exact finite laws and cap arithmetic; no measured acquisition cost or asynchronous cap.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
