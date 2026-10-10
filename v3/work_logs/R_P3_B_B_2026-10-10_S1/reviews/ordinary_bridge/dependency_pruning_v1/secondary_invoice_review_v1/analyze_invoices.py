#!/usr/bin/env python3
"""Read finished secondary invoices without importing or executing workers.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT.
No research-clock credit and no modification of the source run.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json


def digest(raw):
    return sha256(raw).hexdigest()


def read(path):
    raw = path.read_bytes()
    return json.loads(raw), {'path': str(path), 'bytes': len(raw), 'sha256': digest(raw)}


def stage_sum(row, stage):
    return sum(row['invoice']['by_stage'].get(stage, {}).values())


def metrics(row):
    invoice = row['invoice']
    return {
        'proof_bytes': row['proof_bytes'],
        'total_units': invoice['total_units'],
        'consumer_units': invoice['consumer_units'],
        'producer_prune_units': stage_sum(row, 'producer_prune'),
        'producer_live_snapshot_bytes': row['producer_live_snapshot_bytes'],
        'producer_retained_bytes': row['producer_retained_bytes'],
        'receiver_live_snapshot_bytes': row['receiver_live_snapshot_bytes'],
    }


def difference(left, right):
    return {key: left[key] - right[key] for key in left}


def total(rows):
    measured = [metrics(row) for row in rows]
    return {key: sum(row[key] for row in measured) for key in measured[0]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run = args.run.resolve()
    # This existence check precedes every read of the completed invoices.
    if not (run / 'summary.json').is_file():
        raise SystemExit('Finished summary required; invoices were not read.')
    summary, summary_binding = read(run / 'summary.json')
    manifest, manifest_binding = read(run / 'manifest.json')
    assert summary['status'] == 'PASS'
    assert summary['manifest_sha256'] == manifest_binding['sha256']
    raw = (run / 'completed_units.jsonl').read_bytes()
    assert digest(raw) == summary['completed_units_sha256']
    rows = [json.loads(line) for line in raw.splitlines()]
    assert len(rows) == summary['units'] == 148
    assert summary['source_hashes'] == manifest['source_hashes']
    for relative, expected in manifest['source_hashes'].items():
        assert digest((run / 'sources' / relative).read_bytes()) == expected
    for row in rows:
        inv = row['invoice']
        assert all(type(value) is int and value >= 0
                   for values in inv['by_stage'].values() for value in values.values())
        assert sum(sum(values.values()) for values in inv['by_stage'].values()) == inv['total_units']
        assert sum(sum(values.values()) for stage, values in inv['by_stage'].items()
                   if stage.startswith('receiver_') or stage in
                   ('terminal', 'failure_terminal', 'common_source')) == inv['consumer_units']
        assert inv['total_units'] <= inv['budget']
    deliveries = [row for row in rows if row['kind'] == 'secondary_delivery']
    failures = [row for row in rows if row['kind'] == 'secondary_prune_limit_failure']
    assert len(deliveries) == 144 and len(failures) == 4
    assert all(row['status'] == 'NO_CURRENT_CERTIFICATE'
               and row['error']['type'] == 'PruneLimit' for row in failures)
    streams = sorted({row['stream'] for row in deliveries})
    assert len(streams) == 4
    methods = ('O-ADD-WARM', 'O-ADD-WARM-PRUNED')
    results = []
    for stream in streams:
        selected = {}
        for method in methods:
            group = sorted((row for row in deliveries
                            if row['stream'] == stream and row['method'] == method),
                           key=lambda row: row['request_index'])
            assert [row['request_index'] for row in group] == list(range(1, 7))
            assert all(row['status'] == 'DELIVERED' and row['recipient'] == 'fresh'
                       for row in group)
            selected[method] = group
        per_request = []
        for full, pruned in zip(selected[methods[0]], selected[methods[1]]):
            assert full['case'] == pruned['case'] and full['request_id'] == pruned['request_id']
            full_report, pruned_report = json.loads(full['output']), json.loads(pruned['output'])
            assert full_report == pruned_report
            full_metrics, pruned_metrics = metrics(full), metrics(pruned)
            per_request.append({
                'request_index': full['request_index'], 'case': full['case'],
                'full': full_metrics, 'pruned': pruned_metrics,
                'pruned_minus_full': difference(pruned_metrics, full_metrics),
            })
        full_totals, pruned_totals = total(selected[methods[0]]), total(selected[methods[1]])
        delta = difference(pruned_totals, full_totals)
        results.append({
            'stream': stream, 'requests': 6, 'full': full_totals, 'pruned': pruned_totals,
            'pruned_minus_full': delta,
            'other_stage_change_units': delta['total_units'] - delta['producer_prune_units'],
            'per_request': per_request,
        })
    result = {
        'schema': 'value_logic.rp3bb.secondary-pruning-invoice-review.v1',
        'stage': 'DEVELOPMENT', 'reviewed_utc': datetime.now(timezone.utc).isoformat(),
        'principal_clock_credit_seconds': 0, 'agent_research_clock_credit_seconds': 0,
        'worker_runs': 0, 'scope': 'Finished-run arithmetic and matched ordinary invoices only.',
        'analysis_source': {'sha256': digest(Path(__file__).read_bytes())},
        'source_bindings': {
            'summary': summary_binding, 'manifest': manifest_binding,
            'completed_units': {'path': str(run / 'completed_units.jsonl'),
                                'bytes': len(raw), 'sha256': digest(raw)},
        },
        'source_hashes': manifest['source_hashes'], 'summary_counts': summary['counts'],
        'ordinary_comparison': results,
        'paid_prune_failures': [
            {'stream': row['stream'], 'request_index': row['request_index'],
             'total_units': row['invoice']['total_units'],
             'consumer_units': row['invoice']['consumer_units'], 'error': row['error']}
            for row in failures
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x') as handle:
        json.dump(result, handle, sort_keys=True, indent=2)
        handle.write('\n')
    print(json.dumps({
        'status': 'PASS', 'streams': [
            {key: value for key, value in row.items() if key != 'per_request'}
            for row in results
        ],
        'source_bindings': result['source_bindings'],
        'paid_prune_failures': result['paid_prune_failures'],
    }, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
