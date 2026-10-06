"""Final Gate D artifact, navigation and scope check; no scientific execution.

Contributor: ChatGPT (GPT-6 Astra Pro). Uses the unchanged F17 navigation
helpers for the actual Markdown forms in the report, not a universal parser.
Run after clock closure, independent accounting review and status rendering.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
EXPECTED_REPORT = "c8f490ce94584fc93d27b759f1f524d5eeeb0d3885729d24db413cb4f5205c5d"


def binding(path):
    path = Path(path)
    data = (REPO / path).read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def read(path):
    return json.loads((REPO / path).read_text())


def main():
    output = ROOT / "readiness_result.json"
    assert not output.exists(), "Preserve earlier readiness attempts."
    helper = REPO / "v2/work_logs/F17_2026-10-06_S1/reviews/navigation/check_report_navigation.py"
    spec = importlib.util.spec_from_file_location("f17_navigation_helpers", helper)
    nav = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nav)
    checks, problems, links = [], [], []

    def check(name, condition, detail=None):
        row = {"id": name, "passed": bool(condition)}
        if detail is not None:
            row["detail"] = detail
        checks.append(row)
        if not condition:
            problems.append(row)

    paths = ["paper_v2.md", "README.md", "v2/checkpoints/D_1.md",
             "v2/work_logs/D_2026-10-06_S1.md", "v2/reporting/README.md",
             "v2/decisions/2026-10-06_report_presentation.md"]
    for path in paths:
        text = (REPO / path).read_text()
        issues = []
        masked, _, _ = nav.mask_code(text, issues)
        matches = list(re.finditer(r"(?<!!)\[([^]\n]*)\]\(([^)\s]+)\)", masked))
        check("link_syntax:" + path, len(matches) == masked.count("](") and not issues, issues)
        for match in matches:
            label, target = match.groups()
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                check("external_syntax:" + path + ":" + target, parts.scheme in ["http", "https"] and bool(parts.netloc))
                continue
            destination = ((REPO / path).parent / unquote(parts.path)).resolve() if parts.path else REPO / path
            okay = destination.exists()
            if okay and parts.fragment:
                okay = destination.is_file() and unquote(parts.fragment) in nav.anchor_inventory(destination.read_text())["ids"]
            links.append({"document": path, "label": label, "target": target, "resolves": bool(okay)})
            check("local_link:" + path + ":" + target, okay)

    report = (REPO / "paper_v2.md").read_text()
    check("reviewed_report_hash", binding("paper_v2.md")["sha256"] == EXPECTED_REPORT)
    check("no_report_rejected_macros", all(token not in report for token in [r"\operatorname", r"\hline", r"\left\{"]))
    check("explicit_theorem_hypothesis", "vectors $c$ and $d$ are nonproportional" in report)
    check("references_preserved", len(re.findall(r'<a id="ref-', report)) == 24)
    for path in ["v2/checkpoints/D_1.md", "v2/work_logs/D_2026-10-06_S1.md"]:
        text = (REPO / path).read_text()
        check("accounting_rendered:" + path, "<!-- D_ACCOUNTING_SUMMARY -->" not in text)
        check("author_pending:" + path, "Author decision: PENDING" in text)
    todo = (REPO / "TODO_v2.md").read_text()
    check("D_checkbox_pending", "- [ ] **Gate D — final audit and phase disposition.**" in todo)
    check("current_pointer_pending", "**Active pointer: Gate D assessment complete — evaluator recommends PASS; author decision pending.**" in todo)
    for path in ["v2/README.md", "v2/claim_ledger.md"]:
        text = (REPO / path).read_text()
        opening = text[:text.find("### Preserved F17 completion") if "### Preserved F17 completion" in text else text.find("## F10")]
        check("workspace_status:" + path, "author decision pending" in opening and "reporting/D_1/claim_map.json" in opening)

    readme = (REPO / "README.md").read_text()
    visible = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", readme)
    check("README_presentation_only", not re.search(r"Gate [A-D]|current status|F\d{2}|E60|D60|Research90|POST-B|engaged minutes", visible, re.I))
    actuals = read(ROOT.relative_to(REPO) / "actuals.json")
    postappend = read(ROOT.relative_to(REPO) / "reviews/integrity/postappend_attempt1.json")
    check("clock_stopped", read(ROOT.relative_to(REPO) / "clock_state.json") is None)
    check("postappend_pass", postappend["status"] == "PASS" and not postappend["checks_failed"])
    check("no_floor_or_parallel_credit", actuals["protected_minimum"] is None and actuals["concurrent_agent_minutes_credited"] == 0)
    check("gate_scope", actuals["gate_d_evaluator_recommendation"] == "PASS" and actuals["gate_d_author_decision"] == "PENDING")

    allowed_changes = {"README.md", "TODO_v2.md", "paper_v2.md", "v2/README.md", "v2/claim_ledger.md", "v2/time_ledger.csv"}
    inventory = read(ROOT.relative_to(REPO) / "entry_inventory.json")
    preserved, changed = [], []
    for old in inventory:
        current = binding(old["path"])
        (preserved if current == old else changed).append(old["path"])
    check("only_authorized_entry_changes", set(changed) <= allowed_changes, changed)
    diff = subprocess.run(["git", "diff", "--check"], cwd=REPO, capture_output=True, text=True)
    check("git_diff_check", diff.returncode == 0, diff.stdout + diff.stderr)
    command = ["python", "v2/reporting/build_gate_d_report.py", "--check"]
    mapped = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    check("current_map_reproduction", mapped.returncode == 0, {"command": command, "stdout": mapped.stdout, "stderr": mapped.stderr})
    result = {"schema": "Gate-D-final-readiness-v1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
              "recorded_utc": datetime.now(timezone.utc).isoformat(),
              "status": "PASS" if not problems else "FAIL", "checks": checks,
              "checks_passed": sum(c["passed"] for c in checks), "failures": problems,
              "links": links, "local_links_checked": len(links),
              "entry_files_preserved": len(preserved), "entry_files_changed": changed,
              "report_sha256": EXPECTED_REPORT, "new_scientific_execution": False,
              "principal_post_cutoff_credit": 0,
              "source_bindings": [binding(path) for path in paths + ["TODO_v2.md", "v2/README.md", "v2/claim_ledger.md",
                  "v2/reporting/D_1/claim_map.json", "v2/time_ledger.csv", str(ROOT.relative_to(REPO) / "actuals.json"),
                  str(ROOT.relative_to(REPO) / "reviews/integrity/postappend_attempt1.json")]]}
    with output.open("x") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"status": result["status"], "checks_passed": result["checks_passed"],
                      "local_links_checked": len(links), "failures": problems,
                      "entry_files_preserved": len(preserved), "entry_files_changed": changed}))
    raise SystemExit(0 if not problems else 1)


if __name__ == "__main__":
    main()
