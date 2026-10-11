"""DEVELOPMENT: acquire one margin, transport through local CNF edits.

Codex (GPT-6), 2026-10-11. Local runtime source binding, not an externally
authenticated proof of random sample selection or arbitrary supplied bounds.
"""
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import sys
import time
import traceback
import proof_values as proof


@dataclass(frozen=True)
class CountWarrant:
    source: str
    population: int
    lower: int
    alpha: F


def acquire(family,source,target,alpha,seed):
    started=time.perf_counter_ns();before=family.counts.copy();counts=Counter()
    N=len(family.forms);models={};group=[]
    for i,model in enumerate(family.models):
        counts['initial_witness_tests']+=1
        if model is not None:
            if 1 in model:models[i]=model
            else:group.append(i)
    b=len(models);R=len(group);s=k=0
    sampler=proof.sat.base_sampling.WithoutReplacement(R,random.Random(seed))
    m0=target-b-1;stages=[];draws=[];next_check=1
    def warranted():
        return b+k>=target or 0<=m0<R and proof.mixed.reject(R,s,k,m0,alpha,counts)
    got=warranted()
    while not got and s<R:
        i=group[sampler.take()]
        outcome=family.prove(i,1,None);s+=1
        draws.append(dict(index=i,evidence='positive_proof' if outcome=='proved' else 'unresolved'))
        if outcome=='proved':
            # Preserve a concrete receipt for later source binding and edits.
            model=proof.check_model(family.n,family.forms[i],family.solvers[i].get_model(),1)
            assert model is not None
            models[i]=model;k+=1;counts['retained_receipt_checks']+=1
        if b+k>=target:got=True
        elif s>=next_check:
            got=warranted();next_check=max(s+1,(s*1415+999)//1000)
            stages.append(dict(prefix=s,positive_proofs=k,warrant=got))
    if not got:got=warranted()
    lower=max(target,len(models)) if got else len(models)
    # Without statistical success, only the deterministic receipt count is used.
    bound=CountWarrant(source,N,lower,alpha if got and lower>len(models) else F(0))
    report=dict(status='warranted' if got else 'insufficient_for_target',target=target,
                source=source,lower=lower,alpha=bound.alpha,initial_proofs=b,group_size=R,
                sampled_prefix=s,new_proofs=k,total_receipts=len(models),stages=stages,
                group_indices=group,draws=draws,sample_seed=seed,
                counts=dict(counts+family.counts-before),elapsed_ns=time.perf_counter_ns()-started)
    return bound,models,report


class MarginState:
    def __init__(self,n,forms,source,bound,receipts):
        if bound.source!=source or bound.population!=len(forms):raise ValueError('Wrong bound source')
        if not 0<=bound.lower<=len(forms):raise ValueError('Invalid lower count')
        self.n,self.forms,self.bound=n,forms,bound
        self.models={}
        for i,model in receipts:
            if type(i) is not int or not 0<=i<len(forms) or i in self.models:raise ValueError('Bad receipt identity')
            checked=proof.check_model(n,forms[i],model,1)
            if checked is None:raise ValueError('Receipt fails source check')
            self.models[i]=checked
        self.version=0;self.active={};self.uncertain=0;self.lost_cached=0

    def effect(self,i,lit):
        if lit is None or lit==1:return 0,0
        stable=i in self.models and lit in self.models[i]
        return int(not stable),int(i in self.models and not stable)

    def edit(self,parent,index,lit):
        if type(parent) is not int or parent!=self.version:raise ValueError('Wrong parent')
        if type(index) is not int or not 0<=index<len(self.forms):raise ValueError('Invalid index')
        if lit is not None and (type(lit) is not int or not 1<=abs(lit)<=self.n):raise ValueError('Invalid literal')
        old=self.active.get(index)
        old_uncertain,old_lost=self.effect(index,old)
        new_uncertain,new_lost=self.effect(index,lit)
        if lit is None:self.active.pop(index,None)
        else:self.active[index]=lit
        self.uncertain+=new_uncertain-old_uncertain
        self.lost_cached+=new_lost-old_lost
        self.version+=1
        return self.query()

    def query(self):
        support=max(0,self.bound.lower-len(self.active))
        refined=max(0,self.bound.lower-self.uncertain)
        receipts=len(self.models)-self.lost_cached
        refined=max(refined,receipts)
        N=len(self.forms)
        return dict(version=self.version,active=len(self.active),uncertain=self.uncertain,
                    support_lower=support,refined_lower=refined,receipt_lower=receipts,
                    support_warrant=2*support>=N,refined_warrant=2*refined>=N,
                    receipt_warrant=2*receipts>=N)


def invalid_screen(state):
    before=(state.version,dict(state.active),state.uncertain,state.lost_cached)
    cases=[(-1,0,2),(0,-1,2),(0,len(state.forms),2),(0,0,0),(0,0,True),(False,0,2)]
    for args in cases:
        try:state.edit(*args)
        except ValueError:pass
        else:raise AssertionError('Accepted invalid edit')
        assert (state.version,state.active,state.uncertain,state.lost_cached)==before
    return len(cases)


def main(output):
    assert not output.exists()
    paths=[Path(__file__),Path(proof.__file__),Path(proof.sat.__file__),Path(proof.mixed.__file__),Path(proof.sat.sampling.__file__),Path(proof.sat.base_sampling.__file__)]
    reference_path=Path(__file__).with_name('sat_values03.json')
    reference_record=json.loads(reference_path.read_text(encoding='utf-8'))
    result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                reference_sha256=hashlib.sha256(reference_path.read_bytes()).hexdigest(),
                scope='One exposed n=100 cohort, fixed .55 initial margin, alpha .05. Local source/version binding and exact support transport. Seeded sampling is developmental; no external randomness authentication. Common immutable input generation/hash and final serialization excluded; history, acquisition, receipt binding, edits and cleanup separately measured. Exact reference is diagnostic and excluded from controller costs.')
    start=time.monotonic_ns()
    def save(stage):
        result['boundary']=dict(stage=stage,utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8');print(stage,flush=True)
    save('entered')
    try:
        definition=next(x['definition'] for x in reference_record['rows'] if x['definition']['n']==100)
        n=definition['n'];N=definition['N'];rng=random.Random(definition['seed'])
        forms=tuple(proof.sat.formula(n,int(n*F(definition['ratio'])),rng) for _ in range(N))
        assert hashlib.sha256(json.dumps(forms).encode()).hexdigest()==definition['source_sha256']
        source_descriptor=dict(formulas_sha256=definition['source_sha256'],all_unit=1,N=N)
        source=hashlib.sha256(json.dumps(source_descriptor,sort_keys=True).encode()).hexdigest()
        result.update(definition=definition,source_descriptor=source_descriptor,source_id=source)
        family=proof.ProofFamily(n,forms);result['history_ns']=family.history_ns
        bound,models,acquisition=acquire(family,source,(55*N+99)//100,F(1,20),8611)
        result['acquisition']=acquisition
        cleanup_start=time.perf_counter_ns();family.close();result['cleanup_ns']=time.perf_counter_ns()-cleanup_start
        del family
        result['receipts']=[dict(index=i,assignment_bits=hex(sum(1<<(v-1) for v in model if v>0))) for i,model in sorted(models.items())]
        save('margin_acquired')
        before=time.perf_counter_ns();state=MarginState(n,forms,source,bound,list(models.items()))
        result['binding_ns']=time.perf_counter_ns()-before
        before=time.perf_counter_ns();result['invalid_edits_rejected']=invalid_screen(state)
        try:MarginState(n,forms,'wrong-source',bound,[])
        except ValueError:result['wrong_source_rejected']=True
        else:raise AssertionError('Wrong source accepted')
        result['invalid_request_ns']=time.perf_counter_ns()-before
        ref_start=time.perf_counter_ns();reference=proof.sat.Family(forms)
        base_truth=[reference.label(i,1) for i in range(N)];truth=base_truth.copy()
        assert sum(base_truth)==definition['edited_sat'][0]
        result['reference_initial_ns']=time.perf_counter_ns()-ref_start
        result['base_count_bound_realized_valid']=bound.lower<=sum(base_truth)
        edit_rng=random.Random(8610);indices=edit_rng.sample(range(N),128)
        def new_literal():
            v=edit_rng.randrange(2,11);return v if edit_rng.getrandbits(1) else -v
        edits=[(i,new_literal()) for i in indices]+[(i,new_literal()) for i in indices[:16]]+[(i,None) for i in reversed(indices)]
        rows=[dict(operation='initial',bounds=state.query(),actual_count=sum(truth))]
        controller_ns=reference_ns=0
        for i,lit in edits:
            before=time.perf_counter_ns();b=state.edit(state.version,i,lit);elapsed=time.perf_counter_ns()-before
            controller_ns+=elapsed
            before=time.perf_counter_ns()
            if lit is None:truth[i]=base_truth[i]
            elif not base_truth[i]:truth[i]=0
            else:
                assumptions=list(dict.fromkeys((1,lit)))
                truth[i]=int(reference.solvers[i].solve(assumptions=assumptions))
                if truth[i]:
                    model=proof.check_model(n,forms[i],reference.solvers[i].get_model(),1)
                    assert model is not None and lit in model
            reference_ns+=time.perf_counter_ns()-before
            actual=sum(truth)
            if result['base_count_bound_realized_valid']:
                assert b['support_lower']<=actual and b['refined_lower']<=actual
            assert b['receipt_lower']<=actual
            rows.append(dict(operation='remove' if lit is None else 'set',index=i,literal=lit,
                             bounds=b,actual_count=actual,controller_ns=elapsed))
        reference.close();assert not state.active and state.query()['refined_lower']==max(bound.lower,len(models))
        result.update(status='complete',rows=rows,controller_edits_ns=controller_ns,reference_edits_ns=reference_ns,
                      controller_total_ns=result['history_ns']+acquisition['elapsed_ns']+result['binding_ns']+controller_ns+result['cleanup_ns']+result['invalid_request_ns'])
    except Exception:
        result.update(status='failed',failure=traceback.format_exc());raise
    finally:
        result.update(elapsed_ns=time.monotonic_ns()-start,end_utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ('rows','receipts','acquisition')},default=str))


if __name__=='__main__':main(Path(sys.argv[1]))
