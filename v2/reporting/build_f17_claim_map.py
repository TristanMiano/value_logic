"""Assemble or verify F17's report-to-evidence map without scientific execution.

Contributor: ChatGPT (GPT-6 Astra Pro). The independently prepared fragments
are preserved verbatim; this file normalizes field names, checks every source
hash, and binds the canonical report and fixed review snapshots.
"""
import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION = Path("v2/work_logs/F17_2026-10-06_S1")
OUTPUT = Path("v2/reporting/F17_v1/claim_map.json")
REPORT_SHA = "18c45d7df537c6e8a076793c9e38412e5c8d887995ba041d2ee9cbf51971bc8d"


def binding(path):
    data = (REPO / path).read_bytes()
    return {"path": str(path), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def build():
    report = binding("paper_v2.md")
    assert report["sha256"] == REPORT_SHA, "A changed report requires explicit new review disposition."
    claims, fragments = [], []
    for area in ["math", "empirical", "literature"]:
        path = SESSION / "reviews" / f"claim_map_{area}.json"
        fragments.append(binding(path))
        data = json.loads((REPO / path).read_text())
        for original in data["claims"]:
            row = {
                "id": original.get("id", original.get("claim_id")),
                "report_locator": original.get("report_locator", {"sections": original.get("section")}),
                "statement": original.get("statement", original.get("precise_claim")),
                "scope": original["scope"], "kind": original["kind"],
                "disposition": original["disposition"],
                "prior_claim_ids": original["prior_claim_ids"],
                "evidence": original["evidence"],
                "source_fragment": str(path),
            }
            for optional in ["proof_coverage", "primary_urls"]:
                if optional in original:
                    row[optional] = original[optional]
            for source in row["evidence"]:
                assert binding(source["path"])["sha256"] == source["sha256"], source["path"]
            claims.append(row)
    assert len(claims) == 42 and len({c["id"] for c in claims}) == 42
    reviews = [binding(SESSION / "reviews" / name) for name in [
        "report_v1_math.json", "report_v1_empirical.json", "report_v1_literature.json",
        "report_v2_math_regression.json", "report_v2_empirical_regression.json",
        "report_v2_literature_regression.json",
    ]]
    metadata_sources = [binding(SESSION / "source_reads" / "writing_guidance.json"),
                        binding(SESSION / "reviews" / "bibliography_record.json")]
    result = {
        "schema": "F17-report-claim-map-v1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "source_commit": "2e44ed1b711508d7ad451e1ca6272ff989deef81",
        "report": report, "claim_count": len(claims), "claims": claims,
        "fragments": fragments, "reviews": reviews,
        "attribution_and_bibliography_evidence": metadata_sources,
        "tables": binding("v2/reporting/F17_v1/tables.json"),
        "bibliography": binding("v2/reporting/F17_v1/references.bib"),
        "builder": binding(Path(__file__).relative_to(REPO)),
        "coverage": "42 substantive claim groups; prose qualifies these groups, while citations and bibliography carry source attribution. This is an evidence index, not proof-assistant verification.",
        "new_scientific_execution": False, "gate_D_performed": False,
    }
    return (json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    path = REPO / OUTPUT
    if args.check:
        assert path.read_bytes() == data, "Saved F17 claim map differs."
    else:
        with path.open("xb") as handle:
            handle.write(data)
    print(json.dumps({"status": "checked" if args.check else "created", "path": str(OUTPUT),
                      "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                      "claims": 42, "scientific_execution": False}))


if __name__ == "__main__":
    main()
