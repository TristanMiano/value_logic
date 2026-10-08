#!/usr/bin/env python3
"""Fresh DEVELOPMENT v2 substitution checks; v1 outputs remain historical."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys,time,traceback
from fractions import Fraction as F
from itertools import product
from datetime import datetime,timezone
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('p305_substitution_oracle',HERE/'05_counterfactual_transport_check.py')
T=importlib.util.module_from_spec(sp);sys.modules[sp.name]=T;sp.loader.exec_module(T);M,K=T.M,T.K

def run():
    p,q=K.bit(0),K.bit(1)
    old=T.frame(2,hard=(K.neg(q),),d=K.add(K.scale(4,q),K.lit(-1)),scope='old-q-false')
    pr=M.build_band(old,0,-1);c=M.CertificateCache();c.admit('proof',pr,old.record())
    current=T.frame(2,d=old.difference,scope='q-premise-withdrawn')
    substitutions=(p,K.lit(0))
    r=c.derive_substituted('proof',old.record(),current,substitutions,(0,0))
    T.ok(r['status']=='REUSE_CERTIFIED' and r['bound']=='3','Explicit withdrawal penalty not charged.')
    T.ok(r['loss_drift_upper']=='4' and not r['non_deterioration'],'Old -1 promoted to current non-deterioration.')
    for x in T.selected(current):T.ok(T.point(current.difference,x)<=F(r['bound']),'Repaired bound false.')
    T.ok(c.derive('proof',old.record(),current,(0,1),(0,0))['status']=='NO_REUSE_CERTIFICATE','Unchanged map wrongly discharges q=0.')
    # A non-bijective map can support a constant old comparison on a larger domain.
    scalar=T.frame(1,d=K.lit(-2),scope='one-bit')
    pc=M.build_band(scalar,0,-2);c.admit('scalar',pc,scalar.record())
    three=T.frame(3,d=K.lit(-1),scope='three-bits')
    for e in [K.bit(0),K.neg(K.bit(1)),K.AND(K.bit(0),K.bit(2)),K.OR(K.bit(1),K.bit(2)),K.lit(1)]:
        z=c.derive_substituted('scalar',scalar.record(),three,(e,),(0,0,0))
        T.ok(z['bound']=='-1','Larger-domain substitution failed.')
    T.reject(lambda:c.derive_substituted('scalar',scalar.record(),three,(K.lit(2),),(0,0,0)))
    T.reject(lambda:c.derive_substituted('scalar',scalar.record(),three,(),(0,0,0)))
    T.reject(lambda:c.derive_substituted('scalar',scalar.record(),three,(K.bit(4),),(0,0,0)),ValueError)
    # Fixed small corpus of nonlinear maps and signed difference shifts.
    source=T.frame(2,d=K.add(p,K.scale(-1,q)),scope='map-source')
    pc=M.build_band(source,0,1);c.admit('map',pc,source.record())
    formulas=[K.bit(0),K.bit(1),K.neg(K.bit(0)),K.AND(K.bit(0),K.bit(1)),K.lit(0),K.lit(1)]
    count=0
    for a,b in product(formulas,repeat=2):
        d=K.add(K.sub(a,b),K.lit(F(1,3)))
        target=T.frame(2,d=d,scope='map-target')
        out=c.derive_substituted('map',source.record(),target,(a,b),(0,0))
        for x in T.selected(target):
            T.ok(T.point(d,x)<=F(out['bound']),'Substitution unsound.')
        count+=1
    return {'withdrawal':r,'nonlinear_map_cases':count}

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);o=a.parse_args().out;o.mkdir(parents=True,exist_ok=False)
    names=['05_substitution_check.py','05_counterfactual_transport_check.py','05_counterfactual_transport.py','04_counterfactual_repair.py'];src={}
    for n in names:
        b=(HERE/n).read_bytes();(o/n).write_bytes(b);src[n]=hashlib.sha256(b).hexdigest()
    (o/'manifest.json').write_text(json.dumps({'type':'DEVELOPMENT','version':M.VERSION,'sources_sha256':src,'utc':datetime.now(timezone.utc).isoformat(),'command':sys.argv},indent=2)+'\n')
    err=None;out={};t=time.perf_counter_ns()
    try:out=run()
    except Exception:err=traceback.format_exc()
    (o/'results.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    summary={'status':'FAIL' if err else 'PASS','assertions':T.COUNT,'elapsed_ns':time.perf_counter_ns()-t,'error':err,'sources_sha256':src}
    (o/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
    if err:raise SystemExit(1)
if __name__=='__main__':main()
