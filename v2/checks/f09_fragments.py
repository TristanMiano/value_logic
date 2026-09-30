"""Exact F09 fragment audits, not an integrated proof searcher.

Research contributor: Codex (GPT-6), 2026-09-30. Small Boolean formulas are
compiled by exhaustive point cases to the unchanged F06 checker. Tests also
call the actual phase-one consumers with exact Fraction inputs.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import unittest

from verification import kernel as P
from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as H


def loss(formula):
    """Translate the explicitly supplied finite propositional syntax."""
    op, *args = formula
    if op == 'atom' and len(args) == 1 and isinstance(args[0], str):
        return K.src(args[0])
    if op in ('top', 'bottom') and not args:
        return K.num(op == 'bottom' and 1 or 0)
    if op == 'not' and len(args) == 1:
        return K.sub(K.num(1), loss(args[0]))
    if op in ('and', 'or', 'implies') and len(args) == 2:
        constructor = {'and': K.maximum, 'or': K.minimum, 'implies': K.residual}[op]
        return constructor(loss(args[0]), loss(args[1]))
    raise H.AuditError('Malformed propositional formula.')


def classical(formula, truth):
    """Independent Boolean semantics; it does not evaluate numerical terms."""
    op, *args = formula
    if op == 'atom': return truth[args[0]]
    if op == 'top': return True
    if op == 'bottom': return False
    if op == 'not': return not classical(args[0], truth)
    a, b = classical(args[0], truth), classical(args[1], truth)
    if op == 'and': return a and b
    if op == 'or': return a or b
    if op == 'implies': return not a or b
    raise H.AuditError('Unknown connective.')


def boolean_context(names):
    names = tuple(names)
    if len(set(names)) != len(names) or len(names) > 6:
        raise H.AuditError('Unique atom names and at most six audit atoms required.')
    sig = K.Signature('F09-Boolean-loss-v1', ('U',), tuple((n, 'U') for n in names))
    cases = []
    for index, bits in enumerate(product((F(0), F(1)), repeat=len(names))):
        rows = tuple(row for name, value in zip(names, bits)
                     for row in (K.Row(K.src(name), K.num(value)),
                                 K.Row(K.num(value), K.src(name))))
        cases.append(K.Case(str(index), rows, tuple(zip(names, bits))))
    ctx = K.Context(sig, 'fixed-visible-observation', 'r1', tuple(cases))
    ctx.validate()
    return ctx


def _row_zero(builder, index):
    case = next(h for h in builder.ctx.cases if h.name == builder.case)
    row = case.rows[index]
    _, c = K.affine(K.sub(row.lhs, row.rhs), builder.ctx.signature)
    unit = K.infer(row.lhs, builder.ctx.signature)
    root = builder.add(builder.row(index), builder.constant(K.num(c, unit), K.num(0, unit)))
    return builder.rewrite(root, row.lhs, row.rhs)


def _point_equality(builder, term, names, point, cache):
    """Produce both directions t=v from the declared point rows, never sampling."""
    if term in cache: return cache[term]
    if term.op == 'const':
        out = (term.value, builder.constant(term, term), builder.constant(term, term))
    elif term.op == 'source':
        index = names.index(term.name)
        out = (point[term.name], _row_zero(builder, 2*index), _row_zero(builder, 2*index+1))
    else:
        a, au, al = _point_equality(builder, term.args[0], names, point, cache)
        if term.op == 'scale':
            k = term.value
            if k >= 0: up, lo = builder.scale(k, au), builder.scale(k, al)
            else: up, lo = builder.scale(-k, builder.negate(al)), builder.scale(-k, builder.negate(au))
            value = k*a
        else:
            b, bu, bl = _point_equality(builder, term.args[1], names, point, cache)
            if term.op == 'add':
                value, up, lo = a+b, builder.add(au, bu), builder.add(al, bl)
            elif term.op in ('min', 'max'):
                value = min(a,b) if term.op == 'min' else max(a,b)
                up, lo = builder.congruence(term.op, au, bu), builder.congruence(term.op, al, bl)
            elif term.op == 'res':
                value = max(b-a, F(0))
                up, lo = builder.res_congruence(al, bu), builder.res_congruence(au, bl)
            else:
                raise H.AuditError('The Boolean audit compiler has no other term constructors.')
        out = (value, builder.rewrite(up, term, K.num(value)), builder.rewrite(lo, K.num(value), term))
    cache[term] = out
    return out


def entailment_certificate(names, premises, conclusion):
    """Bounded exhaustive producer; native checking, not its truth loop, accepts."""
    names, premises = tuple(names), tuple(premises)
    ctx = boolean_context(names)
    new, old = loss(conclusion), K.num(0)
    for premise in premises: old = K.maximum(old, loss(premise))
    K.infer(new, ctx.signature); K.infer(old, ctx.signature)
    outer, roots = K.Builder(ctx), []
    for case in ctx.cases:
        point = dict(case.witness)
        truth = {n: point[n] == 0 for n in names}
        if all(classical(a, truth) for a in premises) and not classical(conclusion, truth):
            raise H.AuditError('Classical countervaluation: ' + repr(truth))
        builder, cache = K.Builder(ctx, case.name), {}
        nv, upper, _ = _point_equality(builder, new, names, point, cache)
        ov, _, lower = _point_equality(builder, old, names, point, cache)
        middle = builder.constant(K.num(nv), K.num(ov))
        root = builder.trans(builder.trans(upper, middle), lower)
        root = builder.rewrite(root, new, old)
        local = T.prune(ctx, builder.proof(root))
        roots.append(T._copy_into(outer, local))
    root = outer.all_cases(roots)
    proof = outer.proof(root)
    expected = H.request(ctx, None, new, old, F(0))
    H.receive(ctx, proof, expected)
    return ctx, proof, expected


def status(values):
    values = tuple(values)
    if not values: raise H.AuditError('Nonempty exact reference set required.')
    if max(values) <= 0: return P.AtomValue.SUPPORTED
    if min(values) > 0: return P.AtomValue.REFUTED
    return P.AtomValue.OPEN


def status_code(value):
    if not isinstance(value, P.AtomValue): raise H.AuditError('An actual phase-one status is required.')
    return F(2-int(value), 2)


def examples():
    p, q = ('atom','p'), ('atom','q')
    return {
        'excluded_middle': entailment_certificate(('p',), (), ('or',p,('not',p))),
        'modus_ponens': entailment_certificate(('p','q'), (p,('implies',p,q)), q),
        'inconsistent_premises': entailment_certificate(('p','q'), (p,('not',p)), q),
        'no_atoms': entailment_certificate((), (), ('top',)),
    }


class F09BooleanTests(unittest.TestCase):
    def test_all_supplied_certificates_received(self):
        for name, (ctx, proof, expected) in examples().items():
            with self.subTest(name=name):
                self.assertLessEqual(H.receive(ctx, proof, expected).budget, 0)
                for case in ctx.cases:
                    root = proof.steps[proof.root]
                    self.assertLessEqual(H.value(root.new, ctx.signature, dict(case.witness)) -
                                         H.value(root.old, ctx.signature, dict(case.witness)), 0)

    def test_finite_truth_table_against_independent_boolean_interpreter(self):
        atoms = (('atom','p'), ('atom','q'), ('top',), ('bottom',))
        formulas = atoms + tuple(('not',a) for a in atoms) + tuple(
            (op,a,b) for op in ('and','or','implies') for a in atoms for b in atoms)
        ctx = boolean_context(('p','q'))
        for formula, case in product(formulas, ctx.cases):
            point = dict(case.witness)
            truth = {n: v == 0 for n,v in point.items()}
            self.assertEqual(H.value(loss(formula), ctx.signature, point),
                             0 if classical(formula, truth) else 1)

    def test_invalid_entailment_returns_countervaluation(self):
        with self.assertRaisesRegex(H.AuditError, 'countervaluation'):
            entailment_certificate(('p','q'), (('atom','p'),), ('atom','q'))

    def test_interval_excluded_middle_countermodel(self):
        ctx = K.context(('p',), (K.Row(K.num(0),K.src('p')), K.Row(K.src('p'),K.num(1))), {'p':F(1,2)})
        term = loss(('or',('atom','p'),('not',('atom','p'))))
        self.assertTrue(H.case_feasible(ctx, 'h', {'p':F(1,2)}))
        self.assertEqual(H.value(term, ctx.signature, {'p':F(1,2)}), F(1,2))

    def test_equivalent_boolean_implications_differ_continuously(self):
        sig = boolean_context(('p',)).signature
        p = ('atom','p')
        self.assertEqual(H.value(loss(('implies',p,p)),sig,{'p':F(1,2)}),0)
        self.assertEqual(H.value(loss(('or',('not',p),p)),sig,{'p':F(1,2)}),F(1,2))

    def test_not_closed_under_addition(self):
        self.assertEqual(H.value(K.add(K.num(1),K.num(1)), boolean_context(()).signature, {}),2)

    def test_every_case_required_and_literal_pair_bound(self):
        ctx, proof, expected = examples()['excluded_middle']
        steps = list(proof.steps)
        steps[-1] = replace(steps[-1], parents=steps[-1].parents[:-1])
        with self.assertRaises(K.ProofError): K.check(ctx, K.Proof(tuple(steps),proof.root))
        with self.assertRaises(H.AuditError):
            H.receive(ctx, proof, replace(expected, new=K.num(0)))


class F09PhaseOneTests(unittest.TestCase):
    def test_exact_status_meet_embedding_all_families_up_to_four(self):
        for n in range(1,5):
            for family in product(tuple(P.AtomValue),repeat=n):
                self.assertEqual(status_code(P.meet(family)), max(map(status_code,family)))

    def test_actual_upper_bound_consumer_exact_endpoints(self):
        for lo, hi, threshold in product(range(-2,3),repeat=3):
            if lo > hi: continue
            result = P.assess_upper_bound('risk',P.Interval(F(lo),F(hi)),F(threshold),'cert',('source',))
            self.assertEqual(result.value,status((F(lo-threshold),F(hi-threshold))))

    def test_actual_improvement_consumer_exact_rectangles(self):
        intervals = tuple((F(l),F(u)) for l in range(3) for u in range(l,3))
        for (le,ue),(lf,uf),d in product(intervals,intervals,(F(0),F(1))):
            result = P.assess_improvement('improve',P.Interval(le,ue),P.Interval(lf,uf),d,'cert',('source',))
            self.assertEqual(result.value,status((le+d-uf,ue+d-lf)))

    def test_equality_is_supported_not_refuted(self):
        result = P.assess_upper_bound('risk',P.Interval(F(1),F(1)),F(1),'cert',('source',))
        self.assertEqual(result.value,P.AtomValue.SUPPORTED)

    def test_missing_evidence_remains_open_with_obstacle(self):
        result = P.assess_upper_bound('risk',None,F(1),'cert',('source',))
        self.assertEqual(result.value,P.AtomValue.OPEN)
        self.assertTrue(result.obstacles)

    def test_joint_improvement_is_stronger_than_rectangle_adapter(self):
        result = P.assess_improvement('improve',P.Interval(F(0),F(1)),P.Interval(F(1),F(2)),F(1),'cert',('source',))
        self.assertEqual(result.value,P.AtomValue.OPEN)
        self.assertEqual(status(x+1-(x+1) for x in (F(0),F(1,2),F(1))),P.AtomValue.SUPPORTED)

    def test_correlated_open_atoms_jointly_refuted(self):
        marginals = (status((F(0),F(1))),status((F(1),F(0))))
        self.assertEqual(P.meet(marginals),P.AtomValue.OPEN)
        self.assertEqual(status((F(1),F(1))),P.AtomValue.REFUTED)

    def test_product_domain_recovers_atomwise_aggregation(self):
        sets = ((F(-1),),(F(0),),(F(1),),(F(-1),F(1)),(F(0),F(1)))
        for family in product(sets,repeat=3):
            actual = status(max(point) for point in product(*family))
            self.assertEqual(actual,P.meet(status(s) for s in family))

    def test_full_assessment_not_determined_by_numeric_projection(self):
        diag = P.supported('risk','cert',('source',))
        ctx = P.EvaluationContext('q',frozenset(('h',)),F(1),'fallback',P.Interval(F(2),F(2)),F(0))
        state = P.EpistemicState('s',{'m':P.UsePlan('m',frozenset(('h',)),0,0,P.Interval(0,0))},
            {'q':ctx},{'p':P.Profile('p',('risk',))},{'r':P.Request('r','m','q','p')},
            {'r':{'risk':diag}},{},{},frozenset(),P.ProvenanceGraph(frozenset(),()))
        self.assertEqual(P.assess_request(state,'r').outcome,P.Outcome.GRANTED)
        malformed = replace(state,contexts={'q':replace(ctx,fallback=None)})
        self.assertEqual(malformed.diagnostics,state.diagnostics)
        self.assertEqual(P.assess_request(malformed,'r').outcome,P.Outcome.UNDEFINED)

    def test_status_constant_forgets_provenance(self):
        a,b = P.supported('risk','cert-A',('source-A',)),P.supported('risk','cert-B',('source-B',))
        self.assertNotEqual(a,b)
        self.assertEqual(status_code(a.value),status_code(b.value))


if __name__ == '__main__': unittest.main()
