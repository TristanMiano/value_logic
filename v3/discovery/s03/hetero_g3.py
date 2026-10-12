"""Explicit alternate-engine continuation plus ordinary Neyman allocation.

Codex (GPT-6), 2026-10-11. DEVELOPMENT. Original MiniSat22 failure preserved.
The imported constructor alias is intentionally rebound to Glucose3 for every
policy and diagnostic call; no historical source file is edited.
"""
import hashlib,json,math,sys,time,traceback,faulthandler
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
import hetero_service as h
from pysat.solvers import Glucose3
import pysat
h.old.sat.Minisat22=Glucose3


def neyman(spec,forms,target,seed,alpha=F(1,20),deadline_seconds=90):
    begin=time.perf_counter_ns();G=len(spec);ev=h.Evaluator(spec,forms)
    groups=[h.DelayedGroup(s['size']) for s in spec]
    samplers=[h.Sampler(s['size'],seed+101*g) for g,s in enumerate(spec)]
    draws=[];stages=[];lower=[0]*G;next_check=1;warrant=False;profile_ns=selection_ns=0
    def K():return sum(g.positives for g in groups)
    def S():return sum(len(g.trace) for g in groups)
    def expired():return time.perf_counter_ns()-begin>deadline_seconds*1e9
    def acquire(g):
        i=samplers[g].take();z,hint,cost=ev.prove(g,i,None);groups[g].add(i,z)
        draws.append({'group':g,'index':i,'resume':False,'budget':None,'proof':z,
                      'native_hint':'sat' if hint is True else ('negative_unproved' if hint is False else 'unresolved'),'evaluation_ns':cost})
    def check(force=False):
        nonlocal warrant,next_check,profile_ns
        if K()>=target:warrant=True;return
        if not force and S()<next_check:return
        started=time.perf_counter_ns()
        for g,item in enumerate(groups):
            lo,_=h.partial_interval(item.N,len(item.trace),item.positives,0,alpha/G)
            lower[g]=max(lower[g],lo,item.positives)
        warrant=sum(lower)>=target;spent=time.perf_counter_ns()-started;profile_ns+=spent
        stages.append({'samples':S(),'positive_receipts':K(),'warrant':warrant,'group_lower':lower.copy(),'profile_ns':spent})
        next_check=max(S()+1,(S()*1415+999)//1000)
    try:
        for g,s in enumerate(spec):
            for _ in range(min(8,s['size'])):acquire(g)
        check(True)
        while not warrant and any(s.remaining for s in samplers) and not expired():
            started=time.perf_counter_ns();scores=[]
            for g,item in enumerate(groups):
                if not samplers[g].remaining:continue
                s=len(item.trace);p=(item.positives+1)/(s+2);cost=max(1,ev.group_ns[g]/max(1,ev.group_calls[g]))
                scores.append((item.N*math.sqrt(p*(1-p)/cost)/(s+1),g))
            g=max(scores)[1];selection_ns+=time.perf_counter_ns()-started
            for _ in range(min(8,len(samplers[g].remaining))):
                acquire(g);check()
                if warrant or expired() or S()>=next_check:break
        if not warrant:check(True)
        status='warranted' if warrant else ('deadline_abstention' if expired() else 'abstained')
    finally:
        start=time.perf_counter_ns();ev.close();cleanup=time.perf_counter_ns()-start
    lifecycle=time.perf_counter_ns()-begin;start=time.perf_counter_ns();receipts=ev.receipts();export=time.perf_counter_ns()-start
    return {'mode':'strata_neyman','status':status,'target':target,'alpha':str(alpha),'lifecycle_ns':lifecycle,
            'cleanup_ns':cleanup,'receipt_export_ns':export,'profile_ns':profile_ns,'profile_calls':len(stages),
            'selection_ns':selection_ns,'samples':S(),'positive_receipts':K(),'group_samples':[len(g.trace) for g in groups],
            'counts':dict(ev.counts),'group_evaluation_ns':ev.group_ns,'draws':draws,'stages':stages,'receipts':receipts}


def main(out):
    assert not out.exists();journal=out.with_suffix('.jsonl');assert not journal.exists()
    plans=[([256,256],[60,160],[3.8,4.25],F(55,100)),([256,256],[60,220],[3.8,4.25],F(65,100)),
           ([128]*4,[60,100,160,220],[3.8,4.05,4.25,4.35],F(60,100))]
    prior=json.loads(Path(__file__).with_name('hetero01.json').read_text(encoding='utf-8'))
    sources=dict(prior['sources']);sources['s03/hetero_g3.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result={'status':'running','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','start_utc':datetime.now(timezone.utc).isoformat(),
            'engine':'Glucose3','pysat_version':pysat.__version__,'engine_binding':'hetero_service.old.sat.Minisat22 constructor alias rebound to pysat.solvers.Glucose3 in this process',
            'native_dependency_import_ns':h.native_import_ns,'numeric_dependency_import_ns':h.numeric_import_ns,
            'python':sys.version,'sources':sources,'cohorts':[],'timing_scope':prior['timing_scope'],
            'prior_failure':'hetero01_failure.json; this is new developmental execution, not independent confirmation'}
    def save():out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    save()
    try:
        for case,(sizes,ns,ratios,fraction) in enumerate(plans):
            started=time.perf_counter_ns();rng=h.random.Random(93040+case)
            spec=[{'size':N,'variables':n,'clauses':round(n*r)} for N,n,r in zip(sizes,ns,ratios)]
            forms=[[h.old.sat.formula(s['variables'],s['clauses'],rng) for _ in range(s['size'])] for s in spec]
            source=hashlib.sha256(json.dumps({'spec':spec,'forms':forms,'unit':1},separators=(',',':')).encode()).hexdigest()
            if case<len(prior['cohorts']):assert source==prior['cohorts'][case]['source']
            target=(sum(sizes)*fraction.numerator+fraction.denominator-1)//fraction.denominator
            cohort={'case':case,'seed':93040+case,'spec':spec,'source':source,'target':target,'input_generation_binding_ns':time.perf_counter_ns()-started,'arms':[]}
            result['cohorts'].append(cohort);save()
            for mode in ('exact_cost','direct_uniform','strata_cost','strata_neyman','joint_cost','joint_bounded'):
                event={'event':'arm_start','case':case,'mode':mode,'utc':datetime.now(timezone.utc).isoformat()};h.append(journal,event);print(json.dumps(event),flush=True)
                arm=neyman(spec,forms,target,94000+case) if mode=='strata_neyman' else h.policy(spec,forms,target,mode,94000+case)
                cohort['arms'].append(arm);save();h.append(journal,{'event':'arm_complete','case':case,'mode':mode,'status':arm['status'],'lifecycle_ns':arm['lifecycle_ns']})
                print(json.dumps({k:arm[k] for k in ('mode','status','lifecycle_ns','samples','positive_receipts','profile_calls')}),flush=True)
            started=time.perf_counter_ns();truth=[]
            for g,s in enumerate(spec):
                ys=[]
                for clauses in forms[g]:
                    solver=Glucose3(bootstrap_with=clauses);answer=solver.solve(assumptions=[1])
                    if answer:assert h.old.check_model(s['variables'],clauses,solver.get_model(),1) is not None
                    ys.append(int(answer));solver.delete()
                truth.append(ys)
            cohort['reference']={'truth':truth,'total':sum(map(sum,truth)),'elapsed_ns':time.perf_counter_ns()-started,'negative_scope':'trusted native diagnostic, not service evidence'}
            for arm in cohort['arms']:arm['realized_warrant_correct']=None if arm['status']!='warranted' else sum(map(sum,truth))>=target
            save()
        result['status']='complete'
    except Exception:result.update(status='failed',failure=traceback.format_exc());raise
    finally:
        result['end_utc']=datetime.now(timezone.utc).isoformat();save();print(json.dumps({'status':result['status'],'cohorts':len(result['cohorts'])}),flush=True)


if __name__=='__main__':faulthandler.enable();main(Path(sys.argv[1]))
