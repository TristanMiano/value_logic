"""F14 development validation, never final evaluation or universal novelty evidence."""
from fractions import Fraction as Q
from itertools import permutations
from copy import deepcopy
import unittest
from unittest.mock import patch

from v2.checks import f07_soundness as A
from v2.experiments import retention as F
from v2.verification import case_cascade as C
from v2.verification import c4_price_revision as C4


class RetentionDevelopment(unittest.TestCase):
    def setUp(self):
        self.config = F.defaults()
        self.case = F.generate_case(self.config['development_seeds'][0], 'small_price', self.config)

    def test_generator_reproducibility_and_positive_revision_prices(self):
        self.assertEqual(self.case, F.generate_case(14101, 'small_price', self.config))
        for variant in F.VARIANTS:
            case = F.generate_case(14101, variant, self.config)
            self.assertTrue(all(p > 0 for p in case.old_law))
            self.assertEqual(sum(case.old_law), 1)
            self.assertTrue(all(c > 0 for c in case.prices))
            self.assertNotIn(str(case.seed), case.revision)
        self.assertNotEqual(F.generate_case(14101, 'source_drift', self.config).old_law,
                            F.generate_case(14101, 'source_drift', self.config).scoring_law)

    def test_path_values_match_separate_moment_compilation(self):
        law = dict(zip(F.WORLDS, self.case.old_law))
        moments = C.summary(law)
        for order in tuple(permutations(range(3)))+tuple(permutations(range(3), 2)):
            path_mean = F._dot(F._path_vector(order, self.case.prices, Q(4)), self.case.old_law)
            self.assertEqual(path_mean, C.compiled_cost(moments, order, self.case.prices, Q(4)))

    def test_reset_bits_match_actual_existing_native_attempts(self):
        records = C.collect(k=3, budget=Q(0), revision='F14-permanent-reset-development')
        self.assertEqual(set(records), set(F.WORLDS))
        for inputs, (observed, attempts, fallback, ordinary) in records.items():
            self.assertEqual(observed, inputs)
            self.assertEqual(len(attempts), 3)
            self.assertEqual(fallback.status, 'certified')
            self.assertEqual(ordinary.status, 'certified')

    def test_minimal_and_redundant_profiles_have_identical_fibers(self):
        fibers = [F.recover_fiber(F.retain(self.case.old_law, method, self.config), self.config)
                  for method in ('tailored', 'exact_intervals')]
        self.assertEqual(fibers[0].vertices, fibers[1].vertices)
        self.assertEqual(fibers[0].rank, 6)
        for order in F.ORDERS:
            lo, hi = fibers[0].bounds(F._path_vector(order, (Q(1),)*3, Q(4)))
            self.assertEqual(lo, hi)

    def test_tailored_wire_uses_five_values_and_public_coordinate_order(self):
        payload = F.retain(self.case.old_law, 'tailored', self.config)
        base, residuals = F.T.retain(dict(zip(F.WORLDS, self.case.old_law)), (Q(1),)*3, Q(4))
        self.assertEqual(payload['schema'], 'F14-retained-v2')
        self.assertEqual(set(payload['data']), {'profile'})
        self.assertEqual(payload['data']['profile'],
                         [str(base)]+[str(residuals[s]) for s in F.TAILORED_RESIDUAL_ORDER])
        self.assertEqual(F.public_schema(self.config)['tailored_profile']['residual_order'],
                         ((1,), (2,), (0, 2), (1, 2)))
        legacy = {**payload, 'schema': 'F14-retained-v1', 'data': {'base': str(base),
            'residuals': [[list(s), str(v)] for s, v in sorted(residuals.items())]}}
        self.assertLess(F.nbytes(payload), F.nbytes(legacy))
        with self.assertRaisesRegex(ValueError, 'Unsupported retained payload schema'):
            F.recover_fiber(legacy, self.config)
        for size in (4, 6):
            malformed = deepcopy(payload)
            malformed['data']['profile'] = (payload['data']['profile']+['0'])[:size]
            with self.assertRaisesRegex(ValueError, 'five-value'):
                F.recover_fiber(malformed, self.config)

    def test_known_marginals_reduce_fiber_and_full_joint_is_exact(self):
        payload = F.retain(self.case.old_law, 'tailored', self.config)
        known = F.generate_case(14101, 'known_marginals', self.config).known_marginals
        self.assertEqual(F.recover_fiber(payload, self.config, known_marginals=known).rank, 7)
        full = F.recover_fiber(F.retain(self.case.old_law, 'full_joint', self.config), self.config)
        self.assertEqual(full.vertices, (self.case.old_law,))

    def test_generic_intervals_match_c4_specialized_sharp_geometry(self):
        payload = F.retain(self.case.old_law, 'tailored', self.config)
        fiber = F.recover_fiber(payload, self.config)
        summary = C4.retain_equal_price(dict(zip(F.WORLDS, self.case.old_law)), Q(4))
        for subset in ((), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2)):
            vector = tuple(Q(all(w[i] for i in subset)) for w in F.WORLDS)
            specialized = C4.equal_price_reach_interval(summary, subset)
            self.assertEqual(fiber.bounds(vector), (specialized[0][0], specialized[1][0]))

    def test_native_primal_dual_and_current_receiver(self):
        payload = F.retain(self.case.old_law, 'tailored', self.config)
        fiber = F.recover_fiber(payload, self.config)
        context = F.native_context(fiber, 'development')
        self.assertTrue(all(unit == 'P' for _, unit in context.signature.sources))
        conversion = context.signature.conversion('probability_to_declared_loss')
        self.assertEqual((conversion.source, conversion.target, conversion.factor), ('P', 'U', Q(1)))
        for order in (F.ORDERS[0], F.ORDERS[-1], (0, 2)):
            objective = F._path_vector(order, self.case.prices, Q(4))
            proof, bound = F.emit_proof(fiber, objective, context)
            root = A.receive(context, proof, A.request(context, None,
                             F._term(objective), F.K.num(0), bound))
            self.assertEqual(F.K.infer(root.new, context.signature), 'U')
            self.assertEqual(sum(step.rule == 'convert' for step in proof.steps), 1)
            self.assertLessEqual(len(proof.steps), 128)
            self.assertEqual(root.budget, fiber.bounds(objective)[1])
            with self.assertRaises(A.AuditError):
                A.receive(context, proof, A.request(context, None,
                          F._term(objective), F.K.num(0), bound-Q(1, 1000)))

    def test_same_law_regret_does_not_subtract_independent_endpoints(self):
        # One simplex edge, with A(p)=p1 and B(p)=p1+1/2.
        rows = tuple(tuple(Q(i == j) for j in range(8)) for i in range(2, 8))
        fiber = F.Fiber(rows, (Q(0),)*6)
        a = (Q(0), Q(1))+(Q(0),)*6
        b = tuple(x+Q(1, 2) for x in a)
        self.assertEqual(F.worst_regrets(fiber, (a, b)), (Q(0), Q(1, 2)))
        self.assertEqual(fiber.bounds(a)[1]-fiber.bounds(b)[0], Q(1, 2))

    def test_discarded_source_cannot_be_read_by_selective_solver(self):
        payload = F.retain(self.case.old_law, 'tailored', self.config)
        expected = F.recover_fiber(payload, self.config).vertices
        # Poison all source-production/reacquisition routes. Neither a true-law
        # parameter nor a capability is present at this solver boundary.
        with (patch.object(F.T, 'retain', side_effect=AssertionError('raw law accessed')),
              patch.object(F.Acquisition, 'acquire', side_effect=AssertionError('free acquisition'))):
            self.assertEqual(F.recover_fiber(payload, self.config).vertices, expected)

    def test_withdrawal_removes_old_equations_and_acquisition_is_explicit(self):
        payload = F.retain(self.case.old_law, 'tailored', self.config)
        none = F.recover_fiber(payload, self.config, facts_live=False)
        self.assertEqual(none.rank, 1)
        self.assertEqual(len(none.vertices), 8)
        oracle = F.Acquisition(self.case.scoring_law)
        repaired = F.recover_fiber(payload, self.config, facts_live=False, oracle=oracle)
        self.assertEqual(repaired.vertices, (self.case.scoring_law,))
        self.assertEqual(oracle.calls, 1)
        self.assertEqual(oracle.transferred_bytes, oracle.archive_bytes)

    def test_budget_failure_is_not_partial_success(self):
        payload = F.retain(self.case.old_law, 'marginal_diagnostic', self.config)
        reduced = {**self.config, 'max_vertex_bases': 69}
        with self.assertRaisesRegex(ValueError, 'budget_exhausted'):
            F.recover_fiber(payload, reduced)
        self.assertEqual(F.recover_fiber(payload, self.config).basis_checks, 70)

    def test_receiver_and_unit_gap_sentinels(self):
        result = F.development_sentinels()
        self.assertTrue(result['stale_revision'])
        self.assertTrue(result['changed_current_pair'])
        self.assertTrue(result['budget_limited_valid_request'])
        self.assertTrue(result['unreachable_unit']['native_zero_unavailable'])

    def test_resources_refusal_and_equal_access_panels(self):
        config = {**self.config, 'methods': ['fresh', 'cached_proof', 'tailored']}
        case = F.generate_case(14101, 'withdrawal', config)
        report = F.run_case(case, config)
        self.assertEqual({item['resources']['schema_bytes'] for item in report['methods']},
                         {F.nbytes(F.public_schema(config))})
        for item in report['methods']:
            resource = item['resources']
            self.assertGreater(resource['resident_bytes'], 0)
            self.assertEqual(resource['resident_plus_archive_bytes'],
                             resource['resident_bytes']+resource['external_archive_bytes'])
            if item['access'] == 'no_reacquisition':
                self.assertEqual(item['decision_status'], 'refusal_to_fallback')
                self.assertFalse(item['useful_decision'])
                self.assertEqual(item['scoring']['actual_executed_cost'], '5/2')
                self.assertEqual(resource['acquisition_calls'], 0)
            else:
                self.assertEqual(resource['acquisition_calls'], 1)
                self.assertGreater(resource['external_archive_bytes'], 0)
                self.assertTrue(item['useful_decision'])
                self.assertEqual(item['scoring']['realized_regret'], '0')
            if item['method'] == 'cached_proof':
                self.assertGreater(resource['cached_source_context_bytes'], 0)
                self.assertGreater(resource['cached_proof_bytes'], 0)
                self.assertEqual(item['native']['cache'], 'rejected_then_replacement')
            for horizon in config['horizons']:
                self.assertEqual(resource['horizon_compute_ns'][str(horizon)],
                                 resource['initial_total_ns']+horizon*resource['one_update_total_ns'])

    def test_adaptive_acquisition_skips_sufficient_retained_information(self):
        config = {**self.config, 'access_regimes': ['adaptive_reacquisition'],
                  'methods': ['fresh', 'full_joint', 'tailored', 'exact_intervals']}
        report = F.run_case(self.case, config)
        for item in report['methods']:
            self.assertEqual(item['resources']['acquisition_calls'], 0)
            self.assertGreater(item['resources']['external_archive_bytes'], 0)
            self.assertFalse(item['pre_repair']['decision_refused'])
            self.assertEqual(item['pre_repair']['numeric_refusals'], 0)
            if item['method'] in ('fresh', 'full_joint'):
                self.assertEqual(item['resources']['solver_kind'], 'direct_joint_dot_products')
                self.assertEqual(item['resources']['basis_checks'], 0)
            if item['native']['useful_derivation_candidate']:
                self.assertEqual(item['native']['candidate_order'], item['executed'])
                self.assertEqual(item['native']['certificate_role'], 'selected_order')

    def test_two_new_mean_repair_matches_independent_full_fiber(self):
        for variant in ('large_price', 'large_negative_price'):
            case = F.generate_case(14101, variant, self.config)
            for method in ('tailored', 'exact_intervals'):
                payload = F.retain(case.old_law, method, self.config)
                old_fiber = F.recover_fiber(payload, self.config)
                oracle = F.Acquisition(case.scoring_law)
                orders = F.C4.chain_probe_orders(3)
                means = oracle.acquire_means(orders, case.prices, case.penalty)
                repaired = F.repair_from_new_means(payload, old_fiber, means, case.prices, self.config)
                rows, values = F.payload_rows(payload, self.config)
                independent = F.Fiber(rows+tuple(F._path_vector(order, case.prices, case.penalty)
                                                for order in orders), values+means)
                self.assertEqual(repaired.vertices, independent.vertices)
                self.assertEqual(repaired.vertices, (case.scoring_law,))
                self.assertEqual(oracle.scalar_measurements, 2)
                self.assertEqual(oracle.calls, 2)
                self.assertEqual(oracle.path_world_executions, 16)

    def test_adaptive_mean_repair_does_not_read_full_law(self):
        config = {**self.config, 'access_regimes': ['adaptive_reacquisition'],
                  'methods': ['tailored', 'exact_intervals']}
        case = F.generate_case(14101, 'large_price', config)
        with patch.object(F.Acquisition, 'acquire', side_effect=AssertionError('full source read')):
            report = F.run_case(case, config)
        for item in report['methods']:
            self.assertEqual(item['resources']['acquisition_scalar_measurements'], 2)
            self.assertEqual(item['resources']['acquisition_kinds'], ['two_current_order_means'])
            self.assertTrue(all(row['status'] == 'exact' for row in item['numeric']))

    def test_common_production_and_full_source_truth_are_explicit(self):
        config = {**self.config, 'methods': ['fresh', 'tailored'],
                  'access_regimes': ['no_reacquisition']}
        report = F.run_generated_case(14101, 'known_marginals', config)
        common = report['common_input_accounting']
        self.assertTrue(common['generation_observed'])
        self.assertGreater(common['generation_ns'], 0)
        self.assertEqual(common['current_shared_scalar_inputs'], 3)
        for item in report['methods']:
            resource = item['resources']
            self.assertEqual(resource['one_case_method_plus_common_ns'],
                common['observed_common_production_ns']+resource['initial_total_ns']+resource['one_update_total_ns'])
            self.assertEqual(item['scoring']['full_source_semantic_valid'],
                             Q(item['scoring']['full_source_semantic_value']) <= 0)
            self.assertEqual(resource['current_common_scalar_inputs'], 3)
            priced = item['acquisition_sensitivity'][1]
            self.assertEqual(priced['initial_common_source_loss'], '2/5')
            self.assertEqual(priced['current_common_source_loss'], '3/20')


if __name__ == '__main__':
    unittest.main()
