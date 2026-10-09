"""Post-comparison exact identity and sealed-output integrity audit.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. DEVELOPMENT, zero principal credit.
Reads only completed analysis outputs after both private comparison stages;
no policy, source service, RNG or label computation. Statistical inequalities
are summarized, never required as a seeded pass/fail condition.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import zipfile


HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_output_archive(directory, archive_name, manifest_name):
    archive_path = directory / archive_name
    manifest = read(directory / manifest_name)
    assert archive_path.stat().st_size == manifest["bytes"] and sha(archive_path) == manifest["sha256"]
    with zipfile.ZipFile(archive_path) as archive:
        payload = archive.read(manifest["member"])
        assert archive.testzip() is None
    assert len(payload) == manifest["member_bytes"]
    assert hashlib.sha256(payload).hexdigest() == manifest["member_sha256"]
    assert len(payload.splitlines()) == manifest["rows"]
    return {"path": str(archive_path.relative_to(HERE)), "bytes": archive_path.stat().st_size,
            "sha256": sha(archive_path), "raw_member_bytes": len(payload), "rows": manifest["rows"], "crc": "PASS"}


def main():
    baseline_dir, centered_dir = HERE / "public_stage_001", HERE / "centered_public_stage_001"
    baseline, centered = read(baseline_dir / "result.json"), read(centered_dir / "result.json")
    comparison = read(HERE / "centered_comparison_stage_001/result.json")
    baseline_comparison = read(HERE / "comparison_stage_001/result.json")
    assert all(r["status"] == "PASS" for r in (baseline, centered, comparison, baseline_comparison))
    assert all(len(r["rows"]) == 23 for r in (baseline, centered, comparison, baseline_comparison))
    seals, archives = [], []
    for directory in (baseline_dir, centered_dir):
        seal = read(directory / "public_stage_complete.json")
        assert sha(directory / "result.json") == seal["result_sha256"]
        assert sha(directory / "reader_audit.json") == seal["reader_audit_sha256"]
        audit = read(directory / "reader_audit.json")
        assert audit["private_members_deserialized"] == audit["private_summaries_deserialized"] == 0
        assert audit["selected_labels_consumed"] == 10664
        assert audit["public_rows_schema_checked"] == 49600
        for event in audit["events"]:
            if event["mode"] == "public_archive_member":
                assert not any(word in event["member"] for word in ("private_evaluator", "postclosed_evaluator", "/controls/"))
        archives.append(check_output_archive(directory, "selected_observations.zip", "selected_observations_manifest.json"))
        assert archives[-1]["sha256"] == seal["selected_observations_archive_sha256"]
        seals.append(seal)
    archives.append(check_output_archive(centered_dir, "public_block_ranges.zip", "public_block_ranges_manifest.json"))
    assert archives[-1]["sha256"] == seals[-1]["public_block_ranges_archive_sha256"]
    rows = []
    for row in centered["rows"]:
        old = next(r for r in baseline["rows"] if r["name"] == row["name"])
        saved = next(r for r in comparison["rows"] if r["name"] == row["name"])
        v = F(saved["comparisons"]["conditional_action_mean"]["saved_private_score"])
        f = F(saved["comparisons"]["immutable_brier"]["saved_private_score"])
        uc, ac = F(row["U_centered_total"]), F(row["A_centered_total"])
        correction = F(row["shared_deviation_public_correction"])
        assert ac - uc == correction == f - v
        assert v - uc == f - ac
        if row["kind"] == "uniform":
            assert uc == F(old["U_selected_total"])
        radius = F(row["sampling_radius"])
        q, r = F(row["Q_realized_predictable_width_sum"]), row["baseline_integer_sampling_radius_R"]
        assert radius == q / r + F(r, 2) <= r
        rows.append({"name": row["name"], "kind": row["kind"], "shared_public_correction": correction,
                     "saved_private_F_minus_V": f - v, "identical_sampling_residual": v - uc,
                     "fixed_lambda": row["fixed_lambda"], "baseline_sampling_radius": r,
                     "centered_sampling_radius": radius,
                     "conditional_upper_reduction_from_baseline": F(old["conditional_action_mean_upper_clipped"]) - F(row["conditional_action_mean_upper_clipped"]),
                     "terminal_upper_reduction_from_baseline": F(old["realized_terminal_upper_clipped"]) - F(row["realized_terminal_upper_clipped"]),
                     "brier_upper_reduction_from_baseline": F(old["immutable_brier_upper_clipped"]) - F(row["immutable_brier_upper_clipped"])})
    output = {"status": "PASS", "stage": "DEVELOPMENT", "recorded_utc": datetime.now(timezone.utc).isoformat(),
              "kind": "Read-only post-comparison pathwise identity and output-integrity check, not a statistical coverage test.",
              "rows": rows, "public_stage_seals": seals, "archives": archives,
              "archive_total_bytes": sum(a["bytes"] for a in archives),
              "source_sha256": sha(Path(__file__)),
              "baseline_result_sha256": sha(baseline_dir / "result.json"),
              "centered_result_sha256": sha(centered_dir / "result.json"),
              "centered_private_comparison_sha256": sha(HERE / "centered_comparison_stage_001/result.json"),
              "checks": {"both_public_stages_opened_no_private_members_or_summaries": True,
                         "all_23_public_corrections_match_private_target_differences": True,
                         "all_23_sampling_residuals_are_shared": True,
                         "all_20_uniform_centered_U_equals_original_U": True,
                         "all_centered_sampling_radii_at_most_original_R": True},
              "statistical_boundary": "No pass criterion required a sampled score to fall below a probabilistic upper bound. The reported fixed-seed inequalities remain descriptive, without joint23-arm coverage.",
              "new_policy_calls": 0, "new_service_calls": 0, "new_rng_calls": 0, "new_truth_calls": 0,
              "principal_clock_credit_ns": 0}
    path = HERE / "shared_identity_audit.json"
    with path.open("x") as stream:
        stream.write(json.dumps(output, indent=2, default=str) + "\n")
    print(json.dumps({"status": "PASS", "rows": len(rows), "all_23_shared_deviation_identities": True,
                      "archive_total_bytes": output["archive_total_bytes"], "output_sha256": sha(path)}))


if __name__ == "__main__":
    main()
