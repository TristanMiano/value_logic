"""Optional actual-program compiler, independently executed risk and unit scope."""
from fractions import Fraction as Q
from itertools import product
import unittest

from v2.checks import f06_derived_cases as C
from v2.checks import f07_soundness as A
from v2.verification import program
from v2.verification.program_control import report
from v2.verification.program_model import ProgramEvidence, ProgramQuery
from v2.verification.program_reference import difference, execute, loss_law, reference, tail
from v2.verification.model import InputError


class F11ProgramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()

    def test_thirty_family_queries_match_exact_reduct_reference(self):
        self.assertEqual(self.report['family_queries'], 30)
        self.assertEqual(len(self.report['cases']), 6)
        for case in self.report['cases']:
            for result in case['results']:
                self.assertEqual(result['native_bound'], result['target_unit_reduct_maximum'])
                self.assertEqual(result['full_source_maximum'], result['target_unit_reduct_maximum'])

    def test_risk_switch_includes_the_closed_boundary(self):
        evidence = ProgramEvidence()
        for alpha, expected, status in ((Q(0), Q(-1, 40), 'certified'),
                                        (Q(1, 6), Q(0), 'certified'),
                                        (Q(1, 3), Q(3, 80), 'unavailable')):
            result = program.produce(evidence, ProgramQuery('risk_vs_full', alpha))
            self.assertEqual((result.upper_bound, result.status), (expected, status))

    def test_same_old_complete_loss_law_does_not_decide_program_edit(self):
        first = loss_law('adaptive', Q(1, 20), Q(1, 5))
        second = loss_law('adaptive', Q(1, 20), Q(3, 10))
        self.assertEqual(first, second)
        self.assertEqual(difference(ProgramQuery(), Q(1, 20), Q(1, 5)), Q(-1, 40))
        self.assertEqual(difference(ProgramQuery(), Q(1, 20), Q(3, 10)), Q(3, 40))

    def test_reduct_countermodel_is_explicitly_not_a_full_source_countermodel(self):
        gap = self.report['unit_boundary_control']
        self.assertEqual(gap['decision'], 'unavailable')
        self.assertEqual(gap['countermodel_domain'], 'target_unit_reduct')
        self.assertFalse(gap['reduct_attainer_satisfies_full_source'])
        self.assertLess(Q(gap['full_source_maximum']), Q(gap['budget']))
        self.assertGreater(Q(gap['target_unit_reduct_maximum']), Q(gap['budget']))

    def test_every_optional_proof_node_at_execution_witness(self):
        evidence = ProgramEvidence()
        query = ProgramQuery('risk_vs_full', Q(9, 10))
        outcome = program.produce(evidence, query)
        _, witness = reference(evidence, query)
        ctx = program.context(evidence)
        checked = A.audit_points(ctx, outcome.proof, (dict(zip(('error', 'second'), witness)),))
        self.assertGreater(checked['node_evaluations'], 0)
        decoded = C.unpack_proof(ctx, C.pack_proof(outcome.proof))
        self.assertEqual(decoded, outcome.proof)

    def test_reference_execution_and_native_terms_agree_at_noncorner_points(self):
        evidence = ProgramEvidence()
        ctx = program.context(evidence)
        queries = (ProgramQuery(), ProgramQuery('risk_vs_full', Q(2, 5)))
        for e, u in product((Q(0), Q(1, 77), Q(1, 20)), (Q(1, 5), Q(2, 9), Q(3, 10))):
            for query in queries:
                new, old, _ = program.terms(query)
                point = {'error': e, 'second': u}
                self.assertEqual(A.value(new, ctx.signature, point)-A.value(old, ctx.signature, point),
                                 difference(query, e, u))

    def test_current_consumer_cannot_be_taken_from_the_returned_root(self):
        evidence = ProgramEvidence()
        outcome = program.produce(evidence, ProgramQuery('risk_vs_full', Q(0)))
        with self.assertRaises(A.AuditError):
            A.receive(program.context(evidence), outcome.proof,
                      program.request(program.context(evidence), ProgramQuery('risk_vs_full', Q(1, 6))))

    def test_program_resource_limits_return_unavailable(self):
        for kwargs in ({'max_bases': 0}, {'max_steps': 0}):
            result = program.produce(ProgramEvidence(), ProgramQuery(), **kwargs)
            self.assertEqual(result.status, 'unavailable')
            self.assertIsNone(result.proof)

    def test_invalid_program_or_risk_inputs_are_rejected(self):
        for evidence in (ProgramEvidence(error_cap=Q(1, 2)), ProgramEvidence(second_cap=0),
                         ProgramEvidence(foreign_zero=1)):
            with self.assertRaises(InputError):
                program.produce(evidence, ProgramQuery())
        for query in (ProgramQuery(alpha=Q(1, 2)), ProgramQuery('risk_vs_full', 1),
                      ProgramQuery('risk_vs_full', False)):
            with self.assertRaises(InputError):
                program.produce(ProgramEvidence(), query)
        with self.assertRaises(InputError):
            tail((Q(0), Q(1)), (Q(1, 2), Q(1, 3)), Q(0))
        with self.assertRaises(InputError):
            execute('adaptive', 2, 0)

    def test_partial_tail_atoms_are_not_discarded(self):
        self.assertEqual(tail((Q(0), Q(1)), (Q(3, 4), Q(1, 4)), Q(1, 2)), Q(1, 2))
        self.assertEqual(tail((Q(0), Q(1)), (Q(1), Q(0)), Q(99, 100)), 0)

    def test_derived_probability_masses_are_not_subject_to_input_bit_limit(self):
        evidence = ProgramEvidence(error_cap=Q(1, 2**256-189))
        query = ProgramQuery('risk_vs_full', Q(1, 3))
        result = program.produce(evidence, query)
        self.assertEqual(result.upper_bound, reference(evidence, query)[0])


if __name__ == '__main__':
    unittest.main()
