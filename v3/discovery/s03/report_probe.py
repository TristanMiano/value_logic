"""Fresh exact report normalization, partial refinement and conditioning checks."""
import hashlib,json,random,sys,time
from fractions import Fraction as F
from pathlib import Path
from affine_source import eliminate,compile_source,parity
from affine_report import prepare
from rank_planner import profile

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items() if not callable(v)}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x

def main(out):
    assert not out.exists();base=Path(__file__).parent;seed=50764;rng=random.Random(seed);start=time.perf_counter_ns()
    sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['affine_source.py','affine_report.py','rank_planner.py','report_probe.py']}
    cases=[];partial_checks=0
    for k in range(32):
        n=rng.randrange(2,8);m=rng.randrange(0,n+1);matrix=[rng.randrange(1<<n) for _ in range(m)];x=rng.randrange(1<<n)
        b=sum(parity(row&x)<<i for i,row in enumerate(matrix));compiled=compile_source(matrix,n,[],set(range(n)),eliminate(matrix,n));h=len(compiled['free'])
        probs=[F(rng.randrange(5),4) for _ in range(h)];eta=F(rng.randrange(4),4);report=prepare(matrix,b,n,probs,eta)
        masses=[report['mass'](x) for x in range(1<<n)];assert sum(masses)==1
        worlds=[x for x,v in enumerate(masses) if v];assert len(worlds)==1<<h
        assert all(masses[x]>=report['point_floor'] for x in worlds)
        intervals=[]
        for known in range(1<<h):
            for bits in range(1<<h):
                if bits&~known:continue
                bounds=report['partial'](known,bits)
                selected=[x for x in worlds if (sum(((x>>j)&1)<<i for i,j in enumerate(report['free']))&known)==bits]
                assert min(masses[x] for x in selected)==bounds['lower'] and max(masses[x] for x in selected)==bounds['upper']
                assert sum(masses[x] for x in selected)==bounds['event_mass'];partial_checks+=1
                intervals.append(dict(known=known,bits=bits,**bounds))
        cases.append(dict(index=k,n=n,matrix=matrix,rhs=b,probabilities=probs,eta=eta,report=report,masses=masses,partial_intervals=intervals))
    report=prepare([],0,2,[F(0),F(0)],F(1,2));event=report['partial'](1,0)
    assert event['conditional_model_weight']==F(2,3)
    future_wrong=report['mass'](2)/event['event_mass'];assert future_wrong==F(1,6)
    # A log-score rank profile with genuinely changing requested ranks.
    d=64;rows=[1<<j for j in range(d)]+[rng.randrange(1<<d) for _ in range(128)]
    costs=[F(rng.randrange(1,129),64) for _ in rows]
    begin=time.perf_counter_ns();points=profile(rows,costs,d);build_ns=time.perf_counter_ns()-begin
    prices=[F(i,8) for i in range(1,129)];begin=time.perf_counter_ns()
    chosen=[max(points,key=lambda p:(p['rank']-lam*p['cost'],-p['cost'])) for lam in prices]
    queries_ns=time.perf_counter_ns()-begin
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=seed,sources=sources,cases=cases,partial_checks=partial_checks,
        conditional_trust_example=dict(prior_model_weight=F(1,2),event_probability=event['event_mass'],posterior_model_weight=event['conditional_model_weight'],conditional_wrong_probability=future_wrong,unconditional_wrong_probability=report['mass'](2)),
        log_score_profile=dict(d=d,rows=rows,costs=costs,prices=prices,selected_ranks=[p['rank'] for p in chosen],distinct_ranks=len(set(p['rank'] for p in chosen)),profile_build_ns=build_ns,query_scan_ns=queries_ns),
        elapsed_ns=time.perf_counter_ns()-start,limits='Exact finite normalization and probability identities; no empirical forecast adequacy or external query-cost claim. Rank choices optimize minimax log score, not the earlier full-assignment objective. Model support and true-source validity are separate obligations.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',cases=len(cases),partial_checks=partial_checks,conditional_trust_example=result['conditional_trust_example'],
        distinct_ranks=result['log_score_profile']['distinct_ranks'],profile_build_ns=build_ns,query_scan_ns=queries_ns,elapsed_ns=result['elapsed_ns']))))

if __name__=='__main__':main(Path(sys.argv[1]))
