#!/usr/bin/env python3
"""Independently reconstruct saved s07 acquisition traces; no new purchases.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. Raw initial proofs,
new complete/native negative trees, positive models and cost receipts are
checked again, in actual request order. Exact finite diagnostic regret is
computed from freshly checked feasible models only inside this verifier;
no controller receives these models, optima or hidden cost modes.
"""
from __future__ import annotations
from datetime import datetime, timezone
from fractions import Fraction as F
import copy
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'s06'))
import contract_quote
import joint_repair as joint
import joint_repair_v2 as compiled
import native_repair as native
import native_stream as stream
from repair_interface import RepairEvaluator


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encode(v):
    if isinstance(v,F):
        return v.numerator if v.denominator == 1 else str(v)
    raise TypeError(type(v).__name__)


def same(actual,expected,label):
    if actual != expected:
        raise AssertionError(dict(label=label,actual=actual,expected=expected))


def finite_masks(instance,meter):
    masks=set()
    for model in range(1 << instance['variables']):
        try:
            got=native.profile_kernel.compile_witness(instance,model,meter)
        except ValueError:
            continue
        masks.add(got['violation_mask'])
    if not masks:
        raise AssertionError('Admitted source lost its checked feasible incumbent')
    return sorted(masks)


def semantic_regret(mask,price,feasible,costs,meter):
    """Exact finite-source worst regret; no cost-row-product enumeration."""
    def support(coefficient):
        result=0
        for row in costs.possible:
            values=[sum(a*w for a,w in zip(coefficient,costs.modes[k])) for k in row]
            result += max(values)
            meter.pay('diagnostic','finite_model_cohort_support',len(row)*(2*costs.m+1)+2)
        return result
    bits=lambda z:tuple((z >> j)&1 for j in range(costs.m))
    if mask is None:
        return max([F(0)]+[price+support(tuple(-a for a in bits(z))) for z in feasible])
    u=bits(mask)
    values=[F(0),support(u)-price]
    values += [support(tuple(a-b for a,b in zip(u,bits(z)))) for z in feasible]
    return max(values)


def check_answer(stored,row,price,tau,evaluator,costs,feasible,meter):
    got=evaluator.evaluate(row,price,tau)
    for key in ('action','model','mask','method'):
        same(got[key],stored[key],'reconstructed output '+key)
    same(got['bound'],F(stored['bound']),'reconstructed output bound')
    same(got['cost_source_id'],stored['cost_source_id'],'output cost source')
    same(got['logical_source_id'],stored['logical_source_id'],'output logical source')
    exact=semantic_regret(got['mask'],F(price),feasible[row],costs,meter)
    if exact > got['bound']:
        raise AssertionError('Uniform certificate is below exact diagnostic regret')
    return dict(bound=got['bound'],exact_finite_regret=exact,slack=got['bound']-exact)


def check_complete(event,instance,meter):
    q,budget,response=event['weights'],event['budget'],event['response']
    weighted=native.weighted_instance(instance,q)
    same(response['source_id'],native.kernel.digest(weighted),'complete weighted source')
    same(response['budget'],budget,'complete budget')
    same(response['receipt_id'],native.kernel.digest({k:v for k,v in response.items() if k!='receipt_id'}),'complete receipt bytes')
    quote=contract_quote.finite_call_quote(weighted)
    same(response['quote'],quote,'admitted complete provider tariff')
    raw=response['provider_response']
    if raw['status']=='SAT':
        witness=native.profile_kernel.compile_witness(weighted,raw['model'],meter)
        same(witness,response['witness'],'complete positive witness')
        if witness['original_cost']>budget:
            raise AssertionError('Positive witness exceeds purchased budget')
    elif raw['status']=='UNSAT':
        native.kernel.check_negative(weighted,budget,raw['proof'],meter)
        leaves=native.profile_kernel.compile_tree(raw['proof'],meter)
        same(leaves,response['leaf_masks'],'raw negative compilation')
        same(response['checked_lower'],budget+1,'negative lower')
    else:
        raise AssertionError('Complete normal-execution contract did not complete')
    same(response['total_operation_units'],response['wrapper_invoice']['total']+raw['invoice']['total'],'complete invoice sum')
    if response['total_operation_units']>quote['complete_wrapper_units']:
        raise AssertionError('Complete call exceeded named quote')
    retained=dict(source_identity=instance['identity'],witness=response.get('witness'),checked_lower_receipt=None)
    if 'leaf_masks' in response:
        retained['checked_lower_receipt']=dict(checked=True,receipt_id=response['receipt_id'],leaf_masks=response['leaf_masks'],budget=budget)
    return retained,raw['status']


def check_native(event,instance,meter):
    q,budget,response=event['weights'],event['budget'],event['response']
    weighted=native.weighted_instance(instance,q)
    same(response['source_identity'],weighted['identity'],'native weighted source')
    same(response['structural_source_id'],native.structural_id(instance),'native structure')
    same(response['weights'],q,'native weights')
    same(response['requested_budget'],budget,'native requested budget')
    if response.get('witness') is not None:
        witness=native.profile_kernel.compile_witness(weighted,response['witness']['model'],meter)
        same(witness,response['witness'],'native proposed model independently checked')
        if response['status']=='SAT' and not response['exact_requested'] and witness['original_cost']>budget:
            raise AssertionError('Native SAT model exceeds requested budget')
    lower=response.get('checked_lower_receipt')
    if lower is not None:
        same(lower['source_identity'],weighted['identity'],'native negative weighted source')
        same(lower['structural_source_id'],native.structural_id(instance),'native negative structure')
        same(lower['weights'],q,'native negative objective')
        native.kernel.check_negative(weighted,lower['budget'],lower['proof'],meter)
        leaves=native.profile_kernel.compile_tree(lower['proof'],meter)
        same(leaves,lower['leaf_masks'],'native raw negative compilation')
        same(lower['receipt_id'],native.kernel.digest(dict(source=weighted['identity'],budget=lower['budget'],proof=lower['proof'])),'native proof identity')
        if lower.get('checked') is not True:
            raise AssertionError('Retained native negative was never admitted')
    if response['status']=='UNSAT' and lower is None:
        raise AssertionError('Native status without a checked lower')
    return response,response['status']


def check_run(path,data,archive,initial,feasible,diagnostic):
    path=path.resolve()
    saved=json.loads(path.read_text())
    same(saved['status'],'complete','run completion')
    same(saved['source_sha256'],sha(HERE.parent/'s06'/'joint_source.json'),'cost source bytes')
    manifest=json.loads(path.with_name('manifest.json').read_text())
    for f in manifest['files']:
        snapshot=HERE/f['snapshot']
        same(sha(snapshot),f['sha256'],'executed source snapshot')
    same(saved['implementation_sha256'],sha(path.with_name('bundle_service.py')),'executed controller bytes')
    results=[]
    for arm in saved['arms']:
        meter=native.kernel.Meter()
        costs=compiled.CompiledCosts(data['possible_cost_modes'],data['cohort_size'],data['source_identity'],meter)
        bank=stream.CompactBank(initial,meter)
        evaluator=RepairEvaluator(archive['instances'],bank,costs,meter)
        counts=dict(audit=0,complete=0,native=0,SAT=0,UNSAT=0,UNRESOLVED=0)
        checked=[]
        cursor=0
        for request,duty in zip(arm['requests'],data['schedule'],strict=True):
            index,row=request['request'],duty['row']
            same((request['row'],request['price'],request['tolerance']),(row,duty['price'],duty['tolerance']),'request duty')
            before=check_answer(request['before'],row,duty['price'],duty['tolerance'],evaluator,costs,feasible,diagnostic)
            indices=[]
            while cursor<len(arm['events']) and arm['events'][cursor]['request']==index:
                event=arm['events'][cursor]
                counts[event['kind']]+=1
                if event['kind']=='audit':
                    receipt=event['receipt']
                    # Source outcome is checked only here in the diagnostic
                    # verifier, never supplied to a controller's public input.
                    same(receipt['provider_call'],counts['audit']-1,'actual audit call sequence')
                    same(receipt['value'],data['possible_cost_modes'][data['hidden_modes'][receipt['row']]][receipt['coordinate']],'committed audit truth')
                    costs.observe(receipt)
                    same(costs.snapshot(),event['state'],'post-audit admitted state')
                else:
                    same(event['row'],row,'purchase logical row')
                    checker=check_complete if event['kind']=='complete' else check_native
                    retained,status=checker(event,archive['instances'][row],meter)
                    counts[status]+=1
                    bank.retain(row,retained,cursor)
                indices.append(cursor)
                cursor+=1
            same(request['event_indices'],indices,'actual event interval')
            same(costs.snapshot(),request['cost_state'],'output admitted cost state')
            after=check_answer(request['answer'],row,duty['price'],duty['tolerance'],evaluator,costs,feasible,diagnostic)
            if request['status']=='checked_action' and after['bound']>duty['tolerance']:
                raise AssertionError('Requested tolerance not reached')
            checked.append(dict(request=index,before=before,after=after))
        same(cursor,len(arm['events']),'complete chronological event consumption')
        same(bank.rows,arm['final_profiles'],'final profile built only from checked chronological receipts')
        same(costs.snapshot(),arm['final_cost_state'],'final cost state')
        results.append(dict(policy=arm['policy'],requests=len(checked),counts=counts,
                            final_outputs_with_strict_certificate_slack=sum(c['after']['slack']>0 for c in checked),
                            largest_final_exact_regret=max(c['after']['exact_finite_regret'] for c in checked),
                            reconstruction_invoice=meter.record(),outputs=checked))
    return dict(path=str(path.relative_to(HERE.parent.parent.parent)),sha256=sha(path),arms=results)


def run(output,inputs):
    if output.exists():
        raise FileExistsError('Preserve checker results')
    cpu,wall=time.process_time_ns(),time.perf_counter_ns()
    data=json.loads((HERE.parent/'s06'/'joint_source.json').read_text())
    archive,initial,admission=stream.admit_existing_cache()
    diagnostic=native.kernel.Meter()
    feasible=[finite_masks(instance,diagnostic) for instance in archive['instances']]
    results=[check_run(path,data,archive,initial,feasible,diagnostic) for path in inputs]
    result=dict(status='passed',evidence='DEVELOPMENT independent reconstruction',
        contributor='ChatGPT (GPT-6 Astra Pro)',created_utc=datetime.now(timezone.utc).isoformat(),
        checker_sha256=sha(__file__),initial_raw_admission=admission,runs=results,
        feasible_mask_counts=list(map(len,feasible)),diagnostic_invoice=diagnostic.record(),
        actual_new_acquisition_calls=0,
        scope='Checker enumerates logical assignments for exact finite semantic validation; controllers did not receive them. No hidden-source outcomes enter acquisition policies.',
        timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))
    output.write_text(json.dumps(result,indent=2,default=encode)+'\n')
    print(json.dumps(dict(status='passed',runs=len(results),arms=sum(len(r['arms']) for r in results),checked_outputs=sum(a['requests'] for r in results for a in r['arms']),actual_new_acquisition_calls=0)))


if __name__=='__main__':
    run(Path(sys.argv[1]),list(map(Path,sys.argv[2:])))
