"""F08 supplied max-min dual certificates and finite revision audits.

Research contributor: Codex (GPT-6), 2026-09-30.
No automatic normal-form, LP, vertex enumeration or proof search is provided.
Supplied dual points prove sound bounds; their completeness is a separate
mathematical obligation. Keep every meet parent when testing optimal replay.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction as F
from itertools import product
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as H
from v2.checks import f08_unit_characterization as U


@dataclass(frozen=True)
class DualPoint:
    rows: tuple[F, ...]
    leaves: tuple[F, ...]


def fold(kind: str, terms: tuple[K.Term, ...]) -> K.Term:
    if not terms or kind not in ('min', 'max'):
        raise H.AuditError('A nonempty finite min/max list is required.')
    op = K.minimum if kind == 'min' else K.maximum
    result = terms[0]
    for term in terms[1:]:
        result = op(result, term)
    return result


def min_projection(b: K.Builder, leaves: tuple[K.Term, ...], index: int) -> int:
    if not 0 <= index < len(leaves):
        raise H.AuditError('Missing minimum leaf.')
    if len(leaves) == 1:
        return b.constant(leaves[0], leaves[0])
    prefix = fold('min', leaves[:-1])
    if index == len(leaves)-1:
        return b.lattice('min_right', prefix, leaves[-1])
    head = b.lattice('min_left', prefix, leaves[-1])
    return b.trans(head, min_projection(b, leaves[:-1], index))


def clause_certificate(ctx: K.Context, case: str, leaves: tuple[K.Term, ...],
                       point: DualPoint) -> K.Proof:
    """Emit one supplied dual point directly in the original typed context."""
    ctx.validate()
    selected = [h for h in ctx.cases if h.name == case]
    if len(selected) != 1 or not leaves or not isinstance(point, DualPoint):
        raise H.AuditError('A live case, affine clause and dual point are required.')
    weights, alpha = tuple(map(H.exact, point.rows)), tuple(map(H.exact, point.leaves))
    if (len(weights) != len(selected[0].rows) or len(alpha) != len(leaves)
            or any(v < 0 for v in weights+alpha) or sum(alpha) != 1):
        raise H.AuditError('Dual dimensions, signs or leaf-weight normalization fail.')
    unit = K.infer(leaves[0], ctx.signature)
    for leaf in leaves:
        if K.infer(leaf, ctx.signature) != unit:
            raise H.AuditError('Clause leaves have different units.')
        K.affine(leaf, ctx.signature)
    paths = U.paths_to(ctx.signature, unit)
    b = K.Builder(ctx, case); zero = K.num(0, unit)
    clause = fold('min', leaves)
    left = b.constant(zero, zero); weighted = zero
    for index, weight in enumerate(alpha):
        if weight:
            left = b.add(left, b.scale(weight, min_projection(b, leaves, index)))
            weighted = K.add(weighted, K.scale(weight, leaves[index]))
    left = b.rewrite(left, clause, weighted)
    right = b.constant(zero, zero)
    for index, weight in enumerate(weights):
        if weight:
            row_unit = K.normalized_row(ctx, case, index)[2]
            if row_unit not in paths:
                raise H.AuditError('A nonzero row multiplier is inaccessible to this unit.')
            current = U._path_step(b, b.row(index), paths[row_unit])
            right = b.add(right, b.scale(weight, current))
    _, offset = K.affine(weighted, ctx.signature)
    right = b.add(right, b.constant(K.num(offset, unit), zero))
    # This exact native check enforces A^T lambda = sum alpha_j a_j.
    right = b.rewrite(right, weighted, zero)
    result = b.proof(b.trans(left, right))
    K.check(ctx, result)
    return T.prune(ctx, result)


def portfolio(ctx: K.Context, case: str, clauses: tuple[tuple[K.Term, ...], ...],
              points: tuple[tuple[DualPoint, ...], ...]) -> K.Proof:
    """Keep every supplied feasible dual point; no completeness claim here."""
    if not clauses or len(clauses) != len(points) or any(not p for p in points):
        raise H.AuditError('Every nonempty outer clause needs a nonempty portfolio.')
    b = K.Builder(ctx, case); clause_roots = []
    for leaves, candidates in zip(clauses, points):
        roots = [T._copy_into(b, clause_certificate(ctx, case, leaves, p)) for p in candidates]
        root = roots[0]
        for candidate in roots[1:]:
            root = b.meet(root, candidate)
        clause_roots.append(root)
    root = clause_roots[0]
    for candidate in clause_roots[1:]:
        root = b.max_common(root, candidate)
    out = T.prune(ctx, b.proof(root))
    K.check(ctx, out)
    return out


def family_context(parameters, *, revision='initial', priced=False):
    a, c, e = map(H.exact, parameters)
    source_unit = 'P' if priced else 'U'
    conversions = (K.Conversion('price', 'P', 'U', F(2)),) if priced else ()
    sig = K.Signature('F08-revision-family-v1', ('P', 'U') if priced else ('U',),
                      (('x', source_unit), ('y', source_unit), ('z', 'U')), conversions)
    x, y = K.src('x'), K.src('y')
    rows = (K.Row(x, K.num(a, source_unit)), K.Row(y, K.num(c, source_unit)),
            K.Row(K.add(x, y), K.num(e, source_unit)))
    r = min(a, c, e/2)
    ctx = K.Context(sig, 'fixed-policy', revision,
                    (K.Case('h', rows, (('x', r), ('y', r), ('z', F(0)))),))
    ctx.validate()
    return ctx


def family_data(ctx):
    priced = K.infer(K.src('x'), ctx.signature) == 'P'
    x, y, z = K.src('x'), K.src('y'), K.src('z')
    if priced:
        x, y = K.convert('price', x), K.convert('price', y)
    first = (x, y)
    second = (K.sub(K.sub(x, y), K.num(1)), K.sub(K.sub(y, x), K.num(1)))
    points = ((DualPoint((F(1), F(0), F(0)), (F(1), F(0))),
               DualPoint((F(0), F(1), F(0)), (F(0), F(1))),
               DualPoint((F(0), F(0), F(1, 2)), (F(1, 2), F(1, 2)))),
              (DualPoint((F(0), F(0), F(0)), (F(1, 2), F(1, 2))),))
    clauses = (first, second)
    new = K.add(z, fold('max', tuple(fold('min', q) for q in clauses)))
    return clauses, points, new, z


def family_proof(ctx):
    clauses, points, new, old = family_data(ctx)
    b = K.Builder(ctx); roots = []
    for case in ctx.cases:
        b.case = case.name
        root = T._copy_into(b, portfolio(ctx, case.name, clauses, points))
        roots.append(b.rewrite(root, new, old))
    out = b.proof(b.all_cases(roots))
    H.receive(ctx, out, H.request(ctx, None, new, old, K.check(ctx, out).budget))
    return out


def union_separator(ctx: K.Context, target: str):
    """Characteristic zero-set term of the target reduct and its native proof.

    Rows are converted in the original context. This does not project discarded
    rows or construct a characteristic term for their full-source implications.
    """
    paths = U.paths_to(ctx.signature, target); zero = K.num(0, target)
    violations, per_case = [], {}
    for case in ctx.cases:
        b = K.Builder(ctx, case.name); roots, terms = [], []
        for index, row in enumerate(case.rows):
            row_unit = K.infer(row.lhs, ctx.signature)
            if row_unit not in paths:
                continue
            raw, _ = U.path_term(ctx.signature, K.sub(row.lhs, row.rhs), paths[row_unit])
            current = U._path_step(b, b.row(index), paths[row_unit])
            _, offset = K.affine(raw, ctx.signature)
            current = b.add(current, b.constant(K.num(offset, target), zero))
            current = b.rewrite(current, raw, zero)
            current = b.max_common(current, b.constant(zero, zero))
            roots.append(current); terms.append(K.maximum(raw, zero))
        term = fold('max', tuple(terms)) if terms else zero
        current = roots[0] if roots else b.constant(zero, zero)
        for root in roots[1:]:
            current = b.max_common(current, root)
        per_case[case.name] = b.proof(current); violations.append(term)
    all_terms = tuple(violations); characteristic = fold('min', all_terms)
    b = K.Builder(ctx); roots = []
    for index, case in enumerate(ctx.cases):
        b.case = case.name
        projection = min_projection(b, all_terms, index)
        local = T._copy_into(b, per_case[case.name])
        roots.append(b.trans(projection, local))
    out = b.proof(b.all_cases(roots))
    H.receive(ctx, out, H.request(ctx, None, characteristic, zero, F(0), target))
    return characteristic, out


def gap_context(*, inaccessible=False):
    sig = K.Signature('F08-gap-v1', ('U', 'V'), (('x', 'U'),),
                      (K.Conversion('out', 'U', 'V', F(1)),))
    x = K.src('x'); term = K.convert('out', x) if inaccessible else x
    unit = 'V' if inaccessible else 'U'
    return K.Context(sig, 'fixed-policy', 'gap', (
        K.Case('left', (K.Row(term, K.num(-1, unit)),), (('x', F(-1)),)),
        K.Case('right', (K.Row(K.scale(-1, term), K.num(-1, unit)),), (('x', F(1)),))))


class F08RevisionPortfolioTests(unittest.TestCase):
    def test_all_eight_withdrawal_masks_from_the_complete_fixture(self):
        ctx = family_context((-2, 4, 6)); proof = family_proof(ctx)
        entries = (F(-2), F(4), F(3))
        for flags in product((False, True), repeat=3):
            alive = frozenset(('h', i) for i, keep in enumerate(flags) if keep)
            if not alive:
                with self.assertRaises(T.UnavailableProof):
                    T.restrict_rows(ctx, proof, alive)
                empty = replace(ctx, cases=(replace(ctx.cases[0], rows=()),))
                root = proof.steps[proof.root]
                for n in (F(0), F(10), F(1000)):
                    point = {'x': n, 'y': n, 'z': F(0)}
                    self.assertTrue(H.case_feasible(empty, 'h', point))
                    self.assertEqual(H.value(root.new, empty.signature, point)-H.value(root.old, empty.signature, point), n)
                continue
            current, out = T.restrict_rows(ctx, proof, alive)
            r = min(value for value, keep in zip(entries, flags) if keep)
            expected = max(r, F(-1)); root = K.check(current, out)
            self.assertEqual(root.budget, expected)
            witness = {'x': r, 'y': r, 'z': F(0)}
            self.assertTrue(H.case_feasible(current, 'h', witness))
            self.assertEqual(H.value(root.new, current.signature, witness)-H.value(root.old, current.signature, witness), expected)

    def test_finite_relaxation_threshold_matches_actual_withdrawal(self):
        ctx = family_context((-2, 4, 6)); proof = family_proof(ctx)
        withdrawn, exact = T.restrict_rows(ctx, proof, frozenset({('h', 1), ('h', 2)}))
        self.assertEqual(K.check(withdrawn, exact).budget, 3)
        for relaxation, expected in ((0, -1), (1, -1), (2, 0), (5, 3), (100, 3)):
            current = family_context((-2+relaxation, 4, 6), revision='relaxed')
            self.assertEqual(K.check(current, K.replay(ctx, current, proof)).budget, expected)

    def test_new_joint_row_is_not_recovered_by_optimal_old_marginals(self):
        x, y = K.src('x'), K.src('y')
        old = K.context(('x', 'y'), (K.Row(x, K.num(1)), K.Row(y, K.num(1))), {'x': 0, 'y': 0})
        b = K.Builder(old, 'h'); proof = b.proof(b.add(b.row(0), b.row(1)))
        new = replace(old, revision='new-joint-evidence', cases=(replace(old.cases[0],
            rows=old.cases[0].rows+(K.Row(K.add(x, y), K.num(0)),)),))
        replacements = {}
        for index in range(2):
            b = K.Builder(new, 'h'); replacements[('h', 'h', index)] = b.proof(b.row(index))
        retained = T.transport(old, new, proof, replacements, {'h': 'h'})
        self.assertEqual(K.check(new, retained).budget, 2)
        b = K.Builder(new, 'h'); better = b.proof(b.row(2))
        self.assertEqual(K.check(new, better).budget, 0)
        for point in ({'x': F(1), 'y': F(-1)}, {'x': F(-1), 'y': F(1)}):
            self.assertTrue(H.case_feasible(new, 'h', point))
        self.assertEqual(H.value(K.add(x, y), new.signature, {'x': F(0), 'y': F(0)}), 0)

    def test_uniform_optimal_replay_125_rhs_revisions_and_attaining_models(self):
        base = family_context((0, 10, 20)); proof = family_proof(base)
        self.assertEqual(sum(s.rule == 'meet_proofs' for s in proof.steps), 2)
        for parameters in product((F(-3), F(-1, 2), F(0), F(2), F(5)), repeat=3):
            ctx = family_context(parameters, revision='current')
            out = K.replay(base, ctx, proof); root = K.check(ctx, out)
            expected = max(min(parameters[0], parameters[1], parameters[2]/2), F(-1))
            self.assertEqual(root.budget, expected)
            H.receive(ctx, out, H.request(ctx, None, root.new, root.old, expected))
            for z in (F(-1000), F(1000)):
                witness = dict(ctx.cases[0].witness); witness['z'] = z
                self.assertTrue(H.case_feasible(ctx, 'h', witness))
                self.assertEqual(H.value(root.new, ctx.signature, witness)-H.value(root.old, ctx.signature, witness), expected)

    def test_direct_conversion_preserves_entire_portfolio(self):
        base = family_context((0, 10, 20), priced=True); proof = family_proof(base)
        ctx = family_context((10, 0, 20), revision='swapped', priced=True)
        root = K.check(ctx, K.replay(base, ctx, proof))
        self.assertEqual(root.budget, 0)
        self.assertTrue(any(s.rule == 'convert' for s in proof.steps))
        ctx = family_context((F(1, 3), 10, 20), revision='fraction', priced=True)
        self.assertEqual(K.check(ctx, K.replay(base, ctx, proof)).budget, F(2, 3))

    def test_current_transport_can_discard_future_optimal_alternative(self):
        base = family_context((0, 10, 20)); proof = family_proof(base)
        replacements = {}
        for index in range(3):
            b = K.Builder(base, 'h'); replacements[('h', 'h', index)] = b.proof(b.row(index))
        collapsed = T.transport(base, base, proof, replacements, {'h': 'h'})
        self.assertEqual(K.check(base, collapsed).budget, 0)
        self.assertFalse(any(s.rule == 'meet_proofs' for s in collapsed.steps))
        new = family_context((10, 0, 20), revision='swapped')
        self.assertEqual(K.check(new, K.replay(base, new, proof)).budget, 0)
        self.assertEqual(K.check(new, K.replay(base, new, collapsed)).budget, 10)

    def test_global_hidden_cases_keep_one_literal_pair(self):
        first = family_context((0, 10, 20)); other = family_context((-2, 4, 8))
        ctx = replace(first, cases=(replace(first.cases[0], name='one'), replace(other.cases[0], name='two')))
        proof = family_proof(ctx)
        self.assertEqual(K.check(ctx, proof).budget, 0)
        root = proof.steps[proof.root]
        self.assertEqual({(proof.steps[i].new, proof.steps[i].old) for i in root.parents}, {(root.new, root.old)})
        new = replace(ctx, revision='changed', cases=(replace(other.cases[0], name='one'), replace(other.cases[0], name='two')))
        self.assertEqual(K.check(new, K.replay(ctx, new, proof)).budget, -1)

    def test_bad_dual_weights_balance_and_normalization_are_rejected(self):
        ctx = family_context((0, 10, 20)); leaves = family_data(ctx)[0][0]
        for point in (DualPoint((F(-1), F(0), F(0)), (F(1), F(0))),
                      DualPoint((F(1), F(0), F(0)), (F(2), F(0))),
                      DualPoint((F(1), F(0), F(0)), (F(0), F(1))),
                      DualPoint((F(1),), (F(1), F(0)))):
            with self.subTest(point=point):
                with self.assertRaises((H.AuditError, K.ProofError)):
                    clause_certificate(ctx, 'h', leaves, point)

    def test_inaccessible_positive_multiplier_is_rejected(self):
        ctx = U.one_way_fixture()
        with self.assertRaises(H.AuditError):
            clause_certificate(ctx, 'h', (K.src('x'),), DualPoint((F(1),), (F(1),)))

    def test_duplicate_dual_point_is_sound_not_new_independent_evidence(self):
        ctx = family_context((0, 10, 20)); clauses, points, _, _ = family_data(ctx)
        duplicate = (points[0]+(points[0][0],), points[1])
        self.assertEqual(K.check(ctx, portfolio(ctx, 'h', clauses, duplicate)).budget, 0)

    def test_empty_supplied_portfolio_is_not_an_unboundedness_certificate(self):
        ctx = family_context((0, 10, 20)); clauses, points, _, _ = family_data(ctx)
        with self.assertRaises(H.AuditError):
            portfolio(ctx, 'h', clauses, ((), points[1]))

    def test_changed_row_direction_and_stale_context_fail(self):
        ctx = family_context((0, 10, 20)); proof = family_proof(ctx)
        new = family_context((1, 10, 20), revision='new')
        with self.assertRaises(K.ProofError):
            K.check(new, proof)
        row = K.Row(K.scale(2, K.src('x')), K.num(1))
        changed = replace(new, cases=(replace(new.cases[0], rows=(row,)+new.cases[0].rows[1:],
                                              witness=(('x', F(0)), ('y', F(0)), ('z', F(0)))),))
        with self.assertRaises(K.ProofError):
            K.replay(ctx, changed, proof)

    def test_mutated_budget_is_rejected(self):
        ctx = family_context((0, 10, 20)); proof = family_proof(ctx); root = proof.root
        steps = list(proof.steps); steps[root] = replace(steps[root], budget=F(-1))
        with self.assertRaises(K.ProofError):
            K.check(ctx, K.Proof(tuple(steps), root))


class F08SourceInformationTests(unittest.TestCase):
    def test_gap_has_native_zero_separator_and_same_pair_across_cases(self):
        ctx = gap_context(); term, proof = union_separator(ctx, 'U')
        self.assertEqual(K.check(ctx, proof).budget, 0)
        for x in map(F, (-10, -1, 0, 1, 10)):
            value = H.value(term, ctx.signature, {'x': x})
            self.assertEqual(value == 0, x <= -1 or x >= 1)
        self.assertEqual(H.value(term, ctx.signature, {'x': F(0)}), 1)

    def test_foreign_rows_do_not_appear_in_native_characteristic_term(self):
        ctx = gap_context(inaccessible=True)
        term, proof = union_separator(ctx, 'U')
        self.assertEqual(T.used_rows(ctx, proof), frozenset())
        for x in map(F, (-10, -1, 0, 1, 10)):
            self.assertEqual(H.value(term, ctx.signature, {'x': x}), 0)
        full = K.minimum(K.maximum(K.add(K.src('x'), K.num(1)), K.num(0)),
                         K.maximum(K.sub(K.num(1), K.src('x')), K.num(0)))
        self.assertEqual(H.value(full, ctx.signature, {'x': F(0)}), 1)
        self.assertTrue(U.unit_reduct(ctx, 'U').feasible('left', {'x': F(0)}))
        self.assertFalse(ctx.feasible('left', {'x': F(0)}))

    def test_empty_row_case_makes_union_whole_space(self):
        ctx = gap_context(); ctx = replace(ctx, cases=ctx.cases+(K.Case('all', (), (('x', F(0)),)),))
        term, proof = union_separator(ctx, 'U')
        self.assertEqual(K.check(ctx, proof).budget, 0)
        for x in map(F, (-100, 0, 100)):
            self.assertEqual(H.value(term, ctx.signature, {'x': x}), 0)

    def test_converted_separator_keeps_correlated_coordinates(self):
        ctx = U.one_way_fixture(3); term, proof = union_separator(ctx, 'U')
        self.assertEqual({i for _, i in T.used_rows(ctx, proof)}, {0, 1})
        for x in map(F, (-3, -1, 0, 3, 4)):
            self.assertEqual(H.value(term, ctx.signature, {'x': x}) == 0, x <= -1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
