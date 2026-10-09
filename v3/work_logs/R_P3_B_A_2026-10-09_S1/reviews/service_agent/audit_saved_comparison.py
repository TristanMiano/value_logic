"""Read-only arithmetic/binding audit of the already completed comparison."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def lines(path):
    with path.open() as stream:
        return [json.loads(line) for line in stream]


def invoice(record):
    assert record["total"] == sum(record["by_category"].values())
    assert record["total"] == sum(op["units"] for op in record["operations"])
    by_category = Counter()
    for op in record["operations"]:
        assert type(op["units"]) is int and op["units"] >= 0
        by_category[op["category"]] += op["units"]
    assert all(by_category[k] == v for k, v in record["by_category"].items())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    run = Path(args.run).resolve()
    result = read(run / "result.json")
    assert result["status"] == "PASS"
    assert len(result["learner_arms"]) == 20 and len(result["controls"]) == 8
    assert sum(a["kind"] == "main" for a in result["learner_arms"]) == 16
    assert sum(a["kind"] == "variation" for a in result["learner_arms"]) == 4
    for original, expected in result["source_plan_hashes"].items():
        assert digest(run / "sources" / Path(original).name) == expected
    controls = {(c["horizon"], c["name"]): c for c in result["controls"]}
    selector_pairs = {}
    margins = []
    total_rounds = total_purchases = 0
    max_table_units = 0
    for arm in result["learner_arms"]:
        d = run / "learner_arms" / arm["name"]
        closed = read(d / "closed_before_evaluation.json")
        assert closed["transcript_sha256"] == digest(d / "transcript.jsonl")
        assert closed["purchase_invoices_sha256"] == digest(d / "purchase_invoices.jsonl")
        rows = lines(d / "transcript.jsonl")
        annotations = lines(d / "postclosed_evaluator_annotations.jsonl")
        private = lines(d / "private_evaluator_labels.jsonl")
        receipts = lines(d / "purchase_invoices.jsonl")
        assert len(rows) == len(annotations) == len(private) == arm["horizon"]
        assert [r["index"] for r in rows] == list(range(arm["horizon"]))
        bought = [r for r in rows if r["purchased"]]
        assert len(bought) == len(receipts) == arm["contract"]["quota"]
        for row in rows:
            assert "private_label" not in row and "private_residue" not in row
            assert ("purchased_label" in row) == row["purchased"]
        receipt_units = 0
        for row, receipt in zip(bought, receipts):
            assert receipt["query_id"] == row["query"]["query_id"]
            assert receipt["claim_key"] == row["query"]["claim_key"]
            assert receipt["answer"] == row["purchased_label"] == row["terminal_action"]
            assert receipt["status"] == "success" and receipt["checked"] is True
            invoice(receipt["resources"])
            receipt_units += receipt["resources"]["total"]
        for row, annotation, label in zip(rows, annotations, private):
            assert row["query"]["query_id"] == annotation["query_id"] == label["query_id"]
            assert annotation["private_label"] == label["private_label"]
            assert annotation["terminal_error"] == int(row["terminal_action"] != label["private_label"])
        e = arm["evaluation"]
        assert e["terminal_sampled_01_loss"] == sum(a["terminal_error"] for a in annotations)
        assert e["prospective_sampled_01_loss"] == sum(a["prospective_error"] for a in annotations)
        assert F(e["conditional_expected_terminal_01_loss"]) == sum((F(a["conditional_terminal_error"]) for a in annotations), F(0))
        assert F(e["immutable_issued_brier"]) == sum((F(a["issued_brier"]) for a in annotations), F(0))
        assert receipt_units == arm["resource_units"]["purchased_checked_services"]
        for filename in ("deployment_invoice.json", "purchases_aggregate_invoice.json", "private_evaluator_invoice.json"):
            invoice(read(d / filename))
        whole = read(d / "deployment_invoice.json")
        assert whole["total"] == arm["resource_units"]["cold_total"]
        assert not whole["reservations"] and whole["denials"] == 0
        for price, case in e["price_cases"].items():
            assert F(case["realized_cold_total"]) == int(price) * e["terminal_sampled_01_loss"] + F(whole["total"], 1000)
            for name, cost in case["corrected_expert_same_complete_invoice_totals"].items():
                assert F(cost) == int(price) * e["same_selector_corrected_expert_losses"][name] + F(whole["total"], 1000)
        pair = (arm["horizon"], arm["block_size"], arm["seed"])
        path = read(d / "selector_path.json")["selected_offsets"]
        if pair in selector_pairs:
            assert selector_pairs[pair] == path
        else:
            selector_pairs[pair] = path
        table = controls[(arm["horizon"], "quadratic_residue_table")]
        cold_gap = whole["total"] - table["resource_units"]["cold_total"]
        source_specific_lower = 4882 + 11 * arm["horizon"] + receipt_units
        assert cold_gap >= source_specific_lower
        ongoing_gap = arm["resource_units"]["ongoing_including_learner_initialization"] - table["resource_units"]["ongoing_calls"]
        assert ongoing_gap >= 11 * arm["horizon"] + receipt_units
        margins.append({"arm": arm["name"], "cold_resource_gap_to_table": cold_gap,
                        "source_specific_lower": source_specific_lower,
                        "ongoing_gap_before_table_construction": ongoing_gap,
                        "round_and_purchase_only_lower": 11 * arm["horizon"] + receipt_units})
        total_rounds += len(rows)
        total_purchases += len(receipts)
    control_rounds = 0
    for control in result["controls"]:
        d = run / "controls" / f"{control['name']}_T{control['horizon']}"
        rows = lines(d / "control_transcript_and_invoices.jsonl")
        labels = lines(d / "private_evaluator_labels.jsonl")
        assert len(rows) == len(labels) == control["horizon"]
        for row, label in zip(rows, labels):
            receipt = row["result"]
            assert receipt["status"] == "success"
            assert receipt["query_id"] == row["query"]["query_id"] == label["query_id"]
            assert receipt["answer"] == label["private_label"]
            assert receipt["claim_key"] == row["query"]["claim_key"]
            invoice(receipt["resources"])
            if control["name"] == "quadratic_residue_table":
                max_table_units = max(max_table_units, receipt["resources"]["total"])
        invoice(read(d / "deployment_invoice.json"))
        invoice(read(d / "private_evaluator_invoice.json"))
        assert control["resource_units"]["ongoing_calls"] == sum(r["result"]["resources"]["total"] for r in rows)
        assert control["terminal_01_loss"] == 0
        control_rounds += len(rows)
    audit = {"status": "PASS", "stage": "DEVELOPMENT", "kind": "Read-only saved-evidence audit; no new scientific run.",
             "recorded_utc": datetime.now(timezone.utc).isoformat(),
             "completed_learner_arms": 20, "completed_controls": 8,
             "learner_rounds_checked": total_rounds, "purchased_receipts_checked": total_purchases,
             "control_rounds_checked": control_rounds, "paired_selector_paths": len(selector_pairs),
             "maximum_recorded_table_lookup_units": max_table_units,
             "dominance_resource_margins": margins,
             "source_plan_snapshots_verified": result["source_plan_hashes"],
             "result_sha256": digest(run / "result.json"), "audit_source_sha256": digest(Path(__file__).resolve()),
             "principal_clock_credit_ns": 0}
    (run.parent / "saved_evidence_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps({k: v for k, v in audit.items() if k not in {"dominance_resource_margins", "source_plan_snapshots_verified"}}, indent=2))


if __name__ == "__main__":
    main()
