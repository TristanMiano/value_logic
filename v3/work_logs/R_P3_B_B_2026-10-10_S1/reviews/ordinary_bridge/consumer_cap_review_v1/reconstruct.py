#!/usr/bin/env python3
"""Independent, observer-only review of completed capped-delivery records.

Contributor: ChatGPT (GPT-6 Astra Pro), October 10, 2026. DEVELOPMENT.
Imports only the standard library. No worker, checker or parent analyzer runs.
Prefix sums are recomputed from slices; coverage comparisons use bit masks.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import csv
import hashlib
import itertools
import json
import sys
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
SESSION = ROOT / 'v3/work_logs/R_P3_B_B_2026-10-10_S1'
RUN = SESSION / 'development/actual_consumer_cap_v1'
PARENT = SESSION / 'development/actual_consumer_cap_analysis_v1'
ANALYZER = ROOT / 'v3/checks/05_certificate_delivery_cap_analyze.py'
EXPECTED_UNITS = '01e88137a200c02385f1039fb146083780bf66a76900dee62f67d655460ccd4f'
EXPECTED_MANIFEST = '453cdb9baee2ad312d564c82029fddc92b4af45174c729b2797a47641784b072'
EXPECTED_ANALYZER = '2d40060d04a4c019b61a537cc1b19bca0586a27e953451f05a9fbc83e8c8a5fa'
T, BUDGET, RESERVE = 2**20, 2**27, 1024
FAILURE_OUTPUT = ('{"schema":"rp3bb.current-bound.v1","status":'
                  '"NO_CURRENT_CERTIFICATE","reason":"RESOURCE_OR_VALIDATION_FAILURE"}')
BYTE_CATEGORIES = frozenset((
    'source_record_bytes', 'current_request_bytes', 'old_request_bytes',
    'proof_output_bytes', 'proof_input_bytes', 'old_proof_output_bytes',
    'old_proof_input_bytes', 'current_receipt_output_bytes',
    'live_serialized_byte_periods'))
CHECKS = 0


def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    raw = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + '\n').encode('ascii')
    path.write_bytes(raw)
    return digest(raw)


def read_json(path):
    return json.loads(path.read_bytes())


def identity(row):
    return (row['stream'], row['recipient'], row['method'], row['request_index'])


def consumer(stage):
    return stage.startswith('receiver_') or stage in {'common_source', 'terminal', 'failure_terminal'}


def delivered(row):
    return row['status'] == 'DELIVERED'


def coverage(rows):
    return sum(1 << (row['request_index'] - 1) for row in rows if delivered(row))


def invoice_sum(rows, name):
    return sum(row['invoice'][name] for row in rows)


def strict_relation(a, b):
    left, right = a['coverage_mask'], b['coverage_mask']
    return ((left | right) == left and a['total_units'] <= b['total_units']
            and (left != right or a['total_units'] != b['total_units']))


def reconstruct(out):
    summary = read_json(RUN / 'summary.json')
    require(summary['status'] == 'PASS' and summary['units'] == 288, 'Complete run required.')
    require(summary['completed_units_sha256'] == EXPECTED_UNITS
            and summary['manifest_sha256'] == EXPECTED_MANIFEST, 'Unexpected run seal.')
    manifest_raw = (RUN / 'manifest.json').read_bytes()
    units_raw = (RUN / 'completed_units.jsonl').read_bytes()
    require(digest(manifest_raw) == EXPECTED_MANIFEST and digest(units_raw) == EXPECTED_UNITS,
            'Completed inputs changed.')
    manifest = json.loads(manifest_raw)
    contract = manifest['contract']
    require(contract['consumer_budget'] == T and contract['total_budget'] == BUDGET
            and contract['failure_reserve'] == RESERVE, 'Different experiment.')
    require(manifest['source_hashes'] == summary['source_hashes'], 'Source declarations disagree.')
    require(digest(ANALYZER.read_bytes()) == EXPECTED_ANALYZER, 'Different parent analyzer.')
    source_bindings = []
    for name, expected in manifest['source_hashes'].items():
        captured = (RUN / 'sources' / name).read_bytes()
        require(digest(captured) == expected == digest((ROOT / name).read_bytes()),
                'Source/input changed: ' + name)
        source_bindings.append({'path': name, 'bytes': len(captured), 'sha256': expected})
    primary_dir = RUN / 'sources' / contract['primary']['directory']
    primary_raw = (primary_dir / 'completed_units.jsonl').read_bytes()
    for name, expected in contract['primary']['files'].items():
        require(digest((primary_dir / name).read_bytes()) == expected, 'Primary changed: ' + name)
    primary_manifest = read_json(primary_dir / 'manifest.json')
    require(primary_manifest['worker_source_record'] == manifest['worker_source_record'],
            'Worker procurement differs from primary.')
    require(len(json.loads(manifest['worker_source_record'])['sources']) == 8,
            'Original eight-file worker closure required.')
    require(digest((RUN / 'input_declaration.json').read_bytes())
            == contract['primary']['files']['input_declaration.json'], 'Different fixture inputs.')
    require(digest((RUN / 'reference_truths.json').read_bytes()) == manifest['reference_truths_sha256'],
            'Scalar snapshot changed.')
    plan = (HERE / 'plan.md').read_bytes()
    (out / 'source').mkdir()
    for path in (Path(__file__), HERE / 'plan.md', ANALYZER):
        (out / 'source' / path.name).write_bytes(path.read_bytes())
    binding = {'stage': 'DEVELOPMENT', 'worker_executions': 0, 'clock_credit': 0,
               'created_utc': datetime.now(timezone.utc).isoformat(),
               'plan_sha256': digest(plan), 'reader_sha256': digest(Path(__file__).read_bytes()),
               'parent_analyzer_sha256': EXPECTED_ANALYZER,
               'summary_sha256': digest((RUN / 'summary.json').read_bytes()),
               'manifest_sha256': EXPECTED_MANIFEST, 'units_sha256': EXPECTED_UNITS,
               'source_and_input_bindings': source_bindings,
               'exposure': 'Parent summary and analyzer source read before plan; peer summary counts received before computation. Same-model nonblind review.'}
    save(out / 'input_binding.json', binding)

    originals, refs, primary_lines = {}, {}, {}
    primary_rows = [json.loads(line) for line in primary_raw.splitlines()]
    require(len(primary_rows) == 317, 'Primary row count.')
    for number, row in enumerate(primary_rows, 1):
        if row['kind'] == 'primary_delivery':
            k = identity(row)
            require(k not in originals and delivered(row), 'Duplicate or failed primary delivery.')
            originals[k], primary_lines[k] = row, number
        else:
            require(row['kind'] == 'independent_reference', 'Unknown primary row.')
            k = row['stream'], row['case']
            require(k not in refs and row['report']['holds'] is True, 'Duplicate or false scalar reference.')
            refs[k] = row
    require(len(originals) == 288 and len(refs) == 29, 'Primary catalogue size.')
    saved_refs = read_json(RUN / 'reference_truths.json')
    require({(item['row']['stream'], item['row']['case']): item['row'] for item in saved_refs} == refs
            and len(saved_refs) == 29, 'Scalar snapshot is not the original catalogue.')

    rows = [json.loads(line) for line in units_raw.splitlines()]
    expected = list(itertools.product(contract['streams'], contract['recipients'],
                                      contract['methods'], range(1, 7)))
    require([identity(row) for row in rows] == expected and len(set(expected)) == 288,
            'Missing, repeated, reordered or unexpected attempt.')
    blobs, error_stages, source_counts, request_rows = {}, Counter(), Counter(), []
    all_packet_count = 0
    for row in rows:
        k = identity(row)
        old = originals[k]
        reference = refs[row['stream'], row['case']]['report']
        expected_output = json.loads(old['output'])
        require(row['kind'] == 'actual_consumer_cap_delivery'
                and row['case'] == old['case'] and row['request_id'] == old['request_id'],
                'Attempt is not the same primary request.')
        require(row['issued_input'] == {
            'current_record_sha256': digest(reference['current_record'].encode('ascii')),
            'witness': expected_output['witness'], 'bound': expected_output['bound']},
            'Issued input differs from the fixed primary request.')
        inv, obs = row['invoice'], row['observer_state']
        require(inv['tariff'] == manifest['tariff'] and inv['budget'] == BUDGET
                and inv['consumer_budget'] == T and inv['failure_terminal_reserve'] == RESERVE,
                'Different tariff or cap.')
        charges = [(stage, category, amount) for stage, values in inv['by_stage'].items()
                   for category, amount in values.items()]
        require(all(type(n) is int and n >= 0 for _, _, n in charges), 'Invalid invoice amount.')
        require(sum(n for _, _, n in charges) == inv['total_units'] <= BUDGET,
                'Total arithmetic or ceiling.')
        require(sum(n for stage, _, n in charges if consumer(stage)) == inv['consumer_units'] <= T,
                'Consumer arithmetic or ceiling.')
        ok = delivered(row)
        require(row['status'] in {'DELIVERED', 'NO_CURRENT_CERTIFICATE'}, 'Unknown outcome.')
        require(obs['current_receipt_present'] is ok and not obs['stale_receipts_present']
                and type(obs['source_enrolled']) is bool, 'Authority or source observation.')
        if ok:
            require(row['output'] == old['output'] and row['error'] is None and inv['failure'] is None,
                    'Paid output differs from the fixed successful service.')
            require(obs['current_receipt_equals_output'] is True
                    and inv['total_units'] + RESERVE <= BUDGET
                    and inv['consumer_units'] + RESERVE <= T, 'Success or reserve invariant.')
        else:
            require(row['output'] == FAILURE_OUTPUT and obs['scientific_state_empty'] is True
                    and obs['current_receipt_equals_output'] is False
                    and row['receiver_retained_bytes'] == 0, 'Failure receipt, eviction or retention.')
            require(inv['by_stage']['failure_terminal'] == {
                'terminal_bytes': 111, 'delivery_events': 1, 'state_eviction_events': 1},
                'Failure terminal charge.')
            require(row['error'] == {'type': inv['failure']['type'], 'message': inv['failure']['message']},
                    'Error record mismatch.')
            error_stages[row['error']['type'], inv['failure']['stage']] += 1
        recorded = Counter()
        for ref in row['observed_packet_references']:
            require(ref['category'] in BYTE_CATEGORIES
                    and ref['path'] == 'blobs/' + ref['sha256'] + '.json', 'Unknown packet declaration.')
            if ref['sha256'] not in blobs:
                raw = (RUN / ref['path']).read_bytes()
                require(digest(raw) == ref['sha256'], 'Packet digest mismatch.')
                blobs[ref['sha256']] = raw
            raw = blobs[ref['sha256']]
            require(len(raw) == ref['bytes'], 'Packet byte count.')
            recorded[ref['stage'], ref['category']] += len(raw)
            all_packet_count += 1
        charged_bytes = Counter({(stage, category): n for stage, category, n in charges
                                 if category in BYTE_CATEGORIES})
        require(recorded == charged_bytes, 'Packet record and byte bill differ.')
        primary_bill = old['invoice']['consumer_units']
        require(row['primary_observer'] == {
            'primary_line': primary_lines[k], 'primary_consumer_units': primary_bill,
            'primary_bill_leq_cap': primary_bill <= T,
            'primary_bill_plus_reserve_leq_cap': primary_bill + RESERVE <= T}, 'Static predicate mismatch.')
        if 'common_source' in inv['by_stage']:
            source_counts[k[:3]] += 1

    require(Counter(row['status'] for row in rows) == Counter({
        'DELIVERED': summary['counts']['delivered'], 'NO_CURRENT_CERTIFICATE': summary['counts']['failed_delivery']}),
        'Summary does not describe completed records.')
    groups = {k: [row for row in rows if identity(row)[:3] == k]
              for k in itertools.product(contract['streams'], contract['recipients'], contract['methods'])}
    prefixes, histories, discrepancies, matrix = [], [], [], Counter()
    for group, sequence in groups.items():
        source_before = False
        for pos, row in enumerate(sequence):
            k = identity(row)
            earlier = sequence[:pos]
            failures_before = [r for r in earlier if not delivered(r)]
            inv, obs = row['invoice'], row['observer_state']
            source_now = obs['source_enrolled']
            charged_now = 'common_source' in inv['by_stage']
            require(not source_before or source_now, 'Source enrollment regressed.')
            require(not source_before or not charged_now, 'Already enrolled source billed again.')
            if not source_before and source_now:
                require(charged_now, 'Source became enrolled without installation bill.')
            previous_failed = pos > 0 and not delivered(sequence[pos - 1])
            histories.append({
                'stream': k[0], 'recipient': k[1], 'method': k[2], 'request_index': k[3],
                'request_id': row['request_id'], 'status': row['status'],
                'source_enrolled_before': source_before, 'source_enrolled_after': source_now,
                'source_charged_this_attempt': charged_now,
                'reported_scientific_state_empty': obs['scientific_state_empty'],
                'previous_request_failed': previous_failed,
                'prior_failure_ids': [r['request_id'] for r in failures_before],
                'recovery_after_immediate_failure': previous_failed and delivered(row),
                'producer_init_stage_present': 'producer_init' in inv['by_stage'],
                'producer_old_input_stage_present': 'producer_old_input' in inv['by_stage'],
                'receiver_old_input_stage_present': 'receiver_old_input' in inv['by_stage'],
                'source_units': sum(inv['by_stage'].get('common_source', {}).values()),
                'failure_stage': None if delivered(row) else inv['failure']['stage'],
                'total_units': inv['total_units'], 'consumer_units': inv['consumer_units']})
            source_before = source_now
            old = originals[k]
            pb = old['invoice']['consumer_units']
            item = {name: row[name] for name in ('stream', 'recipient', 'method', 'request_index',
                                                'request_id', 'case', 'status')}
            item.update(total_units=inv['total_units'], consumer_units=inv['consumer_units'],
                primary_total_units=old['invoice']['total_units'], primary_consumer_units=pb,
                total_delta=inv['total_units'] - old['invoice']['total_units'],
                consumer_delta=inv['consumer_units'] - pb,
                prior_failure_in_session=bool(failures_before), source_enrolled_after=source_now,
                source_charged_this_attempt=charged_now, static_bill_fits=pb <= T,
                static_bill_plus_reserve_fits=pb + RESERVE <= T,
                failure_type=None if delivered(row) else inv['failure']['type'],
                failure_stage=None if delivered(row) else inv['failure']['stage'])
            request_rows.append(item)
            for name, prediction in (('primary_bill_leq_cap', pb <= T),
                                     ('primary_bill_plus_reserve_leq_cap', pb + RESERVE <= T)):
                matrix[name, prediction, delivered(row)] += 1
                if prediction != delivered(row):
                    discrepancies.append({**{name: item[name] for name in
                        ('stream', 'recipient', 'method', 'request_index', 'request_id')},
                        'predicate': name,
                        'direction': 'predicted_fit_but_failed' if prediction else 'predicted_unfit_but_delivered',
                        'prior_failure_in_session': bool(failures_before),
                        'primary_consumer_units': pb, 'actual_consumer_units': inv['consumer_units']})
        for count in range(1, 7):
            part = sequence[:count]
            failed = [row for row in part if not delivered(row)]
            ids = [row['request_id'] for row in part if delivered(row)]
            prefixes.append({
                'stream': group[0], 'recipient': group[1], 'method': group[2], 'prefix': count,
                'coverage_mask': coverage(part), 'attempts': len(part), 'delivered': len(ids),
                'failed': len(failed), 'delivered_request_ids': ids,
                'failed_request_ids': [row['request_id'] for row in failed],
                'total_units': invoice_sum(part, 'total_units'),
                'consumer_units': invoice_sum(part, 'consumer_units'),
                'failure_total_units': invoice_sum(failed, 'total_units'),
                'failure_consumer_units': invoice_sum(failed, 'consumer_units'),
                'source_charge_attempts': sum('common_source' in r['invoice']['by_stage'] for r in part),
                'complete_prefix_service': not failed})

    totals, aggregate = [p for p in prefixes if p['prefix'] == 6], {}
    for method in contract['methods']:
        selection = [row for row in rows if row['method'] == method]
        failed = [row for row in selection if not delivered(row)]
        bills = [(originals[identity(row)]['invoice']['consumer_units'], delivered(row)) for row in selection]
        aggregate[method] = {
            'attempts': len(selection), 'delivered': len(selection) - len(failed), 'failed': len(failed),
            'total_units': invoice_sum(selection, 'total_units'),
            'consumer_units': invoice_sum(selection, 'consumer_units'),
            'failure_total_units': invoice_sum(failed, 'total_units'),
            'failure_consumer_units': invoice_sum(failed, 'consumer_units'),
            'static_bill_fits': sum(b <= T for b, _ in bills),
            'static_bill_plus_reserve_fits': sum(b + RESERVE <= T for b, _ in bills),
            'predicted_fit_but_failed': sum(b + RESERVE <= T and not ok for b, ok in bills),
            'predicted_unfit_but_delivered': sum(b + RESERVE > T and ok for b, ok in bills)}
    relations, comparisons = [], []
    for cell in itertools.product(contract['streams'], contract['recipients'], range(1, 7)):
        values = [p for p in prefixes if (p['stream'], p['recipient'], p['prefix']) == cell]
        require(len(values) == 6, 'Incomplete prefix comparison.')
        local = []
        for a, b in itertools.permutations(values, 2):
            if strict_relation(a, b):
                local.append({'at_least_coverage_at_no_greater_cost': a['method'],
                    'dominated_method': b['method'], 'winner_has_a_delivery': a['coverage_mask'] != 0,
                    'equal_delivered_service': a['coverage_mask'] == b['coverage_mask'],
                    'cost_saving': b['total_units'] - a['total_units'],
                    'additional_requests': sorted(set(a['delivered_request_ids']) - set(b['delivered_request_ids']))})
        relations.extend({'stream': cell[0], 'recipient': cell[1], 'prefix': cell[2], **r} for r in local)
        equal = []
        for mask in sorted({p['coverage_mask'] for p in values}):
            members = [p for p in values if p['coverage_mask'] == mask]
            lowest = min(p['total_units'] for p in members)
            equal.append({'delivered_request_ids': members[0]['delivered_request_ids'],
                'has_successful_service': mask != 0, 'methods': [p['method'] for p in members],
                'least_total_units': lowest,
                'least_cost_methods': [p['method'] for p in members if p['total_units'] == lowest]})
        enum = next(p for p in values if p['method'] == 'O-ENUM-RECEIVER')
        comparisons.append({'stream': cell[0], 'recipient': cell[1], 'prefix': cell[2],
            'methods': [{k: v for k, v in p.items() if k != 'coverage_mask'} for p in values],
            'strict_coverage_cost_relations': local, 'same_delivered_service_groups': equal,
            'direct_ordinary_dominates_all_other_methods': bool(enum['coverage_mask']) and all(
                strict_relation(enum, other) for other in values if other is not enum),
            'direct_ordinary_has_a_delivery': enum['coverage_mask'] != 0})
    reconstruction = {
        'stage': 'DEVELOPMENT', 'input_manifest_sha256': EXPECTED_MANIFEST,
        'input_completed_units_sha256': EXPECTED_UNITS, 'source_hashes': manifest['source_hashes'],
        'consumer_budget': T, 'total_budget': BUDGET, 'attempts': len(rows),
        'unique_verified_packet_files': len(blobs), 'verified_packet_references': all_packet_count,
        'aggregate_by_method': aggregate, 'prefix_comparisons': comparisons,
        'static_predicate_discrepancies': discrepancies,
        'failure_types_and_stages': [{'type': typ, 'stage': stage, 'count': count}
            for (typ, stage), count in sorted(error_stages.items())],
        'unexpected_failure_types': sorted({typ for typ, _ in error_stages if typ != 'ResourceExhausted'}),
        'totals': totals, 'request_rows': request_rows, 'prefixes': prefixes, 'histories': histories,
        'confusion_tables': [{'predicate': p, 'predicted_fit': fit, 'actually_delivered': ok, 'count': n}
            for (p, fit, ok), n in sorted(matrix.items())],
        'successful_service_relations': [r for r in relations if r['winner_has_a_delivery']],
        'empty_set_cost_relations': [r for r in relations if not r['winner_has_a_delivery']],
        'recovery_events': [h for h in histories if h['recovery_after_immediate_failure']],
        'source_charge_sessions': [{'stream': k[0], 'recipient': k[1], 'method': k[2], 'attempts': n}
                                  for k, n in sorted(source_counts.items())],
        'global_totals': {'total_units': invoice_sum(rows, 'total_units'),
            'consumer_units': invoice_sum(rows, 'consumer_units'),
            'failure_total_units': invoice_sum([r for r in rows if not delivered(r)], 'total_units'),
            'failure_consumer_units': invoice_sum([r for r in rows if not delivered(r)], 'consumer_units')},
        'checks_before_parent_read': CHECKS}
    save(out / 'independent_reconstruction.json', reconstruction)
    return reconstruction


def compare_parent(out, ours):
    require((PARENT / 'files.sha256.json').is_file(), 'Complete parent analysis seal required.')
    seals = read_json(PARENT / 'files.sha256.json')
    for name, expected in seals.items():
        require(digest((PARENT / name).read_bytes()) == expected, 'Parent output changed: ' + name)
    require(seals[ANALYZER.name] == EXPECTED_ANALYZER, 'Parent source binding mismatch.')
    theirs = read_json(PARENT / 'analysis.json')
    differences = []
    def compare(label, left, right):
        if left != right:
            differences.append({'field': label, 'independent': left, 'parent': right})
    for name in ('stage', 'input_manifest_sha256', 'input_completed_units_sha256', 'source_hashes',
                 'consumer_budget', 'total_budget', 'attempts', 'unique_verified_packet_files',
                 'aggregate_by_method', 'failure_types_and_stages', 'unexpected_failure_types'):
        compare(name, ours[name], theirs[name])
    canonical = lambda value: json.dumps(value, sort_keys=True, separators=(',', ':'))
    compare('static_predicate_discrepancies',
            sorted(map(canonical, ours['static_predicate_discrepancies'])),
            sorted(map(canonical, theirs['static_predicate_discrepancies'])))
    prefix_key = lambda row: (row['stream'], row['recipient'], row['prefix'])
    a = {prefix_key(p): p for p in ours['prefix_comparisons']}
    b = {prefix_key(p): p for p in theirs['prefix_comparisons']}
    compare('prefix_comparison_keys', sorted(a), sorted(b))
    for key in sorted(a.keys() & b.keys()):
        left, right = a[key], b[key]
        for name in ('methods', 'strict_coverage_cost_relations', 'same_delivered_service_groups'):
            compare(str(key) + ':' + name, sorted(map(canonical, left[name])),
                    sorted(map(canonical, right[name])))
        for name in ('direct_ordinary_dominates_all_other_methods', 'direct_ordinary_has_a_delivery'):
            compare(str(key) + ':' + name, left[name], right[name])
    expected_csv = {
        'per_request.csv': ours['request_rows'],
        'prefixes.csv': [{k: v for k, v in p.items() if k != 'coverage_mask'} for p in ours['prefixes']],
        'totals.csv': [{k: v for k, v in p.items() if k != 'coverage_mask'} for p in ours['totals']]}
    for name, rows in expected_csv.items():
        with (PARENT / name).open(newline='') as handle:
            actual = list(csv.DictReader(handle))
        expected = [{k: json.dumps(v, separators=(',', ':')) if isinstance(v, (list, dict))
                     else '' if v is None else str(v) for k, v in r.items()} for r in rows]
        compare(name, sorted(map(canonical, expected)), sorted(map(canonical, actual)))
    result = {'status': 'PASS' if not differences else 'FAIL',
              'parent_analysis_sha256': seals['analysis.json'],
              'parent_files_manifest_sha256': digest((PARENT / 'files.sha256.json').read_bytes()),
              'parent_analyzer_sha256': EXPECTED_ANALYZER, 'differences': differences,
              'checks_including_parent_binding': CHECKS,
              'worker_or_checker_executions': 0, 'clock_credit': 0}
    save(out / 'parent_comparison.json', result)
    require(not differences, 'Independent calculations disagree with parent output.')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    try:
        ours = reconstruct(out)
        comparison = compare_parent(out, ours)
        result = {'status': 'PASS', 'checks': CHECKS,
            'attempts': ours['attempts'], 'totals': ours['global_totals'],
            'method_aggregates': ours['aggregate_by_method'],
            'parent_analysis_sha256': comparison['parent_analysis_sha256'],
            'worker_or_checker_executions': 0, 'clock_credit': 0}
    except BaseException as failure:
        result = {'status': 'FAIL', 'checks': CHECKS,
                  'error': {'type': type(failure).__name__, 'message': str(failure),
                            'traceback': traceback.format_exc()},
                  'worker_or_checker_executions': 0, 'clock_credit': 0}
    save(out / 'summary.json', result)
    save(out / 'files.sha256.json', {str(path.relative_to(out)): digest(path.read_bytes())
         for path in sorted(out.rglob('*')) if path.is_file()})
    print(json.dumps(result, sort_keys=True))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
