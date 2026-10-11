"""Paired numerical advice/exact-certificate development probe."""
import time
import_started=time.perf_counter_ns()
from bets_float import numerical_profile
import_ns=time.perf_counter_ns()-import_started
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
from datetime import datetime,timezone
import scipy
from positive_bets import Group,profile
from bets_exchange import exchange


def clone(groups):
    result=[]
    for old in groups:
        g=Group(old.N,old.etas)
        for _,_,z in old.trace:g.observe(z)
        result.append(g)
    return result


def check():
    rng=random.Random(92120);rows=[]
    for case in range(90):
        groups=[]
        for _ in range(rng.randint(1,5)):
            N=rng.randint(2,20);g=Group(N,(F(0),F(1,4),F(1),F(4)))
            for _ in range(rng.randrange(N+1)):g.observe(rng.randrange(2))
            groups.append(g)
        total=rng.randrange(sum(g.N for g in groups)+1);expected=profile(clone(groups),total)
        actual=numerical_profile(clone(groups),total)
        assert actual['value']==(None if expected is None else expected[0])
        rows.append({'case':case,'exchanges':actual['exchanges'],'status':actual['numerical']['status']})
    return rows


def timings():
    # Same prospective fixture generator as exchange01, but all arms rerun on
    # each common trace here. Imported dependencies are separately charged.
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
        for kind in ('greedy','proportional','numerical','numerical_early'):
            gs=clone(groups);start=time.perf_counter_ns()
            if kind=='greedy':
                v=profile(gs,total);got={'status':'optimal','value':v[0],'allocation':v[1],'exchanges':None}
            elif kind=='proportional':got=exchange(gs,total,kind=kind)
            else:got=numerical_profile(gs,total,stop_below=20 if kind=='numerical_early' else None)
            elapsed=time.perf_counter_ns()-start
            if expected is None:expected=got['value']
            if got['status']=='optimal':assert got['value']==expected
            else:assert expected<=got['value']<20
            units.append({'method':kind,'status':got['status'],'profile_ns':elapsed,'wealth_evaluations':sum(g.evaluations for g in gs),
                          'allocation':got['allocation'],'exchanges':got['exchanges'],'numerical':got.get('numerical'),
                          'value_at_least_20':got['value']>=20})
        rows.append({'case':case,'sizes':Ns,'prefixes':ss,'proof_trace':[[z for _,_,z in g.trace] for g in groups],'units':units})
    return rows


if __name__=='__main__':
    out=Path(__file__).with_name('float01.json');assert not out.exists()
    result={'status':'running','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','start_utc':datetime.now(timezone.utc).isoformat(),
            'dependency_import_ns':import_ns,'scipy_version':scipy.__version__,
            'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),*[Path(__file__).with_name(x) for x in ('positive_bets.py','bets_exchange.py','bets_float.py')]]}}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    try:
        result['finite_cases']=check();result['timings']=timings();result['status']='complete'
    except Exception:
        result['status']='failed';result['failure']=__import__('traceback').format_exc();raise
    finally:
        result['end_utc']=datetime.now(timezone.utc).isoformat();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='finite_cases'}))
