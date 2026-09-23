"""Exact finite witnesses for the F03 Lawvere/value source adapters.

This module evaluates small expressions and checks arithmetic translations.
It is not an RLL/Abelian proof checker or a complete consequence procedure.
All exhaustive bounds are explicit in the tests and JSON report.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json
import math
from pathlib import Path
from typing import Mapping
import unittest


@dataclass(frozen=True)
class Pair:
    """Finite nonnegative coordinates representing their signed difference."""
    pos: Q
    neg: Q

    def __post_init__(self) -> None:
        for name in ('pos', 'neg'):
            raw = getattr(self, name)
            if not isinstance(raw, (int, Q)) or isinstance(raw, bool):
                raise TypeError('Pair coordinates must be finite exact rationals or integers')
            value = Q(raw)
            if value < 0:
                raise ValueError('Pair coordinates must be nonnegative')
            object.__setattr__(self, name, value)

    @classmethod
    def encode(cls, value: Q) -> Pair:
        value = Q(value)
        return cls(max(value, Q(0)), max(-value, Q(0)))

    def decode(self) -> Q:
        return self.pos - self.neg

    def plus(self, other: Pair) -> Pair:
        return Pair(self.pos + other.pos, self.neg + other.neg)

    def negative(self) -> Pair:
        return Pair(self.neg, self.pos)

    def times(self, other: Pair) -> Pair:
        return Pair(self.pos * other.pos + self.neg * other.neg,
                    self.pos * other.neg + self.neg * other.pos)

    def le(self, other: Pair) -> bool:
        return self.pos + other.neg <= other.pos + self.neg

    def shifted(self, amount: Q) -> Pair:
        if amount < 0:
            raise ValueError('Common representation shift must be nonnegative')
        return Pair(self.pos + amount, self.neg + amount)


def quotient_graph(x: Pair, y: Pair, z: Pair) -> bool:
    """The graph of a *defined* signed quotient; excludes zero denominator."""
    return y.pos != y.neg and (y.pos*z.pos + y.neg*z.neg + x.neg ==
                               y.pos*z.neg + y.neg*z.pos + x.pos)


# ASTs use tuples with tags v, c, add, neg, sub, mul, min, max, imp.
Expr = tuple
P, R, ZERO = ('v', 'p'), ('v', 'r'), ('c', Q(0))


def scalar_eval(t: Expr, env: Mapping[str, Q]) -> Q:
    """Ordinary finite signed arithmetic, not source RLL semantics."""
    op = t[0]
    if op == 'v':
        return Q(env[t[1]])
    if op == 'c':
        return Q(t[1])
    a = scalar_eval(t[1], env)
    if op == 'neg':
        return -a
    b = scalar_eval(t[2], env)
    if op == 'add':
        return a+b
    if op == 'sub':
        return a-b
    if op == 'mul':
        return a*b
    if op == 'min':
        return min(a, b)
    if op == 'max':
        return max(a, b)
    raise ValueError(f'Unsupported ordinary arithmetic operation: {op}')


def pair_eval(t: Expr, env: Mapping[str, Pair]) -> Pair:
    """Finite polynomial adapter; no subtraction of coordinates until decoding."""
    op = t[0]
    if op == 'v':
        return env[t[1]]
    if op == 'c':
        return Pair.encode(Q(t[1]))
    a = pair_eval(t[1], env)
    if op == 'neg':
        return a.negative()
    b = pair_eval(t[2], env)
    if op == 'add':
        return a.plus(b)
    if op == 'sub':
        return a.plus(b.negative())
    if op == 'mul':
        return a.times(b)
    raise ValueError('Polynomial adapter excludes this operation')


def cost_eval(t: Expr, env: Mapping[str, Q]) -> Q:
    """Finite zero-constant additive source semantics only."""
    op = t[0]
    if op == 'v':
        value = Q(env[t[1]])
        if value < 0:
            raise ValueError('Cost values must be nonnegative')
        return value
    if op == 'c':
        if t[1] != 0:
            raise ValueError('This fragment has only the zero constant')
        return Q(0)
    if op not in ('add', 'imp', 'min', 'max'):
        raise ValueError('Operation outside finite additive fragment')
    a, b = cost_eval(t[1], env), cost_eval(t[2], env)
    return {'add': lambda: a+b, 'imp': lambda: max(b-a, Q(0)),
            'min': lambda: min(a, b), 'max': lambda: max(a, b)}[op]()


def negative_cone(t: Expr) -> Expr:
    """Translate source syntax into the constant-zero real Abelian signature."""
    op = t[0]
    if op == 'v':
        return ('min', t, ZERO)
    if op == 'c':
        if t[1] != 0:
            raise ValueError('Do not silently add named constants to Abelian logic')
        return ZERO
    if op not in ('add', 'imp', 'min', 'max'):
        raise ValueError('No full-RLL embedding is implemented')
    a, b = negative_cone(t[1]), negative_cone(t[2])
    if op == 'imp':
        return ('min', ('sub', b, a), ZERO)
    return ({'add': 'add', 'min': 'max', 'max': 'min'}[op], a, b)


def shortfall(x: Q, y: Q) -> Q:
    """Loss when replacing signed value x by y."""
    return max(Q(x)-Q(y), Q(0))


def directed_loss(x: tuple[Q, ...], y: tuple[Q, ...]) -> Q:
    if not x or len(x) != len(y):
        raise ValueError('A common nonempty task index is required')
    return max(shortfall(a, b) for a, b in zip(x, y))


def residual(x, y):
    """Source residual y dot-minus x on a tiny exact-plus-infinity domain."""
    if x == math.inf:
        return Q(0)
    if y == math.inf:
        return math.inf
    return max(Q(y)-Q(x), Q(0))


def finite_guard(x):
    return residual(residual(x, math.inf), math.inf)


def expressions() -> list[Expr]:
    """39 explicitly generated terms, not all depth-two terms."""
    atoms = [P, R, ZERO]
    return atoms + [(op, a, b) for op in ('add', 'imp', 'min', 'max')
                    for a, b in product(atoms, repeat=2)]


class F03ValueBridgeTests(unittest.TestCase):
    def test_pair_arithmetic_on_all_small_coordinates(self):
        pairs = [Pair(a,b) for a,b in product(range(3), repeat=2)]
        for x,y in product(pairs, repeat=2):
            self.assertEqual(x.plus(y).decode(), x.decode()+y.decode())
            self.assertEqual(x.times(y).decode(), x.decode()*y.decode())
            self.assertEqual(x.le(y), x.decode() <= y.decode())
            self.assertEqual(x.negative().decode(), -x.decode())

    def test_noncanonical_pairs_preserve_comparison(self):
        for a,b,k,l in product(range(-2,3), range(-2,3), range(3), range(3)):
            x,y = Pair.encode(Q(a)).shifted(Q(k)), Pair.encode(Q(b)).shifted(Q(l))
            self.assertEqual(x.le(y), a <= b)

    def test_unbounded_finite_representatives(self):
        for value in (-(10**100), Q(-7,13), 0, Q(7,13), 10**100):
            self.assertEqual(Pair.encode(Q(value)).decode(), value)

    def test_invalid_coordinates_rejected(self):
        for bad in (-1, Q(-1,2)):
            with self.assertRaises(ValueError): Pair(bad, 0)
        for bad in (math.inf, -math.inf, math.nan, 0.5, True):
            with self.assertRaises(TypeError): Pair(bad, 0)

    def test_signed_polynomial_translation(self):
        terms = [P, R, ('c',Q(-3,2)), ('neg',P), ('add',P,R),
                 ('sub',P,R), ('mul',P,R), ('mul',('sub',P,R),('sub',P,R)),
                 ('add',('mul',P,P),('mul',R,R))]
        for a,b in product(range(-3,4), repeat=2):
            e = {'p':Q(a),'r':Q(b)}
            pairs = {k:Pair.encode(v).shifted(Q(3)) for k,v in e.items()}
            for t in terms:
                self.assertEqual(pair_eval(t,pairs).decode(),scalar_eval(t,e))

    def test_cross_sum_direction(self):
        x,y = Pair.encode(Q(-3)),Pair.encode(Q(2))
        self.assertTrue(x.le(y))
        # Compiled antecedent y+ + x- covers consequent x+ + y-.
        self.assertGreaterEqual(y.pos+x.neg, x.pos+y.neg)
        self.assertFalse(y.le(x))

    def test_guard_needed_for_infinite_fake_zero(self):
        self.assertEqual(math.inf+math.inf, math.inf+math.inf)
        self.assertEqual(finite_guard(math.inf), math.inf)
        with self.assertRaises(TypeError): Pair(math.inf, math.inf)

    def test_finiteness_guard_parentheses(self):
        for x in (Q(0),Q(1),Q(1000000),math.inf):
            self.assertEqual(finite_guard(x)==0, x != math.inf)
            # The other grouping has opposite behavior on these values.
            wrong = residual(x, residual(x, math.inf))
            self.assertNotEqual(wrong, finite_guard(x))

    def test_quotient_graph(self):
        for a,b in product(range(-3,4),repeat=2):
            x,y=Pair.encode(Q(a)),Pair.encode(Q(b))
            if b:
                z=Pair.encode(Q(a,b)).shifted(Q(2))
                self.assertTrue(quotient_graph(x,y,z))
                self.assertFalse(quotient_graph(x,y,Pair.encode(Q(a,b)+1)))
            else:
                self.assertFalse(quotient_graph(x,y,Pair.encode(Q(0))))

    def test_zero_over_zero_requires_guard(self):
        zero=Pair(1,1)
        for a in range(-3,4):
            z=Pair.encode(Q(a))
            # Raw polynomial equality accepts all outputs; guarded graph does not.
            self.assertEqual(z.pos+z.neg+1,z.neg+z.pos+1)
            self.assertFalse(quotient_graph(zero,zero,z))

    def test_negative_denominator(self):
        self.assertTrue(quotient_graph(Pair(0,6),Pair(0,2),Pair(3,0)))

    def test_nonnegative_additive_zero_constraint(self):
        for a,b in product(range(5),repeat=2):
            if a+b==0: self.assertEqual((a,b),(0,0))

    def test_cost_residual_adjunction(self):
        for c,x,y in product([Q(0),Q(1,2),Q(2)],repeat=3):
            self.assertEqual(c+x >= y, c >= residual(x,y))

    def test_signed_residual_requires_untruncated_difference(self):
        x,y,c=Q(2),Q(1),Q(-1,2)
        self.assertTrue(c+x >= y)
        self.assertTrue(c >= y-x)
        self.assertFalse(c >= residual(x,y))
        for c,x,y in product(range(-3,4),repeat=3):
            self.assertEqual(c+x>=y,c>=y-x)

    def test_left_weakening_needs_nonnegative_added_value(self):
        self.assertGreaterEqual(0,0)
        self.assertFalse(-1 >= 0)
        for a,b,c in product(range(-2,3),range(-2,3),range(3)):
            if a>=b: self.assertGreaterEqual(a+c,b)

    def test_negative_multiplier_reverses_order(self):
        self.assertTrue(1>=0)
        self.assertFalse(-1>=0)
        for a,b in product(range(-3,4),repeat=2):
            if a>=b: self.assertLessEqual(-2*a,-2*b)

    def test_negative_cone_term_identity(self):
        terms=expressions()
        for a,b in product(range(-3,4),repeat=2):
            v={'p':Q(a),'r':Q(b)}
            c={name:-min(value,Q(0)) for name,value in v.items()}
            for t in terms:
                self.assertEqual(scalar_eval(negative_cone(t),v),-cost_eval(t,c))

    def test_negative_cone_nested_identity(self):
        terms=[('imp',('add',P,R),('max',P,R)),
               ('add',('imp',P,R),('imp',R,P)),
               ('max',('min',P,R),('add',P,R))]
        for a,b in product(range(-3,4),repeat=2):
            v={'p':Q(a),'r':Q(b)}
            c={k:-min(x,Q(0)) for k,x in v.items()}
            for t in terms:
                self.assertEqual(scalar_eval(negative_cone(t),v),-cost_eval(t,c))

    def test_negative_cone_covers_all_supplied_nonnegative_assignments(self):
        for a,b in product([Q(0),Q(1,2),Q(1000)],repeat=2):
            for t in expressions():
                self.assertEqual(scalar_eval(negative_cone(t),{'p':-a,'r':-b}),
                                 -cost_eval(t,{'p':a,'r':b}))

    def test_sequent_formula_polarity_and_empty_antecedent(self):
        for a,b in product(range(-3,4),repeat=2):
            v={'p':Q(a),'r':Q(b)}
            c={k:-min(x,Q(0)) for k,x in v.items()}
            for gamma,target in (([P,R],('add',P,R)),([P],R),([],P)):
                source_margin=sum((cost_eval(t,c) for t in gamma),Q(0))-cost_eval(target,c)
                target_value=scalar_eval(negative_cone(target),v)-sum(
                    (scalar_eval(negative_cone(t),v) for t in gamma),Q(0))
                self.assertEqual(source_margin,target_value)

    def test_fragment_restrictions_enforced(self):
        for t in (('c',Q(1)),('mul',P,R),('div',P,R),('infinity',)):
            with self.assertRaises(ValueError): negative_cone(t)

    def test_abelian_validity_is_nonnegative_not_zero_only(self):
        for p in range(-3,4):
            self.assertGreaterEqual(max(p,-p),0)
        self.assertNotEqual(max(2,-2),0)

    def test_disjunction_does_not_choose_uniform_branch(self):
        # For all p, max(p,-p)>=0; neither branch is nonnegative for all p.
        self.assertTrue(all(max(p,-p)>=0 for p in (-1,1)))
        self.assertFalse(all(p>=0 for p in (-1,1)))
        self.assertFalse(all(-p>=0 for p in (-1,1)))

    def test_source_normalization_representatives(self):
        self.assertTrue(1>=0)  # 1 |- 0 is valid.
        self.assertFalse(0>=1) # 0 |- 1 is unsatisfiable.

    def test_directed_triangle_on_signed_profiles(self):
        profiles=[tuple(map(Q,p)) for p in product(range(-2,3),repeat=2)]
        for x,y,z in product(profiles,repeat=3):
            self.assertLessEqual(directed_loss(x,z),directed_loss(x,y)+directed_loss(y,z))

    def test_sharp_signed_replacement_example(self):
        m,n,p=(Q(5),Q(-2)),(Q(4),Q(1)),(Q(2),Q(0))
        self.assertEqual((directed_loss(m,n),directed_loss(n,p),directed_loss(m,p)),(1,2,3))
        self.assertEqual(directed_loss(n,m),3)

    def test_zero_means_directional_dominance(self):
        for x,y in product([tuple(map(Q,p)) for p in product(range(-2,3),repeat=2)],repeat=2):
            self.assertEqual(directed_loss(x,y)==0, all(a<=b for a,b in zip(x,y)))
            self.assertEqual(directed_loss(x,y)==directed_loss(y,x)==0,x==y)

    def test_common_task_offsets_cancel(self):
        x,y=(Q(-5),Q(9)),(Q(-3),Q(2))
        k=(Q(10**100),Q(-10**100))
        self.assertEqual(directed_loss(tuple(a+b for a,b in zip(x,k)),
                                       tuple(a+b for a,b in zip(y,k))),directed_loss(x,y))

    def test_finite_samples_of_unbounded_profile_family(self):
        # This checks sample identities, not an exhaustive statement over integers.
        for n in (-10**100,-10,-1,0,1,10,10**100):
            self.assertEqual(shortfall(Q(n),Q(n-1)),1)

    def test_empty_or_misaligned_task_sets_rejected(self):
        for x,y in (((),()),((Q(0),),(Q(0),Q(1)))):
            with self.assertRaises(ValueError): directed_loss(x,y)

    def test_threshold_deficit_loses_surplus(self):
        self.assertEqual(shortfall(Q(5),Q(6)),shortfall(Q(5),Q(100)))
        self.assertNotEqual(Q(6),Q(100))

    def test_source_manifest_preserves_previous_sources(self):
        data=json.loads((Path(__file__).parents[1]/'literature/F03_sources.json').read_text())
        sources={s['id']:s for s in data['sources']}
        self.assertEqual(data['core_count'],8)
        self.assertGreaterEqual(data['supplementary_count'],5)
        self.assertEqual(len(data['sources']), data['core_count']+data['supplementary_count'])
        self.assertTrue({f'S{i:02}' for i in range(1,14)} <= set(sources))
        self.assertIn('Abelian',sources['S13']['title'])
        self.assertFalse(sources['S13']['whole_work_verified'])
        self.assertFalse(sources['S12']['whole_work_verified'])


def report() -> dict:
    return {
        'scope':'Finite development fixtures for source adapters; not theorem/proof-system verification',
        'rational_arithmetic':True,
        'tests_expected':32,
        'bounds':{'small_pair_comparisons':81,'noncanonical_comparisons':225,
                  'polynomial_terms':9,'polynomial_assignments':49,
                  'negative_cone_terms':39,'negative_cone_signed_assignments':49,
                  'directed_triangle_profile_triples':15625},
        'sharp_directed_example':{'M':['5','-2'],'N':['4','1'],'P':['2','0'],
                                  'M_to_N':'1','N_to_P':'2','M_to_P':'3','N_to_M':'3'},
        'finite_signed_pair':'Each coordinate finite and nonnegative; decoded range not uniformly bounded',
        'polynomial_import':'S12 Theorem 11 with finitising guards on every premise/target variable',
        'negative_cone_scope':'Finite constant-zero additive fragment; no infinity, positive constants, multiplication or division',
        'normalization_sanity':{'1 |- 0':True,'0 |- 1':False},
        'infinite_claims':'Proved in notes from pointwise identities, not inferred from sampled integers',
        'core_selected':False,
    }


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(F03ValueBridgeTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        data=report(); data['tests_passed']=result.testsRun
        args.json.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
