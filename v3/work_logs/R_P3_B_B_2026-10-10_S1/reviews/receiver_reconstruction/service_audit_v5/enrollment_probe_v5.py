#!/usr/bin/env python3
"""Source-bound v5 enrollment probes, not Session deliveries or policy runs.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT.
The external source expectations vary; the saved worker bytes never do.
This observer does not patch tracing, hashing, file access or worker code.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
SERVICE_PATH = 'v3/checks/05_certificate_delivery_service.py'
SERVICE_SHA256 = 'b96cae82e0fe3f0f734671d57df81ac3a62350746f73228aef63c2f77bb1745f'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    raw = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode('ascii')
    path.write_bytes(raw)
    return {'bytes': len(raw), 'sha256': digest(raw)}


def manifest_at(source, wanted):
    return {name: {'bytes': len(raw), 'sha256': digest(raw)}
            for name in sorted(wanted)
            for raw in [(source / name).read_bytes()]}


def prefix_capacity_states(rows):
    """All attainable cumulative prepayment triples, by static loop order."""
    states = {(0, 0, 0)}
    previous = 0
    for index, row in enumerate(rows):
        size = row['bytes']
        states.add((previous + size, previous, index))
        states.add((previous + size, previous + size, index))
        states.add((previous + size, previous + size, index + 1))
        previous += size
    return states


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    source = args.source_root.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    declared_manifest = json.loads(args.manifest.read_text())
    before = manifest_at(source, declared_manifest)
    assert before == declared_manifest
    assert before[SERVICE_PATH]['sha256'] == SERVICE_SHA256

    spec = importlib.util.spec_from_file_location(
        '_rp3bb_independent_enrollment_probe_v5', source / SERVICE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError('Missing captured service.')
    S = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = S
    spec.loader.exec_module(S)
    assert S.VERSION == 'rp3bb-certificate-service-v5'
    assert S.ROOT == source
    expected = S.A.make_source_record(S.SOURCE_PATHS, repo_root=source)
    exact_rows = json.loads(expected)['sources']
    total_source_bytes = sum(row['bytes'] for row in exact_rows)
    failure_units = len(S.FAILURE_PAYLOAD) + 2
    assert failure_units < S.FAILURE_RESERVE
    save(args.out / 'exact_source_record.json', json.loads(expected))
    results = []

    def run_group(name, source_record, budget, expected_outcome, paid_prefix=None):
        owner = S.Session('O-ENUM-RECEIVER', 'fresh', name, 1, (0,), (), source_record)
        meter = S.Meter(budget)
        error_record = None
        output = None
        try:
            meter.run('coordination', lambda: owner._enroll(meter))
            outcome = 'ENROLLED'
        except S.ResourceExhausted as error:
            outcome = 'RESOURCE_FAILURE'
            error_record = {'type': type(error).__name__, 'stage': error.stage,
                            'category': error.category, 'count': error.count,
                            'message': str(error)}
            output = meter.fail(error)
        except Exception as error:
            outcome = 'VALIDATION_FAILURE'
            error_record = {'type': type(error).__name__, 'message': str(error)}
            output = meter.fail(error)
        assert outcome == expected_outcome, (name, outcome, error_record)
        invoice = meter.invoice()
        fees = invoice['by_stage']['common_source']
        input_bytes = len(source_record.encode('ascii'))
        assert fees['source_record_bytes'] == input_bytes
        rows = json.loads(source_record)['sources']
        capacities = (
            fees.get('source_program_bytes_prepaid', 0),
            fees.get('source_hash_bytes_prepaid', 0),
            fees.get('source_length_probe_bytes_prepaid', 0),
        )
        assert capacities in prefix_capacity_states(rows), (name, capacities)
        assert invoice['total_units'] <= budget
        assert invoice['consumer_units'] <= invoice['total_units']
        if paid_prefix is not None:
            prefix_bytes = sum(row['bytes'] for row in rows[:paid_prefix])
            assert capacities == (prefix_bytes, prefix_bytes, paid_prefix)
        if outcome == 'ENROLLED':
            assert owner.source_enrolled and output is None
            assert 'failure_terminal' not in invoice['by_stage']
            assert invoice['failure'] is None
            assert invoice['total_units'] + S.FAILURE_RESERVE <= budget
        else:
            assert not owner.source_enrolled
            assert output == S.FAILURE_PAYLOAD
            terminal = invoice['by_stage']['failure_terminal']
            assert terminal == {'terminal_bytes': len(S.FAILURE_PAYLOAD),
                                'delivery_events': 1, 'state_eviction_events': 1}
            assert sum(terminal.values()) == failure_units
            paid_work = invoice['total_units'] - failure_units
            assert paid_work <= budget - S.FAILURE_RESERVE
            assert invoice['failure'] is not None
        assert owner.request_index == 0 and owner.current_payload is None
        expected_record_file = name + '_expected_source.json'
        record_hash = save(args.out / expected_record_file, json.loads(source_record))
        result = {
            'name': name, 'status': 'PASS', 'outcome': outcome,
            'expected_source_record_file': expected_record_file,
            'expected_source_record_artifact': record_hash,
            'expected_source_record_ascii_bytes': input_bytes,
            'prepaid_capacities': {'program_bytes': capacities[0],
                                  'hash_bytes': capacities[1],
                                  'length_probe_bytes': capacities[2]},
            'prepaid_prefix_files': paid_prefix, 'source_enrolled': owner.source_enrolled,
            'error': error_record, 'invoice': invoice,
            'failure_payload': None if output is None else output.decode('ascii'),
            'session_deliveries': owner.request_index,
        }
        results.append(result)

    run_group('exact_success', expected, S.SUCCESS_BUDGET, 'ENROLLED', len(exact_rows))
    run_group('reserved_capacity_denial', expected,
              S.FAILURE_RESERVE + 2 * total_source_bytes - 1,
              'RESOURCE_FAILURE')
    for delta, name in ((-1, 'expected_length_short'), (1, 'expected_length_long')):
        altered = json.loads(expected)
        altered['sources'][0]['bytes'] += delta
        assert altered['sources'][0]['bytes'] > 0
        record = S.M.canonical(altered)
        run_group(name, record, S.SUCCESS_BUDGET, 'VALIDATION_FAILURE', 1)
    altered = json.loads(expected)
    actual_hash = altered['sources'][-1]['sha256']
    altered['sources'][-1]['sha256'] = ('0' if actual_hash[0] != '0' else '1') + actual_hash[1:]
    run_group('expected_last_hash_mismatch', S.M.canonical(altered), S.SUCCESS_BUDGET,
              'VALIDATION_FAILURE', len(exact_rows))

    after = manifest_at(source, declared_manifest)
    assert before == after == declared_manifest
    result = {
        'schema': 'rp3bb.independent-source-enrollment-diagnostic.v5',
        'stage': 'DEVELOPMENT', 'status': 'PASS',
        'service_version': S.VERSION, 'service_sha256': SERVICE_SHA256,
        'diagnostic_sha256': digest(Path(__file__).read_bytes()),
        'python': sys.version, 'tariff': S.TARIFF,
        'groups_passed': len(results), 'groups': results,
        'exact_source_file_count': len(exact_rows),
        'exact_source_total_bytes': total_source_bytes,
        'exact_source_record_ascii_bytes': len(expected.encode('ascii')),
        'failure_terminal_units': failure_units,
        'failure_terminal_reserve_units': S.FAILURE_RESERVE,
        'source_before': before, 'source_after': after,
        'sources_unchanged': before == after,
        'source_read_hash_precedence_evidence':
            'Static captured source control flow: all three per-file fees precede open/read; '
            'hash is evaluated only after the bounded read has exactly the declared length.',
        'io_trace_claimed': False,
        'capacity_interpretation':
            'Nonrefundable prepaid installation/hash/length capacity. The invoice does not '
            'assert every capacity byte was actually read or hashed on a failed attempt.',
        'session_deliveries': 0, 'policy_runs': 0,
        'principal_clock_credit_seconds': 0,
    }
    receipt = save(args.out / 'results.json', result)
    print(json.dumps({'status': result['status'], 'groups_passed': len(results),
                      'service_sha256': SERVICE_SHA256,
                      'exact_source_total_bytes': total_source_bytes,
                      'results': receipt}, indent=2))


if __name__ == '__main__':
    main()
