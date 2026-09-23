"""Finite numeric witnesses for the F03 belief/KL source adapters.

Probabilities use explicit finite tables. Logarithms use binary64 math.log;
passing toleranced tests does not prove an unrestricted identity or a logic.
No source equation is silently installed as an inference rule.
"""
from __future__ import annotations

import argparse
from itertools import product
import json
import math
from pathlib import Path
import unittest
from typing import Sequence


def probability(values: Sequence[float]) -> tuple[float, ...]:
    p = tuple(float(x) for x in values)
    if not p or any(not math.isfinite(x) or x < 0 for x in p):
        raise ValueError('Expected a nonempty finite nonnegative probability vector')
    if not math.isclose(math.fsum(p), 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError('Probability mass must sum to one')
    return p


def kl(q: Sequence[float], p: Sequence[float]) -> float:
    """D(q||p), including 0 log 0 = 0 and positive/zero = infinity."""
    q, p = probability(q), probability(p)
    if len(q) != len(p):
        raise ValueError('Probability vectors have different supports')
    if any(qi > 0 and pi == 0 for qi, pi in zip(q, p)):
        return math.inf
    return math.fsum(qi * (math.log(qi) - math.log(pi))
                     for qi, pi in zip(q, p) if qi > 0)


def cross_entropy(q: Sequence[float], p: Sequence[float]) -> float:
    q, p = probability(q), probability(p)
    if len(q) != len(p):
        raise ValueError('Probability vectors have different supports')
    if any(qi > 0 and pi == 0 for qi, pi in zip(q, p)):
        return math.inf
    return -math.fsum(qi * math.log(pi) for qi, pi in zip(q, p) if qi > 0)


def expectation(q: Sequence[float], f: Sequence[float]) -> float:
    q = probability(q)
    if len(q) != len(f) or any(math.isnan(float(x)) for x in f):
        raise ValueError('Invalid values or support size')
    return math.fsum(qi * float(fi) for qi, fi in zip(q, f) if qi > 0)


def channel(p: Sequence[float], rows: Sequence[Sequence[float]]) -> tuple[float, ...]:
    p = probability(p)
    rows = tuple(probability(row) for row in rows)
    if len(rows) != len(p) or len({len(row) for row in rows}) != 1:
        raise ValueError('Invalid stochastic channel dimensions')
    return tuple(math.fsum(pi * row[j] for pi, row in zip(p, rows))
                 for j in range(len(rows[0])))


def soft_value(p: Sequence[float], f: Sequence[float], beta: float = 1,
               robust: bool = False) -> tuple[float, tuple[float, ...]]:
    """Return signed soft value and optimizing law using stable log-sum-exp.

    robust=False: inf_q beta D(q||p)+E_q f.
    robust=True:  sup_q E_q f-beta D(q||p).
    f is finite and beta is strictly positive; these are explicit restrictions.
    """
    p = probability(p)
    if len(f) != len(p) or any(not math.isfinite(float(x)) for x in f):
        raise ValueError('Soft-value adapter requires finite costs on this finite support')
    if not math.isfinite(beta) or beta <= 0:
        raise ValueError('beta must be positive and finite')
    sign = 1 if robust else -1
    terms = [math.log(pi) + sign * float(fi) / beta if pi else -math.inf
             for pi, fi in zip(p, f)]
    high = max(terms)
    logz = high + math.log(math.fsum(math.exp(v - high) for v in terms))
    opt = tuple(math.exp(v - logz) if math.isfinite(v) else 0.0 for v in terms)
    return sign * beta * logz, opt


def condition(p: Sequence[float], event: Sequence[bool]) -> tuple[float, tuple[float, ...]]:
    p = probability(p)
    if len(event) != len(p):
        raise ValueError('Event and probability spaces differ')
    mass = math.fsum(pi for pi, yes in zip(p, event) if yes)
    if mass == 0:
        raise ValueError('No normalized posterior for a zero-probability event')
    return -math.log(mass), tuple(pi / mass if yes else 0 for pi, yes in zip(p, event))


def binary_grid(denominator: int = 8) -> list[tuple[float, float]]:
    return [(i / denominator, 1 - i / denominator) for i in range(denominator + 1)]


def results() -> dict:
    p, q, r = (1., 0.), (.5, .5), (.25, .75)
    lower, lo_opt = soft_value(q, (0, math.log(3)))
    upper, hi_opt = soft_value(q, (0, math.log(3)), robust=True)
    return {
        'task': 'F03', 'scope': 'finite constructed numeric source-adapter witnesses',
        'arithmetic': 'binary64 logarithms, explicit tolerances; not exact symbolic proof',
        'log_base': 'e', 'held_out': False,
        'kl_triangle_counterexample': {'direct': kl(p, r), 'via': kl(p, q) + kl(q, r)},
        'conflicting_beliefs_minimum': -2 * math.log(.6),
        'soft_cost': {'costs': [0, math.log(3)], 'optimistic': lower,
                      'optimistic_law': lo_opt, 'robust': upper, 'robust_law': hi_opt},
        'conditioning_same_posterior_offsets': [math.log(2), math.log(4)],
        'lsc_residual_witness': {'value_at_zero': 1, 'values_at_positive_sequence': 0},
        'infinite_partition_prefix_values': {str(n): math.log(n) for n in (1, 2, 4, 16, 64)},
        'enumeration_bounds': {'binary_probability_grid_denominator': 8,
            'binary_channels': 81, 'KL_channel_comparisons': 6561,
            'finite_cost_coordinates': [-2, 0, 3],
            'sequence_chain_rule': '2 binary stages; 2 input laws and 2 kernels each',
            'infinite_claims': 'analytic notes only; finite prefixes do not establish infinity'},
    }


class F03BeliefKLTests(unittest.TestCase):
    def assertNear(self, x: float, y: float, tolerance: float = 1e-10) -> None:
        self.assertTrue(math.isclose(x, y, rel_tol=tolerance, abs_tol=tolerance), (x, y))

    def test_probability_validation(self):
        for p in ((), (-1, 2), (.1, .2), (math.inf, 0), (math.nan, 1)):
            with self.assertRaises(ValueError):
                probability(p)
        with self.assertRaises(ValueError):
            kl((1,), (.5, .5))
        with self.assertRaises(ValueError):
            channel((1,), ((.5, .5), (.5, .5)))

    def test_KL_support_conventions(self):
        self.assertEqual(kl((0, 1), (0, 1)), 0)
        self.assertEqual(kl((1, 0), (0, 1)), math.inf)
        self.assertNear(kl((1, 0), (.5, .5)), math.log(2))

    def test_KL_nonnegativity_and_unique_zero_on_grid(self):
        for q, p in product(binary_grid(), repeat=2):
            score = kl(q, p)
            self.assertGreaterEqual(score, -1e-12)
            self.assertEqual(abs(score) < 1e-12, q == p)

    def test_imprecise_indicator_has_multiple_zeros(self):
        possibilities = {(1., 0.), (0., 1.)}
        indicator = lambda q: 0 if q in possibilities else math.inf
        self.assertEqual([indicator(q) for q in possibilities], [0, 0])
        for p in binary_grid():
            self.assertTrue(any(kl(q, p) > 0 for q in possibilities))

    def test_normalized_bayesian_beliefs_not_pointwise_ordered(self):
        for p, r in product(binary_grid(), repeat=2):
            if p != r:
                self.assertLess(kl(p, p), kl(p, r))
                self.assertLess(kl(r, r), kl(r, p))

    def test_combination_not_sum_of_individual_minima(self):
        p, r, middle = (.9, .1), (.1, .9), (.5, .5)
        self.assertNear(kl(p, p) + kl(r, r), 0)
        self.assertGreater(kl(middle, p) + kl(middle, r), 1)
        for q in binary_grid():
            self.assertNear(kl(q, p) + kl(q, r), 2 * kl(q, middle) - 2 * math.log(.6))

    def test_weighted_geometric_pool(self):
        p, r = (.75, .25), (.125, .875)
        for a, b in ((1, 1), (1, 2), (.5, 3)):
            s = a + b
            numer = [pi ** (a / s) * ri ** (b / s) for pi, ri in zip(p, r)]
            z = math.fsum(numer)
            m = [v / z for v in numer]
            for q in binary_grid():
                self.assertNear(a * kl(q, p) + b * kl(q, r), s * kl(q, m) - s * math.log(z))

    def test_joint_and_conditional_KL_agree(self):
        rows = ((.25, .75), (.75, .25))
        for joint in ((.1, .2, .3, .4), (0, 0, .75, .25), (1, 0, 0, 0)):
            marginal = (sum(joint[:2]), sum(joint[2:]))
            ref = tuple(marginal[i] * rows[i][j] for i, j in product(range(2), repeat=2))
            weighted = math.fsum(marginal[i] * kl(tuple(joint[2*i+j] / marginal[i] for j in range(2)), rows[i])
                                 for i in range(2) if marginal[i])
            self.assertNear(kl(joint, ref), weighted)

    def test_unvisited_conditional_row_not_certified(self):
        q = (1, 0, 0, 0)
        for unseen in ((1, 0), (0, 1), (.3, .7)):
            reference = (1, 0, 0 * unseen[0], 0 * unseen[1])
            self.assertEqual(kl(q, reference), 0)
        self.assertEqual(kl((1, 0), (0, 1)), math.inf)

    def test_conditioning_identity_and_offset(self):
        p = (.25, .25, .5)
        offset, posterior = condition(p, (True, True, False))
        self.assertNear(offset, math.log(2))
        for t in (0, .125, .5, 1):
            q = (t, 1-t, 0)
            self.assertNear(kl(q, p), kl(q, posterior) + offset)
        self.assertEqual(kl((0, 0, 1), posterior), math.inf)

    def test_impossible_event_has_no_posterior(self):
        with self.assertRaises(ValueError):
            condition((0, 1), (True, False))
        self.assertEqual(kl((1, 0), (0, 1)), math.inf)

    def test_same_posterior_different_evidence_cost(self):
        a, pa = condition((.5, .5), (True, False))
        b, pb = condition((.25, .75), (True, False))
        self.assertEqual(pa, pb)
        self.assertNear(b - a, math.log(2))

    def test_likelihood_update_value_identity(self):
        p, likelihood = (.4, .6), (.25, .75)
        z = expectation(p, likelihood)
        posterior = tuple(pi * li / z for pi, li in zip(p, likelihood))
        cost = tuple(-math.log(li) for li in likelihood)
        for q in binary_grid():
            self.assertNear(kl(q, p) + expectation(q, cost), kl(q, posterior) - math.log(z))

    def test_cross_entropy_fixed_first_argument(self):
        for d, p in product(binary_grid(), repeat=2):
            self.assertNear(cross_entropy(d, p), cross_entropy(d, d) + kl(d, p))

    def test_cross_entropy_variable_first_argument_not_KL(self):
        p = (.5, .5)
        self.assertNear(cross_entropy((1, 0), p), cross_entropy(p, p))
        self.assertGreater(kl((1, 0), p), kl(p, p))

    def test_sampled_log_ratio_can_be_negative(self):
        p, q = (.5, .5), (.75, .25)
        samples = tuple(math.log(qi / pi) for qi, pi in zip(q, p))
        self.assertLess(samples[1], 0)
        self.assertNear(expectation(q, samples), kl(q, p))

    def test_chain_rule_uses_first_argument_prefix_law(self):
        initials = ((.25, .75), (.5, .5))
        kernels = (((.25, .75), (.75, .25)), ((.5, .5), (.5, .5)))
        for qx, px, qk, pk in product(initials, initials, kernels, kernels):
            qjoint = tuple(qx[i]*qk[i][j] for i, j in product(range(2), repeat=2))
            pjoint = tuple(px[i]*pk[i][j] for i, j in product(range(2), repeat=2))
            rhs = kl(qx, px) + math.fsum(qx[i]*kl(qk[i], pk[i]) for i in range(2))
            self.assertNear(kl(qjoint, pjoint), rhs)
        qx, px = (.25, .75), (.75, .25)
        qk, pk = ((1, 0), (.5, .5)), ((.5, .5), (.5, .5))
        self.assertNotEqual(sum(qx[i]*kl(qk[i], pk[i]) for i in range(2)),
                            sum(px[i]*kl(qk[i], pk[i]) for i in range(2)))

    def test_KL_triangle_rule_is_false(self):
        p, q, r = (1, 0), (.5, .5), (.25, .75)
        self.assertGreater(kl(p, r), kl(p, q) + kl(q, r))
        self.assertNear(kl(p, r), math.log(4))

    def test_shared_channel_contracts_KL(self):
        grid = binary_grid()
        for q, p, row1, row2 in product(grid, repeat=4):
            before = kl(q, p)
            after = kl(channel(q, (row1, row2)), channel(p, (row1, row2)))
            self.assertLessEqual(after, before + 1e-10)

    def test_different_channels_do_not_give_contraction(self):
        p = (.5, .5)
        qout = channel(p, ((1, 0), (1, 0)))
        pout = channel(p, ((0, 1), (0, 1)))
        self.assertEqual(kl(p, p), 0)
        self.assertEqual(kl(qout, pout), math.inf)

    def test_soft_value_and_optimizer(self):
        p, f = (.5, .5), (0, math.log(3))
        lo, qlo = soft_value(p, f)
        hi, qhi = soft_value(p, f, robust=True)
        self.assertNear(lo, math.log(1.5))
        self.assertNear(hi, math.log(2))
        self.assertNear(qlo[0], .75)
        self.assertNear(qhi[0], .25)

    def test_soft_value_identity_all_q(self):
        for p, f, beta in product(((.5, .5), (.25, .75)),
                                  product((-2, 0, 3), repeat=2), (.5, 1, 2)):
            value, optimum = soft_value(p, f, beta)
            for q in binary_grid():
                self.assertNear(beta * kl(q, p) + expectation(q, f),
                                beta * kl(q, optimum) + value)

    def test_soft_value_shift_and_nonexpansiveness(self):
        p = (.25, .75)
        vectors = list(product((-2, 0, 3), repeat=2))
        for robust in (False, True):
            for f, g in product(vectors, repeat=2):
                a, _ = soft_value(p, f, robust=robust)
                b, _ = soft_value(p, g, robust=robust)
                self.assertLessEqual(abs(a-b), max(abs(x-y) for x,y in zip(f,g)) + 1e-10)
                shifted, _ = soft_value(p, [x+1000 for x in f], robust=robust)
                self.assertNear(shifted, a+1000)
                if all(x <= y for x,y in zip(f,g)):
                    self.assertLessEqual(a, b+1e-10)

    def test_soft_value_restricted_support_and_invalid_inputs(self):
        value, optimum = soft_value((1, 0), (2, -100))
        self.assertNear(value, 2)
        self.assertEqual(optimum, (1, 0))
        for beta in (0, -1, math.inf):
            with self.assertRaises(ValueError):
                soft_value((1,), (1,), beta)
        with self.assertRaises(ValueError):
            soft_value((1,), (math.inf,))

    def test_proper_finite_penalty_transformer_need_not_normalize_zero(self):
        laws, penalties = ((1, 0), (0, 1), (.5, .5)), (2., 3., math.inf)
        transform = lambda f: min(b + expectation(q, f) for b, q in zip(penalties, laws))
        self.assertEqual(transform((0, 0)), 2)
        for f in product((-2, 0, 3), repeat=2):
            self.assertNear(transform([x+7 for x in f]), transform(f)+7)
            self.assertGreaterEqual(transform(f), min(f))

    def test_unbounded_exponential_moment_prefix_identity(self):
        # Not a normalized truncation of the reference: exact original masses 2^-n.
        for n in (1, 2, 4, 16, 64):
            mean_reward = math.fsum(k * math.log(2) / n for k in range(1, n+1))
            divergence = math.fsum((math.log(1/n) + k*math.log(2))/n for k in range(1, n+1))
            self.assertNear(mean_reward-divergence, math.log(n))

    def test_lsc_residual_counterexample_sequence(self):
        b = lambda t: 0 if t == 0 else 1
        residual = lambda t: max(1-b(t), 0)
        self.assertEqual(residual(0), 1)
        self.assertTrue(all(residual(1/n) == 0 for n in range(1, 100)))

    def test_aggregation_loses_revision_labels(self):
        b = kl((1, 0), (.5, .5))
        a, c = (b, 0), (0, b)
        self.assertEqual(sum(a), sum(c))
        self.assertNotEqual(a[1], c[1])
        self.assertEqual(sum((b, b)), 2*b)

    def test_belief_cost_reallocation_preserves_comparisons(self):
        p, f, h, beta = (.25, .75), (-2, 3), (1, -1), 2
        weights = tuple(pi * math.exp(hi/beta) for pi, hi in zip(p, h))
        z = sum(weights)
        newp = tuple(v/z for v in weights)
        newf = tuple(fi+hi for fi,hi in zip(f,h))
        for q in binary_grid():
            before = beta*kl(q,p)+expectation(q,f)
            after = beta*kl(q,newp)+expectation(q,newf)
            self.assertNear(after-before, beta*math.log(z))

    def test_marginal_beliefs_do_not_impose_independence(self):
        px, py = (.25, .75), (.5, .5)
        for q in ((.5, 0, 0, .5), (.25, .25, .25, .25), (.1, .2, .3, .4)):
            qx, qy = (q[0]+q[1], q[2]+q[3]), (q[0]+q[2], q[1]+q[3])
            product_q = tuple(qx[i]*qy[j] for i,j in product(range(2),repeat=2))
            product_p = tuple(px[i]*py[j] for i,j in product(range(2),repeat=2))
            self.assertNear(kl(q, product_p), kl(qx,px)+kl(qy,py)+kl(q,product_q))
        self.assertNear(kl((.5,0,0,.5),(.25,.25,.25,.25)), math.log(2))

    def test_independence_penalty_is_not_convex(self):
        def mutual(q):
            qx,qy = (q[0]+q[1],q[2]+q[3]),(q[0]+q[2],q[1]+q[3])
            return kl(q, tuple(qx[i]*qy[j] for i,j in product(range(2),repeat=2)))
        self.assertEqual(mutual((1,0,0,0)),0)
        self.assertEqual(mutual((0,0,0,1)),0)
        self.assertGreater(mutual((.5,0,0,.5)),0)

    def test_artificial_observation_encodes_fixed_expected_cost(self):
        p,cost = (.5,.5), (0.,math.log(3))
        rows = tuple((math.exp(-c), 1-math.exp(-c)) for c in cost)
        realized = (p[0],0,p[1],0)
        reference = tuple(p[i]*rows[i][j] for i,j in product(range(2),repeat=2))
        fixed = kl(realized,reference)
        self.assertNear(fixed,expectation(p,cost))
        tilted,_ = soft_value(p,cost)
        self.assertGreater(fixed,tilted)

    def test_source_ids_versions_and_cardinality(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root/'literature/F03_sources.json').read_text())
        ids = [s['id'] for s in data['sources']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({f'S{i:02}' for i in range(1,19)} <= set(ids))
        self.assertEqual(data['core_count'], 8)
        self.assertEqual(data['core_count']+data['supplementary_count'], len(ids))
        s18 = next(s for s in data['sources'] if s['id'] == 'S18')
        self.assertIn('July 29, 2024', s18['inspected_version'])
        self.assertTrue(all(not s['whole_work_verified'] for s in data['sources'] if s['id'] >= 'S14'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    run = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F03BeliefKLTests))
    if run.wasSuccessful() and args.json:
        report = results()
        report['tests_passed'] = run.testsRun
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False)+'\n')
    raise SystemExit(0 if run.wasSuccessful() else 1)
