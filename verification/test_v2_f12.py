"""F12 workload and independent differential boundary regressions."""
from dataclasses import replace
from fractions import Fraction as Q
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.checks import f09_scaling as S
from v2.verification import native, receipts
from v2.verification.model import Evidence, Query
from v2.verification.producer import produce
from v2.verification.reference import reference, task_losses
from v2.verification.differential import check_source, sweep
from v2.verification.workloads import sources, revisions, sequence


class F12DifferentialTests(unittest.TestCase):
    def test_declared_populations_and_deterministic_seed(self):
        for family, count in (('grid', 900), ('rational', 257), ('boundary', 9), ('offgrid', 4)):
            self.assertEqual(len(sources(family)), count)
            self.assertEqual(len({e.revision for e in sources(family)}), count)
            for evidence in sources(family):
                evidence.validate()
        self.assertEqual(sources('rational'), sources('rational'))

    def test_closed_boundaries_and_offgrid_failures_use_the_native_path(self):
        for family in ('boundary', 'offgrid'):
            result = sweep(family)
            self.assertEqual(result['status'], 'PASS')
            self.assertEqual(result['queries'], 3*len(sources(family)))
        for i, evidence in enumerate(sources('boundary')):
            action = ('T1', 'T2', 'R')[i % 3]
            maximum = reference(evidence, Query(action)).maximum
            self.assertEqual(maximum <= 0, i < 6)
            if 3 <= i < 6:
                self.assertEqual(maximum, 0)

    def test_shard_report_cannot_claim_an_empty_or_invalid_interval(self):
        for start, stop in ((0, 0), (-1, 3), (0, 901), (True, 1)):
            with self.assertRaises(ValueError):
                sweep('grid', start, stop)
        result = sweep('grid', 0, 1)
        self.assertEqual((result['start'], result['stop'], result['checked_sources']), (0, 1, 1))

    def test_revision_and_sequence_scope_is_explicit(self):
        self.assertEqual(len(revisions()), 24)
        for name in ('fixed-directions', 'withdrawals', 'stable-revisions'):
            events = sequence(name)
            self.assertEqual(len(events), 18)
            self.assertEqual(len({e.revision for e, _ in events}), 6)
        with self.assertRaises(ValueError):
            sequence('withdrawals', 0)


class F12PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = Evidence(beta=Q(1, 64), gamma=Q(1, 4))
        cls.query = Query('T1')
        cls.ctx = native.context(cls.evidence)
        cls.outcome = produce(cls.evidence, cls.query)

    def test_current_generated_proofs_transport_under_common_positive_scale(self):
        for factor in (Q(1, 7), Q(3), Q(17, 5)):
            changed, proof = S.uniform_scale_proof(self.ctx, self.outcome.proof, factor)
            presentation = S.Presentation(self.ctx.signature, {'U': factor})
            expected = A.request(changed, None, presentation.term(native.loss('T1')),
                                 presentation.term(native.loss('F')), factor*self.outcome.upper_bound)
            root = A.receive(changed, proof, expected)
            self.assertEqual(root.budget, factor*self.outcome.upper_bound)
            point = dict(zip(('beta', 'gamma'), reference(self.evidence, self.query).witness))
            self.assertEqual(A.value(expected.new, changed.signature, presentation.point(point))-
                             A.value(expected.old, changed.signature, presentation.point(point)),
                             factor*self.outcome.upper_bound)

    def test_affine_offsets_correct_native_loss_composition(self):
        presentation = S.Presentation(self.ctx.signature, {'U': Q(3, 2)}, {'U': Q(-7, 3)})
        for point in ((Q(0), Q(0)), (Q(1, 100), Q(-1, 5))):
            mapped = presentation.point(dict(zip(('beta', 'gamma'), point)))
            actual = task_losses(point)
            for action in ('T1', 'T2', 'R', 'F'):
                encoded = presentation.term(native.loss(action))
                self.assertEqual(A.value(encoded, presentation.signature, mapped),
                                 Q(3, 2)*actual[action]-Q(7, 3))

    def test_untransformed_budget_or_old_context_is_not_an_affine_transport(self):
        changed, proof = S.uniform_scale_proof(self.ctx, self.outcome.proof, Q(2))
        with self.assertRaises(K.ProofError):
            K.check(changed, self.outcome.proof)
        presentation = S.Presentation(self.ctx.signature, {'U': Q(2)})
        # This source has a positive sharp T1 bound; failing to scale the
        # requested budget therefore understates the transformed allowance.
        self.assertGreater(self.outcome.upper_bound, 0)
        with self.assertRaises(A.AuditError):
            A.receive(changed, proof, A.request(changed, None,
                      presentation.term(native.loss('T1')), presentation.term(native.loss('F')),
                      self.outcome.upper_bound))

    def test_foreign_scope_and_undeclared_unit_cannot_be_relabelled(self):
        changed = replace(self.ctx, signature=replace(self.ctx.signature, scope='different-operation'))
        with self.assertRaises(K.ProofError):
            K.check(changed, self.outcome.proof)
        request = native.bound_request(self.ctx, 'T1', self.outcome.upper_bound)
        with self.assertRaises(A.AuditError):
            A.receive(self.ctx, self.outcome.proof, replace(request, unit='undeclared'))

    def test_forged_negative_scale_and_additive_budget_are_rejected(self):
        for rule, parents, data in (('scale', (self.outcome.proof.root,), (Q(-1),)),
                                     ('add', (self.outcome.proof.root, self.outcome.proof.root), ())):
            step = replace(self.outcome.proof.steps[-1], rule=rule, parents=parents,
                           budget=Q(-100), data=data)
            proof = K.Proof(self.outcome.proof.steps+(step,), len(self.outcome.proof.steps))
            with self.assertRaises(K.ProofError):
                K.check(self.ctx, proof)


if __name__ == '__main__':
    unittest.main()
