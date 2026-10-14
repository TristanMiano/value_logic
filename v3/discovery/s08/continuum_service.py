#!/usr/bin/env python3
"""Paid off-menu continuum service with checked polynomial regions.
DEVELOPMENT, Codex (GPT-6), 2026-10-14.
"""
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction as F
from math import comb
from pathlib import Path
import copy
import json
import sys
import time
import g01
import action_audits as aa
import star_learning as base
import markov_paths as mk
import markov_service as ms
import continuum_policy as cp

HERE=Path(__file__).resolve().parent
VERSION='s08-continuum-service-v1'
ARMS=('full','static','learner','ordinary_learner','plugin')
BINS=64
EPSILON=F(1,10)
Meter=g01.kernel.Meter


def source(costs):
    data=ms.source(costs);data.pop('identity');data.pop('repeat_numerators')
    data['bit_source']='Fresh stationary symmetric homogeneous Markov indicator rows; fixed rho in [0,1]'
    return g01.seal(data)


def independent_restrict(coeff,lo,hi,meter):
    """Power-basis substitution checks de Casteljau by different arithmetic."""
    d=len(coeff)-1;power=[F(0)]*(d+1)
    for k,c in enumerate(coeff):
        for j in range(d-k+1):
            power[k+j]+=c*comb(d,k)*comb(d-k,j)*(-1)**j
            meter.pay('table_check','bernstein_to_power',4)
    local=[F(0)]*(d+1)
    for i,c in enumerate(power):
        for j in range(i+1):
            local[j]+=c*comb(i,j)*lo**(i-j)*(hi-lo)**j
            meter.pay('table_check','affine_power_substitution',6)
    result=[]
    for k in range(d+1):
        result.append(sum(local[j]*F(comb(k,j),comb(d,j)) for j in range(k+1)))
        meter.pay('table_check','power_to_local_bernstein',3*(k+1))
    return result


def table_for(polynomials,with_masks,meter):
    result=[]
    for j in range(BINS):
        lo,hi=F(j,BINS),F(j+1,BINS)
        local={r:cp.restrict(coeff,lo,hi,meter) for r,coeff in polynomials.items()}
        upper={r:max(coeff) for r,coeff in local.items()};allowed=[]
        meter.pay('table_prepare','fee_coefficient_maxima',sum(len(c) for c in local.values()))
        if with_masks:
            for r in local:
                maximum=max(max(a-b for a,b in zip(local[r],local[q])) for q in local)
                if maximum<=EPSILON:allowed.append(r)
                meter.pay('table_prepare','pairwise_regret_coefficient_maxima',2*len(local)*len(local[r]))
        result.append(dict(interval=[lo,hi],local=local,upper=upper,allowed=allowed))
    return result


def check_table(polynomials,table,with_masks,meter):
    if len(table)!=BINS:raise ValueError('Incomplete continuum cover')
    for j,row in enumerate(table):
        lo,hi=F(j,BINS),F(j+1,BINS)
        if row['interval']!=[lo,hi] or set(row['local'])!=set(polynomials):raise ValueError('Table scope')
        if set(row['upper'])!=set(polynomials):raise ValueError('Fee scope')
        local={r:independent_restrict(coeff,lo,hi,meter) for r,coeff in polynomials.items()}
        if row['local']!=local or row['upper']!={r:max(c) for r,c in local.items()}:raise ValueError('Invalid region coefficient or fee')
        allowed=[]
        if with_masks:
            for r in local:
                if all(all(a-b<=EPSILON for a,b in zip(local[r],local[q])) for q in local):allowed.append(r)
                meter.pay('table_check','all_pairwise_regret_inequalities',2*len(local)*len(local[r]))
        if row['allowed']!=allowed:raise ValueError('Invalid acceptable policy mask')


def prepare(directory,label,data,arm,meter):
    if arm=='full':return {},{},[],None
    bank={};polynomials={};proofs={}
    for r in mk.MENU:
        policy=mk.plan(data['audit_costs'],r);bank[r]=policy['roots']
        proof=cp.produce(data['audit_costs'],bank[r]);checked=cp.check_polynomial(data['audit_costs'],bank[r],proof)
        meter.pay('preparation','model_policy_proposal',policy['invoice']['total'])
        meter.pay('preparation','continuum_polynomial_production',proof['invoice']['total'])
        meter.pay('preparation','independent_polynomial_identity_check',checked['total'])
        polynomials[r]=proof['coefficients'];proofs[r]=dict(roots=bank[r],proof=proof,checking=checked)
    if arm=='plugin':table=[]
    else:
        with_masks=arm in ('learner','ordinary_learner')
        table=table_for(polynomials,with_masks,meter);check_table(polynomials,table,with_masks,meter)
    artifact=cp.normalize(dict(source=data['identity'],policies=proofs,table=table,epsilon=EPSILON))
    g01.save(directory/f'{label}_{arm}_bank.json',artifact)
    return bank,polynomials,table,g01.sha(directory/f'{label}_{arm}_bank.json')


def table_select(table,interval,may_stop,meter):
    lo,hi=interval
    relevant=[row for row in table if row['interval'][0]<=hi and row['interval'][1]>=lo]
    if not relevant:raise ValueError('Uncovered source region')
    meter.pay('selection','scan_intersected_certified_bins',2*len(table))
    shared=set(mk.MENU)
    if may_stop:
        for row in relevant:shared &=set(row['allowed'])
        meter.pay('selection','intersect_acceptable_policy_masks',len(relevant)*len(mk.MENU))
    else:shared=set()
    upper={r:max(row['upper'][r] for row in relevant) for r in mk.MENU}
    meter.pay('selection','maximum_fee_across_relevant_bins',len(relevant)*len(mk.MENU))
    chosen=min(shared) if shared else min(mk.MENU,key=lambda r:(upper[r],r))
    return chosen,upper[chosen],bool(shared),len(relevant)


def run_arm(directory,case,data,rows,arm):
    meter=Meter();cpu=time.process_time_ns();wall=time.perf_counter_ns()
    if data!=source(data['audit_costs']):raise ValueError('Original continuum source mismatch')
    meter.pay('source','read_original_path_factors_and_continuum_source',24+data['n']+sum(len(c)+1 for c in data['hard'])+5*len(data['features']))
    bank,polynomials,table,bank_hash=prepare(directory,case['name'],data,arm,meter);setup=meter.total
    samples=success=fees=audits=epochs=0;interval=[F(0),F(1)];frozen=False;stop_row=None;selected=Counter();coverage_failures=0
    chosen=bound=None;next_update=True;regret_sum=worst_regret=F(0);decisions=[]
    # Diagnostics only: never passed to table_select, cp.evaluate selection, or the provider.
    diagnostic_values={r:cp.evaluate(coeff,F(case['r'],10)) for r,coeff in polynomials.items()}
    diagnostic_opt=min(diagnostic_values.values()) if diagnostic_values else F(0)
    trace_path=directory/f"{case['name']}_{arm}.jsonl";diag_path=directory/f"{case['name']}_{arm}_diag.jsonl"
    with trace_path.open('w',encoding='utf-8') as trace,diag_path.open('w',encoding='utf-8') as diag:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],version=VERSION,arm=arm,bank_sha256=bank_hash))+'\n');trace.flush()
        for t,row in enumerate(rows):
            before=meter.total
            if arm=='full':roots=None;bound=sum(data['audit_costs'])
            else:
                if next_update:
                    if arm=='plugin':
                        estimate=F(success,samples) if samples else F(1,2)
                        chosen=min(bank,key=lambda r:(cp.evaluate(polynomials[r],estimate),r));bound=None
                        meter.pay('selection','plug_in_exact_polynomial_comparison',6*len(bank)*data['n']);epochs+=1
                        payload=dict(estimate=estimate,selected=chosen,samples=samples)
                    else:
                        if arm!='static':
                            lo,hi=base.confidence(samples,success,1,meter)
                            interval=[max(interval[0],lo),min(interval[1],hi)]
                            if interval[0]>interval[1]:raise ValueError('Empty statistical interval; preserve failed run')
                        chosen,bound,frozen,bincount=table_select(table,interval,arm!='static',meter)
                        if frozen:stop_row=t
                        epochs+=1;payload=dict(interval=interval,selected=chosen,samples=samples,fee_upper=bound,
                            certified_epsilon_optimal=frozen,intersected_bins=bincount)
                    decisions.append(dict(before_request=t,**payload))
                    trace.write(json.dumps(dict(kind='decision_epoch',before_request=t,**payload),default=g01.encode)+'\n');trace.flush()
                    next_update=False
                else:meter.pay('selection','reuse_admitted_policy_epoch',1)
                roots=bank[chosen];selected[str(chosen)]+=1
            request=f"{case['name']}-{arm}-{t}"
            trace.write(json.dumps(dict(kind='plan',request=request,policy=chosen,fee_upper=bound,learning_frozen=frozen),default=g01.encode)+'\n');trace.flush()
            provider=base.Provider(data,row,request,trace,meter)
            receipts=ms.acquire(provider,data['n'],roots,meter);action=base.construct(data,receipts,request,meter);base.check(data,receipts,action,meter)
            paid=sum(r['base_fee'] for r in receipts);fees+=paid;audits+=len(receipts)
            trace.write(json.dumps(dict(kind='output',request=request,action=action,base_fee=paid,
                physical_audits=len(receipts),named_units=meter.total-before),separators=(',',':'))+'\n');trace.flush()
            assert aa.direct_regret(data,action['assignment'],row)==0
            excess=diagnostic_values[chosen]-diagnostic_opt if chosen is not None else F(0)
            regret_sum+=excess;worst_regret=max(worst_regret,excess)
            covered=interval[0]<=F(case['r'],10)<=interval[1];coverage_failures+=not covered
            diag.write(json.dumps(dict(request=t,hidden=row,action_regret=0,conditional_expected_bank_fee_excess=excess,
                true_parameter_covered=covered,certified_epsilon_claim=frozen),default=g01.encode,separators=(',',':'))+'\n')
            if frozen and covered:assert excess<=EPSILON
            if arm in ('learner','ordinary_learner','plugin') and not frozen and receipts[0]['value']==1:
                assert len(receipts)>=2 and abs(receipts[0]['node']-receipts[1]['node'])==1
                samples+=1;success+=int(receipts[1]['value']==1)
                meter.pay('learning','retain_compulsory_pair_count',8+samples.bit_length()+success.bit_length())
                trace.write(json.dumps(dict(kind='pair_count',request=t,first=receipts[0]['identity'],next=receipts[1]['identity'],
                    samples=samples,repeats=success))+'\n');trace.flush()
                if samples&(samples-1)==0:next_update=True
    return dict(outputs=len(rows),base_audit_fee=fees,physical_audits=audits,named_units=meter.total,setup_units=setup,
        invoice=meter.record(),learning_samples=samples,repeats=success,decision_epochs=epochs,decisions=decisions,
        stop_before_request=stop_row,final_interval=interval,selected_policies=dict(selected),observed_coverage_failures=coverage_failures,
        cumulative_expected_bank_fee_regret=regret_sum if chosen is not None else None,
        worst_conditional_expected_bank_fee_regret=worst_regret if chosen is not None else None,
        diagnostic_bank_values=diagnostic_values,trace_bytes=trace_path.stat().st_size,diagnostic_bytes=diag_path.stat().st_size,
        arm_cpu_ns=time.process_time_ns()-cpu,arm_wall_ns=time.perf_counter_ns()-wall)


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    previous=json.loads((HERE/'ms01/design.json').read_text());costs=[previous['cases'][i]['costs'] for i in (0,3,6)];cases=[]
    for fee in costs:
        for r in (2,4,8):cases.append(dict(name=f'n{len(fee)}r{r}',costs=fee,r=r,seed=8141470+len(cases)))
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,requests=1024,arms=ARMS,bins=BINS,epsilon=EPSILON,
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'continuum_service.md'),
        dependencies={name:g01.sha(HERE/name) for name in ('continuum_policy.py','markov_service.py','markov_paths.py','star_learning.py','action_audits.py','g01.py')}))
    result=dict(status='running',cases=[])
    for case in cases:
        data=source(case['costs']);rows=ms.draw(data['n'],case['r'],1024,case['seed']);record=dict(name=case['name'],arms={})
        for arm in ARMS:
            record['arms'][arm]=run_arm(directory,case,data,rows,arm)
            g01.save(directory/'progress.json',dict(completed=result['cases'],current=record))
        for key in ('base_audit_fee','physical_audits','named_units','learning_samples','stop_before_request','selected_policies'):
            assert record['arms']['learner'][key]==record['arms']['ordinary_learner'][key]
        result['cases'].append(record);g01.save(directory/'results.json',result)
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat());g01.save(directory/'results.json',result)
    print(json.dumps(dict(status='complete',cases=[dict(name=c['name'],arms={a:{k:v[k] for k in
        ('base_audit_fee','named_units','learning_samples','stop_before_request','cumulative_expected_bank_fee_regret')}
        for a,v in c['arms'].items()}) for c in result['cases']]),default=g01.encode))


if __name__=='__main__':run(Path(sys.argv[1]))
