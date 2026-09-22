"""Exact development checks for the F02 continuation, not the future reasoner.

Run from the repository root:
    python -m v2.checks.f02_continuation --json v2/checks/F02_continuation_results.json
All finite checks use Fraction arithmetic. General claims are proved in the
accompanying mathematical note, not inferred from test counts.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from typing import Iterable, Sequence
import unittest

Number = int | F
Vector = tuple[F, ...]
Matrix = tuple[Vector, ...]
Edge = tuple[str, Vector, str]


def vector(values: Iterable[Number]) -> Vector:
    values = tuple(values)
    if any(isinstance(x, bool) or not isinstance(x, (int, F)) for x in values):
        raise TypeError("Only exact integer/Fraction inputs are accepted.")
    return tuple(F(x) for x in values)


def dot(x: Sequence[Number], y: Sequence[Number]) -> F:
    x, y = vector(x), vector(y)
    if len(x) != len(y):
        raise ValueError("Vector dimensions must agree.")
    return sum((a * b for a, b in zip(x, y)), F(0))


def law(values: Sequence[Number], dimension: int | None = None) -> Vector:
    p = vector(values)
    if not p or (dimension is not None and len(p) != dimension):
        raise ValueError("A law needs the declared nonempty interface.")
    if any(x < 0 for x in p) or sum(p) != 1:
        raise ValueError("A law must be nonnegative and sum to one.")
    return p


def matrix(rows: Iterable[Sequence[Number]]) -> Matrix:
    rows = tuple(vector(row) for row in rows)
    if not rows or not rows[0]:
        raise ValueError("Kernel interfaces must be nonempty.")
    return tuple(law(row, len(rows[0])) for row in rows)


def osc(values: Sequence[Number]) -> F:
    v = vector(values)
    if not v:
        raise ValueError("Oscillation needs a nonempty vector.")
    return max(v) - min(v)


def affine_value(r: Sequence[Number], p: Iterable[Sequence[Number]], h: Sequence[Number]) -> Vector:
    r, p, h = vector(r), matrix(p), vector(h)
    if len(r) != len(p) or len(h) != len(p[0]):
        raise ValueError("Affine interfaces do not match.")
    return tuple(c + dot(row, h) for c, row in zip(r, p))


def affine_span(r: Sequence[Number], p: Iterable[Sequence[Number]], bound: Number) -> F:
    r, p, m = vector(r), matrix(p), vector((bound,))[0]
    if len(r) != len(p) or m < 0:
        raise ValueError("Rewards and rows must match; the span bound is nonnegative.")
    return max(r[a] - r[b] + m * sum((abs(x-y) for x, y in zip(p[a], p[b])), F(0)) / 2
               for a in range(len(r)) for b in range(len(r)))


def menu_values(kernels: Iterable[Iterable[Sequence[Number]]], h: Sequence[Number]) -> tuple[Vector, ...]:
    ps = tuple(matrix(p) for p in kernels)
    if not ps:
        raise ValueError("The controlled menu is nonempty in this query.")
    shape = (len(ps[0]), len(ps[0][0]))
    if any((len(p), len(p[0])) != shape for p in ps):
        raise ValueError("Controlled branches need matching interfaces.")
    h = vector(h)
    if len(h) != shape[1]:
        raise ValueError("Continuation dimension mismatch.")
    return tuple(tuple(dot(row, h) for row in p) for p in ps)


def observation_values(values: Iterable[Sequence[Number]], weights: Sequence[Number]) -> tuple[F, F, tuple[int, ...]]:
    vs = tuple(vector(v) for v in values)
    if not vs:
        raise ValueError("At least one controlled branch is required.")
    mu = law(weights, len(vs[0]))
    if any(len(v) != len(mu) for v in vs):
        raise ValueError("Input interfaces do not match.")
    envelope = tuple(max(v[a] for v in vs) for a in range(len(mu)))
    blind = max(dot(mu, v) for v in vs)
    observed = dot(mu, envelope)
    common = tuple(i for i, v in enumerate(vs)
                   if all(mu[a] == 0 or v[a] == envelope[a] for a in range(len(mu))))
    return blind, observed, common


def _points(points: Iterable[Sequence[Number]], dimension: int) -> tuple[Vector, ...]:
    if dimension <= 0:
        raise ValueError("Cost dimension must be positive.")
    ps = tuple(vector(p) for p in points)
    if any(len(p) != dimension for p in ps):
        raise ValueError("Cost dimensions must agree.")
    return ps


def feasible(points: Iterable[Sequence[Number]], budget: Sequence[Number]) -> bool:
    b = vector(budget)
    return any(all(x <= y for x, y in zip(a, b)) for a in _points(points, len(b)))


def minimal(points: Iterable[Sequence[Number]], dimension: int) -> tuple[Vector, ...]:
    ps = sorted(set(_points(points, dimension)))
    return tuple(p for p in ps if not any(q != p and all(a <= b for a, b in zip(q, p)) for q in ps))


def sums(a: Iterable[Sequence[Number]], b: Iterable[Sequence[Number]], dimension: int) -> tuple[Vector, ...]:
    a, b = _points(a, dimension), _points(b, dimension)
    return minimal((tuple(x+y for x, y in zip(p, q)) for p in a for q in b), dimension)


def intersections(a: Iterable[Sequence[Number]], b: Iterable[Sequence[Number]], dimension: int) -> tuple[Vector, ...]:
    a, b = _points(a, dimension), _points(b, dimension)
    return minimal((tuple(max(x, y) for x, y in zip(p, q)) for p in a for q in b), dimension)


def scalar_optimum(points: Iterable[Sequence[Number]], weights: Sequence[Number]) -> F | None:
    w = vector(weights)
    if not w or any(x < 0 for x in w) or sum(w) == 0:
        raise ValueError("A nonzero nonnegative cost tradeoff is required.")
    ps = _points(points, len(w))
    return min((dot(w, p) for p in ps), default=None)  # None is infeasible, not numerical zero.


def translate(points: Iterable[Sequence[Number]], cost: Sequence[Number]) -> tuple[Vector, ...]:
    c = vector(cost)
    return minimal((tuple(x+y for x, y in zip(c, p)) for p in _points(points, len(c))), len(c))


def backward(edges: Iterable[Edge], downstream: dict[str, tuple[Vector, ...]], inputs: Sequence[str], dimension: int) -> dict[str, tuple[Vector, ...]]:
    edges = tuple((x, vector(c), y) for x, c, y in edges)
    if len(set(inputs)) != len(inputs):
        raise ValueError("Input names must be unique.")
    if any(x not in inputs or len(c) != dimension or y not in downstream for x, c, y in edges):
        raise ValueError("Unknown endpoint or mismatched cost interface.")
    return {x: minimal((p for src, c, y in edges if src == x for p in translate(downstream[y], c)), dimension)
            for x in inputs}


def compose_edges(first: Iterable[Edge], second: Iterable[Edge], dimension: int) -> tuple[Edge, ...]:
    first, second = tuple(first), tuple(second)
    if any(len(c) != dimension for _, c, _ in first + second):
        raise ValueError("Cost dimensions must agree.")
    return tuple((x, tuple(a+b for a, b in zip(vector(c), vector(d))), z)
                 for x, c, y in first for y2, d, z in second if y == y2)


def profile_masks(x: Sequence[Number], weights: Sequence[Number], low: Number, high: Number) -> tuple[Vector, Vector]:
    x = vector(x)
    p = law(weights, len(x))
    lo, hi = vector((low, high))
    if lo >= hi or any(a < lo or a > hi for a in x):
        raise ValueError("A valid supplied finite range is required.")
    if any(a == 0 for a in p):
        raise ValueError("Reconstruction divides by positive supported weights.")
    answers = tuple(dot(p, tuple(min(xj, hi if j == i else lo) for j, xj in enumerate(x))) for i in range(len(x)))
    decoded = tuple((answers[i] - (1-p[i])*lo) / p[i] for i in range(len(x)))
    return answers, decoded


def robust_reduction(rewards: Sequence[Number], kernels: Iterable[Sequence[Number]], suffix: Iterable[Sequence[Number]]) -> tuple[F, F, tuple[int, ...]]:
    r, p = vector(rewards), matrix(kernels)
    s = tuple(vector(v) for v in suffix)
    if len(r) != len(p) or len(s) != len(p) or any(len(v) != len(p[0]) for v in s):
        raise ValueError("The shared model and state interfaces must match.")
    k = tuple(min(v[b] for v in s) for b in range(len(p[0])))
    c = tuple(v + dot(row, k) for v, row in zip(r, p))
    coupled = tuple(v + dot(row, tail) for v, row, tail in zip(r, p, s))
    lower, exact = min(c), min(coupled)
    witnesses = tuple(i for i in range(len(r)) if c[i] == lower and
                      all(p[i][b] == 0 or s[i][b] == k[b] for b in range(len(k))))
    return lower, exact, witnesses


def normal_form_witness(h: Sequence[Number]) -> F:
    h = vector(h)
    if len(h) != 2:
        raise ValueError("The normal-form witness has two terminal coordinates.")
    l0 = dot((F(1, 4), F(3, 4)), h)
    l1 = dot((F(3, 4), F(1, 4)), h)
    l2, l3 = l0 + F(1, 2), dot((F(1, 2), F(1, 2)), h)
    return max(l0, min(l1, l2), min(l1, l3))


def normal_form_reference(h: Sequence[Number]) -> F:
    h = vector(h)
    if len(h) != 2:
        raise ValueError("The reference witness has two terminal coordinates.")
    d = h[0] - h[1]
    if d <= 0: g = d / 4
    elif d <= 1: g = 3 * d / 4
    elif d <= 2: g = d / 4 + F(1, 2)
    else: g = d / 2
    return h[1] + g


def budget_slack(source: Iterable[Sequence[Number]], target: Iterable[Sequence[Number]], scales: Sequence[Number]) -> F:
    s = vector(scales)
    if not s or any(x <= 0 for x in s):
        raise ValueError("Every component needs a strictly positive unit scale.")
    a, b = _points(source, len(s)), _points(target, len(s))
    if not a or not b:
        raise ValueError("This numerical query requires nonempty menus; handle unavailable menus separately.")
    return max(min(max(max((bi-ai)/si, F(0)) for ai, bi, si in zip(x, y, s))
                   for y in b) for x in a)


def ceil_fraction(x: F) -> int:
    return -((-x.numerator) // x.denominator)


def round_front(points: Iterable[Sequence[Number]], scales: Sequence[Number], quantum: Number) -> tuple[Vector, ...]:
    s, e = vector(scales), vector((quantum,))[0]
    if not s or any(x <= 0 for x in s) or e <= 0:
        raise ValueError("Positive scales and positive rounding quantum are required.")
    a = _points(points, len(s))
    if not a:
        return ()
    offset = tuple(min(x[i] for x in a) for i in range(len(s)))
    return minimal((tuple(ai + e*si*ceil_fraction((xi-ai)/(e*si))
                          for xi, ai, si in zip(x, offset, s)) for x in a), len(s))


def line_crossings(lines: Iterable[tuple[Number, Sequence[Number]]], bound: Number) -> tuple[F, ...]:
    """All possible affine-piece crossings on the two-terminal anchored span interval.

    This only enumerates the supplied pieces. Completeness for a function
    requires that its actual affine pieces are all supplied; arbitrary callables
    are not certified by this helper.
    """
    m = vector((bound,))[0]
    if m < 0:
        raise ValueError("The span bound is nonnegative.")
    pieces = tuple((vector((r,))[0], law(row, 2)) for r, row in lines)
    if not pieces:
        raise ValueError("At least one piece is required.")
    points = {-m, m}
    for r, row in pieces:
        for t, other in pieces:
            slope = row[0] - other[0]
            if slope:
                x = (t-r)/slope
                if -m <= x <= m:
                    points.add(x)
    return tuple(sorted(points))


def boolean_collision(h: Sequence[Number]) -> F:
    h = vector(h)
    if len(h) != 2:
        raise ValueError("Two terminal coordinates are required.")
    return min(dot((F(1, 2), F(1, 2)), h),
               max(dot((F(1, 4), F(3, 4)), h),
                   dot((F(3, 4), F(1, 4)), h) - F(1, 4)))


def encode_payoff(value: Number) -> F:
    x = vector((value,))[0]
    return x/(1+abs(x))


def decode_payoff(value: Number) -> F:
    x = vector((value,))[0]
    if not -1 < x < 1:
        raise ValueError("Finite payoff decoding requires the open code interval.")
    return x/(1-abs(x))


def encoded_shift(code: Number, shift: Number) -> F:
    z, v = vector((code, shift))
    if not -1 <= z <= 1:
        raise ValueError("Extended shift codes must lie in the closed interval.")
    if abs(z) == 1:
        return z  # A continuous limit for the encoded report, not a finite decoded payoff.
    return encode_payoff(decode_payoff(z)+v)


def logarithm_interval(value: Number, terms: int = 3) -> tuple[F, F]:
    """Rigorous rational enclosure from dyadic reduction and an integrated geometric series."""
    x = vector((value,))[0]
    if x <= 0 or isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("Positive input and a positive integer term count are required.")
    def core(u: F) -> tuple[F, F]:
        t = (u-1)/(u+1)
        low = 2*sum((t**(2*j+1)/F(2*j+1) for j in range(terms)), F(0))
        error = 2*t**(2*terms+1)/(F(2*terms+1)*(1-t*t))
        return low, low+error
    exponent, u = 0, x
    while u < 1:
        u *= 2; exponent -= 1
    while u >= 2:
        u /= 2; exponent += 1
    lo2, hi2 = core(F(2)); lou, hiu = core(u)
    if exponent >= 0:
        return exponent*lo2+lou, exponent*hi2+hiu
    return exponent*hi2+lou, exponent*lo2+hiu


def entropy_intercept_interval(probability: Number, terms: int = 3) -> tuple[F, F]:
    p = vector((probability,))[0]
    if not 0 <= p <= 1:
        raise ValueError("A probability in the closed unit interval is required.")
    l2, u2 = logarithm_interval(2, terms)
    lo, hi = -u2, -l2
    for weight in (p, 1-p):
        if weight:
            lower, upper = logarithm_interval(weight, terms)
            lo -= weight*upper; hi -= weight*lower
    return lo, hi


def rational_smooth_primitives() -> tuple[tuple[F, Vector], ...]:
    return tuple((entropy_intercept_interval(F(k, 64), 3)[0], (F(k, 64), F(64-k, 64))) for k in range(65))


def affine_breakpoints(lines: Iterable[tuple[Number, Number]], low: Number, high: Number) -> tuple[F, ...]:
    lo, hi = vector((low, high))
    pieces = tuple(vector(p) for p in lines)
    if lo > hi or not pieces or any(len(p) != 2 for p in pieces):
        raise ValueError("Provide affine intercept/slope pairs and an ordered interval.")
    pts = {lo, hi}
    for r, p in pieces:
        for t, q in pieces:
            if p != q:
                z = (t-r)/(p-q)
                if lo <= z <= hi: pts.add(z)
    return tuple(sorted(pts))


def convex_slack_from_tradeoffs(a: Iterable[Sequence[Number]], b: Iterable[Sequence[Number]]) -> F:
    aa, bb = _points(a, 2), _points(b, 2)
    if not aa or not bb:
        raise ValueError("This query requires nonempty menus.")
    pts = affine_breakpoints(((p[1], p[0]-p[1]) for p in aa+bb), 0, 1)
    return max(max(scalar_optimum(bb, (t, 1-t))-scalar_optimum(aa, (t, 1-t)), F(0)) for t in pts)


def convex_slack_two_target_segment(a: Iterable[Sequence[Number]], b: Iterable[Sequence[Number]]) -> F:
    """Directly optimize a target line-segment mixture, independently of the weight-query formula."""
    aa, bb = _points(a, 2), _points(b, 2)
    if not aa or len(bb) != 2:
        raise ValueError("Use a nonempty source and exactly two target vectors.")
    losses = []
    for x in aa:
        lines = ((F(0), F(0)),)+tuple((bb[0][i]-x[i], bb[1][i]-bb[0][i]) for i in range(2))
        pts = affine_breakpoints(lines, 0, 1)
        losses.append(min(max(r+t*p for r, p in lines) for t in pts))
    return max(losses)


class F02ContinuationTests(unittest.TestCase):
    def test_tradeoff_pair(self) -> None:
        a = ((0, 2), (2, 0)); b = a + ((F(3, 2), F(3, 2)),)
        for n in range(41):
            w = (F(n, 40), F(40-n, 40))
            self.assertEqual(scalar_optimum(a, w), scalar_optimum(b, w))

    def test_deterministic_budget_separation(self) -> None:
        a = ((0, 2), (2, 0)); budget = (F(3, 2), F(3, 2))
        self.assertFalse(feasible(a, budget)); self.assertTrue(feasible(a+(budget,), budget))

    def test_mean_lottery_vs_realized_caps(self) -> None:
        a = ((0, 2), (2, 0)); b = (F(3, 2), F(3, 2))
        mean = tuple((F(x)+y)/2 for x, y in zip(*a))
        self.assertTrue(feasible((mean,), b))
        self.assertFalse(any(feasible((point,), b) for point in a))

    def test_robust_randomization(self) -> None:
        for n in range(41):
            t = F(n, 40)
            worst = max(2*(1-t), 2*t)
            self.assertEqual(worst, 1+2*abs(t-F(1, 2)))
            self.assertGreaterEqual(worst, 1)
        self.assertEqual(max(F(1), F(1)), 1)
        self.assertEqual(F(1, 2)*2+F(1, 2)*2, 2)

    def test_compress_then_mix_is_conservative(self) -> None:
        for entries in product(range(3), repeat=4):
            a, b = entries[:2], entries[2:]
            for n in range(5):
                t = F(n, 4)
                direct = max(t*a[j]+(1-t)*b[j] for j in range(2))
                compressed = t*max(a)+(1-t)*max(b)
                self.assertLessEqual(direct, compressed)

    def test_adversary_observes_draw(self) -> None:
        costs = ((0, 2), (2, 0))
        self.assertEqual(min(max(row) for row in costs), 2)
        self.assertEqual(sum((F(1, 2)*max(row) for row in costs), F(0)), 2)

    def test_tradeoff_rejects_negative_and_zero_weights(self) -> None:
        for w in ((-1, 0), (0, 0)):
            with self.assertRaises(ValueError): scalar_optimum(((0, 0),), w)

    def test_positive_unit_change(self) -> None:
        points = ((0, 2), (2, 0), (F(3, 2), F(3, 2)))
        scales = (1000, F(1, 60))
        converted = tuple(tuple(x*s for x, s in zip(p, scales)) for p in points)
        for b in product((F(0), F(3, 2), F(2)), repeat=2):
            self.assertEqual(feasible(points, b), feasible(converted, tuple(x*s for x, s in zip(b, scales))))

    def test_equal_optimized_maps_blind_difference(self) -> None:
        identity = ((1, 0), (0, 1)); swap = ((0, 1), (1, 0))
        const_l = ((1, 0), (1, 0)); const_r = ((0, 1), (0, 1))
        for h in product((-2, 0, 3), repeat=2):
            v1 = menu_values((identity, swap), h)
            v2 = menu_values((identity, swap, const_l, const_r), h)
            self.assertEqual(tuple(max(v[a] for v in v1) for a in range(2)),
                             tuple(max(v[a] for v in v2) for a in range(2)))
        mu = (F(1, 2), F(1, 2)); h = (1, 0)
        self.assertEqual(observation_values(menu_values((identity, swap), h), mu)[:2], (F(1, 2), F(1)))
        self.assertEqual(observation_values(menu_values((identity, swap, const_l, const_r), h), mu)[:2], (F(1), F(1)))

    def test_blind_input_mixtures_do_not_repair(self) -> None:
        for n in range(21):
            t = F(n, 20)
            self.assertEqual((t+(1-t))/2, F(1, 2))

    def test_observation_equality_criterion(self) -> None:
        for entries in product((-1, 0, 1), repeat=4):
            vs = (entries[:2], entries[2:])
            for n in range(5):
                lo, hi, common = observation_values(vs, (F(n, 4), F(4-n, 4)))
                self.assertLessEqual(lo, hi)
                self.assertEqual(lo == hi, bool(common))

    def test_zero_probability_input_needs_no_common_maximum(self) -> None:
        lo, hi, common = observation_values(((1, 0), (0, 1)), (1, 0))
        self.assertEqual((lo, hi, common), (F(1), F(1), (0,)))

    def test_affine_span_exact_on_finite_family(self) -> None:
        rows = tuple((F(n, 4), F(4-n, 4)) for n in range(5))
        for p in product(rows, repeat=2):
            for r in product((-2, 0, 3), repeat=2):
                for m in (0, 1, 3):
                    reference = max(osc(affine_value(r, p, h)) for h in product((0, m), repeat=2))
                    self.assertEqual(affine_span(r, p, m), reference)

    def test_affine_span_pairwise_vs_separate_maxima(self) -> None:
        r = (0, 1, 2); p = ((0, 1), (1, 0), (0, 1))
        self.assertEqual(affine_span(r, p, 1), 2)
        self.assertEqual(osc(r)+1, 3)

    def test_affine_span_identical_rows(self) -> None:
        for m in (0, 1, 1000):
            self.assertEqual(affine_span((0, 10), ((F(1, 3), F(2, 3)),)*2, m), 10)

    def test_affine_span_worked_allowance(self) -> None:
        p = ((F(3, 4), F(1, 4)), (F(1, 4), F(3, 4)))
        self.assertEqual(affine_value((0, 1), p, (0, 2)), (F(1, 2), F(5, 2)))
        self.assertEqual(affine_span((0, 1), p, 2), 2)

    def test_suffix_cancellation_for_different_prefixes(self) -> None:
        q = ((F(1, 3), F(2, 3)),)*2
        for h in product((-100, 0, 137), repeat=2):
            tail = affine_value((0, 0), q, h)
            self.assertEqual(tail[0], tail[1])

    def test_nonzero_suffix_coefficient_has_separating_tasks(self) -> None:
        for t in (1, 10, 100):
            h = (-t, t)
            self.assertEqual(h[0]-h[1], -2*t)
        self.assertLess(-2*100+10, 0)

    def test_affine_invalid_inputs(self) -> None:
        for p in (((-1, 2),), ((F(1, 2), 0),), ((1, 0), (1,))):
            with self.assertRaises(ValueError): affine_span((0,), p, 1)
        with self.assertRaises(ValueError): affine_span((0,), ((1,),), -1)
        with self.assertRaises(TypeError): affine_span((0.5,), ((1,),), 1)

    def test_profile_masks_recover_supported_coordinates(self) -> None:
        weights = [(F(i, 6), F(j, 6), F(6-i-j, 6)) for i in range(1, 5) for j in range(1, 6-i)]
        self.assertEqual(len(weights), 10)
        for x in product((-1, 0, 1), repeat=3):
            for p in weights:
                _, decoded = profile_masks(x, p, -1, 1)
                self.assertEqual(decoded, vector(x))

    def test_profile_masks_reject_missing_premises(self) -> None:
        with self.assertRaises(ValueError): profile_masks((0, 1), (1, 0), 0, 1)
        with self.assertRaises(ValueError): profile_masks((0, 2), (F(1, 2),)*2, 0, 1)
        with self.assertRaises(ValueError): profile_masks((0, 0), (F(1, 2),)*2, 0, 0)

    def test_mask_difference_scales_with_coordinate_weight(self) -> None:
        p = (F(1, 4), F(3, 4)); x = (0, 1); y = (2, 1)
        a, _ = profile_masks(x, p, 0, 2); b, _ = profile_masks(y, p, 0, 2)
        self.assertEqual(abs(a[0]-b[0]), F(1, 2))
        self.assertEqual(a[1], b[1])
        self.assertEqual(abs(a[0]-b[0])/2, F(1, 4))

    def test_additive_positive_control(self) -> None:
        p = (F(1, 2),)*2; x = (3, -1); y = (-1, 3)
        self.assertEqual(dot(p, tuple(a+b for a, b in zip(x, y))), dot(p, x)+dot(p, y))
        self.assertEqual(dot(p, tuple(min(a, b) for a, b in zip(x, y))), -1)
        self.assertEqual(min(dot(p, x), dot(p, y)), 1)

    def test_intersection_does_not_distribute_through_sum(self) -> None:
        a = ((0, 2),); b = ((2, 0),); c = a+b
        lhs = sums(intersections(a, b, 2), c, 2)
        rhs = intersections(sums(a, c, 2), sums(b, c, 2), 2)
        self.assertEqual(lhs, (vector((2, 4)), vector((4, 2))))
        self.assertEqual(rhs, (vector((2, 2)),))
        self.assertFalse(feasible(lhs, (2, 2))); self.assertTrue(feasible(rhs, (2, 2)))

    def test_valid_intersection_sum_inclusion(self) -> None:
        pool = ((0, 2), (1, 1), (2, 0))
        menus = tuple(tuple(pool[i] for i in range(3) if bits & (1 << i)) for bits in range(1, 8))
        for a, b, c in product(menus, repeat=3):
            lhs = sums(intersections(a, b, 2), c, 2)
            rhs = intersections(sums(a, c, 2), sums(b, c, 2), 2)
            self.assertTrue(all(feasible(rhs, point) for point in lhs))

    def test_budget_backward_endpoint_example(self) -> None:
        r = (('x', vector((0, 0)), 'L'), ('x', vector((1, 0)), 'R'))
        b = {'L': (vector((100, 0)),), 'R': (vector((0, 0)),)}
        self.assertEqual(backward(r, b, ('x',), 2)['x'], (vector((1, 0)),))

    def test_backward_composition(self) -> None:
        r = (('x', vector((0, 1)), 'a'), ('x', vector((2, 0)), 'b'))
        s = (('a', vector((2, 0)), 'z'), ('a', vector((0, 3)), 'z'), ('b', vector((0, 1)), 'z'))
        b = {'z': (vector((1, 0)), vector((0, 2)))}
        direct = backward(compose_edges(r, s, 2), b, ('x',), 2)
        nested = backward(r, backward(s, b, ('a', 'b'), 2), ('x',), 2)
        self.assertEqual(direct, nested)

    def test_scalar_projection_of_budget_composition(self) -> None:
        edges = (('x', vector((0, 1)), 'a'), ('x', vector((2, 0)), 'b'))
        b = {'a': (vector((2, 0)), vector((0, 3))), 'b': (vector((0, 1)),)}
        total = backward(edges, b, ('x',), 2)['x']
        for n in range(11):
            w = (F(n, 10), F(10-n, 10))
            direct = scalar_optimum(total, w)
            separate = min(dot(w, c)+scalar_optimum(b[y], w) for _, c, y in edges)  # all suffixes nonempty here
            self.assertEqual(direct, separate)

    def test_empty_capability_is_not_zero_cost(self) -> None:
        r = (('x', vector((0,)), 'a'),)
        self.assertEqual(backward(r, {'a': ()}, ('x',), 1)['x'], ())
        self.assertIsNone(scalar_optimum((), (1,)))
        self.assertEqual(scalar_optimum(((0,),), (1,)), 0)

    def test_backward_rejects_wrong_interfaces(self) -> None:
        with self.assertRaises(ValueError): backward((('x', vector((0,)), 'missing'),), {}, ('x',), 1)
        with self.assertRaises(ValueError): backward((('x', vector((0, 0)), 'a'),), {'a': ()}, ('x',), 1)

    def test_nonlinear_terminal_budget_test_separates_menus(self) -> None:
        costs = ((0, 2), (2, 0), (F(3, 2), F(3, 2)))
        h = tuple(int(feasible((p,), (F(3, 2), F(3, 2)))) for p in costs)
        a = (((1, 0, 0),), ((0, 1, 0),)); b = a + (((0, 0, 1),),)
        self.assertEqual(max(v[0] for v in menu_values(a, h)), 0)
        self.assertEqual(max(v[0] for v in menu_values(b, h)), 1)

    def test_robust_reduction_strict_gap(self) -> None:
        self.assertEqual(robust_reduction((0, 1), ((1,), (1,)), ((1,), (0,))), (F(0), F(1), ()))

    def test_robust_reduction_unreachable_state(self) -> None:
        lo, exact, ws = robust_reduction((0, 10), ((1, 0), (0, 1)), ((0, 100), (100, 0)))
        self.assertEqual((lo, exact, ws), (F(0), F(0), (0,)))

    def test_robust_reduction_equality_finite_family(self) -> None:
        rows = ((F(0), F(1)), (F(1, 2), F(1, 2)), (F(1), F(0)))
        count = 0
        for r in product((-1, 0, 1), repeat=2):
            for ps in product(rows, repeat=2):
                for entries in product((0, 1), repeat=4):
                    suffix = (entries[:2], entries[2:])
                    lo, exact, witnesses = robust_reduction(r, ps, suffix)
                    # Directly enumerate independent suffix model choices at each intermediate state.
                    direct_lo = min(F(r[i])+sum((ps[i][j]*suffix[choices[j]][j] for j in range(2)), F(0))
                                    for i in range(2) for choices in product(range(2), repeat=2))
                    direct_exact = min(F(r[i])+dot(ps[i], suffix[i]) for i in range(2))
                    self.assertEqual((lo, exact), (direct_lo, direct_exact))
                    self.assertLessEqual(lo, exact)
                    self.assertEqual(lo == exact, bool(witnesses))
                    count += 1
        self.assertEqual(count, 1296)

    def test_robust_reduction_rejects_model_mismatch(self) -> None:
        with self.assertRaises(ValueError): robust_reduction((0,), ((1,), (1,)), ((0,), (1,)))
        with self.assertRaises(ValueError): robust_reduction((0,), ((1,),), ((0, 1),))

    def test_infinite_menu_claim_has_only_finite_prefix_checks(self) -> None:
        for n in (1, 2, 5, 20, 100):
            prefix = tuple((F(1, k), F(0)) for k in range(1, n+1))
            self.assertEqual(minimal(prefix, 2), ((F(1, n), F(0)),))
            self.assertFalse(feasible(prefix, (0, 0)))
            self.assertTrue(feasible(prefix, (F(1, n), 0)))
            self.assertLess(max(F(3)-F(1, k) for k in range(1, n+1)), 3)

    def test_fixture_report_is_deterministic(self) -> None:
        self.assertEqual(json.dumps(report(), sort_keys=True), json.dumps(report(), sort_keys=True))


    def test_nonconvex_normal_form_matches_piecewise_reference(self) -> None:
        count = 0
        for d in (F(k, 8) for k in range(-24, 33)):
            for shift in (F(k, 3) for k in range(-9, 10)):
                h = (d+shift, shift)
                self.assertEqual(normal_form_witness(h), normal_form_reference(h))
                count += 1
        self.assertEqual(count, 1083)

    def test_normal_form_is_monotone_and_shift_equivariant_on_grid(self) -> None:
        for h in product((F(-1), F(0), F(1, 2), F(1), F(2)), repeat=2):
            for inc in product((F(0), F(1, 4), F(1)), repeat=2):
                self.assertLessEqual(normal_form_witness(h), normal_form_witness(tuple(x+y for x, y in zip(h, inc))))
            for c in (-1000, F(-1, 3), 0, F(7, 2), 1000):
                self.assertEqual(normal_form_witness(tuple(x+c for x in h)), normal_form_witness(h)+c)

    def test_normal_form_is_neither_convex_nor_concave(self) -> None:
        g = lambda d: normal_form_witness((d, 0))
        self.assertLess(g(0), (g(-1)+g(1))/2)
        self.assertGreater(g(1), (g(F(1, 2))+g(F(3, 2)))/2)
        self.assertNotEqual(g(3), 2*g(F(3, 2)))

    def test_normal_form_nonexpansive_finite_pairs(self) -> None:
        points = tuple(product((F(-2), F(-1), F(0), F(1, 2), F(1), F(2)), repeat=2))
        for h, k in product(points, repeat=2):
            self.assertLessEqual(abs(normal_form_witness(h)-normal_form_witness(k)), max(abs(a-b) for a, b in zip(h, k)))

    def test_duplicator_breaks_common_shift(self) -> None:
        self.assertNotEqual(2*F(3), 2*F(0)+3)
        for offset in (-5, 0, 5):
            errors = [abs(F(offset)+n-2*n) for n in (10, 100, 1000)]
            self.assertTrue(errors[0] < errors[1] < errors[2])

    def test_tangent_approximation_rational_bound_ingredients(self) -> None:
        # This checks algebraic ingredients, not evaluation of transcendental coefficients.
        for u in (F(n, d) for n in range(1, 11) for d in range(1, 11)):
            self.assertEqual((1+u)**2-4*u, (u-1)**2)
            self.assertLessEqual(u/(1+u)**2, F(1, 4))
        exp_lower = F(1)+4+8+F(64, 6)+F(256, 24)
        self.assertEqual(exp_lower, F(103, 3))
        self.assertGreater(exp_lower, 32)
        self.assertEqual(F(1, 8)*F(1, 2)**2, F(1, 32))

    def test_directed_slack_separates_same_scalar_optima(self) -> None:
        a = ((0, 2), (2, 0)); b = a+((F(3, 2), F(3, 2)),)
        self.assertEqual(budget_slack(a, b, (1, 1)), 0)
        self.assertEqual(budget_slack(b, a, (1, 1)), F(1, 2))
        for scale in (1, 2, 10, 100):
            aa = tuple(tuple(scale*x for x in p) for p in a)
            bb = tuple(tuple(scale*x for x in p) for p in b)
            self.assertEqual(budget_slack(bb, aa, (1, 1)), F(scale, 2))

    def test_directed_slack_triangle_and_zero_inclusion(self) -> None:
        pool = ((0, 2), (1, 1), (2, 0))
        menus = tuple(tuple(pool[i] for i in range(3) if bits & (1 << i)) for bits in range(1, 8))
        for a, b, c in product(menus, repeat=3):
            self.assertLessEqual(budget_slack(a, c, (1, 1)), budget_slack(a, b, (1, 1))+budget_slack(b, c, (1, 1)))
        for a, b in product(menus, repeat=2):
            self.assertEqual(budget_slack(a, b, (1, 1)) == 0, all(feasible(b, x) for x in a))

    def test_slack_operation_bounds(self) -> None:
        menus = (((0, 2),), ((2, 0),), ((0, 2), (2, 0)), ((F(3, 2), F(3, 2)),))
        for a, b, c, d in product(menus, repeat=4):
            e, f = budget_slack(a, b, (1, 1)), budget_slack(c, d, (1, 1))
            self.assertLessEqual(budget_slack(sums(a, c, 2), sums(b, d, 2), (1, 1)), e+f)
            self.assertLessEqual(budget_slack(a+c, b+d, (1, 1)), max(e, f))
            self.assertLessEqual(budget_slack(intersections(a, c, 2), intersections(b, d, 2), (1, 1)), max(e, f))

    def test_slack_unit_changes_and_pruning(self) -> None:
        a = ((0, 2), (2, 0), (3, 3)); b = ((1, 1), (4, 4))
        base = budget_slack(a, b, (1, 1))
        self.assertEqual(base, budget_slack(minimal(a, 2), minimal(b, 2), (1, 1)))
        for diagonal in ((2, 3), (F(1, 10), 100)):
            aa = tuple(tuple(x*s for x, s in zip(p, diagonal)) for p in a)
            bb = tuple(tuple(x*s for x, s in zip(p, diagonal)) for p in b)
            self.assertEqual(base, budget_slack(aa, bb, diagonal))

    def test_slack_implies_translated_budget_and_scalar_guarantees(self) -> None:
        a = ((0, 2), (2, 0), (F(3, 2), F(3, 2))); b = ((0, 2), (2, 0))
        scales = (F(1), F(2)); e = budget_slack(a, b, scales)
        for budget in product((F(k, 2) for k in range(-1, 8)), repeat=2):
            if feasible(a, budget):
                self.assertTrue(feasible(b, tuple(x+e*s for x, s in zip(budget, scales))))
        for k in range(21):
            w = (F(k, 20), F(20-k, 20))
            self.assertLessEqual(scalar_optimum(b, w), scalar_optimum(a, w)+e*dot(w, scales))

    def test_rounding_keeps_tolerated_capability(self) -> None:
        a = ((0, 2), (2, 0), (F(3, 2), F(3, 2)))
        self.assertEqual(round_front(a, (1, 1), 1), (vector((0, 2)), vector((2, 0))))
        self.assertEqual(round_front(a, (1, 1), F(1, 4)), minimal(a, 2))
        for offset in ((0, 0), (-100, 500)):
            aa = tuple(tuple(x+y for x, y in zip(p, offset)) for p in a)
            for scales in ((1, 1), (F(1, 2), 2)):
                for e in (F(1, 4), F(1, 3), F(1), F(3)):
                    rounded = round_front(aa, scales, e)
                    self.assertEqual(budget_slack(rounded, aa, scales), 0)
                    self.assertLessEqual(budget_slack(aa, rounded, scales), e)
                    sizes = [1+ceil_fraction((max(p[i] for p in aa)-min(p[i] for p in aa))/(e*scales[i])) for i in range(2)]
                    self.assertLessEqual(len(rounded), sizes[0]*sizes[1])

    def test_slack_and_rounding_input_guards(self) -> None:
        with self.assertRaises(ValueError): budget_slack(((0,),), (), (1,))
        with self.assertRaises(ValueError): budget_slack(((0,),), ((1,),), (0,))
        with self.assertRaises(ValueError): budget_slack(((0, 1),), ((1,),), (1,))
        with self.assertRaises(ValueError): round_front(((0,),), (1,), 0)
        with self.assertRaises(TypeError): round_front(((0,),), (1,), 0.5)
        self.assertEqual(round_front((), (1,), 1), ())

    def test_zero_cost_slack_does_not_preserve_unmatched_endpoints(self) -> None:
        first = (('x', vector((0,)), 'u'),); substitute = (('x', vector((0,)), 'v'),)
        suffix = (('u', vector((0,)), 'z'), ('v', vector((100,)), 'z'))
        self.assertEqual(budget_slack((first[0][1],), (substitute[0][1],), (1,)), 0)
        a = tuple(c for _, c, _ in compose_edges(first, suffix, 1))
        b = tuple(c for _, c, _ in compose_edges(substitute, suffix, 1))
        self.assertEqual(budget_slack(a, b, (1,)), 100)

    def test_vertex_only_transformer_comparison_is_false(self) -> None:
        t = lambda h: max(F(h[0]), F(h[1])-F(1, 2))
        u = lambda h: sum(map(F, h), F(0))/2
        for h in product((0, 1), repeat=2):
            self.assertGreaterEqual(t(h), u(h))
        self.assertEqual(t((0, F(1, 2)))-u((0, F(1, 2))), F(-1, 4))
        pieces = ((0, (1, 0)), (F(-1, 2), (0, 1)), (0, (F(1, 2), F(1, 2))))
        vertices = line_crossings(pieces, 1)
        self.assertIn(F(-1, 2), vertices)
        diffs = tuple(t((d, 0))-u((d, 0)) for d in vertices)
        self.assertEqual((min(diffs), max(diffs)), (F(-1, 4), F(1, 2)))

    def test_boolean_terminal_collision_and_internal_gap(self) -> None:
        u = lambda h: sum(map(F, h), F(0))/2
        for h in product((0, 1), repeat=2):
            self.assertEqual(boolean_collision(h), u(h))
        self.assertEqual(boolean_collision((F(1, 2), 0)), F(1, 8))
        pieces = ((0, (F(1, 2), F(1, 2))), (0, (F(1, 4), F(3, 4))),
                  (F(-1, 4), (F(3, 4), F(1, 4))))
        vertices = line_crossings(pieces, 1)
        diffs = tuple(boolean_collision((d, 0))-u((d, 0)) for d in vertices)
        self.assertEqual((min(diffs), max(diffs)), (F(-1, 8), F(0)))

    def test_piece_crossings_suffice_for_displayed_grid_family(self) -> None:
        for reward in (F(-1), F(-1, 2), F(0), F(1, 2), F(1)):
            for slope in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
                for m in (F(0), F(1, 2), F(1), F(2)):
                    pieces = ((0, (1, 0)), (reward, (0, 1)), (0, (slope, 1-slope)))
                    pts = line_crossings(pieces, m)
                    diff = lambda d: max(d, reward)-slope*d
                    low, high = min(map(diff, pts)), max(map(diff, pts))
                    for k in range(41):
                        val = diff(-m+2*m*F(k, 40))
                        self.assertLessEqual(low, val); self.assertLessEqual(val, high)

    def test_affine_primitive_is_recovered_by_zero_and_indicator_tests(self) -> None:
        r = (F(-2), F(3, 2)); p = ((F(1, 3), F(2, 3)), (F(3, 4), F(1, 4)))
        zero = affine_value(r, p, (0, 0))
        cols = tuple(tuple(x-y for x, y in zip(affine_value(r, p, e), zero)) for e in ((1, 0), (0, 1)))
        self.assertEqual(zero, r)
        self.assertEqual(tuple(tuple(cols[j][i] for j in range(2)) for i in range(2)), p)

    def test_crossing_enumeration_input_guards(self) -> None:
        with self.assertRaises(ValueError): line_crossings(((0, (1, 0)),), -1)
        with self.assertRaises(ValueError): line_crossings((), 1)
        with self.assertRaises(ValueError): line_crossings(((0, (2, -1)),), 1)
        self.assertEqual(line_crossings(((0, (1, 0)),), 0), (F(0),))


    def test_raw_codes_hide_opposite_unit_rankings(self) -> None:
        for c in (0, 1, 10, 1000, 10**6):
            lo, hi = encode_payoff(c), encode_payoff(c+1)
            gap = F(1, (c+1)*(c+2))
            self.assertEqual(hi-lo, gap)
            middle = (lo+hi)/2
            self.assertEqual(abs(middle-lo), gap/2)
            self.assertEqual(abs(middle-hi), gap/2)
            for k in range(11):
                probability = F(k, 10)
                self.assertGreaterEqual(max(probability, 1-probability), F(1, 2))

    def test_encoded_mean_cancellation_paths(self) -> None:
        for c in (1000, 10**4, 10**6):
            for k in (-100, -1, 0, 1, 100):
                a, b = encode_payoff(c+k), encode_payoff(-c)
                answer = encode_payoff((decode_payoff(a)+decode_payoff(b))/2)
                self.assertEqual(answer, encode_payoff(F(k, 2)))
                self.assertLess(abs(a-1), F(1, c-100))
                self.assertLess(abs(b+1), F(1, c-100))
        for c in (1, 10, 1000):
            gap = encode_payoff(c+1)-encode_payoff(c)
            self.assertEqual(F(1, 3)/gap, F((c+1)*(c+2), 3))

    def test_centering_preserves_continuation_differences(self) -> None:
        maps = (lambda h: h[0], lambda h: h[1],
                lambda h: (h[0]+h[1])/2-F(1, 4),
                lambda h: max(h[0], h[1]-F(1, 2)))
        for c in (F(-10**6), F(0), F(10**6)):
            for d in (F(k, 4) for k in range(-4, 5)):
                relative = (d, F(0)); actual = (d+c, c)
                for fn in maps:
                    self.assertEqual(fn(actual), fn(relative)+c)
                self.assertEqual(max(range(len(maps)), key=lambda j: maps[j](relative)),
                                 max(range(len(maps)), key=lambda j: maps[j](actual)))

    def test_clipped_relative_codes_control_real_input_error(self) -> None:
        for m in (F(0), F(1, 4), F(1), F(3)):
            for k in range(9):
                x = -m+2*m*F(k, 8)
                for error in (F(-1, 10), F(0), F(1, 10)):
                    received = encode_payoff(x)+error
                    clipped = min(encode_payoff(m), max(encode_payoff(-m), received))
                    decoded = decode_payoff(clipped)
                    self.assertLessEqual(abs(decoded-x), (1+m)**2*abs(error))
                    self.assertLessEqual(abs(decoded), m)

    def test_relative_greedy_regret_is_simultaneously_bounded(self) -> None:
        maps = (lambda h: h[0], lambda h: h[1],
                lambda h: (h[0]+h[1])/2-F(1, 4),
                lambda h: max(h[0], h[1]-F(1, 2)))
        for d in (F(k, 8) for k in range(-8, 9)):
            h = (d, F(0))
            for errors in product((F(-1, 20), F(0), F(1, 20)), repeat=2):
                hd = tuple(decode_payoff(min(F(1, 2), max(F(-1, 2), encode_payoff(x)+e))) for x, e in zip(h, errors))
                delta = max(abs(x-y) for x, y in zip(h, hd))
                action = max(range(len(maps)), key=lambda j: maps[j](hd))
                regret = max(fn(h) for fn in maps)-maps[action](h)
                self.assertLessEqual(delta, F(1, 5))
                self.assertLessEqual(regret, 2*delta)
                self.assertLessEqual(regret, F(2, 5))

    def test_encoded_shift_has_bounded_parameter_sensitivity(self) -> None:
        codes = (F(-1), F(-999, 1000), F(-1, 2), F(0), F(1, 2), F(999, 1000), F(1))
        shifts = (F(-3), F(-1), F(0), F(1), F(3))
        for v in shifts:
            for z, zz in product(codes, repeat=2):
                self.assertLessEqual(abs(encoded_shift(z, v)-encoded_shift(zz, v)), 16*abs(z-zz))
        for z in codes:
            for v, vv in product(shifts, repeat=2):
                self.assertLessEqual(abs(encoded_shift(z, v)-encoded_shift(z, vv)), abs(v-vv))

    def test_loss_of_normalization_leaks_the_common_level(self) -> None:
        zeta = F(1, 100)
        for c in (100, 1000, 10**6):
            self.assertEqual((1+zeta)*c-c, zeta*c)
        self.assertGreater(F(0), 2*F(0)-1)
        self.assertLess(F(2), 2*F(2)-1)

    def test_finite_decode_and_boundary_extension_are_different(self) -> None:
        for endpoint in (-1, 1):
            with self.assertRaises(ValueError): decode_payoff(endpoint)
            self.assertEqual(encoded_shift(endpoint, 100), endpoint)
        with self.assertRaises(ValueError): encoded_shift(F(3, 2), 0)
        with self.assertRaises(TypeError): encode_payoff(0.5)


    def test_rational_log_enclosures_are_nested(self) -> None:
        for x in (F(k, 64) for k in range(1, 65)):
            lo, hi = logarithm_interval(x, 3)
            tight_lo, tight_hi = logarithm_interval(x, 8)
            self.assertLessEqual(lo, tight_lo); self.assertLessEqual(tight_hi, hi)
            self.assertLessEqual(hi-lo, F(7, 6804))
        lo, hi = logarithm_interval(2, 3)
        self.assertEqual(hi-lo, F(1, 6804))
        self.assertEqual(logarithm_interval(1), (F(0), F(0)))

    def test_rational_smooth_intercept_certificate(self) -> None:
        primitives = rational_smooth_primitives()
        self.assertEqual(len(primitives), 65)
        for k, (r, row) in enumerate(primitives):
            lo, hi = entropy_intercept_interval(F(k, 64), 3)
            tight_lo, tight_hi = entropy_intercept_interval(F(k, 64), 8)
            self.assertEqual(row, law(row, 2)); self.assertEqual(r, lo)
            self.assertLessEqual(lo, tight_lo); self.assertLessEqual(tight_hi, hi)
            self.assertLessEqual(hi-lo, F(2, 1701))
        self.assertLess(F(1, 32)+F(2, 1701), F(1, 16))
        self.assertLess(F(21, 4096), F(1, 32))
        lo, hi = entropy_intercept_interval(F(1, 2))
        self.assertLessEqual(lo, 0); self.assertLessEqual(0, hi)

    def test_rational_smooth_values_with_independent_log_intervals(self) -> None:
        primitives = rational_smooth_primitives()
        for exponent in range(-12, 13):
            ratio = F(2)**exponent
            dlo, dhi = logarithm_interval(ratio, 10)
            glo, ghi = logarithm_interval((1+ratio)/2, 10)
            approximation_lo = max(r+row[0]*dlo for r, row in primitives)
            approximation_hi = max(r+row[0]*dhi for r, row in primitives)
            self.assertLessEqual(approximation_hi, glo)
            self.assertLessEqual(ghi-approximation_lo, F(1, 32)+F(2, 1701))

    def test_log_and_intercept_guards(self) -> None:
        with self.assertRaises(ValueError): logarithm_interval(0)
        with self.assertRaises(ValueError): logarithm_interval(1, 0)
        with self.assertRaises(TypeError): logarithm_interval(0.5)
        with self.assertRaises(ValueError): entropy_intercept_interval(F(3, 2))

    def test_convex_slack_matches_direct_mixture_optimization(self) -> None:
        pool = ((0, 0), (0, 2), (2, 0), (2, 2))
        menus = tuple(product(pool, repeat=2))
        count = 0
        for a, b in product(menus, repeat=2):
            self.assertEqual(convex_slack_from_tradeoffs(a, b), convex_slack_two_target_segment(a, b))
            count += 1
        self.assertEqual(count, 256)

    def test_convex_slack_is_not_deterministic_slack(self) -> None:
        a = ((0, 2), (2, 0)); b = a+((F(3, 2), F(3, 2)),)
        self.assertEqual(convex_slack_from_tradeoffs(b, a), 0)
        self.assertEqual(budget_slack(b, a, (1, 1)), F(1, 2))
        shifted = tuple((F(x)+F(1, 4), F(y)+F(1, 2)) for x, y in a)
        self.assertEqual(convex_slack_from_tradeoffs(a, shifted), F(1, 2))
        other = a+((F(1), F(1, 2)),)
        for w in ((1, 0), (0, 1)):
            self.assertEqual(scalar_optimum(a, w), scalar_optimum(other, w))
        self.assertEqual(scalar_optimum(a, (F(1, 2), F(1, 2))), 1)
        self.assertEqual(scalar_optimum(other, (F(1, 2), F(1, 2))), F(3, 4))

    def test_common_signal_example_for_all_carriers(self) -> None:
        probabilities = (F(3, 8), F(1, 8), F(1, 8), F(3, 8))
        gross = (dot(probabilities, (3, 3, -1, -1)), dot(probabilities, (3, -1, -1, 3)), F(3))
        self.assertEqual(gross, (F(1), F(2), F(3)))
        menu = ((F(1, 2), F(0)), (F(1, 4), F(1)), (F(0), F(3)))
        self.assertEqual(minimal(menu, 2), tuple(sorted(menu)))
        self.assertEqual(tuple(v-F(1, 4)*cost for v, (_, cost) in zip(gross, menu)), (F(1), F(7, 4), F(9, 4)))
        self.assertTrue(feasible(menu, (F(1, 4), 1)))
        self.assertFalse(feasible(menu, (F(1, 10), 1)))
        self.assertEqual(tuple(v-cost for v, (_, cost) in zip(gross, menu)), (F(1), F(1), F(0)))
        self.assertEqual(-F(1, 4)+dot((F(1, 2), F(1, 2)), (2, 2)), F(7, 4))


def report() -> dict[str, object]:
    return {
        'task': 'F02 continuation; constructed development evidence',
        'general_claim_basis': 'Displayed conditional proofs, not extrapolation from finite tests',
        'scalarization': {'A': [[0, 2], [2, 0]], 'B_extra': ['3/2', '3/2'],
                         'same_weighted_optima': True, 'separating_budget': ['3/2', '3/2'],
                         'convexified_mean_witness': [1, 1]},
        'randomized_robust_cost': {'pure_or_draw_observing_adversary': '2', 'independent_hidden_model_half_mixture': '1'},
        'blind_input': {'identity_swap': '1/2', 'menu_with_constant_output': '1', 'observed_input_both': '1'},
        'affine_suffix': {'exact_span': '2', 'generic_span_bound': '3', 'identical_rows_cancel_prefix_kernel_difference': True},
        'G_intersection_sum': {'left_generators': [[2, 4], [4, 2]], 'right_generators': [[2, 2]]},
        'robust_reduction': {'anti_correlated_rewards': {'lower': '0', 'coupled': '1'},
                             'unreachable_state_example': {'lower': '0', 'coupled': '0'}},
        'exhaustive_finite_checks': {'scalar_tradeoff_weights': 41, 'robust_mixture_bound_cases': 405,
                                   'observation_equality_cases': 405, 'affine_span_cases': 675,
                                   'profile_mask_profiles_and_laws': 270, 'G_inclusion_menu_triples': 343,
                                   'robust_reduction_cases': 1296},
        'new_boundaries': {'nonconvex_normal_form_grid': 1083, 'slack_triangle_menu_triples': 343,
                           'slack_operation_menu_quadruples': 256, 'crossing_comparison_instances': 100,
                           'vertex_only_missed_deficit': '-1/4', 'boolean_test_missed_deficit': '-1/8',
                           'same_scalar_optima_directed_slack': '1/2',
                           'smooth_eleven_primitive_analytic_error_bound': '1/32',
                           'bounded_mean_closed_box_uniform_error_lower_bound': '1',
                           'relative_greedy_cases': 153, 'recoding_cancellation_paths': 15, 'rational_smooth_primitives': 65,
                           'rational_smooth_global_error_bound': str(F(1, 32)+F(2, 1701)),
                           'rational_log_value_checks': 25, 'convex_slack_direct_mixture_cases': 256},
        'infinite_menu': 'Only finite prefixes tested; nonattainment follows from the proof in the note',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path, help='Write the deterministic report after all tests pass.')
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F02ContinuationTests))
    if not result.wasSuccessful():
        return 1
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        with args.json.open('w', encoding='utf-8', newline='\n') as stream:
            json.dump(report(), stream, indent=2, sort_keys=True)
            stream.write('\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
