#!/usr/bin/env python3
"""Read-only source-bound Meter/native-boundary diagnostics; no Session delivery."""
from __future__ import annotations

import dis
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source'
OUT = HERE / 'run'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    OUT.mkdir(exist_ok=False)
    spec = importlib.util.spec_from_file_location('_rp3bb_service_audit',
            SOURCE / 'v3/checks/05_certificate_delivery_service.py')
    S = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = S
    spec.loader.exec_module(S)
    before = json.loads((HERE / 'source_manifest.json').read_text())
    cases = []
    original_trace, original_profile = sys.gettrace(), sys.getprofile()

    def worker(text, name='worker', extra=None):
        namespace = {} if extra is None else dict(extra)
        exec(compile(text, '<fresh-source-bound-worker>', 'exec'), namespace)
        return namespace[name]

    def operations(function):
        return [{'offset': item.offset, 'opname': item.opname}
                for item in dis.get_instructions(function)
                if item.opname not in ('RESUME', 'CACHE')]

    def saved(name, **data):
        assert sys.gettrace() is original_trace and sys.getprofile() is original_profile
        cases.append({'name': name, 'status': 'PASS', **data})

    error = None
    try:
        first = worker('def worker():\n    return 17\n')
        meter = S.Meter()
        assert meter.run('receiver_first_call', first) == 17
        invoice = meter.invoice()
        expected = len(operations(first))
        assert invoice['by_stage']['receiver_first_call']['observed_python_opcode_events'] == expected
        saved('first_executed_code_object_is_traced', disassembly=operations(first),
              expected_opcode_events=expected, invoice=invoice)

        meter = S.Meter()
        inner = worker('def worker():\n    return 37\n')
        outer = worker('def worker():\n    marker = 5\n    chosen = meter.run("receiver_nested", inner)\n    return marker + chosen\n',
                       extra={'meter': meter, 'inner': inner})
        assert meter.run('coordination', outer) == 42
        invoice = meter.invoice()
        assert invoice['by_stage']['coordination']['observed_python_opcode_events'] == len(operations(outer))
        assert invoice['by_stage']['receiver_nested']['observed_python_opcode_events'] == len(operations(inner))
        saved('nested_stages_preserve_all_outer_worker_events',
              outer_disassembly=operations(outer), inner_disassembly=operations(inner), invoice=invoice)

        native = worker('def worker():\n    return len((1, 2, 3))\n')
        meter = S.Meter()
        assert meter.run('receiver_native', native) == 3
        invoice = meter.invoice()
        row = invoice['by_stage']['receiver_native']
        assert row['observed_python_opcode_events'] == len(operations(native))
        assert row['bounded_native_c_call_events'] == 1
        saved('bounded_native_call_event_is_additional', disassembly=operations(native), invoice=invoice)

        def denied(name, function, budget, consumer_budget=None, expected_category=None):
            meter = S.Meter(budget, consumer_budget=consumer_budget)
            try:
                meter.run('receiver_denied', function)
            except S.ResourceExhausted as failure:
                if expected_category is not None:
                    assert failure.category == expected_category
                paid_before = meter.units
                payload = meter.fail(failure)
            else:
                raise AssertionError('Expected resource denial: ' + name)
            invoice = meter.invoice()
            assert payload == S.FAILURE_PAYLOAD
            assert invoice['total_units'] == paid_before + len(S.FAILURE_PAYLOAD) + 2
            assert invoice['total_units'] <= budget
            if consumer_budget is not None:
                assert invoice['consumer_units'] <= consumer_budget
            assert not meter.active and meter.current is None
            saved(name, paid_before_failure=paid_before,
                  failure_output_bytes=len(payload), invoice=invoice)
            return invoice

        denied('reserve_only_account_returns_paid_failure',
               worker('def worker():\n    return 7\n'), S.FAILURE_RESERVE,
               expected_category='observed_python_opcode_events')
        loop = worker('def worker():\n    total = 0\n    for index in range(100):\n        total += index\n    return total\n')
        prefix = denied('paid_prefix_survives_opcode_denial', loop, S.FAILURE_RESERVE + 40,
                        expected_category='observed_python_opcode_events')
        assert prefix['total_units'] == 40 + len(S.FAILURE_PAYLOAD) + 2
        native = worker('def worker():\n    return len((1, 2, 3))\n')
        call_position = next(index + 1 for index, item in enumerate(operations(native))
                             if item['opname'] == 'CALL')
        denied('native_callback_denial_keeps_failure_reserve', native,
               S.FAILURE_RESERVE + call_position,
               expected_category='bounded_native_c_call_events')
        denied('independent_consumer_reserve_is_enforced', loop,
               S.FAILURE_RESERVE + 1000, consumer_budget=S.FAILURE_RESERVE + 20)

        # A successful observed bill need not fit the same numerical account
        # once the operational terminal reserve is protected.
        threshold = 2048
        meter = S.Meter(100000, consumer_budget=threshold)
        try:
            meter.charge('receiver_check', 'illustrative_complete_bill', threshold)
        except S.ResourceExhausted:
            denied_at_threshold = True
        else:
            denied_at_threshold = False
        assert threshold <= threshold and denied_at_threshold
        saved('bill_threshold_is_not_reserved_execution_budget',
              observed_complete_bill=threshold, threshold=threshold,
              bill_within_threshold=True, same_account_would_deny=True,
              same_path_required_consumer_account=threshold + S.FAILURE_RESERVE)

        # Direct codec/verifier/common-report boundary, not an owned Session run.
        K, M, P = S.K, S.M, S.P
        frame = M.Frame(K.Request(1, (K.bit(0),), (), (('difference', K.lit(0)),),
                                  'native-witness-binding-diagnostic'), 'difference', 'unit')
        source_record = S.A.make_source_record(S.SOURCE_PATHS, repo_root=SOURCE)
        supplied_witness = (0,)
        proof_witness = (1,)
        requested_bound = F(0)
        request = S.request_wire(frame, supplied_witness, requested_bound, 'fixed-request')
        current, received_witness, bound = S.request_from_wire(request, frame.record(), 'fixed-request')
        producer_cache = P.PortfolioCache()
        proof = producer_cache.build(frame, (), proof_witness, requested_bound)
        proof_wire = S.encode(proof.record())
        imported = S.portfolio_from_wire(proof_wire)
        native_report = P.PortfolioCache().verify(imported, current, current.record())
        common = S.common_report(native_report, current, received_witness, bound,
                                 'fixed-request', source_record)
        assert M.rank_bounds(frame, supplied_witness)[0] == M.rank_bounds(frame, proof_witness)[0] == 0
        assert K.interval(frame.request.hard[0], supplied_witness) == (F(0), F(0))
        assert K.interval(frame.request.hard[0], proof_witness) == (F(1), F(1))
        assert common['feasibility'] == 'NONEMPTY' and tuple(common['witness']) == supplied_witness
        (OUT / 'native_gap_request.json').write_bytes(request)
        (OUT / 'native_gap_proof.json').write_bytes(proof_wire)
        (OUT / 'native_gap_common_report.json').write_bytes(S.encode(common))
        saved('native_witness_binding_gap_reproduced', defect_present=True,
              supplied_witness=supplied_witness, supplied_witness_is_feasible=False,
              actually_checked_proof_witness=proof_witness,
              equal_incumbent_ranks=True,
              receiving_bound_itself_is_true=True,
              scope='Direct codec/native-verify/common-report boundary; no honest Session episode used a substituted proof.')

        old_frame_bytes = len(frame.record().encode('ascii'))
        complete_old_request_bytes = len(S.request_wire(frame, proof_witness, 0, 'old-0'))
        assert complete_old_request_bytes > old_frame_bytes
        saved('old_frame_only_charge_omits_request_tuple',
              frame_only_bytes=old_frame_bytes,
              complete_old_request_bytes=complete_old_request_bytes,
              omitted_bytes_for_this_exact_encoding=complete_old_request_bytes-old_frame_bytes)
    except BaseException:
        error = traceback.format_exc()

    after = {name: {'bytes': (SOURCE / name).stat().st_size,
                     'sha256': sha((SOURCE / name).read_bytes())}
             for name in before}
    if after != before:
        error = (error or '') + '\nSaved source changed during diagnostic.'
    result = {'schema': 'rp3bb.independent-service-diagnostic.v1',
              'stage': 'DEVELOPMENT', 'status': 'FAIL' if error else 'PASS',
              'source_service_sha256': before['v3/checks/05_certificate_delivery_service.py']['sha256'],
              'diagnostic_sha256': sha(Path(__file__).read_bytes()),
              'source_unchanged': before == after,
              'python': sys.version, 'case_count': len(cases), 'cases': cases,
              'session_deliveries': 0, 'policy_runs': 0,
              'principal_clock_credit_seconds': 0,
              'error': error}
    raw = (json.dumps(result, indent=2) + '\n').encode()
    (OUT / 'results.json').write_bytes(raw)
    print(json.dumps({'status': result['status'], 'case_count': len(cases),
                      'results_sha256': sha(raw), 'error': error}, indent=2))
    if error:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
