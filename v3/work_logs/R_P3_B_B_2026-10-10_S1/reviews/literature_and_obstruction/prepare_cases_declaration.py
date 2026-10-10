#!/usr/bin/env python3
"""Preparation only: serialize declared cases without running truth or policies."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).with_name('cases_v1')
OUT.mkdir(exist_ok=False)
SOURCE = ROOT / 'v3/checks/05_certificate_delivery_cases.py'
NAME = '_rp3bb_fixed_cases'
spec = importlib.util.spec_from_file_location(NAME, SOURCE)
module = importlib.util.module_from_spec(spec)
sys.modules[NAME] = module
try:
    spec.loader.exec_module(module)
    declared = module.declaration()
    if declared['stream_count'] != 4 or declared['current_case_count'] != 24 or declared['old_case_count'] != 5:
        raise AssertionError('Prospective fixture cardinality mismatch.')
    if sys.modules['_p305_inherited_p304'] is not module.K or sys.modules['_p305_portfolio_base'] is not module.M:
        raise AssertionError('Shared inherited module identity mismatch.')
    encoded = json.dumps(declared, sort_keys=True, indent=2, allow_nan=False) + '\n'
    (OUT / 'fixture_declaration.json').write_text(encoded)
    closure = OUT / 'source'
    closure.mkdir()
    bindings = []
    for relative in (
        'v3/checks/04_counterfactual_repair.py',
        'v3/checks/05_counterfactual_transport.py',
        'v3/checks/05_certificate_delivery_cases.py',
        str(Path(__file__).resolve().relative_to(ROOT)),
    ):
        raw = (ROOT / relative).read_bytes()
        target = closure / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        bindings.append({'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'captured_path': str(target.relative_to(ROOT))})
    record = {
        'stage': 'DEVELOPMENT', 'task': 'R-P3-B-B',
        'role': 'same-model nonblind integration reviewer and fixture author',
        'base_commit': '33c6d6795aac894bd3cf8575e44f1d6f38f6ae56',
        'principal_research_minutes_credited': 0,
        'action': 'Construct and serialize exact prospectively fixed inputs only.',
        'scientific_executions': [], 'scalar_reference_executed': False,
        'producer_executed': False, 'receiver_executed': False,
        'policy_or_benchmark_executed': False,
        'cardinality': {'streams': 4, 'current_requests': 24, 'old_requests': 5},
        'shared_inherited_module_identity': 'PASS',
        'declaration': {'path': str((OUT / 'fixture_declaration.json').relative_to(ROOT)), 'bytes': len(encoded.encode()), 'sha256': hashlib.sha256(encoded.encode()).hexdigest()},
        'source_closure': bindings,
        'capture_scope': 'Fixture preparation closure only; this is not the later producer/receiver/runner all-pay source closure.',
    }
    (OUT / 'preparation_binding.json').write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
    print(json.dumps(record, sort_keys=True))
except Exception as exc:
    (OUT / 'preparation_failure.json').write_text(json.dumps({'type': type(exc).__name__, 'detail': str(exc), 'policy_or_benchmark_executed': False}, sort_keys=True, indent=2) + '\n')
    raise
