"""DEVELOPMENT: 30 small common-monotone envelopes, 40 receipts each.
Budget n<=8, M<=7, expected under30s. Enumeration is a separate oracle.
No arm runtime comparison and no empirical generalization claim.
"""
import ast
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import time

HERE = Path(__file__).resolve().parent
DEP = HERE/'expand_probe.py'
COUNTS = dict(panels=0, receipts=0, patterns=0, sat_calls=0,
              core_clause_scans=0, strict_envelopes=0, nonempty_envelopes=0,
              satisfiable_receipts=0, maximal_core_zero_bits=0)
tree = ast.parse(DEP.read_text(encoding='utf-8'))
names = {'lit', 'models', 'key', 'sat2'}
namespace = {'counts': COUNTS}
exec(compile(ast.Module(body=[node for node in tree.body
                             if isinstance(node, ast.FunctionDef) and node.name in names],
                        type_ignores=[]), str(DEP), 'exec'), namespace)
lit, models, key, sat2 = (namespace[s] for s in ('lit','models','key','sat2'))
RNG = random.Random(2026102101)


def greatest(nq, core, receipts):
    clauses = core+[((i+1) if b else -(i+1),) for i,b in receipts.items() if i<nq]
    assert all(sum(l<0 for l in c)<=1 for c in clauses)
    q = (1<<nq)-1
    changed = True
    while changed:
        changed = False
        for c in clauses:
            COUNTS['core_clause_scans'] += 1
            if any(lit(q,l) for l in c):
                continue
            negative = [l for l in c if l<0]
            if not negative:
                return None
            q &= ~(1 << (-negative[0]-1))
            changed = True
    return q


def solve(n, nq, core, residuals, petals, receipts, enforce=True):
    if enforce:
        assert all(all(l>0 or abs(l)>nq for l in c) for d in residuals for c in d)
    q = greatest(nq, core, receipts)
    if q is None:
        return False
    COUNTS['maximal_core_zero_bits'] += nq-q.bit_count()
    for petal in petals:
        found = False
        units = [((i+1) if b else -(i+1),) for i,b in receipts.items() if i in petal]
        for d in residuals:
            restricted = [tuple(l for l in c if abs(l)>nq) for c in d
                          if not any(abs(l)<=nq and lit(q,l) for l in c)]
            if sat2(n, restricted+units):
                found = True
                break
        if not found:
            return False
    return True


def hull(n, nq, core, residuals, petals):
    union = set().union(*(models(n, core+d) for d in residuals))
    scopes = [tuple(range(nq))+p for p in petals]
    projections = [{key(x,s) for x in union} for s in scopes]
    envelope = {x for x in range(1<<n)
                if all(key(x,s) in p for s,p in zip(scopes, projections))}
    return union, envelope


def main():
    began = time.perf_counter_ns()
    for panel in range(30):
        nq = 2+panel%3
        n = nq+4
        petals = [(nq,nq+1),(nq+2,nq+3)]
        core = []
        for _ in range(nq+2):
            variables = RNG.sample(range(nq), RNG.randrange(1,min(nq,3)+1))
            negative = RNG.choice(variables) if RNG.random()<.65 else -1
            core.append(tuple(-(i+1) if i==negative else i+1 for i in variables))
        residuals = []
        for _ in range(3+panel%5):
            d = []
            for _ in range(n+2):
                variables = RNG.sample(range(n), 1 if RNG.random()<.15 else 2)
                d.append(tuple(i+1 if i<nq else (i+1)*RNG.choice((-1,1)) for i in variables))
            residuals.append(d)
        union, envelope = hull(n,nq,core,residuals,petals)
        COUNTS['strict_envelopes'] += envelope != union
        COUNTS['nonempty_envelopes'] += bool(envelope)
        # Physical coordinates can use different signs from the normalized proof.
        flip = RNG.randrange(1<<nq)
        physical_hull = {x^flip for x in envelope}
        for _ in range(40):
            physical = {i:RNG.randrange(2) for i in range(n) if RNG.random()<.4}
            receipt = {i:b^(flip>>i&1) for i,b in physical.items()}
            actual = any(all((x>>i&1)==b for i,b in physical.items()) for x in physical_hull)
            got = solve(n,nq,core,residuals,petals,receipt)
            assert got==actual, (panel,physical,'receipt')
            COUNTS['receipts'] += 1
            COUNTS['satisfiable_receipts'] += actual
            scope = RNG.sample(range(n),2)
            for bits in product((0,1),repeat=2):
                extra = dict(zip(scope,bits))
                conflict = any(i in physical and physical[i]!=b for i,b in extra.items())
                merged = physical|extra
                normalized = {i:b^(flip>>i&1) for i,b in merged.items()}
                actual = not conflict and any(all((x>>i&1)==b for i,b in merged.items())
                                              for x in physical_hull)
                got = not conflict and solve(n,nq,core,residuals,petals,normalized)
                assert actual==got, (panel,physical,scope,bits,'pattern')
                COUNTS['patterns'] += 1
        COUNTS['panels'] += 1

    # Combining all petal receipts in one model is an invalid stronger test.
    ds = [[(-1,),(-2,)],[(1,),(2,)]]
    assert solve(2,0,[],ds,[(0,),(1,)],{0:0,1:1})
    assert not any(sat2(2,d+[(-1,),(2,)]) for d in ds)

    # Dropping common polarity causes a false negative, even for one model.
    assert not solve(2,1,[],[[(-1,2)]],[(1,)],{1:0},enforce=False)
    assert models(2,[(-1,2),(-2,)])

    # Overlap outside Q causes a false positive in the illegal independent test.
    ds = [[(-1,3),(-2,-3)]]
    assert solve(3,0,[],ds,[(0,2),(1,2)],{0:1,1:1})
    assert not models(3,ds[0]+[(1,),(2,)])

    out = dict(status='PASS',contributor='Codex (GPT-6)',seed=2026102101,
               counts=COUNTS,contract_boundary_examples=3,
               elapsed_ns=time.perf_counter_ns()-began,
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               dependency_sha256=hashlib.sha256(DEP.read_bytes()).hexdigest(),
               scope='finite same-model development; ordinary extremal-witness implementation ties')
    (HERE/'monotone_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':
    main()
