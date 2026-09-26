"""Gate A reconstruction fixtures, independent of the F04 implementation.

These small exact-rational examples audit selected readiness premises. They do
not implement the future calculus or mechanically decide whether a gate passes.
Run: python -m v2.checks.gate_a_review --json <path>
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import unittest
from itertools import product


def dot(a, b):
    if len(a) != len(b):
        raise ValueError('dimension mismatch')
    return sum((Q(x)*Q(y) for x, y in zip(a, b)), Q(0))


def certificate(A, rhs, v, intercept, bound, weights, witness, *,
                source_version='v1', proof_version='v1'):
    """Check a supplied finite linear certificate and a feasibility witness.

    This helper does not discover weights or certify empirical source validity.
    """
    n = len(v)
    if not A or any(len(row) != n for row in A):
        raise ValueError('nonempty, dimensionally consistent rows required')
    if len(A) != len(rhs) or len(A) != len(weights) or len(witness) != n:
        raise ValueError('dimension mismatch')
    if source_version != proof_version:
        return False
    if any(Q(w) < 0 for w in weights):
        return False
    if any(dot(row, witness) > Q(b) for row, b in zip(A, rhs)):
        return False
    coefficients = tuple(sum((Q(A[i][j])*Q(weights[i]) for i in range(len(A))), Q(0))
                         for j in range(n))
    return coefficients == tuple(map(Q, v)) and Q(intercept)+dot(weights, rhs) <= Q(bound)


def failure(p, s, r):
    return (1-r)*p + r*s


def least_report(p, s, slack=Q(0)):
    p, s, slack = Q(p), Q(s), Q(slack)
    if not (0 <= p <= 1 and 0 <= s <= 1 and slack >= 0):
        raise ValueError('probability or slack out of range')
    den = 1+p-s
    return Q(0) if den == 0 else max(Q(0), (p-slack)/den)


def chord(theta, cells=4):
    theta = Q(theta)
    if cells < 1 or not 0 <= theta <= 1:
        raise ValueError('invalid mesh or input')
    i = min((theta*cells).numerator//(theta*cells).denominator, cells-1)
    a, b = Q(i, cells), Q(i+1, cells)
    return (a+b)*theta-a*b


A = ((1,-1,0),(-1,1,0),(0,1,0),(0,-1,0),(0,0,1))
ETA = (Q(1,2),Q(-1,2),Q(1,4),Q(0),Q(1,32))
V = (Q(-1,4),Q(1,4),Q(1))
WEIGHTS = (Q(0),Q(1,4),Q(0),Q(0),Q(1))
WITNESS = (Q(1,2),Q(0),Q(0))


class GateAReviewTests(unittest.TestCase):
    def test_reflective_intended_cost_certificate_and_tightness(self):
        self.assertTrue(certificate(A, ETA, V, Q(1,16), Q(-1,32), WEIGHTS, WITNESS))
        for s in (Q(0),Q(1,8),Q(1,4)):
            x = (s+Q(1,2),s,Q(1,32))
            self.assertEqual(Q(1,16)+dot(V,x),Q(-1,32))

    def test_report_certificates_are_tight_and_use_fixed_reports(self):
        for r in (Q(1,2),Q(3,4)):
            v = (1-r,r,0)
            lam = (1-r,0,1,0,0)
            b = Q(3,4)-Q(3,2)*r
            self.assertTrue(certificate(A, ETA, v, -r, b, lam, WITNESS))
            self.assertEqual(failure(Q(3,4),Q(1,4),r)-r,b)

    def test_reversed_or_negative_certificate_is_not_accepted(self):
        bad = (0,Q(-1,4),0,0,1)
        self.assertFalse(certificate(A, ETA, V, Q(1,16), 0, bad, WITNESS))
        self.assertFalse(certificate(A, ETA, tuple(-x for x in V), Q(1,16), 0,
                                     WEIGHTS, WITNESS))

    def test_wrong_source_version_does_not_authorize_reuse(self):
        self.assertFalse(certificate(A, ETA, V, Q(1,16), 0, WEIGHTS, WITNESS,
                                     source_version='changed',proof_version='v1'))

    def test_empty_evidence_cannot_supply_deployment_witness(self):
        self.assertFalse(certificate(((1,),(-1,)),(0,-1),(0,),0,0,(1,1),(0,)))

    def test_omitted_proxy_alignment_allows_reversal(self):
        self.assertGreater(Q(1,16)+dot(V,(Q(1,2),0,Q(1,8))),0)

    def test_shared_composition_differs_from_sum_of_separate_maxima(self):
        grid = [Q(k,8) for k in range(9)]
        d1 = [t-Q(3,4) for t in grid]
        d2 = [Q(1,4)-t for t in grid]
        self.assertEqual(max(a+b for a,b in zip(d1,d2)),Q(-1,2))
        self.assertEqual(max(d1)+max(d2),Q(1,2))

    def test_chord_error_matches_exact_identity(self):
        for i in range(4):
            a,b=Q(i,4),Q(i+1,4)
            for j in range(17):
                t=a+(b-a)*Q(j,16)
                self.assertEqual(chord(t)-t*t,(t-a)*(b-t))
                self.assertLessEqual(chord(t)-t*t,Q(1,64))

    def test_approximate_function_retains_exact_requested_improvement(self):
        knots=[Q(1,4),Q(1,2),Q(3,4)]
        self.assertEqual(max(chord(t)-t for t in knots),Q(-3,16))
        self.assertEqual(max(t*t-t for t in knots),Q(-3,16))
        self.assertNotEqual(chord(Q(3,8)),Q(3,8)**2)

    def test_exact_report_has_degenerate_jump(self):
        self.assertEqual(least_report(0,1),0)
        self.assertEqual(least_report(Q(1,10**12),1),1)

    def test_slack_report_grid_checks_lipschitz_bound(self):
        points=list(product([Q(i,8) for i in range(9)],repeat=2))
        xi=Q(1,4)
        for (p,s),(u,v) in product(points,repeat=2):
            self.assertLessEqual(abs(least_report(p,s,xi)-least_report(u,v,xi)),
                                 max(abs(p-u),abs(s-v))/xi)

    def test_rounding_constant_and_policy_parameter_distinction(self):
        r=Q(5,16)
        self.assertEqual(failure(Q(1),Q(0),r)-r,Q(1,4)+2*Q(1,16))
        published=r+Q(1,4)+2*Q(1,16)
        self.assertNotEqual(failure(1,0,r),failure(1,0,published))

    def test_evidence_weakening_preserves_report_but_not_improvement(self):
        # Delta=1/4 weakens row two; the new feasible source attains deterioration.
        x=(Q(1,4),Q(0),Q(1,32))
        self.assertLessEqual(failure(x[0],x[1],Q(3,4)),Q(3,4))
        self.assertEqual(Q(1,16)+dot(V,x),Q(1,32))

    def test_invertible_numerical_recoding_can_lose_a_bound(self):
        x,y=Q(3),Q(0)
        self.assertLessEqual(x+y,3)
        self.assertLessEqual(y,2)
        self.assertGreater(x,1)

    def test_regional_lift_uses_domain_and_correct_sign(self):
        lam=nu=Q(1)
        self.assertEqual(lam-(-nu),2)
        for z in (Q(1),Q(3,2),Q(10)):
            self.assertLessEqual(z,2*z-1)
        self.assertGreater(Q(0),2*Q(0)-1)

    def test_brier_improvement_does_not_order_classification_error(self):
        eta=Q(3,5)
        def brier(q): return eta*(1-q)**2+(1-eta)*q*q
        self.assertLess(brier(Q(49,100)),brier(Q(1)))
        self.assertGreater(eta,1-eta)

    def test_valid_portfolio_is_not_necessarily_the_tightest_bound(self):
        # g<=eta1, g<=eta2; retaining only lambda=(1,0) is sound but may be loose.
        eta=(Q(2),Q(1))
        self.assertTrue(certificate(((1,),(1,)),eta,(1,),0,2,(1,0),(0,)))
        self.assertLess(min(eta),dot((1,0),eta))


def summary():
    return {'scope':'Gate A selected-premise reconstruction; not a calculus or neural result',
            'arithmetic':'fractions.Fraction; no F04 implementation imported',
            'reflective_intended_cost_bound':'-1/32',
            'shared_composition_bound':'-1/2',
            'separate_composition_bound':'1/2',
            'four_cell_chord_max_excess':'1/64',
            'comparison_bound_on_quarter_interval':'-3/16',
            'slack_lipschitz_finite_cases':9**4,
            'limits':'Finite examples support reconstruction; general statements rely on arguments in A_1_reconstruction.md and the source notes.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(GateAReviewTests))
    if result.wasSuccessful() and args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps({'tests_run':result.testsRun,**summary()},indent=2)+'\n',encoding='utf-8')
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':
    raise SystemExit(main())
