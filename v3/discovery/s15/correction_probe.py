"""Exact finite information-bound screens; no performance or coverage experiment."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb
import hashlib
import json
from pathlib import Path
from time import perf_counter_ns

HERE = Path(__file__).resolve().parent
OUT = HERE/'correction_probe.json'
assert not OUT.exists(), 'Preserve exposed outputs.'
started = perf_counter_ns()
collision_cases = 0
equalities = 0
for n,q in [(4,3),(6,3),(8,2)]:
    for e in product(range(q),repeat=n):
        counts = Counter(e)
        beta = sum(F(v,n)**2 for v in counts.values())
        if beta <= F(1,2):
            continue
        for x in range(n):
            prob = F(sum(e[(r+x)%n]==e[r] for r in range(n)),n)
            assert prob**2 >= 2*beta-1
            collision_cases += 1
            equalities += prob**2 == 2*beta-1

witnesses = []
for n in [8,16,32]:
    for minority in range(n//2+1):
        e = [int(i<minority) for i in range(n)]
        beta = F(minority,n)**2+F(n-minority,n)**2
        prob = F(sum(e[(r+n//2)%n]==e[r] for r in range(n)),n)
        assert prob**2 == 2*beta-1
        witnesses.append(dict(n=n,minority=minority,beta=str(beta),success=str(prob)))

laws = [tuple(F(z,sum(w)) for z in w) for w in
        [(1,1,1,1),(1,0,0,0),(4,3,2,1),(3,0,1,0),(1,2,2,1)]]
approx_cases = 0
for e in product(range(3),repeat=4):
    for law in laws:
        for epsilon in [F(0),F(1,2),F(1),F(2)]:
            beta = sum(law[u]*law[v] for u in range(4) for v in range(4)
                       if abs(e[u]-e[v])<=epsilon)
            for x in range(4):
                shifted = tuple(law[(j-x)%4] for j in range(4))
                rho = sum(abs(a-b) for a,b in zip(law,shifted))/2
                success = sum(law[r] for r in range(4)
                              if abs(e[(r+x)%4]-e[r])<=2*epsilon)
                assert success >= max(0,2*beta-1-rho)
                approx_cases += 1

offset = dict(n=8,offset=1,absolute_correct=0,translated_correct=0)
f = lambda x: 3*x%8
g = lambda x: (f(x)+1)%8
offset['absolute_correct'] = sum(f(x)==g(x) for x in range(8))
offset['translated_correct'] = sum((g((x+r)%8)-g(r))%8==f(x)
                                  for x in range(8) for r in range(8))
assert offset['absolute_correct']==0 and offset['translated_correct']==64

def tail(k,p):
    return sum(F(comb(k,j))*p**j*(1-p)**(k-j) for j in range(k//2+1))
ks = [k for k in range(1,100,2) if tail(k,F(7,10))<=F(1,100)]
assert ks
k = min(ks)
assert k==1 or tail(k-2,F(7,10))>F(1,100)

result = dict(status='PASS',classification='DEVELOPMENT; exact finite information bounds',
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              elapsed_ns=perf_counter_ns()-started,collision_shift_cases=collision_cases,
              collision_equalities=equalities,sharp_witnesses=witnesses,
              approximate_translation_cases=approx_cases,offset_example=offset,
              p07_target001=dict(first_odd_k=k,tail=str(tail(k,F(7,10))),model_calls=2*k),
              no_translation_budget_counterexample=dict(beta=1,epsilon='1/2',
                    law='point mass at0',residual='e(0)=0,e(1)=2',target=1,success=0,rho=1))
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:val for key,val in result.items() if key!='sharp_witnesses'},indent=2))
