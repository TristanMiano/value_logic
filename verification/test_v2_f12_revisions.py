"""New F12 consumer and retained-support regressions."""
from dataclasses import replace
from fractions import Fraction as Q
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as A
from v2.verification import native, receipts
from v2.verification.model import Evidence, Query
from v2.verification.producer import produce
from v2.verification.reference import reference
from v2.verification.reuse import reuse
from v2.verification.revision_study import check_revision
from v2.verification.workloads import revisions
from v2.verification.sequence_cost import Strategy, compact, run
from v2.verification.minimize_reuse import candidates


class F12RevisionTests(unittest.TestCase):
    def test_smaller_strict_margin_miss_survives_current_receipt_check(self):
        old, query = Evidence(0, 0, 0, 0), Query('T1')
        saved = receipts.make_receipt(old, query, produce(old, query))
        current = Evidence(beta=0, gamma=Q(3, 32), revision='strict-margin')
        rebuilt = reuse(current, query, saved)
        fresh = produce(current, query)
        self.assertEqual(reference(current, query).maximum, Q(-3, 8192))
        self.assertEqual((fresh.status, fresh.upper_bound), ('certified', Q(-3, 8192)))
        self.assertEqual((rebuilt.status, rebuilt.upper_bound), ('unavailable', Q(3, 8192)))
        wire = receipts.make_receipt(current, query, rebuilt)
        self.assertEqual(receipts.receive_receipt(current, Query('T1', Q(3, 8192)), wire).budget, Q(3, 8192))
        with self.assertRaises(A.AuditError):
            receipts.receive_receipt(current, query, wire)

    def test_minimizer_order_is_finite_unique_and_denominator_first(self):
        values = tuple(candidates())
        self.assertEqual(len(values), len(set(values)))
        self.assertEqual(values, tuple(sorted(values, key=lambda x: (x.denominator, x.numerator))))
        witness_index = values.index(Q(3, 32))
        self.assertEqual(witness_index, 310)
        self.assertTrue(all(value.denominator <= 32 for value in values))
        for bad in (0, 33, True):
            with self.assertRaises(ValueError):
                tuple(candidates(bad))

    def test_one_of_each_declared_revision_kind(self):
        for change in revisions()[6:12]:
            result = check_revision(change, 'T1')
            self.assertEqual(result['relation'], change.relation)
            if result['reused_bound'] is not None:
                self.assertGreaterEqual(Q(result['reused_bound']), Q(result['fresh_bound']))

    def test_parametric_reuse_threshold_miss_and_explicit_fallback(self):
        old, query = Evidence(0, 0, 0, 0), Query('T1')
        saved = receipts.make_receipt(old, query, produce(old, query))
        for offset in (-Q(1, 10000), Q(0), Q(1, 10000)):
            current = Evidence(beta=Q(0), gamma=Q(8, 85)+offset, revision=str(offset))
            rebuilt = reuse(current, query, saved)
            maximum = reference(current, query).maximum
            self.assertGreaterEqual(rebuilt.upper_bound, maximum)
            fresh = produce(current, query)
            self.assertEqual(fresh.upper_bound, maximum)
            if not offset:
                self.assertEqual((rebuilt.upper_bound, maximum), (Q(1, 1360), Q(0)))

    def test_a_retained_alternative_survives_when_selected_support_is_lost(self):
        x, z = K.src('x'), K.num(0)
        ctx = K.context(('x',), (K.Row(x, K.num(-1)), K.Row(x, z)), {'x': -1})
        one = K.Builder(ctx, 'h'); one.rewrite(one.row(0), x, z)
        both = K.Builder(ctx, 'h')
        first = both.rewrite(both.row(0), x, z)
        second = both.rewrite(both.row(1), x, z)
        both.meet(first, second)
        alive = frozenset({('h', 1)})
        with self.assertRaises(T.UnavailableProof):
            T.restrict_rows(ctx, one.proof(), alive)
        current, proof = T.restrict_rows(ctx, both.proof(), alive)
        self.assertEqual(A.receive(current, proof, A.request(current, None, x, z, 0)).budget, 0)
        with self.assertRaises(T.UnavailableProof):
            T.restrict_rows(ctx, both.proof(), frozenset())

    def test_changed_consumer_does_not_get_a_free_old_certificate(self):
        evidence = Evidence(0, 0, 0, 0)
        saved = receipts.make_receipt(evidence, Query('T1'), produce(evidence, Query('T1')))
        self.assertEqual(reuse(evidence, Query('R'), saved).reason, 'query_changed')
        with self.assertRaises(receipts.ReceiptError):
            receipts.receive_receipt(evidence, Query('R'), saved)

    def test_context_observation_change_requires_a_separate_bridge(self):
        old, proof = T.alternative_example()
        changed = replace(old, observation='different-observed-information')
        with self.assertRaises(K.ProofError):
            T.transport(old, changed, proof, {}, {'h': 'h'})


class F12CostContractTests(unittest.TestCase):
    def test_reconstruction_fallback_is_charged_and_repaired(self):
        strategy = Strategy('reuse-fallback')
        old, current = Evidence(0, 0, 0, 0), Evidence(beta=0, gamma=Q(8, 85), revision='boundary')
        strategy.answer(old, Query('T1'))
        outcome, stages, counters, wire = strategy.answer(current, Query('T1'))
        self.assertEqual(outcome.status, 'certified')
        self.assertEqual(outcome.upper_bound, 0)
        self.assertEqual(counters['fallback_calls'], 1)
        self.assertEqual(counters['reuse_calls'], 1)
        self.assertEqual(counters['fresh_calls'], 1)
        self.assertGreater(stages['reconstruction_ns'], 0)
        self.assertGreater(stages['fresh_generation_ns'], 0)
        self.assertEqual(receipts.receive_receipt(current, Query('T1'), receipts.loads(wire)).budget, 0)

    def test_catalogue_schema_rebuilds_are_not_free(self):
        strategy = Strategy('catalogue')
        for evidence, expected_builds in ((Evidence(beta=0), 1),
                                          (Evidence(beta=Q(1, 4), revision='new'), 0),
                                          (Evidence(), 1)):
            _, _, counters, _ = strategy.answer(evidence, Query('T1'))
            self.assertEqual(counters['catalogue_builds'], expected_builds)
        self.assertEqual(len(strategy.catalogues), 2)
        self.assertGreater(sum(strategy.catalogue_sizes.values()), 0)

    def test_fresh_sequence_has_common_receiver_costs_and_no_unearned_retention(self):
        data = run('fresh', 'stable-revisions')
        self.assertEqual(data['queries'], 18)
        self.assertEqual(data['exact_bounds'], 18)
        self.assertEqual(data['missed_true_requests'], 0)
        self.assertEqual(data['total_operation_ns'], sum(r['operation_ns'] for r in data['rows']))
        for row in data['rows']:
            self.assertGreater(row['stage_ns']['receiver_decode_check_ns'], 0)
            self.assertEqual(row['retained_receipt_bytes_including_old_sources'], 0)
            self.assertEqual(row['retained_catalogue_bytes'], 0)
            self.assertEqual(row['total_live_serialized_bytes'],
                             row['request_bytes_including_source']+row['output_receipt_bytes'])


if __name__ == '__main__':
    unittest.main()
