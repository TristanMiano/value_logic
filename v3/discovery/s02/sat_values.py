"""DEVELOPMENT: finite SAT-family values after explicit unit-clause edits.

Codex (GPT-6), 2026-10-11. Same paid base history, native incremental kernel,
checked SAT witnesses, trusted native UNSAT. All arms can use identical kernels.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import random
import sys
import time
import traceback
if os.environ.get('VL_SAT_DEPS'):
    sys.path.insert(0,os.environ['VL_SAT_DEPS'])
from pysat.solvers import Minisat22
import sampling_probe as base_sampling
import sampling_v2 as sampling


def formula(n,m,rng):
    return tuple(tuple(v if rng.getrandbits(1) else -v for v in rng.sample(range(1,n+1),3)) for _ in range(m))


class Family:
    def __init__(self,forms):
        self.forms=forms
        self.solvers=[]
        self.models=[]
        self.base=[]
        self.counts=Counter()
        start=time.perf_counter_ns()
        for clauses in forms:
            solver=Minisat22(bootstrap_with=clauses)
            self.solvers.append(solver)
            self.counts['history_solver_calls']+=1
            answer=solver.solve()
            model=frozenset(solver.get_model()) if answer else frozenset()
            if answer:
                assert all(any(lit in model for lit in c) for c in clauses)
                self.counts['history_checked_clauses']+=len(clauses)
            self.base.append(int(answer)); self.models.append(model)
        self.history_ns=time.perf_counter_ns()-start

    def proof(self,i,lit):
        if not self.base[i]:
            self.counts['unsat_transports']+=1
            return 0
        self.counts['witness_unit_tests']+=1
        if lit in self.models[i]:
            self.counts['witness_hits']+=1
            return 1
        return None

    def label(self,i,lit):
        self.counts['label_requests']+=1
        proved=self.proof(i,lit)
        if proved is not None:return proved
        self.counts['edit_solver_calls']+=1
        answer=self.solvers[i].solve(assumptions=[lit])
        if answer:
            model=frozenset(self.solvers[i].get_model())
            assert lit in model and all(any(v in model for v in c) for c in self.forms[i])
            self.counts['edit_checked_clauses']+=len(self.forms[i])+1
        return int(answer)

    def close(self):
        for solver in self.solvers:solver.delete()


def direct_action(N,s,ones,zeros,offset,total,alpha,counts):
    """Remaining N unknown bits, offset proven ones in total population.

    ones+zeros may be less than s: missing labels remain in the prefix.
    Deterministic bounds include all unsampled/missing labels conservatively.
    """
    assert ones+zeros<=s<=N
    if 2*(offset+ones)>=total:return 1
    if 2*(offset+N-zeros)<=total:return 0
    threshold=(total+1)//2
    m0=threshold-1-offset
    # Fixed .8 working success alternative, clipped to the null boundary.
    if 0<=m0<N:
        m1=max(m0+1,min(N,(4*N+4)//5))
        if sampling.reject_lower(N,s,ones,m0,m1,alpha/2,counts):return 1
    # Negative action needs remaining zeros >= offset+N-floor(total/2).
    z0=offset+N-total//2-1
    if 0<=z0<N:
        z1=max(z0+1,min(N,(4*N+4)//5))
        if sampling.reject_lower(N,s,zeros,z0,z1,alpha/2,counts):return 0
    return None


def request(family,lit,mode,alpha,seed):
    start=time.perf_counter_ns()
    before=family.counts.copy()
    total=len(family.forms)
    counts=Counter()
    if mode=='uniform_direct':
        group=list(range(total)); offset=0
    else:
        # Exact old-UNSAT transport removes those indices from the population.
        group=[i for i,bit in enumerate(family.base) if bit]
        counts['base_partition_reads']+=total
        offset=0
        if mode in ('proof_first_direct','exact_proof_first'):
            pending=[]
            for i in group:
                if family.proof(i,lit)==1:offset+=1
                else:pending.append(i)
            group=pending
    N=len(group)
    sampler=base_sampling.WithoutReplacement(N,random.Random(seed))
    s=ones=zeros=0
    stages=[]
    while True:
        if 2*(offset+ones)>=total:action=1
        elif 2*(offset+N-zeros)<=total:action=0
        elif mode=='exact_proof_first':action=None
        elif mode=='monotone_ci':
            low,high=sampling.interval(N,s,ones,alpha,counts)
            action=base_sampling.choose(F(offset+low,total),F(offset+high,total),F(0))
        else:action=direct_action(N,s,ones,zeros,offset,total,alpha,counts)
        if action is not None:break
        target=min(N,s+1 if mode=='exact_proof_first' else max(1,2*s))
        assert target>s
        while s<target:
            bit=family.label(group[sampler.take()],lit)
            ones+=bit;zeros+=1-bit;s+=1
        stages.append(dict(sampled=s,ones=ones,zeros=zeros))
    return dict(mode=mode,unit_literal=lit,action=action,sampled=s,remaining_population=N,
                proved_ones=offset,counts=dict(counts+family.counts-before),stages=stages,
                request_ns=time.perf_counter_ns()-start)


def missing_screen():
    from itertools import product
    checked=0
    for N in range(2,8):
        for s in range(N+1):
            for states in product((-1,0,1),repeat=s):
                ones=states.count(1);zeros=states.count(0);u=states.count(-1)
                got=direct_action(N,s,ones,zeros,0,N,F(1,5),Counter())
                if got is not None:
                    # Every compatible full-label prefix warrants that same
                    # action, or a tie permits either deterministic choice.
                    for e in range(ones,ones+u+1):
                        if got==1:
                            assert 2*e>=N or sampling.reject_lower(N,s,e,(N+1)//2-1,max((N+1)//2,(4*N+4)//5),F(1,10))
                        else:
                            assert 2*(N-(s-e))<=N or sampling.reject_lower(N,s,s-e,N-N//2-1,max(N-N//2,(4*N+4)//5),F(1,10))
                checked+=1
    failure=dict(N=8,true_ones=3,naive_discard_rejects=sampling.reject_lower(8,3,3,3,8,F(1,10)),
                 partial_rejects=sampling.reject_lower(8,8,3,3,8,F(1,10)))
    assert failure['naive_discard_rejects'] and not failure['partial_rejects']
    return dict(partial_prefix_states=checked,discard_failure=failure)


def main(output):
    assert not output.exists()
    source_paths=[Path(__file__),Path(sampling.__file__),Path(base_sampling.__file__)]
    result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
                dependency_versions={'python':sys.version,'python-sat':importlib.metadata.version('python-sat')},
                scope='Warm installed runtime; base-history-inclusive and marginal edit costs, includes checked SAT witnesses and solver cleanup; common population generation/import excluded. Native UNSAT is trusted. Statistical decision risk at most .05 over three predeclared requests under ideal uniform sampling; seeded streams are development fixtures.')
    start=time.monotonic_ns()
    rows=[]
    result['rows']=rows
    try:
        result['missing_labels']=missing_screen()
        for n in (40,60):
            for ratio in (F(19,5),F(83,20),F(22,5)):
                seed=8500+n*100+int(ratio*100)
                rng=random.Random(seed)
                forms=tuple(formula(n,int(n*ratio),rng) for _ in range(256))
                edits=[1,-2,3]
                definition=dict(n=n,ratio=str(ratio),N=len(forms),seed=seed,
                                source_sha256=hashlib.sha256(json.dumps(forms).encode()).hexdigest())
                reference=Family(forms)
                truth=[[reference.label(i,lit) for i in range(len(forms))] for lit in edits]
                reference.close()
                exact_actions=[int(2*sum(y)>=len(y)) for y in truth]
                definition.update(base_sat=sum(reference.base),edited_sat=list(map(sum,truth)),
                                  edited_truth_sha256=[hashlib.sha256(bytes(y)).hexdigest() for y in truth])
                for mode in ('exact_proof_first','uniform_direct','monotone_direct','proof_first_direct','monotone_ci'):
                    family=Family(forms)
                    margin_start=time.perf_counter_ns()
                    requests=[]
                    for j,lit in enumerate(edits):
                        r=request(family,lit,mode,F(1,60),seed+j)
                        r['realized_correct']=r['action']==exact_actions[j] or 2*sum(truth[j])==len(forms)
                        requests.append(r)
                    family.close()
                    marginal=time.perf_counter_ns()-margin_start
                    rows.append(dict(definition=definition,mode=mode,requests=requests,history_ns=family.history_ns,
                                     marginal_ns=marginal,total_ns=family.history_ns+marginal,counts=dict(family.counts)))
        result['status']='complete'
    except Exception:
        result.update(status='failed',failure=traceback.format_exc())
        raise
    finally:
        result.update(elapsed_ns=time.monotonic_ns()-start,end_utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='rows'},default=str))


if __name__=='__main__':main(Path(sys.argv[1]))
