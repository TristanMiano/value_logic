#!/usr/bin/env python3
"""DEVELOPMENT checks, with a separate exact point evaluator.

Writes fresh evidence directory only; complete inputs, sources, checks and
failures are preserved. Counts are assertions, not independent discoveries.
"""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse, hashlib, importlib.util, json, platform, random, sys, time, traceback
sys.dont_write_bytecode = True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('transport_under_test', HERE/'05_counterfactual_transport.py')
M=importlib.util.module_from_spec(spec);sys.modules[spec.name]=M;spec.loader.exec_module(M)
K=M.K
COUNT=0
ROWS=[]

def ok(condition, message):
    global COUNT
    COUNT+=1
    if not condition:raise AssertionError(message)


def reject(call, kind=M.Rejected):
    global COUNT
    COUNT+=1
    try:call()
    except kind as exc:return str(exc)
    raise AssertionError('Expected rejection did not happen.')


def point(e,x):
    """No calls to production interval evaluator, collector or rank helper."""
    if e[0]=='lit':return F(e[1])
    if e[0]=='bit':return F(x[e[1]])
    if e[0]=='scale':return F(e[1])*point(e[2],x)
    if e[0]=='not':return 1-point(e[1],x)
    a,b=point(e[1],x),point(e[2],x)
    return {'add':lambda:a+b,'and':lambda:F(bool(a) and bool(b)),
            'or':lambda:F(bool(a) or bool(b)),'eq':lambda:F(a==b),
            'min':lambda:min(a,b),'max':lambda:max(a,b)}[e[0]]()


def rank(frame,x):
    return sum((F(s.weight)*(1-point(s.formula,x)) for s in frame.request.soft),F(0))


def feasible(frame,x):return all(point(h,x)==1 for h in frame.request.hard)


def selected(frame):
    xs=[x for x in product((0,1),repeat=frame.request.nbits) if feasible(frame,x)]
    if not xs:return []
    v=min(rank(frame,x) for x in xs)
    return [x for x in xs if rank(frame,x)==v]


def frame(n,hard=(),soft=(),d=None,scope='test',meta='{}',unit='U'):
    return M.Frame(K.Request(n,tuple(hard),tuple(soft),(('D',d or K.lit(0)),),scope,meta),'D',unit)


def check_proof_oracle(p):
    for x in product((0,1),repeat=p.frame.request.nbits):
        if feasible(p.frame,x) and rank(p.frame,x)<=p.cutoff:
            ok(point(p.frame.difference,x)<=p.bound,'Band proof violates independent point oracle.')


def fixtures():
    p,q=K.bit(0),K.bit(1)
    old=frame(2,soft=(K.Soft('p',K.neg(p),F(1)),K.Soft('q',K.neg(q),F(2))),d=K.add(K.scale(4,q),K.lit(-1)),scope='base')
    work={};wide=M.build_band(old,1,-1,work);check_proof_oracle(wide)
    admit={};cache=M.CertificateCache();cache.admit('wide',wide,old.record(),admit)
    narrow=M.build_band(old,0,-1);cache.admit('narrow',narrow,old.record())
    new=replace(old,request=replace(old.request,hard=(p,),scope='p-required'))
    report=cache.derive('wide',old.record(),new,(0,1),(1,0))
    ok(selected(old)==[(0,0)] and selected(new)==[(1,0)],'Not a real optimizer turnover.')
    ok(report['bound']=='-1','Expected wider-band reuse.')
    ok(cache.derive('narrow',old.record(),new,(0,1),(1,0))['status']=='NO_REUSE_CERTIFICATE','Narrow old-winner certificate reused.')
    bad=replace(old,request=replace(old.request,hard=(q,),scope='q-required'))
    ok(point(bad.difference,selected(bad)[0])==3,'Missing adverse winner.')
    ok(cache.derive('wide',old.record(),bad,(0,1),(0,1))['status']=='NO_REUSE_CERTIFICATE','Winner escaped the certified band.')
    for shift,expected in [(F(1,2),'-1/2'),(F(2),'1')]:
        changed=replace(new,request=replace(new.request,losses=(('D',K.add(old.difference,K.lit(shift))),)))
        r=cache.derive('wide',old.record(),changed,(0,1),(1,0))
        ok(r['bound']==expected,'Loss drift mishandled.')
        ok(r['non_deterioration']==(shift<=1),'Non-deterioration mislabeled.')
    # Coordinate permutation is an explicit complete map, not a coincidental value match.
    perm=(1,0)
    ren=frame(2,hard=(q,),soft=tuple(K.Soft(s.identity,M.rename(s.formula,perm),s.weight) for s in old.request.soft),
              d=M.rename(old.difference,perm),scope='renamed')
    ok(cache.derive('wide',old.record(),ren,perm,(0,1))['bound']=='-1','Transported rename failed.')
    for count in range(1,5):
        req=replace(new,request=replace(new.request,scope=f'edit-{count}',losses=(('D',K.add(old.difference,K.lit(F(count,10)))),)))
        r=cache.derive('wide',old.record(),req,(0,1),(1,0))
        ok(F(r['bound'])==F(-1)+F(count,10),'Repeated edits incorrectly accumulate stale values.')
    ok(cache.derive('wide',old.record(),old,(0,1),(0,0))['bound']=='-1','Exact undo blocked valid direct reuse.')
    # Explicit positive scaling; same declared unit in this restricted receiver.
    scaled=replace(new,request=replace(new.request,losses=(('D',K.scale(2,old.difference)),)))
    ok(cache.derive('wide',old.record(),scaled,(0,1),(1,0),alpha=2)['bound']=='-2','Scaling bridge failed.')
    ROWS.append({'suite':'turnover_loss_edits_rename_undo','wide_proof':wide.record(),'new_request':new.record(),
                 'report':report,'build_work':work,'admission_work':admit})
    # Retained hard-premise membership is required; no blanket narrowing inference.
    restricted=frame(2,hard=(K.neg(q),),d=old.difference,scope='uses-q0')
    pr=M.build_band(restricted,0,-1);c=M.CertificateCache();c.admit('r',pr,restricted.record())
    withdrawn=frame(2,d=old.difference,scope='withdrawn')
    ok(c.derive('r',restricted.record(),withdrawn,(0,1),(0,0))['status']=='NO_REUSE_CERTIFICATE','Withdrawn premise reused without repair.')
    ROWS.append({'suite':'withdrawal','proof':pr.record(),'current_request':withdrawn.record()})
    return cache,old,new,wide,report


def hostile(cache,old,new,proof,report):
    errors={}
    errors['forged_bound']=reject(lambda:M.verify_band(replace(proof,bound=F(-100)),old.record()))
    errors['missing_partition']=reject(lambda:M.verify_band(replace(proof,tree=('split',0,('leaf','loss'))),old.record()))
    errors['bool_split']=reject(lambda:M.verify_band(replace(proof,tree=('split',True,proof.tree,proof.tree)),old.record()))
    errors['bad_permutation']=reject(lambda:cache.derive('wide',old.record(),new,(0,0),(1,0)))
    errors['bool_witness']=reject(lambda:cache.derive('wide',old.record(),new,(0,1),(True,0)))
    errors['false_witness']=reject(lambda:cache.derive('wide',old.record(),new,(0,1),(0,0)))
    errors['wrong_unit']=reject(lambda:cache.derive('wide',old.record(),replace(new,unit='V'),(0,1),(1,0)))
    errors['negative_scale']=reject(lambda:cache.derive('wide',old.record(),new,(0,1),(1,0),alpha=-1))
    forged=dict(report);forged['bound']='-999'
    errors['forged_report']=reject(lambda:cache.receive(forged,'wide',old.record(),new,(0,1),(1,0)))
    forged=dict(report);forged['non_deterioration']=1
    errors['bool_equals_one_report']=reject(lambda:cache.receive(forged,'wide',old.record(),new,(0,1),(1,0)))
    a=replace(old,request=replace(old.request,metadata_json='{"flag":true}'))
    b=replace(old,request=replace(old.request,metadata_json='{"flag":1}'))
    ok(a.record()!=b.record(),'Metadata true silently equated with 1.')
    pa=M.build_band(a,1,-1)
    errors['bool_equals_one_request']=reject(lambda:M.verify_band(pa,b.record()))
    errors['duplicate_metadata']=reject(lambda:replace(old,request=replace(old.request,metadata_json='{"flag":0,"flag":1}')))
    errors['float_metadata']=reject(lambda:replace(old,request=replace(old.request,metadata_json='{"flag":1.0}')))
    errors['lexicographic_not_scalar']=reject(lambda:frame(1,soft=(K.Soft('x',K.bit(0),F(1),1),)))
    errors['bad_bound_real_failure']=reject(lambda:M.build_band(old,1,-2),M.NoBandProof)
    ROWS.append({'suite':'hostile_inputs','rejections':errors})


def ties_and_ports():
    for eps in [F(1,10),F(1),F(5)]:
        old=frame(1,soft=(K.Soft('n',K.neg(K.bit(0)),2*eps),),d=K.scale(100,K.bit(0)))
        new=frame(1,soft=(K.Soft('n',K.neg(K.bit(0)),eps),K.Soft('p',K.bit(0),eps)),d=old.difference)
        ok(selected(old)==[(0,)] and selected(new)==[(0,),(1,)],'Sharp 2-error tie witness failed.')
        ok(M.rank_drift(old,new,(0,))==eps,'Exact fixture rank drift wrong.')
        pr=M.build_band(old,2*eps,100);cc=M.CertificateCache();cc.admit('tie',pr,old.record())
        r=cc.derive('tie',old.record(),new,(0,),(0,))
        ok(F(r['needed_cutoff'])==2*eps and F(r['bound'])==100,'Boundary tied candidate lost.')
    ok(max(min(a,b) for a,b in [(0,10),(10,0)])==0,'Pointwise portfolio.')
    ok(min(max(0,10),max(10,0))==10,'Portfolio order separator.')
    # Explicit affine withdrawal penalty, exact finite arithmetic check.
    for x in range(-5,6):
        d=3*x+2;old_bound=5;penalty=3*max(x-1,0)
        ok(d<=old_bound+penalty,'Affine withdrawal inequality failed.')
    for Mbig in [1,10,10000]:
        rho0=[(F(0),F(0)),(F(1,10),F(Mbig))]
        rho1=[(F(1,10),F(0)),(F(0),F(Mbig))]
        ok(min(range(2),key=lambda i:rho0[i])==0 and min(range(2),key=lambda i:rho1[i])==1,'Lexicographic warning absent.')
    ROWS.append({'suite':'ties_portfolios_withdrawal_lexicographic','type':'finite fixtures for hand derivations'})


def structural_cases():
    outputs={}
    for name,mask,want in [('token',(True,False,False,False),7),('shared',(True,True,False,False),5),
                            ('copy_too',(True,True,True,False),4),('predictor_too',(True,True,True,True),2)]:
        r=K.route_replacement((0,0),(1,0),0,tuple(zip(('A','B','C','P'),mask)),1)
        d=r['outputs'];v=6+d['A']-2*d['B']-d['C']-2*d['P']
        ok(v==want,'Routing dependency lost.')
        outputs[name]={'outputs':d,'loss':v}
    # Same whole observational law, different intervention.
    for u in (0,1):
        direct_obs=(u,u); common_obs=(u,u)
        ok(direct_obs==common_obs,'Observational twins differ.')
    ok((1,1)!=(1,0),'Intervention not separated.')
    ROWS.append({'suite':'structural_dependence','actual_loss':6,'cases':outputs,
                 'note':'Given finite tables and routing, not learned causal/counterpossible structure.'})


def corpus():
    rng=random.Random(3052026)
    cases=[];accepted=denied=0
    for i in range(160):
        n=1+i%5;bits=[K.bit(j) for j in range(n)]
        soft=tuple(K.Soft(f's{j}',K.neg(bits[j]),F(rng.randrange(1,5),2)) for j in range(n))
        d=K.lit(rng.randrange(-3,4))
        for j in range(n):d=K.add(d,K.scale(rng.randrange(-4,5),bits[j]))
        if i%3==0:d=K.add(d,('min',bits[0],K.neg(bits[0])))
        old=frame(n,soft=soft,d=d,scope=f'corpus-old-{i}')
        xs=list(product((0,1),repeat=n))
        h=rank(old,xs[rng.randrange(len(xs))])
        band=[x for x in xs if rank(old,x)<=h]
        bound=max(point(d,x) for x in band)
        proof=M.build_band(old,h,bound);M.verify_band(proof,old.record());check_proof_oracle(proof)
        c=M.CertificateCache();c.admit('x',proof,old.record())
        p=list(range(n));rng.shuffle(p);p=tuple(p)
        seed=tuple(rng.randrange(2) for _ in range(n));hard=(bits[0] if seed[0] else K.neg(bits[0]),)
        nsoft=tuple(K.Soft(s.identity,M.rename(s.formula,p),s.weight+F(rng.randrange(-1,2),4)) for s in soft)
        offset=F(rng.randrange(-3,4),4)
        nd=K.add(M.rename(d,p),K.lit(offset))
        new=frame(n,hard=hard,soft=nsoft,d=nd,scope=f'corpus-new-{i}')
        r=c.derive('x',old.record(),new,p,seed)
        chosen=selected(new);ok(bool(chosen),'Generated infeasible current problem.')
        if r['status']=='REUSE_CERTIFIED':
            accepted+=1
            for y in chosen:
                old_y=tuple(y[j] for j in p)
                ok(rank(old,old_y)<=h,'New minimizer outside claimed old band.')
                ok(point(nd,y)<=F(r['bound']),'Returned bound unsound on a new winner.')
            ok(c.receive(r,'x',old.record(),new,p,seed)==r,'Receiving its exact report failed.')
        else:denied+=1
        cases.append({'old':old.record(),'new':new.record(),'cutoff':str(h),'bound':str(bound),'permutation':p,'witness':seed,
                      'report':r,'exact_new_winners':chosen,'exact_new_upper':str(max(point(nd,x) for x in chosen))})
    ROWS.append({'suite':'fixed_seed_corpus','seed':3052026,'cases':cases,'accepted':accepted,'inconclusive':denied})


def resource_cases():
    data=[]
    for n in (1,4,7):
        parity=K.bit(0)
        for i in range(1,n):parity=K.neg(K.eq(parity,K.bit(i)))
        d=K.add(('min',parity,K.neg(parity)),K.lit(F(-1,4)))
        old=frame(n,soft=(K.Soft('p',K.neg(K.bit(0)),F(1)),),d=d,scope='parity')
        oldwork={};t=time.perf_counter_ns();proof=M.build_band(old,1,F(-1,4),oldwork);c=M.CertificateCache();c.admit('p',proof,old.record(),oldwork);initial=time.perf_counter_ns()-t
        new=replace(old,request=replace(old.request,hard=(K.bit(0),),losses=(('D',K.add(d,K.lit(F(1,8)))),),scope='parity-edit'))
        witness=(1,)+(0,)*(n-1)
        warm={};t=time.perf_counter_ns();r=c.derive('p',old.record(),new,tuple(range(n)),witness,work=warm);warm_ns=time.perf_counter_ns()-t
        fresh={};t=time.perf_counter_ns();p=M.build_band(new,rank(new,witness),0,fresh);M.verify_band(p,new.record(),fresh);fresh_ns=time.perf_counter_ns()-t
        ok(r['status']=='REUSE_CERTIFIED' and F(r['bound'])<=0,'Resource fixture failed its shared decision threshold.')
        ok(all(point(new.difference,x)<=0 for x in selected(new)),'Reference resource bound false.')
        data.append({'bits':n,'initial_build_and_admit':oldwork,'initial_ns':initial,'warm':warm,'warm_ns':warm_ns,
                     'fresh_build_and_admit':fresh,'fresh_ns':fresh_ns,'threshold':0,'warm_bound':r['bound']})
    # Constant case exposes unnecessary warm bridge work; no universal speedup.
    old=frame(1,d=K.lit(-1));p=M.build_band(old,0,-1);c=M.CertificateCache();c.admit('e',p,old.record())
    warm={};r=c.derive('e',old.record(),old,(0,),(0,),work=warm)
    fresh={};q=M.build_band(old,0,0,fresh);M.verify_band(q,old.record(),fresh)
    data.append({'case':'constant_easy','warm':warm,'fresh':fresh})
    ROWS.append({'suite':'resource_diagnostics','cases':data,
       'limits':'Single-run illustrative timings, not a benchmark. Instrumented counters omit Python allocation, structural key traversal and some validation. Same-access ordinary cache has identical algorithm. Boolean symbolic simplification can beat both parity runs.'})


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    sources={}
    for name in ('05_counterfactual_transport.py','05_counterfactual_transport_check.py','04_counterfactual_repair.py'):
        content=(HERE/name).read_bytes();(args.out/name).write_bytes(content);sources[name]=hashlib.sha256(content).hexdigest()
    manifest={'status':'PREPARED','label':'DEVELOPMENT','version':M.VERSION,'sources_sha256':sources,
              'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),
              'protocol':'Fixed fixtures, seed 3052026 corpus (160), three resource sizes plus constant case. All prior designs visible; no final evaluation.',
              'command':sys.argv}
    (args.out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    start=time.perf_counter_ns();error=None
    try:
        c,o,n,p,r=fixtures();hostile(c,o,n,p,r);ties_and_ports();structural_cases();corpus();resource_cases()
    except Exception:
        error=traceback.format_exc()
    summary={'status':'FAIL' if error else 'PASS','assertions':COUNT,'suites_completed':len(ROWS),
             'elapsed_ns':time.perf_counter_ns()-start,'error':error,'independent_point_oracle':True,
             'review':'self-review; evaluator separately implemented by same contributor','sources_sha256':sources}
    (args.out/'results.json').write_text(json.dumps(ROWS,indent=2,default=str)+'\n')
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    if error:raise SystemExit(1)

if __name__=='__main__':main()
