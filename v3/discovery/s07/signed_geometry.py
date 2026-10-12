#!/usr/bin/env python3
"""Paid signed-geometry proof bridge; one small DEVELOPMENT construction.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. Three new transformed-source proof
calls and one cost audit. Signed geometry is checked before use; ordinary
definitional CNF and weighted objective complementation are not new methods.
"""
from datetime import datetime, timezone
import copy
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'s06'))
import native_repair as native
import contract_quote
import contract_guard
import joint_repair as joint

VERSION = 's07-signed-geometry-v1'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def transform(original, coefficient, meter):
    n, m = original['variables'], len(original['soft'])
    if original['identity'] != native.kernel.digest({k:v for k,v in original.items() if k!='identity'}):
        raise ValueError('Original source changed')
    if len(coefficient) != m or any(type(c) is not int for c in coefficient):
        raise ValueError('One integral coefficient per ordered original soft clause')
    hard = copy.deepcopy(original['hard'])
    mapping = []
    for j, soft in enumerate(original['soft']):
        v = n+j+1
        clause = list(soft['clause'])
        # v iff every original clause literal is false.
        hard.append([v]+clause)
        hard.extend([[-v, -literal] for literal in clause])
        mapping.append(dict(soft_index=j, variable=v, original_clause=clause))
        meter.pay('signed_compile', 'fresh_violation_definition_and_ordered_binding', 8+6*len(clause))
    witness = native.profile_kernel.compile_witness(original, original['public_incumbent'], meter)
    extended = witness['model'] | (witness['violation_mask'] << n)
    query = dict(row=original['row']+'-signed', variables=n+m, hard=hard,
        soft=[dict(weight=abs(c), clause=[-(n+j+1) if c>=0 else n+j+1]) for j,c in enumerate(coefficient)],
        public_incumbent=extended, objective_max=sum(map(abs, coefficient)),
        original_source=original['identity'], ordered_violation_binding=mapping,
        signed_coefficient=list(coefficient))
    query['identity'] = native.kernel.digest(query)
    offset = sum(-c for c in coefficient if c<0)
    meter.pay('signed_compile', 'source_copy_signed_weights_offset_and_identity',
              16+5*m+sum(1+len(c) for c in hard))
    return query, offset


def admit(original, coefficient, bound, query, receipt, meter):
    expected, offset = transform(original, coefficient, meter)
    if query != expected or type(bound) is not int:
        raise ValueError('Wrong exact definitional source or integral lower target')
    budget = offset+bound-1
    if (receipt['source_id'] != native.kernel.digest(expected) or receipt['budget'] != budget
            or receipt['receipt_id'] != native.kernel.digest({k:v for k,v in receipt.items() if k!='receipt_id'})):
        raise ValueError('Receipt belongs to a different transformed query')
    raw = receipt['provider_response']
    if raw['status'] != 'UNSAT':
        raise ValueError('A proposed inequality needs an actual checked negative proof')
    native.kernel.check_negative(expected, budget, raw['proof'], meter)
    leaves = native.profile_kernel.compile_tree(raw['proof'], meter)
    if leaves != receipt['leaf_masks'] or receipt['checked_lower'] != offset+bound:
        raise ValueError('Transformed proof compilation or integral lower changed')
    meter.pay('signed_check', 'exact_extension_projection_objective_identity_and_receipt_binding',
              24+8*len(coefficient)+native.kernel.proof_words(raw['proof']))
    result = dict(original_source=original['identity'], coefficient=list(coefficient), lower=bound,
                  objective_offset=offset, transformed_source=expected['identity'],
                  raw_proof_receipt=receipt['receipt_id'], checked=True)
    result['receipt_id'] = native.kernel.digest(result)
    return result


def gate(witnesses, costs, mandatory, price, meter):
    if mandatory['coefficient'] != [0,0,1] or mandatory['lower'] != 1 or not mandatory['checked']:
        raise ValueError('The specific admitted mandatory-coordinate geometry is required')
    answers = []
    for witness in witnesses:
        z = joint.bits(witness['violation_mask'], costs.m)
        values = []
        for k in costs.possible[0]:
            w = costs.modes[k]
            value = sum(a*b for a,b in zip(z,w))
            values.append(max(0, value-w[2], value-price))
            meter.pay('geometry_gate', 'feasible_cost_mandatory_lower_and_replacement_contrast', 2*costs.m+8)
        answers.append(dict(model=witness['model'], violation_mask=witness['violation_mask'],
                            bound=max(values), cost_source=costs.source_id,
                            logical_source=mandatory['original_source'], proof=mandatory['receipt_id']))
    meter.pay('geometry_gate', 'checked_fixed_action_minimum_and_record', len(answers)+12)
    return min(answers, key=lambda a:(a['bound'],a['model']))


def run(output):
    if output.exists():
        raise FileExistsError('Preserve signed-geometry acquisition and failed prefixes')
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    meter = native.kernel.Meter()
    original = dict(row='signed-derived-mandatory-pair', variables=4,
        hard=[[-1,3],[1,-3],[-2,-3],[2,3],[3,4],[-3,4]],
        soft=[dict(weight=1,clause=[-1]),dict(weight=1,clause=[-2]),dict(weight=1,clause=[-4])],
        public_incumbent=13,objective_max=3)
    original['identity'] = native.kernel.digest(original)
    data = dict(version=VERSION,possible_cost_modes=[[0,4,1],[0,4,100],[4,0,1],[4,0,100]],
                cohort_size=1,hidden_modes=[1],chosen_audit=dict(row=0,coordinate=0),price=105,tolerance=0)
    data['source_identity'] = native.kernel.digest(data)
    targets = [dict(coefficient=[0,0,1],lower=1), dict(coefficient=[1,1,0],lower=1),
               dict(coefficient=[-1,-1,0],lower=-1)]
    result = dict(version=VERSION,status='source_frozen_before_acquisition',evidence='DEVELOPMENT',
        contributor='ChatGPT (GPT-6 Astra Pro)',created_utc=datetime.now(timezone.utc).isoformat(),
        implementation_sha256=sha(__file__),original_source=original,cost_source=data,targets=targets,
        dependencies={str(Path(p).relative_to(HERE.parent.parent.parent)):sha(p) for p in
            [contract_quote.__file__,native.kernel.__file__,native.profile_kernel.__file__,joint.__file__]},
        acquisitions=[],signed_receipts=[],actual_new_proof_calls=0,actual_cost_audits=0,
        policy='Check all three frozen geometry targets, then inspect the single frozen coordinate0 audit. Select a checked fixed repair by mandatory-cost contrasts at p105,tau0. No hidden mode is an input to the gate.')
    def save(status):
        result['status'] = status
        result['local_invoice'] = meter.record()
        result['timing'] = dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall)
        output.write_text(json.dumps(result,indent=2)+'\n')
    save('source_frozen_before_acquisition')
    try:
        words = (len(Path(__file__).read_bytes())+7)//8
        meter.pay('signed_admission','bridge_code_words_and_hash_blocks',words+(words+7)//8+1)
        meter.pay('signed_admission','fixed_original_source_cost_modes_targets_and_policy_words',
                  32+sum(1+len(c) for c in original['hard'])+3*len(original['soft'])+12+sum(2+len(t['coefficient']) for t in targets))
        result['code_admission'] = contract_guard.admit()
        witnesses = [native.profile_kernel.compile_witness(original,m,meter) for m in (13,10)]
        result['checked_original_witnesses'] = witnesses
        prepared = []
        for target in targets:
            query, offset = transform(original,target['coefficient'],meter)
            prepared.append(dict(query=query,offset=offset,budget=offset+target['lower']-1))
        result['prepared_queries'] = prepared
        save('all_derived_sources_frozen_before_first_call')
        for index,(target,prepared_query) in enumerate(zip(targets,prepared)):
            result['active_acquisition'] = dict(kind='complete',index=index,query_identity=prepared_query['query']['identity'],budget=prepared_query['budget'])
            save('before_actual_complete_call')
            raw = contract_quote.execute_complete(prepared_query['query'],prepared_query['budget'])
            result['acquisitions'].append(dict(kind='complete',index=index,response=raw))
            result['actual_new_proof_calls'] += 1
            save('raw_complete_receipt_retained_before_projection')
            receipt = admit(original,target['coefficient'],target['lower'],prepared_query['query'],raw,meter)
            result['signed_receipts'].append(receipt)
            meter.pay('output','derived_geometry_receipt_record',24+len(target['coefficient']))
            save('derived_original_source_inequality_admitted')
        result['derived_equalities'] = [dict(coefficient=[0,0,1],value=1,
            lower_receipt=result['signed_receipts'][0]['receipt_id'],upper='Boolean original violation variable <=1'),
            dict(coefficient=[1,1,0],value=1,lower_receipt=result['signed_receipts'][1]['receipt_id'],
                 upper_receipt=result['signed_receipts'][2]['receipt_id'])]
        meter.pay('geometry_compile','two_signed_inequalities_and_boolean_upper',18)
        costs = joint.CostState(data['possible_cost_modes'],1,data['source_identity'],meter)
        result['before_audit'] = gate(witnesses,costs,result['signed_receipts'][0],data['price'],meter)
        oracle = joint.CostOracle(data)
        result['active_acquisition'] = dict(kind='audit',**data['chosen_audit'])
        save('before_frozen_actual_coordinate_audit')
        observed = oracle.audit(**data['chosen_audit'])
        result['acquisitions'].append(dict(kind='audit',receipt=observed))
        result['actual_cost_audits'] += 1
        save('raw_audit_retained_before_update')
        costs.observe(observed)
        result['final_answer'] = gate(witnesses,costs,result['signed_receipts'][0],data['price'],meter)
        result['final_cost_state'] = costs.snapshot()
        if result['final_answer']['bound'] != 0 or costs.possible != [(0,1)]:
            raise AssertionError('Constructed paid geometry gate failed')
        meter.pay('output','final_source_bound_fixed_action_and_invoice',32)
        proof_units = sum(a['response']['total_operation_units'] for a in result['acquisitions'] if a['kind']=='complete')
        result['invoice'] = dict(local_preparation_checking_gate_units=meter.total,
            complete_proof_wrapper_and_provider_units=proof_units,audit_provider_software_units=4,
            complete_code_admission_units=result['code_admission']['declared_admission_units'],
            total_named_units=meter.total+proof_units+4+result['code_admission']['declared_admission_units'],
            external_proof_calls=3,external_cost_audits=1,
            full_cost='Named U plus actual proof/audit fees, CPU/wall, storage/byte-time and all remaining host costs; unassigned rates are not zero.')
        result.pop('active_acquisition',None)
        save('complete')
    except BaseException as exc:
        result['error'] = dict(type=type(exc).__name__,message=str(exc))
        save('failed_or_interrupted_prefix')
        raise
    print(json.dumps(dict(status=result['status'],proof_calls=3,audits=1,before=result['before_audit']['bound'],
        final=result['final_answer'],invoice=result['invoice'])))


if __name__ == '__main__':
    run(Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'signed_geometry_results.json')
