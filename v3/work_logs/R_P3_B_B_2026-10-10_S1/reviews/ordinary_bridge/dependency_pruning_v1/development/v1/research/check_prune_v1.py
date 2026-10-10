"""Fixed source-bound dependency-pruning checks; DEVELOPMENT, zero clock credit."""
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import traceback

sys.dont_write_bytecode = True


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name, path):
    if name in sys.modules:
        raise RuntimeError('The fixed check needs a fresh interpreter: ' + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(source_root, out):
    source_root, out = Path(source_root).resolve(), Path(out).resolve()
    if out.exists():
        raise RuntimeError('A fresh output directory is required.')
    out.mkdir(parents=True)
    frozen = source_root.parent
    manifest = json.loads((frozen / 'source_manifest.json').read_text())

    def verify_sources():
        for row in manifest['files']:
            raw = (source_root / row['path']).read_bytes()
            assert len(raw) == row['bytes'] and digest(raw) == row['sha256']
        for row in manifest['research']:
            raw = (frozen / 'research' / row['path']).read_bytes()
            assert len(raw) == row['bytes'] and digest(raw) == row['sha256']

    verify_sources()
    events, comparisons = [], []

    def save(name, value, *, raw=False):
        path = out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = value if raw else (canonical(value) + '\n').encode('ascii')
        path.write_bytes(payload)
        return {'path': name, 'bytes': len(payload), 'sha256': digest(payload)}

    def event(name, **record):
        row = {'name': name, **record}
        events.append(row)
        with (out / 'events.jsonl').open('a') as handle:
            handle.write(canonical(row) + '\n')
        return row

    def rejected(name, expected, callback, work):
        try:
            callback()
        except expected as error:
            return event(name, status='EXPECTED_REJECTION',
                         exception=type(error).__name__, reason=str(error), work=work)
        raise AssertionError('Expected rejection did not occur: ' + name)

    try:
        Z = load('_rp3bb_add_evidence_prune', source_root / 'v3/checks/05_add_evidence_prune.py')
        E, M, K = Z.E, Z.M, Z.K
        C = load('_rp3bb_certificate_cases', source_root / 'v3/checks/05_certificate_delivery_cases.py')
        assert C.M is M and C.K is K
        R = E.receiver_module()
        streams = C.streams()
        assert [(s.name, s.nbits, len(s.edits)) for s in streams] == [
            ('constant_n3', 3, 6), ('parity_reassociation_n6', 6, 6),
            ('complementary_k3_n5', 5, 6), ('complementary_k5_n7', 7, 6)]
        save('inputs.json', {'stage': 'DEVELOPMENT', 'streams': [s.record() for s in streams],
                             'dependency_step_limit': Z.MAX_DEPENDENCY_STEPS,
                             'primary_clock_credit_seconds': 0})
        setup = {}
        source_paths = (*Z.SOURCE_PATHS, 'v3/checks/05_certificate_delivery_cases.py')
        source_record = E.make_source_record(source_paths, repo_root=source_root, work=setup)
        save('source_record.json', source_record.encode('ascii'), raw=True)
        common_fields = ('status', 'version', 'current_record', 'bound',
                         'non_deterioration', 'feasibility', 'incumbent_rank',
                         'coverage', 'selected_identities_claimed', 'certificate_format',
                         'mode', 'epoch', 'request_id', 'receipt_number', 'trusted_cache')
        saved = {}

        def compare(stream, case, manager, index, *, label=None, convenience=False):
            label = stream.name if label is None else label
            producer_work, full_receiver_work = {}, {}
            prune_work, pruned_receiver_work = {}, {}
            before = manager.state_bytes()
            full = E.export_dag(manager, case.frame, case.witness, case.bound,
                                case.frame.record(), work=producer_work)
            full_wire = E.to_wire(full, producer_work)
            full_path = f'packets/{label}/{index:02d}.full.json'
            full_file = save(full_path, full_wire, raw=True)
            full_receiver = R.Receiver(source_record, manager.context.epoch,
                                       stream.nbits, manager.order, work=full_receiver_work)
            request_id = label + ':' + str(index)
            full_report = full_receiver.receive(
                full_wire, case.frame, case.frame.record(), case.witness, case.bound,
                work=full_receiver_work, request_id=request_id)
            after_export = manager.state_bytes()
            if convenience:
                separate = E.RecordingManager(stream.nbits, manager.order,
                                               source_record=source_record,
                                               epoch=manager.context.epoch, work=prune_work)
                pruned = Z.export_pruned(separate, case.frame, case.witness, case.bound,
                                         case.frame.record(), work=prune_work)
                assert separate.state_bytes() == after_export
            else:
                pruned = Z.prune_full(full, case.frame, case.witness, case.bound,
                                      case.frame.record(), work=prune_work)
            assert manager.state_bytes() == after_export
            pruned_wire = E.to_wire(pruned, prune_work)
            pruned_file = save(f'packets/{label}/{index:02d}.pruned.json', pruned_wire, raw=True)
            assert E.from_wire(pruned_wire) == pruned
            pruned_receiver = R.Receiver(source_record, manager.context.epoch,
                                         stream.nbits, manager.order, work=pruned_receiver_work)
            pruned_report = pruned_receiver.receive(
                pruned_wire, case.frame, case.frame.record(), case.witness, case.bound,
                work=pruned_receiver_work, request_id=request_id)
            assert all(full_report[key] == pruned_report[key] for key in common_fields)
            assert full_receiver.current_receipt(request_id) == full_report
            assert pruned_receiver.current_receipt(request_id) == pruned_report
            full_counts = tuple(len(rows) for rows in (full.nodes, full.applies, full.expressions))
            pruned_counts = tuple(len(rows) for rows in (pruned.nodes, pruned.applies, pruned.expressions))
            assert all(a <= b for a, b in zip(pruned_counts, full_counts))
            assert len(pruned_wire) <= len(full_wire)
            state_file = save(f'states/{label}/{index:02d}.manager.json', after_export, raw=True)
            row = event('compare:' + label + ':' + str(index), status='PASS',
                        stream=label, request_index=index, current_record=case.frame.record(),
                        full=full_file, pruned=pruned_file,
                        full_counts=dict(zip(('nodes', 'applies', 'expressions'), full_counts)),
                        pruned_counts=dict(zip(('nodes', 'applies', 'expressions'), pruned_counts)),
                        saved_wire_bytes=len(full_wire)-len(pruned_wire),
                        producer_work=producer_work, pruning_work=prune_work,
                        pruning_work_includes_separate_full_export=convenience,
                        receiver_execution_order=['full', 'pruned'],
                        full_receiver_work=full_receiver_work,
                        pruned_receiver_work=pruned_receiver_work,
                        full_report=full_report, pruned_report=pruned_report,
                        manager_before_bytes=len(before), manager_after_bytes=len(after_export),
                        manager_unchanged_by_pruning=True, warm_manager_state=state_file)
            return full, pruned, pruned_wire, row

        for stream in streams:
            manager = E.RecordingManager(stream.nbits, stream.order,
                                           source_record=source_record,
                                           epoch='pruning-v1:' + stream.name, work=setup)
            for index, case in enumerate(stream.edits):
                full, pruned, wire, row = compare(stream, case, manager, index)
                comparisons.append(row)
                saved[(stream.name, index)] = (full, pruned, wire, case)

        parity = next(s for s in streams if s.name == 'parity_reassociation_n6')
        reverse = E.RecordingManager(parity.nbits, tuple(reversed(parity.order)),
                                     source_record=source_record,
                                     epoch='pruning-v1:reverse-order', work=setup)
        compare(parity, parity.edits[0], reverse, 0, label='reverse_order_parity_n6',
                convenience=True)

        _, last, last_wire, last_case = saved[('complementary_k5_n7', 5)]
        work = {}
        twice = Z.prune_full(last, last_case.frame, last_case.witness, last_case.bound,
                             last_case.frame.record(), work=work)
        assert E.to_wire(twice, work) == last_wire
        event('idempotence_last_complement_k5', status='PASS', work=work,
              wire_sha256=digest(last_wire))

        first_full, first, _, first_case = saved[(parity.name, 0)]
        terminal_bound = first.nodes.index(('T', first_case.bound.numerator, first_case.bound.denominator))
        loss_test = next(row[3] for row in first.applies
                         if row[:3] == ('gt', first.roots[2], terminal_bound))
        left, right = sorted((first.roots[0], loss_test))
        key = ('and', left, right)
        assert sum(row[:3] == key for row in first.applies) == 1
        missing = replace(first, applies=tuple(row for row in first.applies if row[:3] != key))
        missing_wire = E.to_wire(missing)
        save('adverse/missing_required_apply.json', missing_wire, raw=True)
        work = {}
        rejected('missing_dependency_pruner', Z.PruneRejected,
                 lambda: Z.prune_full(missing, first_case.frame, first_case.witness,
                                       first_case.bound, first_case.frame.record(), work=work), work)
        work = {}
        bad_receiver = R.Receiver(source_record, missing.epoch, missing.bits, missing.order,
                                  work=work)
        rejected('missing_dependency_receiver', R.Rejected,
                 lambda: bad_receiver.receive(missing_wire, first_case.frame,
                                               first_case.frame.record(), first_case.witness,
                                               first_case.bound, work=work,
                                               request_id='missing-required-apply'), work)
        assert bad_receiver.state_counts() == {'nodes': 0, 'applies': 0, 'expressions': 0}
        assert bad_receiver.current_receipt('missing-required-apply') is None

        second_full, _, _, second_case = saved[(parity.name, 1)]
        base = tuple(len(rows) for rows in (first_full.nodes, first_full.applies, first_full.expressions))
        delta = replace(second_full, mode='delta', base=base,
                        nodes=second_full.nodes[base[0]:], applies=second_full.applies[base[1]:],
                        expressions=second_full.expressions[base[2]:])
        save('adverse/genuine_delta.json', E.to_wire(delta), raw=True)
        work = {}
        rejected('reject_delta_input', Z.PruneRejected,
                 lambda: Z.prune_full(delta, second_case.frame, second_case.witness,
                                      second_case.bound, second_case.frame.record(), work=work), work)

        input_wire = E.to_wire(first_full)
        work = {}
        rejected('one_step_guard', Z.PruneLimit,
                 lambda: Z.prune_full(first_full, first_case.frame, first_case.witness,
                                      first_case.bound, first_case.frame.record(),
                                      work=work, limit_steps=1), work)
        assert work['prune_steps'] <= 1 and E.to_wire(first_full) == input_wire

        false_frame = M.Frame(K.Request(1, (), (), (('difference', K.bit(0)),),
                                        'pruning-v1-false-bound'), 'difference', 'task_loss')
        work = {}
        false_manager = E.RecordingManager(1, source_record=source_record,
                                           epoch='pruning-v1:false', work=work)
        try:
            Z.export_pruned(false_manager, false_frame, (0,), F(0), false_frame.record(), work=work)
        except E.NoBoundProof as error:
            assert error.counterexample == (1,)
            assert K.interval(false_frame.difference, error.counterexample) == (F(1), F(1))
            event('actual_false_bound', status='EXPECTED_REJECTION',
                  exception=type(error).__name__, reason=str(error),
                  counterexample=error.counterexample, work=work)
        else:
            raise AssertionError('False bound unexpectedly produced evidence.')

        summary = []
        for stream in streams:
            rows = [row for row in comparisons if row['stream'] == stream.name]
            summary.append({'stream': stream.name, 'requests': len(rows),
                            'full_wire_bytes': sum(row['full']['bytes'] for row in rows),
                            'pruned_wire_bytes': sum(row['pruned']['bytes'] for row in rows),
                            'saved_wire_bytes': sum(row['saved_wire_bytes'] for row in rows),
                            'max_prune_steps': max(row['pruning_work']['prune_steps'] for row in rows)})
        result = {'stage': 'DEVELOPMENT', 'status': 'PASS',
                  'interpretation': 'Dependency/wire comparison only; no complete scalar cost or superiority claim.',
                  'version': Z.VERSION, 'dependency_step_limit': Z.MAX_DEPENDENCY_STEPS,
                  'primary_comparisons': len(comparisons), 'events': len(events),
                  'principal_clock_credit_seconds': 0, 'setup_work': setup,
                  'source_manifest_sha256': digest((frozen/'source_manifest.json').read_bytes()),
                  'source_record_sha256': digest(source_record.encode('ascii')),
                  'streams': summary, 'completed_utc': datetime.now(timezone.utc).isoformat()}
        save('results.json', result)
        verify_sources()
        rows = []
        for path in sorted(out.rglob('*')):
            if path.is_file():
                raw = path.read_bytes()
                rows.append({'path': path.relative_to(out).as_posix(),
                             'bytes': len(raw), 'sha256': digest(raw)})
        save('manifest.json', {'stage': 'DEVELOPMENT', 'files': rows})
        print(json.dumps(result, sort_keys=True))
    except BaseException as error:
        save('failure.json', {'status': 'UNEXPECTED_FAILURE', 'exception': type(error).__name__,
                              'message': str(error), 'traceback': traceback.format_exc(),
                              'events_completed': len(events), 'principal_clock_credit_seconds': 0})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    run(args.source_root, args.out)
