"""Second prospective public-only observable-certificate calculation.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. DEVELOPMENT, zero principal credit.
Reuses only the reviewed baseline analysis reader and public-schema checks;
no scientific controller/service import or execution. Fixed lambda=8/R is
determined by the declared horizon/propensity floor before the observed Q.
The centered design is read only for hashing; private comparison is separate.
"""
from fractions import Fraction as F
import argparse
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time
import traceback
import zipfile


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("_observable_public_analysis", HERE / "calculate_public.py")
B = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = B
SPEC.loader.exec_module(B)
ROOT, DEVELOPMENT, UNIFORM, ADAPTIVE = B.ROOT, B.DEVELOPMENT, B.UNIFORM, B.ADAPTIVE
DESIGN = DEVELOPMENT / "centered_certificate_design.md"
VERSION = "observable-centered-public-certificate-v1"


def calculate(arm, transcript, receipts, allocations, bindings):
    baseline, selected = B.calculate(arm, transcript, receipts, allocations, bindings)
    t, b, m, h = arm["T"], arm["B"], baseline["m"], arm["action_bits"]
    denominator = 1 << h
    factor = b + 1 if arm["kind"] == "adaptive" else 1
    s_bound = 2 * b if arm["kind"] == "adaptive" else b
    common = denominator * factor
    if denominator % 2:
        raise AssertionError("These source-bound dyadic arms have h>=1.")
    u_integer = (t - m) * common // 2
    a_denominator = denominator * denominator * factor
    a_integer = t * a_denominator // 2
    v_integer = vcap_integer = fcap_integer = 0
    centered_selected = []
    peak_u_bits, peak_a_bits = abs(u_integer).bit_length(), abs(a_integer).bit_length()
    selected_d_sum = F(0)
    for row in transcript:
        q_integer = row["issued_dyadic_probability"]["numerator"]
        v_integer += q_integer * (denominator - q_integer)
        fcap_integer += max(q_integer * q_integer, (denominator - q_integer) ** 2)
        if not row["purchased"]:
            vcap_integer += max(q_integer, denominator - q_integer)
    a_integer -= v_integer * factor
    peak_a_bits = max(peak_a_bits, abs(a_integer).bit_length())
    for row in selected:
        d = row["d_selected"]
        d_integer = d * denominator
        if d_integer.denominator != 1:
            raise AssertionError("Selected d lost its source dyadic denominator.")
        r_integer = d_integer.numerator - denominator // 2
        r = F(r_integer, denominator)
        if arm["kind"] == "adaptive":
            tickets = allocations[row["block"]]["selected_tickets"]
            total = 2 * b
        else:
            tickets, total = 1, b
        scale = factor // tickets
        if factor % tickets:
            raise AssertionError("The actual propensity cannot use the declared common denominator.")
        u_integer += (total - tickets) * scale * r_integer
        a_integer += total * scale * r_integer * denominator
        peak_u_bits = max(peak_u_bits, abs(u_integer).bit_length())
        peak_a_bits = max(peak_a_bits, abs(a_integer).bit_length())
        selected_d_sum += d
        centered_selected.append({**row, "r_selected": r,
                                  "centered_U_piece": (1 / row["selected_propensity"] - 1) * r,
                                  "centered_A_piece": r / row["selected_propensity"]})
    u, a = F(u_integer, common), F(a_integer, a_denominator)
    v_sum = F(v_integer, denominator * denominator)
    if u != F(t - m, 2) + sum((r["centered_U_piece"] for r in centered_selected), F(0)):
        raise AssertionError("Centered signed U accumulation disagrees with exact fractions.")
    if a != F(t, 2) - v_sum + sum((r["centered_A_piece"] for r in centered_selected), F(0)):
        raise AssertionError("Centered signed A accumulation disagrees with exact fractions.")
    correction = selected_d_sum - v_sum
    if a - u != correction:
        raise AssertionError("Public common-deviation correction identity failed.")
    if arm["kind"] == "uniform" and u != baseline["U_selected_total"]:
        raise AssertionError("Uniform centering must leave the action estimator unchanged.")
    q_integer_sum = 0
    ranges = []
    for k in range(m):
        block = transcript[k * b:(k + 1) * b]
        widths = []
        for offset, row in enumerate(block):
            q_integer = row["issued_dyadic_probability"]["numerator"]
            if arm["kind"] == "adaptive":
                tickets = b + 1 if offset == allocations[k]["favorite"] else 1
                total = 2 * b
            else:
                tickets, total = 1, b
            widths.append(total * (factor // tickets) * abs(denominator - 2 * q_integer))
        width_integer = max(widths)
        width = F(width_integer, common)
        if width > s_bound:
            raise AssertionError("Predictable block width exceeds its source-known S.")
        q_integer_sum += width_integer * width_integer
        ranges.append({"arm": arm["name"], "block": k, "width_C": width,
                       "width_common_numerator": width_integer, "width_common_denominator": common,
                       "first_maximizing_offset": widths.index(width_integer),
                       "public_predictability": "Frozen block's issued q and complete uniform/ticket probability vector; no labels in the width."})
    q_sum = F(q_integer_sum, common * common)
    original_radius = s_bound * B.ceil_sqrt(2 * m)
    fixed_lambda = F(8, original_radius)
    radius = q_sum / original_radius + F(original_radius, 2)
    if q_sum > m * s_bound * s_bound or radius > original_radius:
        raise AssertionError("Fixed-lambda realized-Q bound exceeded the conservative integer radius.")
    vcap, fcap = F(vcap_integer, denominator), F(fcap_integer, denominator * denominator)
    action_radius = B.ceil_sqrt(2 * (t - m))
    mean_raw, terminal_raw, brier_raw = u + radius, u + radius + action_radius, a + radius
    mean_clipped, terminal_clipped, brier_clipped = (
        min(vcap, max(F(0), mean_raw)), min(F(t - m), max(F(0), terminal_raw)),
        min(fcap, max(F(0), brier_raw)))
    row = {**baseline, "certificate_method": VERSION,
           "U_centered_total": u, "A_centered_total": a,
           "centering_changes": {"U_centered_minus_U_original": u - baseline["U_selected_total"],
                                 "A_centered_minus_A_original": a - baseline["A_selected_total"],
                                 "uniform_U_identity_verified": arm["kind"] == "uniform"},
           "public_variance_sum": v_sum, "selected_d_sum": selected_d_sum,
           "shared_deviation_public_correction": correction,
           "identity_Ac_minus_Uc_checked": a - u,
           "shared_deviation_identity": "F-Ac = V-Uc because F-V = Ac-Uc = sum_selected d - sum_all q(1-q). The right side is checked using public q and purchased labels only.",
           "centered_integer_accumulators": {
               "U_signed_numerator": u_integer, "U_denominator": common,
               "A_signed_numerator": a_integer, "A_denominator": a_denominator,
               "Q_numerator": q_integer_sum, "Q_denominator": common * common,
               "peak_U_signed_magnitude_bits": peak_u_bits, "peak_A_signed_magnitude_bits": peak_a_bits,
               "Q_numerator_bits": q_integer_sum.bit_length(),
               "scope": "Raw exact accumulator widths only; signed arithmetic and Fraction/radius intermediates require their own tariff if deployed."},
           "Q_realized_predictable_width_sum": q_sum,
           "baseline_integer_sampling_radius_R": original_radius,
           "fixed_lambda": fixed_lambda,
           "lambda_selection": "8/R, with R determined only by declared m and S. No optimization using realized Q, labels, scores or a posthoc delta.",
           "sampling_radius": radius, "action_radius": action_radius,
           "public_deterministic_caps": {"conditional_action_mean": vcap, "immutable_brier": fcap,
                                         "realized_terminal": t - m},
           "conditional_action_mean_upper_raw": mean_raw,
           "conditional_action_mean_upper_clipped": mean_clipped,
           "realized_terminal_upper_raw": terminal_raw, "realized_terminal_upper_clipped": terminal_clipped,
           "immutable_brier_upper_raw": brier_raw, "immutable_brier_upper_clipped": brier_clipped,
           "strictly_below_trivial_cap": {"conditional_action_mean": mean_clipped < t - m,
                                         "realized_terminal": terminal_clipped < t - m,
                                         "immutable_brier": brier_clipped < t},
           "strictly_below_public_deterministic_cap": {"conditional_action_mean": mean_clipped < vcap,
                                                       "immutable_brier": brier_clipped < fcap},
           "clipping": "Upper bounds clipped below by zero; V/F use their pointwise public caps. Realized terminal count uses only T-m, never the conditional-mean cap.",
           "coverage_scope": "Under the centered fair-bit proof contract, the shared sampling event supports V and F together; one additional fixed-end action tail yields joint terminal+Brier at least19/20 for one arm. This is not an anytime terminal claim or simultaneous23-arm coverage."}
    return row, centered_selected, ranges


def archive_ranges(path, rows):
    payload = b"".join((json.dumps(row, sort_keys=True, separators=(",", ":"), default=str) + "\n").encode() for row in rows)
    info = zipfile.ZipInfo("public_block_ranges.jsonl", date_time=(1980, 1, 1, 0, 0, 0))
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr(info, payload, compresslevel=9)
    with zipfile.ZipFile(path) as archive:
        if archive.read(info.filename) != payload:
            raise AssertionError("Public predictable-range output archive mismatch.")
    receipt = {"status": "PASS", "archive": path.name, "bytes": path.stat().st_size,
               "sha256": B.sha(path.read_bytes()), "member": info.filename, "rows": len(rows),
               "member_bytes": len(payload), "member_sha256": B.sha(payload),
               "verification": "Canonical raw rows byte-identical on ZIP readback; per-member CRC verified.",
               "loose_raw_jsonl_written": False}
    B.write(path.with_name("public_block_ranges_manifest.json"), receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-public-stage", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out, baseline_dir = Path(args.out).resolve(), Path(args.baseline_public_stage).resolve()
    out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter_ns()
    uniform_plan_path, adaptive_plan_path = UNIFORM / "run_001/sources/run_plan_v1.json", ADAPTIVE / "sources/allocation_run_plan_v1.json"
    seal_path = baseline_dir / "public_stage_complete.json"
    reader = B.PublicReader((uniform_plan_path, adaptive_plan_path, seal_path), {})
    rows, all_selected, all_ranges = [], [], []
    result = {"status": "FAIL", "stage": "DEVELOPMENT", "version": VERSION, "principal_clock_credit_ns": 0}
    try:
        baseline_seal = reader.metadata(seal_path)
        if baseline_seal["status"] != "PASS" or baseline_seal["rows"] != 23 or baseline_seal["private_score_reads_before_closure"] != 0:
            raise AssertionError("The original public-only diagnostic must already be complete.")
        definitions = B.uniform_arms(reader.metadata(uniform_plan_path)) + B.adaptive_arms(reader.metadata(adaptive_plan_path))
        uniform_archive = UNIFORM / "raw_traces_v1.zip"
        prefix = B.rel(UNIFORM / "run_001/learner_arms")
        allowlists = {uniform_archive: {"RAW_EVIDENCE_MANIFEST.json"}}
        receipt_paths = []
        for arm in definitions:
            if arm["kind"] == "uniform":
                allowlists[uniform_archive].update({f"{prefix}/{arm['name']}/transcript.jsonl", f"{prefix}/{arm['name']}/purchase_invoices.jsonl"})
            else:
                path = ADAPTIVE / "learner_arms" / arm["name"] / "public_raw.zip"
                allowlists[path] = {"MANIFEST.json", "transcript.jsonl", "purchase_invoices.jsonl", "allocation_records.jsonl"}
                receipt_paths.append(path.with_name("public_raw_manifest.json"))
        initial_events = reader.events
        reader = B.PublicReader((uniform_plan_path, adaptive_plan_path, seal_path, UNIFORM / "raw_archive_manifest_v2.json", *receipt_paths), allowlists)
        reader.events.extend(initial_events)
        sources = [reader.digest_only(path, "calculator_or_design_binding") for path in (Path(__file__), HERE / "calculate_public.py", DESIGN, B.DESIGN)]
        for directory, names in ((UNIFORM / "run_001/sources", ("07_selective_feedback.py", "07_selective_feedback_service.py", "07_computation_adapter.py", "07_selective_feedback_development.py")),
                                 (ADAPTIVE / "sources", ("07_selective_feedback_allocation.py", "07_selective_feedback.py", "07_selective_feedback_service.py", "07_computation_adapter.py", "07_selective_feedback_allocation_development.py"))):
            sources.extend(reader.digest_only(directory / name, "scientific_source_binding") for name in names)
        authoritative = reader.metadata(UNIFORM / "raw_archive_manifest_v2.json")
        uniform_binding = reader.digest_only(uniform_archive, "opaque_archive_binding")
        if uniform_binding["bytes"] != authoritative["archive_bytes"] or uniform_binding["sha256"] != authoritative["archive_sha256"]:
            raise AssertionError("Uniform archive differs from authoritative manifestv2.")
        manifest, manifest_event = reader.member(uniform_archive, "RAW_EVIDENCE_MANIFEST.json")
        members = {r["archive_path"]: r for r in manifest["files"]}
        if members != {r["archive_path"]: r for r in authoritative["files"]}:
            raise AssertionError("Uniform public manifest payload records changed.")
        B.write(out / "protocol.json", {
            "stage": "DEVELOPMENT", "started_utc": B.utc(), "command": sys.argv,
            "baseline_public_stage_seal": baseline_seal, "source_bindings": sources,
            "public_member_allowlists": {B.rel(p): sorted(names) for p, names in allowlists.items()},
            "first_stage": "Independent centered calculation from the same allowlisted public archive members. No private summary, score, unbought label or policy execution.",
            "lambda": "Fixed8/R from declared m,S; realized Q only enters Q/R+R/2 after lambda is fixed.",
            "coverage_scope": "Per-arm centered shared-sampling-event proof contract; joint fixed-end terminal+Brier19/20 after one action tail. No joint23-arm or anytime-terminal statement; fixed MT seeds do not establish coverage.",
            "archive_hash_scope": "Opaque whole-container SHA256; only allowlisted public members are decompressed/deserialized.",
            "analysis_cost_scope": "Offline analysis only. No free deployed calculator, invoice adjustment or resource improvement is claimed.",
            "environment": {"python": sys.version, "platform": platform.platform()}, "principal_clock_credit_ns": 0,
        })
        for arm in definitions:
            allocations = None
            if arm["kind"] == "uniform":
                archive, archive_binding = uniform_archive, uniform_binding
                q_name, r_name = (f"{prefix}/{arm['name']}/{n}" for n in ("transcript.jsonl", "purchase_invoices.jsonl"))
                transcript, q_event = reader.member(archive, q_name, members[q_name])
                receipts, r_event = reader.member(archive, r_name, members[r_name])
                member_bindings = [manifest_event, q_event, r_event]
                expected_private_sha, policy_hashes = manifest["run_result_sha256"], None
            else:
                archive = ADAPTIVE / "learner_arms" / arm["name"] / "public_raw.zip"
                archive_binding = reader.digest_only(archive, "opaque_archive_binding")
                saved_receipt = reader.metadata(archive.with_name("public_raw_manifest.json"))
                if archive_binding["sha256"] != saved_receipt["archive_sha256"] or archive_binding["bytes"] != saved_receipt["archive_bytes"]:
                    raise AssertionError("Adaptive public archive differs from its original verified hash.")
                adaptive_manifest, adaptive_manifest_event = reader.member(archive, "MANIFEST.json")
                entries = {r["name"]: r for r in adaptive_manifest["entries"]}
                transcript, q_event = reader.member(archive, "transcript.jsonl", entries["transcript.jsonl"])
                receipts, r_event = reader.member(archive, "purchase_invoices.jsonl", entries["purchase_invoices.jsonl"])
                allocations, a_event = reader.member(archive, "allocation_records.jsonl", entries["allocation_records.jsonl"])
                member_bindings = [adaptive_manifest_event, q_event, r_event, a_event]
                expected_private_sha, policy_hashes = None, adaptive_manifest["source_plan_hashes"]
            bindings = {"archive": archive_binding, "members": member_bindings,
                        "expected_prior_private_result_sha256_from_manifest_only": expected_private_sha,
                        "observed_policy_source_plan_hashes": policy_hashes}
            row, selected, ranges = calculate(arm, transcript, receipts, allocations, bindings)
            rows.append(row)
            all_selected.extend({"arm": arm["name"], **s} for s in selected)
            all_ranges.extend(ranges)
            B.write(out / "progress.json", {"completed_arms": len(rows), "last": arm["name"], "updated_utc": B.utc()})
        for binding in sources:
            if B.sha((ROOT / binding["path"]).read_bytes()) != binding["sha256"]:
                raise RuntimeError("Source or prospective design changed during centered calculation.")
        result.update(status="PASS", rows=rows, source_bindings=sources, all_23_rows_retained=True,
                      new_policy_calls=0, new_service_calls=0, new_rng_calls=0, new_truth_calls=0,
                      certificate_scope="Public-only fixed-lambda formula reconstruction; fresh fair-bit coverage remains a theorem premise, not established by fixed seed agreement.")
    except BaseException as error:
        result.update(error=repr(error), traceback=traceback.format_exc(), completed_rows=rows,
                      disposition="Preserve first-stage failure; do not retry, retune or compare private scores for an incomplete result.")
    result.update(finished_utc=B.utc(), elapsed_runtime_ns=time.perf_counter_ns() - started)
    audit = {"status": result["status"], "events": reader.events, "private_members_deserialized": 0,
             "private_summaries_deserialized": 0, "public_rows_schema_checked": sum(r["T"] for r in rows),
             "selected_labels_consumed": sum(r["m"] for r in rows), "predictable_block_ranges_retained": len(all_ranges),
             "new_labels_computed": 0, "separate_private_stage_not_started_by_this_program": True,
             "scope": "Explicit allowlisted reader and exact public schema; not a general OS information-flow sandbox.",
             "principal_clock_credit_ns": 0}
    B.write(out / "reader_audit.json", audit)
    selected_archive = B.archive_selected(out / "selected_observations.zip", all_selected)
    ranges_archive = archive_ranges(out / "public_block_ranges.zip", all_ranges)
    B.write(out / "result.json", result)
    if result["status"] == "PASS":
        B.write(out / "public_stage_complete.json", {
            "status": "PASS", "closed_utc": B.utc(), "rows": len(rows),
            "result_sha256": B.sha((out / "result.json").read_bytes()),
            "reader_audit_sha256": B.sha((out / "reader_audit.json").read_bytes()),
            "selected_observations_archive_sha256": selected_archive["sha256"],
            "public_block_ranges_archive_sha256": ranges_archive["sha256"],
            "private_score_reads_before_closure": 0,
            "disposition": "Centered public-only stage complete; a separately invoked score comparison may now start.",
        })
    print(json.dumps({"status": result["status"], "rows": len(rows), "private_members_deserialized": 0,
                      "elapsed_runtime_ns": result["elapsed_runtime_ns"]}), flush=True)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
