"""Cheap feasible allocation advice and integer exact control; DEVELOPMENT."""
from collections import deque
from fractions import Fraction as F
from math import lcm


def scaled(terms,prices):
    assert all(isinstance(r,F) and r>=0 and 0<=mask<1<<len(prices) for mask,r in terms)
    assert all(isinstance(q,F) and q>=0 for q in prices)
    den=lcm(*(x.denominator for x in prices),*(r.denominator for _,r in terms))
    demands=[int(r*den) for _,r in terms];caps=[int(q*den) for q in prices]
    supports=[[i for i in range(len(prices)) if mask&(1<<i)] for mask,_ in terms]
    return den,demands,caps,supports


def greedy(terms,prices):
    den,demands,caps,supports=scaled(terms,prices);left=caps.copy();allocation=[]
    pressure=[sum(i in row for row in supports) for i in range(len(caps))]
    for e in sorted(range(len(terms)),key=lambda e:(len(supports[e]),-demands[e],e)):
        remaining=demands[e]
        order=sorted(supports[e],key=lambda i:(pressure[i]/max(1,left[i]),i))
        for i in order:
            amount=min(remaining,left[i])
            if amount:allocation.append((e,i,F(amount,den)));remaining-=amount;left[i]-=amount
            if not remaining:break
    return allocation


def exact(terms,prices):
    den,demands,caps,supports=scaled(terms,prices);n=len(terms);m=len(prices);s=n+m;t=s+1;adj=[[] for _ in range(t+1)];edges=[];incidences=[]
    def add(u,v,c):
        k=len(edges);edges.extend([[u,v,c],[v,u,0]]);adj[u].append(k);adj[v].append(k+1);return k
    for e,d in enumerate(demands):add(s,e,d)
    big=1+sum(demands)
    for e,row in enumerate(supports):
        for i in row:incidences.append((e,i,add(e,n+i,big)))
    for i,c in enumerate(caps):add(n+i,t,c)
    phases=0
    while True:
        level=[-1]*(t+1);level[s]=0;queue=deque([s])
        while queue:
            u=queue.popleft()
            for e in adj[u]:
                _,v,c=edges[e]
                if c and level[v]<0:level[v]=level[u]+1;queue.append(v)
        if level[t]<0:break
        phases+=1;next_edge=[0]*(t+1)
        def push(u,limit):
            if u==t:return limit
            while next_edge[u]<len(adj[u]):
                e=adj[u][next_edge[u]];_,v,c=edges[e]
                if c and level[v]==level[u]+1:
                    amount=push(v,min(c,limit))
                    if amount:edges[e][2]-=amount;edges[e^1][2]+=amount;return amount
                next_edge[u]+=1
            return 0
        while push(s,big):pass
    allocation=[(e,i,F(edges[k^1][2],den)) for e,i,k in incidences if edges[k^1][2]]
    reachable={j for j,l in enumerate(level) if l>=0}
    cut=sum(demands[e] for e in range(n) if e not in reachable)+sum(caps[i] for i in range(m) if n+i in reachable)
    assert all(not (e in reachable and n+i not in reachable) for e,row in enumerate(supports) for i in row)
    assert sum(a for _,_,a in allocation)==F(cut,den)
    return allocation,dict(cut=F(cut,den),phases=phases)


def check(terms,prices,allocation):
    received=[F(0)]*len(terms);spent=[F(0)]*len(prices);seen=set()
    for e,i,amount in allocation:
        assert type(e) is int and type(i) is int and 0<=e<len(terms) and 0<=i<len(prices)
        assert (e,i) not in seen and isinstance(amount,F) and amount>=0 and terms[e][0]&(1<<i)
        seen.add((e,i));received[e]+=amount;spent[i]+=amount
    assert all(a<=r for a,(_,r) in zip(received,terms)) and all(a<=q for a,q in zip(spent,prices))
    total=sum(received);upper=sum(r for _,r in terms)-total
    return dict(upper=upper,allocated=total,nonzero_incidences=len(allocation))
