"""Versioned administrative entry point; ChatGPT (GPT-6 Astra Pro), 2026-10-07.

The accounting-bound original verifier omitted its TASK global in close mode.
Preserve those original bytes and every check; supply exactly that missing
binding from the same accounting module. No scientific run or time credit.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / 'verify_close.py'
EXPECTED_ORIGINAL = 'ce584fb92075a653b392f06e9232df241b2f8beaa5bd98485f355688c52aac22'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', nargs='?', default='close', choices=('preview', 'close'))
    args = parser.parse_args()
    entry = Path(__file__).resolve()
    entry_hash = hashlib.sha256(entry.read_bytes()).hexdigest()
    original_hash = hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()
    if original_hash != EXPECTED_ORIGINAL:
        raise ValueError('Original accounting-bound verifier bytes changed')
    spec = importlib.util.spec_from_file_location('p302_preserved_close', ORIGINAL)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    if hasattr(checker, 'TASK') or checker.accounting.TASK != 'P3-02':
        raise ValueError('Correction precondition changed')
    checker.TASK = checker.accounting.TASK
    report = checker.verify(args.mode)
    report['original_verifier_command_template'] = report['command']
    report['command'] = [sys.executable, checker.relative(entry), args.mode]
    report['versioned_entry_point'] = {
        'path': checker.relative(entry), 'sha256': entry_hash,
        'original_path': checker.relative(ORIGINAL), 'original_sha256': original_hash,
        'correction': 'Supply the omitted TASK global from accounting.TASK; no check removed or weakened.',
    }
    stable = hashlib.sha256(entry.read_bytes()).hexdigest() == entry_hash
    report['snapshot_hashes'][checker.relative(entry)] = entry_hash
    report['checks']['versioned_entry_point_stable'] = stable
    report['status'] = ('PASS' if args.mode == 'close' else 'SNAPSHOT_VALID') if all(report['checks'].values()) else 'FAIL'
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if all(report['checks'].values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
