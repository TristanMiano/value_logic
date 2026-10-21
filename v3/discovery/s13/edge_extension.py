"""Prospective cheap screen only: 500 trees, <=30s, no all-size assertion.
Check a conjectured higher-cap edge inequality using exact maximum closure.
Codex (GPT-6), DEVELOPMENT. Retain any counterexample without tuning it away.
"""
from collections import deque
from pathlib import Path
from itertools import product
import hashlib
import json
import random
import time

HERE=Path(__file__).resolve().parent
rng=random.Random(91320261020)
begun=time.perf_counter_ns()

class Flow:
    def __init__(self,n):self.g=[[] for _ in range(n)]
    def add(self,u,v,c):
        self.g[u].append([v,c,len(self.g[v])])
        self.g[v].append([u,0,len(self.g[u])-1])
    def maxflow(self,s,t):
        total=0
        while True:
            level=[-1]*len(self.g);level[s]=0;queue=deque([s])
            while queue:
                u=queue.popleft()
                for v,c,_ in self.g[u]:
                    if c and level[v]<0:level[v]=level[u]+1;queue.append(v)
            if level[t]<0:break
            ptr=[0]*len(self.g)
            def send(u,amount):
                if u==t:return amount
                while ptr[u]<len(self.g[u]):
                    e=self.g[u][ptr[u]];v,c,r=e
                    if c and level[v]==level[u]+1:
                        got=send(v,min(amount,c))
                        if got:e[1]-=got;self.g[v][r][1]+=got;return got
                    ptr[u]+=1
                return 0
            while True:
                sent=send(s,10**20)
                if not sent:break
                total+=sent
        seen={s};queue=deque([s])
        while queue:
            for v,c,_ in self.g[queue.popleft()]:
                if c and v not in seen:seen.add(v);queue.append(v)
        return total,seen

def screen(costs,n,cap):
    edges=[(x,x^(1<<i)) for x in range(1<<n) for i in range(n)
           if not (x>>i&1) and costs[x]!=costs[x^(1<<i)]]
    a=(1<<cap)-1;b=(1<<(cap-1))-1
    vcount=len(costs);s=vcount+len(edges);t=s+1
    g=Flow(t+1);positive=a*len(edges);inf=positive+b*sum(costs)+1
    for x,c in enumerate(costs):g.add(x,t,b*c)
    for k,(x,y) in enumerate(edges):
        node=vcount+k;g.add(s,node,a);g.add(node,x,inf);g.add(node,y,inf)
    paid,reachable=g.maxflow(s,t)
    w={x for x in range(vcount) if x in reachable}
    profit=a*sum(x in w and y in w for x,y in edges)-b*sum(costs[x] for x in w)
    assert profit==positive-paid
    return profit,w

def tree(available,depth,stop):
    if not available or not depth or rng.random()<stop:return None
    i=rng.choice(available);rest=tuple(j for j in available if j!=i)
    return i,tree(rest,depth-1,stop),tree(rest,depth-1,stop)

def bill(tr,x):
    return 0 if tr is None else 1+bill(tr[1+(x>>tr[0]&1)],x)

# Validate this reduction on arbitrary small invoice-value maps by enumeration.
validated=0
for _ in range(25):
    costs=[rng.randrange(1,4) for _ in range(8)]
    gain,w=screen(costs,3,3)
    edges=[(x,x^(1<<i)) for x in range(8) for i in range(3)
           if not (x>>i&1) and costs[x]!=costs[x^(1<<i)]]
    exact=max(7*sum(mask>>x&1 and mask>>y&1 for x,y in edges)-
              3*sum(costs[x] for x in range(8) if mask>>x&1) for mask in range(256))
    assert gain==exact
    validated+=1

panels=[];counter=None;budget=False
for cap,n,limit in [(4,7,300),(5,8,100),(6,8,100)]:
    completed=0
    for k in range(limit):
        if time.perf_counter_ns()-begun>30_000_000_000:budget=True;break
        tr=tree(tuple(range(n)),cap,(.05,.15,.3,.5)[k%4])
        costs=[bill(tr,x) for x in range(1<<n)]
        gain,w=screen(costs,n,cap)
        completed+=1
        if gain>0:
            counter=dict(cap=cap,n=n,case=k,gain=gain,worlds=sorted(w),tree=tr,
                         costs=costs)
            break
    panels.append(dict(cap=cap,n=n,completed=completed,planned=limit))
    if counter or budget:break
result=dict(status='COUNTEREXAMPLE' if counter else 'BUDGET' if budget else 'NO_COUNTEREXAMPLE_IN_PANEL',
            contributor='Codex (GPT-6)',seed=91320261020,closure_validation_maps=validated,
            panels=panels,counterexample=counter,elapsed_ns=time.perf_counter_ns()-begun,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='finite generated private trees only; no proof of conjectured general cap inequality')
(HERE/'edge_extension.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='counterexample'}))
if counter:print(json.dumps({k:v for k,v in counter.items() if k not in ('costs','tree','worlds')}))
