#!/usr/bin/env python3
"""Read-only DEVELOPMENT probe of source ambiguity at recorded witness calls.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. Saved raw proof and feasible witness
admission is repeated; no source/provider acquisitions or policy reruns occur.
Full finite optimization is a separate diagnostic, never the floor's input.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import copy
import json
from pathlib import Path
import sys
import time

import discrete_ambiguity as af
import trace_check as tc

HERE = Path(__file__).resolve().parent


def proposed_witness(event, instance, meter):
    response = event['response']
    if response['source_identity'] != instance['identity']:
        raise ValueError('Changed proposal source')
    if response['checked_lower_receipt'] is not None:
        raise ValueError('A native proposal must not introduce unchecked lower evidence')
    witness = response.get('witness')
    if witness is not None:
        checked = tc.native.profile_kernel.compile_witness(instance, witness['model'], meter)
        for key in ('model', 'violation_mask', 'original_cost'):
            if checked[key] != witness[key]:
                raise ValueError('Proposal witness differs from original source: ' + key)
    return response


def check_source_trace(saved, data, archive, initial):
    result = []
    diagnostic = tc.native.kernel.Meter()
    feasible = [tc.finite_masks(instance, diagnostic) for instance in archive['instances']]
    for arm in saved['arms']:
        meter = tc.native.kernel.Meter()
        costs = tc.compiled.CompiledCosts(data['possible_cost_modes'], data['cohort_size'],
                                          data['source_identity'], meter)
        bank = tc.stream.CompactBank(initial, meter)
        probes = []
        for index, event in enumerate(arm['events']):
            row = event.get('row')
            if event['kind'] == 'audit':
                costs.observe(event['receipt'])
            elif event['kind'] == 'complete':
                retained, status = tc.check_complete(event, archive['instances'][row], meter)
                bank.retain(row, retained, index)
            elif event['kind'] == 'robust_witness':
                duty = data['schedule'][event['request']]
                quote = af.source_floor(row, bank, costs, duty['price'])
                # Exact finite minimax is diagnostic only, after the public
                # evidence calculation has finished and its receipt is fixed.
                exact = min(tc.semantic_regret(z, F(duty['price']), feasible[row], costs, diagnostic)
                            for z in feasible[row] + [None])
                if quote['bound'] > exact:
                    raise AssertionError('Ambiguity floor exceeds true finite minimax regret')
                probes.append(dict(event=index, request=event['request'], row=row,
                    tolerance=duty['tolerance'], receipt=quote,
                    blocks_immediate_closure=quote['bound'] > duty['tolerance'],
                    exact_finite_minimax_regret=exact,
                    actual_before_bound=F(event['before']['bound']),
                    actual_after_bound=F(event['after']['bound']),
                    actual_strict_improvement=event['strict_bound_improvement'],
                    proposal_named_units=event['response']['invoice']['total']))
                bank.retain(row, proposed_witness(event, archive['instances'][row], meter), index)
            else:
                raise ValueError('Unrecognized saved event')
        if bank.rows != arm['final_profiles'] or costs.snapshot() != arm['final_cost_state']:
            raise ValueError('Chronological source/evidence reconstruction differs')
        result.append(dict(policy=arm['policy'], probes=probes,
            summary=dict(proposal_states=len(probes),
                certified_immediate_closure_impossible=sum(p['blocks_immediate_closure'] for p in probes),
                exact_immediate_closure_impossible=sum(p['exact_finite_minimax_regret'] > p['tolerance'] for p in probes),
                blocked_states_with_actual_strict_improvement=sum(p['blocks_immediate_closure'] and p['actual_strict_improvement'] for p in probes),
                total_floor_invoice_units=sum(p['receipt']['invoice_units'] for p in probes),
                largest_floor=max(p['receipt']['bound'] for p in probes)),
            reconstruction_invoice=meter.record()))
    return result, diagnostic.record()


def opposing_family():
    saved = json.loads((HERE / 'bundle_example_results.json').read_text())
    instance = saved['logical_source']
    raw = saved['actual_logical_calls'][0]['checked_call']
    meter = tc.native.kernel.Meter()
    retained, status = tc.check_complete(dict(weights=[2, 2], budget=0, response=raw), instance, meter)
    profile = dict(row=0, source_identity=instance['identity'], witnesses=[], trees=[])
    bank = tc.stream.CompactBank([profile], meter)
    bank.retain(0, retained, 0)
    # Two explicit illustrative candidates are independently checked. No
    # search oracle or free optimum is attributed to a controller.
    for model in (1, 2):
        witness = tc.native.profile_kernel.compile_witness(instance, model, meter)
        bank.retain(0, dict(source_identity=instance['identity'], witness=witness,
                            checked_lower_receipt=None), 1 + model)
    cases = []
    diagnostic = tc.native.kernel.Meter()
    feasible = tc.finite_masks(instance, diagnostic)
    for h in (1, 2, 3, 8, 32):
        modes = [[0, h], [h, 0]]
        costs = tc.compiled.CompiledCosts(modes, 1, tc.native.kernel.digest(modes), meter)
        for price in (F(0), F(h, 4), F(h, 2), F(h), F(h + 1)):
            got = af.source_floor(0, bank, costs, price)
            exact = min(tc.semantic_regret(z, price, feasible, costs, diagnostic) for z in feasible + [None])
            if got['bound'] != min(price, h) or exact != min(price, h):
                raise AssertionError('Constructive opposing-cost family does not match the proof')
            if not af.verify_floor(got, 0, bank, costs, price):
                raise AssertionError('Receipt reconstruction failed')
            cases.append(dict(h=h, price=price, lower=got['bound'], exact_finite_minimax_regret=exact,
                              floor_invoice_units=got['invoice_units'], receipt=got))
    return dict(cases=cases, existing_paid_raw_receipt=raw['receipt_id'],
                source_file_sha256=tc.sha(HERE / 'bundle_example_results.json'),
                named_reconstruction_invoice=meter.record(),
                diagnostic_invoice=diagnostic.record(), actual_new_acquisitions=0)


def run(output):
    if output.exists():
        raise FileExistsError('Preserve read-only probe evidence')
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    path = HERE / 'witness_service_results.json'
    saved = json.loads(path.read_text())
    data = json.loads((HERE.parent / 's06' / 'joint_source.json').read_text())
    if saved['status'] != 'complete' or saved['source_sha256'] != tc.sha(HERE.parent / 's06' / 'joint_source.json'):
        raise ValueError('Saved source/trace mismatch')
    archive, initial, admission = tc.stream.admit_existing_cache()
    arms, diagnostic = check_source_trace(saved, data, archive, initial)
    result = dict(status='passed', evidence='DEVELOPMENT read-only source ambiguity probe',
        contributor='ChatGPT (GPT-6 Astra Pro)', created_utc=datetime.now(timezone.utc).isoformat(),
        implementation_sha256=tc.sha(__file__), floor_sha256=tc.sha(HERE / 'discrete_ambiguity.py'),
        base_floor_sha256=tc.sha(HERE / 'ambiguity_floor.py'),
        trace_sha256=tc.sha(path), raw_initial_admission=admission,
        arms=arms, exact_diagnostic_invoice=diagnostic, opposing_cost_family=opposing_family(),
        actual_new_acquisitions=0,
        limitations='Replays recorded evidence states, not a skipped-call counterfactual execution. Earlier skipped witnesses could alter later states; diagnostic exact minima were not available to the floor. Raw admission, compilation, floor evaluation, native/search cost and all other fees remain chargeable.',
        timing=dict(process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-wall))
    output.write_text(json.dumps(result, indent=2, default=tc.encode) + '\n')
    print(json.dumps(dict(status='passed', arms=[dict(policy=a['policy'], **a['summary']) for a in arms],
                          family_cases=len(result['opposing_cost_family']['cases']), actual_new_acquisitions=0), default=tc.encode))


if __name__ == '__main__':
    run(Path(sys.argv[1]))
