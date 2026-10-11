"""Small exact development: allocation, censoring and controller cost."""
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib
from itertools import product as cartesian
import json
from pathlib import Path
import random
import time
from positive_bets import Group,profile,product


def optimization_checks():
    rng=random.Random(91711);rows=[];vectors=0
    for case in range(200):
        groups=[]
        for _ in range(rng.randint(1,4)):
            N=rng.randint(2,9)
            etas=(F(1),) if case%2 else (F(0),F(1,4),F(1),F(4))
            g=Group(N,etas)
            for _ in range(rng.randrange(N+1)):
                g.observe(rng.randrange(2))
            vals=[g.wealth(m) for m in range(g.positives,g.N+1)]
            assert all(a>=b for a,b in zip(vals,vals[1:]))
            assert all(b*b<=a*c for a,b,c in zip(vals,vals[1:],vals[2:]))
            groups.append(g)
        total=rng.randrange(sum(g.N for g in groups)+1)
        feasible=[]
        for ms in cartesian(*(range(g.positives,g.N+1) for g in groups)):
            if sum(ms)<=total:
                vectors+=1;feasible.append((product(g.wealth(m) for g,m in zip(groups,ms)),ms))
        actual=profile(groups,total)
        assert (None if actual is None else actual[0])==(min(feasible)[0] if feasible else None)
        rows.append({'case':case,'sizes':[g.N for g in groups],'prefixes':[len(g.trace) for g in groups],
                     'proofs':[g.positives for g in groups],'total':total,
                     'minimum':None if actual is None else str(actual[0])})
    return rows,vectors


def sequential_checks():
    # Exact dynamic probability recursion over fixed populations. Outcomes
    # are uniform sampling without replacement; one truth-dependent censor
    # returns no proof for every other sampled positive according to its group
    # draw position. Group choice uses only previous production indicators.
    rows=[]
    for truth in cartesian(range(4),repeat=2):
        for alpha in (F(1,5),F(1,2)):
            for censor in (False,True):
                Ns=(3,3);cross=F();nodes=0
                def visit(js,es,ks,traces,prob,hit):
                    nonlocal cross,nodes
                    nodes+=1
                    gs=[]
                    for g in range(2):
                        item=Group(3,(F(0),F(1),F(4)))
                        for z in traces[g]:item.observe(z)
                        gs.append(item)
                    ew=product(g.wealth(m) for g,m in zip(gs,truth))
                    hit=hit or ew>=1/alpha
                    if hit:
                        cross+=prob;return
                    if sum(js)==6:return
                    available=[g for g in range(2) if js[g]<3]
                    # Favor the currently better proof yield; ties alternate.
                    chosen=max(available,key=lambda g:(F(ks[g]+1,js[g]+2),int(g==sum(js)%2)))
                    remaining=3-js[chosen];ones=truth[chosen]-es[chosen]
                    for y,count in ((1,ones),(0,remaining-ones)):
                        if count==0:continue
                        z=y*int(not censor or js[chosen]%2==0)
                        j2=list(js);e2=list(es);k2=list(ks);t2=[list(t) for t in traces]
                        j2[chosen]+=1;e2[chosen]+=y;k2[chosen]+=z;t2[chosen].append(z)
                        visit(tuple(j2),tuple(e2),tuple(k2),t2,prob*F(count,remaining),hit)
                visit((0,0),(0,0),(0,0),[[],[]],F(1),False)
                assert cross<=alpha,(truth,alpha,censor,cross)
                rows.append({'truth':truth,'alpha':str(alpha),'censor':censor,'crossing_probability':str(cross),'recursion_nodes':nodes})
    return rows


def timings():
    rng=random.Random(91712);rows=[]
    for sizes,prefixes in (((64,64),(12,12)),((256,256),(48,48)),((256,)*4,(32,)*4)):
        for etas in ((F(1),),(F(0),F(1,4),F(1),F(4))):
            groups=[]
            for N,s in zip(sizes,prefixes):
                g=Group(N,etas)
                for _ in range(s):g.observe(int(rng.random()<.85))
                groups.append(g)
            before=time.perf_counter_ns();got=profile(groups,sum(sizes)//2-1);elapsed=time.perf_counter_ns()-before
            rows.append({'sizes':sizes,'prefixes':prefixes,'etas':list(map(str,etas)),
                         'positive_counts':[g.positives for g in groups],
                         'profile_ns':elapsed,'wealth_evaluations':sum(g.evaluations for g in groups),
                         'allocation':None if got is None else got[1],
                         'warrant_alpha_05':got is None or got[0]>=20,
                         'minimum_log10_approx':None if got is None else __import__('math').log10(got[0].numerator)-__import__('math').log10(got[0].denominator)})
    return rows


if __name__=='__main__':
    out=Path(__file__).with_name('bets01.json');assert not out.exists()
    result={'status':'running','contributor':'Codex (GPT-6)','evidence':'DEVELOPMENT','start_utc':datetime.now(timezone.utc).isoformat(),
            'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(__file__).with_name('positive_bets.py'))}}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    try:
        result['optimization_cases'],result['enumerated_null_vectors']=optimization_checks()
        result['sequential_cases']=sequential_checks();result['timings']=timings();result['status']='complete'
    except Exception:
        result['status']='failed';result['failure']=__import__('traceback').format_exc();raise
    finally:
        result['end_utc']=datetime.now(timezone.utc).isoformat()
        out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ('optimization_cases','sequential_cases')}))
