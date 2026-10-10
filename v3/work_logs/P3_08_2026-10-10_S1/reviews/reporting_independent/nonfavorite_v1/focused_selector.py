"""P3-08 DEVELOPMENT focused public selected-nonfavorite branch audit.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. See selector_addendum.md.
No private evaluator; expected values imported only from the independent
Fraction reconstruction, with production code used solely as the subject.
"""
from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
import shutil
import sys

from audit_reporting import (SOURCE_PATHS, IdentityOnly, PurchaseBoundary,
                             derive_public, differences, fingerprint, save, utc)


def run(review, out):
    if out.exists():
        raise FileExistsError("Preserve previous evidence; use a fresh output directory")
    original = review / "run_v1"
    before = [fingerprint(original / "source" / path, path) for path in SOURCE_PATHS]
    expected_manifest = json.loads((original / "manifest_before.json").read_text())["sources"]
    if before != expected_manifest:
        raise AssertionError("The accepted subject snapshot changed")
    public = json.loads((original / "public_input.json").read_text())
    out.mkdir(parents=True)
    shutil.copyfile(Path(__file__), out / "focused_selector.py")
    shutil.copyfile(review / "selector_addendum.md", out / "selector_addendum.md")
    save(out / "manifest_before.json", {"stage": "DEVELOPMENT", "created_utc": utc(),
         "source_reference": str(original / "source"), "sources": before,
         "independent_calculator": fingerprint(review / "audit_reporting.py", "audit_reporting.py"),
         "audit_script": fingerprint(Path(__file__), "focused_selector.py"),
         "public_input": fingerprint(original / "public_input.json", "run_v1/public_input.json"),
         "seed": 7, "principal_time_credit_seconds": 0})
    sys.path.insert(0, str(original / "source/v3/experiments"))
    broker = importlib.import_module("p308_broker")
    service = importlib.import_module("p308_cnf")
    reporter = importlib.import_module("p308_reporting")
    tape = tuple(service.make_query(q["query_id"], q["variables"], q["clauses"],
                                    source_version=q["source_version"])
                 for q in public["queries"])
    boundary = PurchaseBoundary(service)
    episode = broker.execute(boundary, tape, broker.Contract(12, 4, 6, 16, 16, "tickets", 128),
                             seed=7, hard=True, purchase_solver="enumeration",
                             scope_epoch="independent-nonfavorite")
    save(out / "public_episode.json", episode)
    expected = derive_public(episode)
    report = reporter.report_owned_episode(IdentityOnly(service), episode)
    errors = differences(expected, report)
    first = episode["blocks"][0]
    branch_ok = (first["ticket"] == first["selected"] == 0 and first["favorite"] == 3
                 and first["multiplicity"] == 1
                 and episode["trace"][0]["propensity"] == [1, 8])
    purchase_ok = boundary.calls == [r["query_id"] for r in episode["trace"] if r["selected"]]
    save(out / "comparison.json", {"expected": expected, "report": report,
                                    "differences": errors, "purchase_calls": boundary.calls})
    after = [fingerprint(original / "source" / path, path) for path in SOURCE_PATHS]
    save(out / "manifest_after.json", {"created_utc": utc(), "sources": after,
                                       "unchanged": before == after})
    summary = {"stage": "DEVELOPMENT", "subject_version": reporter.VERSION,
               "formula_equal": not errors, "first_selected_nonfavorite_branch": branch_ok,
               "only_selected_purchases": purchase_ok, "snapshot_unchanged": before == after,
               "report_units": report["meter"]["total"], "n_live": report["n_live"],
               "peak_integer_bits": report["peak_integer_bits"],
               "ticket_records": [{k: b[k] for k in ("ticket", "selected", "favorite", "multiplicity")}
                                  for b in episode["blocks"]],
               "private_truth_evaluations": 0, "principal_time_credit_seconds": 0,
               "reproduce": "python " + str(Path(__file__)) + " --review " + str(review)
                            + " --out /tmp/p308_reporting_nonfavorite_replay"}
    summary["passed"] = not errors and branch_ok and purchase_ok and before == after
    save(out / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    summary = run(args.review.resolve(), args.out.resolve())
    raise SystemExit(not summary["passed"])
