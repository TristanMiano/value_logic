#!/usr/bin/env python3
"""Post-primary ordinary fresh-recipient control with fully paid DAG pruning.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT.
This adapter leaves the primary v5 source and data intact. Every compared method
in the secondary process enrolls the same expanded source closure. The receiver,
event tariff, live-state period convention and failure governor are unchanged.
"""
from __future__ import annotations

from pathlib import Path
import importlib.util
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def load(name, filename):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


S = load('_rp3bb_delivery_service', '05_certificate_delivery_service.py')
PRUNE = load('_rp3bb_add_evidence_prune', '05_add_evidence_prune.py')
VERSION = 'rp3bb-pruned-certificate-service-v1'
METHOD = 'O-ADD-WARM-PRUNED'
METHODS = ('P-REUSE', 'O-ADD-COLD', 'O-ADD-WARM', METHOD,
           'O-ENUM-RECEIVER', 'O-ADD-PORTFOLIO')
SOURCE_PATHS = (*S.SOURCE_PATHS, 'v3/checks/05_add_evidence_prune.py',
                'v3/checks/05_certificate_delivery_pruned_service.py')
# This secondary process has a prospectively declared larger installed program.
# Existing source files are not rewritten. The common enrollment method reads
# this complete owned closure for every arm, including ordinary direct checks.
S.SOURCE_PATHS = SOURCE_PATHS
S.METHODS = (*S.METHODS, METHOD)


class PrunedSession(S.Session):
    def __init__(self, stream_name, nbits, order, expected_source_record):
        super().__init__(METHOD, 'fresh', stream_name, nbits, order, (), expected_source_record)
        self.prune_limit_steps = PRUNE.MAX_DEPENDENCY_STEPS

    def _producer_state(self):
        record = super()._producer_state()
        record['prune_limit_steps'] = self.prune_limit_steps
        return record

    def _execute(self, meter, frame, witness, bound, request_id, work):
        if not self.source_enrolled:
            self._enroll(meter)
        expected_record = meter.run('request_encoding', frame.record)
        request = meter.run('request_encoding', lambda: S.request_wire(
            frame, witness, bound, request_id))
        meter.bytes('receiver_input', 'current_request_bytes', request)
        current_r, witness_r, bound_r = meter.run('receiver_input', lambda: S.request_from_wire(
            request, expected_record, request_id))
        meter.bytes('producer_input', 'current_request_bytes', request)
        current_p, witness_p, bound_p = meter.run('producer_input', lambda: S.request_from_wire(
            request, expected_record, request_id))
        if self.manager is None:
            self.manager = self._manager(meter)
        full = meter.run('producer_build', lambda: S.A.export_dag(
            self.manager, current_p, witness_p, bound_p, expected_record, work=work))
        evidence = meter.run('producer_prune', lambda: PRUNE.prune_full(
            full, current_p, witness_p, bound_p, expected_record,
            work=work, limit_steps=self.prune_limit_steps))
        # The unpruned immutable export is temporary. Its construction and
        # pruning are paid, but it is not deliberately retained at delivery.
        del full
        packet = meter.run('producer_export', lambda: S.A.to_wire(evidence, work))
        meter.bytes('producer_export', 'proof_output_bytes', packet)
        meter.bytes('receiver_input', 'proof_input_bytes', packet)
        candidate_receiver = self._receiver(meter)
        report = meter.run('receiver_check', lambda: candidate_receiver.receive(
            packet, current_r, expected_record, witness_r, bound_r,
            work=work, request_id=request_id))
        common = meter.run('terminal', lambda: S.common_report(
            report, current_r, witness_r, bound_r, request_id, self.source_record))
        output = meter.run('terminal', lambda: S.encode(common))
        self.cursor = None
        producer_bytes = meter.retain('producer', 'producer', lambda: {
            'retained': self._producer_state(), 'current_request': request.decode('ascii'),
            'current_evidence': packet.decode('ascii')})
        receiver_bytes = meter.retain('receiver', 'receiver', lambda: {
            'retained': self._receiver_state(candidate_receiver, None, output, request_id),
            'current_request': request.decode('ascii'),
            'current_evidence': packet.decode('ascii')})
        meter.bytes('terminal', 'current_receipt_output_bytes', output)
        meter.charge('terminal', 'delivery_events', 1)
        meter.charge('terminal', 'candidate_publication_events', 1)
        # The unchanged base governor disposes of this fresh receiver only after
        # its live period and current output have both been fully paid.
        return output, candidate_receiver, None, len(packet), producer_bytes, receiver_bytes


def make_session(method, stream, expected_source_record):
    """Only methods actually using old domains retain those supplied recipes."""
    if method not in METHODS:
        raise ValueError('Declared secondary method required.')
    if method == METHOD:
        return PrunedSession(stream.name, stream.nbits, stream.order, expected_source_record)
    old = ([(case.frame, case.witness, case.bound) for case in stream.old]
           if method in ('P-REUSE', 'O-ADD-PORTFOLIO') else [])
    return S.Session(method, 'fresh', stream.name, stream.nbits, stream.order,
                     old, expected_source_record)
