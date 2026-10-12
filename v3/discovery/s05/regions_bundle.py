#!/usr/bin/env python3
"""Build and admit a compact cache after checking the raw repair evidence.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. No new solver calls.
A later checksum admission requires a previously trusted checker receipt;
an untrusted self-declared checksum does not establish proof validity.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import maxsat_repair as kernel
import maxsat_reprice as supports
import reprice_regions as regions


DIRECTORY = Path(__file__).resolve().parent


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def fingerprint(value, meter):
    raw = canonical(value)
    meter.pay('canonical_receipt_eight_byte_words', (len(raw)+7)//8)
    meter.pay('receipt_sha256_message_blocks', (len(raw)+9+63)//64)
    return hashlib.sha256(raw).hexdigest()


def cell_index(compiled, radius, price, meter):
    repairs, replacement = [], None
    for region in compiled['regions']:
        if region['action'] == 'repair':
            worst = None
            for inequality in region['inequalities']:
                if inequality['kind'] != 'tree_leaf':
                    continue
                value = (F(inequality['center_value'])
                         + radius*F(inequality['weighted_absolute_sum']))
                meter.pay('cell_leaf_support_value_and_maximum', 4)
                worst = value if worst is None else max(worst, value)
            upper = F(region['center_action_cost'])*(1+radius)
            meter.pay('cell_repair_upper', 2)
            repairs.append((worst, upper, region['witness_model'], region['tree_index']))
        else:
            lower = min(price-F(q['center_value']) for q in region['inequalities'])*(1-radius)
            meter.pay('cell_tree_lower', 2*len(region['inequalities'])+2)
            if replacement is None or lower > replacement[0]:
                replacement = (lower, region['tree_index'])
    # The archive is small; an explicit insertion sort gives an actual
    # comparison count instead of claiming a free language-runtime sort.
    ordered = []
    def key(item):
        return item[:3]+(-1 if item[3] is None else item[3],)
    for item in repairs:
        position = len(ordered)
        while position:
            meter.pay('repair_index_sort_comparison')
            if key(ordered[position-1]) <= key(item):
                break
            position -= 1
        meter.pay('repair_index_record_shift', len(ordered)-position)
        ordered.insert(position, item)
    staircase = []
    best = None
    for item in ordered:
        meter.pay('repair_prefix_minimum_comparison')
        if best is None or item[1] < best:
            staircase.append([str(item[0]), str(item[1]), item[2], item[3]])
            best = item[1]
    return dict(radius=str(radius),
                repairs=staircase,
                replacement=[str(replacement[0]), replacement[1]])


def admit(path, expected_sha256, expected_source_id, meter):
    """Integrity admission relative to an already trusted raw-checker receipt."""
    if expected_sha256 is None or expected_source_id is None:
        raise ValueError('A previously trusted raw-checker receipt is required')
    raw = regions.admitted(path, meter)
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError('Cache differs from the previously checked export')
    data = json.loads(raw)
    if (data['schema'] != 'checked_repair_regions_v1'
            or data['raw_source']['source_identity'] != expected_source_id):
        raise ValueError('Cache source/schema mismatch')
    weights = tuple(map(F, data['original_weights']))
    if any(w <= 0 for w in weights):
        raise ValueError('Positive cell-center weights required')
    runtime_rows = []
    for row in data['rows']:
        meter.pay('cache_row_and_cell_binding', 8)
        radius = F(row['cell']['radius'])
        if not 0 <= radius <= 1:
            raise ValueError('Bad cached cell radius')
        witnesses = {w[0]: (w[1], w[2]) for w in row['witnesses']}
        meter.pay('witness_role_admission', 3*len(witnesses))
        trees = row['trees']
        meter.pay('tree_role_admission', sum(4+len(t[1]) for t in trees))
        for mask, receipt in witnesses.values():
            if not 0 <= mask < 1 << len(weights):
                raise ValueError('Malformed witness mask')
        for tree in trees:
            if not tree[1] or any(not 0 <= mask < 1 << len(weights) for mask in tree[1]):
                raise ValueError('Malformed proof supports')
        repairs = [(F(d), F(b), model, tree) for d, b, model, tree in row['cell']['repairs']]
        meter.pay('region_index_record_admission', 4*len(repairs)+2)
        if any(a[0] > b[0] or a[1] <= b[1] for a, b in zip(repairs, repairs[1:])):
            raise ValueError('Malformed prefix-minimum staircase')
        for d, b, model, tree in repairs:
            if model not in witnesses or (tree is None and trees) or (tree is not None and not 0 <= tree < len(trees)):
                raise ValueError('Region points to an absent checked receipt')
        lower, tree = row['cell']['replacement']
        if (tree is None and trees) or (tree is not None and not 0 <= tree < len(trees)):
            raise ValueError('Replacement points to an absent checked receipt')
        runtime_rows.append(dict(row=row['row'], source=row['source'], radius=radius,
                                 witnesses=witnesses, trees=trees, repairs=repairs,
                                 replacement=(F(lower), tree)))
    return dict(source=expected_source_id, weights=weights, rows=runtime_rows,
                trusted_export_sha256=expected_sha256)


def dispatch(cache, row_index, weights, price, tolerance, source_identity, meter):
    meter.pay('source_row_and_query_binding', 4)
    if source_identity != cache['source'] or not 0 <= row_index < len(cache['rows']):
        raise ValueError('Query has another source or row')
    price, tolerance = F(price), F(tolerance)
    meter.pay('price_tolerance_read_and_nonnegative_check', 4)
    if price < 0 or tolerance < 0:
        raise ValueError('Nonnegative price and tolerance required')
    row = cache['rows'][row_index]
    meter.pay('weight_vector_length_check')
    if len(weights) != len(cache['weights']):
        raise ValueError('Changed objective indexing')
    for value, old in zip(weights, cache['weights']):
        meter.pay('relative_cell_coordinate_bounds', 6)
        if not (1-row['radius'])*old <= F(value) <= (1+row['radius'])*old:
            return dict(accepted=False, reason='outside_cached_weight_cell')
    lower, lower_tree = row['replacement']
    replacement_ok = price-tolerance <= lower
    meter.pay('replacement_subtraction_and_comparison', 2)
    # Last staircase threshold D<=tau.
    first, last = 0, len(row['repairs'])
    while first < last:
        middle = (first+last)//2
        meter.pay('repair_index_comparison_and_position', 3)
        if row['repairs'][middle][0] <= tolerance:
            first = middle+1
        else:
            last = middle
    repair = None if first == 0 else row['repairs'][first-1]
    meter.pay('repair_prefix_read_and_price_test', 3)
    repair_ok = repair is not None and repair[1] <= price+tolerance
    if not replacement_ok and not repair_ok:
        meter.pay('unanswered_query_output', 2)
        return dict(accepted=False, reason='cell_wide_regions_do_not_certify_tolerance')
    # Prefer the smaller quoted worst-case cost among the certified choices.
    meter.pay('certified_action_selection')
    if repair_ok and (not replacement_ok or repair[1] < price):
        _, upper, model, tree = repair
        mask, witness_id = row['witnesses'][model]
        action = dict(action='repair', model=model, witness_id=witness_id,
                      violation_mask=mask, quoted_cost_upper=str(upper))
    else:
        tree = lower_tree
        action = dict(action='replacement', quoted_cost_upper=str(price))
    proof_id = 'nonnegative_objective' if tree is None else row['trees'][tree][2]
    meter.pay('action_and_proof_receipt_lookups', 4)
    meter.pay('accepted_query_output_fields', len(action)+6)
    return dict(accepted=True, row=row['row'], source=row['source'],
                price=str(price), tolerance=str(tolerance), proof_id=proof_id,
                **action)


def main():
    bundle_path = DIRECTORY/'regions_bundle.json'
    result_path = DIRECTORY/'regions_bundle_results.json'
    if bundle_path.exists() or result_path.exists():
        raise FileExistsError('Preserve existing development evidence')
    started, cpu = time.perf_counter_ns(), time.process_time_ns()
    raw_admission, binding, compilation, indexing = (regions.Meter() for _ in range(4))
    sources = {name: regions.admitted(DIRECTORY/name, raw_admission) for name in
               ('maxsat_repair_results.json', 'maxsat_repair.py',
                'maxsat_reprice.py', 'reprice_regions.py')}
    source = json.loads(sources['maxsat_repair_results.json'])
    if (source['status'] != 'complete'
            or kernel.digest(source['instances']) != source['source_identity']
            or hashlib.sha256(sources['maxsat_repair.py']).hexdigest() != source['implementation_sha256']):
        raise ValueError('Raw source/kernel identity mismatch')
    # This call actually checks the raw source, every retained feasible
    # witness, and every negative tree used in the exported cache.
    profiles, checked_shared, checked_trees = supports.acquire_profiles(source)
    weights = tuple(F(s['weight']) for s in source['instances'][0]['soft'])
    if any(tuple(F(s['weight']) for s in i['soft']) != weights for i in source['instances']):
        raise ValueError('Expected common objective weights')
    compiled = regions.compile_profiles(profiles, weights, regions.PRICE, regions.TAU, compilation)
    arm = next(a for a in source['arms'] if a['mode'] == 'conventional_requested_value')
    rows = []
    for profile, regions_row in zip(profiles, compiled):
        radius = F(regions_row['maximum_fixed_pair_radius'])
        witnesses = []
        for witness in profile['witnesses']:
            identity = fingerprint(dict(source=profile['source_identity'], model=witness['model'],
                                        violation_mask=witness['violation_mask']), binding)
            witnesses.append([witness['model'], witness['violation_mask'], identity])
        negative_events = [(j, e) for j, e in enumerate(arm['events'])
                           if e['row'] == profile['row'] and e['status'] == 'UNSAT']
        assert len(negative_events) == len(profile['trees'])
        trees = []
        for (event_index, event), tree in zip(negative_events, profile['trees']):
            assert event['budget'] == tree['original_budget']
            identity = fingerprint(dict(source=profile['source_identity'], budget=event['budget'],
                                        proof=event['proof']), binding)
            trees.append([tree['original_budget'], tree['leaf_masks'], identity, event_index])
        rows.append(dict(row=profile['row'], source=profile['source_identity'],
                         witnesses=witnesses, trees=trees,
                         cell=cell_index(regions_row, radius, regions.PRICE, indexing)))
    bundle = dict(schema='checked_repair_regions_v1',
                  trust='Cache relative to a previously trusted raw-checker receipt; '
                        'not a stand-alone proof or authenticated signature.',
                  raw_source=dict(path='v3/discovery/s05/maxsat_repair_results.json',
                                  sha256=hashlib.sha256(sources['maxsat_repair_results.json']).hexdigest(),
                                  source_identity=source['source_identity'],
                                  arm='conventional_requested_value'),
                  checker=dict(kernel=hashlib.sha256(sources['maxsat_repair.py']).hexdigest(),
                               support_compiler=hashlib.sha256(sources['maxsat_reprice.py']).hexdigest(),
                               region_compiler=hashlib.sha256(sources['reprice_regions.py']).hexdigest(),
                               bundle_builder=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
                  original_weights=list(map(str, weights)),
                  base_duty=dict(price=str(regions.PRICE), tolerance=str(regions.TAU),
                                 common_symmetric_radius='0'),
                  tuple_fields=dict(witnesses=['model','violation_mask','checked_assignment_id'],
                                    trees=['original_budget','leaf_masks','raw_proof_id','raw_event_index'],
                                    repair_index=['D','B','model','tree_index'],
                                    replacement_index=['A','tree_index']),
                  rows=rows)
    encoded = canonical(bundle)+b'\n'
    bundle_path.write_bytes(encoded)
    export_sha = hashlib.sha256(encoded).hexdigest()
    build_cpu = time.process_time_ns()-cpu
    build_wall = time.perf_counter_ns()-started
    # The expected digest below comes from this actual successful raw check,
    # held by the caller, rather than being asserted by an untrusted cache.
    cache_admission, query_meter = regions.Meter(), regions.Meter()
    admit_cpu = time.process_time_ns()
    cache = admit(bundle_path, export_sha, source['source_identity'], cache_admission)
    admit_cpu = time.process_time_ns()-admit_cpu
    query_start = time.process_time_ns()
    queries = []
    for name, price, tolerance in (('base', 6, 1), ('changed_price', 3, 1),
                                   ('tighter_tolerance', 6, 0), ('free_replacement', 0, 0)):
        for row in range(len(rows)):
            before = sum(query_meter.counts.values())
            answer = dispatch(cache, row, weights, price, tolerance,
                              source['source_identity'], query_meter)
            queries.append(dict(query=name, row=row, answer=answer,
                                units=sum(query_meter.counts.values())-before))
    query_cpu = time.process_time_ns()-query_start
    assert all(q['answer']['accepted'] for q in queries if q['query'] == 'base')
    absent_receipt_rejected = False
    try:
        admit(bundle_path, None, None, regions.Meter())
    except ValueError:
        absent_receipt_rejected = True
    assert absent_receipt_rejected
    result = dict(status='complete', evidence='DEVELOPMENT',
                  contributor='ChatGPT (GPT-6 Astra Pro)',
                  command=['python', 'v3/discovery/s05/regions_bundle.py'],
                  new_solver_calls=0, diagnostic_optima_used=False,
                  trusted_checker_receipt=dict(bundle_sha256=export_sha,
                                              source_identity=source['source_identity'],
                                              raw_proof_trees_checked=sum(len(p['trees']) for p in profiles),
                                              feasible_witnesses_checked=sum(len(p['witnesses']) for p in profiles),
                                              authority_scope='Same-session checked export; later consumers must '
                                                              'already trust this receipt or recheck raw evidence.'),
                  bytes=dict(raw_source_result=len(sources['maxsat_repair_results.json']),
                             compact_bundle=len(encoded),
                             admitted_builder_inputs=sum(map(len, sources.values())),
                             original_full_region_profile=(DIRECTORY/'reprice_regions_results.json').stat().st_size),
                  invoices=dict(raw_archive_admission=raw_admission.record(),
                                raw_source_and_witness_check=checked_shared.record(),
                                raw_tree_check_and_support_compile=checked_trees.record(),
                                raw_receipt_ids=binding.record(),
                                region_compilation=compilation.record(),
                                price_tolerance_index=indexing.record(),
                                trusted_cache_admission=cache_admission.record(),
                                complete_queries=query_meter.record()),
                  measurement=dict(build_process_ns=build_cpu, build_wall_ns=build_wall,
                                   trusted_admission_process_ns=admit_cpu,
                                   query_process_ns=query_cpu,
                                   scope='Build includes compact JSON serialization and file write; '
                                         'query includes action/proof output construction. Final '
                                         'result-file serialization and external delivery are additional.'),
                  tuple_fields=bundle['tuple_fields'],
                  repair_index_records=sum(len(row['cell']['repairs']) for row in rows),
                  proof_leaf_masks=sum(len(t[1]) for row in rows for t in row['trees']),
                  query_results=queries,
                  checks=dict(all_base_queries_admitted=True,
                              missing_trusted_receipt_rejected=absent_receipt_rejected,
                              scope='Checksum identity is tested; omitted proofs were validated only '
                                    'by the one-time raw-checker pass, not by checksum admission.'))
    result_path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(bytes=result['bytes'],
                         invoices={key:value['total'] for key,value in result['invoices'].items()},
                         accepted_by_query={name:sum(q['answer']['accepted'] for q in queries if q['query']==name)
                                            for name in sorted({q['query'] for q in queries})},
                         repair_index_records=result['repair_index_records'],
                         measurements=result['measurement'])))


if __name__ == '__main__':
    main()
