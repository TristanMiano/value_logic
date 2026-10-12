"""Finite adaptive-policy transport under explicit affine source bijections."""
import hashlib,json,random,sys,time
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from affine_source import parity

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x

def source(matrix,b,n):return [x for x in range(1<<n) if all(parity(row&x)==((b>>i)&1) for i,row in enumerate(matrix))]
def rhs(matrix,x):return sum(parity(row&x)<<i for i,row in enumerate(matrix))

def plan(probabilities,rows,costs):
    count=len(probabilities);ones=[sum(1<<x for x in range(count) if parity(row&x)) for row in rows]
    root=sum(1<<x for x,p in enumerate(probabilities) if p);policy={}
    @lru_cache(None)
    def solve(worlds):
        xs=[x for x in range(count) if worlds>>x&1];mass=sum((probabilities[x] for x in xs),F(0))
        guess=max(xs,key=lambda x:probabilities[x]);value=probabilities[guess]/mass;action=('guess',guess)
        for j,q in enumerate(costs):
            pos=worlds&ones[j];neg=worlds^pos
            if not (pos and neg):continue
            pos_mass=sum((probabilities[x] for x in xs if pos>>x&1),F(0))
            trial=-q+(pos_mass*solve(pos)+(mass-pos_mass)*solve(neg))/mass
            if trial>value:value=trial;action=('query',j)
        policy[worlds]=dict(value=value,action=action);return value
    return solve(root),policy,root,ones

def run(policy,root,ones,rows,costs,world,delta):
    state=root;cost=F(0);path=[]
    while True:
        kind,a=policy[state]['action']
        if kind=='guess':return a^delta,cost,path
        observed=parity(rows[a]&world);old_label=observed^parity(rows[a]&delta)
        path.append((a,observed));cost+=costs[a]
        pos=state&ones[a];state=pos if old_label else state^pos

def main(out):
    assert not out.exists();base=Path(__file__).parent;seed=61894;rng=random.Random(seed);start=time.perf_counter_ns()
    sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['affine_source.py','transport_probe.py']}
    cases=[];pair_checks=0;state_count=0
    for k in range(32):
        n=rng.randrange(2,7);matrix=[rng.randrange(1,1<<n) for _ in range(rng.randrange(1,n))];x0=rng.randrange(1<<n);b=rhs(matrix,x0)
        worlds=source(matrix,b,n);raw=[rng.randrange(1,17) for _ in worlds];total=sum(raw);probabilities=[F(0)]*(1<<n)
        for x,w in zip(worlds,raw):probabilities[x]=F(w,total)
        rows=[1<<j for j in range(n)]+[rng.randrange(1,1<<n) for _ in range(3)];costs=[F(rng.randrange(1,17),128) for _ in rows]
        delta=rng.randrange(1<<n);new_b=b^rhs(matrix,delta);new_probabilities=[probabilities[x^delta] for x in range(1<<n)]
        old_value,policy,root,ones=plan(probabilities,rows,costs);new_value,new_policy,new_root,new_ones=plan(new_probabilities,rows,costs)
        assert old_value==new_value;wrapped_value=F(0);pairs=[]
        for x in worlds:
            old_guess,old_cost,old_path=run(policy,root,ones,rows,costs,x,0)
            guess,cost,path=run(policy,root,ones,rows,costs,x^delta,delta)
            assert cost==old_cost and guess==old_guess^delta and [j for j,_ in path]==[j for j,_ in old_path]
            assert (guess==(x^delta))==(old_guess==x)
            wrapped_value+=probabilities[x]*(F(guess==(x^delta))-cost);pair_checks+=1
            pairs.append(dict(old_world=x,new_world=x^delta,old_guess=old_guess,new_guess=guess,cost=cost,old_path=old_path,new_path=path))
        assert wrapped_value==new_value
        relaxed=matrix[:-1];relaxed_b=b&((1<<len(relaxed))-1);larger=source(relaxed,relaxed_b,n)
        expanded=[F(1,2*len(larger))+probabilities[x]/2 if x in larger else F(0) for x in range(1<<n)]
        assert sum(expanded)==1 and all(expanded[x]>=F(1,2*len(larger)) for x in larger)
        cases.append(dict(index=k,n=n,matrix=matrix,old_rhs=b,new_rhs=new_b,delta=delta,old_probabilities=probabilities,new_probabilities=new_probabilities,
            rows=rows,costs=costs,old_value=old_value,new_value=new_value,wrapped_value=wrapped_value,old_policy=policy,new_policy=new_policy,
            old_root=root,new_root=new_root,world_pairs=pairs,relaxed_matrix=relaxed,relaxed_rhs=relaxed_b,expanded_report=expanded))
        state_count+=len(policy)+len(new_policy)
    ambiguity=dict(matrix=[1],old_rhs=0,new_rhs=1,old_point_model=0,transports=[dict(delta=1,new_point=1),dict(delta=3,new_point=3)])
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=seed,sources=sources,cases=cases,
        paired_world_checks=pair_checks,total_policy_states=state_count,transport_ambiguity=ambiguity,elapsed_ns=time.perf_counter_ns()-start,
        scope='Explicit finite correlated laws and pushforwards; adaptive pure priced linear queries, full-assignment guess utility. Pointwise policy equality and optimum equality checked. No inference that a real program change has this law/cost correspondence; no economic speedup claim.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',cases=len(cases),paired_world_checks=pair_checks,total_policy_states=state_count,expanded_reports=len(cases),transport_ambiguity=ambiguity,elapsed_ns=result['elapsed_ns']))))

if __name__=='__main__':main(Path(sys.argv[1]))
