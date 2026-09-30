"""Finite F08 report-boundary fixtures; no automatic vertex/report search.

Research contributor: Codex (GPT-6), 2026-09-30.
The source laws and complete vertex lists below are supplied and justified in
04d_warranted_report_characterization.md. They are not empirical calibration.
"""
from __future__ import annotations

from fractions import Fraction as F
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as H
from v2.checks import f08_unit_characterization as U


def least_report(vertices):
    """Exact bound for a supplied nonempty probability vertex catalogue."""
    if not isinstance(vertices, tuple) or not vertices:
        raise H.AuditError('A nonempty finite vertex tuple is required.')
    ratios = [F(0)]
    for p, s in vertices:
        p, s = H.exact(p), H.exact(s)
        if not 0 <= p <= 1 or not 0 <= s <= 1:
            raise H.AuditError('Probabilities must belong to the unit square.')
        denominator = 1+p-s
        if denominator:
            ratios.append(p/denominator)
    return max(ratios)


def risk(r):
    r = H.exact(r)
    if not 0 <= r <= 1:
        raise H.AuditError('A fixed mixture report must belong to [0,1].')
    return K.add(K.scale(1-r, K.src('p')), K.scale(r, K.src('s')))


def rectangle_context():
    p, s = K.src('p'), K.src('s')
    rows = (K.Row(p, K.num(1, 'P')), K.Row(s, K.num(F(1, 4), 'P')),
            K.Row(K.scale(-1, p), K.num(0, 'P')), K.Row(K.scale(-1, s), K.num(0, 'P')))
    return K.context((('p', 'P'), ('s', 'P')), rows, {'p': 1, 's': F(1, 4)},
                     units=('P',), scope='F08-report-rectangle-v1')


def segment_context():
    p, s = K.src('p'), K.src('s'); total = K.add(p, s)
    rows = (K.Row(total, K.num(1, 'P')), K.Row(K.scale(-1, total), K.num(-1, 'P')),
            K.Row(K.scale(-1, p), K.num(0, 'P')), K.Row(K.scale(-1, s), K.num(0, 'P')))
    return K.context((('p', 'P'), ('s', 'P')), rows, {'p': 1, 's': 0},
                     units=('P',), scope='F08-report-joint-v1')


class F08WarrantedReportTests(unittest.TestCase):
    def test_rectangle_least_report_is_four_sevenths_and_native(self):
        vertices = tuple((p, s) for p in (F(0), F(1)) for s in (F(0), F(1, 4)))
        r = least_report(vertices); self.assertEqual(r, F(4, 7))
        ctx = rectangle_context(); new, old = risk(r), K.num(r, 'P')
        proof = U.affine_certificate(ctx, 'h', new, old, F(0), (1-r, r, F(0), F(0)))
        self.assertEqual(H.receive(ctx, proof, H.request(ctx, 'h', new, old, 0, 'P')).budget, 0)

    def test_every_smaller_test_report_has_an_exact_source_countermodel(self):
        ctx = rectangle_context(); point = {'p': F(1), 's': F(1, 4)}
        for r in (F(0), F(1, 3), F(7, 16), F(4, 7)-F(1, 10**6)):
            self.assertTrue(H.case_feasible(ctx, 'h', point))
            self.assertGreater(H.value(risk(r), ctx.signature, point), r)
        self.assertEqual(H.value(risk(F(7, 16)), ctx.signature, point)-F(7, 16), F(15, 64))

    def test_higher_report_has_strict_native_margin_without_corner(self):
        ctx = rectangle_context(); r = F(3, 4)
        proof = U.affine_certificate(ctx, 'h', risk(r), K.num(r, 'P'), F(-5, 16),
                                     (1-r, r, F(0), F(0)))
        self.assertLess(K.check(ctx, proof).budget, 0)
        with self.assertRaises(H.AuditError):
            H.receive(ctx, proof, H.request(ctx, 'h', risk(F(7, 16)), K.num(F(7, 16), 'P'), 0, 'P'))

    def test_joint_segment_has_exact_native_boundary_for_eight_reports(self):
        ctx = segment_context(); self.assertEqual(least_report(((F(1), F(0)), (F(0), F(1)))), F(1, 2))
        for r in (F(0), F(1, 4), F(7, 16), F(1, 2), F(4, 7), F(3, 4), F(9, 10), F(1)):
            if r >= F(1, 2):
                weights = (r, F(0), 2*r-1, F(0)); bound = F(0); witness = {'p': F(0), 's': F(1)}
            else:
                weights = (1-r, F(0), F(0), 1-2*r); bound = 1-2*r; witness = {'p': F(1), 's': F(0)}
            proof = U.affine_certificate(ctx, 'h', risk(r), K.num(r, 'P'), bound, weights)
            self.assertEqual(K.check(ctx, proof).budget, bound)
            self.assertTrue(H.case_feasible(ctx, 'h', witness))
            self.assertEqual(H.value(risk(r), ctx.signature, witness)-r, bound)

    def test_zero_denominator_corner_never_yields_strict_report(self):
        self.assertEqual(least_report(((F(0), F(1)),)), 0)
        self.assertEqual(least_report(((F(1), F(0)), (F(0), F(1)))), F(1, 2))
        ctx = segment_context(); point = {'p': F(0), 's': F(1)}
        for r in (F(0), F(1, 2), F(3, 4), F(1)):
            self.assertEqual(H.value(risk(r), ctx.signature, point), r)

    def test_marginal_probability_box_loses_joint_warrant(self):
        square = tuple((p, s) for p in (F(0), F(1)) for s in (F(0), F(1)))
        self.assertEqual(least_report(square), 1)
        self.assertEqual(least_report(((F(1), F(0)), (F(0), F(1)))), F(1, 2))

    def test_probability_validation_and_empty_catalogue(self):
        for bad in ((), iter(()), ((F(-1), F(0)),), ((F(0), F(2)),), ((0.5, F(0)),)):
            with self.assertRaises((H.AuditError, K.SemanticError)):
                least_report(bad)

    def test_least_warranted_and_cost_optimal_need_not_coincide(self):
        self.assertEqual(least_report(((F(1), F(0)),)), F(1, 2))
        loss = lambda r, cost: 1-r+cost*r
        self.assertLess(loss(F(1), F(1, 10)), loss(F(1, 2), F(1, 10)))
        self.assertLess(loss(F(1, 2), F(2)), loss(F(1), F(2)))

    def test_robust_improvement_is_not_uniform_paired_improvement(self):
        vertices = ((F(9, 10), F(1, 10)), (F(1, 10), F(9, 10)))
        self.assertEqual(least_report(vertices), F(1, 2))
        value = lambda r, pair: (1-r)*pair[0]+r*pair[1]
        self.assertEqual(max(value(F(3, 4), v) for v in vertices), F(7, 10))
        self.assertEqual(max(value(F(1, 2), v) for v in vertices), F(1, 2))
        self.assertEqual(value(F(1, 2), vertices[0])-value(F(3, 4), vertices[0]), F(1, 5))


if __name__ == '__main__':
    unittest.main(verbosity=2)
