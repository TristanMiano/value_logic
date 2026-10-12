"""Publication-only byte inventory; no scientific imports or acquisition calls.

ChatGPT (GPT-6 Astra Pro), s06. Create once with ``write``; portable byte check
with ``verify``. Native environment comparison is optional: ``verify --environment``.
This is a binding inventory, not proof admission or scientific validation.
"""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = HERE.relative_to(ROOT).as_posix()
REPORT = HERE / "integrity.json"
HEX = re.compile(r"[0-9a-f]{64}\Z")
EXTENSIONS = {".py", ".json", ".jsonl", ".txt"}
S05_DEPENDENCIES = (
    "maxsat_repair.py", "maxsat_reprice.py", "maxsat_repair_results.json",
    "regions_bundle.json",
)
PAYLOAD_HASHES = {"encoding_sha256", "raw_proof_sha256", "admitted_proof_sha256"}
MISSING_RUNNER = "432ec16d781c862de32005c7c251c26f638ade8d15721c68703bf92c6676a833"
ARCHIVED = {
    "461fe7ba95be95c118e778891b2defea861065380d22d5a03b852214c15d47d2":
        "native_warm_attempt.py",
    "2226d8b0d9b81f2473bf31ae2e1e17ee35d5b31e8dbe042319ad4cf0eaf46854":
        "native_attempt_runner.py",
}
IMPLEMENTATIONS = {
    "audit_results.json": "audit_example.py",
    "complete_check_results.json": "complete_check.py",
    "complete_service_results.json": "complete_service.py",
    "contract_fallback_results.json": "contract_fallback.py",
    "contract_results.json": "contract_quote.py",
    "cut_dual_results.json": "cut_dual_probe.py",
    "joint_check_results.json": "joint_check.py",
    "joint_results.json": "joint_repair.py",
    "joint_v2_results.json": "joint_repair_v2.py",
    "mix_results.json": "mix_repair.py",
    "native_attempt_02.json": "native_stream.py",
    "native_stream_results.json": "native_stream.py",
    "proof_cap_results.json": "proof_cap_probe.py",
    "rup_check_results.json": "rup_checks.py",
    "rup_check_v2_results.json": "rup_checks_v2.py",
    "rup_replay_results.json": "rup_replay.py",
    "rup_stream_results.json": "rup_stream.py",
    "vertex_results.json": "vertex_probe.py",
}
SCALAR_TARGETS = {
    "adapter_sha256": "native_repair.py",
    "checked_prior_result_sha256": "contract_results.json",
    "checks_sha256": "contract_checks.py",
    "clock_source_sha256": "clock_source.py",
    "code_sha256": "native_check.py",
    "compilation_sha256": "maxsat_reprice.py",
    "dual_sha256": "cut_dual.py",
    "guard_sha256": "contract_guard.py",
    "inherited_adapter_sha256": "native_repair.py",
    "logical_archive_sha256": "maxsat_repair_results.json",
    "parent_public_menu_sha256": "joint_source.json",
    "prior_quote_result_sha256": "contract_results.json",
    "provider_sha256": "maxsat_repair.py",
    "raw_archive_sha256": "maxsat_repair_results.json",
    "result_sha256": "complete_service_results.json",
    "runner_sha256": "native_stream.py",
    "rup_bridge_sha256": "rup_bridge_v2.py",
    "rup_checker_sha256": "rup_bridge_v2.py",
    "rup_sha256": "rup_bridge_v2.py",
    "script_sha256": "native_stream.py",
    "service_sha256": "complete_service.py",
    "source_archive_sha256": "maxsat_repair_results.json",
    "stream_sha256": "native_stream_results.json",
    "vertex_sha256": "vertex_repair.py",
}


def file_info(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def target_path(name):
    """Relocate recorded checkout paths; retain absolute external package paths."""
    if "/v3/discovery/" in name:
        return ROOT / ("v3/discovery/" + name.split("/v3/discovery/", 1)[1])
    p = Path(name)
    if p.is_absolute():
        return p
    if name.startswith("v3/"):
        return ROOT / p
    if (HERE / p).is_file():
        return HERE / p
    if p.name in S05_DEPENDENCIES:
        return HERE.parent / "s05" / p
    return HERE / p


def display(path):
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def walk(value, location="", key="", parent=None):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from walk(v, location + "." + k, k, value)
    elif isinstance(value, list):
        for v in value:
            yield from walk(v, location + "[]", key, parent)
    elif isinstance(value, str) and HEX.fullmatch(value):
        yield location, key, value, parent


def create_report():
    files = sorted(p for p in HERE.iterdir()
                   if p.is_file() and p.name != REPORT.name
                   and (p.suffix in EXTENSIONS or p.name == "reproduce.md"))
    files += [HERE.parent / "s05" / name for name in S05_DEPENDENCIES]
    inventory = {display(p): file_info(p) for p in files}
    by_hash = defaultdict(list)
    for name, info in inventory.items():
        by_hash[info["sha256"]].append(name)
    documents = {p.name: json.loads(p.read_text()) for p in files
                 if p.parent == HERE and p.suffix == ".json"}
    external = {}
    for data in documents.values():
        for _, key, digest, parent in walk(data):
            if key == "sha256" and parent and "path" in parent:
                path = target_path(parent["path"])
                if not path.is_relative_to(ROOT):
                    external[str(path)] = {"recorded_sha256": digest}
    for name, record in external.items():
        path = Path(name)
        record["observed"] = file_info(path) if path.is_file() else None
        record["status"] = ("MATCH" if record["observed"] and
                            record["observed"]["sha256"] == record["recorded_sha256"]
                            else "UNAVAILABLE_OR_DIFFERENT_ENVIRONMENT")
    external_by_hash = defaultdict(list)
    for name, record in external.items():
        external_by_hash[record["recorded_sha256"]].append(name)

    groups = Counter()
    payloads = Counter()
    non_file_ids = Counter()
    for owner, data in sorted(documents.items()):
        for location, key, digest, parent in walk(data):
            if key in PAYLOAD_HASHES:
                payloads[key] += 1
                continue
            is_file_hash = ("sha256" in key or Path(key).suffix in EXTENSIONS
                            or ".hashes." in location)
            if not is_file_hash:
                non_file_ids[key] += 1
                continue
            named = None
            if key == "sha256" and parent:
                named = parent.get("path", parent.get("file"))
            elif Path(key).suffix in EXTENSIONS:
                named = key
            elif key in SCALAR_TARGETS:
                named = SCALAR_TARGETS[key]
            elif location == ".implementation_sha256":
                named = IMPLEMENTATIONS.get(owner)
            elif key == "source_sha256":
                named = ("rup_stream_results.json" if owner in
                         {"cut_dual_results.json", "rup_replay_results.json"}
                         else "joint_source.json")
            recorded_target = display(target_path(named)) if named else None
            resolved = None
            if recorded_target in inventory:
                if inventory[recorded_target]["sha256"] == digest:
                    status, resolved = "MATCH_NAMED_FILE", recorded_target
                elif digest in ARCHIVED and owner in {
                        "native_attempts.json", "native_attempt_02.json"}:
                    resolved = PREFIX + "/" + ARCHIVED[digest]
                    status = ("MATCH_ARCHIVED_VERSION" if
                              inventory[resolved]["sha256"] == digest else "MISMATCH")
                elif owner == "native_attempts.json" and digest == MISSING_RUNNER:
                    status = "DOCUMENTED_MISSING_FIRST_ATTEMPT_RUNNER"
                else:
                    status = "MISMATCH"
            elif recorded_target in external:
                status, resolved = "ENVIRONMENT_BINDING", recorded_target
                if external[recorded_target]["recorded_sha256"] != digest:
                    status = "MISMATCH"
            elif named:
                status = "MISSING_NAMED_FILE"
            elif digest in by_hash:
                # Scalar hashes without a recorded filename are content-resolved.
                # This records the matching bytes, not the semantic role of code.
                resolved = sorted(by_hash[digest])[0]
                status = "MATCH_CONTENT_RESOLVED_FILE"
            elif digest in external_by_hash:
                resolved = sorted(external_by_hash[digest])[0]
                status = "ENVIRONMENT_BINDING"
            else:
                status = "UNRESOLVED_FILE_HASH"
            groups[(owner, location, digest, recorded_target, resolved, status)] += 1
    bindings = [dict(result=owner, field=field, recorded_sha256=digest,
                     recorded_target=target, resolved_file=resolved, status=status,
                     occurrences=count)
                for (owner, field, digest, target, resolved, status), count
                in sorted(groups.items(), key=lambda item: repr(item[0]))]
    counts = Counter()
    for row in bindings:
        counts[row["status"]] += row["occurrences"]
    failures = [r for r in bindings if r["status"] in
                {"MISMATCH", "MISSING_NAMED_FILE", "UNRESOLVED_FILE_HASH"}]
    clock = documents["effective_actuals.json"]
    closed = (clock.get("clock_active") is False and clock.get("open_segment") is None
              and clock.get("publication_research_credit_ns") == 0)
    if not closed:
        failures.append({"status": "CLOCK_NOT_CLOSED"})
    return {
        "schema": "s06-publication-integrity-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "status": "FAIL" if failures else "PASS_WITH_DOCUMENTED_HISTORICAL_GAP",
        "research_credit_ns": 0,
        "new_audits": 0, "new_native_calls": 0, "new_proof_calls": 0,
        "scope": [
            "Byte identity and recorded file-hash bindings only; no proof admission or scientific rerun.",
            "Every present s06 py/json/jsonl/txt file, stable reproduce.md, and four cited s05 dependencies.",
            "This report is excluded from its own manifest; integrity.py is included. No self-hash cycle.",
            "Handoff prose, pointers, time ledger, later publication artifacts and external package bytes are outside the repository content manifest.",
            "Names absent from original scalar hash fields are explicitly content-resolved; semantic source identity and receipt validity remain the scientific checkers' responsibility.",
            "Files without an earlier source binding receive a publication identity here, not retroactive execution provenance.",
        ],
        "content_manifest": inventory,
        "manifest_file_count": len(inventory),
        "manifest_total_bytes": sum(x["bytes"] for x in inventory.values()),
        "scanned_json": sorted(documents),
        "binding_occurrences_by_status": dict(sorted(counts.items())),
        "file_binding_groups": bindings,
        "unexpected_failures": failures,
        "external_environment": external,
        "embedded_payload_hashes_not_semantically_checked": dict(sorted(payloads.items())),
        "source_and_receipt_identity_occurrences_outside_file_binding_scope":
            dict(sorted(non_file_ids.items())),
        "closed_clock_binding": {
            "closed": closed, "research_minutes": clock["research_minutes"],
            "session_research_ns": clock["session_research_ns"],
            "research_closed_utc": clock["research_closed_utc"],
            "action": "Existing closed records hashed; no time credited or reconciled by this script.",
        },
        "historical_limitations": [
            {
                "record": "native_attempts.json", "attempt": 1,
                "runner_sha256": MISSING_RUNNER,
                "status": "Exact first runner bytes and raw failed-run receipts were not preserved.",
                "adapter": "Its exact adapter is preserved as native_warm_attempt.py.",
                "consequence": "No reconstruction or reusable proof/performance evidence is claimed for lost receipts.",
            },
            {
                "record": "native_attempt_02.json",
                "status": "Preserved unresolved development attempt; original code names refer to archived versions.",
                "adapter": "native_warm_attempt.py", "runner": "native_attempt_runner.py",
                "consequence": "Keep this paid failed attempt separate from corrected native_stream_results.json.",
            },
            {
                "record": "rup_check_results.json",
                "status": "Historical partial result retains its original running status, documented by rup_attempt_01.json.",
                "source": "rup_checks.py and rup_bridge.py are preserved alongside v2 sources/results.",
                "consequence": "No relabeling of unresolved RUP calls as checked lower proofs.",
            },
        ],
    }


def verify(report, environment=False):
    failures = list(report["unexpected_failures"])
    for name, expected in report["content_manifest"].items():
        path = ROOT / name
        observed = file_info(path) if path.is_file() else None
        if observed != expected:
            failures.append({"file": name, "expected": expected, "observed": observed})
    environment_failures = []
    if environment:
        for name, expected in report["external_environment"].items():
            p = Path(name)
            actual = file_info(p) if p.is_file() else None
            if not actual or actual["sha256"] != expected["recorded_sha256"]:
                environment_failures.append({"file": name, "observed": actual})
    return {
        "status": "FAIL" if failures or environment_failures else
                  "PASS_WITH_DOCUMENTED_HISTORICAL_GAP",
        "manifest_files_checked": len(report["content_manifest"]),
        "repository_failures": failures,
        "environment_checked": environment,
        "environment_failures": environment_failures,
        "historical_missing_runner_count": 1,
        "new_acquisitions": 0, "research_credit_ns": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("write", "verify"))
    parser.add_argument("--environment", action="store_true")
    args = parser.parse_args()
    if args.command == "write":
        report = create_report()
        # Refuse to overwrite a prior publication identity.
        with REPORT.open("x") as stream:
            json.dump(report, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
    else:
        report = json.loads(REPORT.read_text())
    result = verify(report, args.environment)
    print(json.dumps(result, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
