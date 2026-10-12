"""Fresh exact full-belief and subset comparisons for arbitrary linear queries."""
import hashlib,json,random,sys,time
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from rank_planner import profile,best,rank,completion

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x

def bellman(rows,costs,d):
    ones=[sum(1<<x for x in range(1<<d) if (row&x).bit_count()&1) for row in rows]
    @lru_cache(None)
    def solve(worlds):
        count=worlds.bit_count();value=F(1,count)
        for mask,q in zip(ones,costs):
            pos=worlds&mask;neg=worlds^pos
            if pos and neg:value=max(value,-q+F(pos.bit_count(),count)*solve(pos)+F(neg.bit_count(),count)*solve(neg))
        return value
    value=solve((1<<(1<<d))-1)
    return value,solve.cache_info().currsize

def main(out):
    assert not out.exists();base=Path(__file__).parent;seed=16042;rng=random.Random(seed);start=time.perf_counter_ns()
    sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['rank_planner.py','rank_probe.py']}
    cases=[];subset_checks=0;action_checks=0
    for k in range(36):
        d=rng.randrange(2,7);m=rng.randrange(2,10);rows=[rng.randrange(1<<d) for _ in range(m)]
        costs=[F(rng.randrange(0,17),64) for _ in rows];points=profile(rows,costs,d);chosen=best(points)
        value,states=bellman(rows,costs,d)
        assert value==chosen['success']-chosen['cost']
        minimum={0:F(0)}
        for mask in range(1<<m):
            selected=[j for j in range(m) if mask>>j&1];r=rank([rows[j] for j in selected]);cost=sum((costs[j] for j in selected),F(0))
            minimum[r]=min(cost,minimum.get(r,cost));subset_checks+=1
        assert all(p['cost']==minimum[p['rank']] for p in points)
        actions=[]
        for x in range(1<<d):
            query_rows=[rows[j] for j in chosen['queries']];labels=[(row&x).bit_count()&1 for row in query_rows]
            guess=completion(query_rows,labels,d);actions.append(guess);action_checks+=1
        assert F(sum(guess==x for x,guess in enumerate(actions)),1<<d)==chosen['success']
        cases.append(dict(index=k,d=d,rows=rows,costs=costs,profile=points,chosen=chosen,adaptive_value=value,belief_states=states,guesses=actions))
    d=128;m=512;begin=time.perf_counter_ns();rows=[]
    for _ in range(m):rows.append(sum(1<<i for i in rng.sample(range(d),rng.randrange(1,9))))
    costs=[F(rng.randrange(1,65),32768) for _ in rows];construction_ns=time.perf_counter_ns()-begin
    begin=time.perf_counter_ns();points=profile(rows,costs,d);profile_ns=time.perf_counter_ns()-begin
    prices=[F(i,16) for i in range(129)];begin=time.perf_counter_ns();choices=[best(points,p) for p in prices];query_ns=time.perf_counter_ns()-begin
    chosen=best(points);x=rng.getrandbits(d);query_rows=[rows[j] for j in chosen['queries']]
    # Supplied observation labels. Completing the decision is timed separately;
    # this does not measure buying the real mathematical query results.
    labels=[(row&x).bit_count()&1 for row in query_rows]
    begin=time.perf_counter_ns();guess=completion(query_rows,labels,d);completion_ns=time.perf_counter_ns()-begin
    assert all(((row&guess).bit_count()&1)==y for row,y in zip(query_rows,labels))
    bad_rejected=False
    try:completion([1,1],[0,1],1)
    except AssertionError:bad_rejected=True
    assert bad_rejected
    large=dict(d=d,rows=rows,costs=costs,profile=points,prices=prices,selected_ranks=[p['rank'] for p in choices],chosen=chosen,
        construction_ns=construction_ns,profile_ns=profile_ns,query_ns=query_ns,completion_ns=completion_ns,labels=labels,guess=guess)
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=seed,sources=sources,cases=cases,
        subset_checks=subset_checks,action_checks=action_checks,large=large,inconsistent_labels_rejected=bad_rejected,elapsed_ns=time.perf_counter_ns()-start,
        limits='Uniform latent source and priced pure linear queries supplied. Full-assignment objective differs from weighted coordinate prediction. Ordinary matroid greedy is the algorithm; no comparative real-world speedup or external query-cost measurement.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',cases=len(cases),subset_checks=subset_checks,action_checks=action_checks,belief_states=sum(c['belief_states'] for c in cases),
        large={k:large[k] for k in ['construction_ns','profile_ns','query_ns','completion_ns']}|dict(chosen_rank=chosen['rank'],chosen_cost=chosen['cost'],success=chosen['success']),elapsed_ns=result['elapsed_ns']))))

if __name__=='__main__':main(Path(sys.argv[1]))
