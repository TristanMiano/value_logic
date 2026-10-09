"""P3-B retained-evidence and narrow source-scope boundary check.

Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation reviewer.
No development suite or original experiment is rerun. The only new execution
uses one retained profile and three low-cost source/catalogue admission cases.
The question is whether incomplete admission can use an unvalidated policy,
or complete admission can accept a changed generator scope. Agent time gets
zero principal research credit. All outputs use exclusive creation.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
BASE = "c7e2967d18475bda54a327864601c245c8a29062"
P3 = ROOT / "v3"
W = P3 / "work_logs"
S3 = W / "P3_03_2026-10-07_S1"
S4 = W / "P3_04_2026-10-08_S2"
S5 = W / "P3_05_2026-10-08_S3"
S6 = W / "P3_06_2026-10-09_S1"
S7 = W / "P3_07_2026-10-09_S1"
INPUTS = {}
CHECKS = []
NOTES = []


def rel(path):
    path = Path(path)
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def sha(path):
    path = Path(path)
    raw = path.read_bytes()
    value = hashlib.sha256(raw).hexdigest()
    INPUTS.setdefault(rel(path), {"sha256": value, "bytes": len(raw)})
    return value


def read(path):
    sha(path)
    return json.loads(Path(path).read_text())


def write(name, value):
    with (OUT / name).open("x") as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write("\n")


def check(name, condition, **details):
    CHECKS.append({"check": name, "pass": bool(condition), **details})


def protected(path):
    return (path.startswith(("v2/", "v3/checks/", "v3/derivations/", "v3/literature/"))
            or path.startswith("v3/work_logs/P3_0"))


def git_state():
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    return {"changed_tracked_paths": changed,
            "changed_protected_paths": [p for p in changed if protected(p)]}


def bound_sources(directory, source_map, snapshot_subdir="", current=True):
    rows = []
    for name, expected in source_map.items():
        source = ROOT / name if name.startswith("v3/") else P3 / "checks" / name
        snapshot = directory / snapshot_subdir / Path(name).name
        row = {"source": rel(source), "snapshot": rel(snapshot), "expected_sha256": expected}
        row["snapshot_match"] = snapshot.exists() and sha(snapshot) == expected
        row["current_match"] = source.exists() and sha(source) == expected
        check("saved_source_binding", row["snapshot_match"] and (row["current_match"] or not current), **row)
        rows.append(row)
    return rows


def main():
    started = datetime.now(timezone.utc).isoformat()
    start_mono = time.monotonic_ns()
    base_state = git_state()
    current_sources = {}
    for p in sorted((P3 / "checks").glob("*.py")):
        if p.name[:2] in {"03", "04", "05", "06", "07"}:
            current_sources[rel(p)] = sha(p)
    write("manifest.json", {
        "schema": "value_logic.p3b.implementation_review.v1",
        "base_commit": BASE, "started_utc": started,
        "contributor": "ChatGPT (GPT-6 Astra Pro), independent same-model nonblind reviewer",
        "principal_research_credit_ns": 0,
        "stage": "GATE_REVIEW_ONLY_NO_FINAL_EVALUATION",
        "current_source_sha256": current_sources,
        "review_script_sha256": sha(Path(__file__)),
        "baseline": base_state,
        "targeted_question": "Current v3 selector rejects a changed generator scope when admission completes, and fixed fallback survives incomplete admission despite a reordered generic profile.",
        "execution_limit": "One saved 1024-row profile; three selector calls; no rollout, generator, solver, or development-suite execution.",
        "command": [sys.executable, "-B", rel(Path(__file__))],
        "python": sys.version, "platform": platform.platform(),
    })
    check("protected_base_source_and_evidence", not base_state["changed_protected_paths"], **base_state)

    # P3-03's last receipt repair binds current kernel and wrapper, while
    # retaining exact old core bytes under their explicitly historical path.
    receipt = read(S3 / "development/receipt_identity_repair/attempt_1/manifest.json")
    for name, expected in receipt["files_sha256"].items():
        check("p303_receipt_repair_exact_file", sha(ROOT / name) == expected, path=name, expected_sha256=expected)
    for run in ("attempt_1", "composition_1"):
        directory = S4 / "development" / run
        manifest = read(directory / "manifest.json")
        bound_sources(directory, manifest["source_sha256"])
        check("p304_replacement_run_complete", read(directory / "summary.json")["status"] == "PASS", run=run)

    # Read saved exact bytes, respecting failed/diagnostic and superseded rows.
    correspondence = read(S5 / "reviews/evidence_correspondence.json")
    historical = []
    for row in correspondence["runs"]:
        directory = S5 / "development" / row["run"]
        if "manifest_sha256" not in row:
            check("p305_retained_diagnostic_files", all((directory / n).exists() for n in row["files"]), run=row["run"], recorded_status=row["status"])
            historical.append({"run": row["run"], "recorded_status": row["status"]})
            continue
        check("p305_manifest_binding", sha(directory / "manifest.json") == row["manifest_sha256"], run=row["run"])
        m = read(directory / "manifest.json")
        bindings = bound_sources(directory, m["sources_sha256"], current=False)
        for b in bindings:
            expected_current = row["current_source_matches"][Path(b["source"]).name]
            check("p305_current_vs_historical_version", b["current_match"] == expected_current, run=row["run"], source=b["source"], recorded_current=expected_current)
        for field, name in (("summary_sha256", "summary.json"), ("results_sha256", "results.json"), ("disposition_sha256", "external_interruption.json")):
            if field in row:
                check("p305_result_binding", sha(directory / name) == row[field], run=row["run"], file=name)
        if row["status"] != "PASS" or not all(row["current_source_matches"].values()):
            historical.append({"run": row["run"], "recorded_status": row["status"], "current_source_matches": row["current_source_matches"]})
    NOTES.append({"p305_retained_historical_rows": historical, "interpretation": "These rows are not current-version failures or current-version timing measurements."})

    # P3-06's own final evidence audit lists the exact surviving source files.
    # Check those bytes independently; retain its one declared whole-draft gap.
    evidence6 = read(S6 / "reviews/final_evidence_audit.json")
    for row in evidence6["current_six_modules"]:
        check("p306_current_source_binding", sha(ROOT / row["path"]) == row["sha256"], source=row["path"], version=row["version"])
    missing6 = []
    for row in evidence6["file_hash_claims"]:
        if row["resolution"] == "SOURCE_BYTES_NOT_LOCATED":
            missing6.append(row)
            continue
        candidates = [ROOT / p for p in row["matching_files"]]
        matched = [rel(p) for p in candidates if p.exists() and sha(p) == row["expected_sha256"]]
        check("p306_saved_hash_claim", bool(matched), record=row["record"], field=row["field"], expected_sha256=row["expected_sha256"], matching_files=matched)
    check("p306_declared_historical_gap_count", len(missing6) == 1, count=len(missing6))
    NOTES.append({"p306_historical_gap": missing6, "interpretation": "Missing full historical CF-7 draft remains unavailable; current manuscript and preserved section are not substituted for its hash."})

    # Four main P3-07 closures, plus later acquisition and actual dependency
    # closures omitted by the earlier four-family closure note.
    closure7 = read(S7 / "reviews/final_primary_source_closure_check.json")
    for row in closure7["rows"]:
        directory = S7 / row["run"]
        check("p307_current_result_binding", sha(directory / "result.json") == row["result_sha256"], run=row["run"])
        for s in row["sources"]:
            check("p307_current_source_closure", sha(ROOT / s["path"]) == s["sha256"] == sha(ROOT / s["snapshot"]), **s)
    acquisition = S7 / "development/acquisition_planning_run_v1_1"
    bound_sources(acquisition, read(acquisition / "result.json")["source_hashes"], "sources")
    dependency = S7 / "development/adapter_agent/dependency_probe_v2"
    dm = read(dependency / "manifest.json")
    bound_sources(dependency, dm["source_sha256"], "source_snapshot")

    # Manuscript formatting created explicit original sidecars. A historical
    # review hash is checked against exact original bytes, never overwritten.
    sidecars = []
    for directory, name in (("whole_audit_agent", "review_manifest_v2.json"),
                            ("analytic_profile_agent", "analytic_review_manifest_v2.json"),
                            ("proof_agent", "multi_action_code_v2_review_manifest.json"),
                            ("acquisition_planning_agent", "review_v1_1_manifest.json")):
        rd = S7 / "reviews" / directory
        rm = read(rd / name)
        for artifact, claim in rm["artifacts"].items():
            expected = claim["sha256"] if isinstance(claim, dict) else claim
            path = rd / artifact
            if path.exists() and sha(path) == expected:
                check("p307_review_artifact_binding", True, path=rel(path), sha256=expected)
                continue
            original = Path(str(path) + ".original.txt")
            exact_original = original.exists() and sha(original) == expected
            check("p307_review_original_sidecar", exact_original, path=rel(path), original=rel(original), expected_sha256=expected)
            sidecars.append({"display_path": rel(path), "display_sha256": sha(path) if path.exists() else None, "original_path": rel(original), "original_sha256": expected, "exact_original": exact_original})
    NOTES.append({"p307_notation_original_sidecars": sidecars})

    # Narrow composition check on current source only. The data is an old
    # acquired profile; the caller's expected scope is independently rebuilt.
    spec = importlib.util.spec_from_file_location("_p3b_driver", P3 / "checks/07_paid_reasoning_development.py")
    D = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = D
    spec.loader.exec_module(D)
    C = D.C
    raw = read(S7 / "development/run_v3/profile_1024.json")
    profile = C.Profile(C.Scope(**raw["scope"]), tuple(raw["names"]), tuple(raw["feature_names"]),
                        tuple(tuple(tuple(pair) for pair in row) for row in raw["ranges"]),
                        tuple(tuple(row) for row in raw["sums"]), raw["n"], tuple(raw["checkpoints"]),
                        F(raw["delta"]), tuple(raw["setup_resources"]))
    scope = D.actual_scope(D.source_hashes())
    check("current_profile_full_scope_binding", profile.scope == scope)
    profile_before = C.canonical(profile.record())
    swapped = replace(profile, names=(profile.names[1], profile.names[0]) + profile.names[2:])
    low = C.select(swapped, scope, D.PRICES["high"], 64, assessment_limit=321, pre_screen=False)
    check("unvalidated_catalogue_budget_exhaustion_is_fixed_fallback",
          low["policy"] == "fallback" and low["profile_id"] is None and not low["profile_scope_validated"]
          and F(low["conditional_batch_lower_gain"]) == 0 and low["meter"]["total"] <= 321,
          result=low)
    changed = dict(D.source_hashes())
    changed["07_paid_reasoning_development.py"] = "0" * 64
    changed_scope = D.actual_scope(changed)
    stale_low = C.select(profile, changed_scope, D.PRICES["high"], 64, assessment_limit=321, pre_screen=False)
    check("unvalidated_changed_generator_is_unprofiled_fallback",
          stale_low["policy"] == "fallback" and stale_low["profile_id"] is None
          and not stale_low["profile_scope_validated"] and F(stale_low["conditional_batch_lower_gain"]) == 0,
          result=stale_low)
    try:
        C.select(profile, changed_scope, D.PRICES["high"], 64, assessment_limit=20000, pre_screen=False)
    except C.Rejected as exc:
        stale_rejected, message = True, str(exc)
    else:
        stale_rejected, message = False, "No rejection"
    check("funded_changed_generator_admission_rejects", stale_rejected, rejection=message)
    check("retained_profile_unchanged", C.canonical(profile.record()) == profile_before)

    end_state = git_state()
    check("protected_source_and_evidence_unchanged_after_review", not end_state["changed_protected_paths"], **end_state)
    changed_inputs = [name for name, data in INPUTS.items()
                      if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != data["sha256"]]
    check("all_read_source_and_evidence_bytes_unchanged", not changed_inputs, changed=changed_inputs)
    counts = Counter(row["check"] for row in CHECKS)
    failed = [row for row in CHECKS if not row["pass"]]
    result = {"schema": "value_logic.p3b.implementation_checks.v1",
              "status": "PASS" if not failed else "BLOCKED",
              "scope": "Retained evidence/source closure and three current source/catalogue admission boundaries; not an integrated reasoner, new development evaluation, or whole-suite rerun.",
              "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
              "execution_elapsed_ns": time.monotonic_ns() - start_mono,
              "principal_research_credit_ns": 0,
              "check_counts": dict(counts), "failures": failed, "checks": CHECKS,
              "declared_history_and_scope": NOTES, "input_sha256": INPUTS,
              "inspection_setup_disposition": "An earlier read-only inventory assumed every P3-05 record had a manifest and stopped at dependency_1. The saved record explicitly calls it a pre-execution diagnostic; this checker respects that type. No scientific source, result or manifest was changed."}
    write("check_results.json", result)
    print(json.dumps({"status": result["status"], "checks": len(CHECKS), "failures": failed,
                      "inputs": len(INPUTS), "script_runtime_ns": result["execution_elapsed_ns"]}, indent=2))


if __name__ == "__main__":
    main()
