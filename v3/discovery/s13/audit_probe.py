"""DEVELOPMENT: 30 implication formulas, n<=7, <=3 supplied predictions.
Compare min-cut certificates with all-completion enumeration, then all worlds.
Small screen only, prospective expected runtime below30s.
"""
import ast
from collections import deque
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import time

HERE = Path(__file__).resolve().parent
DEP = HERE/'edge_extension.py'
space = {'deque':deque}
tree = ast.parse(DEP.read_text(encoding='utf-8'))
exec(compile(ast.Module(body=[node for node in tree.body if isinstance(node,ast.ClassDef)
                             and node.name=='Flow'],type_ignores=[]),str(DEP),'exec'),space)
Flow = space['Flow']
RNG = random.Random(2026102102)


def true(x,l):
    return bool(x>>(abs(l)-1)&1)==(l>0)


def accepts(x,clauses):
    return all(any(true(x,l) for l in c) for c in clauses)


def cost(mask,prices):
    return sum(p for i,p in enumerate(prices) if mask>>i&1)


def certificate(y,clauses,prices):
    n = len(prices)
    forced = set()
    edges = []
    for clause in clauses:
        supporting = {abs(l)-1 for l in clause if true(y,l)}
        assert supporting
        if len(supporting)==1:
            forced |= supporting
        else:
            a,b = supporting
            if y>>a&1:
                a,b = b,a
            assert not (y>>a&1) and (y>>b&1)
            edges.append((a,b))
    flow = Flow(n+2)
    source,sink = n,n+1
    for i,p in enumerate(prices):
        if i in forced:
            continue
        if y>>i&1:
            flow.add(i,sink,p)
        else:
            flow.add(source,i,p)
    for a,b in edges:
        if a not in forced and b not in forced:
            flow.add(a,b,sum(prices)+1)
    value,reach = flow.maxflow(source,sink)
    cover = forced|{i for i in range(n) if i not in forced and
                    ((bool(y>>i&1) and i in reach) or (not(y>>i&1) and i not in reach))}
    mask = sum(1<<i for i in cover)
    assert cost(mask,prices)==sum(prices[i] for i in forced)+value
    return mask


def audit(x,clauses,first):
    requirements = {}
    for clause in clauses:
        if any(first>>(abs(l)-1)&1 and true(x,l) for l in clause):
            continue
        remaining = [l for l in clause if not(first>>(abs(l)-1)&1)]
        if not remaining:
            return False,first,0
        assert len(remaining)==1
        l = remaining[0]
        i,b = abs(l)-1,l>0
        if i in requirements and requirements[i]!=b:
            return False,first,0
        requirements[i] = b
    rest = sum(1<<i for i in requirements)
    result = all(bool(x>>i&1)==b for i,b in requirements.items())
    return result,first|rest,rest


def neighborhood(errors,clauses):
    result = errors
    for c in clauses:
        mask = sum(1<<(abs(l)-1) for l in c)
        if mask&errors:
            result |= mask
    return result


def main():
    began = time.perf_counter_ns()
    counts = dict(panels=0,predictions=0,completion_certificate_checks=0,
                  actual_worlds=0,positive_bound_checks=0,mandatory_repair_checks=0,
                  globally_wrong_first_round_accepts=0,inconsistent_residuals=0)
    for n in range(3,8):
        for panel in range(6):
            witness = RNG.randrange(1<<n)
            arcs = {tuple(RNG.sample(range(n),2)) for _ in range(2*n)}
            clauses = [(-(i+1),j+1) for i,j in arcs if not(witness>>i&1) or witness>>j&1]
            if panel%2:
                i = RNG.randrange(n)
                clauses.append(((i+1) if witness>>i&1 else -(i+1),))
            prices = [RNG.randrange(1,8) for _ in range(n)]
            good = [x for x in range(1<<n) if accepts(x,clauses)]
            bad = [x for x in range(1<<n) if not accepts(x,clauses)]
            mask_costs = [cost(mask,prices) for mask in range(1<<n)]
            exact = {}
            mandatory = {}
            for x in good:
                valid = [mask for mask in range(1<<n)
                         if all((x^z)&mask for z in bad)]
                counts['completion_certificate_checks'] += 1<<n
                exact[x] = min(mask_costs[mask] for mask in valid)
                mandatory[x] = (1<<n)-1
                for mask in valid:
                    mandatory[x] &= mask
            for y in RNG.sample(good,min(3,len(good))):
                first = certificate(y,clauses,prices)
                assert mask_costs[first]==exact[y]
                counts['predictions'] += 1
                for x in range(1<<n):
                    result,paid,repair = audit(x,clauses,first)
                    assert result==accepts(x,clauses)
                    counts['actual_worlds'] += 1
                    assert mask_costs[paid]<=sum(prices)
                    if result:
                        near = neighborhood(x^y,clauses)
                        assert not (repair & ~near)
                        assert not (repair & ~mandatory[x])
                        assert mask_costs[paid]<=exact[x]+mask_costs[near]
                        counts['positive_bound_checks'] += 1
                        counts['mandatory_repair_checks'] += bool(repair)
                        counts['globally_wrong_first_round_accepts'] += x!=y and not repair
                    elif not repair:
                        counts['inconsistent_residuals'] += 1
            counts['panels'] += 1

    stars = []
    for leaves in (2,4,8,16):
        clauses = [(-1,i+2) for i in range(leaves)]
        y = (1<<(leaves+1))-1
        x = y^1
        first = certificate(y,clauses,[1]*(leaves+1))
        result,paid,rest = audit(x,clauses,first)
        assert result and paid.bit_count()==leaves and not rest
        stars.append(dict(leaves=leaves,prediction_errors=1,query_fee=leaves,
                          actual_optimal_certificate_fee=1,neighborhood_fee=leaves+1))
    out = dict(status='PASS',contributor='Codex (GPT-6)',seed=2026102102,
               counts=counts,one_error_stars=stars,elapsed_ns=time.perf_counter_ns()-began,
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               dependency_sha256=hashlib.sha256(DEP.read_bytes()).hexdigest(),
               scope='finite same-model development, query bounds only; no complete-cost win')
    (HERE/'audit_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':
    main()
