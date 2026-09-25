"""Finite source-to-phase-one adapters, not an adopted Value Logic calculus.

All mathematical fixtures use exact finite sets and Fraction arithmetic. The
exhaustive searches cover nonempty subsets of {0,1}^n only for n = 1,2,3.
The general statements and source-transfer limits are in literature/01j.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import unittest
from typing import Iterable, Literal, Sequence

Status = Literal['refuted', 'open', 'supported']
RANK: dict[Status, int] = {'refuted': 0, 'open': 1, 'supported': 2}


def abstract_truth(values: Iterable[bool]) -> Status:
    """Classify a nonempty possible-truth set; no empty-evidence vacuity."""
    vals = tuple(values)
    if not vals or any(type(x) is not bool for x in vals):
        raise ValueError('Expected a nonempty family of Boolean possibilities.')
    if all(vals):
        return 'supported'
    if not any(vals):
        return 'refuted'
    return 'open'


def region_status(values: Iterable[Fraction], ceiling: Fraction) -> Status:
    """Restricted current, valid scalar-region atom; not full evidence handling."""
    return abstract_truth(v <= ceiling for v in values)


def required_meet(values: Iterable[Status]) -> Status:
    vals = tuple(values)
    if not vals or any(v not in RANK for v in vals):
        raise ValueError('Expected nonempty meaningful statuses.')
    return min(vals, key=RANK.__getitem__)


def ordinary_argument(values: Iterable[Status]) -> Status:
    """S27 ordinary implication-block fragment, without an active defeater.

    This deliberately is not the rule for every assurance node. Refuting an
    antecedent alone does not refute an otherwise possibly true consequent.
    """
    vals = tuple(values)
    required_meet(vals)  # Same type/nonempty check, different evaluation.
    return 'supported' if all(v == 'supported' for v in vals) else 'open'


def information_leq(a: Status, b: Status) -> bool:
    if a not in RANK or b not in RANK:
        raise ValueError('Unknown meaningful status.')
    return a == b or a == 'open'


def validate_patterns(patterns: Iterable[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    rows = tuple(tuple(row) for row in patterns)
    if not rows or not rows[0]:
        raise ValueError('Expected a nonempty set of positive-dimensional patterns.')
    n = len(rows[0])
    if any(len(row) != n for row in rows):
        raise ValueError('Pattern dimensions disagree.')
    if any(type(x) is not int or x not in (0, 1) for row in rows for x in row):
        raise ValueError('Each coordinate must be the integer zero or one.')
    return tuple(sorted(set(rows)))


def separate_and_joint(patterns: Iterable[Sequence[int]]) -> tuple[Status, Status]:
    rows = validate_patterns(patterns)
    n = len(rows[0])
    marginal = [abstract_truth(bool(row[i]) for row in rows) for i in range(n)]
    return required_meet(marginal), abstract_truth(all(row) for row in rows)


def characterized_gap(patterns: Iterable[Sequence[int]]) -> bool:
    rows = validate_patterns(patterns)
    n = len(rows[0])
    return (1,) * n not in rows and all(any(row[i] for row in rows) for i in range(n))


def nonempty_subsets(items: Sequence) -> Iterable[tuple]:
    for size in range(1, len(items) + 1):
        yield from combinations(items, size)


def joint_improvement(pairs: Iterable[tuple[Fraction, Fraction]], margin: Fraction) -> bool:
    rows = tuple(pairs)
    if not rows:
        raise ValueError('A joint certificate must be nonempty.')
    return all(candidate + margin <= fallback for candidate, fallback in rows)


def marginal_improvement(pairs: Iterable[tuple[Fraction, Fraction]], margin: Fraction) -> bool:
    rows = tuple(pairs)
    if not rows:
        raise ValueError('A marginal certificate must be nonempty.')
    return max(a for a, _ in rows) + margin <= min(b for _, b in rows)


def report() -> dict:
    counts = {}
    for n in (1, 2, 3):
        cases = list(nonempty_subsets(tuple(product((0, 1), repeat=n))))
        discrepancies = [rows for rows in cases if separate_and_joint(rows)[0] != separate_and_joint(rows)[1]]
        counts[str(n)] = {'nonempty_joint_sets': len(cases), 'discrepancies': len(discrepancies)}
    rows = ((Fraction(0), Fraction(1)), (Fraction(1), Fraction(2)))
    return {
        'scope': 'Exact finite adapters; not a source proof system or new core.',
        'exhaustive_joint_patterns': counts,
        'smallest_joint_gap': {
            'patterns': [[1, 0], [0, 1]],
            'separate_status_meet': separate_and_joint(((1, 0), (0, 1)))[0],
            'joint_claim_status': separate_and_joint(((1, 0), (0, 1)))[1],
            'phase_one_frozen_profile_semantics_changed': False,
        },
        'correlated_improvement': {
            'joint_losses': [['0', '1'], ['1', '2']], 'required_margin': '1',
            'joint_guarantee': joint_improvement(rows, Fraction(1)),
            'marginal_endpoint_guarantee': marginal_improvement(rows, Fraction(1)),
        },
        'ordinary_argument_vs_requirements': {
            'premises': ['supported', 'refuted'],
            'ordinary_implication_block': ordinary_argument(('supported', 'refuted')),
            'required_condition_meet': required_meet(('supported', 'refuted')),
        },
        'source_priority_or_global_novelty_proved': False,
    }


class F03PhaseOneBridgeTests(unittest.TestCase):
    def test_region_recovers_supported_refuted_open(self):
        self.assertEqual(region_status([Fraction(0)], Fraction(1)), 'supported')
        self.assertEqual(region_status([Fraction(2)], Fraction(1)), 'refuted')
        self.assertEqual(region_status([Fraction(0), Fraction(2)], Fraction(1)), 'open')

    def test_empty_evidence_is_not_vacuous_support(self):
        with self.assertRaises(ValueError):
            region_status([], Fraction(1))

    def test_invalid_boolean_input(self):
        with self.assertRaises(ValueError):
            abstract_truth([1])

    def test_region_information_narrowing(self):
        points = tuple(map(Fraction, (-2, 0, 2)))
        for region in nonempty_subsets(points):
            for smaller in nonempty_subsets(region):
                for ceiling in map(Fraction, (-3, -1, 1, 3)):
                    self.assertTrue(information_leq(region_status(region, ceiling), region_status(smaller, ceiling)))

    def test_information_order_is_not_conjunction_order(self):
        self.assertTrue(information_leq('open', 'refuted'))
        self.assertLess(RANK['refuted'], RANK['open'])
        self.assertFalse(information_leq('refuted', 'supported'))

    def test_joint_characterization_exhaustive(self):
        for n in (1, 2, 3):
            for rows in nonempty_subsets(tuple(product((0, 1), repeat=n))):
                separate, joint = separate_and_joint(rows)
                self.assertEqual(separate != joint, characterized_gap(rows))
                if separate != joint:
                    self.assertEqual((separate, joint), ('open', 'refuted'))

    def test_exhaustive_counts(self):
        self.assertEqual(report()['exhaustive_joint_patterns'], {
            '1': {'nonempty_joint_sets': 3, 'discrepancies': 0},
            '2': {'nonempty_joint_sets': 15, 'discrepancies': 2},
            '3': {'nonempty_joint_sets': 255, 'discrepancies': 90},
        })

    def test_product_fragment_agrees(self):
        for n in (1, 2, 3):
            for marginals in product(((0,), (1,), (0, 1)), repeat=n):
                separate, joint = separate_and_joint(product(*marginals))
                self.assertEqual(separate, joint)

    def test_smallest_joint_gap(self):
        self.assertEqual(separate_and_joint(((1, 0), (0, 1))), ('open', 'refuted'))

    def test_shared_support_and_single_refutation_agree(self):
        self.assertEqual(separate_and_joint(((1, 1),)), ('supported', 'supported'))
        self.assertEqual(separate_and_joint(((0, 0), (0, 1))), ('refuted', 'refuted'))

    def test_pattern_validation(self):
        for rows in ((), ((),), ((0,), (0, 1)), ((1, 2),), ((False, 1),)):
            with self.assertRaises(ValueError):
                separate_and_joint(rows)

    def test_pattern_duplicate_invariance(self):
        self.assertEqual(separate_and_joint(((1, 0), (0, 1), (1, 0))), ('open', 'refuted'))

    def test_assurance_not_required_meet(self):
        self.assertEqual(ordinary_argument(('supported', 'refuted')), 'open')
        self.assertEqual(required_meet(('supported', 'refuted')), 'refuted')

    def test_assurance_positive_fragment(self):
        self.assertEqual(ordinary_argument(('supported', 'supported')), 'supported')
        self.assertEqual(ordinary_argument(('supported', 'open')), 'open')
        for values in ((), ('undefined',)):
            with self.assertRaises(ValueError):
                ordinary_argument(values)

    def test_correlated_difference_beats_marginal_projection(self):
        rows = ((Fraction(0), Fraction(1)), (Fraction(1), Fraction(2)))
        self.assertTrue(joint_improvement(rows, Fraction(1)))
        self.assertFalse(marginal_improvement(rows, Fraction(1)))

    def test_marginal_bound_is_sufficient(self):
        candidates = tuple(product(map(Fraction, (-1, 0, 1)), repeat=2))
        for rows in nonempty_subsets(candidates[:5]):
            for margin in map(Fraction, (0, 1)):
                if marginal_improvement(rows, margin):
                    self.assertTrue(joint_improvement(rows, margin))

    def test_signed_translation_invariance(self):
        rows = ((Fraction(0), Fraction(1)), (Fraction(1), Fraction(2)))
        for shift in (Fraction(-10**50), Fraction(10**50)):
            shifted = tuple((a + shift, b + shift) for a, b in rows)
            self.assertEqual(joint_improvement(rows, Fraction(1)), joint_improvement(shifted, Fraction(1)))
            self.assertEqual(marginal_improvement(rows, Fraction(1)), marginal_improvement(shifted, Fraction(1)))

    def test_source_register_retains_old_and_new_identities(self):
        root = Path(__file__).resolve().parents[1] / 'literature'
        data = json.loads((root / 'F03_sources.json').read_text(encoding='utf-8'))
        sources = data['sources']
        self.assertEqual({r['id'] for r in sources}, {f'S{i:02}' for i in range(1, 29)})
        self.assertEqual(len(sources), 28)
        self.assertEqual(sum(r['role'] == 'core' for r in sources), 8)
        self.assertEqual(data['supplementary_count'], 20)
        for r in sources[21:]:
            self.assertFalse(r['whole_work_verified'])
            self.assertTrue(r['locators'])
            self.assertTrue(r['hypotheses'])
        contracts = json.loads((root / 'F03_import_contracts.json').read_text(encoding='utf-8'))
        self.assertEqual({r['source_id'] for r in contracts['contracts']}, {r['id'] for r in sources})
        self.assertFalse(contracts['passes_gate'])
        self.assertFalse(contracts['selects_calculus'])

    def test_no_foundation_choice_hidden_in_audit(self):
        root = Path(__file__).resolve().parents[1] / 'literature'
        agenda = json.loads((root / 'F03_calculus_agenda.json').read_text(encoding='utf-8'))
        self.assertFalse(agenda['selects_calculus'])
        self.assertFalse(agenda['passes_gate'])
        self.assertEqual(agenda['fixed_axioms_added'], [])

    def test_no_empty_improvement_certificate(self):
        for fun in (joint_improvement, marginal_improvement):
            with self.assertRaises(ValueError):
                fun([], Fraction(0))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path, help='Write the exact finite report after passing tests.')
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(F03PhaseOneBridgeTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful() and args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report(), indent=2) + '\n', encoding='utf-8')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
