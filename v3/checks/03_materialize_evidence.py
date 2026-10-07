"""Materialize exact P3-03 development traces stored as lossless gzip.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-07. Storage utility only.
Existing materialized files are checked, never overwritten.
"""
import gzip
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
record = root / "v3/work_logs/P3_03_2026-10-07_S1/development/artifact_storage.json"
for item in json.loads(record.read_text())["artifacts"]:
    source, target = root / item["stored_path"], root / item["logical_path"]
    packed = source.read_bytes()
    assert len(packed) == item["stored_bytes"]
    assert hashlib.sha256(packed).hexdigest() == item["stored_sha256"]
    raw = gzip.decompress(packed)
    assert len(raw) == item["uncompressed_bytes"]
    assert hashlib.sha256(raw).hexdigest() == item["uncompressed_sha256"]
    if target.exists():
        assert target.read_bytes() == raw, f"Existing file differs: {target}"
    else:
        with target.open("xb") as output:
            output.write(raw)
    print(f"Verified {item['logical_path']} ({len(raw)} bytes)")
