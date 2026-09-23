"""Exact finite checks for F03 source-adapter assumptions, not a proof calculus.

Finite arithmetic uses Fraction. The explicit 'inf' sentinel follows the
endpoint conventions in Rational Lawvere Logic, Table 1. These tests do not
verify that paper's entire deduction system, its completeness theorem, or a
mathematical citation against the network.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
from typing import Iterable, Literal
import unittest

INF: Literal['inf'] = 'inf'
Ext = Q | Literal['inf']
GRID: tuple[Ext, ...] = (Q(0), Q(1, 2), Q(1), Q(2), INF)
REAL = tuple(Q(i, 2) for i in range(-4, 5))
ROOT = Path(__file__).resolve().parents[2]


def checked(x: Ext | int) -> Ext:
    if x == INF:
        return INF
    if isinstance(x, bool) or not isinstance(x, (Q, int)) or x < 0:
        raise ValueError('a nonnegative rational or the explicit inf sentinel is required')
    return Q(x)


def le(a: Ext | int, b: Ext | int) -> bool:
    a, b = checked(a), checked(b)
    return b == INF or (a != INF and a <= b)


def add(a: Ext | int, b: Ext | int) -> Ext:
    a, b = checked(a), checked(b)
    return INF if a == INF or b == INF else a + b


def mul(a: Ext | int, b: Ext | int) -> Ext:
    a, b = checked(a), checked(b)
    if a == 0 or b == 0:
        return Q(0)
    return INF if a == INF or b == INF else a * b


def sub(b: Ext | int, a: Ext | int) -> Ext:
    """The residual b dotminus a, including inf dotminus inf = 0."""
    b, a = checked(b), checked(a)
    if a == INF:
        return Q(0)
    return INF if b == INF else max(Q(0), b - a)


def div(b: Ext | int, a: Ext | int) -> Ext:
    """Right residual of multiplication: c*a <= b iff c <= b/a."""
    b, a = checked(b), checked(a)
    if a == 0 or b == INF:
        return INF
    return Q(0) if a == INF else b / a


def sequent(gamma: Iterable[Ext | int], consequent: Ext | int) -> bool:
    total: Ext = Q(0)
    for term in gamma:
        total = add(total, term)
    return le(consequent, total)


def neg(a: Ext | int) -> Ext:
    return sub(INF, a)


def finite_test(a: Ext | int) -> Ext:
    return neg(neg(a))


def zero_test(a: Ext | int) -> Ext:
    return mul(a, INF)


@dataclass(frozen=True)
class SignedPair:
    positive: Q
    negative: Q

    def __post_init__(self) -> None:
        if any(isinstance(x, bool) or not isinstance(x, (Q, int)) or x < 0
               for x in (self.positive, self.negative)):
            raise ValueError('both coordinates must be finite nonnegative rationals')
        object.__setattr__(self, 'positive', Q(self.positive))
        object.__setattr__(self, 'negative', Q(self.negative))

    @classmethod
    def encode(cls, x: Q) -> SignedPair:
        return cls(max(Q(0), x), max(Q(0), -x))

    def decode(self) -> Q:
        return self.positive - self.negative

    def plus(self, other: SignedPair) -> SignedPair:
        return SignedPair(self.positive + other.positive, self.negative + other.negative)

    def negate(self) -> SignedPair:
        return SignedPair(self.negative, self.positive)

    def times(self, other: SignedPair) -> SignedPair:
        a, b, c, d = self.positive, self.negative, other.positive, other.negative
        return SignedPair(a*c + b*d, a*d + b*c)

    def extremum(self, other: SignedPair, *, maximum: bool) -> SignedPair:
        a, b, c, d = self.positive, self.negative, other.positive, other.negative
        op = max if maximum else min
        return SignedPair(op(a+d, c+b), b+d)

    def below(self, other: SignedPair) -> bool:
        return sequent((other.positive, self.negative), self.positive + other.negative)


def directed(x: Q, y: Q, unit: Q = Q(1)) -> Q:
    if unit <= 0:
        raise ValueError('unit must be positive')
    return min(Q(1), max(Q(0), y-x) / unit)


def scale_allowance(epsilon: Q, coefficient: Q) -> Q:
    if not 0 <= epsilon <= 1 or coefficient < 0:
        raise ValueError('allowance in [0,1] and nonnegative coefficient required')
    if coefficient == 0:
        return Q(0)
    if epsilon == 1:
        return Q(1)
    return min(Q(1), coefficient * epsilon)


def relation_context(labels: tuple[str, ...], premises: tuple[tuple[str, str, Q], ...]):
    if len(labels) != len(set(labels)):
        raise ValueError('distinct variable labels required')
    relation = {(x, y): Q(1) for x in labels for y in labels}
    for x, y, epsilon in premises:
        if (x, y) not in relation or not 0 <= epsilon <= 1:
            raise ValueError('premise references unknown variables or an invalid bound')
        relation[x, y] = min(relation[x, y], epsilon)
    return relation


def admissible(values: dict[str, Q], relation: dict[tuple[str, str], Q]) -> bool:
    return all(directed(values[x], values[y]) <= e for (x, y), e in relation.items())


def violation(menu: tuple[tuple[Q, ...], ...], budget: tuple[Q, ...]) -> Q:
    if not menu or not budget:
        raise ValueError('finite nonempty menu and positive dimension required')
    if any(len(option) != len(budget) for option in menu):
        raise ValueError('all cost and budget dimensions must agree')
    for x in (*budget, *(x for option in menu for x in option)):
        if not isinstance(x, (Q, int)) or isinstance(x, bool) or x < 0:
            raise ValueError('finite nonnegative normalized costs required')
    return min(max(max(Q(0), c-b) for c, b in zip(option, budget)) for option in menu)


class F03ProofAuditTests(unittest.TestCase):
    def test_endpoint_addition_and_multiplication(self):
        self.assertEqual(add(0, INF), INF)
        self.assertEqual(mul(0, INF), 0)
        self.assertEqual(mul(INF, 0), 0)
        self.assertEqual(mul(INF, Q(1, 2)), INF)

    def test_endpoint_residuals(self):
        self.assertEqual(sub(INF, INF), 0)
        self.assertEqual(sub(2, INF), 0)
        self.assertEqual(sub(INF, 2), INF)
        self.assertEqual(div(0, 0), INF)
        self.assertEqual(div(INF, INF), INF)
        self.assertEqual(div(2, INF), 0)

    def test_additive_adjunction(self):
        for a, b, c in product(GRID, repeat=3):
            self.assertEqual(le(b, add(c, a)), le(sub(b, a), c))

    def test_multiplicative_adjunction(self):
        for a, b, c in product(GRID, repeat=3):
            self.assertEqual(le(mul(c, a), b), le(c, div(b, a)))

    def test_semiring_distributivity_with_endpoints(self):
        for a, b, c in product(GRID, repeat=3):
            self.assertEqual(mul(a, add(b, c)), add(mul(a, b), mul(a, c)))

    def test_finiteness_and_zero_are_different(self):
        for x in GRID:
            self.assertEqual(finite_test(x) == 0, x != INF)
            self.assertEqual(zero_test(x) == 0, x == 0)
        self.assertEqual(finite_test(1), 0)
        self.assertEqual(zero_test(1), INF)

    def test_antecedent_contraction_is_invalid(self):
        self.assertTrue(sequent((1, 1), 2))
        self.assertFalse(sequent((1,), 2))

    def test_finite_common_summand_cancellation(self):
        for a, b in product(GRID, repeat=2):
            for c in GRID[:-1]:
                self.assertEqual(le(add(a, c), add(b, c)), le(a, b))

    def test_infinite_common_summand_cancellation_fails(self):
        self.assertTrue(le(add(1, INF), add(0, INF)))
        self.assertFalse(le(1, 0))

    def test_two_bounds_compose_to_two_not_one(self):
        for u, v in product((Q(0), Q(1, 2), Q(1)), repeat=2):
            for e in (Q(0), Q(1, 2), Q(1), Q(3, 2), Q(2)):
                if sequent((u, v), e):
                    self.assertTrue(sequent((1, 1), e))
        self.assertFalse(sequent((1,), 2))

    def test_inconsistent_premises_have_no_sampled_model(self):
        self.assertFalse(any(sequent((0,), p) and sequent((p,), 1) for p in GRID))

    def test_finite_parts_do_not_force_zero(self):
        for n in range(1, 31):
            p = Q(1, 2**n)
            self.assertTrue(all(sequent((Q(1, 2**k),), p) for k in range(1, n+1)))
            self.assertFalse(sequent((), p))

    def test_positive_tolerance_has_finite_dyadic_evidence(self):
        for denominator in range(1, 101):
            delta = Q(1, denominator)
            n = denominator.bit_length()
            self.assertLessEqual(Q(1, 2**n), delta)

    def test_signed_pair_add_negation_and_multiplication(self):
        pairs = tuple(SignedPair(a, b) for a, b in product(GRID[:-1], repeat=2))
        for a, b in product(pairs, repeat=2):
            self.assertEqual(a.plus(b).decode(), a.decode() + b.decode())
            self.assertEqual(a.times(b).decode(), a.decode() * b.decode())
            self.assertEqual(a.negate().decode(), -a.decode())

    def test_signed_pair_comparisons(self):
        for x, y in product(REAL, repeat=2):
            a, b = SignedPair.encode(x), SignedPair.encode(y)
            self.assertEqual(a.below(b), x <= y)

    def test_noncanonical_pair_representations(self):
        for x in REAL:
            p = SignedPair.encode(x)
            q = SignedPair(p.positive+7, p.negative+7)
            self.assertEqual(p.decode(), q.decode())
            self.assertTrue(p.below(q) and q.below(p))

    def test_signed_pair_min_and_max(self):
        pairs = tuple(SignedPair(a, b) for a, b in product(GRID[:-1], repeat=2))
        for a, b in product(pairs, repeat=2):
            for maximum in (False, True):
                op = max if maximum else min
                self.assertEqual(a.extremum(b, maximum=maximum).decode(), op(a.decode(), b.decode()))

    def test_signed_pair_polynomial_example(self):
        for x, y in product(REAL, repeat=2):
            a, b = SignedPair.encode(x), SignedPair.encode(y)
            term = a.times(a).plus(b.times(SignedPair.encode(Q(-2)))).plus(a.times(b))
            self.assertEqual(term.decode(), x*x - 2*y + x*y)

    def test_infinite_signed_pair_is_rejected(self):
        for a, b in ((INF, INF), (-1, 0), (0.5, 0)):
            with self.assertRaises(ValueError):
                SignedPair(a, b)

    def test_directed_zero_is_order_not_equality(self):
        self.assertEqual(directed(Q(2), Q(1)), 0)
        self.assertEqual(directed(Q(1), Q(2)), 1)
        self.assertNotEqual(Q(2), Q(1))

    def test_directed_triangle_and_unit_scaling(self):
        for x, y, z in product(REAL, repeat=3):
            self.assertLessEqual(directed(x, z), min(Q(1), directed(x, y)+directed(y, z)))
            self.assertEqual(directed(3*x, 3*y, Q(3)), directed(x, y))

    def test_directed_sum_and_bottleneck_bounds(self):
        for a, b, c, d in product(REAL, repeat=4):
            bound = min(Q(1), directed(a, c)+directed(b, d))
            self.assertLessEqual(directed(a+b, c+d), bound)
            bottleneck = max(directed(a, c), directed(b, d))
            self.assertLessEqual(directed(min(a, b), min(c, d)), bottleneck)
            self.assertLessEqual(directed(max(a, b), max(c, d)), bottleneck)

    def test_cap_endpoint_invalidates_naive_scaled_error(self):
        self.assertEqual(directed(Q(0), Q(100)), 1)
        self.assertEqual(directed(Q(0), Q(50)), 1)
        self.assertGreater(directed(Q(0), Q(50)), Q(1, 2)*directed(Q(0), Q(100)))

    def test_guarded_scale_allowance(self):
        for x, y in product((*REAL, Q(100)), repeat=2):
            for coefficient in (Q(0), Q(1, 10), Q(1, 2), Q(1), Q(3)):
                e = directed(x, y)
                self.assertLessEqual(directed(coefficient*x, coefficient*y), scale_allowance(e, coefficient))

    def test_variable_context_uses_ordered_pairs(self):
        context = relation_context(('x', 'y', 'z'), (('x', 'y', Q(1, 5)),))
        self.assertEqual(context['x', 'y'], Q(1, 5))
        self.assertEqual(context['y', 'x'], 1)
        self.assertEqual(context['z', 'z'], 1)  # no reflexivity rule was silently installed

    def test_finite_context_matches_all_supplied_premises(self):
        premises = (('x', 'y', Q(1, 2)), ('x', 'y', Q(1, 4)), ('y', 'x', Q(0)))
        context = relation_context(('x', 'y'), premises)
        for x, y in product(REAL, repeat=2):
            values = {'x': x, 'y': y}
            self.assertEqual(admissible(values, context), all(directed(values[a], values[b]) <= e for a,b,e in premises))

    def test_unrestricted_context_substitution_fails(self):
        source = relation_context(('x', 'y'), (('x', 'y', Q(1, 5)),))
        self.assertTrue(admissible({'x': Q(0), 'y': Q(1, 10)}, source))
        self.assertFalse(admissible({'x': Q(0), 'y': Q(9, 10)}, source))

    def test_mean_zero_class_is_not_minimum_congruence(self):
        x, y = (Q(3), Q(-1)), (Q(-1), Q(3))
        mean = lambda t: sum(t, Q(0))/len(t)
        self.assertEqual(mean(x), mean(y))
        self.assertEqual(mean(tuple(min(a,b) for a,b in zip(x,x))), 1)
        self.assertEqual(mean(tuple(min(a,b) for a,b in zip(x,y))), -1)

    def test_finite_budget_formula_matches_direct_feasibility(self):
        points = tuple(product((Q(0), Q(1), Q(2)), repeat=2))
        for a, b, budget in product(points, repeat=3):
            menu = (a,b)
            expected = any(all(x <= y for x,y in zip(c,budget)) for c in menu)
            self.assertEqual(violation(menu, budget) == 0, expected)

    def test_unsupported_budget_option_is_retained(self):
        a,b,c = (Q(0),Q(2)), (Q(2),Q(0)), (Q(3,2),Q(3,2))
        self.assertEqual(violation((a,b), c), Q(1,2))
        self.assertEqual(violation((a,b,c), c), 0)

    def test_budget_quantifier_order(self):
        v = ((Q(0), Q(2)), (Q(2), Q(0)))  # rows: models; columns: options
        self.assertEqual(max(min(row) for row in v), 0)
        self.assertEqual(min(max(row[i] for row in v) for i in range(2)), 2)

    def test_infinite_menu_prefixes_do_not_attain_zero(self):
        for n in range(1, 31):
            menu = tuple((Q(1,k),) for k in range(1,n+1))
            self.assertEqual(violation(menu, (Q(0),)), Q(1,n))
            self.assertGreater(violation(menu, (Q(0),)), 0)

    def test_reused_factor_changes_cost(self):
        unary, binary = Q(1), Q(2)
        self.assertEqual(unary + binary, 3)
        unary = unary + binary
        self.assertEqual(unary + binary, 5)
        unary = unary + binary
        self.assertEqual(unary + binary, 7)

    def test_single_elimination_keeps_joint_minimum(self):
        a,b = (Q(0),Q(2)), (Q(1),Q(0))
        c = lambda x,y: Q(0) if x == y else Q(3)
        table = tuple(tuple(a[x]+b[y]+c(x,y) for y in range(2)) for x in range(2))
        message = tuple(min(b[y]+c(x,y) for y in range(2)) for x in range(2))
        self.assertEqual(table, ((1,3),(6,2)))
        self.assertEqual(message, (1,0))
        self.assertEqual(min(min(row) for row in table), min(a[x]+message[x] for x in range(2)))
        self.assertEqual(min(a)+min(b)+min(c(x,y) for x,y in product(range(2),repeat=2)), 0)

    def test_shared_model_mixing_vs_actionwise_rectangularity(self):
        for i in range(21):
            q = Q(i,20)
            shared = min(q, 1-q)
            rectangular = min(q*a+(1-q)*b for a,b in product((Q(0),Q(1)),repeat=2))
            self.assertEqual(rectangular, 0)
            self.assertLessEqual(shared, Q(1,2))
        self.assertEqual(min(Q(1,2), 1-Q(1,2)), Q(1,2))

    def test_survival_normalization_reverses_comparison(self):
        unconditioned = Q(1,100)*10
        conditioned = unconditioned / Q(1,100)
        self.assertLess(unconditioned, 1)
        self.assertGreater(conditioned, 1)

    def test_cemetery_shift_must_include_all_outcomes(self):
        m, value, c = Q(1,4), Q(8), Q(2)
        self.assertEqual(m*(value+c)-m*value, m*c)
        self.assertEqual(m*(value+c)+(1-m)*c-m*value, c)

    def test_reject_invalid_contract_inputs(self):
        for x in (-1, True, float('nan'), 'infinity'):
            with self.assertRaises(ValueError):
                checked(x)
        with self.assertRaises(ValueError): violation((), (Q(1),))
        with self.assertRaises(ValueError): violation(((Q(1),),), ())
        with self.assertRaises(ValueError): violation(((Q(1),),), (Q(1),Q(2)))
        with self.assertRaises(ValueError): directed(Q(0),Q(1),Q(0))
        with self.assertRaises(ValueError): scale_allowance(Q(2),Q(1))
        with self.assertRaises(ValueError): relation_context(('x',), (('x','y',Q(0)),))

    def test_manifest_keeps_original_sources_and_adds_targeted_s12(self):
        manifest = json.loads((ROOT/'v2/literature/F03_sources.json').read_text(encoding='utf-8'))
        by_id = {s['id']:s for s in manifest['sources']}
        self.assertEqual(set(by_id), {f'S{i:02}' for i in range(1,13)})
        self.assertEqual((manifest['core_count'],manifest['supplementary_count']), (8,4))
        self.assertEqual(by_id['S12']['title'], 'Rational Lawvere Logic')
        self.assertEqual(by_id['S12']['publication_year'], 2026)
        self.assertFalse(by_id['S12']['whole_work_verified'])
        self.assertIn('10.4230/LIPIcs.CSL.2026.3', by_id['S12']['primary_urls'][0])


def report(count: int) -> dict:
    return {
        'task':'F03', 'session':'2026-09-22-S2',
        'base_commit':'973af3cd668fb4f558f2ca30133da3779a68e1b4',
        'test_count':count,
        'scope':'source-adapter arithmetic and finite countermodels, not a theorem prover',
        'witnesses':{
            'zero_times_infinity': '0', 'infinity_dotminus_infinity':'0',
            'zero_divided_by_zero':'inf', 'infinity_divided_by_infinity':'inf',
            'resource_composition_bound':'2', 'invalid_contracted_bound':'1',
            'capped_half_scale':{'input':'1','output':'1','invalid_allowance':'1/2'},
            'menu_violation_without_third':'1/2','menu_violation_with_third':'0',
            'model_then_choice':'0','choice_then_model':'2',
            'factor_original':'3','factor_reused_once':'5',
            'exact_elimination_minimum':'1','independent_factor_minima':'0',
            'shared_reward_mixture':'1/2','actionwise_product_reward':'0',
            'unconditioned_survival_reward':'1/10','conditioned_reward':'10'
        },
        'finite_bounds':{
            'extended_values':['0','1/2','1','2','inf'],
            'each_adjoint_check_triples':len(GRID)**3,
            'real_grid':[str(x) for x in REAL],
            'directed_sum_four_tuples':len(REAL)**4,
            'signed_pair_coordinate_grid':['0','1/2','1','2'],
            'pair_pairs_per_polynomial_check':4**4,
            'finite_budget_menu_pair_and_budget_cases':9**3,
            'dyadic_and_infinite_menu_prefixes':[1,30],
            'mixing_probabilities':'i/20, i=0,...,20'
        },
        'not_established':[
            'complete source deduction or Positivstellensatz procedure',
            'unrestricted theorem truth from finite enumeration',
            'new Value Logic core, F04 or readiness gate',
            'F03 L60 from these tests or full repository validation'
        ]
    }


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F03ProofAuditTests))
    if not result.wasSuccessful():
        return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(result.testsRun),indent=2)+'\n',encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
