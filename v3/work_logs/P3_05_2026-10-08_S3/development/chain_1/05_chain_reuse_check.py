#!/usr/bin/env python3
"""DEVELOPMENT ordered portfolio admissions and non-sharp scalar chains."""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime,timezone
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,hashlib,importlib.util,json,platform,sys,time,traceback
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_p305_chain_portfolio',HERE/'05_portfolio_transport.py')
P=importlib.util.module_from_spec(sp);sys.modules[sp.name]=P;sp.loader.exec_module(P)
M,K=P.M,P.K
COUNT=0;CASES=[];OUT=None

def ok(v,msg):
    global COUNT
    COUNT+=1
    if not v:raise AssertionError(msg)

def rejection(fn):
    global COUNT
    COUNT+=1
    try:fn()
    except ValueError as e:return {'type':type(e).__name__,'reason':str(e)}
    raise AssertionError('Invalid input accepted.')

def save(v):
    CASES.append(v)
    with (OUT/'completed_units.jsonl').open('a') as f:f.write(json.dumps({'assertions':COUNT,'case':v},default=str)+'\n');f.flush()

def frame(n,d,hard=(),soft=(),scope='v'):
    return M.Frame(K.Request(n,tuple(hard),tuple(soft),(('delta',d),),scope),'delta','U')

def ev(e,x):
    if e[0]=='lit':return F(e[1])
    if e[0]=='bit':return F(x[e[1]])
    if e[0]=='not':return 1-ev(e[1],x)
    if e[0]=='scale':return F(e[1])*ev(e[2],x)
    a,b=ev(e[1],x),ev(e[2],x)
    if e[0]=='add':return a+b
    if e[0]=='min':return min(a,b)
    if e[0]=='max':return max(a,b)
    if e[0]=='eq':return F(a==b)
    if e[0]=='and':return F(a==b==1)
    if e[0]=='or':return F(a==1 or b==1)
    raise ValueError('Reference expression grammar.')

def check_points(f,witness,bound):
    cutoff=sum(s.weight*(1-ev(s.formula,witness)) for s in f.request.soft);n=0
    for x in product((0,1),repeat=f.request.nbits):
        if all(ev(h,x)==1 for h in f.request.hard) and sum(s.weight*(1-ev(s.formula,x)) for s in f.request.soft)<=cutoff:
            ok(ev(f.difference,x)<=bound,'Accepted chain theorem is false on its recorded domain.');n+=1
    ok(n>0,'Current chain lost nonemptiness.');return n

def scalar_slack():
    old=frame(1,K.lit(0),(K.neg(K.bit(0)),),scope='root')
    b=M.build_band(old,0,0);cache=P.PortfolioCache();cache.admit_band('root',b,old.record())
    f1=frame(1,K.bit(0),scope='first');f2=frame(1,K.lit(0),scope='second')
    ch0=P.Choice('root',old.record(),(K.lit(0),));p1=cache.build(f1,(ch0,),(0,),1,allow_direct=False)
    r1=cache.admit_portfolio('first',p1,f1,f1.record());check_points(f1,(0,),1)
    ch1=P.Choice('first',f1.record(),(K.bit(0),))
    failed=rejection(lambda:cache.build(f2,(ch1,),(0,),0,allow_direct=False))
    p2loose=cache.build(f2,(ch1,),(0,),1,allow_direct=False);cache.verify(p2loose,f2,f2.record());check_points(f2,(0,),1)
    proot=cache.build(f2,(ch0,),(0,),0,allow_direct=False);rroot=cache.verify(proot,f2,f2.record());check_points(f2,(0,),0)
    direct=P.PortfolioCache();pd=direct.build(f2,(),(0,),0);rd=direct.verify(pd,f2,f2.record())
    ok(rroot['counts']['reuse_leaves']>0 and rd['counts']['direct_leaves']>0,'Root reuse and direct routes were not distinguished.')
    save({'suite':'scalar_chain_slack_and_cancelling_corrections','first':r1,'tight_latest_route_failure':failed,'root_route':rroot,'fresh_route':rd,'first_proof':p1.record(),'loose_second':p2loose.record(),'tight_second_root':proot.record(),'meaning':'Latest scalar bound loses tightness; retaining the root or fresh reasoning recovers it. No universal reuse advantage.'})

def finite_chains():
    total=0
    for n in (1,2,3):
        d=K.lit(-1);old=frame(n,d,scope='chain-root-'+str(n));band=M.build_band(old,0,-1)
        cache=P.PortfolioCache();cache.admit_band('root',band,old.record());recorded=[];current=old;handle='root';bound=F(-1)
        for j in range(12):
            alpha=F(2) if j%3==0 else F(1,2) if j%3==1 else F(1)
            shift=F((j%5)-2,3)
            d=K.add(K.scale(alpha,d),K.lit(shift));bound=alpha*bound+shift
            i=j%n;value=j%2;hard=(K.bit(i) if value else K.neg(K.bit(i)),)
            witness=tuple(value if k==i else 0 for k in range(n))
            soft=(K.Soft('rank',K.bit((i+1)%n),F(j+1)),)
            f=frame(n,d,hard,soft,scope='chain-'+str(n)+'-'+str(j))
            # Constant-output comparisons have no input dependence, but old
            # domain/rank still needs its explicit feasible constant map.
            old_witness=(0,)*n if j==0 else recorded[-1]['witness']
            mapping=tuple(K.lit(x) for x in old_witness)
            choice=P.Choice(handle,current.record(),mapping,alpha)
            work={};proof=cache.build(f,(choice,),witness,bound,allow_direct=False,work=work)
            name='step-'+str(j);report=cache.admit_portfolio(name,proof,f,f.record(),work)
            reference=check_points(f,witness,bound)
            recorded.append({'handle':name,'frame':f,'proof':proof,'witness':witness,'bound':bound,'report':report,'work':work,'reference_points':reference})
            if OUT:
                with (OUT/'chain_units.jsonl').open('a') as out:out.write(json.dumps({'nbits':n,'unit':{**recorded[-1],'frame':f.record(),'proof':proof.record()}},default=str)+'\n');out.flush()
            current,handle=f,name;total+=1
        fresh=P.PortfolioCache();fresh.admit_band('root',band,old.record())
        for r in recorded:
            report=fresh.admit_portfolio(r['handle'],r['proof'],r['frame'],r['frame'].record())
            ok(report==r['report'],'Ordered complete proof replay differs.')
        errs=[rejection(lambda:cache.admit_portfolio(handle,recorded[-1]['proof'],current,current.record())),
              rejection(lambda:P.PortfolioCache().verify(recorded[-1]['proof'],current,current.record()))]
        changed=frame(n,d,hard,soft,scope='same-numbers-but-new-program-version')
        errs.append(rejection(lambda:cache.verify(recorded[-1]['proof'],changed,changed.record())))
        save({'suite':'repeated_program_loss_and_scope_edits','nbits':n,'steps':len(recorded),'final_report':recorded[-1]['report'],'rejections':errs,'replayed':True})
    return total

def hostile_admission():
    f=frame(1,K.lit(-1),scope='base');b=M.build_band(f,0,-1);c=P.PortfolioCache();c.admit_band('base',b,f.record())
    ch=P.Choice('future',f.record(),(K.bit(0),));p=P.PortfolioProof(f.record(),(ch,),(0,),F(-1),('reuse',0,(),(),()))
    errors=[rejection(lambda:c.admit_portfolio('future',p,f,f.record()))]
    valid=c.build(f,(P.Choice('base',f.record(),(K.bit(0),)),),(0,),-1,allow_direct=False)
    # The failed admission must not poison the requested future handle.
    c.admit_portfolio('future',valid,f,f.record());ok('future' in c._domains,'Failed admission left a poisoned handle.')
    bad=replace(valid,bound=F(-2));errors.append(rejection(lambda:c.admit_portfolio('bad',bad,f,f.record())))
    errors.append(rejection(lambda:c.receive({'status':'CURRENT_BOUND_CERTIFIED'},valid,f,f.record())))
    altered=replace(valid,choices=(P.Choice('base','same-display-name-only',(K.bit(0),)),))
    errors.append(rejection(lambda:c.verify(altered,f,f.record())))
    ok('bad' not in c._domains,'Invalid bound was admitted before verification.')
    save({'suite':'failed_circular_and_metadata_admissions','rejections':errors})

def main():
    global OUT
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();OUT=a.out;OUT.mkdir(parents=True,exist_ok=False)
    names=['05_chain_reuse_check.py','05_portfolio_transport.py','05_counterfactual_transport.py','04_counterfactual_repair.py'];hs={}
    for name in names:
        raw=(HERE/name).read_bytes();(OUT/name).write_bytes(raw);hs[name]=hashlib.sha256(raw).hexdigest()
    manifest={'schema':'p305.chain.development.v1','stage':'DEVELOPMENT','prepared_utc':datetime.now(timezone.utc).isoformat(),'version':P.VERSION,'sources_sha256':hs,'command':sys.argv,'python':sys.version,'platform':platform.platform(),'plan':['strict scalar composition slack versus root/direct routes','36 repeated edits and full ordered replay','failed circular, invalid, and stale admissions'],'reference':'Separate point expression interpreter over every receiving sublevel.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');start=time.monotonic_ns();error=None
    try:scalar_slack();finite_chains();hostile_admission()
    except Exception:error=traceback.format_exc()
    raw=(json.dumps({'assertions':COUNT,'cases':CASES,'error':error},indent=2,default=str)+'\n').encode();(OUT/'results.json').write_bytes(raw)
    r={'status':'FAIL' if error else 'PASS','assertions':COUNT,'suites':len(CASES),'elapsed_ns':time.monotonic_ns()-start,'sources_sha256':hs,'results_sha256':hashlib.sha256(raw).hexdigest(),'error':error};(OUT/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
