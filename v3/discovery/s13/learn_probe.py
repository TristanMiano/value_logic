"""Permission-vocabulary and partial-source screen; expected under10s."""
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import time

HERE=Path(__file__).resolve().parent
RNG=random.Random(2026102105)


def accepts(x,clauses):
    return all(any(bool(x>>(abs(l)-1)&1)==(l>0) for l in c) for c in clauses)


def acted(x,a):
    return sum((((x>>i)&1) if v==-1 else v)<<i for i,v in enumerate(a))


def source(worlds,boxes):
    return {x for x in worlds if any(all(v is None or (x>>i)&1==v
                                       for i,v in enumerate(b)) for b in boxes)}


def main():
    began=time.perf_counter_ns()
    counts=dict(panels=0,refinement_stages=0,action_checks=0,
                strict_source_expansions=0,nonempty_menus=0,grid_subsets=0)
    for n in (3,4):
        for _ in range(12):
            worlds=set(range(1<<n))
            edges=[(-i-1,j+1) for i in range(n) for j in range(n)
                   if i!=j and RNG.random()<.3]
            units=[((i+1) if RNG.randrange(2) else -(i+1),)
                   for i in range(n) if RNG.random()<.2]
            goal=edges+units
            vocab=[(l,) for i in range(n) for l in (i+1,-i-1)]+edges
            assert len(vocab)<=2*n+len(edges)
            actions=list(product((-1,0,1),repeat=n))
            preimage={a:{x for x in worlds if accepts(acted(x,a),goal)} for a in actions}
            for a,ga in preimage.items():
                if ga:
                    representation=[c for c in vocab if all(accepts(x,[c]) for x in ga)]
                    assert {x for x in worlds if accepts(x,representation)}==ga
            observed=[RNG.randrange(1<<n) for _ in range(4)]
            boxes=[[None]*n for _ in observed]
            previous_h=worlds
            previous_a=set()
            for stage in range(n+1):
                if stage:
                    for x,b in zip(observed,boxes):
                        b[stage-1]=(x>>(stage-1))&1
                f=source(worlds,boxes)
                clauses=[c for c in vocab if all(accepts(x,[c]) for x in f)]
                h={x for x in worlds if accepts(x,clauses)}
                assert set(observed)<=f<=h<=previous_h
                af={a for a in actions if f<=preimage[a]}
                ah={a for a in actions if h<=preimage[a]}
                assert af==ah and previous_a<=af
                warrant={x for x in worlds if all(x in preimage[a] for a in af)}
                assert h<=warrant
                previous_h,previous_a=h,af
                counts['refinement_stages']+=1
                counts['action_checks']+=len(actions)
                counts['strict_source_expansions']+=f!=h
                counts['nonempty_menus']+=bool(af)
            counts['panels']+=1
    for a,b in ((1,2),(2,2),(2,3),(3,3)):
        n=a+b
        edges=[(-i-1,j+1) for i in range(a) for j in range(a,n)]
        grid=[]
        actions=[]
        for i in range(a):
            for j in range(a,n):
                x=(1<<i)+sum(1<<k for k in range(a,n) if k!=j)
                grid.append(x)
                action=[0]*a+[1]*b
                action[i]=action[j]=-1
                actions.append(tuple(action))
        actions.append(tuple([0]*a+[1]*b))
        assert all(sum(not accepts(x,[e]) for e in edges)==1 for x in grid)
        for mask in range(1<<len(grid)):
            observed={x for i,x in enumerate(grid) if mask>>i&1}
            menu=[v for v in actions if all(accepts(acted(x,v),edges) for x in observed)]
            covered={x for x in grid if all(accepts(acted(x,v),edges) for v in menu)}
            assert covered==observed
            counts['grid_subsets']+=1
    out=dict(status='PASS',contributor='Codex (GPT-6)',seed=2026102105,counts=counts,
             elapsed_ns=time.perf_counter_ns()-began,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scope='finite preimage/learning identities; no observed label savings or new PAC theorem')
    (HERE/'learn_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':
    main()
