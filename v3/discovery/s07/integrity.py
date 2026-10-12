#!/usr/bin/env python3
"""Verify the s07 handoff byte inventory; no source acquisitions or proof claim."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def main():
    manifest = json.loads((HERE/'manifest.json').read_text())
    count = size = 0
    for item in manifest['files']+manifest['prior_source_files']:
        path = REPO/item['path']
        if not path.resolve().is_relative_to(REPO):
            raise ValueError('Inventory path outside the repository')
        data = path.read_bytes()
        if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('Changed or missing bound bytes: '+item['path'])
        count += 1
        size += len(data)
    print(json.dumps(dict(status='verified',files=count,bytes=size,
        actual_new_acquisitions=0,research_credit_ns=0,
        scope='Byte identities only. The independent raw-proof and trace checks are separately recorded.')))


if __name__ == '__main__':
    main()
