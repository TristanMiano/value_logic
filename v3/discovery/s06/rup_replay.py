#!/usr/bin/env python3
"""Re-admit raw RUP dependencies and replay every action gate, zero search."""
from datetime import datetime,timezone
import copy
import json
from pathlib import Path
import sys
import time

import native_repair as native
import native_stream as stream
import rup_bridge_v2 as rup

HERE=Path(__file__).resolve().parent


def run(path,output):
    if output.exists():
        raise FileExistsError('Preserve admission results')
    cpu,wall=time.process_time_ns(),time.perf_counter_ns()
    data=json.loads(path.read_text())
    if data['implementation_sha256']!=native.sha(HERE/'rup_stream.py'):
        raise ValueError('Different executed stream version')
    archive,initial,admission=stream.admit_existing_cache()
    meter=native.kernel.Meter()
    meter.pay('archive_read','words_and_sha_blocks',(path.stat().st_size+7)//8+(path.stat().st_size+72)//64)
    outcomes=[]
    for arm in data['arms']:
        bank=stream.CompactBank(initial,meter)
        row_cuts={i:[] for i in range(len(initial))}
        checked_proofs=checked_witnesses=resident_links=0
        purchases_by_request={}
        prior_states={}
        for purchase in arm['purchases']:
            purchases_by_request.setdefault(purchase['request'],[]).append(purchase)
        for request in arm['requests']:
            row=request['row']
            instance=archive['instances'][row]
            bank.set_weights(request['weights'])
            before=bank.bounds(row)
            assert before==request['before']
            for purchase in purchases_by_request.get(request['request'],[]):
                response=purchase['response']
                assert response['structural_source_id']==native.structural_id(instance)
                assert response['weights']==request['weights']
                wb=native.weighted_instance(instance,response['weights'])
                assert wb['identity']==response['source_identity']
                checked=copy.deepcopy(response)
                for key in ('sat_object_id','highs_object_id','state_id'):
                    assert response['state_before'][key]==response['state_after'][key]
                    if row in prior_states:
                        assert prior_states[row][key]==response['state_before'][key]
                if row in prior_states:
                    resident_links+=1
                prior_states[row]=response['state_after']
                if response.get('witness') is not None:
                    w=native.profile_kernel.compile_witness(wb,response['witness']['model'],meter)
                    assert w['violation_mask']==response['witness']['violation_mask']
                    assert w['original_cost']==response['witness']['original_cost']
                    checked['witness']=w
                    checked_witnesses+=1
                for event in response['events']:
                    if event['kind']!='separate_rup_proof_provider':
                        continue
                    paid=event['purchase']
                    if paid.get('checked_lower_receipt') is None:
                        continue
                    cut=rup.check_export(instance,paid,meter)
                    assert cut==paid['checked_lower_receipt']
                    if not any(c['receipt_id']==cut['receipt_id'] for c in row_cuts[row]):
                        row_cuts[row].append(cut)
                    projected=rup.compile_cut_supports(instance,row_cuts[row],meter)
                    expected=response['checked_lower_receipt']
                    assert expected is not None
                    assert projected==expected['projection']
                    assert projected['leaf_masks']==expected['leaf_masks']
                    assert projected['receipt_id']==expected['receipt_id']
                    assert projected['dependencies']==expected['dependency']['cut_receipts']
                    checked['checked_lower_receipt']=copy.deepcopy(expected)
                    checked['checked_lower_receipt']['leaf_masks']=projected['leaf_masks']
                    checked_proofs+=1
                ai=response['adapter_invoice']
                # This composite invoice's top categories are the native
                # wrapper; projection is a separate nested Meter counted once.
                assert ai['total']==sum(ai['by_category'].values())+ai['projection']['total']
                bank.retain(row,checked,purchase['purchase'])
            after=bank.bounds(row)
            assert after==request['after']
            gap=min(after['upper'],request['price'])-min(after['lower'],request['price'])
            assert gap==request['regret_bound'] and gap<=request['tolerance']
            assert min(after['upper'],request['price'])==request['action_cost']
            expected_action='repair' if after['upper']<request['price'] else 'replace'
            assert expected_action==request['action']
            assert request['model']==(after['model'] if expected_action=='repair' else None)
        outcomes.append(dict(mode=arm['mode'],checked_requests=len(arm['requests']),newly_readmitted_RUP_proofs=checked_proofs,
                             checked_new_witnesses=checked_witnesses,resident_links=resident_links,
                             final_own_checked_cuts=sum(len(v) for v in row_cuts.values())))
    result=dict(status='PASS',evidence='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                created_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=native.sha(__file__),
                source_sha256=native.sha(path),rup_checker_sha256=native.sha(rup.__file__),initial_admission=admission,
                arms=outcomes,new_native_calls=0,new_branch_provider_calls=0,new_cost_observations=0,
                replay_invoice=meter.record(),timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall),
                meaning='Actual raw clause proof rechecks and objective projection from freshly admitted cuts, followed by all160 supplied-weight gates. This establishes this checker-relative reconstruction, not formal verification or a new acquisition run.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','arms','timing')}))


if __name__=='__main__':
    run(Path(sys.argv[1]),Path(sys.argv[2]))
