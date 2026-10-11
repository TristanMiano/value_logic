"""Compare saved documentary/chronology records to the reviewed results draft.

No scientific method, private scorer, production analyzer, or observer is imported
or executed. This is record comparison and deterministic document parsing only.
"""
from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
import json
import traceback

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
W = REPO / "v3/work_logs/P3_10_2026-10-11_S1"
FROZEN = REPO / "v3/experiments/frozen_v1"
ORIGINAL = REPO / "v3/experiments/final_v1"
AMENDED = REPO / "v3/experiments/final_v1_amended_A1"
OUT = HERE / "record_comparison_01"


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return sha256(data).hexdigest()


def write(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def main():
    OUT.mkdir(exist_ok=False)
    write("start.json", {"signed_utc": utc(), "reviewer": "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction", "scope": "saved document and execution metadata comparison", "source_sha256": digest(Path(__file__).read_bytes()), "scientific_executions": 0, "principal_clock_credit_ns": 0})
    checks = []
    bindings = []

    def check(label, ok):
        checks.append({"check": label, "pass": bool(ok)})
        if not ok:
            raise AssertionError(label)

    def read(path):
        b = path.read_bytes()
        bindings.append({"path": str(path.relative_to(REPO)), "bytes": len(b), "sha256": digest(b)})
        return b

    def load(path):
        return json.loads(read(path))

    try:
        draft_bytes = read(HERE / "results.reviewed.md")
        check("reviewed snapshot pin", digest(draft_bytes) == "48b0f0dac6e06566206381edefd0e8bf094a3d252b5e95f448bbdb319f5be338")
        text = draft_bytes.decode()
        section8 = text.split("## 8. Execution", 1)[1].split("## 9.", 1)[0]
        commands = [
            ("Original inputs", "inputs", 0),
            ("Original public", "public", 1),
            ("A1 public", "P3-10-A1/public", 0),
            ("A1 evaluation", "P3-10-A1/evaluation", 0),
            ("A1 analysis", "P3-10-A1/analysis", 0),
        ]
        row_records = []
        completions = []
        for label, rel, rc in commands:
            path = W / "commands" / rel
            start = load(path / "start.json")
            end = load(path / "completion.json")
            completions.append(end)
            check(label + " start object exact", start["observed"] == end["start"])
            check(label + " command exact", start["command"] == end["command"])
            check(label + " expected return code", end["returncode"] == rc)
            check(label + " measured wall ns", end["end"]["monotonic_ns"] - end["start"]["monotonic_ns"] == end["wall_ns"])
            check(label + " stable recorded boot", end["start"]["boot_id"] == end["end"]["boot_id"] == "0aa2a50c-3819-4728-bbd8-b8743f8bc121")
            rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in section8.splitlines() if line.startswith("| " + label + " |")]
            check(label + " exactly two table rows", len(rows) == 2)
            timing, resources = rows
            interval = end["start"]["utc"][11:26] + "–" + end["end"]["utc"][11:26]
            check(label + " exact UTC interval", timing[1] == interval)
            check(label + " exact displayed wall seconds", Decimal(timing[3]) * Decimal(10**9) == end["wall_ns"])
            check(label + " table return code", ("exit " + str(rc)) in timing[2])
            check(label + " exact user CPU", Decimal(resources[1]) == Decimal(str(end["child_user_cpu_seconds"])))
            check(label + " exact system CPU", Decimal(resources[2]) == Decimal(str(end["child_system_cpu_seconds"])))
            check(label + " exact peak RSS", int(resources[3].replace(",", "")) == end["child_peak_rss_kib"])
            for stream, filename in [("stdout", "stdout.json"), ("stderr", "stderr.txt")]:
                data = read(path / filename)
                check(label + " " + stream + " byte count", len(data) == end[stream + "_bytes"])
                check(label + " " + stream + " digest", digest(data) == end[stream + "_sha256"])
            row_records.append({"label": label, "record_path": str((path / "completion.json").relative_to(REPO)), "utc_start": end["start"]["utc"], "utc_end": end["end"]["utc"], "wall_ns": end["wall_ns"], "returncode": rc, "child_user_cpu_seconds": end["child_user_cpu_seconds"], "child_system_cpu_seconds": end["child_system_cpu_seconds"], "child_peak_rss_kib": end["child_peak_rss_kib"], "stderr_bytes": end["stderr_bytes"]})
        for previous, current in zip(completions, completions[1:]):
            check("recorded command chronology " + current["start"]["utc"], previous["end"]["monotonic_ns"] < current["start"]["monotonic_ns"])
        check("three amended stderr streams empty", all(r["stderr_bytes"] == 0 for r in completions[2:]))
        check("original stderr 3193 bytes", completions[1]["stderr_bytes"] == 3193)

        entry = load(W / "entry_inventory.json")
        entry_observation = load(W / "entry_observation.json")
        check("entry commit recorded", entry["base_commit"] == "ea3e20dd9889c2ee22141c17390595867d33d8ab" and entry["base_commit"] in section8)
        check("entry tree recorded", entry["base_tree"] == "3900e2333e1324af72b0b7f51764bfecc79794ba" and entry["base_tree"] in section8)
        check("saved remote match assertion", entry["local_and_remote_main_match"] is True)
        check("entry platform", entry_observation["platform"] == "Linux-6.18.44-x86_64-with-glibc2.39")
        check("entry boot matches commands", entry_observation["boot_id"] == completions[0]["start"]["boot_id"])
        freeze_bytes = read(FROZEN / "manifest.json")
        freeze = json.loads(freeze_bytes)
        check("freeze manifest digest", digest(freeze_bytes) == "69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70")
        check("machine protocol pin", freeze["protocol_sha256"] == "dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f")
        check("50 source records; 12 groups; 500 units", len(freeze["sources"]) == 50 and freeze["expected_groups"] == 12 and freeze["expected_public_units"] == 500)
        methods_bytes = read(FROZEN / "methods.json")
        check("prepared methods byte binding", digest(methods_bytes) == freeze["prepared_methods_sha256"])
        check("114 prepared representations", len(json.loads(methods_bytes)["methods"]) == 114)
        runtime_bytes = read(FROZEN / "runtime.json")
        check("runtime byte binding", digest(runtime_bytes) == freeze["runtime_sha256"])
        runtime = json.loads(runtime_bytes)
        check("frozen implementation platform", runtime["byteorder"] == "little" and runtime["implementation"] == "cpython" and runtime["version"] == [3, 12, 14] and runtime["system"] == "Linux")
        check("recorded compiler", "Clang 22.1.3" in runtime["full_version"] and runtime["full_version"] == entry_observation["python"])

        failure_bytes = read(ORIGINAL / "stages/public/attempts/attempt_01/failure.json")
        failure = json.loads(failure_bytes)
        check("failure type and named unit", failure["error_type"] == "AttributeError" and failure["failed_unit_id"] == "conformance_structural_legacy__counterpossible_tied_minima__candidate")
        check("reported failure time", failure["observed_utc"] == "2026-10-11T15:20:33.505276+00:00")
        check("no automatic retry", failure["automatic_retry"] is False)
        amendment_bytes = read(REPO / "v3/experiments/amendments/P3_10_A1/manifest.json")
        amendment = json.loads(amendment_bytes)
        check("amendment digest", digest(amendment_bytes) == "36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359")
        check("amendment original failure binding", amendment["original_failure_sha256"] == digest(failure_bytes))
        check("1365 inventoried original files", len(amendment["original_evidence"]) == 1365)
        check("134825103 inventoried original bytes", sum(r["bytes"] for r in amendment["original_evidence"]) == 134825103)
        check("amendment sealed before continuation", amendment["sealed_utc"] < completions[2]["start"]["utc"])
        check("no new input generation", amendment["new_input_generations"] == 0)
        check("manifest exact 440 and 60 rosters", len(amendment["reused_public_unit_ids"]) == 440 and len(amendment["remaining_public_units"]) == 60)
        check("original incomplete and no private start at amendment", amendment["original_public_stage_complete"] is False and amendment["original_private_evaluation_started"] is False and amendment["original_failed_prefix_cost"] == "unknown")

        stage_records = []
        for root, stage, count in [(ORIGINAL, "inputs", 12), (AMENDED, "public", 60), (AMENDED, "evaluation", 500), (AMENDED, "analysis", 1)]:
            path = root / "stages" / stage / "complete.json"
            record = load(path)
            check(stage + " stage count " + str(count), record["completed_units"] == record["expected_units"] == len(record["seals"]) == count)
            stage_records.append({"path": str(path.relative_to(REPO)), "count": count})
        for stage in ["public", "evaluation", "analysis"]:
            check("original " + stage + " completion still absent", not (ORIGINAL / "stages" / stage / "complete.json").exists())
        composite_bytes = read(AMENDED / "composite_public.json")
        composite = json.loads(composite_bytes)
        check("composite counts and status", composite["original_units"] == 440 and composite["amended_units"] == 60 and composite["completed_units"] == composite["expected_units"] == len(composite["seals"]) == 500 and composite["original_public_stage_complete"] is False)
        check("exact mixed evidence classes", sum(r["evidence_class"] == "original_prospective_unchanged_public_record" for r in composite["seals"]) == 440 and sum(r["evidence_class"] == "post_exposure_amended_inherited_conformance" for r in composite["seals"]) == 60)
        input_bytes = read(AMENDED / "input_reference.json")
        inputs = json.loads(input_bytes)
        check("12 unchanged input references", inputs["new_generations"] == 0 and inputs["completed_units"] == inputs["expected_units"] == len(inputs["seals"]) == 12)
        release = load(W / "completion_release_A1.json")
        check("explicit release timestamp", release["recorded_utc"] == "2026-10-11T15:37:22.120309+00:00")
        check("release after analysis end", release["monotonic_ns"] > completions[-1]["end"]["monotonic_ns"])
        check("release bound composite and input refs", release["lineage"]["composite_public_sha256"] == digest(composite_bytes) and release["lineage"]["input_reference_sha256"] == digest(input_bytes))
        check("release permissions and original status", release["principal_authorized_completed_stage_observation"] is True and release["all_public_evaluation_analysis_complete"] is True and release["original_public_complete"] is False)
        for name in ["reviews/freeze_review/verify_receipt.json", "reviews/freeze_review/review.json", "decision_service_interpretation.md", "decision_service_interpretation_addendum.md", "reviews/certificate_reconstruction/cost_uncertainty_source_review_v1/review.md", "reviews/conformance_reconstruction/root_attachment_review_v1/REVIEW.md", "reviews/conformance_reconstruction/root_attachment_review_v1/run_01/results.json", "reviews/conformance_reconstruction/assumption_matrix_v1/output/matrix.md", "reviews/conformance_reconstruction/REVIEW.md", "reviews/broker_reconstruction/broker_reconstruction_review_A1.md", "reviews/broker_reconstruction/results_sections_1_5_review_v1/REVIEW.md"]:
            read(W / name)
        write("results.json", {"schema": "P3-10-independent-final-prose-saved-record-comparison-v1", "status": "PASS", "signed_utc": utc(), "reviewer": "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction", "scope": "source-bound draft and recorded metadata only; no empirical recomputation", "reviewed_results_sha256": digest(draft_bytes), "checks_total": len(checks), "checks": checks, "command_rows": row_records, "stage_counts": stage_records, "source_bindings": bindings, "scientific_executions": 0, "principal_clock_credit_ns": 0, "live_results_current_sha256_at_end": digest((REPO / "v3/experiments/results.md").read_bytes()), "future_revisions_not_covered": True})
        print(json.dumps({"status": "PASS", "checks": len(checks), "result_sha256": digest((OUT / "results.json").read_bytes())}))
    except Exception as error:
        write("failure.json", {"signed_utc": utc(), "type": type(error).__name__, "message": str(error), "traceback": traceback.format_exc(), "checks": checks, "source_bindings": bindings})
        raise


if __name__ == "__main__":
    main()
