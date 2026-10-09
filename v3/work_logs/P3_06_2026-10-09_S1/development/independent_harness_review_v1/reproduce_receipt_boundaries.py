"""Preserve receipt-boundary failures in the frozen pre-repair harness.

These are accepted-type/integrity defects; they do not claim that a wrong
integer answer was accepted or that the valid saved runs contain false labels.
Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation reviewer.
"""
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
here = Path(__file__).resolve().parent
source = here / 'source_snapshot/06_mathematical_forecast_development.py'
target = here / 'receipt_boundary_failures.json'
if target.exists():
    raise SystemExit('Refusing to overwrite an existing negative record.')
expected_hash = 'c4dcb0ffafc74e888f434af8009bec19a6632a240461b5bb3cfd341634473e04'
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected_hash
spec = importlib.util.spec_from_file_location('receipt_boundary_snapshot', source)
harness = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = harness
spec.loader.exec_module(harness)
start_utc = datetime.now(timezone.utc).isoformat()
start = time.monotonic_ns()


def setup(identity):
    evidence = harness.Evidence()
    query = harness.Query(identity, 2, 3, 5, 3)
    evidence.register(query, 1)
    core = harness.CORE.Forecaster(harness.EXPERTS, scope=harness.SCOPE)
    core.issue(identity, {name: F(1, 2) for name in harness.EXPERTS})
    evidence.event('all_reports_committed', query_id=identity, tick=1,
                   reports_sha256=harness.sha(core.pending))
    receipt = evidence.prepare(query, 1)
    return evidence, query, core, receipt


aliases = []
for alias in (True, F(1), 1.0):
    evidence, query, core, original = setup('alias-' + type(alias).__name__)
    changed = replace(original, answer=alias)
    before = evidence.cache_fingerprint()
    evidence.admit(changed, 1)
    rejected_by_core = None
    try:
        core.reveal(query.query_id, changed.answer, scope=harness.SCOPE)
    except Exception as exc:
        rejected_by_core = {'type': type(exc).__name__, 'message': str(exc)}
    assert original == changed and original.digest != changed.digest
    assert query.query_id in evidence.admitted and core.pending is not None and rejected_by_core
    aliases.append({'alias_type': type(alias).__name__, 'dataclass_equal': original == changed,
                    'canonical_digests_equal': original.digest == changed.digest,
                    'evidence_cache_changed': evidence.cache_fingerprint() != before,
                    'evidence_admitted': True, 'core_still_pending': True,
                    'core_rejection': rejected_by_core})

evidence, query, core, receipt = setup('mutable-counter')
old_digest = receipt.digest
receipt.producer_counts['modular_multiplies'] = -123
evidence.admit(receipt, 1)
mutable_counts = {'digest_changed_after_return': receipt.digest != old_digest,
                   'modified_receipt_count': receipt.producer_counts['modular_multiplies'],
                   'actual_metered_count': evidence.counts['producer_modular_multiplies'],
                   'modified_record_admitted': query.query_id in evidence.admitted}
assert mutable_counts['digest_changed_after_return'] and mutable_counts['modified_record_admitted']

# Keep the successful mathematical-field rejection next to the narrower failures.
evidence, query, core, receipt = setup('wrong-answer-control')
before = evidence.cache_fingerprint()
wrong_integer_rejected = False
try:
    evidence.admit(replace(receipt, answer=0), 1)
except ValueError:
    wrong_integer_rejected = True
assert wrong_integer_rejected and evidence.cache_fingerprint() == before and core.pending is not None

result = {'schema': 'value_logic.p306.independent_receipt_boundaries.v1',
          'status': 'REPRODUCED_PRE_REPAIR_DEFECTS', 'source_sha256': expected_hash,
          'numeric_answer_aliases': aliases, 'mutable_counter_alias': mutable_counts,
          'wrong_integer_answer_control': {'rejected': True, 'cache_unchanged': True, 'core_pending_preserved': True},
          'start_utc': start_utc, 'end_utc': datetime.now(timezone.utc).isoformat(),
          'execution_ns': time.monotonic_ns() - start,
          'review_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'contributor': 'ChatGPT (GPT-6 Astra Pro), independent implementation reviewer',
          'research_time_credit_ns': 0,
          'scope': 'Local receipt type/integrity boundary only; no external certificate authentication claim.'}
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'result': str(target)}))
