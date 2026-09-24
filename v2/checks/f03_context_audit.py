"""Finite F03 context/convexity fixtures and exact rational log certificates.

This is not an RLL prover. The enclosure formula is justified in
v2/literature/01e_belief_value_import_contracts.md. Decisive certificates use
Fraction arithmetic; separately named numerical-reference tests use binary64.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json
import math
from pathlib import Path
from typing import Iterable, Sequence
import unittest


def rational(x: int | Q) -> Q:
    """Reject floats rather than silently treating rounded inputs as exact data."""
    if isinstance(x, bool) or not isinstance(x, (int, Q)):
        raise TypeError('Expected an int or Fraction, not a rounded float.')
    return Q(x)


@dataclass(frozen=True)
class Bounds:
    lower: Q
    upper: Q

    def __post_init__(self) -> None:
        object.__setattr__(self, 'lower', rational(self.lower))
        object.__setattr__(self, 'upper', rational(self.upper))
        if self.lower > self.upper:
            raise ValueError('Reversed enclosure.')

    def scale(self, weight: int | Q) -> Bounds:
        w = rational(weight)
        a, b = w * self.lower, w * self.upper
        return Bounds(min(a, b), max(a, b))

    def __add__(self, other: Bounds) -> Bounds:
        return Bounds(self.lower + other.lower, self.upper + other.upper)

    def __sub__(self, other: Bounds) -> Bounds:
        return self + other.scale(-1)

    def data(self) -> dict[str, str]:
        return {'lower': str(self.lower), 'upper': str(self.upper)}


def log_bounds(r: int | Q, n: int = 6) -> Bounds:
    """Enclose natural log(r); n is the last series index, starting from zero."""
    r = rational(r)
    if r <= 0:
        raise ValueError('The logarithm ratio must be strictly positive.')
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError('The last series index must be a nonnegative integer.')
    z = (r - 1) / (r + 1)
    partial = 2 * sum((z ** (2*k + 1) / (2*k + 1) for k in range(n + 1)), Q(0))
    tail = 2 * abs(z) ** (2*n + 3) / ((2*n + 3) * (1 - z*z))
    return Bounds(partial, partial + tail) if z >= 0 else Bounds(partial - tail, partial)


def distribution(values: Sequence[int | Q]) -> tuple[Q, ...]:
    p = tuple(rational(v) for v in values)
    if not p or any(v < 0 for v in p) or sum(p) != 1:
        raise ValueError('Expected a nonempty normalized nonnegative distribution.')
    return p


def kl_bounds(q: Sequence[int | Q], p: Sequence[int | Q], n: int = 6) -> Bounds | None:
    """None denotes +infinity caused by a positive-q/zero-p support mismatch."""
    q, p = distribution(q), distribution(p)
    if len(q) != len(p):
        raise ValueError('Distribution dimensions differ.')
    # Validate n even in the zero/support-mismatch cases.
    log_bounds(1, n)
    out = Bounds(Q(0), Q(0))
    for qi, pi in zip(q, p):
        if not qi:
            continue
        if not pi:
            return None
        out = out + log_bounds(qi/pi, n).scale(qi)
    # KL >= 0 is a separately proved inequality; individual log ratios may be negative.
    return Bounds(max(Q(0), out.lower), out.upper)


def budget_status(q: Sequence[int | Q], p: Sequence[int | Q], b: int | Q,
                  n: int = 6) -> str:
    b = rational(b)
    bound = kl_bounds(q, p, n)
    if bound is None or bound.lower > b:
        return 'refuted'
    if bound.upper <= b:
        return 'guaranteed'
    return 'unresolved'


def product_law(a: int | Q, b: int | Q) -> tuple[Q, ...]:
    a, b = rational(a), rational(b)
    if not 0 <= a <= 1 or not 0 <= b <= 1:
        raise ValueError('Binary probabilities must be in [0,1].')
    return ((1-a)*(1-b), (1-a)*b, a*(1-b), a*b)


def independent(q: Sequence[int | Q]) -> bool:
    p = distribution(q)
    if len(p) != 4:
        raise ValueError('Expected the four binary-pair outcomes.')
    return p[0]*p[3] == p[1]*p[2]


def fair(q: Sequence[int | Q]) -> bool:
    p = distribution(q)
    if len(p) != 4:
        raise ValueError('Expected the four binary-pair outcomes.')
    return p[0]+p[1] == p[0]+p[2] == Q(1, 2)


def dot(q: Sequence[Q], f: Sequence[int | Q]) -> Q:
    if len(q) != len(f):
        raise ValueError('Dimensions differ.')
    return sum((qi*rational(fi) for qi, fi in zip(q, f)), Q(0))


def simplex4(denominator: int = 4) -> Iterable[tuple[Q, ...]]:
    if denominator < 1:
        raise ValueError('Positive denominator required.')
    for a in range(denominator + 1):
        for b in range(denominator - a + 1):
            for c in range(denominator - a - b + 1):
                yield tuple(Q(v, denominator) for v in (a, b, c, denominator-a-b-c))


def p_from_root_odds(a: int | Q) -> tuple[Q, Q]:
    a = rational(a)
    if a <= 0:
        raise ValueError('Positive root odds required.')
    return a*a/(1+a*a), 1/(1+a*a)


def pool_optimizer(a: int | Q) -> tuple[Q, Q]:
    a = rational(a)
    if a <= 0:
        raise ValueError('Positive root odds required.')
    return a/(1+a), 1/(1+a)


def pool_log_argument(a: int | Q) -> Q:
    a = rational(a)
    if a <= 0:
        raise ValueError('Positive root odds required.')
    return 2*(1+a*a)/((1+a)*(1+a))


def jensen_gap(n: int = 4) -> Bounds:
    return log_bounds(pool_log_argument(9), n) - log_bounds(pool_log_argument(81), n).scale(Q(1,2))


def kl_reference(q: Sequence[Q], p: Sequence[Q]) -> float:
    """Binary64 reference only; decisive certificates never use this function."""
    if any(qi > 0 and pi == 0 for qi, pi in zip(q, p)):
        return math.inf
    return math.fsum(float(qi)*math.log(float(qi/pi)) for qi, pi in zip(q,p) if qi)


def quadratic_transformer(f: Sequence[int | Q]) -> Q:
    """Exact positive control: B(q)=(q0-1/2)^2 on a binary simplex."""
    a, b = (rational(x) for x in f)
    x = max(Q(0), min(Q(1), Q(1,2)-(a-b)/2))
    return (x-Q(1,2))**2 + x*a + (1-x)*b


def results() -> dict:
    p = (Q(1,2), Q(1,2))
    q = (Q(1,4), Q(3,4))
    bound = kl_bounds(q,p,6)
    assert bound is not None
    return {
        'task': 'F03', 'session': '2026-09-24-S5',
        'kind': 'constructed development fixtures; not a whole-paper proof or a selected calculus',
        'arithmetic': 'Fraction certificates; binary64 used only by separately named reference tests',
        'context_collision': {
            'outcomes': ['00','01','10','11'], 'cost': [0,1,1,0],
            'prior_value_equality': 'for every finite cost vector: both min(cost); proved in note',
            'after_fair_marginals_independent': '1/2', 'after_fair_marginals_unrestricted': '0',
            'grid_simplex_denominator': 4, 'grid_laws': 35, 'grid_cost_vectors': 81,
        },
        'S16_objection': {
            'id': 'O-S16-01', 'source_version': 'arXiv:2604.17140v1',
            'claim': 'Proposition 1 parameter convexity is refuted as stated by this finite model',
            'gamma': 0, 'beta': [1,1], 'parameter_points': ['0','2*log(9)','4*log(9)'],
            'probabilities': [[str(v) for v in p_from_root_odds(a)] for a in [1,9,81]],
            'optimizers': [[str(v) for v in pool_optimizer(a)] for a in [1,9,81]],
            'minimum_log_arguments': [str(pool_log_argument(a)) for a in [1,9,81]],
            'integer_sign_certificate': {'left': 1681**2, 'right':625*3281,
                                         'strict_positive_difference':1681**2-625*3281},
            'jensen_gap_enclosure': jensen_gap(4).data(), 'gap_exceeds': '1/10',
            'repair': 'joint convexity, for example affine probability coordinates in this finite gamma=0 setting',
            'external_review': 'not author-confirmed; same-agent derivation and computational checks',
        },
        'fixed_kl_certificate': {'q':['1/4','3/4'], 'p':['1/2','1/2'], 'last_series_index':6,
                                 'bounds':bound.data(), 'budget':'1/5', 'status':budget_status(q,p,Q(1,5),6)},
        'finite_enumerations': {
            'log_ratio_grid': 'a/b for integers a,b in 1..8, n=0..5',
            'log_nested_grid': 'a/b for integers a,b in 1..8, consecutive n=0..5',
            'binary_kl_grid': 'q=k/8, p=j/8 for k,j=0..8',
            'pool_reference': 'a in {1,3,9,81}, q=k/10 for k=0..10',
            'convex_recovery_grid': 'q0=k/8 for k=0..8',
        },
    }


class F03ContextAuditTests(unittest.TestCase):
    def test_log_identity(self):
        self.assertEqual(log_bounds(1), Bounds(Q(0),Q(0)))

    def test_log_reciprocal(self):
        for a,b in product(range(1,9),repeat=2):
            self.assertEqual(log_bounds(Q(a,b),4),log_bounds(Q(b,a),4).scale(-1))

    def test_log_invalid_domain(self):
        for r in [0,-1,Q(-1,3)]:
            with self.assertRaises(ValueError): log_bounds(r)

    def test_log_invalid_index(self):
        for n in [-1,1.5,True]:
            with self.assertRaises(ValueError): log_bounds(2,n)

    def test_reject_rounded_input(self):
        for x in [1.0,True,'1/2']:
            with self.assertRaises(TypeError): log_bounds(x)

    def test_interval_invalid(self):
        with self.assertRaises(ValueError): Bounds(Q(2),Q(1))

    def test_interval_signed_arithmetic(self):
        a=Bounds(Q(-2),Q(3)); b=Bounds(Q(1),Q(4))
        self.assertEqual(a-b,Bounds(Q(-6),Q(2)))
        self.assertEqual(a.scale(-2),Bounds(Q(-6),Q(4)))

    def test_log_reference_grid_binary64(self):
        for a,b,n in product(range(1,9),range(1,9),range(6)):
            v=math.log(a/b); interval=log_bounds(Q(a,b),n)
            self.assertLessEqual(float(interval.lower),v+2e-14)
            self.assertGreaterEqual(float(interval.upper),v-2e-14)

    def test_log_exact_nested_intervals(self):
        for a,b,n in product(range(1,9),range(1,9),range(6)):
            old,new=log_bounds(Q(a,b),n),log_bounds(Q(a,b),n+1)
            self.assertLessEqual(old.lower,new.lower)
            self.assertLessEqual(new.upper,old.upper)

    def test_log_sign(self):
        self.assertGreater(log_bounds(2,0).lower,0)
        self.assertLess(log_bounds(Q(1,2),0).upper,0)

    def test_large_ratio_remains_finite(self):
        for r in [Q(10**6),Q(1,10**6)]:
            x=log_bounds(r,4)
            self.assertIsInstance(x.lower,Q)
            self.assertLess(x.lower,x.upper)

    def test_kl_equal_is_exact_zero(self):
        for k in range(9):
            q=(Q(k,8),1-Q(k,8))
            self.assertEqual(kl_bounds(q,q),Bounds(Q(0),Q(0)))

    def test_kl_support_mismatch(self):
        self.assertIsNone(kl_bounds((Q(1,2),Q(1,2)),(1,0)))
        self.assertEqual(budget_status((Q(1,2),Q(1,2)),(1,0),100),'refuted')

    def test_kl_zero_zero_skipped(self):
        self.assertEqual(kl_bounds((1,0),(1,0)),Bounds(Q(0),Q(0)))

    def test_kl_invalid_distribution(self):
        for p in [(),(Q(1,4),Q(1,4)),(-1,2)]:
            with self.assertRaises(ValueError): kl_bounds(p,p)
        with self.assertRaises(ValueError): kl_bounds((1,),(1,0))

    def test_kl_reference_grid_binary64(self):
        for a,b in product(range(9),repeat=2):
            q,p=(Q(a,8),1-Q(a,8)),(Q(b,8),1-Q(b,8))
            out=kl_bounds(q,p,6); v=kl_reference(q,p)
            if out is None: self.assertTrue(math.isinf(v))
            else:
                self.assertLessEqual(float(out.lower),v+2e-14)
                self.assertGreaterEqual(float(out.upper),v-2e-14)
                self.assertGreaterEqual(out.lower,0)

    def test_budget_guarantee(self):
        self.assertEqual(budget_status((Q(1,4),Q(3,4)),(Q(1,2),Q(1,2)),Q(1,5)),'guaranteed')

    def test_budget_refutation(self):
        self.assertEqual(budget_status((Q(1,4),Q(3,4)),(Q(1,2),Q(1,2)),Q(1,10)),'refuted')

    def test_budget_unresolved(self):
        q,p=(Q(1,4),Q(3,4)),(Q(1,2),Q(1,2))
        v=kl_bounds(q,p,0); assert v is not None
        self.assertEqual(budget_status(q,p,(v.lower+v.upper)/2,0),'unresolved')

    def test_product_vertices(self):
        for a,b in product([0,1],repeat=2): self.assertTrue(independent(product_law(a,b)))

    def test_diagonal_is_not_independent(self):
        self.assertFalse(independent((Q(1,2),0,0,Q(1,2))))
        self.assertTrue(fair((Q(1,2),0,0,Q(1,2))))

    def test_product_grid(self):
        for a,b in product(range(5),repeat=2):
            self.assertTrue(independent(product_law(Q(a,4),Q(b,4))))

    def test_current_value_collision_grid(self):
        laws=list(simplex4(4)); self.assertEqual(len(laws),35)
        for f in product([-2,0,3],repeat=4):
            unrestricted=min(dot(q,f) for q in laws)
            products=min(dot(q,f) for q in laws if independent(q))
            self.assertEqual(products,unrestricted)
            self.assertEqual(products,min(f))

    def test_after_same_context_values_differ(self):
        laws=list(simplex4(4)); f=(0,1,1,0)
        a=min(dot(q,f) for q in laws if fair(q) and independent(q))
        b=min(dot(q,f) for q in laws if fair(q))
        self.assertEqual((a,b),(Q(1,2),Q(0)))

    def test_fair_independent_law_unique_on_grid(self):
        self.assertEqual([q for q in simplex4(4) if fair(q) and independent(q)],[(Q(1,4),)*4])

    def test_all_fair_laws_parameterized(self):
        for q in simplex4(8):
            if fair(q):
                t=q[0]; self.assertEqual(q,(t,Q(1,2)-t,Q(1,2)-t,t))

    def test_convex_penalty_recovered_positive_control(self):
        for k in range(9):
            x=Q(k,8); f=(1-2*x,Q(0))
            self.assertEqual(quadratic_transformer(f)-dot((x,1-x),f),(x-Q(1,2))**2)

    def test_context_addition_associativity_on_finite_penalties(self):
        for b,h,k in product(range(3),repeat=3): self.assertEqual((b+h)+k,b+(h+k))
        # Hard constraints compose by intersection; no inference from an empty set.
        laws=set(simplex4(4)); i={q for q in laws if independent(q)}; h={q for q in laws if fair(q)}
        self.assertEqual((laws&i)&h,laws&(i&h))

    def test_source_witness_probabilities(self):
        self.assertEqual(p_from_root_odds(9),(Q(81,82),Q(1,82)))
        self.assertEqual(p_from_root_odds(81),(Q(6561,6562),Q(1,6562)))
        self.assertEqual(pool_optimizer(9),(Q(9,10),Q(1,10)))

    def test_source_witness_minimum_arguments(self):
        self.assertEqual([pool_log_argument(a) for a in [1,9,81]],[Q(1),Q(41,25),Q(3281,1681)])

    def test_source_witness_integer_jensen_violation(self):
        self.assertEqual(1681**2-625*3281,775136)
        self.assertGreater(Q(41,25)**2,Q(3281,1681))

    def test_source_witness_rational_gap_certificate(self):
        out=jensen_gap(4)
        self.assertGreater(out.lower,Q(1,10))
        self.assertLess(out.upper,Q(1,5))

    def test_source_witness_negative_curvature(self):
        self.assertLess(Q(81,6724)-Q(9,200),0)
        self.assertGreater(Q(1,4)-Q(1,8),0)

    def test_source_witness_logconcavity_condition(self):
        for a in [1,3,9,81]:
            p=p_from_root_odds(a)[0]
            self.assertLess(-p*(1-p),0)

    def test_source_witness_joint_hessian_indefinite(self):
        p,q=p_from_root_odds(9)[0],pool_optimizer(9)[0]
        self.assertLess(2*p*(1-p)/(q*(1-q))-1,0)

    def test_geometric_pool_identity_reference_binary64(self):
        r=(Q(1,2),Q(1,2))
        for a,k in product([1,3,9,81],range(11)):
            p,qstar=p_from_root_odds(a),pool_optimizer(a)
            q=(Q(k,10),1-Q(k,10))
            left=kl_reference(q,p)+kl_reference(q,r)
            right=2*kl_reference(q,qstar)+math.log(float(pool_log_argument(a)))
            self.assertAlmostEqual(left,right,places=12)

    def test_affine_probability_repair_hessian(self):
        # Equality of the Hessian form to an explicit square, without square roots.
        for x,y,u,v in product([Q(1,4),Q(1,2),Q(3,4)],repeat=4):
            h=u*u/x-2*u*v/y+x*v*v/(y*y)
            self.assertEqual(h,(u*y-x*v)**2/(x*y*y))
            self.assertGreaterEqual(h,0)

    def test_affine_probability_repair_reference_binary64(self):
        def value(t): return -2*math.log((math.sqrt(t)+math.sqrt(1-t))/math.sqrt(2))
        for a,b,w in product(range(1,8),range(1,8),range(5)):
            x,y,s=a/8,b/8,w/4
            self.assertLessEqual(value(s*x+(1-s)*y),s*value(x)+(1-s)*value(y)+1e-13)

    def test_source_metadata_records_scoped_objection(self):
        path=Path(__file__).resolve().parents[1]/'literature'/'F03_sources.json'
        sources=json.loads(path.read_text(encoding='utf-8'))['sources']
        self.assertEqual({s['id'] for s in sources},{f'S{i:02}' for i in range(1,19)})
        s16=next(s for s in sources if s['id']=='S16')
        self.assertIn('O-S16-01',json.dumps(s16))
        self.assertFalse(s16['whole_work_verified'])

    def test_report_decisive_certificate_is_exact(self):
        data=results(); cert=data['S16_objection']['jensen_gap_enclosure']
        self.assertGreater(Q(cert['lower']),Q(1,10))
        self.assertEqual(data['fixed_kl_certificate']['status'],'guaranteed')


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path,help='Write deterministic evidence only after tests pass.')
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F03ContextAuditTests))
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(results(),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
