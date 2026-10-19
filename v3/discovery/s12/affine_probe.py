"""DEVELOPMENT exact small-world screen of affine_edits.md; Codex (GPT-6)."""
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import random
import sys
import time

HERE=Path(__file__).resolve().parent


def parity(x):
    return x.bit_count() & 1


def holds(rows, x):
    return all(parity(a & x)==b for a,b in rows)


def affine_space(n, rows):
    rows=list(rows)
    pivots=[]
    rank=0
    for col in range(n):
        index=next((j for j in range(rank,len(rows)) if (rows[j][0]>>col)&1),None)
        if index is None:
            continue
        rows[index],rows[rank]=rows[rank],rows[index]
        a,b=rows[rank]
        for j,(other,right) in enumerate(rows):
            if j!=rank and (other>>col)&1:
                rows[j]=(other^a,right^b)
        pivots.append(col)
        rank+=1
    if any(a==0 and b==1 for a,b in rows):
        return None
    base=sum(rows[j][1]<<col for j,col in enumerate(pivots))
    basis=[]
    for free in set(range(n))-set(pivots):
        v=1<<free
        for j,col in enumerate(pivots):
            v |= ((rows[j][0]>>free)&1)<<col
        basis.append(v)
    return base,basis


def compile_maps(n, base, basis, target):
    return [(a&v,0) for a,_ in target for v in basis]+[
        ((a&base)|(a<<n),b) for a,b in target]


def span(base, basis):
    result=[base]
    for v in basis:
        result += [x^v for x in result]
    return set(result)


def circulation(m):
    # Vertex v_i has index i; w_i has index m+1+i for i=0,...,m-1.
    edges=[]
    for i in range(m):
        edges += [(i,i+1),(i,m+1+i),(m+1+i,i+1)]
    edges.append((0,m))
    rows=[(sum(1<<j for j,(a,b) in enumerate(edges) if vertex in (a,b)),0)
          for vertex in range(2*m+1)]
    return edges,rows


def main():
    begun=time.perf_counter_ns()
    rng=random.Random(120020)
    totals=dict(fixtures=0,receipts=0,contradictions=0,action_checks=0,
                translation_checks=0,erasure_checks=0)
    for trial in range(64):
        n=1+trial%4
        hidden=rng.randrange(1<<n)
        source=[(a,parity(a&hidden)) for a in
                [rng.randrange(1<<n) for _ in range(rng.randrange(n+2))]]
        target=[(rng.randrange(1<<n),rng.randrange(2))
                for _ in range(rng.randrange(n+2))]
        worlds=[x for x in range(1<<n) if holds(source,x)]
        totals['fixtures']+=1
        for values in product([-1,0,1],repeat=n):
            units=[(1<<i,b) for i,b in enumerate(values) if b!=-1]
            compatible=[x for x in worlds if holds(units,x)]
            result=affine_space(n,source+units)
            if not compatible:
                assert result is None
                totals['contradictions']+=1
                continue
            assert result is not None
            base,basis=result
            assert span(base,basis)==set(compatible)
            compiled=compile_maps(n,base,basis,target)
            totals['receipts']+=1
            for action in range(1<<(2*n)):
                d=action&((1<<n)-1)
                c=action>>n
                expected=all(holds(target,(d&x)^c) for x in compatible)
                assert holds(compiled,action)==expected,(trial,values,d,c)
                totals['action_checks']+=1
            for delta in range(1<<n):
                expected=all(holds(source,x^delta) for x in compatible)
                assert expected==all(parity(a&delta)==0 for a,_ in source)
                totals['translation_checks']+=1
    circulation_results=[]
    for m in range(2,5):
        edges,rows=circulation(m)
        n=len(edges)
        base,basis=affine_space(n,rows)
        worlds=span(base,basis)
        assert len(worlds)==1<<(m+1)
        after={x for x in worlds if not (x>>(3*m))&1}
        assert len(after)==1<<m
        before_maps=[]
        after_maps=[]
        # Keep the already-zero observed edge unchanged, avoiding duplicate maps.
        seen_outputs=set()
        for keep in range(1<<n):
            before_ok=all(holds(rows,x&keep) for x in worlds)
            after_ok=all(holds(rows,x&keep) for x in after)
            if before_ok:
                before_maps.append(keep)
            if after_ok and (keep>>(3*m))&1:
                after_maps.append(keep)
                seen_outputs.add(tuple(x&keep for x in sorted(after)))
            totals['erasure_checks']+=2
        assert before_maps==[0,(1<<n)-1]
        assert len(after_maps)==len(seen_outputs)==1<<m
        clear_first=((1<<n)-1)^7
        assert all(holds(rows,x&clear_first) for x in after)
        assert all(not holds(rows,x&clear_first) for x in worlds-after)
        circulation_results.append(dict(triangles=m,edge_bits=n,
            source_worlds=len(worlds),worlds_after_zero_receipt=len(after),
            universally_safe_erasure_maps_before=len(before_maps),
            distinct_safe_erasure_maps_after=len(after_maps),
            query_coordinate=3*m,query_value=0,
            clear_first_impossible_on_one_receipt=True))
    result=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',seed=120020,
        python=sys.version,platform=platform.platform(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        elapsed_ns=time.perf_counter_ns()-begun,totals=totals,
        circulation=circulation_results,
        limitations='Finite exact semantic checks; no solver performance comparison, paid workload, priority or independent confirmation')
    (HERE/'affine_probe.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({key:result[key] for key in ['status','totals','circulation','elapsed_ns']}))


if __name__=='__main__':
    main()
