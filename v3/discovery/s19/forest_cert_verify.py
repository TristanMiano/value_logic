"""Rational verifier for rooted forest upper-message certificates.

DEVELOPMENT: compactness and the truth of supplied source premises are external.
No optimizer, producer, or forest solver is imported.
"""
from fractions import Fraction as Q
from math import inf
import hashlib,json

def need(ok,why):
    if not ok: raise ValueError(why)

def digest(problem):
    return hashlib.sha256(json.dumps(problem,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def decode(problem):
    p=dict(bases=[[tuple(map(Q,r)) for r in b] for b in problem['bases']],
           gs=[{int(i):tuple(map(Q,g)) for i,g in group.items()} for group in problem['gs']],
           los=list(map(Q,problem['los'])),his=list(map(Q,problem['his'])),
           fs=[tuple(map(Q,f)) for f in problem['fs']])
    n=len(p['bases']); k=len(p['gs'])
    need(n>0 and len(p['fs'])==n,'block count')
    need(len(p['los'])==len(p['his'])==k,'receipt count')
    for i,f in enumerate(p['fs']):
        need(len(f)>=2 and all(len(r)==len(f) for r in p['bases'][i]),'dimension')
    for j,group in enumerate(p['gs']):
        need(bool(group) and p['los'][j]<=p['his'][j],'receipt interval')
        need(all(0<=i<n and len(g)==len(p['fs'][i]) for i,g in group.items()),'form shape')
    return p

def orientation(p):
    n=len(p['bases']); k=len(p['gs']); adj=[[] for _ in range(n+k)]
    for j,group in enumerate(p['gs']):
        for i in sorted(group): adj[i].append(n+j); adj[n+j].append(i)
    seen=set(); parent={}; order=[]; roots=[]
    for root in range(n):
        if root in seen: continue
        roots.append(root); seen.add(root); parent[root]=None; todo=[root]
        while todo:
            v=todo.pop(); order.append(v)
            for w in adj[v]:
                if w==parent[v]: continue
                need(w not in seen,'incidence cycle')
                seen.add(w); parent[w]=v; todo.append(w)
    need(len(seen)==n+k,'isolated receipt')
    children={i:[] for i in range(n)}
    for j in range(k):
        i=parent[n+j]; children[i].append((j,[h for h in adj[n+j] if h!=i]))
    return roots,parent,children,[i for i in reversed(order) if i<n]

def dot(a,x): return sum(u*v for u,v in zip(a,x))
def value(f,x): return dot(f[:-1],x)+f[-1]
def up(p,j,i):
    g=p['gs'][j][i]; return g[:-1]+(p['his'][j]-g[-1],)
def rows(p,i):
    out=list(p['bases'][i])
    for j,group in enumerate(p['gs']):
        if i in group:
            g=group[i]; out.append(tuple(-a for a in g[:-1])+(g[-1]-p['los'][j],))
    return out

def dual_check(rs,lam,target,rhs,empty=False):
    lam=list(map(Q,lam)); d=len(target)
    need(len(lam)==len(rs) and all(v>=0 for v in lam),'dual signs/length')
    need(all(sum(lam[t]*rs[t][j] for t in range(len(rs)))==target[j] for j in range(d)),'dual coefficients')
    b=sum(v*r[-1] for v,r in zip(lam,rs))
    need(b<0 if empty else b<=rhs,'dual bound')

def verify(problem,cert):
    need(cert['problem_sha256']==digest(problem),'problem binding')
    p=decode(problem); roots,parent,children,order=orientation(p); n=len(p['bases'])
    need(set(cert['messages'])==set(map(str,range(n))),'message coverage')
    bounds={}; kinds={}
    for i in order:
        group=cert['messages'][str(i)]; par=parent[i]
        need(set(group)==({'A'} if par is None else {'A','B'}),'message variants')
        cap=min((bounds[(h,'A')] for j,hs in children[i] for h in hs),default=inf)
        ts={j:max((bounds[(h,'B')] for h in hs),default=-inf) for j,hs in children[i]}
        for variant,e in group.items():
            r=-inf if e['value'] is None else Q(e['value']); bounds[i,variant]=r
            base=rows(p,i)
            if variant=='B': base.append(up(p,par-n,i))
            proof=e['proof']; kind=proof['kind']; kinds[kind]=kinds.get(kind,0)+1
            if r==-inf:
                need(e['x'] is None,'empty witness')
                if kind=='child_empty': need(cap==-inf,'empty child')
                else:
                    need(kind=='empty','empty proof kind')
                    base.extend(up(p,j,i) for j,t in ts.items() if t==-inf)
                    dual_check(base,proof['dual'],[Q(0)]*(len(p['fs'][i])-1),None,True)
                continue
            x=tuple(map(Q,e['x'])); need(len(x)==len(p['fs'][i])-1,'primal dimension')
            need(all(dot(a[:-1],x)<=a[-1] for a in base),'primal rows')
            need(value(p['fs'][i],x)>=r and cap>=r,'primal objective/children')
            for j,hs in children[i]:
                need(value(p['gs'][j][i],x)<=p['his'][j] or ts[j]>=r,'receipt witness')
            if kind=='child_cap': need(cap==r,'child upper cap')
            else:
                need(cap>r and kind in ('empty','dual'),'upper proof kind')
                base.extend(up(p,j,i) for j,t in ts.items() if t<=r)
                if kind=='empty': dual_check(base,proof['dual'],[Q(0)]*len(x),None,True)
                else: dual_check(base,proof['dual'],p['fs'][i][:-1],r-p['fs'][i][-1])
    answer=min(bounds[i,'A'] for i in roots)
    need((cert['upper'] is None and answer==-inf) or
         (cert['upper'] is not None and answer==Q(cert['upper'])),'global upper')
    return answer,kinds
