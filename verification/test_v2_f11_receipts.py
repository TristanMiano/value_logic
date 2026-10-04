"""Saved-receipt integration and hostile transport boundaries."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.verification.model import Evidence, Query
from v2.verification.producer import Limits, produce
from v2.verification import receipts as W


class F11ReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = Evidence(Q(0), Q(0), Q(0), Q(0), 'receipt-example')
        cls.query = Query('T1')
        cls.outcome = produce(cls.evidence, cls.query)
        cls.receipt = W.make_receipt(cls.evidence, cls.query, cls.outcome)

    def test_roundtrip_and_independent_current_request(self):
        payload = W.loads(json.dumps(self.receipt))
        root = W.receive_receipt(self.evidence, self.query, payload)
        self.assertEqual(root.budget, Q(-3, 32))
        evidence, query = W.parse_request(W.loads(json.dumps(W.request_payload(self.evidence, self.query))))
        self.assertEqual((evidence, query), (self.evidence, self.query))

    def test_receipt_can_meet_a_weaker_request_without_relabeling_its_bound(self):
        root = W.receive_receipt(self.evidence, Query('T1', Q(2)), self.receipt)
        self.assertEqual(root.budget, Q(-3, 32))
        with self.assertRaises(A.AuditError):
            W.receive_receipt(self.evidence, Query('T1', Q(-1)), self.receipt)

    def test_derived_bound_can_exceed_the_individual_input_bit_limit(self):
        evidence = Evidence(beta=Q(1, 2**251-1), gamma=Q(1, 2**249-1))
        outcome = produce(evidence, self.query)
        self.assertGreater(outcome.upper_bound.denominator.bit_length(), 256)
        payload = W.make_receipt(evidence, self.query, outcome)
        root = W.receive_receipt(evidence, self.query, payload)
        self.assertEqual(root.budget, outcome.upper_bound)

    def test_action_annotation_cannot_replace_current_request(self):
        with self.assertRaises(W.ReceiptError):
            W.receive_receipt(self.evidence, Query('T2'), self.receipt)
        changed = deepcopy(self.receipt)
        changed['action'] = 'T2'
        with self.assertRaises(A.AuditError):
            W.receive_receipt(self.evidence, Query('T2'), changed)

    def test_unavailable_request_can_have_a_sound_but_insufficient_bound_receipt(self):
        evidence = Evidence()
        outcome = produce(evidence, self.query)
        receipt = W.make_receipt(evidence, self.query, outcome)
        with self.assertRaises(A.AuditError):
            W.receive_receipt(evidence, self.query, receipt)
        root = W.receive_receipt(evidence, Query('T1', outcome.upper_bound), receipt)
        self.assertEqual(root.budget, Q(471, 256))

    def test_no_proof_means_no_saved_receipt(self):
        with self.assertRaises(W.ReceiptError):
            W.make_receipt(self.evidence, self.query, produce(self.evidence, self.query, Limits(0)))

    def test_version_or_withdrawal_requires_new_receipt(self):
        for new in (replace(self.evidence, revision='changed'), Evidence()):
            with self.assertRaises(W.ReceiptError):
                W.receive_receipt(new, self.query, self.receipt)

    def test_forged_source_annotation_does_not_rebind_old_proof(self):
        new = Evidence()
        changed = deepcopy(self.receipt)
        changed['evidence'] = W.evidence_payload(new)
        with self.assertRaises(K.ProofError):
            W.receive_receipt(new, self.query, changed)

    def test_bound_annotation_must_match_checked_root(self):
        changed = deepcopy(self.receipt)
        changed['bound'] = '-1'
        with self.assertRaises(W.ReceiptError):
            W.receive_receipt(self.evidence, self.query, changed)

    def test_duplicate_unknown_and_numeric_json_fields_are_rejected(self):
        for text in ('{"x":1,"x":2}', '{"x":0.1}', '{"x":NaN}',
                     '{"x":Infinity}', '{"x":1e99999999}'):
            with self.assertRaises(W.ReceiptError):
                W.loads(text)
        changed = W.request_payload(self.evidence, self.query)
        changed['query']['extra'] = 'ignored?'
        with self.assertRaises(W.ReceiptError):
            W.parse_request(changed)

    def test_invalid_rational_spellings_never_reach_fraction_expansion(self):
        for value in ('1e99999999', '1/0', 'NaN', '0.0', True, 0, '9'*1251):
            changed = deepcopy(self.receipt)
            changed['bound'] = value
            with self.assertRaises(W.ReceiptError):
                W.receive_receipt(self.evidence, self.query, changed)

    def test_forward_term_reference_is_rejected_before_decode(self):
        changed = deepcopy(self.receipt)
        changed['proof']['terms'][0]['args'] = [0]
        with self.assertRaises(W.ReceiptError):
            W.receive_receipt(self.evidence, self.query, changed)

    def test_malformed_and_semantically_forged_receipts_have_explicit_rejections(self):
        mutations = []
        def mutated(label, change):
            payload = deepcopy(self.receipt)
            change(payload)
            mutations.append((label, payload))
        for value in (True, -1, 99999, None, '0', []):
            mutated(f'root-{value!r}', lambda p, value=value: p['proof'].__setitem__('root', value))
        for value in (True, 4, [], {}):
            mutated(f'case-{value!r}', lambda p, value=value: p['proof']['steps'][0].__setitem__('case', value))
        mutated('forward-parent', lambda p: p['proof']['steps'][1].__setitem__('parents', [1]))
        mutated('boolean-parent', lambda p: p['proof']['steps'][1].__setitem__('parents', [True]))
        mutated('wrong-term-arity', lambda p: p['proof']['terms'][0].__setitem__('args', [0, 0, 0]))
        mutated('unknown-native-rule', lambda p: p['proof']['steps'][0].__setitem__('rule', 'trust_me'))
        mutated('hidden-source-switch', lambda p: p['proof']['steps'][0].__setitem__('context_id', 'different'))
        mutated('missing-all-cases', lambda p: p['proof']['steps'][-1].__setitem__('parents', []))
        mutated('alter-both-budget-claims', lambda p: (
            p.__setitem__('bound', '-1'), p['proof']['steps'][-1].__setitem__('budget', '-1')))
        mutated('rational-exponent-in-term', lambda p: next(
            t for t in p['proof']['terms'] if t['value'] is not None).__setitem__('value', '1e99999999'))
        mutated('extra-envelope-field', lambda p: p.__setitem__('trusted', True))
        for label, payload in mutations:
            with self.subTest(label=label), self.assertRaises(ValueError):
                W.receive_receipt(self.evidence, self.query, payload)

    def test_deep_backward_term_chain_is_rejected(self):
        changed = deepcopy(self.receipt)
        terms = changed['proof']['terms']
        for _ in range(W.MAX_DEPTH + 1):
            terms.append({'op': 'scale', 'args': [len(terms)-1],
                          'name': '', 'unit': '', 'value': '1'})
        with self.assertRaises(W.ReceiptError):
            W.receive_receipt(self.evidence, self.query, changed)

    def test_byte_limit_and_utf8_are_checked(self):
        with self.assertRaises(W.ReceiptError):
            W.loads(' ' * (W.MAX_BYTES + 1))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            path.write_bytes(b'\xff')
            with self.assertRaises(W.ReceiptError):
                W.read(path)

    def test_compact_dag_expansion_is_rejected_before_native_decode(self):
        changed = deepcopy(self.receipt)
        terms = changed['proof']['terms']
        # A tiny wire table can describe an exponential tree, even when that
        # tree appears only in instruction data rather than a judgment pair.
        for _ in range(16):
            terms.append({'op': 'add', 'args': [len(terms)-1]*2,
                          'name': '', 'unit': '', 'value': None})
        changed['proof']['steps'][0]['data'] = {'tuple': [{'term': len(terms)-1}]}
        with patch.object(W.C, 'unpack_proof', side_effect=AssertionError('decoder reached')):
            with self.assertRaises(W.ReceiptError):
                W.receive_receipt(self.evidence, self.query, changed)

    def test_instruction_data_terms_share_the_occurrence_budget(self):
        changed = deepcopy(self.receipt)
        terms = changed['proof']['terms']
        terms.append({'op': 'num', 'args': [], 'name': '', 'unit': 'U', 'value': '0'})
        for _ in range(10):
            terms.append({'op': 'add', 'args': [len(terms)-1]*2,
                          'name': '', 'unit': '', 'value': None})
        # Each referenced tree is small enough alone; their aggregate is not.
        changed['proof']['steps'][0]['data'] = {'tuple': [{'term': len(terms)-1}]*10}
        with patch.object(W.C, 'unpack_proof', side_effect=AssertionError('decoder reached')):
            with self.assertRaises(W.ReceiptError):
                W.receive_receipt(self.evidence, self.query, changed)

    def test_cli_generate_check_and_reject_stale_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            request = Path(directory) / 'request.json'
            receipt = Path(directory) / 'receipt.json'
            request.write_text(json.dumps(W.request_payload(self.evidence, self.query)), encoding='utf-8')
            base = [sys.executable, '-X', 'faulthandler', '-m', 'v2.verification', '--request', str(request)]
            generated = subprocess.run(base + ['--receipt-out', str(receipt)], capture_output=True, text=True, timeout=30)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            self.assertTrue(json.loads(generated.stdout)['receipt_saved'])
            checked = subprocess.run(base + ['--check-receipt', str(receipt)], capture_output=True, text=True, timeout=30)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertEqual(json.loads(checked.stdout)['status'], 'ACCEPTED')
            request.write_text(json.dumps(W.request_payload(replace(self.evidence, revision='new'), self.query)), encoding='utf-8')
            rejected = subprocess.run(base + ['--check-receipt', str(receipt)], capture_output=True, text=True, timeout=30)
            self.assertEqual(rejected.returncode, 2, rejected.stderr)
            self.assertEqual(json.loads(rejected.stderr)['status'], 'REJECTED_INPUT_OR_RECEIPT')

    def test_cli_does_not_disguise_its_own_invalid_proof_as_bad_user_input(self):
        from v2.verification.__main__ import main
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'request.json'
            path.write_text(json.dumps(W.request_payload(self.evidence, self.query)), encoding='utf-8')
            with patch('sys.argv', ['v2.verification', '--request', str(path)]), \
                 patch('v2.verification.__main__.assess_with_proof', side_effect=K.ProofError('internal invalid proof')):
                with self.assertRaises(K.ProofError):
                    main()


if __name__ == '__main__':
    unittest.main()
