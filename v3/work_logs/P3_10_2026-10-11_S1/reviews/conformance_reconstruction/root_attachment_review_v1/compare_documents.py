"""Read-only document/status comparison; no scientific execution or result recomputation.

Contributor: ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction.
Own output only. A first failure, if any, is preserved; existing output is never reused.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import traceback

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
W = REPO / "v3/work_logs/P3_10_2026-10-11_S1"
OUT = HERE / "run_01"


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def write(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def main():
    OUT.mkdir(exist_ok=False)
    write("start.json", {
        "reviewer": "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction",
        "started_utc": utc(), "scope": "document/status/residual equality and evidence hash bindings only",
        "scientific_executions": 0, "principal_clock_credit_ns": 0,
        "source_sha256": digest(Path(__file__).read_bytes()),
    })
    checks = []
    bindings = []

    def check(label, ok):
        checks.append({"check": label, "pass": bool(ok)})
        if not ok:
            raise AssertionError(label)

    def read(path, snapshot=None):
        data = path.read_bytes()
        bindings.append({"path": str(path.relative_to(REPO)), "bytes": len(data), "sha256": digest(data)})
        if snapshot:
            (OUT / snapshot).write_bytes(data)
        return data

    try:
        prior_bytes = read(REPO / "v3/checkpoints/B_1_R_P3_B_B.v1.json", "accepted_overlay.reviewed.json")
        check("accepted checkpoint pinned bytes", digest(prior_bytes) == "4dbff438e98fcdf2abd03abd29596ecbc5b99f22557e0d7d20374f05049d5677")
        prior = json.loads(prior_bytes)
        root_bytes = read(W / "duty_evidence_attachment.json", "root_attachment.reviewed.json")
        root = json.loads(root_bytes)
        markdown = read(W / "duty_evidence_attachment.md", "root_attachment.reviewed.md").decode()
        read(W / "build_duty_attachment.py", "root_builder.reviewed.py")
        conf = json.loads(read(HERE.parent / "duty_attachment_v1/output/attachment.json"))
        broker = json.loads(read(W / "reviews/broker_reconstruction/broker_duty_evidence_attachment_A1.json"))
        conf_by = {r["id"]: r for r in conf["duties"]}
        broker_by = {r["id"]: r for r in broker["duties"]}
        ids = [r["id"] for r in prior["duties"]]
        check("exact 21-duty ordered roster", len(ids) == len(set(ids)) == 21 and [r["id"] for r in root["duties"]] == ids)
        check("declared duty count", root["duty_count"] == 21)
        check("accepted overlay binding", root["accepted_overlay"] == {"path": "v3/checkpoints/B_1_R_P3_B_B.v1.json", "bytes": len(prior_bytes), "sha256": digest(prior_bytes)})
        rows = []
        for accepted, row in zip(prior["duties"], root["duties"]):
            rid = accepted["id"]
            retained = row["accepted_record_retained_verbatim"]
            check(rid + " entire prior object exact", retained == accepted)
            check(rid + " authoritative change false", row["authoritative_status_change"] is False)
            check(rid + " independent conformance attachment exact", row["independent_conformance_attachment"] == conf_by[rid])
            check(rid + " independent broker attachment exact", row["independent_broker_attachment"] == {k: v for k, v in broker_by[rid].items() if k != "prior_record_retained_verbatim"})
            status_line = "Accepted status retained: `" + accepted["status"] + "`."
            check(rid + " markdown status exact once", markdown.count(status_line) == 1)
            evidence_line = "**Evidence (" + row["P3_10_endpoint_scope"] + ").** " + row["P3_10_finite_evidence"]
            check(rid + " markdown evidence exact once", markdown.count(evidence_line) == 1)
            boundary_line = "**Interpretation.** " + row["P3_10_interpretation_and_retained_boundary"]
            check(rid + " markdown interpretation exact once", markdown.count(boundary_line) == 1)
            rows.append({
                "id": rid, "accepted_status": accepted["status"],
                "entire_record_canonical_sha256": digest(canonical(accepted)),
                "residual_canonical_sha256": digest(canonical(accepted["limitations_and_open_obligations"])),
                "prior_status_exact": retained["prior_status"] == accepted["prior_status"],
                "scope_exact": retained["scope"] == accepted["scope"],
                "inherited_scope_exact": retained["inherited_scope_retained"] == accepted["inherited_scope_retained"],
                "residual_exact": retained["limitations_and_open_obligations"] == accepted["limitations_and_open_obligations"],
            })
        check("markdown complete ordered 21-duty headings", re.findall(r"^## ([A-Z][0-9]{2}) —", markdown, flags=re.M) == ids)
        check("zero status and residual changes", root["accepted_statuses_changed"] == root["accepted_residuals_changed"] == 0)
        check("historical metadata not asserted current", root["accepted_overlay_historical_metadata_treated_as_current"] is False)
        check("no new paid execution", root["new_paid_executions"] == 0)
        check("Q3 remains open", root["Q3_affirmative_strongest_ordinary_advantage"] == "OPEN")
        check("P3-N01 scope unchanged", root["P3_N01"] == "SUPPORTED at the accepted modest formal-adaptation and implementation-synthesis scope")
        check("later selections absent", root["P3_11"] == "unstarted" and root["P3_C"] == root["P3_D"] == "unattempted")
        check("amended conformance type retained", root["conformance_status"] == "post-exposure amended inherited conformance")
        check("original completion absent and prefix cost unknown", root["original_public_complete"] is False and root["original_failed_prefix_exact_cost"] is None)
        evidence_bindings = []
        for expected in root["new_evidence_bindings"]:
            data = read(REPO / expected["path"])
            actual = {"path": expected["path"], "bytes": len(data), "sha256": digest(data)}
            check("declared evidence byte binding: " + expected["path"], actual == expected)
            evidence_bindings.append(actual)
        supporting = [
            HERE.parent / "REVIEW.md",
            HERE.parent / "assumption_matrix_v1/output/matrix.md",
            HERE.parent / "results_sections_6_7_review_v1/review.md",
            HERE.parent / "gate_architecture_observation_review_v1/REVIEW.md",
            HERE.parent / "transfer_review_v1/REVIEW.md",
        ]
        for path in supporting:
            read(path)
        check("root JSON unchanged during document comparison", (W / "duty_evidence_attachment.json").read_bytes() == root_bytes)
        write("results.json", {
            "schema": "P3-10-independent-duty-attachment-document-review-v1",
            "status": "PASS", "signed_utc": utc(),
            "reviewer": "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction",
            "scope": "document/status/residual comparison; no numerical result recomputation",
            "duties": rows, "duties_checked": 21,
            "prior_objects_changed": 0, "accepted_statuses_changed": 0,
            "accepted_residuals_changed": 0, "checks": checks, "checks_total": len(checks),
            "declared_evidence_bindings_checked": evidence_bindings,
            "source_bindings": bindings, "scientific_executions": 0,
            "principal_clock_credit_ns": 0, "author_gate_changed": False,
        })
        print(json.dumps({"status": "PASS", "duties": 21, "checks": len(checks), "scientific_executions": 0, "result_sha256": digest((OUT / "results.json").read_bytes())}))
    except Exception as error:
        write("failure.json", {"signed_utc": utc(), "type": type(error).__name__, "message": str(error), "traceback": traceback.format_exc(), "checks": checks, "source_bindings": bindings})
        raise


if __name__ == "__main__":
    main()
