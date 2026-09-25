"""Finite illustrations for the F03 theorem agenda, not proofs of its targets.

All arithmetic here is exact over ints/Fractions. General consumer-class and
infinite-family statements are proved only at the elementary scope in the note.
Metadata checks establish consistency of research records, not source validity.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
from typing import Sequence
import unittest

Scalar = int | Q


def rational(value: Scalar) -> Q:
    if isinstance(value, bool) or not isinstance(value, (int, Q)):
        raise TypeError('Only finite exact ints/Fractions are accepted.')
    return Q(value)


def profiles(x: Sequence[Scalar], y: Sequence[Scalar]) -> tuple[tuple[Q, ...], tuple[Q, ...]]:
    if not x or len(x) != len(y):
        raise ValueError('Profiles must have equal positive dimension.')
    return tuple(map(rational, x)), tuple(map(rational, y))


def shortfall(x: Sequence[Scalar], y: Sequence[Scalar]) -> Q:
    a, b = profiles(x, y)
    return max(Q(0), *(u-v for u, v in zip(a, b)))


def projection_witness(x: Sequence[Scalar], y: Sequence[Scalar]) -> int:
    a, b = profiles(x, y)
    return max(range(len(a)), key=lambda i: a[i]-b[i])


def budgeted_loss(x: Scalar, y: Scalar, budget: int) -> Q:
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 0:
        raise ValueError('The copy budget must be a nonnegative integer.')
    return budget * max(Q(0), rational(x)-rational(y))


def dyadic_certificate(delta: Scalar, *, strict: bool = False) -> tuple[int, Q]:
    tolerance = rational(delta)
    if tolerance <= 0:
        raise ValueError('The requested tolerance must be positive.')
    n, bound = 1, Q(1, 2)
    while bound > tolerance or (strict and bound == tolerance):
        n, bound = n+1, bound/2
    return n, bound


def report() -> dict:
    x, y = (5, -2), (4, 1)
    return {
        'task': 'F03', 'scope': 'Elementary illustrations; ambitious targets remain unproved.',
        'profile': {'x': list(x), 'y': list(y), 'loss_x_to_y': str(shortfall(x, y)),
                    'loss_y_to_x': str(shortfall(y, x)), 'attaining_coordinate': projection_witness(x, y)},
        'budgets': {str(b): str(budgeted_loss(1, 0, b)) for b in (0, 1, 2, 8, 100)},
        'tolerance_nontransitivity': {'points': ['0', '3/4', '3/2'], 'tolerance': '1'},
        'dyadic_certificates': {str(t): {'N': dyadic_certificate(t)[0],
                                       'bound': str(dyadic_certificate(t)[1])}
                                for t in (Q(1), Q(1, 2), Q(1, 10), Q(1, 1000))},
        'enumeration': {'profile_grid': [-2, 0, 3], 'dimension': 3,
                        'profile_pairs': 729, 'tested_consumers': 5,
                        'budget_grid': 'integers 0 through 8',
                        'infinite_family': 'analytic argument, not enumerated'},
        'metadata': 'Coherence of 21 sources and five unproved theorem targets only.'
    }


class F03TheoremAgendaTests(unittest.TestCase):
    def test_known_profile(self):
        self.assertEqual(shortfall((5, -2), (4, 1)), 1)
        self.assertEqual(projection_witness((5, -2), (4, 1)), 0)

    def test_asymmetric_directions_and_dominance(self):
        self.assertEqual(shortfall((4, 1), (5, -2)), 3)
        self.assertEqual(shortfall((-4, -2), (0, 1)), 0)

    def test_sample_consumers_respect_structural_bound(self):
        consumers = [min, max, lambda a: sum(a)/3,
                     lambda a: Q(1, 4)*a[0]+Q(3, 4)*a[2],
                     lambda a: max(a[0], min(a[1]+2, a[2]-1))]
        vectors = list(product(map(Q, (-2, 0, 3)), repeat=3))
        for x, y in product(vectors, repeat=2):
            bound = shortfall(x, y)
            for f in consumers:
                self.assertLessEqual(max(Q(0), f(x)-f(y)), bound)

    def test_projection_attains_on_finite_grid(self):
        vectors = list(product((-2, 0, 3), repeat=3))
        for x, y in product(vectors, repeat=2):
            i = projection_witness(x, y)
            self.assertEqual(max(0, x[i]-y[i]), shortfall(x, y))

    def test_no_global_magnitude_cap_is_needed(self):
        for offset in (-(10**80), -1, 0, 1, 10**80):
            self.assertEqual(shortfall((5+offset, -2+offset), (4+offset, 1+offset)), 1)

    def test_budget_formula_against_enumeration(self):
        for x, y, b in product(range(-3, 4), range(-3, 4), range(9)):
            actual = max(max(0, k*x-k*y) for k in range(b+1))
            self.assertEqual(budgeted_loss(x, y, b), actual)

    def test_amplification_family_prefix(self):
        for b in (1, 10, 100, 10**30):
            self.assertEqual(budgeted_loss(1, 0, b), b)
        # Unboundedness is proved by choosing an integer b above any finite cap,
        # not by extrapolating from this finite list.

    def test_tolerance_is_not_an_equivalence_relation(self):
        x, y, z, tolerance = Q(0), Q(3, 4), Q(3, 2), Q(1)
        self.assertLessEqual(abs(x-y), tolerance)
        self.assertLessEqual(abs(y-z), tolerance)
        self.assertGreater(abs(x-z), tolerance)

    def test_dyadic_certificates_have_requested_slack(self):
        for delta in (Q(2), Q(1), Q(1, 2), Q(1, 10), Q(1, 1000), Q(1, 10**50)):
            n, bound = dyadic_certificate(delta)
            self.assertEqual(bound, Q(1, 2**n))
            self.assertLessEqual(bound, delta)
            if n > 1:
                self.assertGreater(2*bound, delta)
            self.assertLess(dyadic_certificate(delta, strict=True)[1], delta)

    def test_reject_invalid_domains(self):
        for x, y in (((), ()), ((1,), (1, 2))):
            with self.assertRaises(ValueError): shortfall(x, y)
        for x in (float('inf'), float('nan'), 0.25, True):
            with self.assertRaises(TypeError): shortfall((x,), (0,))
        for b in (-1, True, Q(1, 2)):
            with self.assertRaises(ValueError): budgeted_loss(1, 0, b)
        for delta in (0, -1):
            with self.assertRaises(ValueError): dyadic_certificate(delta)

    def test_current_source_identities_and_counts(self):
        root = Path(__file__).resolve().parents[1]/'literature'
        d = json.loads((root/'F03_sources.json').read_text(encoding='utf-8'))
        ids = [s['id'] for s in d['sources']]
        # S9 identities remain required; later declared comparisons may be added.
        self.assertTrue({f'S{i:02}' for i in range(1, 22)}.issubset(ids))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(d['core_count'], 8)
        self.assertGreaterEqual(d['supplementary_count'], 13)
        self.assertEqual(len(d['sources']), d['core_count'] + d['supplementary_count'])
        by_id = {s['id']: s for s in d['sources']}
        self.assertIn('Crubille', by_id['S19']['authors'][0])
        self.assertIn('Maccheroni', by_id['S20']['authors'][0])
        self.assertEqual(by_id['S21']['title'], 'Abstract Interpretation Repair')
        for sid in ('S19', 'S20', 'S21'):
            self.assertFalse(by_id[sid]['whole_work_verified'])
            self.assertTrue(by_id[sid]['locators'])

    def test_agenda_does_not_mark_a_target_proved_or_selected(self):
        root = Path(__file__).resolve().parents[1]/'literature'
        d = json.loads((root/'F03_calculus_agenda.json').read_text(encoding='utf-8'))
        self.assertFalse(d['selects_calculus'])
        self.assertFalse(d['passes_gate'])
        self.assertEqual(d['fixed_axioms_added'], [])
        self.assertEqual([t['id'] for t in d['targets']], ['T0', 'T1', 'T2', 'T3', 'T4'])
        self.assertTrue(all(t['status'] == 'unproved-for-eventual-calculus' for t in d['targets']))

    def test_all_agenda_and_import_sources_are_declared(self):
        root = Path(__file__).resolve().parents[1]/'literature'
        src = json.loads((root/'F03_sources.json').read_text(encoding='utf-8'))
        reg = json.loads((root/'F03_import_contracts.json').read_text(encoding='utf-8'))
        agenda = json.loads((root/'F03_calculus_agenda.json').read_text(encoding='utf-8'))
        ids = {s['id'] for s in src['sources']}
        self.assertEqual({s['source_id'] for s in reg['contracts']}, ids)
        for row in agenda['attributes']+agenda['targets']:
            self.assertTrue(set(row['source_ids']) <= ids)
        bib = (root.parent/'references.bib').read_text(encoding='utf-8')
        for s in src['sources'][-3:]: self.assertIn(s['key'], bib)

    def test_report_is_deterministic_and_serializable(self):
        self.assertEqual(json.dumps(report(), sort_keys=True), json.dumps(report(), sort_keys=True))
        self.assertEqual(report()['profile']['loss_x_to_y'], '1')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path, help='Write deterministic evidence after tests pass.')
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(F03TheoremAgendaTests))
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report(), indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
