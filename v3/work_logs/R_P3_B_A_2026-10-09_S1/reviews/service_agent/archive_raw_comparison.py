"""Deterministic raw-evidence archive; verifies but never deletes originals."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import zipfile
import zlib


ROOT = Path(__file__).resolve().parents[5]
COMPARISON = ROOT / "v3/work_logs/R_P3_B_A_2026-10-09_S1/development/service_comparison"
RUN = COMPARISON / "run_001"
REVIEW = Path(__file__).resolve().parent
ARCHIVE = COMPARISON / "raw_traces_v1.zip"
INTERNAL_MANIFEST = "RAW_EVIDENCE_MANIFEST.json"


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def zip_info(name):
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def build(target, files, manifest_bytes):
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9,
                         allowZip64=True, strict_timestamps=True) as archive:
        archive.writestr(zip_info(INTERNAL_MANIFEST), manifest_bytes, compresslevel=9)
        for row in files:
            archive.writestr(zip_info(row["archive_path"]), (ROOT / row["repository_path"]).read_bytes(),
                             compresslevel=9)


def main():
    candidates = sorted(RUN.rglob("*.jsonl"))
    assert len(candidates) == 96
    allowed_names = {"transcript.jsonl", "purchase_invoices.jsonl", "private_evaluator_labels.jsonl",
                     "postclosed_evaluator_annotations.jsonl", "control_transcript_and_invoices.jsonl"}
    assert all(p.name in allowed_names for p in candidates)
    candidates += [REVIEW / f"service_probe_run_{number:03d}" / "domain_checks.json" for number in (1, 2, 3)]
    candidates = sorted(candidates, key=lambda p: p.relative_to(ROOT).as_posix())
    assert len(candidates) == 99 and len(set(candidates)) == 99
    rows = []
    for path in candidates:
        assert path.is_file() and not path.is_symlink()
        name = path.relative_to(ROOT).as_posix()
        assert not name.startswith("/") and ".." not in Path(name).parts
        rows.append({"repository_path": name, "archive_path": name,
                     "bytes": path.stat().st_size, "sha256": digest(path)})
    raw_manifest = {
        "schema": "value_logic.selective_feedback.raw_evidence_archive.v1",
        "stage": "DEVELOPMENT",
        "scope": "96 completed-comparison JSONL traces/invoices/private annotations and three large new-service correctness domain reports.",
        "run_result_sha256": digest(RUN / "result.json"),
        "run_manifest_sha256": digest(RUN / "manifest.json"),
        "files": rows,
        "direct_records_retained": "Result/summary JSON, source/plan/environment/command receipts, aggregate and denial invoices, selector paths and source snapshots remain outside this archive.",
        "restoration": "Archive paths are repository-relative. Extract to a separate directory for inspection; do not overwrite a newer repository file without comparing its hash.",
    }
    manifest_bytes = (json.dumps(raw_manifest, sort_keys=True, indent=2) + "\n").encode()
    build(ARCHIVE, rows, manifest_bytes)
    second = COMPARISON / "raw_traces_v1.determinism_check.zip"
    build(second, rows, manifest_bytes)
    first_hash, second_hash = digest(ARCHIVE), digest(second)
    assert first_hash == second_hash
    verified = []
    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.namelist() == [INTERNAL_MANIFEST] + [r["archive_path"] for r in rows]
        assert archive.read(INTERNAL_MANIFEST) == manifest_bytes
        assert archive.testzip() is None
        for row in rows:
            path = ROOT / row["repository_path"]
            original_digest, archived_digest = hashlib.sha256(), hashlib.sha256()
            matched_bytes = 0
            with path.open("rb") as original, archive.open(row["archive_path"]) as stored:
                while True:
                    left, right = original.read(1024 * 1024), stored.read(1024 * 1024)
                    assert left == right
                    if not left:
                        break
                    matched_bytes += len(left)
                    original_digest.update(left)
                    archived_digest.update(right)
            assert matched_bytes == row["bytes"]
            assert original_digest.hexdigest() == archived_digest.hexdigest() == row["sha256"]
            verified.append({**row, "byte_for_byte_equal": True, "sha256_verified": True})
    second.unlink()  # Only this newly created reproducibility-check archive.
    public_manifest = {
        **raw_manifest,
        "archive_repository_path": ARCHIVE.relative_to(ROOT).as_posix(),
        "archive_bytes": ARCHIVE.stat().st_size,
        "archive_sha256": first_hash,
        "embedded_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "candidate_removal_count": len(rows),
        "candidate_removal_total_bytes": sum(r["bytes"] for r in rows),
        "originals_deleted": False,
        "removal_guard": "Root may remove only these exact repository paths after rechecking archive SHA and each original SHA. All original files still exist at this verification boundary.",
    }
    (COMPARISON / "raw_archive_manifest_v1.json").write_text(json.dumps(public_manifest, indent=2) + "\n")
    verification = {
        "schema": "value_logic.selective_feedback.raw_archive_verification.v1",
        "status": "PASS", "stage": "DEVELOPMENT", "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "archive_sha256": first_hash, "archive_bytes": ARCHIVE.stat().st_size,
        "archive_entries": len(rows) + 1, "raw_files": len(rows),
        "raw_total_bytes": sum(r["bytes"] for r in rows),
        "deterministic_rebuild_sha256": second_hash, "deterministic_rebuild_identical": True,
        "zip_crc_check": "PASS", "embedded_manifest_verified": True,
        "every_entry_byte_for_byte_equal_to_original": True,
        "every_entry_sha256_matches_original_and_manifest": True,
        "originals_deleted": False, "verified_files": verified,
        "builder_source_sha256": digest(Path(__file__).resolve()),
        "python": platform.python_version(), "zlib": zlib.ZLIB_VERSION,
        "determinism_scope": "Identical fixed entry order, 1980 timestamps, Unix 0644 metadata and level-9 deflate; identical rebuild verified in the recorded Python/zlib runtime.",
        "principal_clock_credit_ns": 0,
    }
    (COMPARISON / "raw_archive_verification_v1.json").write_text(json.dumps(verification, indent=2) + "\n")
    print(json.dumps({k: verification[k] for k in ("status", "archive_sha256", "archive_bytes", "raw_files",
                                                   "raw_total_bytes", "deterministic_rebuild_identical", "originals_deleted")}, indent=2))


if __name__ == "__main__":
    main()
