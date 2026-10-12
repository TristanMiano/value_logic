"""Complete-cost heterogeneous positive-proof value service. DEVELOPMENT.

Codex (GPT-6), 2026-10-11. Every coordinate is SAT(F and variable 1).
Native negative answers are scheduling hints only. See service_plan.md.
"""
import time
import_start=time.perf_counter_ns()
import hashlib,json,math,os,random,sys,traceback,faulthandler
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'s02'))
if os.environ.get('VL_SAT_DEPS'):sys.path.insert(0,os.environ['VL_SAT_DEPS'])
import proof_values as old
from censored_count import partial_interval
native_import_ns=time.perf_counter_ns()-import_start
numeric_start=time.perf_counter_ns()
from bets_float import numerical_profile
from delayed_bets import DelayedGroup
numeric_import_ns=time.perf_counter_ns()-numeric_start


class Sampler:
    def __init__(self,N,seed):self.remaining=list(range(N));self.rng=random.Random(seed)
    def take(self):
        j=self.rng.randrange(len(self.remaining));i=self.remaining[j]
        self.remaining[j]=self.remaining[-1];self.remaining.pop();return i


class Evaluator:
    def __init__(self,spec,forms):
        self.spec,self.forms=spec,forms;self.solvers={};self.models={};self.hints={}
        self.counts=Counter();self.group_ns=[0]*len(spec);self.group_calls=[0]*len(spec)

    def prove(self,g,i,budget):
        started=time.perf_counter_ns();key=(g,i)
        if key in self.models:return 1,True,0
        if key not in self.solvers:
            self.solvers[key]=old.sat.Minisat22(bootstrap_with=self.forms[g][i]);self.counts['native_builds']+=1
        solver=self.solvers[key]
        if budget is None:answer=solver.solve(assumptions=[1])
        else:
            solver.conf_budget(budget);answer=solver.solve_limited(assumptions=[1])
            self.counts['requested_conflict_budget']+=budget
        self.counts['native_calls']+=1;self.group_calls[g]+=1
        checked=old.check_model(self.spec[g]['variables'],self.forms[g][i],solver.get_model(),1) if answer is True else None
        if checked is not None:
            self.models[key]=checked;self.counts['checked_positive_receipts']+=1
        elif answer is True:self.counts['rejected_positive_proposals']+=1
        else:self.counts['unsupported_negative_hints' if answer is False else 'unresolved_returns']+=1
        self.hints[key]=answer
        elapsed=time.perf_counter_ns()-started;self.group_ns[g]+=elapsed
        return int(checked is not None),answer,elapsed

    def close(self):
        for solver in self.solvers.values():solver.delete()

    def receipts(self):
        return [{'group':g,'index':i,'positive_bits':hex(sum(1<<(v-1) for v in model if v>0))} for (g,i),model in sorted(self.models.items())]


def group_gain(group,m,p):
    if m<group.positives:return float('inf')
    R=group.N-len(group.trace)
    if not R:return -float('inf')
    mu=min(1.0,(m-group.positives)/R);logs=[]
    for eta_q in group.etas:
        eta=float(eta_q);val=group.positives*math.log1p(eta)
        for remaining,k,_ in group.trace:val-=math.log1p(eta*min(1.0,(m-k)/remaining))
        logs.append(val)
    scale=max(logs);ws=[math.exp(x-scale) for x in logs];den=sum(ws)
    f0=sum(w/(1+float(eta)*mu) for w,eta in zip(ws,group.etas))/den
    f1=sum(w*(1+float(eta))/(1+float(eta)*mu) for w,eta in zip(ws,group.etas))/den
    return p*math.log(f1)+(1-p)*math.log(f0)


def policy(spec,forms,target,mode,seed,alpha=F(1,20),deadline_seconds=90):
    begin=time.perf_counter_ns();G=len(spec);sizes=[s['size'] for s in spec];N=sum(sizes)
    ev=Evaluator(spec,forms);etas=(F(0),F(1,4),F(1),F(4))
    groups=[DelayedGroup(n,etas) for n in sizes]
    samplers=[Sampler(n,seed+101*g) for g,n in enumerate(sizes)]
    flat=[(g,i) for g,n in enumerate(sizes) for i in range(n)];uniform=Sampler(N,seed+9101)
    draws=[];stages=[];lower=[0]*G;allocation=None;profile_calls=0;profile_ns=0;selection_ns=0
    next_check=1;warranted=False;status='exhausted';budget=64 if mode=='joint_bounded' else None

    def count():return sum(g.positives for g in groups)
    def sampled():return sum(len(g.trace) for g in groups)
    def timed_out():return time.perf_counter_ns()-begin>deadline_seconds*1e9

    def acquire(g,i,limit,resume=False):
        proved,hint,elapsed=ev.prove(g,i,limit)
        if resume:
            if proved:groups[g].accept(i)
        else:groups[g].add(i,proved)
        draws.append({'group':g,'index':i,'resume':resume,'budget':limit,'proof':proved,
                      'native_hint':'sat' if hint is True else ('negative_unproved' if hint is False else 'unresolved'),
                      'evaluation_ns':elapsed})

    def check(force=False):
        nonlocal warranted,next_check,allocation,profile_calls,profile_ns
        K=count();S=sampled()
        if K>=target:warranted=True;return
        if mode=='exact_cost':return
        if not force and S<next_check:return
        started=time.perf_counter_ns();details={}
        if mode=='direct_uniform':
            warranted=old.mixed.reject(N,S,K,target-1,alpha,Counter())
        elif mode=='strata_cost':
            for g,item in enumerate(groups):
                lo,_=partial_interval(item.N,len(item.trace),item.positives,0,alpha/G)
                lower[g]=max(lower[g],lo,item.positives)
            warranted=sum(lower)>=target;details['group_lower']=lower.copy()
        else:
            got=numerical_profile(groups,target-1,stop_below=1/alpha)
            warranted=got['status']=='hard_refutation' or got['status']=='optimal' and got['value']>=1/alpha
            allocation=got['allocation'];details={'profile_status':got['status'],'allocation':allocation,
                'value':None if got['value'] is None else str(got['value']),'exchanges':got['exchanges'],'numerical':got.get('numerical')}
        spent=time.perf_counter_ns()-started;profile_ns+=spent;profile_calls+=1
        stages.append({'samples':S,'positive_receipts':K,'warrant':warranted,'profile_ns':spent,**details})
        next_check=max(S+1,(S*1415+999)//1000)

    def choose():
        nonlocal selection_ns
        started=time.perf_counter_ns();available=[g for g in range(G) if samplers[g].remaining];scores=[]
        for g in available:
            item=groups[g];s=len(item.trace);p=(item.positives+1)/(s+2)
            cost=max(1,ev.group_ns[g]/max(1,ev.group_calls[g]))
            score=p/cost
            if mode=='strata_cost':
                b=min(8,item.N-s);k=min(s+b,item.positives+round(b*p))
                proposed=partial_interval(item.N,s+b,k,0,alpha/G)[0]
                score=max(0,proposed-lower[g])/(b*cost)
            elif mode.startswith('joint') and allocation is not None:
                score=group_gain(item,allocation[g],p)/cost
            scores.append((score,g,p/cost))
        best=max(scores)
        if best[0]<=0:best=max(scores,key=lambda x:(x[2],-x[1]))
        selection_ns+=time.perf_counter_ns()-started
        return best[1]

    try:
        if mode!='direct_uniform':
            for g in range(G):
                for _ in range(min(8,sizes[g])):acquire(g,samplers[g].take(),budget)
            check(True)
        while not warranted and sampled()<N and not timed_out():
            if mode=='direct_uniform':
                g,i=flat[uniform.take()];acquire(g,i,budget);check()
            else:
                if allocation is not None and any(item.positives>m for item,m in zip(groups,allocation)):check(True)
                if warranted:break
                g=choose()
                for _ in range(min(8,len(samplers[g].remaining))):
                    acquire(g,samplers[g].take(),budget);check()
                    if warranted or timed_out() or sampled()>=next_check:break
        if not warranted:check(True)
        if mode=='joint_bounded' and not warranted and not timed_out():
            for limit in (256,None):
                pending=[(g,i) for g,item in enumerate(groups) for i in item.identities if (g,i) not in ev.models and ev.hints[(g,i)] is None]
                pending.sort(key=lambda pair:(ev.group_ns[pair[0]]/max(1,ev.group_calls[pair[0]]),groups[pair[0]].position[pair[1]]))
                last_k=count()
                for g,i in pending:
                    acquire(g,i,limit,True)
                    if count()>=target or count()-last_k>=8:
                        check(True);last_k=count()
                    if warranted or timed_out():break
                check(True)
                if warranted or timed_out():break
        status='warranted' if warranted else ('deadline_abstention' if timed_out() else 'abstained')
    finally:
        start=time.perf_counter_ns();ev.close();cleanup_ns=time.perf_counter_ns()-start
    lifecycle=time.perf_counter_ns()-begin
    # Receipt encoding/output is a separate export cost, not hidden service work.
    start=time.perf_counter_ns();receipts=ev.receipts();export_ns=time.perf_counter_ns()-start
    return {'mode':mode,'status':status,'target':target,'alpha':str(alpha) if mode!='exact_cost' else '0',
            'lifecycle_ns':lifecycle,'cleanup_ns':cleanup_ns,'receipt_export_ns':export_ns,
            'profile_ns':profile_ns,'profile_calls':profile_calls,'selection_ns':selection_ns,
            'samples':sampled(),'positive_receipts':count(),'group_samples':[len(g.trace) for g in groups],
            'counts':dict(ev.counts),'group_evaluation_ns':ev.group_ns,'draws':draws,'stages':stages,'receipts':receipts}


def append(path,event):
    with path.open('a',encoding='utf-8') as f:f.write(json.dumps(event,separators=(',',':'))+'\n');f.flush();os.fsync(f.fileno())


def main(out):
    assert not out.exists();journal=out.with_suffix('.jsonl');assert not journal.exists()
    plans=[([256,256],[60,160],[3.8,4.25],F(55,100)),([256,256],[60,220],[3.8,4.25],F(65,100)),
           ([128]*4,[60,100,160,220],[3.8,4.05,4.25,4.35],F(60,100))]
    paths=[Path(__file__),Path(old.__file__),Path(old.sat.__file__),Path(old.mixed.__file__),
           Path(old.sat.sampling.__file__),Path(old.sat.base_sampling.__file__)]
    paths += [Path(__file__).with_name(n) for n in ('positive_bets.py','delayed_bets.py','bets_exchange.py','bets_float.py')]
    paths += [Path(__file__).parent.parent/'s02'/'censored_count.py']
    result={'status':'running','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','start_utc':datetime.now(timezone.utc).isoformat(),
            'native_dependency_import_ns':native_import_ns,'numeric_dependency_import_ns':numeric_import_ns,
            'python':sys.version,'sources':{p.relative_to(Path(__file__).parent.parent).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            'cohorts':[],'timing_scope':'Lifecycle includes controller, on-demand sampling, native construction/calls, proof checks and cleanup. Formula generation/hash is common input. Dependency startup and receipt export are separate costs. No free full-solve history; diagnostic reference comes after all arms.'}
    def save():out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    save()
    try:
        for case,(sizes,ns,ratios,fraction) in enumerate(plans):
            started=time.perf_counter_ns();rng=random.Random(93040+case)
            spec=[{'size':N,'variables':n,'clauses':round(n*r)} for N,n,r in zip(sizes,ns,ratios)]
            forms=[[old.sat.formula(s['variables'],s['clauses'],rng) for _ in range(s['size'])] for s in spec]
            source=hashlib.sha256(json.dumps({'spec':spec,'forms':forms,'unit':1},separators=(',',':')).encode()).hexdigest()
            target=(sum(sizes)*fraction.numerator+fraction.denominator-1)//fraction.denominator
            cohort={'case':case,'seed':93040+case,'spec':spec,'source':source,'target':target,'input_generation_binding_ns':time.perf_counter_ns()-started,'arms':[]}
            result['cohorts'].append(cohort);save()
            for mode in ('exact_cost','direct_uniform','strata_cost','joint_cost','joint_bounded'):
                event={'event':'arm_start','case':case,'mode':mode,'utc':datetime.now(timezone.utc).isoformat()};append(journal,event);print(json.dumps(event),flush=True)
                arm=policy(spec,forms,target,mode,94000+case)
                cohort['arms'].append(arm);save();append(journal,{'event':'arm_complete','case':case,'mode':mode,'status':arm['status'],'lifecycle_ns':arm['lifecycle_ns']})
                print(json.dumps({k:arm[k] for k in ('mode','status','lifecycle_ns','samples','positive_receipts','profile_calls')}),flush=True)
            started=time.perf_counter_ns();truth=[]
            for g,s in enumerate(spec):
                ys=[]
                for clauses in forms[g]:
                    solver=old.sat.Minisat22(bootstrap_with=clauses);answer=solver.solve(assumptions=[1])
                    if answer:assert old.check_model(s['variables'],clauses,solver.get_model(),1) is not None
                    ys.append(int(answer));solver.delete()
                truth.append(ys)
            cohort['reference']={'truth':truth,'total':sum(map(sum,truth)),'elapsed_ns':time.perf_counter_ns()-started,'negative_scope':'trusted native diagnostic; not service evidence'}
            for arm in cohort['arms']:
                arm['realized_warrant_correct']=None if arm['status']!='warranted' else sum(map(sum,truth))>=target
            save()
        result['status']='complete'
    except Exception:result.update(status='failed',failure=traceback.format_exc());raise
    finally:
        result['end_utc']=datetime.now(timezone.utc).isoformat();save()
        print(json.dumps({'status':result['status'],'cohorts':len(result['cohorts']),'numeric_import_ns':numeric_import_ns}),flush=True)


if __name__=='__main__':
    faulthandler.enable();main(Path(sys.argv[1]))
