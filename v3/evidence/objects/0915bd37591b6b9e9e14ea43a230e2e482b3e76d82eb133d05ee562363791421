#!/usr/bin/env python3
"""One fixed inherited-input versus evidence-fragment scope witness.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT.
No common-service tariff or policy run. No cap or source is modified.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import resource
import signal
import sys
import traceback

sys.dont_write_bytecode = True
RELATIVE_REVIEW = Path('v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/rational_fragment_v1')


class DiagnosticBudgetExceeded(BaseException):
    pass


def cpu_timeout(signum, frame):
    raise DiagnosticBudgetExceeded('Prospective 30-second process CPU ceiling reached.')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, value):
    raw = (json.dumps(value, sort_keys=True, indent=2) + '\n').encode('ascii')
    with path.open('xb') as handle:
        handle.write(raw)
    return {'file': path.name, 'bytes': len(raw), 'sha256': digest(raw)}


def source_manifest(source, names):
    return {name: {'bytes': len(raw), 'sha256': digest(raw)}
            for name in sorted(names)
            for raw in [(source / name).read_bytes()]}


def independent_tree(expression):
    """Syntax counts, flat literal order and exact subtree denominator products."""
    if expression[0] == 'lit':
        assert len(expression) == 2 and expression[1].startswith('-1/')
        q = int(expression[1][3:])
        return 1, 0, [q], q, [q.bit_length()]
    assert expression[0] == 'add' and len(expression) == 3
    left, right = independent_tree(expression[1]), independent_tree(expression[2])
    assert len(left[2]) == len(right[2])
    product = left[3] * right[3]
    return (1 + left[0] + right[0], 1 + max(left[1], right[1]),
            left[2] + right[2], product,
            left[4] + right[4] + [product.bit_length()])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    source = args.source_root.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    wanted = json.loads(args.manifest.read_text())
    before = source_manifest(source, wanted)
    assert before == wanted
    fixture = json.loads((source / RELATIVE_REVIEW / 'fixture.json').read_text())
    budget = json.loads((source / RELATIVE_REVIEW / 'budget.json').read_text())
    assert budget['cpu_soft_limit_seconds'] == 30 and budget['cpu_hard_limit_seconds'] == 31
    signal.signal(signal.SIGXCPU, cpu_timeout)
    resource.setrlimit(resource.RLIMIT_CPU, (30, 31))
    groups, artifacts = [], []
    state = {'status': 'RUNNING', 'error': None}
    try:
        spec = importlib.util.spec_from_file_location(
            '_rp3bb_rational_fragment_producer', source / 'v3/checks/05_add_evidence.py')
        if spec is None or spec.loader is None:
            raise ImportError('Missing captured producer.')
        E = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = E
        spec.loader.exec_module(E)
        O, M, K = E.A, E.M, E.K
        C = E.receiver_module()
        assert C.MAX_TERMINAL_BITS == E.MAX_TERMINAL_BITS == 4096
        assert K.MAX_NODES == 1024 and K.MAX_DEPTH == 32
        expected_source = E.make_source_record(E.DEFAULT_SOURCE_PATHS, repo_root=source)
        artifacts.append(write_json(args.out / 'worker_source_record.json', json.loads(expected_source)))

        assert fixture['nbits'] == 1 and fixture['hard'] == fixture['soft'] == []
        assert fixture['witness'] == [0] and fixture['bound'] == [0, 1]
        expression = fixture['losses'][0][1]
        nodes, depth, denominators, product, subtree_bits = independent_tree(expression)
        assert nodes == 127 and depth == 6 and len(denominators) == 64
        prime_rows = fixture['prime_powers']
        assert denominators == [int(row['denominator']) for row in prime_rows]
        primes = [row['prime'] for row in prime_rows]
        exact_first_primes = [n for n in range(2, 312)
                              if all(n % d != 0 for d in range(2, math.isqrt(n) + 1))]
        assert primes == exact_first_primes and len(primes) == 64 and primes[-1] == 311
        for row, q in zip(prime_rows, denominators):
            assert row['numerator'] == '-1'
            p, exponent = row['prime'], row['exponent']
            assert q == p**exponent and q <= 2**127 < q*p
            assert q.bit_length() <= 128

        def inherited_expr(value):
            if value[0] == 'lit':
                return K.lit(value[1])
            return K.add(inherited_expr(value[1]), inherited_expr(value[2]))

        difference = inherited_expr(expression)
        request = K.Request(1, (), (), (('difference', difference),),
                            fixture['scope'], json.dumps(fixture['metadata'], sort_keys=True))
        frame = M.Frame(request, 'difference', fixture['unit'])
        record = frame.record()
        frame.__post_init__()
        assert K.validate(difference, 1) == 'number' and request.tiers == 1
        assert M._point((0,), 1) is None
        groups.append({'name': 'inherited_input_valid', 'status': 'PASS',
                       'expression_nodes': nodes, 'root_zero_depth': depth,
                       'levels': depth + 1, 'literal_count': 64,
                       'input_component_bits_max': max(q.bit_length() for q in denominators),
                       'nbits': 1, 'rank_tiers': request.tiers,
                       'nonempty_current_sublevel': [[0], [1]],
                       'all_domain_points_are_tied_minimizers': True,
                       'current_record_bytes': len(record.encode('ascii'))})
        artifacts.append(write_json(args.out / 'current_frame_record.json', json.loads(record)))

        # Independent exact arithmetic: no ADD, interval or portfolio calculator.
        assert product == math.prod(denominators)
        positive_numerator = sum(product // q for q in denominators)
        assert all(product % q == 0 for q in denominators)
        residues = [positive_numerator % p for p in primes]
        assert all(residues) and math.gcd(positive_numerator, product) == 1
        assert 0 < positive_numerator < product
        numerator_bits = positive_numerator.bit_length()
        denominator_bits = product.bit_length()
        proper_subtree_bits = max(subtree_bits[:-1])
        assert 4096 < denominator_bits <= 16384
        assert numerator_bits < denominator_bits and proper_subtree_bits <= 4096
        exact_value = F(-positive_numerator, product)
        independent = {
            'method': 'Pairwise-coprime integer product and exact numerator sum; no deployed solver calculator.',
            'numerator': str(-positive_numerator), 'denominator': str(product),
            'numerator_bits': numerator_bits, 'denominator_bits': denominator_bits,
            'proper_subtree_denominator_bits_max': proper_subtree_bits,
            'prime_residues_of_positive_numerator': residues,
            'gcd': math.gcd(positive_numerator, product),
            'strictly_below_bound_zero': exact_value < 0,
            'constant_on_every_boolean_point': True,
            'whole_sublevel_including_both_tied_minimizers': [[0], [1]],
        }
        artifacts.append(write_json(args.out / 'independent_exact_bound.json', independent))
        groups.append({'name': 'independent_exact_bound', 'status': 'PASS',
                       'numerator_bits': numerator_bits, 'denominator_bits': denominator_bits,
                       'proper_subtree_denominator_bits_max': proper_subtree_bits,
                       'gcd': 1, 'strictly_below_zero': True})

        old_work = {}
        old = O.Manager(1, (0,))
        old_report = old.query(frame, (0,), record, old_work)
        assert old_report['status'] == 'EXACT_CURRENT_SUBLEVEL_RANGE'
        assert F(old_report['lower']) == F(old_report['upper']) == exact_value
        assert old_report['incumbent_rank'] == '0'
        assert old_work['max_rational_component_bits'] == denominator_bits
        assert old_work['max_rational_component_bits'] <= 16384
        artifacts.append(write_json(args.out / 'old_add_report.json', old_report))
        groups.append({'name': 'old_add_construction', 'status': 'PASS',
                       'report_status': old_report['status'], 'work': dict(old_work),
                       'storage': old_report['storage'],
                       'exact_range_matches_independent_calculation': True})

        epoch = 'rp3bb-rational-fragment-v1'
        new_work = {}
        new = E.RecordingManager(1, (0,), source_record=expected_source,
                                 epoch=epoch, work=new_work)
        try:
            E.export_dag(new, frame, (0,), F(0), record, work=new_work)
        except E.EvidenceLimit as error:
            export_rejection = {'type': type(error).__name__, 'message': str(error)}
        else:
            raise AssertionError('Expected unchanged new-producer fragment rejection.')
        assert 'rational component cap' in export_rejection['message']
        assert new_work['max_requested_terminal_component_bits'] == denominator_bits
        assert new_work['max_wire_rational_component_bits'] <= 4096
        partial = new.state_record()
        artifacts.append(write_json(args.out / 'new_producer_partial_state.json', partial))
        artifacts.append(write_json(args.out / 'new_producer_rejection.json', {
            'rejection': export_rejection, 'work': new_work,
            'counts': {'nodes': len(new.nodes), 'applies': len(new.apply_log),
                       'expressions': len(new.expression_log)},
            'no_wire_emitted': True, 'not_a_false_mathematical_bound': True,
        }))
        groups.append({'name': 'new_producer_fragment_rejection', 'status': 'PASS',
                       'expected_rejection': export_rejection, 'work': dict(new_work),
                       'no_wire_emitted': True})

        # A diagnostic attempted wire, not a replacement producer implementation.
        # Old Manager's dictionaries are insertion-ordered actual postorder facts.
        completion_work = {}
        roots = old_report['roots']
        zero = old.terminal(F(0), completion_work)
        bad = old.apply('and', roots['guard'],
                        old.apply('gt', roots['difference'], zero, completion_work),
                        completion_work)
        assert old.nodes[bad] == ('terminal', F(0))
        packet_nodes = []
        for node in old.nodes:
            if node[0] == 'terminal':
                packet_nodes.append(['T', node[1].numerator, node[1].denominator])
            else:
                packet_nodes.append(['N', *node[1:]])
        wire_record = {'schema': C.SCHEMA, 'mode': 'full', 'source_record': expected_source,
                       'epoch': epoch, 'bits': 1, 'order': [0],
                       'base': {'nodes': 0, 'applies': 0, 'expressions': 0},
                       'nodes': packet_nodes,
                       'applies': [[*key, out] for key, out in old.operations.items()],
                       'expressions': [[M._key(expr), root] for expr, root in old.expressions.items()],
                       'current_record': record, 'witness': [0], 'bound': [0, 1],
                       'roots': dict(roots, bad=bad)}
        raw_wire = json.dumps(wire_record, ensure_ascii=True, sort_keys=True,
                              separators=(',', ':'), allow_nan=False).encode('ascii')
        assert len(raw_wire) < C.MAX_WIRE_BYTES
        with (args.out / 'attempted_out_of_fragment_packet.json').open('xb') as handle:
            handle.write(raw_wire)
        artifacts.append({'file': 'attempted_out_of_fragment_packet.json',
                          'bytes': len(raw_wire), 'sha256': digest(raw_wire)})
        receiver_work = {}
        receiver = C.Receiver(expected_source, epoch, 1, (0,))
        request_id = 'oversized-rational-scope-check-1'
        try:
            receiver.receive(raw_wire, frame, record, (0,), F(0),
                             work=receiver_work, request_id=request_id)
        except C.Rejected as error:
            receiver_rejection = {'type': type(error).__name__, 'message': str(error)}
        else:
            raise AssertionError('Expected unchanged receiving wire-cap rejection.')
        assert receiver_rejection['message'] in (
            'JSON integer syntax or digit cap.', 'Terminal: rational component cap exceeded.')
        assert receiver.state_counts() == {'nodes': 0, 'applies': 0, 'expressions': 0}
        assert receiver.current_receipt(request_id) is None
        artifacts.append(write_json(args.out / 'receiver_rejection.json', {
            'rejection': receiver_rejection, 'work': receiver_work,
            'state_counts': receiver.state_counts(), 'current_receipt': None,
            'state': receiver.state_record(),
            'diagnostic_packet_not_issued_by_new_producer': True,
            'old_manager_bad_set_completion_work': completion_work,
        }))
        groups.append({'name': 'receiver_wire_fragment_rejection', 'status': 'PASS',
                       'expected_rejection': receiver_rejection,
                       'attempted_packet_bytes': len(raw_wire), 'work': receiver_work,
                       'admitted_nodes': 0, 'current_receipt': None})
        state['status'] = 'PASS'
    except BaseException as error:
        state['status'] = 'UNEXPECTED_FAILURE_PRESERVED'
        state['error'] = {'type': type(error).__name__, 'message': str(error),
                          'traceback': traceback.format_exc()}
    after = source_manifest(source, wanted)
    if after != before:
        state['status'] = 'UNEXPECTED_SOURCE_CHANGE'
    result = {'schema': 'rp3bb.rational-fragment-scope-result.v1',
              'stage': 'DEVELOPMENT', **state,
              'groups': groups, 'groups_passed': sum(g['status'] == 'PASS' for g in groups),
              'artifacts': artifacts, 'budget': budget, 'python': sys.version,
              'diagnostic_sha256': digest(Path(__file__).read_bytes()),
              'source_before': before, 'source_after': after,
              'sources_unchanged': before == after,
              'ordinary_cost_superiority_claimed': False,
              'all_inherited_inputs_bridge_claimed': False,
              'physical_cost_or_paid_tariff_claimed': False,
              'common_service_deliveries': 0, 'policy_runs': 0,
              'principal_clock_credit_seconds': 0}
    receipt = write_json(args.out / 'results.json', result)
    bit_record = next((g for g in groups if g['name'] == 'independent_exact_bound'), None)
    print(json.dumps({'status': result['status'], 'groups_passed': result['groups_passed'],
                      'bits': bit_record, 'results': receipt}, indent=2))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
