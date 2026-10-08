#!/usr/bin/env python3
"""DEVELOPMENT ADD validation and fixed matched-resource diagnostics.

No post hoc choice of only favorable families. Every complete unit is saved.
Times are local observations; heterogeneous counters are not silently summed.
"""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime,timezone
from fractions import Fraction as F
from itertools import permutations,product
from pathlib import Path
import argparse,hashlib,importlib.util,json,platform,sys,time,traceback
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def load(name,file):
    sp=importlib.util.spec_from_file_location(name,HERE/file);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
D=load('_p305_resource_dependency','05_dependency_frontend.py');P,M,K=D.P,D.M,D.K
A=load('_p305_resource_add','05_ordinary_add.py')
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
    raise AssertionError('Invalid input accepted.')


def save(v):
    CASES.append(v)
    if OUT:
        with (OUT/'completed_units.jsonl').open('a') as f:f.write(json.dumps({'assertions':COUNT,'case':v},default=str)+'\n');f.flush()


def point(e,x):
    op=e[0]
    if op=='lit':return F(e[1])
    if op=='bit':return F(x[e[1]])
    if op=='not':return 1-point(e[1],x)
    if op=='scale':return F(e[1])*point(e[2],x)
    a,b=point(e[1],x),point(e[2],x)
    if op=='add':return a+b
    if op=='min':return min(a,b)
    if op=='max':return max(a,b)
    if op=='eq':return F(a==b)
    if op=='and':return F(a==1 and b==1)
    if op=='or':return F(a==1 or b==1)
    raise ValueError('Reference grammar.')


def fold(op,es,identity):
    if not es:return identity
    if len(es)==1:return es[0]
    i=len(es)//2;return op(fold(op,es[:i],identity),fold(op,es[i:],identity))


def characteristic(n,mask):
    terms=[]
    for j,x in enumerate(product((0,1),repeat=n)):
        if mask>>j&1:terms.append(fold(K.AND,[K.bit(i) if b else K.neg(K.bit(i)) for i,b in enumerate(x)],K.lit(1)))
    return fold(K.OR,terms,K.lit(0))


def frame(n,d,hard=(),soft=(),scope='request'):
    return M.Frame(K.Request(n,tuple(hard),tuple(soft),(('D',d),),scope),'D','U')


def scalar_range(f,witness,work=None):
    cutoff=sum(s.weight*(1-point(s.formula,witness)) for s in f.request.soft)
    xs=[]
    for x in product((0,1),repeat=f.request.nbits):
        if work is not None:work['enumerated_assignments']=work.get('enumerated_assignments',0)+1
        if all(point(h,x)==1 for h in f.request.hard):
            if sum(s.weight*(1-point(s.formula,x)) for s in f.request.soft)<=cutoff:xs.append(x)
    values=[point(f.difference,x) for x in xs]
    return min(values),max(values),xs


def add_validation():
    n=3;cases=0
    for order in permutations(range(n)):
        manager=A.Manager(n,order)
        for mask in range(256):
            e=characteristic(n,mask);root=manager.compile(e);expanded=K.OR(K.AND(e,K.bit(0)),K.AND(e,K.neg(K.bit(0))))
            ok(manager.compile(expanded)==root,'Canonical Shannon expansion differs.')
            for j,x in enumerate(product((0,1),repeat=n)):
                ok(manager.evaluate(root,x)==((mask>>j)&1),'ADD truth table differs.')
            cases+=1
    save({'suite':'complete_three_bit_functions_all_variable_orders','function_order_pairs':cases,'reference':'direct mask bits, with canonical Shannon expansion equality'})
    p,q,r=(K.bit(i) for i in range(3));exprs=[K.sub(p,q),('max',K.scale(-3,p),K.scale(F(2,3),q)),('min',K.sub(p,r),K.sub(q,p)),K.eq(K.add(p,q),K.lit(1)),K.scale(F(-7,5),K.OR(p,q))]
    count=0;manager=A.Manager(3)
    for mask in range(1,256):
        hard=characteristic(3,mask);witness=next(x for j,x in enumerate(product((0,1),repeat=3)) if mask>>j&1)
        d=exprs[mask%len(exprs)];f=frame(3,d,(hard,),(K.Soft('p',K.neg(p),F(2)),K.Soft('q',q,F(3)),K.Soft('r',r,F(1))),scope='v-'+str(mask))
        got=manager.query(f,witness,f.record());lo,hi,xs=scalar_range(f,witness)
        ok((F(got['lower']),F(got['upper']))==(lo,hi),'ADD restricted extrema differ.')
        ok(got['lower_witness'] in xs and got['upper_witness'] in xs,'Infeasible endpoint witness.')
        ok(point(d,got['lower_witness'])==lo and point(d,got['upper_witness'])==hi,'Endpoint values not attained.')
        count+=1
    save({'suite':'all_nonempty_three_bit_sources_with_correlated_rank','sources':count,'final_storage':manager.storage()})
    m=A.Manager(1);zero=m.terminal(0);two=m.terminal(2);bit=m.compile(K.bit(0));f=frame(1,K.bit(0),scope='scope')
    errors=[reject(lambda:m.apply('and',two,two)),reject(lambda:m.extrema(two,bit)),reject(lambda:m.node(0,bit,zero)),reject(lambda:m.evaluate(bit,(True,))),reject(lambda:m.query(f,(0,),'different')),reject(lambda:m.compile(K.scale(0,K.bit(2))))]
    ok(m.extrema(zero,bit) is None,'Empty source became a value bound.')
    save({'suite':'ADD_type_and_nonvacuity_guards','rejections':errors})


def parity(indices):
    x=K.bit(indices[0])
    for i in indices[1:]:x=K.neg(K.eq(x,K.bit(i)))
    return x


def benchmark_family(name,old,old_witness,old_bound,edits,*,replacement=None):
    """All edits are supplied explicitly before this family's executions."""
    cache=P.PortfolioCache();build0={};t=time.monotonic_ns();band=M.build_band(old,M.rank_bounds(old,old_witness)[0],F(old_bound),build0);build_ns=time.monotonic_ns()-t
    admit0={};t=time.monotonic_ns();cache.admit_band('old',band,old.record(),admit0);admit_ns=time.monotonic_ns()-t
    warm=A.Manager(old.request.nbits);warm0={};t=time.monotonic_ns();warm.query(old,old_witness,old.record(),warm0);warm_ns=time.monotonic_ns()-t
    proof_bytes=len(M.canonical(band.record()).encode());results=[]
    for j,(current,witness,bound) in enumerate(edits):
        mapping=tuple(K.bit(i) for i in range(old.request.nbits)) if replacement is None else replacement
        ch=(P.Choice('old',old.record(),mapping),)
        rw={};t=time.monotonic_ns();proof=cache.build(current,ch,witness,bound,work=rw);generation_ns=time.monotonic_ns()-t
        rc={};t=time.monotonic_ns();report=cache.verify(proof,current,current.record(),rc);verification_ns=time.monotonic_ns()-t
        fw={};t=time.monotonic_ns();fresh=P.PortfolioCache();fp=fresh.build(current,(),witness,bound,work=fw);fresh_generation_ns=time.monotonic_ns()-t
        fc={};t=time.monotonic_ns();fresh.verify(fp,current,current.record(),fc);fresh_check_ns=time.monotonic_ns()-t
        cw={};cold=A.Manager(current.request.nbits);t=time.monotonic_ns();cr=cold.query(current,witness,current.record(),cw);cold_ns=time.monotonic_ns()-t
        ww={};t=time.monotonic_ns();wr=warm.query(current,witness,current.record(),ww);warm_query_ns=time.monotonic_ns()-t
        truthwork={};lo,hi,xs=scalar_range(current,witness,truthwork)
        ok(F(cr['upper'])==F(wr['upper'])==hi<=F(report['bound']), 'Methods disagree on receiving sublevel.')
        results.append({'edit_index':j,'current_record':current.record(),'witness':witness,'requested_bound':str(bound),'exact_range':[str(lo),str(hi)],'current_source_count':len(xs),
            'reuse':{'generation_ns':generation_ns,'verification_ns':verification_ns,'generation_work':rw,'verification_work':rc,'report':report,'proof_bytes':len(M.canonical(proof.record()).encode())},
            'fresh_certificate':{'generation_ns':fresh_generation_ns,'verification_ns':fresh_check_ns,'generation_work':fw,'verification_work':fc,'proof_bytes':len(M.canonical(fp.record()).encode())},
            'cold_ADD':{'elapsed_ns':cold_ns,'work':cw,'storage':cold.storage()},'warm_ADD':{'elapsed_ns':warm_query_ns,'work':ww,'storage':warm.storage()},'independent_reference_work':truthwork})
        if OUT:
            with (OUT/'benchmark_units.jsonl').open('a') as f:f.write(json.dumps({'family':name,'unit':results[-1]},default=str)+'\n');f.flush()
    return {'suite':'matched_resource_family','name':name,'old_record':old.record(),'initial_costs':{'old_certificate_generation_ns':build_ns,'old_certificate_generation_work':build0,'old_certificate_admission_ns':admit_ns,'old_certificate_admission_work':admit0,'old_certificate_bytes':proof_bytes,'warm_ADD_initial_ns':warm_ns,'warm_ADD_initial_work':warm0},'edits':results,'scope':'Raw costs for these routines and cases; no universal performance result or independent statistical experiment.'}


def fixed_benchmarks():
    old=frame(3,K.lit(-1),scope='constant-old');eds=[]
    for j in range(8):
        bit=j%3;val=j%2;hard=(K.bit(bit) if val else K.neg(K.bit(bit)),);w=tuple(val if i==bit else 0 for i in range(3))
        eds.append((frame(3,old.difference,hard,scope='constant-edit-'+str(j)),w,-1))
    save(benchmark_family('constant_loss_overhead',old,(0,0,0),-1,eds))
    for n in (3,5,7):
        d=K.sub(parity(tuple(range(n))),parity(tuple(reversed(range(n)))))
        old=frame(n,d,scope='parity-old-'+str(n));eds=[]
        for j in range(6):
            bit=j%n;val=j%2;hard=(K.bit(bit) if val else K.neg(K.bit(bit)),);w=tuple(val if i==bit else 0 for i in range(n))
            # Changes in soft priorities are included, not just different labels.
            ss=(K.Soft('priority',K.bit((bit+1)%n),F(j+1)),)
            eds.append((frame(n,d,hard,ss,scope='parity-edit-'+str(n)+'-'+str(j)),w,0))
        save(benchmark_family('associated_parity_'+str(n),old,(0,)*n,0,eds))
    p,q=(K.bit(i) for i in range(2));rank=(K.Soft('p',K.neg(p),F(1)),K.Soft('q',K.neg(q),F(2)))
    old=frame(2,K.add(K.scale(4,q),K.lit(-1)),(),rank,scope='turnover-old')
    # The old incumbent 10 intentionally certifies a wider band, not just 00.
    eds=[(frame(2,old.difference,(p,),rank,scope='turnover-new'),(1,0),-1),
         (frame(2,K.add(old.difference,K.lit(F(1,2))),(p,),rank,scope='turnover-loss-price'),(1,0),F(-1,2))]
    save(benchmark_family('optimizer_turnover',old,(1,0),-1,eds))
    old=frame(1,K.add(K.scale(2,K.bit(0)),K.lit(-1)),(K.neg(K.bit(0)),),scope='withdraw-old')
    eds=[(frame(1,old.difference,scope='withdraw-'+str(i)),(0,),1) for i in range(4)]
    save(benchmark_family('withdrawal_penalty',old,(0,),-1,eds,replacement=(K.lit(0),)))


def main():
    global OUT
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);args=ap.parse_args();OUT=args.out;OUT.mkdir(parents=True,exist_ok=False)
    names=['05_ordinary_add.py','05_resource_comparison_check.py','05_dependency_frontend.py','05_portfolio_transport.py','05_counterfactual_transport.py','04_counterfactual_repair.py'];hs={}
    for name in names:
        b=(HERE/name).read_bytes();(OUT/name).write_bytes(b);hs[name]=hashlib.sha256(b).hexdigest()
    manifest={'schema':'p305.ordinary_resource.development.v1','stage':'DEVELOPMENT','prepared_utc':datetime.now(timezone.utc).isoformat(),'sources_sha256':hs,'versions':{'ADD':A.VERSION,'portfolio':P.VERSION},'python':sys.version,'platform':platform.platform(),'command':sys.argv,'fixed_corpora':['1536 Boolean function/order pairs','255 nonempty source/rank cases','constant overhead','parity n=3,5,7, six edits each','optimizer turnover','withdrawal penalty'],'cost_scope':'One local timed execution per declared unit; all operation vectors saved, no unpriced heterogeneous sum. Old setup and cache retention separate. Shared supplied witnesses; acquisition not measured.','output_binding':'Same incumbent-sublevel service; diagrams are a trusted algorithm rather than portable independent proof objects.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');start=time.monotonic_ns();error=None
    try:add_validation();fixed_benchmarks()
    except Exception:error=traceback.format_exc()
    raw=(json.dumps({'assertions':COUNT,'cases':CASES,'error':error},indent=2,default=str)+'\n').encode();(OUT/'results.json').write_bytes(raw)
    result={'status':'FAIL' if error else 'PASS','assertions':COUNT,'suites':len(CASES),'elapsed_ns':time.monotonic_ns()-start,'sources_sha256':hs,'results_sha256':hashlib.sha256(raw).hexdigest(),'error':error};(OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
