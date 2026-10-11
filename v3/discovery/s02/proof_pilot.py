"""DEVELOPMENT: pay for proof-recipe profiles, then select by a heuristic.

Codex (GPT-6), 2026-10-11. Selection is fallible; warrant uses a monotone
finite-population test on independently checked positive proofs only.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import time
import traceback
import proof_values as proof

BUDGETS=(32,128,512,None)


def recipe(family,i,lit,stage,profile=False):
    started=time.perf_counter_ns();accepted=[];costs=[];outcome='unknown'
    for j,budget in enumerate(BUDGETS[:stage+1]):
        if outcome=='unknown':outcome=family.prove(i,lit,budget)
        accepted.append(int(outcome=='proved'))
        costs.append(time.perf_counter_ns()-started)
        if outcome!='unknown':
            # The recipe itself terminates after a proof or negative hint.
            # Later cumulative recipes have identical realized outcomes/cost.
            while len(accepted)<=stage:
                accepted.append(accepted[-1]);costs.append(costs[-1])
            break
    return outcome,accepted,costs


def pilot_request(family,lit,alpha,seed):
    start=time.perf_counter_ns();before=family.counts.copy();counts=Counter()
    N=len(family.forms);b=0;group=[]
    for i,model in enumerate(family.models):
        counts['history_membership_reads']+=1
        if model is not None:
            counts['unit_witness_tests']+=1
            if lit in model:b+=1
            else:group.append(i)
    R=len(group);s=k=0;m0=(N+1)//2-1-b
    sampler=proof.sat.base_sampling.WithoutReplacement(R,random.Random(seed))
    seen=[];status={};stages=[];profiles=[]
    def warranted():
        if 2*(b+k)>=N:return True
        return 0<=m0<R and proof.mixed.reject(R,s,k,m0,alpha,counts)
    got=warranted();selected=None;scores=[]
    if not got and R>0:
        for _ in range(min(16,R)):
            i=group[sampler.take()];seen.append(i)
            outcome,accepted,costs=recipe(family,i,lit,3,True)
            status[i]=outcome;s+=1;k+=outcome=='proved'
            profiles.append(dict(accepted=accepted,cumulative_ns=costs))
        q=F((N+1)//2-b,R)
        for j in range(4):
            total_proofs=sum(p['accepted'][j] for p in profiles)
            total_ns=sum(p['cumulative_ns'][j] for p in profiles)
            rate=(total_proofs+.5)/(len(profiles)+1)
            null=float(q)
            divergence=0.0
            if 0<null<rate<1:
                divergence=rate*math.log(rate/null)+(1-rate)*math.log((1-rate)/(1-null))
            score=divergence/(total_ns/len(profiles)) if total_ns else 0.0
            scores.append(dict(stage=j,proofs=total_proofs,pilot_size=len(profiles),
                               total_ns=total_ns,smoothed_rate=rate,required_rate=q,
                               heuristic_kl=divergence,score_per_ns=score))
        selected=max(range(4),key=lambda j:scores[j]['score_per_ns'])
        if scores[selected]['score_per_ns']==0:selected=3
        got=warranted();stages.append(dict(prefix=s,accepted=k,warrant=got,phase='pilot'))
        target=min(R,max(s+1,(s*1415+999)//1000))
        while not got and s<R:
            i=group[sampler.take()];seen.append(i)
            outcome,_,_=recipe(family,i,lit,selected)
            status[i]=outcome;s+=1;k+=outcome=='proved'
            if 2*(b+k)>=N:got=True
            elif s>=target:
                got=warranted();stages.append(dict(prefix=s,accepted=k,warrant=got,phase='selected'))
                target=min(R,max(s+1,(s*1415+999)//1000))
        if not got:got=warranted()
        # Complete-call fallback retains the missing-label interpretation.
        if not got:
            for i in seen:
                if status[i]!='unknown':continue
                outcome=family.prove(i,lit,None);status[i]=outcome;k+=outcome=='proved'
                got=warranted()
                if got:break
    return dict(mode='paid_pilot',unit_literal=lit,outcome='warrant_positive' if got else 'insufficient_evidence',
                population=N,immediate_proofs=b,remaining_group=R,sampled_prefix=s,accepted_sample_proofs=k,
                selected_stage=selected,profile_scores=scores,pilot_profiles=profiles,stages=stages,
                counts=dict(counts+family.counts-before),request_ns=time.perf_counter_ns()-start)


def main(output):
    assert not output.exists();journal=output.with_suffix('.jsonl');assert not journal.exists()
    paths=[Path(__file__),Path(proof.__file__),Path(proof.sat.__file__),Path(proof.mixed.__file__),Path(proof.sat.sampling.__file__),Path(proof.sat.base_sampling.__file__)]
    reference_path=Path(__file__).with_name('sat_values03.json');reference=json.loads(reference_path.read_text(encoding='utf-8'))
    rows=[];result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',rows=rows,
                       start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                       sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                       reference_sha256=hashlib.sha256(reference_path.read_bytes()).hexdigest(),
                       scope='Same exposed SAT populations. One 16-index paid pilot for nested recipes, heuristic KL/cost selection, then complete-call fallback. No free counterfactual direct-full-call cost estimate. All accepted evidence is checked positive proof. Warm installed runtime; histories and marginal controller/proposal/check/cleanup/journal costs recorded; common inputs/import/final artifact serialization excluded.')
    def save(stage):
        result['boundary']=dict(stage=stage,utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8');print(stage,flush=True)
    start=time.monotonic_ns();save('entered')
    try:
        for n in (60,100):
            definition=next(x['definition'] for x in reference['rows'] if x['definition']['n']==n)
            rng=random.Random(definition['seed']);N=definition['N']
            forms=tuple(proof.sat.formula(n,int(n*F(definition['ratio'])),rng) for _ in range(N))
            assert hashlib.sha256(json.dumps(forms).encode()).hexdigest()==definition['source_sha256']
            edits=[lit for i in range(1,5) for lit in (i,-i)]
            for mode in ('stat_full','stat_bounded','paid_pilot'):
                save('history_next_'+str(n)+'_'+mode);family=proof.ProofFamily(n,forms)
                margin_start=time.perf_counter_ns();requests=[]
                for j,lit in enumerate(edits):
                    if mode=='paid_pilot':r=pilot_request(family,lit,F(1,160),definition['seed']+j)
                    else:r=proof.request(family,lit,mode,F(1,160),definition['seed']+j)
                    r['realized_warrant_valid']=r['outcome']!='warrant_positive' or 2*definition['edited_sat'][j]>=N
                    requests.append(r)
                    with journal.open('a',encoding='utf-8') as f:f.write(json.dumps(dict(n=n,mode=mode,j=j,request=r),default=str)+'\n')
                family.close();marginal=time.perf_counter_ns()-margin_start
                rows.append(dict(definition=definition,mode=mode,requests=requests,history_ns=family.history_ns,
                                 marginal_ns=marginal,total_ns=family.history_ns+marginal,counts=dict(family.counts)))
                save('lifecycle_complete_'+str(n)+'_'+mode)
        result['status']='complete'
    except Exception:
        result.update(status='failed',failure=traceback.format_exc());raise
    finally:
        result.update(elapsed_ns=time.monotonic_ns()-start,end_utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='rows'},default=str))


if __name__=='__main__':main(Path(sys.argv[1]))
