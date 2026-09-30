"""Finite audits for F08's unit-directed completeness reconstruction.

Research contributor: Codex (GPT-6), 2026-09-30.
No general LP solver, validity decider, or automatic CPWA proof search is added.
Every emitted proof is checked by the unchanged F06 kernel and bound to its
actual request where supplied. Exact rational arithmetic; standard library.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f06_derived_cases as D
from v2.checks import f07_soundness as H


def paths_to(signature: K.Signature, target: str) -> dict[str, tuple[str, ...]]:
    """One finite conversion path from each ancestor unit to target."""
    signature.validate()
    if target not in signature.units:
        raise H.AuditError('Unknown target unit.')
    paths = {target: ()}
    frontier = [target]
    while frontier:
        endpoint = frontier.pop(0)
        for conversion in signature.conversions:
            if conversion.target == endpoint and conversion.source not in paths:
                paths[conversion.source] = (conversion.name,) + paths[endpoint]
                frontier.append(conversion.source)
    return paths


def path_term(signature: K.Signature, term: K.Term, path: tuple[str, ...]):
    """Return the typed converted term and the exact positive path factor."""
    K.infer(term, signature)
    factor = F(1)
    for name in path:
        conversion = signature.conversion(name)
        term = K.convert(name, term)
        K.infer(term, signature)
        factor *= K.rat(conversion.factor)
    return term, factor


def source_closed(signature: K.Signature, target: str) -> bool:
    """The fixed-signature condition UC, not an empirical source check."""
    ancestors = paths_to(signature, target)
    reachable_sources = [u for _, u in signature.sources if u in ancestors]
    return all(v in ancestors or all(u not in paths_to(signature, v) for u in reachable_sources)
               for v in signature.units)


def unit_reduct(ctx: K.Context, target: str) -> K.Context:
    ctx.validate()
    ancestors = paths_to(ctx.signature, target)
    cases = tuple(replace(h, rows=tuple(row for row in h.rows
                    if K.infer(row.lhs, ctx.signature) in ancestors)) for h in ctx.cases)
    out = replace(ctx, revision=ctx.revision + '/F08-reduct-' + target, cases=cases)
    out.validate()
    return out


def converted_context(ctx: K.Context, target: str):
    """Same models as the reduct, with every retained row explicitly in target.

    Returns row-origin indices for use by the separately checked grafting adapter.
    No source coordinate is identified, cloned, resampled, or silently retyped.
    """
    ctx.validate()
    paths = paths_to(ctx.signature, target)
    cases, origins = [], {}
    for case in ctx.cases:
        rows, indices = [], []
        for index, row in enumerate(case.rows):
            unit = K.infer(row.lhs, ctx.signature)
            if unit not in paths:
                continue
            lhs, _ = path_term(ctx.signature, row.lhs, paths[unit])
            rhs, _ = path_term(ctx.signature, row.rhs, paths[unit])
            rows.append(K.Row(lhs, rhs)); indices.append(index)
        cases.append(replace(case, rows=tuple(rows)))
        origins[case.name] = tuple(indices)
    out = replace(ctx, revision=ctx.revision + '/F08-converted-' + target, cases=tuple(cases))
    out.validate()
    return out, origins


def _path_step(builder: K.Builder, index: int, path: tuple[str, ...]) -> int:
    for name in path:
        index = builder.conversion(name, index)
    return index


def receive_converted(ctx: K.Context, proof: K.Proof, expected: H.Request) -> K.Proof:
    """Graft a global converted-context proof into the current source/request."""
    if expected.case is not None:
        raise H.AuditError('This finite adapter accepts a global request.')
    converted, origins = converted_context(ctx, expected.unit)
    root = K.check(converted, proof)
    if root.case is not None or K.infer(root.new, ctx.signature) != expected.unit:
        raise H.AuditError('A global target-unit source proof is required.')
    paths = paths_to(ctx.signature, expected.unit)
    replacements = {}
    for case in converted.cases:
        for index, original in enumerate(origins[case.name]):
            b = K.Builder(ctx, case.name)
            current = b.row(original)
            unit = K.infer(b.steps[current].new, ctx.signature)
            current = _path_step(b, current, paths[unit])
            wanted, _, _, _ = K.normalized_row(converted, case.name, index)
            current = b.rewrite(current, wanted, K.num(0, expected.unit))
            candidate = b.proof(current)
            K.check(ctx, candidate)
            replacements[(case.name, case.name, index)] = candidate
    result = T.transport(converted, ctx, proof, replacements,
                         {h.name: h.name for h in ctx.cases})
    H.receive(ctx, result, expected)
    return result


def affine_certificate(ctx: K.Context, case: str, new: K.Term, old: K.Term,
                       budget: F, multipliers: tuple[F, ...]) -> K.Proof:
    """Check supplied affine multipliers and emit their native proof, no search."""
    ctx.validate()
    found = [h for h in ctx.cases if h.name == case]
    if len(found) != 1 or len(multipliers) != len(found[0].rows):
        raise H.AuditError('Multipliers must address exactly the selected case rows.')
    unit = K.infer(new, ctx.signature)
    if K.infer(old, ctx.signature) != unit:
        raise H.AuditError('Mixed query units.')
    _, offset = K.affine(K.sub(new, old), ctx.signature)
    weights = tuple(H.exact(x) for x in multipliers)
    budget = H.exact(budget)
    if any(x < 0 for x in weights):
        raise H.AuditError('Negative affine multiplier.')
    b = K.Builder(ctx, case)
    zero = K.num(0, unit)
    root = b.constant(zero, zero)
    for index, weight in enumerate(weights):
        if weight:
            if K.normalized_row(ctx, case, index)[2] != unit:
                raise H.AuditError('Convert nonzero-weight rows to the query unit.')
            root = b.add(root, b.scale(weight, b.row(index)))
    root = b.add(root, b.constant(K.num(offset, unit), zero))
    root = b.rewrite(root, new, old)
    slack = budget - b.steps[root].budget
    if slack < 0:
        raise H.AuditError('The supplied certificate does not meet this budget.')
    root = b.slack(slack, root)
    result = b.proof(root)
    K.check(ctx, result)
    return result


def lattice_path_equivalence(ctx: K.Context, case: str, a: K.Term, c: K.Term,
                             path: tuple[str, ...], kind: str):
    """Native zero-budget proofs of both path/min-or-max homomorphism directions."""
    if kind not in ('min', 'max'):
        raise H.AuditError('Expected min or max.')
    op = K.minimum if kind == 'min' else K.maximum
    left, gain = path_term(ctx.signature, op(a, c), path)
    pa, _ = path_term(ctx.signature, a, path)
    pc, _ = path_term(ctx.signature, c, path)
    right = op(pa, pc)
    b = K.Builder(ctx, case)
    if kind == 'max':
        ia = _path_step(b, b.lattice('max_left', a, c), path)
        ic = _path_step(b, b.lattice('max_right', a, c), path)
        backward = b.rewrite(b.max_common(ia, ic), right, left)
        aa, cc = K.scale(gain, a), K.scale(gain, c)
        ia = b.scale(1/gain, b.lattice('max_left', aa, cc))
        ic = b.scale(1/gain, b.lattice('max_right', aa, cc))
        forward = _path_step(b, b.max_common(ia, ic), path)
        forward = b.rewrite(forward, left, right)
    else:
        ia = _path_step(b, b.lattice('min_left', a, c), path)
        ic = _path_step(b, b.lattice('min_right', a, c), path)
        forward = b.rewrite(b.min_common(ia, ic), left, right)
        aa, cc = K.scale(gain, a), K.scale(gain, c)
        ia = b.scale(1/gain, b.lattice('min_left', aa, cc))
        ic = b.scale(1/gain, b.lattice('min_right', aa, cc))
        backward = _path_step(b, b.min_common(ia, ic), path)
        backward = b.rewrite(backward, right, left)
    first, second = T.prune(ctx, b.proof(forward)), T.prune(ctx, b.proof(backward))
    if K.check(ctx, first).budget != 0 or K.check(ctx, second).budget != 0:
        raise H.AuditError('Homomorphism construction lost zero-budget equality.')
    return first, second


def one_way_fixture(upper=None, *, reverse=False):
    conversions = [K.Conversion('price', 'P', 'U', F(2))]
    if reverse:
        conversions.append(K.Conversion('back', 'U', 'P', F(3)))
    sig = K.Signature('F08-unit-fixture-v1', ('P', 'U'), (('x', 'P'),), tuple(conversions))
    x = K.src('x')
    rows = (K.Row(K.convert('price', x), K.num(-2, 'U')),)
    if upper is not None:
        rows += (K.Row(x, K.num(H.exact(upper), 'P')),)
    ctx = K.Context(sig, 'fixed-observation', 'r1', (K.Case('h', rows, (('x', F(-1)),)),))
    ctx.validate()
    return ctx


def _guard_max(b: K.Builder, raw: K.Term, row_index: int, positive: bool):
    """Two directed equalities from a supplied exact sign row to selected max."""
    unit = K.infer(raw, b.ctx.signature); zero = K.num(0, unit)
    row = next(h for h in b.ctx.cases if h.name == b.case).rows[row_index]
    _, offset = K.affine(K.sub(row.lhs, row.rhs), b.ctx.signature)
    sign = b.add(b.row(row_index), b.constant(K.num(offset, unit), zero))
    sign = b.rewrite(sign, zero if positive else raw, raw if positive else zero)
    if b.steps[sign].budget != 0:
        raise H.AuditError('A sign equality requires a zero-threshold guard.')
    chosen = raw if positive else zero
    identity = b.constant(chosen, chosen)
    upper = b.max_common(identity, sign) if positive else b.max_common(sign, identity)
    lower = b.lattice('max_left' if positive else 'max_right', raw, zero)
    return upper, lower, chosen


def three_region_example():
    """Supplied two-cut tree with three live affine cells and one empty cell.

    Proves max(x,0)+max(1-x,0)<=2 on [-1,2], retaining an unbounded common z.
    Explicit witnesses/multipliers are development inputs, not found by search.
    """
    x, z = K.src('x'), K.src('z')
    other = K.sub(K.num(1), x)
    ctx = K.context(('x', 'z'), (K.Row(K.scale(-1, x), K.num(1)), K.Row(x, K.num(2))),
                    {'x': 0, 'z': 0}, scope='F08-three-region-v1')
    lhs = K.add(z, K.add(D.rho(x, ctx), D.rho(other, ctx)))
    negative = D.branch_context(ctx, x, False, {'x': F(0), 'z': F(0)})
    positive = D.branch_context(ctx, x, True, {'x': F(0), 'z': F(0)})

    def leaf(parent, xpos, opos, point, weights, bound):
        source = D.branch_context(parent, other, opos, {'x': F(point), 'z': F(0)})
        b = K.Builder(source, 'h')
        ix, _, selected_x = _guard_max(b, x, 2, xpos)
        io, _, selected_o = _guard_max(b, other, 3, opos)
        upper = b.add(b.constant(z, z), b.add(ix, io))
        selected = K.add(z, K.add(selected_x, selected_o))
        upper = b.rewrite(upper, lhs, selected)
        p = affine_certificate(source, 'h', selected, z, F(bound), tuple(map(F, weights)))
        index = T._copy_into(b, p)
        result = b.proof(b.trans(upper, index))
        K.check(source, result)
        return D.LiveBranch(source, result)

    neg_live = leaf(negative, False, True, -1, (1, 0, 0, 0), 2)
    ray = D.EmptyBranch((F(0), F(0), F(1)), F(1))
    neg_result = D.compile_sign_split(negative, other, ray, neg_live)
    pos_neg = leaf(positive, True, False, 2, (0, 1, 0, 0), 2)
    pos_pos = leaf(positive, True, True, F(1, 2), (0, 0, 0, 0), 1)
    pos_result = D.compile_sign_split(positive, other, pos_neg, pos_pos)
    result = D.compile_sign_split(ctx, x, D.LiveBranch(negative, neg_result.proof),
                                 D.LiveBranch(positive, pos_result.proof))
    H.receive(ctx, result.proof, H.request(ctx, 'h', lhs, z, 2))
    return ctx, result.proof, (neg_result.method, pos_result.method, result.method)


class F08UnitCharacterizationTests(unittest.TestCase):
    def test_one_way_reduct_countermodel_is_not_original_countermodel(self):
        ctx = one_way_fixture(); reduced = unit_reduct(ctx, 'P')
        self.assertTrue(ctx.feasible('h', {'x': F(-1)}))
        self.assertFalse(ctx.feasible('h', {'x': F(0)}))
        self.assertTrue(reduced.feasible('h', {'x': F(0)}))
        self.assertGreater(H.value(K.src('x'), ctx.signature, {'x': F(0)}), -1)
        self.assertEqual(reduced.cases[0].rows, ())

    def test_source_closed_direction(self):
        sig = one_way_fixture().signature
        self.assertFalse(source_closed(sig, 'P'))
        self.assertTrue(source_closed(sig, 'U'))

    def test_inaccessible_row_can_hide_arbitrarily_large_gap(self):
        for upper in (0, 1, 1000):
            ctx = one_way_fixture(upper); reduced = unit_reduct(ctx, 'P')
            self.assertTrue(reduced.feasible('h', {'x': F(upper)}))
            self.assertFalse(ctx.feasible('h', {'x': F(upper)}))
            p = affine_certificate(reduced, 'h', K.src('x'), K.num(0, 'P'), F(upper), (F(1),))
            self.assertEqual(K.check(reduced, p).budget, upper)

    def test_return_path_repairs_inference_even_with_nonreciprocal_factors(self):
        ctx = one_way_fixture(reverse=True); b = K.Builder(ctx, 'h')
        i = b.scale(F(1, 6), b.conversion('back', b.row(0)))
        i = b.rewrite(i, K.src('x'), K.num(0, 'P'))
        root = H.receive(ctx, b.proof(i), H.request(ctx, 'h', K.src('x'), K.num(0, 'P'), -1, 'P'))
        self.assertEqual(root.budget, -1)
        self.assertTrue(source_closed(ctx.signature, 'P'))

    def test_disconnected_unit_does_not_require_conversion(self):
        sig = K.Signature('disconnected', ('U', 'V'), (('x', 'U'), ('y', 'V')))
        self.assertTrue(source_closed(sig, 'U'))
        self.assertTrue(source_closed(sig, 'V'))

    def test_empty_source_signature_weakens_graph_only_requirement(self):
        sig = replace(one_way_fixture().signature, sources=())
        self.assertTrue(source_closed(sig, 'P'))

    def test_source_upstream_of_fork_is_relevant(self):
        sig = K.Signature('fork', ('A', 'U', 'V'), (('x', 'A'),),
                          (K.Conversion('a', 'A', 'U', F(1)), K.Conversion('b', 'A', 'V', F(1))))
        self.assertFalse(source_closed(sig, 'U'))
        self.assertFalse(source_closed(sig, 'V'))

    def test_source_after_fork_can_be_closed(self):
        sig = K.Signature('fork', ('A', 'U', 'V'), (('x', 'U'),),
                          (K.Conversion('a', 'A', 'U', F(1)), K.Conversion('b', 'A', 'V', F(1))))
        self.assertTrue(source_closed(sig, 'U'))

    def test_all_three_unit_graphs_against_independent_transitive_closure(self):
        units = ('A', 'B', 'C'); edges = tuple((a, b) for a in units for b in units if a != b)
        for flags in product((False, True), repeat=len(edges)):
            conversions = tuple(K.Conversion(str(i), a, b, F(i+1))
                                for i, ((a, b), active) in enumerate(zip(edges, flags)) if active)
            sig = K.Signature('graph', units, tuple((u, u) for u in units), conversions)
            reach = {(a, b): a == b or any(c.source == a and c.target == b for c in conversions)
                     for a in units for b in units}
            for middle in units:
                for a in units:
                    for b in units:
                        reach[a, b] = reach[a, b] or (reach[a, middle] and reach[middle, b])
            for target in units:
                ancestors = {a for a in units if reach[a, target]}
                self.assertEqual(set(paths_to(sig, target)), ancestors)
                expected = all(c.target in ancestors for c in conversions if c.source in ancestors)
                self.assertEqual(source_closed(sig, target), expected)

    def test_converted_context_is_same_reduct_not_same_full_source(self):
        ctx = one_way_fixture(3)
        for unit in ctx.signature.units:
            reduced = unit_reduct(ctx, unit); converted, _ = converted_context(ctx, unit)
            for x in map(F, (-3, -1, 0, 3, 4)):
                self.assertEqual(reduced.feasible('h', {'x': x}), converted.feasible('h', {'x': x}))
            self.assertTrue(all(K.infer(row.lhs, ctx.signature) == unit for row in converted.cases[0].rows))

    def test_exact_converted_proof_grafts_to_current_request(self):
        ctx = one_way_fixture(3); converted, _ = converted_context(ctx, 'U')
        x = K.convert('price', K.src('x')); zero = K.num(0)
        local = affine_certificate(converted, 'h', x, zero, F(-2), (F(1), F(0)))
        b = K.Builder(converted); index = T._copy_into(b, local); proof = b.proof(b.all_cases([index]))
        expected = H.request(ctx, None, x, zero, -2)
        output = receive_converted(ctx, proof, expected)
        self.assertEqual(H.receive(ctx, output, expected).budget, -2)
        self.assertEqual({s.context_id for s in output.steps}, {K.fingerprint(ctx)})
        with self.assertRaises((H.AuditError, K.ProofError)):
            receive_converted(ctx, proof, replace(expected, budget=F(-3)))
        with self.assertRaises((H.AuditError, K.ProofError)):
            receive_converted(ctx, proof, replace(expected, new=K.num(12)))
        with self.assertRaises((H.AuditError, K.ProofError)):
            receive_converted(ctx, proof, replace(expected, context_id='stale'))

    def test_affine_certificate_rejects_bad_multipliers_and_budget(self):
        ctx = one_way_fixture(3); reduced = unit_reduct(ctx, 'P')
        for weights, budget in (((F(-1),), F(3)), ((F(2),), F(6)), ((F(1),), F(2)), ((), F(3))):
            with self.subTest(weights=weights, budget=budget):
                with self.assertRaises((H.AuditError, K.ProofError)):
                    affine_certificate(reduced, 'h', K.src('x'), K.num(0, 'P'), budget, weights)

    def test_affine_certificate_rejects_unconverted_nonzero_row(self):
        ctx = one_way_fixture()
        with self.assertRaises(H.AuditError):
            affine_certificate(ctx, 'h', K.src('x'), K.num(0, 'P'), F(-1), (F(1),))

    def test_zero_weight_does_not_import_foreign_evidence(self):
        ctx = one_way_fixture()
        proof = affine_certificate(ctx, 'h', K.num(-1, 'P'), K.num(0, 'P'), F(-1), (F(0),))
        self.assertEqual(T.used_rows(ctx, proof), frozenset())

    def test_constant_comparison_with_no_rows(self):
        ctx = unit_reduct(one_way_fixture(), 'P')
        proof = affine_certificate(ctx, 'h', K.num(-2, 'P'), K.num(1, 'P'), F(-3), ())
        self.assertEqual(K.check(ctx, proof).budget, -3)

    def test_foreign_dead_let_does_not_invalidate_dependency_lemma(self):
        ctx = one_way_fixture(); sig = ctx.signature
        term = K.let('unused', K.convert('price', K.src('x')), K.num(-1, 'P'))
        b = K.Builder(ctx, 'h'); b.constant(term, K.num(0, 'P'))
        self.assertEqual(K.check(ctx, b.proof()).budget, -1)
        self.assertEqual(T.used_rows(ctx, b.proof()), frozenset())

    def test_unused_foreign_instruction_is_not_root_evidence(self):
        ctx = one_way_fixture(); b = K.Builder(ctx, 'h')
        b.row(0); b.constant(K.num(-1, 'P'), K.num(0, 'P'))
        self.assertEqual(T.used_rows(ctx, b.proof()), frozenset())
        self.assertEqual(len(T.prune(ctx, b.proof()).steps), 1)

    def test_lattice_conversion_requires_more_than_collected_identity(self):
        ctx = one_way_fixture(); a, c = K.src('x'), K.num(0, 'P')
        for kind, op in (('min', K.minimum), ('max', K.maximum)):
            left = K.convert('price', op(a, c)); right = op(K.convert('price', a), K.convert('price', c))
            self.assertNotEqual(K._form(left, ctx.signature), K._form(right, ctx.signature))
            for proof in lattice_path_equivalence(ctx, 'h', a, c, ('price',), kind):
                self.assertEqual(K.check(ctx, proof).budget, 0)
                self.assertEqual(T.used_rows(ctx, proof), frozenset())
                for x in map(F, (-3, -1, 0, 5)):
                    root = proof.steps[proof.root]
                    self.assertEqual(H.value(root.new, ctx.signature, {'x': x}),
                                     H.value(root.old, ctx.signature, {'x': x}))

    def test_multiedge_path_with_fractional_gain(self):
        ctx = one_way_fixture()
        sig = replace(ctx.signature, units=('P', 'U', 'W'), conversions=ctx.signature.conversions+
                      (K.Conversion('next', 'U', 'W', F(1, 3)),))
        ctx = replace(ctx, signature=sig)
        a, c = K.src('x'), K.scale(-2, K.src('x'))
        for kind in ('min', 'max'):
            for proof in lattice_path_equivalence(ctx, 'h', a, c, ('price', 'next'), kind):
                self.assertEqual(K.infer(K.check(ctx, proof).new, sig), 'W')

    def test_empty_path_and_nested_nonlinear_children(self):
        ctx = one_way_fixture()
        a = K.maximum(K.src('x'), K.num(0, 'P')); c = K.minimum(K.src('x'), K.num(1, 'P'))
        for path in ((), ('price',)):
            for kind in ('min', 'max'):
                for proof in lattice_path_equivalence(ctx, 'h', a, c, path, kind):
                    self.assertEqual(K.check(ctx, proof).budget, 0)

    def test_invalid_path_and_unknown_unit_fail(self):
        ctx = one_way_fixture()
        with self.assertRaises((K.SemanticError, H.AuditError)):
            path_term(ctx.signature, K.num(0), ('price',))
        with self.assertRaises(H.AuditError):
            paths_to(ctx.signature, 'missing')

    def test_zero_conversion_is_outside_fragment(self):
        ctx = one_way_fixture()
        sig = replace(ctx.signature, conversions=(K.Conversion('zero', 'P', 'U', F(0)),))
        with self.assertRaises(K.SemanticError):
            paths_to(sig, 'U')


class F08FiniteCaseConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctx, cls.proof, cls.methods = three_region_example()

    def test_three_live_regions_and_empty_child_compile_to_original_kernel(self):
        self.assertEqual(self.methods, ('strict-ray-exclusion', 'derived-sign', 'derived-sign'))
        self.assertEqual(K.check(self.ctx, self.proof).budget, 2)
        self.assertLessEqual({s.rule for s in self.proof.steps}, H.NATIVE_RULES)
        self.assertEqual({s.context_id for s in self.proof.steps}, {K.fingerprint(self.ctx)})

    def test_attainment_and_common_unbounded_baseline(self):
        root = K.check(self.ctx, self.proof)
        for x, z in product(map(F, (-1, 0, F(1, 2), 1, 2)), map(F, (-1000, 0, 1000))):
            point = {'x': x, 'z': z}
            self.assertTrue(H.case_feasible(self.ctx, 'h', point))
            delta = H.value(root.new, self.ctx.signature, point)-H.value(root.old, self.ctx.signature, point)
            self.assertLessEqual(delta, 2)
            if x in (F(-1), F(2)):
                self.assertEqual(delta, 2)

    def test_strict_request_cannot_use_attained_equality(self):
        root = K.check(self.ctx, self.proof)
        self.assertFalse(root.budget < 2)
        self.assertTrue(root.budget < F(5, 2))
        with self.assertRaises(H.AuditError):
            H.receive(self.ctx, self.proof, H.request(self.ctx, 'h', root.new, root.old, F(3, 2)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
