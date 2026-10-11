"""Administrative P3-10 preservation and completion readback; no scientific rerun.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
"""
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import csv
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = "ea3e20dd9889c2ee22141c17390595867d33d8ab"
ALLOWED = {"TODO_v3.md", "v3/README.md", "v3/claim_ledger.md", "v3/plan.v1.json", "v3/time_ledger.csv"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def main():
    errors, protected, permitted = [], 0, []
    def check(ok, label, detail=None):
        if not ok:
            errors.append({"check": label, "detail": detail})
    tree = subprocess.check_output(["git", "ls-tree", "-rz", BASE], cwd=ROOT)
    entries = []
    for item in tree.split(b"\0"):
        if not item: continue
        meta, name = item.split(b"\t", 1)
        mode, kind, expected = meta.decode().split()
        path = name.decode(); entries.append(path)
        p = ROOT / path
        if path in ALLOWED:
            permitted.append(path)
            continue
        check(p.exists() or p.is_symlink(), "protected_path_exists", path)
        if not (p.exists() or p.is_symlink()): continue
        data = os.readlink(p).encode() if p.is_symlink() else p.read_bytes()
        actual_mode = "120000" if p.is_symlink() else ("100755" if p.stat().st_mode & 0o111 else "100644")
        check(blob(data) == expected and actual_mode == mode, "protected_bytes_and_mode", path)
        protected += 1
    changed = subprocess.check_output(["git", "diff", "--name-only", BASE], cwd=ROOT, text=True).splitlines()
    check(set(changed) == ALLOWED, "exactly_five_existing_control_edits", changed)
    check(sha((ROOT/"v3/experiments/frozen_v1/manifest.json").read_bytes()) == "69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70", "freeze_manifest")
    check(sha((ROOT/"v3/experiments/protocol.v1.json").read_bytes()) == "dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f", "frozen_protocol")
    a1 = ROOT/"v3/experiments/amendments/P3_10_A1"
    manifest = load(a1/"manifest.json")
    check(sha((a1/"manifest.json").read_bytes()) == "36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359", "amendment_manifest")
    for field, name in [("amendment_prose_sha256","protocol.md"),("amendment_protocol_sha256","protocol.json")]:
        check(sha((a1/name).read_bytes()) == manifest[field], field)
    preserved_bytes = 0
    for record in manifest["original_evidence"] + manifest["new_sources"] + [manifest["development_check"]]:
        p = ROOT/record["path"]; data = p.read_bytes()
        check(len(data) == record["bytes"] and sha(data) == record["sha256"], "amendment_bound_file", record["path"])
    for record in manifest["original_evidence"]: preserved_bytes += record["bytes"]
    old = ROOT/"v3/experiments/final_v1"; new = ROOT/"v3/experiments/final_v1_amended_A1"
    check(not (old/"stages/public/complete.json").exists(), "original_public_completion_absent")
    check(not (old/"stages/evaluation").exists(), "original_evaluation_absent")
    check(not (old/"stages/analysis").exists(), "original_analysis_absent")
    failure = old/"stages/public/attempts/attempt_01/failure.json"
    check(sha(failure.read_bytes()) == manifest["original_failure_sha256"], "original_failure_preserved")
    composite = load(new/"composite_public.json")
    check(composite["completed_units"] == composite["expected_units"] == 500, "complete_public_barrier")
    check(composite["original_units"] == 440 and composite["amended_units"] == 60, "mixed_provenance_counts")
    sealed_paths = set()
    def verify_seal(path):
        if str(path) in sealed_paths: return
        seal = load(path)
        for field,name in [("result_sha256","result.json"),("start_sha256","start.json")]:
            check(sha((path.parent/name).read_bytes()) == seal[field], "unit_"+field, str(path.relative_to(ROOT)))
        sealed_paths.add(str(path))
    for record in composite["seals"]:
        origin = ROOT/record["origin_root"]
        for field,pathfield in [("result_sha256","result_path"),("seal_sha256","seal_path")]:
            check(sha((origin/record[pathfield]).read_bytes()) == record[field], "composite_bound_file", record[pathfield])
        verify_seal(origin/record["seal_path"])
    stage_counts = {}
    for origin,stage,count in [(old,"inputs",12),(new,"public",60),(new,"evaluation",500),(new,"analysis",1)]:
        completion = load(origin/"stages"/stage/"complete.json")
        check(completion["completed_units"] == completion["expected_units"] == count, "stage_count", stage)
        check(len(completion["seals"]) == count, "stage_seal_count", stage)
        stage_counts[("original_" if origin == old else "A1_")+stage] = count
        for record in completion["seals"]:
            path=origin/record["path"]
            check(sha(path.read_bytes()) == record["sha256"], "stage_seal_hash", str(path.relative_to(ROOT)))
            verify_seal(path)
    actuals = load(HERE/"actuals.json"); plan = load(ROOT/"v3/plan.v1.json")
    check(load(HERE/"clock_state.json") is None and actuals["clock_stopped"], "stopped_clock")
    check(actuals["research_ns"] == 5417014164347 and actuals["research_floor_satisfied"], "Research90")
    check(actuals["phase_research_ns"] == 65167882041849, "phase_research")
    check(actuals["agent_overlap_added_ns"] == actuals["historical_recredit_ns"] == 0, "no_duplicate_credit")
    check(plan["next_task"] == "P3-11" and plan["active_session"] is None, "next_unselected_boundary")
    byid={c["id"]:c for c in plan["chunks"]}
    check(byid["P3-10"]["status"] == "complete" and byid["P3-11"]["status"] == "unstarted", "task_statuses")
    check(plan["observed_progress"]["research_ns"] == actuals["phase_research_ns"] and plan["observed_progress"]["measured_engaged_ns"] == actuals["phase_measured_engaged_ns"], "plan_actuals_match")
    prior = subprocess.check_output(["git","show",BASE+":v3/time_ledger.csv"],cwd=ROOT)
    ledger = (ROOT/"v3/time_ledger.csv").read_bytes(); append=(HERE/"ledger_append.csv").read_bytes()
    check(len(prior)==200471 and ledger==prior+append, "append_only_ledger")
    check(sha(ledger)==actuals["ledger"]["result_sha256"] and sha(append)==actuals["ledger"]["append_sha256"], "ledger_hashes")
    rows=list(csv.DictReader(io.StringIO(ledger.decode())))
    research_sum=sum(int(Decimal(r["engaged_seconds"])*Decimal(1_000_000_000)) for r in rows if r["mode"] in ("D","L","E"))
    check(research_sum==actuals["phase_research_ns"], "phase_reconstructed_from_ledger", research_sum)
    names=subprocess.check_output(["git","ls-files","--others","--exclude-standard"],cwd=ROOT,text=True).splitlines()
    json_count=0
    for name in names:
        if name.endswith(".json"):
            try: load(ROOT/name); json_count += 1
            except Exception as exc: errors.append({"check":"new_json_parse","path":name,"error":str(exc)})
    spec=importlib.util.spec_from_file_location("markdown_guard",ROOT/"v3/checks/math_markdown.py")
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    focused=["TODO_v3.md","v3/README.md","v3/claim_ledger.md","v3/experiments/results.md",
             "v3/work_logs/P3_10_2026-10-11_S1.md"] + ["v3/work_logs/P3_10_2026-10-11_S1/"+x for x in
             ["scientific_review_closure.md","review_closure.md","duty_evidence_attachment.md","duty_evidence_attachment_addendum.md"]]
    link_count=span_count=0
    for name in focused:
        p=ROOT/name; data=p.read_text(); spans=list(guard.math_spans(data));span_count += len(spans)
        check(guard.transform(data,protect=True)==data, "focused_markdown_math", name)
        for target in re.findall(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)",data):
            target=target.split("#",1)[0]
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:",target):continue
            resolved=(p.parent/target).resolve()
            check(resolved.exists() or resolved==HERE/"closing_verification.json", "focused_local_link", {"from":name,"target":target})
            link_count+=1
    result={"schema":"value_logic.p310.closing_verification.v1","contributor":"ChatGPT (GPT-6 Astra Pro)",
        "verified_utc":datetime.now(timezone.utc).isoformat(),"status":"FAIL" if errors else "PASS",
        "scope":"Administrative saved-byte, seal, accounting, JSON and principal-document readback; no scientific worker, scorer, analyzer or live renderer executed.",
        "entry_commit":BASE,"entry_files":len(entries),"protected_files_byte_and_mode_identical":protected,
        "allowed_existing_edits":sorted(ALLOWED),"actual_existing_edits":changed,
        "original_evidence_files":len(manifest["original_evidence"]),"original_evidence_bytes":preserved_bytes,
        "original_public_completion_absent":True,"amended_public_units":60,"composite_public_units":500,
        "stage_counts":stage_counts,"unique_unit_seals_verified":len(sealed_paths),
        "actuals_sha256":sha((HERE/"actuals.json").read_bytes()),"ledger":actuals["ledger"],
        "phase_research_ns_reconstructed_from_ledger":research_sum,"research_ns":actuals["research_ns"],
        "clock_stopped":True,"P3_10_status":byid["P3-10"]["status"],"P3_11_status":byid["P3-11"]["status"],
        "next_task":plan["next_task"],"new_json_files_parsed":json_count,
        "markdown":{"files":len(focused),"local_links_checked":link_count,"math_spans":span_count,"scope":"Portable source conventions and local file targets; global debt recorded separately."},
        "verification_source_sha256":sha(Path(__file__).read_bytes()),"errors":errors}
    attempts=HERE/"closing_checks";attempts.mkdir(exist_ok=True)
    n=1
    while (attempts/f"attempt_{n:02d}.json").exists():n+=1
    (attempts/f"attempt_{n:02d}.json").write_text(json.dumps(result,indent=2)+"\n")
    if not errors:
        with (HERE/"closing_verification.json").open("x") as stream:
            json.dump(result,stream,indent=2);stream.write("\n")
    print(json.dumps(result))
    if errors:raise SystemExit(1)


if __name__ == "__main__":
    main()
