"""Gate B finite hostile fixtures, not an integrated reasoner or validity oracle.

Codex (GPT-6), 2026-09-30. The analytic arguments are in B_1_reconstruction.md.
Expected bounds/witnesses below use direct rational calculations, separately
from the native proof constructors and receiver. Existing kernel code is reused
unchanged; finite checks do not prove the general characterization theorem.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from fractions import Fraction as F
import json
from pathlib import Path
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as A


def capped_tent(cap: F, revision: str = 'initial'):
    """Two explicit proofs of min(x,2-x): a row bound and a source-free bound."""
    x, zero = K.src('x'), K.num(0)
    ctx = K.context(('x',), (K.Row(zero, x), K.Row(x, K.num(cap))),
                    {'x': 0}, scope='GateB-capped-tent-v1', revision=revision)
    query = K.minimum(x, K.sub(K.num(2), x))
    b = K.Builder(ctx, 'h')
    left = b.lattice('min_left', x, K.sub(K.num(2), x))
    row = b.rewrite(b.row(1), x, zero)
    by_row = b.trans(left, row)
    right = b.lattice('min_right', x, K.sub(K.num(2), x))
    balanced = b.scale(F(1, 2), b.add(left, right))
    balanced = b.rewrite(balanced, query, K.num(1))
    balanced = b.trans(balanced, b.constant(K.num(1), zero))
    both = b.meet(by_row, balanced)
    return ctx, b.proof(both), query, by_row, balanced


def receive(ctx, proof, new, old, budget, case='h', unit='U'):
    return A.receive(ctx, proof, A.request(ctx, case, new, old, budget, unit))


def separated_cases():
    x, zero = K.src('x'), K.num(0)
    sig = K.Signature('GateB-separate-cases', ('U',), (('x', 'U'),))
    cases = tuple(K.Case(name, (K.Row(x, K.num(v)), K.Row(K.num(v), x)),
                         (('x', F(v)),)) for name, v in (('left', -1), ('right', 1)))
    ctx = K.Context(sig, 'same-visible-observation', 'initial', cases)
    b = K.Builder(ctx)
    roots = []
    for case in cases:
        b.case = case.name
        roots.append(b.rewrite(b.row(0), x, zero))
    b.all_cases(roots)
    return ctx, b.proof(), tuple(roots)


def report():
    caps = tuple(F(n, 4) for n in range(13))
    points = 0
    received = []
    for cap in caps:
        ctx, proof, query, _, _ = capped_tent(cap, f'cap-{cap}')
        expected = min(cap, F(1))
        root = receive(ctx, proof, query, K.num(0), expected)
        if root.budget != expected:
            raise AssertionError('The received bound differs from the independent optimum.')
        witness = min(cap, F(1))
        if not (0 <= witness <= cap and min(witness, 2-witness) == expected):
            raise AssertionError('The independent attaining witness failed.')
        for j in range(17):
            x = cap * F(j, 16)
            if min(x, 2-x) > expected:
                raise AssertionError('Direct rational point contradicts the bound.')
            points += 1
        received.append({'cap': str(cap), 'bound': str(root.budget),
                         'attaining_x': str(witness)})
    # Declare requested pairs before receiving producer output. Copying them
    # from a returned root would only test trace validity, not use correctness.
    def intended(r, new):
        h = K.add(K.scale(1-r, K.src('p')), K.scale(r, K.src('s')))
        loss = K.add(K.convert('failure_cost', h),
                     K.add(K.num(r/4, 'L'), K.src('z')))
        tail = K.add(K.src('w'), K.src('e')) if new else K.src('w')
        return K.add(K.convert('proxy_value', loss), tail)

    examples = {}
    for name, factory, expected, new, old, case, unit in (
        ('shared_composition', K.composition_example, F(-1, 2),
         K.add(K.src('N1'), K.src('N2')), K.add(K.src('O1'), K.src('O2')), 'h', 'U'),
        ('quadratic_enclosure', K.quadratic_example, F(-3, 16),
         K.add(K.src('q'), K.src('z')), K.add(K.src('theta'), K.src('z')), None, 'U'),
        ('versioned_self_assessment', K.reflection_example, F(-1, 32),
         intended(F(3, 4), True), intended(F(1, 2), False), 'h', 'J'),
    ):
        data = factory()
        ctx, proof = data[:2]
        root = receive(ctx, proof, new, old, expected, case, unit)
        examples[name] = {'received_budget': str(root.budget),
                          'steps': len(proof.steps), 'cases': len(ctx.cases)}
    return {'scope': 'finite gate fixtures; not a general solver or theorem proof',
            'native_kernel_changed': False, 'portfolio_family': received,
            'direct_points': points, 'composite_examples': examples}


class GateBReviewTests(unittest.TestCase):
    def test_family_has_exact_attaining_models_and_current_received_proofs(self):
        result = report()
        self.assertEqual(len(result['portfolio_family']), 13)
        self.assertEqual(result['direct_points'], 221)

    def test_retaining_only_current_best_loses_future_optimum(self):
        old, proof, query, by_row, _ = capped_tent(F(1, 2))
        new, _, _, _, _ = capped_tent(F(2), 'relaxed')
        selected = T.prune(old, replace(proof, root=by_row))
        full_replay = K.replay(old, new, proof)
        selected_replay = K.replay(old, new, selected)
        self.assertEqual(receive(new, full_replay, query, K.num(0), 1).budget, 1)
        self.assertEqual(K.check(new, selected_replay).budget, 2)
        with self.assertRaises(A.AuditError):
            receive(new, selected_replay, query, K.num(0), 1)
        self.assertEqual(min(F(1), 2-F(1)), 1)

    def test_withdrawal_recovers_the_retained_source_free_alternative(self):
        old, proof, query, by_row, _ = capped_tent(F(1, 2))
        alive = frozenset({('h', 0)})
        new, kept = T.restrict_rows(old, proof, alive, 'upper-row-withdrawn')
        self.assertEqual(receive(new, kept, query, K.num(0), 1, None).budget, 1)
        with self.assertRaises(T.UnavailableProof):
            T.restrict_rows(old, T.prune(old, replace(proof, root=by_row)), alive)

    def test_old_trace_is_not_current_evidence_even_when_bound_would_hold(self):
        old, proof, query, _, _ = capped_tent(F(1, 2))
        new, _, _, _, _ = capped_tent(F(1, 4), 'strengthened')
        with self.assertRaises(K.ProofError):
            receive(new, proof, query, K.num(0), F(1, 2))

    def test_replayed_trace_does_not_validate_an_old_request(self):
        old, proof, query, _, _ = capped_tent(F(1, 2))
        new, _, _, _, _ = capped_tent(F(1, 4), 'strengthened')
        request = A.request(old, 'h', query, K.num(0), F(1, 2))
        with self.assertRaises(A.AuditError):
            A.receive(new, K.replay(old, new, proof), request)

    def test_valid_same_difference_is_not_the_literal_requested_pair(self):
        ctx, proof, query, _, _ = capped_tent(F(1, 2))
        b = K.Builder(ctx, 'h')
        b.steps = list(proof.steps)
        b.rewrite(proof.root, K.add(query, K.num(3)), K.num(3))
        K.check(ctx, b.proof())
        with self.assertRaises(A.AuditError):
            receive(ctx, b.proof(), query, K.num(0), F(1, 2))

    def test_invalid_unused_instruction_is_rejected(self):
        ctx, proof, _, _, _ = capped_tent(F(1, 2))
        bad = replace(proof.steps[-1], budget=F(99))
        with self.assertRaises(K.ProofError):
            K.check(ctx, K.Proof(proof.steps+(bad,), proof.root))

    def test_false_negative_constant_bound_is_rejected(self):
        ctx, _, _, _, _ = capped_tent(F(0))
        b = K.Builder(ctx, 'h')
        b.emit('constant', (), K.num(0), K.num(0), -1)
        with self.assertRaises(K.ProofError):
            K.check(ctx, b.proof())

    def test_bad_feasibility_witness_cannot_admit_the_context(self):
        ctx, proof, _, _, _ = capped_tent(F(1, 2))
        bad = replace(ctx, cases=(replace(ctx.cases[0], witness=(('x', F(2)),)),))
        with self.assertRaises(K.SemanticError):
            K.check(bad, proof)

    def test_separate_case_proofs_need_no_common_case_point(self):
        ctx, proof, _ = separated_cases()
        self.assertEqual(receive(ctx, proof, K.src('x'), K.num(0), 1, None).budget, 1)
        self.assertFalse(ctx.feasible('left', {'x': F(1)}))
        self.assertTrue(ctx.feasible('right', {'x': F(1)}))

    def test_minimum_case_budget_is_not_a_union_bound(self):
        ctx, proof, _ = separated_cases()
        changed = proof.steps[:-1]+(replace(proof.steps[-1], budget=F(-1)),)
        with self.assertRaises(K.ProofError):
            K.check(ctx, replace(proof, steps=changed))
        self.assertGreater(F(1), F(-1))

    def test_local_proof_cannot_receive_a_global_request(self):
        ctx, proof, roots = separated_cases()
        with self.assertRaises(A.AuditError):
            receive(ctx, replace(proof, root=roots[0]), K.src('x'), K.num(0), 1, None)

    def test_omitted_case_is_not_proof_coverage(self):
        ctx, proof, roots = separated_cases()
        bad = replace(proof.steps[-1], parents=(roots[0],), budget=F(-1))
        with self.assertRaises(K.ProofError):
            K.check(ctx, replace(proof, steps=proof.steps[:-1]+(bad,)))

    def test_lexical_shadowing_uses_the_old_environment_for_rhs(self):
        x = K.src('x')
        term = K.let('a', x, K.add(K.let('a', K.add(K.loc('a'), K.num(1)),
                                        K.loc('a')), K.loc('a')))
        ctx = K.context(('x',), (), {'x': 0}, scope='GateB-lexical')
        b = K.Builder(ctx, 'h')
        b.constant(term, K.add(K.scale(2, x), K.num(1)))
        self.assertEqual(K.check(ctx, b.proof()).budget, 0)
        for value in (F(-100), F(0), F(2, 3)):
            self.assertEqual(K.evaluate(term, ctx.signature, {'x': value}), 2*value+1)

    def test_zero_coefficient_does_not_hide_an_undeclared_source(self):
        ctx = K.context(('x',), (), {'x': 0}, scope='GateB-type-first')
        b = K.Builder(ctx, 'h')
        with self.assertRaises(K.SemanticError):
            b.constant(K.scale(0, K.src('undeclared')), K.num(0))

    def test_reduct_countermodel_is_not_a_full_source_countermodel(self):
        x = K.src('x')
        sig = K.Signature('GateB-directed', ('U', 'V'), (('x', 'U'),),
                          (K.Conversion('uv', 'U', 'V', F(1)),))
        row = K.Row(K.convert('uv', x), K.num(-1, 'V'))
        ctx = K.Context(sig, 'fixed', 'v1', (K.Case('h', (row,), (('x', F(-1)),)),))
        ctx.validate()
        reduct = replace(ctx, cases=(replace(ctx.cases[0], rows=()),))
        self.assertTrue(reduct.feasible('h', {'x': F(0)}))
        self.assertFalse(ctx.feasible('h', {'x': F(0)}))
        self.assertGreater(F(0), F(-1))

    def test_return_path_works_without_reciprocal_conversion_factors(self):
        x = K.src('x')
        sig = K.Signature('GateB-return-path', ('U', 'V'), (('x', 'U'),),
                          (K.Conversion('uv', 'U', 'V', F(3)),
                           K.Conversion('vu', 'V', 'U', F(2))))
        ctx = K.Context(sig, 'fixed', 'v1',
                        (K.Case('h', (K.Row(K.convert('uv', x), K.num(-3, 'V')),),
                                (('x', F(-1)),)),))
        b = K.Builder(ctx, 'h')
        step = b.scale(F(1, 6), b.conversion('vu', b.row(0)))
        b.rewrite(step, x, K.num(0))
        self.assertEqual(receive(ctx, b.proof(), x, K.num(0), -1).budget, -1)

    def test_reflective_revision_leaves_actual_improvement_unresolved(self):
        old, proof, roots = K.reflection_example()
        new, _, _ = K.reflection_example(e_bound=F(3, 32), revision='relaxed-error')
        updated = K.replay(old, new, proof)
        root = updated.steps[roots['intended']]
        self.assertEqual(root.budget, F(1, 32))
        with self.assertRaises(A.AuditError):
            receive(new, updated, root.new, root.old, 0, 'h', 'J')
        for discrepancy, sign in ((F(-1, 32), -1), (F(3, 32), 1)):
            point = {'p': F(1, 2), 's': F(0), 'e': discrepancy, 'z': F(0), 'w': F(0)}
            self.assertTrue(new.feasible('h', point))
            direct_change = -F(1, 16)+discrepancy
            self.assertGreater(sign*direct_change, 0)
            actual = K.evaluate(root.new, new.signature, point)-K.evaluate(root.old, new.signature, point)
            self.assertEqual(actual, direct_change)

    def test_controller_scope_change_is_not_rhs_only_replay(self):
        ctx, proof, _ = K.reflection_example()
        changed = replace(ctx, signature=replace(ctx.signature, scope='SELF-MIX-reversed'))
        with self.assertRaises(K.ProofError):
            K.replay(ctx, changed, proof)
        # Independent law calculation: both reports valid, cost difference reverses.
        for s in (F(0), F(1, 8), F(1, 4)):
            p = s+F(1, 2)
            costs = []
            for r in (F(1, 2), F(3, 4)):
                hazard = r*p+(1-r)*s
                self.assertLessEqual(hazard, r)
                costs.append(hazard+(1-r)/4)
            self.assertEqual(costs[1]-costs[0], F(1, 16))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    text = json.dumps(report(), indent=2, sort_keys=True)+'\n'
    if args.json:
        args.json.write_text(text, encoding='utf-8')
    print(text, end='')


if __name__ == '__main__':
    main()
