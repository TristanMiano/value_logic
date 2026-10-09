"""Purchased-label observable certificates: public-only offline first stage.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. R-P3-B-A DEVELOPMENT.
No controller/service imports, policy executions, random draws, modular truth
calculations or private-score reads. Only allowlisted public ZIP members are
deserialized. Whole-container hashes process opaque bytes without opening
private members. Exact source/member/container hashes and reader events are
saved before a separately invoked private-score comparison is permitted.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time
import traceback
import zipfile


HERE = Path(__file__).resolve().parent
DEVELOPMENT = HERE.parent
ROOT = HERE.parents[4]
UNIFORM = DEVELOPMENT / "service_comparison"
ADAPTIVE = DEVELOPMENT / "allocation_comparison/run_001"
VERSION = "observable-public-certificate-v1"
DESIGN = DEVELOPMENT / "observable_certificate_design.md"
PUBLIC_QUERY_FIELDS = {"query_id", "a", "n", "m", "r", "source_version", "semantics_version", "claim_key"}
PUBLIC_TRANSCRIPT_FIELDS = {"index", "block", "query", "expert_actions", "issued_dyadic_probability",
                            "prospective_action", "purchased", "terminal_action"}
ALLOCATION_FIELDS = {"block", "favorite", "selected", "selected_tickets", "ticket_total",
                     "scores", "cost_proxies", "frozen_weights", "buffer_words"}


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    temporary = path.with_name(path.name + ".writing")
    temporary.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temporary.replace(path)


def rel(path):
    return str(path.relative_to(ROOT))


def archive_selected(path, rows):
    payload = b"".join((json.dumps(row, sort_keys=True, separators=(",", ":"), default=str) + "\n").encode()
                       for row in rows)
    info = zipfile.ZipInfo("selected_observations.jsonl", date_time=(1980, 1, 1, 0, 0, 0))
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr(info, payload, compresslevel=9)
    with zipfile.ZipFile(path) as archive:
        if archive.read(info.filename) != payload:
            raise AssertionError("Selected public-observation archive differs from computed records.")
    receipt = {"status": "PASS", "archive": path.name, "bytes": path.stat().st_size,
               "sha256": sha(path.read_bytes()), "member": info.filename, "rows": len(rows),
               "member_bytes": len(payload), "member_sha256": sha(payload),
               "verification": "Every output byte equals canonical selected public-observation JSONL; ZIP CRC checked on reading.",
               "loose_raw_jsonl_written": False}
    write(path.with_name("selected_observations_manifest.json"), receipt)
    return receipt


class PublicReader:
    """One deserialization gateway with a finite exact allowlist and audit.

    Provenance-only source and ZIP digests do not deserialize any labels.
    No private summary, result, evaluator or annotation path is an allowed
    metadata read or member. The private comparison is a separate program.
    """
    def __init__(self, metadata_paths, member_allowlists):
        self.metadata_paths = {p.resolve() for p in metadata_paths}
        self.member_allowlists = {p.resolve(): set(names) for p, names in member_allowlists.items()}
        self.events = []
        self.archive_metadata = {}

    def metadata(self, path):
        path = path.resolve()
        if path not in self.metadata_paths:
            raise PermissionError("First-stage metadata path is not allowlisted: " + str(path))
        payload = path.read_bytes()
        self.events.append({"mode": "public_metadata_json", "path": rel(path),
                            "bytes": len(payload), "sha256": sha(payload)})
        return json.loads(payload)

    def digest_only(self, path, purpose):
        path = path.resolve()
        if purpose not in ("scientific_source_binding", "calculator_or_design_binding", "opaque_archive_binding"):
            raise PermissionError("Unrecognized digest-only purpose.")
        if purpose == "opaque_archive_binding" and path not in self.member_allowlists:
            raise PermissionError("Unknown archive container.")
        if purpose != "opaque_archive_binding" and path.suffix not in (".py", ".md"):
            raise PermissionError("Digest-only source bindings require source/design files.")
        payload = path.read_bytes()
        record = {"mode": purpose, "path": rel(path), "bytes": len(payload), "sha256": sha(payload),
                  "deserialized": False}
        self.events.append(record)
        if purpose == "opaque_archive_binding":
            self.archive_metadata[path] = record
        return record

    def member(self, archive_path, name, manifest_row=None):
        archive_path = archive_path.resolve()
        if name not in self.member_allowlists.get(archive_path, set()):
            raise PermissionError("Non-public or unplanned archive member denied: " + name)
        if any(token in name for token in ("private_evaluator", "postclosed_evaluator", "/controls/")):
            raise PermissionError("A private/control member cannot enter the certificate calculator.")
        with zipfile.ZipFile(archive_path) as archive:
            # Reading this one selected member verifies its CRC. Deliberately
            # do not call testzip(), which would read every private member.
            payload = archive.read(name)
        digest = sha(payload)
        if manifest_row is not None and (len(payload) != manifest_row["bytes"] or digest != manifest_row["sha256"]):
            raise AssertionError("Public member differs from its saved payload manifest.")
        event = {"mode": "public_archive_member", "archive": rel(archive_path), "member": name,
                 "bytes": len(payload), "sha256": digest,
                 "manifest_size_and_hash_checked": manifest_row is not None,
                 "private_label_member": False}
        self.events.append(event)
        if name.endswith(".jsonl"):
            values = [json.loads(line) for line in payload.splitlines()]
            if manifest_row is not None and "rows" in manifest_row and len(values) != manifest_row["rows"]:
                raise AssertionError("Public JSONL row count disagrees with the saved manifest.")
            event["rows"] = len(values)
            return values, event
        return json.loads(payload), event


def uniform_arms(plan):
    main, variation = plan["main_arms"], plan["variation_arms"]
    if (plan["stage"] != "DEVELOPMENT" or plan["saved_before_planned_runs"] is not True
            or plan["tape"]["horizons"] != [992, 3968]
            or main["block_sizes"] != [2, 4, 8, 16] or main["state_bits"] != [None, 16]
            or main["action_bits"] != 16 or main["seed"] != 307201
            or variation["additional_seeds"] != [307203, 307207]):
        raise ValueError("Unexpected prospective uniform source grid.")
    definitions = []
    for t in plan["tape"]["horizons"]:
        for b in main["block_sizes"]:
            for state in main["state_bits"]:
                definitions.append(("main", t, b, state, main["seed"]))
    for seed in variation["additional_seeds"]:
        for state in variation["state_bits"]:
            definitions.append(("variation", variation["horizon"], variation["block_size"], state, seed))
    return [{"kind": "uniform", "name": f"{kind}_T{t}_B{b}_state{'exact' if state is None else state}_seed{seed}",
             "T": t, "B": b, "state_bits": state, "action_bits": 16, "seed": seed}
            for kind, t, b, state, seed in definitions]


def adaptive_arms(plan):
    expected = [{"T": 992, "B": 4, "s": 16, "h": 16, "seed": 307201},
                {"T": 992, "B": 8, "s": 16, "h": 16, "seed": 307201},
                {"T": 3968, "B": 8, "s": 16, "h": 16, "seed": 307201}]
    if plan["stage"] != "DEVELOPMENT" or plan["saved_before_runs"] is not True or plan["arms"] != expected:
        raise ValueError("Unexpected prospective adaptive source grid.")
    return [{"kind": "adaptive", "name": f"adaptive_T{a['T']}_B{a['B']}_state{a['s']}_seed{a['seed']}",
             "T": a["T"], "B": a["B"], "state_bits": a["s"], "action_bits": a["h"], "seed": a["seed"]}
            for a in plan["arms"]]


def ceil_sqrt(value):
    root = math.isqrt(value)
    result = root + int(root * root != value)
    if not (result * result >= value and (result == 0 or (result - 1) ** 2 < value)):
        raise AssertionError("Integer square-root upper enclosure failed.")
    return result


def calculate(arm, transcript, receipts, allocations, bindings):
    t, b, h = arm["T"], arm["B"], arm["action_bits"]
    m, denominator = t // b, 1 << h
    if len(transcript) != t or len(receipts) != m:
        raise AssertionError("The public episode did not retain its declared complete quota.")
    receipt_map = {r["query_id"]: r for r in receipts}
    if len(receipt_map) != m:
        raise AssertionError("Duplicate receipt identities.")
    if arm["kind"] == "adaptive":
        if allocations is None or len(allocations) != m:
            raise AssertionError("The adaptive episode requires every public allocation record.")
        for k, record in enumerate(allocations):
            if set(record) != ALLOCATION_FIELDS or record["block"] != k or record["ticket_total"] != 2 * b:
                raise AssertionError("Unsupported public allocation record schema.")
            favorite, selected = record["favorite"], record["selected"]
            if not 0 <= favorite < b or not 0 <= selected < b:
                raise AssertionError("Allocation index out of admitted block.")
            if record["selected_tickets"] != (b + 1 if selected == favorite else 1):
                raise AssertionError("Selected propensity does not match public ticket multiplicity.")
        common_factor, s_bound = b + 1, 2 * b
    else:
        common_factor, s_bound = 1, b
    u_integer = a_integer = 0
    peak_u_bits = peak_a_bits = 0
    selected_rows, block_counts = [], Counter()
    total_receipt_units = 0
    for index, record in enumerate(transcript):
        purchased = record.get("purchased")
        expected_keys = PUBLIC_TRANSCRIPT_FIELDS | ({"purchased_label"} if purchased else set())
        if type(purchased) is not bool or set(record) != expected_keys:
            raise AssertionError("An unpurchased label or unexpected field entered the public schema.")
        if record["index"] != index or record["block"] != index // b or set(record["query"]) != PUBLIC_QUERY_FIELDS:
            raise AssertionError("Public request/order/schema mismatch.")
        probability = record["issued_dyadic_probability"]
        if set(probability) != {"numerator", "denominator"}:
            raise AssertionError("Unsupported issued probability schema.")
        numerator, actual_denominator = probability["numerator"], probability["denominator"]
        if (type(numerator) is not int or actual_denominator != denominator
                or not 0 <= numerator <= denominator):
            raise AssertionError("Invalid immutable pre-purchase dyadic forecast.")
        query = record["query"]
        if not purchased:
            if query["query_id"] in receipt_map:
                raise AssertionError("A receipt binds an unpurchased public row.")
            continue  # no unpurchased truth/score is read or computed
        receipt = receipt_map.get(query["query_id"])
        if (receipt is None or receipt["claim_key"] != query["claim_key"]
                or receipt["status"] != "success" or receipt["checked"] is not True
                or receipt["provider"] != "cold_checked_modular_adapter"
                or type(receipt["answer"]) is not int or receipt["answer"] not in (0, 1)
                or receipt["answer"] != record["purchased_label"]
                or receipt["answer"] != record["terminal_action"]):
            raise AssertionError("Purchased checked receipt does not bind this issued request.")
        if arm["kind"] == "adaptive":
            allocation = allocations[index // b]
            if allocation["selected"] != index % b:
                raise AssertionError("Public selected receipt and allocation disagree.")
            tickets, ticket_total = allocation["selected_tickets"], 2 * b
        else:
            tickets, ticket_total = 1, b
        pi = F(tickets, ticket_total)
        if pi < F(1, s_bound):
            raise AssertionError("The deterministic reciprocal-propensity bound failed.")
        y = receipt["answer"]
        d_integer = numerator if y == 0 else denominator - numerator
        g_integer = (numerator - denominator * y) ** 2
        d, g = F(d_integer, denominator), F(g_integer, denominator * denominator)
        u_piece, a_piece = (1 / pi - 1) * d, g / pi
        if common_factor % tickets:
            raise AssertionError("The declared common denominator cannot encode this propensity.")
        scale = common_factor // tickets
        u_integer += (ticket_total - tickets) * scale * d_integer
        a_integer += ticket_total * scale * g_integer
        peak_u_bits, peak_a_bits = max(peak_u_bits, u_integer.bit_length()), max(peak_a_bits, a_integer.bit_length())
        block_counts[index // b] += 1
        total_receipt_units += receipt["resources"]["total"]
        selected_rows.append({"index": index, "block": index // b, "query_id": query["query_id"],
                              "claim_key": query["claim_key"], "issued_numerator": numerator,
                              "issued_denominator": denominator, "purchased_label": y,
                              "selected_propensity": pi, "d_selected": d, "g_selected": g,
                              "U_piece": u_piece, "A_piece": a_piece,
                              "receipt_provider": receipt["provider"], "receipt_provider_version": receipt["provider_version"]})
    if set(block_counts) != set(range(m)) or set(block_counts.values()) != {1}:
        raise AssertionError("Every complete block must have exactly one paid label.")
    u_denominator, a_denominator = common_factor * denominator, common_factor * denominator * denominator
    u, a = F(u_integer, u_denominator), F(a_integer, a_denominator)
    if (u != sum((r["U_piece"] for r in selected_rows), F(0))
            or a != sum((r["A_piece"] for r in selected_rows), F(0))):
        raise AssertionError("Exact integer accumulation disagrees with Fraction estimators.")
    sampling_root, action_root = ceil_sqrt(2 * m), ceil_sqrt(2 * (t - m))
    sampling_radius, action_radius = s_bound * sampling_root, action_root
    mean_raw, terminal_raw, brier_raw = u + sampling_radius, u + sampling_radius + action_radius, a + sampling_radius
    row = {**arm, "m": m, "S": s_bound, "U_selected_total": u, "A_selected_total": a,
           "integer_accumulators": {"U_numerator": u_integer, "U_denominator": u_denominator,
                                    "A_numerator": a_integer, "A_denominator": a_denominator,
                                    "common_propensity_denominator_factor": common_factor,
                                    "peak_U_accumulator_bits": peak_u_bits, "peak_A_accumulator_bits": peak_a_bits},
           "sampling_radius": sampling_radius, "action_radius": action_radius,
           "integer_radius_witnesses": {"sampling_radicand": 2 * m, "sampling_ceiling_root": sampling_root,
                                        "action_radicand": 2 * (t - m), "action_ceiling_root": action_root},
           "conditional_action_mean_upper_raw": mean_raw,
           "conditional_action_mean_upper_clipped": min(F(t - m), mean_raw),
           "realized_terminal_upper_raw": terminal_raw,
           "realized_terminal_upper_clipped": min(F(t - m), terminal_raw),
           "immutable_brier_upper_raw": brier_raw,
           "immutable_brier_upper_clipped": min(F(t), brier_raw),
           "strictly_below_trivial_cap": {"conditional_action_mean": mean_raw < t - m,
                                         "realized_terminal": terminal_raw < t - m,
                                         "immutable_brier": brier_raw < t},
           "observed_selected_receipt_units_for_provenance_only": total_receipt_units,
           "receipt_fee_scope": "An existing path's observed receipt total; excluded from concentration algebra and not an unconditional expected fee.",
           "input_bindings": bindings,
           "privacy": {"public_rows_schema_checked": t, "selected_labels_consumed": m,
                       "unpurchased_label_fields_permitted": 0, "private_members_opened": 0,
                       "private_summaries_opened": 0, "new_label_computations": 0},
           "immutable_forecast": "Use the original issued dyadic probability even when that purchased round's terminal action was corrected."}
    return row, selected_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter_ns()
    uniform_plan_path = UNIFORM / "run_001/sources/run_plan_v1.json"
    adaptive_plan_path = ADAPTIVE / "sources/allocation_run_plan_v1.json"
    # These two immutable prospective plans contain no run scores or labels.
    plan_reader = PublicReader((uniform_plan_path, adaptive_plan_path), {})
    rows, all_selected = [], []
    result = {"status": "FAIL", "stage": "DEVELOPMENT", "version": VERSION,
              "principal_clock_credit_ns": 0}
    reader = plan_reader
    try:
        definitions = uniform_arms(plan_reader.metadata(uniform_plan_path)) + adaptive_arms(plan_reader.metadata(adaptive_plan_path))
        if len(definitions) != 23:
            raise AssertionError("Require exactly the20 saved uniform and3 adaptive arms.")
        uniform_archive = UNIFORM / "raw_traces_v1.zip"
        public_prefix = rel(UNIFORM / "run_001/learner_arms")
        allowlists = {uniform_archive: {"RAW_EVIDENCE_MANIFEST.json"}}
        for arm in definitions:
            if arm["kind"] == "uniform":
                allowlists[uniform_archive].update({f"{public_prefix}/{arm['name']}/transcript.jsonl",
                                                   f"{public_prefix}/{arm['name']}/purchase_invoices.jsonl"})
            else:
                allowlists[ADAPTIVE / "learner_arms" / arm["name"] / "public_raw.zip"] = {
                    "MANIFEST.json", "transcript.jsonl", "purchase_invoices.jsonl", "allocation_records.jsonl"}
        adaptive_archive_receipts = [ADAPTIVE / "learner_arms" / arm["name"] / "public_raw_manifest.json"
                                     for arm in definitions if arm["kind"] == "adaptive"]
        reader = PublicReader((uniform_plan_path, adaptive_plan_path, UNIFORM / "raw_archive_manifest_v2.json",
                               *adaptive_archive_receipts), allowlists)
        reader.events.extend(plan_reader.events)
        source_bindings = [reader.digest_only(Path(__file__), "calculator_or_design_binding"),
                           reader.digest_only(DESIGN, "calculator_or_design_binding")]
        for directory, names in ((UNIFORM / "run_001/sources", ("07_selective_feedback.py", "07_selective_feedback_service.py", "07_computation_adapter.py", "07_selective_feedback_development.py")),
                                 (ADAPTIVE / "sources", ("07_selective_feedback_allocation.py", "07_selective_feedback.py", "07_selective_feedback_service.py", "07_computation_adapter.py", "07_selective_feedback_allocation_development.py"))):
            source_bindings.extend(reader.digest_only(directory / name, "scientific_source_binding") for name in names)
        authoritative = reader.metadata(UNIFORM / "raw_archive_manifest_v2.json")
        uniform_binding = reader.digest_only(uniform_archive, "opaque_archive_binding")
        if (uniform_binding["bytes"] != authoritative["archive_bytes"]
                or uniform_binding["sha256"] != authoritative["archive_sha256"]):
            raise AssertionError("Uniform archive does not match authoritative manifestv2.")
        uniform_manifest, uniform_manifest_event = reader.member(uniform_archive, "RAW_EVIDENCE_MANIFEST.json")
        uniform_members = {r["archive_path"]: r for r in uniform_manifest["files"]}
        if uniform_members != {r["archive_path"]: r for r in authoritative["files"]}:
            raise AssertionError("Uniform embedded and current payload manifests differ.")
        write(out / "protocol.json", {
            "stage": "DEVELOPMENT", "started_utc": utc(), "command": sys.argv,
            "source_bindings": source_bindings, "public_member_allowlists": {rel(p): sorted(v) for p, v in allowlists.items()},
            "separation": "This process cannot deserialize private/evaluator/control members through its finite reader gateway. No private score is read before public_stage_complete.json is saved. A separate program may compare scores afterward.",
            "archive_hash_scope": "Whole-container SHA256 reads opaque bytes, including compressed private payload bytes in the shared uniform ZIP; only allowlisted public members are decompressed/deserialized.",
            "coverage_scope": "Per arm under fresh fair selectors/actions: conditional mean39/40, Brier39/40, terminal19/20. No simultaneous23-arm or joint Brier+terminal coverage is claimed. Fixed seeded DEVELOPMENT traces do not establish coverage.",
            "analysis_cost_scope": "Offline post-run arithmetic, parsing, hashes and storage are external evidence work; no units are added to or subtracted from existing deployed invoices, and no free deployed calculator is claimed.",
            "environment": {"python": sys.version, "executable": sys.executable, "platform": platform.platform()},
            "principal_clock_credit_ns": 0,
        })
        for arm in definitions:
            allocations = None
            if arm["kind"] == "uniform":
                archive, archive_binding = uniform_archive, uniform_binding
                transcript_name, receipt_name = (f"{public_prefix}/{arm['name']}/{n}" for n in ("transcript.jsonl", "purchase_invoices.jsonl"))
                transcript, q_event = reader.member(archive, transcript_name, uniform_members[transcript_name])
                receipts, receipt_event = reader.member(archive, receipt_name, uniform_members[receipt_name])
                member_bindings = [uniform_manifest_event, q_event, receipt_event]
                expected_private_result_sha = uniform_manifest["run_result_sha256"]  # digest metadata only
                policy_hashes = None
            else:
                archive = ADAPTIVE / "learner_arms" / arm["name"] / "public_raw.zip"
                archive_binding = reader.digest_only(archive, "opaque_archive_binding")
                stored_archive_receipt = reader.metadata(archive.with_name("public_raw_manifest.json"))
                if (archive_binding["bytes"] != stored_archive_receipt["archive_bytes"]
                        or archive_binding["sha256"] != stored_archive_receipt["archive_sha256"]):
                    raise AssertionError("Adaptive public archive changed since its original verification.")
                manifest, manifest_event = reader.member(archive, "MANIFEST.json")
                entries = {r["name"]: r for r in manifest["entries"]}
                transcript, q_event = reader.member(archive, "transcript.jsonl", entries["transcript.jsonl"])
                receipts, receipt_event = reader.member(archive, "purchase_invoices.jsonl", entries["purchase_invoices.jsonl"])
                allocations, allocation_event = reader.member(archive, "allocation_records.jsonl", entries["allocation_records.jsonl"])
                member_bindings = [manifest_event, q_event, receipt_event, allocation_event]
                expected_private_result_sha = None
                policy_hashes = manifest["source_plan_hashes"]
            bindings = {"archive": archive_binding, "members": member_bindings,
                        "expected_prior_private_result_sha256_from_manifest_only": expected_private_result_sha,
                        "observed_policy_source_plan_hashes": policy_hashes}
            row, selected = calculate(arm, transcript, receipts, allocations, bindings)
            rows.append(row)
            all_selected.extend({"arm": arm["name"], **s} for s in selected)
            write(out / "progress.json", {"completed_arms": len(rows), "last": arm["name"], "updated_utc": utc()})
        for binding in source_bindings:
            if sha((ROOT / binding["path"]).read_bytes()) != binding["sha256"]:
                raise RuntimeError("Source or prospective design changed during the public calculation.")
        result.update(status="PASS", rows=rows, source_bindings=source_bindings,
                      all_23_rows_retained=True, new_policy_calls=0, new_service_calls=0,
                      new_rng_calls=0, new_truth_calls=0,
                      certificate_scope="Exact calculations from saved public receipts; fair-randomness theorem coverage is a premise, not established by deterministic seed agreement.")
    except BaseException as error:
        result.update(error=repr(error), traceback=traceback.format_exc(), completed_rows=rows,
                      disposition="First-stage failure preserved; no retry or private-score comparison authorized from this incomplete result.")
    result.update(finished_utc=utc(), elapsed_runtime_ns=time.perf_counter_ns() - started)
    audit = {"status": result["status"], "schema": "value_logic.public_certificate_reader_audit.v1",
             "events": reader.events, "private_members_deserialized": 0, "private_summaries_deserialized": 0,
             "allowed_label_fields": "Only purchased_label on purchased public rows and their bound receipt.answer.",
             "public_rows_schema_checked": sum(r["privacy"]["public_rows_schema_checked"] for r in rows),
             "selected_labels_consumed": sum(r["m"] for r in rows),
             "new_labels_computed": 0, "separate_private_stage_not_started_by_this_program": True,
             "scope": "Audit of the explicit reader gateway and exact public schemas in this source, not a general operating-system information-flow sandbox.",
             "principal_clock_credit_ns": 0}
    write(out / "reader_audit.json", audit)
    selected_archive = archive_selected(out / "selected_observations.zip", all_selected)
    write(out / "result.json", result)
    if result["status"] == "PASS":
        write(out / "public_stage_complete.json", {
            "status": "PASS", "closed_utc": utc(), "rows": len(rows),
            "result_sha256": sha((out / "result.json").read_bytes()),
            "reader_audit_sha256": sha((out / "reader_audit.json").read_bytes()),
            "selected_observations_archive_sha256": selected_archive["sha256"],
            "private_score_reads_before_closure": 0,
            "disposition": "Public-only calculation completed. Only now may a separate comparison process read existing private scores.",
        })
    print(json.dumps({"status": result["status"], "rows": len(rows),
                      "private_members_deserialized": 0, "elapsed_runtime_ns": result["elapsed_runtime_ns"]}), flush=True)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
