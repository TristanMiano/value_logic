from pathlib import Path
import hashlib
import json
root = Path(__file__).resolve().parent / "ds01"
obj = json.loads((root / "hash_failure05.object.json").read_text(encoding="utf-8"))
claim = obj.pop("id")
expected = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
actual = (root / "hash_failure05.canonical.txt").read_bytes()
print("claim", claim)
print("canonical equal", actual == expected, "lengths", len(actual), len(expected))
print("actual", hashlib.sha256(actual).hexdigest())
print("expected", hashlib.sha256(expected).hexdigest())
if actual != expected:
    for i, (a, b) in enumerate(zip(actual, expected)):
        if a != b:
            print("first difference", i, repr(actual[max(0,i-80):i+80]), repr(expected[max(0,i-80):i+80]))
            break
