#!/usr/bin/env python3
"""DEVELOPMENT: current clauses and correlated rank conditions in portfolio-v2."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from dataclasses import replace
from itertools import product
import argparse,hashlib,importlib.util,json,sys,time,traceback
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_p305_clause_oracle',HERE/'05_portfolio_check.py')
T=importlib.util.module_from_spec(sp);sys.modules[sp.name]=T;sp.loader.exec_module(T)
P,M,K=T.P,T.M,T.K
ROWS=[]

def run():
    p,q,r=K.bit(0),K.bit(1),K.bit(2)
    # A relationship between soft Boolean formulas makes separate drift overly loose.
    old=T.frame(1,soft=(K.Soft('p',p,F(1)),K.Soft('not-p',K.neg(p),F(1))),d=K.lit(-1),scope='rank-complement')
    new=T.frame(1,d=K.lit(-1),scope='unranked')
    bp=M.build_band(old,1,-1);prior=M.CertificateCache();prior.admit('old',bp,old.record())
    old_result=prior.derive('old',old.record(),new,(0,),(0,))
    T.ok(old_result['status']=='NO_REUSE_CERTIFICATE','Independent drift test should be loose here.')
    cache=P.PortfolioCache();cache.admit_band('old',bp,old.record())
    proof=cache.build(new,(T.choice('old',old),),(0,),-1,allow_direct=False)
    report,_=T.audit(cache,proof,new)
    T.ok(report['counts']['splits']==0,'Complementary ranks should cancel without splitting.')
    ROWS.append({'case':'complementary_rank','old':old.record(),'current':new.record(),'prior_report':old_result,
                 'proof':proof.record(),'report':report})
    # Hard p -> q bounds p+1-q by 1. Linear clause extraction is essential.
    hard=K.OR(K.neg(p),q)
    old=T.frame(2,soft=(K.Soft('not-p',K.neg(p),F(1)),K.Soft('q',q,F(1))),d=K.lit(-2),scope='old-rank-p-not-q')
    bp=M.build_band(old,1,-2);cache.admit_band('implication',bp,old.record())
    new=T.frame(2,hard=(hard,),d=K.lit(-2),scope='conditional-rank')
    proof=cache.build(new,(T.choice('implication',old),),(0,0),-2,allow_direct=False)
    report,_=T.audit(cache,proof,new)
    T.ok(report['counts']['splits']==0,'Clause inequality should establish the rank band at the root.')
    T.ok(set(T.worlds(new))=={(0,0),(0,1),(1,1)},'Implication fixture wrong.')
    # A rank band should not be silently enlarged after dropping that implication.
    unconstrained=T.frame(2,d=K.lit(-2),scope='implication-withdrawn')
    failed=T.reject(lambda:cache.build(unconstrained,(T.choice('implication',old),),(0,0),-2,allow_direct=False),P.Uncertified)
    direct=cache.build(unconstrained,(),(0,0),-2,allow_direct=True);T.audit(cache,direct,unconstrained)
    ROWS.append({'case':'conditional_rank_from_implication','old':old.record(),'current':new.record(),
                 'proof':proof.record(),'report':report,'withdrawal_rejection':failed,
                 'direct_fallback':direct.record()})
    # Check every generated inequality against a separate point evaluator.
    leaves=[p,q,r,K.neg(p),K.neg(q),K.neg(r),K.lit(0),K.lit(1)]
    formulas=[K.OR(a,b) for a,b in product(leaves,repeat=2)]
    formulas += [K.neg(K.AND(a,b)) for a,b in product(leaves,repeat=2)]
    formulas += [K.AND(K.OR(p,q),K.OR(K.neg(p),r)),K.OR(K.AND(p,q),K.eq(q,r))]
    cases=[]
    for i,h in enumerate(formulas):
        f=T.frame(3,hard=(h,),scope=f'clause-{i}')
        xs=T.worlds(f); derived=P.clause_inequalities(h)
        for e in derived:
            for x in xs:T.ok(T.point(e,x)<=0,'Generated clause row is not a consequence of the hard formula.')
        if xs:
            rows=P.context_rows(f,(None,)*3,0)
            for j in rows.one_sided_indices:
                for x in xs:T.ok(T.point(rows.expressions[j],x)<=0,'One-sided context row false at a relevant point.')
        cases.append({'hard':h,'rows':derived,'feasible_points':xs})
    ROWS.append({'case':'row_semantics_exhaustion','cases':cases})
    # Positive coefficients, including nonintegral multipliers; no sign heuristic is trusted.
    for numerator in (-5,-2,1,3,7):
        coefficient=F(numerator,3)
        if coefficient<=0: continue
        f=T.frame(2,hard=(hard,),scope='rational-clause')
        rows=P.context_rows(f,(None,None),0)
        target=K.add(K.scale(coefficient,K.sub(p,q)),K.lit(F(2,7)))
        w=P.best_witness(target,F(2,7),rows,(None,None))
        T.ok(w is not None,'Valid rational conic certificate not found.')
        u=P.conditional_upper(target,w,rows,(None,None))
        T.ok(u<=F(2,7),'Positive rational side certificate failed.')
        for x in T.worlds(f):T.ok(T.point(target,x)<=u,'Rational conditional upper bound is false.')
        ROWS.append({'case':'rational_clause','coefficient':str(coefficient),'target':target,'weights':w,'upper':str(u)})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);o=ap.parse_args().out;o.mkdir(parents=True,exist_ok=False)
    names=['05_clause_transport_check.py','05_portfolio_check.py','05_portfolio_transport.py','05_counterfactual_transport.py','04_counterfactual_repair.py']
    hashes={}
    for n in names:
        b=(HERE/n).read_bytes();(o/n).write_bytes(b);hashes[n]=hashlib.sha256(b).hexdigest()
    (o/'manifest.json').write_text(json.dumps({'status':'PREPARED','evidence_type':'DEVELOPMENT','version':P.VERSION,
               'sources_sha256':hashes,'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'command':sys.argv,
               'purpose':'Current clause consequences, related ranking formulas, rational certificate signs and withdrawal.'},indent=2)+'\n')
    t=time.monotonic_ns();error=None
    try:run()
    except Exception:error=traceback.format_exc()
    raw=(json.dumps({'cases':ROWS,'error':error},indent=2,default=str)+'\n').encode();(o/'results.json').write_bytes(raw)
    summary={'status':'FAIL' if error else 'PASS','assertions':T.COUNT,'cases_recorded':len(ROWS),
             'elapsed_ns':time.monotonic_ns()-t,'error':error,'sources_sha256':hashes,'results_sha256':hashlib.sha256(raw).hexdigest()}
    (o/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
