"""DEVELOPMENT finite petal and selector screen. 48 sources n<=7, <=10s.
Read only helper definitions from the immutable earlier same-session probe;
never execute its top-level panel or rewrite its results. Codex (GPT-6).
"""
from itertools import combinations, product
from pathlib import Path
import ast
import hashlib
import json
import random
import time

HERE=Path(__file__).resolve().parent
helper=HERE/'expand_probe.py'
tree=ast.parse(helper.read_text(encoding='utf-8'))
chosen={'lit','models','key','canonical','sat2'}
env={'combinations':combinations,'counts':{'sat_calls':0}}
exec(compile(ast.Module(body=[node for node in tree.body if isinstance(node,ast.FunctionDef)
                             and node.name in chosen],type_ignores=[]),str(helper),'exec'),env)
lit,models,key,canonical,sat2=[env[name] for name in ('lit','models','key','canonical','sat2')]
rng=random.Random(1320261020)
begun=time.perf_counter_ns()
stats=dict(panels=0,conditional_projection_lemmas=0,receipts=0,selector_checks=0,
           initial_patterns=0,model_tuple_branches=0)

def consistent(n,q,petals,bases,units,receipt):
    qcs=[((i+1) if b else -(i+1),) for i,b in receipt.items() if i in q]
    for size in range(1,len(bases)+1):
        for branch in combinations(range(len(bases)),size):
            cs=qcs+[c for m in branch for c in bases[m]]
            nv=n
            for j,petal in enumerate(petals):
                pattern=tuple(receipt.get(i,-1) for i in petal)
                arms=[units[m,j,pattern] for m in branch]
                if len(arms)==1:cs+=arms[0]
                else:
                    nv+=1;s=nv
                    for arm,guard in zip(arms,(-s,s)):
                        cs += [(guard,)+c for c in arm]
            stats['selector_checks']+=1
            if sat2(nv,cs):return True
    return False

def initial_projection(n,q,petals,bases,units,receipt):
    touched=[j for j,p in enumerate(petals) if any(i in receipt for i in p)]
    qcs=[((i+1) if b else -(i+1),) for i,b in receipt.items() if i in q]
    choices=product(range(len(bases)),repeat=len(touched)) if touched else ((m,) for m in range(len(bases)))
    for selected in choices:
        cs=qcs+[c for m in set(selected) for c in bases[m]]
        for j,m in zip(touched,selected):
            pattern=tuple(receipt.get(i,-1) for i in petals[j])
            cs+=units[m,j,pattern]
        stats['model_tuple_branches']+=1
        if sat2(n,cs):return True
    return False

for n in (6,7):
    for case in range(24):
        q=tuple(range(n-4));petals=(tuple(range(n-4,n-2)),tuple(range(n-2,n)))
        sources=[]
        for m in range(1+case%3):
            witness=rng.randrange(1<<n);cs=[]
            for _ in range(3*n):
                coords=rng.sample(range(n),1 if rng.random()<.1 else 2)
                c=tuple((i+1)*rng.choice((-1,1)) for i in coords)
                if any(lit(witness,l) for l in c):cs.append(c)
            sources.append(models(n,cs))
        union=set().union(*sources)
        projections=[{key(x,q+p) for x in union} for p in petals]
        hull={x for x in range(1<<n) if all(key(x,q+p) in proj for p,proj in zip(petals,projections))}
        bases=[canonical(w,q) for w in sources];units={}
        for m,w in enumerate(sources):
            for j,p in enumerate(petals):
                for pattern in product((-1,0,1),repeat=len(p)):
                    remaining={x for x in w if all(b<0 or x>>i&1==b for i,b in zip(p,pattern))}
                    u=[()] if not remaining else [(l,) for i in q for l in (i+1,-i-1)
                                                  if all(lit(x,l) for x in remaining)]
                    units[m,j,pattern]=u
                    expected={key(x,q) for x in remaining}
                    got={key(x,q) for x in models(n,bases[m]+u)}
                    assert got==expected,(n,case,m,j,pattern,'unit projection')
                    stats['conditional_projection_lemmas']+=1
        # Exact initial pair projections with any number of supplied models.
        binary=[]
        for scope in combinations(range(n),2):
            for pattern in product((0,1),repeat=2):
                receipt=dict(zip(scope,pattern))
                expected=any(all(x>>i&1==b for i,b in receipt.items()) for x in hull)
                got=initial_projection(n,q,petals,bases,units,receipt)
                assert got==expected,(n,case,scope,pattern,'initial pattern')
                if not got:binary.append(tuple(-(i+1) if b else i+1 for i,b in receipt.items()))
                stats['initial_patterns']+=1
        binary_worlds=models(n,binary)
        assert hull<=binary_worlds
        assert all({key(x,s) for x in hull}=={key(x,s) for x in binary_worlds}
                   for s in combinations(range(n),2))
        if len(sources)<=2:
            for pattern in product((-1,0,1),repeat=4):
                receipt={i:b for i,b in zip(petals[0]+petals[1],pattern) if b>=0}
                for i in q:
                    if rng.random()<.3:receipt[i]=rng.randrange(2)
                expected=any(all(x>>i&1==b for i,b in receipt.items()) for x in hull)
                got=consistent(n,q,petals,bases,units,receipt)
                assert got==expected,(n,case,receipt,'selector')
                stats['receipts']+=1
        stats['panels']+=1

# Known-consistent guarded 3-CNF query, including the unsatisfiable input.
guarded=[]
all_clauses=[tuple((i+1)*(1 if b else -1) for i,b in enumerate(bits)) for bits in product((0,1),repeat=3)]
for clauses in [all_clauses,all_clauses[:-1],[(1,2,3),(-1,-2,-3)]]:
    z=4;cs=[]
    for j,(a,b,c) in enumerate(clauses):
        w=5+j;cs += [(-z,a,w),(-w,b,c)]
    nw=4+len(clauses)
    candidates=models(nw,cs)
    assert 0 in candidates
    original=bool(models(3,clauses));z_true=any(x>>(z-1)&1 for x in candidates)
    assert original==z_true
    guarded.append(dict(input_clauses=len(clauses),input_satisfiable=original,
                        guarded_worlds=len(candidates),known_witness=0,forced_z_zero=not z_true))

out=dict(status='PASS',contributor='Codex (GPT-6)',seed=1320261020,counts=stats,
         sat_calls=env['counts']['sat_calls'],guarded_cases=guarded,
         elapsed_ns=time.perf_counter_ns()-begun,
         hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),helper)},
         scope='same-model finite development; arbitrary overlap and general nonlinear receipts not covered')
(HERE/'petal_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
