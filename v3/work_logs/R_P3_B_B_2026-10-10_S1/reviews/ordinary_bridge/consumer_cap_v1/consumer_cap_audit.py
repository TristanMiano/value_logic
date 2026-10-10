#!/usr/bin/env python3
"""Fixed actual-consumer-cap development observer; no worker source changes.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. This is post-exposure
DEVELOPMENT. It reuses 29 sealed scalar truths and never runs their oracle.
Only --out is configurable. The prospective contract fixes all 288 attempts.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import sys
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
CONTRACT = HERE / 'consumer_cap_contract_v1.json'
VERSION = 'rp3bb-actual-consumer-cap-observer-v1'
spec = importlib.util.spec_from_file_location(
    '_rp3bb_consumer_cap_base_runner', ROOT / 'v3/checks/05_certificate_delivery_run.py')
if spec is None or spec.loader is None:
    raise ImportError('Original primary runner unavailable.')
R = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = R
spec.loader.exec_module(R)
S, FAMILY = R.S, R.FAMILY


def require(condition, message):
    if not condition:
        raise ValueError(message)


def primary_evidence(contract):
    """Observer reads sealed primary records; no reference or worker call."""
    root = ROOT / contract['primary']['directory']
    captured = {}
    for name, expected in contract['primary']['files'].items():
        path = root / name
        raw = path.read_bytes()
        require(R.sha(raw) == expected, 'Primary evidence hash mismatch: ' + name)
        captured[path] = raw
    manifest = json.loads(captured[root / 'manifest.json'])
    summary = json.loads(captured[root / 'summary.json'])
    require(summary['status'] == 'PASS' and summary['units'] == 317,
            'The complete sealed primary run is required.')
    require(summary['manifest_sha256'] == contract['primary']['files']['manifest.json']
            and summary['completed_units_sha256'] == contract['primary']['files']['completed_units.jsonl'],
            'Primary seals disagree.')
    require(manifest['execution_budget'] == contract['total_budget']
            and manifest['methods'] == contract['methods']
            and manifest['recipients'] == contract['recipients']
            and contract['consumer_budget'] in manifest['consumer_thresholds'],
            'Different primary budgets, methods or threshold declaration.')
    expected_sources = contract['primary']['source_hashes']
    require(manifest['source_hashes'] == summary['source_hashes'] == expected_sources,
            'Primary source declarations disagree.')
    for relative, expected in expected_sources.items():
        require(R.sha((ROOT / relative).read_bytes()) == expected,
                'Original live source changed: ' + relative)
    rows = [json.loads(line) for line in captured[root / 'completed_units.jsonl'].splitlines()]
    refs, baseline = {}, {}
    for number, row in enumerate(rows, 1):
        if row['kind'] == 'independent_reference':
            key = (row['stream'], row['case'])
            require(key not in refs and row['status'] == 'REFERENCE_HOLDS'
                    and row['report']['holds'] is True, 'Invalid primary scalar reference.')
            refs[key] = {'primary_line': number, 'row': row}
        elif row['kind'] == 'primary_delivery':
            key = (row['stream'], row['recipient'], row['method'], row['request_index'])
            require(key not in baseline and row['status'] == 'DELIVERED',
                    'Invalid primary delivery catalogue.')
            require(row['invoice']['consumer_budget'] is None
                    and row['invoice']['budget'] == contract['total_budget'],
                    'The matched primary must have no enforced consumer cap.')
            baseline[key] = {'primary_line': number, 'row': row}
        else:
            raise ValueError('Unexpected primary unit kind.')
    require(len(rows) == 317 and len(refs) == 29 and len(baseline) == 288,
            'Incomplete immutable primary evidence.')
    return {'captured': captured, 'manifest': manifest, 'refs': refs, 'baseline': baseline}


class Writer(R.Writer):
    def __init__(self, out, contract, contract_raw, evidence):
        super().__init__(out, 'actual-consumer-cap', argparse.Namespace(budget=contract['total_budget']))
        require(self.source_hashes == contract['primary']['source_hashes'],
                'The primary observer/worker closure changed.')
        require(self.expected_source_record == evidence['manifest']['worker_source_record'],
                'Worker procurement must remain byte-identical to the primary run.')
        source_rows = json.loads(self.expected_source_record)['sources']
        require(len(source_rows) == contract['worker_source_files'] == len(S.SOURCE_PATHS) == 8
                and {row['path'] for row in source_rows} == set(S.SOURCE_PATHS),
                'The original eight-file worker closure is required.')
        require(S.VERSION == contract['worker_revision'] and FAMILY.M is S.M,
                'Original worker revision and shared Frame identity required.')
        require(list(S.METHODS) == contract['methods']
                and contract['recipients'] == ['resident', 'fresh']
                and contract['consumer_budget'] == 2**20
                and contract['consumer_budget'] in S.CONSUMER_THRESHOLDS
                and contract['total_budget'] == S.SUCCESS_BUDGET == 2**27
                and contract['failure_reserve'] == S.FAILURE_RESERVE == 1024,
                'The fixed primary methods, modes and declared budgets are required.')
        require(R.sha((self.out / 'input_declaration.json').read_bytes())
                == contract['primary']['files']['input_declaration.json'],
                'Current fixture declaration differs from the primary inputs.')
        captured = {**evidence['captured'], Path(__file__).resolve(): Path(__file__).read_bytes(),
                    CONTRACT: contract_raw}
        for path, raw in captured.items():
            relative = str(path.relative_to(ROOT))
            target = self.out / 'sources' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            self.source_hashes[relative] = R.sha(raw)
        self.streams = FAMILY.streams()
        require([stream.name for stream in self.streams] == contract['streams']
                and all(len(stream.edits) == contract['requests_per_stream'] == 6
                        for stream in self.streams), 'Fixed four-by-six streams required.')
        self.refs, self.baseline = evidence['refs'], evidence['baseline']
        declared = {(stream.name, case.name): case
                    for stream in self.streams for case in stream.old + stream.edits}
        require(set(declared) == set(self.refs), 'Scalar references do not cover the exact old/current inputs.')
        for key, case in declared.items():
            report = self.refs[key]['row']['report']
            require(report['current_record'] == case.frame.record()
                    and report['requested_bound'] == str(case.bound)
                    and report['coverage'] == FAMILY.COVERAGE,
                    'Saved scalar truth is for a different current service.')
        expected_keys = {(stream.name, recipient, method, index)
                         for stream in self.streams for recipient in contract['recipients']
                         for method in contract['methods'] for index in range(1, 7)}
        require(set(self.baseline) == expected_keys and len(expected_keys) == contract['delivery_attempts'] == 288,
                'Primary matched catalogue or prospective attempt count differs.')
        refs_hash = R.write_json(self.out / 'reference_truths.json', list(self.refs.values()))
        self.manifest.update(
            observer_version=VERSION, contract=contract, contract_sha256=R.sha(contract_raw),
            source_hashes=self.source_hashes, execution_budget=contract['total_budget'],
            consumer_budget=contract['consumer_budget'], expected_attempts=288,
            scalar_reference_count=29, new_scalar_reference_executions=0,
            reference_truths_sha256=refs_hash,
            primary_evidence_hashes=contract['primary']['files'],
            exposure=contract['selection'],
            source_procurement='Original primary eight-file worker closure; additions are observer apparatus.',
            old_specs_policy='Exact original primary Session constructor for every method.',
            scope='Separate post-exposure funded-state DEVELOPMENT; outside primary and secondary populations.')
        self.manifest_hash = R.write_json(self.out / 'manifest.json', self.manifest)
        self.stable()


def observe(worker, previous_ids, row):
    receipt = worker.current_receipt(row['request_id'])
    return {
        'current_receipt_present': receipt is not None,
        'current_receipt_equals_output': receipt is not None
            and R.canonical(receipt) == R.canonical(json.loads(row['output'])),
        'stale_receipts_present': [old for old in previous_ids if worker.current_receipt(old) is not None],
        'scientific_state_empty': all(getattr(worker, key) is None for key in
            ('manager', 'cursor', 'receiver', 'producer_cache', 'receiver_cache'))
            and not worker.old_packets and not worker.old_input_records,
        'source_enrolled': worker.source_enrolled,
    }


def check_attempt(writer, contract, case, row, reference):
    writer.check(row['status'] in ('DELIVERED', 'NO_CURRENT_CERTIFICATE'), 'Unknown worker outcome.')
    R.assert_service(writer, case, row)
    invoice = row['invoice']
    writer.check(invoice['budget'] == contract['total_budget']
                 and invoice['consumer_budget'] == contract['consumer_budget'], 'Different actual budget.')
    writer.check(all(type(value) is int and value >= 0
                     for values in invoice['by_stage'].values() for value in values.values()),
                 'Noninteger or negative invoice category.')
    writer.check(sum(sum(values.values()) for values in invoice['by_stage'].values()) == invoice['total_units'],
                 'Invoice total does not sum.')
    writer.check(sum(sum(values.values()) for stage, values in invoice['by_stage'].items()
                     if stage.startswith('receiver_') or stage in ('terminal', 'failure_terminal', 'common_source'))
                 == invoice['consumer_units'], 'Consumer invoice does not sum.')
    writer.check(0 <= invoice['total_units'] <= contract['total_budget']
                 and 0 <= invoice['consumer_units'] <= contract['consumer_budget'], 'An actual cap was exceeded.')
    observation = row['observer_state']
    delivered = row['status'] == 'DELIVERED'
    writer.check(observation['current_receipt_present'] == delivered
                 and not observation['stale_receipts_present'], 'Wrong current/stale receipt authority.')
    if delivered:
        expected = {key: reference['report'][key] for key in
                    ('status', 'bound', 'incumbent_rank', 'feasibility', 'coverage')}
        expected.update(schema='rp3bb.current-bound.v1', current_record=case.frame.record(),
                        request_id=row['request_id'], unit=case.frame.unit,
                        witness=list(case.witness), source_record=writer.expected_source_record)
        writer.check(R.canonical(json.loads(row['output'])) == R.canonical(expected),
                     'Delivered output differs from the complete independently fixed service.')
        writer.check(observation['current_receipt_equals_output'] and row['error'] is None
                     and invoice['failure'] is None, 'Delivered authority or failure metadata disagrees.')
    else:
        writer.check(observation['scientific_state_empty'], 'Failed scientific caches survived.')
        writer.check(sum(invoice['by_stage'].get('failure_terminal', {}).values())
                     == contract['failure_terminal_units'] == 113, 'Failure terminal was not fully paid.')
        writer.check(row['error'] is not None and invoice['failure'] is not None,
                     'Failed attempt lost its cause.')


def run_attempts(writer, contract):
    issued = set()
    for stream in writer.streams:
        for recipient in contract['recipients']:
            for method in contract['methods']:
                worker = R.session(writer, stream, method, recipient)
                previous_ids = []
                for index, case in enumerate(stream.edits, 1):
                    key = (stream.name, recipient, method, index)
                    baseline = writer.baseline[key]
                    source = baseline['row']
                    issued_input = {'current_record_sha256': R.sha(case.frame.record().encode('ascii')),
                                    'witness': list(case.witness), 'bound': str(case.bound)}
                    try:
                        row = worker.deliver(case.frame, case.witness, case.bound,
                                             budget=contract['total_budget'],
                                             consumer_budget=contract['consumer_budget'])
                    except BaseException as failure:
                        writer.save({'kind': 'consumer_cap_harness_exception', 'status': 'HARNESS_EXCEPTION',
                                     'stream': stream.name, 'recipient': recipient, 'method': method,
                                     'request_index': index, 'case': case.name, 'issued_input': issued_input,
                                     'error': {'type': type(failure).__name__, 'message': str(failure)},
                                     'invoice_unavailable': True})
                        raise
                    bill = source['invoice']['consumer_units']
                    row.update(kind='actual_consumer_cap_delivery', case=case.name, issued_input=issued_input,
                               primary_observer={'primary_line': baseline['primary_line'],
                                   'primary_consumer_units': bill,
                                   'primary_bill_leq_cap': bill <= contract['consumer_budget'],
                                   'primary_bill_plus_reserve_leq_cap':
                                       bill + contract['failure_reserve'] <= contract['consumer_budget']})
                    try:
                        row['observer_state'] = observe(worker, previous_ids, row)
                    except BaseException as failure:
                        row['observer_error'] = {'type': type(failure).__name__, 'message': str(failure)}
                        writer.save(row)
                        raise
                    writer.save(row)
                    writer.check(key not in issued and row['stream'] == stream.name
                                 and row['method'] == method and row['recipient'] == recipient
                                 and row['request_index'] == index
                                 and row['request_id'] == stream.name + ':' + str(index)
                                 and source['case'] == case.name, 'Wrong or duplicate issued request.')
                    issued.add(key)
                    check_attempt(writer, contract, case, row, writer.refs[(stream.name, case.name)]['row'])
                    previous_ids.append(row['request_id'])
    writer.check(len(issued) == len(writer.units) == contract['delivery_attempts'] == 288,
                 'Incomplete fixed actual-cap sequence.')
    writer.stable()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    contract_raw = CONTRACT.read_bytes()
    contract = json.loads(contract_raw)
    evidence = primary_evidence(contract)
    writer = Writer(args.out, contract, contract_raw, evidence)
    error = None
    try:
        run_attempts(writer, contract)
    except BaseException as failure:
        error = {'type': type(failure).__name__, 'message': str(failure),
                 'traceback': traceback.format_exc()}
    result = writer.finish(error)
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
