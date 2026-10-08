#!/usr/bin/env python3
"""DEVELOPMENT: finite program compilation, edit routing and proof binding.

Finite exhaustive truth tables and supplied source families, not blind evaluation.
Separate scalar evaluators and structural tables check the compiler's denotation.
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
sp=importlib.util.spec_from_file_location('_p305_dependency_test_target',HERE/'05_dependency_frontend.py')
D=importlib.util.module_from_spec(sp);sys.modules[sp.name]=D;sp.loader.exec_module(D)
P,M,K=D.P,D.M,D.K
COUNT=0;CASES=[];OUT=None


def ok(v,msg):
    global COUNT
    COUNT+=1
    if not v:raise AssertionError(msg)


def reject(fn,kind=(ValueError,)):
    global COUNT
    COUNT+=1
    try:fn()
    except kind as e:return {'type':type(e).__name__,'reason':str(e)}
    raise AssertionError('Expected rejection did not occur.')


def save(v):
    CASES.append(v)
    if OUT:
        with (OUT/'completed_units.jsonl').open('a') as f:f.write(json.dumps({'assertions':COUNT,'case':v},default=str)+'\n');f.flush()


def point(e,x):
    op=e[0]
    if op=='lit':return F(e[1])
    if op=='bit':return F(x[e[1]])
    if op=='scale':return F(e[1])*point(e[2],x)
    if op=='not':return 1-point(e[1],x)
    a,b=point(e[1],x),point(e[2],x)
    if op=='add':return a+b
    if op=='and':return F(a==1 and b==1)
    if op=='or':return F(a==1 or b==1)
    if op=='eq':return F(a==b)
    if op=='min':return min(a,b)
    if op=='max':return max(a,b)
    raise ValueError('Oracle grammar.')


def evaluate(prog,x):
    """Point semantics; no compiler, interval, or denotational shortcut."""
    tables={t.name:t for t in prog.tables};state={}
    def go(e):
        if e[0]=='const':return e[1]
        if e[0]=='input':return x[e[1]]
        if e[0]=='ref':return state[e[1]]
        if e[0]=='not':return 1-go(e[1])
        if e[0]=='and':return go(e[1]) & go(e[2])
        if e[0]=='or':return go(e[1]) | go(e[2])
        if e[0]=='xor':return go(e[1]) ^ go(e[2])
        if e[0]=='call':
            i=0
            for a in e[2]:i=2*i+go(a)
            return tables[e[1]].values[i]
        raise ValueError('Oracle input grammar.')
    for name,e in prog.definitions:state[name]=go(e)
    return {name:go(e) for name,e in prog.outputs}


def prog(n,tables=(),defs=(),outputs=(('o',('input',0)),),scope='base'):
    return D.Program(scope,tuple('h'+str(i) for i in range(n)),tuple(tables),tuple(defs),tuple(outputs))


def compile_check(p):
    work={};c=D.compile_program(p,work)
    for x in product((0,1),repeat=len(p.inputs)):
        got={name:point(e,x) for name,e in c.outputs}
        ok(got==evaluate(p,x),'Compiler differs from independently evaluated program.')
        for _,e in c.outputs:ok(K.interval(e,x)==(point(e,x),)*2,'Imported exact-point evaluator differs.')
    return c,work


def complete_table_tests():
    rows=0;counts={}
    for arity in range(4):
        count=0
        for values in product((0,1),repeat=2**arity):
            p=prog(max(1,arity),tables=(D.Table('f',arity,values),),
                outputs=(('o',('call','f',tuple(('input',i) for i in range(arity)))),),scope='table-'+str(arity)+'-'+str(count))
            _,w=compile_check(p);count+=1;rows+=2**arity
        counts[str(arity)]=count
    save({'suite':'all_boolean_tables_through_arity_three','tables':counts,'table_entries':rows})
    functions=(('and',(0,0,0,1)),('xor',(0,1,1,0)),('or',(0,1,1,1)),('proj',(0,0,1,1)))
    count=0
    for (na,a),(nb,b) in product(functions,repeat=2):
        for route in ('ref','inline'):
            core=('call','a',(('input',0),('input',1)))
            arg=('ref','shared') if route=='ref' else core
            p=prog(2,tables=(D.Table('a',2,a),D.Table('b',2,b)),defs=(('shared',core),),
                outputs=(('o',('call','b',(arg,('not',arg)))),('other',('xor',arg,('input',0)))),scope=na+nb+route)
            compile_check(p);count+=1
    save({'suite':'shared_and_inlined_composition','programs':count})


def base_program():
    tables=tuple(D.Table(t,1,(0,1)) for t in ('live','copy','original_predictor'))
    call=lambda t:('call',t,(('input',0),))
    return prog(1,tables,defs=(('live_result',call('live')),),outputs=(('A',('ref','live_result')),('B',('ref','live_result')),('C',call('copy')),('P',call('original_predictor'))),scope='old-runtime')


def modified(p,names,scope):
    return replace(p,scope=scope,tables=tuple(replace(t,values=(1,0)) if t.name in names else t for t in p.tables))


def comparison(a,b,hard=(),scope='compare'):
    return D.Comparison(scope,a,b,(('A',F(1)),('B',F(-2)),('C',F(-1)),('P',F(-2))),tuple(hard),())


def routing_and_binding():
    old=base_program();token=replace(old,scope='token',outputs=tuple((n,('const',1)) if n=='A' else (n,e) for n,e in old.outputs))
    new=modified(old,{'live'},'live-replaced');copy=modified(old,{'live','copy'},'live-copy-replaced');all_=modified(old,{'live','copy','original_predictor'},'all-replaced')
    results=[]
    for p,expected in ((token,1),(new,-1),(copy,-2),(all_,-4)):
        req=comparison(old,p,(K.neg(K.bit(0)),),scope=p.scope);c=D.compile_comparison(req)
        compile_check(p);ok(point(c.difference,(0,))==expected,'Routing loss mismatch.')
        cache=P.PortfolioCache();build={};proof=D.produce(cache,req,(),(0,),expected,work=build);check={}
        receipt=D.receive(cache,proof,req,req.record(),expected,check)
        results.append({'request':req.record(),'difference_at_zero':expected,'proof':M.canonical(proof.portfolio.record()),'receive':receipt,'build_work':build,'receive_work':check})
    oldreq=comparison(old,new,(K.neg(K.bit(0)),),'h-fixed');current=replace(oldreq,scope='h-withdrawn',hard=())
    oldframe=D.compile_comparison(oldreq);oldproof=M.build_band(oldframe,F(0),F(-1));cache=P.PortfolioCache();cache.admit_band('old',oldproof,oldframe.record())
    ch=(P.Choice('old',oldframe.record(),(K.lit(0),)),)
    proof=D.produce(cache,current,ch,(0,),1,allow_direct=False);receipt=D.receive(cache,proof,current,current.record(),1)
    ok(receipt['certificate']['counts']['reuse_leaves']>0,'Withdrawal did not exercise reuse.')
    ok([point(D.compile_comparison(current).difference,(h,)) for h in (0,1)]==[F(-1),F(1)],'Wrong withdrawn loss range.')
    errors=[reject(lambda:D.produce(cache,current,ch,(0,),-1,allow_direct=False)),
            reject(lambda:D.receive(cache,proof,current,current.record(),0)),
            reject(lambda:D.receive(cache,proof,replace(current,new=all_),replace(current,new=all_).record(),1)),
            reject(lambda:D.receive(cache,replace(proof,comparison_record='forged'),current,current.record(),1))]
    fresh=D.produce(cache,current,(),(0,),1)
    wrong=replace(fresh,portfolio=replace(fresh.portfolio,bound=F(-100)))
    errors.append(reject(lambda:D.receive(cache,wrong,current,current.record(),1)))
    save({'suite':'typed_routing_and_independently_bound_receiving','cases':results,'withdrawal':receipt,'rejections':errors})


def dependence_and_renaming():
    p=base_program();twin=replace(p,scope='twin-copy-B',outputs=tuple((n,('call','copy',(('input',0),))) if n=='B' else (n,e) for n,e in p.outputs))
    for h in (0,1):ok(evaluate(p,(h,))==evaluate(twin,(h,)),'Observational twins differ.')
    a=modified(p,{'live'},'changed');b=modified(twin,{'live'},'changed-twin')
    ok(evaluate(a,(0,))['B']==1 and evaluate(b,(0,))['B']==0,'Shared edit did not expose routing ambiguity.')
    # Irrelevant-copy editing preserves A's support, but not C's support.
    changed=modified(p,{'copy'},'only-copy')
    ok(D.relevant_record(p,'A')==D.relevant_record(changed,'A'),'Unrelated edit changes sufficient support.')
    ok(D.relevant_record(p,'C')!=D.relevant_record(changed,'C'),'Relevant edit missed.')
    def rename(e):
        if e[0]=='ref':return ('ref','renamed-'+e[1])
        if e[0]=='call':return ('call','renamed-'+e[1],tuple(rename(x) for x in e[2]))
        if e[0] in ('const','input'):return e
        return (e[0],)+tuple(rename(x) for x in e[1:])
    rp=replace(p,scope='renamed',tables=tuple(replace(t,name='renamed-'+t.name) for t in p.tables),definitions=tuple(('renamed-'+n,rename(e)) for n,e in p.definitions),outputs=tuple((n,rename(e)) for n,e in p.outputs))
    cp,_=compile_check(p);cr,_=compile_check(rp)
    for h in (0,1):
        ok(evaluate(p,(h,))==evaluate(rp,(h,)),'Consistent renaming changes outputs.')
        ok({n:point(e,(h,)) for n,e in cp.outputs}=={n:point(e,(h,)) for n,e in cr.outputs},'Compiled renaming mismatch.')
    # Explicit structural-equation comparator on each shared context.
    for h in (0,1):
        equations=tuple(K.Equation(n,(0,1),('h',),(((0,),0),((1,),1))) for n in ('A','B','C','P'))
        s=K.structural(equations,{'h':h});ok({n:s[n] for n in ('A','B','C','P')}==evaluate(p,(h,)),'Ordinary structural comparator disagrees.')
    save({'suite':'observational_twins_support_and_consistent_renaming','base':p.record(),'twin':twin.record(),'changed_outputs_at_zero':[evaluate(a,(0,)),evaluate(b,(0,))],'compiler_scope':'Boolean denotation, not cost-preserving arbitrary refactoring.'})


def malformed_and_caps():
    p=base_program();bad=[]
    bad.append(reject(lambda:D.compile_program(replace(p,definitions=p.definitions+(('unused',('ref','missing')),)))))
    bad.append(reject(lambda:D.compile_program(replace(p,definitions=(('cycle',('ref','cycle')),)))))
    bad.append(reject(lambda:D.compile_program(replace(p,tables=(D.Table('f',1,(0,True)),)))))
    bad.append(reject(lambda:D.compile_program(replace(p,tables=p.tables+(p.tables[0],)))))
    bad.append(reject(lambda:D.compile_program(replace(p,outputs=(('A',('call','live',())),)))))
    bad.append(reject(lambda:D.compile_program(replace(p,outputs=(('A',('input',True)),)))))
    bad.append(reject(lambda:D.compile_program(replace(p,inputs=('x',)*2))))
    # Compact DAG can have exponential expansion; admission must reject the
    # expanded expression rather than claim a bounded proof was supplied.
    ds=[('a0',('input',0))]
    for i in range(1,12):ds.append(('a'+str(i),('xor',('ref','a'+str(i-1)),('ref','a'+str(i-1)))))
    bad.append(reject(lambda:D.compile_program(prog(1,defs=ds,outputs=(('o',('ref','a11')),)))))
    bad.append(reject(lambda:D.compile_comparison(replace(comparison(p,p),weights=(('A',0.5),)))))
    bad.append(reject(lambda:D.compile_comparison(replace(comparison(p,p),weights=(('A',True),)))))
    bad.append(reject(lambda:D.compile_comparison(replace(comparison(p,p),new=replace(p,inputs=('different',)))))))
    bad.append(reject(lambda:D.compile_comparison(replace(comparison(p,p),soft=({},)))))
    save({'suite':'malformed_inputs_expansion_and_scope','rejections':bad,'boundary':'Input and expression caps do not bound all Python CPU/RAM.'})


def all_routing_maps():
    p=base_program();count=0;records=[]
    for oldv,newv in product(product((0,1),repeat=2),repeat=2):
        for mask in range(16):
            a=replace(p,tables=tuple(replace(t,values=oldv) for t in p.tables),scope='old-tables')
            b=replace(a,scope='routed-new',tables=a.tables+(D.Table('new',1,newv),),outputs=tuple((name,('call','new',(('input',0),))) if mask>>j&1 else (name,e) for j,(name,e) in enumerate(a.outputs)))
            req=comparison(a,b,scope='finite-routed-'+str(count));frame=D.compile_comparison(req)
            for h in (0,1):
                x,y=evaluate(a,(h,)),evaluate(b,(h,));wanted=sum(w*(y[n]-x[n]) for n,w in req.weights)
                ok(point(frame.difference,(h,))==wanted,'Paired output loss was not preserved.')
                k=K.route_replacement(oldv,newv,h,tuple((n,bool(mask>>j&1)) for j,(n,_) in enumerate(a.outputs)),required=newv[h])
                ok(y==k['outputs'],'Explicit routing comparator disagrees.')
            count+=1
    ok(count==256,'Routing corpus is incomplete.')
    save({'suite':'complete_one_bit_function_pair_routing_family','requests':count,'same_original_and_replacement_body_allowed':True})


def main():
    global OUT
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();OUT=args.out;OUT.mkdir(parents=True,exist_ok=False)
    names=['05_dependency_frontend.py','05_dependency_frontend_check.py','05_portfolio_transport.py','05_counterfactual_transport.py','04_counterfactual_repair.py'];hashes={}
    for n in names:
        b=(HERE/n).read_bytes();(OUT/n).write_bytes(b);hashes[n]=hashlib.sha256(b).hexdigest()
    manifest={'schema':'p305.dependency.development.v1','stage':'DEVELOPMENT','version':D.VERSION,'sources_sha256':hashes,'prepared_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'command':sys.argv,'fixed_targets':['complete Boolean tables arity 0-3','all one-bit table pairs and 16 routing masks','paired loss and withdrawal receiver','twins, renaming, unused malformed definitions, expansion caps'],'review':'Same-model self-review; scalar evaluators and inherited structural comparator, not a separate external reviewer.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');start=time.monotonic_ns();error=None
    try:complete_table_tests();routing_and_binding();dependence_and_renaming();malformed_and_caps();all_routing_maps()
    except Exception:error=traceback.format_exc()
    result={'cases':CASES,'assertions':COUNT,'error':error};raw=(json.dumps(result,indent=2,default=str)+'\n').encode();(OUT/'results.json').write_bytes(raw)
    summary={'status':'FAIL' if error else 'PASS','assertions':COUNT,'suites':len(CASES),'elapsed_ns':time.monotonic_ns()-start,'sources_sha256':hashes,'results_sha256':hashlib.sha256(raw).hexdigest(),'error':error};(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
