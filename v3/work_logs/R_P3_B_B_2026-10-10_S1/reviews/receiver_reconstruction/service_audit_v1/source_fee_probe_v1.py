#!/usr/bin/env python3
"""One source-enrollment-stage diagnostic; no Session deliver or policy run.

The prospective question is whether a saved service revision can finish all
source reads/hashes and then deny their postpaid byte bill. Its account is fixed
at reserve + twice the declared source bytes - one. No source is modified.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source'
OUT = HERE / 'source_fee_run_v1'
OUT.mkdir(exist_ok=False)
spec = importlib.util.spec_from_file_location('_rp3bb_source_fee_probe',
    SOURCE / 'v3/checks/05_certificate_delivery_service.py')
S = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = S
spec.loader.exec_module(S)
expected = S.A.make_source_record(S.SOURCE_PATHS, repo_root=SOURCE)
source_bytes = sum(item['bytes'] for item in json.loads(expected)['sources'])
account = S.FAILURE_RESERVE + 2 * source_bytes - 1
owner = S.Session('O-ENUM-RECEIVER', 'fresh', 'source-fee-only', 1, (0,), (), expected)
meter = S.Meter(account)
try:
    meter.run('coordination', lambda: owner._enroll(meter))
except S.ResourceExhausted as error:
    failure_category = error.category
    output = meter.fail(error)
else:
    raise AssertionError('Expected source-byte postpayment denial.')
invoice = meter.invoice()
assert failure_category in ('source_program_bytes', 'source_hash_input_bytes')
# Both charges occur only after make_source_record has returned: all source
# bytes have already been read and hashed in the captured implementation.
charged_hash_bytes = invoice['by_stage'].get('common_source', {}).get('source_hash_input_bytes', 0)
assert charged_hash_bytes == 0 and not owner.source_enrolled
assert invoice['total_units'] <= account and output == S.FAILURE_PAYLOAD
result = {
    'schema': 'rp3bb.source-fee-diagnostic.v1', 'stage': 'DEVELOPMENT',
    'status': 'EXPECTED_DEFECT_REPRODUCED',
    'service_sha256': hashlib.sha256((SOURCE / 'v3/checks/05_certificate_delivery_service.py').read_bytes()).hexdigest(),
    'diagnostic_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'declared_source_bytes': source_bytes, 'all_source_reads_and_hashes_completed_before_denied_charge': True,
    'completion_evidence': 'The denied source-byte charge follows the successful make_source_record return in the captured source.',
    'charged_hash_input_bytes': charged_hash_bytes, 'denied_category': failure_category,
    'source_enrolled': owner.source_enrolled, 'invoice': invoice,
    'session_deliveries': 0, 'policy_runs': 0, 'principal_clock_credit_seconds': 0,
}
raw = (json.dumps(result, indent=2) + '\n').encode()
(OUT / 'results.json').write_bytes(raw)
print(json.dumps({'status': result['status'], 'declared_source_bytes': source_bytes,
                  'denied_category': failure_category, 'charged_hash_input_bytes': charged_hash_bytes,
                  'results_sha256': hashlib.sha256(raw).hexdigest()}, indent=2))
