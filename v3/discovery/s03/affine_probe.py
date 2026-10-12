"""Fresh finite affine sources, source revisions and complete kernel retention cost."""
import copy,hashlib,json,random,sys,time
from fractions import Fraction as F
from pathlib import Path
from affine_source import eliminate,compile_source,parity
from flow_v2 import check
from price_flow import exact

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items() if not callable(v)}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x

def rhs(matrix,x):return sum(parity(row&x)<<i for i,row in enumerate(matrix))

def main(out):
    assert not out.exists();base=Path(__file__).parent;seed=89203;rng=random.Random(seed);start=time.perf_counter_ns()
    sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['flow_v2.py','price_flow.py','affine_source.py','affine_probe.py']}
    cases=[];world_checks=0;rhs_checks=0
    for k in range(32):
        n=rng.randrange(2,8);m=rng.randrange(1,7);matrix=[rng.randrange(1<<n) for _ in range(m)]
        targets=[rng.randrange(1<<n) for _ in range(rng.randrange(2,9))]
        cert=eliminate(matrix,n);compiled=compile_source(matrix,n,targets,set(range(n)),cert)
        statuses=[]
        for b in range(1<<m):
            phase=compiled['revise'](b);worlds=[x for x in range(1<<n) if rhs(matrix,x)==b];rhs_checks+=1
            assert (phase is None)==(not worlds)
            if phase is not None:
                assert len(worlds)==1<<len(compiled['free'])
                seen=set()
                for x in worlds:
                    z=sum(((x>>j)&1)<<i for i,j in enumerate(compiled['free']));seen.add(z)
                    for j in range(n):
                        assert ((x>>j)&1)==(parity(compiled['fact_support'][j]&z)^parity(compiled['fact_rhs'][j]&b))
                    for e,target in enumerate(targets):
                        assert parity(target&x)==(parity(compiled['target_support'][e]&z)^phase[e])
                    world_checks+=1
                assert len(seen)==len(worlds)
            statuses.append(dict(rhs=b,consistent=phase is not None,phases=phase))
        rejected=[]
        malformed=copy.deepcopy(cert);malformed['steps'].append(('xor',0,0))
        for name,available,c in [('noninvertible',set(range(n)),malformed)]+([('missing_query',set(),cert)] if compiled['free'] else []):
            try:compile_source(matrix,n,targets,available,c)
            except AssertionError:rejected.append(name)
            else:raise AssertionError('invalid source accepted')
        cases.append(dict(index=k,n=n,matrix=matrix,targets=targets,certificate=cert,compiled=compiled,revisions=statuses,rejected=rejected))
    n=128;r=64;begin=time.perf_counter_ns()
    matrix=[]
    for j in range(r):matrix.append((1<<j)|sum(1<<i for i in rng.sample(range(r,n),rng.randrange(2,7))))
    matrix += [matrix[i]^matrix[j] for i,j in [rng.sample(range(r),2) for _ in range(16)]]
    permutation=list(range(len(matrix)));rng.shuffle(permutation);matrix=[matrix[i] for i in permutation]
    redundant_index=permutation.index(r)
    targets=[sum(1<<i for i in rng.sample(range(n),rng.randrange(1,4))) for _ in range(256)]
    weights=[F(1,256)]*len(targets);construction_ns=time.perf_counter_ns()-begin
    begin=time.perf_counter_ns();cert=eliminate(matrix,n);compiled=compile_source(matrix,n,targets,set(range(n)),cert);compile_check_ns=time.perf_counter_ns()-begin
    prices=[F(rng.randrange(1,17),1024) for _ in compiled['free']]
    nonconstant=[(mask,w/2) for mask,w in zip(compiled['target_support'],weights) if mask]
    baseline=sum((w if not mask else w/2 for mask,w in zip(compiled['target_support'],weights)),F(0))
    begin=time.perf_counter_ns();allocation,witness=exact(nonconstant,prices);bound=check(nonconstant,prices,allocation);solve_check_ns=time.perf_counter_ns()-begin
    updates=[]
    for k in range(48):
        x=rng.getrandbits(n);b=rhs(matrix,x)
        begin=time.perf_counter_ns();phase=compiled['revise'](b);retained_ns=time.perf_counter_ns()-begin
        assert phase is not None
        begin=time.perf_counter_ns();cold=compile_source(matrix,n,targets,set(range(n)),eliminate(matrix,n))
        cold_terms=[(mask,w/2) for mask,w in zip(cold['target_support'],weights) if mask]
        a,w=exact(cold_terms,prices);cold_bound=check(cold_terms,prices,a);cold_phase=cold['revise'](b);cold_ns=time.perf_counter_ns()-begin
        assert cold_phase==phase and cold_bound['upper']==bound['upper'] and cold['target_support']==compiled['target_support']
        bad=b^(1<<redundant_index);assert compiled['revise'](bad) is None
        updates.append(dict(index=k,rhs=b,phases=phase,retained_ns=retained_ns,cold_ns=cold_ns,inconsistent_rhs=bad,inconsistent_rejected=True))
    initial=construction_ns+compile_check_ns+solve_check_ns
    large=dict(n=n,matrix=matrix,targets=targets,weights=weights,certificate=cert,compiled=compiled,prices=prices,flow=allocation,witness=witness,bound=bound,baseline=baseline,
        construction_ns=construction_ns,compile_check_ns=compile_check_ns,solve_check_ns=solve_check_ns,updates=updates,
        initial_plus_updates_ns=initial+sum(q['retained_ns'] for q in updates),cold_updates_ns=sum(q['cold_ns'] for q in updates),
        source_generation_plus_cold_ns=construction_ns+sum(q['cold_ns'] for q in updates),optimal_net_utility=baseline+bound['upper'])
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=seed,sources=sources,cases=cases,world_checks=world_checks,rhs_checks=rhs_checks,large=large,
        elapsed_ns=time.perf_counter_ns()-start,limits='Uniform affine source and physical access to chosen free facts supplied. Replayed operations check algebraic equivalence, not external model adequacy. Identical prepared ordinary linear-algebra/closure service allowed; comparison is cold repetition. Revision changes assumptions, not an inferred causal intervention.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',cases=len(cases),world_checks=world_checks,rhs_checks=rhs_checks,
        large={k:large[k] for k in ['construction_ns','compile_check_ns','solve_check_ns','initial_plus_updates_ns','source_generation_plus_cold_ns','optimal_net_utility']},updates=len(updates),free_coordinates=len(compiled['free']),elapsed_ns=result['elapsed_ns']))))

if __name__=='__main__':main(Path(sys.argv[1]))
