"""DEVELOPMENT screen, Codex GPT-6. Budget: 90 sources, n<=6, <=30s expected.
Compare enumerated adequacy hulls with independently compiled branch 2-SAT.
All receipts are exact; no statistical or empirical-generalization claim.
"""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random
import time

HERE = Path(__file__).resolve().parent
rng = random.Random(20261020)
started = time.perf_counter_ns()
counts = dict(panels=0, receipts=0, patterns=0, sat_calls=0, expanded_clauses=0)

def lit(x, l):
    return bool(x >> (abs(l)-1) & 1) == (l > 0)

def models(n, clauses):
    return {x for x in range(1 << n) if all(any(lit(x,l) for l in c) for c in clauses)}

def key(x, scope):
    return tuple(x >> i & 1 for i in scope)

def canonical(worlds, scope):
    assert worlds
    ls = [s*(i+1) for i in scope for s in (-1,1)]
    candidates = [(l,) for l in ls]
    candidates += [c for c in combinations(ls,2) if abs(c[0]) != abs(c[1])]
    return [c for c in candidates if all(any(lit(x,l) for l in c) for x in worlds)]

def sat2(n, clauses):
    counts['sat_calls'] += 1
    graph=[[] for _ in range(2*n)]
    back=[[] for _ in graph]
    def idx(l): return 2*(abs(l)-1)+(l<0)
    for c in clauses:
        assert len(c)<=2
        if not c: return False
        a,b=(c[0],c[-1])
        for u,v in ((idx(a)^1,idx(b)),(idx(b)^1,idx(a))):
            graph[u].append(v);back[v].append(u)
    seen=set();order=[]
    def visit(u):
        if u in seen:return
        seen.add(u)
        for v in graph[u]:visit(v)
        order.append(u)
    for u in range(2*n):visit(u)
    comp={}
    def assign(u,c):
        if u in comp:return
        comp[u]=c
        for v in back[u]:assign(v,c)
    for u in reversed(order):assign(u,u)
    return all(comp[2*i] != comp[2*i+1] for i in range(n))

def disjoin_units(groups):
    # Each group is a CNF of unit clauses or an empty contradiction clause.
    # [] is true; [()] is false. Distribute OR without semantic simplification.
    return [tuple(dict.fromkeys(l for c in choice for l in c))
            for choice in product(*groups)]

def prepare(n, sources, q, targets):
    bases=[canonical(w,q) for w in sources]
    conditions={}
    for m,w in enumerate(sources):
        for t in targets:
            cs=[c for c in canonical(w,tuple(q)+(t,)) if any(abs(l)==t+1 for l in c)]
            for b in (0,1):
                units=[]
                for c in cs:
                    if any(abs(l)==t+1 and (l>0)==bool(b) for l in c):continue
                    units.append(tuple(l for l in c if abs(l)!=t+1))
                assert all(len(c)<=1 for c in units)
                conditions[m,t,b]=units
    return bases,conditions

def compiled_consistent(n,sources,q,targets,prepared,receipt):
    bases,conditions=prepared
    for size in range(1,len(sources)+1):
        for branch in combinations(range(len(sources)),size):
            cs=[c for m in branch for c in bases[m]]
            cs += [((i+1) if b else -(i+1),) for i,b in receipt.items() if i in q]
            for t,b in receipt.items():
                if t in targets:
                    cs += disjoin_units([conditions[m,t,b] for m in branch])
            counts['expanded_clauses'] += len(cs)
            if sat2(n,cs):return True
    return False

for n in range(2,7):
    for panel in range(18):
        q=tuple(range(max(1,n//2)))
        targets=tuple(range(len(q),n))
        sources=[]
        for m in range(1+panel%2):
            witness=rng.randrange(1<<n)
            cs=[]
            for _ in range(2*n+panel%5):
                coords=rng.sample(range(n),1 if rng.random()<.15 else 2)
                c=tuple((i+1)*rng.choice((-1,1)) for i in coords)
                if any(lit(witness,l) for l in c):cs.append(c)
            sources.append(models(n,cs))
        union=set().union(*sources)
        projections={t:{key(x,q+(t,)) for x in union} for t in targets}
        hull={x for x in range(1<<n) if all(key(x,q+(t,)) in projections[t] for t in targets)}
        prepared=prepare(n,sources,q,targets)
        for states in product((-1,0,1),repeat=len(targets)):
            receipt={t:b for t,b in zip(targets,states) if b>=0}
            for i in q:
                if rng.random()<.4:receipt[i]=rng.randrange(2)
            actual=any(all((x>>i&1)==b for i,b in receipt.items()) for x in hull)
            got=compiled_consistent(n,sources,q,targets,prepared,receipt)
            assert got==actual,(n,panel,receipt,'consistency')
            counts['receipts']+=1
            scope=tuple(rng.sample(range(n),min(n,2)))
            for bits in product((0,1),repeat=len(scope)):
                added=dict(zip(scope,bits))
                conflict=any(i in receipt and receipt[i]!=b for i,b in added.items())
                merged=receipt|added
                actual=not conflict and any(all((x>>i&1)==b for i,b in merged.items()) for x in hull)
                got=not conflict and compiled_consistent(n,sources,q,targets,prepared,merged)
                assert got==actual,(n,panel,receipt,scope,bits,'projection')
                counts['patterns']+=1
        counts['panels']+=1

# Exact three-model encoding of arbitrary 3-CNF, including a guarded witness.
reductions=[]
for nq in range(3,6):
    for case in range(8):
        clauses=[tuple((i+1)*rng.choice((-1,1)) for i in rng.sample(range(nq),3)) for _ in range(4)]
        n=nq+len(clauses)
        q=tuple(range(nq));targets=tuple(range(nq,n))
        sources=[models(n,[(t+1,clauses[j][m]) for j,t in enumerate(targets)]) for m in range(3)]
        union=set().union(*sources)
        projs={t:{key(x,q+(t,)) for x in union} for t in targets}
        after={x for x in range(1<<nq) if all(key(x,q+(t,)) in projs[t] for t in targets)}
        expected=models(nq,clauses)
        assert after==expected
        reductions.append(dict(nq=nq,case=case,models_after=len(after)))

out=dict(status='PASS',contributor='Codex (GPT-6)',seed=20261020,counts=counts,
         three_model_reductions=reductions,elapsed_ns=time.perf_counter_ns()-started,
         source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         scope='finite development only; all source preparation counted in combined runtime; no arm speedup')
(HERE/'expand_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
