"""Ordinary closure acquisition and separate exact witness check, Codex GPT-6.

DEVELOPMENT. Rewards/receipts/price contracts are external assumptions.
"""
from collections import deque
from fractions import Fraction as F


def objective(bits,terms,prices):
    return sum(r for mask,r in terms if mask&bits==mask)-sum(q for i,q in enumerate(prices) if bits&(1<<i))


def network(terms,prices):
    m,n=len(prices),len(terms);source=m+n;sink=source+1
    assert all(isinstance(q,F) and q>=0 for q in prices)
    assert all(0<=mask<1<<m and isinstance(r,F) and r>=0 for mask,r in terms)
    big=1+sum(r for _,r in terms);edges=[]
    for k,(mask,r) in enumerate(terms):
        node=m+k;edges.append((source,node,r))
        for i in range(m):
            if mask&(1<<i):edges.append((node,i,big))
    for i,q in enumerate(prices):edges.append((i,sink,q))
    return sink+1,source,sink,edges


def solve(terms,prices):
    n,s,t,edges=network(terms,prices);adj=[[] for _ in range(n)];res=[]
    for u,v,c in edges:
        k=len(res);res.extend([[u,v,c],[v,u,F(0)]]);adj[u].append(k);adj[v].append(k+1)
    flow=F(0);augmentations=0
    while True:
        parent=[None]*n;parent[s]=-1;queue=deque([s])
        while queue and parent[t] is None:
            u=queue.popleft()
            for e in adj[u]:
                _,v,c=res[e]
                if c>0 and parent[v] is None:parent[v]=e;queue.append(v)
        if parent[t] is None:break
        path=[];v=t
        while v!=s:
            e=parent[v];path.append(e);v=res[e][0]
        delta=min(res[e][2] for e in path)
        for e in path:res[e][2]-=delta;res[e^1][2]+=delta
        flow+=delta;augmentations+=1
    cut=[i for i in range(n) if parent[i] is not None]
    bits=sum(1<<i for i in cut if i<len(prices))
    witness=dict(flows=[c-res[2*k][2] for k,(_,_,c) in enumerate(edges)],cut=cut,flow=flow,
                 bits=bits,objective=objective(bits,terms,prices),augmentations=augmentations)
    check(terms,prices,witness)
    return witness


def check(terms,prices,witness):
    n,s,t,edges=network(terms,prices);flows=witness['flows'];cut=set(witness['cut'])
    assert len(flows)==len(edges) and s in cut and t not in cut and all(0<=i<n for i in cut)
    balance=[F(0)]*n
    for (u,v,c),f in zip(edges,flows):
        assert isinstance(f,F) and 0<=f<=c
        balance[u]-=f;balance[v]+=f
    assert all(balance[i]==0 for i in range(n) if i not in (s,t))
    value=balance[t];assert value==-balance[s]==witness['flow']
    capacity=sum(c for u,v,c in edges if u in cut and v not in cut)
    assert value==capacity
    bits=sum(1<<i for i in cut if i<len(prices))
    assert bits==witness['bits']
    assert all(mask&bits==mask for k,(mask,_) in enumerate(terms) if len(prices)+k in cut)
    optimum=sum(r for _,r in terms)-capacity
    assert objective(bits,terms,prices)==optimum==witness['objective']
    return optimum


def greedy(terms,prices):
    bits=0;value=objective(bits,terms,prices)
    while True:
        options=[(objective(bits|(1<<i),terms,prices),i) for i in range(len(prices)) if not bits&(1<<i)]
        if not options:break
        new,i=max(options)
        if new<=value:break
        bits|=1<<i;value=new
    return bits,value
