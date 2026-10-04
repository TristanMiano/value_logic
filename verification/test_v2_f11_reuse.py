"""Small retained-proof integration controls; the broad exploration is separate."""
from dataclasses import replace
from fractions import Fraction as Q
import json
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.verification import native, receipts
from v2.verification.model import Evidence, InputError, Query
from v2.verification.producer import produce
from v2.verification.reference import reference
from v2.verification.reuse import ReuseLimits, reuse


class F11ReuseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = Evidence(Q(0), Q(0), Q(0), Q(0), 'old')
        cls.query = Query('T1')
        cls.payload = receipts.make_receipt(cls.old, cls.query, produce(cls.old, cls.query))

    def test_explicit_version_rebuild_gets_current_receipt(self):
        new = replace(self.old, revision='new')
        result = reuse(new, self.query, self.payload)
        self.assertEqual(result.status, 'certified')
        self.assertEqual(result.upper_bound, Q(-3, 32))
        saved = receipts.make_receipt(new, self.query, result)
        root = receipts.receive_receipt(new, self.query, saved)
        self.assertEqual(root.context_id, K.fingerprint(native.context(new)))

    def test_withdrawal_replaces_old_directions_but_does_not_copy_old_bound(self):
        new = Evidence(revision='withdrawn')
        result = reuse(new, self.query, self.payload)
        self.assertEqual(result.status, 'unavailable')
        self.assertEqual(result.upper_bound, Q(505, 256))
        actual = reference(new, self.query)
        self.assertEqual(actual.maximum, Q(471, 256))
        self.assertGreater(result.upper_bound, actual.maximum)
        root = A.receive(native.context(new), result.proof,
                         native.bound_request(native.context(new), 'T1', result.upper_bound))
        self.assertEqual(root.budget, result.upper_bound)

    def test_sound_reuse_can_miss_a_true_closed_threshold(self):
        new = Evidence(beta=Q(0), gamma=Q(8, 85), revision='boundary')
        result = reuse(new, self.query, self.payload)
        fresh = produce(new, self.query)
        self.assertEqual(result.upper_bound, Q(1, 1360))
        self.assertEqual(result.status, 'unavailable')
        self.assertEqual(fresh.status, 'certified')
        self.assertEqual(fresh.upper_bound, 0)
        self.assertEqual(reference(new, self.query).maximum, 0)

    def test_stronger_source_can_reuse_weak_source_proof(self):
        source = Evidence()
        saved = receipts.make_receipt(source, self.query, produce(source, self.query))
        result = reuse(self.old, self.query, saved)
        self.assertEqual(result.status, 'certified')
        self.assertEqual(result.upper_bound, Q(-3, 32))

    def test_reuse_is_nonmutating(self):
        before = json.dumps(self.payload, sort_keys=True)
        reuse(replace(self.old, revision='new'), self.query, self.payload)
        self.assertEqual(json.dumps(self.payload, sort_keys=True), before)

    def test_different_consumer_requires_an_explicit_new_query_search(self):
        result = reuse(self.old, Query('R'), self.payload)
        self.assertEqual(result.reason, 'query_changed')
        self.assertIsNone(result.proof)

    def test_resource_refusal_is_not_refutation(self):
        for limits, reason in ((ReuseLimits(0), 'row_replacement_limit'),
                               (ReuseLimits(max_steps=0), 'reused_step_limit')):
            result = reuse(self.old, self.query, self.payload, limits)
            self.assertEqual(result.status, 'unavailable')
            self.assertEqual(result.reason, reason)
            self.assertIsNone(result.proof)
        with self.assertRaises(InputError):
            reuse(self.old, self.query, self.payload, ReuseLimits(True))


if __name__ == '__main__':
    unittest.main()
