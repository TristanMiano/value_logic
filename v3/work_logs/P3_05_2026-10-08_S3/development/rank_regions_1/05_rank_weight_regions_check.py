#!/usr/bin/env python3
"""DEVELOPMENT rank-margin reconstruction and independent certificate rejection.

New S3 evidence; none of this reconstructs a lost historical execution.
"""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime,timezone
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,hashlib,importlib.util,json,platform,sys,time,traceback
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_p305_weight_check',HERE/'05_rank_weight_regions.py')
W=importlib.util.module_from_spec(sp);sys.modules[sp.name]=W;sp.loader.exec_module(W)
M,K=W.M,W.K
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
    raise AssertionError('Invalid certificate/input was accepted.')

def save(v):
    CASES.append(v)
    with (OUT/'completed_units.jsonl').open('a') as f:f.write(json.dumps({'assertions':COUNT,'case':v},default=str)+'\n');f.flush()

def example(a,*,outside2=False):
    feats=((F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(0),F(0),F(1)))
    if outside2:feats+=((F(0),F(0),F(2)),)
    return W.Problem('three-component-example-'+str(a),tuple('case'+str(i) for i in range(len(feats))),feats,(0,1),
        (F(1,4),F(1,4),F(a)),(F(3,4),F(3,4),F(a)),
        (((F(1),F(1),F(0)),F(1)),((F(-1),F(-1),F(0)),F(-1))),(F(1,2),F(1,2),F(a)))

def direct_winners(p,w):
    ranks=[sum(F(x)*F(y) for x,y in zip(v,w)) for v in p.features]
    return tuple(i for i,x in enumerate(ranks) if x==min(ranks))

def examples():
    for a,expected in ((F(3,5),F(1,10)),(F(2,5),F(-1,10)),(F(1,2),F(0))):
        p=example(a);work={};ans=W.search(p,work=work);ok(ans['status']=='VERIFIED','Expected a proved optimum.')
        proof=ans['proof'];r=W.verify(p,proof,p.record());ok(F(r['margin'])==expected,'Incorrect exact margin.');ok(r['coverage']==(a>F(1,2)),'Tie/strictness rule wrong.')
        for i in range(17):
            w=(F(1,4)+F(i,32),F(3,4)-F(i,32),a);ok(p.feasible(w),'Example grid infeasible.')
            if r['coverage']:ok(set(direct_winners(p,w))<=set(p.covered),'Positive coverage fails in grid.')
        if a==F(3,5):
            ok(direct_winners(p,(F(1,4),F(3,4),a))==(0,),'First endpoint must choose first covered state.')
            ok(direct_winners(p,(F(3,4),F(1,4),a))==(1,),'Second endpoint must choose second covered state.')
            ok(not W.search(replace(p,covered=(0,)))['report']['coverage'],'A common first witness was incorrectly sufficient.')
            ok(not W.search(replace(p,covered=(1,)))['report']['coverage'],'A common second witness was incorrectly sufficient.')
        else:
            ok(set(direct_winners(p,(F(1,4),F(3,4),a)))<=set(p.covered),'Endpoint should be safe.')
            ok(set(direct_winners(p,(F(3,4),F(1,4),a)))<=set(p.covered),'Other endpoint should be safe.')
            ok(2 in direct_winners(p,(F(1,2),F(1,2),a)),'Interior uncovered winner/tie missing.')
        save({'suite':'coupled_weight_exact_example','a':str(a),'report':r,'proof':proof.record(),'work':work,'meaning':'Analytical optimum a-1/2; endpoint-only check and a common incumbent are insufficient.'})

def scalar_reference(p):
    # For a one-dimensional interval, max of finitely many homogeneous lines
    # minimizes at an endpoint or pairwise intersection (here possibly zero).
    values=[]
    for j in range(len(p.states)):
        if j in p.covered:continue
        slopes=[F(p.features[j][0])-F(p.features[g][0]) for g in p.covered]
        candidates={F(p.lower[0]),F(p.upper[0])}
        if any(x!=y for x in slopes for y in slopes) and p.lower[0]<=0<=p.upper[0]:candidates.add(F(0))
        values.append(min(max(s*w for s in slopes) for w in candidates))
    return min(values)

def scalar_cases():
    cases=0
    for coeffs in product((-2,0,3),repeat=4):
        p=W.Problem('scalar-'+str(coeffs),('g0','g1','j0','j1'),tuple((F(x),) for x in coeffs),(0,1),(F(-2),),(F(1),),(),(F(0),))
        work={};a=W.search(p,work=work);ok(a['status']=='VERIFIED','Scalar finite profile did not certify.')
        expect=scalar_reference(p);ok(F(a['report']['margin'])==expect,'Analytical one-dimensional envelope disagrees.')
        for m in a['proof'].margins:ok(W.verify_margin(p,m)==F(m.margin),'Certificate replay differs.')
        if not a['report']['coverage']:
            c=a['report']['counterexample'];ws=tuple(map(F,c['weights']));ok(any(j not in p.covered for j in direct_winners(p,ws)),'Invalid attained coverage counterexample.')
        cases+=1
    save({'suite':'all_four_profile_scalar_coefficients','cases':cases,'coefficient_set':[-2,0,3],'reference':'Independent endpoints/pairwise-line intersection minimization, not the basis search.'})

def hostile():
    p=example(F(3,5),outside2=True);a=W.search(p);ok(a['status']=='VERIFIED','Two outside profiles not certified.');proof=a['proof'];first=proof.margins[0]
    ok(len(proof.margins)==2,'Missing outside profile.')
    errors=[]
    errors.append(reject(lambda:W.verify(p,replace(proof,margins=proof.margins[:1]),p.record())))
    errors.append(reject(lambda:W.verify(p,replace(proof,margins=(first,first)),p.record())))
    errors.append(reject(lambda:W.verify(p,proof,'unrelated request')))
    errors.append(reject(lambda:W.verify(replace(p,scope='changed'),proof,replace(p,scope='changed').record())))
    errors.append(reject(lambda:W.verify_margin(p,replace(first,margin=first.margin+1))))
    mu=list(first.multipliers);mu[0]=F(-1);errors.append(reject(lambda:W.verify_margin(p,replace(first,multipliers=tuple(mu)))))
    errors.append(reject(lambda:W.verify_margin(p,replace(first,multipliers=(F(0),)*len(first.multipliers)))))
    u=list(first.point);u[0]=F(9);errors.append(reject(lambda:W.verify_margin(p,replace(first,point=tuple(u)))))
    errors.append(reject(lambda:W.verify_margin(p,replace(first,outside=True))))
    errors.append(reject(lambda:replace(p,weight_witness=(F(0),F(0),F(3,5))).validate()))
    errors.append(reject(lambda:replace(p,covered=(True,1)).validate()))
    errors.append(reject(lambda:replace(p,features=(p.features[0],)).validate()))
    errors.append(reject(lambda:replace(p,lower=(0.25,F(1,4),F(3,5))).validate()))
    r=W.search(p,max_trials_per_case=0);ok(r['status']=='SEARCH_INCOMPLETE' and r['proof'] is None,'Zero budget became impossibility or guarantee.')
    complete=replace(p,covered=tuple(range(len(p.states))));r=W.search(complete,max_trials_per_case=0)
    ok(r['report']['status']=='FULL_DOMAIN_ALREADY_COVERED','Trivial full coverage failed.')
    empty=replace(p,covered=());ok(W.search(empty)['status']=='NO_CERTIFIED_DOMAIN','Empty certification produced a warrant.')
    errors.append(reject(lambda:W.verify(empty,W.CoverageProof(empty.record(),()),empty.record())))
    save({'suite':'independent_primal_dual_binding_and_search_status','errors':errors,'all_outside_report':a['report'],'all_outside_proof':proof.record()})

def band_integration():
    b0,b1=K.bit(0),K.bit(1)
    cases=(K.AND(K.neg(b0),K.neg(b1)),K.AND(K.neg(b0),b1),K.AND(b0,K.neg(b1)))
    soft=tuple(K.Soft('case'+str(i),K.neg(c),w) for i,(c,w) in enumerate(zip(cases,(F(1,4),F(1,2),F(1)))))
    hard=(K.neg(K.AND(b0,b1)),);d=K.add(K.scale(4,b0),K.lit(-1))
    old=M.Frame(K.Request(2,hard,soft,(('D',d),),'rank-region-band'),'D','U')
    work={};band=M.build_band(old,F(1,2),F(-1),work);M.verify_band(band,old.record())
    records=[]
    for alpha in (F(3,5),F(2,5),F(1,2)):
        e=example(alpha);p=W.from_band(band,old.record(),e.lower,e.upper,e.extra_rows,e.weight_witness,work)
        ok(p.states==('00','01','10') and p.covered==(0,1),'Old band/profile extraction differs.')
        proof=W.search(p)['proof'];r=W.receive_band_region(band,old.record(),e.lower,e.upper,e.extra_rows,e.weight_witness,proof,work)
        ok(r['loss_bound_transported']==(alpha>F(1,2)),'Wrong band transport status.')
        oldw=(F(1,4),F(1,2),F(1));neww=(F(3,4),F(1,4),alpha)
        ok(direct_winners(p,oldw)==(0,) and direct_winners(p,neww)==(1,),'Old winner should disappear.')
        if alpha<=F(1,2):
            ws=tuple(map(F,r['counterexample']['weights']));winners=direct_winners(p,ws)
            actual=[4*int(p.states[j][0])-1 for j in winners]
            ok(max(actual)==3,'Adverse coverage example must really break old -1 loss bound.')
        records.append({'alpha':str(alpha),'report':r,'problem_record':p.record(),'proof':proof.record()})
    e=example(F(3,5));p=W.from_band(band,old.record(),e.lower,e.upper,e.extra_rows,e.weight_witness);pr=W.search(p)['proof']
    errors=[reject(lambda:W.receive_band_region(band,'wrong',e.lower,e.upper,e.extra_rows,e.weight_witness,pr)),
            reject(lambda:W.receive_band_region(replace(band,bound=F(-2)),old.record(),e.lower,e.upper,e.extra_rows,e.weight_witness,pr)),
            reject(lambda:W.from_band(band,old.record(),(F(0),F(1,4),F(3,5)),e.upper,e.extra_rows,e.weight_witness))]
    save({'suite':'actual_verified_band_and_changed_rank_weights','records':records,'work':work,'errors':errors,'old_band':band.record()})

def main():
    global OUT
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();OUT=a.out;OUT.mkdir(parents=True,exist_ok=False)
    names=['05_rank_weight_regions.py','05_rank_weight_regions_check.py','05_counterfactual_transport.py','04_counterfactual_repair.py'];hs={}
    for name in names:
        raw=(HERE/name).read_bytes();(OUT/name).write_bytes(raw);hs[name]=hashlib.sha256(raw).hexdigest()
    manifest={'schema':'p305.rank_regions.development.v1','stage':'DEVELOPMENT','prepared_utc':datetime.now(timezone.utc).isoformat(),'version':W.VERSION,'sources_sha256':hs,'command':sys.argv,'python':sys.version,'platform':platform.platform(),'plan':['analytic coupled weights at a=3/5,2/5,1/2','81 exact one-dimensional four-profile cases','hostile primal/dual and record inputs','binding to an actual three-case old band'],'limits':'Explicit finite profiles and exact arithmetic; optimized LP, statistical rank learning, and a native v2 proof compilation are not implemented.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');start=time.monotonic_ns();error=None
    try:examples();scalar_cases();hostile();band_integration()
    except Exception:error=traceback.format_exc()
    raw=(json.dumps({'assertions':COUNT,'cases':CASES,'error':error},indent=2,default=str)+'\n').encode();(OUT/'results.json').write_bytes(raw)
    r={'status':'FAIL' if error else 'PASS','assertions':COUNT,'suites':len(CASES),'elapsed_ns':time.monotonic_ns()-start,'sources_sha256':hs,'results_sha256':hashlib.sha256(raw).hexdigest(),'error':error};(OUT/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
