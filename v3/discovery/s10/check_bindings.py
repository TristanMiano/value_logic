"""Independent JSON object binding check; read only, no scientific acquisitions."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent / "ds01"
for path in sorted((root / "objects").glob("*.json")):
    raw = path.read_bytes()
    obj = json.loads(raw)
    def digest(value):
        canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert digest(obj) + ".json" == path.name, path
    claimed = obj.pop("id")
    assert digest(obj) == claimed, path
    print(path.name, hashlib.sha256(raw).hexdigest(), "PASS")
