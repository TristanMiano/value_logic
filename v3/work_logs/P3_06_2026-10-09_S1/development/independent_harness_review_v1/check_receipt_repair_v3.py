"""Independent no-mutation recheck of the v3 receipt-boundary repair.

Valid saved results are compared separately from adversarial representation
tests. No authentication or global multi-consumer transaction is claimed.
Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation reviewer.
"""
from dataclasses import replace
from datetime import datetime, timezone
from decimal import localcontext
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
import traceback
from types import SimpleNamespace

sys.dont_write_bytecode = True


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(h, here):
    evidence = h.Evidence()
    query = h.Query('checked-representation', 2, 3, 5, 3)
    evidence.register(query, 1)
    pools = [h.CORE.DelayedPool(h.EXPERTS, scope=h.SCOPE, decision_features=mode)
             for mode in (False, True)]
    reports = [pool.issue(query.query_id, {name: F(1, 2) for name in h.EXPERTS},
                         actions=h.CORE.ActionTable(((0, 1), (1, 0)), F(1, 4)) if pool.settings.decision_features else None)
               for pool in pools]
    evidence.event('all_reports_committed', query_id=query.query_id, tick=1, reports_sha256=h.sha(reports))
    receipt = evidence.prepare(query, 1)

    def fingerprint():
        return h.sha({'evidence': evidence.full_fingerprint(),
                      'cores': [pool.audit() for pool in pools], 'reports': reports})

    changed_integer_counts = tuple((key, value + (key == 'modular_multiplies'))
                                    for key, value in receipt.producer_counts)
    candidates = [
        ('boolean_answer', replace(receipt, answer=True)),
        ('fraction_answer', replace(receipt, answer=F(1))),
        ('float_answer', replace(receipt, answer=1.0)),
        ('wrong_integer_answer', replace(receipt, answer=0)),
        ('boolean_residue', replace(receipt, residue=True)),
        ('fraction_residue', replace(receipt, residue=F(3))),
        ('float_residue', replace(receipt, residue=3.0)),
        ('wrong_consistent_integer_residue', replace(receipt, residue=4, answer=0)),
        ('wrong_scope', replace(receipt, scope=h.SCOPE + ':other')),
        ('unknown_query', replace(receipt, query_id='unregistered')),
        ('mutable_claim_key', replace(receipt, claim_key=list(receipt.claim_key))),
        ('claim_numeric_alias', replace(receipt, claim_key=(h.SCOPE, F(2), 3, 5, 3))),
        ('event_boolean_alias', replace(receipt, issued_event=False)),
        ('event_fraction_alias', replace(receipt, produced_event=F(receipt.produced_event))),
        ('event_float_alias', replace(receipt, checked_event=float(receipt.checked_event))),
        ('crosscheck_integer_alias', replace(receipt, python_pow_crosscheck=1)),
        ('mutable_counter_dict', replace(receipt, producer_counts=dict(receipt.producer_counts))),
        ('mutable_counter_list', replace(receipt, checker_counts=list(receipt.checker_counts))),
        ('counter_numeric_alias', replace(receipt, producer_counts=tuple((key, F(value))
                                                                        for key, value in receipt.producer_counts))),
        ('valid_integer_counter_digest_change', replace(receipt, producer_counts=changed_integer_counts)),
        ('foreign_record_type', SimpleNamespace(query_id=receipt.query_id)),
    ]
    outcomes = []
    for label, candidate in candidates:
        before = fingerprint()
        error = None
        try:
            evidence.admit(candidate, 1)
        except ValueError as exc:
            error = str(exc)
        assert error is not None and fingerprint() == before, label
        outcomes.append({'case': label, 'rejected': True, 'full_evidence_and_cores_unchanged': True, 'reason': error})
    for tick in (True, F(1), 1.0, 0, -1):
        before = fingerprint()
        rejected = False
        try:
            evidence.admit(receipt, tick)
        except ValueError:
            rejected = True
        assert rejected and fingerprint() == before
        outcomes.append({'case': 'invalid_tick_' + repr(tick), 'rejected': True,
                         'full_evidence_and_cores_unchanged': True})
    before = fingerprint()
    original_digest = receipt.digest
    immutable = False
    try:
        receipt.producer_counts[0] = ('loop_iterations', -123)
    except TypeError:
        immutable = True
    assert immutable and receipt.digest == original_digest and fingerprint() == before

    # An equal canonical reconstruction remains acceptable; object identity is
    # not accidentally required in place of registered canonical content.
    reconstructed = replace(receipt)
    assert reconstructed is not receipt and reconstructed.digest == receipt.digest
    evidence.admit(reconstructed, 1)
    for pool in pools:
        pool.reveal(query.query_id, reconstructed.answer, scope=h.SCOPE)
    assert query.query_id in evidence.admitted and all(pool.audit()['settled'] == 1 and not pool.pending for pool in pools)
    after_valid = fingerprint()
    duplicate_rejected = False
    try:
        evidence.admit(reconstructed, 1)
    except ValueError:
        duplicate_rejected = True
    assert duplicate_rejected and fingerprint() == after_valid
    cached_true = evidence.lookup(replace(query, query_id='cached-true'))
    cached_false = evidence.lookup(replace(query, query_id='cached-false', r=4))
    assert cached_true == (1, receipt.digest) and cached_false == (0, receipt.digest)

    chronology_module = load('reused_saved_chronology_checker', here / 'audit_saved_chronology.py')
    with localcontext() as context:
        context.prec = 80
        chronology = chronology_module.run(here.parent / 'mathematical_queries_v3')
    cases = []
    for name in ('recurring_shortcuts', 'balanced_nonshortcut_null', 'delayed_pending_tail', 'varying_stakes_actions'):
        original = json.loads((here.parent / 'mathematical_queries_v1' / (name + '.json')).read_text())
        repaired = json.loads((here.parent / 'mathematical_queries_v3' / (name + '.json')).read_text())
        assert original['metrics'] == repaired['metrics']
        assert original['pending_ids'] == repaired['pending_ids']
        for old, new in zip(original['records'], repaired['records']):
            for field in ('query', 'tick', 'scheduled_admission_tick', 'weight', 'actions', 'experts', 'outcome', 'status'):
                assert old[field] == new[field], (name, field)
            for method in old['reports']:
                for field in ('probability', 'action_one_probability', 'forecast_action_costs', 'hard_action', 'route'):
                    assert old['reports'][method][field] == new['reports'][method][field], (name, method, field)
        cases.append({'case': name, 'population_and_forecasts_unchanged': True, 'all_metrics_unchanged': True,
                      'receipt_representation_and_digests_versioned': True})
    return {'status': 'PASS', 'rejected_candidates': outcomes,
            'immutable_counter_check': True, 'canonical_reconstruction_accepted': True,
            'correct_admission_after_rejections': True, 'duplicate_rejected_without_mutation': True,
            'cached_same_scope_residue_entailment': True,
            'new_saved_tape_chronology': chronology, 'original_to_repaired_population_comparison': cases}


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    source = here / 'source_snapshot_v3/06_mathematical_forecast_development.py'
    expected = '7e19e1e0930cbcdea3637af16c1ade4e1f2099b615a3600821196c2c8c5cecd4'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
    target = here / 'receipt_repair_v3_result.json'
    if target.exists():
        raise SystemExit('Refusing to overwrite a receipt-repair result.')
    h = load('repaired_receipt_harness_snapshot', source)
    start_utc = datetime.now(timezone.utc).isoformat()
    start = time.monotonic_ns()
    try:
        result = run(h, here)
    except Exception:
        result = {'status': 'FAIL', 'traceback': traceback.format_exc()}
    result.update({'schema': 'value_logic.p306.independent_receipt_repair.v1',
                   'start_utc': start_utc, 'end_utc': datetime.now(timezone.utc).isoformat(),
                   'execution_ns': time.monotonic_ns() - start,
                   'source_sha256': expected,
                   'review_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'chronology_checker_sha256': hashlib.sha256((here / 'audit_saved_chronology.py').read_bytes()).hexdigest(),
                   'contributor': 'ChatGPT (GPT-6 Astra Pro), independent implementation reviewer',
                   'research_time_credit_ns': 0,
                   'scope': 'Local receipt integrity and saved-tape validation; no arbitrary external certificate authentication.'})
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'rejections': len(result.get('rejected_candidates', [])),
                      'result': str(target)}))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
