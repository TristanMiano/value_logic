"""DEVELOPMENT screen: unary-map compilation and incremental receipt updates.

Codex (GPT-6). Reuses the frozen source graph adapter, but checks actions by
direct execution on every compatible original world. This is same-model
finite evidence, not independent confirmation or a performance benchmark.
"""
from collections import deque
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import platform
import random
import sys
import time

from permission_probe import graph, holds, lit_true, projections

HERE = Path(__file__).resolve().parent


def map_clauses(target, cached, forced, menus):
    result = []
    for clause, (variables, patterns) in zip(target, cached):
        false_bit = {lit//2: 1-(lit&1) for lit in clause}
        for bits in patterns:
            if any((forced >> (2*i+1-b)) & 1
                   for i, b in zip(variables, bits)):
                continue
            result.append(tuple(2*(2*i+b) + 1-false_bit[i]
                                for i,b in zip(variables,bits)))
    for i, menu in enumerate(menus):
        for operation in set(range(4))-set(menu):
            result.append(tuple(2*(2*i+b)+1-((operation >> b)&1)
                                for b in range(2)))
    return result


def execute(world, operations):
    return sum(((operation >> ((world >> i)&1))&1) << i
               for i,operation in enumerate(operations))


def source_edges(n, clauses):
    edges = [set() for _ in range(2*n)]
    for clause in clauses:
        a,b = (clause[0],clause[0]) if len(clause)==1 else clause
        edges[a^1].add(b)
        edges[b^1].add(a)
    return edges


def incremental_run(n, source, target, cached, initial_forced, world, order):
    edges = source_edges(n,source)
    # Each obligation's endpoint incidence is installed exactly once.
    patterns = [(j,variables,bits) for j,(variables,values) in enumerate(cached)
                for bits in values]
    incidence = [[] for _ in range(2*n)]
    for index,(_,variables,bits) in enumerate(patterns):
        for i,b in zip(variables,bits):
            incidence[2*i+1-b].append(index)
    live = set(range(len(patterns)))
    forced = 0
    stats = dict(new_literals=0, edge_visits=0, incidence_visits=0,
                 clauses_deleted=0, receipt_inputs=0)

    def propagate(seeds):
        nonlocal forced
        queue=deque(seeds)
        while queue:
            literal=queue.popleft()
            if (forced >> literal)&1:
                continue
            assert not ((forced >> (literal^1))&1)
            forced |= 1 << literal
            stats['new_literals'] += 1
            for dest in edges[literal]:
                stats['edge_visits'] += 1
                queue.append(dest)
            for index in incidence[literal]:
                stats['incidence_visits'] += 1
                if index in live:
                    live.remove(index)
                    stats['clauses_deleted'] += 1

    propagate([lit for lit in range(2*n) if (initial_forced >> lit)&1])
    receipt=[]
    all_worlds=[x for x in range(1 << n) if holds(source,x)]
    for i in order:
        literal=2*i+((world >> i)&1)
        receipt.append(literal)
        stats['receipt_inputs'] += 1
        propagate([literal])
        compatible=[x for x in all_worlds if all(lit_true(l,x) for l in receipt)]
        expected={(j,tuple((x >> i)&1 for i in variables))
                  for j,(variables,_) in enumerate(cached) for x in compatible}
        actual={(j,bits) for index,(j,_,bits) in enumerate(patterns) if index in live}
        assert actual == expected
    assert stats['new_literals'] <= n
    assert stats['edge_visits'] <= sum(map(len,edges))
    assert stats['incidence_visits'] <= sum(map(len,incidence))
    assert stats['clauses_deleted'] <= len(patterns)
    return stats


def main():
    begun=time.perf_counter_ns()
    rng=random.Random(120019)
    totals=dict(formulas=0,satisfiable=0,receipts=0,action_checks=0,
                receipt_chains=0,new_literals=0,edge_visits=0,
                incidence_visits=0,clauses_deleted=0,receipt_inputs=0)
    for trial in range(72):
        n=2+trial%3
        pool=[(lit,) for lit in range(2*n)]
        pool += [(2*i+a,2*j+b) for i,j in combinations(range(n),2)
                 for a,b in product([0,1],repeat=2)]
        source=rng.sample(pool,rng.randint(0,min(len(pool),2*n)))
        target=rng.sample(pool,rng.randint(0,min(len(pool),n+2)))
        worlds=[x for x in range(1<<n) if holds(source,x)]
        satisfiable,reach,initial_forced=graph(n,source)
        assert satisfiable == bool(worlds)
        totals['formulas'] += 1
        if not worlds:
            continue
        totals['satisfiable'] += 1
        cached=projections(n,target,reach,initial_forced)
        # Alternate the full overwrite menu with independently restricted menus.
        menus=[list(range(4)) if trial%2==0 else
               rng.sample(range(4),rng.randint(1,4)) for _ in range(n)]
        for values in product([-1,0,1],repeat=n):
            units=[2*i+b for i,b in enumerate(values) if b!=-1]
            compatible=[x for x in worlds if all(lit_true(l,x) for l in units)]
            if not compatible:
                continue
            forced=initial_forced
            for lit in units:
                forced |= reach[lit]
            compiled=map_clauses(target,cached,forced,menus)
            totals['receipts'] += 1
            for operations in product(range(4),repeat=n):
                expected=all(operation in menus[i] for i,operation in enumerate(operations))
                expected=expected and all(holds(target,execute(x,operations)) for x in compatible)
                encoded=sum(operation << (2*i) for i,operation in enumerate(operations))
                assert holds(compiled,encoded)==expected,(trial,units,operations)
                totals['action_checks'] += 1
        for world in worlds:
            order=list(range(n))
            rng.shuffle(order)
            stats=incremental_run(n,source,target,cached,initial_forced,world,order)
            totals['receipt_chains'] += 1
            for key,value in stats.items():
                totals[key] += value
    result=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',seed=120019,
        python=sys.version,platform=platform.platform(),
        sources={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                 for name in ['map_probe.py','permission_probe.py']},
        elapsed_ns=time.perf_counter_ns()-begun,totals=totals,
        limitations='Finite diagnostic only; graph preparation, optimization, reset and source changes are outside incremental counters')
    (HERE/'map_probe.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({key:result[key] for key in ['status','totals','elapsed_ns']}))


if __name__=='__main__':
    main()
