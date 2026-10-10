#!/usr/bin/env python3
"""Exact observer analysis of a completed R-P3-B-B development run.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
This program executes no producer or receiver and adds no worker tariff units.
It reports all declared methods, failures, prefixes and raw price categories.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import csv
import hashlib
import json
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def write_csv(path, rows):
    if not rows:
        path.write_text('')
        return
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def cumulative(values):
    result, total = [], 0
    for value in values:
        total += value
        result.append(total)
    return result


def analyze(run, out):
    manifest = read_json(run / 'manifest.json')
    completion = read_json(run / 'summary.json')
    assert manifest['stage'] == completion['stage'] == 'DEVELOPMENT'
    assert completion['status'] == 'PASS', 'Keep failed run evidence; do not rank it as completed.'
    assert digest((run / 'manifest.json').read_bytes()) == completion['manifest_sha256']
    raw = (run / 'completed_units.jsonl').read_bytes()
    assert digest(raw) == completion['completed_units_sha256']
    units = [json.loads(line) for line in raw.splitlines()]
    assert len(units) == completion['units']
    for relative, expected in manifest['source_hashes'].items():
        assert digest((run / 'sources' / relative).read_bytes()) == expected
    verified_blobs = {}
    for unit in units:
        for ref in unit.get('observed_packet_references', []):
            key = ref['path']
            if key not in verified_blobs:
                blob = (run / key).read_bytes()
                verified_blobs[key] = (digest(blob), len(blob))
            assert verified_blobs[key] == (ref['sha256'], ref['bytes'])

    rows = [r for r in units if r.get('kind') in ('primary_delivery', 'secondary_delivery')]
    assert rows, 'No declared delivery comparison.'
    groups = defaultdict(list)
    common_outputs = defaultdict(set)
    for row in rows:
        groups[row['stream'], row['recipient'], row['method']].append(row)
        invoice = row['invoice']
        total = sum(sum(counts.values()) for counts in invoice['by_stage'].values())
        consumer = sum(sum(counts.values()) for stage, counts in invoice['by_stage'].items()
                       if stage.startswith('receiver_') or stage in
                       ('terminal', 'failure_terminal', 'common_source'))
        assert total == invoice['total_units'] <= invoice['budget']
        assert consumer == invoice['consumer_units']
        if row['status'] == 'DELIVERED':
            common_outputs[row['stream'], row['case']].add(row['output'])
        else:
            assert row['status'] == 'NO_CURRENT_CERTIFICATE'
    assert all(len(values) == 1 for values in common_outputs.values()), 'Successful output mismatch.'

    thresholds = manifest['consumer_thresholds']
    totals, detail, categories, proof_counts = [], [], [], []
    for (stream, recipient, method), seq in sorted(groups.items()):
        seq.sort(key=lambda r: r['request_index'])
        assert [r['request_index'] for r in seq] == list(range(1, len(seq) + 1))
        invoice_totals = [r['invoice']['total_units'] for r in seq]
        consumer_totals = [r['invoice']['consumer_units'] for r in seq]
        delivered = sum(r['status'] == 'DELIVERED' for r in seq)
        cost_categories, cost_stages = Counter(), Counter()
        for row in seq:
            for stage, counts in row['invoice']['by_stage'].items():
                cost_categories.update(counts)
                cost_stages[stage] += sum(counts.values())
                for category, count in counts.items():
                    categories.append(dict(stream=stream, recipient=recipient, method=method,
                                           request_index=row['request_index'], stage=stage,
                                           category=category, count=count))
            one = dict(stream=stream, recipient=recipient, method=method,
                       request_index=row['request_index'], case=row['case'], status=row['status'],
                       total_units=row['invoice']['total_units'],
                       consumer_units=row['invoice']['consumer_units'],
                       source_units=sum(row['invoice']['by_stage'].get('common_source', {}).values()),
                       proof_bytes=row['proof_bytes'],
                       producer_live_bytes=row['producer_live_snapshot_bytes'],
                       receiver_live_bytes=row['receiver_live_snapshot_bytes'],
                       producer_retained_bytes=row['producer_retained_bytes'],
                       receiver_retained_bytes=row['receiver_retained_bytes'])
            for threshold in thresholds:
                accepted = row['status'] == 'DELIVERED'
                one['observed_consumer_bill_le_' + str(threshold)] = accepted and one['consumer_units'] <= threshold
                one['observed_bill_plus_reserve_le_' + str(threshold)] = (accepted and one['consumer_units']
                    + row['invoice']['failure_terminal_reserve'] <= threshold)
            detail.append(one)
            packets = [r for r in row['observed_packet_references']
                       if r['stage'] == 'producer_export' and r['category'] == 'proof_output_bytes']
            for ref in packets:
                proof = read_json(run / ref['path'])
                if proof.get('schema') == 'rp3bb.add-evidence.v1':
                    counts = {name: len(proof[name]) for name in ('nodes', 'applies', 'expressions')}
                    proof_counts.append(dict(stream=stream, recipient=recipient, method=method,
                                             request_index=row['request_index'], mode=proof['mode'],
                                             packet_bytes=ref['bytes'], **counts,
                                             base_nodes=proof['base']['nodes'],
                                             base_applies=proof['base']['applies'],
                                             base_expressions=proof['base']['expressions']))
        totals.append(dict(stream=stream, recipient=recipient, method=method, requests=len(seq),
                           delivered=delivered, failed=len(seq)-delivered,
                           all_delivered=delivered == len(seq), total_units=sum(invoice_totals),
                           first_request_units=invoice_totals[0], later_five_units=sum(invoice_totals[1:]),
                           consumer_units=sum(consumer_totals), maximum_consumer_units=max(consumer_totals),
                           source_units=cost_stages['common_source'],
                           python_opcode_events=cost_categories['observed_python_opcode_events'],
                           bounded_native_c_call_events=cost_categories['bounded_native_c_call_events'],
                           live_serialized_byte_periods=cost_categories['live_serialized_byte_periods'],
                           proof_output_bytes=sum(r['proof_bytes'] or 0 for r in seq),
                           final_producer_retained_bytes=seq[-1]['producer_retained_bytes'],
                           final_receiver_retained_bytes=seq[-1]['receiver_retained_bytes']))

    comparisons, crossings, cells = [], [], []
    for stream, recipient in sorted({key[:2] for key in groups}):
        cell = [row for row in totals if row['stream'] == stream and row['recipient'] == recipient]
        ordinary = [r for r in cell if r['method'].startswith('O-') and r['all_delivered']]
        best = min((r['total_units'] for r in ordinary), default=None)
        pseq = groups.get((stream, recipient, 'P-REUSE'))
        ptotal = next((r['total_units'] for r in cell if r['method'] == 'P-REUSE' and r['all_delivered']), None)
        cells.append(dict(stream=stream, recipient=recipient,
                          best_complete_fixed_ordinary_methods=[r['method'] for r in ordinary if r['total_units'] == best],
                          best_complete_fixed_ordinary_units=best, portfolio_reuse_units=ptotal,
                          portfolio_minus_best_ordinary_units=ptotal-best if ptotal is not None and best is not None else None,
                          comparison='Descriptive best fixed method on this declared finite six-request stream.'))
        if not pseq:
            continue
        for other in sorted(k[2] for k in groups if k[:2] == (stream, recipient) and k[2] != 'P-REUSE'):
            oseq = groups[stream, recipient, other]
            assert len(pseq) == len(oseq)
            assert [r['case'] for r in pseq] == [r['case'] for r in oseq]
            eligible = all(r['status'] == 'DELIVERED' for r in pseq + oseq)
            gains = []
            pcum = cumulative(r['invoice']['total_units'] for r in pseq)
            ocum = cumulative(r['invoice']['total_units'] for r in oseq)
            for index, (p, o) in enumerate(zip(pcum, ocum), 1):
                gains.append(o-p if eligible else None)
                comparisons.append(dict(stream=stream, recipient=recipient, comparator=other,
                                        prefix_requests=index, complete_service_comparable=eligible,
                                        portfolio_cumulative_units=p, comparator_cumulative_units=o,
                                        comparator_minus_portfolio_units=o-p if eligible else None))
            good = [index+1 for index, gain in enumerate(gains) if gain is not None and gain > 0]
            sustained = [index+1 for index in range(len(gains))
                         if all(gain is not None and gain > 0 for gain in gains[index:])]
            crossings.append(dict(stream=stream, recipient=recipient, comparator=other,
                                  complete_service_comparable=eligible,
                                  first_observed_strict_portfolio_saving_prefix=min(good) if good else None,
                                  first_sustained_strict_saving_within_observed_horizon=min(sustained) if sustained else None,
                                  horizon=len(gains), comparator_minus_portfolio_by_prefix=gains))

    out.mkdir(parents=True, exist_ok=False)
    (out / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    for name, data in [('totals.csv', totals), ('per_request.csv', detail),
                       ('raw_categories.csv', categories), ('cumulative.csv', comparisons),
                       ('proof_counts.csv', proof_counts)]:
        write_csv(out / name, data)
    result = {'schema': 'value_logic.rp3bb.delivery-analysis.v1', 'stage': 'DEVELOPMENT',
              'created_utc': datetime.now(timezone.utc).isoformat(), 'command': sys.argv,
              'input_run': str(run), 'input_manifest_sha256': completion['manifest_sha256'],
              'input_completed_units_sha256': digest(raw), 'input_source_hashes': manifest['source_hashes'],
              'delivery_rows': len(rows), 'unique_verified_packet_files': len(verified_blobs),
              'complete_output_equality_cases': len(common_outputs),
              'delivery_status_counts': dict(Counter(r['status'] for r in rows)),
              'cells': cells, 'crossings': crossings,
              'threshold_contract': 'Observed bill thresholds; bill plus reserved terminal capacity is reported separately. No execution at these thresholds is inferred.',
              'scope': 'Exact finite source/tariff comparisons. No significance, population, infinite-horizon, heap or physical-runtime claim.'}
    write_json(out / 'analysis.json', result)
    files = {p.name: digest(p.read_bytes()) for p in out.iterdir() if p.is_file()}
    write_json(out / 'files.sha256.json', files)
    print(json.dumps({'delivery_rows': len(rows), 'cells': cells,
                      'delivery_status_counts': result['delivery_status_counts'],
                      'verified_packet_files': len(verified_blobs)}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    analyze(args.run, args.out)


if __name__ == '__main__':
    main()
