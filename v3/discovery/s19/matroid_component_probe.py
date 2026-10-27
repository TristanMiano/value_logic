"""Development screen for a proposed tight-set connectivity characterization."""
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib, json, random, sys, time, traceback

HERE=Path(__file__).resolve().parent


def linear_ranks(columns):
    ranks=[]
    for mask in range(1<<len(columns)):
        basis={}
        for j,value in enumerate(columns):
            if not(mask>>j&1): continue
            x=value
            while x:
                b=x.bit_length()-1
                if b in basis: x^=basis[b]
                else:
                    basis[b]=x
                    break
        ranks.append(len(basis))
    return tuple(ranks)


def analyze(ranks,k):
    n=len(ranks); states={}
    for labels in product(range(n),repeat=k):
        masks=[0]*n
        for j,i in enumerate(labels): masks[i]|=1<<j
        if all(r[m]==m.bit_count() for r,m in zip(ranks,masks)):
            states[labels]=masks
    if not states: return dict(feasible=False,states=0)
    tight=[s for s in range(1<<k) if sum(r[s] for r in ranks)==s.bit_count()]
    star=0
    for s in tight: star|=s
    assert sum(r[star] for r in ranks)==star.bit_count()
    todo=set(states); projections={}; components=0; moves=0
    while todo:
        seed=min(todo); todo.remove(seed); stack=[seed]; keys=set()
        while stack:
            cur=stack.pop(); masks=states[cur]
            keys.add(tuple(cur[j] for j in range(k) if star>>j&1))
            for j,old in enumerate(cur):
                for dest in range(n):
                    if dest==old: continue
                    newmask=masks[dest]|(1<<j)
                    if ranks[dest][newmask]!=newmask.bit_count(): continue
                    neighbor=cur[:j]+(dest,)+cur[j+1:]
                    assert neighbor in states
                    moves+=1
                    if neighbor in todo:
                        todo.remove(neighbor); stack.append(neighbor)
        assert len(keys)==1,('necessary invariant failed',ranks,keys)
        key=next(iter(keys))
        projections.setdefault(key,[]).append(components)
        components+=1
    violations=[(key,ids) for key,ids in projections.items() if len(ids)>1]
    return dict(feasible=True,states=len(states),components=components,
                tight_union=star,strict_slack=star==0,moves=moves,
                violations=violations)


def run():
    all3=sorted({linear_ranks(cols) for cols in product(range(8),repeat=3)})
    cases=[]
    for n in (1,2,3):
        cases.extend((3,rs) for rs in combinations_with_replacement(all3,n))
    exhaustive=len(cases)
    rng=random.Random(191932)
    for trial in range(360):
        k,n=4+trial%4,2+trial%3
        rs=[]
        for i in range(n):
            rank=rng.randrange(k+1)
            if rng.randrange(3)==0:
                rs.append(tuple(min(rank,s.bit_count()) for s in range(1<<k)))
            else:
                rs.append(linear_ranks([rng.randrange(1<<min(rank,4)) for _ in range(k)]))
        cases.append((k,rs))
    raw=(json.dumps(cases,separators=(',',':'))+'\n').encode()
    (HERE/'matroid_component_inputs.json').write_bytes(raw)
    rows=[]; counterexample=None
    for index,(k,rs) in enumerate(cases):
        row=analyze(rs,k); rows.append(dict(case=index,k=k,n=len(rs),**row))
        if row.get('violations'):
            counterexample=dict(case=index,k=k,ranks=rs,result=row)
            break
    return dict(distinct_three_element_rank_tables=len(all3),exhaustive_cases=exhaustive,
                planned_cases=len(cases),completed_cases=len(rows),
                feasible_cases=sum(r['feasible'] for r in rows),
                states=sum(r['states'] for r in rows),
                strict_slack_cases=sum(r.get('strict_slack',False) for r in rows),
                components=sum(r.get('components',0) for r in rows),
                counterexample=counterexample,rows=rows,
                input_sha256=hashlib.sha256(raw).hexdigest())


if __name__=='__main__':
    plan=json.loads((HERE/'matroid_component_plan.json').read_text())
    sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    assert sha==plan['source_sha256']
    assert not (HERE/'matroid_component_result.json').exists()
    started=time.perf_counter_ns()
    try:
        result=dict(status='COMPLETED_SCREEN',source_sha256=sha,results=run(),python=sys.version)
        result['runtime_ns']=time.perf_counter_ns()-started
        (HERE/'matroid_component_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
        print(json.dumps({k:v for k,v in result.items() if k!='results'}))
        print(json.dumps({k:v for k,v in result['results'].items() if k!='rows'}))
    except Exception:
        failure=dict(status='FAIL',traceback=traceback.format_exc(),runtime_ns=time.perf_counter_ns()-started)
        (HERE/'matroid_component_failure.json').write_bytes((json.dumps(failure,indent=2)+'\n').encode())
        raise
