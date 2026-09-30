"""F08 case-scope, source-map and quantitative-deduction regression fixtures.

Research contributor: Codex (GPT-6), 2026-09-30.
These supplied examples emit ordinary native proofs; they do not implement
the general image, normal-form, or least-penalty optimizers.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as H
from v2.checks import f08_unit_characterization as U


def extend_local(old: K.Context, new: K.Context, proof: K.Proof, case: str) -> K.Proof:
    """Extend a checked case-local trace while preserving its exact row context."""
    K.check(old, proof); new.validate()
    if old.signature != new.signature or old.observation != new.observation:
        raise H.AuditError('Local extension keeps signature and observation fixed.')
    before = [h for h in old.cases if h.name == case]
    after = [h for h in new.cases if h.name == case]
    if len(before) != 1 or len(after) != 1 or before[0].rows != after[0].rows:
        raise H.AuditError('Local extension needs the same named case and exact rows.')
    local = T.localize(old, proof, case)
    if any(s.case != case or s.rule == 'all_cases' for s in local.steps):
        raise H.AuditError('Localization did not remove global aggregation.')
    out = K.Proof(tuple(replace(s, context_id=K.fingerprint(new)) for s in local.steps), local.root)
    K.check(new, out)
    return out


def cap_context(cap=None, *, sources=(('x', 'U'),), revision='initial'):
    rows = () if cap is None else (K.Row(K.src('x'), K.num(H.exact(cap))),)
    witness = {key: F(0) for key, _ in sources}
    if cap is not None:
        witness['x'] = min(F(0), H.exact(cap))
    return replace(K.context(sources, rows, witness, scope='F08-transfer-v1'), revision=revision)


def hinge_deduction(ctx: K.Context, case='h'):
    """Row-free ReLU(x-1)<=ReLU(x), the least-gain-one U17 fixture."""
    b = K.Builder(ctx, case); x, zero = K.src('x'), K.num(0)
    left = K.sub(x, K.num(1))
    order = b.slack(1, b.constant(left, x))
    root = b.congruence('max', order, b.constant(zero, zero))
    proof = b.proof(root); K.check(ctx, proof)
    return proof


def hinge_cap(ctx: K.Context, epsilon: F):
    """ReLU(x)<=epsilon from the supplied x<=epsilon row, epsilon>=0."""
    epsilon = H.exact(epsilon)
    if epsilon < 0:
        raise H.AuditError('This cap fixture requires epsilon>=0.')
    b = K.Builder(ctx, 'h'); zero = K.num(0)
    row = b.rewrite(b.row(0), K.src('x'), zero)
    root = b.max_common(row, b.slack(epsilon, b.constant(zero, zero)))
    proof = b.proof(root); K.check(ctx, proof)
    return proof


def geometry_fixture(e, relaxation):
    """Supplied sharp certificate for x<=R, -x+e*y<=R, e>0, R>=0."""
    e, relaxation = H.exact(e), H.exact(relaxation)
    if e <= 0 or relaxation < 0:
        raise H.AuditError('Positive fixed matrix parameter and nonnegative relaxation required.')
    x, y = K.src('x'), K.src('y')
    rows = (K.Row(x, K.num(relaxation)),
            K.Row(K.add(K.scale(-1, x), K.scale(e, y)), K.num(relaxation)))
    ctx = K.context(('x', 'y'), rows, {'x': 0, 'y': 0}, scope='F08-geometry-v1')
    gain = 1+2/e
    proof = U.affine_certificate(ctx, 'h', K.add(x, y), K.num(0), gain*relaxation,
                                 (1+1/e, 1/e))
    point = {'x': relaxation, 'y': 2*relaxation/e}
    return ctx, proof, gain, point


class F08TransferAuditTests(unittest.TestCase):
    def test_geometry_gain_and_attainment_across_nine_exact_cases(self):
        for e in (F(2), F(1, 10), F(1, 100)):
            for relaxation in (F(0), F(1, 100), F(1)):
                ctx, proof, gain, point = geometry_fixture(e, relaxation)
                root = H.receive(ctx, proof, H.request(ctx, 'h', K.add(K.src('x'), K.src('y')),
                                                       K.num(0), gain*relaxation))
                self.assertTrue(H.case_feasible(ctx, 'h', point))
                self.assertEqual(H.value(root.new, ctx.signature, point), root.budget)
        _, proof, _, _ = geometry_fixture(F(1, 100), F(1, 100))
        self.assertEqual(proof.steps[proof.root].budget, F(201, 100))

    def test_zero_matrix_parameter_changes_the_query_to_unbounded(self):
        x, y = K.src('x'), K.src('y')
        ctx = K.context(('x', 'y'), (K.Row(x, K.num(0)), K.Row(K.scale(-1, x), K.num(0))),
                        {'x': 0, 'y': 0})
        for height in (F(0), F(100), F(10**9)):
            point = {'x': F(0), 'y': height}
            self.assertTrue(H.case_feasible(ctx, 'h', point))
            self.assertEqual(H.value(K.add(x, y), ctx.signature, point), height)
        with self.assertRaises(H.AuditError):
            geometry_fixture(0, 1)

    def test_weighted_report_gain_one_and_strict_transfer_boundary(self):
        from v2.checks import f08_warranted_report as W
        from v2.checks import f08_revision_portfolio as P
        original = W.rectangle_context(); violation, _ = P.union_separator(original, 'P')
        ctx = replace(original, revision='row-free-report', cases=(replace(original.cases[0], rows=()),))
        b = K.Builder(ctx, 'h'); zero = K.num(0, 'P')
        raw = tuple(K.sub(row.lhs, row.rhs) for row in original.cases[0].rows)
        hinges = tuple(K.maximum(t, zero) for t in raw)
        def inject(index):
            target = K.maximum(hinges[0], hinges[1])
            root = b.lattice('max_left' if index == 0 else 'max_right', hinges[0], hinges[1])
            for term in hinges[2:]:
                root = b.trans(root, b.lattice('max_left', target, term))
                target = K.maximum(target, term)
            return b.trans(b.lattice('max_left', raw[index], zero), root)
        r = F(3, 4); left, right = inject(0), inject(1)
        root = b.add(b.scale(1-r, left), b.scale(r, right))
        root = b.add(root, b.constant(K.num(F(-5, 16), 'P'), zero))
        query = K.sub(W.risk(r), K.num(r, 'P'))
        root = b.rewrite(root, query, violation)
        proof = b.proof(root)
        self.assertEqual(K.check(ctx, proof).budget, F(-5, 16))
        self.assertEqual(T.used_rows(ctx, proof), frozenset())
        for epsilon in (F(1, 100), F(5, 16), F(1)):
            point = {'p': 1+epsilon, 's': F(1, 4)+epsilon}
            self.assertEqual(H.value(violation, ctx.signature, point), epsilon)
            self.assertEqual(H.value(query, ctx.signature, point), F(-5, 16)+epsilon)
        self.assertLess(F(-5, 16)+F(1, 100), 0)
        self.assertEqual(F(-5, 16)+F(5, 16), 0)

    def test_single_case_global_proof_extends_only_as_local(self):
        old = cap_context(0); b = K.Builder(old, 'h')
        proof = b.proof(b.all_cases([b.row(0)]))
        other = K.Case('other', (K.Row(K.src('x'), K.num(9)),), (('x', F(9)),))
        new = replace(old, revision='extra-case', cases=old.cases+(other,))
        out = extend_local(old, new, proof, 'h')
        self.assertEqual(K.check(new, out).case, 'h')
        self.assertTrue(all(s.case == 'h' for s in out.steps))
        self.assertFalse(any(s.rule == 'all_cases' for s in out.steps))
        self.assertTrue(H.case_feasible(new, 'other', {'x': F(9)}))
        with self.assertRaises(H.AuditError):
            H.receive(new, out, H.request(new, None, K.src('x'), K.num(0), 0))

    def test_extension_rejects_changed_rows_meanings_and_case(self):
        old = cap_context(0); b = K.Builder(old, 'h'); proof = b.proof(b.row(0))
        for new in (cap_context(1), replace(old, observation='changed'),
                    replace(old, cases=(replace(old.cases[0], name='different'),))):
            with self.subTest(new=new.revision):
                with self.assertRaises(H.AuditError):
                    extend_local(old, new, proof, 'h')

    def test_extension_revalidates_stale_and_corrupt_input(self):
        old = cap_context(0); b = K.Builder(old, 'h'); proof = b.proof(b.row(0))
        corrupt = K.Proof((replace(proof.steps[0], budget=F(-1)),), 0)
        with self.assertRaises(K.ProofError):
            extend_local(old, old, corrupt, 'h')
        with self.assertRaises(K.ProofError):
            K.check(replace(old, revision='new'), proof)

    def test_local_extensions_aggregate_only_after_every_case_is_proved(self):
        old = cap_context(0); second = replace(old.cases[0], name='second')
        ctx = replace(old, cases=old.cases+(second,))
        global_builder = K.Builder(ctx); roots = []
        for case in ctx.cases:
            single = replace(ctx, cases=(case,)); b = K.Builder(single, case.name)
            row = b.rewrite(b.row(0), K.src('x'), K.num(0))
            roots.append(T._copy_into(global_builder, extend_local(single, ctx, b.proof(row), case.name)))
        proof = global_builder.proof(global_builder.all_cases(roots))
        self.assertEqual(H.receive(ctx, proof, H.request(ctx, None, K.src('x'), K.num(0), 0)).budget, 0)

    def test_deduction_has_no_source_rows_and_gain_one(self):
        ctx = cap_context(); proof = hinge_deduction(ctx)
        self.assertEqual(T.used_rows(ctx, proof), frozenset())
        self.assertEqual(K.check(ctx, proof).budget, 0)
        for x in map(F, (-10, 0, F(1, 2), 1, 2, 100)):
            root = K.check(ctx, proof)
            self.assertLessEqual(H.value(root.new, ctx.signature, {'x': x}),
                                 H.value(root.old, ctx.signature, {'x': x}))

    def test_smaller_gain_has_exact_rational_countermodel(self):
        for gain in (F(0), F(1, 2), F(99, 100), F(999999, 1000000)):
            x = 2/(1-gain)
            self.assertGreater(x-1, gain*x)
            self.assertLess((x-1)/x, 1)

    def test_approximate_transfer_is_sound_but_can_be_slack(self):
        ctx = cap_context(F(1, 2)); b = K.Builder(ctx, 'h')
        first = T._copy_into(b, hinge_deduction(ctx)); second = T._copy_into(b, hinge_cap(ctx, F(1, 2)))
        proof = b.proof(b.trans(first, second)); root = K.check(ctx, proof)
        self.assertEqual(root.budget, F(1, 2))
        H.receive(ctx, proof, H.request(ctx, 'h', root.new, K.num(0), F(1, 2)))
        direct = K.Builder(ctx, 'h')
        row = direct.add(direct.row(0), direct.constant(K.num(-1), K.num(0)))
        row = direct.rewrite(row, K.sub(K.src('x'), K.num(1)), K.num(0))
        sharp = direct.proof(direct.max_common(row, direct.constant(K.num(0), K.num(0))))
        self.assertEqual(K.check(ctx, sharp).budget, 0)
        with self.assertRaises(H.AuditError):
            H.receive(ctx, proof, H.request(ctx, 'h', root.new, K.num(0), 0))

    def test_row_free_deduction_substitutes_nonlinear_sources(self):
        old = cap_context(); new = cap_context(sources=(('z', 'U'), ('w', 'U')))
        expression = K.add(K.minimum(K.src('z'), K.src('w')), K.num(2))
        out = T.transport(old, new, hinge_deduction(old), {}, {'h': 'h'},
                          source_map={'x': expression})
        self.assertEqual(K.check(new, out).budget, 0)
        self.assertEqual(T.used_rows(new, out), frozenset())
        root = K.check(new, out)
        self.assertEqual(root.new, K.maximum(K.sub(expression, K.num(1)), K.num(0)))

    def test_onto_affine_substitution_retains_the_offset(self):
        old = cap_context(3); b = K.Builder(old, 'h'); proof = b.proof(b.row(0))
        new = cap_context(sources=(('z', 'U'), ('w', 'U')))
        new = replace(new, cases=(replace(new.cases[0], rows=(K.Row(K.src('z'), K.num(1)),)),))
        expression = K.add(K.src('z'), K.num(2))
        replacement = U.affine_certificate(new, 'h', expression, K.num(0), F(3), (F(1),))
        out = T.transport(old, new, proof, {('h', 'h', 0): replacement}, {'h': 'h'},
                          source_map={'x': expression})
        self.assertEqual(K.check(new, out).budget, 3)
        self.assertEqual(H.value(K.check(new, out).new, new.signature, {'z': F(1), 'w': F(100)}), 3)

    def test_injective_diagonal_adds_a_correlation(self):
        old = cap_context(sources=(('x', 'U'), ('y', 'U')))
        new = cap_context(sources=(('z', 'U'),)); zero = K.num(0)
        difference = K.sub(K.src('x'), K.src('y'))
        self.assertEqual(H.value(difference, old.signature, {'x': F(1), 'y': F(0)}), 1)
        b = K.Builder(new, 'h')
        proof = b.proof(b.constant(K.sub(K.src('z'), K.src('z')), zero))
        self.assertEqual(K.check(new, proof).budget, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
