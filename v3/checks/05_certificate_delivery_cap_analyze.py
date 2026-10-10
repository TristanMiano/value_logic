#!/usr/bin/env python3
"""Observer-only reconstruction of one complete fixed consumer-cap run.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT.
No worker modules are imported or executed. Failed costs remain in every prefix;
coverage inclusion is required for any coverage/cost dominance statement.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import csv
import hashlib
import itertools
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SCHEMA = 'value_logic.rp3bb.consumer-cap-analysis.v1'
PACKET_CATEGORIES = frozenset((
    'source_record_bytes', 'current_request_bytes', 'old_request_bytes',
    'proof_output_bytes', 'proof_input_bytes', 'old_proof_output_bytes',
    'old_proof_input_bytes', 'current_receipt_output_bytes',
    'live_serialized_byte_periods'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + '\n').encode('ascii')


def is_consumer(stage):
    return stage.startswith('receiver_') or stage in ('terminal', 'failure_terminal', 'common_source')


def key(row):
    return row['stream'], row['recipient'], row['method'], row['request_index']


def validate(run):
    summary = json.loads((run / 'summary.json').read_bytes())
    require(summary['status'] == 'PASS' and summary['units'] == 288,
            'Only a complete passing fixed-cap run may be analyzed.')
    manifest_raw = (run / 'manifest.json').read_bytes()
    units_raw = (run / 'completed_units.jsonl').read_bytes()
    manifest = json.loads(manifest_raw)
    require(summary['manifest_sha256'] == sha(manifest_raw)
            and summary['completed_units_sha256'] == sha(units_raw), 'Run seal mismatch.')
    require(manifest['source_hashes'] == summary['source_hashes'], 'Source declarations disagree.')
    for relative, expected in manifest['source_hashes'].items():
        require(sha((run / 'sources' / relative).read_bytes()) == expected,
                'Captured source/input changed: ' + relative)
        require(sha((ROOT / relative).read_bytes()) == expected,
                'Live bound source/input changed: ' + relative)
    require(sha((run / 'reference_truths.json').read_bytes())
            == manifest['reference_truths_sha256'], 'Scalar reference snapshot changed.')
    contract = manifest['contract']
    require(manifest['suite'] == 'actual-consumer-cap'
            and manifest['stage'] == 'DEVELOPMENT'
            and manifest['consumer_budget'] == contract['consumer_budget'] == 2**20
            and manifest['execution_budget'] == contract['total_budget'] == 2**27
            and contract['failure_reserve'] == 1024, 'Different fixed experiment.')
    primary = run / 'sources' / contract['primary']['directory']
    for name, expected in contract['primary']['files'].items():
        require(sha((primary / name).read_bytes()) == expected, 'Primary evidence seal mismatch.')
    require(sha((run / 'input_declaration.json').read_bytes())
            == contract['primary']['files']['input_declaration.json'], 'Current input mismatch.')
    primary_rows = [json.loads(line) for line in (primary / 'completed_units.jsonl').read_bytes().splitlines()]
    baseline = {key(row): row for row in primary_rows if row['kind'] == 'primary_delivery'}
    references = {(row['stream'], row['case']): row for row in primary_rows
                  if row['kind'] == 'independent_reference'}
    require(len(baseline) == 288 and len(references) == 29, 'Incomplete primary catalogue.')
    rows = [json.loads(line) for line in units_raw.splitlines()]
    expected_keys = set(itertools.product(contract['streams'], contract['recipients'],
                                         contract['methods'], range(1, 7)))
    require(len(rows) == 288 and len({key(row) for row in rows}) == 288
            and {key(row) for row in rows} == set(baseline) == expected_keys,
            'Missing or duplicate fixed attempt.')
    packet_hashes = set()
    failures = Counter()
    for row in rows:
        require(row['kind'] == 'actual_consumer_cap_delivery', 'Unexpected unit kind.')
        original = baseline[key(row)]
        require(row['case'] == original['case']
                and row['request_id'] == original['request_id'], 'Wrong primary match.')
        require(references[(row['stream'], row['case'])]['report']['holds'] is True,
                'Missing immutable scalar truth.')
        invoice = row['invoice']
        require(invoice['tariff'] == manifest['tariff']
                and invoice['budget'] == 2**27 and invoice['consumer_budget'] == 2**20
                and invoice['failure_terminal_reserve'] == 1024, 'Invoice contract mismatch.')
        require(all(type(n) is int and n >= 0 for cats in invoice['by_stage'].values()
                    for n in cats.values()), 'Invalid integer invoice.')
        require(sum(sum(cats.values()) for cats in invoice['by_stage'].values())
                == invoice['total_units'] <= invoice['budget'], 'Total invoice mismatch.')
        require(sum(sum(cats.values()) for stage, cats in invoice['by_stage'].items()
                    if is_consumer(stage)) == invoice['consumer_units'] <= invoice['consumer_budget'],
                'Consumer invoice mismatch.')
        delivered = row['status'] == 'DELIVERED'
        obs = row['observer_state']
        require(row['status'] in ('DELIVERED', 'NO_CURRENT_CERTIFICATE')
                and obs['current_receipt_present'] == delivered
                and not obs['stale_receipts_present'], 'Current/stale authority mismatch.')
        if delivered:
            require(row['output'] == original['output'], 'Successful common output is not byte-identical.')
            require(row['error'] is None and invoice['failure'] is None
                    and obs['current_receipt_equals_output'], 'Successful receipt metadata mismatch.')
            require(invoice['consumer_units'] + 1024 <= 2**20, 'Success consumed protected reserve.')
            require(invoice['total_units'] + 1024 <= 2**27, 'Success consumed total protected reserve.')
        else:
            require(json.loads(row['output'])['status'] == 'NO_CURRENT_CERTIFICATE'
                    and len(row['output'].encode('ascii')) == 111
                    and obs['scientific_state_empty'], 'Failure authority or eviction mismatch.')
            require(sum(invoice['by_stage'].get('failure_terminal', {}).values()) == 113,
                    'Failure terminal bill mismatch.')
            require(row['error'] == {k: invoice['failure'][k] for k in ('type', 'message')},
                    'Failure cause mismatch.')
            failures[row['error']['type'], invoice['failure']['stage']] += 1
        original_bill = original['invoice']['consumer_units']
        p = row['primary_observer']
        require(p['primary_consumer_units'] == original_bill
                and p['primary_bill_leq_cap'] == (original_bill <= 2**20)
                and p['primary_bill_plus_reserve_leq_cap'] == (original_bill + 1024 <= 2**20),
                'Primary static predicate changed.')
        packets = defaultdict(int)
        for ref in row['observed_packet_references']:
            relative = Path(ref['path'])
            require(relative.parts == ('blobs', ref['sha256'] + '.json'), 'Invalid packet path.')
            raw = (run / relative).read_bytes()
            require(len(raw) == ref['bytes'] and sha(raw) == ref['sha256'], 'Captured packet changed.')
            packets[ref['stage'], ref['category']] += len(raw)
            packet_hashes.add(ref['sha256'])
        for (stage, category), count in packets.items():
            require(invoice['by_stage'][stage][category] == count,
                    'Captured packet bytes do not equal the billed category.')
        for stage, categories in invoice['by_stage'].items():
            for category, count in categories.items():
                if category in PACKET_CATEGORIES:
                    require(packets[stage, category] == count,
                            'A billed packet category is missing captured bytes.')
    statuses = Counter(row['status'] for row in rows)
    require(summary['counts']['delivered'] == statuses['DELIVERED']
            and summary['counts']['failed_delivery'] == statuses['NO_CURRENT_CERTIFICATE'],
            'Summary outcome counts disagree.')
    return manifest, summary, rows, baseline, packet_hashes, failures


def analyze(manifest, summary, rows, baseline, packet_hashes, failures):
    contract = manifest['contract']
    groups = defaultdict(list)
    for row in rows:
        groups[key(row)[:3]].append(row)
    request_rows, prefixes, discrepancies = [], [], []
    aggregate = {m: {'attempts': 0, 'delivered': 0, 'failed': 0, 'total_units': 0,
                     'consumer_units': 0, 'failure_total_units': 0, 'failure_consumer_units': 0,
                     'static_bill_fits': 0, 'static_bill_plus_reserve_fits': 0,
                     'predicted_fit_but_failed': 0, 'predicted_unfit_but_delivered': 0}
                 for m in contract['methods']}
    for stream, recipient, method in itertools.product(contract['streams'], contract['recipients'], contract['methods']):
        sequence = sorted(groups[stream, recipient, method], key=lambda r: r['request_index'])
        delivered_ids, failed_ids = [], []
        total = consumer = failure_total = failure_consumer = source_events = 0
        for row in sequence:
            n = row['request_index']
            inv = row['invoice']
            prior_failure = bool(failed_ids)
            delivered = row['status'] == 'DELIVERED'
            (delivered_ids if delivered else failed_ids).append(row['request_id'])
            total += inv['total_units']; consumer += inv['consumer_units']
            if not delivered:
                failure_total += inv['total_units']; failure_consumer += inv['consumer_units']
            source_events += int(bool(inv['by_stage'].get('common_source')))
            primary = baseline[key(row)]
            p = row['primary_observer']
            item = {k: row[k] for k in ('stream', 'recipient', 'method', 'request_index', 'request_id', 'case', 'status')}
            item.update(total_units=inv['total_units'], consumer_units=inv['consumer_units'],
                        primary_total_units=primary['invoice']['total_units'],
                        primary_consumer_units=primary['invoice']['consumer_units'],
                        total_delta=inv['total_units'] - primary['invoice']['total_units'],
                        consumer_delta=inv['consumer_units'] - primary['invoice']['consumer_units'],
                        prior_failure_in_session=prior_failure,
                        source_enrolled_after=row['observer_state']['source_enrolled'],
                        source_charged_this_attempt=bool(inv['by_stage'].get('common_source')),
                        static_bill_fits=p['primary_bill_leq_cap'],
                        static_bill_plus_reserve_fits=p['primary_bill_plus_reserve_leq_cap'],
                        failure_type=None if delivered else row['error']['type'],
                        failure_stage=None if delivered else inv['failure']['stage'])
            request_rows.append(item)
            for predicate in ('primary_bill_leq_cap', 'primary_bill_plus_reserve_leq_cap'):
                if p[predicate] != delivered:
                    discrepancies.append({**{k: item[k] for k in ('stream', 'recipient', 'method', 'request_index', 'request_id')},
                                          'predicate': predicate,
                                          'direction': 'predicted_fit_but_failed' if p[predicate] else 'predicted_unfit_but_delivered',
                                          'prior_failure_in_session': prior_failure,
                                          'primary_consumer_units': p['primary_consumer_units'],
                                          'actual_consumer_units': inv['consumer_units']})
            prefix = {'stream': stream, 'recipient': recipient, 'method': method, 'prefix': n,
                      'attempts': n, 'delivered': len(delivered_ids), 'failed': len(failed_ids),
                      'delivered_request_ids': list(delivered_ids), 'failed_request_ids': list(failed_ids),
                      'total_units': total, 'consumer_units': consumer,
                      'failure_total_units': failure_total, 'failure_consumer_units': failure_consumer,
                      'source_charge_attempts': source_events,
                      'complete_prefix_service': len(delivered_ids) == n}
            prefixes.append(prefix)
            a = aggregate[method]
            for name, value in (('attempts', 1), ('delivered', int(delivered)), ('failed', int(not delivered)),
                                ('total_units', inv['total_units']), ('consumer_units', inv['consumer_units']),
                                ('failure_total_units', 0 if delivered else inv['total_units']),
                                ('failure_consumer_units', 0 if delivered else inv['consumer_units']),
                                ('static_bill_fits', int(p['primary_bill_leq_cap'])),
                                ('static_bill_plus_reserve_fits', int(p['primary_bill_plus_reserve_leq_cap'])),
                                ('predicted_fit_but_failed', int(p['primary_bill_plus_reserve_leq_cap'] and not delivered)),
                                ('predicted_unfit_but_delivered', int(not p['primary_bill_plus_reserve_leq_cap'] and delivered))):
                a[name] += value
    by_prefix = defaultdict(list)
    for row in prefixes:
        by_prefix[row['stream'], row['recipient'], row['prefix']].append(row)
    comparisons = []
    for cell, items in by_prefix.items():
        dominance, equal_sets = [], defaultdict(list)
        for a, b in itertools.permutations(items, 2):
            aa, bb = set(a['delivered_request_ids']), set(b['delivered_request_ids'])
            if aa >= bb and a['total_units'] <= b['total_units'] and (aa != bb or a['total_units'] < b['total_units']):
                dominance.append({'at_least_coverage_at_no_greater_cost': a['method'],
                                  'dominated_method': b['method'], 'winner_has_a_delivery': bool(aa),
                                  'equal_delivered_service': aa == bb,
                                  'cost_saving': b['total_units'] - a['total_units'],
                                  'additional_requests': sorted(aa - bb)})
        for a in items:
            equal_sets[tuple(a['delivered_request_ids'])].append(a)
        same_service_groups = []
        for ids, members in equal_sets.items():
            minimum = min(a['total_units'] for a in members)
            same_service_groups.append({'delivered_request_ids': list(ids), 'has_successful_service': bool(ids),
                                        'methods': [a['method'] for a in members],
                                        'least_total_units': minimum,
                                        'least_cost_methods': [a['method'] for a in members if a['total_units'] == minimum]})
        enum = next(a for a in items if a['method'] == 'O-ENUM-RECEIVER')
        comparisons.append({'stream': cell[0], 'recipient': cell[1], 'prefix': cell[2],
                            'methods': items, 'strict_coverage_cost_relations': dominance,
                            'same_delivered_service_groups': same_service_groups,
                            'direct_ordinary_dominates_all_other_methods': bool(enum['delivered_request_ids']) and all(
                                any(d['at_least_coverage_at_no_greater_cost'] == enum['method']
                                    and d['dominated_method'] == b['method'] for d in dominance)
                                for b in items if b['method'] != enum['method']),
                            'direct_ordinary_has_a_delivery': bool(enum['delivered_request_ids'])})
    output = {'schema': SCHEMA, 'stage': 'DEVELOPMENT', 'created_utc': datetime.now(timezone.utc).isoformat(),
              'command': sys.argv, 'input_manifest_sha256': summary['manifest_sha256'],
              'input_completed_units_sha256': summary['completed_units_sha256'],
              'source_hashes': manifest['source_hashes'], 'consumer_budget': 2**20, 'total_budget': 2**27,
              'attempts': len(rows), 'unique_verified_packet_files': len(packet_hashes),
              'aggregate_by_method': aggregate, 'prefix_comparisons': comparisons,
              'static_predicate_discrepancies': discrepancies,
              'failure_types_and_stages': [{'type': k[0], 'stage': k[1], 'count': v} for k, v in sorted(failures.items())],
              'unexpected_failure_types': sorted({k[0] for k in failures if k[0] != 'ResourceExhausted'}),
              'scope': 'Exact fixed attempts; all failures paid. Coverage inclusion plus cost is a partial order, not an assigned utility or an optimal adaptive policy.',
              'cause_limit': 'Saved ResourceExhausted records identify the stage, but not the rejected charge or which ceiling branch raised. No unique trigger is reconstructed from absent fields.'}
    return output, request_rows, prefixes


def write_csv(path, rows):
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, separators=(',', ':')) if isinstance(v, (list, dict)) else v
                             for k, v in row.items()})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    values = validate(args.run)
    report, requests, prefixes = analyze(*values)
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / 'analysis.json').write_bytes(json_bytes(report))
    write_csv(args.out / 'per_request.csv', requests)
    write_csv(args.out / 'prefixes.csv', prefixes)
    write_csv(args.out / 'totals.csv', [r for r in prefixes if r['prefix'] == 6])
    (args.out / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    hashes = {p.name: sha(p.read_bytes()) for p in sorted(args.out.iterdir()) if p.is_file()}
    (args.out / 'files.sha256.json').write_bytes(json_bytes(hashes))
    print(json.dumps({'status': 'PASS', 'attempts': report['attempts'],
                      'verified_packet_files': report['unique_verified_packet_files'],
                      'aggregate_by_method': report['aggregate_by_method'],
                      'unexpected_failure_types': report['unexpected_failure_types']}, sort_keys=True))


if __name__ == '__main__':
    main()
