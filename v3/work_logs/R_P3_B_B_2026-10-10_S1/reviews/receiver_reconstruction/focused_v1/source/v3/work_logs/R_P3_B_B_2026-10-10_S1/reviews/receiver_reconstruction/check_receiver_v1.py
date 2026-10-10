#!/usr/bin/env python3
"""Source-bound focused functional probes of the independent R-P3-B-B receiver.

This evaluator does not bill or run the parent common delivery service. Its
finite cases and mutation recipes are fixed before execution. No final freeze,
policy benchmark, physical performance or principal-clock credit is claimed.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import traceback

sys.dont_write_bytecode = True


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    source_root = args.source_root.resolve()
    producer_path = source_root / 'v3/checks/05_add_evidence.py'
    spec = importlib.util.spec_from_file_location('_rp3bb_probe_producer', producer_path)
    E = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = E
    spec.loader.exec_module(E)
    R = E.receiver_module()
    M, K = E.M, E.K
    source_record = E.make_source_record(repo_root=source_root)
    source_data = json.loads(source_record)
    before = {item['path']: {'bytes': item['bytes'], 'sha256': item['sha256']}
              for item in source_data['sources']}
    (args.out / 'source_record.json').write_text(source_record + '\n')
    cases = []
    wires = args.out / 'wires'
    wires.mkdir()
    reports = args.out / 'reports'
    reports.mkdir()

    def frame(bits, difference, hard=(), soft=(), scope='probe', metadata='{}'):
        return M.Frame(K.Request(bits, hard, soft, (('difference', difference),),
                                 scope, metadata), 'difference', 'one fixed loss unit')

    def parity(indices):
        value = K.bit(indices[0])
        for index in indices[1:]:
            value = K.neg(K.eq(value, K.bit(index)))
        return value

    def ordinary(bits, order=None, epoch='probe-epoch'):
        return E.RecordingManager(bits, order, source_record=source_record, epoch=epoch)

    def receiver(bits, order=None, epoch='probe-epoch'):
        return R.Receiver(source_record, epoch, bits, order)

    def wire(evidence):
        return E.to_wire(evidence)

    def record(name, details):
        cases.append({'name': name, 'status': 'PASS', **details})

    def accept(name, rec, evidence, current, witness, bound, *, request_id=None):
        payload = wire(evidence)
        (wires / (name + '.json')).write_bytes(payload)
        work = {}
        request_id = name if request_id is None else request_id
        report = rec.receive(payload, current, current.record(), witness, bound,
                             work=work, request_id=request_id)
        assert report['status'] == 'CURRENT_BOUND_CERTIFIED'
        assert report['current_record'] == current.record()
        assert report['feasibility'] == 'NONEMPTY'
        assert report['bound'] == str(F(bound))
        assert report['coverage'] == 'ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS'
        assert rec.current_receipt(request_id) == report
        assert rec.current_receipt('a-different-request-id') is None
        (reports / (name + '.json')).write_text(json.dumps(report, indent=2) + '\n')
        record(name, {'wire_sha256': sha(payload), 'wire_bytes': len(payload),
                      'work': work, 'admitted': rec.state_counts(),
                      'storage': rec.storage()})
        return report

    def reject(name, payload, current, witness, bound, rec=None):
        rec = receiver(current.request.nbits) if rec is None else rec
        payload = payload if type(payload) is bytes else E.canonical(payload).encode()
        (wires / (name + '.json')).write_bytes(payload)
        old = rec.state_record()
        work = {}
        try:
            rec.receive(payload, current, current.record(), witness, bound,
                        work=work, request_id=name)
        except R.Rejected as error:
            reason = str(error)
        else:
            raise AssertionError('Receiver accepted invalid case: ' + name)
        after = rec.state_record()
        assert rec.current_receipt(name) is None
        assert after['chunks'] == old['chunks']
        assert after['counts'] == old['counts']
        assert after['receipts'] == old['receipts']
        assert after['request_ids'] == old['request_ids']
        record(name, {'rejection': reason, 'wire_sha256': sha(payload),
                      'wire_bytes': len(payload), 'work': work,
                      'unchanged_admitted_chunks': True})

    error = None
    try:
        # Nonempty constant case, immutable report ownership, warm delta and cold replay.
        constant = frame(2, K.lit(-1), scope='constant')
        man = ordinary(2)
        ev = E.export_dag(man, constant, (0, 0), -1, constant.record())
        rec = receiver(2)
        report = accept('constant_full', rec, ev, constant, (0, 0), -1)
        report['bound'] = 'forged returned dictionary'
        assert rec.current_receipt('constant_full')['bound'] == '-1'
        record('returned_report_cannot_mutate_receipt', {})
        cursor = ev.next_cursor()
        edited = frame(2, K.lit(-1), hard=(K.bit(0),), scope='constant-edit')
        edited_ev = E.export_dag(man, edited, (1, 0), -1, edited.record(), base=cursor)
        rec_fork = rec.fork()
        old_record = rec.state_record()
        accept('constant_resident_delta', rec_fork, edited_ev, edited, (1, 0), -1)
        assert rec.state_record() == old_record
        assert rec.current_receipt('constant_resident_delta') is None
        record('fork_commit_does_not_publish_to_owner', {})
        full_again = E.export_dag(man, edited, (1, 0), -1, edited.record())
        cold = receiver(2)
        accept('cold_full_after_delta', cold, full_again, edited, (1, 0), -1)
        assert cold.state_counts() == rec_fork.state_counts()
        duplicate = rec_fork.fork()
        reject('full_requires_fresh_receiver', wire(full_again), edited, (1, 0), -1, duplicate)

        # All accepted expression constructors, rational weights and alternative order.
        p, q, r = K.bit(0), K.bit(1), K.bit(2)
        difference = K.add(('min', K.scale(F(3, 2), p),
                           ('max', K.scale(-2, q), K.lit(F(1, 3)))),
                          K.scale(2, K.eq(K.AND(p, K.neg(q)), K.OR(r, K.lit(0)))))
        rational = frame(3, difference,
                         soft=(K.Soft('prefer-not-p', K.neg(p), F(1, 2)),
                               K.Soft('prefer-q', q, F(2))), scope='grammar-rational')
        for name, order in (('grammar_natural_order', (0, 1, 2)),
                            ('grammar_reversed_order', (2, 1, 0))):
            manager = ordinary(3, order)
            evidence = E.export_dag(manager, rational, (0, 0, 0), 3, rational.record())
            accept(name, receiver(3, order), evidence, rational, (0, 0, 0), 3)

        # Equal parity functions and a separate legacy proof delivered to its old checker.
        parity_frame = frame(3, K.sub(parity((0, 1, 2)), parity((2, 1, 0))),
                             scope='parity')
        parity_man = ordinary(3)
        parity_ev = E.export_dag(parity_man, parity_frame, (0, 0, 0), 0,
                                 parity_frame.record())
        accept('parity_shared_dag', receiver(3), parity_ev, parity_frame, (0, 0, 0), 0)
        tree = E.export_tree(parity_man, parity_frame, (0, 0, 0), 0,
                             parity_frame.record())
        native_report = E.P.PortfolioCache().verify(tree, parity_frame, parity_frame.record())
        assert native_report['counts']['splits'] == 7
        assert native_report['counts']['direct_leaves'] == 8
        record('parity_legacy_tree_checked', {'native_counts': native_report['counts']})

        # Mutations are generated from one valid full packet and each uses a fresh receiver.
        base = json.loads(wire(parity_ev))
        def mutate(name, change):
            changed = copy.deepcopy(base)
            change(changed)
            reject(name, changed, parity_frame, (0, 0, 0), 0)
        zero = next(i for i, node in enumerate(base['nodes']) if node == ['T', 0, 1])
        one = next(i for i, node in enumerate(base['nodes']) if node == ['T', 1, 1])
        decision = next(i for i, node in enumerate(base['nodes']) if node[0] == 'N')
        mutate('unknown_top_level_field', lambda obj: obj.update(unchecked=True))
        mutate('boolean_root_id', lambda obj: obj['roots'].update(bad=False))
        mutate('unreduced_terminal', lambda obj: obj['nodes'].__setitem__(zero, ['T', 0, 2]))
        mutate('nonpositive_denominator', lambda obj: obj['nodes'].__setitem__(zero, ['T', 0, 0]))
        mutate('terminal_component_cap', lambda obj: obj['nodes'].__setitem__(zero, ['T', 1 << 4096, 1]))
        mutate('forward_node_reference', lambda obj: obj['nodes'][decision].__setitem__(2, decision))
        mutate('duplicate_node', lambda obj: obj['nodes'].append(['T', 0, 1]))
        mutate('wrong_apply_equation', lambda obj: obj['applies'][0].__setitem__(3,
                    one if obj['applies'][0][3] != one else zero))
        mutate('reversed_apply_premises', lambda obj: obj['applies'].reverse())
        mutate('missing_expression_child', lambda obj: obj['expressions'].pop(0))
        mutate('wrong_expression_denotation', lambda obj: obj['expressions'][0].__setitem__(1,
                    one if obj['expressions'][0][1] != one else zero))
        mutate('forged_guard_root', lambda obj: obj['roots'].update(guard=zero))
        mutate('wrong_source_record', lambda obj: obj.update(source_record=obj['source_record'] + ' '))
        mutate('wrong_epoch', lambda obj: obj.update(epoch='foreign-epoch'))
        mutate('wrong_variable_order', lambda obj: obj['order'].reverse())
        mutate('wrong_base_counts', lambda obj: obj['base'].update(nodes=1))
        mutate('wire_incumbent_substitution', lambda obj: obj['witness'].__setitem__(0, 1))
        mutate('wire_bound_substitution', lambda obj: obj.update(bound=[1, 1]))
        mutate('float_bound', lambda obj: obj.update(bound=[0.0, 1]))
        duplicate_json = b'{"schema":"' + E.SCHEMA.encode() + b'",' + wire(parity_ev)[1:]
        reject('duplicate_json_key', duplicate_json, parity_frame, (0, 0, 0), 0)
        reject('outer_depth_cap', ('[' * 13 + '0' + ']' * 13).encode(),
               parity_frame, (0, 0, 0), 0)
        reject('malformed_utf8', b'\xff', parity_frame, (0, 0, 0), 0)

        # Independently supplied metadata distinguishes Boolean true from integer one.
        typed = frame(3, parity_frame.difference, scope='parity', metadata='{"reference":true}')
        forged = copy.deepcopy(base)
        forged['current_record'] = typed.record()
        reject('independent_exact_frame_type_binding', forged, parity_frame, (0, 0, 0), 0)

        # Vacuous bad=0 cannot stand in for feasible-incumbent checking.
        infeasible = frame(3, parity_frame.difference, hard=(K.bit(0),), scope='bad-incumbent')
        forged = copy.deepcopy(base)
        forged['current_record'] = infeasible.record()
        reject('infeasible_incumbent', forged, infeasible, (0, 0, 0), 0)
        empty = frame(3, K.lit(0), hard=(K.bit(0), K.neg(K.bit(0))), scope='empty-current')
        forged['current_record'] = empty.record()
        reject('empty_current_domain', forged, empty, (0, 0, 0), 0)

        # Tied optimal ranks all remain in the current sublevel.
        tied = frame(2, K.bit(1), soft=(K.Soft('prefer-not-p', K.neg(K.bit(0))),),
                     scope='tied-optima')
        tie_man = ordinary(2)
        tie_ev = E.export_dag(tie_man, tied, (0, 0), 1, tied.record())
        accept('all_tied_optima_valid_bound', receiver(2), tie_ev, tied, (0, 0), 1)
        try:
            E.export_dag(tie_man, tied, (0, 0), 0, tied.record())
        except E.NoBoundProof as failure:
            assert failure.counterexample == (0, 1)
            record('tied_optimum_exposes_false_bound', {'counterexample': failure.counterexample})
        else:
            raise AssertionError('A tied violating optimum disappeared.')

        # Withdrawal cannot promote an old guard-scoped claim to an unconditional fact.
        constrained = frame(1, K.bit(0), hard=(K.neg(K.bit(0)),), scope='before-withdrawal')
        withdrawal_man = ordinary(1)
        before_ev = E.export_dag(withdrawal_man, constrained, (0,), 0, constrained.record())
        withdrawal_rec = receiver(1)
        accept('before_constraint_withdrawal', withdrawal_rec, before_ev, constrained, (0,), 0)
        withdrawn = frame(1, K.bit(0), scope='after-withdrawal')
        stale = json.loads(wire(before_ev))
        stale['current_record'] = withdrawn.record()
        reject('stale_guard_after_withdrawal', stale, withdrawn, (0,), 0)
        valid_after = E.export_dag(withdrawal_man, withdrawn, (0,), 1,
                                   withdrawn.record(), base=before_ev.next_cursor())
        accept('withdrawal_rechecked_delta', withdrawal_rec.fork(), valid_after,
               withdrawn, (0,), 1)

        # The sole explicit receipt-depth boundary: 256 admissions, then rejection.
        capped = frame(1, K.lit(0), scope='receipt-cap')
        cap_man = ordinary(1)
        cap_rec = receiver(1)
        cap_cursor = None
        last_wire = None
        for index in range(R.MAX_RECEIPTS):
            cap_ev = E.export_dag(cap_man, capped, (0,), 0, capped.record(), base=cap_cursor)
            last_wire = wire(cap_ev)
            cap_rec.receive(last_wire, capped, capped.record(), (0,), 0,
                            request_id='cap-' + str(index))
            cap_cursor = cap_ev.next_cursor()
        cap_delta = E.export_dag(cap_man, capped, (0,), 0, capped.record(), base=cap_cursor)
        reject('receipt_cap_257th_attempt', wire(cap_delta), capped, (0,), 0, cap_rec)
        assert cap_rec.state_record()['receipts'] == 256

        # Explicit fresh allocation/epoch/order resets old wire authority.
        reset_receiver = receiver(3, (2, 1, 0), epoch='reset-epoch')
        reject('old_wire_after_explicit_reset', wire(parity_ev), parity_frame,
               (0, 0, 0), 0, reset_receiver)
    except Exception:
        error = traceback.format_exc()

    after = {path: {'bytes': (source_root / path).stat().st_size,
                    'sha256': sha((source_root / path).read_bytes())}
             for path in before}
    if after != before:
        error = (error or '') + '\nSource closure changed during probes.'
    results = {'schema': 'rp3bb.receiver-focused-check.v1',
               'stage': 'DEVELOPMENT', 'status': 'FAIL' if error else 'PASS',
               'prepared_case_scope': 'Finite functional grammar, full/delta, independent binding, admission/fork and malformed-wire probes; no scalar resource claim.',
               'python': sys.version, 'platform': platform.platform(),
               'utc': datetime.now(timezone.utc).isoformat(),
               'source_before': before, 'source_after': after,
               'source_unchanged': before == after,
               'case_count': len(cases), 'cases': cases, 'error': error,
               'principal_clock_credit_seconds': 0}
    raw = (json.dumps(results, indent=2) + '\n').encode()
    (args.out / 'results.json').write_bytes(raw)
    print(json.dumps({'status': results['status'], 'case_count': len(cases),
                      'results_sha256': sha(raw), 'error': error}, indent=2))
    if error:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
