#!/usr/bin/env python3
"""Actual closed-loop objective updates on the existing finite repair provider.

DEVELOPMENT, ChatGPT (GPT-6 Astra Pro). Representation ablation only;
this is not the prospective persistent native IHS comparison.
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


def run(instances, initial, mode, common_setup):
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
                got = src.budget_provider(instance, budget, src.PROVIDER_CAP)
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
                        'new_provider_calls': calls, 'new_provider_units': provider_units,
                        'new_adapter_units': adapter['total'], 'common_source_profile_setup': common_setup,
                        'total_with_common_setup': common_setup + provider_units + adapter['total'],
                        'sum_realized_request_action_costs': sum(r['action_cost'] for r in requests),
                        'retained_witnesses': sum(len(p['witnesses']) for p in profiles),
                        'retained_trees': sum(len(p['trees']) for p in profiles)},
            'adapter_invoice': adapter, 'final_profiles': profiles,
            'runtime_ns': time.perf_counter_ns()-begun}


def main():
    here = Path(__file__).parent
    output = here / 'repair_stream_results.json'
    if output.exists():
        raise FileExistsError('Preserve earlier development evidence')
    p = here / 'maxsat_repair_results.json'
    data = json.loads(p.read_text())
    if sha(Path(src.__file__)) != data['implementation_sha256']:
        raise ValueError('Changed original source provider')
    profiles, shared, tree = raw.acquire_profiles(data)
    setup = shared.total + tree.total
    arms = [run(data['instances'], profiles, mode, setup)
            for mode in ('tree_profile', 'scalar_cut_profile')]
    assert all(a['summary']['checked_action_requests']==80 for a in arms)
    result = {'status': 'complete', 'evidence': 'DEVELOPMENT',
              'contributor': 'ChatGPT (GPT-6 Astra Pro)',
              'utc': datetime.now(timezone.utc).isoformat(),
              'implementation_sha256': sha(Path(__file__)),
              'provider_sha256': sha(Path(src.__file__)), 'repricer_sha256': sha(Path(raw.__file__)),
              'input_result_sha256': sha(p), 'source': p.name,
              'old_source_acquisition_units_common_to_both': next(a['final']['total_units'] for a in data['arms'] if a['mode']=='conventional_requested_value'),
              'source_bundle_bytes_read': p.stat().st_size,
              'new_source_diagnostic_calls': 0, 'fixed_existing_recipes': True,
              'comparisons': 'Representation ablation on one stateless checked provider, not native IHS performance',
              'arms': arms,
              'limits': ['Declared service operation tariff; JSON/hash/serialization overhead additional',
                         'All prior tree and witness evidence available to both representations',
                         'Each arm retains only its own newly purchased results',
                         'Raw repricing rescans; compact DAG/regions intentionally not integrated in this prototype',
                         'A production warm-state baseline remains outstanding']}
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps([a['summary'] for a in arms]))


if __name__ == '__main__':
    main()
