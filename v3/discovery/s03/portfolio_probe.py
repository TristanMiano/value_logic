"""Fresh parity portfolios: explicit belief Bellman versus closure and budget LP."""
import hashlib,json,random,sys,time
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from flow_v2 import check
from price_flow import exact
from price_profile import build,line
from portfolio_budget import budget

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x

def bellman(outputs,prices,random_cost=False):
    m=len(prices);worlds=range(1<<m)
    @lru_cache(None)
    def solve(known,bits):
        possible=[x for x in worlds if x&known==bits]
        # Explicit marginal counts, not the closure/completion shortcut.
        stop=F(0)
        for mask,w in outputs:
            ones=sum((x&mask).bit_count()%2 for x in possible)
            stop+=w*F(max(ones,len(possible)-ones),len(possible))
        value=stop
        for i,q in enumerate(prices):
            if known>>i&1:continue
            q0=q/2 if random_cost else q
            q1=q*F(3,2) if random_cost else q
            trial=(-q0+solve(known|1<<i,bits)-q1+solve(known|1<<i,bits|1<<i))/2
            value=max(value,trial)
        return value
    return solve(0,0),solve.cache_info().currsize

def brute_budget(terms,prices,b):
    points=[line(terms,prices,x) for x in range(1<<len(prices))]
    best=max((a for a,c in points if c<=b),default=F(0))
    # Every extreme feasible lottery uses at most two batches.
    low=[(a,c) for a,c in points if c<b];high=[(a,c) for a,c in points if c>b]
    for al,cl in low:
        for ah,ch in high:
            theta=(b-cl)/(ch-cl);best=max(best,(1-theta)*al+theta*ah)
    return best

def main(out):
    assert not out.exists();base=Path(__file__).parent;seed=79861;rng=random.Random(seed);start=time.perf_counter_ns()
    sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['flow_v2.py','price_flow.py','price_profile.py','portfolio_budget.py','portfolio_probe.py']}
    cases=[]
    for k in range(28):
        m=rng.randrange(2,7);n=rng.randrange(2,11)
        raw=[(rng.randrange(1,1<<m),rng.randrange(1,17)) for _ in range(n)]
        total=sum(w for _,w in raw);outputs=[(mask,F(w,total)) for mask,w in raw]
        terms=[(mask,w/2) for mask,w in outputs];prices=[F(rng.randrange(1,17),128) for _ in range(m)]
        allocation,witness=exact(terms,prices);bound=check(terms,prices,allocation)['upper']
        value,states=bellman(outputs,prices);random_value,random_states=bellman(outputs,prices,True)
        assert value==F(1,2)+bound==random_value
        profile=build(terms,prices);budgets=[]
        for scale in (F(0),F(1,5),F(1,2),F(4,5),F(1)):
            b=scale*sum(prices);certificate=budget(terms,prices,profile,b)
            assert certificate['gain']==brute_budget(terms,prices,b)
            budgets.append(certificate)
        cases.append(dict(index=k,outputs=outputs,prices=prices,flow=allocation,cut=witness,adaptive_value=value,states=states,random_own_cost_value=random_value,random_cost_states=random_states,profile=profile,budgets=budgets))
    # A compact larger action portfolio, with actual solver/checker kernel costs.
    m=256;n=768;raw=[]
    begin=time.perf_counter_ns()
    for e in range(n):
        mask=sum(1<<i for i in rng.sample(range(m),rng.randrange(1,7)))
        raw.append((mask,rng.randrange(1,33)))
    total=sum(w for _,w in raw);outputs=[(mask,F(w,total)) for mask,w in raw];terms=[(mask,w/2) for mask,w in outputs]
    prices=[F(rng.randrange(1,17),4096) for _ in range(m)];source_ns=time.perf_counter_ns()-begin
    begin=time.perf_counter_ns();allocation,witness=exact(terms,prices);solve_ns=time.perf_counter_ns()-begin
    begin=time.perf_counter_ns();bound=check(terms,prices,allocation);check_ns=time.perf_counter_ns()-begin
    assert bound['upper']==witness['value']
    large=dict(outputs=outputs,prices=prices,flow=allocation,witness=witness,bound=bound,source_ns=source_ns,solve_ns=solve_ns,check_ns=check_ns,
        utility=F(1,2)+bound['upper'],implicit_action_count_power_of_two=n,implicit_world_count_power_of_two=m,purchased_bits=witness['bits'].bit_count())
    # Explicit expected versus hard-budget separation.
    terms=[(3,F(1,2))];prices=[F(1),F(1)];profile=build(terms,prices);lottery=budget(terms,prices,profile,F(1))
    assert lottery['gain']==F(1,4)
    hard=max(line(terms,prices,x)[0] for x in range(4) if line(terms,prices,x)[1]<=1)
    assert hard==0
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=seed,sources=sources,cases=cases,large=large,
        budget_separation=dict(expected_budget=lottery,hard_budget_gain=hard),elapsed_ns=time.perf_counter_ns()-start,
        scope='Supplied independent fair-bit source, additive independently chosen output actions, pure complete queries. Random-cost check ties each cost to its own bit only. Ordinary closure is the exact comparison; no expensive Bellman computation attempted on the large case.',
        cost_scope='Large kernel includes source generation/normalization, flow and rational certificate check. Does not include authenticating an external independence model, actual bit acquisition, or executing output actions.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',cases=len(cases),bellman_states=sum(c['states'] for c in cases),budget_comparisons=sum(len(c['budgets']) for c in cases),
        large={k:large[k] for k in ['source_ns','solve_ns','check_ns','utility','purchased_bits']},expected_budget_gain=lottery['gain'],hard_budget_gain=hard,elapsed_ns=result['elapsed_ns']))))

if __name__=='__main__':main(Path(sys.argv[1]))
