"""Exact post-score decomposition of selected-receipt reuse. DEVELOPMENT.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
This reads sealed records only. It neither runs a policy nor changes its tariff.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def operations(record, prefix=None, exclude_prefix=None):
    result = Counter()
    for entry in record["operations"]:
        name = entry["operation"]
        if prefix is not None:
            if not name.startswith(prefix):
                continue
            name = name[len(prefix):]
        if exclude_prefix is not None and name.startswith(exclude_prefix):
            continue
        result[(entry["category"], name)] += entry["units"]
    return result


def analyze(run, out):
    run, out = Path(run).resolve(), Path(out).resolve()
    assert not out.exists(), "Use a fresh evidence directory."
    public = json.loads((run / "public_seal.json").read_text())
    private = json.loads((run / "private/seal.json").read_text())
    for row in public["files"]:
        assert digest(run / row["path"]) == row["sha256"]
    for row in private["files"]:
        assert digest(run / "private" / row["path"]) == row["sha256"]
    index = {row["run_id"]: row for row in
             json.loads((run / "public_index.json").read_text())["records"]}
    records = {}
    with gzip.open(run / "public_records.jsonl.gz", "rt") as stream:
        for line in stream:
            row = json.loads(line)
            assert hashlib.sha256(line.rstrip("\n").encode()).hexdigest() == index[row["run_id"]]["record_sha256"]
            records[row["run_id"]] = row
    scores = json.loads((run / "private/scores.json").read_text())
    pairs = []
    for pair in scores["paired_coupling_checks"]:
        cold, cached = records[pair["plain_run"]], records[pair["reuse_run"]]
        ce, ae = cold["episode"], cached["episode"]
        assert ce["status"] == ae["status"] == "success"
        assert ce["trace"] == ae["trace"] and ce["blocks"] == ae["blocks"]
        assert ce["weights"] == ae["weights"]
        assert ce["random_bits_consumed"] == ae["random_bits_consumed"]
        assert cold["source_invoice"] == cached["source_invoice"]
        nonprovider_cold = operations(ce["meter"], exclude_prefix="selected_provider:")
        nonprovider_cached = operations(ae["meter"], exclude_prefix="selected_provider:")
        assert nonprovider_cold == nonprovider_cached
        # The available account changes with the provider bill; paid report
        # operations and totals, rather than the account limit, must agree.
        assert operations(cold["report"]["meter"]) == operations(cached["report"]["meter"])
        assert cold["report"]["meter"]["total"] == cached["report"]["meter"]["total"]
        avoided, overhead, cold_calls, hits = 0, 0, 0, 0
        invoice_aggregate = Counter()
        requests = cached["service_audit"]["requests"]
        assert len(requests) == len(ce["invoices"]) == len(ae["invoices"])
        for original, admitted, request in zip(ce["invoices"], ae["invoices"], requests):
            assert admitted == request["adapter_receipt"]
            assert original["query_id"] == request["query_id"]
            assert original["claim_key"] == admitted["claim_key"]
            assert original["answer"] == admitted["answer"]
            total = admitted["resources"]["total"]
            child = request["cold_receipt"]
            if request["cache_hit"]:
                assert child is None
                hits += 1
                avoided += original["resources"]["total"]
                overhead += total
            else:
                assert child == original
                cold_calls += 1
                child_bill = child["resources"]["total"]
                assert total >= child_bill
                assert operations(admitted["resources"], prefix="selected_cache_cold_provider:") == operations(child["resources"])
                overhead += total - child_bill
            invoice_aggregate.update(operations(admitted["resources"]))
        assert operations(ae["meter"], prefix="selected_provider:") == invoice_aggregate
        saved = ce["meter"]["total"] - ae["meter"]["total"]
        assert saved == avoided - overhead == pair["local_units_saved"]
        assert hits == pair["physical_calls_saved"]
        pairs.append({
            "configuration": cached["configuration"],
            "cold_run": cold["run_id"], "reuse_run": cached["run_id"],
            "logical_selected_receipts": len(requests),
            "physical_cold_calls": cold_calls, "checked_cache_hits": hits,
            "avoided_cold_provider_units": avoided,
            "added_adapter_units": overhead, "net_local_units_saved": saved,
            "source_units_each": cold["source_invoice"]["total"],
            "nonprovider_operations_equal": True,
            "miss_child_invoice_equal_to_original": True,
            "child_and_parent_operation_conservation": True,
            "report_invoice_equal": True,
        })
    assert len(records) == 48 and len(pairs) == 32
    out.mkdir(parents=True)
    result = {
        "stage": "DEVELOPMENT", "analysis": "post-score exact resource decomposition",
        "runs": len(records), "paired_records": len(pairs),
        "less_expensive": sum(p["net_local_units_saved"] > 0 for p in pairs),
        "more_expensive": sum(p["net_local_units_saved"] < 0 for p in pairs),
        "same_cost": sum(p["net_local_units_saved"] == 0 for p in pairs),
        "pair_counts_are_not_independent_trials": True,
        "identity": "net units saved = avoided cold-provider units - added adapter units",
        "public_seal_sha256": digest(run / "public_seal.json"),
        "private_seal_sha256": digest(run / "private/seal.json"),
        "scores_sha256": digest(run / "private/scores.json"), "pairs": pairs,
    }
    (out / "analysis.json").write_text(json.dumps(result, indent=2) + "\n")
    source = Path(__file__).read_bytes()
    (out / Path(__file__).name).write_bytes(source)
    manifest = {"stage": "DEVELOPMENT", "files": [
        {"path": p.name, "bytes": p.stat().st_size, "sha256": digest(p)}
        for p in sorted(out.iterdir())]}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return {k: v for k, v in result.items() if k != "pairs"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(canonical(analyze(args.run, args.out)))
