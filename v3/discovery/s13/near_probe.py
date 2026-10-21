"""Development min-marginal/warrant screen, all action spaces deliberately small."""
from pathlib import Path
from itertools import product
import hashlib
import importlib.util
import json
import random
import time

ROOT=Path(__file__).resolve().parent
dep=ROOT/'ordered_probe.py'
spec=importlib.util.spec_from_file_location('ordered_helpers',dep)
H=importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)  # main guard prevents re-running its experiment
RNG=random.Random(202610208)


def exact_level(upper,i,s):
    return [(H.TRUE,H.bit(upper,i,s)),(H.bit(upper,i,s+1),H.FALSE)]


def run():
    started=time.perf_counter()
    count=dict(panels=0,cutoff_cases=0,mincut_calls=0,projected_pairs=0,
               repricings=0,inside_exact_oscillation=0,inside_separable_bound=0,
               accepted_guards_outside_bound=0,strict_warrant_enlargements=0)
    witness=None
    for n in range(2,5):
        for case in range(16):
            upper=tuple(RNG.randrange(1,4) for _ in range(n))
            actions=list(product(*(range(k+1) for k in upper)))
            worlds=list(product(*(range(k+2) for k in upper)))
            seedworlds=list(product(*(range(k+1) for k in upper)))
            source=set(RNG.sample(seedworlds,RNG.randrange(1,min(8,len(seedworlds))+1)))
            edges=list({tuple(RNG.sample(range(n),2)) for _ in range(RNG.randrange(1,2*n+1))})
            units=[(RNG.randrange(n),True)]
            availability=[]
            for _ in range(RNG.randrange(n+1)):
                i,j=RNG.sample(range(n),2)
                availability.append((H.bit(upper,i,RNG.randrange(upper[i]+1)),
                                     H.bit(upper,j,RNG.randrange(upper[j]+1))))
            prices=[tuple(RNG.randrange(10) for _ in range(k+1)) for k in upper]
            arcs=H.compile_actions(upper,source,edges,units,availability)
            allowed={a for a in actions if H.accepts(a,arcs)}
            assert allowed
            oldcost=lambda a:sum(prices[i][a[i]] for i in range(n))
            optimum,chosen=H.optimize(upper,arcs,prices)
            count['mincut_calls']+=1
            assert optimum==min(map(oldcost,allowed))
            pair_min={}
            for i,j in edges:
                for s in range(upper[i]+1):
                    for t in range(upper[j]+1):
                        cost,_=H.optimize(upper,arcs+exact_level(upper,i,s)+exact_level(upper,j,t),prices)
                        pair_min[i,j,s,t]=cost
                        count['mincut_calls']+=1
            one_min={}
            for i,_ in units:
                for s in range(upper[i]+1):
                    cost,_=H.optimize(upper,arcs+exact_level(upper,i,s),prices)
                    one_min[i,s]=cost
                    count['mincut_calls']+=1
            for epsilon in (0,1,3,7):
                near={a for a in allowed if oldcost(a)<=optimum+epsilon}
                tu=tuple(k+1 for k in upper)
                warcs=H.chains(tu)
                for i,j in edges:
                    pairs={(s,t) for s in range(upper[i]+1) for t in range(upper[j]+1)
                           if pair_min[i,j,s,t] is not None and pair_min[i,j,s,t]<=optimum+epsilon}
                    assert pairs=={(a[i],a[j]) for a in near}
                    count['projected_pairs']+=len(pairs)
                    warcs.extend((H.bit(tu,j,t+1),H.bit(tu,i,s+1)) for s,t in pairs)
                for i,b in units:
                    levels={s for s in range(upper[i]+1) if one_min[i,s] is not None and one_min[i,s]<=optimum+epsilon}
                    assert levels=={a[i] for a in near}
                    warcs.append((H.bit(tu,i,min(levels)+1),H.FALSE))
                warrant={w for w in worlds if H.accepts(w,warcs)}
                exact={w for w in worlds if all(H.goal_ok(a,w,edges,units) for a in near)}
                assert warrant==exact and source<=warrant
                retained={a for a in actions if H.accepts(a,availability) and all(H.goal_ok(a,w,edges,units) for w in warrant)}
                assert near<=retained<=allowed
                assert {a for a in retained if oldcost(a)<=optimum+epsilon}==near
                if source<warrant:count['strict_warrant_enlargements']+=1
                for _ in range(6):
                    change=[tuple(RNG.randrange(-2,3) for _ in range(k+1)) for k in upper]
                    delta=lambda a:sum(change[i][a[i]] for i in range(n))
                    newcost=lambda a:oldcost(a)+delta(a)+2*n
                    osc=max(map(delta,allowed))-min(map(delta,allowed))
                    sep=sum(max(row)-min(row) for row in change)
                    assert osc<=sep
                    newbest=min(map(newcost,allowed))
                    newopt={a for a in allowed if newcost(a)==newbest}
                    retainedbest=min(map(newcost,retained))
                    if osc<=epsilon:
                        assert newopt<=near and retainedbest==newbest
                        count['inside_exact_oscillation']+=1
                    if sep<=epsilon:count['inside_separable_bound']+=1
                    elif any(a in near for a in newopt):count['accepted_guards_outside_bound']+=1
                    if witness is None and osc<=epsilon and source<warrant and near<allowed:
                        witness=dict(n=n,upper=upper,source_size=len(source),warrant_size=len(warrant),
                                     allowed_count=len(allowed),protected_count=len(near),epsilon=epsilon,
                                     old_optimum=optimum,new_optimum=newbest,oscillation=osc,
                                     separable_bound=sep,goal_edges=edges,goal_units=units,
                                     prices=prices,changes=change)
                    count['repricings']+=1
                count['cutoff_cases']+=1
            count['panels']+=1
    assert witness is not None
    return dict(status='PASS',contributor='Codex (GPT-6)',seed=202610208,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in (dep,ROOT/'edge_extension.py')},
                counts=count,example=witness,elapsed_seconds=time.perf_counter()-started,
                scope='Finite exposed correctness comparisons; counts are work performed, not a speedup claim')


if __name__=='__main__':
    result=run()
    (ROOT/'near_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
