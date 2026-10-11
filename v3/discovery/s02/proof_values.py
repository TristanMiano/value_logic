"""DEVELOPMENT: value warrants from checked positive proofs alone.

Codex (GPT-6), 2026-10-11. Native negative outputs only affect scheduling;
they never enter the evidence count. Uniform sample selection is trusted.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import sys
import time
import traceback
import sat_values as sat
import sat_values_v2 as mixed


def check_model(n,clauses,model,lit=None):
    if not isinstance(model,(list,tuple,frozenset,set)) or len(model)!=n:return None
    if any(type(v) is not int or not 1<=abs(v)<=n for v in model):return None
    if len({abs(v) for v in model})!=n:return None
    assignment=frozenset(model)
    if lit is not None and lit not in assignment:return None
    if not all(any(v in assignment for v in c) for c in clauses):return None
    return assignment


class ProofFamily:
    def __init__(self,n,forms):
        started=time.perf_counter_ns()
        self.n,self.forms=n,forms
        self.models=[];self.solvers=[];self.cost_hints=[]
        self.counts=Counter()
        for clauses in forms:
            solver=sat.Minisat22(bootstrap_with=clauses)
            self.solvers.append(solver)
            answer=solver.solve()
            self.counts['history_calls']+=1
            model=check_model(n,clauses,solver.get_model()) if answer is True else None
            if answer is True:assert model is not None
            self.models.append(model)
            self.cost_hints.append(solver.accum_stats()['conflicts'])
            self.counts['history_accepted_sat']+=int(model is not None)
            self.counts['history_no_proof']+=int(model is None)
        self.history_ns=time.perf_counter_ns()-started

    def prove(self,i,lit,budget):
        solver=self.solvers[i]
        self.counts['proof_attempts']+=1
        if budget is None:
            answer=solver.solve(assumptions=[lit])
        else:
            solver.conf_budget(budget)
            self.counts['requested_conflict_budget']+=budget
            answer=solver.solve_limited(assumptions=[lit])
        if answer is True:
            self.counts['positive_proposals']+=1
            model=check_model(self.n,self.forms[i],solver.get_model(),lit)
            if model is None:
                self.counts['invalid_proposals']+=1
                return 'unknown'
            self.counts['accepted_sat']+=1
            return 'proved'
        self.counts['negative_proposals' if answer is False else 'unknown_returns']+=1
        return 'deprioritized' if answer is False else 'unknown'

    def close(self):
        for solver in self.solvers:solver.delete()


def request(family,lit,mode,alpha,seed):
    start=time.perf_counter_ns();before=family.counts.copy()
    counts=Counter()
    N=len(family.forms);b=0;group=[]
    for i,model in enumerate(family.models):
        counts['history_membership_reads']+=1
        if model is not None:
            counts['unit_witness_tests']+=1
            if lit in model:b+=1
            else:group.append(i)
    R=len(group);k=s=0
    counts['untreated_outside_group']=N-b-R
    statistical=mode.startswith('stat')
    bounded='bounded' in mode
    if mode=='exact_bounded_cost':
        order=sorted(group,key=lambda i:family.cost_hints[i])
        counts['sorted_candidates']=R
    else:
        sampler=sat.base_sampling.WithoutReplacement(R,random.Random(seed))
        order=[group[sampler.take()] for _ in range(R)]
    statuses={};stages=[]
    m0=(N+1)//2-1-b
    def warranted():
        if 2*(b+k)>=N:return True
        return statistical and 0<=m0<R and mixed.reject(R,s,k,m0,alpha,counts)
    budgets=(32,128,512) if bounded else (None,)
    got=warranted()
    for round_index,budget in enumerate(budgets):
        if got:break
        pending=order if round_index==0 else [i for i in order if statuses[i]=='unknown']
        next_check=1
        for i in pending:
            outcome=family.prove(i,lit,budget)
            statuses[i]=outcome
            if round_index==0:s+=1
            if outcome=='proved':k+=1
            # Exact bounds are checked after every new proof. Statistical
            # tests use sqrt(2) growing prefixes, then every resumed proof.
            if 2*(b+k)>=N:
                got=True;break
            if statistical and (round_index>0 or s>=next_check):
                got=warranted()
                stages.append(dict(round=round_index,prefix=s,accepted=k,warrant=got))
                next_check=max(s+1,(s*1415+999)//1000)
                if got:break
        if not got:got=warranted()
    return dict(mode=mode,unit_literal=lit,outcome='warrant_positive' if got else 'insufficient_evidence',
                population=N,immediate_proofs=b,remaining_group=R,sampled_prefix=s,accepted_sample_proofs=k,
                counts=dict(counts+family.counts-before),stages=stages,
                request_ns=time.perf_counter_ns()-start)


def checker_screen():
    clauses=((1,2),(-1,3));good=[1,-2,3]
    assert check_model(3,clauses,good,3)
    bad=[[],[1,-2],[1,-2,3,4],[1,-1,3],[1,1,3],[True,-2,3],[0,-2,3],[4,-2,3],[-1,-2,3],[1,-2,-3]]
    assert all(check_model(3,clauses,m,3) is None for m in bad)
    assert check_model(3,clauses,good,-3) is None
    return dict(valid_accepted=1,invalid_rejected=len(bad)+1)


def main(output):
    assert not output.exists()
    journal=output.with_suffix('.jsonl');assert not journal.exists()
    sources=[Path(__file__),Path(sat.__file__),Path(mixed.__file__),Path(sat.sampling.__file__),Path(sat.base_sampling.__file__)]
    reference_path=Path(__file__).with_name('sat_values03.json')
    reference=json.loads(reference_path.read_text(encoding='utf-8'))
    rows=[]
    result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',rows=rows,
                start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                reference_sha256=hashlib.sha256(reference_path.read_bytes()).hexdigest(),
                scope='Same exposed SAT populations as diagnostic scale run; positive proof service, unsupported negatives never accepted. Warm installed runtime, common generation/import/output serialization excluded; separate full base histories and marginal costs include partition/proposals/checks/sampling/cleanup. Fresh-first bounded budgets 32,128,512; total positive-warrant error <=.05 across eight requests under trusted uniform sampling. Statistical and exact controls may report insufficient evidence.')
    def checkpoint(stage):
        result['boundary']=dict(stage=stage,utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(stage,flush=True)
    start=time.monotonic_ns();checkpoint('entered')
    try:
        result['checker_screen']=checker_screen()
        for n in (60,100):
            definition=next(x['definition'] for x in reference['rows'] if x['definition']['n']==n)
            rng=random.Random(definition['seed']);N=definition['N']
            forms=tuple(sat.formula(n,int(n*F(definition['ratio'])),rng) for _ in range(N))
            assert hashlib.sha256(json.dumps(forms).encode()).hexdigest()==definition['source_sha256']
            edits=[lit for i in range(1,5) for lit in (i,-i)]
            for mode in ('exact_full','stat_full','exact_bounded_random','exact_bounded_cost','stat_bounded'):
                checkpoint('history_next_'+str(n)+'_'+mode)
                family=ProofFamily(n,forms)
                margin_start=time.perf_counter_ns();requests=[]
                for j,lit in enumerate(edits):
                    r=request(family,lit,mode,F(1,160),definition['seed']+j)
                    r['realized_warrant_valid']=r['outcome']!='warrant_positive' or 2*definition['edited_sat'][j]>=N
                    requests.append(r)
                    # Durable complete request units; serialization lies in
                    # the marginal lifecycle bill and is separately reported.
                    io_start=time.perf_counter_ns()
                    with journal.open('a',encoding='utf-8') as f:
                        f.write(json.dumps(dict(n=n,mode=mode,j=j,request=r),default=str)+'\n')
                    r['journal_ns']=time.perf_counter_ns()-io_start
                family.close();marginal=time.perf_counter_ns()-margin_start
                rows.append(dict(definition=definition,mode=mode,requests=requests,history_ns=family.history_ns,
                                 marginal_ns=marginal,total_ns=family.history_ns+marginal,counts=dict(family.counts)))
                checkpoint('lifecycle_complete_'+str(n)+'_'+mode)
        result['status']='complete'
    except Exception:
        result.update(status='failed',failure=traceback.format_exc());raise
    finally:
        result.update(elapsed_ns=time.monotonic_ns()-start,end_utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='rows'},default=str))


if __name__=='__main__':main(Path(sys.argv[1]))
