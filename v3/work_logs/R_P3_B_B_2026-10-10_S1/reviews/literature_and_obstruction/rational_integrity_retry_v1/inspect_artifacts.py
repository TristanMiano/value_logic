#!/usr/bin/env python3
"""Read-only, nonblind inspection of the retained partial run and one retry.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT.
Only standard-library file/JSON/hash operations; no worker, proof checker,
experiment runner or policy is imported or executed. Zero scientific credit.
This observer writes only a new sibling run directory and never repairs input.
"""
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import hashlib
import json
import sys


ROOT = Path(sys.argv[1]).resolve()
HERE = Path(__file__).resolve().parent
OUT = HERE / 'run'
OUT.mkdir(exist_ok=False)
SESSION = ROOT / 'v3/work_logs/R_P3_B_B_2026-10-10_S1'
DEV = SESSION / 'development'
OLD = DEV / 'rational_service_v1'
RETRY = DEV / 'rational_service_v1_retry1'
INPUTS = {}
FAILURES = []
CHECKS = 0


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    raw = path.read_bytes()
    relative = str(path.relative_to(ROOT))
    binding = {'bytes': len(raw), 'sha256': digest(raw)}
    if relative in INPUTS and INPUTS[relative] != binding:
        raise RuntimeError('Input changed while reading: ' + relative)
    INPUTS[relative] = binding
    return raw


def record(path):
    return json.loads(read(path))


def require(value, message, detail=None):
    global CHECKS
    CHECKS += 1
    if not value:
        FAILURES.append({'message': message, 'detail': detail})


def key(row):
    return row['method'], row['request_index'], row['case']


def differences(a, b, path=''):
    if type(a) is not type(b):
        return [path]
    if isinstance(a, dict):
        out = []
        for name in sorted(set(a) | set(b)):
            child = path + '/' + name
            out.extend([child] if name not in a or name not in b
                       else differences(a[name], b[name], child))
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [path + '/length']
        return [p for i, (x, y) in enumerate(zip(a, b))
                for p in differences(x, y, path + '/' + str(i))]
    return [] if a == b else [path]


def file_stat(path):
    value = path.stat()
    return {'size': value.st_size, 'mtime_ns': value.st_mtime_ns,
            'ctime_ns': value.st_ctime_ns, 'inode': value.st_ino}


old_stat = file_stat(OLD / 'completed_units.jsonl')
retry_declaration = record(DEV / 'rational_integrity_retry_1.json')
contract = record(DEV / 'rational_service_contract_v1.json')
source_review_paths = [
    'v3/checks/05_certificate_delivery_run.py',
    'v3/checks/05_certificate_delivery_service.py',
    'v3/work_logs/R_P3_B_B_2026-10-10_S1/development/rational_service_audit.py',
    'v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/synthesis_review_v1/transcription_readback.py',
    'v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/synthesis_review_v1/transcription_readback_v2.py',
]
for relative in source_review_paths:
    read(ROOT / relative)
read(Path(__file__).resolve())

manifests, summaries, all_rows, all_blobs = {}, {}, {}, {}
run_details = {}
for name, base in [('original', OLD), ('retry', RETRY)]:
    manifest = manifests[name] = record(base / 'manifest.json')
    summary = summaries[name] = record(base / 'summary.json')
    raw_units = read(base / 'completed_units.jsonl')
    rows = all_rows[name] = [json.loads(line) for line in raw_units.splitlines()]
    require(raw_units.endswith(b'\n'), name + ': final complete line delimiter')
    require(all(line for line in raw_units.splitlines()), name + ': no blank JSONL row')
    require(summary['manifest_sha256'] == digest(read(base / 'manifest.json')),
            name + ': summary manifest digest')
    require(summary['source_hashes'] == manifest['source_hashes'],
            name + ': summary source closure')
    require(manifest['contract'] == contract, name + ': exact contract')
    require(manifest['contract_sha256'] == digest(read(DEV / 'rational_service_contract_v1.json')),
            name + ': contract source digest')
    scope_inputs = record(base / 'scope_input_declaration.json')
    require(digest(read(base / 'scope_input_declaration.json')) == manifest['scope_inputs_sha256'],
            name + ': scope input seal')
    read(base / 'input_declaration.json')
    declared = {row['name']: row for row in scope_inputs}
    require([row['name'] for row in scope_inputs] == [r['name'] for r in contract['sequence']],
            name + ': all five declared scope inputs in order')
    require(len(declared) == 5, name + ': unique scope inputs')
    source_names = set(manifest['source_hashes'])
    captured_names = {str(p.relative_to(base / 'sources'))
                      for p in (base / 'sources').rglob('*') if p.is_file()}
    require(captured_names == source_names, name + ': exact captured source membership')
    for relative, expected in manifest['source_hashes'].items():
        require(digest(read(base / 'sources' / relative)) == expected,
                name + ': captured source digest', relative)
        require(digest(read(ROOT / relative)) == expected,
                name + ': current source digest', relative)
    worker = json.loads(manifest['worker_source_record'])
    require(len(worker['sources']) == 8, name + ': eight installed worker sources')
    worker_bytes = 0
    for source in worker['sources']:
        raw_source = read(base / 'sources' / source['path'])
        require(len(raw_source) == source['bytes'] and digest(raw_source) == source['sha256'],
                name + ': installed source record binds bytes', source['path'])
        worker_bytes += len(raw_source)
    require(worker_bytes == 197956, name + ': full installed source byte count')
    require(len(manifest['source_hashes']) == 12, name + ': twelve total captured source/input files')
    expected_keys = [(method, i, case['name']) for method in contract['methods']
                     for i, case in enumerate(contract['sequence'], 1)]
    actual_keys = [key(row) for row in rows]
    require(actual_keys == expected_keys[:len(rows)], name + ': planned ordered prefix')
    require(len(set(actual_keys)) == len(actual_keys), name + ': unique method/request/case keys')
    actual_counts = Counter(r['status'] for r in rows)
    stored_blobs = {}
    for path in sorted((base / 'blobs').iterdir()):
        require(path.is_file() and path.suffix == '.json', name + ': blob file shape', path.name)
        payload = read(path)
        require(path.stem == digest(payload), name + ': content-addressed blob hash', path.name)
        stored_blobs[str(path.relative_to(base))] = digest(payload)
    all_blobs[name] = stored_blobs
    referenced_paths = set()
    reference_count = 0
    row_summary = []
    for row in rows:
        row_key = key(row)
        case = declared[row['case']]
        planned = next(c for c in contract['sequence'] if c['name'] == row['case'])
        delivered = row['method'] in planned['expected_delivered']
        require(row['expected_delivered'] is delivered, name + ': declared row expectation', row_key)
        require((row['status'] == 'DELIVERED') is delivered, name + ': expected result', row_key)
        require(row['recipient'] == 'fresh', name + ': fresh receiving endpoint', row_key)
        require(row['kind'] == 'rational_scope_delivery', name + ': diagnostic row kind', row_key)
        require(row['request_id'] == 'rational-fragment-service-v1:' + str(row['request_index']),
                name + ': current request ID', row_key)
        require(row['stale_receipts_present'] == [], name + ': no saved stale receipt', row_key)
        require(row['current_receipt_present'] is delivered, name + ': current receipt availability', row_key)
        invoice = row['invoice']
        require(invoice['budget'] == (1024 if row['case'] == 'zero_work_capacity' else 134217728),
                name + ': exact prescribed budget', row_key)
        require(invoice['consumer_budget'] is None and invoice['failure_terminal_reserve'] == 1024,
                name + ': unchanged consumer account/reserve', row_key)
        require(all(type(v) is int and v >= 0 for values in invoice['by_stage'].values()
                    for v in values.values()), name + ': nonnegative integer invoice fields', row_key)
        total = sum(sum(values.values()) for values in invoice['by_stage'].values())
        consumer = sum(sum(values.values()) for stage, values in invoice['by_stage'].items()
                       if stage.startswith('receiver_') or stage in
                       ('terminal', 'failure_terminal', 'common_source'))
        require(total == invoice['total_units'] and consumer == invoice['consumer_units'],
                name + ': independently summed total and receiving account', row_key)
        require(total <= invoice['budget'], name + ': total within admitted budget', row_key)
        require(invoice['instrumentation_included'] is False and
                invoice['physical_cpu_or_heap_bound_claimed'] is False,
                name + ': preserved declared tariff scope', row_key)
        if row['request_index'] == 1:
            source_invoice = invoice['by_stage']['common_source']
            require(source_invoice['source_program_bytes_prepaid'] == worker_bytes and
                    source_invoice['source_hash_bytes_prepaid'] == worker_bytes and
                    source_invoice['source_length_probe_bytes_prepaid'] == 8 and
                    source_invoice['source_record_bytes'] == len(manifest['worker_source_record'].encode('ascii')),
                    name + ': complete prepaid source enrollment', row_key)
            require(sum(source_invoice.values()) == 430041, name + ': unchanged source enrollment total', row_key)
        else:
            require('common_source' not in invoice['by_stage'], name + ': installed source charged once per owner', row_key)
        reference_fees = Counter()
        for ref in row['observed_packet_references']:
            reference_count += 1
            referenced_paths.add(ref['path'])
            payload = read(base / ref['path'])
            require(len(payload) == ref['bytes'] and digest(payload) == ref['sha256'],
                    name + ': observed packet reference binding', row_key)
            require(ref['path'] == 'blobs/' + ref['sha256'] + '.json',
                    name + ': observed packet canonical path', row_key)
            reference_fees[ref['stage'], ref['category']] += len(payload)
            if ref['category'] == 'current_receipt_output_bytes':
                require(payload == row['output'].encode('ascii'), name + ': paid output blob matches row', row_key)
            if ref['category'] == 'source_record_bytes':
                require(payload == manifest['worker_source_record'].encode('ascii'),
                        name + ': source blob matches declared installation', row_key)
        for (stage, category), count in reference_fees.items():
            require(invoice['by_stage'][stage][category] == count,
                    name + ': observed byte transfers match corresponding invoice', [row_key, stage, category])
        if delivered:
            output = json.loads(row['output'])
            require(output['current_record'] == case['current_record'] and
                    output['bound'] == case['bound'] and output['witness'] == case['witness'],
                    name + ': exact current input/witness/bound in receipt', row_key)
            require(output['request_id'] == row['request_id'] and
                    output['source_record'] == manifest['worker_source_record'],
                    name + ': current receipt request/source binding', row_key)
            require(output['status'] == 'CURRENT_BOUND_CERTIFIED' and
                    output['feasibility'] == 'NONEMPTY' and
                    output['coverage'] == 'ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS',
                    name + ': complete declared receiving claim', row_key)
            require(row['error'] is None and invoice['failure'] is None,
                    name + ': success error fields', row_key)
        else:
            require(row['scientific_state_empty'] is True, name + ': failed owned scientific state evicted', row_key)
            require(invoice['by_stage']['failure_terminal'] == {
                'terminal_bytes': 111, 'delivery_events': 1, 'state_eviction_events': 1},
                name + ': complete paid failure footer', row_key)
            require(json.loads(row['output']) == {
                'schema': 'rp3bb.current-bound.v1', 'status': 'NO_CURRENT_CERTIFICATE',
                'reason': 'RESOURCE_OR_VALIDATION_FAILURE'}, name + ': explicit no-certificate output', row_key)
        if row['case'] == 'zero_work_capacity':
            require(total == consumer == 113 and row['observed_packet_references'] == [] and
                    row['error'] == {'type': 'ResourceExhausted', 'message': 'coordination: reserved budget exhausted'},
                    name + ': zero work capacity exact denial record', row_key)
        row_summary.append({k: row[k] for k in ('method', 'request_index', 'case', 'status', 'error',
                                              'current_receipt_present', 'scientific_state_empty')}
                           | {'total_units': total, 'consumer_units': consumer,
                              'proof_bytes': row['proof_bytes'],
                              'observed_packet_reference_count': len(row['observed_packet_references'])})
    run_details[name] = {
        'completed_sha256': digest(raw_units), 'completed_bytes': len(raw_units),
        'rows': len(rows), 'actual_status_counts': dict(actual_counts),
        'summary_declared_rows': summary['units'],
        'summary_declared_completed_sha256': summary['completed_units_sha256'],
        'summary_digest_matches_actual': summary['completed_units_sha256'] == digest(raw_units),
        'missing_planned_keys': [list(k) for k in expected_keys if k not in actual_keys],
        'all_blob_files': len(stored_blobs), 'unique_referenced_blob_files': len(referenced_paths),
        'unreferenced_blob_files': sorted(set(stored_blobs) - referenced_paths),
        'packet_references': reference_count,
        'row_observations': row_summary,
    }

require(len(all_rows['original']) == 29 and len(all_rows['retry']) == 30, 'retained partial run and complete retry counts')
require(run_details['original']['actual_status_counts'] == {'DELIVERED': 12, 'NO_CURRENT_CERTIFICATE': 17},
        'original surviving record counts')
require(run_details['retry']['actual_status_counts'] == {'DELIVERED': 13, 'NO_CURRENT_CERTIFICATE': 17},
        'retry independent record counts')
require(not run_details['original']['summary_digest_matches_actual'], 'retain original digest mismatch')
require(run_details['retry']['summary_digest_matches_actual'], 'retry summary digest binding')
require(summaries['retry']['units'] == 30 and summaries['retry']['counts'] == {
    'assertions': 302, 'delivered': 13, 'failed_delivery': 17} and
    summaries['retry']['status'] == 'PASS' and summaries['retry']['error'] is None,
    'retry author summary agrees with counted outcomes; author assertions are not rerun')
require(manifests['original']['source_hashes'] == manifests['retry']['source_hashes'] == retry_declaration['source_hashes'],
        'retry source closure unchanged and prospectively bound')
manifest_differences = differences(manifests['original'], manifests['retry'])
require(set(manifest_differences) == {'/command/2', '/prepared_utc'},
        'only output path and preparation time differ in manifests', manifest_differences)
require(datetime.fromisoformat(retry_declaration['created_utc']) <
        datetime.fromisoformat(manifests['retry']['prepared_utc']),
        'retry declaration precedes prepared run timestamp')
require(retry_declaration['retry_number'] == retry_declaration['retry_limit'] == 1,
        'single unchanged integrity retry declaration')
for filename in ('input_declaration.json', 'scope_input_declaration.json'):
    require(read(OLD / filename) == read(RETRY / filename), 'unchanged exact input file', filename)
prefix_differences = Counter()
for old_row, retry_row in zip(all_rows['original'], all_rows['retry']):
    paths = differences(old_row, retry_row)
    require(set(paths) <= {'/observed_wall_ns'}, 'complete surviving row matches retry except measured wall time',
            [key(old_row), paths])
    prefix_differences.update(paths)
require(all_blobs['original'] == all_blobs['retry'], 'identical full content-addressed blob membership and bytes')
preserved = SESSION / 'reviews/receiver_reconstruction/synthesis_review_v1'
preserved_units = preserved / ('observed_rational_completed_units_' +
    'df3e500eac31c649b9afa3fc285b3d5428ed157ced94e2a63c462ff6bc92f69f.jsonl')
require(read(preserved_units) == read(OLD / 'completed_units.jsonl'), 'original preserved 29-row copy agrees')
require(read(preserved / 'observed_rational_summary.json') == read(OLD / 'summary.json'),
        'original preserved inconsistent summary agrees')
for relative, expected in INPUTS.items():
    raw = (ROOT / relative).read_bytes()
    require({'bytes': len(raw), 'sha256': digest(raw)} == expected, 'input bytes unchanged after inspection', relative)
require(file_stat(OLD / 'completed_units.jsonl') == old_stat, 'original file size/mtime/ctime/inode unchanged')

result = {
    'schema': 'value_logic.rp3bb.rational-integrity-independent-review.v1',
    'contributor': 'ChatGPT (GPT-6 Astra Pro)', 'stage': 'DEVELOPMENT',
    'review_mode': 'same-model nonblind, artifact-only independent inspection',
    'worker_executions': 0, 'proof_checker_executions': 0, 'principal_clock_credit': 0,
    'status': 'PASS_RETRY_WITH_RETAINED_ORIGINAL_MISMATCH' if not FAILURES else 'REVIEW_CHECK_FAILURE',
    'observational_checks': CHECKS, 'failures': FAILURES,
    'original_mismatch_cause': 'UNKNOWN; no cause inferred from the successful retry or missing final planned key',
    'original_file_stat_before': old_stat,
    'original_file_stat_after': file_stat(OLD / 'completed_units.jsonl'),
    'manifest_difference_paths': manifest_differences,
    'surviving_prefix_rows_compared': 29,
    'surviving_prefix_difference_path_counts': dict(prefix_differences),
    'summary_assertions_are_author_reported_not_reexecuted': 302,
    'runs': run_details, 'inputs': INPUTS,
}
with (OUT / 'results.json').open('x') as handle:
    json.dump(result, handle, sort_keys=True, indent=2)
    handle.write('\n')
print(json.dumps({k: result[k] for k in ('status', 'observational_checks', 'failures',
      'surviving_prefix_difference_path_counts')}, sort_keys=True))
print(json.dumps({name: {k: d[k] for k in ('rows', 'actual_status_counts', 'all_blob_files',
      'unique_referenced_blob_files', 'unreferenced_blob_files', 'packet_references')}
      for name, d in run_details.items()}, sort_keys=True))
