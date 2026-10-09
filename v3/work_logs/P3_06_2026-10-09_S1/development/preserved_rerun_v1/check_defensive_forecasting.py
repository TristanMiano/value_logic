"""New development diagnostics; neither old-run recovery nor final evaluation."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, platform, time, traceback
from defensive_forecasting import Forecaster, DelayedPool, squared_norm


def run():
    assertions=0
    def check(b,msg):
        nonlocal assertions
        assertions+=1
        if not b: raise AssertionError(msg)
    names=('zero','one','previous')
    cases=[]
    for outcomes in product((0,1),repeat=5):
        f=Forecaster(names,bins=3)
        trace=[]
        for t,y in enumerate(outcomes):
            q={'zero':0,'one':1,'previous':outcomes[t-1] if t else F(1,2)}
            w=(F(1),F(3),F(1,2))[t%3]
            pred=f.issue(str(t),q,w,tolerance=F(1,128),max_bisections=24)
            check(not f.history or f.history[-1][0].query != str(t),'No future outcome in history.')
            before=f.own_loss
            check(f.pending is pred and before==sum((p.weight*(p.probability-z)**2 for p,z in f.history),F(0)),
                  'Pending predictions must not be scored.')
            f.reveal(str(t),y)
            check(squared_norm(f.residual)<=f.variance+f.allowance,'Potential certificate.')
            for i in range(len(names)):
                d=f.own_loss-f.expert_losses[i]
                check(d==2*f.residual[i]/f.alpha-f.expert_distances[i],'Regret identity.')
                check(d<=0 or d*d<=4*(f.variance+f.allowance),'Regret norm bound.')
            trace.append({'p':str(pred.probability),'y':y,'weight':str(w),
                          'allowance':str(pred.allowance),'tolerance_met':pred.tolerance_met})
        cases.append({'outcomes':outcomes,'trace':trace,'own_loss':str(f.own_loss),
                      'expert_losses':list(map(str,f.expert_losses))})
    # Zero root work must retain its actual approximation allowance.
    f=Forecaster(('zero','quarter'),bins=2)
    for t,y in enumerate((1,0,0,1,1,0,1,0)):
        p=f.issue('budget-'+str(t),{'zero':0,'quarter':F(1,4)},max_bisections=0)
        check(p.bisections==0,'Explicit root budget.')
        f.reveal(p.query,y)
        check(squared_norm(f.residual)<=f.variance+f.allowance,'Budgeted bound with allowance.')
    # Delayed labels arrive out of issuance order; outstanding entries stay unscored.
    pool=DelayedPool(('zero','one'),bins=2)
    saved={}
    for t in range(18):
        query='delay-'+str(t)
        saved[query]=pool.issue(query,{'zero':0,'one':1},weight=1+t%3)
        if t>=2 and t%3==2:
            for j in (t-1,t-2):
                old='delay-'+str(j)
                returned=pool.reveal(old,j%2)
                check(returned is saved[old],'Original forecast preserved.')
        report=pool.audit()
        check(report['pending']==len(pool.pending),'Pending coverage count.')
        check(report['settled']+report['pending']==t+1,'No imaginary feedback.')
    for query in list(pool.pending):
        t=int(query.split('-')[-1]);pool.reveal(query,t%2);pool.audit()
    check(pool.audit()['settled']==18,'All eventual labels counted once.')
    # Zero weights leave weighted statistics untouched, without assigning an outcome.
    f=Forecaster(('zero','one'))
    p=f.issue('zero-weight',{'zero':0,'one':1},weight=0)
    f.reveal(p.query,1)
    check(f.own_loss==0 and squared_norm(f.residual)==0,'Zero weight semantics.')
    # Input and identity rejection, and transactional retention of pending prediction.
    f=Forecaster(('zero','one'))
    p=f.issue('id',{'zero':0,'one':1})
    for call in (lambda:f.reveal('other',0), lambda:f.reveal('id',None),
                 lambda:f.issue('new',{'zero':0,'one':1})):
        rejected=False
        try:call()
        except ValueError:rejected=True
        check(rejected and f.pending is p,'Bad feedback cannot destroy pending state.')
    f.reveal('id',0)
    rejected=False
    try:f.reveal('id',0)
    except ValueError:rejected=True
    check(rejected,'Duplicate outcome rejected.')
    # Descriptive finite behavior, not a universal finite-horizon success claim.
    f=Forecaster(('zero','one'),bins=4)
    trajectory=[]
    for t in range(64):
        p=f.issue('all-zero-'+str(t),{'zero':0,'one':1},max_bisections=32)
        trajectory.append(str(p.probability));f.reveal(p.query,0)
    return {'status':'PASS','assertions':assertions,'binary_sequence_cases':len(cases),
            'cases':cases,'delayed_audit':pool.audit(),
            'all_zero_trajectory':trajectory,'all_zero_weighted_loss':str(f.own_loss),
            'scope':'New finite development checks, not prior evidence recovery or independent review.'}

if __name__=='__main__':
    start=time.monotonic_ns();utc=datetime.now(timezone.utc).isoformat()
    root=Path(__file__).resolve().parent
    try:result=run()
    except Exception:
        result={'status':'FAIL','traceback':traceback.format_exc()}
    result.update(start_utc=utc,end_utc=datetime.now(timezone.utc).isoformat(),
                  execution_ns=time.monotonic_ns()-start,python=platform.python_version(),
                  contributor='ChatGPT (GPT-6 Astra Pro)',
                  research_time_credit_ns=0,
                  source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in root.glob('*.py')})
    target=root/'development_result.json'
    if target.exists():
        raise SystemExit('Refusing to overwrite an existing development result.')
    target.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'assertions':result.get('assertions'),
                      'result':str(target)}))
    raise SystemExit(0 if result['status']=='PASS' else 1)
