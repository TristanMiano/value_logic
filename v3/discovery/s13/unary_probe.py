"""Finite development screen for local actions and the priced implication fragment."""
from pathlib import Path
from itertools import product
from collections import deque
import ast
import hashlib
import json
import random
import time

ROOT=Path(__file__).resolve().parent
RNG=random.Random(202610206)
flow_path=ROOT/'edge_extension.py'
tree=ast.parse(flow_path.read_text(encoding='utf-8'))
namespace={'deque':deque}
exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='Flow'],
                       type_ignores=[]), str(flow_path), 'exec'),namespace)
Flow=namespace['Flow']


def holds(x,clauses):
    return all(any((x>>i&1)==b for i,b in clause) for clause in clauses)


def models(n,clauses):
    return {x for x in range(1<<n) if holds(x,clauses)}


def random_cnf(n):
    return [tuple((i,RNG.randrange(2)) for i in RNG.sample(range(n),RNG.choice((1,2))))
            for _ in range(RNG.randrange(2*n+1))]


def apply(n,a,x):
    return sum((a>>(2*i+(x>>i&1))&1)<<i for i in range(n))


def first_pass(source,goal):
    return tuple(sorted({tuple(sorted((2*i+(x>>i&1),b) for i,b in clause))
                         for clause in goal for x in source}))


def second_pass(allowed,goal):
    clauses=set()
    for clause in goal:
        for pattern in product(range(2),repeat=len(clause)):
            if any(all((a>>(2*i+xbit)&1)!=b for (i,b),xbit in zip(clause,pattern)) for a in allowed):
                clauses.add(tuple(sorted((i,1-xbit) for (i,b),xbit in zip(clause,pattern))))
    return tuple(sorted(clauses))


def monotone(n):
    return [((2*i,0),(2*i+1,1)) for i in range(n)]


def price(n,a,costs):
    kinds=[(a>>(2*i)&1,a>>(2*i+1)&1) for i in range(n)]
    assert all(k!=(1,0) for k in kinds)
    return sum(c0 if k==(0,0) else c1 if k==(1,1) else 0 for k,(c0,c1) in zip(kinds,costs))


def mincut(n,clauses,costs):
    s,t=2*n,2*n+1
    flow=Flow(t+1)
    inf=1+sum(sum(c) for c in costs)
    for i,(c0,c1) in enumerate(costs):
        flow.add(s,2*i+1,c0)
        flow.add(2*i,t,c1)
    for clause in clauses:
        if len(clause)==1:
            i,b=clause[0]
            flow.add(s,i,inf) if b else flow.add(i,t,inf)
        else:
            negatives=[i for i,b in clause if b==0]
            positives=[i for i,b in clause if b==1]
            assert len(negatives)==len(positives)==1
            flow.add(negatives[0],positives[0],inf)
    paid,reachable=flow.maxflow(s,t)
    if paid>=inf:return None,None
    action=sum(1<<i for i in range(2*n) if i in reachable)
    assert holds(action,clauses) and price(n,action,costs)==paid
    return paid,action


def run():
    start=time.perf_counter()
    stats=dict(general_panels=0,world_action_checks=0,closure_checks=0,
               mincut_panels=0,feasible_repairs=0,infeasible_repairs=0)
    witness=None
    for n in range(2,6):
        worlds=set(range(1<<n));actions=set(range(1<<(2*n)))
        for case in range(24):
            source=models(n,random_cnf(n))
            if not source:continue
            goal=random_cnf(n)
            avail=random_cnf(2*n)
            if case%2:avail+=monotone(n)
            available=models(2*n,avail)
            compiled=first_pass(source,goal)
            allowed=models(2*n,compiled)&available
            direct={a for a in available if all(holds(apply(n,a,x),goal) for x in source)}
            assert allowed==direct
            closure=models(n,second_pass(allowed,goal))
            exact={x for x in worlds if all(holds(apply(n,a,x),goal) for a in allowed)}
            assert closure==exact and source<=closure
            assert models(2*n,first_pass(closure,goal))&available==allowed
            stats['general_panels']+=1
            stats['world_action_checks']+=len(source)*len(available)
            stats['closure_checks']+=len(worlds)*len(allowed)
        for _ in range(28):
            source=models(n,random_cnf(n))
            if not source:continue
            goal=[]
            for _ in range(RNG.randrange(1,2*n+1)):
                i,j=RNG.sample(range(n),2)
                goal.append(((i,0),(j,1)))
            for i in RNG.sample(range(n),RNG.randrange(3)):
                goal.append(((i,RNG.randrange(2)),))
            compiled=list(first_pass(source,goal))+monotone(n)
            costs=[(RNG.randrange(1,10),RNG.randrange(1,10)) for _ in range(n)]
            feasible=models(2*n,compiled)
            best=min((price(n,a,costs) for a in feasible),default=None)
            got,chosen=mincut(n,compiled,costs)
            assert best==got
            stats['mincut_panels']+=1
            if got is None:
                stats['infeasible_repairs']+=1
                continue
            stats['feasible_repairs']+=1
            closure=models(n,second_pass(feasible,goal))
            assert all(holds(apply(n,chosen,x),goal) for x in closure)
            reset_actions={a for a in feasible if all((a>>(2*i)&1)==(a>>(2*i+1)&1) for i in range(n))}
            reset=min((price(n,a,costs) for a in reset_actions),default=None)
            if witness is None and source<closure and reset is not None and got<reset:
                witness=dict(n=n,source=sorted(source),closure=sorted(closure),goal=goal,
                             costs=costs,selected_action=chosen,write_fee=got,blind_reset_fee=reset)
    assert witness is not None
    return dict(status='PASS',contributor='Codex (GPT-6)',seed=202610206,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256={flow_path.name:hashlib.sha256(flow_path.read_bytes()).hexdigest()},
                statistics=stats,constructed_witness=witness,
                elapsed_seconds=time.perf_counter()-start,
                scope='Exposed finite compiler and optimizer checks; constructed command prices, not deployment performance')


if __name__=='__main__':
    result=run()
    (ROOT/'unary_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
