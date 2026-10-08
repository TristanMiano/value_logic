#!/usr/bin/env python3
"""Read-only P3-05 evidence binding check, not a mathematical or execution verifier.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-08.
Python 3.10+, standard library. Does not modify archives or append time.
"""
from pathlib import Path
import argparse
import hashlib
import json

SESSION = 'v3/work_logs/P3_05_2026-10-08_S2'

def verify(root: Path) -> dict:
    dev = root / SESSION / 'development'
    index = json.loads((dev/'evidence_index.json').read_bytes())
    if set(index['runs']) != {'attempt_1','extension_1','substitution_1','v2_regression_1','v2_extension_1'}:
        raise ValueError('Unexpected saved run set.')
    summaries = {}
    for name, entry in index['runs'].items():
        folder = dev/name
        for file, digest in entry['files'].items():
            if Path(file).name != file or '/' in file or '\\' in file:
                raise ValueError('Unsafe archived file path.')
            if hashlib.sha256((folder/file).read_bytes()).hexdigest() != digest:
                raise ValueError(f'Saved evidence changed: {name}/{file}')
        manifest=json.loads((folder/'manifest.json').read_bytes())
        summary=json.loads((folder/'summary.json').read_bytes())
        json.loads((folder/'results.json').read_bytes())
        if summary['status']!='PASS' or summary['error'] is not None or summary['assertions']!=entry['expected_assertions']:
            raise ValueError(f'Unexpected summary: {name}')
        if manifest['sources_sha256']!=summary['sources_sha256']:
            raise ValueError(f'Preparation/source mismatch: {name}')
        for file,digest in manifest['sources_sha256'].items():
            if entry['files'].get(file)!=digest:
                raise ValueError(f'Source snapshot mismatch: {name}/{file}')
            if name in index['current_runs']:
                live=root/'v3/checks'/file
                # The installer separately pins the inherited P3-04 dependency.
                if not live.exists() and file=='04_counterfactual_repair.py':
                    continue
                if hashlib.sha256(live.read_bytes()).hexdigest()!=digest:
                    raise ValueError(f'Current code differs from selected evidence: {file}')
        summaries[name]=summary['assertions']
    return {'status':'PASS','saved_bundles':len(summaries),'assertions_by_bundle':summaries,
            'scope':'Checksums and recorded bindings only; not a fresh scientific run.',
            'historical_lost_attempt_recovered':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
    args=parser.parse_args()
    print(json.dumps(verify(args.repo),indent=2))
