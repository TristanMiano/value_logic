"""Supplied workload comparison, preserving failures and nonzero residuals."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from acquire_flow import solve
from flow_advice import greedy,exact,check


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def main(out):
    assert not out.exists();rng=random.Random(35419);rows=[];start=time.perf_counter_ns()
    for case in range(80):
        m=rng.randrange(2,18);n=rng.randrange(2,35);terms=[]
        for _ in range(n):terms.append((sum(1<<i for i in rng.sample(range(m),rng.randrange(1,min(m,5)+1))),F(rng.randrange(1,12),8)))
        prices=[F(rng.randrange(1,16),8) for _ in range(m)]
        g=greedy(terms,prices);gb=check(terms,prices,g);a,w=exact(terms,prices);eb=check(terms,prices,a)
        ordinary=solve(terms,prices)['objective'];assert ordinary==eb['upper']<=gb['upper']
        rows.append(dict(case=case,terms=terms,prices=prices,greedy_bound=gb,exact_bound=eb,greedy_allocation=g,exact_allocation=a,exact_witness=w))
    workloads=[]
    for family in ['ample','balanced','shared_core']:
        m=128;n=384;terms=[]
        for _ in range(n):
            universe=range(16) if family=='shared_core' else range(m)
            terms.append((sum(1<<i for i in rng.sample(list(universe),rng.randrange(2,7))),F(rng.randrange(1,9),8)))
        scale=12 if family=='ample' else 3
        prices=[F(scale*rng.randrange(1,9),8) for _ in range(m)]
        begin=time.perf_counter_ns();g=greedy(terms,prices);proposal=time.perf_counter_ns()-begin
        begin=time.perf_counter_ns();gb=check(terms,prices,g);checking=time.perf_counter_ns()-begin
        begin=time.perf_counter_ns();a,w=exact(terms,prices);exact_proposal=time.perf_counter_ns()-begin
        begin=time.perf_counter_ns();eb=check(terms,prices,a);exact_check=time.perf_counter_ns()-begin
        assert eb['upper']<=gb['upper']
        workloads.append(dict(family=family,m=m,terms=terms,prices=prices,greedy_allocation=g,greedy=gb,exact_allocation=a,exact=eb,exact_witness=w,
            greedy_proposal_ns=proposal,greedy_check_ns=checking,exact_proposal_ns=exact_proposal,exact_check_ns=exact_check,
            two_stage_no_gain_ns=proposal+checking+(exact_proposal+exact_check if gb['upper'] else 0)))
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=35419,
        sources={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ['acquire_flow.py','flow_advice.py','flow_probe.py']},
        small_cases=rows,workloads=workloads,elapsed_ns=time.perf_counter_ns()-start,
        limits='Supplied graphs/prices; conventional greedy allocation and integer Dinic control, source construction included locally. Not external decision performance or final confirmation.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',small_cases=len(rows),small_greedy_gaps=sum(r['greedy_bound']['upper']>r['exact_bound']['upper'] for r in rows),
        workloads=[{k:r[k] for k in ['family','greedy','exact','greedy_proposal_ns','greedy_check_ns','exact_proposal_ns','exact_check_ns','two_stage_no_gain_ns']} for r in workloads],elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
