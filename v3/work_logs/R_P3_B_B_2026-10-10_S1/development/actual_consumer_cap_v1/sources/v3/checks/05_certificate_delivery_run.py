#!/usr/bin/env python3
"""Source-bound development execution writer for the Option B common service.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. This observer, independent
truth oracle and artifact writer are outside the worker's event/byte tariff.
Every materialized or transmitted worker packet is retained by content hash.
Output directories are fresh; completed units and failed source revisions stay.
"""
from __future__ import annotations

from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import platform
import sys
import time
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


S = load('_rp3bb_delivery_service', '05_certificate_delivery_service.py')
FAMILY = load('_rp3bb_delivery_cases', '05_certificate_delivery_cases.py')


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def write_json(path, value):
    raw = (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n').encode('ascii')
    path.write_bytes(raw)
    return sha(raw)


class Writer:
    def __init__(self, destination, suite, args):
        self.out = destination.resolve()
        self.out.mkdir(parents=True, exist_ok=False)
        (self.out / 'sources').mkdir()
        (self.out / 'blobs').mkdir()
        self.source_hashes = {}
        source_paths = (*S.SOURCE_PATHS, 'v3/checks/05_certificate_delivery_run.py')
        for relative in source_paths:
            content = (ROOT / relative).read_bytes()
            self.source_hashes[relative] = sha(content)
            target = self.out / 'sources' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        self.expected_source_record = S.A.make_source_record(S.SOURCE_PATHS, repo_root=ROOT)
        self.manifest = {
            'schema': 'value_logic.rp3bb.development-run.v1', 'stage': 'DEVELOPMENT',
            'task': 'R-P3-B-B', 'suite': suite,
            'prepared_utc': datetime.now(timezone.utc).isoformat(),
            'python': sys.version, 'platform': platform.platform(),
            'command': sys.argv, 'source_hashes': self.source_hashes,
            'worker_source_record': self.expected_source_record,
            'tariff': S.TARIFF, 'execution_budget': args.budget,
            'methods': list(S.METHODS), 'recipients': ['resident', 'fresh'],
            'consumer_thresholds': list(S.CONSUMER_THRESHOLDS),
            'observer_and_reference_oracle_in_worker_bill': False,
            'scope': 'Finite fixed development cases; no final challenge or statistical population.'}
        self.manifest_hash = write_json(self.out / 'manifest.json', self.manifest)
        self.units = []
        self.counts = {'delivered': 0, 'failed_delivery': 0, 'assertions': 0}
        self.started = time.monotonic_ns()
        write_json(self.out / 'input_declaration.json', FAMILY.declaration())

    def stable(self):
        for relative, expected in self.source_hashes.items():
            if sha((ROOT / relative).read_bytes()) != expected:
                raise RuntimeError('Source changed during execution: ' + relative)

    def check(self, condition, message):
        self.counts['assertions'] += 1
        if not condition:
            raise AssertionError(message)

    def save(self, unit):
        references = []
        for stage, category, payload in unit.pop('audit_packets', []):
            digest = sha(payload)
            target = self.out / 'blobs' / (digest + '.json')
            if not target.exists():
                target.write_bytes(payload)
            elif target.read_bytes() != payload:
                raise AssertionError('Content-addressed packet collision.')
            references.append({'stage': stage, 'category': category,
                               'bytes': len(payload), 'sha256': digest,
                               'path': 'blobs/' + target.name})
        unit['observed_packet_references'] = references
        if unit.get('status') == 'DELIVERED':
            self.counts['delivered'] += 1
        elif unit.get('status') == 'NO_CURRENT_CERTIFICATE':
            self.counts['failed_delivery'] += 1
        self.units.append(unit)
        with (self.out / 'completed_units.jsonl').open('a') as handle:
            handle.write(canonical(unit) + '\n')
            handle.flush()
        self.stable()
        print(canonical({'unit': len(self.units), 'kind': unit.get('kind'),
                         'stream': unit.get('stream'), 'method': unit.get('method'),
                         'recipient': unit.get('recipient'), 'index': unit.get('request_index'),
                         'status': unit.get('status'),
                         'units': unit.get('invoice', {}).get('total_units')}), flush=True)

    def finish(self, error=None):
        status = 'FAIL' if error else 'PASS'
        summary = {'schema': 'value_logic.rp3bb.run-summary.v1',
                   'stage': 'DEVELOPMENT', 'status': status,
                   'suite': self.manifest['suite'], 'manifest_sha256': self.manifest_hash,
                   'units': len(self.units), 'counts': self.counts,
                   'elapsed_ns': time.monotonic_ns() - self.started,
                   'source_hashes': self.source_hashes,
                   'completed_units_sha256': (sha((self.out / 'completed_units.jsonl').read_bytes())
                                              if (self.out / 'completed_units.jsonl').exists() else None),
                   'finished_utc': datetime.now(timezone.utc).isoformat(), 'error': error}
        write_json(self.out / 'summary.json', summary)
        print(json.dumps(summary, indent=2), flush=True)
        return summary


def session(writer, stream, method, recipient):
    return S.Session(method, recipient, stream.name, stream.nbits, stream.order,
                     [(case.frame, case.witness, case.bound) for case in stream.old],
                     writer.expected_source_record)


def assert_service(writer, case, row):
    if row['status'] != 'DELIVERED':
        writer.check(row['output'] == S.FAILURE_PAYLOAD.decode('ascii'), 'Failure payload changed.')
        writer.check(row['invoice']['total_units'] <= row['invoice']['budget'], 'Failure overspent budget.')
        return
    report = json.loads(row['output'])
    writer.check(report['status'] == 'CURRENT_BOUND_CERTIFIED', 'Wrong receipt service.')
    writer.check(report['current_record'] == case.frame.record(), 'Delivered wrong request.')
    writer.check(report['bound'] == str(case.bound), 'Delivered wrong requested bound.')
    writer.check(report['feasibility'] == 'NONEMPTY', 'Vacuous receipt.')
    writer.check(report['coverage'] == FAMILY.COVERAGE, 'Narrowed incumbent sublevel.')
    writer.check(tuple(report['witness']) == case.witness, 'Changed supplied incumbent.')
    writer.check(row['invoice']['total_units'] <= row['invoice']['budget'], 'Success overspent budget.')


def references(writer, streams):
    for stream in streams:
        for case in stream.old + stream.edits:
            report = FAMILY.reference_report(case)
            writer.check(report['holds'], 'Declared bound has an actual counterexample.')
            if case.named_witnesses:
                lower, upper = (F(report['diagnostics'][key])
                                for key in ('exact_lower', 'exact_upper'))
                writer.check(lower < upper, 'Complementary-domain loss became constant.')
                cutoff = F(report['incumbent_rank'])
                for name, point in case.named_witnesses:
                    writer.check(all(FAMILY.scalar_value(h, point) == 1
                                     for h in case.frame.request.hard), 'Named witness infeasible.')
                    rank = sum((row.weight * (1 - FAMILY.scalar_value(row.formula, point))
                                for row in case.frame.request.soft), F(0))
                    writer.check(rank <= cutoff, 'Named witness outside current incumbent sublevel.')
                left, right = dict(case.named_witnesses)['left_exclusive_parity_one'], dict(case.named_witnesses)['right_exclusive_parity_zero']
                writer.check(left[0:2] == (0, 0) and right[0:2] == (1, 1), 'Exclusive old-domain points lost.')
            writer.save({'kind': 'independent_reference', 'stream': stream.name,
                         'case': case.name, 'report': report, 'status': 'REFERENCE_HOLDS'})


def primary(writer, args):
    streams = FAMILY.streams()
    references(writer, streams)
    for stream in streams:
        for recipient in ('resident', 'fresh'):
            for method in S.METHODS:
                worker = session(writer, stream, method, recipient)
                for case in stream.edits:
                    row = worker.deliver(case.frame, case.witness, case.bound, budget=args.budget)
                    row.update(kind='primary_delivery', case=case.name)
                    # Save the full attempted unit even when it exposes a defect.
                    writer.save(row)
                    assert_service(writer, case, row)
                    writer.check(worker.current_receipt(row['request_id']) is not None
                                 if row['status'] == 'DELIVERED' else worker.current_receipt(row['request_id']) is None,
                                 'Current receipt disagrees with paid publication.')


def smoke(writer, args):
    streams = FAMILY.streams()
    # Declared smoke probes exercise every method and both recipient conditions,
    # followed by a real changed request under the same session. The small
    # nonconstant complement stream exposes bootstrap/codec/delta integration.
    selected = (streams[0], streams[2])
    references(writer, selected)
    for stream in selected:
        for recipient in ('resident', 'fresh'):
            for method in S.METHODS:
                worker = session(writer, stream, method, recipient)
                for case in stream.edits[:2]:
                    row = worker.deliver(case.frame, case.witness, case.bound, budget=args.budget)
                    row.update(kind='service_smoke', case=case.name)
                    writer.save(row)
                    assert_service(writer, case, row)
                    writer.check(row['status'] == 'DELIVERED', 'Smoke service did not deliver.')
                previous_id = row['request_id']
                denied = worker.deliver(stream.edits[2].frame, stream.edits[2].witness,
                                        stream.edits[2].bound, budget=S.FAILURE_RESERVE)
                denied.update(kind='reserved_failure_smoke', case=stream.edits[2].name)
                writer.save(denied)
                writer.check(denied['status'] == 'NO_CURRENT_CERTIFICATE', 'Zero-work budget delivered.')
                writer.check(worker.current_receipt(previous_id) is None, 'Old receipt survived as current.')
                writer.check(worker.current_receipt(denied['request_id']) is None, 'Denied receipt published.')
                writer.check(worker.manager is None and worker.receiver is None,
                             'Denied mutable worker state was retained.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--suite', choices=('smoke', 'primary', 'reference'), required=True)
    parser.add_argument('--budget', type=int, default=S.SUCCESS_BUDGET)
    args = parser.parse_args()
    writer = Writer(args.out, args.suite, args)
    error = None
    try:
        if args.suite == 'smoke':
            smoke(writer, args)
        elif args.suite == 'primary':
            primary(writer, args)
        else:
            references(writer, FAMILY.streams())
        writer.stable()
    except BaseException:
        error = traceback.format_exc()
    result = writer.finish(error)
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
