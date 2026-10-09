"""Resolve two literal-location failures without rerunning scientific checks.

The original check_contract.py, manifest.json and check_results.json remain
unchanged. Only two already recorded historical binding scopes are resolved.
No historical bytes or hashes are overwritten; no principal time is credited.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    initial_path = OUT / "check_results.json"
    initial = json.loads(initial_path.read_text())
    expected_failures = {
        ("p303_receipt_repair_exact_file", "v3/work_logs/P3_03_2026-10-07_S1/development/receipt_identity_repair/plan.md"),
        ("p306_saved_hash_claim", "v3/time_ledger.csv_sha256"),
    }
    observed = {(r["check"], r.get("path", r.get("field"))) for r in initial["failures"]}
    checks = [{"check": "only_two_declared_historical_location_failures", "pass": observed == expected_failures}]
    plan_path = ROOT / "v3/work_logs/P3_03_2026-10-07_S1/development/receipt_identity_repair/plan.md"
    receipt_path = ROOT / "v3/work_logs/P3_03_2026-10-07_S1/rendering/final_math_repair.json"
    receipt = json.loads(receipt_path.read_text())
    row = next(r for r in receipt["changed_files"] if r["path"] == str(plan_path.relative_to(ROOT)))
    current = plan_path.read_bytes()
    protected_span = b"$`i\\ne j`$"
    historical = current.replace(protected_span, b"$i\\ne j$")
    checks.append({"check": "p303_exact_documented_notation_before_and_after", "pass": current.count(protected_span) == 1 and sha(current) == row["after_sha256"] and sha(historical) == row["before_sha256"],
                   "before_sha256": sha(historical), "after_sha256": sha(current),
                   "operation": "In memory only: remove code-protection backticks from the single i-not-equal-j inline expression.",
                   "receipt": str(receipt_path.relative_to(ROOT)), "receipt_sha256": sha(receipt_path.read_bytes())})
    base_path = ROOT / "v3/work_logs/P3_06_2026-10-09_S1/accounting_base.json"
    base = json.loads(base_path.read_text())
    ledger = (ROOT / "v3/time_ledger.csv").read_bytes()
    prefix = ledger[:base["v3_ledger_bytes"]]
    git_prefix = subprocess.check_output(["git", "show", base["base_commit"] + ":v3/time_ledger.csv"], cwd=ROOT)
    checks.append({"check": "p306_historical_ledger_is_exact_preserved_prefix", "pass": sha(prefix) == base["v3_ledger_sha256"] and prefix == git_prefix,
                   "base_commit": base["base_commit"], "prefix_bytes": len(prefix), "prefix_sha256": sha(prefix),
                   "current_ledger_bytes": len(ledger), "accounting_base_sha256": sha(base_path.read_bytes()),
                   "interpretation": "The recovery inventory bound the ledger at P3-06 entry; later authorized append bytes do not change that historical prefix."})
    changed = subprocess.check_output(["git", "diff", "--name-only", "c7e2967d18475bda54a327864601c245c8a29062", "--"], cwd=ROOT, text=True).splitlines()
    changed_protected = [p for p in changed if p.startswith(("v2/", "v3/checks/", "v3/derivations/", "v3/literature/", "v3/work_logs/P3_0"))]
    checks.append({"check": "all_prior_protected_scientific_bytes_unchanged", "pass": not changed_protected, "changed_protected": changed_protected})
    result = {"schema": "value_logic.p3b.implementation_historical_binding_disposition.v1",
              "status": "PASS" if all(r["pass"] for r in checks) else "BLOCKED",
              "scope": "P3-B local implementation/source-evidence readiness after explicit disposition of historical locations.",
              "utc": datetime.now(timezone.utc).isoformat(), "principal_research_credit_ns": 0,
              "initial_result": "check_results.json", "initial_result_sha256": sha(initial_path.read_bytes()),
              "initial_passed_checks": len(initial["checks"]) - len(initial["failures"]),
              "initial_literal_location_failures_retained": initial["failures"],
              "checks": checks, "script_sha256": sha(Path(__file__).read_bytes()),
              "scientific_runs_repeated": False, "historical_bytes_or_hashes_modified": False,
              "missing_end_to_end_integration": "The bounded modules and separate declared bridges are ready to inform P3-08; a single integrated cross-task paid reasoner has not been implemented or validated."}
    with (OUT / "final_check_result.json").open("x") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
