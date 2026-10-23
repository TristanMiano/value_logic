"""Exact stopped-path check of a finite multinomial PAC-Bayes confidence event."""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from time import perf_counter_ns

start = perf_counter_ns()
den = 10
prior_penalty = [((F(k,5)**k if k else 1) *
                  (F(10-k,5)**(10-k) if k<10 else 1)) for k in range(11)]

def crosses(counts, probs, delta):
    a,b,c = counts
    n = a+b+c
    cardinal = F((n+1)*(n+2),2)
    for k in range(11):
        # h1=(G,B,O), h2=(O,G,B) on the three primitive atoms.
        weighted = (k*b+(10-k)*c, k*a+(10-k)*b, k*c+(10-k)*a)
        true = ((k*probs[1]+(10-k)*probs[2])/10,
                (k*probs[0]+(10-k)*probs[1])/10,
                (k*probs[2]+(10-k)*probs[0])/10)
        likelihood = F(1)
        for z,p in zip(weighted,true):
            if z:
                assert p > 0
                likelihood *= (F(z,10*n)/p)**z
        # Raise both sides to ten: all comparisons remain rational/exact.
        if likelihood > (cardinal/delta)**10 * prior_penalty[k]:
            return True
    return False

records=[]
for probs in [(F(1,2),F(1,3),F(1,6)),(F(1,10),F(3,10),F(3,5)),
              (F(1,3),)*3,(F(0),F(1,2),F(1,2))]:
    for delta in (F(1,2),F(1,5),F(1,20)):
        active={(0,0,0):F(1)}
        failed=F(0)
        inspected=0
        for n in range(1,13):
            nxt=defaultdict(F)
            for counts,mass in active.items():
                for j,p in enumerate(probs):
                    if not p:
                        continue
                    dest=list(counts)
                    dest[j]+=1
                    nxt[tuple(dest)]+=mass*p
            active={}
            for counts,mass in nxt.items():
                inspected+=1
                if crosses(counts,probs,delta):
                    failed+=mass
                else:
                    active[counts]=mass
            assert failed+sum(active.values())==1
        assert failed <= delta
        records.append(dict(atom_probabilities=list(map(str,probs)),delta=str(delta),
            all_prefixes_through=12,posterior_grid_denominator=10,
            crossing_probability=str(failed),states_inspected=inspected))

def kl(x,y):
    return ((x*math.log(x/y) if x else 0) +
            ((1-x)*math.log((1-x)/(1-y)) if x<1 else 0))

def upper(b, allowance):
    if b==1:
        return 1.0
    lo=b
    hi=1.0
    for _ in range(70):
        mid=(lo+hi)/2
        if mid==1 or kl(b,mid)>allowance:
            hi=mid
        else:
            lo=mid
    return (lo+hi)/2

n=1500
released=1000
c=math.log(((n+1)*(n+2)/2)/.05)
endpoints=[upper(u/released,c/released) for u in range(21)]
assert all(a<=b for a,b in zip(endpoints,endpoints[1:]))
examples=dict(prefix=n,released=released,prior_mass=1,delta=.05,
    unknown_bad_upper_0_10_20=[endpoints[i] for i in (0,10,20)],
    endpoint_scope='Floating-point illustrations, not outward-rounded certificates.',
    mixture_example=dict(policy1_release='1/100',policy1_conditional_error='0',
      policy2_release='1',policy2_conditional_error='99/100',posterior='1/2 each',
      actual_conditional_error=str(F(99,101)),incorrect_average='99/200'))
result=dict(status='PASS',model='Codex (GPT-6)',python=platform.python_version(),
    source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
    exact_crossing_checks=records,examples=examples,
    elapsed_ns=perf_counter_ns()-start,
    scope='Finite exact stopped-path confidence checks; no independent theorem confirmation or workload benchmark.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
