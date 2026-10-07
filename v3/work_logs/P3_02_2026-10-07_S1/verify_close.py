"""Read-only P3-02 input/closing verification; GPT-6 Astra Pro, 2026-10-07.

preview validates the current administrative snapshot without requiring closure.
close also requires finalized accounting and synchronized completion controls.
Prints a receipt to stdout; never writes it, closes a clock, or reruns science.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
spec = importlib.util.spec_from_file_location("p302_accounting", HERE/"accounting.py")
accounting = importlib.util.module_from_spec(spec)
spec.loader.exec_module(accounting)
TASK_LOG = REPO/accounting.ARTIFACT
PRINCIPAL = REPO/"v3/derivations/02_probability_information.md"
CONTROL_PATHS = (REPO/"TODO_v3.md", REPO/"v3/README.md", REPO/"v3/claim_ledger.md", REPO/"v3/plan.v1.json")
GENERATED_OUTPUTS = {HERE/"final_validation.json", HERE/"artifact_hashes.json"}


def relative(path):
    path = Path(path).resolve()
    return str(path.relative_to(REPO)) if path.is_relative_to(REPO) else str(path)


def unfence(body):
    lines, fence = [], None
    for line in body.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            char = match.group(1)[0]
            if fence is None:
                fence = char
            elif char == fence:
                fence = None
            lines.append("")
        else:
            lines.append(line if fence is None else "")
    return "\n".join(lines)


def anchors(body):
    found, counts, uncertain = set(), {}, []
    for line in unfence(body).splitlines():
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        title = match.group(1)
        if not title.isascii() or re.search(r"[<>\\$]", title):
            uncertain.append(title)
            continue
        title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", title)
        slug = re.sub(r"[^a-z0-9_\-\s]", "", title.lower())
        slug = re.sub(r"\s", "-", slug)
        count = counts.get(slug, 0)
        counts[slug] = count+1
        found.add(slug if count == 0 else f"{slug}-{count}")
    found.update(re.findall(r'<a\s+(?:name|id)=["\x27]([^"\x27]+)', body))
    return found, uncertain


def verify(mode):
    snapshots = {}
    def read(path):
        path = Path(path).resolve()
        data = path.read_bytes()
        snapshots[path] = accounting.digest(data)
        return data
    def parsed(path):
        return accounting.parse(read(path))
    development_paths = sorted((HERE/"development").rglob("*.json"))
    development_documents = {path: parsed(path) for path in development_paths}
    revision_bindings, revision_records = {}, []
    for path, declaration in development_documents.items():
        if not isinstance(declaration, dict) or declaration.get("stage") != "development_revision":
            continue
        source = (REPO/declaration["source_path"]).resolve()
        archived = (REPO/declaration["archived_source"]).resolve()
        expected = declaration["source_sha256"]
        accounting.require(source.is_relative_to(REPO/"v3/checks"), "Revision source must identify a canonical v3/checks file")
        accounting.require(archived.is_relative_to(HERE/"development/versions") and archived != source,
                           "Historical source must be explicitly archived in this attempt's development/versions")
        accounting.require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected), "Invalid historical source hash")
        accounting.require(accounting.digest(read(archived)) == expected, "Archived source does not match declared historical hash")
        failed_path = (REPO/declaration["failed_result"]).resolve()
        failed = parsed(failed_path)
        accounting.require(failed.get("stage") == "development" and failed.get("status") == "failed",
                           "Historical mapping must retain its explicitly failed development result")
        named = relative(source)
        bound = failed.get("script_path") == named and failed.get("script_sha256") == expected
        bound = bound or failed.get("dependencies", {}).get(named) == expected
        accounting.require(bound, "Preserved failure does not bind the declared historical source/hash")
        key = (named, expected)
        accounting.require(key not in revision_bindings, "Duplicate historical source mapping requires explicit reconciliation")
        revision_bindings[key] = dict(archived=archived, declaration=relative(path), failed_result=relative(failed_path))
        revision_records.append(dict(record=relative(path), source_path=named, source_sha256=expected,
                                     archived_source=relative(archived), failed_result=relative(failed_path)))
    def hash_check(path, expected):
        path = Path(path)
        if not path.is_absolute():
            path = REPO/path
        path = path.resolve()
        current = accounting.digest(read(path)) if path.is_file() else None
        binding = revision_bindings.get((relative(path), expected)) if current != expected else None
        resolved = binding["archived"] if binding else path
        observed = accounting.digest(read(resolved)) if resolved.is_file() else None
        result = dict(path=relative(path), expected_sha256=expected, current_sha256=current,
                      resolved_source_path=relative(resolved), actual_sha256=observed, matches=observed == expected,
                      source_version="explicit_revision_archive" if binding else "current")
        if binding:
            result.update(revision_record=binding["declaration"], preserved_failure=binding["failed_result"])
        return result

    audit, inputs, prefix, append = accounting.audit()
    read(HERE/"verify_close.py")
    report = dict(schema="value_logic.P3-02.closing_verification.v1", mode=mode,
                  classification="read-only administrative verification; no scientific run or gate",
                  contributor="ChatGPT (GPT-6 Astra Pro)", observed_utc=datetime.now(timezone.utc).isoformat(),
                  python=platform.python_version(), command=[sys.executable, relative(__file__), mode],
                  task_completion_inferred_from_accounting=False)
    checks = dict(clock_replay_and_exact_preservation=True,
                  no_closed_engaged_gap_over_15_minutes=not audit["cadence"]["violations"],
                  no_unaccounted_stopped_gaps=not audit["uncredited_stopped_gaps"],
                  principal_time_only=audit["principal_time_only"] and audit["extra_agent_time_credited_ns"] == 0)

    # Parse new session JSON, without executing or reinterpreting historical runs.
    json_errors, json_count = [], 0
    for path in sorted(set(HERE.rglob("*.json")) | {REPO/"v3/plan.v1.json"}):
        if path in GENERATED_OUTPUTS:
            continue  # Output receipts/manifests cannot be inputs to their own generation.
        try:
            parsed(path)
            json_count += 1
        except (OSError, ValueError, TypeError) as error:
            json_errors.append(dict(path=relative(path), error=str(error)))
    report["json_syntax"] = dict(files=json_count, errors=json_errors,
                                 generated_outputs_not_input_scanned=sorted(relative(path) for path in GENERATED_OUTPUTS))
    checks["json_syntax"] = not json_errors

    # Only current task/controls and changed v3 Markdown need a new link scan.
    baseline = accounting.parse(inputs["baseline.json"])
    changed = set(accounting.git("diff", "--name-only", baseline["source_commit"]).decode().splitlines())
    changed.update(accounting.git("ls-files", "--others", "--exclude-standard").decode().splitlines())
    unexpected = sorted(name for name in changed if name != "TODO_v3.md" and not name.startswith("v3/"))
    diff_check = accounting.git("diff", "--check").decode()
    report["change_scope"] = dict(source_commit=baseline["source_commit"], changed_paths=sorted(changed),
                                  unexpected_paths=unexpected, git_diff_check_output=diff_check)
    checks["changes_confined_to_phase_three"] = not unexpected
    md_paths = set(HERE.rglob("*.md")) | {TASK_LOG, PRINCIPAL} | {p for p in CONTROL_PATHS if p.suffix == ".md"}
    md_paths.update(REPO/name for name in changed if name.endswith(".md") and name.startswith("v3/") and (REPO/name).is_file())
    inline = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]*>|[^\s)]+)(?:\s+[\"\x27][^\n]*[\"\x27])?\s*\)")
    reference = re.compile(r"^ {0,3}\[[^]\n]+\]:\s*(<[^>]*>|\S+)", re.M)
    links, missing, confirmed, unresolved = [], [], [], []
    for path in sorted(md_paths):
        if not path.is_file():
            missing.append(dict(source="required current artifact", target=relative(path), resolved=relative(path)))
            continue
        body = unfence(read(path).decode("utf-8"))
        for match in list(inline.finditer(body))+list(reference.finditer(body)):
            target = match.group(1).strip("<>")
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            local = unquote(url.path)
            destination = ((REPO/local.lstrip("/")) if local.startswith("/") else path.parent/local).resolve()
            record = dict(source=relative(path), target=target, resolved=relative(destination))
            links.append(record)
            if not destination.exists():
                missing.append(record)
            elif url.fragment:
                if destination.suffix.lower() != ".md":
                    unresolved.append(dict(record, reason="non-Markdown anchor"))
                    continue
                known, uncertain = anchors(read(destination).decode("utf-8"))
                if unquote(url.fragment) in known:
                    confirmed.append(record)
                else:
                    unresolved.append(dict(record, reason="not confirmed by conservative heading parser",
                                           special_headings=len(uncertain)))
    pending_names = {relative(path) for path in GENERATED_OUTPUTS}
    missing_inputs = [record for record in missing if record["resolved"] not in pending_names]
    report["markdown"] = dict(files=len(md_paths), local_links=len(links), missing_inputs=missing_inputs,
                              deferred_output_links=[record for record in missing if record["resolved"] in pending_names],
                              confirmed_anchors=len(confirmed), unresolved_anchors=unresolved,
                              scope="Inline/reference links outside code fences; conservative ASCII ATX/explicit anchors. Unicode or special anchors require inspection; no external URL audit.")
    checks["no_missing_linked_input"] = not missing_inputs

    development, evidence_ok, run_records = [], True, 0
    record_to_script = {
        "probability_checks_1.json": "v3/checks/02_probability_checks.py",
        "decision_geometry_agent.json": "v3/checks/02_decision_geometry_check.py",
        "decision_geometry_principal.json": "v3/checks/02_decision_geometry_check.py",
    }
    for path, data in development_documents.items():
        accounting.require(isinstance(data, dict), "Development metadata must be an object: " + path.name)
        entry = dict(record=relative(path), result_sha256=accounting.digest(read(path)), hash_checks=[],
                     scientific_execution_repeated=False)
        stage = data.get("stage")
        if stage in {"development_plan", "development_preparation"}:
            accounting.require("execution" not in data and "runs" not in data,
                               "Prospective metadata must not also claim an execution: " + path.name)
            for dependency, metadata in data.get("code", {}).items():
                expected = metadata.get("sha256") if isinstance(metadata, dict) else metadata
                accounting.require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
                                   "Invalid preparation code-hash declaration: " + path.name)
                check = hash_check(dependency, expected)
                if isinstance(metadata, dict) and "bytes" in metadata:
                    dependency_path = Path(check["resolved_source_path"])
                    if not dependency_path.is_absolute():
                        dependency_path = REPO/dependency_path
                    check.update(expected_bytes=metadata["bytes"], actual_bytes=len(read(dependency_path)))
                    check["matches"] = check["matches"] and check["expected_bytes"] == check["actual_bytes"]
                entry["hash_checks"].append(check)
            metadata_hashes_match = all(check["matches"] for check in entry["hash_checks"])
            entry.update(evidence_role="prepared_code_snapshot_not_an_executed_result"
                         if stage == "development_preparation" and data.get("status") != "planned"
                         else "prospective_plan_not_an_executed_result", development_only=True,
                         saved_hashes_match=metadata_hashes_match if entry["hash_checks"] else None,
                         separately_credited_ns=0)
            evidence_ok = evidence_ok and metadata_hashes_match
            development.append(entry)
            continue
        if stage == "development_revision":
            check = hash_check(data["source_path"], data["source_sha256"])
            entry.update(evidence_role="explicit_preserved_source_revision_not_an_executed_result", development_only=True,
                         hash_checks=[check], saved_hashes_match=check["matches"], separately_credited_ns=0)
            evidence_ok = evidence_ok and check["matches"]
            development.append(entry)
            continue
        if stage == "development" and data.get("status") not in {"passed", "failed", "running", "verified"} and "execution" not in data and "runs" not in data and (
                "run_policy" in data or data.get("status") in {"planned", "prospective"}):
            entry.update(evidence_role="prospective_plan_not_an_executed_result", development_only=True,
                         saved_hashes_match=None, separately_credited_ns=0)
            development.append(entry)
            continue
        if stage is None and "runs" not in data and data.get("status") != "DEVELOPMENT":
            entry.update(evidence_role="auxiliary_json_without_development_execution_stage",
                         development_only=None, saved_hashes_match=None, separately_credited_ns=0,
                         scope="Parsed and hashed as an input/auxiliary record; it is not accepted as an executed development result.")
            development.append(entry)
            continue
        run_records += 1
        entry["evidence_role"] = "saved_development_execution"
        if "runs" in data:
            entry.update(history_units=len(data["runs"]), latest_status=data.get("latest_status"),
                         run_outcomes=[run.get("status") for run in data["runs"]])
            entry["development_only"] = bool(data["runs"]) and all(run.get("evidence_class") == "DEVELOPMENT" for run in data["runs"])
            for run in data["runs"]:
                for dependency, expected in run.get("direct_tooling_sha256", {}).items():
                    entry["hash_checks"].append(hash_check(dependency, expected))
                if run.get("additional_research_time_credit", 0) != 0:
                    evidence_ok = False
        else:
            entry.update(development_only=data.get("status") == "DEVELOPMENT" or data.get("stage") == "development",
                         recorded_passed=data.get("passed"), recorded_status=data.get("status"))
            expected = data.get("script_sha256", data.get("execution", {}).get("script_sha256"))
            if expected:
                script_path = data.get("script_path", data.get("execution", {}).get("script_path")) or record_to_script.get(path.name)
                if script_path is None:
                    candidates = [candidate for candidate in (REPO/"v3/checks").glob("*.py")
                                  if accounting.digest(read(candidate)) == expected]
                    accounting.require(len(candidates) == 1,
                                       "Saved script hash needs one identifiable current script: " + path.name)
                    script_path = candidates[0]
                    entry["script_path_basis"] = "Unique current v3/checks file matching the saved content hash; filename execution provenance is not inferred."
                entry["hash_checks"].append(hash_check(script_path, expected))
            dependency_maps = [data.get("execution", {}).get("dependencies", {})]
            dependency_maps.extend(data.get(key, {}) for key in ("dependencies", "dependency_hashes", "dependency_sha256", "direct_tooling_sha256"))
            for dependency_map in dependency_maps:
                if not isinstance(dependency_map, dict):
                    continue
                for dependency, expected in dependency_map.items():
                    if isinstance(expected, dict):
                        expected = expected.get("sha256")
                    if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{64}", expected) is None:
                        continue  # Version/resource metadata is not silently interpreted as a content hash.
                    dependency_path = dependency if "/" in dependency else "v3/checks/"+dependency
                    entry["hash_checks"].append(hash_check(dependency_path, expected))
        entry["saved_hashes_match"] = bool(entry["hash_checks"]) and all(check["matches"] for check in entry["hash_checks"])
        entry["file_binding_checks"] = [hash_check(data[path_key], data[hash_key])
                                       for path_key, hash_key in (("input_path", "input_sha256"), ("artifact_path", "artifact_sha256"))
                                       if path_key in data and hash_key in data]
        evidence_ok = evidence_ok and entry["development_only"] and entry["saved_hashes_match"] and all(
            check["matches"] for check in entry["file_binding_checks"])
        development.append(entry)
    report["saved_development_evidence"] = development
    report["explicit_historical_source_bindings"] = revision_records
    checks["development_classification_and_declared_hashes"] = bool(run_records) and evidence_ok
    progress_jsonl = []
    for path in sorted((HERE/"development").rglob("*.jsonl")):
        data = read(path)
        units = accounting.records(data)
        progress_jsonl.append(dict(path=relative(path), records=len(units), sha256=accounting.digest(data),
                                   separately_credited_ns=0,
                                   scope="Saved progress/provenance records; not extra independent scientific cases or principal time."))
    report["development_progress_jsonl"] = progress_jsonl

    report["accounting"] = {key: audit[key] for key in (
        "research_ns", "research_minutes", "engaged_ns", "engaged_minutes", "excluded_ns", "category_ns",
        "lane_research_ns", "remaining_task_research_ns", "phase3_research_ns", "phase3_engaged_ns",
        "remaining_phase3_research_ns", "protected_research_floor_met", "cadence", "ledger_relation",
        "two_research_attempt_lane_window", "finalize_blockers")}
    report["preservation"] = audit["preservation"]
    if mode == "close":
        actual = parsed(HERE/"actuals.json")
        plan = parsed(REPO/"v3/plan.v1.json")
        prepared = parsed(HERE/"accounting_attempts/attempt0001/prepared.json")
        result = parsed(HERE/"accounting_attempts/attempt0001/result.json")
        compare_keys = set(audit)-{"ledger_relation", "finalize_blockers"}
        differences = sorted(key for key in compare_keys if actual.get(key) != audit[key])
        prepared_differences = sorted(key for key in compare_keys if prepared.get(key) != audit[key])
        checks.update(actuals_match_current_exact_replay=not differences,
                      prepared_matches_current_exact_replay=not prepared_differences,
                      actuals_finalized=actual.get("finalized") is True,
                      clock_stopped=audit["open_segment"] is None,
                      actual_Research90_met=audit["protected_research_floor_met"],
                      exactly_one_matching_ledger_append=audit["ledger_relation"] == "already_matches_this_attempt_append",
                      append_file_matches=read(HERE/"ledger_append.csv") == append,
                      prepared_append_matches=read(HERE/"accounting_attempts/attempt0001/ledger_append.csv") == append,
                      ledger_hash_matches=actual.get("ledger_after_sha256") == accounting.digest(prefix+append),
                      ledger_size_matches=actual.get("ledger_after_bytes") == len(prefix+append),
                      appended_row_count_matches=actual.get("ledger_rows_appended") == len(audit["effective_segments"]),
                      finalized_result_matches=result.get("status") == "finalized" and result.get("actuals_sha256") == accounting.digest(read(HERE/"actuals.json")),
                      no_failed_or_live_finalize_marker=not (HERE/"accounting.finalize.lock").exists()
                          and not list((HERE/"accounting_attempts").rglob("failure.json")))
        report["actuals_differences"], report["prepared_differences"] = differences, prepared_differences
        chunks = {chunk["id"]: chunk for chunk in plan["chunks"]}
        p2, progress = chunks[TASK], plan["observed_progress"]
        actual_name = relative(HERE/"actuals.json")
        claims = read(REPO/"v3/claim_ledger.md").decode()
        claim_section = re.search(r"^## Current contribution record[^\n]*P3-N01\s*\n(.*?)(?=\n## |\Z)", claims, re.M | re.S)
        claim_status = None
        if claim_section:
            found = re.search(r"\*\*Status:\s*(SUPPORTED|NOT YET SUPPORTED|DISPLACED)\.?\*\*", claim_section.group(1))
            if found:
                claim_status = found.group(1)
        todo = read(REPO/"TODO_v3.md").decode()
        log = read(TASK_LOG).decode()
        checks.update(P3_01_stays_complete=chunks["P3-01"]["status"] == "complete",
                      P3_02_marked_complete=p2["status"] == "complete",
                      P3_02_actuals_pointer=p2.get("actuals") == actual_name,
                      P3_02_exact_task_total=p2.get("research_ns") == audit["task_research_ns"],
                      later_chunks_unstarted=all(chunk["status"] == "unstarted" for key, chunk in chunks.items() if key not in {"P3-01", TASK}),
                      report_unstarted=plan["report_task"]["status"] == "unstarted",
                      gates_unattempted=all(gate["status"] == "unattempted" for gate in plan["gates"].values()),
                      next_pointer_P3_A=plan["next_task"] == "P3-A",
                      last_completed_session_synchronized=plan.get("last_completed_session") == accounting.ARTIFACT,
                      phase_floor_preserved=accounting.exact_ns(plan["phase_research_floor_minutes"], accounting.NS_MINUTE) == accounting.PHASE_FLOOR,
                      no_final_freeze_or_exposure=plan["experimental_freeze_created"] is False and plan["final_evaluation_exposed"] is False,
                      contribution_status_synchronized=claim_status is not None and claim_status == plan["contribution_status"],
                      plan_cumulative_research=progress["research_ns"] == audit["phase3_research_ns"],
                      plan_cumulative_engaged=progress["measured_engaged_ns"] == audit["phase3_engaged_ns"],
                      plan_remaining_phase_floor=progress["remaining_floor_ns"] == audit["remaining_phase3_research_ns"],
                      plan_progress_source=progress["source"] == actual_name,
                      TODO_P3_02_checked=bool(re.search(r"^-\s+\[[xX]\]\s+\*\*P3-02\b", todo, re.M)),
                      TODO_P3_A_unchecked=bool(re.search(r"^-\s+\[ \]\s+\*\*P3-A\b", todo, re.M)),
                      work_log_header_complete=bool(re.search(r"Status:\s*\*\*COMPLETE\b", log[:700], re.I)),
                      task_readiness_audit_present=(HERE/"readiness_audit.md").is_file()
                          and bool(read(HERE/"readiness_audit.md").strip()))

    changed_during = [relative(path) for path, expected in snapshots.items()
                      if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected]
    checks["snapshot_stable"] = not changed_during and accounting.snapshot() == inputs
    checks["development_inventory_stable"] = development_paths == sorted((HERE/"development").rglob("*.json"))
    report["snapshot_changed_during_validation"] = changed_during
    report["snapshot_hashes"] = {relative(path): expected for path, expected in snapshots.items()}
    report["checks"] = checks
    report["manual_review_boundaries"] = [
        "Unresolved special/Unicode anchors are listed for inspection; this is not a full Markdown renderer.",
        "The two-attempt R/X window is reported exactly; interpretation of cycles or any exception is not invented by this helper.",
        "The actuals and plan can be synchronized without proving the mathematical or contribution claims; readiness review supplies that assessment.",
        "Final validation and artifact-manifest output links may be generated after this input receipt; publication must check their eventual existence/hashes.",
        "No old result, executable probe, or external source was rerun. Tool/agent resource reports are not added to principal time.",
    ]
    report["status"] = ("PASS" if mode == "close" else "SNAPSHOT_VALID") if all(checks.values()) else "FAIL"
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", default="preview", choices=("preview", "close"))
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    try:
        report = verify(args.mode)
        if args.summary:
            report = {key: report[key] for key in ("status", "mode", "checks", "accounting", "markdown", "manual_review_boundaries")}
        print(accounting.dumps(report), end="")
        return 0 if report["status"] != "FAIL" else 1
    except (accounting.AuditError, OSError, ValueError, KeyError, TypeError, ArithmeticError) as error:
        print(accounting.dumps(dict(status="ERROR", error=type(error).__name__, message=str(error),
                                    read_only=True, automatic_retry=False)), file=sys.stderr, end="")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
