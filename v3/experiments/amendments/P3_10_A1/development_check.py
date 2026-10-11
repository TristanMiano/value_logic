"""Source-only A1 startup and barrier checks; never invokes a final endpoint.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import importlib.util
import json
import tempfile
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
spec = importlib.util.spec_from_file_location('p310_a1_declared_driver', HERE / 'continue.py')
D = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = D
spec.loader.exec_module(D)
L, F = D.L, D.F
F.require_runtime_startup()
schedule = L.read_json(REPO / F.FROZEN / 'schedule.json')
loaded = F.adapters()
unit = next(u for u in schedule['units'] if u['arm'] == 'conformance' and u['engine'] == 'legacy_structural')
legacy = loaded['conformance']._load('v3/experiments/p308_structural.py')
assert legacy.M is None and legacy.K is None
D.bootstrap(loaded, unit)
assert legacy.M is not None and legacy.K is not None
identity = (id(legacy.M), id(legacy.K))
D.bootstrap(loaded, unit)
assert identity == (id(legacy.M), id(legacy.K))
paths = [r['path'] for r in L.read_json(REPO / F.FROZEN / 'manifest.json')['sources']]
paths += [(HERE / p).relative_to(REPO).as_posix() for p in ('continue.py', 'development_check.py')]
origins = F.validate_loaded_local_sources(paths)
checks = ['fresh structural module begins uninitialized', 'explicit bootstrap initializes M and K',
          'repeat prerequisite check is idempotent', 'expanded source closure admits only declared old/new sources']
# Empty composite must refuse before writing a barrier or accessing any payload.
with tempfile.TemporaryDirectory(prefix='p310-a1-source-check-') as scratch:
    saved_root = D.ROOT
    D.ROOT = Path(scratch)
    try:
        try:
            D.composite({}, {'units': [{'id': 'development-only-placeholder'}]}, [], [], create=True)
        except L.IntegrityError as exc:
            assert 'all 500' in str(exc)
        else:
            raise AssertionError('Incomplete composite accepted')
        assert not (D.ROOT / 'composite_public.json').exists()
    finally:
        D.ROOT = saved_root
checks.append('missing public denominator blocks composite publication before private work')
for value in ('../escape', '/absolute'):
    try:
        D.checked_path(value)
    except L.IntegrityError:
        pass
    else:
        raise AssertionError('Unsafe reference path accepted')
checks.append('noncanonical reference paths rejected')
print(json.dumps({'status': 'PASS', 'scope': 'source-only startup and barrier development checks',
                  'final_inputs_read': False, 'final_endpoints_called': False, 'final_payloads_read': False,
                  'checks': checks, 'loaded_local_source_origins': origins,
                  'driver_sha256': L.sha256_file(HERE / 'continue.py'),
                  'check_sha256': L.sha256_file(Path(__file__)), 'observed_utc': L.utc_now()}, indent=2))
