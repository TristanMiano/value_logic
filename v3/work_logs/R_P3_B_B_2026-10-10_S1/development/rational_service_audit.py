#!/usr/bin/env python3
"""One declared 30-unit arithmetic-fragment/failure service diagnostic.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT only.
Worker and inherited sources stay unchanged; this script is observer apparatus.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import importlib.util
import json
import sys
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = HERE / 'rational_service_contract_v1.json'
WITNESS = HERE.parent / 'reviews/receiver_reconstruction/rational_fragment_v1/run/current_frame_record.json'
spec = importlib.util.spec_from_file_location('_rp3bb_rational_audit_runner',
                                            ROOT / 'v3/checks/05_certificate_delivery_run.py')
R = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = R
spec.loader.exec_module(R)
S, K, M, FAMILY = R.S, R.S.K, R.S.M, R.FAMILY


def cases():
    saved = json.loads(WITNESS.read_text())
    negative = S.frame_from_record(M.canonical(saved))
    positive = M.Frame(K.Request(1, (), (),
        (('difference', K.scale(-1, negative.difference)),),
        'rp3bb-positive-rational-scope-v1', M.canonical({'case': 'positive'})),
        'difference', negative.unit)
    p, q = 2**127 - 1, 2**127 - 3
    cutoff = M.Frame(K.Request(1, (),
        (K.Soft('left', K.bit(0), F(1, p), 0),
         K.Soft('right', K.bit(0), F(1, q), 0)),
        (('difference', K.lit(0)),), 'rp3bb-cutoff-rational-scope-v1',
        M.canonical({'case': 'cutoff', 'p': str(p), 'q': str(q)})),
        'difference', negative.unit)
    zero = M.Frame(K.Request(1, (), (), (('difference', K.lit(0)),),
        'rp3bb-rational-recovery-v1', M.canonical({'case': 'recovery'})),
        'difference', negative.unit)
    return [FAMILY.Case(name, frame, (0,), F(0)) for name, frame in (
        ('large_negative_constant', negative), ('large_positive_constant', positive),
        ('large_incumbent_cutoff', cutoff), ('zero_work_capacity', zero),
        ('recovery_zero', zero))]


class Writer(R.Writer):
    def __init__(self, out, contract, declared_cases):
        super().__init__(out, 'rational-fragment-service', argparse.Namespace(budget=contract['normal_budget']))
        for source in (Path(__file__), CONTRACT, WITNESS):
            relative = str(source.relative_to(ROOT))
            content = source.read_bytes()
            target = self.out / 'sources' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            self.source_hashes[relative] = R.sha(content)
        assert self.source_hashes['v3/checks/05_certificate_delivery_service.py'] == contract['worker_sha256']
        inputs = [{'name': case.name, 'current_record': case.frame.record(),
                   'witness': case.witness, 'bound': str(case.bound)} for case in declared_cases]
        input_hash = R.write_json(self.out / 'scope_input_declaration.json', inputs)
        self.manifest.update(recipients=['fresh'], source_hashes=self.source_hashes,
            contract=contract, contract_sha256=R.sha(CONTRACT.read_bytes()),
            scope_inputs_sha256=input_hash, expected_units=30,
            scope='Out-of-fragment/failure diagnostic; excluded from comparative delivery populations.')
        self.manifest_hash = R.write_json(self.out / 'manifest.json', self.manifest)


def run(out):
    contract = json.loads(CONTRACT.read_text())
    declared = cases()
    writer = Writer(out, contract, declared)
    expected = {row['name']: set(row['expected_delivered']) for row in contract['sequence']}
    try:
        for method in contract['methods']:
            session = S.Session(method, 'fresh', 'rational-fragment-service-v1',
                                1, (0,), (), writer.expected_source_record)
            previous_ids = []
            for case in declared:
                budget = contract['denial_budget'] if case.name == 'zero_work_capacity' else contract['normal_budget']
                row = session.deliver(case.frame, case.witness, case.bound, budget=budget)
                row.update(kind='rational_scope_delivery', case=case.name,
                           expected_delivered=method in expected[case.name])
                row['current_receipt_present'] = session.current_receipt(row['request_id']) is not None
                row['stale_receipts_present'] = [old for old in previous_ids
                                                if session.current_receipt(old) is not None]
                row['scientific_state_empty'] = all(getattr(session, key) is None for key in
                    ('manager', 'cursor', 'receiver', 'producer_cache', 'receiver_cache')) and not session.old_packets
                writer.save(row)
                writer.check((row['status'] == 'DELIVERED') == row['expected_delivered'],
                             'Unexpected fragment acceptance or failure.')
                R.assert_service(writer, case, row)
                invoice = row['invoice']
                writer.check(sum(sum(v.values()) for v in invoice['by_stage'].values()) == invoice['total_units'],
                             'Invoice categories do not sum.')
                writer.check(not row['stale_receipts_present'], 'A stale receipt remains current.')
                writer.check(row['current_receipt_present'] == row['expected_delivered'], 'Wrong receipt availability.')
                if row['status'] == 'NO_CURRENT_CERTIFICATE':
                    writer.check(row['scientific_state_empty'], 'Failed scientific state was not evicted.')
                    writer.check(sum(invoice['by_stage']['failure_terminal'].values()) == 113,
                                 'Failure terminal was not paid exactly.')
                if case.name == 'large_negative_constant' and not row['expected_delivered']:
                    writer.check(row['error']['type'] == 'EvidenceLimit',
                                 'Large exact result failed for an unrelated reason.')
                    writer.check(row['error']['message'] == 'Evidence rational component cap.',
                                 'Large exact result did not reach the declared evidence cap.')
                if case.name == 'large_incumbent_cutoff' and not row['expected_delivered']:
                    writer.check(row['error']['type'] == 'ValueError',
                                 'Native large-cutoff path failed for an unrelated reason.')
                    writer.check(row['error']['message'] == 'Input rational exceeds 128-bit component cap.',
                                 'Native cutoff did not fail at a rational restriction.')
                if case.name == 'zero_work_capacity':
                    writer.check(row['error']['type'] == 'ResourceExhausted', 'Wrong governor failure.')
                    writer.check(invoice['total_units'] == 113, 'Zero worker capacity did work.')
                previous_ids.append(row['request_id'])
        writer.check(len(writer.units) == 30, 'Incomplete fixed scope diagnostic.')
    except BaseException:
        writer.finish(traceback.format_exc())
        raise
    return writer.finish()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    run(parser.parse_args().out)
