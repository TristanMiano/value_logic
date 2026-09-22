"""Exact F01 continuation fixtures, not a general calculus or held-out experiment.

Run: python -m v2.checks.f01_reconstruction --json v2/checks/F01_reconstruction_results.json
All inputs are constructed finite examples and all calculations use fractions.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
from typing import Callable, Mapping, Sequence
import unittest

from v2.checks.f01_examples import squash, unsquash

State = tuple[int, ...]
Law = dict[State, F]


def compositions(total: int, slots: int):
    """Enumerate nonnegative integer histograms without an exponential grid."""
    if total < 0 or slots < 1:
        raise ValueError("Nonnegative total and positive slot count required.")
    for cuts in combinations(range(total + slots - 1), slots - 1):
        marks = (-1, *cuts, total + slots - 1)
        yield tuple(marks[i + 1] - marks[i] - 1 for i in range(slots))


def validate_law(law: Mapping[State, F]) -> int:
    if not law:
        raise ValueError("A probability law must be nonempty.")
    dimensions = {len(state) for state in law}
    if len(dimensions) != 1 or next(iter(dimensions)) == 0:
        raise ValueError("States must have a fixed positive arity.")
    if any(p < 0 for p in law.values()) or sum(law.values()) != 1:
        raise ValueError("Nonnegative, exactly normalized probabilities required.")
    return next(iter(dimensions))


def expectation(law: Mapping[State, F], fn: Callable[[State], int | F]) -> F:
    validate_law(law)
    return sum((p * fn(state) for state, p in law.items()), F(0))


def marginal(law: Mapping[State, F], indices: Sequence[int]) -> Law:
    arity = validate_law(law)
    if not indices or len(set(indices)) != len(indices) or any(i < 0 or i >= arity for i in indices):
        raise ValueError("This fixture interface requires nonempty, distinct valid coordinates.")
    result: defaultdict[State, F] = defaultdict(F)
    for state, probability in law.items():
        if probability:
            result[tuple(state[i] for i in indices)] += probability
    return dict(result)


def tv(left: Mapping[State, F], right: Mapping[State, F]) -> F:
    if validate_law(left) != validate_law(right):
        raise ValueError("Probability laws must describe the same arity.")
    return sum((abs(left.get(s, F(0)) - right.get(s, F(0)))
                for s in left.keys() | right.keys()), F(0)) / 2


def binary_joint_from_covariance(a: F, b: F, c: F, d: F,
                                 alpha: F, beta: F, covariance: F) -> tuple[F, ...]:
    if not a < b or not c < d:
        raise ValueError("Each declared binary support must be ordered and nondegenerate.")
    if not 0 <= alpha <= 1 or not 0 <= beta <= 1:
        raise ValueError("Marginal probabilities must be in [0,1].")
    t = alpha * beta + covariance / ((b-a) * (d-c))
    if not max(F(0), alpha+beta-1) <= t <= min(alpha, beta):
        raise ValueError("The supplied covariance and marginals are incompatible.")
    return (1-alpha-beta+t, beta-t, alpha-t, t)


def parity_law(n: int, parity: int) -> Law:
    if n < 2 or parity not in (0, 1):
        raise ValueError("This family requires at least two bits and parity 0 or 1.")
    return {row: F(1, 2**(n-1)) for row in product((0, 1), repeat=n)
            if sum(row) % 2 == parity}


def decode_nonnegative_interval(center: F, radius: F) -> tuple[F, F]:
    """Only the explicitly bounded nonnegative-code fragment is admitted."""
    if radius < 0 or center-radius < 0 or center+radius >= 1:
        raise ValueError("Require radius >= 0 and 0 <= center-radius <= center+radius < 1.")
    return unsquash(center-radius), unsquash(center+radius)


def common_epsilon_actions(models: Sequence[Sequence[F]], epsilon: F) -> set[int]:
    if epsilon < 0 or not models or not models[0]:
        raise ValueError("Nonempty compatible models/actions and nonnegative tolerance required.")
    size = len(models[0])
    if any(len(row) != size for row in models):
        raise ValueError("Every model must evaluate the same action set.")
    return {a for a in range(size)
            if all(max(row)-row[a] <= epsilon for row in models)}


def information_values(joint: Mapping[State, F], payoffs: Sequence[Sequence[F]]) -> tuple[F, F, F]:
    if validate_law(joint) != 2 or not payoffs or not payoffs[0]:
        raise ValueError("A hidden-state/signal law and nonempty payoff table required.")
    actions = range(len(payoffs[0]))
    if any(len(row) != len(payoffs[0]) for row in payoffs):
        raise ValueError("Each hidden state must have the same available actions.")
    if any(w < 0 or w >= len(payoffs) for w, _ in joint):
        raise ValueError("The payoff table must cover all hidden-state labels.")
    signals = {s for _, s in joint}
    without = max(sum((p*payoffs[w][a] for (w, _), p in joint.items()), F(0))
                  for a in actions)
    with_signal = sum((max(sum((p*payoffs[w][a] for (w, t), p in joint.items()
                               if t == s), F(0)) for a in actions) for s in signals), F(0))
    oracle = sum((p*max(payoffs[w]) for (w, _), p in joint.items()), F(0))
    return without, with_signal, oracle


def conditional_mean(law: Mapping[State, F], value_index: int,
                     event: Callable[[State], bool]) -> F:
    arity = validate_law(law)
    if not 0 <= value_index < arity:
        raise ValueError("Invalid payoff coordinate.")
    mass = sum((p for state, p in law.items() if event(state)), F(0))
    if mass <= 0:
        raise ValueError("Conditioning event must have positive probability.")
    return sum((p*state[value_index] for state, p in law.items() if event(state)), F(0)) / mass


TRIPLES = tuple(product((0, 1), repeat=3))
PAIRS = ((0, 1), (1, 2), (0, 2))
TARGETS = ({(0, 0): F(1, 2), (1, 1): F(1, 2)},
           {(0, 0): F(1, 2), (1, 1): F(1, 2)},
           {(0, 1): F(1, 2), (1, 0): F(1, 2)})
SINGLE_VIOLATION_PAIRS = (((0, 1, 1), (1, 0, 0)),
                          ((0, 0, 1), (1, 1, 0)),
                          ((0, 0, 0), (1, 1, 1)))


def violations(state: State) -> tuple[int, int, int]:
    if len(state) != 3 or any(b not in (0, 1) for b in state):
        raise ValueError("This witness has three binary coordinates.")
    a, b, c = state
    return int(a != b), int(b != c), int(a == c)


def violation_probabilities(law: Mapping[State, F]) -> tuple[F, ...]:
    return tuple(expectation(law, lambda row, i=i: violations(row)[i]) for i in range(3))


def compatible_error_law(caps: Sequence[F]) -> Law:
    if len(caps) != 3 or any(e < 0 or e > 1 for e in caps):
        raise ValueError("Three error caps in [0,1] required.")
    total = sum(caps)
    if total < 1:
        raise ValueError("These error caps have no common realization.")
    return {row: caps[i]/total/2 for i, pair in enumerate(SINGLE_VIOLATION_PAIRS)
            for row in pair if caps[i]}


def exact_error_law(errors: Sequence[F]) -> Law:
    """Realize an exact vector, rather than treating it as three upper caps."""
    if len(errors) != 3 or any(r < 0 or r > 1 for r in errors):
        raise ValueError("Three exact probabilities in [0,1] required.")
    triple = (sum(errors)-1)/2
    weights = tuple(r-triple for r in errors) + (triple,)
    if any(w < 0 for w in weights):
        raise ValueError("This exact error vector is not realizable.")
    pairs = SINGLE_VIOLATION_PAIRS + (((0, 1, 0), (1, 0, 1)),)
    return {row: w/2 for w, pair in zip(weights, pairs) for row in pair if w}


def ternary_uniform_tables(row_total: int = 4):
    """Enumerate integer tables with all row/column sums fixed, independently of bounds."""
    if row_total < 1:
        raise ValueError("A positive integer row total is required.")
    r = row_total
    labels = (-1, 0, 1)
    for a, b, d, e in product(range(r+1), repeat=4):
        c, f, g, h = r-a-b, r-d-e, r-a-d, r-b-e
        i = r-g-h
        counts = ((a, b, c), (d, e, f), (g, h, i))
        if any(v < 0 for row in counts for v in row):
            continue
        yield {(x, y): F(counts[ix][iy], 3*r)
               for ix, x in enumerate(labels) for iy, y in enumerate(labels)}


class F01ReconstructionTests(unittest.TestCase):
    def test_restricted_task_endpoint_criterion(self):
        vectors = tuple(product(range(3), repeat=2))
        for u, v in product(vectors, repeat=2):
            delta = lambda t: t*(u[0]-v[0]) + (1-t)*(u[1]-v[1])
            for lo, hi in ((F(0), F(1)), (F(1, 4), F(3, 4)), (F(1, 2), F(1, 2))):
                endpoints = delta(lo) <= 0 and delta(hi) <= 0
                grid = all(delta(lo+(hi-lo)*F(k, 8)) <= 0 for k in range(9))
                self.assertEqual(endpoints, grid)
        self.assertTrue(all(1 <= 4*(1-F(k, 8)) for k in range(2, 7)))
        self.assertGreater(1, 4*(1-F(1)))

    def test_binary_covariance_reconstructs_all_denominator_four_tables(self):
        bits = tuple(product((0, 1), repeat=2))
        supports = ((F(-1), F(3), F(-1), F(3)),
                    (F(0), F(1), F(-2), F(2)),
                    (F(-3), F(-1), F(2), F(5)))
        count = 0
        for counts in compositions(4, 4):
            weights = tuple(F(n, 4) for n in counts)
            alpha, beta = weights[2]+weights[3], weights[1]+weights[3]
            for a, b, c, d in supports:
                xs = tuple(a+(b-a)*i for i, j in bits)
                ys = tuple(c+(d-c)*j for i, j in bits)
                ex = sum(p*x for p, x in zip(weights, xs))
                ey = sum(p*y for p, y in zip(weights, ys))
                cov = sum(p*x*y for p, x, y in zip(weights, xs, ys))-ex*ey
                rebuilt = binary_joint_from_covariance(a, b, c, d, alpha, beta, cov)
                self.assertEqual(rebuilt, weights)
                self.assertEqual(sum(p*min(x, y) for p, x, y in zip(rebuilt, xs, ys)),
                                 sum(p*min(x, y) for p, x, y in zip(weights, xs, ys)))
                count += 1
        self.assertEqual(count, 105)

    def test_binary_covariance_rejects_incompatible_and_malformed_inputs(self):
        with self.assertRaises(ValueError):
            binary_joint_from_covariance(F(0), F(1), F(0), F(1), F(1, 2), F(1, 2), F(1))
        with self.assertRaises(ValueError):
            binary_joint_from_covariance(F(0), F(0), F(0), F(1), F(1, 2), F(1, 2), F(0))
        with self.assertRaises(ValueError):
            binary_joint_from_covariance(F(0), F(1), F(0), F(1), F(-1), F(1, 2), F(0))

    def test_all_proper_marginals_match_in_parity_family(self):
        for n in range(2, 8):
            even, odd = parity_law(n, 0), parity_law(n, 1)
            self.assertEqual(len(even), 2**(n-1))
            for k in range(1, n):
                for indices in combinations(range(n), k):
                    left, right = marginal(even, indices), marginal(odd, indices)
                    self.assertEqual(left, right)
                    self.assertEqual(set(left.values()), {F(1, 2**k)})
            scores = (expectation(even, min), expectation(odd, min))
            self.assertEqual(scores[n % 2], F(1, 2**(n-1)))
            self.assertEqual(scores[1-n % 2], 0)

    def test_scaled_parity_gap_stays_one(self):
        for n in range(2, 8):
            scale = 2**(n-1)
            values = [expectation(parity_law(n, p), lambda row: scale*min(row)) for p in (0, 1)]
            self.assertEqual(abs(values[0]-values[1]), 1)

    def test_shared_uncertainty_exact_and_interval_answers(self):
        for k in (3, 10, 100):
            shared = ((1, 3), (k+1, k+3))
            opposed = ((1, k+3), (k+1, 3))
            self.assertEqual(sorted(c for c, f in shared), sorted(c for c, f in opposed))
            self.assertEqual(sorted(f for c, f in shared), sorted(f for c, f in opposed))
            self.assertEqual(min(f-c for c, f in shared), 2)
            self.assertEqual(min(f-c for c, f in opposed), 2-k)

    def test_coextremizer_criterion_on_511_joint_sets(self):
        pool = tuple(product(range(3), repeat=2))
        count = 0
        for k in range(1, len(pool)+1):
            for joint in combinations(pool, k):
                fmin, cmax = min(f for c, f in joint), max(c for c, f in joint)
                bound, actual = fmin-cmax, min(f-c for c, f in joint)
                self.assertLessEqual(bound, actual)
                self.assertEqual(bound == actual, (cmax, fmin) in joint)
                count += 1
        self.assertEqual(count, 511)

    def test_affine_equal_length_order_on_5625_comparisons(self):
        vectors = tuple(product(range(-2, 3), repeat=2))
        count = 0
        for a, b in product((F(1, 3), F(1), F(2)), (F(-2), F(0), F(3))):
            for u, v in product(vectors, repeat=2):
                self.assertEqual(sum(u) <= sum(v),
                                 sum(a*x+b for x in u) <= sum(a*x+b for x in v))
                count += 1
        self.assertEqual(count, 5625)

    def test_affine_offset_can_reverse_unequal_length_totals(self):
        left, right = (2,), (1, 0)
        self.assertGreater(sum(left), sum(right))
        self.assertLess(sum(2*x+3 for x in left), sum(2*x+3 for x in right))

    def test_positive_linear_scaling_handles_unequal_lengths(self):
        vectors = tuple(row for n in range(1, 4) for row in product((-1, 0, 1), repeat=n))
        for u, v in product(vectors, repeat=2):
            self.assertEqual(sum(u) <= sum(v), sum(3*x for x in u) <= sum(3*x for x in v))

    def test_finite_range_inverse_error_bound(self):
        for cap in (F(1), F(3), F(10)):
            grid = tuple(cap*F(k, 8) for k in range(9))
            for x, y in product(grid, repeat=2):
                encoded, decoded = abs(squash(x)-squash(y)), abs(x-y)
                self.assertEqual(encoded, decoded/((1+x)*(1+y)))
                self.assertLessEqual(encoded, decoded)
                self.assertLessEqual(decoded, (1+cap)**2*encoded)

    def test_range_condition_and_clipping_repair(self):
        cap, truth, reported = F(1), F(1, 2), F(3, 5)
        radius = abs(reported-truth)
        self.assertGreater(abs(unsquash(reported)-unsquash(truth)), (1+cap)**2*radius)
        clipped = min(squash(cap), max(F(0), reported))
        self.assertLessEqual(abs(clipped-truth), radius)
        self.assertLessEqual(abs(unsquash(clipped)-unsquash(truth)), (1+cap)**2*radius)

    def test_decoded_interval_width(self):
        for center in (F(1, 4), F(1, 2), F(9, 10)):
            for radius in (F(0), F(1, 100), F(1, 20)):
                lo, hi = decode_nonnegative_interval(center, radius)
                self.assertEqual(hi-lo, 2*radius/((1-center)**2-radius**2))
                self.assertEqual((squash(lo), squash(hi)), (center-radius, center+radius))
        for center, radius in ((F(1), F(0)), (F(1, 2), F(1, 2)), (F(0), F(1, 10)), (F(1, 2), F(-1))):
            with self.assertRaises(ValueError):
                decode_nonnegative_interval(center, radius)

    def test_approximate_codes_hide_a_large_real_decision_gap(self):
        n, gap, radius = F(1000), F(10), F(1, 10000)
        lo, hi = squash(n), squash(n+gap)
        center = (lo+hi)/2
        self.assertEqual(hi-lo, gap/((n+1)*(n+gap+1)))
        self.assertLessEqual(max(center-lo, hi-center), radius)
        # Two opposite score orderings share the exact same reported pair.
        models = ((n+gap, n), (n, n+gap))
        self.assertEqual(common_epsilon_actions(models, gap-F(1, 100)), set())
        self.assertEqual(common_epsilon_actions(models, gap), {0, 1})

    def test_midpoint_minimax_reconstruction(self):
        for lo, hi in combinations(range(-3, 4), 2):
            center = F(lo+hi, 2)
            radius = F(hi-lo, 2)
            self.assertEqual(max(abs(lo-center), abs(hi-center)), radius)
            for estimate in (F(k, 2) for k in range(-8, 9)):
                self.assertGreaterEqual(max(abs(lo-estimate), abs(hi-estimate)), radius)

    def test_sign_guarantees_need_the_error_margin(self):
        for radius in (F(0), F(1, 2), F(1)):
            for center in (F(-2), F(-1), F(0), F(1), F(2)):
                compatible = tuple(center-radius+2*radius*F(k, 8) for k in range(9))
                self.assertTrue(all(abs(v-center) <= radius for v in compatible))
                self.assertEqual(center-radius >= 0, all(v >= 0 for v in compatible))
                self.assertEqual(center+radius < 0, all(v < 0 for v in compatible))
                if center-radius < 0 <= center+radius:
                    self.assertTrue(any(v < 0 for v in compatible))
                    self.assertTrue(any(v >= 0 for v in compatible))

    def test_optimal_action_without_exact_value(self):
        models = tuple((F(n), F(0)) for n in (1, 3, 100, 10000))
        self.assertEqual(common_epsilon_actions(models, F(0)), {0})
        self.assertGreater(max(row[0] for row in models)-min(row[0] for row in models), 100)
        changed = tuple((a-2, b) for a, b in models)
        self.assertEqual(common_epsilon_actions(changed, F(0)), set())
        self.assertEqual(common_epsilon_actions(changed[:1], F(0)), {1})
        self.assertEqual(common_epsilon_actions(changed[1:], F(0)), {0})

    def test_deterministic_and_randomized_regret_are_different(self):
        models = ((F(1), F(0)), (F(0), F(1)))
        self.assertEqual(common_epsilon_actions(models, F(1, 2)), set())
        self.assertEqual(common_epsilon_actions(models, F(1)), {0, 1})
        for r in (F(k, 8) for k in range(9)):
            self.assertGreaterEqual(max(1-r, r), F(1, 2))
        self.assertEqual(max(1-F(1, 2), F(1, 2)), F(1, 2))

    def test_simultaneous_score_error_gives_two_delta_regret(self):
        vectors = tuple(product((-1, 0, 1), repeat=3))
        for truth, estimate in product(vectors, repeat=2):
            delta = max(abs(x-y) for x, y in zip(truth, estimate))
            chosen = max(range(3), key=lambda a: estimate[a])
            self.assertLessEqual(max(truth)-truth[chosen], 2*delta)
            runner_up = max(estimate[a] for a in range(3) if a != chosen)
            if estimate[chosen]-runner_up > 2*delta:
                self.assertTrue(all(truth[chosen] > truth[a] for a in range(3) if a != chosen))
        truth, estimate, delta = (F(-1), F(1)), (F(0), F(0)), F(1)
        chosen = max(range(2), key=lambda a: estimate[a])
        self.assertEqual(max(truth)-truth[chosen], 2*delta)

    def test_score_margin_equality_allows_a_true_tie(self):
        estimate, truth, delta = (F(2), F(0)), (F(1), F(1)), F(1)
        self.assertEqual(estimate[0]-estimate[1], 2*delta)
        self.assertEqual(truth[0], truth[1])
        self.assertEqual(max(abs(x-y) for x, y in zip(truth, estimate)), delta)

    def test_invalid_model_families_are_not_vacuous_choices(self):
        for models, tolerance in (((), F(0)), (((),), F(0)), (((F(1),), (F(1), F(0))), F(0)), (((F(1),),), F(-1))):
            with self.assertRaises(ValueError):
                common_epsilon_actions(models, tolerance)

    def test_information_values_by_exhaustive_policy_enumeration(self):
        cells = tuple(product((0, 1), repeat=2))
        count = 0
        for counts in compositions(4, 4):
            joint = {cell: F(c, 4) for cell, c in zip(cells, counts)}
            for entries in product((-1, 0, 1), repeat=4):
                payoffs = (entries[:2], entries[2:])
                v0, vs, oracle = information_values(joint, payoffs)
                enumerated = max(sum(p*payoffs[w][policy[s]] for (w, s), p in joint.items())
                                 for policy in product((0, 1), repeat=2))
                self.assertEqual(vs, enumerated)
                self.assertLessEqual(v0, vs)
                self.assertLessEqual(vs, oracle)
                attainable = all(any(all(payoffs[w][a] == max(payoffs[w])
                                         for w in (0, 1) if joint[(w, s)] > 0)
                                     for a in (0, 1)) for s in (0, 1))
                self.assertEqual(vs == oracle, attainable)
                count += 1
        self.assertEqual(count, 2835)

    def test_symmetric_signal_values_and_zero_probability_cells(self):
        for accuracy in (F(0), F(1, 2), F(3, 4), F(1)):
            joint = {(w, s): (accuracy if w == s else 1-accuracy)/2
                     for w, s in product((0, 1), repeat=2)}
            v0, vs, oracle = information_values(joint, ((3, -1), (-1, 3)))
            self.assertEqual((v0, oracle), (1, 3))
            self.assertEqual(vs, 1+abs(4*accuracy-2))

    def test_robust_expected_and_realized_guarantees(self):
        for r in (F(k, 8) for k in range(9)):
            expected_by_state = (4*r-1, 3-4*r)
            self.assertEqual(min(expected_by_state), 1-4*abs(r-F(1, 2)))
            self.assertLessEqual(min(expected_by_state), 1)
            possible_actions = [a for a, mass in ((0, r), (1, 1-r)) if mass > 0]
            realized_worst = min(3 if a == w else -1 for a in possible_actions for w in (0, 1))
            self.assertEqual(realized_worst, -1)

    def test_matching_marginals_do_not_determine_conditioning(self):
        p = {(-1, 0): F(1, 2), (1, 1): F(1, 2)}
        q = {(-1, 1): F(1, 2), (1, 0): F(1, 2)}
        self.assertEqual(marginal(p, (0,)), marginal(q, (0,)))
        self.assertEqual(marginal(p, (1,)), marginal(q, (1,)))
        self.assertEqual((expectation(p, lambda r: r[0]), expectation(q, lambda r: r[0])), (0, 0))
        self.assertEqual(conditional_mean(p, 0, lambda r: r[1] == 1), 1)
        self.assertEqual(conditional_mean(q, 0, lambda r: r[1] == 1), -1)

    def test_conditioning_rejects_null_event(self):
        with self.assertRaises(ValueError):
            conditional_mean({(1, 0): F(1)}, 0, lambda r: r[1] == 1)

    def test_rare_event_instability(self):
        for mass in (F(1, 2), F(1, 10), F(1, 1000)):
            p = {(1, 1): mass, (0, 0): 1-mass}
            q = {(-1, 1): mass, (0, 0): 1-mass}
            self.assertEqual(tv(p, q), mass)
            self.assertEqual(conditional_mean(p, 0, lambda r: r[1] == 1)-
                             conditional_mean(q, 0, lambda r: r[1] == 1), 2)

    def test_conditional_ratio_error_bound(self):
        count = 0
        for probability, value, estimated_p, estimated_b in product(
                (F(1, 4), F(1, 2), F(1)), (F(-1), F(0), F(1)),
                (F(1, 8), F(1, 4), F(1, 2), F(1)),
                (F(-1), F(-1, 2), F(0), F(1, 2), F(1))):
            numerator = probability*value
            db, dp = abs(numerator-estimated_b), abs(probability-estimated_p)
            self.assertLessEqual(abs(value-estimated_b/estimated_p), (db+dp)/estimated_p)
            count += 1
        self.assertEqual(count, 180)

    def test_pairwise_constraint_intersections_but_empty_triple(self):
        accepted = tuple({row for row in TRIPLES if violations(row)[i] == 0} for i in range(3))
        for i, j in combinations(range(3), 2):
            self.assertEqual(len(accepted[i] & accepted[j]), 2)
        self.assertEqual(set.intersection(*accepted), set())
        self.assertTrue(all(sum(violations(row)) >= 1 for row in TRIPLES))

    def test_error_cap_constructor_and_full_pair_distances(self):
        grid = (F(0), F(1, 4), F(1, 3), F(1, 2), F(1))
        for caps in product(grid, repeat=3):
            if sum(caps) < 1:
                with self.assertRaises(ValueError):
                    compatible_error_law(caps)
                continue
            law = compatible_error_law(caps)
            self.assertEqual(validate_law(law), 3)
            errors = violation_probabilities(law)
            for i in range(3):
                self.assertLessEqual(errors[i], caps[i])
                self.assertEqual(marginal(law, (i,)), {(0,): F(1, 2), (1,): F(1, 2)})
                self.assertEqual(tv(marginal(law, PAIRS[i]), TARGETS[i]), errors[i])

    def test_one_third_threshold_by_1716_joint_laws(self):
        best, count = F(1), 0
        for counts in compositions(6, 8):
            law = {row: F(n, 6) for row, n in zip(TRIPLES, counts)}
            errors = violation_probabilities(law)
            self.assertGreaterEqual(sum(errors), 1)
            worst_distance = max(tv(marginal(law, pair), target) for pair, target in zip(PAIRS, TARGETS))
            best = min(best, worst_distance)
            count += 1
        self.assertEqual(count, 1716)
        self.assertEqual(best, F(1, 3))
        witness = compatible_error_law((F(1, 3),)*3)
        self.assertEqual(len(witness), 6)
        self.assertEqual(set(witness.values()), {F(1, 6)})

    def test_exact_error_vector_is_not_an_upper_cap_vector(self):
        law = compatible_error_law((F(1), F(1), F(0)))
        self.assertEqual(violation_probabilities(law), (F(1, 2), F(1, 2), F(0)))
        both_first_errors = [row for row in TRIPLES if violations(row)[:2] == (1, 1)]
        self.assertTrue(both_first_errors)
        self.assertTrue(all(violations(row)[2] == 1 for row in both_first_errors))

    def test_bottleneck_uniform_bound_on_15625_tuple_pairs(self):
        rows = tuple(product(range(-2, 3), repeat=3))
        for left, right in product(rows, repeat=2):
            self.assertLessEqual(abs(min(left)-min(right)), max(abs(x-y) for x, y in zip(left, right)))

    def test_bottleneck_average_errors_require_sum_in_worst_case(self):
        delta = F(1, 10)
        for n in range(2, 8):
            approximations = tuple(tuple(-n*delta if i == w else F(0) for w in range(n)) for i in range(n))
            component_errors = tuple(sum(abs(x) for x in row)/n for row in approximations)
            output_error = sum(abs(min(row[w] for row in approximations)) for w in range(n))/n
            self.assertEqual(component_errors, (delta,)*n)
            self.assertEqual(output_error, n*delta)
            self.assertEqual(output_error, sum(component_errors))
            self.assertGreater(output_error, max(component_errors))

    def test_error_of_mean_is_not_mean_absolute_error(self):
        for magnitude in (F(1), F(10), F(1000)):
            errors = (magnitude, -magnitude)
            self.assertEqual(abs(sum(errors)/2), 0)
            self.assertEqual(sum(abs(e) for e in errors)/2, magnitude)

    def test_global_mean_does_not_restrict_for_free(self):
        for n in (2, 10, 100):
            losses = (F(1),) + (F(0),)*(n-1)
            self.assertEqual(sum(losses)/n, F(1, n))
            self.assertEqual(losses[0], 1)
            self.assertEqual((sum(losses)/n)/F(1, n), losses[0])

    def test_exact_error_frontier_against_independent_pattern_enumeration(self):
        # Enumerate pattern mixtures, not the formula used by the constructor.
        patterns = tuple(violations(pair[0]) for pair in SINGLE_VIOLATION_PAIRS) + (violations((0, 1, 0)),)
        attained = {tuple(sum(F(c, 8)*pattern[i] for c, pattern in zip(counts, patterns))
                          for i in range(3)) for counts in compositions(8, 4)}
        self.assertEqual(len(attained), 165)
        tested = 0
        for errors in product((F(k, 4) for k in range(5)), repeat=3):
            if errors not in attained:
                with self.assertRaises(ValueError):
                    exact_error_law(errors)
            else:
                law = exact_error_law(errors)
                self.assertEqual(violation_probabilities(law), errors)
                for i, pair in enumerate(PAIRS):
                    self.assertEqual(marginal(law, (i,)), {(0,): F(1, 2), (1,): F(1, 2)})
                    self.assertEqual(tv(marginal(law, pair), TARGETS[i]), errors[i])
            tested += 1
        self.assertEqual(tested, 125)
        with self.assertRaises(ValueError):
            exact_error_law((F(1), F(1), F(0)))
        self.assertEqual(violation_probabilities(exact_error_law((F(1), F(0), F(0)))), (1, 0, 0))
        for bad in ((F(-1), F(1), F(1)), (F(1),), (F(2), F(0), F(0))):
            with self.assertRaises(ValueError):
                exact_error_law(bad)

    def test_weighted_repair_and_minimax_repair_are_different(self):
        patterns = tuple(violations(row) for row in ((0, 1, 1), (0, 0, 1), (0, 0, 0), (0, 1, 0)))
        for costs in product((0, 1, 2), repeat=3):
            pattern_costs = tuple(sum(c*e for c, e in zip(costs, pattern)) for pattern in patterns)
            self.assertEqual(min(pattern_costs), min(costs))
            for counts in compositions(8, 4):
                self.assertGreaterEqual(sum(F(c, 8)*v for c, v in zip(counts, pattern_costs)), min(costs))
        costs = (1, 2, 3)
        self.assertEqual(sum(c*e for c, e in zip(costs, (F(1, 3),)*3)), 2)
        self.assertEqual(sum(c*e for c, e in zip(costs, (1, 0, 0))), 1)
        # Negative costs lie outside the theorem: three rewarded violations win.
        self.assertEqual(min(sum(-e for e in row) for row in patterns), -3)
        self.assertNotEqual(-3, min((-1, -1, -1)))

    def test_independence_is_an_additional_compatibility_restriction(self):
        independent = {row: F(1, 8) for row in TRIPLES}
        self.assertEqual(violation_probabilities(independent), (F(1, 2),)*3)
        correlated = compatible_error_law((F(1, 3),)*3)
        self.assertEqual(violation_probabilities(correlated), (F(1, 3),)*3)
        for pair in PAIRS:
            self.assertEqual(set(marginal(independent, pair).values()), {F(1, 4)})
            self.assertNotEqual(marginal(independent, pair), marginal(correlated, pair))

    def test_cost_update_retains_a_sharp_finite_regret_guarantee(self):
        for cost in (F(0), F(1, 2), F(1), F(3, 2), F(2), F(10)):
            regrets = tuple(max(cost-n, 0) for n in range(1, 21))
            self.assertEqual(max(regrets), max(cost-1, 0))
            if cost <= 1:
                self.assertEqual(max(regrets), 0)
            for probability_first in (F(0), F(1, 2), F(9, 10)):
                n1, n2 = 100, 1000
                loss1 = (1-probability_first)*(n1-cost)
                loss2 = (1-probability_first)*(n2-cost)
                self.assertGreater(loss2, loss1)
                self.assertEqual(loss2-loss1, 900*(1-probability_first))
        models = tuple((F(n-2), F(0)) for n in (1, 2, 3, 100))
        self.assertEqual(common_epsilon_actions(models, F(0)), set())
        self.assertEqual(common_epsilon_actions(models, F(1)), {0})

    def test_marginal_coverage_can_coexist_with_certain_selection_error(self):
        for m in (2, 10, 100):
            truth = (1,) + (0,)*m
            reports = tuple(tuple(2 if a == i else truth[a] for a in range(m+1)) for i in range(1, m+1))
            coverages = tuple(sum(F(row[a] == truth[a], m) for row in reports) for a in range(m+1))
            self.assertEqual(coverages, (F(1),) + (F(m-1, m),)*m)
            for report in reports:
                selected = max(range(m+1), key=lambda a: report[a])
                self.assertNotEqual(selected, 0)
                self.assertEqual(max(truth)-truth[selected], 1)
                self.assertFalse(all(x == y for x, y in zip(truth, report)))

    def test_union_bound_and_bounded_expected_regret(self):
        rows = tuple(product((-1, 0, 1), repeat=2))
        count = 0
        for truth, delta in product(rows, (F(0), F(1, 2), F(1))):
            bound = max(truth)-min(truth)
            on_good = min(bound, 2*delta)
            for counts in compositions(2, len(rows)):
                probabilities = tuple(F(c, 2) for c in counts)
                failures = tuple(sum(p for p, report in zip(probabilities, rows)
                                     if abs(report[a]-truth[a]) > delta) for a in range(2))
                alpha = min(F(1), sum(failures))
                good = sum(p for p, report in zip(probabilities, rows)
                           if all(abs(x-y) <= delta for x, y in zip(truth, report)))
                expected_regret = sum(p*(max(truth)-truth[max(range(2), key=lambda a: report[a])])
                                      for p, report in zip(probabilities, rows))
                self.assertGreaterEqual(good, 1-alpha)
                self.assertLessEqual(expected_regret, (1-alpha)*on_good+alpha*bound)
                count += 1
        self.assertEqual(count, 1215)

    def test_integrable_tail_spike_is_hidden_by_any_tested_prefix(self):
        for n, magnitude in product(range(1, 17), (F(1, 2), F(2), F(100))):
            k, probability = n+1, F(1, 2**(n+1))
            height = magnitude*2**k
            changed = lambda j: F(j) + (height if j == k else 0)
            self.assertEqual(tuple(changed(j) for j in range(1, n+1)), tuple(range(1, n+1)))
            self.assertEqual(probability*(changed(k)-k), magnitude)
            encoded_difference = probability*(squash(changed(k))-squash(F(k)))
            self.assertGreater(encoded_difference, 0)
            self.assertLess(encoded_difference, probability)
            self.assertEqual(encoded_difference, magnitude/((k+1)*(k+1+height)))

    def test_geometric_envelope_tail_bound_and_sharp_extensions(self):
        for n in range(1, 21):
            prefix = sum(F(k, 2**k) for k in range(1, n+1))
            tail = F(n+2, 2**n)
            self.assertEqual(prefix+tail, 2)
            for stop in (n+1, n+5, n+20):
                finite_tail = sum(F(k, 2**k) for k in range(n+1, stop+1))
                self.assertLessEqual(finite_tail, tail)
                self.assertEqual(tail-finite_tail, F(stop+2, 2**stop))
        prefix, tail = sum(F(k, 2**k) for k in range(1, 9)), F(10, 256)
        self.assertEqual((prefix, tail, prefix+tail), (F(251, 128), F(5, 128), F(2)))

    def test_sharp_ternary_covariance_bounds_by_table_enumeration(self):
        all_values, zero_covariance = [], []
        for law in ternary_uniform_tables():
            self.assertEqual(marginal(law, (0,)), {(i,): F(1, 3) for i in (-1, 0, 1)})
            self.assertEqual(marginal(law, (1,)), {(i,): F(1, 3) for i in (-1, 0, 1)})
            value = expectation(law, min)
            all_values.append(value)
            if expectation(law, lambda row: row[0]*row[1]) == 0:
                zero_covariance.append(value)
                self.assertGreaterEqual(value, F(-1, 2))
                self.assertLessEqual(value, F(-1, 3))
        self.assertEqual(len(all_values), 120)
        self.assertEqual((min(all_values), max(all_values)), (F(-2, 3), F(0)))
        self.assertEqual((min(zero_covariance), max(zero_covariance)), (F(-1, 2), F(-1, 3)))
        self.assertTrue(all(v >= F(-3, 5) for v in zero_covariance))
        self.assertTrue(any(v < F(-3, 5) for v in all_values))
        independent = {(x, y): F(1, 9) for x, y in product((-1, 0, 1), repeat=2)}
        self.assertEqual(expectation(independent, min), F(-4, 9))

    def test_pointwise_moment_certificates_on_normalized_grid(self):
        for x, y in product((F(k, 8) for k in range(-8, 9)), repeat=2):
            lower = (x+y+x*y-1)/2
            upper = (x+y)/2-(x-y)**2/4
            self.assertLessEqual(lower, min(x, y))
            self.assertLessEqual(min(x, y), upper)
        # Dropping the support condition invalidates the pointwise formulas.
        x = y = F(2)
        self.assertGreater((x+y+x*y-1)/2, min(x, y))
        x, y = F(3), F(-3)
        self.assertLess((x+y)/2-(x-y)**2/4, min(x, y))

    def test_same_moments_without_support_can_violate_both_endpoint_bounds(self):
        values = {}
        for amplitude in (F(6, 5), F(4), F(10), F(100)):
            p = 1/(3*amplitude**2)
            law = {(1, 0): p, (-1, 0): p, (0, 1): p, (0, -1): p, (0, 0): 1-4*p}
            self.assertEqual(expectation(law, lambda r: amplitude*r[0]), 0)
            self.assertEqual(expectation(law, lambda r: amplitude*r[1]), 0)
            self.assertEqual(expectation(law, lambda r: (amplitude*r[0])**2), F(2, 3))
            self.assertEqual(expectation(law, lambda r: (amplitude*r[1])**2), F(2, 3))
            self.assertEqual(expectation(law, lambda r: amplitude**2*r[0]*r[1]), 0)
            value = expectation(law, lambda r: amplitude*min(r))
            self.assertEqual(value, -2/(3*amplitude))
            self.assertLess(value, 0)
            self.assertLessEqual(value**2, F(1, 3))  # Weaker square-moment bound survives.
            values[amplitude] = value
        self.assertEqual(values[F(6, 5)], F(-5, 9))
        self.assertLess(values[F(6, 5)], F(-1, 2))
        self.assertEqual(values[F(4)], F(-1, 6))
        self.assertGreater(values[F(4)], F(-1, 3))

    def test_variable_sensitivity_means_hide_composite_error(self):
        for n, t in product((3, 4, 10, 100), (F(0), F(1, 4), F(1, 2), F(1))):
            errors = (1+(n-1)*t,) + (1-t,)*(n-1)
            sensitivities = tuple(2*d for d in errors)
            mean_error, mean_sensitivity = sum(errors)/n, sum(sensitivities)/n
            actual = sum(d*d for d in errors)/n
            product_mean = sum(k*d for k, d in zip(sensitivities, errors))/n
            self.assertEqual((mean_error, mean_sensitivity), (1, 2))
            self.assertEqual(actual, 1+(n-1)*t*t)
            self.assertGreaterEqual(actual, 1)
            self.assertLessEqual(actual, n)
            self.assertLessEqual(actual, product_mean)
            if t == 1:
                self.assertGreater(actual, mean_error*mean_sensitivity)
            for d, k in zip(errors, sensitivities):
                for u, v in product((d*F(i, 4) for i in range(5)), repeat=2):
                    self.assertLessEqual(abs(u*u-v*v), k*abs(u-v))

    def test_strict_sign_witness_checks_do_not_replace_the_limit_proof(self):
        for n in (1, 2, 10, 1000):
            value = -F(1, n)
            self.assertLess(value, 0)
            self.assertGreaterEqual(value, -1)
            prefix = tuple(-F(1, k) for k in range(1, min(n, 20)+1))
            self.assertTrue(all(v < 0 for v in prefix))
            self.assertFalse(all(v < 0 for v in prefix+(F(0),)))
        # Nonattainment and supremum zero are proved analytically in the note.

    def test_probability_and_dimension_guards(self):
        for law in ({}, {(0,): F(1, 2)}, {(0,): F(-1), (1,): F(2)}, {(0,): F(1, 2), (0, 1): F(1, 2)}):
            with self.assertRaises(ValueError):
                validate_law(law)
        for indices in ((), (-1,), (2,), (0, 0)):
            with self.assertRaises(ValueError):
                marginal({(0, 1): F(1)}, indices)
        with self.assertRaises(ValueError):
            information_values({(2, 0): F(1)}, ((1, 0), (0, 1)))
        with self.assertRaises(ValueError):
            compatible_error_law((F(-1), F(1), F(1)))
        with self.assertRaises(ValueError):
            parity_law(1, 0)


def snapshot(tests_run: int) -> dict:
    return {
        "scope": "Constructed F01 reconstruction fixtures; not a general reasoner, independent review, or held-out performance study.",
        "tests_run": tests_run,
        "exhaustive_bounds": {
            "binary_tables_support_pairs": 105,
            "parity_dimensions": [2, 3, 4, 5, 6, 7],
            "joint_nonempty_subsets": 511,
            "affine_two_component_order_comparisons": 5625,
            "three_action_truth_estimate_pairs": 729,
            "information_laws_payoff_tables": 2835,
            "conditional_ratio_cases": 180,
            "three_error_cap_grid_triples": 125,
            "joint_laws_denominator_6": 1716,
            "bottleneck_tuple_pairs": 15625,
            "exact_error_grid_vectors": 125,
            "independently_enumerated_pattern_mixtures": 165,
            "union_bound_reporting_cases": 1215,
            "tail_spike_examples": 48,
            "ternary_uniform_tables_denominator_12": 120,
            "pointwise_moment_grid_pairs": 289,
            "variable_sensitivity_profiles": 16,
        },
        "parity_minimum_means": {str(n): [str(expectation(parity_law(n, p), min)) for p in (0, 1)] for n in range(2, 8)},
        "shared_uncertainty_K100": {"exact_improvement": "2", "interval": ["-98", "102"]},
        "finite_range_guard": {"cap": "1", "true_code": "1/2", "reported_code": "3/5", "decoded_error": "1/2", "invalid_unclipped_bound": "2/5"},
        "minimax_midpoint_known_marginals": {"answer": "0", "uniform_absolute_error": "1"},
        "symmetric_ambiguous_choice": {"deterministic_worst_regret": "1", "randomized_expected_worst_regret": "1/2"},
        "conditioning_matched_marginals": ["1", "-1"],
        "pairwise_model_threshold": {"equal_error_cap": "1/3", "criterion": "epsilon_1 + epsilon_2 + epsilon_3 >= 1", "applies_to": "upper caps, not all exact error vectors", "witness": {"".join(map(str, row)): str(p) for row, p in sorted(compatible_error_law((F(1, 3),)*3).items())}},
        "exact_error_frontier": {"triple_pattern_weight": "(sum(r)-1)/2", "single_pattern_weights": "r_i - (sum(r)-1)/2", "criterion": "all four pattern weights nonnegative", "exact_110": "infeasible", "caps_110": "feasible"},
        "cost_update": {"scores": "(n-kappa,0), integer n>=1", "choose_first_worst_regret": "max(kappa-1,0)", "kappa_2": "1"},
        "marginal_coverage_counterexample": {"m": 100, "best_action_coverage": "1", "each_other_action_coverage": "99/100", "greedy_regret_probability_one": "1"},
        "geometric_tail": {"N": 8, "C": "1", "prefix": "251/128", "upper_tail": "5/128", "expectation_interval": ["251/128", "2"], "unrestricted_spike_expected_increment": "M"},
        "sharp_ternary_minimum": {"marginals_only": ["-2/3", "0"], "also_covariance_zero": ["-1/2", "-1/3"], "independence_only_if_assumed": "-4/9", "same_bounds_from": "support [-1,1], zero means, second moments 2/3, cross moment zero"},
        "support_countermodels": {"amplitude_6_over_5_minimum": "-5/9", "amplitude_4_minimum": "-1/6", "second_moments": "2/3", "cross_moment": "0"},
        "variable_sensitivity": {"mean_upstream_error": "1", "mean_local_sensitivity": "2", "sharp_composite_error_interval": "[1,n]", "correct_product_aggregation": "E[K*delta], not E[K]*E[delta]"},
        "general_claim_evidence": "Displayed proofs in the reconstruction note; finite test counts do not prove unrestricted statements.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(F01ReconstructionTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(snapshot(result.testsRun), indent=2, sort_keys=True)+"\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
