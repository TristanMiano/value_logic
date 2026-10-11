"""Source-bootstrap probe only: no fixture, query, worker or scoring call."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from datetime import datetime, timezone
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
PATH = REPO / "v3/experiments/frozen_v1/source/v3/experiments/p308_structural.py"
name = "p310_external_structural_bootstrap_probe"
spec = importlib.util.spec_from_file_location(name, PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[name] = module
spec.loader.exec_module(module)
before = {"M_is_none": module.M is None, "K_is_none": module.K is None}
assert all(before.values())
module._load_legacy()
after = {"M_initialized": module.M is not None, "K_initialized": module.K is not None,
         "kernel_entries_callable": {name: callable(getattr(module.K, name, None)) for name in
           ("paired_request", "Search", "interval", "Equation", "structural", "route_replacement")}}
assert after["M_initialized"] and after["K_initialized"] and all(after["kernel_entries_callable"].values())
old_M, old_K = module.M, module.K
module._load_legacy()
assert module.M is old_M and module.K is old_K
record = {"schema": "value_logic.p310.structural_bootstrap_source_probe.v1", "status": "PASS",
          "contributor": "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction",
          "utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
          "before": before, "after": after, "second_initialization_preserves_modules": True,
          "structural_source_sha256": hashlib.sha256(PATH.read_bytes()).hexdigest(),
          "probe_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          "fixture_materializations": 0, "paid_worker_calls": 0, "private_score_calls": 0,
          "final_input_reads": 0, "final_result_reads": 0, "principal_clock_credit_seconds": 0,
          "scope": "Cold module import and explicit dependency bootstrap only; no claim that a final unit completed."}
with (HERE / "bootstrap_probe_result.json").open("x") as f:
    json.dump(record, f, indent=2, sort_keys=True)
    f.write("\n")
print(json.dumps({"status": record["status"], "before": before, "after": after}))
