"""DEVELOPMENT oracle comparison for parity_price.md; Codex (GPT-6).

Enumerate every distinct invoice function of every permitted deterministic
private query tree. Independently optimize the public adaptive strategy by
Bellman recursion over compatible worlds, then compare the closed formula.
The finite oracle does not assume block queries or character representatives.
"""
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import sys
import time

HERE=Path(__file__).resolve().parent


def parity(x):
    return x.bit_count()&1


def affine_sources(n):
    subspaces={frozenset([0])}
    for vector in range(1,1<<n):
        subspaces |= {frozenset(set(space)|{x^vector for x in space})
                      for space in list(subspaces)}
    return sorted({sum(1<<(x^offset) for x in space)
                   for space in subspaces for offset in range(1<<n)})


def all_invoice_functions(fees, cap):
    n=len(fees)
    worlds=range(1<<n)
    @lru_cache(None)
    def programs(available, depth):
        out={tuple(0 for _ in worlds)}
        if depth==0:
            return frozenset(out)
        for i in range(n):
            if not (available>>i)&1:
                continue
            children=programs(available^(1<<i),depth-1)
            for left,right in product(children,repeat=2):
                out.add(tuple(fees[i]+(right[x] if (x>>i)&1 else left[x])
                              for x in worlds))
        return frozenset(out)
    return programs((1<<n)-1,cap)


def partitions(functions):
    answer=[]
    for function in sorted(functions):
        groups={}
        for x,cost in enumerate(function):
            groups[cost]=groups.get(cost,0)|(1<<x)
        answer.append(tuple(sorted(groups.items())))
    return answer


def phi(fees,cap,overhead,target):
    if target==0:
        return 0
    n=len(fees)
    size=target.bit_count()
    q=(size+cap-2)//(cap-1)
    base=sum(fees[i] for i in range(n) if (target>>i)&1)
    cheapest=min(range(n),key=lambda i:fees[i])
    first=fees[cheapest]
    second=min(fees[i] for i in range(n) if i!=cheapest)
    if not (target>>cheapest)&1:
        return base+q*(first+overhead)
    if q>=2:
        return base+(q-1)*first+second+q*overhead
    outside=min((fees[i] for i in range(n) if not (target>>i)&1),default=float('inf'))
    return base+min(outside+overhead,first+second+2*overhead)


def equivalent_characters(n, source, target):
    worlds=[x for x in range(1<<n) if (source>>x)&1]
    return [other for other in range(1<<n)
            if len({parity((target^other)&x) for x in worlds})==1]


def public_oracle(n,bank,target,overhead):
    ones=sum(1<<x for x in range(1<<n) if parity(target&x))
    stats=dict(states=0,program_checks=0)
    @lru_cache(None)
    def value(source):
        if not (source&ones) or (source&ones)==source:
            return 0
        stats['states']+=1
        best=float('inf')
        for program in bank:
            groups=[(cost,subset&source) for cost,subset in program if subset&source]
            # Positive-cost episodes with no information cannot improve a
            # stationary private-reset problem; omission is exact.
            if len(groups)<=1:
                continue
            stats['program_checks']+=1
            worst=0
            for cost,subset in groups:
                worst=max(worst,cost+overhead+value(subset))
                if worst>=best:
                    break
            best=min(best,worst)
        assert best!=float('inf')
        return best
    return value,stats


def main():
    begun=time.perf_counter_ns()
    n=3
    sources=affine_sources(n)
    assert len(sources)==51
    panels=[]
    totals=dict(comparisons=0,bellman_states=0,program_checks=0)
    for fees in [(1,1,1),(1,2,7),(2,3,5),(1,1,100)]:
        for cap in [2,3]:
            functions=all_invoice_functions(fees,cap)
            bank=partitions(functions)
            panel=dict(fees=fees,cap=cap,private_invoice_functions=len(functions),
                       comparisons=0,full_source=[])
            for overhead in [0,1,10,98,100]:
                formula=[phi(fees,cap,overhead,t) for t in range(1<<n)]
                for target in range(1,1<<n):
                    oracle,stats=public_oracle(n,bank,target,overhead)
                    for source in sources:
                        expected=min(formula[t] for t in
                                     equivalent_characters(n,source,target))
                        actual=oracle(source)
                        assert actual==expected,(fees,cap,overhead,target,source,actual,expected)
                        totals['comparisons']+=1
                        panel['comparisons']+=1
                    panel['full_source'].append(dict(overhead=overhead,target=target,
                        optimum=oracle((1<<(1<<n))-1)))
                    totals['bellman_states']+=stats['states']
                    totals['program_checks']+=stats['program_checks']
            panels.append(panel)
    result=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',
        python=sys.version,platform=platform.platform(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        elapsed_ns=time.perf_counter_ns()-begun,source_count=len(sources),
        totals=totals,panels=panels,
        limitations='Complete finite oracle only for n=3 at the listed prices/caps; not an all-size proof, noisy/expected-cost result, priority review or independent confirmation')
    (HERE/'parity_price_probe.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({key:result[key] for key in ['status','source_count','totals','elapsed_ns']}))


if __name__=='__main__':
    main()
