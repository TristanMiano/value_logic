#!/usr/bin/env python3
"""DEVELOPMENT fixed identity-map library coverage and task complementarity."""
from __future__ import annotations
from datetime import datetime,timezone
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse,hashlib,importlib.util,json,platform,sys,time,traceback
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_p305_retention_P',HERE/'05_portfolio_transport.py')
P=importlib.util.module_from_spec(sp);sys.modules[sp.name]=P;sp.loader.exec_module(P)
M,K=P.M,P.K
COUNT=0

def ok(v,msg):
    global COUNT
    COUNT+=1
    if not v:raise AssertionError(msg)

def frame(unit,hard=(),scope='base'):
    return M.Frame(K.Request(1,tuple(hard),(),(('D',K.lit(-1)),),scope),'D',unit)

def run():
    a=frame('U',(K.neg(K.bit(0)),),'A');b=frame('U',(K.bit(0),),'B');d=frame('V',scope='D')
    old=(a,b,d);cache=P.PortfolioCache()
    for name,f in zip(('A','B','D'),old):cache.admit_band(name,M.build_band(f,0,-1),f.record())
    reqs=(frame('U',scope='main'),frame('V',scope='minor'))
    incidence=({(0,0)},{(0,1)},{(1,0),(1,1)})
    rows=[]
    for mask in range(8):
        selected=[i for i in range(3) if mask>>i&1];union=set().union(*(incidence[i] for i in selected))
        flags=[];reports=[]
        for j,f in enumerate(reqs):
            choices=tuple(P.Choice(('A','B','D')[i],old[i].record(),(K.bit(0),)) for i in selected if old[i].unit==f.unit)
            try:
                proof=cache.build(f,choices,(0,),-1,allow_direct=False);report=cache.verify(proof,f,f.record())
                got=True;reports.append({'report':report,'proof':proof.record()})
            except P.Uncertified as e:got=False;reports.append({'status':'NOT_CERTIFIED_BY_THIS_FIXED_LIBRARY','reason':str(e)})
            expected={(j,0),(j,1)}<=union
            ok(got==expected,'Fixed-library receiver and coverage reduction disagree.')
            flags.append(got)
        rows.append({'mask':mask,'certificate_names':[('A','B','D')[i] for i in selected],'units':['U','U','V'],'coverage_flags':flags,'storage_cost':len(selected),'covered_points':sorted(union),'receipts':reports})
    ok(rows[1]['coverage_flags']==[False,False] and rows[2]['coverage_flags']==[False,False],'Singleton complementarity lost.')
    ok(rows[3]['coverage_flags']==[True,False],'Combined certificates fail main request.')
    greedy=[]
    for eps in (F(1,2),F(1,10),F(1,1000)):
        value=lambda mask:F(rows[mask]['coverage_flags'][0])+eps*int(rows[mask]['coverage_flags'][1])
        mask=0
        for step in range(2):
            candidates=[(value(mask|(1<<i))-value(mask),i) for i in range(3) if not mask>>i&1]
            gain,i=max(candidates)
            if gain<=0:break
            mask|=1<<i
        optimum=max(value(m) for m in range(8) if m.bit_count()<=2)
        ok(mask==4 and value(mask)==eps and optimum==1,'Greedy/optimal complementarity witness differs.')
        greedy.append({'epsilon':str(eps),'greedy_mask':mask,'greedy_value':str(value(mask)),'optimal_value':str(optimum),'ratio':str(value(mask)/optimum)})
    return {'libraries':rows,'greedy':greedy,'meaning':'Fixed stored-certificate service with identity maps and no fresh proof. Not a lower bound against unrestricted ordinary symbolic reasoning or better proof-map selection.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();out=a.out;out.mkdir(parents=True,exist_ok=False)
    names=['05_portfolio_retention_check.py','05_portfolio_transport.py','05_counterfactual_transport.py','04_counterfactual_repair.py'];hs={}
    for n in names:
        b=(HERE/n).read_bytes();(out/n).write_bytes(b);hs[n]=hashlib.sha256(b).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'schema':'p305.retention.development.v1','stage':'DEVELOPMENT','prepared_utc':datetime.now(timezone.utc).isoformat(),'sources_sha256':hs,'version':P.VERSION,'command':sys.argv,'python':sys.version,'platform':platform.platform(),'plan':['all eight three-certificate libraries','unit/type-ineligible pairs excluded explicitly','three epsilon values for the general symbolic greedy counterexample']},indent=2)+'\n')
    start=time.monotonic_ns();error=None;result=None
    try:result=run()
    except Exception:error=traceback.format_exc()
    raw=(json.dumps({'assertions':COUNT,'result':result,'error':error},indent=2,default=str)+'\n').encode();(out/'results.json').write_bytes(raw)
    r={'status':'FAIL' if error else 'PASS','assertions':COUNT,'elapsed_ns':time.monotonic_ns()-start,'sources_sha256':hs,'results_sha256':hashlib.sha256(raw).hexdigest(),'error':error};(out/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
