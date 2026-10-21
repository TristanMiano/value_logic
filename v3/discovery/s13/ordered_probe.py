"""Finite exact development check of ordered_responses.md, no application claim."""
from pathlib import Path
from itertools import product
from collections import deque
import ast
import hashlib
import json
import random
import time

ROOT=Path(__file__).resolve().parent
RNG=random.Random(202610207)
dependency=ROOT/'edge_extension.py'
tree=ast.parse(dependency.read_text(encoding='utf-8'))
space={'deque':deque}
exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='Flow'],
                       type_ignores=[]),str(dependency),'exec'),space)
Flow=space['Flow']
TRUE=(-1,1)
FALSE=(-1,0)


def bit(upper,i,k):
    return TRUE if k<=0 else FALSE if k>upper[i] else (i,k)


def val(x,node):
    return bool(node[1]) if node[0]<0 else x[node[0]]>=node[1]


def accepts(x,arcs):
    return all(not val(x,u) or val(x,v) for u,v in arcs)


def chains(upper):
    return [(bit(upper,i,k+1),bit(upper,i,k)) for i in range(len(upper)) for k in range(1,upper[i])]


def goal_ok(a,theta,edges,units):
    y=tuple(ai>=ti for ai,ti in zip(a,theta))
    return all(not y[i] or y[j] for i,j in edges) and all(y[i]==b for i,b in units)


def compile_actions(upper,source,edges,units,availability):
    assert source
    arcs=chains(upper)+list(availability)
    for i,j in edges:
        for k in range(upper[i]+1):
            r=max([0]+[theta[j] for theta in source if theta[i]<=k])
            arcs.append((bit(upper,i,k),bit(upper,j,r)))
    for i,b in units:
        if b:
            arcs.append((TRUE,bit(upper,i,max(theta[i] for theta in source))))
        else:
            arcs.append((bit(upper,i,min(theta[i] for theta in source)),FALSE))
    return arcs


def compile_warrant(upper,allowed,edges,units):
    tu=tuple(k+1 for k in upper)
    arcs=chains(tu)
    if not allowed:return arcs
    for i,j in edges:
        for s,t in {(a[i],a[j]) for a in allowed}:
            arcs.append((bit(tu,j,t+1),bit(tu,i,s+1)))
    for i,b in units:
        if b:
            arcs.append((bit(tu,i,1+min(a[i] for a in allowed)),FALSE))
        else:
            arcs.append((TRUE,bit(tu,i,1+max(a[i] for a in allowed))))
    return arcs


def optimize(upper,arcs,costs):
    nodes=[(i,k) for i in range(len(upper)) for k in range(1,upper[i]+1)]
    index={node:i for i,node in enumerate(nodes)}
    s,t=len(nodes),len(nodes)+1
    deltas={(i,k):costs[i][k]-costs[i][k-1] for i,k in nodes}
    infinity=1+sum(abs(d) for d in deltas.values())
    flow=Flow(t+1);offset=sum(c[0] for c in costs)
    for node,d in deltas.items():
        if d>=0:flow.add(index[node],t,d)
        else:flow.add(s,index[node],-d);offset+=d
    for u,v in arcs:
        if u==FALSE or v==TRUE:continue
        if u==TRUE and v==FALSE:return None,None
        flow.add(s if u==TRUE else index[u],t if v==FALSE else index[v],infinity)
    cut,reachable=flow.maxflow(s,t)
    if cut>=infinity:return None,None
    action=tuple(max([0]+[k for k in range(1,upper[i]+1) if index[i,k] in reachable]) for i in range(len(upper)))
    assert accepts(action,arcs)
    assert sum(costs[i][a] for i,a in enumerate(action))==offset+cut
    return offset+cut,action


def run():
    start=time.perf_counter()
    counts=dict(panels=0,actions_checked=0,warrant_worlds_checked=0,
                feasible_optima=0,infeasible=0,receipt_checks=0,strict_warrant_enlargements=0)
    examples=[]
    for n in range(2,5):
        for _ in range(36):
            upper=tuple(RNG.randrange(1,4) for _ in range(n))
            actions=list(product(*(range(k+1) for k in upper)))
            worlds=list(product(*(range(k+2) for k in upper)))
            source=set(RNG.sample(worlds,RNG.randrange(1,min(9,len(worlds))+1)))
            edges=[tuple(RNG.sample(range(n),2)) for _ in range(RNG.randrange(2*n+1))]
            units=[(i,bool(RNG.randrange(2))) for i in RNG.sample(range(n),RNG.randrange(3))]
            availability=[]
            for _ in range(RNG.randrange(n+1)):
                i,j=RNG.sample(range(n),2)
                availability.append((bit(upper,i,RNG.randrange(upper[i]+1)),bit(upper,j,RNG.randrange(upper[j]+1))))
            costs=[tuple(RNG.randrange(13) for _ in range(k+1)) for k in upper]
            arcs=compile_actions(upper,source,edges,units,availability)
            compiled={a for a in actions if accepts(a,arcs)}
            direct={a for a in actions if accepts(a,availability) and all(goal_ok(a,w,edges,units) for w in source)}
            assert compiled==direct
            best=min((sum(costs[i][a[i]] for i in range(n)) for a in direct),default=None)
            got,chosen=optimize(upper,arcs,costs)
            assert got==best
            counts['feasible_optima' if got is not None else 'infeasible']+=1
            warcs=compile_warrant(upper,compiled,edges,units)
            warrant={w for w in worlds if accepts(w,warcs)}
            exact={w for w in worlds if all(goal_ok(a,w,edges,units) for a in compiled)}
            assert warrant==exact and source<=warrant
            again=compile_actions(upper,warrant,edges,units,availability)
            assert {a for a in actions if accepts(a,again)}==compiled
            for i in range(n):
                q=RNG.randrange(upper[i]+1)
                for high in (False,True):
                    sf={w for w in source if (w[i]>q)==high}
                    sw={w for w in warrant if (w[i]>q)==high}
                    if not sf:continue
                    af={a for a in actions if accepts(a,availability) and all(goal_ok(a,w,edges,units) for w in sf)}
                    aw={a for a in actions if accepts(a,availability) and all(goal_ok(a,w,edges,units) for w in sw)}
                    assert compiled<=aw<=af
                    counts['receipt_checks']+=1
            counts['panels']+=1
            counts['actions_checked']+=len(actions)
            counts['warrant_worlds_checked']+=len(worlds)
            if source<warrant:
                counts['strict_warrant_enlargements']+=1
                if got is not None and len(examples)<2:
                    examples.append(dict(upper=upper,source=sorted(source),warrant_size=len(warrant),
                        edges=edges,units=units,availability=availability,costs=costs,
                        optimum=got,action=chosen,allowed_actions=len(compiled)))
    return dict(status='PASS',contributor='Codex (GPT-6)',seed=202610207,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256={dependency.name:hashlib.sha256(dependency.read_bytes()).hexdigest()},
                counts=counts,examples=examples,elapsed_seconds=time.perf_counter()-start,
                scope='Exact exposed finite panels; no independent confirmation or empirical savings')


if __name__=='__main__':
    result=run()
    (ROOT/'ordered_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
