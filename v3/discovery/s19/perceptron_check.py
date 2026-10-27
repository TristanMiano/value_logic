"""s19 bounded DEVELOPMENT check; standard library, exact integer arithmetic."""
from collections import deque
from itertools import combinations, product
from pathlib import Path
import hashlib, json, platform, time

HERE=Path(__file__).resolve().parent
OUT=HERE/'perceptron_result.json'
assert not OUT.exists(), 'Frozen result already exists; do not overwrite'
started=time.perf_counter_ns()

def zvec(n):
 m=n//2
 return tuple(range(m,-m-1,-1)) if n%2 else tuple(range(m,0,-1))+tuple(range(-1,-m-1,-1))

def inside(v):
 z=zvec(len(v))
 return sum(v)==0 and all(sum(sorted(v,reverse=True)[:k])<=sum(z[:k]) for k in range(1,len(v)))

def transfer_screen(n):
 initial=(0,)*n
 seen={initial}; q=deque([initial]); edges=0
 while q:
  v=q.popleft()
  for a in range(n):
   for b in range(n):
    if a==b or v[a]>v[b]: continue
    w=list(v); w[a]+=1; w[b]-=1; w=tuple(w)
    assert inside(w),(n,v,a,b,w)
    edges+=1
    if w not in seen: seen.add(w); q.append(w)
 return dict(d=n,states=len(seen),transitions=edges,max_abs=max(map(abs,(x for v in seen for x in v))))

def matroids(n):
 out=[]
 for r in range(n+1):
  candidates=[frozenset(b) for b in combinations(range(n),r)]
  for mask in range(1,1<<len(candidates)):
   fs=frozenset(b for i,b in enumerate(candidates) if mask>>i&1)
   if all(any((a-{x})|{y} in fs for y in b-a) for a in fs for b in fs for x in a-b):
    out.append(tuple(sorted(tuple(sorted(b)) for b in fs)))
 return out

def weakorders(n):
 out=set()
 for u in product(range(n),repeat=n):
  levels={x:i for i,x in enumerate(sorted(set(u)))}
  out.add(tuple(levels[x] for x in u))
 return sorted(out)

def scc(adj):
 # Iterative Kosaraju, independent of the charging argument.
 seen=set(); order=[]
 for root in range(len(adj)):
  if root in seen: continue
  seen.add(root); stack=[(root,iter(adj[root]))]
  while stack:
   v,it=stack[-1]
   try:
    w,_=next(it)
    if w not in seen:
     seen.add(w); stack.append((w,iter(adj[w])))
   except StopIteration:
    stack.pop(); order.append(v)
 rev=[[] for _ in adj]
 for v,edges in enumerate(adj):
  for w,_ in edges: rev[w].append(v)
 comp={}; c=0
 for root in reversed(order):
  if root in comp: continue
  comp[root]=c; stack=[root]
  while stack:
   v=stack.pop()
   for w in rev[v]:
    if w not in comp: comp[w]=c; stack.append(w)
  c+=1
 return comp,c

def exact_game(n,u,ms):
 initial=((0,)*n,0)
 states=[initial]; ids={initial:0}; adj=[]; q=deque([initial]); transitions=0
 while q:
  v,c=q.popleft(); edges={}
  for bases in ms:
   b=min(bases,key=lambda b:(-sum(v[i] for i in b),b))
   ub=sum(u[i] for i in b); best=max(sum(u[i] for i in a) for a in bases)
   wrong=int(ub<best)
   for a in bases:
    bad=int(sum(u[i] for i in a)<best)
    if c+bad>1: continue
    w=tuple(v[i]+int(i in a)-int(i in b) for i in range(n))
    assert inside(w),(u,v,b,a,w)
    target=(w,c+bad)
    if target not in ids: ids[target]=len(states); states.append(target); q.append(target)
    j=ids[target]; edges[j]=max(edges.get(j,0),wrong); transitions+=1
  adj.append(sorted(edges.items()))
 comp,nc=scc(adj)
 dag=[{} for _ in range(nc)]; indeg=[0]*nc
 for i,edges in enumerate(adj):
  for j,cost in edges:
   x,y=comp[i],comp[j]
   if x==y: assert cost==0,('positive mistake cycle',n,u,states[i],states[j])
   else: dag[x][y]=max(dag[x].get(y,0),cost)
 for edges in dag:
  for y in edges: indeg[y]+=1
 ready=deque(i for i,a in enumerate(indeg) if not a); dist=[-10**9]*nc; dist[comp[0]]=0
 while ready:
  x=ready.popleft()
  for y,w in dag[x].items():
   dist[y]=max(dist[y],dist[x]+w); indeg[y]-=1
   if not indeg[y]: ready.append(y)
 maxima=[max(dist[comp[i]] for i,(_,c) in enumerate(states) if c<=limit) for limit in (0,1)]
 Q=n*(n*n-1)//12 if n%2 else n*(n+2)*(2*n-1)//24
 for c,m in enumerate(maxima): assert m<=Q+c*((n*n)//4+1),(n,u,c,m,Q)
 return dict(d=n,truth=u,states=len(states),transitions=transitions,scc=nc,max_mistakes_C0=maxima[0],max_mistakes_C1=maxima[1],bound_C0=Q,bound_C1=Q+(n*n)//4+1)

transfer=[transfer_screen(n) for n in range(2,7)]
games=[]; counts={}
for n in range(2,5):
 ms=matroids(n); counts[n]=len(ms)
 for u in weakorders(n): games.append(exact_game(n,u,ms))
result=dict(status='pass',model='Codex (GPT-6)',evidence='DEVELOPMENT, same-model',python=platform.python_version(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed_ns=time.perf_counter_ns()-started,transfer_screens=transfer,matroid_counts=counts,games=games,scope='All reachable integer-transfer states d=2..6; all weak orders and labeled matroids d=2..4, at most one bad feasible report, unbounded horizon via SCC condensation. This is a finite model check, not independent confirmation or a novelty test.')
OUT.write_bytes((json.dumps(result,indent=2)+'\n').encode())
print(json.dumps(dict(status=result['status'],elapsed_ns=result['elapsed_ns'],transfer=transfer,matroids=counts,games=len(games),states=sum(g['states'] for g in games),transitions=sum(g['transitions'] for g in games),worst={n:{c:max(g['max_mistakes_C'+str(c)] for g in games if g['d']==n) for c in (0,1)} for n in counts})))
