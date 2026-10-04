"""Exact independent path challenges to F13's optional analytic statements."""
from fractions import Fraction as Q
from itertools import permutations, product
import unittest

from v2.verification import case_reference as R, case_retention as T
from v2.verification.program_reference import tail


class RetentionCases(unittest.TestCase):
    def test_full_order_ranks_with_unequal_and_zero_costs(self):
        for k in range(1, 5):
            for positive in range(k+1):
                costs = tuple(Q(i+1) if i < positive else Q(0) for i in range(k))
                zeros = k-positive
                for penalty in (Q(0), Q(4)):
                    with self.subTest(k=k, positive=positive, penalty=penalty):
                        rows = T.path_rows(costs, penalty)
                        if positive == 0:
                            expected = int(penalty > 0)
                            differences = 0
                        else:
                            differences = 2**k-2**zeros-positive
                            expected = differences+int(penalty > 0 or positive >= 2)
                        self.assertEqual(T.rank(rows), expected)
                        self.assertEqual(T.rank([tuple(x-y for x, y in zip(row, rows[0]))
                                                 for row in rows[1:]]), differences)
                        distribution_rank = (int(penalty > 0) if positive == 0
                                             else 2**k-2**zeros-1+int(penalty > 0))
                        self.assertEqual(T.rank(T.path_rows(costs, penalty, distributions=True)),
                                         distribution_rank)

    def test_all_ordered_subsets_restore_moments(self):
        for k in range(1, 5):
            costs = tuple(Q(i+1, i+2) for i in range(k))
            for penalty in (Q(0), Q(3, 2)):
                self.assertEqual(T.rank(T.path_rows(costs, penalty, subsets=True)),
                                 2**k-2+int(penalty > 0))

    def test_positive_price_summary_on_every_point_mass(self):
        # Linearity makes testing every vertex stronger than selected random laws.
        for k in range(2, 5):
            for costs in ((Q(1),)*k, tuple(Q(i+1, i+2) for i in range(k))):
                for world in product((0, 1), repeat=k):
                    for penalty in (Q(0), Q(4)):
                        population = {world: Q(1)}
                        summary = T.retain(population, costs, penalty)
                        self.assertEqual(len(summary[1])+1, 2**k-k)
                        for order in permutations(range(k)):
                            self.assertEqual(T.recover(summary, order, costs),
                                             R.execute(world, order, costs, penalty)[0])

    def test_complete_mean_profile_collision_and_risk(self):
        laws = (T.identified_law(Q(15, 128)), T.identified_law(Q(17, 128)))
        for law, wanted in zip(laws, (Q(27, 4), Q(7))):
            self.assertEqual(sum(law.values()), 1)
            for order in permutations(range(3)):
                self.assertEqual(R.expected(law, order, (Q(1),)*3, Q(4))[0], Q(9, 4))
                losses = [R.execute(bits, order, (Q(1),)*3, Q(4))[0] for bits in law]
                self.assertEqual(tail(losses, tuple(law.values()), Q(7, 8)), wanted)
        self.assertLess(laws[0][(1, 1, 1)], Q(1, 8))
        self.assertGreater(laws[1][(1, 1, 1)], Q(1, 8))

    def test_sharp_fiber_endpoints_and_all_piecewise_tail_branches(self):
        low, high = Q(1, 9), Q(7, 52)
        self.assertEqual((high-low)/2, Q(11, 936))
        for t in (low, Q(15, 128), Q(1, 8), Q(17, 128), high):
            law = T.identified_law(t)
            self.assertEqual(sum(law.values()), 1)
            losses = [R.execute(bits, (0, 1, 2), (Q(1),)*3, Q(4))[0] for bits in law]
            for alpha in (Q(0), Q(1, 2), Q(2, 3), Q(25, 36), Q(3, 4), Q(7, 8), Q(99, 100)):
                expected = ((Q(9, 4)-alpha)/(1-alpha) if alpha <= Q(1, 2)
                            else min(2+Q(3, 4)/(1-alpha), 3+4*t/(1-alpha), Q(7)))
                self.assertEqual(tail(losses, tuple(law.values()), alpha), expected)
            for change in (Q(-4), Q(-1), Q(0), Q(1), Q(1000)):
                self.assertEqual(R.expected(law, (0, 1, 2), (Q(1),)*3, 4+change)[0],
                                 Q(9, 4)+change*t)
        for invalid in (low-Q(1, 10000), high+Q(1, 10000)):
            with self.assertRaises(ValueError):
                T.identified_law(invalid)

    def test_cheap_fallback_equivalence_and_boundary_failure(self):
        for weights in product(range(5), repeat=3):
            if not sum(weights):
                continue
            masses = tuple(Q(w, sum(weights)) for w in weights)
            losses = (Q(5), Q(10), Q(35))
            mean = sum(p*x for p, x in zip(masses, losses))
            for alpha, fallback in product((Q(0), Q(1, 16), Q(1, 2), Q(9, 10)),
                                           (Q(5), Q(7), Q(9), Q(999, 100))):
                self.assertEqual(tail(losses, masses, alpha) <= fallback,
                                 mean <= alpha*5+(1-alpha)*fallback)
        # Once the fallback exceeds the next possible cost, the shortcut can fail.
        losses, masses = (Q(5), Q(10)), (Q(1, 2), Q(1, 2))
        self.assertLessEqual(tail(losses, masses, Q(3, 4)), 11)
        self.assertGreater(Q(15, 2), Q(3, 4)*5+Q(1, 4)*11)

    def test_independent_ratio_order_and_stopping_match_exhaustive_policy_search(self):
        costs = (Q(1), Q(3, 2), Q(2))
        for failures in product((Q(0), Q(1, 3), Q(2, 3), Q(1)), repeat=3):
            law = T.independent_law(failures)
            for penalty in (Q(0), Q(2), Q(7)):
                order = T.independent_order(failures, costs, penalty)
                self.assertEqual(R.expected(law, order, costs, penalty)[0],
                                 min(R.expected(law, p, costs, penalty)[0] for p in R.all_orders(3)))
                full = T.independent_order(failures, costs)
                self.assertEqual(R.expected(law, full, costs, penalty)[0],
                                 min(R.expected(law, p, costs, penalty)[0]
                                     for p in permutations(range(3))))

    def test_correlated_marginal_greedy_counterexample(self):
        law = {(0, 0, 1): Q(3, 10), (1, 0, 1): Q(1, 5),
               (0, 1, 0): Q(3, 10), (1, 1, 0): Q(1, 5)}
        self.assertEqual(R.expected(law, (0, 1, 2), (Q(1),)*3, Q(4)), (Q(8, 5), 0))
        self.assertEqual(R.expected(law, (1, 2, 0), (Q(1),)*3, Q(4)), (Q(3, 2), 0))


class RefinedBounds(unittest.TestCase):
    def test_physical_noise_bound_against_cut_box_vertices(self):
        # Maximize a two-piece affine objective directly on a five-dimensional
        # box, including all intersections of its edges with q.x+J=0.
        s = (Q(1, 6), Q(2, 3), Q(1, 6), Q(0))
        rules = ((Q(-1, 126), Q(64, 135), Q(989, 4410), Q(2048, 6615)),
                 (Q(253, 18480), Q(2141, 4200), Q(4141, 18480), Q(486, 1925)))
        for rule_index, q in enumerate(rules):
            for residual, noise in product((Q(0), Q(1, 100), Q(1)),
                                            (Q(0), Q(1, 2), Q(20))):
                amplitude = residual+noise
                radii = (amplitude,)*4+(residual,)
                normal = q+(Q(1),)
                points = set(product(*[(-r, r) for r in radii]))
                for free in range(5):
                    if normal[free] == 0:
                        continue
                    for endpoint in tuple(points):
                        point = list(endpoint)
                        point[free] = -sum(normal[j]*point[j] for j in range(5) if j != free)/normal[free]
                        if abs(point[free]) <= radii[free]:
                            points.add(tuple(point))
                actual = max(sum(s[j]*p[j] for j in range(4))+p[4]
                             -abs(sum(normal[j]*p[j] for j in range(5))) for p in points)
                expected = (amplitude*Q(28633, 46200) if rule_index == 1 else min(
                    amplitude*Q(694, 945), amplitude*Q(6382, 8901)+residual*Q(254, 989)))
                self.assertEqual(actual, expected)

    def test_one_sided_cost_rounding_regret_for_mean_and_tail(self):
        true_costs, rounded = (Q(1, 10), Q(1, 5), Q(2)), (Q(0), Q(0), Q(2))
        laws = (T.independent_law((Q(1, 3), Q(2, 3), Q(1, 4))),
                {bits: Q(i+1, 36) for i, bits in enumerate(product((0, 1), repeat=3))})
        for law in laws:
            for alpha in (Q(0), Q(1, 2), Q(9, 10)):
                def value(order, costs):
                    losses = [R.execute(bits, order, costs, Q(4))[0] for bits in law]
                    return tail(losses, tuple(law.values()), alpha)
                orders = tuple(permutations(range(3)))
                free_first = ((0, 1, 2), (1, 0, 2))
                self.assertEqual(min(value(p, rounded) for p in free_first),
                                 min(value(p, rounded) for p in orders))
                chosen = min(free_first, key=lambda p: value(p, rounded))
                self.assertLessEqual(value(chosen, true_costs)-min(value(p, true_costs) for p in orders),
                                     Q(3, 10))
                for p in orders:
                    self.assertTrue(0 <= value(p, true_costs)-value(p, rounded) <= Q(3, 10))

    def test_sharp_full_order_price_edit_bound(self):
        old = (Q(2), Q(3), Q(4))
        for change, penalty_change in product(((Q(1), Q(-2), Q(3)),
                                               (Q(-1), Q(0), Q(-2)),
                                               (Q(1), Q(2), Q(3))), (Q(-2), Q(0), Q(5))):
            new = tuple(x+d for x, d in zip(old, change))
            positive = sum(max(d, Q(0)) for d in change)
            negative = -sum(min(d, Q(0)) for d in change)
            actual = max(abs(R.execute(bits, order, new, 4+penalty_change)[0]
                             -R.execute(bits, order, old, Q(4))[0])
                         for bits, order in product(product((0, 1), repeat=3), permutations(range(3))))
            self.assertEqual(actual, max(positive, negative, abs(positive-negative+penalty_change)))

    def test_combined_drift_and_risk_frontier_on_attaining_laws(self):
        even = {bits: Q(1, 4) if sum(bits) % 2 == 0 else Q(0)
                for bits in product((0, 1), repeat=3)}
        odd = {bits: Q(1, 4)-even[bits] for bits in even}
        for q, rho in product((Q(0), Q(1, 160), Q(1, 80)),
                              (Q(0), Q(1, 240), Q(1, 120), Q(1, 100))):
            law = {bits: (1-4*q)*even[bits]+4*q*odd[bits] for bits in even}
            law[(0, 0, 0)] -= rho
            law[(1, 1, 1)] += rho
            for order in permutations(range(3)):
                losses = [R.execute(bits, order, (Q(5),)*3, Q(20))[0] for bits in law]
                self.assertEqual(sum(x*p for x, p in zip(losses, law.values())), Q(35, 4)+20*q+30*rho)
                for alpha in (Q(0), Q(1, 32), Q(1, 16), Q(1, 2)):
                    self.assertEqual(tail(losses, tuple(law.values()), alpha) <= 9,
                                     20*q+30*rho+4*alpha <= Q(1, 4))

    def test_exact_zero_failure_sample_counts(self):
        for cap, count in ((Q(1, 80), 239), (Q(1, 160), 478)):
            self.assertGreater((1-cap)**(count-1), Q(1, 20))
            self.assertLessEqual((1-cap)**count, Q(1, 20))
        self.assertEqual(478*15/Q(1, 8), 57360)


class ScientificAcquisition(unittest.TestCase):
    def test_old_output_plus_one_new_sample_loses_unbounded_integral(self):
        for z in (Q(1, 12), Q(1, 8), Q(2, 5), Q(7, 8)):
            h = R.evaluate(R.polynomial(0, 0, 0, 1), z)
            for b in (Q(-10**6), Q(1), Q(10**6)):
                v = (Q(1, 2)-z)*b/h
                p = R.polynomial(-b/2, b, 0, v)
                self.assertEqual(R.evaluate(p, z), 0)
                self.assertEqual(R.integral(p), v)
                self.assertNotEqual(v, 0)

    def test_frozen_experiment_scalar_and_free_location_rank(self):
        rows = []
        for z in (Q(1, 12), Q(1, 8), Q(2, 5), Q(7, 8)):
            g = R.evaluate(R.polynomial(0, 0, 1, 0), z)
            h = R.evaluate(R.polynomial(0, 0, 0, 1), z)
            row = (1-1/h, Q(1, 2)-z/h, 1-g/h)
            self.assertEqual(T.rank((row, (Q(1), Q(1, 2), Q(1)))), 2)
            rows.append(row)
            for a, b, u, v in product((Q(-1), Q(2)), repeat=4):
                retained = sum(x*y for x, y in zip(row, (a, b, u)))
                p = R.polynomial(a, b, u, v)
                self.assertEqual(retained+R.evaluate(p, z)/h, R.integral(p))
        self.assertEqual(T.rank(rows), 3)

    def test_rational_node_near_optimal_and_sharp_posterior_radius(self):
        # Rational bracket for sqrt(13) independently certifies the stated ratio.
        root_lower, root_upper = Q(7211, 2000), Q(1803, 500)
        self.assertLess(root_lower**2, 13)
        self.assertGreater(root_upper**2, 13)
        h = R.evaluate(R.polynomial(0, 0, 0, 1), Q(1, 12))
        self.assertGreater(h, Q(199, 200)*(245+91*root_upper)/144)
        for width, delta in product((Q(0), Q(1, 10), Q(2)), (Q(0), Q(1, 5), Q(100))):
            radius = min(width, delta/h)
            self.assertEqual(min(width, delta/h)-max(-width, -delta/h), 2*radius)
            # The two endpoints have the same zero observation under allowed noise.
            for v in (-radius, radius):
                self.assertLessEqual(abs(-h*v), delta)
                self.assertLessEqual(abs(v), width)


if __name__ == '__main__':
    unittest.main()
