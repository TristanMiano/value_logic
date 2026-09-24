"""Finite exact checks for the F03 source-use handoff, not a general reasoner.

The unrestricted statements are proved in 01f_consolidated_source_handoff.md.
This module tests constructed rational cases and source-register bookkeeping.
It neither checks external proofs nor implements Rational Lawvere deduction.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from typing import Sequence
import unittest

Q = Fraction
Exact = int | Fraction


def exact(value: Exact) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError('Use an integer or Fraction, not a rounded float.')
    return Q(value)


def vector(values: Sequence[Exact]) -> tuple[Fraction, ...]:
    if not values:
        raise ValueError('At least one coordinate is required.')
    return tuple(exact(v) for v in values)


def shortfall(x: Sequence[Exact], y: Sequence[Exact]) -> Fraction:
    x, y = vector(x), vector(y)
    if len(x) != len(y):
        raise ValueError('Coordinate dimensions must match.')
    return max(Q(0), *(a - b for a, b in zip(x, y)))


def affine(matrix: Sequence[Sequence[Exact]], offset: Sequence[Exact],
           x: Sequence[Exact]) -> tuple[Fraction, ...]:
    x, offset = vector(x), vector(offset)
    rows = [vector(row) for row in matrix]
    if len(rows) != len(offset) or any(len(row) != len(x) for row in rows):
        raise ValueError('Matrix, offset and input dimensions do not match.')
    return tuple(r + sum((a*b for a, b in zip(row, x)), Q(0))
                 for r, row in zip(offset, rows))


def matrix_gain(matrix: Sequence[Sequence[Exact]]) -> Fraction:
    rows = [vector(row) for row in matrix]
    if not rows or len({len(row) for row in rows}) != 1:
        raise ValueError('A nonempty rectangular matrix is required.')
    if any(a < 0 for row in rows for a in row):
        raise ValueError('This certificate requires nonnegative entries.')
    return max(sum(row, Q(0)) for row in rows)


def belief_b(q: Exact) -> Fraction:
    q = exact(q)
    if not 0 <= q <= 1:
        raise ValueError('q must belong to the unit interval.')
    return Q(0) if q == 0 else Q(1)


def compound_h(q: Exact) -> Fraction:
    q = exact(q)
    return q + max(Q(0), Q(1) - belief_b(q))


def report() -> dict:
    p = ((Q(1, 2), 0), (0, Q(1, 4)))
    x, y = (5, -2), (4, 1)
    fx, fy = affine(p, (0, 0), x), affine(p, (0, 0), y)
    return {
        'task': 'F03', 'session': '2026-09-24-S6',
        'scope': 'Exact constructed finite fixtures; not external-proof validation.',
        'scalar_domain': 'Fraction over finite rational numbers; no floating point or infinity.',
        'directed_example': {'input_shortfall': str(shortfall(x, y)),
                             'output_shortfall': str(shortfall(fx, fy)),
                             'matrix_gain': str(matrix_gain(p)),
                             'shift_two': ['1', '1/2']},
        'addition_gain_witness': {'input_shortfall': '1', 'output_shortfall': '2'},
        'pointwise_disjunction': {'at_zero': [True, False],
                                 'at_one': [False, True],
                                 'one_branch_valid_everywhere': False},
        'derived_cost': {'h_at_zero': str(compound_h(0)),
                        'h_at_1_over_n': {str(n): str(compound_h(Q(1, n)))
                                          for n in range(1, 17)},
                        'infimum': '0', 'attained': False,
                        'infinite_claim_evidence': 'Analytic proof in note section 7, not finite samples.'},
        'bounds': {'rational_grid': ['-2', '-1/2', '0', '1/2', '2'],
                   'vector_pairs_per_matrix': 625, 'matrices': 5,
                   'nonnegative_shifts': ['0', '1/2', '2'],
                   'sequence_indices': '1 through 16'},
        'metadata_evidence': 'Register coherence only, not a theorem-proof audit.'
    }


class F03HandoffTests(unittest.TestCase):
    def test_shortfall_zero_exactly_coordinatewise_order(self):
        for a, b, c, d in product(range(-2, 3), repeat=4):
            self.assertEqual(shortfall((a, b), (c, d)) == 0, a <= c and b <= d)

    def test_shortfall_triangle_on_finite_grid(self):
        grid = list(product((-1, 0, 1), repeat=2))
        for x, y, z in product(grid, repeat=3):
            self.assertLessEqual(shortfall(x, z), shortfall(x, y)+shortfall(y, z))

    def test_input_validation(self):
        for x, y in [((), ()), ((0,), (0, 1))]:
            with self.assertRaises(ValueError):
                shortfall(x, y)
        for v in [0.5, True, '1']:
            with self.assertRaises(TypeError):
                shortfall((v,), (0,))
        for p in [(), ((1, 0), (1,)), ((-1,),)]:
            with self.assertRaises(ValueError):
                matrix_gain(p)
        with self.assertRaises(ValueError):
            affine(((1, 0),), (0, 0), (1, 2))

    def test_affine_directed_gain(self):
        grid = list(product((Q(-2), Q(-1, 2), Q(0), Q(1, 2), Q(2)), repeat=2))
        matrices = [((1, 0), (0, 1)), ((Q(1, 2), 0), (0, Q(1, 4))),
                    ((1, 1),), ((0, 0),), ((Q(1, 3), Q(2, 3)), (1, 2))]
        for p in matrices:
            gain = matrix_gain(p)
            offset = tuple((-1)**i * 10**20 for i in range(len(p)))
            for x, y in product(grid, repeat=2):
                self.assertLessEqual(shortfall(affine(p, offset, x), affine(p, offset, y)),
                                     gain*shortfall(x, y))

    def test_affine_shift_bound(self):
        p = ((Q(1, 2), 0), (0, Q(1, 4)))
        gain = matrix_gain(p)
        for x in product((-2, 0, 2), repeat=2):
            for c in (0, Q(1, 2), 2):
                out = affine(p, (3, -5), x)
                shifted = affine(p, (3, -5), tuple(v+c for v in x))
                self.assertTrue(all(b <= a+gain*c for a, b in zip(out, shifted)))

    def test_substochastic_does_not_require_exact_common_shift(self):
        p = ((Q(1, 2), 0), (0, Q(1, 4)))
        x, y = (5, -2), (4, 1)
        self.assertEqual(shortfall(x, y), 1)
        self.assertEqual(shortfall(affine(p, (0, 0), x), affine(p, (0, 0), y)), Q(1, 2))
        delta = tuple(b-a for a, b in zip(affine(p, (0, 0), x),
                      affine(p, (0, 0), tuple(v+2 for v in x))))
        self.assertEqual(delta, (1, Q(1, 2)))
        self.assertNotEqual(delta, (2, 2))

    def test_gains_compose(self):
        f = lambda x: (x[0]+x[1],)
        g = lambda y: (Q(1, 2)*y[0]+7, Q(1, 4)*y[0]-8)
        for x, y in product(product((-2, 0, 2), repeat=2), repeat=2):
            self.assertLessEqual(shortfall(g(f(x)), g(f(y))), shortfall(x, y))

    def test_addition_needs_gain_two(self):
        self.assertEqual(shortfall((1, 1), (0, 0)), 1)
        self.assertEqual(shortfall((2,), (0,)), 2)

    def test_monotonicity_is_necessary(self):
        self.assertEqual(shortfall((0,), (1,)), 0)
        self.assertEqual(shortfall((0,), (-1,)), 1)  # F(x)=-x

    def test_zero_gain_and_nonlinear_positive_control(self):
        for x, y in product(range(-5, 6), repeat=2):
            self.assertEqual(shortfall((999,), (999,)), 0)
            f = lambda v: max(0, min(1, v))
            self.assertLessEqual(shortfall((f(x),), (f(y),)), shortfall((x,), (y,)))

    def test_pointwise_disjunction_is_not_uniform_choice(self):
        branches = [(q >= 1-q, 1-q >= q) for q in (0, Q(1, 4), Q(1, 2), Q(3, 4), 1)]
        self.assertTrue(all(a or b for a, b in branches))
        self.assertFalse(all(a for a, b in branches) or all(b for a, b in branches))

    def test_compound_cost_at_boundary(self):
        self.assertEqual(belief_b(0), 0)
        self.assertEqual(compound_h(0), 1)
        for n in range(1, 17):
            q = Q(1, n)
            self.assertEqual(belief_b(q), 1)
            self.assertEqual(compound_h(q), q)
            self.assertGreater(compound_h(q), 0)
        with self.assertRaises(ValueError):
            compound_h(-1)

    def test_source_register_scope_and_identities(self):
        root = Path(__file__).resolve().parents[1]/'literature'
        reg = json.loads((root/'F03_import_contracts.json').read_text())
        src = json.loads((root/'F03_sources.json').read_text())
        self.assertFalse(reg['is_proof_checker'])
        self.assertFalse(reg['selects_calculus'])
        self.assertFalse(reg['passes_gate'])
        ids = [r['source_id'] for r in reg['contracts']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {r['id'] for r in src['sources']})
        self.assertEqual(len(ids), 18)
        self.assertEqual(sum(r['role'] == 'core' for r in src['sources']), 8)
        for row in reg['contracts']:
            for field in ('status', 'usable_interface', 'required_hypotheses', 'not_licensed', 'locators'):
                self.assertTrue(row[field])
            self.assertFalse(row['whole_work_verified'])

    def test_no_accidental_strong_imports(self):
        root = Path(__file__).resolve().parents[1]/'literature'
        reg = json.loads((root/'F03_import_contracts.json').read_text())
        rows = {r['source_id']: r for r in reg['contracts']}
        self.assertEqual(rows['S14']['status'], 'lead-only')
        self.assertEqual(rows['S16']['status'], 'rejected-claim-retained-definitions')
        self.assertTrue(any('conclusion' in x for x in rows['S12']['required_hypotheses']))
        self.assertTrue(any('Ordinary equality' in x for x in rows['S10']['required_hypotheses']))
        self.assertTrue(any('Arbitrary joins' in x for x in rows['S06']['required_hypotheses']))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path, help='Write deterministic fixture values on test success.')
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(F03HandoffTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report(), indent=2)+'\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
