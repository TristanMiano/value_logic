"""DEVELOPMENT: Horn bill minima and twelve tiny upper-bill reductions.
Expected under30s; exhaustive finite checks, not a general proof.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import time

HERE = Path(__file__).resolve().parent
DEP = HERE/'audit_probe.py'
spec = importlib.util.spec_from_file_location('audit_helpers_bill',DEP)
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)
RNG = random.Random(2026102103)


def least_error(n,clauses,y,receipts):
    renamed = [tuple(-l if y>>(abs(l)-1)&1 else l for l in c) for c in clauses]
    renamed += [((i+1) if b^(y>>i&1) else -(i+1),) for i,b in receipts.items()]
    assert all(sum(l>0 for l in c)<=1 for c in renamed)
    errors = 0
    changed = True
    while changed:
        changed = False
        for clause in renamed:
            if any(H.true(errors,l) for l in clause):
                continue
            positive = [l for l in clause if l>0]
            if not positive:
                return None
            errors |= 1<<(positive[0]-1)
            changed = True
    return errors


def bill(x,y,clauses,first,prices):
    neighbors = {i:set() for i in range(len(prices)) if not(first>>i&1)}
    for c in clauses:
        outside = [abs(l)-1 for l in c if not(first>>(abs(l)-1)&1)]
        if outside:
            assert len(outside)==1 and len(c)==2
            i = outside[0]
            j = next(abs(l)-1 for l in c if abs(l)-1!=i)
            neighbors[i].add(j)
    return H.cost(first,prices)+sum(prices[i] for i,ns in neighbors.items()
                                    if any((x^y)>>j&1 for j in ns))


def reduction(n,cnf):
    graph = []
    y = 0
    first = 0
    for i in range(n):
        p,neg,r,s = range(4*i,4*i+4)
        graph += [(-(p+1),neg+1), (-(p+1),r+1), (-(s+1),neg+1)]
        y |= (1<<neg)|(1<<s)
        first |= (1<<p)|(1<<neg)
    for j,c in enumerate(cnf):
        t = 4*n+j
        assert all(l>0 for l in c) or all(l<0 for l in c)
        if c[0]>0:
            graph += [(-(4*(l-1)+1),t+1) for l in c]
        else:
            y |= 1<<t
            graph += [(-(t+1),4*(-l-1)+2) for l in c]
    return graph,y,first,4*n+len(cnf)


def main():
    began = time.perf_counter_ns()
    counts = dict(range_panels=0,receipt_queries=0,inconsistent_receipts=0,
                  bill_completion_checks=0,least_error_checks=0,
                  reduction_panels=0,reduction_worlds=0,satisfiable_cnfs=0,
                  unsatisfiable_cnfs=0)
    for n in range(3,8):
        for panel in range(7):
            y = RNG.randrange(1<<n)
            clauses = []
            for _ in range(n+3):
                ids = RNG.sample(range(n),1 if RNG.random()<.2 else 2)
                c = tuple((i+1)*RNG.choice((-1,1)) for i in ids)
                if any(H.true(y,l) for l in c):
                    clauses.append(c)
            first = (1<<n)-1
            for i in RNG.sample(range(n),n):
                trial = first & ~(1<<i)
                if all(any(trial>>(abs(l)-1)&1 and H.true(y,l) for l in c) for c in clauses):
                    first = trial
            prices = [RNG.randrange(1,8) for _ in range(n)]
            good = [x for x in range(1<<n) if H.accepts(x,clauses)]
            for _ in range(18):
                receipts = {i:RNG.randrange(2) for i in range(n) if RNG.random()<.4}
                residual = [x for x in good if all((x>>i&1)==b for i,b in receipts.items())]
                errors = least_error(n,clauses,y,receipts)
                counts['receipt_queries'] += 1
                assert (errors is None)==(not residual)
                if errors is None:
                    counts['inconsistent_receipts'] += 1
                    continue
                actual_bills = []
                for x in residual:
                    assert not(errors & ~(x^y))
                    counts['least_error_checks'] += 1
                    result,paid,_ = H.audit(x,clauses,first)
                    assert result
                    b = bill(x,y,clauses,first,prices)
                    assert b==H.cost(paid,prices)
                    actual_bills.append(b)
                    counts['bill_completion_checks'] += 1
                assert bill(y^errors,y,clauses,first,prices)==min(actual_bills)
            counts['range_panels'] += 1

    reductions = []
    for n in (2,3):
        for panel in range(6):
            cnf = [(1,),(-1,)] if panel==0 else []
            while len(cnf)<4:
                sign = RNG.choice((-1,1))
                cnf.append(tuple(sign*(i+1) for i in RNG.sample(range(n),RNG.randrange(1,n+1))))
            graph,y,first,nall = reduction(n,cnf)
            assert H.accepts(y,graph)
            assert H.certificate(y,graph,[1]*nall)==first
            sat = any(H.accepts(z,cnf) for z in range(1<<n))
            minimum,maximum = nall+1,-1
            for x in range(1<<nall):
                counts['reduction_worlds'] += 1
                if H.accepts(x,graph):
                    result,paid,_ = H.audit(x,graph,first)
                    assert result
                    minimum = min(minimum,paid.bit_count())
                    maximum = max(maximum,paid.bit_count())
            assert minimum==2*n
            assert maximum<=3*n+len(cnf)
            assert (maximum==3*n+len(cnf))==sat
            counts['satisfiable_cnfs'] += sat
            counts['unsatisfiable_cnfs'] += not sat
            counts['reduction_panels'] += 1
            reductions.append(dict(n=n,cnf=cnf,satisfiable=sat,minimum_bill=minimum,
                                   maximum_bill=maximum,target=3*n+len(cnf)))
    out = dict(status='PASS',contributor='Codex (GPT-6)',seed=2026102103,counts=counts,
               reductions=reductions,elapsed_ns=time.perf_counter_ns()-began,
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               dependency_sha256=hashlib.sha256(DEP.read_bytes()).hexdigest(),
               scope='finite development; no measured policy-learning or complete-cost advantage')
    (HERE/'bill_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':
    main()
