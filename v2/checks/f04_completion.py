"""Exact finite F04 completion examples; not a general optimizer or RLL prover.

The analytical claims are in 01e_equal_information_completion.md. This module
checks supplied rational certificates, attained witnesses and finite controls.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import sys
import unittest


def rational(x: int | Q) -> Q:
    if isinstance(x, bool) or not isinstance(x, (int, Q)):
        raise TypeError('Use exact integers or Fractions, not floats/bools.')
    return Q(x)


def vector(xs, n: int | None = None) -> tuple[Q, ...]:
    result = tuple(rational(x) for x in xs)
    if n is not None and len(result) != n:
        raise ValueError('Dimension mismatch.')
    return result


def dot(xs, ys) -> Q:
    a, b = vector(xs), vector(ys)
    if len(a) != len(b):
        raise ValueError('Dimension mismatch.')
    return sum((x*y for x, y in zip(a, b)), Q(0))


@dataclass(frozen=True)
class Source:
    """A declared finite linear source with an explicit feasibility witness."""
    scope: str
    rows: tuple[tuple[Q, ...], ...]
    bounds: tuple[Q, ...]
    witness: tuple[Q, ...]

    def __post_init__(self):
        if not isinstance(self.scope, str) or not self.scope:
            raise ValueError('A nonempty source/evaluator scope is required.')
        w = vector(self.witness)
        if not w:
            raise ValueError('At least one source coordinate is required.')
        rows = tuple(vector(row, len(w)) for row in self.rows)
        bounds = vector(self.bounds, len(rows))
        object.__setattr__(self, 'rows', rows)
        object.__setattr__(self, 'bounds', bounds)
        object.__setattr__(self, 'witness', w)
        if not self.contains(w):
            raise ValueError('The supplied witness does not satisfy the source.')

    @property
    def n(self):
        return len(self.witness)

    def contains(self, point) -> bool:
        p = vector(point, self.n)
        return all(dot(row, p) <= b for row, b in zip(self.rows, self.bounds))

    def check(self, *, scope: str, query, constant=0, weights, bound) -> Q:
        """Check a supplied multiplier vector; return its derived upper bound."""
        if scope != self.scope:
            raise ValueError('Source/evaluator scope mismatch.')
        v = vector(query, self.n)
        lam = vector(weights, len(self.rows))
        c, b = rational(constant), rational(bound)
        if any(x < 0 for x in lam):
            raise ValueError('Negative source multiplier.')
        lhs = tuple(sum((lam[i]*row[j] for i, row in enumerate(self.rows)), Q(0))
                    for j in range(self.n))
        if lhs != v:
            raise ValueError('Certificate does not reproduce the query coefficients.')
        derived = c + dot(lam, self.bounds)
        if derived > b:
            raise ValueError('Certificate exceeds the requested bound.')
        return derived


def finite_upper(points, query, constant=0) -> Q:
    """Maximum on an explicitly enumerated finite set, not an inferred hull."""
    pts = tuple(vector(x) for x in points)
    if not pts:
        raise ValueError('Do not authorize from empty evidence.')
    v = vector(query, len(pts[0]))
    c = rational(constant)
    return max(c+dot(x, v) for x in pts)


def composition_values(points, queries, constants):
    pts = tuple(vector(p) for p in points)
    if not pts:
        raise ValueError('Empty evidence.')
    qs = tuple(vector(q, len(pts[0])) for q in queries)
    cs = vector(constants, len(qs))
    if not qs:
        raise ValueError('Use at least one component.')
    vals = tuple(tuple(c+dot(q, p) for p in pts) for q, c in zip(qs, cs))
    maxima = tuple(max(v) for v in vals)
    joint = max(sum((v[i] for v in vals), Q(0)) for i in range(len(pts)))
    common = tuple(i for i in range(len(pts))
                   if all(v[i] == m for v, m in zip(vals, maxima)))
    return joint, sum(maxima, Q(0)), common


def relu(x):
    return max(rational(x), Q(0))


def chord(k: int, theta: int | Q) -> Q:
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError('k must be a positive integer.')
    t = rational(theta)
    if not Q(0) <= t <= Q(1):
        raise ValueError('This envelope is scoped to [0,1].')
    return t/k + Q(2,k)*sum((relu(t-Q(j,k)) for j in range(1,k)), Q(0))


def report_floor(points) -> Q:
    pts = tuple(vector(p, 2) for p in points)
    if not pts:
        raise ValueError('Empty branch-probability family.')
    if any(not Q(0) <= x <= Q(1) for p in pts for x in p):
        raise ValueError('Probabilities must lie in [0,1].')
    return max((p/(1+p-s) if 1+p-s else Q(0) for p, s in pts), default=Q(0))


def failure(p, s, r) -> Q:
    p, s, r = vector((p,s,r), 3)
    if any(not Q(0) <= x <= Q(1) for x in (p,s,r)):
        raise ValueError('Probabilities/report outside [0,1].')
    return (1-r)*p+r*s


def reflective_source(delta=Q(0), epsilon=Q(0)) -> Source:
    d, e = rational(delta), rational(epsilon)
    if not Q(0) <= d <= Q(1,2) or e < 0:
        raise ValueError('Revision is outside the declared domain.')
    return Source('SELF-MIX:v1:cost-units-1:paired-error',
                  ((1,-1,0),(-1,1,0),(0,1,0),(0,-1,0),(0,0,1)),
                  (Q(1,2),-Q(1,2)+d,Q(1,4),Q(0),Q(1,32)+e),
                  (Q(1,2)-d,Q(0),Q(1,32)+e))


def report_bound(source: Source, r) -> Q:
    r = rational(r)
    if not Q(0) <= r <= Q(1):
        raise ValueError('Report outside [0,1].')
    b = Q(3,4)-Q(3,2)*r
    return source.check(scope=source.scope, query=(1-r,r,0), constant=-r,
                        weights=(1-r,0,1,0,0), bound=b)


def intended_change_bound(source: Source) -> Q:
    lam = (0,Q(1,4),0,0,1)
    b = Q(1,16)+dot(lam, source.bounds)
    return source.check(scope=source.scope, query=(-Q(1,4),Q(1,4),1),
                        constant=Q(1,16), weights=lam, bound=b)


def slack_floor(p, s, xi) -> Q:
    p, s, xi = vector((p,s,xi), 3)
    if not 0 <= p <= 1 or not 0 <= s <= 1 or xi < 0:
        raise ValueError('Probability/slack outside the declared domain.')
    d = 1+p-s
    return max(Q(0),(p-xi)/d) if d else Q(0)


def report() -> dict:
    src = reflective_source()
    joint, separate, common = composition_values(((0,),(1,)), ((1,),(-1,)),
                                                  (-Q(3,4),Q(1,4)))
    return {
        'scope': 'F04 finite completion fixtures; no full calculus, solver or neural training',
        'source_feasibility_witness': list(map(str, src.witness)),
        'composition': {'joint':str(joint),'separate':str(separate),
                        'common_maximizer_indices':list(common)},
        'update_counterexample': {'K_after': '0', 'convex_hull_after': '1',
                                 'shared_condition': 'x=y'},
        'quadratic_chord': {'k':4,'uniform_upper_error':'1/64',
                            'restricted_old_new_bound_k2':'-1/8',
                            'restricted_old_new_bound_k4':'-3/16',
                            'lower_bound_scope':'affine interval count, not neuron count'},
        'reflective': {'old_report':'1/2','new_report':'3/4',
                       'old_report_shortfall_bound':str(report_bound(src,Q(1,2))),
                       'new_report_shortfall_bound':str(report_bound(src,Q(3,4))),
                       'intended_change_bound':str(intended_change_bound(src)),
                       'relaxed_delta_1_8':str(intended_change_bound(reflective_source(Q(1,8)))),
                       'relaxed_delta_1_4':str(intended_change_bound(reflective_source(Q(1,4))))},
        'enumeration': {'common_argmax_cases':625,'chord_k_values':list(range(1,9)),
                        'reflective_revision_cases':45},
        'reflection_stability': {'exact_corner_threshold':'0', 'positive_p_s1_threshold':'1',
                                 'slack_lipschitz_bound':'1/xi in infinity norm, xi>0',
                                 'rounding_example_shortfall':'3/8'},
        'analytic_not_enumerated': ['finite-cone converse','non-ReLU-exact quadratic',
                                   'sharp conservative interpolation lower bound']
    }


class F04CompletionTests(unittest.TestCase):
    def test_nonempty_source_required(self):
        with self.assertRaises(ValueError):
            Source('bad', ((1,),(-1,)), (0,-1), (0,))

    def test_scope_required(self):
        with self.assertRaises(ValueError):
            Source('', ((1,),), (1,), (0,))

    def test_dimensions_are_checked(self):
        with self.assertRaises(ValueError):
            Source('bad', ((1,0),), (1,), (0,))
        with self.assertRaises(ValueError):
            dot((1,2),(1,))

    def test_float_input_rejected(self):
        with self.assertRaises(TypeError):
            Source('bad', ((1,),), (1.0,), (0,))

    def test_unit_interval_linear_certificate(self):
        src=Source('unit', ((1,),(-1,)), (1,0), (0,))
        for v in range(-3,4):
            lam=(max(v,0),max(-v,0))
            b=max(v,0)
            self.assertEqual(src.check(scope='unit', query=(v,), weights=lam,bound=b),b)
            self.assertEqual(finite_upper(((0,),(1,)),(v,)),b)

    def test_negative_multiplier_rejected(self):
        src=reflective_source()
        with self.assertRaises(ValueError):
            src.check(scope=src.scope,query=(0,0,0),weights=(-1,0,0,0,0),bound=100)

    def test_changed_scope_rejected(self):
        src=reflective_source()
        with self.assertRaises(ValueError):
            src.check(scope='different evaluator',query=(0,0,0),weights=(0,)*5,bound=1)

    def test_wrong_query_and_bound_rejected(self):
        src=reflective_source()
        with self.assertRaises(ValueError):
            src.check(scope=src.scope,query=(1,1,1),weights=(0,)*5,bound=100)
        with self.assertRaises(ValueError):
            src.check(scope=src.scope,query=(-Q(1,4),Q(1,4),1),
                      weights=(0,Q(1,4),0,0,1),constant=Q(1,16),bound=-Q(1,16))

    def test_unbounded_free_query_has_no_supplied_certificate(self):
        src=Source('free', (), (), (0,))
        with self.assertRaises(ValueError):
            src.check(scope='free',query=(1,),weights=(),bound=100)
        self.assertEqual(src.check(scope='free',query=(0,),weights=(),constant=-1,bound=-1),-1)

    def test_coupled_stage_bound(self):
        joint,separate,common=composition_values(((0,),(1,)),((1,),(-1,)),(-Q(3,4),Q(1,4)))
        self.assertEqual((joint,separate,common),(-Q(1,2),Q(1,2),()))

    def test_common_maximizer_control(self):
        j,s,c=composition_values(((0,),(1,)),((1,),(1,)),(-Q(3,4),-Q(1,4)))
        self.assertEqual(j,s)
        self.assertEqual(c,(1,))

    def test_common_maximizer_equivalence_finite_grid(self):
        count=0
        for a,b,c,d in product(range(-2,3),repeat=4):
            j,s,shared=composition_values(((-1,),(0,),(1,)),((a,),(b,)),(c,d))
            self.assertLessEqual(j,s)
            self.assertEqual(j==s,bool(shared))
            count+=1
        self.assertEqual(count,625)

    def test_independent_sources_lose_cancellation(self):
        points=tuple(product((0,1),repeat=2))
        self.assertEqual(finite_upper(points,(1,-1),-Q(1,2)),Q(1,2))

    def test_nonnegative_unbounded_losses_keep_paired_bound(self):
        for theta,z in product((Q(0),Q(1,2),Q(1)),(Q(0),Q(10**50))):
            old=(2+z,2+z); new=(Q(5,4)+z+theta,Q(9,4)+z-theta)
            self.assertTrue(all(x>=0 for x in (*old,*new)))
            self.assertEqual(sum(new)-sum(old),-Q(1,2))

    def test_current_affine_values_and_new_evidence(self):
        K=((0,0),(1,0),(0,1))
        H=tuple((Q(i,8),Q(j,8)) for i in range(9) for j in range(9-i))
        for q in product(range(-2,3), repeat=2):
            self.assertEqual(finite_upper(K,q),finite_upper(H,q))
        self.assertEqual(finite_upper(tuple(p for p in K if p[0]==p[1]),(1,1)),0)
        self.assertEqual(finite_upper(tuple(p for p in H if p[0]==p[1]),(1,1)),1)

    def test_no_empty_evidence_authorization(self):
        with self.assertRaises(ValueError): finite_upper((),(1,))
        with self.assertRaises(ValueError): report_floor(())

    def test_single_residual_loses_strict_margin(self):
        self.assertEqual(relu(-Q(1,2)),relu(0))
        self.assertNotEqual(relu(-Q(1,2)+Q(1,4)),relu(Q(1,4)))

    def test_chord_exact_knots_and_sharp_midpoints(self):
        for k in range(1,9):
            for j in range(k+1):
                t=Q(j,k); self.assertEqual(chord(k,t),t*t)
            for j in range(k):
                t=Q(2*j+1,2*k)
                self.assertEqual(chord(k,t)-t*t,Q(1,4*k*k))

    def test_chord_enclosures_on_finite_grid(self):
        for k in range(1,9):
            for j in range(81):
                t=Q(j,80); e=chord(k,t)-t*t
                self.assertGreaterEqual(e,0); self.assertLessEqual(e,Q(1,4*k*k))

    def test_chord_domain_is_explicit(self):
        for k,t in ((0,Q(1,2)),(2,-Q(1,4)),(2,Q(5,4))):
            with self.assertRaises(ValueError): chord(k,t)

    def test_restricted_decision_matches_exact_despite_approximation(self):
        pts=tuple(Q(i,16) for i in range(4,13))
        self.assertEqual(max(t*t-t for t in pts),-Q(3,16))
        self.assertEqual(max(chord(4,t)-t for t in pts),-Q(3,16))
        self.assertEqual(max(chord(2,t)-t for t in pts),-Q(1,8))

    def test_quadratic_midpoint_obstruction(self):
        a,b=Q(1,4),Q(3,4); m=(a+b)/2
        self.assertEqual((a*a+b*b)/2-m*m,(b-a)**2/4)
        self.assertGreater((b-a)**2/4,0)

    def test_query_dependent_coefficients_vs_value(self):
        for eta,v in product((Q(0),Q(1,3),Q(1)), repeat=2):
            src=Source('varying query',((1,),(-1,)),(eta,0),(0,))
            value=src.check(scope=src.scope,query=(v,),weights=(v,0),bound=v*eta)
            self.assertEqual(value,v*eta)

    def test_reflective_floor_and_degenerate_corner(self):
        self.assertEqual(report_floor(((Q(1,2),0),(Q(3,4),Q(1,4)))),Q(1,2))
        self.assertEqual(report_floor(((0,1),)),0)
        self.assertEqual(report_floor(((1,1),)),1)
        for r in (0,Q(1,3),1): self.assertEqual(failure(0,1,r),r)

    def test_common_report_certificates_are_tight(self):
        src=reflective_source()
        for r in (Q(0),Q(49,100),Q(1,2),Q(3,4),Q(1)):
            self.assertEqual(report_bound(src,r),failure(Q(3,4),Q(1,4),r)-r)
        self.assertGreater(report_bound(src,Q(49,100)),0)
        self.assertEqual(report_bound(src,Q(1,2)),0)
        self.assertEqual(report_bound(src,Q(3,4)),-Q(3,8))

    def test_reflective_risk_and_proxy_change(self):
        for t in (Q(0),Q(1,2),Q(1)):
            p,s=Q(1,2)+t/4,t/4
            old=failure(p,s,Q(1,2))+Q(1,4)*Q(1,2)
            new=failure(p,s,Q(3,4))+Q(1,4)*Q(3,4)
            self.assertEqual(new-old,-Q(1,16))
            self.assertTrue(Q(1,8)<=failure(p,s,Q(3,4))<=Q(3,8))

    def test_intended_change_attains_certificate(self):
        src=reflective_source(); v=(-Q(1,4),Q(1,4),1)
        self.assertEqual(intended_change_bound(src),-Q(1,32))
        self.assertEqual(Q(1,16)+dot(v,src.witness),intended_change_bound(src))

    def test_selective_revision_boundary(self):
        count=0
        for delta,epsilon in product((Q(i,16) for i in range(9)),(Q(j,128) for j in range(5))):
            src=reflective_source(delta,epsilon)
            b=intended_change_bound(src)
            self.assertEqual(b,-Q(1,32)+delta/4+epsilon)
            self.assertEqual(b<=0,delta/4+epsilon<=Q(1,32))
            self.assertEqual(b,Q(1,16)+dot((-Q(1,4),Q(1,4),1),src.witness))
            self.assertEqual(report_bound(src,Q(1,2)),0)
            count+=1
        self.assertEqual(count,45)

    def test_revision_scope_cannot_be_silently_exceeded(self):
        for d,e in ((-Q(1,4),0),(Q(3,4),0),(0,-Q(1,4))):
            with self.assertRaises(ValueError): reflective_source(d,e)

    def test_missing_alignment_permits_reversal(self):
        self.assertEqual(-Q(1,16)+Q(1,8),Q(1,16))
        self.assertGreater(-Q(1,16)+Q(1,8),0)

    def test_available_policy_not_casewise_witness(self):
        f1,f2={Q(0)},{Q(1)}
        self.assertTrue(f1 and f2); self.assertFalse(f1&f2)
        reports={Q(0),Q(1,2),Q(3,4),Q(1)}
        self.assertTrue({r for r in reports if r>=Q(1,2)} &
                        {r for r in reports if r>=Q(3,4)})


    def test_exact_reflection_threshold_is_discontinuous(self):
        self.assertEqual(slack_floor(0,1,0),0)
        for k in (2,10,10**20):
            self.assertEqual(slack_floor(Q(1,k),1,0),1)

    def test_slack_floor_validity_and_ceiling(self):
        for p,s,xi in product((Q(i,8) for i in range(9)),
                              (Q(i,8) for i in range(9)),
                              (Q(1,8),Q(1,4),Q(1,2),Q(1))):
            r=slack_floor(p,s,xi)
            self.assertGreaterEqual(r,0); self.assertLessEqual(r,1-xi)
            self.assertLessEqual(failure(p,s,r),r+xi)
            if r>0: self.assertEqual(failure(p,s,r),r+xi)

    def test_slack_lipschitz_bound_finite_pairs(self):
        pts=tuple(product((Q(i,4) for i in range(5)), repeat=2))
        for x,y,xi in product(pts,pts,(Q(1,8),Q(1,4),Q(1,2))):
            distance=max(abs(a-b) for a,b in zip(x,y))
            self.assertLessEqual(abs(slack_floor(*x,xi)-slack_floor(*y,xi)),distance/xi)

    def test_slack_conditioning_limit(self):
        xi=Q(1,4)
        for eps in (Q(1,100),Q(1,1000),Q(1,10000)):
            rate=(slack_floor(xi+eps,1,xi)-slack_floor(xi,1,xi))/eps
            self.assertEqual(rate,1/(xi+eps))
            self.assertLess(rate,1/xi)

    def test_rounding_factor_two_is_attained(self):
        xi,eps=Q(1,4),Q(1,16)
        r=slack_floor(1,0,xi); rounded=r-eps
        self.assertEqual(r,Q(3,8))
        self.assertEqual(failure(1,0,rounded)-rounded,xi+2*eps)

    def test_source_approximation_bound_for_fixed_policy(self):
        for r in (0,Q(1,3),Q(3,4),1):
            delta=Q(1,4)
            self.assertEqual(failure(Q(1,2),Q(1,2),r)-failure(Q(1,4),Q(1,4),r),delta)

    def test_slack_does_not_change_controller_argument(self):
        xi=Q(1,4); r=slack_floor(Q(3,4),Q(1,4),xi)
        self.assertEqual(r,Q(1,3))
        self.assertNotEqual(failure(Q(3,4),Q(1,4),r),failure(Q(3,4),Q(1,4),r+xi))
        self.assertEqual(failure(Q(3,4),Q(1,4),r),r+xi)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(F04CompletionTests))
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    sys.exit(main())
