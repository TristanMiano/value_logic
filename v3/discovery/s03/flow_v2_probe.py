"""Explicitly reused flow inputs and a new sparse scaling case; DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from flow_v2 import greedy,exact,check


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def measure(terms,prices):
    begin=time.perf_counter_ns();g=greedy(terms,prices);gb=check(terms,prices,g);greedy_ns=time.perf_counter_ns()-begin
    begin=time.perf_counter_ns();a,w=exact(terms,prices);eb=check(terms,prices,a);exact_ns=time.perf_counter_ns()-begin
    assert eb['upper']<=gb['upper']
    return dict(greedy=gb,exact=eb,greedy_with_check_ns=greedy_ns,exact_with_check_ns=exact_ns,
        two_stage_no_gain_ns=greedy_ns+(exact_ns if gb['upper'] else 0),greedy_allocation=g,exact_allocation=a)


def main(out):
    assert not out.exists();base=Path(__file__).parent;source=base/'flow01.json';old=json.loads(source.read_text());checks=0;start=time.perf_counter_ns()
    for row in old['small_cases']:
        terms=[(m,F(v)) for m,v in row['terms']];prices=list(map(F,row['prices']))
        g=check(terms,prices,greedy(terms,prices));a,w=exact(terms,prices);e=check(terms,prices,a)
        assert g['upper']==F(row['greedy_bound']['upper']) and e['upper']==F(row['exact_bound']['upper']);checks+=1
    workloads=[]
    for row in old['workloads']:
        terms=[(m,F(v)) for m,v in row['terms']];prices=list(map(F,row['prices']))
        workloads.append(dict(family=row['family'],kind='reused exposure',result=measure(terms,prices)))
    rng=random.Random(35420);m=1024;n=3072;terms=[(sum(1<<i for i in rng.sample(range(m),4)),F(rng.randrange(1,9),8)) for _ in range(n)]
    prices=[F(3*rng.randrange(1,9),2) for _ in range(m)]
    workloads.append(dict(family='new_sparse_ample',kind='new development input',m=m,terms=terms,prices=prices,result=measure(terms,prices)))
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,
        amendment='Replace dense mask/pressure scanning by sparse incidence loops in both greedy and exact controls. Prior exposed inputs explicitly replayed.',
        sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['flow_v2.py','flow_v2_probe.py','flow_advice.py']},
        reused_input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),replayed_small_cases=checks,new_seed=35420,workloads=workloads,elapsed_ns=time.perf_counter_ns()-start,
        limits='Single cold calls; supplied graphs, no external evaluator, selection transfer or generic economics claim. The exact conventional control receives the same representation repair.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',replays=checks,workloads=[dict(family=w['family'],**{k:w['result'][k] for k in ['greedy','exact','greedy_with_check_ns','exact_with_check_ns','two_stage_no_gain_ns']}) for w in workloads],elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
