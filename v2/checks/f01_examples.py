"""Exact, finite F01 witnesses; not a phase-two calculus or reasoner.

Run from the repository root:
    python -m v2.checks.f01_examples --json v2/checks/F01_results.json
Only the Python standard library is required. All arithmetic is rational.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from typing import Callable, Sequence
import unittest

Number = int | F


def mean(values: Sequence[Number], weights: Sequence[Number] | None = None) -> F:
    """Evaluate a finite, explicitly normalized weighted mean."""
    if not values:
        raise ValueError("A mean requires at least one value.")
    if weights is None:
        weights = [F(1, len(values))] * len(values)
    if len(weights) != len(values):
        raise ValueError("Values and weights must have matching lengths.")
    if any(w < 0 for w in weights) or sum(weights) != 1:
        raise ValueError("Weights must be nonnegative and sum to one.")
    return sum((F(x) * F(w) for x, w in zip(values, weights)), F(0))


def polynomial_case(a: F, rate: F, budget: Number = 8, tolerance: F = F(1, 100)) -> dict:
    if a <= 0 or rate < 0 or budget < 0 or tolerance < 0:
        raise ValueError("The fixture requires positive amplitude and nonnegative costs/bounds.")
    inputs = (-a, a)
    reference = tuple(z + z**3 for z in inputs)
    cheap = inputs
    accurate = reference
    risks = {
        "cheap": mean([abs(x - y) for x, y in zip(cheap, reference)]),
        "accurate": mean([abs(x - y) for x, y in zip(accurate, reference)]),
    }
    costs = {"cheap": F(1), "accurate": F(8)}
    combined = {name: risks[name] + rate * costs[name] for name in risks}
    feasible = [name for name in risks if risks[name] <= tolerance and costs[name] <= budget]
    selected = [] if not feasible else [name for name in feasible if combined[name] == min(combined[x] for x in feasible)]
    return {"risk": risks, "combined": combined, "feasible": feasible, "selected": selected}


def joint_expectation(counts: Sequence[Sequence[int]], fn: Callable[[int, int], Number]) -> F:
    values = (-1, 0, 1)
    if len(counts) != 3 or any(len(row) != 3 for row in counts):
        raise ValueError("This witness uses a three-by-three table.")
    total = sum(map(sum, counts))
    if total <= 0 or any(x < 0 for row in counts for x in row):
        raise ValueError("Counts must be nonnegative, with positive total.")
    return sum((F(counts[i][j], total) * fn(x, y)
                for i, x in enumerate(values) for j, y in enumerate(values)), F(0))


def best_decoder_loss(observed_modulus: int, target_modulus: int) -> F:
    """Enumerate every deterministic map from one residue alphabet to another."""
    if observed_modulus not in (2, 3) or target_modulus not in (2, 3):
        raise ValueError("Only the two declared toy representations are in this fixture.")
    losses = []
    for decoder in product(range(target_modulus), repeat=observed_modulus):
        errors = sum(decoder[n % observed_modulus] != n % target_modulus for n in range(6))
        losses.append(F(errors, 6))
    return min(losses)


def squash(x: Number) -> F:
    x = F(x)
    return x / (1 + abs(x))


def unsquash(y: Number) -> F:
    y = F(y)
    if abs(y) >= 1:
        raise ValueError("The inverse is defined only on (-1, 1).")
    return y / (1 - abs(y))


def transported_add(a: Number, b: Number) -> F:
    return squash(unsquash(a) + unsquash(b))


def signal_value(policy: tuple[int, int], accuracy: F) -> F:
    if len(policy) != 2 or any(action not in (0, 1) for action in policy):
        raise ValueError("A policy chooses one of two actions for each signal.")
    if not F(1, 2) <= accuracy <= 1:
        raise ValueError("This fixture declares symmetric accuracy in [1/2, 1].")
    result = F(0)
    for state, signal in product((0, 1), repeat=2):
        probability = F(1, 2) * (accuracy if state == signal else 1 - accuracy)
        result += probability * (3 if policy[signal] == state else -1)
    return result


X = (F(3), F(-1))
Y = (F(-1), F(3))
PLUS = ((3, 0, 3), (1, 4, 1), (2, 2, 2))
MINUS = ((1, 4, 1), (3, 0, 3), (2, 2, 2))
EVEN = ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0))
ODD = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1))


class F01FixtureTests(unittest.TestCase):
    def test_e01_polynomial_errors(self) -> None:
        for a in (F(1, 10), F(1, 2), F(1), F(2)):
            result = polynomial_case(a, F(1, 1000))
            self.assertEqual(result["risk"], {"cheap": a**3, "accurate": 0})

    def test_e01_contextual_selection_and_gap(self) -> None:
        small = polynomial_case(F(1, 10), F(1, 1000))
        self.assertEqual(small["combined"], {"cheap": F(2, 1000), "accurate": F(8, 1000)})
        self.assertEqual(small["selected"], ["cheap"])
        large = polynomial_case(F(1, 2), F(1, 1000))
        self.assertEqual(large["combined"]["cheap"], F(126, 1000))
        self.assertEqual(large["selected"], ["accurate"])
        self.assertEqual(polynomial_case(F(1, 10), F(1, 10000))["selected"], ["accurate"])
        self.assertEqual(polynomial_case(F(1, 2), F(1, 1000), budget=2)["feasible"], [])

    def test_e01_equal_combined_loss_different_admissibility(self) -> None:
        result = polynomial_case(F(1, 2), F(1, 56))
        self.assertEqual(result["combined"], {"cheap": F(1, 7), "accurate": F(1, 7)})
        self.assertEqual(result["feasible"], ["accurate"])

    def test_e01_inclusive_tolerance_budget_and_tie(self) -> None:
        result = polynomial_case(F(1), F(1, 7), tolerance=F(1), budget=8)
        self.assertEqual(result["selected"], ["cheap", "accurate"])
        self.assertEqual(result["combined"]["cheap"], F(8, 7))

    def test_e02_task_reversal_and_boundary(self) -> None:
        self.assertEqual((4 * (1 - F(9, 10)), F(1)), (F(2, 5), F(1)))
        self.assertEqual((4 * (1 - F(1, 10)), F(1)), (F(18, 5), F(1)))
        self.assertEqual(4 * (1 - F(3, 4)), 1)

    def test_e02_finite_dominance_grid(self) -> None:
        vectors = list(product(range(3), repeat=2))
        weights = [F(k, 4) for k in range(5)]
        for u, v in product(vectors, repeat=2):
            by_components = all(x <= y for x, y in zip(u, v))
            by_queries = all(t * u[0] + (1 - t) * u[1] <= t * v[0] + (1 - t) * v[1] for t in weights)
            self.assertEqual(by_components, by_queries)

    def test_e03_required_witness(self) -> None:
        self.assertEqual((mean(X), mean(Y)), (1, 1))
        self.assertEqual(sorted(X), sorted(Y))
        self.assertEqual(mean([min(x, y) for x, y in zip(X, Y)]), -1)
        self.assertEqual(mean([min(x, y) for x, y in zip(X, X)]), 1)
        self.assertEqual(mean([max(x, y) for x, y in zip(X, Y)]), 3)
        self.assertEqual(mean([max(x, y) for x, y in zip(X, X)]), 1)

    def test_e03_positive_identities_on_625_pairs(self) -> None:
        vectors = list(product(range(-2, 3), repeat=2))
        weights = (F(1, 3), F(2, 3))
        for x, y in product(vectors, repeat=2):
            mx, my = mean(x, weights), mean(y, weights)
            difference = mean([abs(a - b) for a, b in zip(x, y)], weights)
            self.assertEqual(mean([a + b for a, b in zip(x, y)], weights), mx + my)
            self.assertEqual(mean([min(a, b) for a, b in zip(x, y)], weights), (mx + my - difference) / 2)

    def test_e03_means_alone_have_no_common_finite_lower_bound_witness_family(self) -> None:
        # These finite instances check the symbolic family; the unbounded conclusion is in the notes.
        for a in (0, 1, 10, 1000):
            x, y = (1 + 2 * a, 1 - 2 * a), (1 - 2 * a, 1 + 2 * a)
            self.assertEqual((mean(x), mean(y)), (1, 1))
            self.assertEqual(mean([min(s, t) for s, t in zip(x, y)]), 1 - 2 * a)

    def test_e03_known_marginal_coupling_bounds(self) -> None:
        scores = []
        for t in [F(k, 16) for k in range(9)]:
            probabilities = (t, F(1, 2) - t, F(1, 2) - t, t)
            scores.append(mean((3, -1, -1, -1), probabilities))
            self.assertEqual(scores[-1], 4 * t - 1)
        self.assertEqual((min(scores), max(scores)), (-1, 1))

    def test_e03_covariance_is_insufficient(self) -> None:
        for table in (PLUS, MINUS):
            self.assertEqual([sum(row) for row in table], [6, 6, 6])
            self.assertEqual([sum(table[i][j] for i in range(3)) for j in range(3)], [6, 6, 6])
            self.assertEqual(joint_expectation(table, lambda x, y: x), 0)
            self.assertEqual(joint_expectation(table, lambda x, y: y), 0)
            self.assertEqual(joint_expectation(table, lambda x, y: x*x), F(2, 3))
            self.assertEqual(joint_expectation(table, lambda x, y: y*y), F(2, 3))
            self.assertEqual(joint_expectation(table, lambda x, y: x*y), 0)
        self.assertEqual(joint_expectation(PLUS, min), F(-7, 18))
        self.assertEqual(joint_expectation(MINUS, min), F(-1, 2))
        self.assertEqual(joint_expectation(PLUS, lambda x, y: abs(x-y)), F(7, 9))
        self.assertEqual(joint_expectation(MINUS, lambda x, y: abs(x-y)), 1)

    def test_e03_pairwise_laws_do_not_determine_triple_minimum(self) -> None:
        for i, j in ((0, 1), (0, 2), (1, 2)):
            even_pairs = sorted((row[i], row[j]) for row in EVEN)
            odd_pairs = sorted((row[i], row[j]) for row in ODD)
            self.assertEqual(even_pairs, list(product((0, 1), repeat=2)))
            self.assertEqual(even_pairs, odd_pairs)
        self.assertEqual(mean([min(row) for row in EVEN]), 0)
        self.assertEqual(mean([min(row) for row in ODD]), F(1, 4))

    def test_e04_amplification_and_sharp_bound(self) -> None:
        for z in (F(-1), F(0), F(2, 3), F(100)):
            actual = abs((100 * (z + F(1, 100)) + F(1, 50)) - 100*z)
            self.assertEqual(actual, F(51, 50))
            self.assertGreater(actual, F(1, 100) + F(1, 50))
            self.assertEqual(actual, 100 * F(1, 100) + F(1, 50))

    def test_e04_cancellation(self) -> None:
        for z in (F(-2), F(0), F(3)):
            self.assertEqual(100 * (z + F(1, 100)) - 1, 100*z)

    def test_e04_threshold_and_missing_reachable_scope(self) -> None:
        for delta in (F(1), F(1, 100), F(1, 1000000)):
            self.assertEqual(abs(int(delta/2 >= 0) - int(-delta/2 >= 0)), 1)
            ghat = lambda u: 100 * u / delta
            self.assertEqual(ghat(0), 0)
            self.assertEqual(ghat(delta), 100)

    def test_e05_midrange_and_compatibility(self) -> None:
        precise, uncertain = {1}, {-1, 3}
        self.assertEqual(F(min(precise) + max(precise), 2), F(min(uncertain) + max(uncertain), 2))
        self.assertTrue(all(x >= 0 for x in precise))
        self.assertFalse(all(x >= 0 for x in uncertain))
        for values in (precise, uncertain, {-3, -1}, {0, 2}):
            self.assertEqual(min(values) >= 0, all(x >= 0 for x in values))
        compatible = {1, 2} & {-2, -1}
        self.assertFalse(compatible)
        self.assertTrue(all(x >= 0 for x in compatible))
        self.assertTrue(all(x < 0 for x in compatible))
        self.assertFalse(bool(compatible) and all(x >= 0 for x in compatible))

    def test_e05_nonempty_refinement_and_revision(self) -> None:
        base = {1, 2}
        for refined in ({1}, {2}, {1, 2}):
            self.assertTrue(refined <= base)
            self.assertTrue(all(x >= 0 for x in refined))
        self.assertFalse(all(x >= 0 for x in {-1, 1, 2}))

    def test_e06_tables_and_internal_equations(self) -> None:
        self.assertEqual((1 + 1) % 2, 0)
        self.assertEqual((1 + 1) % 3, 2)
        self.assertEqual((1 + 1 + 1) % 3, 0)
        self.assertEqual((1 + 1 + 1) % 2, 1)
        for k in (2, 3):
            for a, b, c in product(range(k), repeat=3):
                self.assertEqual(((a+b) % k + c) % k, (a + (b+c) % k) % k)

    def test_e06_all_adapters_and_joint_recovery(self) -> None:
        self.assertEqual(best_decoder_loss(2, 2), 0)
        self.assertEqual(best_decoder_loss(2, 3), F(2, 3))
        self.assertEqual(best_decoder_loss(3, 2), F(1, 2))
        self.assertEqual(best_decoder_loss(3, 3), 0)
        decoder = {(n % 2, n % 3): n for n in range(6)}
        self.assertEqual(len(decoder), 6)
        for n in range(6):
            self.assertEqual(decoder[(n % 2, n % 3)], n)

    def test_e07_naive_recoding_reverses_totals(self) -> None:
        self.assertGreater(3+0, 1+1)
        self.assertLess(squash(3)+squash(0), squash(1)+squash(1))
        self.assertEqual(squash(1)+squash(1), 1)
        self.assertEqual(squash(2), F(2, 3))
        self.assertGreater(transported_add(squash(3), squash(0)), transported_add(squash(1), squash(1)))

    def test_e07_inverse_and_transported_addition(self) -> None:
        grid = [F(k, 3) for k in range(-12, 13)]
        for x in grid:
            self.assertEqual(unsquash(squash(x)), x)
        for x, y in product(grid, repeat=2):
            self.assertEqual(transported_add(squash(x), squash(y)), squash(x+y))
        for a, b in product([F(0), F(1, 4), F(1, 2), F(9, 10)], repeat=2):
            self.assertEqual(transported_add(a, b), (a+b-2*a*b)/(1-a*b))

    def test_e07_precision_overlap(self) -> None:
        n, eta = 1000, F(1, 1000000)
        left, right = squash(n), squash(n+1)
        self.assertEqual(right-left, F(1, (n+1)*(n+2)))
        self.assertLess(right-left, 2*eta)
        midpoint = (left+right)/2
        self.assertLessEqual(abs(midpoint-left), eta)
        self.assertLessEqual(abs(midpoint-right), eta)

    def test_e07_unbounded_object_partial_sum_and_tail(self) -> None:
        for n in range(1, 41):
            partial = sum((F(k, 2**k) for k in range(1, n+1)), F(0))
            self.assertEqual(partial, 2 - F(n+2, 2**n))
            self.assertLessEqual(F(n+3, 2*(n+2)), F(2, 3))
        n = 40
        tail_partial = sum((F(1, 2**k) for k in range(8, n+1)), F(0))
        self.assertEqual(tail_partial + F(1, 2**n), F(1, 128))

    def test_e08_no_information_and_signal_optima(self) -> None:
        for r in (F(0), F(1, 4), F(1, 2), F(1)):
            self.assertEqual(r*mean(X)+(1-r)*mean(Y), 1)
        policies = list(product((0, 1), repeat=2))
        for p in (F(1, 2), F(3, 4), F(1)):
            values = [signal_value(policy, p) for policy in policies]
            self.assertEqual(max(values), 4*p-1)
        self.assertEqual(signal_value((0, 1), F(3, 4)) - F(1, 2), F(3, 2))
        self.assertEqual(signal_value((0, 1), F(1)), 3)

    def test_e08_acquisition_boundary(self) -> None:
        for p in (F(1, 2), F(3, 4), F(1)):
            for cost in (F(0), F(1, 2), F(1), F(2), F(3)):
                self.assertEqual(4*p-1-cost >= 1, cost <= 4*p-2)

    def test_invalid_fixture_inputs(self) -> None:
        for values, weights in (([], None), ([1, 2], [1]), ([1, 2], [1, 1]), ([1, 2], [-1, 2])):
            with self.assertRaises(ValueError):
                mean(values, weights)
        for value in (F(-1), F(1), F(2)):
            with self.assertRaises(ValueError):
                unsquash(value)
        with self.assertRaises(ValueError):
            signal_value((0, 1), F(1, 4))


def report() -> dict:
    """Return deterministic machine-readable results, not a statistical experiment."""
    n = 40
    return {
        "schema": "value-logic-f01-fixtures-v1",
        "arithmetic": "exact fractions",
        "scope": "finite witnesses and grids; unrestricted arguments are in the derivation note",
        "E01": {name: polynomial_case(a, rate, budget) for name, a, rate, budget in (
            ("cheap_selected", F(1, 10), F(1, 1000), 8),
            ("accurate_required", F(1, 2), F(1, 1000), 8),
            ("rate_changed", F(1, 10), F(1, 10000), 8),
            ("gap", F(1, 2), F(1, 1000), 2),
            ("equal_score_different_admissibility", F(1, 2), F(1, 56), 8))},
        "E02": {"theta_9_10": [F(2, 5), F(1)], "theta_1_10": [F(18, 5), F(1)], "tie_theta": F(3, 4)},
        "E03": {"component_means": [mean(X), mean(Y)],
                "opposed_min": mean([min(x, y) for x, y in zip(X, Y)]),
                "aligned_min": mean(X),
                "opposed_max": mean([max(x, y) for x, y in zip(X, Y)]),
                "joint_difference_statistic": [mean([abs(x-y) for x, y in zip(X, Y)]), F(0)],
                "matching_covariance_minima": [joint_expectation(PLUS, min), joint_expectation(MINUS, min)],
                "matching_pairwise_law_triple_minima": [mean([min(x) for x in EVEN]), mean([min(x) for x in ODD])]},
        "E04": {"actual_error": F(51, 50), "naive_bound": F(3, 100), "sensitivity_bound": F(51, 50), "cancellation_error": F(0), "missing_scope_error": F(100)},
        "E05": {"precise_uniformly_nonnegative": True, "uncertain_uniformly_nonnegative": False, "conflict_has_nonempty_basis": False},
        "E06": {"minimum_loss_rows_mod2_mod3_columns_parity_residue3": [[best_decoder_loss(2, 2), best_decoder_loss(2, 3)], [best_decoder_loss(3, 2), best_decoder_loss(3, 3)]], "joint_distinct_codes": len({(k % 2, k % 3) for k in range(6)})},
        "E07": {"original_totals": [3, 2], "naively_recoded_totals": [squash(3)+squash(0), squash(1)+squash(1)], "transported_totals": [squash(3), squash(2)], "partial_sum_N": n, "unbounded_partial_sum": sum((F(k, 2**k) for k in range(1, n+1)), F(0)), "analytic_remainder": F(n+2, 2**n), "adjacent_encoded_gap_at_1000": squash(1001)-squash(1000)},
        "E08": {"signal_accuracy": F(3, 4), "signal_cost": F(1, 2), "four_policy_values_before_cost": {str(policy): signal_value(policy, F(3, 4)) for policy in product((0, 1), repeat=2)}, "optimal_net_value": F(3, 2)},
        "finite_enumeration_bounds": {"dominance_vector_pairs": 81, "dominance_weights": 5, "pair_identity_grid_pairs": 625, "inverse_addition_grid_pairs": 625, "mod2_to_mod3_decoders": 9, "mod3_to_mod2_decoders": 8, "signal_policies_per_accuracy": 4, "infinite_series_partial_sums_checked": 40},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write exact fixture results only after tests pass.")
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(F01FixtureTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report(), indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
        print(f"Wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
