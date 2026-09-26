"""Exact finite source-transport and certificate-lift fixtures for F04 S5.

These checks validate supplied rational witnesses. They do not search all linear
programs, enumerate general neural activation regions, or certify empirical
source assumptions. No third-party dependencies and no floating-point inputs.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import json
from pathlib import Path
import unittest

Vector = tuple[F, ...]
Matrix = tuple[Vector, ...]


def rational(x: int | F) -> F:
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError('Use finite exact int/Fraction inputs, not floats or booleans.')
    return F(x)


def vector(xs) -> Vector:
    return tuple(rational(x) for x in xs)


def matrix(rows) -> Matrix:
    return tuple(vector(row) for row in rows)


def dot(x, y) -> F:
    if len(x) != len(y):
        raise ValueError('Dot-product dimensions disagree.')
    return sum((rational(a) * rational(b) for a, b in zip(x, y)), F(0))


def mv(a, x) -> Vector:
    return tuple(dot(row, x) for row in a)


def tv(a, y, width: int) -> Vector:
    if len(a) != len(y) or any(len(row) != width for row in a):
        raise ValueError('Transpose-product dimensions disagree.')
    return tuple(sum((rational(row[j]) * rational(t) for row, t in zip(a, y)), F(0))
                 for j in range(width))


def mm(a, b) -> Matrix:
    if not b or any(len(row) != len(b[0]) for row in b):
        raise ValueError('Nonempty rectangular right matrix required.')
    return tuple(tv(b, row, len(b[0])) for row in a)


def positive(xs) -> bool:
    return all(x >= 0 for x in xs)


@dataclass(frozen=True)
class Context:
    """Ag <= eta0+Bz, Dz <= d, with a fixed queried vector v."""
    A: Matrix
    B: Matrix
    eta0: Vector
    D: Matrix
    d: Vector
    v: Vector
    scope: str = 'fixed-source-v1'

    def __post_init__(self):
        for name in ('A', 'B', 'D'):
            object.__setattr__(self, name, matrix(getattr(self, name)))
        for name in ('eta0', 'd', 'v'):
            object.__setattr__(self, name, vector(getattr(self, name)))
        if not self.A or not self.v or not self.B or not self.B[0]:
            raise ValueError('Positive source, target and input dimensions required.')
        m, n, k = len(self.A), len(self.v), len(self.B[0])
        if (len(self.B) != m or len(self.eta0) != m or
            any(len(row) != n for row in self.A) or
            any(len(row) != k for row in self.B) or
            any(len(row) != k for row in self.D) or len(self.D) != len(self.d)):
            raise ValueError('Malformed source/chart/domain dimensions.')
        if not isinstance(self.scope, str) or not self.scope:
            raise ValueError('A nonempty declared scope is required.')

    @property
    def input_dim(self):
        return len(self.B[0])

    def feasible(self, g, z) -> bool:
        g, z = vector(g), vector(z)
        if len(g) != len(self.v) or len(z) != self.input_dim:
            raise ValueError('Feasibility witness has the wrong dimensions.')
        eta = tuple(a + b for a, b in zip(self.eta0, mv(self.B, z)))
        return (all(a <= b for a, b in zip(mv(self.A, g), eta)) and
                all(a <= b for a, b in zip(mv(self.D, z), self.d)))


def check_lift(ctx: Context, lam, nu, alpha, c, feasible_g, feasible_z,
               *, scope='fixed-source-v1') -> F:
    """Return the nonnegative proof margin; reject invalid/unspecified evidence.

    The feasible pair guards against a vacuous empty context. Its validity does
    not establish that the actual physical target satisfies the source rows.
    """
    lam, nu, alpha, c = vector(lam), vector(nu), vector(alpha), rational(c)
    if scope != ctx.scope:
        raise ValueError('Certificate scope does not match the current context.')
    if not ctx.feasible(feasible_g, feasible_z):
        raise ValueError('A valid nonempty-source witness is required.')
    if len(alpha) != ctx.input_dim or len(lam) != len(ctx.A) or len(nu) != len(ctx.D):
        raise ValueError('Certificate dimensions disagree.')
    if not positive(lam) or not positive(nu):
        raise ValueError('Source and domain multipliers must be nonnegative.')
    if tv(ctx.A, lam, len(ctx.v)) != ctx.v:
        raise ValueError('Target query identity fails.')
    source_slope = tv(ctx.B, lam, ctx.input_dim)
    domain_slope = tv(ctx.D, nu, ctx.input_dim)
    if tuple(a - b for a, b in zip(source_slope, domain_slope)) != alpha:
        raise ValueError('Input coefficient identity fails.')
    margin = c - dot(ctx.eta0, lam) - dot(ctx.d, nu)
    if margin < 0:
        raise ValueError('Intercept budget fails.')
    return margin


def pullback_certificate(A, eta, R, mu, v, *, independent_upper_bounds=True):
    """Check R^T mu as an original certificate; return weights and bound.

    With independent_upper_bounds=False, signs of R/mu are not restricted:
    membership in the pulled-back dual cone R^T mu>=0 is checked instead.
    This validates the pulled-back proof, not arbitrary transformed premises.
    """
    A, R, eta, mu, v = matrix(A), matrix(R), vector(eta), vector(mu), vector(v)
    if not A or len(eta) != len(A) or any(len(row) != len(v) for row in A):
        raise ValueError('Malformed source dimensions.')
    if not R or len(mu) != len(R) or any(len(row) != len(A) for row in R):
        raise ValueError('Malformed transport dimensions.')
    if independent_upper_bounds and (not positive(mu) or any(not positive(r) for r in R)):
        raise ValueError('Independent upper-bound aggregation requires nonnegative entries.')
    lam = tv(R, mu, len(A))
    if not positive(lam) or tv(A, lam, len(v)) != v:
        raise ValueError('Transported query/dual-cone condition fails.')
    return lam, dot(eta, lam)


def pure_copy_rows(R) -> bool:
    R = matrix(R)
    if not R or not R[0] or any(len(r) != len(R[0]) or not positive(r) for r in R):
        raise ValueError('A nonnegative rectangular matrix is required.')
    return all(any(row[i] > 0 and all(row[j] == 0 for j in range(len(row)) if j != i)
                   for row in R) for i in range(len(R[0])))


def alternate_lift(lam, direction, A, B):
    """Produce a distinct feasible coefficient from a supplied direction (11)."""
    lam, direction, A, B = vector(lam), vector(direction), matrix(A), matrix(B)
    if len(lam) != len(direction) or len(A) != len(lam) or len(B) != len(lam):
        raise ValueError('Mismatched direction dimensions.')
    if not positive(lam) or not any(direction):
        raise ValueError('A nonzero direction and nonnegative starting coefficient are needed.')
    if any(d < 0 for l, d in zip(lam, direction) if l == 0):
        raise ValueError('Direction leaves a zero nonnegative coordinate.')
    if any(tv(A, direction, len(A[0]))) or any(tv(B, direction, len(B[0]))):
        raise ValueError('Direction does not preserve the two coefficient identities.')
    limits = [l / (-2*d) for l, d in zip(lam, direction) if d < 0]
    step = min([F(1)] + limits)
    return tuple(l + step*d for l, d in zip(lam, direction)), step


def portfolio_derivative(portfolio, eta, direction):
    rows, eta, direction = matrix(portfolio), vector(eta), vector(direction)
    if not rows:
        raise ValueError('The finite portfolio must be nonempty.')
    scores = [dot(row, eta) for row in rows]
    best = min(scores)
    return min(dot(row, direction) for row, score in zip(rows, scores) if score == best)


def residual_support(residual, center, unbounded, bounded):
    """Exact support of center+N*t+C*e (free t, |e|<=1); None means +infinity."""
    r, center, N, C = vector(residual), vector(center), matrix(unbounded), matrix(bounded)
    if not r or len(center) != len(r) or len(N) != len(r) or len(C) != len(r):
        raise ValueError('Enclosure dimensions disagree.')
    if any(len(row) != len(N[0]) for row in N) or any(len(row) != len(C[0]) for row in C):
        raise ValueError('Enclosure matrices must be rectangular.')
    if any(tv(N, r, len(N[0]))):
        return None
    return dot(r, center) + sum(map(abs, tv(C, r, len(C[0]))), F(0))


def relu(x):
    return max(F(0), rational(x))


def scalar_context(D=(), d=()):
    return Context(((1,),), ((1,),), (0,), D, d, (1,))


class SourceTransportTests(unittest.TestCase):
    def test_aggregate_sum_exact(self):
        self.assertEqual(pullback_certificate(((1,0),(0,1)), (1,2), ((1,1),), (1,), (1,1)),
                         ((F(1),F(1)), F(3)))

    def test_aggregate_loses_coordinate_query(self):
        with self.assertRaises(ValueError):
            pullback_certificate(((1,0),(0,1)), (1,2), ((1,1),), (1,), (1,0))
        for t in (4,10,10**30):
            self.assertEqual(t+(3-t), 3)
            self.assertGreater(t,1)

    def test_invertible_numbers_not_upper_bound_equivalence(self):
        R=((1,1),(0,1)); self.assertEqual(mv(R,(1,2)),(3,2))
        self.assertEqual(mv(R,(4,-1)),(3,-1))
        self.assertFalse(pure_copy_rows(R))

    def test_negative_aggregate_rejected(self):
        with self.assertRaises(ValueError):
            pullback_certificate(((1,),), (1,), ((-1,),), (-1,), (1,))

    def test_dual_cone_recovers_invertible_transform(self):
        self.assertEqual(pullback_certificate(((1,0),(0,1)), (1,2), ((1,1),(0,1)),
                                             (1,-1),(1,0),independent_upper_bounds=False),
                         ((F(1),F(0)),F(1)))

    def test_rectangular_pure_copy_characterization(self):
        self.assertTrue(pure_copy_rows(((0,3),(2,0),(1,1))))
        self.assertFalse(pure_copy_rows(((1,1),(2,1),(0,3))))
        self.assertTrue(positive(mv(((1,1),(2,1),(0,3)),(-1,3))))

    def test_correlated_chart_lift_not_ambient_gradient(self):
        ctx=Context(((1,),(1,)),((1,),(1,)),(0,0),(),(),(1,))
        self.assertEqual(check_lift(ctx,(1,0),(),(1,),0,(0,),(0,)),0)
        self.assertEqual(check_lift(ctx,(0,1),(),(1,),0,(0,),(0,)),0)
        with self.assertRaises(ValueError):
            check_lift(ctx,(2,-1),(),(1,),0,(0,),(0,))
        self.assertLess(2*0-1,0)  # off-manifold target g=0 remains feasible

    def test_negative_intercept_valid_with_cell(self):
        self.assertEqual(check_lift(scalar_context(((-1,),),(-1,)), (1,),(1,),(2,),-1,(1,),(1,)),0)

    def test_constant_upper_bound_on_bounded_cell(self):
        self.assertEqual(check_lift(scalar_context(((1,),),(1,)), (1,),(1,),(0,),1,(0,),(0,)),0)

    def test_domain_multiplier_sign_tamper(self):
        with self.assertRaises(ValueError):
            check_lift(scalar_context(((-1,),),(-1,)), (1,),(-1,),(2,),-1,(1,),(1,))

    def test_intercept_budget_tamper(self):
        with self.assertRaises(ValueError):
            check_lift(scalar_context(((-1,),),(-1,)), (1,),(1,),(2,),-2,(1,),(1,))

    def test_scope_and_query_tamper(self):
        with self.assertRaises(ValueError):
            check_lift(scalar_context(),(1,),(),(1,),0,(0,),(0,),scope='different-task')
        with self.assertRaises(ValueError):
            check_lift(scalar_context(),(0,),(),(0,),0,(0,),(0,))

    def test_nonempty_guard(self):
        ctx=Context(((0,),),((0,),),(-1,),(),(),(0,))
        with self.assertRaises(ValueError):
            check_lift(ctx,(0,),(),(0,),0,(0,),(0,))

    def test_input_coordinate_reversal(self):
        ctx=Context(((1,),),((-1,),),(0,),(),(),(1,))
        self.assertEqual(check_lift(ctx,(1,),(),(-1,),0,(0,),(0,)),0)

    def test_input_translation_and_scaling(self):
        # z'=2z+3 transforms g<=z, z>=1 and F=2z-1.
        ctx=Context(((1,),),((F(1,2),),),(-F(3,2),),((-F(1,2),),),(-F(5,2),),(1,))
        self.assertEqual(check_lift(ctx,(1,),(1,),(1,),-4,(1,),(5,)),0)

    def test_good_network_all_regions(self):
        check_lift(scalar_context(((1,),),(1,)),(1,),(0,),(1,),0,(0,),(0,))
        check_lift(scalar_context(((-1,),),(-1,)),(1,),(1,),(2,),-1,(1,),(1,))
        for n in range(-24,25):
            z=F(n,4)
            for gap in (F(0),F(1,3),F(10)):
                self.assertGreaterEqual(z+relu(z-1),z-gap)

    def test_bad_network_countermodel(self):
        with self.assertRaises(ValueError):
            check_lift(scalar_context(((-1,),),(-1,)),(1,),(0,),(0,),1,(2,),(2,))
        self.assertLess(F(2)-relu(F(2)-1),F(2))

    def test_negative_gradient_sound_network(self):
        ctx=Context(((1,),(1,)),((1,0),(0,1)),(0,0),((1,-1),(-1,1)),(2,-1),(1,))
        self.assertEqual(check_lift(ctx,(0,1),(1,0),(-1,2),2,(0,),(F(3,2),0)),0)
        for i in range(-12,13):
            t=F(i,4)
            tri=relu(t)-2*relu(t-1)+relu(t-2)
            self.assertEqual(tri,relu(1-abs(t-1)))
            self.assertGreaterEqual(tri,min(t,0))

    def test_affine_context_exhaustive_certificate_evaluation(self):
        count=0
        for a in (-2,0,3):
            for nu in (F(0),F(1,2),F(2)):
                ctx=Context(((1,),),((1,),),(a,),((-1,),),(-1,),(1,))
                alpha=(1+nu,); c=F(a)-nu
                check_lift(ctx,(1,),(nu,),alpha,c,(a+1,),(1,))
                for z in (F(1),F(3,2),F(5),F(10**20)):
                    for gap in (F(0),F(1),F(9)):
                        g=a+z-gap
                        self.assertTrue(ctx.feasible((g,),(z,)))
                        self.assertLessEqual(g,dot(alpha,(z,))+c); count+=1
        self.assertEqual(count,108)

    def test_lift_family_nonunique(self):
        alt,step=alternate_lift((F(1,2),F(1,2)),(1,-1),((1,),(1,)),((1,),(1,)))
        self.assertNotEqual(alt,(F(1,2),F(1,2)))
        self.assertEqual(sum(alt),1);self.assertTrue(positive(alt));self.assertGreater(step,0)

    def test_boundary_rank_deficiency_not_ambiguity(self):
        for sign in (-1,1):
            with self.assertRaises(ValueError):
                alternate_lift((1,0,0),(0,sign,-sign),((1,),(1,),(1,)),((1,),(0,),(0,)))

    def test_independent_intervention_separates(self):
        a,b=(F(1),F(0)),(F(0),F(1))
        self.assertEqual(dot(a,(1,1)),dot(b,(1,1)))
        self.assertNotEqual(dot(a,(1,0)),dot(b,(1,0)))

    def test_nearly_parallel_probe_precision(self):
        eps,rho=F(1,100),F(1,1000)
        self.assertEqual(rho/eps,F(1,10))
        for t in (F(0),F(1,3),F(1)):
            self.assertEqual(dot((1-t,t),(1,1+eps)),1+eps*t)

    def test_invisible_null_proof_weight(self):
        for t in (0,1,100,10**30):
            lam=(1+t,t)
            self.assertEqual(tv(((1,),(-1,)),lam,1),(1,))
            self.assertEqual(dot(lam,(7,-7)),7)
            rho=F(1,10)
            self.assertEqual(dot(lam,(7+rho,-7+rho)),7+rho+2*t*rho)

    def test_distinct_directional_derivatives_not_one_proof(self):
        P=((1,0),(0,1));eta=(0,0)
        self.assertEqual(portfolio_derivative(P,eta,(1,0)),0)
        self.assertEqual(portfolio_derivative(P,eta,(0,1)),0)
        self.assertEqual(portfolio_derivative(P,eta,(1,1)),1)

    def test_coherent_cell_after_weakening(self):
        P=((1,0),(0,1));eps=F(1,100);eta=(eps,2*eps)
        self.assertEqual(portfolio_derivative(P,eta,(1,0)),1)
        self.assertEqual(portfolio_derivative(P,eta,(0,1)),0)

    def test_positive_slack_direction_recovery(self):
        P=((1,0),(0,1),(F(1,2),F(1,2)));eta=(1,1);s=(1,1);k=1
        for a in range(-3,4):
            for b in range(-3,4):
                w=(a,b);t=max(0,-a,-b);u=(a+t,b+t)
                self.assertTrue(positive(u))
                self.assertEqual(portfolio_derivative(P,eta,w),portfolio_derivative(P,eta,u)-t*k)

    def test_residual_cancels_joint_unbounded_direction(self):
        e=F(1,100)
        self.assertEqual(residual_support((e,-e),(0,0),((1,),(1,)),((1,),(0,))),e)
        self.assertIsNone(residual_support((0,e),(0,0),((1,),(1,)),((1,),(0,))))

    def test_chart_slope_error_no_global_additive_bound(self):
        eps=F(1,100);z=-10**8;g=z
        self.assertGreater(g,(1+eps)*z+100)

    def test_same_controller_original_improvement(self):
        r0,r1=F(3,4),F(19,20);a,b=F(0),F(1,2)
        H=lambda r:a*r+b*(1-r)
        self.assertLessEqual(H(r0),r0);self.assertLessEqual(H(r1),r1)
        self.assertEqual(5*(H(r1)-H(r0)),-F(1,2))

    def test_same_controller_relaxation_sharp(self):
        a,b=F(11,14),F(9,14);r0,r1=F(3,4),F(19,20)
        self.assertEqual(a-2*b,-F(1,2));self.assertEqual(3*a+b,3)
        self.assertLessEqual(19*a+b,19)
        self.assertEqual(F(4,7)*(-F(1,2))+F(1,7)*3,F(1,7))
        self.assertEqual(5*((a*r1+b*(1-r1))-(a*r0+b*(1-r0))),F(1,7))
        self.assertGreater(a-b,-F(1,2))

    def test_loss_fixed_query_warning(self):
        self.assertLessEqual(F(1,2)*(-10),F(1,2))
        self.assertGreater((-F(1,2))*(-10),-F(1,2))

    def test_feedback_solution_and_iteration_differ(self):
        for beta in (F(0),F(1,2),F(1),F(2)):
            z=beta/(1+beta)
            self.assertEqual(z,beta*(1-relu(z)))
        z=F(0);seen=[]
        for _ in range(6):
            seen.append(z);z=1-relu(z)
        self.assertEqual(seen,[0,1,0,1,0,1])

    def test_no_strict_source_hull_not_identified(self):
        for a in range(-5,6):
            for b in range(-5,6):
                if a+b>=0:
                    self.assertEqual(min(a,2*a+b),a)
        self.assertEqual(dot((1,0),(0,0)),dot((2,1),(0,0)))

    def test_offsets_break_weakening_hull_recovery(self):
        for a in range(6):
            for b in range(6):
                eta=(1+a,1+b)
                self.assertEqual(eta[0]+2,min(eta[0]+2,2*eta[0]+eta[1]))
        eta=(F(1,2),F(1,2))
        self.assertEqual(eta[0]+2,F(5,2))
        self.assertEqual(min(eta[0]+2,2*eta[0]+eta[1]),F(3,2))

    def test_malformed_shapes_and_numeric_types(self):
        with self.assertRaises(ValueError):
            Context(((1,2),),((1,),),(0,),(),(),(1,))
        with self.assertRaises(ValueError):dot((1,2),(1,))
        with self.assertRaises(TypeError):rational(0.1)
        with self.assertRaises(TypeError):rational(True)


def report():
    return {
        'scope':'F04 S5 finite supplied-witness fixtures; no trained network or general proof search',
        'arithmetic':'exact Fraction; None denotes an unbounded residual correction',
        'lift':{'negative_intercept':'lambda=1, nu=1, g<=z, z>=1, F=2z-1',
                'source_chart_example':'eta=(z,z); ambient gradient (2,-1), valid lifts (1,0) and (0,1)'},
        'aggregate':{'sum_query_bound':'3','lost_coordinate':'unbounded in aggregated source'},
        'controller':{'old_report':'3/4','new_report':'19/20','original_bound':'-1/2',
                      'relaxed_sharp_bound':'1/7','relaxation_witness':['11/14','9/14'],
                      'proof_weights':['4/7','1/7']},
        'residual':{'joint_cancelling':'1/100','unmatched_direction':None},
        'finite_enumerations':{'affine_context_evaluations':108,'weakening_direction_cases':49,
                              'good_network_source_pairs':147,'triangle_inputs':25},
        'analytical_claims':'General alternatives, uniqueness, order and hull claims rely on the derivation note, not these finite tests.'
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SourceTransportTests))
    if not result.wasSuccessful():return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
