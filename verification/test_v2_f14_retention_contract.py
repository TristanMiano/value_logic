"""Prospective retention result-contract checks on development episodes only."""
from copy import deepcopy
from fractions import Fraction as Q
import json
import unittest

from v2.experiments import analysis as A
from v2.experiments import retention as R


class RetentionAssessmentContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rc = R.defaults()
        rc['variants'] = ['small_price', 'proportional', 'withdrawal']
        cls.config = {'retention': rc, 'analysis': A.defaults()}
        raw = [R.run_generated_case(seed, variant, rc)
               for seed in rc['development_seeds'] for variant in rc['variants']]
        # Exercise the actual JSON transport form, including tuple-to-list conversion.
        cls.results = json.loads(json.dumps(raw))

    def assess(self, data=None):
        return A.retention_assessment(self.results if data is None else data,
                                      self.config, development=True)

    def changed_row(self, predicate=lambda row: True):
        data = deepcopy(self.results)
        selected = next(row for case in data for row in case['methods'] if predicate(row))
        return data, selected

    def test_complete_development_grid_and_fallback_dispositions(self):
        report = self.assess()
        self.assertEqual(report['case_count'], 6)
        self.assertEqual(report['method_rows'], 72)
        self.assertEqual(sum(report['numeric_dispositions'].values()), 72*6)
        self.assertGreater(report['decision_dispositions'].get('certified_fallback', 0), 0)
        self.assertGreater(report['decision_dispositions'].get('refusal_to_fallback', 0), 0)
        self.assertFalse(report['bounded_application_criterion_met'])
        self.assertFalse(report['novelty_criterion_independently_established'])
        pairs = report['paired_resource_and_decision_comparisons']
        refused = [p for p in pairs
                   if p['method_quality']['decision']['status'] == 'refusal_to_fallback']
        self.assertTrue(refused)
        self.assertTrue(all(not p['both_admit_all_numeric_queries_and_certify_decision']
                            and not p['both_admit_numeric_decision_and_selected_order_proof'] for p in refused))
        self.assertEqual(len(report['equal_information_control_comparisons']), 36)

    def test_uncertain_law_does_not_imply_approximate_selected_cost(self):
        report = self.assess()
        evidence = report['uncertain_approximate_selective_useful_cases']
        exact_key = {'seed': 14101, 'variant': 'small_price',
                     'method': 'tailored', 'access': 'no_reacquisition'}
        approximate_key = dict(exact_key, seed=14102)
        for key, expected in ((exact_key, 'exact'), (approximate_key, 'approximate')):
            case = next(c for c in self.results
                        if c['seed'] == key['seed'] and c['variant'] == key['variant'])
            row = next(r for r in case['methods']
                       if r['method'] == key['method'] and r['access'] == key['access'])
            self.assertGreater(row['resources']['fiber_vertex_count'], 1)
            self.assertTrue(row['native']['useful_derivation_candidate'])
            self.assertEqual(row['numeric'][row['executed_index']]['status'], expected)
        self.assertIn(exact_key, report['uncertain_selective_useful_cases'])
        self.assertNotIn(exact_key, evidence)
        self.assertIn(approximate_key, evidence)

    def test_missing_or_reordered_sample_is_rejected(self):
        for data in (self.results[:-1], list(reversed(self.results))):
            with self.assertRaisesRegex(ValueError, 'Every frozen retention case'):
                self.assess(data)

    def test_missing_or_duplicated_control_is_rejected(self):
        missing = deepcopy(self.results)
        missing[0]['methods'].pop()
        duplicate = deepcopy(self.results)
        duplicate[0]['methods'][-1] = deepcopy(duplicate[0]['methods'][0])
        for data in (missing, duplicate):
            with self.assertRaisesRegex(ValueError, 'ordinary control'):
                self.assess(data)

    def test_false_numerical_admission_is_rejected(self):
        data, row = self.changed_row(lambda r: r['method'] == 'fresh')
        row['scoring']['numeric_errors'][0] = '1'
        with self.assertRaisesRegex(ValueError, 'False numerical admission'):
            self.assess(data)

    def test_equal_information_controls_must_agree_on_tight_intervals(self):
        data, row = self.changed_row(lambda r: r['method'] == 'exact_intervals'
            and r['access'] == 'no_reacquisition'
            and any(a['status'] == 'approximate' for a in r['numeric']))
        answer = next(a for a in row['numeric'] if a['status'] == 'approximate')
        # This conservative widening preserves midpoint, scoring error,
        # disposition and the existing decision/native fields. Per-row safety
        # checks alone therefore miss the false claim of tight equivalence.
        answer['lower'] = str(Q(answer['lower'])-Q(1, 10000))
        answer['upper'] = str(Q(answer['upper'])+Q(1, 10000))
        with self.assertRaisesRegex(ValueError, 'Equal-information controls'):
            self.assess(data)

    def test_refusal_cannot_be_credited_as_safe_fallback(self):
        data, row = self.changed_row(lambda r: r['decision_status'] == 'refusal_to_fallback')
        row['decision_status'] = 'certified_fallback'
        with self.assertRaisesRegex(ValueError, 'fallback|refusal'):
            self.assess(data)

    def test_false_received_native_proof_is_rejected(self):
        data, row = self.changed_row(lambda r: r['native']['status'] == 'received')
        row['native']['upper_bound'] = '1/10'
        row['native']['semantic_valid'] = False
        with self.assertRaisesRegex(ValueError, 'received current proof'):
            self.assess(data)

    def test_full_source_flag_must_match_its_actual_value(self):
        data, row = self.changed_row(lambda r: r['native']['status'] == 'received')
        row['scoring']['full_source_semantic_value'] = '1'
        row['scoring']['full_source_semantic_valid'] = True
        with self.assertRaises(ValueError):
            self.assess(data)

    def test_negative_coherent_regret_is_not_a_certificate(self):
        data, row = self.changed_row(lambda r: r['decision_status'] == 'certified_order')
        row['coherent_worst_regret'] = '-1'
        with self.assertRaises(ValueError):
            self.assess(data)

    def test_actual_certified_regret_must_fit_the_coherent_bound(self):
        data, row = self.changed_row(lambda r: r['decision_status'] == 'certified_order')
        row['scoring']['realized_regret'] = '1/40'
        row['coherent_worst_regret'] = '0'
        with self.assertRaises(ValueError):
            self.assess(data)

    def test_duplicate_numeric_query_does_not_cover_all_orders(self):
        data, row = self.changed_row()
        row['numeric'][1]['order'] = deepcopy(row['numeric'][0]['order'])
        with self.assertRaises(ValueError):
            self.assess(data)

    def test_selected_and_executed_order_indices_are_binding(self):
        data, row = self.changed_row(lambda r: r['decision_status'] == 'certified_order')
        row['selected_index'] = 6
        with self.assertRaises(ValueError):
            self.assess(data)

    def test_useful_proof_cannot_certify_an_unchosen_order(self):
        data, row = self.changed_row(lambda r: r['native']['useful_derivation_candidate'])
        alternatives = [n['order'] for n in row['numeric'] if n['order'] != row['executed']]
        row['native']['candidate_order'] = alternatives[0]
        with self.assertRaisesRegex(ValueError, 'useful derivation'):
            self.assess(data)


if __name__ == '__main__':
    unittest.main()
