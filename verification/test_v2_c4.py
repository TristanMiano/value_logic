"""Direct-execution challenges to C4's price-family retention claims."""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import comb
import unittest

from v2.verification import case_reference as R, case_retention as T
from v2.verification import c4_price_revision as C
from v2.verification.program_reference import tail


def direct_ranks(profiles, known=()):
    groups = [T.path_rows(costs, penalty) for costs, penalty in profiles]
    rows = [row for group in groups for row in group]
    within = [tuple(x-y for x, y in zip(row, group[0]))
              for group in groups for row in group]
    cross = [tuple(x-y for x, y in zip(row, rows[0])) for row in rows]
    return {label: T.rank(list(known)+queries)-T.rank(known)
            for label, queries in (('numeric', rows), ('within', within), ('cross', cross))}


def known_moment_rows(k, through):
    worlds = tuple(product((0, 1), repeat=k))
    return [tuple(Q(all(world[i] for i in subset)) for world in worlds[1:])
            for size in range(1, through+1) for subset in combinations(range(k), size)]


def nullspace(rows):
    """Exact test-side elimination, with no formula for the expected kernel."""
    matrix = [list(map(Q, row)) for row in rows]
    width, pivot_columns = len(matrix[0]), []
    for col in range(width):
        pivot = len(pivot_columns)
        found = next((i for i in range(pivot, len(matrix)) if matrix[i][col]), None)
        if found is None:
            continue
        matrix[pivot], matrix[found] = matrix[found], matrix[pivot]
        divisor = matrix[pivot][col]
        matrix[pivot] = [x/divisor for x in matrix[pivot]]
        for i in range(len(matrix)):
            if i != pivot:
                factor = matrix[i][col]
                matrix[i] = [x-factor*y for x, y in zip(matrix[i], matrix[pivot])]
        pivot_columns.append(col)
    basis = []
    for free in set(range(width))-set(pivot_columns):
        vector = [Q(0)]*width
        vector[free] = Q(1)
        for i, col in enumerate(pivot_columns):
            vector[col] = -matrix[i][free]
        basis.append(tuple(vector))
    return basis


def indistinguishable_law_difference_vertices(penalty):
    # The two-dimensional section of the L1 ball has a vertex whenever a
    # nonconstant world mass changes sign. Construct it from direct executions.
    worlds = tuple(product((0, 1), repeat=3))
    rows = [[Q(1)]*8]+[[R.execute(w, order, (1, 1, 1), penalty)[0] for w in worlds]
                       for order in permutations(range(3))]
    first, second = nullspace(rows)
    vertices = set()
    for x, y in zip(first, second):
        vector = tuple(a*y-b*x for a, b in zip(first, second))
        norm = sum(map(abs, vector))
        if norm:
            vertices.add(tuple(2*v/norm for v in vector))
            vertices.add(tuple(-2*v/norm for v in vector))
    return worlds, rows, vertices


def families(k):
    c = tuple(Q(i+1, i+2) for i in range(k))
    d = c[:-1]+(c[-1]+Q(1, 7),)
    twice = tuple(2*x for x in c)
    return (
        ((c, 0),), ((c, 3),), ((c, 3), (c, 3)),
        ((c, 0), (twice, 0)), ((c, 3), (twice, 6)),
        ((c, 3), (twice, 3)), ((c, 0), (c, 3)),
        ((c, 0), (twice, 0), (c, 3)),
        ((c, 0), (d, 0)), ((c, 3), (d, 0)),
        ((c, 0), (d, 3)), ((c, 3), (d, 3)),
        ((c, 3), (d, 5)), ((c, 0), (d, 0), (twice, 3)),
    )


class PriceRevisionTests(unittest.TestCase):
    def test_three_consumer_ranks_across_42_price_families(self):
        for k in range(2, 5):
            for profiles in families(k):
                with self.subTest(k=k, profiles=profiles):
                    self.assertEqual(direct_ranks(profiles), C.predicted_ranks(profiles))

    def test_five_procedure_nonproportional_pair(self):
        profiles = (((Q(1),)*5, Q(2)), ((Q(1),)*4+(Q(1001, 1000),), Q(2)))
        self.assertEqual(direct_ranks(profiles), {'numeric': 31, 'within': 30, 'cross': 30})

    def test_full_law_repair_on_all_vertices(self):
        for k in range(2, 5):
            worlds = tuple(product((0, 1), repeat=k))
            for costs in ((Q(1),)*k, tuple(Q(i+1, i+2) for i in range(k))):
                for change in (Q(-1, 8), Q(1, 1000)):
                    new_costs = costs[:-1]+(costs[-1]+change,)
                    for world in worlds:
                        with self.subTest(k=k, costs=costs, change=change, world=world):
                            summary = T.retain({world: Q(1)}, costs, Q(3))
                            means = [R.execute(world, order, new_costs, Q(3))[0]
                                     for order in C.chain_probe_orders(k)]
                            moments = C.repair_from_chain(summary, costs, Q(3), change, means)
                            recovered = C.invert_moments(moments, k)
                            self.assertEqual(recovered, {w: Q(w == world) for w in worlds})

    def test_zero_penalty_repairs_only_proper_moments(self):
        for k in range(2, 5):
            costs = tuple(Q(i+1, i+2) for i in range(k))
            change = Q(1, 17)
            new_costs = costs[:-1]+(costs[-1]+change,)
            for world in product((0, 1), repeat=k):
                summary = T.retain({world: Q(1)}, costs, Q(0))
                means = [R.execute(world, order, new_costs, Q(0))[0]
                         for order in C.chain_probe_orders(k, False)]
                moments = C.repair_from_chain(summary, costs, Q(0), change, means)
                self.assertNotIn(tuple(range(k)), moments)
                for subset, value in moments.items():
                    self.assertEqual(value, Q(all(world[i] for i in subset)))
                self.assertEqual(len(means), k-2)

    def test_new_queries_add_exactly_the_missing_rank(self):
        for k in range(2, 5):
            costs, change = tuple(Q(i+1) for i in range(k)), Q(1, 23)
            new_costs = costs[:-1]+(costs[-1]+change,)
            for penalty in (Q(0), Q(4)):
                rows = T.path_rows(costs, penalty)
                all_new_rows = dict(zip(permutations(range(k)), T.path_rows(new_costs, penalty)))
                initial = T.rank(rows)
                for i, order in enumerate(C.chain_probe_orders(k, penalty > 0), 1):
                    rows.append(all_new_rows[order])
                    self.assertEqual(T.rank(rows), initial+i)
                self.assertEqual(T.rank(rows), 2**k-2+int(penalty > 0))

    def test_explicit_same_old_profile_different_new_threshold(self):
        worlds = tuple(product((0, 1), repeat=3))
        plus = dict(zip(worlds, map(lambda x: Q(x, 560), (105, 35, 35, 101, 35, 97, 93, 59))))
        minus = dict(zip(worlds, map(lambda x: Q(x, 560), (35, 105, 105, 39, 105, 43, 47, 81))))
        costs = (Q(1), Q(2), Q(3))
        self.assertEqual(sum(plus.values()), 1)
        self.assertEqual(sum(minus.values()), 1)
        self.assertEqual(T.retain(plus, costs, 4), T.retain(minus, costs, 4))
        for order in permutations(range(3)):
            self.assertEqual(R.expected(plus, order, costs, 4)[0],
                             R.expected(minus, order, costs, 4)[0])
        for change in (Q(1), Q(1, 1000)):
            new_costs = costs[:-1]+(costs[-1]+change,)
            threshold = Q(13, 4)+change/4
            self.assertGreater(R.expected(plus, (0, 1, 2), new_costs, 4)[0], threshold)
            self.assertLess(R.expected(minus, (0, 1, 2), new_costs, 4)[0], threshold)

    def test_pointwise_order_differences_do_not_fix_robust_absolute_choice(self):
        worlds = tuple(product((0, 1), repeat=2))
        p = dict(zip(worlds, (Q(1, 2), Q(1, 10), Q(0), Q(2, 5))))
        q = dict(zip(worlds, (Q(1, 10), Q(1, 10), Q(4, 5), Q(0))))
        costs, orders = (Q(1), Q(1)), ((0, 1), (1, 0))
        values = {}
        for penalty in (Q(0), Q(1)):
            table = [[R.expected(law, order, costs, penalty)[0] for order in orders]
                     for law in (p, q)]
            values[penalty] = tuple(max(table[row][column] for row in range(2))
                                    for column in range(2))
            self.assertEqual(tuple(row[0]-row[1] for row in table), (Q(-1, 10), Q(7, 10)))
        self.assertEqual(values[0], (Q(9, 5), Q(3, 2)))
        self.assertEqual(values[1], (Q(9, 5), Q(19, 10)))

    def test_small_edit_regret_for_means_tails_and_robust_sources(self):
        worlds = tuple(product((0, 1), repeat=3))
        laws = [dict(zip(worlds, (Q(1, 8),)*8)),
                dict(zip(worlds, (Q(0), Q(1, 4), Q(0), Q(1, 4), Q(1, 4), Q(0), Q(1, 4), Q(0))))]
        costs, penalty = (Q(1), Q(3, 2), Q(2)), Q(5)
        orders = tuple(permutations(range(3)))
        for change, alpha, robust in product((Q(-1, 5), Q(1, 7)),
                                             (Q(0), Q(1, 2), Q(9, 10)), (False, True)):
            new_costs = costs[:-1]+(costs[-1]+change,)
            source = laws if robust else laws[:1]
            def value(order, prices):
                return max(tail(tuple(R.execute(w, order, prices, penalty)[0] for w in worlds),
                                tuple(law[w] for w in worlds), alpha) for law in source)
            old = min(orders, key=lambda order: value(order, costs))
            regret = value(old, new_costs)-min(value(order, new_costs) for order in orders)
            self.assertGreaterEqual(regret, 0)
            self.assertLessEqual(regret, abs(change))

    def test_regret_bound_is_sharp_without_old_ties(self):
        # Both procedures succeed; price edit switches the unique optimal first action.
        for zeta in (Q(1, 10), Q(1, 1000)):
            costs, change, world = (Q(1), Q(1)-zeta), Q(1, 2), (0, 0)
            self.assertLess(R.execute(world, (1, 0), costs, 0)[0],
                            R.execute(world, (0, 1), costs, 0)[0])
            new = costs[:-1]+(costs[-1]+change,)
            regret = R.execute(world, (1, 0), new, 0)[0]-R.execute(world, (0, 1), new, 0)[0]
            self.assertEqual(regret, change-zeta)

    def test_degenerate_inputs_are_outside_the_claim(self):
        for profiles in ((), (((1,), 0),), (((0, 1), 0),), (((1, 1), -1),),
                         (((1, 1), 0), ((1, 1, 1), 0))):
            with self.assertRaises(ValueError):
                C.predicted_ranks(profiles)
        summary = T.retain({(0, 0): Q(1)}, (Q(1), Q(1)), Q(1))
        for change in (0, -1):
            with self.assertRaises(ValueError):
                C.repair_from_chain(summary, (1, 1), 1, change, (1,))
        with self.assertRaises(ValueError):
            C.repair_from_chain(summary, (1, 1), 1, 1, ())

    def test_known_lower_moments_single_and_two_profile_ranks(self):
        # Direct world-coordinate rows, with moments treated as prior information.
        # The uniform law is interior to every tested fixed-moment fiber.
        for k in range(2, 5):
            c = tuple(Q(i+1, i+2) for i in range(k))
            d = c[:-1]+(c[-1]+Q(1, 11),)
            for s in range(k):
                known = known_moment_rows(k, s)
                dimension = 2**k-1-len(known)
                for penalty in (0, 3):
                    numeric = (dimension-k+s+1 if s <= k-2 else int(penalty > 0))
                    self.assertEqual(direct_ranks(((c, penalty),), known),
                                     {'numeric': numeric, 'within': dimension-k+s,
                                      'cross': dimension-k+s})
                for m, n in ((0, 0), (0, 3), (3, 3), (3, 5)):
                    self.assertEqual(direct_ranks(((c, m), (d, n)), known),
                                     {'numeric': dimension-1+int(bool(m or n)),
                                      'within': dimension-1,
                                      'cross': dimension-1+int(m != n)})

    def test_known_lower_moments_reduce_minimal_repair_queries(self):
        for k in range(2, 5):
            costs = tuple(Q(i+1) for i in range(k))
            new_costs = costs[:-1]+(costs[-1]+Q(1, 19),)
            for s, penalty in product(range(k), (Q(0), Q(4))):
                known = known_moment_rows(k, s)
                rows = known+T.path_rows(costs, penalty)
                before = T.rank(rows)
                new_rows = dict(zip(permutations(range(k)), T.path_rows(new_costs, penalty)))
                all_probes = C.chain_probe_orders(k, penalty > 0)
                probes = all_probes[s:]
                self.assertEqual(len(probes), max(k-s-1-int(not penalty), 0))
                for i, order in enumerate(probes, 1):
                    rows.append(new_rows[order])
                    self.assertEqual(T.rank(rows), before+i)
                self.assertEqual(T.rank(rows), 2**k-2+int(penalty > 0))

    def test_boundary_face_invalidates_full_support_dimension(self):
        # m_0=0 forces every moment containing procedure 0 to vanish as well.
        # With the other two singleton moments fixed, only m_{1,2} varies.
        k, costs = 3, (Q(1), Q(2), Q(3))
        worlds = tuple(product((0, 1), repeat=k))
        known = known_moment_rows(k, 1)
        hidden_equalities = [tuple(Q(all(w[i] for i in subset)) for w in worlds[1:])
                             for subset in ((0, 1), (0, 2), (0, 1, 2))]
        self.assertEqual(direct_ranks(((costs, 4),), known)['numeric'], 3)
        self.assertEqual(direct_ranks(((costs, 4),), known+hidden_equalities)['numeric'], 1)

    def test_paired_trace_difference_recovers_reach_without_inverse_edit_noise(self):
        costs = (Q(1), Q(2), Q(3))
        worlds = tuple(product((0, 1), repeat=3))
        sample = (worlds[0], worlds[3], worlds[7], worlds[3], worlds[6])
        order = (0, 1, 2)
        for edit in (Q(-1, 7), Q(1, 10**9)):
            new_costs = costs[:-1]+(costs[-1]+edit,)
            normalized = sum((R.execute(w, order, new_costs, 4)[0]
                              - R.execute(w, order, costs, 4)[0] for w in sample), Q(0))/edit
            self.assertEqual(normalized/len(sample),
                             Q(sum(all(w[i] for i in (0, 1)) for w in sample), len(sample)))

    def test_sharp_approximation_diameters_from_direct_query_nullspace(self):
        penalties = (Q(1, 100), Q(1, 3), Q(1, 2), Q(99, 100), Q(1),
                     Q(101, 100), Q(4, 3), Q(3, 2), Q(4), Q(20), Q(100))
        for m in penalties:
            worlds, rows, vertices = indistinguishable_law_difference_vertices(m)
            self.assertTrue(vertices)
            for vector in vertices:
                self.assertEqual(sum(map(abs, vector)), 2)
                for row in rows:
                    self.assertEqual(sum(x*y for x, y in zip(row, vector)), 0)
            diameters = []
            for size in (1, 2):
                for subset in combinations(range(3), size):
                    actual = max(abs(sum(v for w, v in zip(worlds, vector)
                                         if all(w[i] for i in subset))) for vector in vertices)
                    if size == 1:
                        predicted = (2*m+1)/(3*(m+2))
                    elif m <= 1:
                        predicted = 1/(3*(m+2))
                    elif m <= Q(4, 3):
                        predicted = Q(1, 9)
                    else:
                        predicted = (3*m-1)/(3*(3*m+5))
                    with self.subTest(m=m, subset=subset):
                        self.assertEqual(actual, predicted)
                    diameters.append(actual)
            self.assertEqual(max(diameters), (2*m+1)/(3*(m+2)))

    def test_uniform_approximation_lower_bound_witness_and_action_caveat(self):
        worlds = tuple(product((0, 1), repeat=3))
        orders = tuple(permutations(range(3)))
        p = {w: Q(1, 3) if sum(w) == 2 else Q(0) for w in worlds}
        for m in (Q(1, 10), Q(1), Q(4, 3), Q(4), Q(20)):
            q = {w: (m+1)/(m+2) if sum(w) == 0 else
                 1/(m+2) if sum(w) == 3 else Q(0) for w in worlds}
            for law in (p, q):
                self.assertEqual(sum(law.values()), 1)
                for order in orders:
                    self.assertEqual(R.expected(law, order, (1, 1, 1), m)[0], 2)
            for edit in (Q(-1, 3), Q(1, 5)):
                costs = (1, 1, 1+edit)
                values = [R.expected(law, (0, 2, 1), costs, m)[0] for law in (p, q)]
                self.assertEqual(abs(values[0]-values[1])/2,
                                 abs(edit)*(2*m+1)/(6*(m+2)))
                if edit > 0:
                    for law in (p, q):
                        self.assertEqual(R.expected(law, (0, 1, 2), costs, m)[0],
                                         min(R.expected(law, order, costs, m)[0] for order in orders))

    def test_general_equal_price_diameter_reduces_to_sharp_three_procedure_formula(self):
        for m in (Q(1, 100), Q(1), Q(6, 5), Q(4, 3), Q(4), Q(100)):
            actual = C.equal_price_diameters(3, m)
            pair = (1/(3*(m+2)) if m <= 1 else Q(1, 9) if m <= Q(4, 3)
                    else (3*m-1)/(3*(3*m+5)))
            self.assertEqual(actual, (Q(0), (2*m+1)/(3*(m+2)), pair))
        self.assertEqual(C.equal_price_diameters(2, 0), (Q(0), Q(0)))
        self.assertEqual(C.equal_price_diameters(4, 0), (Q(0), Q(5, 18), Q(1, 12), Q(1, 4)))

    def test_equal_price_summary_has_minimal_rank_and_preserves_old_profiles(self):
        for k in range(2, 5):
            worlds = tuple(product((0, 1), repeat=k))
            orders = tuple(permutations(range(k)))
            for m in (Q(0), Q(1, 10), Q(4)):
                observations = []
                for w in worlds:
                    summary = C.retain_equal_price({w: Q(1)}, m)
                    self.assertEqual(len(summary[3])+1, 2**k-k)
                    observations.append((summary[2],)+tuple(summary[3].values()))
                    self.assertEqual(summary[2], sum(R.execute(w, order, (1,)*k, m)[0]
                                                      for order in orders)/len(orders))
                rows = [tuple(observations[j][i]-observations[0][i] for j in range(1, len(worlds)))
                        for i in range(len(observations[0]))]
                self.assertEqual(T.rank(rows), 2**k-k)
                self.assertEqual(T.rank(rows+T.path_rows((1,)*k, m)), 2**k-k)

    def test_conditional_reach_intervals_are_attained_by_compatible_laws(self):
        for k in range(2, 5):
            worlds = tuple(product((0, 1), repeat=k))
            orders = tuple(permutations(range(k)))
            total = len(worlds)*(len(worlds)+1)//2
            populations = [{w: Q(i+1, total) for i, w in enumerate(worlds)},
                           {w: Q(1, len(worlds)) for w in worlds},
                           {w: Q(1) if w == worlds[1] else Q(0) for w in worlds}]
            for p, m in product(populations, (Q(0), Q(1, 10), Q(4))):
                summary = C.retain_equal_price(p, m)
                old_means = tuple(R.expected(p, order, (1,)*k, m)[0] for order in orders)
                for size in range(k):
                    for subset in combinations(range(k), size):
                        low, high = C.equal_price_reach_interval(summary, subset)
                        actual = sum((mass for w, mass in p.items() if all(w[i] for i in subset)), Q(0))
                        self.assertLessEqual(low[0], actual)
                        self.assertLessEqual(actual, high[0])
                        self.assertLessEqual(high[0]-low[0], C.equal_price_diameters(k, m)[size])
                        for value, law in (low, high):
                            self.assertEqual(sum(law.values()), 1)
                            self.assertGreaterEqual(min(law.values()), 0)
                            self.assertEqual(sum(mass for w, mass in law.items()
                                                 if all(w[i] for i in subset)), value)
                            self.assertEqual(tuple(R.expected(law, order, (1,)*k, m)[0]
                                                   for order in orders), old_means)

    def test_independent_midpoints_need_not_describe_a_joint_law(self):
        worlds = tuple(product((0, 1), repeat=4))
        p = {w: Q(1, 2) if sum(w) == 0 else Q(1, 8) if sum(w) == 1 else Q(0) for w in worlds}
        summary = C.retain_equal_price(p, Q(1, 10))
        self.assertEqual(summary[2], Q(9, 8))
        midpoints = {(): Q(1)}
        expected = {1: Q(41, 496), 2: Q(1, 48), 3: Q(5, 248)}
        for size in range(1, 4):
            for subset in combinations(range(4), size):
                low, high = C.equal_price_reach_interval(summary, subset)
                midpoints[subset] = (low[0]+high[0])/2
                self.assertEqual(midpoints[subset], expected[size])
        midpoints[tuple(range(4))] = (Q(9, 8)-1-sum(expected.values()))/Q(1, 10)
        self.assertEqual(midpoints[tuple(range(4))], Q(5, 372))
        negative_mass = midpoints[(0, 1)]-midpoints[(0, 1, 2)]-midpoints[(0, 1, 3)]+midpoints[(0, 1, 2, 3)]
        self.assertEqual(negative_mass, Q(-3, 496))
        with self.assertRaises(ValueError):
            C.invert_moments(midpoints, 4)

    def test_coherent_center_attains_common_radius_in_midpoint_counterexample(self):
        k, penalty = 4, Q(1, 10)
        worlds = tuple(product((0, 1), repeat=k))
        original = {w: Q(1, 2) if sum(w) == 0 else Q(1, 8) if sum(w) == 1 else Q(0) for w in worlds}
        levels = (Q(11081, 13144), Q(0), Q(63, 424), Q(0), Q(55, 6572))
        candidate = {w: levels[sum(w)]/comb(k, sum(w)) for w in worlds}
        self.assertEqual(sum(candidate.values()), 1)
        self.assertGreaterEqual(min(candidate.values()), 0)
        for order in permutations(range(k)):
            self.assertEqual(R.expected(candidate, order, (1,)*k, penalty)[0], Q(9, 8))
        summary = C.retain_equal_price(original, penalty)
        largest_error, largest_half_width = Q(0), Q(0)
        for size in range(k):
            for subset in combinations(range(k), size):
                low, high = C.equal_price_reach_interval(summary, subset)
                value = sum(p for w, p in candidate.items() if all(w[i] for i in subset))
                largest_error = max(largest_error, high[0]-value, value-low[0])
                largest_half_width = max(largest_half_width, (high[0]-low[0])/2)
        self.assertEqual(largest_error, Q(21, 496))
        self.assertEqual(largest_error, largest_half_width)

    def test_singleton_chord_formula_matches_general_extremal_triples(self):
        for k in range(2, 13):
            for m in (Q(0), Q(1, 10), Q(1), Q(4), Q(20)):
                g, f = C.equal_price_geometry(k, m)
                actual = max(abs(f[1][j]-((g[l]-g[j])*f[1][i]+(g[j]-g[i])*f[1][l])/(g[l]-g[i]))
                             for i, j, l in combinations(range(k+1), 3))
                predicted = max(Q(j, k)-Q(j)/((k-j+1)*(k+m-1)) for j in range(1, k))
                self.assertEqual(actual, predicted)

    def test_stopped_prefix_repair_has_one_error_per_size_for_asymmetric_laws(self):
        # Deterministic identity audit, not an empirical validation of DKW.
        for k in range(2, 5):
            worlds = tuple(product((0, 1), repeat=k))
            population = {w: Q(i+1, len(worlds)*(len(worlds)+1)//2) for i, w in enumerate(worlds)}
            sample = (worlds[0], worlds[-1], worlds[-2], worlds[-1], worlds[len(worlds)//2])
            observed = []
            for w in sample:
                failures = 0
                for value in w[:k-1]:
                    if not value:
                        break
                    failures += 1
                observed.append(failures)
            estimates = tuple(Q(sum(j >= r for j in observed), len(observed)) for r in range(k))
            errors = tuple(estimates[r]-sum(p for w, p in population.items() if all(w[i] for i in range(r)))
                           for r in range(k))
            for penalty in (Q(0), Q(4)):
                summary = C.retain_equal_price(population, penalty)
                for size in range(k):
                    for subset in combinations(range(k), size):
                        estimated = C.repair_reach_from_prefix_estimates(summary, subset, estimates)
                        actual = sum(p for w, p in population.items() if all(w[i] for i in subset))
                        self.assertEqual(estimated-actual, errors[size])
                for order in permutations(range(k)):
                    old = R.expected(population, order, (1,)*k, penalty)[0]
                    for position in range(k):
                        reach = C.repair_reach_from_prefix_estimates(summary, order[:position], estimates)
                        for edit in (Q(-1, 3), Q(1, 1000)):
                            costs = tuple(1+edit if i == order[position] else 1 for i in range(k))
                            revised = R.expected(population, order, costs, penalty)[0]
                            self.assertEqual(old+edit*reach-revised, edit*errors[position])
                    edits = tuple(Q((-1)**i*(i+1), k+1) for i in range(k))
                    predicted = old+sum(edits[index]*C.repair_reach_from_prefix_estimates(
                        summary, order[:position], estimates) for position, index in enumerate(order))
                    revised = R.expected(population, order, tuple(1+x for x in edits), penalty)[0]
                    self.assertEqual(predicted-revised,
                                     sum(edits[index]*errors[position] for position, index in enumerate(order)))
                    self.assertLessEqual(abs(predicted-revised), sum(map(abs, edits))*max(map(abs, errors)))

    def test_capacity_representation_matches_direct_world_execution(self):
        for k in range(2, 5):
            costs = tuple(Q(i+1, i+2) for i in range(k))
            for world, order, penalty in product(product((0, 1), repeat=k),
                                                  permutations(range(k)), (Q(0), Q(4))):
                x = tuple(penalty+sum(costs[i] for i in order[j+1:]) for j in range(k))
                integral = sum((x[j]-(x[j+1] if j+1 < k else 0))
                               *int(any(not world[i] for i in order[:j+1])) for j in range(k))
                self.assertEqual(sum(costs)+penalty-integral, R.execute(world, order, costs, penalty)[0])


if __name__ == '__main__':
    unittest.main()
