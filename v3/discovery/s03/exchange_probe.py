"""Paired allocation-profile probe with costs and counterexample stopping."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import time
from datetime import datetime,timezone
from positive_bets import Group,profile,product
from bets_exchange import exchange


def clone(groups):
    result=[]
    for old in groups:
        g=Group(old.N,old.etas)
        for _,_,z in old.trace:g.observe(z)
        result.append(g)
    return result


def check():
    rng=random.Random(91990);rows=[]
    for case in range(240):
        groups=[]
        for _ in range(rng.randint(1,6)):
            N=rng.randint(1,20);g=Group(N,(F(0),F(1,4),F(1),F(4)) if case%2 else (F(1),))
            for _ in range(rng.randrange(N+1)):g.observe(rng.randrange(2))
            groups.append(g)
        total=rng.randrange(sum(g.N for g in groups)+1)
        expected=profile(clone(groups),total)
        outcomes=[]
        for kind in ('proportional','trace'):
            got=exchange(clone(groups),total,kind=kind)
            assert got['value']==(None if expected is None else expected[0])
            if expected is not None:
                distance=sum(abs(a-b) for a,b in zip(got['initial'],expected[1]))//2
                assert got['exchanges']<=distance,(case,kind,got,expected)
            early=exchange(clone(groups),total,kind=kind,stop_below=20)
            if early['status']=='counterexample':
                assert expected is not None and expected[0]<=early['value']<20
            else:
                assert early['value']==got['value']
            outcomes.append({'proposal':kind,'exchanges':got['exchanges'],'early_status':early['status'],'early_exchanges':early['exchanges']})
        rows.append({'case':case,'sizes':[g.N for g in groups],'total':total,'outcomes':outcomes})
    return rows


def timings():
    rng=random.Random(91991);rows=[]
    fixtures=[((256,256),(48,48),(.85,.85)),((256,)*4,(32,)*4,(.8,.8,.8,.8)),
              ((1024,)*4,(16,32,48,64),(.9,.7,.4,.85)),((1024,)*8,(12,)*8,(.7,)*8)]
    for case,(Ns,ss,ps) in enumerate(fixtures):
        groups=[]
        for N,s,p in zip(Ns,ss,ps):
            g=Group(N,(F(0),F(1,4),F(1),F(4)))
            for _ in range(s):g.observe(int(rng.random()<p))
            groups.append(g)
        total=sum(Ns)//2-1;units=[];expected=None
        for kind in ('greedy','proportional','trace','trace_early'):
            gs=clone(groups);start=time.perf_counter_ns()
            if kind=='greedy':
                v=profile(gs,total);got={'status':'optimal','value':v[0],'allocation':v[1],'exchanges':None,'neighbor_scans':None,'initial':None}
            else:
                got=exchange(gs,total,kind='trace' if kind=='trace_early' else kind,stop_below=20 if kind=='trace_early' else None)
            elapsed=time.perf_counter_ns()-start
            if expected is None:expected=got['value']
            if got['status']=='optimal':assert got['value']==expected
            else:assert expected<=got['value']<20
            units.append({'method':kind,'status':got['status'],'profile_ns':elapsed,'wealth_evaluations':sum(g.evaluations for g in gs),
                          'allocation':got['allocation'],'exchanges':got['exchanges'],'neighbor_scans':got['neighbor_scans'],
                          'value_at_least_20':got['value']>=20})
        rows.append({'case':case,'sizes':Ns,'prefixes':ss,'positive_counts':[g.positives for g in groups],'units':units})
    return rows


if __name__=='__main__':
    out=Path(__file__).with_name('exchange01.json');assert not out.exists()
    result={'status':'running','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','start_utc':datetime.now(timezone.utc).isoformat(),
            'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(__file__).with_name('positive_bets.py'),Path(__file__).with_name('bets_exchange.py'))}}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    try:
        result['finite_cases']=check();result['timings']=timings();result['status']='complete'
    except Exception:
        result['status']='failed';result['failure']=__import__('traceback').format_exc();raise
    finally:
        result['end_utc']=datetime.now(timezone.utc).isoformat();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='finite_cases'}))
