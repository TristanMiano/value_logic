#!/usr/bin/env python3
"""DEVELOPMENT shared nominal receiver identity and cross-front-end proof use."""
from __future__ import annotations
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import argparse,ast,hashlib,importlib.util,json,platform,sys,time,traceback
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def load(name,path):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
D=load('_shared_D',HERE/'05_dependency_frontend.py');B=load('_shared_B',HERE/'05_counterpossible_bridge.py');P,M,K=D.P,D.M,D.K
COUNT=0

def ok(v,msg):
    global COUNT
    COUNT+=1
    if not v:raise AssertionError(msg)

def definitions(path):
    tree=ast.parse(path.read_text());return {n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--before',required=True,type=Path);a=ap.parse_args();out=a.out;out.mkdir(parents=True,exist_ok=False)
    names=['05_shared_frontend_check.py','05_dependency_frontend.py','05_counterpossible_bridge.py','05_portfolio_transport.py','05_counterfactual_transport.py','04_counterfactual_repair.py'];hs={}
    for n in names:
        b=(HERE/n).read_bytes();(out/n).write_bytes(b);hs[n]=hashlib.sha256(b).hexdigest()
    manifest={'schema':'p305.shared_frontend.development.v1','stage':'DEVELOPMENT','prepared_utc':datetime.now(timezone.utc).isoformat(),'sources_sha256':hs,'versions':{'program':D.VERSION,'hypothetical':B.VERSION,'portfolio':P.VERSION},'command':sys.argv,'before_source':str(a.before),'python':sys.version,'platform':platform.platform(),'plan':['same cache/proof nominal classes','unchanged function/class ASTs versus earlier preserved wrappers','program-derived bound reused in a quoted counterpossible through checked scale/map/correction']};(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    error=None;result={};start=time.monotonic_ns()
    try:
        ok(D.P is B.P and D.P.PortfolioCache is B.P.PortfolioCache,'Front ends still use different nominal types.')
        before={}
        for n in ['05_dependency_frontend.py','05_counterpossible_bridge.py']:
            old=a.before/n;ok(old.exists(),'Preserved prior source missing.');before[n]=hashlib.sha256(old.read_bytes()).hexdigest()
            ok(definitions(old)==definitions(HERE/n),'Alias repair changed a function/class AST.')
        original=D.Program('zero-program',('x',),(),(),(('out',('const',0)),))
        changed=D.Program('identity-program',('x',),(),(),(('out',('input','x')),))
        request=D.Comparison('observed-program-difference',original,changed,(('out',F(1)),),(),())
        frame=D.compile_comparison(request);band=M.build_band(frame,0,1);cache=D.P.PortfolioCache();cache.admit_band('program',band,frame.record())
        p=('atom','p');theta=('and',p,('not',p))
        query=B.Query(('p','q'),theta,(0,0),('p',),(),(),K.add(K.scale(4,K.bit(2)),K.lit(-1)))
        current=query.compile();choice=B.P.Choice('program',frame.record(),(K.bit(2),),F(4))
        proof=cache.build(current,(choice,),(1,1,0,1),3,allow_direct=False)
        report=B.receive(cache,proof,query,query.record(),3)
        ok(report['counts']['reuse_leaves']>0 and report['counts']['direct_leaves']==0,'Cross-front-end reuse was bypassed.')
        ok(report['bound']=='3','Wrong receiving loss correction.')
        result={'unchanged_definitions':True,'before_sources_sha256':before,'source_program_record':request.record(),'band':band.record(),'hypothetical_query':query.record(),'proof':proof.record(),'report':report,'meaning':'Mathematical proof map and scale; not an inferred causal link between the program and an impossible world.'}
    except Exception:error=traceback.format_exc()
    raw=(json.dumps({'assertions':COUNT,'result':result,'error':error},indent=2,default=str)+'\n').encode();(out/'results.json').write_bytes(raw)
    r={'status':'FAIL' if error else 'PASS','assertions':COUNT,'elapsed_ns':time.monotonic_ns()-start,'sources_sha256':hs,'results_sha256':hashlib.sha256(raw).hexdigest(),'error':error};(out/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
