"""Public-only reporting replay, followed by separately invoked private audit.

P3-08 DEVELOPMENT. Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
The public command reads only sealed public broker records. Reanalysis of
already seen seeds checks formulas/costs; it is not prospective coverage.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import argparse
import gzip
import hashlib
import json
from pathlib import Path

import p308_cnf as S
import p308_reporting as P
from p308_common import REPO, canonical

VERSION = "p308-report-replay-v1"


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save(p, value):
    Path(p).write_text(json.dumps(value, indent=2, sort_keys=True)+"\n")


def sources():
    names = ["v3/experiments/"+n for n in ("p308_reporting.py", "p308_report_replay.py", "p308_common.py", "p308_broker.py", "p308_cnf.py")]
    names += ["v3/checks/"+n for n in ("07_selective_feedback.py", "07_selective_feedback_service.py", "07_computation_adapter.py")]
    return [{"path": p, "bytes": (REPO/p).stat().st_size, "sha256": sha(REPO/p)} for p in names]


def public_replay(input_dir, out):
    input_dir, out = Path(input_dir).resolve(), Path(out).resolve()
    out.mkdir(exist_ok=False, parents=True)
    before = sources()
    save(out/"plan_and_sources.json", {"stage": "DEVELOPMENT", "version": VERSION,
         "created_utc": datetime.now(timezone.utc).isoformat(),
         "read_boundary": "public_seal.json and public_records.jsonl.gz only",
         "constructions": [["base","fixed"],["snapshot","fixed"],["snapshot","grid"],["base","grid"]],
         "retrospective_development": True, "prospective_coverage_claim": False,
         "sources": before})
    seal = json.loads((input_dir/"public_seal.json").read_text())
    expected = next(row["sha256"] for row in seal["files"] if row["path"] == "public_records.jsonl.gz")
    assert sha(input_dir/"public_records.jsonl.gz") == expected
    reports = []
    with gzip.open(input_dir/"public_records.jsonl.gz", "rt") as archive:
        for line in archive:
            record = json.loads(line)
            if record["configuration"]["kind"] != "broker":
                continue
            for basis, radius in (("base","fixed"),("snapshot","fixed"),("snapshot","grid"),("base","grid")):
                result = P.report_owned_episode(S, record["episode"], basis=basis, radius=radius)
                reports.append({"run_id": record["run_id"], "basis": basis, "radius": radius,
                                "report": result})
    with (out/"public_reports.jsonl.gz").open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as archive:
            for row in reports:
                archive.write(canonical(row).encode()+b"\n")
    after = sources()
    assert before == after
    save(out/"public_seal.json", {"stage": "DEVELOPMENT", "sealed_utc": datetime.now(timezone.utc).isoformat(),
         "input_public_seal_sha256": sha(input_dir/"public_seal.json"),
         "input_public_archive_sha256": expected, "report_count": len(reports),
         "all_success": all(row["report"]["status"] == "success" for row in reports),
         "sources_unchanged": True, "private_truth_read": False,
         "output_sha256": sha(out/"public_reports.jsonl.gz")})
    return {"reports": len(reports), "successful": sum(r["report"]["status"] == "success" for r in reports)}


def private_audit(input_dir, out):
    input_dir, out = Path(input_dir).resolve(), Path(out).resolve()
    if (out/"private_audit.json").exists():
        raise ValueError("Preserve an existing audit; use a new output run.")
    seal = json.loads((out/"public_seal.json").read_text())
    assert sha(out/"public_reports.jsonl.gz") == seal["output_sha256"]
    scored = {r["run_id"]: r for r in json.loads((input_dir/"private/scores.json").read_text())["runs"]}
    groups, rows = {}, []
    with gzip.open(out/"public_reports.jsonl.gz", "rt") as archive:
        for line in archive:
            row = json.loads(line)
            result, target = row["report"], scored[row["run_id"]]
            if result["status"] != "success":
                rows.append({"run_id": row["run_id"], "basis": row["basis"], "radius": row["radius"], "status": "failed", "detail": result["failure_detail"]})
                continue
            f, v, z = F(*target["issued_brier"]), F(*target["lottery_mean_diagnostic"]), F(target["terminal_errors"])
            assert f-F(*result["live_centers"]["F"]) == v-F(*result["live_centers"]["V"])
            assert F(*target["base_issued_brier"])-f == F(*result["corrections"]["F"])
            assert F(*target["base_lottery_mean_diagnostic"])-v == F(*result["corrections"]["V"])
            assert target["base_terminal_errors"]-z == result["corrections"]["Z"]
            coverage = {key: F(*result["intervals"][key]["lower"]) <= value <= F(*result["intervals"][key]["upper"])
                        for key, value in (("F",f),("V",v),("Z",z))}
            rows.append({"run_id": row["run_id"], "basis": row["basis"], "radius": row["radius"],
                         "status": "success", "shared_identity": True, "exact_corrections": True,
                         "coverage_diagnostic_only": coverage, "Q": result["Q"], "R": result["R"],
                         "sampling_radius": result["sampling_radius"], "intervals": result["intervals"],
                         "report_units": result["meter"]["total"], "n_live": result["n_live"]})
            groups.setdefault(row["run_id"], {})[(row["basis"],row["radius"])] = result
    width_checks = []
    for run_id, group in groups.items():
        q0, qs = F(*group[("base","fixed")]["Q"]), F(*group[("snapshot","fixed")]["Q"])
        assert qs <= q0
        assert group[("base","fixed")]["corrections"] == group[("snapshot","grid")]["corrections"]
        width_checks.append({"run_id":run_id,"Q_snapshot_le_base":True,"strict":qs<q0})
    save(out/"private_audit.json", {"stage":"DEVELOPMENT","retrospective_development":True,
         "prospective_coverage_claim":False,"public_seal_sha256":sha(out/"public_seal.json"),
         "private_scores_sha256":sha(input_dir/"private/scores.json"),"rows":rows,"width_checks":width_checks})
    return {"reports":len(rows),"strict_width_reductions":sum(r["strict"] for r in width_checks),
            "uncovered_diagnostics":sum(not all(r.get("coverage_diagnostic_only",{}).values()) for r in rows)}


if __name__ == "__main__":
    p=argparse.ArgumentParser();p.add_argument("command",choices=("public","audit"));p.add_argument("--input",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();print(canonical(public_replay(a.input,a.out) if a.command=="public" else private_audit(a.input,a.out)))
