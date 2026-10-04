"""Ordinary precomputed coefficients still require a fresh native receipt."""
from dataclasses import replace
from fractions import Fraction as Q
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.verification import catalogue, native
from v2.verification.model import Evidence, Query
from v2.verification.producer import produce
from v2.verification.reference import reference


class F11CatalogueTests(unittest.TestCase):
    def test_same_directions_new_budgets_and_versions_match_cold_search(self):
        old = Evidence(beta=Q(0), gamma=Q(0), revision='catalogue-build')
        for action in ('T1', 'T2', 'R'):
            query = Query(action)
            stored = catalogue.build(old, query)
            self.assertTrue(stored.complete)
            for new in (Evidence(beta=Q(0), gamma=Q(8, 85), revision='boundary'),
                        Evidence(beta=Q(1, 64), gamma=Q(1, 4), revision='looser')):
                selected = catalogue.select(new, query, stored)
                cold = produce(new, query)
                self.assertEqual(selected.outcome.upper_bound, cold.upper_bound)
                self.assertEqual(cold.upper_bound, reference(new, query).maximum)
                self.assertEqual(selected.outcome.basis_checks, 0)
                self.assertGreater(selected.template_evaluations, 0)
                root = A.receive(native.context(new), selected.outcome.proof,
                                 native.bound_request(native.context(new), action, cold.upper_bound))
                self.assertEqual(root.context_id, K.fingerprint(native.context(new)))

    def test_changed_presence_or_action_does_not_reuse_a_different_schema(self):
        stored = catalogue.build(Evidence(), Query('T1'))
        for evidence, query in ((Evidence(beta=0), Query('T1')), (Evidence(), Query('T2'))):
            result = catalogue.select(evidence, query, stored)
            self.assertEqual(result.outcome.reason, 'catalogue_schema_mismatch')

    def test_partial_catalogue_and_selection_budget_remain_explicit(self):
        source, query = Evidence(), Query('T1')
        partial = catalogue.build(source, query, max_bases=0)
        self.assertFalse(partial.complete)
        self.assertEqual(catalogue.select(source, query, partial).outcome.reason, 'catalogue_missing_sign')
        complete = catalogue.build(source, query)
        self.assertEqual(catalogue.select(source, query, complete, max_evaluations=0).outcome.reason,
                         'catalogue_selection_limit')

    def test_forged_coefficients_do_not_bypass_the_kernel(self):
        source, query = Evidence(), Query('T1')
        stored = catalogue.build(source, query)
        invalid = ((0, 1, 4), (Q(0), Q(0), Q(0)))
        forged = replace(stored, branches=((invalid,), (invalid,)))
        with self.assertRaises((AssertionError, K.ProofError)):
            catalogue.select(source, query, forged)

    def test_incomplete_catalogue_can_supply_a_checked_bound_without_claiming_optimality(self):
        source, query = Evidence(), Query('T1', Q(10))
        stored = catalogue.build(source, query, max_bases=39)
        self.assertFalse(stored.complete)
        selected = catalogue.select(source, query, stored)
        self.assertFalse(selected.catalogue_complete)
        self.assertEqual(selected.outcome.status, 'certified')
        self.assertGreaterEqual(selected.outcome.upper_bound, reference(source, query).maximum)
        A.receive(native.context(source), selected.outcome.proof,
                  native.request(native.context(source), query))


if __name__ == '__main__':
    unittest.main()
