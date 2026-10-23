"""Cheap finite scope screen, not a scalable compiler. Codex (GPT-6)."""
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import hashlib
import heapq
import json
import platform
import random
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'target_warrant_probe.json'
assert not OUT.exists()
start=time.perf_counter_ns()
started=datetime.now(timezone.utc).isoformat()
rng=random.Random(2026102223)
def parity(x):return x.bit_count()%2
def span(rows):
    out={0}
    for r in rows:out|={x^r for x in out}
    return out
def independent_basis(rows,key):
    basis=[]; current={0}
    for r in sorted(set(rows),key=key):
        if r not in current:
            basis.append(r); current|={x^r for x in current}
    return basis
def target_price(h,prices,T):
    targets=[prices[i] for i in range(len(prices)) if (h&T)>>i&1]
    return sum(p for i,p in enumerate(prices) if h>>i&1)-max(targets) if targets else float('inf')

affine_panels=world_checks=overstrong_panels=0
for n in range(2,7):
    for case in range(10):
        dual=span(rng.randrange(1,1<<n) for _ in range(rng.randrange(n+1)))
        x0=rng.randrange(1<<n)
        source=[x for x in range(1<<n) if all(not parity((x^x0)&h) for h in dual)]
        circuits=[h for h in dual-{0} if not any(g!=h and g&h==g for g in dual-{0})]
        prices=[rng.randrange(5) for _ in range(n)]
        for T in (1<<rng.randrange(n),rng.randrange(1,1<<n),(1<<n)-1):
            for B in (0,1,3,8):
                eligible=[h for h in circuits if target_price(h,prices,T)<=B]
                W={x for x in range(1<<n) if all(not parity((x^x0)&h) for h in eligible)}
                direct=set(range(1<<n))
                for S in range(1<<n):
                    if sum(prices[i] for i in range(n) if S>>i&1)>B:continue
                    fibers={}
                    for x in source:fibers.setdefault(x&S,[]).append(x)
                    for x in list(direct):
                        fiber=fibers.get(x&S)
                        if not fiber:continue
                        for j in range(n):
                            if S>>j&1 or not T>>j&1:continue
                            values={(y>>j)&1 for y in fiber}
                            if len(values)==1 and (x>>j&1) not in values:
                                direct.remove(x);break
                assert W==direct,(n,case,T,B,prices,circuits,W,direct)
                overstrong={x for x in range(1<<n) if all(not parity((x^x0)&h) for h in dual if target_price(h,prices,T)<=B)}
                assert overstrong<=W
                overstrong_panels+=overstrong!=W
                affine_panels+=1;world_checks+=1<<n

# The explicit (a,b,c) counterexample.
dual=span([2,5]);circuits=[2,5];T=1;prices=[1,1,1];B=2
assert target_price(7,prices,T)<=B
example_warrant=[x for x in range(8) if not parity(x&5)]
example_overstrong=[x for x in range(8) if not parity(x&5) and not parity(x&7)]
assert example_warrant==[0,2,5,7] and example_overstrong==[0,5]

def simple_cycles(n,edges):
    result=[]
    for mask in range(1,1<<len(edges)):
        adjacency=[[] for _ in range(n)]
        for i,(a,b) in enumerate(edges):
            if mask>>i&1:adjacency[a].append(b);adjacency[b].append(a)
        used=[i for i,a in enumerate(adjacency) if a]
        if not used or any(len(adjacency[i])!=2 for i in used):continue
        seen={used[0]};todo=[used[0]]
        while todo:
            for v in adjacency[todo.pop()]:
                if v not in seen:seen.add(v);todo.append(v)
        if len(seen)==len(used):result.append(mask)
    return result

def odd_walk_oracle(n,edges,prices,z):
    best=float('inf')
    for omitted,(s,t) in enumerate(edges):
        adjacency=[[] for _ in range(n)]
        for i,(a,b) in enumerate(edges):
            if i==omitted or prices[i]>prices[omitted]:continue
            adjacency[a].append((b,i));adjacency[b].append((a,i))
        target=2*t+(1-(z>>omitted&1));initial=2*s
        dist={initial:0};heap=[(0,initial)]
        while heap:
            d,state=heapq.heappop(heap)
            if d!=dist[state]:continue
            if state==target:best=min(best,d);break
            v,p=divmod(state,2)
            for u,i in adjacency[v]:
                nxt=2*u+(p^(z>>i&1));nd=d+prices[i]
                if nd<dist.get(nxt,float('inf')):
                    dist[nxt]=nd;heapq.heappush(heap,(nd,nxt))
    return best

graph_panels=threshold_checks=odd_oracle_checks=0
graph_records=[]
for case in range(24):
    n=rng.choice((4,5,6));all_edges=list(combinations(range(n),2))
    rng.shuffle(all_edges);edges=sorted(all_edges[:rng.randrange(n,min(len(all_edges),10)+1)])
    m=len(edges);cycles=simple_cycles(n,edges)
    prices=[rng.randrange(6) for _ in edges]
    def cost(C):return sum(prices[i] for i in range(m) if C>>i&1)
    for T in (1<<rng.randrange(m),rng.randrange(1,1<<m),(1<<m)-1):
        candidates=[]
        for e in range(m):
            if T>>e&1:
                candidates+=independent_basis((C for C in cycles if C>>e&1),lambda C:(cost(C),C))
        compressed=independent_basis(candidates,lambda C:(target_price(C,prices,T),C))
        for B in range(sum(prices)+1):
            expected=span(C for C in cycles if target_price(C,prices,T)<=B)
            actual=span(C for C in compressed if target_price(C,prices,T)<=B)
            assert actual==expected,(case,edges,prices,T,B,cycles,compressed)
            threshold_checks+=1
        graph_panels+=1
    for z in [rng.randrange(1,1<<m) for _ in range(12)]:
        expected=min((target_price(C,prices,(1<<m)-1) for C in cycles if parity(C&z)),default=float('inf'))
        assert odd_walk_oracle(n,edges,prices,z)==expected,(case,edges,prices,z,expected)
        odd_oracle_checks+=1
    graph_records.append(dict(vertices=n,edges=edges,prices=prices,simple_cycle_count=len(cycles)))

result=dict(status='PASS',label='DEVELOPMENT exact finite screen; not independent confirmation',
            contributor='Codex (GPT-6)',started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            python=sys.version,platform=platform.platform(),affine_panels=affine_panels,world_checks=world_checks,
            overstrong_all_word_panels=overstrong_panels,graph_panels=graph_panels,threshold_checks=threshold_checks,
            odd_walk_oracle_checks=odd_oracle_checks,example_warrant=example_warrant,example_overstrong=example_overstrong,
            graph_records=graph_records)
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='graph_records'},indent=2))
