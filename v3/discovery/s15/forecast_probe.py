"""Exact checks of a declared miss-probability process, not a workload."""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import time

HERE=Path(__file__).resolve().parent
Z=F(4,257); DELTA=F(1,1000); A=F(1,2)/Z; B=F(1,2)/(1-Z)

def cap(r, mixture):
    h=0
    while A**h*B**r < (2 if mixture else 1)/DELTA:
        h+=1
    return r+h

def process(r, t0, mixture):
    N=cap(r,mixture)
    ap=[A**i for i in range(N+1)]
    bp=[B**i for i in range(r+1)]
    vp=[Z**(-max(0,t-t0)) for t in range(N+1)]
    live={(0,True):1}
    stopped=defaultdict(F)
    false=F(0)
    for t in range(N+1):
        nxt=defaultdict(int)
        denom=257**t
        for (j,alive), mass in live.items():
            w=ap[t-j]*bp[j]
            wealth=(w+(vp[t] if alive else 0))/2 if mixture else w
            if wealth>=1/DELTA:
                prob=F(mass,denom)
                stopped[t]+=prob
                if j<r:
                    false+=prob
                continue
            if j==r:
                nxt[j,alive]+=257*mass
            else:
                nxt[j,alive]+=4*mass
                nxt[j+1,alive and t+1<=t0]+=253*mass
        live=dict(nxt)
    assert not live
    assert sum(stopped.values())==1 and false<=DELTA
    return dict(rank=r,forecast_start=t0,mixture=mixture,cap=N,
                false_probability=str(false),false_probability_float=float(false),
                mean_probes=str(sum(t*p for t,p in stopped.items())),
                mean_probes_float=float(sum(t*p for t,p in stopped.items())),
                stopping_law={str(t):str(p) for t,p in stopped.items()})

def main():
    start=time.perf_counter_ns()
    ranks=list(range(17))+[32,128]
    baseline=[process(r,4,False) for r in ranks]
    mixed=[process(r,t0,True) for r in ranks for t0 in (0,4,8)]
    assert all(cap(r,True)<=cap(r,False)+1 for r in ranks)
    record=next(d for d in mixed if d['rank']==4 and d['forecast_start']==4)
    upper=7-(1-Z)**4
    lower=7-5*DELTA
    assert cap(4,True)==7
    assert Z**-2>2/DELTA
    assert F(record['mean_probes'])<=upper<lower
    base4=next(d for d in baseline if d['rank']==4)
    assert F(base4['mean_probes'])>=lower
    assert sum(F(p) for t,p in record['stopping_law'].items() if int(t)<=6)>=(1-Z)**4
    # Choosing the best fresh start after seeing the stream is not a test.
    # Under a Bernoulli(1/2) null, a four-success run yields wealth 16.
    survive={0:1}
    for _ in range(64):
        nxt=defaultdict(int)
        for run,mass in survive.items():
            nxt[0]+=mass
            if run<3:
                nxt[run+1]+=mass
        survive=dict(nxt)
    unsafe=1-F(sum(survive.values()),2**64)
    assert unsafe>F(1,10)
    result=dict(status='PASS',attribution='Codex (GPT-6), DEVELOPMENT',
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                elapsed_ns=time.perf_counter_ns()-start,
                forecast_mean_upper=str(upper),forecast_mean_upper_float=float(upper),
                baseline_mean_lower=str(lower),
                guaranteed_relative_probe_reduction=float(1-upper/lower),
                unsafe_best_start_false_probability=str(unsafe),
                unsafe_best_start_false_probability_float=float(unsafe),
                baseline=baseline,mixed=mixed,
                note='Abstract constant miss-probability law; not a claim of realizability by every polynomial rank or a CPU/audit benchmark.')
    (HERE/'forecast_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('baseline','mixed')},indent=2))

if __name__=='__main__':
    main()
