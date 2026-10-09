"""Read-only verification of the completed three-arm adaptive evidence.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. DEVELOPMENT; zero principal credit.
No learner, service, RNG or private truth call: only existing saved bytes.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / "v3/work_logs/R_P3_B_A_2026-10-09_S1/development/allocation_comparison"
RUN = OUT / "run_001"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), default=str) + "\n").encode()


def invoice(record):
    assert record["total"] == sum(record["by_category"].values())
    assert record["total"] == sum(r["units"] for r in record["operations"])
    by_category = Counter()
    for row in record["operations"]:
        assert row["units"] >= 0
        by_category[row["category"]] += row["units"]
    assert all(by_category[k] == v for k, v in record["by_category"].items())


def info(name):
    result = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    result.compress_type = zipfile.ZIP_DEFLATED
    result._compresslevel = 9
    result.create_system = 3
    result.external_attr = 0o100644 << 16
    return result


def archive(path, expected):
    receipt = read(path.with_name(path.stem + "_manifest.json"))
    assert receipt["status"] == "PASS"
    data = path.read_bytes()
    assert len(data) == receipt["archive_bytes"]
    assert digest(data) == receipt["archive_sha256"]
    manifest = receipt["manifest"]
    assert manifest["source_plan_hashes"] == expected
    rows, raw_bytes = {}, 0
    rebuild = io.BytesIO()
    with zipfile.ZipFile(path) as saved, zipfile.ZipFile(rebuild, "w", compression=zipfile.ZIP_DEFLATED,
                                                       compresslevel=9) as rebuilt:
        assert saved.testzip() is None
        assert saved.namelist() == [e["name"] for e in manifest["entries"]] + ["MANIFEST.json"]
        for entry in manifest["entries"]:
            payload = saved.read(entry["name"])
            raw_bytes += len(payload)
            assert len(payload) == entry["bytes"] and digest(payload) == entry["sha256"]
            lines = payload.splitlines(keepends=True)
            assert len(lines) == entry["rows"]
            parsed = [json.loads(line) for line in lines]
            assert all(canonical(row) == line for row, line in zip(parsed, lines))
            rows[entry["name"]] = parsed
            with rebuilt.open(info(entry["name"]), "w") as target:
                target.write(payload)
        payload = saved.read("MANIFEST.json")
        assert payload == canonical(manifest)
        rebuilt.writestr(info("MANIFEST.json"), payload)
    assert rebuild.getvalue() == data
    return rows, {"path": str(path.relative_to(ROOT)), "bytes": len(data), "sha256": digest(data),
                  "raw_jsonl_bytes": raw_bytes, "entries": manifest["entries"]}


def main():
    result = read(RUN / "result.json")
    assert result["status"] == "PASS" and len(result["learner_arms"]) == 3
    assert result["new_controls"] == 0 and result["initial_probe_repeated"] is False
    expected = result["source_plan_hashes"]
    for path, wanted in expected.items():
        assert digest(Path(path).read_bytes()) == wanted
    sources = RUN / "sources"
    for path, wanted in expected.items():
        source = Path(path)
        if source.suffix == ".py":
            assert digest((sources / source.name).read_bytes()) == wanted
    assert not list(RUN.rglob("*.jsonl"))
    archives, arms = [], []
    for summary in result["learner_arms"]:
        directory = RUN / "learner_arms" / summary["name"]
        assert read(directory / "summary.json") == summary
        public, index = archive(directory / "public_raw.zip", expected)
        archives.append(index)
        private, index = archive(directory / "evaluation_raw.zip", expected)
        archives.append(index)
        transcript, receipts, allocations = (public[n] for n in
                                            ("transcript.jsonl", "purchase_invoices.jsonl", "allocation_records.jsonl"))
        labels, annotations = (private[n] for n in
                               ("private_evaluator_labels.jsonl", "postclosed_evaluator_annotations.jsonl"))
        t, b = summary["horizon"], summary["block_size"]
        assert len(transcript) == len(labels) == len(annotations) == t
        assert len(receipts) == len(allocations) == t // b
        invoice(read(directory / "deployment_invoice.json"))
        invoice(read(directory / "private_evaluator_invoice.json"))
        source_registry = read(directory / "source_registry.json")["resources"]
        invoice(source_registry)
        assert source_registry["total"] == summary["resource_units"]["source_registry"]
        receipt_map = {r["query_id"]: r for r in receipts}
        assert len(receipt_map) == t // b
        purchases = terminal = prospective = 0
        expected_terminal, expected_prospective, brier = F(0), F(0), F(0)
        expert_losses, corrected_losses = [0] * 4, [0] * 4
        for i, (row, truth, annotation) in enumerate(zip(transcript, labels, annotations)):
            q = row["query"]
            assert row["index"] == truth["index"] == annotation["index"] == i
            assert q["query_id"] == truth["query_id"] == annotation["query_id"]
            y = truth["private_label"]
            assert y == annotation["private_label"] and y in (0, 1)
            probability = row["issued_dyadic_probability"]
            numerator, denominator = probability["numerator"], probability["denominator"]
            assert denominator == 1 << summary["action_bits"]
            expected_piece = F(numerator if y == 0 else denominator - numerator, denominator)
            brier_piece = F((numerator - denominator * y) ** 2, denominator ** 2)
            terminal_piece, prospective_piece = int(row["terminal_action"] != y), int(row["prospective_action"] != y)
            if row["purchased"]:
                purchases += 1
                receipt = receipt_map[q["query_id"]]
                invoice(receipt["resources"])
                assert receipt["claim_key"] == q["claim_key"]
                assert receipt["status"] == "success" and receipt["checked"] is True
                assert receipt["answer"] == row["purchased_label"] == row["terminal_action"] == y
                assert allocations[i // b]["selected"] == i % b
            else:
                assert "purchased_label" not in row and q["query_id"] not in receipt_map
            terminal += terminal_piece
            prospective += prospective_piece
            expected_prospective += expected_piece
            expected_terminal += F(0) if row["purchased"] else expected_piece
            brier += brier_piece
            assert annotation["terminal_error"] == terminal_piece
            assert annotation["prospective_error"] == prospective_piece
            assert F(annotation["conditional_prospective_error"]) == expected_piece
            assert F(annotation["conditional_terminal_error"]) == (F(0) if row["purchased"] else expected_piece)
            assert F(annotation["issued_brier"]) == brier_piece
            for j, action in enumerate(row["expert_actions"]):
                expert_losses[j] += action != y
                corrected_losses[j] += (action != y) and not row["purchased"]
        assert purchases == t // b
        ev = summary["evaluation"]
        assert terminal == ev["terminal_sampled_01_loss"]
        assert prospective == ev["prospective_sampled_01_loss"]
        assert expected_terminal == F(ev["conditional_expected_terminal_01_loss"])
        assert expected_prospective == F(ev["conditional_expected_prospective_01_loss"])
        assert brier == F(ev["immutable_issued_brier"])
        assert expert_losses == list(ev["fixed_expert_all_issued_losses"].values())
        assert corrected_losses == list(ev["same_selector_corrected_expert_losses"].values())
        purchased_units = sum(r["resources"]["total"] for r in receipts)
        assert purchased_units == summary["resource_units"]["purchased_checked_services"]
        deployment = read(directory / "deployment_invoice.json")
        component_units = Counter()
        for charge in deployment["operations"]:
            component_units[charge["operation"].split(":", 1)[0]] += charge["units"]
        assert component_units["checked_purchase"] == purchased_units
        assert component_units["standalone_setup"] == source_registry["total"]
        arms.append({"name": summary["name"], "rows_checked": t, "receipts_checked": purchases,
                     "allocation_records_checked": len(allocations), "cold_units": deployment["total"],
                     "terminal_loss": terminal, "conditional_terminal": str(expected_terminal),
                     "issued_brier": str(brier)})
    report = {"status": "PASS", "stage": "DEVELOPMENT", "recorded_utc": datetime.now(timezone.utc).isoformat(),
              "kind": "Read-only saved-evidence audit; no learner, service, private truth or RNG execution.",
              "result_sha256": digest((RUN / "result.json").read_bytes()),
              "audit_source_sha256": digest(Path(__file__).read_bytes()),
              "source_and_plan_hashes_unchanged": True, "source_snapshots_match": True,
              "no_loose_raw_jsonl": True, "archives": archives,
              "archive_bytes_total": sum(a["bytes"] for a in archives),
              "raw_jsonl_bytes_total": sum(a["raw_jsonl_bytes"] for a in archives),
              "verification": "SHA256, CRC, raw entry manifest, canonical JSONL and complete deterministic ZIP rebuild; raw transcript/annotation/receipt identities, actual invoice sums and saved score reconstruction.",
              "arms": arms, "principal_clock_credit_ns": 0}
    (OUT / "saved_archive_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "archive_bytes_total", "raw_jsonl_bytes_total", "result_sha256")}))


if __name__ == "__main__":
    main()
