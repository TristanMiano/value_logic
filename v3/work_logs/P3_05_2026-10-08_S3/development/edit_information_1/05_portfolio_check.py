#!/usr/bin/env python3
"""New DEVELOPMENT checks of joined certificates, with a separate point oracle.

No old research run is replayed or relabelled. The fixed suite writes source
snapshots, a prospective manifest, complete case records and any failure.
"""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse, hashlib, importlib.util, json, platform, sys, time, traceback
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_p305_portfolio_test_target',HERE/'05_portfolio_transport.py')
P=importlib.util.module_from_spec(sp);sys.modules[sp.name]=P;sp.loader.exec_module(P)
M,K=P.M,P.K
COUNT=0
CASES=[]
PROGRESS_OUT=None

def save_unit(kind, record):
    if PROGRESS_OUT is not None:
        with PROGRESS_OUT.open("a",encoding="utf-8") as f:
            f.write(json.dumps({"kind":kind,"assertions_so_far":COUNT,"record":record},default=str)+"\n")
            f.flush()


def ok(value, message):
    global COUNT
    COUNT+=1
    if not value: raise AssertionError(message)

def reject(call, kind=(ValueError,)):
    global COUNT
    COUNT+=1
    try:call()
    except kind as exc:return {'type':type(exc).__name__,'reason':str(exc)}
    raise AssertionError('Expected rejection did not occur.')

def point(e,x):
    """Independent scalar semantics: never calls interval/collection/checker."""
    op=e[0]
    if op=='lit':return F(e[1])
    if op=='bit':return F(x[e[1]])
    if op=='scale':return F(e[1])*point(e[2],x)
    if op=='not':return 1-point(e[1],x)
    a,b=point(e[1],x),point(e[2],x)
    if op=='add':return a+b
    if op=='eq':return F(a==b)
    if op=='and':return F(a==1 and b==1)
    if op=='or':return F(a==1 or b==1)
    if op=='min':return min(a,b)
    if op=='max':return max(a,b)
    raise ValueError('Independent oracle grammar.')

def frame(n,hard=(),soft=(),d=None,scope='new',metadata='{}',unit='U'):
    return M.Frame(K.Request(n,tuple(hard),tuple(soft),(('D',K.lit(0) if d is None else d),),scope,metadata),'D',unit)

def feasible(f,x):return all(point(h,x)==1 for h in f.request.hard)
def rank(f,x):return sum((s.weight*(1-point(s.formula,x)) for s in f.request.soft),F(0))
def worlds(f):return [x for x in product((0,1),repeat=f.request.nbits) if feasible(f,x)]
def selected(f):
    xs=worlds(f)
    if not xs:return []
    m=min(rank(f,x) for x in xs)
    return [x for x in xs if rank(f,x)==m]

def audit(cache, proof, current):
    verification={};r=cache.verify(proof,current,current.record(),verification)
    xs=[x for x in worlds(current) if rank(current,x)<=rank(current,proof.witness)]
    ok(bool(xs),'A supposedly nonempty report has no source case.')
    for x in xs:ok(point(current.difference,x)<=F(r['bound']),'False all-sublevel bound accepted.')
    for x in selected(current):ok(point(current.difference,x)<=F(r['bound']),'False selected bound accepted.')
    ok(not r['selected_identities_claimed'],'Bound certificate pretends to enumerate all winners.')
    return r,verification

def choice(handle, old, n=None, alpha=F(1), replacements=None):
    rs=tuple(K.bit(i) for i in range(old.request.nbits)) if replacements is None else replacements
    return P.Choice(handle,old.record(),rs,alpha)

def conditional_cases():
    p,q=K.bit(0),K.bit(1)
    current=frame(2,hard=(K.neg(p),K.eq(q,p)),d=q)
    cell=(None,None);rows=P.context_rows(current,cell,F(0))
    w=P.best_witness(q,0,rows,cell)
    ok(w is not None and len(w)>0,'Conditional implication was not established symbolically.')
    ok(P.conditional_upper(q,(),rows,cell)==1,'This is not a separator from unconditioned intervals.')
    ok(P.conditional_upper(q,w,rows,cell)<=0,'Supplied equality witness is invalid.')
    for x in worlds(current):ok(point(q,x)==0,'Premise implication oracle differs.')
    withdrawn=frame(2,hard=(K.eq(q,p),),d=q)
    rw=P.context_rows(withdrawn,cell,F(0))
    ok(P.best_witness(q,0,rw,cell) is None,'Withdrawing p=0 did not reopen q.')
    bad=reject(lambda:P.conditional_upper(q,((0,F(-1)),),rows,cell))
    duplicate=reject(lambda:P.conditional_upper(q,((0,F(1)),(0,F(1))),rows,cell))
    for h,wanted in [(K.AND(p,q),True),(K.OR(p,q),False)]:
        f=frame(2,hard=(h,));r=P.context_rows(f,cell,F(0))
        proof=P.best_witness(K.neg(q),0,r,cell)
        ok((proof is not None)==wanted,'Conjunctive/disjunctive premise direction is wrong.')
    CASES.append({'suite':'conditional_premises','current':current.record(),'target':'q<=0',
                  'weights':w,'rows':rows.expressions,'withdrawn':withdrawn.record(),
                  'negative_multiplier':bad,'duplicate_multiplier':duplicate})

def complementary():
    p,q,r=K.bit(0),K.bit(1),K.bit(2)
    d=K.add(('max',K.sub(p,q),K.sub(q,p)),K.lit(-1))
    old0=frame(3,hard=(K.neg(p),K.neg(q),K.neg(r)),d=d,scope='old-left')
    old1=frame(3,hard=(p,q,K.neg(r)),d=d,scope='old-right')
    current=frame(3,hard=(K.eq(p,q),r),d=d,scope='current-union')
    cache=P.PortfolioCache();build_old={};admit_old={}
    priors=[]
    for name,f in [('left',old0),('right',old1)]:
        b=M.build_band(f,0,-1,build_old);cache.admit_band(name,b,f.record(),admit_old);priors.append(b.record())
    cs=(choice('left',old0,replacements=(p,q,K.lit(0))),choice('right',old1,replacements=(p,q,K.lit(0))))
    build={};pf=cache.build(current,cs,(0,0,1),-1,symbolic=True,allow_direct=False,work=build)
    result,verify=audit(cache,pf,current)
    ok(result['counts']['reuse_leaves']==2 and result['counts']['splits']==1,'Expected a two-leaf joined proof.')
    ok(set(worlds(current)).isdisjoint(set(worlds(old0)+worlds(old1))),'Old candidate identities did not all disappear.')
    for c in cs:
        reject(lambda c=c:cache.build(current,(c,),(0,0,1),-1,allow_direct=False),P.Uncertified)
    # The old syntactic-only receiver cannot infer both partially applicable domains globally.
    old_cache=M.CertificateCache()
    for name,f in [('left',old0),('right',old1)]:old_cache.admit(name,M.build_band(f,0,-1),f.record())
    for c in cs:
        out=old_cache.derive_substituted(c.handle,c.expected_old_record,current,c.replacements,(0,0,1))
        ok(out['status']=='NO_REUSE_CERTIFICATE','The fixture does not separate the prior receiver.')
    CASES.append({'suite':'complementary_domains','old_proofs':priors,'current':current.record(),
                  'proof':pf.record(),'report':result,'old_build_work':build_old,'old_admit_work':admit_old,
                  'current_build_work':build,'current_verify_work':verify})
    return cache,pf,current,cs

def forged_inputs(cache,pf,current,cs):
    errors={}
    errors['wrong_receiving_scope']=reject(lambda:cache.verify(pf,replace(current,request=replace(current.request,scope='other')),current.record()))
    errors['forged_bound']=reject(lambda:cache.verify(replace(pf,bound=F(-100)),current,current.record()))
    errors['missing_sibling']=reject(lambda:cache.verify(replace(pf,tree=('split',0,pf.tree[2])),current,current.record()))
    errors['boolean_split']=reject(lambda:cache.verify(replace(pf,tree=('split',True,pf.tree[2],pf.tree[3])),current,current.record()))
    errors['false_witness']=reject(lambda:cache.verify(replace(pf,witness=(0,0,0)),current,current.record()))
    errors['boolean_witness']=reject(lambda:cache.verify(replace(pf,witness=(0,0,True)),current,current.record()))
    errors['unadmitted_handle']=reject(lambda:cache.verify(replace(pf,choices=(replace(cs[0],handle='absent'),cs[1])),current,current.record()))
    errors['stale_old_record']=reject(lambda:cache.verify(replace(pf,choices=(replace(cs[0],expected_old_record=cs[1].expected_old_record),cs[1])),current,current.record()))
    errors['nonboolean_map']=reject(lambda:cache.verify(replace(pf,choices=(replace(cs[0],replacements=(K.lit(2),K.bit(1),K.lit(0))),cs[1])),current,current.record()))
    errors['negative_scale']=reject(lambda:cache.verify(replace(pf,choices=(replace(cs[0],alpha=F(-1)),cs[1])),current,current.record()))
    errors['cycle']=reject(lambda:cache.admit_portfolio('cycle',replace(pf,choices=(replace(cs[0],handle='cycle'),cs[1])),current,current.record()))
    received=cache.verify(pf,current,current.record());forged=dict(received);forged['bound']='-999'
    errors['forged_report']=reject(lambda:cache.receive(forged,pf,current,current.record()))
    forged=dict(received);forged['non_deterioration']=1
    errors['boolean_integer_report']=reject(lambda:cache.receive(forged,pf,current,current.record()))
    unit_changed=replace(current,unit='other-unit');pfunit=replace(pf,current_record=unit_changed.record())
    errors['wrong_unit']=reject(lambda:cache.verify(pfunit,unit_changed,unit_changed.record()))
    CASES.append({'suite':'hostile_inputs','rejections':errors})

def ties_actions_and_incumbents():
    p=K.bit(0)
    # Strict rank boundary: both points tie, including the adverse one.
    current=frame(1,d=K.add(K.scale(4,p),K.lit(-1)),scope='tied')
    bogus=P.PortfolioProof(current.record(),(),(0,),F(-1),('split',0,('direct',()),('rank',)))
    c=P.PortfolioCache();tie_error=reject(lambda:c.verify(bogus,current,current.record()))
    ok(set(selected(current))=={(0,),(1,)},'Tied source was not correctly represented.')
    # One good action per hidden case is not one good unobserving action.
    da=K.add(K.scale(2,p),K.lit(-1));db=K.scale(-1,da)
    left=frame(1,hard=(K.neg(p),),d=da,scope='proof-action-A')
    right=frame(1,hard=(p,),d=db,scope='proof-action-B')
    fixed=frame(1,d=da,scope='receiving-A-versus-B')
    for name,f in [('A',left),('B',right)]:c.admit_band(name,M.build_band(f,0,-1),f.record())
    options=(choice('A',left),choice('B',right))
    action_error=reject(lambda:c.build(fixed,options,(0,),0,allow_direct=False),P.Uncertified)
    ok(max(point(da,x) for x in selected(fixed))==1,'Hidden-action example has no real conflict.')
    # A loose incumbent expands the certified domain beyond the actual winner.
    ranked=frame(1,soft=(K.Soft('prefer-zero',K.neg(p),F(1)),),d=current.difference,scope='ranked')
    c.admit_band('band',M.build_band(ranked,0,-1),ranked.record())
    option=(choice('band',ranked),)
    weak_error=reject(lambda:c.build(ranked,option,(1,),-1,allow_direct=False),P.Uncertified)
    good=c.build(ranked,option,(0,),-1,allow_direct=False);report,_=audit(c,good,ranked)
    ok(selected(ranked)==[(0,)],'Weak incumbent is not merely a cover failure.')
    CASES.append({'suite':'ties_actions_incumbents','tie_current':current.record(),'rejected_tie_tree':bogus.record(),
                  'tie_error':tie_error,'action_error':action_error,'fixed_action_request':fixed.record(),
                  'weak_incumbent_error':weak_error,'strong_incumbent_proof':good.record(),'report':report})

def chains_and_maps():
    p,q=K.bit(0),K.bit(1)
    old=frame(2,soft=(K.Soft('p',K.neg(p),F(1)),K.Soft('q',K.neg(q),F(2))),
              d=K.add(K.scale(4,q),K.lit(-1)),scope='original')
    c=P.PortfolioCache();c.admit_band('original',M.build_band(old,1,-1),old.record())
    first=replace(old,request=replace(old.request,hard=(p,),scope='first',losses=(('D',K.add(old.difference,K.lit(F(1,2)))),)))
    pf=c.build(first,(choice('original',old),),(1,0),F(-1,2),allow_direct=False)
    r1=c.admit_portfolio('first',pf,first,first.record())
    second=replace(first,request=replace(first.request,scope='second',losses=(('D',K.add(K.scale(2,first.difference),K.lit(F(1,4)))),)))
    second_proof=c.build(second,(choice('first',first,alpha=2),),(1,0),F(-3,4),allow_direct=False)
    r2,_=audit(c,second_proof,second)
    bad=reject(lambda:c.build(second,(choice('first',first,alpha=2),),(1,0),F(-1),allow_direct=False),P.Uncertified)
    undo=reject(lambda:c.build(old,(choice('first',first),),(0,0),-1,allow_direct=False),P.Uncertified)
    direct_original=c.build(old,(choice('original',old),),(0,0),-1,allow_direct=False)
    audit(c,direct_original,old)
    zero=frame(0,d=K.lit(-2),scope='zero-bits');c.admit_band('zero',M.build_band(zero,0,-2),zero.record())
    pzero=c.build(zero,(choice('zero',zero),),(),-2);audit(c,pzero,zero)
    # A simple variable renaming and its mapped loss/rank.
    perm=(1,0);ren=frame(2,hard=(q,),soft=tuple(K.Soft(s.identity,M.rename(s.formula,perm),s.weight) for s in old.request.soft),
                        d=M.rename(old.difference,perm),scope='rename')
    pr=c.build(ren,(choice('original',old,replacements=(q,p)),),(0,1),-1,allow_direct=False);audit(c,pr,ren)
    CASES.append({'suite':'chains_scaling_undo_maps','first':pf.record(),'first_report':r1,
                  'second':second_proof.record(),'second_report':r2,'unscaled_error_rejected':bad,
                  'intermediate_undo_rejected':undo,'original_undo':direct_original.record(),
                  'zero_bits':pzero.record(),'rename':pr.record()})

def disjunction_for(points,n):
    terms=[]
    for x in points:
        parts=[K.bit(i) if v else K.neg(K.bit(i)) for i,v in enumerate(x)]
        e=K.lit(1)
        for part in parts:e=K.AND(e,part)
        terms.append(e)
    if not terms:return K.lit(0)
    while len(terms)>1:
        terms=[K.OR(terms[i],terms[i+1]) if i+1<len(terms) else terms[i] for i in range(0,len(terms),2)]
    return terms[0]

def completeness_corpus():
    n=3;xs=list(product((0,1),repeat=n));bits=[K.bit(i) for i in range(n)]
    difference=P.balanced_sum([bits[0],K.scale(2,bits[1]),K.scale(-3,bits[2])])
    cache=P.PortfolioCache();opts=[];sources=[]
    for i,x in enumerate(xs):
        f=frame(n,hard=tuple(K.bit(j) if v else K.neg(K.bit(j)) for j,v in enumerate(x)),d=difference,scope=f'point-{i}')
        b=point(difference,x);proof=M.build_band(f,0,b);cache.admit_band(str(i),proof,f.record())
        opts.append(choice(str(i),f));sources.append(proof.record())
    records=[]
    # Every nonempty subset. Complete pointwise coverage implies a tree exists.
    for mask in range(1,256):
        keep=[x for i,x in enumerate(xs) if mask&(1<<i)]
        current=frame(n,hard=(disjunction_for(keep,n),),d=difference,scope=f'subset-{mask}')
        bound=max(point(difference,x) for x in keep)
        before=COUNT;pf=cache.build(current,tuple(opts),keep[0],bound,allow_direct=False)
        result,_=audit(cache,pf,current)
        # Removing a point's only proof cannot be hidden by unrelated proof handles.
        if mask in (1,3,7,15,31,63,127,255):
            removed=xs.index(keep[-1]);reduced=tuple(o for i,o in enumerate(opts) if i!=removed)
            reject(lambda:cache.build(current,reduced,keep[0],bound,allow_direct=False),P.Uncertified)
        records.append({'mask':mask,'current_record':current.record(),'proof':pf.record(),
                        'report':result,'assertions':COUNT-before})
        save_unit('completed_source_subset',records[-1])
    CASES.append({'suite':'finite_relative_completeness','nbits':n,'source_proofs':sources,'cases':records})

def main():
    global PROGRESS_OUT
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    out=args.out;out.mkdir(parents=True,exist_ok=False)
    PROGRESS_OUT=out/"completed_units.jsonl"
    files=['05_portfolio_check.py','05_portfolio_transport.py','05_counterfactual_transport.py','04_counterfactual_repair.py']
    hashes={}
    for name in files:
        b=(HERE/name).read_bytes();(out/name).write_bytes(b);hashes[name]=hashlib.sha256(b).hexdigest()
    manifest={'schema':'value_logic.p305.s3.development.v1','status':'PREPARED','evidence_type':'DEVELOPMENT',
              'version':P.VERSION,'sources_sha256':hashes,'utc':datetime.now(timezone.utc).isoformat(),
              'python':sys.version,'platform':platform.platform(),'command':sys.argv,
              'purpose':'Joined coverage, conditional premises, false certificates, fixed action, chaining and all nonempty three-bit source subsets.',
              'review':'Same contributor; independent scalar evaluator, not external or distinct-agent validation.'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    start=time.monotonic_ns();error=None
    try:
        conditional_cases();save_unit('suite',CASES[-1])
        c,p,f,cs=complementary();save_unit('suite',CASES[-1])
        forged_inputs(c,p,f,cs);save_unit('suite',CASES[-1])
        ties_actions_and_incumbents();save_unit('suite',CASES[-1])
        chains_and_maps();save_unit('suite',CASES[-1])
        completeness_corpus()
    except Exception:error=traceback.format_exc()
    result={'cases':CASES,'assertions':COUNT,'error':error}
    raw=(json.dumps(result,indent=2,default=str)+'\n').encode();(out/'results.json').write_bytes(raw)
    summary={'status':'FAIL' if error else 'PASS','assertions':COUNT,'suites_completed':len(CASES),
             'elapsed_ns':time.monotonic_ns()-start,'error':error,'sources_sha256':hashes,
             'results_sha256':hashlib.sha256(raw).hexdigest()}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
