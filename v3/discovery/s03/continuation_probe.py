"""Source-bound small finite continuation checks, not confirmation."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from continuation import System,solve,normalize,quotient,aggregate


def random_system(rng,n,a,e):
    return System(tuple(tuple(F(rng.randrange(-8,15),rng.randrange(1,4)) for _ in range(a)) for _ in range(n)),
                  tuple(tuple(F(rng.randrange(0,5),rng.randrange(1,4)) for _ in range(e)) for _ in range(n)),
                  tuple(tuple(rng.randrange(3) for _ in range(e)) for _ in range(n)),
                  tuple(tuple(rng.randrange(n) for _ in range(e)) for _ in range(n)))


def encode(s):
    return {k:[list(map(str,row)) if k in ('terminal','cost') else list(row) for row in getattr(s,k)] for k in ('terminal','cost','obs','dest')}


def check(s,b,h):
    start=time.perf_counter_ns();reduced,blocks,base,hist=quotient(s);build=time.perf_counter_ns()-start
    start=time.perf_counter_ns();full=solve(s,b,h);full_ns=time.perf_counter_ns()-start
    start=time.perf_counter_ns();compressed=solve(reduced,aggregate(b,blocks),h);small_ns=time.perf_counter_ns()-start
    offset=sum(p*v for p,v in zip(b,base))
    assert full[0]==offset+compressed[0]
    assert full[1]==compressed[1]
    normalized,_=normalize(s);middle=solve(normalized,b,h)
    assert full[:2]==(offset+middle[0],middle[1])
    return {'states':len(b),'blocks':len(set(blocks)),'partition_sizes':hist,'horizon':h,
            'value':str(full[0]),'offset':str(offset),'first_choices':list(full[1]),
            'build_ns':build,'original_ns':full_ns,'quotient_request_ns':small_ns,
            'original_beliefs':full[2],'quotient_beliefs':compressed[2]}


def nuisance_family(copies):
    # Hidden sensor type remains fixed. Nuisance offsets never affect transitions.
    # Two opposite terminal preferences; probe identifies type at price 1/4.
    terminal=[];cost=[];obs=[];dest=[]
    for h in range(2):
        for j in range(copies):
            terminal.append(tuple(F(v+j-3) for v in ((0,5) if h==0 else (5,0))))
            cost.append((F(1,4),));obs.append((h,));dest.append((h*copies+j,))
    return System(tuple(terminal),tuple(cost),tuple(obs),tuple(dest))


def cache_system():
    # States: live; cached-empty; cached-zero; cached-one; frozen.
    terminal=tuple(tuple(map(F,row)) for row in ((0,9),(0,9),(0,-1),(10,9),(0,-1)))
    # Diagnostics: call bound 1 and restore binding; call bound 0; full restore probe.
    cost=tuple((F(0),F(0),F(1,5)) for _ in range(5))
    obs=((1,0,1),(1,0,1),(0,0,0),(1,1,1),(0,0,0))
    dest=((0,0,0),(3,2,1),(2,2,2),(3,3,3),(4,4,4))
    return System(terminal,cost,obs,dest)


def main(out):
    assert not out.exists();rng=random.Random(10471);start=time.perf_counter_ns();cases=[]
    for i in range(120):
        n=rng.randrange(2,8);s=random_system(rng,n,rng.randrange(2,4),rng.randrange(1,3))
        counts=[rng.randrange(1,8) for _ in range(n)];b=tuple(F(x,sum(counts)) for x in counts)
        row=check(s,b,rng.randrange(4));row.update(system=encode(s),prior=list(map(str,b)));cases.append(row)
    nuisance=[]
    for copies in (1,8,64,256):
        s=nuisance_family(copies);b=(F(1,2*copies),)*(2*copies);nuisance.append(check(s,b,3))
    cache=cache_system();cache_result=check(cache,(F(1,3),F(1,3),F(0),F(0),F(1,3)),2)
    # The bad merged current-regret classes split at depth one.
    reduced,blocks,base,history=quotient(cache)
    assert cache.terminal[0]==cache.terminal[1] and blocks[0]!=blocks[1]
    # Known cached-zero and frozen may merge: all available behavior agrees.
    assert blocks[2]==blocks[4]
    result={'status':'complete','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)',
            'seed':10471,'python':sys.version,'sources':{p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ('continuation.py','continuation_probe.py')},
            'random_cases':cases,'nuisance':nuisance,'cache':dict(cache_result,system=encode(cache),blocks=list(blocks)),
            'elapsed_ns':time.perf_counter_ns()-start}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'complete','random_cases':len(cases),'nuisance':nuisance,'cache':cache_result,'elapsed_ns':result['elapsed_ns']}))


if __name__=='__main__':main(Path(sys.argv[1]))
