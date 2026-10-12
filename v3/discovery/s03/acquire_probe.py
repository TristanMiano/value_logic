"""Exposed closure probe; no independent confirmation or actual evaluator economy."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from acquire_flow import solve,objective,greedy,check


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def lower(terms,a0,A,world):
    return a0+sum(a*(1 if (mask&world).bit_count()%2==0 else -1) if mask&A==mask else -abs(a) for mask,a in terms)


def main(out):
    assert not out.exists();rng=random.Random(61381);start=time.perf_counter_ns();rows=[]
    for case in range(100):
        m=rng.randrange(1,9);terms=[(rng.randrange(1,1<<m),F(rng.randrange(1,17),8)) for _ in range(rng.randrange(1,14))]
        prices=[F(rng.randrange(0,17),8) for _ in range(m)]
        a=time.perf_counter_ns();w=solve(terms,prices);elapsed=time.perf_counter_ns()-a
        oracle=max(objective(b,terms,prices) for b in range(1<<m));g=greedy(terms,prices)
        assert w['objective']==oracle
        # The independently evaluated feasibility checks reject a perturbed flow.
        bad=dict(w,flow=w['flow']+1)
        try:check(terms,prices,bad)
        except AssertionError:pass
        else:raise AssertionError('corrupted flow value accepted')
        rows.append(dict(case=case,m=m,terms=terms,prices=prices,witness=w,exhaustive_optimum=oracle,greedy=g,solve_and_check_ns=elapsed))
    receipts=[];world_checks=batch_checks=0
    for case in range(16):
        m=rng.randrange(2,6);n=rng.randrange(1,7)
        terms=[(rng.randrange(1,1<<m),F(rng.choice([-1,1]),2*n)) for _ in range(n)]
        A=rng.randrange(1<<m);observed=rng.randrange(1<<m)&A;pending=[(mask&~A,abs(a)) for mask,a in terms if mask&A!=mask]
        prices=[F(rng.randrange(1,5),32) if not A&(1<<i) else F(0) for i in range(m)]
        worlds=[x for x in range(1<<m) if x&A==observed]
        for x in worlds:
            for i in range(m):
                assert lower(terms,F(1,2),A,x)<=lower(terms,F(1,2),A|(1<<i),x)<=lower(terms,F(1,2),(1<<m)-1,x)
                world_checks+=1
        for B in range(1<<m):
            gain=sum(lower(terms,F(1,2),A|B,x)-lower(terms,F(1,2),A,x) for x in worlds)/len(worlds)
            forecast=sum(r for mask,r in pending if mask&B==mask)
            assert gain==forecast;batch_checks+=1
        w=solve(pending,prices)
        receipts.append(dict(m=m,terms=terms,A=A,observed=observed,worlds=len(worlds),pending=pending,prices=prices,witness=w))
    examples=[]
    for name,terms,prices in [('parity',[(15,F(1,2))],[F(1,16)]*4),('shared',[(3,F(5,8)),(6,F(5,8))],[F(3,8)]*3)]:
        examples.append(dict(name=name,terms=terms,prices=prices,optimal=solve(terms,prices),greedy=greedy(terms,prices)))
    m=80;terms=[]
    for _ in range(240):
        mask=sum(1<<i for i in rng.sample(range(m),rng.randrange(2,8)))
        terms.append((mask,F(rng.randrange(1,17),8)))
    prices=[F(rng.randrange(1,49),8) for _ in range(m)]
    a=time.perf_counter_ns();w=solve(terms,prices);scaling_ns=time.perf_counter_ns()-a
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=61381,
        sources={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ['acquire_flow.py','acquire_probe.py']},
        small_closure_cases=rows,receipt_cases=receipts,world_refinement_checks=world_checks,batch_expectation_checks=batch_checks,examples=examples,
        scaling=dict(m=m,terms=terms,prices=prices,witness=w,solve_and_check_ns=scaling_ns),elapsed_ns=time.perf_counter_ns()-start,
        limits='Prices and primitive outputs are supplied. Conventional exact max-closure is the same algorithm. No external evaluator cost, calibrated forecast or realized decision-utility advantage measured.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',small_cases=len(rows),world_checks=world_checks,batch_checks=batch_checks,
        examples=[dict(name=x['name'],optimal=x['optimal']['objective'],greedy=x['greedy'][1]) for x in examples],scaling_ns=scaling_ns,elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
