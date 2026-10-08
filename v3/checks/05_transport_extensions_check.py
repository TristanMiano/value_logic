#!/usr/bin/env python3
"""Focused DEVELOPMENT supplement: retained envelopes and a counterpossible edit.

Separate fixed cases; does not relabel or rerun the prior complete corpus.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys,time,traceback
from fractions import Fraction as F
from itertools import product
from dataclasses import replace
from datetime import datetime,timezone
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('p305_oracle_helpers',HERE/'05_counterfactual_transport_check.py')
T=importlib.util.module_from_spec(spec);sys.modules[spec.name]=T;spec.loader.exec_module(T)
M,K=T.M,T.K

def cases():
    p,q=K.bit(0),K.bit(1)
    old=T.frame(2,soft=(K.Soft('p',K.neg(p),F(1)),K.Soft('q',K.neg(q),F(2))),d=K.add(K.scale(4,q),K.lit(-1)))
    table=[]
    for h in range(4):
        band=[x for x in product((0,1),repeat=2) if T.rank(old,x)<=h]
        u=max(T.point(old.difference,x) for x in band)
        proof=M.build_band(old,h,u);M.verify_band(proof,old.record());T.check_proof_oracle(proof)
        table.append((h,str(u)))
    T.ok(table==[(0,'-1'),(1,'-1'),(2,'3'),(3,'3')],'Wrong envelope.')
    # Every nonempty restriction; threshold from any feasible witness.
    xs=list(product((0,1),repeat=2));checks=0
    for mask in range(1,16):
        remaining=[x for i,x in enumerate(xs) if mask&(1<<i)]
        winners=[x for x in remaining if T.rank(old,x)==min(T.rank(old,y) for y in remaining)]
        for z in remaining:
            threshold=T.rank(old,z)
            eligible=[F(u) for h,u in table if h>=threshold]
            T.ok(max(T.point(old.difference,y) for y in winners)<=min(eligible),'Envelope failed after a restriction.')
            checks+=1
    # Full paired-label counterpossible. q normality is retained as a hard link.
    tp,fp,tq,fq=[K.bit(i) for i in range(4)]
    normalq=K.eq(K.add(tq,fq),K.lit(1));normalp=K.eq(K.add(tp,fp),K.lit(1))
    base=T.frame(4,hard=(tp,fp,normalq),soft=(K.Soft('normal-p',normalp,F(1)),K.Soft('frame-q',K.neg(tq),F(1))),
                 d=K.add(K.scale(4,tq),K.lit(-1)),scope='paired-hypothetical',meta='{"antecedent":"p and not p","q_normal":true}')
    proof=M.build_band(base,1,-1);M.verify_band(proof,base.record());c=M.CertificateCache();c.admit('genuine',proof,base.record())
    T.ok(T.selected(base)==[(1,1,0,1)],'Old hypothetical is not the declared singleton.')
    dropped=replace(base,request=replace(base.request,soft=base.request.soft[:1],scope='frame-withdrawn'))
    r=c.derive('genuine',base.record(),dropped,tuple(range(4)),(1,1,0,1))
    T.ok(r['status']=='NO_REUSE_CERTIFICATE','Removed q frame was reused.')
    T.ok(set(T.selected(dropped))=={(1,1,0,1),(1,1,1,0)},'Tied hypothetical consequences were lost.')
    T.ok(max(T.point(dropped.difference,x) for x in T.selected(dropped))==3,'Adverse hypothetical was not real in the selected adapter.')
    narrowed=replace(base,request=replace(base.request,hard=base.request.hard+(fq,),scope='hard-q-false'))
    good=c.derive('genuine',base.record(),narrowed,tuple(range(4)),(1,1,0,1))
    T.ok(good['bound']=='-1','Safe hypothetical narrowing was rejected.')
    return {'envelope':table,'restriction_witness_pairs':checks,'counterpossible_old':base.record(),
            'counterpossible_withdrawal':r,'counterpossible_retained_frame':good}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);o=ap.parse_args().out
    o.mkdir(parents=True,exist_ok=False)
    names=['05_transport_extensions_check.py','05_counterfactual_transport_check.py','05_counterfactual_transport.py','04_counterfactual_repair.py']
    sources={}
    for n in names:
        b=(HERE/n).read_bytes();(o/n).write_bytes(b);sources[n]=hashlib.sha256(b).hexdigest()
    (o/'manifest.json').write_text(json.dumps({'status':'PREPARED','type':'DEVELOPMENT', 'sources_sha256':sources,
                'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'command':sys.argv},indent=2)+'\n')
    start=time.perf_counter_ns();data={};err=None
    try:data=cases()
    except Exception:err=traceback.format_exc()
    (o/'results.json').write_text(json.dumps(data,indent=2,default=str)+'\n')
    summary={'status':'FAIL' if err else 'PASS','assertions':T.COUNT,'elapsed_ns':time.perf_counter_ns()-start,'error':err,'sources_sha256':sources}
    (o/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
    if err:raise SystemExit(1)

if __name__=='__main__':main()
