"""Exact finite F04 development fixtures; not a general calculus or trained model.

Run: python -m v2.checks.f04_countermodels --json path/to/report.json
All numerical inputs are integers or Fractions. None in an affine bound means
an unbounded endpoint, not an empty or inconsistent uncertainty set.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys
from typing import Iterable, Optional, Sequence
import unittest


def q(value: int | F) -> F:
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError("Exact arithmetic requires an int or Fraction, not float/bool.")
    return F(value)


def vec(values: Iterable[int | F]) -> tuple[F, ...]:
    return tuple(q(v) for v in values)


def probability(value: int | F) -> F:
    value = q(value)
    if not 0 <= value <= 1:
        raise ValueError("Probability outside [0, 1].")
    return value


def dot(a: Sequence[F], b: Sequence[F]) -> F:
    if len(a) != len(b):
        raise ValueError("Mismatched vector lengths.")
    return sum((x * y for x, y in zip(a, b)), F(0))


def brier(eta: int | F, p: int | F) -> F:
    eta, p = probability(eta), probability(p)
    return eta * (1 - p)**2 + (1 - eta) * p**2


def classification(eta: int | F, p: int | F) -> F:
    eta, p = probability(eta), probability(p)
    return 1 - eta if p >= F(1, 2) else eta


@dataclass(frozen=True)
class AffineFamily:
    """J = centre + unbounded*z + bounded*eps, with eps in [-1,1]^m."""
    centre: tuple[F, ...]
    unbounded: tuple[tuple[F, ...], ...]
    bounded: tuple[tuple[F, ...], ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, 'centre', vec(self.centre))
        object.__setattr__(self, 'unbounded', tuple(vec(r) for r in self.unbounded))
        object.__setattr__(self, 'bounded', tuple(vec(r) for r in self.bounded))
        n = len(self.centre)
        if not n or len(self.unbounded) != n or len(self.bounded) != n:
            raise ValueError("Nonempty family needs one row per output.")
        for matrix in (self.unbounded, self.bounded):
            if len({len(row) for row in matrix}) != 1:
                raise ValueError("Ragged source matrix.")

    def projected(self, w: Iterable[int | F]) -> tuple[F, tuple[F, ...], tuple[F, ...]]:
        w = vec(w)
        if len(w) != len(self.centre):
            raise ValueError("Wrong query dimension.")
        def columns(matrix: tuple[tuple[F, ...], ...]) -> tuple[F, ...]:
            return tuple(sum((w[i] * matrix[i][j] for i in range(len(w))), F(0))
                         for j in range(len(matrix[0])))
        return dot(w, self.centre), columns(self.unbounded), columns(self.bounded)

    def bounds(self, w: Iterable[int | F]) -> tuple[Optional[F], Optional[F]]:
        centre, nuisance, errors = self.projected(w)
        if any(nuisance):
            return None, None  # independently -infinity and +infinity
        radius = sum(map(abs, errors), F(0))
        return centre - radius, centre + radius

    def evaluate(self, z: Iterable[int | F], eps: Iterable[int | F]) -> tuple[F, ...]:
        z, eps = vec(z), vec(eps)
        if len(z) != len(self.unbounded[0]) or len(eps) != len(self.bounded[0]):
            raise ValueError("Wrong source dimension.")
        if any(abs(e) > 1 for e in eps):
            raise ValueError("Bounded error source outside [-1,1].")
        return tuple(c + dot(b, z) + dot(a, eps)
                     for c, b, a in zip(self.centre, self.unbounded, self.bounded))

    def pushforward(self, matrix: Iterable[Iterable[int | F]],
                    offset: Optional[Iterable[int | F]] = None) -> AffineFamily:
        rows = tuple(vec(row) for row in matrix)
        if not rows or any(len(row) != len(self.centre) for row in rows):
            raise ValueError("Invalid affine output map.")
        offset = vec(offset) if offset is not None else (F(0),) * len(rows)
        if len(offset) != len(rows):
            raise ValueError("Invalid affine offset dimension.")
        projections = [self.projected(row) for row in rows]
        return AffineFamily(tuple(p[0] + d for p, d in zip(projections, offset)),
                            tuple(p[1] for p in projections), tuple(p[2] for p in projections))


def shared_example() -> AffineFamily:
    return AffineFamily((F(3), F(1)), ((F(1),), (F(1),)), ((F(1, 4),), (F(-1, 4),)))


SELF_VERSION = 'F04_SELF_MIX_v1'


@dataclass(frozen=True)
class SelfBound:
    low_theta: F
    high_theta: F
    report: F
    failure_low: F
    failure_high: F
    version: str = SELF_VERSION


def self_bound(a: int | F, b: int | F) -> SelfBound:
    a, b = probability(a), probability(b)
    if a > b:
        raise ValueError("Empty evidence interval is not a vacuous certificate.")
    r = b / (1 + b)
    return SelfBound(a, b, r, a / (1 + b), r)


def validate_self_bound(bound: SelfBound, current_version: str = SELF_VERSION) -> None:
    if bound.version != current_version or current_version != SELF_VERSION:
        raise ValueError("Controller version mismatch.")
    expected = self_bound(bound.low_theta, bound.high_theta)
    if bound != expected:
        raise ValueError("Incorrect self-bound certificate.")


def deployed_failure(bound: SelfBound, theta: int | F,
                     current_version: str = SELF_VERSION) -> F:
    validate_self_bound(bound, current_version)
    theta = probability(theta)
    if not bound.low_theta <= theta <= bound.high_theta:
        raise ValueError("Actual model is outside the declared evidence contract.")
    return theta * (1 - bound.report)


def execute_self_policy(bound: SelfBound, theta: int | F,
                        control_coin: int | F, failure_coin: int | F) -> int:
    """Finite fixture for two independent uniform draws; theta belongs to environment."""
    deployed_failure(bound, theta)  # validate all inputs/contract first
    u, v = probability(control_coin), probability(failure_coin)
    if u == 1 or v == 1:
        raise ValueError("Uniform draws must be in [0,1).")
    if u < bound.report:
        return 0  # safe action; policy selection does not use theta
    return int(v < theta)


def assessment(low: int | F, high: int | F, tolerance: int | F) -> str:
    low, high, tolerance = q(low), q(high), q(tolerance)
    if low > high:
        raise ValueError("Empty interval.")
    return 'supported' if high <= tolerance else 'refuted' if low > tolerance else 'open'


def hard_response(r: int | F) -> F:
    return F(int(probability(r) < F(1, 2)))


def mix_response(b: int | F, r: int | F) -> F:
    return probability(b) * (1 - probability(r))


def identity_response(r: int | F) -> F:
    """Separate toy controller with report-independent calibration quality."""
    return probability(r)


def damped_response(b: int | F, r: int | F) -> F:
    return (probability(r) + mix_response(b, r)) / 2


@dataclass(frozen=True)
class TinyRelu:
    weights: tuple[tuple[F, ...], ...]
    biases: tuple[F, ...]
    output_weights: tuple[F, ...]
    output_bias: F = F(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, 'weights', tuple(vec(r) for r in self.weights))
        object.__setattr__(self, 'biases', vec(self.biases))
        object.__setattr__(self, 'output_weights', vec(self.output_weights))
        object.__setattr__(self, 'output_bias', q(self.output_bias))
        if not self.weights or not self.weights[0] or len({len(r) for r in self.weights}) != 1:
            raise ValueError("Nonempty rectangular weights required.")
        if not len(self.weights) == len(self.biases) == len(self.output_weights):
            raise ValueError("Hidden widths differ.")

    def hidden(self, x: Iterable[int | F]) -> tuple[F, ...]:
        x = vec(x)
        return tuple(max(F(0), dot(row, x) + bias) for row, bias in zip(self.weights, self.biases))

    def output(self, x: Iterable[int | F]) -> F:
        return self.output_bias + dot(self.output_weights, self.hidden(x))

    def gauge(self, scales: Iterable[int | F], permutation: Sequence[int]) -> TinyRelu:
        scales = vec(scales)
        n = len(self.weights)
        if (len(scales) != n or any(c <= 0 for c in scales) or
            len(permutation) != n or any(type(i) is not int for i in permutation) or
            set(permutation) != set(range(n))):
            raise ValueError("Positive scales and a genuine permutation are required.")
        return TinyRelu(tuple(tuple(c * w for w in self.weights[i]) for c, i in zip(scales, permutation)),
                        tuple(c * self.biases[i] for c, i in zip(scales, permutation)),
                        tuple(self.output_weights[i] / c for c, i in zip(scales, permutation)),
                        self.output_bias)

    def interchange(self, base: Iterable[int | F], donor: Iterable[int | F], indices: Sequence[int]) -> F:
        n = len(self.weights)
        if len(set(indices)) != len(indices) or any(type(i) is not int or i < 0 or i >= n for i in indices):
            raise ValueError("Invalid hidden-coordinate selection.")
        h, d = list(self.hidden(base)), self.hidden(donor)
        for i in indices:
            h[i] = d[i]
        return self.output_bias + dot(self.output_weights, h)


def example_network() -> TinyRelu:
    return TinyRelu(((F(1), F(2)), (F(-2), F(1)), (F(1), F(-1))),
                    (F(-1), F(1, 2), F(2)), (F(2), F(-1), F(3, 2)), F(-2))


def report() -> dict:
    old, new = self_bound(0, 1), self_bound(F(1, 5), F(2, 5))
    fam = shared_example()
    return {
        'scope': 'F04 constructed exact fixtures; no trained-network or general-calculus claim',
        'arithmetic': 'fractions.Fraction; all reported rationals are exact',
        'W1': {'eta': '3/5', 'old_brier': str(brier(F(3, 5), 1)),
               'new_brier': str(brier(F(3, 5), F(49, 100))),
               'old_classification_error': str(classification(F(3, 5), 1)),
               'new_classification_error': str(classification(F(3, 5), F(49, 100)))},
        'W2': {'new_minus_old': list(map(str, fam.bounds((-1, 1)))),
               'double_new_minus_old': ['-infinity', '+infinity'],
               'hypothesis': 'one shared unrestricted source plus one bounded source'},
        'self_update': {'old_report': str(old.report), 'new_report': str(new.report),
                        'new_deployed_interval': [str(new.failure_low), str(new.failure_high)],
                        'pointwise_equilibria_interval_not_deployed': ['1/6', '2/7'],
                        'fixed_theta_2_over_5_old_actual': str(deployed_failure(old, F(2, 5))),
                        'fixed_theta_2_over_5_new_actual': str(deployed_failure(new, F(2, 5))),
                        'unsafe_first_lower_iterate': '1/5; actual worst failure 8/25',
                        'safe_iteration_start': '1; all subsequent damped iterates remain upper bounds',
                        'old_assessment_at_1_over_3': assessment(old.failure_low, old.failure_high, F(1, 3)),
                        'new_assessment_at_1_over_3': assessment(new.failure_low, new.failure_high, F(1, 3))},
        'neural': {'trained': False, 'architecture': 'one-hidden-layer ReLU with affine output',
                   'controls': ['positive rescaling', 'permutation', 'unused duplicate', 'whole-layer baseline']},
        'finite_enumeration_bounds': {'brier_eta_p_pairs': '21x21 rational grid',
             'affine_bounded_extrema': '243 coefficient/centre/query configurations, 4 box vertices each',
             'self_bounds': 'all 66 ordered pairs on 1/10 grid; 11 within-interval theta values each',
             'policy_execution': '7x5 equiprobable pairs of independent discrete uniform draws',
             'neural_inputs': '25 integer grid pairs; 625 donor/base intervention pairs'},
        'unrestricted_proofs': 'See v2/derivations/01_candidate_countermodels.md; finite grids do not establish them.'
    }


class F04CountermodelTests(unittest.TestCase):
    def test_proxy_reversal(self):
        eta = F(3, 5)
        self.assertLess(brier(eta, F(49, 100)), brier(eta, 1))
        self.assertGreater(classification(eta, F(49, 100)), classification(eta, 1))
        self.assertEqual(brier(eta, F(49, 100)), F(2521, 10000))

    def test_brier_decomposition_and_regret_grid(self):
        for a, b in product(range(21), repeat=2):
            eta, p = F(a, 20), F(b, 20)
            excess_s = brier(eta, p) - eta * (1 - eta)
            excess_j = classification(eta, p) - min(eta, 1 - eta)
            self.assertEqual(excess_s, (p - eta)**2)
            self.assertLessEqual(excess_j**2, 4 * excess_s)

    def test_shared_unbounded_cancellation(self):
        fam = shared_example()
        self.assertEqual(fam.bounds((-1, 1)), (F(-5, 2), F(-3, 2)))
        self.assertEqual(fam.bounds((1, 0)), (None, None))
        self.assertEqual(fam.bounds((0, 1)), (None, None))
        for z, e in product((F(-10**50), F(0), F(10**50)), (F(-1), F(0), F(1))):
            old, new = fam.evaluate((z,), (e,))
            self.assertLessEqual(new + F(3, 2), old)

    def test_unshared_nuisance_breaks_comparison(self):
        fam = AffineFamily((3, 1), ((1, 0), (0, 1)), ((F(1, 4),), (F(-1, 4),)))
        self.assertEqual(fam.bounds((-1, 1)), (None, None))
        old, new = fam.evaluate((0, 4), (0,))
        self.assertEqual(new - old, 2)

    def test_changed_use_count_breaks_cancellation(self):
        self.assertEqual(shared_example().bounds((-1, 2)), (None, None))

    def test_box_projection_is_attained_on_vertices(self):
        # 3^5=243 scalar-output configurations, each with 2 bounded sources.
        for c, a, b, w, z in product((-1, 0, 1), repeat=5):
            fam = AffineFamily((c,), ((0,),), ((a, b),))
            low, high = fam.bounds((w,))
            values = [w * fam.evaluate((z,), e)[0] for e in product((-1, 1), repeat=2)]
            self.assertEqual((low, high), (min(values), max(values)))

    def test_same_marginal_intervals_different_margins(self):
        shared = AffineFamily((3, 1), ((), ()), ((1,), (1,)))
        separate = AffineFamily((3, 1), ((), ()), ((1, 0), (0, 1)))
        for w in ((1, 0), (0, 1)):
            self.assertEqual(shared.bounds(w), separate.bounds(w))
        self.assertEqual(shared.bounds((-1, 1)), (F(-2), F(-2)))
        self.assertEqual(separate.bounds((-1, 1)), (F(-4), F(0)))

    def test_joint_propagation_preserves_cancelled_source(self):
        fam = AffineFamily((0, 0), ((), ()), ((1,), (-1,)))
        self.assertEqual(fam.bounds((1, 0)), (F(-1), F(1)))
        self.assertEqual(fam.pushforward(((1, 1),)).bounds((1,)), (F(0), F(0)))

    def test_unit_change_and_offsets(self):
        fam = shared_example()
        for scale in (F(1, 1000), F(2), F(10**30)):
            g = fam.pushforward(((scale, 0), (0, scale)), (7, 7))
            self.assertEqual(g.bounds((-1, 1)), tuple(scale * x for x in fam.bounds((-1, 1))))

    def test_bad_affine_inputs_rejected(self):
        with self.assertRaises(ValueError):
            AffineFamily((1, 2), ((1,), ()), ((1,), (1,)))
        with self.assertRaises(ValueError):
            shared_example().bounds((1,))
        with self.assertRaises(ValueError):
            shared_example().evaluate((0,), (2,))
        with self.assertRaises(ValueError):
            shared_example().pushforward(((1,),))
        with self.assertRaises(TypeError):
            q(0.1)

    def test_report_is_least_robust_bound(self):
        for a, b in ((F(i, 10), F(j, 10)) for i in range(11) for j in range(i, 11)):
            cert = self_bound(a, b)
            self.assertEqual(mix_response(b, cert.report), cert.report)
            for k in range(11):
                theta = a + (b - a) * F(k, 10)
                self.assertLessEqual(deployed_failure(cert, theta), cert.report)
            if cert.report > 0:
                too_low = cert.report / 2
                self.assertGreater(mix_response(b, too_low), too_low)

    def test_executable_randomized_policy_matches_bound(self):
        cert = self_bound(F(1, 5), F(2, 5))
        failures = sum(execute_self_policy(cert, F(2, 5), F(i, 7), F(j, 5))
                       for i, j in product(range(7), range(5)))
        self.assertEqual(F(failures, 35), F(2, 7))

    def test_unknown_then_supported_self_assessment(self):
        old, new = self_bound(0, 1), self_bound(F(1, 5), F(2, 5))
        self.assertEqual(assessment(old.failure_low, old.failure_high, F(1, 3)), 'open')
        self.assertEqual(assessment(new.failure_low, new.failure_high, F(1, 3)), 'supported')

    def test_pointwise_equilibrium_interval_is_not_deployed(self):
        cert = self_bound(F(1, 5), F(2, 5))
        self.assertEqual(deployed_failure(cert, F(1, 5)), F(1, 7))
        self.assertLess(cert.failure_low, F(1, 6))

    def test_better_self_bound_can_raise_actual_failure(self):
        old, new = self_bound(0, 1), self_bound(F(1, 5), F(2, 5))
        self.assertLess(new.report, old.report)
        self.assertGreater(deployed_failure(new, F(2, 5)), deployed_failure(old, F(2, 5)))
        self.assertEqual(deployed_failure(old, F(2, 5)) + old.report, F(7, 10))
        self.assertEqual(deployed_failure(new, F(2, 5)) + new.report, F(4, 7))

    def test_unique_fixed_point_can_have_oscillating_iteration(self):
        r, values = F(0), []
        for _ in range(6):
            values.append(r)
            r = mix_response(1, r)
        self.assertEqual(values, [0, 1, 0, 1, 0, 1])
        self.assertEqual(mix_response(1, F(1, 2)), F(1, 2))

    def test_damped_iteration_exact_error_factor(self):
        for b, initial in product((F(0), F(1, 5), F(1, 2), F(1)), (F(0), F(1, 3), F(1))):
            fixed, r = b / (1 + b), initial
            for _ in range(8):
                nxt = damped_response(b, r)
                self.assertEqual(nxt - fixed, (1 - b) * (r - fixed) / 2)
                self.assertTrue(0 <= nxt <= 1)
                r = nxt

    def test_damped_lower_iterate_is_not_a_valid_report(self):
        r = damped_response(F(2, 5), F(0))
        self.assertEqual(r, F(1, 5))
        self.assertEqual(mix_response(F(2, 5), r), F(8, 25))
        self.assertGreater(mix_response(F(2, 5), r), r)

    def test_damped_upper_iterates_remain_deployable(self):
        for j in range(11):
            b, r = F(j, 10), F(1)
            fixed = b / (1 + b)
            for _ in range(12):
                nxt = damped_response(b, r)
                self.assertTrue(fixed <= nxt <= r <= 1)
                self.assertLessEqual(mix_response(b, nxt), nxt)
                self.assertEqual(nxt - fixed, (1 - b) * (r - fixed) / 2)
                r = nxt

    def test_hard_self_prediction_fails_on_grid_but_bound_exists(self):
        # General no-fixed-point proof is by cases in the note, not this grid.
        for i in range(101):
            r = F(i, 100)
            self.assertNotEqual(hard_response(r), r)
        self.assertLessEqual(hard_response(F(1, 2)), F(1, 2))

    def test_self_consistency_is_not_adequacy(self):
        r = F(9, 10)  # identity response is exactly calibrated
        failure = identity_response(r)
        self.assertEqual(failure, r)
        self.assertEqual(assessment(failure, failure, F(1, 10)), 'refuted')

    def test_version_and_evidence_scope(self):
        cert = self_bound(F(1, 5), F(2, 5))
        with self.assertRaises(ValueError):
            deployed_failure(cert, F(2, 5), 'ALWAYS_STRESS_v2')
        self.assertGreater(F(2, 5), cert.report)  # v2's actual loss exceeds old bound
        with self.assertRaises(ValueError):
            deployed_failure(cert, F(3, 5))
        with self.assertRaises(ValueError):
            self_bound(F(2, 5), F(1, 5))
        with self.assertRaises(ValueError):
            self_bound(-1, 1)
        with self.assertRaises(ValueError):
            validate_self_bound(SelfBound(F(0), F(1), F(0), F(0), F(0)))

    def test_gauge_preserves_output(self):
        net = example_network()
        gauged = net.gauge((3, F(1, 7), 11), (2, 0, 1))
        for x in product(range(-2, 3), repeat=2):
            self.assertEqual(net.output(x), gauged.output(x))

    def test_gauge_changes_raw_activations_preserves_contributions(self):
        net = example_network()
        scales, pi = (F(3), F(1, 7), F(11)), (2, 0, 1)
        gauged = net.gauge(scales, pi)
        for x in product(range(-2, 3), repeat=2):
            h, g = net.hidden(x), gauged.hidden(x)
            for j, i in enumerate(pi):
                self.assertEqual(g[j], scales[j] * h[i])
                self.assertEqual(gauged.output_weights[j] * g[j], net.output_weights[i] * h[i])
        self.assertNotEqual(net.hidden((1, 1)), gauged.hidden((1, 1)))

    def test_interchange_is_gauge_transportable(self):
        net = example_network()
        pi = (2, 0, 1)
        gauged = net.gauge((3, F(1, 7), 11), pi)
        old_indices = (0, 2)
        new_indices = tuple(j for j, i in enumerate(pi) if i in old_indices)
        points = tuple(product(range(-2, 3), repeat=2))
        for base, donor in product(points, repeat=2):
            self.assertEqual(net.interchange(base, donor, old_indices),
                             gauged.interchange(base, donor, new_indices))

    def test_unused_duplicate_is_decodable_not_causal(self):
        net = TinyRelu(((1,), (1,)), (0, 0), (1, 0))
        self.assertEqual(net.hidden((1,)), (F(1), F(1)))
        self.assertEqual(net.hidden((2,)), (F(2), F(2)))
        self.assertEqual(net.interchange((1,), (2,), (1,)), 1)
        self.assertEqual(net.interchange((1,), (2,), (0,)), 2)

    def test_whole_layer_interchange_is_only_donor_output(self):
        net = example_network()
        self.assertEqual(net.interchange((1, -1), (2, 1), (0, 1, 2)), net.output((2, 1)))

    def test_bad_neural_interventions_rejected(self):
        net = example_network()
        for scales, pi in (((0, 1, 1), (0, 1, 2)), ((1, 1, 1), (0, 0, 2))):
            with self.assertRaises(ValueError):
                net.gauge(scales, pi)
        with self.assertRaises(ValueError):
            net.interchange((0, 0), (1, 1), (0, 0))
        with self.assertRaises(ValueError):
            net.output((1,))

    def test_report_and_design_are_explicitly_nontraining(self):
        self.assertFalse(report()['neural']['trained'])
        design = Path(__file__).resolve().parents[1] / 'experiments/F04_neural_probe_design.md'
        text = design.read_text(encoding='utf-8')
        self.assertIn('design only', text)
        self.assertIn('F14 must freeze', text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(F04CountermodelTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report(), indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
