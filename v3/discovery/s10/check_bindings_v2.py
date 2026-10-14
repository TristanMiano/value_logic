"""Independent saved-byte bindings; retain and report misnamed objects."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent / "ds01"
def digest(value):
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()
def binding(obj):
    body = dict(obj)
    claimed = body.pop("id")
    assert digest(body) == claimed, (claimed, digest(body))

objects = []
for path in sorted((root / "objects").glob("*.json")):
    raw = path.read_bytes()
    obj = json.loads(raw)
    binding(obj)
    actual = digest(obj)
    objects.append({"path": path.name, "canonical_sha256": actual,
                    "raw_sha256": hashlib.sha256(raw).hexdigest(),
                    "filename_matches": path.stem == actual})

receipts = 0
request_files = sorted(root.glob("*/*/requests.jsonl"))
for path in request_files:
    for line in path.read_text(encoding="utf-8").splitlines():
        request = json.loads(line)
        for receipt in request["receipts"]:
            binding(receipt)
            receipts += 1

report = {"status": "pass_object_and_receipt_bodies", "objects": objects,
          "request_files": len(request_files), "receipts": receipts,
          "filename_mismatches": sum(not row["filename_matches"] for row in objects),
          "disposition": "Preserve misnamed immutable bytes and all original references. Resolve by this manifest's exact path and verified body/raw digests; do not treat its filename as a valid content digest."}
(root / "bindings_manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
