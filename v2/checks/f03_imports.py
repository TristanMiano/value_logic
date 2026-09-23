"""Exact finite witnesses for F03's literature-import boundaries.

These checks do not prove the cited infinite-domain theorems, validate citations
against the network, or implement the prospective phase-two reasoner.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
GRID = tuple(Q(i, 2) for i in range(-2, 3))


def capped_distance(x: Q, y: Q) -> Q:
    return min(Q(1), abs(x - y))


def product_distance(x: tuple[Q, Q], y: tuple[Q, Q]) -> Q:
    return min(Q(1), sum((capped_distance(a, b) for a, b in zip(x, y)), Q(0)))


def dot(x: tuple[Q, ...], y: tuple[Q, ...]) -> Q:
    if len(x) != len(y):
        raise ValueError("dot product requires matching dimensions")
    return sum((a * b for a, b in zip(x, y)), Q(0))


def matvec(p: tuple[tuple[Q, ...], ...], h: tuple[Q, ...]) -> tuple[Q, ...]:
    if any(len(row) != len(h) for row in p):
        raise ValueError("kernel and continuation dimensions do not agree")
    return tuple(dot(row, h) for row in p)


def rowmat(mu: tuple[Q, ...], p: tuple[tuple[Q, ...], ...]) -> tuple[Q, ...]:
    if len(mu) != len(p) or not p or not p[0]:
        raise ValueError("nonempty matrix and matching input dimensions required")
    if any(len(row) != len(p[0]) for row in p):
        raise ValueError("ragged matrix")
    return tuple(sum((mu[i] * p[i][j] for i in range(len(mu))), Q(0))
                 for j in range(len(p[0])))


def matrix_product(p: tuple[tuple[Q, ...], ...], q: tuple[tuple[Q, ...], ...]):
    return tuple(rowmat(row, q) for row in p)


def feasible(menu: tuple[tuple[Q, ...], ...], budget: tuple[Q, ...]) -> bool:
    if any(len(option) != len(budget) for option in menu):
        raise ValueError("budget and option dimensions do not agree")
    return any(all(x <= b for x, b in zip(option, budget)) for option in menu)


def minkowski(f: tuple[tuple[Q, ...], ...], g: tuple[tuple[Q, ...], ...]):
    if f and g and any(len(x) != len(y) for x in f for y in g):
        raise ValueError("cost dimensions do not agree")
    return tuple(tuple(a + b for a, b in zip(x, y)) for x in f for y in g)


def scalarized(menu: tuple[tuple[Q, ...], ...], weight: tuple[Q, ...]) -> Q:
    if not menu or any(w < 0 for w in weight):
        raise ValueError("nonempty menu and nonnegative weights required")
    return min(dot(x, weight) for x in menu)


def staircase(n: int) -> tuple[tuple[Q, Q], ...]:
    if n <= 0:
        raise ValueError("positive staircase resolution required")
    return tuple((Q(k, n), 1 - Q(k + 1, n)) for k in range(n))


class F03ImportTests(unittest.TestCase):
    def test_interval_square_outer_bound_not_exact(self):
        self.assertEqual({x * x for x in (Q(-1), Q(1))}, {Q(1)})
        self.assertIn(Q(0), {x * x for x in GRID})

    def test_possible_outcome_outer_bound_polarity(self):
        outcomes = (Q(1), Q(2))
        enclosure = (Q(0), Q(3))
        self.assertGreaterEqual(min(outcomes), min(enclosure))
        self.assertTrue(all(enclosure[0] <= x <= enclosure[1] for x in outcomes))

    def test_guarantee_outer_approximation_not_membership_certificate(self):
        actual = ((Q(2),),)
        optimistic = ((Q(1),),)
        self.assertTrue(feasible(optimistic, (Q(1),)))
        self.assertFalse(feasible(actual, (Q(1),)))

    def test_addition_fails_max_metric_common_error(self):
        self.assertGreater(abs((Q(1) + 1) - (Q(0) + 0)), max(Q(1), Q(1)))

    def test_addition_sum_error_bound(self):
        for a, b, c, d in product(GRID, repeat=4):
            self.assertLessEqual(abs(a + b - c - d), abs(a - c) + abs(b - d))

    def test_min_max_are_max_metric_nonexpansive(self):
        for a, b, c, d in product(GRID, repeat=4):
            bound = max(abs(a - c), abs(b - d))
            self.assertLessEqual(abs(min(a, b) - min(c, d)), bound)
            self.assertLessEqual(abs(max(a, b) - max(c, d)), bound)

    def test_fixed_mixture_is_nonexpansive(self):
        for weight in (Q(0), Q(1, 3), Q(1)):
            for a, b, c, d in product(GRID, repeat=4):
                change = weight * (a - c) + (1 - weight) * (b - d)
                self.assertLessEqual(abs(change), max(abs(a - c), abs(b - d)))

    def test_changing_mixture_not_covered_by_input_only_bound(self):
        self.assertEqual(max(abs(Q(0) - 0), abs(Q(10) - 10)), 0)
        self.assertNotEqual(Q(0) * 0 + 1 * 10, Q(1) * 0 + 0 * 10)

    def test_capped_distance_triangle_and_separation(self):
        for a, b, c in product(GRID, repeat=3):
            self.assertLessEqual(capped_distance(a, c), capped_distance(a, b) + capped_distance(b, c))
            self.assertEqual(capped_distance(a, b) == 0, a == b)

    def test_capped_product_triangle(self):
        pairs = tuple(product(GRID, repeat=2))
        for a, b, c in product(pairs, repeat=3):
            self.assertLessEqual(product_distance(a, c), product_distance(a, b) + product_distance(b, c))

    def test_addition_for_capped_sum_lifting(self):
        for a, b, c, d in product(GRID, repeat=4):
            self.assertLessEqual(capped_distance(a + b, c + d), product_distance((a, b), (c, d)))

    def test_capping_does_not_bound_the_carrier(self):
        self.assertEqual(capped_distance(Q(0), Q(10**20)), 1)
        self.assertGreater(Q(10**20), 1)
        self.assertEqual(capped_distance(Q(0), Q(1, 5)), Q(1, 5))

    def test_forward_backward_duality(self):
        p = ((Q(1, 2), Q(1, 4)), (Q(1, 3), Q(2, 3)))
        for h in product(GRID, repeat=2):
            for mu in ((Q(1, 2), Q(1, 2)), (Q(1), Q(0))):
                self.assertEqual(dot(rowmat(mu, p), h), dot(mu, matvec(p, h)))

    def test_affine_kernel_composition(self):
        p = ((Q(1, 2), Q(1, 2)), (Q(0), Q(1)))
        q = ((Q(1), Q(0)), (Q(1, 3), Q(2, 3)))
        r, s = (Q(1), Q(-1)), (Q(2), Q(3))
        for h in product(GRID, repeat=2):
            inner = tuple(a + b for a, b in zip(s, matvec(q, h)))
            left = tuple(a + b for a, b in zip(r, matvec(p, inner)))
            right = tuple(a + b + c for a, b, c in zip(r, matvec(p, s), matvec(matrix_product(p, q), h)))
            self.assertEqual(left, right)

    def test_substochastic_shift_differs_from_stochastic_shift(self):
        for h, c in product(GRID, repeat=2):
            self.assertEqual(Q(1, 2) * (h + c) - Q(1, 2) * h, c / 2)
        self.assertNotEqual(Q(1, 2), Q(1))

    def test_stochastic_shift_law(self):
        p = ((Q(1, 3), Q(2, 3)), (Q(1), Q(0)))
        h = (Q(4), Q(-3))
        for c in GRID:
            self.assertEqual(matvec(p, tuple(x + c for x in h)), tuple(x + c for x in matvec(p, h)))

    def test_agh_finite_sample_majorants_not_finite_representation_claim(self):
        f = lambda x: max(x[0] - 1, min(x[0] + 1, x[1] + Q(1, 2)))
        pairs = tuple(product(GRID, repeat=2))
        for x, y in product(pairs, repeat=2):
            self.assertLessEqual(f(x), max(a - b for a, b in zip(x, y)) + f(y))
        for x in pairs:
            # Equality uses y=x; no claim that a fixed external finite y set works everywhere.
            self.assertEqual(f(x), max(a - b for a, b in zip(x, x)) + f(x))

    def test_additive_homogeneity_does_not_imply_positive_homogeneity(self):
        f = lambda x: 1 + x
        self.assertEqual(f(Q(2) + 3), f(Q(2)) + 3)
        self.assertNotEqual(f(Q(2) * 2), 2 * f(Q(2)))

    def test_signed_cost_unit_not_top(self):
        negative = ((Q(-1),),)
        unit = ((Q(0),),)
        self.assertTrue(feasible(negative + unit, (Q(-1),)))
        self.assertFalse(feasible(unit, (Q(-1),)))

    def test_minkowski_multiplication_not_idempotent(self):
        menu = ((Q(1),),)
        self.assertTrue(feasible(menu, (Q(1),)))
        self.assertFalse(feasible(minkowski(menu, menu), (Q(1),)))

    def test_minkowski_finite_distributivity_and_unit(self):
        f = ((Q(0), Q(2)), (Q(2), Q(0)))
        g, h = ((Q(1), Q(3)),), ((Q(4), Q(1)),)
        self.assertEqual(set(minkowski(f, g + h)), set(minkowski(f, g) + minkowski(f, h)))
        self.assertEqual(minkowski(f, ((Q(0), Q(0)),)), f)
        self.assertEqual(minkowski(f, ()), ())

    def test_staircase_covers_sampled_upper_triangle(self):
        boundary = tuple((Q(k, 20), 1 - Q(k, 20)) for k in range(21))
        for n in range(1, 16):
            for point in boundary:
                self.assertTrue(feasible(staircase(n), point))
            self.assertTrue(all(sum(x) == 1 - Q(1, n) for x in staircase(n)))

    def test_staircase_excludes_each_sampled_outside_point_eventually(self):
        for point in product((Q(k, 10) for k in range(10)), repeat=2):
            if sum(point) < 1:
                self.assertFalse(feasible(staircase(20), point))

    def test_scalarization_collision(self):
        f = ((Q(0), Q(2)), (Q(2), Q(0)))
        z = (Q(3, 2), Q(3, 2))
        for weight in product((Q(k, 4) for k in range(9)), repeat=2):
            self.assertEqual(scalarized(f, weight), scalarized(f + (z,), weight))
        self.assertFalse(feasible(f, z))
        self.assertTrue(feasible(f + (z,), z))

    def test_boundary_weight_can_choose_dominated_option(self):
        self.assertEqual(dot((Q(0), Q(0)), (Q(1), Q(0))), dot((Q(0), Q(1)), (Q(1), Q(0))))

    def test_lottery_expected_budget_does_not_mean_pathwise_budget(self):
        f = ((Q(0), Q(2)), (Q(2), Q(0)))
        budget = (Q(3, 2), Q(3, 2))
        mean = tuple((x + y) / 2 for x, y in zip(*f))
        self.assertTrue(feasible((mean,), budget))
        self.assertFalse(feasible(f, budget))

    def test_shared_parameter_vs_rectangular_relaxation(self):
        shared = min(t + (1 - t) for t in (Q(0), Q(1)))
        independent_choices = min(a + (1 - b) for a, b in product((Q(0), Q(1)), repeat=2))
        self.assertEqual((shared, independent_choices), (1, 0))
        self.assertLessEqual(independent_choices, shared)

    def test_quantitative_substitution_requires_its_side_premise(self):
        a, b, epsilon = Q(0), Q(1, 10), Q(1, 10)
        self.assertLessEqual(capped_distance(a, b), epsilon)
        self.assertGreater(capped_distance(10 * a, 10 * b), epsilon)

    def test_zero_fuzzy_distance_does_not_imply_equality_without_separation(self):
        self.assertNotEqual("a", "b")
        zero_distance = lambda x, y: Q(0)
        self.assertEqual(zero_distance("a", "b"), 0)

    def test_bad_dimensions_rejected(self):
        with self.assertRaises(ValueError):
            matvec(((Q(1), Q(0)),), (Q(1),))
        with self.assertRaises(ValueError):
            feasible(((Q(1),),), (Q(1), Q(2)))
        with self.assertRaises(ValueError):
            staircase(0)

    def test_source_manifest_and_bibliography_integrity(self):
        manifest = json.loads((ROOT / "v2/literature/F03_sources.json").read_text(encoding="utf-8"))
        sources = manifest["sources"]
        self.assertEqual(len(sources), manifest["core_count"] + manifest["supplementary_count"])
        self.assertEqual(len({s["id"] for s in sources}), len(sources))
        self.assertTrue({f"S{i:02}" for i in range(1, 12)} <= {s["id"] for s in sources})
        self.assertEqual(sum(s["role"] == "core" for s in sources), 8)
        bib = (ROOT / "v2/references.bib").read_text(encoding="utf-8")
        keys = re.findall(r"@\w+\{([^,]+),", bib)
        self.assertEqual(len(keys), len(set(keys)))
        for source in sources:
            self.assertIn(source["key"], keys)
            self.assertTrue(source["locators"])
            self.assertTrue(source["hypotheses"])
            self.assertFalse(source["whole_work_verified"])
            for url in source["primary_urls"]:
                self.assertEqual(urlparse(url).scheme, "https")
                self.assertTrue(urlparse(url).netloc)


def report(test_count: int) -> dict:
    return {
        "task": "F03", "status": "partial literature audit; no adopted calculus or gate pass",
        "test_count": test_count, "base_commit": "65e91d9b46bf61566160de9dbdcb4a1a98b33f02",
        "witnesses": {
            "addition_common_input_error": "1", "addition_output_error": "2",
            "substochastic_common_shift_factor": "1/2",
            "signed_cost_top_counterexample": {"unit_lower_endpoint": "0", "other_lower_endpoint": "-1"},
            "Minkowski_idempotence_counterexample": {"input_lower_endpoint": "1", "square_lower_endpoint": "2"},
            "same_scalarized_menu_hard_budget": ["3/2", "3/2"],
            "shared_parameter_value": "1", "rectangular_relaxation_value": "0",
            "naive_substitution_input_distance": "1/10", "output_distance": "1"
        },
        "enumeration": {
            "scalar_grid": [str(x) for x in GRID],
            "four_scalar_tuples_per_grid_check": len(GRID) ** 4,
            "capped_product_triangle_triples": len(GRID) ** 6,
            "staircase_resolutions": [1, 15], "staircase_boundary_samples_per_resolution": 21,
            "scalarization_weight_pairs": 81
        },
        "not_established_by_tests": [
            "unrestricted cited theorems", "infinite-domain closure or representation",
            "source authenticity or literature novelty", "F03 L60 completion", "full repository validation"
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write deterministic results only after all tests pass")
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F03ImportTests))
    if not result.wasSuccessful():
        return 1
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report(result.testsRun), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
