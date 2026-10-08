#!/usr/bin/env python3
"""S2 focused composition check; new evidence, not a missing historical run.

Normality t+f=1 is first translated to Boolean XOR, with pointwise verification.
The general arithmetic grammar is not claimed to compile to CNF automatically.
Run with --output a new directory. Python 3.10+, standard library only.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, platform, sys, time, traceback
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from datetime import datetime, timezone
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('p304_reconstruction_oracle',H/'04_counterfactual_repair_check.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v);k=v.k

def normal_to_bool(e):
    if e[0]=='eq' and e[1][0]=='add' and e[2]==k.lit(1) and all(c[0]=='bit' for c in e[1][1:]):
        return k.neg(k.eq(e[1][1],e[1][2]))
    if e[0] in ('bit','lit'): return e
    if e[0]=='scale': return ('scale',e[1],normal_to_bool(e[2]))
    return (e[0],*(normal_to_bool(x) for x in e[1:]))

def run(out):
    out.mkdir(parents=True,exist_ok=False)
    files=[H/'04_counterfactual_repair.py',H/'04_counterfactual_repair_check.py',Path(__file__).resolve()]
    manifest={'kind':'DEVELOPMENT_RECONSTRUCTION_COMPOSITION','source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
              'command':['python','-B','v3/checks/04_cnf_composition_check.py','--output',str(out)],
              'started_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),
              'historical_S1_evidence_recovered':False}
    for p in files:(out/p.name).write_bytes(p.read_bytes())
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    start=time.monotonic_ns();count=0;requests=0;error=None
    def ck(ok):
        nonlocal count
        count+=1
        if not ok:raise AssertionError('Composition mismatch')
    try:
        p,q=('atom','p'),('atom','q')
        formulas=[p,('not',p),('and',p,('not',p)),('or',p,q),('and',p,q),('bottom',)]
        for formula,baseline,exceptions,frame,center in product(formulas,product((0,1),repeat=2),[(),('p',),('p','q')],[(),('q',)],[False,True]):
            original=k.paired_request(('p','q'),formula,baseline,exceptions,frame=frame,preserve_baseline=center)
            new=k.Request(4,tuple(map(normal_to_bool,original.hard)),tuple(k.Soft(x.identity,normal_to_bool(x.formula),x.weight,x.tier) for x in original.soft),(),original.scope,original.metadata_json)
            compiled=k.compile_cnf(new);scalar=k.scalar_weights(new);ranks={};scalar_ranks={};feasible=[]
            for x in product((0,1),repeat=4):
                for a,b in zip(original.hard,new.hard):ck(v.ev(a,x)==v.ev(b,x))
                for a,b in zip(original.soft,new.soft):ck(v.ev(a.formula,x)==v.ev(b.formula,x))
                ext={i+1:b for i,b in enumerate(x)}
                for y,op,*args in compiled['gates']:
                    if op=='const':ext[y]=args[0]
                    elif op=='not':ext[y]=1-ext[args[0]]
                    elif op=='and':ext[y]=int(all(ext[i] for i in args))
                    elif op=='or':ext[y]=int(any(ext[i] for i in args))
                    elif op=='eq':ext[y]=int(ext[args[0]]==ext[args[1]])
                holds=all(any(ext[abs(z)]==int(z>0) for z in c) for c in compiled['hard_clauses'])
                original_holds=all(v.ev(h,x)==1 for h in original.hard);ck(holds==original_holds)
                rank=[]
                for t in range(new.tiers):
                    rank.append(sum((F(s['weight']) for s in compiled['soft_roots'] if s['tier']==t and ext[s['root']]==0),F(0)))
                    ck(rank[-1]==sum((F(s.weight) for s in original.soft if s.tier==t and v.ev(s.formula,x)==0),F(0)))
                if holds:
                    feasible.append(x);ranks[x]=tuple(rank)
                    scalar_ranks[x]=sum(w for w,s in zip(scalar,new.soft) if not v.ev(s.formula,x))
            ref=v.oracle(original)[1]
            winners={x for x in feasible if ranks[x]==min(ranks.values())} if feasible else set()
            scaled={x for x in feasible if scalar_ranks[x]==min(scalar_ranks.values())} if feasible else set()
            ck(winners==ref==scaled);requests+=1
        # The arithmetic normality input is explicitly rejected before translation.
        r=k.paired_request(('p',),p,(0,),('p',))
        try:k.compile_cnf(r)
        except ValueError:ck(True)
        else:ck(False)
    except Exception:error=traceback.format_exc()
    result={'status':'FAIL' if error else 'PASS','label':'DEVELOPMENT','requests':requests,'assertions':count,
            'elapsed_ns':time.monotonic_ns()-start,'ended_utc':datetime.now(timezone.utc).isoformat(),
            'boundary':'Explicit Boolean normalization only, not a general arithmetic compiler or native proof checker.', 'error':error}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
    if error:raise SystemExit(1)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
