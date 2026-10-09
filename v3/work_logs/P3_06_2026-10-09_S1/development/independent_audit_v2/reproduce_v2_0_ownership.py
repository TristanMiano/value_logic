"""Preserve two reproduced defects of the superseded integrated v2.0 source.

The current source is already amended separately. This file records failures
of the exact retained revision rather than treating them as current behavior.
Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation reviewer.
"""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
here = Path(__file__).resolve().parent
source = here.parent / 'core_revisions/scalar_v2_0.py'
target = here / 'v2_0_ownership_findings.json'
if target.exists():
    raise SystemExit('Refusing to overwrite an existing finding.')
expected = 'fafa3a07a3549f4c1faddcd5396bc50c38d7ed6fe2ff7a24727ecb4c0b3af5ef'
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
spec = importlib.util.spec_from_file_location('old_integrated_v2_0', source)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
start = time.monotonic_ns()
start_utc = datetime.now(timezone.utc).isoformat()
pool = module.DelayedPool(('zero', 'one'))
pool.issue('query', {'zero': 0, 'one': 1})
before = pool.audit()
pool.copies[0].reveal('query', 0, scope=pool.settings.scope)
after = pool.audit()
assert after['settled'] + after['pending'] == 2 and len(pool.used) == 1
precision = []
for bits in (-1, True, 1.5):
    report = module.DelayedPool(('zero', 'one')).audit(sqrt_bits=bits)
    precision.append({'supplied': bits, 'returned': report['sqrt_enclosure_bits'], 'rejected': False})
result = {'status': 'REPRODUCED_SUPERSEDED_DEFECTS',
          'public_copy_settlement': {'before': before, 'after': after, 'issued_query_count': len(pool.used)},
          'empty_pool_precision': precision,
          'start_utc': start_utc, 'end_utc': datetime.now(timezone.utc).isoformat(),
          'execution_ns': time.monotonic_ns() - start,
          'source_sha256': expected,
          'repro_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'disposition': 'The principal preserved v2.0 and amended production to v2.1 before this rerun.',
          'contributor': 'ChatGPT (GPT-6 Astra Pro), independent implementation reviewer',
          'research_time_credit_ns': 0}
target.write_text(json.dumps(result, indent=2, default=str) + '\n')
print(json.dumps({'status': result['status'], 'result': str(target)}))
