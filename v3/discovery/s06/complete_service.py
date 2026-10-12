#!/usr/bin/env python3
"""An executable complete finite-source fallback, with full paid receipts.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. Complete means within
the quoted operation/observation caps during normal uninterrupted execution,
not a hard CPU/wall bound or a guarantee against host interruption.
"""
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
import time

import contract_guard
import contract_quote
import joint_repair as joint
import native_repair as native
import native_stream as stream

HERE=Path(__file__).resolve().parent


def execute(input_path,output):
    if output.exists():
        raise FileExistsError('Preserve actual calls and observations')
    cpu,wall=time.process_time_ns(),time.perf_counter_ns()
    data=json.loads(input_path.read_text())
    oracle=joint.CostOracle(data)
    archive,initial,admission=stream.admit_existing_cache()
    if joint.sha(joint.S05/'maxsat_repair_results.json')!=data['logical_archive_sha256']:
        raise ValueError('Logical source changed')
    code_admission=contract_guard.admit()
    meter=native.kernel.Meter()
    meter.pay('cost_manifest_admission','read_words_and_sha_blocks',(input_path.stat().st_size+7)//8+(input_path.stat().st_size+72)//64)
    costs=joint.CostState(data['possible_cost_modes'],data['cohort_size'],data['source_identity'],meter)
    modes=costs.modes
    if len({(v[0],v[1]) for v in modes})!=len(modes):
        raise ValueError('The admitted two-coordinate identification contract is unavailable')
    if any(d['price']!=48 or d['tolerance']!=4 for d in data['schedule']):
        raise ValueError('This saved four-call ceiling is for p48, tau4')
    result=dict(status='running',evidence='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                start_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=native.sha(__file__),
                source_sha256=native.sha(input_path),source_identity=data['source_identity'],
                initial_admission=admission,complete_code_admission=code_admission,
                planned_contract=dict(max_external_observations=2*costs.n,max_complete_calls=4*len(data['schedule']),
                    per_request_clipped_gap=48,tolerance=4,worst_gap_sequence=[48,24,12,6,3],
                    quote_scope='Declared provider/checker tariff on pinned finite source code; exact known finite cohort after audited identification. CPU/wall/host survival not bounded.'),
                audits=[],requests=[],calls=[])
    def save():
        output.write_text(json.dumps(result,indent=2)+'\n')
    save()
    # Public mode identification; no read of hidden_modes except inside the
    # paid oracle. Earlier identified rows are not audited again.
    for row in range(costs.n):
        for coordinate in (0,1):
            if len(costs.possible[row])==1:
                break
            receipt=oracle.audit(row,coordinate)
            costs.observe(receipt)
            result['audits'].append(receipt)
            save()
        if len(costs.possible[row])!=1:
            raise ValueError('Mode identification did not finish under the declared source')
    weights=[sum(costs.modes[choices[0]][j] for choices in costs.possible) for j in range(costs.m)]
    meter.pay('cost_update','cohort_sum_from_identified_rows',costs.n*costs.m+costs.m)
    bank=stream.CompactBank(initial,meter)
    bank.set_weights(weights)
    wrapper_units=0
    for index,duty in enumerate(data['schedule']):
        row,price,tau=duty['row'],duty['price'],duty['tolerance']
        instance=archive['instances'][row]
        before=bank.bounds(row)
        bounds=before
        indices=[]
        while min(bounds['upper'],price)-min(bounds['lower'],price)>tau:
            u,l=min(bounds['upper'],price),min(bounds['lower'],price)
            budget=(u+l)//2
            meter.pay('complete_controller','clipped_bracket_and_balanced_budget',8)
            weighted=native.weighted_instance(instance,weights)
            # The loaded immutable quote/provider/compiler were actually
            # admitted above. Every new result is still independently checked.
            got=contract_quote.execute_complete(weighted,budget)
            wrapper_units+=got['total_operation_units']
            response=dict(source_identity=weighted['identity'],witness=got.get('witness'),checked_lower_receipt=None)
            if 'leaf_masks' in got:
                response['checked_lower_receipt']=dict(checked=True,receipt_id=got['receipt_id'],
                    leaf_masks=got['leaf_masks'],budget=budget,dependency='complete-call raw branching proof')
            call_id=len(result['calls'])
            bank.retain(row,response,call_id)
            next_bounds=bank.bounds(row)
            new_gap=min(next_bounds['upper'],price)-min(next_bounds['lower'],price)
            assert new_gap<=(u-l)//2
            result['calls'].append(dict(call=call_id,request=index,row=row,weights=weights,budget=budget,
                                        before=bounds,after=next_bounds,checked_call=got))
            indices.append(call_id)
            bounds=next_bounds
            save()
            if len(indices)>4:
                raise AssertionError('The finite delivery ceiling was exceeded')
        u,l=min(bounds['upper'],price),min(bounds['lower'],price)
        action='repair' if bounds['upper']<price else 'replace'
        result['requests'].append(dict(request=index,row=row,logical_source_id=instance['identity'],
                                      cost_source_id=costs.source_id,weights=weights,price=price,tolerance=tau,
                                      status='checked_action',action=action,model=bounds['model'] if action=='repair' else None,
                                      witness_id=bounds['witness_id'] if action=='repair' else None,proof_id=bounds['proof_id'],
                                      action_cost=u,regret_bound=u-l,before=before,after=bounds,
                                      closed_from_cache=min(before['upper'],price)-min(before['lower'],price)<=tau,
                                      complete_call_indices=indices))
        meter.pay('output','action_receipt_invoice_fields',24)
        save()
    assert len(result['audits'])<=2*costs.n and len(result['calls'])<=4*len(data['schedule'])
    result.update(status='complete',end_utc=datetime.now(timezone.utc).isoformat(),
                  final_cost_state=costs.snapshot(),final_cache=bank.rows,
                  summary=dict(checked_requests=len(result['requests']),cost_observations=len(result['audits']),
                               complete_branch_calls=len(result['calls']),new_native_calls=0,
                               cache_hits=sum(r['closed_from_cache'] for r in result['requests']),
                               summed_action_cost=sum(r['action_cost'] for r in result['requests']),
                               largest_certified_regret=max(r['regret_bound'] for r in result['requests'])),
                  invoice=dict(common_raw_admission_units=admission['total_declared_units'],
                               complete_code_admission_units=code_admission['declared_admission_units'],
                               complete_call_wrapper_units=wrapper_units,controller_and_cost_operations=meter.record(),
                               audit_provider_software_units=4*len(result['audits']),external_audit_count=len(result['audits']),
                               native_search_units=0,external_audit_monetary_price=None,
                               historical_acquisition_common_units=77646,
                               limitations='Named operation tariffs and measured CPU/wall; serialization/allocator/storage bytes timed but not fully priced. One actual retained code admission shared across calls. No runtime/economic superiority claim.'),
                  storage=dict(cache_serialized_bytes=len(joint.canonical(bank.rows)),
                               raw_receipt_archive_bytes_before_final_write=output.stat().st_size),
                  timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))
    save()
    print(json.dumps(result['summary']|dict(wrapper_units=wrapper_units,controller_units=meter.total,timing=result['timing'])))


if __name__=='__main__':
    execute(Path(sys.argv[1]),Path(sys.argv[2]))
