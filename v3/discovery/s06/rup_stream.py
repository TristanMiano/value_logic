#!/usr/bin/env python3
"""Exposed 80-request integration of compact receipts and persistent native IHS.

ChatGPT (GPT-6 Astra Pro), DEVELOPMENT, 2026-10-12. No diagnostic optima.
Both conventional paths get identical checked receipts and compact evaluator.
"""
from __future__ import annotations

from collections import Counter
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import native_rup as native
from native_repair import kernel, profile_kernel as raw

HERE, S05 = Path(__file__).resolve().parent, native.S05


def admit_existing_cache():
    """Re-establish the pointwise projection's admission chain from raw proofs.

    We consume the existing small cache, compare each source/model/mask/proof ID
    with actual raw checking, and use only its pointwise witness/tree fields.
    Cached cell geometry is not used or claimed newly admitted by this checker.
    """
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    meter = kernel.Meter()
    names = ['maxsat_repair_results.json', 'regions_bundle.json',
             'maxsat_repair.py', 'maxsat_reprice.py']
    blobs = {name: (S05/name).read_bytes() for name in names}
    for name, data in blobs.items():
        meter.pay('raw_admission', 'eight_byte_words', (len(data)+7)//8)
        meter.pay('raw_admission', 'sha256_message_blocks', (len(data)+9+63)//64)
    archive = json.loads(blobs['maxsat_repair_results.json'])
    bundle = json.loads(blobs['regions_bundle.json'])
    if (archive['status'] != 'complete'
            or kernel.digest(archive['instances']) != archive['source_identity']
            or hashlib.sha256(blobs['maxsat_repair.py']).hexdigest() != archive['implementation_sha256']
            or bundle['raw_source']['sha256'] != hashlib.sha256(blobs['maxsat_repair_results.json']).hexdigest()
            or bundle['raw_source']['source_identity'] != archive['source_identity']
            or bundle['checker']['kernel'] != native.sha(kernel.__file__)
            or bundle['checker']['support_compiler'] != native.sha(raw.__file__)):
        raise ValueError('Raw checker/source binding mismatch')
    checked, shared, trees = raw.acquire_profiles(archive)
    original_events = next(a['events'] for a in archive['arms']
                           if a['mode'] == 'conventional_requested_value')
    if len(checked) != len(bundle['rows']):
        raise ValueError('Cache row count differs from checked source')
    banks = []
    for expected, compact in zip(checked, bundle['rows']):
        if expected['row'] != compact['row'] or expected['source_identity'] != compact['source']:
            raise ValueError('Changed cache row source')
        expected_witnesses = []
        for w in expected['witnesses']:
            receipt = kernel.digest(dict(source=expected['source_identity'],
                                         model=w['model'], violation_mask=w['violation_mask']))
            expected_witnesses.append([w['model'], w['violation_mask'], receipt])
            meter.pay('cache_projection_binding', 'witness_id_and_fields', 3 + 10)
        negatives = [(i, e) for i, e in enumerate(original_events)
                     if e['row'] == expected['row'] and e['status'] == 'UNSAT']
        expected_trees = []
        for (i, e), tree in zip(negatives, expected['trees']):
            receipt = kernel.digest(dict(source=expected['source_identity'], budget=e['budget'], proof=e['proof']))
            expected_trees.append([tree['original_budget'], tree['leaf_masks'], receipt, i])
            meter.pay('cache_projection_binding', 'negative_proof_id_and_fields',
                      kernel.proof_words(e['proof']) + len(tree['leaf_masks']) + 8)
        if compact['witnesses'] != expected_witnesses or compact['trees'] != expected_trees:
            raise ValueError('Cache pointwise projection differs from actually checked raw evidence')
        banks.append(dict(row=compact['row'], source_identity=compact['source'],
                          witnesses=[dict(model=m, violation_mask=z, receipt_id=i)
                                     for m, z, i in compact['witnesses']],
                          trees=[dict(original_budget=b, leaf_masks=leaves, receipt_id=i,
                                      dependency=dict(archive='s05/maxsat_repair_results.json', event=ev))
                                 for b, leaves, i, ev in compact['trees']]))
    return archive, banks, dict(
        scope='Actual raw check and exact binding of existing cache pointwise witness/tree projection; cell geometry unused',
        hashes={name: hashlib.sha256(value).hexdigest() for name, value in blobs.items()},
        bytes={name: len(value) for name, value in blobs.items()},
        invoices=dict(admission_and_binding=meter.record(),
                      source_and_witness_check=shared.record(),
                      negative_proof_check_and_compile=trees.record()),
        total_declared_units=meter.total + shared.total + trees.total,
        checked_witnesses=sum(len(x['witnesses']) for x in banks),
        checked_trees=sum(len(x['trees']) for x in banks),
        timing=dict(process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-wall))


class CompactBank:
    """Same demand-driven LSB sum DAG for both controllers, including new masks."""
    def __init__(self, banks, meter):
        self.rows = copy.deepcopy(banks)
        self.meter = meter
        self.nodes, self.sums = {}, {0: 0}
        self.weights = None
        meter.pay('cache_admission', 'trusted_projected_cache_fields',
                  sum(4 + 3*len(p['witnesses']) + sum(4 + len(t['leaf_masks']) for t in p['trees'])
                      for p in banks))

    def set_weights(self, weights):
        if self.weights == list(weights):
            return
        self.meter.pay('weight_update', 'weight_admission', len(weights))
        self.weights = list(weights)
        self.sums = {0: 0}
        for mask, (parent, index) in self.nodes.items():
            self.sums[mask] = self.sums[parent] + weights[index]
            self.meter.pay('dag_update', 'compiled_instruction_read_sum_write', 7)

    def value(self, mask):
        if mask not in self.sums:
            low = mask & -mask
            parent, index = mask ^ low, low.bit_length()-1
            self.meter.pay('dag_compile', 'mask_lsb_parent_index', 5)
            self.sums[mask] = self.value(parent) + self.weights[index]
            self.nodes[mask] = (parent, index)
            self.meter.pay('dag_compile', 'node_storage_and_initial_value', 5)
        self.meter.pay('dag_query', 'sum_lookup')
        return self.sums[mask]

    def bounds(self, row):
        bank = self.rows[row]
        options = [(self.value(w['violation_mask']), w['model'], w['receipt_id'])
                   for w in bank['witnesses']]
        upper, model, witness_id = min(options)
        self.meter.pay('selection', 'witness_minimum', len(options))
        lower, proof_id = 0, 'nonnegative_objective'
        for t in bank['trees']:
            ell = min(self.value(z) for z in t['leaf_masks'])
            self.meter.pay('selection', 'tree_leaf_minimum_and_bank_maximum', len(t['leaf_masks'])+1)
            if ell > lower:
                lower, proof_id = ell, t['receipt_id']
        if lower > upper:
            raise ValueError('Inconsistent checked pointwise interval')
        return dict(lower=lower, upper=upper, model=model, witness_id=witness_id, proof_id=proof_id)

    def retain(self, row, response, purchase_id):
        bank = self.rows[row]
        if response.get('witness') is not None:
            w = response['witness']
            if not any(v['model'] == w['model'] for v in bank['witnesses']):
                receipt_id = kernel.digest(dict(source=response['source_identity'],
                                                model=w['model'], violation_mask=w['violation_mask']))
                bank['witnesses'].append(dict(model=w['model'], violation_mask=w['violation_mask'],
                                              receipt_id=receipt_id, purchase=purchase_id))
                self.meter.pay('retention', 'new_checked_witness_reference', 4)
        t = response.get('checked_lower_receipt')
        if t is not None:
            if t['checked'] is not True:
                raise ValueError('Unadmitted negative receipt')
            bank['trees'].append(dict(original_budget=t['budget'], leaf_masks=t['leaf_masks'],
                                      receipt_id=t['receipt_id'],
                                      dependency=dict(purchase=purchase_id)))
            self.meter.pay('retention', 'new_checked_tree_reference', 4+len(t['leaf_masks']))


def run_arm(instances, initial, mode):
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    meter = kernel.Meter()
    bank = CompactBank(initial, meter)
    engines, purchases, requests = {}, [], []
    old = [s['weight'] for s in instances[0]['soft']]
    try:
        for recipe, weights in raw.recipes(old):
            bank.set_weights(weights)
            for row, instance in enumerate(instances):
                previous_count = len(purchases)
                initial_bounds = bank.bounds(row)
                b = initial_bounds
                price, tau = 6, 1
                cache_hit = min(b['upper'], price)-min(b['lower'], price) <= tau
                unresolved_reason = None
                while min(b['upper'], price)-min(b['lower'], price) > tau:
                    meter.pay('controller', 'action_gap_and_requested_budget', 6)
                    if row not in engines:
                        engines[row] = native.PersistentIHS(instance)
                    budget = min(b['upper'], price)-tau-1
                    got = engines[row].purchase(weights, budget, exact=mode == 'native_exact')
                    purchase_id = len(purchases)
                    purchases.append(dict(purchase=purchase_id, request=len(requests),
                                          row=row, recipe=recipe, before=b, response=got))
                    prior_interval = (b['lower'], b['upper'])
                    bank.retain(row, got, purchase_id)
                    b = bank.bounds(row)
                    if got['status'] == 'UNRESOLVED':
                        unresolved_reason = got.get('reason', 'unresolved')
                        break
                    if (b['lower'], b['upper']) == prior_interval:
                        unresolved_reason = 'checked_interval_did_not_improve'
                        break
                    if len(purchases) - previous_count >= 256:
                        unresolved_reason = 'outer_purchase_cap'
                        break
                regret = min(b['upper'], price)-min(b['lower'], price)
                status = 'checked_action' if regret <= tau else 'unresolved'
                meter.pay('output', 'action_evidence_and_invoice_fields', 18)
                requests.append(dict(request=len(requests), row=row, recipe=recipe,
                                     structural_source_id=native.structural_id(instance),
                                     weights=weights, price=price, tolerance=tau,
                                     before=initial_bounds, after=b, closed_from_cache=cache_hit,
                                     status=status, unresolved_reason=unresolved_reason,
                                     action='repair' if b['upper'] < price else 'replace',
                                     model=b['model'] if b['upper'] < price else None,
                                     witness_id=b['witness_id'] if b['upper'] < price else None,
                                     proof_id=b['proof_id'], action_cost=min(b['upper'], price),
                                     regret_bound=regret, new_purchases=len(purchases)-previous_count))
        states = {str(i): e.state() for i, e in engines.items()}
        calls = Counter()
        for e in engines.values():
            calls.update(e.calls)
        proof_units = sum(p['response']['proof_provider_invoice']['total']
                          for p in purchases if p['response']['proof_provider_invoice'] is not None)
        purchase_adapter_units = sum(p['response']['adapter_invoice']['total'] for p in purchases)
        setup_units = sum(e.setup_meter.total for e in engines.values())
        native_events = [e for p in purchases for e in p['response']['events']
                         if e['kind'] in ('native_sat', 'native_hitting_set')]
        timings = dict(native_search_process_ns=sum(e['timing']['process_ns'] for e in native_events),
                       native_search_wall_ns=sum(e['timing']['wall_ns'] for e in native_events),
                       proof_native_process_ns=sum((p['response'].get('proof_native_timing') or {}).get('process_ns',0) for p in purchases),
                       proof_native_wall_ns=sum((p['response'].get('proof_native_timing') or {}).get('wall_ns',0) for p in purchases),
                       whole_arm_process_ns=time.process_time_ns()-cpu,
                       whole_arm_wall_ns=time.perf_counter_ns()-wall)
        final_cache = dict(rows=bank.rows, nodes={str(k): v for k, v in bank.nodes.items()})
        cache_bytes = len(json.dumps(final_cache, sort_keys=True, separators=(',', ':')).encode())
        return dict(mode=mode, requests=requests, purchases=purchases, final_states=states,
                    final_cache=final_cache, cache_serialized_bytes=cache_bytes,
                    native_memory_bytes=None,
                    native_memory_note='Native SAT learned-clause and MIP working memory not measured separately',
                    shared_service_invoice=meter.record(),
                    native_setup={str(i): dict(invoice=e.setup_meter.record(), timing=e.setup_timing)
                                  for i, e in engines.items()},
                    timings=timings,
                    summary=dict(requests=len(requests),
                                 checked_action_requests=sum(r['status']=='checked_action' for r in requests),
                                 closed_from_cache=sum(r['closed_from_cache'] for r in requests),
                                 unresolved=sum(r['status']=='unresolved' for r in requests),
                                 purchases=len(purchases), native_engines_initialized=len(engines),
                                 native_calls=dict(calls), new_proof_provider_units=proof_units,
                                 new_native_setup_units=setup_units,
                                 new_purchase_adapter_units=purchase_adapter_units,
                                 shared_service_units=meter.total,
                                 declared_units_excluding_native_search=proof_units + setup_units + purchase_adapter_units + meter.total,
                                 native_search_units=None,
                                 sum_action_costs=sum(r['action_cost'] for r in requests),
                                 retained_witnesses=sum(len(x['witnesses']) for x in bank.rows),
                                 retained_checked_trees=sum(len(x['trees']) for x in bank.rows),
                                 retained_native_cores=sum(len(e.cores) for e in engines.values())))
    finally:
        for e in engines.values():
            e.close()


def main(destination):
    if destination.exists():
        raise FileExistsError('Preserve prior development evidence')
    archive, banks, admission = admit_existing_cache()
    started = datetime.now(timezone.utc).isoformat()
    arms = [run_arm(archive['instances'], banks, mode)
            for mode in ('native_requested_tolerance', 'native_exact')]
    for arm in arms:
        for p in arm['purchases']:
            before, after = p['response']['state_before'], p['response']['state_after']
            if before['sat_object_id'] != after['sat_object_id'] or before['highs_object_id'] != after['highs_object_id']:
                raise ValueError('Native objects replaced during purchase')
    result = dict(status='complete' if all(a['summary']['checked_action_requests'] == 80 for a in arms) else 'unresolved_development', evidence='DEVELOPMENT',
                  contributor='ChatGPT (GPT-6 Astra Pro)', start_utc=started,
                  end_utc=datetime.now(timezone.utc).isoformat(),
                  command=['python', 'v3/discovery/s06/rup_stream.py', str(destination)],
                  implementation_sha256=native.sha(__file__), capability=native.capabilities(),
                  admission=admission, arms=arms,
                  historical_acquisition_common_units=next(a['final']['total_units']
                    for a in archive['arms'] if a['mode']=='conventional_requested_value'),
                  new_diagnostic_optimum_calls=0,
                  comparison_scope='Two conventional persistent native IHS paths with the same RUP bridge and cut projection on the exposed s05 fixture',
                  costs='Common current raw readmission is actual once; both arms then receive identical compact checked banks. Each arm pays own native initialization, objective updates, searches, checking, receipts, and storage. Native CPU/wall/counters are separate from declared Python/DPLL operations; no total cost ranking is asserted.',
                  limitations=['Existing source cohort and five recipes are exposed development, not independent validation',
                               'Native IHS orchestrator is not optimized iMaxHS; retained MIP model/core rows and explicit starts do not imply branch-tree retention',
                               'Fresh RUP proof calls and Boolean objective projection are separately paid; no large-instance scaling evidence',
                               'Caps are a disclosed resource vector, not a shared monetary invoice; native memory and monetary cost remain unknown',
                               'Cache cell geometry unused; exact pointwise witness/tree projection independently readmitted'])
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(admission=admission['total_declared_units'],
                          summaries=[a['summary'] for a in arms],
                          timings=[a['timings'] for a in arms]), indent=2))


if __name__ == '__main__':
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE/'rup_stream_results.json')
