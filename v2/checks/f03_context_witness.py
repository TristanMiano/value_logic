"""Finite source-interface checks, not a general relational or RLL prover.

Relations use exact fractions in [0,1]. Extended distances use None for
positive infinity. All probability/potential inputs in this fixture are finite.
Run from the repository root, optionally with --json OUTPUT.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import unittest

Q = int | F
Matrix = tuple[tuple[F, ...], ...]
ExtendedMatrix = tuple[tuple[F | None, ...], ...]


def rational(value: Q) -> F:
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise ValueError('Exact int/Fraction input required, not a float or bool.')
    return F(value)


def relation(rows: tuple[tuple[Q, ...], ...]) -> Matrix:
    n = len(rows)
    if any(len(row) != n for row in rows):
        raise ValueError('Relation must be square.')
    result = tuple(tuple(rational(x) for x in row) for row in rows)
    if any(x < 0 or x > 1 for row in result for x in row):
        raise ValueError('Fuzzy relation entries must lie in [0,1].')
    return result


def assignments(domain: Matrix, target: Matrix) -> tuple[tuple[int, ...], ...]:
    """Enumerate all relation-preserving maps, including the empty domain."""
    domain, target = relation(domain), relation(target)
    return tuple(t for t in product(range(len(target)), repeat=len(domain))
                 if all(target[t[i]][t[j]] <= domain[i][j]
                        for i in range(len(domain)) for j in range(len(domain))))


def probability(values: tuple[Q, ...]) -> tuple[F, ...]:
    result = tuple(rational(x) for x in values)
    if not result or any(x < 0 for x in result) or sum(result) != 1:
        raise ValueError('Expected a nonempty exact probability vector.')
    return result


def extended_metric(rows: tuple[tuple[Q | None, ...], ...]) -> ExtendedMatrix:
    """Validate a finite extended pseudometric; None is +infinity."""
    n = len(rows)
    if not n or any(len(row) != n for row in rows):
        raise ValueError('Expected a nonempty square distance matrix.')
    d = tuple(tuple(None if x is None else rational(x) for x in row) for row in rows)
    for i in range(n):
        if d[i][i] != 0:
            raise ValueError('A pseudometric needs zero diagonal.')
        for j in range(n):
            if d[i][j] != d[j][i] or (d[i][j] is not None and d[i][j] < 0):
                raise ValueError('Distances must be symmetric and nonnegative.')
            for k in range(n):
                a, b = d[i][k], d[k][j]
                if a is not None and b is not None:
                    if d[i][j] is None or d[i][j] > a + b:
                        raise ValueError('Extended triangle inequality violated.')
    return d


def finite_components(d: ExtendedMatrix) -> tuple[tuple[int, ...], ...]:
    d = extended_metric(d)
    todo = set(range(len(d)))
    groups = []
    while todo:
        i = min(todo)
        component = tuple(j for j in sorted(todo) if d[i][j] is not None)
        groups.append(component)
        todo.difference_update(component)
    return tuple(groups)


def finite_coupling(d: ExtendedMatrix, mu: tuple[Q, ...], nu: tuple[Q, ...]) -> Matrix | None:
    """Return a finite-cost feasible coupling, or None for component imbalance.

    The returned coupling is not asserted to minimize transport cost.
    """
    d = extended_metric(d)
    mu, nu = probability(mu), probability(nu)
    if len(mu) != len(d) or len(nu) != len(d):
        raise ValueError('Probability and distance dimensions differ.')
    pi = [[F(0) for _ in mu] for _ in mu]
    for group in finite_components(d):
        mass = sum(mu[i] for i in group)
        if mass != sum(nu[i] for i in group):
            return None
        if mass:
            for i in group:
                for j in group:
                    pi[i][j] = mu[i] * nu[j] / mass
    return tuple(tuple(row) for row in pi)


def transport_cost(d: ExtendedMatrix, pi: Matrix) -> F | None:
    """Exact finite sum, with 0 * infinity = 0 and None for infinite cost."""
    d = extended_metric(d)
    if len(pi) != len(d) or any(len(row) != len(d) for row in pi):
        raise ValueError('Coupling shape does not match distances.')
    pi = tuple(tuple(rational(x) for x in row) for row in pi)
    if any(x < 0 for row in pi for x in row):
        raise ValueError('Coupling weights must be nonnegative.')
    total = F(0)
    for i, row in enumerate(pi):
        for j, weight in enumerate(row):
            if weight:
                if d[i][j] is None:
                    return None
                total += weight * d[i][j]
    return total


def optimality_certificate(d: ExtendedMatrix, mu: tuple[Q, ...], nu: tuple[Q, ...],
                           pi: Matrix, potential: tuple[Q, ...], claimed: Q | None) -> bool:
    """Check S12's finite-potential feasibility/optimality conditions numerically.

    This does not emit a proof in Rational Lawvere Logic or find a witness.
    """
    d = extended_metric(d)
    mu, nu = probability(mu), probability(nu)
    potential = tuple(rational(x) for x in potential)
    n = len(d)
    if len(mu) != n or len(nu) != n or len(potential) != n:
        raise ValueError('Certificate dimensions differ.')
    if any(x < 0 for x in potential):
        raise ValueError('This source interface uses nonnegative finite potentials.')
    cost = transport_cost(d, pi)
    if any(sum(row) != mu[i] for i, row in enumerate(pi)):
        return False
    if any(sum(pi[i][j] for i in range(n)) != nu[j] for j in range(n)):
        return False
    if any(d[i][j] is not None and abs(potential[i] - potential[j]) > d[i][j]
           for i in range(n) for j in range(n)):
        return False
    dual = abs(sum(potential[i] * (mu[i] - nu[i]) for i in range(n)))
    if cost is None or claimed is None:
        return False  # A finite dual cannot dominate positive infinity.
    return dual >= rational(claimed) >= cost


D3 = relation(((0, F(1, 2), 1), (F(1, 2), 0, F(1, 2)), (1, F(1, 2), 0)))
D2 = relation(((0, 1), (1, 0)))
DISCONNECTED = extended_metric(((0, 1, None, None), (1, 0, None, None),
                               (None, None, 0, 2), (None, None, 2, 0)))


class F03ContextWitnessTests(unittest.TestCase):
    def test_full_context_has_only_constant_maps(self):
        self.assertEqual(assignments(D3, D2), ((0, 0, 0), (1, 1, 1)))
        self.assertTrue(all(t[0] == t[2] for t in assignments(D3, D2)))

    def test_pruned_context_admits_a_refuting_assignment(self):
        small = assignments(D2, D2)
        self.assertEqual(len(small), 4)
        self.assertIn((0, 1), small)

    def test_restriction_is_not_surjective(self):
        image = {(t[0], t[2]) for t in assignments(D3, D2)}
        smaller = set(assignments(D2, D2))
        self.assertLess(image, smaller)
        self.assertEqual(smaller - image, {(0, 1), (1, 0)})

    def test_unconstrained_extra_variable_extends_every_map(self):
        target = relation(((F(1, 2), 1), (F(1, 4), F(3, 4))))
        old = relation(((1,),))
        new = relation(((1, 1), (1, 1)))
        self.assertEqual({t[:1] for t in assignments(new, target)},
                         set(assignments(old, target)))
        self.assertEqual(len(assignments(new, target)), 4)

    def test_diagonal_constraint_can_destroy_extension(self):
        target = relation(((F(1, 2),),))
        self.assertEqual(assignments((), target), ((),))
        self.assertEqual(assignments(relation(((0,),)), target), ())
        self.assertEqual(assignments(relation(((1,),)), target), ((0,),))

    def test_relation_validation_is_exact_and_square(self):
        for bad in (((F(3, 2),),), ((-1,),), ((0, 1),), ((0.0,),)):
            with self.assertRaises(ValueError):
                relation(bad)
        self.assertEqual(assignments((), ()), ((),))
        self.assertEqual(assignments(relation(((0,),)), ()), ())

    def test_metric_contexts_really_satisfy_triangle(self):
        self.assertEqual(extended_metric(D3), D3)
        self.assertEqual(extended_metric(D2), D2)
        for bad in (((0, 1), (2, 0)), ((0, 1, None), (1, 0, 1), (None, 1, 0))):
            with self.assertRaises(ValueError):
                extended_metric(bad)

    def test_finite_distance_positive_certificates(self):
        pi = ((F(0), F(1)), (F(0), F(0)))
        for distance in (F(0), F(1, 3), F(7), F(10**50)):
            d = extended_metric(((0, distance), (distance, 0)))
            self.assertTrue(optimality_certificate(d, (1, 0), (0, 1), pi,
                                                   (distance, 0), distance))

    def test_infinite_transport_has_no_finite_potential_certificate(self):
        d = extended_metric(((0, None), (None, 0)))
        pi = ((F(0), F(1)), (F(0), F(0)))
        self.assertIsNone(transport_cost(d, pi))
        self.assertIsNone(finite_coupling(d, (1, 0), (0, 1)))
        for a, b, k in product((0, 1, 100, 10**50), repeat=3):
            self.assertFalse(optimality_certificate(d, (1, 0), (0, 1), pi, (a, b), k))
        self.assertFalse(optimality_certificate(d, (1, 0), (0, 1), pi, (0, 0), None))

    def test_tampered_certificates_are_rejected(self):
        pi = ((F(0), F(1)), (F(0), F(0)))
        d = extended_metric(((0, 3), (3, 0)))
        for k in (0, 2, 4):
            self.assertFalse(optimality_certificate(d, (1, 0), (0, 1), pi, (3, 0), k))
        self.assertFalse(optimality_certificate(d, (1, 0), (0, 1), pi, (4, 0), 3))
        self.assertFalse(optimality_certificate(d, (1, 0), (0, 1),
                                               ((F(1), F(0)), (F(0), F(0))), (3, 0), 3))

    def test_balanced_components_produce_feasible_finite_coupling(self):
        mu, nu = (F(1, 2), 0, F(1, 4), F(1, 4)), (F(1, 4), F(1, 4), 0, F(1, 2))
        pi = finite_coupling(DISCONNECTED, mu, nu)
        self.assertIsNotNone(pi)
        self.assertEqual(tuple(map(sum, pi)), tuple(mu))
        self.assertEqual(tuple(sum(row[j] for row in pi) for j in range(4)), tuple(nu))
        self.assertEqual(transport_cost(DISCONNECTED, pi), F(3, 4))
        self.assertEqual(finite_components(DISCONNECTED), ((0, 1), (2, 3)))

    def test_unbalanced_components_have_no_finite_coupling(self):
        self.assertIsNone(finite_coupling(DISCONNECTED, (1, 0, 0, 0), (0, 0, 0, 1)))

    def test_zero_mass_component_and_zero_times_infinity(self):
        pi = finite_coupling(DISCONNECTED, (1, 0, 0, 0), (0, 1, 0, 0))
        self.assertEqual(transport_cost(DISCONNECTED, pi), 1)
        self.assertEqual(pi[2:], ((F(0),) * 4, (F(0),) * 4))

    def test_feasible_construction_is_not_necessarily_optimal(self):
        pi = finite_coupling(D2, (F(1, 2), F(1, 2)), (F(1, 2), F(1, 2)))
        self.assertEqual(transport_cost(D2, pi), F(1, 2))
        diagonal = ((F(1, 2), F(0)), (F(0), F(1, 2)))
        self.assertEqual(transport_cost(D2, diagonal), 0)

    def test_coupling_input_validation(self):
        for mu in ((1, 1), (F(-1), F(2)), (F(1, 2),), (0.5, 0.5)):
            with self.assertRaises(ValueError):
                finite_coupling(D2, mu, (1, 0))
        with self.assertRaises(ValueError):
            transport_cost(D2, ((F(-1), 2), (0, 0)))
        # Reject an invalid later entry even when an earlier term is infinite.
        with self.assertRaises(ValueError):
            transport_cost(((0, None), (None, 0)), ((0, 1), (-1, 1)))


def report() -> dict:
    return {
        'task': 'F03', 'session': '2026-09-24-S8',
        'scope': 'Finite exact source-interface fixtures, not a complete prover.',
        'full_context_assignments': [list(t) for t in assignments(D3, D2)],
        'pruned_context_assignments': [list(t) for t in assignments(D2, D2)],
        'nonextendible_assignments': [[0, 1], [1, 0]],
        'balanced_components': [list(c) for c in finite_components(DISCONNECTED)],
        'certificate_boundaries': {
            'finite_distances_tested': ['0', '1/3', '7', str(10**50)],
            'infinite_input': 'Cost is +infinity; every finite potential gives finite dual.',
            'finite_potential_triples_checked': 64,
            'arbitrary_finite_potential_impossibility': 'Analytic proof in note, not inferred from grid.',
            'constructed_coupling_is_optimal': False},
        'test_count': 15,
        'novelty_claim': False, 'selected_core': False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(F03ContextWitnessTests))
    if not result.wasSuccessful():
        return 1
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report(), indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
