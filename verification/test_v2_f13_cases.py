"""F13 development checks: independent execution, current guarantees and limits."""
from fractions import Fraction as Q
from itertools import product, combinations
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.verification import case_science as S, case_reference as R, case_cascade as C
from v2.verification.model import InputError
from v2.verification.program_reference import tail


class ScienceCases(unittest.TestCase):
    def test_shared_discrepancy_native_certificate_with_unbounded_common_error(self):
        for z, expected_norm in ((Q(1, 8), Q(694, 945)), (Q(1, 12), Q(28633, 46200))):
            source = S.Source(Q(1), Q(1), Q(1, 64))
            ctx, proof, new, old = S.prove_shared_error(source, Q(1, 32), Q(1, 100), Q(1, 200), z)
            expected = Q(1, 64)+Q(3, 200)*expected_norm-Q(1, 32)
            self.assertEqual(proof.steps[proof.root].budget, expected)
            A.receive(ctx, proof, A.request(ctx, None, new, old, expected))
            with self.assertRaises(A.AuditError):
                A.receive(ctx, proof, A.request(ctx, None, new, old, expected-Q(1, 10000)))
            points = []
            for common in (Q(-10**6), Q(0), Q(10**6)):
                point = dict(ctx.cases[0].witness)
                point['J'] = common
                points.append(point)
            self.assertGreater(A.audit_points(ctx, proof, points)['node_evaluations'], 0)

    def test_polynomial_execution_and_integration(self):
        rules = {**S.RULES, 'Q8': S.weights(Q(1, 8)), 'Q12': S.weights(Q(1, 12))}
        for a, b, u, v in product((Q(-1), Q(0), Q(2, 3)), repeat=4):
            poly = R.polynomial(a, b, u, v)
            exact = R.integral(poly)
            self.assertEqual(exact, a+b/2+u+v)
            expected = {'T': -u-v, 'S': u/4-v, 'B': -v, 'Q8': 0, 'Q12': 0}
            for name, rule in rules.items():
                values = {x: S.sample(x, a, b, u, v) for x, _ in rule}
                self.assertTrue(all(values[x] == R.evaluate(poly, x) for x in values))
                self.assertEqual(S.integrate_samples(rule, values)-exact, expected[name])

    def test_complete_five_node_observation_hides_unbounded_integral(self):
        nodes = tuple(Q(i, 4) for i in range(5))
        for v in (Q(-10**8), Q(-1, 99), Q(0), Q(13, 7), Q(10**8)):
            poly = R.polynomial(0, 0, 0, v)
            self.assertEqual(tuple(R.evaluate(poly, x) for x in nodes), (0,)*5)
            self.assertEqual(R.integral(poly), v)

    def test_fourth_node_noise_constants_and_attaining_signs(self):
        for z, norm in ((Q(1, 8), Q(64, 63)), (Q(1, 12), Q(1))):
            rule = S.weights(z)
            self.assertEqual(sum(w for _, w in rule), 1)
            self.assertEqual(sum(abs(w) for _, w in rule), norm)
            delta = Q(1, 100)
            noise = {x: delta if w >= 0 else -delta for x, w in rule}
            self.assertEqual(S.integrate_samples(rule, noise), delta*norm)

    def test_joint_native_bound_matches_independent_execution(self):
        for u, v, d, price in product((Q(0), Q(1, 8), Q(1)),
                                      (Q(0), Q(1, 16), Q(1)),
                                      (None, Q(0), Q(1, 64), Q(1, 8)),
                                      (Q(0), Q(1, 32))):
            source = S.Source(u, v, d)
            bound, point = R.scientific_bound(source, price)
            ctx, proof = S.prove(source, price)
            new, old = S.pair(price)
            A.receive(ctx, proof, A.request(ctx, None, new, old, bound))
            self.assertEqual(proof.steps[proof.root].budget, bound)
            with self.assertRaises(A.AuditError):
                A.receive(ctx, proof, A.request(ctx, None, new, old, bound-Q(1, 128)))
            self.assertTrue(A.case_feasible(ctx, 'h', dict(zip(('u', 'v'), point))))

    def test_joint_withdrawal_and_integer_input(self):
        source = S.Source(1, 1, Q(1, 64))
        ctx, proof = S.prove(source, Q(1, 32))
        self.assertEqual(proof.steps[proof.root].budget, Q(-1, 64))
        changed = S.context(S.Source(1, 1, None, 'withdrawn'))
        new, old = S.pair(Q(1, 32))
        with self.assertRaises((A.AuditError, K.ProofError)):
            A.receive(changed, proof, A.request(changed, None, new, old, 0))
        _, marginal = S.prove(source, Q(1, 32), use_joint=False)
        self.assertEqual(marginal.steps[marginal.root].budget, Q(39, 32))

    def test_relative_success_does_not_imply_absolute_adequacy(self):
        for v in (Q(0), Q(10), Q(10**6)):
            poly = R.polynomial(0, 0, 0, v)
            truth = R.integral(poly)
            losses = {name: abs(S.integrate_samples(rule, {x: R.evaluate(poly, x) for x, _ in rule})-truth)
                      for name, rule in S.RULES.items()}
            self.assertEqual(losses['S']-losses['B'], 0)
            self.assertEqual(losses['S'], v)

    def test_unidentifying_node_and_negative_cap_rejected(self):
        for z in (0, Q(1, 4), Q(1, 2), Q(3, 4), 1):
            with self.assertRaises(InputError):
                S.weights(z)
        with self.assertRaises(InputError):
            S.context(S.Source(Q(-1), Q(1)))


class CascadeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = C.collect()

    def test_actual_bounded_outcomes_and_complete_ordinary_control(self):
        for caps, (observed, attempts, fallback, ordinary) in self.records.items():
            self.assertEqual(observed, caps)
            self.assertEqual(tuple(a.proof_nodes for a in attempts), (5, 5, 5))
            self.assertEqual(fallback.proof_nodes, 9)
            self.assertEqual(ordinary.proof_nodes, 9 if all(caps) else 5)
            self.assertEqual(ordinary.status, 'certified')
            self.assertEqual(fallback.status, 'certified')

    def test_weaker_query_changes_self_assessed_availability(self):
        records = C.collect(budget=Q(1), revision='query-revision-2')
        self.assertTrue(all(observed == (0, 0, 0) for observed, *_ in records.values()))

    def test_proper_marginals_do_not_predict_full_cascade(self):
        for k in range(2, 7):
            p, q = (C.parity_population(k, parity) for parity in (0, 1))
            mp, mq = C.summary(p), C.summary(q)
            self.assertTrue(all(mp[a] == mq[a] for a in mp if len(a) < k))
            self.assertEqual(abs(mp[tuple(range(k))]-mq[tuple(range(k))]), Q(1, 2**(k-1)))

    def test_all_subsets_orders_costs_and_penalties_match_execution(self):
        for parity, costs, penalty in product((0, 1),
                ((Q(1),)*3, (Q(1, 2), Q(1), Q(2))), (Q(0), Q(1), Q(4))):
            population = C.parity_population(3, parity)
            moments = C.summary(population)
            for order in R.all_orders(3):
                actual, _ = R.expected(population, order, costs, penalty)
                self.assertEqual(actual, C.compiled_cost(moments, order, costs, penalty))

    def test_self_assessment_selects_different_later_reasoning(self):
        costs, penalty, fallback = (Q(5),)*3, Q(20), Q(9)
        good = R.choose(C.parity_population(3, 0), costs, penalty, fallback)
        bad = R.choose(C.parity_population(3, 1), costs, penalty, fallback)
        self.assertEqual(good, (Q(35, 4), Q(0), 3, (0, 1, 2)))
        self.assertEqual(bad, (Q(9), Q(0), 0, None))
        self.assertEqual(R.expected(C.parity_population(3, 1), (0, 1, 2), costs, penalty),
                         (Q(55, 4), Q(1, 4)))

    def test_white_box_ordinary_control_has_smaller_audit_work(self):
        for parity, expected in ((0, Q(5)), (1, Q(6))):
            population = C.parity_population(3, parity)
            audit = sum((p*self.records[world][3].proof_nodes for world, p in population.items()), Q(0))
            self.assertEqual(audit, expected)
            self.assertLess(audit, Q(35, 4))

    def test_selected_next_stage_actually_executes_current_procedures(self):
        for budget in (Q(0), Q(1)):
            records = self.records if budget == 0 else C.collect(budget=budget, revision='weaker-calibration')
            for parity, penalty in product((0, 1), (Q(2), Q(20))):
                input_law = C.parity_population(3, parity)
                observed_law = {}
                for caps, probability in input_law.items():
                    observed = records[caps][0]
                    observed_law[observed] = observed_law.get(observed, Q(0))+probability
                selected = R.choose(observed_law, (Q(5),)*3, penalty, Q(9))
                actual = missing = Q(0)
                for caps, probability in input_law.items():
                    ctx = C.context(caps, 'later-current-request')
                    cost, unresolved, attempts = C.deploy(ctx, selected[3], penalty, budget)
                    actual += probability*cost
                    missing += probability*unresolved
                    if not unresolved:
                        self.assertEqual(attempts[-1].status, 'certified')
                        A.receive(ctx, attempts[-1].proof,
                                  A.request(ctx, None, K.src('x'), K.num(0), budget))
                self.assertEqual((actual, missing), selected[:2])

    def test_compiled_cheap_fallback_risk_frontier(self):
        for q in (Q(0), Q(1, 160), Q(1, 80), Q(1, 4)):
            ctx, proof, new, old = C.meta_proof(q)
            # Actual proper-uniform law is (1-4q)*even + 4q*odd.
            even, odd = C.parity_population(3, 0), C.parity_population(3, 1)
            population = {bits: (1-4*q)*even.get(bits, 0)+4*q*odd.get(bits, 0)
                          for bits in product((0, 1), repeat=3)}
            losses = [R.execute(bits, (0, 1, 2), (Q(5),)*3, Q(20))[0] for bits in population]
            for alpha in (Q(0), Q(1, 64), Q(1, 32), Q(1, 16), Q(1, 2)):
                allowed = 20*q+4*alpha <= Q(1, 4)
                self.assertEqual(tail(losses, tuple(population.values()), alpha) <= 9, allowed)
                request = A.request(ctx, None, new, old, -4*alpha, 'L')
                if allowed:
                    A.receive(ctx, proof, request)
                else:
                    with self.assertRaises(A.AuditError):
                        A.receive(ctx, proof, request)

    def test_native_metalevel_threshold_and_current_request(self):
        for cap in (Q(0), Q(1, 100), Q(1, 80), Q(1, 64), Q(1, 4)):
            ctx, proof, new, old = C.meta_proof(cap)
            bound = Q(-1, 4)+20*cap
            self.assertEqual(proof.steps[proof.root].budget, bound)
            A.receive(ctx, proof, A.request(ctx, None, new, old, bound, 'L'))
            if cap <= Q(1, 80):
                A.receive(ctx, proof, A.request(ctx, None, new, old, 0, 'L'))
            else:
                with self.assertRaises(A.AuditError):
                    A.receive(ctx, proof, A.request(ctx, None, new, old, 0, 'L'))

    def test_tail_consumer_switch_derived_from_executed_paths(self):
        population = C.parity_population(3, 0)
        losses = [R.execute(bits, (0, 1, 2), (Q(5),)*3, Q(20))[0] for bits in population]
        masses = list(population.values())
        for alpha in (Q(0), Q(1, 17), Q(1, 16), Q(1, 15), Q(1, 2), Q(3, 4), Q(99, 100)):
            risk = tail(losses, masses, alpha)
            self.assertEqual(risk <= 9, alpha <= Q(1, 16))

    def test_unrestricted_drift_invalidates_q_only_revision(self):
        old = C.parity_population(3, 0)
        rho = Q(1, 100)
        new = dict(old)
        new[(0, 0, 0)] -= rho
        new[(1, 1, 1)] = rho
        tv = sum(abs(new.get(bits, 0)-old.get(bits, 0)) for bits in set(new)|set(old))/2
        self.assertEqual(tv, rho)
        actual, unresolved = R.expected(new, (0, 1, 2), (Q(5),)*3, Q(20))
        self.assertEqual(unresolved, rho)
        self.assertLess(Q(35, 4)+20*rho, 9)
        self.assertEqual(actual, Q(181, 20))
        self.assertGreater(actual, 9)

    def test_proper_marginal_preserving_drift_has_different_radius(self):
        even, odd = C.parity_population(3, 0), C.parity_population(3, 1)
        for rho in (Q(0), Q(1, 120), Q(1, 20), Q(1, 19), Q(1)):
            mixture = {bits: (1-rho)*even.get(bits, 0)+rho*odd.get(bits, 0)
                       for bits in product((0, 1), repeat=3)}
            actual, unresolved = R.expected(mixture, (0, 1, 2), (Q(5),)*3, Q(20))
            self.assertEqual(unresolved, rho/4)
            self.assertEqual(actual, Q(35, 4)+5*rho)
            self.assertEqual(actual <= 9, rho <= Q(1, 20))

    def test_moment_inversion_recovers_every_exact_world_mass(self):
        population = {bits: Q(i+1, 36) for i, bits in enumerate(product((0, 1), repeat=3))}
        moments = C.summary(population)
        for bits, mass in population.items():
            ones = frozenset(i for i, bit in enumerate(bits) if bit)
            reconstructed = sum(((-1)**(len(subset)-len(ones))*value
                                 for subset, value in moments.items() if ones <= frozenset(subset)), Q(0))
            self.assertEqual(reconstructed, mass)

    def test_stateful_order_invalidates_static_trace_prediction(self):
        self.assertEqual(C.stateful_run(('A',))[0], 'unavailable')
        self.assertEqual(C.stateful_run(('B',))[0], 'unavailable')
        self.assertEqual(C.stateful_run(('A', 'B'))[0], 'certified')
        self.assertEqual(C.stateful_run(('B', 'A'))[0], 'unavailable')

    def test_cached_lemma_rejected_on_context_revision(self):
        _, _, cache, _ = C.stateful_run(('A',), revision='old')
        with self.assertRaises((A.AuditError, K.ProofError)):
            C.stateful_run(('B',), revision='new', initial_cache=cache)

    def test_stale_reset_proof_and_stronger_query_rejected(self):
        old = C.context((0, 0, 0), 'old')
        proof = C.run(old, 0).proof
        new = C.context((1, 1, 1), 'new')
        with self.assertRaises((A.AuditError, K.ProofError)):
            A.receive(new, proof, A.request(new, None, K.src('x'), K.num(0), 0))
        with self.assertRaises(A.AuditError):
            A.receive(old, proof, A.request(old, None, K.src('x'), K.num(0), Q(-1, 100)))


if __name__ == '__main__':
    unittest.main()
