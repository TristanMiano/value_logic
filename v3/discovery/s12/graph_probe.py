"""Small DEVELOPMENT screen of graph_invoices.md; Codex (GPT-6).

Exact integer max flow, separate certificate checks, and direct enumeration
of the affine source/coset representatives. No external optimizer is used.
"""
from collections import deque
from pathlib import Path
import hashlib
import json
import platform
import random
import sys
import time

HERE=Path(__file__).resolve().parent


def parity(mask):
    return mask.bit_count()&1


def boundary(edges,world):
    out=0
    for i,(u,v) in enumerate(edges):
        if (world>>i)&1:
            out^=(1<<u)^(1<<v)
    return out


def maxflow(capacity,s,t):
    n=len(capacity)
    flow=[[0]*n for _ in range(n)]
    value=visits=augmentations=0
    while True:
        parent=[-1]*n
        parent[s]=s
        queue=deque([s])
        while queue and parent[t]<0:
            u=queue.popleft()
            for v in range(n):
                visits+=1
                if parent[v]<0 and capacity[u][v]>flow[u][v]:
                    parent[v]=u
                    queue.append(v)
        if parent[t]<0:
            side=frozenset(i for i,p in enumerate(parent) if p>=0)
            return value,flow,side,dict(edge_scans=visits,augmentations=augmentations)
        delta=None
        v=t
        while v!=s:
            u=parent[v]
            residual=capacity[u][v]-flow[u][v]
            delta=residual if delta is None else min(delta,residual)
            v=u
        assert delta is not None and delta>0
        v=t
        while v!=s:
            u=parent[v]
            flow[u][v]+=delta
            flow[v][u]-=delta
            v=u
        value+=delta
        augmentations+=1


def check_flow(capacity,s,t,value,flow,side):
    n=len(capacity)
    assert s in side and t not in side
    for u in range(n):
        for v in range(n):
            assert flow[u][v]==-flow[v][u]
            assert -capacity[u][v]<=flow[u][v]<=capacity[u][v]
        expected=value if u==s else -value if u==t else 0
        assert sum(flow[u])==expected
    assert sum(capacity[u][v] for u in side for v in range(n) if v not in side)==value


def graph_price(n,edges,fees,overhead,b,known,values,target):
    m=len(edges)
    weights=[fees[i]+min(fees[j] for j in range(m) if i!=j)+overhead for i in range(m)]
    if (known>>target)&1:
        return 0,0,(values>>target)&1,dict(kind='known')
    u,v=edges[target]
    if u==v:
        return weights[target],1<<target,0,dict(kind='direct_loop')
    cap=[[0]*n for _ in range(n)]
    for i,(a,z) in enumerate(edges):
        if i==target or (known>>i)&1 or a==z:
            continue
        cap[a][z]+=weights[i]
        cap[z][a]+=weights[i]
    value,flow,side,counts=maxflow(cap,u,v)
    check_flow(cap,u,v,value,flow,side)
    if value>=weights[target]:
        return weights[target],1<<target,0,dict(kind='direct',**counts)
    crossing=sum(1<<i for i,(a,z) in enumerate(edges) if (a in side)!=(z in side))
    assert (crossing>>target)&1
    representative=crossing&~known&~(1<<target)
    offset=parity(b&sum(1<<z for z in side))^parity(values&known&crossing)
    assert sum(weights[i] for i in range(m) if (representative>>i)&1)==value
    return value,representative,offset,dict(kind='cut',side=sorted(side),**counts)


def brute_price(edges,fees,overhead,worlds,target):
    m=len(edges)
    weights=[fees[i]+min(fees[j] for j in range(m) if i!=j)+overhead for i in range(m)]
    best=float('inf')
    checked=0
    for rep in range(1<<m):
        price=sum(weights[i] for i in range(m) if (rep>>i)&1)
        if price>=best:
            continue
        checked+=1
        if len({parity((rep^(1<<target))&x) for x in worlds})==1:
            best=price
    return best,checked


def invoice_decode(edges,fees,overhead,rep,offset,x):
    result=offset
    bill=0
    for i in range(len(edges)):
        if not (rep>>i)&1:
            continue
        marker=min((j for j in range(len(edges)) if i!=j),key=lambda j:fees[j])
        invoice=fees[i]+(fees[marker] if (x>>i)&1 else 0)+overhead
        decoded=int(invoice==fees[i]+fees[marker]+overhead)
        assert invoice in (fees[i]+overhead,fees[i]+fees[marker]+overhead)
        result^=decoded
        bill+=invoice
    return result,bill


def main():
    begun=time.perf_counter_ns()
    rng=random.Random(202610190538)
    fixtures=[]
    for _ in range(36):
        n=rng.randrange(2,7)
        m=rng.randrange(2,9)
        edges=[(rng.randrange(n),rng.randrange(n)) for _ in range(m)]
        fees=[rng.choice([1,2,3,7,19,100]) for _ in range(m)]
        fixtures.append((n,edges,fees,rng.choice([0,1,5,20])))
    example_edges=[(0,1)]+[(u,v) for z in [2,3,4] for u,v in [(0,z),(z,1)]]
    fixtures.append((5,example_edges,[100,1,1,1,1,1,1],0))
    totals=dict(fixtures=len(fixtures),receipts=0,targets=0,representatives_checked=0,
                decoded_worlds=0,cut_certificates=0,known=0,direct=0,edge_scans=0,augmentations=0)
    examples=[]
    for index,(n,edges,fees,overhead) in enumerate(fixtures):
        m=len(edges)
        x0=0 if index==len(fixtures)-1 else rng.randrange(1<<m)
        b=boundary(edges,x0)
        full=[x for x in range(1<<m) if boundary(edges,x)==b]
        receipts={(0,0)}
        for _ in range(8):
            x=rng.choice(full)
            known=rng.randrange(1<<m)
            receipts.add((known,x&known))
        for known,values in sorted(receipts):
            worlds=[x for x in full if (x&known)==values]
            assert worlds
            totals['receipts']+=1
            for target in range(m):
                price,rep,offset,certificate=graph_price(n,edges,fees,overhead,b,known,values,target)
                brute,checks=brute_price(edges,fees,overhead,worlds,target)
                assert price==brute,(index,known,values,target,price,brute)
                totals['targets']+=1
                totals['representatives_checked']+=checks
                totals['cut_certificates']+=certificate['kind']=='cut'
                totals['known']+=certificate['kind']=='known'
                totals['direct']+=certificate['kind'].startswith('direct')
                totals['edge_scans']+=certificate.get('edge_scans',0)
                totals['augmentations']+=certificate.get('augmentations',0)
                bills=[]
                for x in worlds:
                    decoded,bill=invoice_decode(edges,fees,overhead,rep,offset,x)
                    assert decoded==((x>>target)&1)
                    assert bill<=price
                    bills.append(bill)
                    totals['decoded_worlds']+=1
                # A cheapest positive-weight representative has no redundant
                # source parity on its support, so its maximum is attained.
                assert max(bills)==price,(index,known,target,price,max(bills))
                if index==len(fixtures)-1 and known==0 and target==0:
                    assert price==6
                    examples.append(dict(edges=edges,fees=fees,source_syndrome=b,
                                         direct_price=101,cut_price=price,representative=rep,
                                         offset=offset,certificate=certificate,world_bills=bills))
    result=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',python=sys.version,
                platform=platform.platform(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                seed=202610190538,elapsed_ns=time.perf_counter_ns()-begun,totals=totals,examples=examples,result='PASS')
    (HERE/'graph_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('result','elapsed_ns','totals')}))


if __name__=='__main__':
    main()
