"""Exact, tiny development checks; no sampled population or CPU claim."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
from time import perf_counter_ns

HERE = Path(__file__).resolve().parent
OUT = HERE/'drift_probe.json'
assert not OUT.exists()
start = perf_counter_ns()


def shifted_law(lower, alpha):
    law = defaultdict(F)
    law[F(0)] += alpha
    remain, weight = 1-alpha, F(1,len(lower))
    for d in sorted(lower):
        add = min(remain,weight)
        law[F(d)] += add
        remain -= add
        if remain == 0:
            break
    assert sum(law.values()) == 1
    return dict(law)


def primal(law,rho):
    mass, budget = F(0), rho
    for d,w in sorted(law.items()):
        if d == 0:
            mass += w
        else:
            move = min(w,budget/d)
            mass += move
            budget -= move*d
    return mass


def dual(law,rho):
    points = {F(0)} | {1/d for d in law if d>0}
    return min(lam*rho+sum(w*max(0,1-lam*d) for d,w in law.items()) for lam in points)


def partial_sum(lower, mass):
    n, acc = len(lower), F(0)
    amount = mass*n
    for d in sorted(lower):
        use = min(F(1),amount)
        acc += use*d/n
        amount -= use
        if amount == 0:
            break
    return acc


panels, certificate_checks, monotonic_checks = [], 0, 0
for lower in [(0,1,3,5),(1,2,3,4),(0,0,2,2),(10,10,10,10)]:
    for alpha in [F(0),F(1,4),F(1,2)]:
        law = shifted_law(lower,alpha)
        for rho in [F(0),F(1,10),F(1,2),F(1),F(2),F(4)]:
            value = primal(law,rho)
            assert value == dual(law,rho)
            for epsilon in [F(1,4),F(1,2),F(3,4)]:
                if epsilon>alpha and rho>0:
                    budget = partial_sum(lower,epsilon-alpha)
                    assert (value<=epsilon) == (rho<=budget and budget>0)
                    certificate_checks += 1
            for i in range(len(lower)):
                refined = list(lower)
                refined[i] += 1
                assert primal(shifted_law(refined,alpha),rho) <= value
                monotonic_checks += 1
            panels.append(dict(lower=lower,alpha=str(alpha),rho=str(rho),risk=str(value)))

def sat(clause,x):
    return any(bool((x>>j)&1)==sign for j,sign in clause)

weights = [1,3,5]
formulas = [(((0,True),),((1,False),(2,True))),
            (((0,True),(1,True),(2,False)),),
            (((0,False),(1,True)),((1,False),(2,True))),
            (((0,True),),((0,False),))]
cnf_checks = 0
for cnf in formulas:
    bad = [x for x in range(8) if not all(sat(c,x) for c in cnf)]
    assert bad
    distances = {x:min(sum(w for j,w in enumerate(weights) if (x^y)>>j&1) for y in bad) for x in range(8)}
    for partial in product([None,False,True],repeat=3):
        worlds = [x for x in range(8) if all(v is None or bool(x>>j&1)==v for j,v in enumerate(partial))]
        bound = min(sum(weights[j] for j,sign in clause if partial[j] is not None and partial[j]==sign) for clause in cnf)
        assert bound == min(distances[x] for x in worlds)
        cnf_checks += 1

example = []
for zeros in [100,50,0]:
    lower = [0]*zeros+[10]*(5000-zeros)
    budget = partial_sum(lower,F(1,20)-F(1,50))
    assert budget == {100:F(1,10),50:F(1,5),0:F(3,10)}[zeros]
    assert primal(shifted_law(lower,F(1,50)),budget) == F(1,20)
    example.append(dict(unresolved=zeros,drift_budget=str(budget),risk='1/20'))

result = dict(status='PASS',classification='DEVELOPMENT; exact arithmetic screen',
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              elapsed_ns=perf_counter_ns()-start,transport_panels=len(panels),
              certificate_checks=certificate_checks,refinement_checks=monotonic_checks,
              cnf_partial_boxes=cnf_checks,example=example,panels=panels)
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='panels'},indent=2))
