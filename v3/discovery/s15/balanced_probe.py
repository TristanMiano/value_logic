"""Finite exact channel checks and floating sequential-KL arithmetic."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import math
import platform
import time

start=time.monotonic_ns()
inputs=zero_support_cases=0
for n in (4,6,8,10):
    m=n//2
    pairs=list(combinations(range(n),2))
    for bits in product((0,1),repeat=n):
        Q=(sum(bits)-m)**2
        p=F(sum(bits[i]==bits[j] for i,j in pairs),len(pairs))
        target=F(n-2,2*(n-1))+F(2*Q,n*(n-1))
        assert p==target
        inputs+=1
    for ones in range(n+1):
        for zeros in range(n-ones+1):
            free=n-ones-zeros
            if free and ones<=m<=ones+free:
                assert (ones<=m-1<=ones+free) or (ones<=m+1<=ones+free)
                zero_support_cases+=1

# Every deterministic adaptive depth-two binary-output tree on four bits.
tree_cases=0
n=4
cells={q:[] for q in (0,1,4)}
for bits in product((0,1),repeat=n): cells[(sum(bits)-2)**2].append(bits)
for first in range(n):
    rest=[i for i in range(n) if i!=first]
    for second0,second1 in product(rest,repeat=2):
        for leaves in product((0,1),repeat=4):
            u=F(leaves[1]+leaves[2],2)
            v=F(leaves[0]+leaves[3],2)
            for q,cell in cells.items():
                actual=F(sum(leaves[2*x[first]+x[second1 if x[first] else second0]]
                             for x in cell),len(cell))
                p=F(1,3)+F(q,6)
                assert actual==u+(v-u)*p
            tree_cases+=1

def kl(p,q):
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
examples=[]
epsilon=.01
decision_kl=(1-2*epsilon)*math.log((1-epsilon)/epsilon)
for n in (4,8,16,100):
    p0=F(n-2,2*(n-1))
    p1=p0+F(2,n*(n-1))
    div=kl(float(p0),float(p1))
    upper=math.ceil(n*n*(n-1)*(n-1)/2*math.log(2/epsilon))+1
    examples.append(dict(n=n,p0=str(p0),p1=str(p1),kl_01=div,
                         error_per_input=epsilon,
                         expected_episodes_lower=decision_kl/div,
                         expected_input_probes_lower=2*decision_kl/div,
                         sufficient_fixed_episodes=upper,
                         larger_cap_exact_episodes=math.ceil(math.log2(n//2+1)),
                         larger_cap=n+1))

out=dict(status='PASS',input_channel_equalities=inputs,
         balanced_partial_assignment_count_types=zero_support_cases,
         adaptive_depth_two_trees=tree_cases,examples=examples,
         source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         python=platform.python_version(),elapsed_ns=time.monotonic_ns()-start,
         scope='Exact finite channel/support/tree checks; KL arithmetic is floating, not an independently verified sequential lower-bound proof.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
