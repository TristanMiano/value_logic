"""Fresh graph-query development; exhaustive decisions, then paid tree kernels."""
import hashlib,json,random,sys,time
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from graph_plan import solve,check,predict

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x

def bellman(weights,anchors,edges):
    n=len(weights);queries=[(1<<v,c) for v,c in enumerate(anchors) if c is not None]+[((1<<u)|(1<<v),c) for u,v,c in edges]
    @lru_cache(None)
    def best(worlds):
        stop=sum(w*F(max(sum(x>>v&1 for x in worlds),sum(1-(x>>v&1) for x in worlds)),len(worlds)) for v,w in enumerate(weights))
        value=stop
        for mask,c in queries:
            zero=tuple(x for x in worlds if not ((x&mask).bit_count()&1));one=tuple(x for x in worlds if ((x&mask).bit_count()&1))
            if not zero or not one:continue
            value=max(value,-c+F(len(zero),len(worlds))*best(zero)+F(len(one),len(worlds))*best(one))
        return value
    return best(tuple(range(1<<n))),best.cache_info().currsize

def main(out):
    assert not out.exists();base=Path(__file__).parent;seed=64283;rng=random.Random(seed);start=time.perf_counter_ns()
    sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['graph_plan.py','graph_probe.py']}
    cases=[];subset_checks=0;world_checks=0
    for k in range(32):
        n=rng.randrange(2,6 if k<12 else 7);raw=[rng.randrange(0,17) for _ in range(n)];raw[0]+=1;total=sum(raw)
        weights=[F(w,total) for w in raw];prizes=[w/2 for w in weights]
        anchors=[None if rng.randrange(4)==0 else F(rng.randrange(0,25),64) for _ in range(n)]
        edges=[(rng.randrange(v),v,F(rng.randrange(0,17),128)) for v in range(1,n)]
        plan=solve(prizes,anchors,edges);checked=check(prizes,anchors,edges,plan)
        available=[v for v,c in enumerate(anchors) if c is not None];best=F(0)
        for bits in range(1<<(len(edges)+len(available))):
            p=dict(edges=[j for j in range(len(edges)) if bits>>j&1],anchors=[v for j,v in enumerate(available) if bits>>(j+len(edges))&1])
            best=max(best,check(prizes,anchors,edges,p)['value']);subset_checks+=1
        assert best==plan['value']
        adaptive,states=bellman(weights,anchors,edges) if k<12 else (None,0)
        if k<12:assert adaptive==F(1,2)+best
        for x in range(1<<n):
            edge_labels={j:((x>>edges[j][0])^(x>>edges[j][1]))&1 for j in plan['edges']}
            anchor_labels={v:x>>v&1 for v in plan['anchors']}
            score=F(0)
            for flip in (0,1):
                guess=predict(n,edges,plan,edge_labels,anchor_labels,flip)
                score+=sum(w for v,w in enumerate(weights) if guess[v]==(x>>v&1))/2
            assert score-checked['cost']==F(1,2)+best;world_checks+=1
        cases.append(dict(index=k,weights=weights,anchors=anchors,edges=edges,plan=plan,checked=checked,adaptive_value=adaptive,belief_states=states))
    large=[]
    for shape in ('path','star','random'):
        n=4096;begin=time.perf_counter_ns();raw=[rng.randrange(1,33) for _ in range(n)];total=sum(raw);prizes=[F(w,2*total) for w in raw]
        anchors=[None if rng.randrange(3)==0 else F(rng.randrange(1,49),65536) for _ in range(n)]
        edges=[((v-1 if shape=='path' else 0 if shape=='star' else rng.randrange(v)),v,F(rng.randrange(0,17),65536)) for v in range(1,n)]
        source_ns=time.perf_counter_ns()-begin;begin=time.perf_counter_ns();plan=solve(prizes,anchors,edges);solve_ns=time.perf_counter_ns()-begin
        begin=time.perf_counter_ns();checked=check(prizes,anchors,edges,plan);check_ns=time.perf_counter_ns()-begin
        large.append(dict(shape=shape,prizes=prizes,anchors=anchors,edges=edges,plan=plan,checked=checked,source_ns=source_ns,solve_ns=solve_ns,check_ns=check_ns))
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=seed,sources=sources,cases=cases,
        subset_checks=subset_checks,world_checks=world_checks,large=large,elapsed_ns=time.perf_counter_ns()-start,
        limits='Supplied graph/weights/exact prices. Ordinary identical tree DP is the strong comparison. Timings exclude real observation acquisition and external model validation; finite checks do not establish general theorem or useful empirical transfer.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',cases=len(cases),subset_checks=subset_checks,world_checks=world_checks,bellman_cases=12,belief_states=sum(c['belief_states'] for c in cases),large=[dict(shape=c['shape'],gain=c['plan']['value'],covered=len(c['checked']['covered']),anchors=len(c['plan']['anchors']),edges=len(c['plan']['edges']),source_ns=c['source_ns'],solve_ns=c['solve_ns'],check_ns=c['check_ns']) for c in large],elapsed_ns=result['elapsed_ns']))))

if __name__=='__main__':main(Path(sys.argv[1]))
