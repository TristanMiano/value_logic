"""F11 integration boundary tests, not a replacement for F12's revision study."""
from dataclasses import replace
from fractions import Fraction as Q
import json
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.verification import native
from v2.verification.experiment import assess, core_report
from v2.verification.model import Evidence, InputError, Query, core_states
from v2.verification.producer import Limits, produce, solve_three
from v2.verification.reference import reference, task_losses


class F11IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = core_report()
        cls.exact = Evidence(Q(0), Q(0), Q(0), Q(0))
        cls.query = Query('T1')
        cls.good = produce(cls.exact, cls.query)

    def test_all_48_queries_have_exact_native_and_ordinary_bounds(self):
        self.assertEqual(self.report['states'], 16)
        self.assertEqual(self.report['queries'], 48)
        self.assertEqual(sum(self.report['decisions'].values()), 48)
        self.assertNotIn('unavailable', self.report['decisions'])
        for case in self.report['cases']:
            for result in case['comparisons']:
                self.assertEqual(result['native_upper_bound'], result['reference_maximum'])
                self.assertEqual(result['ordinary_bound'], result['reference_maximum'])

    def test_all_returned_proof_nodes_hold_at_independently_found_attainers(self):
        for evidence in core_states():
            for action in ('T1', 'T2', 'R'):
                query = Query(action)
                proof = produce(evidence, query).proof
                point = dict(zip(('beta', 'gamma'), reference(evidence, query).witness))
                report = A.audit_points(native.context(evidence), proof, (point,))
                self.assertGreater(report['node_evaluations'], 0)

    def test_unavailable_is_not_refuted_when_search_is_capped(self):
        result = assess(self.exact, self.query, Limits(0))
        self.assertEqual(result['decision'], 'unavailable')
        self.assertEqual(result['producer_reason'], 'basis_limit')
        self.assertLess(Q(result['reference_maximum']), 0)

    def test_too_small_proof_budget_is_explicit(self):
        result = produce(self.exact, self.query, Limits(max_steps=0))
        self.assertEqual(result.reason, 'step_limit')
        self.assertIsNone(result.proof)

    def test_false_request_requires_a_full_source_countermodel(self):
        result = assess(Evidence(), Query('T1'))
        self.assertEqual(result['decision'], 'refuted')
        self.assertEqual(result['producer_status'], 'unavailable')
        self.assertEqual(result['countermodel_domain'], 'full_source')
        self.assertTrue(result['target_unit_reduct_equals_full_source'])

    def test_receiver_rejects_a_different_action_pair(self):
        ctx = native.context(self.exact)
        with self.assertRaises(A.AuditError):
            A.receive(ctx, self.good.proof, native.request(ctx, Query('T2')))

    def test_receiver_rejects_a_stricter_than_proven_budget(self):
        ctx = native.context(self.exact)
        with self.assertRaises(A.AuditError):
            A.receive(ctx, self.good.proof, native.request(ctx, Query('T1', Q(-1))))

    def test_receipt_is_stale_even_when_only_version_changes(self):
        old = native.context(self.exact)
        new = native.context(replace(self.exact, revision='next'))
        with self.assertRaises(A.AuditError):
            A.receive(new, self.good.proof, native.request(old, self.query))
        with self.assertRaises(K.ProofError):
            A.receive(new, self.good.proof, native.request(new, self.query))

    def test_altered_native_budget_is_not_a_certificate(self):
        proof = self.good.proof
        steps = list(proof.steps)
        steps[proof.root] = replace(steps[proof.root], budget=Q(-1))
        with self.assertRaises(K.ProofError):
            A.receive(native.context(self.exact), K.Proof(tuple(steps), proof.root),
                      native.request(native.context(self.exact), self.query))

    def test_zero_is_present_not_missing(self):
        self.assertGreater(reference(Evidence(), self.query).maximum, 0)
        self.assertLess(reference(self.exact, self.query).maximum, 0)

    def test_closed_equality_threshold_is_certified(self):
        maximum = reference(Evidence(), self.query).maximum
        result = produce(Evidence(), Query('T1', maximum))
        self.assertEqual(result.status, 'certified')
        self.assertEqual(result.upper_bound, maximum)

    def test_invalid_and_out_of_scope_inputs_are_not_logical_outcomes(self):
        for evidence in (Evidence(beta=True), Evidence(plus=0.0),
                         Evidence(gamma=Q(-1, 2)), Evidence(minus=3),
                         Evidence(revision=''), Evidence(beta=Q(1, 2**257))):
            with self.assertRaises(InputError):
                produce(evidence, self.query)
        for query in (Query('unknown'), Query('T1', True)):
            with self.assertRaises(InputError):
                produce(self.exact, query)
        for limits in (Limits(True), Limits(-1), Limits(441), Limits(max_steps=129)):
            with self.assertRaises(InputError):
                produce(self.exact, self.query, limits)

    def test_direct_execution_is_separate_from_native_loss_evaluation(self):
        ctx = native.context(Evidence())
        for beta, gamma in ((Q(0), Q(0)), (Q(-1), Q(1)),
                            (Q(2, 7), Q(-3, 11)), (Q(1), Q(1))):
            actual = task_losses((beta, gamma))
            for action in ('T1', 'T2', 'R', 'F'):
                self.assertEqual(actual[action], A.value(native.loss(action), ctx.signature,
                                                        {'beta': beta, 'gamma': gamma}))

    def test_template_elimination_handles_singular_and_exact_systems(self):
        self.assertIsNone(solve_three(((1, 0, 0), (2, 0, 0), (0, 1, 0)), (1, 1, 1)))
        self.assertEqual(solve_three(((1, 0, 0), (0, 1, 0), (0, 0, 1)), (Q(1, 3), 2, 1)),
                         (Q(1, 3), Q(2), Q(1)))

    def test_report_has_json_safe_exact_values(self):
        encoded = json.dumps(self.report, sort_keys=True)
        self.assertEqual(json.loads(encoded), self.report)
        self.assertNotIn('NaN', encoded)


if __name__ == '__main__':
    unittest.main()
