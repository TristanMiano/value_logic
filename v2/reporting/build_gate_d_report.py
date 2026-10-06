"""Build or check Gate D's versioned report-to-evidence map.

Contributor: ChatGPT (GPT-6 Astra Pro). Read-only scientific verification;
never trains a model, generates a population or modifies an earlier report map.
The F17 map describes its preserved snapshot. D explicitly binds a later report.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION = Path("v2/work_logs/D_2026-10-06_S1")
OUTPUT = Path("v2/reporting/D_1/claim_map.json")
SOURCE_COMMIT = "f7aa0bef07cb21da9336429426244f6e944644a4"
ENTRY_REPORT_SHA = "18c45d7df537c6e8a076793c9e38412e5c8d887995ba041d2ee9cbf51971bc8d"
CURRENT_REPORT_SHA = "c8f490ce94584fc93d27b759f1f524d5eeeb0d3885729d24db413cb4f5205c5d"
ENTRY_MAP_SHA = "53b1fe17adf46aaf4c6443efffe7bcad1f6d9f4451c0e3eed30556584ae28218"
HISTORICAL_SNAPSHOT = Path("v2/work_logs/F17_2026-10-06_S1/drafts/report_v2.md")


def binding(path):
    path = Path(path)
    data = (REPO / path).read_bytes()
    return {"path": path.as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def load(path):
    return json.loads((REPO / path).read_text())


def verify_historical_bindings(value):
    """Resolve the earlier report pointer at its explicitly preserved epoch."""
    count = 0
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            path = HISTORICAL_SNAPSHOT if value["path"] == "paper_v2.md" else value["path"]
            actual = binding(path)
            assert actual["sha256"] == value["sha256"], value["path"]
            if "bytes" in value:
                assert actual["bytes"] == value["bytes"], value["path"]
            count += 1
        count += sum(verify_historical_bindings(v) for v in value.values())
    elif isinstance(value, list):
        count += sum(verify_historical_bindings(v) for v in value)
    return count


def build():
    current = binding("paper_v2.md")
    assert current["sha256"] == CURRENT_REPORT_SHA, "A changed report needs a new explicit review disposition."
    snapshot = binding(SESSION / "drafts/report_final.md")
    assert snapshot["sha256"] == CURRENT_REPORT_SHA
    assert binding(HISTORICAL_SNAPSHOT)["sha256"] == ENTRY_REPORT_SHA
    old_path = Path("v2/reporting/F17_v1/claim_map.json")
    old_binding = binding(old_path)
    assert old_binding["sha256"] == ENTRY_MAP_SHA, "Preserve F17's historical map."
    old = load(old_path)
    historical_checked = verify_historical_bindings(old)
    assert historical_checked == 145

    claims = deepcopy(old["claims"])
    assert len(claims) == len({row["id"] for row in claims}) == 42
    revised = [row for row in claims if row["id"] == "F17-MATH-13"]
    assert len(revised) == 1
    claim = revised[0]
    before = "For two nonproportional positive profiles,"
    after = ("For two profiles with strictly positive nonproportional attempt-price "
             "vectors c,d and nonnegative terminal penalties M,N,")
    assert claim["statement"].count(before) == 1
    claim["statement"] = claim["statement"].replace(before, after)
    claim["scope"].append("Nonproportionality is required of c,d themselves; differing terminal penalties alone are insufficient.")
    claim["revision"] = {"id": "D-CON-01", "classification": "source-backed report hypothesis clarification",
                         "source_theorem_changed": False,
                         "review": str(SESSION / "reviews/contribution/review_final_spacing.json")}

    reviews = [binding(SESSION / path) for path in [
        "reviews/contribution/review_initial.json",
        "reviews/contribution/review_final.json",
        "reviews/contribution/review_final_spacing.json",
        "reviews/editorial/review_final.json",
        "reviews/editorial/editorial_evidence.json",
        "reviews/editorial/lineage_evidence.json",
        "reviews/integrity/entry_audit_attempt2.json",
        "principal_review.md",
    ]]
    result = {
        "schema": "Gate-D-report-claim-map-v1",
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "source_commit": SOURCE_COMMIT,
        "report": current, "reviewed_snapshot": snapshot,
        "claim_count": len(claims), "claims": claims,
        "historical_F17_map": old_binding,
        "historical_F17_report": binding(HISTORICAL_SNAPSHOT),
        "historical_bindings_checked": historical_checked,
        "version_policy": "F17 is immutable historical evidence. Its canonical-path report binding resolves to its saved report_v2 snapshot; all other original bindings resolve to unchanged current files.",
        "current_reviews": reviews,
        "tables": binding("v2/reporting/F17_v1/tables.json"),
        "bibliography": binding("v2/reporting/F17_v1/references.bib"),
        "builder": binding(Path(__file__).relative_to(REPO)),
        "revision_scope": [
            "Nine rejected operatorname occurrences replaced with upright names; explicit rank and supremum spacing preserves meaning.",
            "Theorem 3 and introduction specify nonproportional attempt-price vectors, as required by the unchanged accepted theorem.",
            "Author byline and contribution roles follow saved model-attribution evidence.",
            "Reproducibility links identify the current report version while preserving the original assembly evidence.",
        ],
        "evidence_transfer": "The other 41 claim groups and all original supporting evidence transfer unchanged. The clarification narrows an ambiguous report phrase to its source theorem; no experiment, endpoint or scientific source changed.",
        "new_scientific_execution": False,
        "gate_D_assessment_performed": True,
        "gate_D_author_decision": "PENDING",
        "coverage": "42 substantive claim groups; an evidence index with internal fixed-snapshot review, not proof-assistant verification.",
    }
    return (json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    path = REPO / OUTPUT
    if args.check:
        assert path.read_bytes() == data, "Saved Gate D claim map differs."
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(data)
    print(json.dumps({"status": "checked" if args.check else "created",
                      "path": str(OUTPUT), "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest(),
                      "claims": 42, "historical_bindings": 145,
                      "scientific_execution": False}))


if __name__ == "__main__":
    main()
