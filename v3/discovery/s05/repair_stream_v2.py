#!/usr/bin/env python3
"""Corrected adapter replay of paid repair_stream v1 receipts; no source calls.

DEVELOPMENT, ChatGPT (GPT-6 Astra Pro). The only controller/representation
change is omission of scalar-only new leaf compilation. Full proofs are retained
and independently rechecked. Historical source bills are not current execution.
"""
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import copy
import hashlib
import json
import time
import maxsat_repair as src
import maxsat_reprice as raw


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bounds(profile, weights, mode, meter):
    options = [(raw.dot(w['violation_mask'], weights, meter, 'witness_reprice'), w['model'])
               for w in profile['witnesses']]
    upper, model = min(options)
    meter.pay('selection', 'witness_minimum', len(options))
    lower = 0
    if mode == 'tree_profile':
        for tree in profile['trees']:
            values = [raw.dot(mask, weights, meter, 'tree_reprice') for mask in tree['leaf_masks']]
            lower = max(lower, min(values))
            meter.pay('selection', 'tree_minimum_and_maximum', len(values) + 1)
    else:
        for cut in profile['cuts']:
            old, ell = cut['weights'], cut['lower']
            additive = max(0, ell + sum(min(0, w-a) for w, a in zip(weights, old)))
            ratios = [Fraction(w, a) for w, a in zip(weights, old) if a > 0]
            scaled = ell * min(ratios) if ratios else Fraction(0)
            lower = max(lower, additive, -(-scaled.numerator // scaled.denominator))
            meter.pay('scalar_reprice', 'cut_admission_arithmetic_and_comparison', 5 * len(weights) + 5)
    if lower > upper:
        raise ValueError('Inconsistent checked bounds')
    return lower, upper, model


def run(instances, initial, mode, common_setup, replay):
    begun = time.perf_counter_ns()
    profiles = copy.deepcopy(initial)
    meter = src.Meter()
    provider_units, calls = 0, 0
    requests, receipts = [], []
    old = [s['weight'] for s in instances[0]['soft']]
    for profile in profiles:
        profile['cuts'] = [{'weights': old, 'lower': t['original_budget'] + 1}
                           for t in profile['trees']]
    for name, weights in raw.recipes(old):
        if any(type(w) is not int or w < 0 for w in weights):
            raise ValueError('Nonnegative integer weights required')
        for row, (original, profile) in enumerate(zip(instances, profiles)):
            instance = copy.deepcopy(original)
            for soft, w in zip(instance['soft'], weights):
                soft['weight'] = w
            instance['objective_max'] = sum(weights)
            instance['identity'] = src.digest({k:v for k,v in instance.items() if k != 'identity'})
            meter.pay('update', 'source_scope_weight_admission_and_retention', 2 * len(weights) + 8)
            price, tau = 6, 1
            before_bill, before_calls = meter.total + provider_units, calls
            lower, upper, model = bounds(profile, weights, mode, meter)
            before = [lower, upper]
            initial_hit = min(upper, price) - min(lower, price) <= tau
            status = 'checked_action'
            while min(upper, price) - min(lower, price) > tau:
                budget = min(upper, price) - tau - 1
                meter.pay('controller', 'gap_check_and_budget_selection', 6)
                got = replay.purchase(instance, budget, src.PROVIDER_CAP, row, name, [lower, upper])
                calls += 1
                provider_units += got['invoice']['total']
                event = {'event': len(receipts), 'row': row, 'recipe': name,
                         'source_identity': instance['identity'], 'weights': weights,
                         'budget': budget, 'before': [lower, upper], **got}
                if got['status'] == 'SAT':
                    compiled = raw.compile_witness(instance, got['model'], meter)
                    if compiled['original_cost'] > budget:
                        raise ValueError('Budget-exceeding witness')
                    if not any(w['model'] == compiled['model'] for w in profile['witnesses']):
                        profile['witnesses'].append(compiled)
                    upper, model = compiled['original_cost'], compiled['model']
                    event['checked_objective'] = upper
                elif got['status'] == 'UNSAT':
                    src.check_negative(instance, budget, got['proof'], meter)
                    if mode == 'tree_profile':
                        masks = raw.compile_tree(got['proof'], meter)
                        profile['trees'].append({'original_budget': budget, 'leaf_masks': masks,
                                                 'weight_id': src.digest(weights), 'receipt': len(receipts)})
                    profile['cuts'].append({'weights': weights, 'lower': budget + 1})
                    lower = max(lower, budget + 1)
                    meter.pay('storage', 'negative_receipt_and_cut', 8 + src.proof_words(got['proof']) + len(weights))
                else:
                    status = 'unresolved'
                event['after'] = [lower, upper]
                meter.pay('output', 'paid_receipt_record', 20)
                receipts.append(event)
                if status == 'unresolved':
                    break
            regret = min(upper, price) - min(lower, price)
            if status == 'checked_action' and regret > tau:
                raise ValueError('Unwarranted requested tolerance')
            meter.pay('output', 'complete_action_response', 16)
            requests.append({'request': len(requests), 'row': row, 'recipe': name,
                             'source_identity': instance['identity'], 'weights': weights,
                             'price': price, 'tolerance': tau, 'before': before,
                             'after': [lower, upper], 'status': status,
                             'closed_from_cache': initial_hit,
                             'action': 'repair' if upper < price else 'replace',
                             'witness': model if upper < price else None,
                             'action_cost': min(upper, price), 'regret_bound': regret,
                             'new_calls': calls-before_calls,
                             'query_units': meter.total + provider_units-before_bill})
    adapter = meter.record()
    return {'mode': mode, 'requests': requests, 'receipts': receipts,
            'summary': {'requests': len(requests), 'closed_from_cache': sum(r['closed_from_cache'] for r in requests),
                        'checked_action_requests': sum(r['status']=='checked_action' for r in requests),
                        'replayed_historical_provider_calls': calls, 'historical_provider_units': provider_units,
                        'current_execution_provider_calls': 0,
                        'corrected_adapter_units_performed_now': adapter['total'], 'common_source_profile_setup': common_setup,
                        'corrected_end_to_end_tariff_with_historical_provider': common_setup + provider_units + adapter['total'],
                        'sum_realized_request_action_costs': sum(r['action_cost'] for r in requests),
                        'retained_witnesses': sum(len(p['witnesses']) for p in profiles),
                        'retained_trees': sum(len(p['trees']) for p in profiles)},
            'adapter_invoice': adapter, 'final_profiles': profiles,
            'runtime_ns': time.perf_counter_ns()-begun}



class PaidReplay:
    """Strict per-arm stream replay. Never synthesizes or searches for a result."""
    def __init__(self, archived_arm, historical_cap):
        self.arm = archived_arm
        self.cursor = 0
        self.cap = historical_cap
        self.meter = src.Meter()
        self.matches = []

    def purchase(self, instance, budget, cap, row, recipe, before):
        self.meter.pay('replay', 'source_identity_words', 8 + sum(1+len(c) for c in instance['hard'])
                       + sum(2+len(s['clause']) for s in instance['soft']))
        actual_identity = src.digest({k:v for k,v in instance.items() if k != 'identity'})
        if actual_identity != instance['identity']:
            raise ValueError('Current replay source identity is invalid')
        if self.cursor >= len(self.arm['receipts']):
            raise ValueError('Controller asks for an unrecorded source purchase')
        event = self.arm['receipts'][self.cursor]
        expected = (self.cursor, row, recipe, actual_identity, budget, before,
                    [s['weight'] for s in instance['soft']])
        observed = tuple(event[k] for k in ('event','row','recipe','source_identity','budget','before','weights'))
        self.meter.pay('replay', 'query_order_scope_budget_and_cap_comparisons', 8)
        if expected != observed or cap != self.cap:
            raise ValueError('Replay query order, source, budget, cap or frontier changed')
        invoice = event['invoice']
        by_category = {}
        for op in invoice['operations']:
            self.meter.pay('replay', 'archived_invoice_operation_check', 3)
            if type(op['units']) is not int or op['units'] < 0:
                raise ValueError('Invalid archived invoice operation')
            by_category[op['category']] = by_category.get(op['category'], 0) + op['units']
        if (sum(by_category.values()) != invoice['total'] or by_category != invoice['by_category']
                or invoice['total'] > cap):
            raise ValueError('Archived source invoice inconsistent or above original cap')
        if event['status'] not in ('SAT','UNSAT','UNRESOLVED'):
            raise ValueError('Unknown archived source status')
        if event['status'] == 'UNRESOLVED' and (event['model'] is not None or event['proof'] is not None):
            raise ValueError('Unresolved receipt must not carry an asserted answer')
        proof_words = src.proof_words(event['proof']) if event['proof'] is not None else 0
        self.meter.pay('replay', 'archived_payload_copy_words', 20 + proof_words + len(invoice['operations']) * 3)
        got = {k:copy.deepcopy(event[k]) for k in ('status','model','proof','invoice')}
        self.matches.append({'event':self.cursor, 'source_identity':actual_identity,
                             'budget':budget, 'provider_cap':cap, 'row':row, 'recipe':recipe})
        self.cursor += 1
        return got

    def finish(self):
        if self.cursor != len(self.arm['receipts']):
            raise ValueError('Replay did not consume all paid results in the original order')
        return {'matched_calls':self.cursor, 'historical_provider_cap':self.cap,
                'cap_evidence':'Constant in hash-verified v1 caller and provider; v1 event has no cap field',
                'matches':self.matches, 'replay_only_invoice':self.meter.record()}


def forbidden_provider(*args, **kwargs):
    raise RuntimeError('This replay is forbidden to make a new source call')


def compare_replay(arm, archived):
    if len(arm['requests']) != len(archived['requests']):
        raise ValueError('Changed request stream')
    for current, old in zip(arm['requests'], archived['requests']):
        # Only the invoice can change. All actions, bounds, models, statuses and
        # source identities must be identical to the previously paid execution.
        if {k:v for k,v in current.items() if k != 'query_units'} != {
                k:v for k,v in old.items() if k != 'query_units'}:
            raise ValueError('Replay changed a request outcome')
    if arm['receipts'] != archived['receipts']:
        raise ValueError('Replay altered an original proof or provider receipt')


def main():
    begun = time.perf_counter_ns()
    here = Path(__file__).parent
    output = here / 'repair_stream_v2_results.json'
    if output.exists():
        raise FileExistsError('Preserve earlier development evidence')
    v1_path = here / 'repair_stream_results.json'
    v1_source = here / 'repair_stream.py'
    source_path = here / 'maxsat_repair_results.json'
    hashes = {p.name:sha(p) for p in (v1_path, v1_source, source_path, Path(src.__file__), Path(raw.__file__))}
    v1 = json.loads(v1_path.read_text())
    data = json.loads(source_path.read_text())
    checks = ((v1_source, v1['implementation_sha256']),
              (Path(src.__file__),v1['provider_sha256']),
              (Path(raw.__file__),v1['repricer_sha256']),
              (source_path,v1['input_result_sha256']),
              (Path(src.__file__),data['implementation_sha256']))
    if any(sha(path) != expected for path,expected in checks):
        raise ValueError('Changed historical implementation or receipt bundle')
    output.write_text(json.dumps({'status':'running','evidence':'DEVELOPMENT',
                                  'input_sha256':hashes}, indent=2)+'\n')
    # Installing the refusal guard makes accidentally calling the original native
    # search fail, including through raw.original (which is this same module).
    original_provider = src.budget_provider
    src.budget_provider = forbidden_provider
    try:
        profiles, shared, tree = raw.acquire_profiles(data)
        setup = shared.total + tree.total
        arms = []
        for historical in v1['arms']:
            replay = PaidReplay(historical, src.PROVIDER_CAP)
            arm = run(data['instances'], profiles, historical['mode'], setup, replay)
            arm['replay'] = replay.finish()
            compare_replay(arm, historical)
            arm['historical_v1_summary'] = historical['summary']
            arm['checks'] = {'exact_query_order':True, 'all_request_outcomes_unchanged':True,
                             'full_original_receipts_unchanged':True,
                             'independent_witness_and_negative_proof_checks_repeated':True}
            arm['summary']['invoice_reduction_from_v1'] = historical['summary']['total_with_common_setup'] - arm['summary']['corrected_end_to_end_tariff_with_historical_provider']
            arm['summary']['new_actual_adapter_and_replay_units_excluding_common_rebuild'] = arm['summary']['corrected_adapter_units_performed_now'] + replay.meter.total
            arms.append(arm)
        tree_arm, scalar_arm = arms
        scalar_ops = scalar_arm['adapter_invoice']['operations']
        if any(o['category']=='tree_compile' or o['operation']=='compiled_tree_leaf_masks' for o in scalar_ops):
            raise ValueError('Scalar mode still compiled unused new leaf masks')
        if tree_arm['summary']['invoice_reduction_from_v1'] != 0:
            raise ValueError('Unintended change to tree arm tariff')
        if scalar_arm['summary']['invoice_reduction_from_v1'] != 1117:
            raise ValueError('Unexpected scalar tariff change')
        if any(sha(here/name) != value for name,value in hashes.items()):
            raise ValueError('An input changed during replay')
        result = {
            'status':'complete', 'evidence':'DEVELOPMENT_REPLAY_OF_EXPOSED_PAID_RECEIPTS',
            'contributor':'ChatGPT (GPT-6 Astra Pro)',
            'utc':datetime.now(timezone.utc).isoformat(),
            'implementation_sha256':sha(Path(__file__)), 'input_sha256':hashes,
            'correction':'Scalar mode omits new tree mask compilation and mask storage; full proof checking and receipt storage unchanged',
            'historical_work':{
                'original_common_source_acquisition_units':v1['old_source_acquisition_units_common_to_both'],
                'v1_provider_calls':sum(a['summary']['new_provider_calls'] for a in v1['arms']),
                'v1_provider_units':sum(a['summary']['new_provider_units'] for a in v1['arms']),
                'provider_invoice_status':'Previously paid archive values; internal sums checked, search not repeated'},
            'current_execution':{
                'new_provider_calls':0, 'new_provider_search_units':0, 'new_source_diagnostic_calls':0,
                'common_profile_rebuild_units_performed_once':setup,
                'common_profile_rebuild_invoices':{'shared':shared.record(),'tree':tree.record()},
                'adapter_units_both_arms':sum(a['summary']['corrected_adapter_units_performed_now'] for a in arms),
                'replay_only_units_both_arms':sum(a['replay']['replay_only_invoice']['total'] for a in arms),
                'total_new_declared_work_units':setup+sum(a['summary']['new_actual_adapter_and_replay_units_excluding_common_rebuild'] for a in arms),
                'archive_bundle_bytes_read':v1_path.stat().st_size+source_path.stat().st_size,
                'runtime_ns_excluding_final_serialization':time.perf_counter_ns()-begun},
            'comparison':{
                'tree_corrected_tariff':tree_arm['summary']['corrected_end_to_end_tariff_with_historical_provider'],
                'scalar_corrected_tariff':scalar_arm['summary']['corrected_end_to_end_tariff_with_historical_provider'],
                'tree_tariff_margin':scalar_arm['summary']['corrected_end_to_end_tariff_with_historical_provider']-tree_arm['summary']['corrected_end_to_end_tariff_with_historical_provider'],
                'equal_action_cost':tree_arm['summary']['sum_realized_request_action_costs']==scalar_arm['summary']['sum_realized_request_action_costs'],
                'old_common_source_acquisition_excluded_from_both_corrected_tariffs':True},
            'arms':arms,
            'limits':[
                'One exposed development stream; representation ablation, not persistent native IHS comparison',
                'Corrected tariff combines historical provider work and repeated adapter work; replay is not a new source performance measurement',
                'Replay-only scope/order/payload checks are additional current work and excluded from the hypothetical fresh controller tariff',
                'Initial old tree profiles are rebuilt and charged identically to both arms as in v1',
                'Historical v1 caller/provider hashes establish the fixed cap; old event records did not include a separate cap field',
                'JSON loading, hashing and serialization are additional to the declared operation tariff; archive bytes and runtime are recorded',
                'All old and newly paid full proof bytes remain in source archives and replay receipts; scalar may compile them later at the stated extra cost']}
        output.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'comparison':result['comparison'],'current_execution':{k:v for k,v in result['current_execution'].items() if k!='common_profile_rebuild_invoices'},'arms':[a['summary'] for a in arms]}))
    except Exception as exc:
        output.write_text(json.dumps({'status':'partial_error','error':repr(exc),'input_sha256':hashes},indent=2)+'\n')
        raise
    finally:
        src.budget_provider = original_provider


if __name__ == '__main__':
    main()
