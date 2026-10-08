#!/usr/bin/env python3
"""DEVELOPMENT actual quoted-source transport, including impossible reference."""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime,timezone
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,hashlib,importlib.util,json,platform,sys,time,traceback
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_p305_counterpossible_test',HERE/'05_counterpossible_bridge.py')
B=importlib.util.module_from_spec(sp);sys.modules[sp.name]=B;sp.loader.exec_module(B)
P,M,K=B.P,B.M,B.K
COUNT=0;CASES=[];OUT=None

def ok(v,msg):
    global COUNT
    COUNT+=1
    if not v:raise AssertionError(msg)

def reject(fn):
    global COUNT
    COUNT+=1
    try:fn()
    except ValueError as e:return {'type':type(e).__name__,'reason':str(e)}
    raise AssertionError('Invalid source-bound input accepted.')

def save(v):
    CASES.append(v)
    with (OUT/'completed_units.jsonl').open('a') as f:f.write(json.dumps({'assertions':COUNT,'case':v},default=str)+'\n');f.flush()

def pair(formula,atoms,x):
    # Direct reference evaluation, independent of the inherited compiler.
    tag=formula[0]
    if tag=='atom':
        i=atoms.index(formula[1]);return x[2*i],x[2*i+1]
    if tag=='top':return 1,0
    if tag=='bottom':return 0,1
    if tag=='not':
        a,b=pair(formula[1],atoms,x);return b,a
    a,b=pair(formula[1],atoms,x),pair(formula[2],atoms,x)
    if tag=='and':return int(a[0] and b[0]),int(a[1] or b[1])
    if tag=='or':return int(a[0] or b[0]),int(a[1] and b[1])
    raise ValueError('Reference syntax.')

def ordinary(f,atoms,x):return pair(f,atoms,tuple(y for bit in x for y in (bit,1-bit)))[0]

def sources(q):
    feasible=[]
    for x in product((0,1),repeat=2*len(q.atoms)):
        if not pair(q.antecedent,q.atoms,x)[0] or any(not pair(b,q.atoms,x)[0] for b in q.background):continue
        if any(x[2*i]+x[2*i+1]!=1 for i,a in enumerate(q.atoms) if a not in q.exceptions):continue
        if any((x[2*i],x[2*i+1])!=(q.baseline[i],1-q.baseline[i]) for i,a in enumerate(q.atoms) if a in q.frame):continue
        rank=sum(int(x[2*i]+x[2*i+1]!=1) for i,a in enumerate(q.atoms) if a in q.exceptions)
        feasible.append((x,rank))
    if not feasible:return [],[]
    rank=min(r for x,r in feasible);return feasible,[x for x,r in feasible if r==rank]

def fixtures():
    p,q=('atom','p'),('atom','q');theta=('and',p,('not',p));d=K.add(K.scale(4,K.bit(2)),K.lit(-1))
    old=B.Query(('p','q'),theta,(0,0),('p',),('q',),(),d)
    ordinary_values=[ordinary(theta,old.atoms,x) for x in product((0,1),repeat=2)]
    ok(ordinary_values==[0]*4,'Original quoted antecedent is not genuinely impossible.')
    f=old.compile();feasible,winners=sources(old);ok(winners==[(1,1,0,1)],'Old framed support source differs.')
    band=M.build_band(f,1,-1);cache=P.PortfolioCache();cache.admit_band('old',band,f.record())
    ch=P.Choice('old',f.record(),(K.bit(0),K.bit(1),K.lit(0),K.lit(1)))
    cases=[('unchanged',old,-1),('frame_withdrawal',replace(old,frame=()),3),('hypothetical_q',replace(old,frame=(),background=(q,)),3),('second_local_conflict',replace(old,frame=(),exceptions=('p','q'),background=(q,('not',q))),3)]
    rows=[]
    for label,current,bound in cases:
        nf=current.compile();fs,ws=sources(current);ok(ws,'Nonempty example unexpectedly infeasible.')
        for x in product((0,1),repeat=4):
            actual=all(K.interval(h,x)==(F(1),F(1)) for h in nf.request.hard)
            ok(actual==any(x==s for s,r in fs),'Compiler differs from direct paired semantics.')
        witness=ws[0];proof=cache.build(nf,(ch,),witness,bound,allow_direct=False);r=B.receive(cache,proof,current,current.record(),bound)
        for x in ws:ok(4*x[2]-1<=F(r['bound']),'Selected hypothetical state refutes accepted comparison.')
        ok(all(pair(theta,current.atoms,x)[0] for x in ws),'Quoted contradiction ceased to be supported.')
        if bound==3:ok(any(x[2] for x in ws),'Positive-loss witness missing.')
        rows.append({'label':label,'request':current.record(),'selected':ws,'report':r,'proof':proof.record()})
    new=replace(old,frame=());nf=new.compile();error=reject(lambda:cache.build(nf,(ch,),(1,1,0,1),-1,allow_direct=False))
    classical=replace(old,exceptions=(),frame=());cf=classical.compile();ok(sources(classical)==([],[]),'Strict ordinary completion became feasible.')
    errors=[error]+[reject(lambda x=x:cache.build(cf,(ch,),x,100)) for x in product((0,1),repeat=4)]
    save({'suite':'genuine_reference_and_declared_source_changes','ordinary_theta':ordinary_values,'cases':rows,'infeasibility_and_stale_bound_rejections':errors})
    return old,band,cache,ch

def renaming(old,band,cache,ch):
    renamed=replace(old,atoms=('q','p'),difference=K.add(K.scale(4,K.bit(0)),K.lit(-1)))
    rf=renamed.compile();mapping=(K.bit(2),K.bit(3),K.bit(0),K.bit(1))
    choice=P.Choice('old',old.record(),mapping);proof=cache.build(rf,(choice,),(0,1,1,1),-1,allow_direct=False)
    report=B.receive(cache,proof,renamed,renamed.record(),-1)
    _,ws=sources(renamed);ok(ws==[(0,1,1,1)],'Renamed support positions incorrect.')
    duplicated=replace(old,background=(old.antecedent,old.antecedent));df=duplicated.compile()
    ok(sources(duplicated)==sources(old),'Duplicate hard antecedent changed selection semantics.')
    dup=cache.build(df,(ch,),(1,1,0,1),-1,allow_direct=False);B.receive(cache,dup,duplicated,duplicated.record(),-1)
    errors=[reject(lambda:B.receive(cache,proof,old,old.record(),-1)),
            reject(lambda:B.receive(cache,proof,renamed,'stale-record',-1)),
            reject(lambda:B.receive(cache,proof,renamed,renamed.record(),-2)),
            reject(lambda:B.receive(cache,proof,replace(renamed,antecedent=('atom','q')),replace(renamed,antecedent=('atom','q')).record(),-1)),
            reject(lambda:replace(old,baseline=(False,0)).compile()),
            reject(lambda:replace(old,atoms=['p','q']).compile()),
            reject(lambda:replace(old,unit='').compile())]
    save({'suite':'full_semantic_renaming_duplicate_premises_and_receiving_binding','report':report,'proof':proof.record(),'errors':errors,'limits':'Selection preserved; duplicated validation work is not claimed identical.'})

def all_fragment_labels():
    atoms=('p','q');p,q=('atom','p'),('atom','q')
    formulas=(p,q,('not',p),('not',q),('and',p,('not',p)),('or',p,('not',p)),('not',('not',p)),('and',('or',p,q),('not',p)),('not',('and',p,q)))
    for f in formulas:
        positive,negative=K.paired(f,atoms)
        for x in product((0,1),repeat=4):ok((int(K.interval(positive,x)[0]),int(K.interval(negative,x)[0]))==pair(f,atoms,x),'Paired compiler mismatch.')
    save({'suite':'direct_paired_syntax_reference','formulas':len(formulas),'support_states_per_formula':16})

def main():
    global OUT
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();OUT=a.out;OUT.mkdir(parents=True,exist_ok=False)
    names=['05_counterpossible_bridge.py','05_counterpossible_bridge_check.py','05_portfolio_transport.py','05_counterfactual_transport.py','04_counterfactual_repair.py'];hs={}
    for name in names:
        raw=(HERE/name).read_bytes();(OUT/name).write_bytes(raw);hs[name]=hashlib.sha256(raw).hexdigest()
    manifest={'schema':'p305.paired_bridge.development.v1','stage':'DEVELOPMENT','prepared_utc':datetime.now(timezone.utc).isoformat(),'version':B.VERSION,'sources_sha256':hs,'command':sys.argv,'python':sys.version,'platform':platform.platform(),'plan':['ordinary theta impossibility','four actual hypothetical source revisions','atom/support renaming and source binding','nine quoted formulas at all paired support states'],'semantic_scope':'P3-04 paired-support construction; no uniquely correct philosophical counterpossible selection claim.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');start=time.monotonic_ns();error=None
    try:o,b,c,ch=fixtures();renaming(o,b,c,ch);all_fragment_labels()
    except Exception:error=traceback.format_exc()
    raw=(json.dumps({'assertions':COUNT,'cases':CASES,'error':error},indent=2,default=str)+'\n').encode();(OUT/'results.json').write_bytes(raw)
    r={'status':'FAIL' if error else 'PASS','assertions':COUNT,'suites':len(CASES),'elapsed_ns':time.monotonic_ns()-start,'sources_sha256':hs,'results_sha256':hashlib.sha256(raw).hexdigest(),'error':error};(OUT/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
