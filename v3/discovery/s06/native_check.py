#!/usr/bin/env python3
"""Focused admission/receipt replay and paid-cap checks, no optimum diagnostic.

ChatGPT (GPT-6 Astra Pro), DEVELOPMENT. Historical receipts checked without
new search; the two explicitly separated cap probes create fresh native work.
"""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

import native_repair as native
from native_repair import kernel, profile_kernel

HERE = Path(__file__).resolve().parent


def main(destination):
    if destination.exists():
        raise FileExistsError('Preserve earlier check evidence')
    saved_path = HERE/'native_stream_results.json'
    saved = json.loads(saved_path.read_text())
    if saved['capability']['implementation_files']['adapter']['sha256'] != native.sha(native.__file__):
        raise ValueError('Changed executed adapter')
    source = json.loads((native.S05/'maxsat_repair_results.json').read_text())
    instances = source['instances']
    meter = kernel.Meter()
    checked_models, checked_proofs, warm_requests = 0, 0, 0
    checks = {}
    for arm in saved['arms']:
        latest = {}
        for purchase in arm['purchases']:
            row, r = purchase['row'], purchase['response']
            weighted = native.weighted_instance(instances[row], r['weights'])
            if weighted['identity'] != r['source_identity']:
                raise ValueError('Receipt source mismatch')
            before, after = r['state_before'], r['state_after']
            if row in latest:
                old = latest[row]
                if (before['state_id'] != old['state_id']
                        or before['sat_object_id'] != old['sat_object_id']
                        or before['highs_object_id'] != old['highs_object_id']
                        or before['core_rows'] != old['core_rows']):
                    raise ValueError('Missing persistent predecessor')
                warm_requests += 1
            latest[row] = after
            if after['native_row_count'] != after['core_rows']:
                raise ValueError('Native core row count differs')
            if r['witness'] is not None:
                check = profile_kernel.compile_witness(weighted, r['model'], meter)
                if check != r['witness']:
                    raise ValueError('Checked witness fields differ')
                checked_models += 1
            proof = r['checked_lower_receipt']
            if proof is not None:
                kernel.check_negative(weighted, proof['budget'], proof['proof'], meter)
                masks = profile_kernel.compile_tree(proof['proof'], meter)
                if masks != proof['leaf_masks'] or r['checked_lower'] != proof['budget']+1:
                    raise ValueError('Checked lower binding differs')
                checked_proofs += 1
            if arm['mode'] == 'native_exact':
                if r['checked_lower'] != r['witness']['original_cost']:
                    raise ValueError('Native exact completion lacks independent exact lower')
        for request in arm['requests']:
            if request['regret_bound'] > request['tolerance'] or request['status'] != 'checked_action':
                raise ValueError('Recorded action is not at requested tolerance')
    checks.update(checked_new_witnesses=checked_models,
                  checked_new_lower_proofs=checked_proofs,
                  purchases_with_verified_native_predecessor=warm_requests,
                  exact_native_completions_independently_certified=True)
    # Zero rounds cannot manufacture new native or proof work.
    zero = native.PersistentIHS(instances[1])
    try:
        a = zero.purchase([s['weight'] for s in instances[1]['soft']], 4,
                          limits=dict(max_rounds=0))
        assert a['status'] == 'UNRESOLVED' and a['checked_lower_receipt'] is None
        assert not a['state_after']['calls'].get('hitting_set_calls', 0)
        zero_setup = dict(invoice=zero.setup_meter.record(), timing=zero.setup_timing)
    finally:
        zero.close()
    # The model is forced to have positive weighted cost by source row0's
    # actual hard formula; we do not obtain an exact label to choose this duty.
    # Budget -1 is universally impossible for admitted nonnegative weights.
    # Native's lower hint is still prevented from entering the checked bank
    # when the independent proof budget is zero.
    capped = native.PersistentIHS(instances[0])
    try:
        b = capped.purchase([s['weight'] for s in instances[0]['soft']], -1,
                            limits=dict(proof_units=0))
        assert b['status'] == 'UNRESOLVED' and b['checked_lower_receipt'] is None
        assert b['checked_lower'] is None and b['proof_provider_invoice']['total'] == 0
        cap_setup = dict(invoice=capped.setup_meter.record(), timing=capped.setup_timing)
    finally:
        capped.close()
    checks.update(zero_native_round_cap_preserves_unresolved=True,
                  zero_proof_cap_does_not_admit_native_lower=True)
    result = dict(status='complete', evidence='DEVELOPMENT',
                  contributor='ChatGPT (GPT-6 Astra Pro)', utc=datetime.now(timezone.utc).isoformat(),
                  code_sha256=native.sha(__file__), adapter_sha256=native.sha(native.__file__),
                  stream_sha256=native.sha(saved_path), checks=checks,
                  replay_checker_invoice=meter.record(), replay_new_source_calls=0,
                  cap_probes=[dict(kind='zero_native_rounds', setup=zero_setup, response=a),
                              dict(kind='zero_negative_proof_budget', setup=cap_setup, response=b)],
                  diagnostic_optimum_calls=0)
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE/'native_check_results.json')
