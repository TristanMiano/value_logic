"""Optional F12 stronger ordinary controls and program coverage boundaries."""
from dataclasses import replace
from fractions import Fraction as Q
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.verification import native, receipts, selected_cache
from v2.verification.model import Evidence, Query
from v2.verification.producer import produce
from v2.verification.optional_cost import Anchored, SelectedFresh, factory
from v2.verification.sequence_cost import run
from v2.verification.program_differential import sources, check_source


class F12OptionalTests(unittest.TestCase):
    def test_anchored_policy_keeps_original_source_and_counts_new_output(self):
        strategy = Anchored()
        old = Evidence(0, 0, 0, 0, 'origin')
        query = Query('T1')
        strategy.answer(old, query)
        original = strategy.saved['T1']
        sizes = []
        for revision in ('one', 'two', 'three'):
            current = replace(old, revision=revision)
            outcome, _, _, wire = strategy.answer(current, query)
            self.assertIs(strategy.saved['T1'], original)
            self.assertFalse(strategy.output_is_retained)
            self.assertEqual(receipts.receive_receipt(current, query, receipts.loads(wire)).budget, Q(-3, 32))
            sizes.append(len(outcome.proof.steps))
        self.assertEqual(len(set(sizes)), 1)

    def test_selected_coefficients_emit_a_current_received_proof(self):
        old, query = Evidence(beta=0, gamma=0), Query('T1')
        stored = selected_cache.from_outcome(old, query, produce(old, query))
        current = replace(old, revision='new-version')
        outcome = selected_cache.replay(current, query, stored)
        self.assertEqual(outcome.status, 'certified')
        A.receive(native.context(current), outcome.proof, native.request(native.context(current), query))

    def test_selected_numeric_refusal_is_not_an_unchecked_certificate(self):
        old, query = Evidence(beta=0, gamma=0), Query('T1')
        stored = selected_cache.from_outcome(old, query, produce(old, query))
        outcome = selected_cache.replay(Evidence(beta=1, gamma=1), query, stored)
        self.assertEqual(outcome.status, 'unavailable')
        self.assertIsNone(outcome.proof)
        self.assertIsNone(outcome.upper_bound)

    def test_selected_schema_change_and_forged_weights_do_not_bypass_checks(self):
        source, query = Evidence(), Query('T1', Q(10))
        stored = selected_cache.from_outcome(source, query, produce(source, query))
        self.assertEqual(selected_cache.replay(Evidence(beta=0), query, stored).reason, 'selected_schema_changed')
        forged = replace(stored, branches=(((0, 1, 4), (Q(0), Q(0), Q(0))),)*2)
        with self.assertRaises((K.ProofError, AssertionError)):
            selected_cache.replay(source, query, forged)

    def test_selected_fallback_charges_fresh_search_and_storage(self):
        strategy = SelectedFresh()
        query = Query('T1')
        strategy.answer(Evidence(beta=0, gamma=0), query)
        outcome, stages, counters, _ = strategy.answer(Evidence(), query)
        self.assertEqual(counters['fresh_calls'], 1)
        self.assertEqual(counters['fallback_calls'], 1)
        self.assertGreater(stages['selected_storage_encoding_ns'], 0)
        self.assertGreater(sum(strategy.catalogue_sizes.values()), 0)
        self.assertEqual(outcome.upper_bound, Q(471, 256))

    def test_program_population_and_degenerate_foreign_source(self):
        population = sources()
        self.assertEqual(len(population), 60)
        for evidence in (population[0], population[1], population[-2], population[-1]):
            answers = check_source(evidence)
            self.assertEqual(len(answers), 7)
            for row in answers:
                self.assertGreaterEqual(Q(row['native_reduct_bound']), Q(row['full_bound']))

    def test_optional_storage_counts_transmitted_outputs_separately(self):
        data = run('selected-fresh', 'stable-revisions', strategy_factory=factory)
        self.assertEqual(data['missed_true_requests'], 0)
        for row in data['rows']:
            self.assertEqual(row['total_live_serialized_bytes'], row['request_bytes_including_source']+
                             row['output_receipt_bytes']+row['retained_catalogue_bytes'])


if __name__ == '__main__':
    unittest.main()
