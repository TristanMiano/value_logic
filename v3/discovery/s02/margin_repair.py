"""DEVELOPMENT: pointwise proof repair of a persistent statistical margin.

Codex (GPT-6), 2026-10-11. Same supplied warrant/receipts/attempt cap; source
locality changes the acquisition order, not the proof acceptance rule.
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
import margin_edits as old


class RepairState(old.MarginState):
    def accept(self,parent,i,model):
        if type(parent) is not int or parent!=self.version:raise ValueError('Wrong receipt parent')
        if type(i) is not int or not 0<=i<len(self.forms):raise ValueError('Wrong receipt index')
        checked=old.proof.check_model(self.n,self.forms[i],model,1)
        current=self.active.get(i)
        if checked is None or current is not None and current not in checked:return False
        uncertain,lost=self.effect(i,current)
        self.models[i]=checked
        self.uncertain-=uncertain;self.lost_cached-=lost
        return True

    def proved(self,i):
        current=self.active.get(i)
        return i in self.models and (current is None or current in self.models[i])


class Proposer:
    def __init__(self,forms):
        self.forms=forms;self.solvers={};self.counts=Counter()
    def propose(self,i,lit):
        if i not in self.solvers:
            self.solvers[i]=old.proof.sat.Minisat22(bootstrap_with=self.forms[i]+((1,),))
            self.counts['native_builds']+=1
        solver=self.solvers[i];self.counts['native_calls']+=1
        answer=solver.solve(assumptions=[] if lit is None else [lit])
        self.counts['positive_proposals' if answer else 'unsupported_negatives']+=1
        return solver.get_model() if answer else None
    def close(self):
        for solver in self.solvers.values():solver.delete()


def snapshot(state):
    return (state.version,dict(state.active),state.uncertain,state.lost_cached,dict(state.models))


def receipt_screen(state):
    before=snapshot(state);i=next(iter(state.models));model=list(state.models[i]);rejected=0
    for parent,index in ((state.version+1,i),(state.version,len(state.forms))):
        try:state.accept(parent,index,model)
        except ValueError:rejected+=1
        else:raise AssertionError('Accepted stale/wrong-identity receipt')
        assert snapshot(state)==before
    assert not state.accept(state.version,i,[1,-1]);rejected+=1
    assert snapshot(state)==before
    return rejected


def lifecycle(forms,n,source,bound,receipts,old_sat_hints,edits,mode):
    start=time.perf_counter_ns();state=RepairState(n,forms,source,bound,receipts)
    invalid=receipt_screen(state);proposer=Proposer(forms)
    rng=random.Random(8640);order=list(range(len(forms)));rng.shuffle(order)
    rank={i:j for j,i in enumerate(order)};failed=set();rows=[];accepted=[]
    for entry in edits:
        request_start=time.perf_counter_ns()
        before_counts=proposer.counts.copy();state.edit(state.version,entry['index'],entry['literal'])
        before=state.query();attempts=[]
        if mode!='transport_only' and not before['refined_warrant']:
            pending=[i for i in order if not state.proved(i) and (i,state.active.get(i)) not in failed]
            def priority(i):
                # The saved old-SAT assay is a yield hint only. All controllers
                # receive it; no unsupported negative becomes a truth label.
                local=mode=='targeted' and state.active.get(i) is not None and state.effect(i,state.active[i])[0]
                return (i not in old_sat_hints,not local,rank[i])
            pending.sort(key=priority)
            for i in pending[:8]:
                lit=state.active.get(i);model=proposer.propose(i,lit)
                ok=state.accept(state.version,i,model)
                attempts.append(dict(index=i,literal=lit,accepted=ok))
                if ok:
                    accepted.append(dict(version=state.version,index=i,literal=lit,
                                         assignment_bits=hex(sum(1<<(v-1) for v in model if v>0))))
                else:failed.add((i,lit))
                if state.query()['refined_warrant']:break
        after=state.query()
        assert after['refined_lower']<=entry['actual_count']
        assert after['receipt_lower']<=entry['actual_count']
        rows.append(dict(version=state.version,index=entry['index'],literal=entry['literal'],
                         before=before,after=after,attempts=attempts,
                         proposer_counts=dict(proposer.counts-before_counts),
                         request_ns=time.perf_counter_ns()-request_start,
                         realized_valid=True))
    proposer.close()
    return dict(mode=mode,rows=rows,accepted_receipts=accepted,counts=dict(proposer.counts),
                invalid_receipts_rejected=invalid,elapsed_ns=time.perf_counter_ns()-start,
                sample_selection='fixed broad rank seed 8640; repair choices need no fresh lottery or statistical alpha',
                warranted_states=sum(row['after']['refined_warrant'] for row in rows),
                final_receipt_count=len(state.models),final_lower=state.query()['refined_lower'])


def main(output):
    assert not output.exists();input_path=Path(__file__).with_name('margin_edits01.json')
    record=json.loads(input_path.read_text(encoding='utf-8'))
    paths=[Path(__file__),Path(old.__file__),Path(old.proof.__file__),Path(old.proof.sat.__file__),Path(old.proof.mixed.__file__),Path(old.proof.sat.sampling.__file__),Path(old.proof.sat.base_sampling.__file__)]
    units=[];result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',units=units,
                        start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                        sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                        input_sha256=hashlib.sha256(input_path.read_bytes()).hexdigest(),
                        scope='Same exposed 272-edit stream and saved margin/receipts. Eight-attempt cap per edit, not equal wall-time caps. New work includes receipt binding, scheduling, native construction/calls, failed attempts, proof checks, bookkeeping and cleanup; common immutable input reconstruction and final serialization excluded. Locality/broad controls may be copied by ordinary methods. No new alpha is spent: proofs pointwise refine the existing source.')
    start=time.monotonic_ns()
    def save(stage):
        result['boundary']=dict(stage=stage,utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8');print(stage,flush=True)
    save('entered')
    try:
        d=record['definition'];n=d['n'];N=d['N'];rng=random.Random(d['seed'])
        forms=tuple(old.proof.sat.formula(n,int(n*F(d['ratio'])),rng) for _ in range(N))
        assert hashlib.sha256(json.dumps(forms).encode()).hexdigest()==d['source_sha256']
        a=record['acquisition'];bound=old.CountWarrant(record['source_id'],N,a['lower'],F(a['alpha']))
        receipts=[]
        for r in record['receipts']:
            bits=int(r['assignment_bits'],16)
            receipts.append((r['index'],[j if bits>>(j-1)&1 else -j for j in range(1,n+1)]))
        drawn_positives={d['index'] for d in a['draws'] if d['evidence']=='positive_proof'}
        initial_positives={i for i,model in receipts}-drawn_positives
        old_sat_hints=set(a['group_indices'])|initial_positives
        assert len(old_sat_hints)==record['definition']['base_sat']
        result['shared_paid_input_ns']=record['history_ns']+a['elapsed_ns']+record['cleanup_ns']
        result['shared_input_cost_meaning']='Historical acquisition bill reused for accounting; not a fresh latency measurement or new research credit.'
        for mode in ('transport_only','broad','targeted'):
            save('lifecycle_next_'+mode)
            unit=lifecycle(forms,n,record['source_id'],bound,receipts,old_sat_hints,record['rows'][1:],mode)
            units.append(unit);save('lifecycle_complete_'+mode)
        result['status']='complete'
    except Exception:
        result.update(status='failed',failure=traceback.format_exc());raise
    finally:
        result.update(elapsed_ns=time.monotonic_ns()-start,end_utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='units'},default=str))


if __name__=='__main__':main(Path(sys.argv[1]))
