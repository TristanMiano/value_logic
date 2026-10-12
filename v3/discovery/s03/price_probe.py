"""Fresh developmental profile cases; freeze this source before first exposure."""
import hashlib,json,random,sys,time
from fractions import Fraction as F
from pathlib import Path
from flow_v2 import check
from price_flow import exact
from price_profile import build,prepare

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x

def main(out):
    assert not out.exists();base=Path(__file__).parent;seed=61803;rng=random.Random(seed)
    sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['flow_v2.py','price_flow.py','price_profile.py','price_probe.py']}
    begin=time.perf_counter_ns();cases=[]
    for k in range(32):
        m=rng.randrange(2,7);n=rng.randrange(2,14)
        terms=[(rng.randrange(1,1<<m),F(rng.randrange(0,17),8)) for _ in range(n)]
        prices=[F(rng.randrange(1,17),8) for _ in range(m)]
        profile=build(terms,prices);answer=prepare(terms,prices,profile,'case'+str(k))
        xs=sorted(set([F(i,7) for i in range(65)]+[p['price'] for p in profile['endpoints']]))
        for x in xs:
            value,bits=answer(x,'case'+str(k))
            exhaustive=max(sum((r for mask,r in terms if mask&b==mask),F(0))-x*sum((q for i,q in enumerate(prices) if b>>i&1),F(0)) for b in range(1<<m))
            assert value==exhaustive
        cases.append(dict(index=k,terms=terms,prices=prices,profile=profile,exhaustive_queries=len(xs)))
    workloads=[]
    for kind in ['overlapping','blocks']:
        m=64;n=192
        terms=[]
        for e in range(n):
            block=list(range((e%8)*8,(e%8+1)*8)) if kind=='blocks' else list(range(m))
            mask=sum(1<<i for i in rng.sample(block,rng.randrange(1,5)))
            terms.append((mask,F(rng.randrange(1,33),8)))
        prices=[F(rng.randrange(1,33),8) for _ in range(m)]
        start=time.perf_counter_ns();profile=build(terms,prices);build_ns=time.perf_counter_ns()-start
        start=time.perf_counter_ns();answer=prepare(terms,prices,profile,kind);verify_ns=time.perf_counter_ns()-start
        top=sum((r for _,r in terms),F(0))/sum(prices)*3
        xs=[F(rng.randrange(0,65537),65536)*top for _ in range(128)]
        queries=[]
        for x in xs:
            start=time.perf_counter_ns();value,bits=answer(x,kind);lookup_ns=time.perf_counter_ns()-start
            start=time.perf_counter_ns();allocation,witness=exact(terms,[x*q for q in prices]);upper=check(terms,[x*q for q in prices],allocation)['upper'];cold_ns=time.perf_counter_ns()-start
            assert value==witness['value']==upper
            queries.append(dict(x=x,value=value,bits=bits,lookup_ns=lookup_ns,cold_ns=cold_ns))
        rejected=[]
        for x,ver in [(F(1),'wrong'),(F(-1),kind),(1.0,kind)]:
            try:answer(x,ver)
            except AssertionError:rejected.append([x,ver])
            else:raise AssertionError('invalid request accepted')
        workloads.append(dict(kind=kind,terms=terms,prices=prices,profile=profile,queries=queries,build_ns=build_ns,verify_ns=verify_ns,
            total_service_ns=build_ns+verify_ns+sum(q['lookup_ns'] for q in queries),cold_queries_ns=sum(q['cold_ns'] for q in queries),rejected=rejected))
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=seed,sources=sources,cases=cases,workloads=workloads,
        elapsed_ns=time.perf_counter_ns()-begin,limits='Supplied fixed graph and price ray, one cold run. Identical ordinary parametric-closure service allowed; no external semantic deployment or superior-to-parametric-flow claim.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',small_cases=len(cases),exhaustive_queries=sum(c['exhaustive_queries'] for c in cases),
        workloads=[{k:w[k] for k in ['kind','build_ns','verify_ns','total_service_ns','cold_queries_ns']}|dict(pieces=len(w['profile']['pieces']),oracle_calls=w['profile']['oracle_calls']) for w in workloads],elapsed_ns=result['elapsed_ns']))))

if __name__=='__main__':main(Path(sys.argv[1]))
