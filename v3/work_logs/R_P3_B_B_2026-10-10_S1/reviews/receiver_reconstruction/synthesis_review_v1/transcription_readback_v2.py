"""Read saved CSV/JSON evidence and compare a captured Markdown synthesis.

No worker, analyzer, policy or proof checker is imported or executed.
"""
from collections import Counter, defaultdict
from pathlib import Path
import csv
import hashlib
import json
import sys


ROOT = Path(sys.argv[1]).resolve()
HERE = Path(__file__).resolve().parent
BASE = ROOT / "v3/work_logs/R_P3_B_B_2026-10-10_S1/development"
INPUTS = {}


def read(path):
    raw = path.read_bytes()
    INPUTS[str(path.relative_to(ROOT))] = {
        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    return raw.decode("utf-8")


def rows(path):
    return list(csv.DictReader(read(path).splitlines()))


def table(text):
    answer = {}
    for line in text.splitlines():
        if line.startswith("|"):
            cells = [s.strip().replace("**", "") for s in line.split("|")[1:-1]]
            answer[cells[0]] = cells[1:]
    return answer


def number(text):
    return int(text.replace(",", ""))


DRAFT = read(HERE / "source/v3/experiments/certificate_delivery.md")
primary = rows(BASE / "primary_analysis_v1/totals.csv")
requests = rows(BASE / "primary_analysis_v1/per_request.csv")
secondary = rows(BASE / "secondary_analysis_v1/totals.csv")
secondary_requests = rows(BASE / "secondary_analysis_v1/per_request.csv")
primary_analysis = json.loads(read(BASE / "primary_analysis_v1/analysis.json"))
lookup = {(r["stream"], r["recipient"], r["method"]): r for r in primary}
secondary_lookup = {(r["stream"], r["method"]): r for r in secondary}
families = {"Constant": "constant_n3", "Parity": "parity_reassociation_n6",
            "Complement k3": "complementary_k3_n5", "Complement k5": "complementary_k5_n7"}
methods = ["P-REUSE", "P-FRESH", "O-ADD-COLD", "O-ADD-WARM",
           "O-ENUM-RECEIVER", "O-ADD-PORTFOLIO"]
primary_table = table(DRAFT.split("### 3.1", 1)[1].split("### 3.2", 1)[0])
for label, stream in families.items():
    for recipient in ("resident", "fresh"):
        actual = [number(x) for x in primary_table[label + " / " + recipient]]
        expected = [int(lookup[stream, recipient, m]["total_units"]) for m in methods]
        assert actual == expected, (label, recipient, actual, expected)
        assert expected[4] < min(expected[:4] + expected[5:])

crossing_table = table(DRAFT.split("### 3.2", 1)[1].split("### 3.3", 1)[0])
for label in ("Parity", "Complement k3"):
    actual = [number(x) for x in crossing_table[label + " / resident"]]
    entry = next(r for r in primary_analysis["crossings"]
                 if r["stream"] == families[label] and r["recipient"] == "resident"
                 and r["comparator"] == "O-ADD-COLD")
    assert actual == entry["comparator_minus_portfolio_by_prefix"]

threshold_labels = {"P-REUSE": "P-REUSE", "P-FRESH": "P-FRESH",
                    "ADD cold": "O-ADD-COLD", "ADD warm": "O-ADD-WARM",
                    "Direct ordinary": "O-ENUM-RECEIVER", "ADD–portfolio": "O-ADD-PORTFOLIO"}
threshold_table = table(DRAFT.split("### 3.4", 1)[1].split("## 4.", 1)[0])
threshold_counts = {}
for label, method in threshold_labels.items():
    subset = [r for r in requests if r["method"] == method]
    assert len(subset) == 48
    counts = [sum(int(r["consumer_units"]) + 1024 <= cap for r in subset)
              for cap in (2**20, 2**22, 2**24)]
    assert threshold_table[label] == [f"{counts[0]} / 48", f"{counts[1]} / 48"]
    assert counts[1] == counts[2] == 48
    threshold_counts[method] = counts

pruning_table = table(DRAFT.split("## 4.", 1)[1].split("## 5.", 1)[0])
aggregate = [[0, 0] for _ in range(3)]
for label, stream in families.items():
    pair = [secondary_lookup[stream, m] for m in ("O-ADD-WARM", "O-ADD-WARM-PRUNED")]
    expected = [[int(r[key]) for r in pair]
                for key in ("proof_output_bytes", "total_units", "consumer_units")]
    actual = [[number(x.strip()) for x in cell.split("→")]
              for cell in pruning_table[label]]
    assert actual == expected, (label, actual, expected)
    for i, values in enumerate(expected):
        for j, value in enumerate(values):
            aggregate[i][j] += value
assert [[number(x.strip()) for x in cell.split("→")]
        for cell in pruning_table["All 24"]] == aggregate

paired = defaultdict(dict)
for r in secondary_requests:
    if r["method"] in ("O-ADD-WARM", "O-ADD-WARM-PRUNED"):
        paired[r["stream"], r["request_index"]][r["method"]] = r
pruning_counts = Counter()
for key, pair in paired.items():
    full, pruned = (pair[m] for m in ("O-ADD-WARM", "O-ADD-WARM-PRUNED"))
    assert int(pruned["total_units"]) > int(full["total_units"])
    delta_bytes = int(pruned["proof_bytes"]) - int(full["proof_bytes"])
    delta_consumer = int(pruned["consumer_units"]) - int(full["consumer_units"])
    if key[1] == "1":
        assert delta_bytes == 0 and delta_consumer == 3
        pruning_counts["unchanged_first_packet_plus_three_consumer_units"] += 1
    else:
        assert delta_bytes < 0 and delta_consumer < 0
        pruning_counts["later_packet_and_consumer_reduction"] += 1

primary_records = [json.loads(line) for line in read(BASE / "primary_v5/completed_units.jsonl").splitlines()]
direct = [r for r in primary_records if r.get("method") == "O-ENUM-RECEIVER"]
screening = defaultdict(Counter)
for row in direct:
    key = row["stream"] + "/" + row["recipient"]
    work = row["work"]
    screening[key]["requests"] += 1
    screening[key]["screened_requests"] += int(work.get("global_interval_shortcuts", 0) > 0)
    screening[key]["enumerated_requests"] += int(work.get("enumerated_assignments", 0) > 0)
    screening[key]["assignments"] += work.get("enumerated_assignments", 0)
assert len(direct) == 48
source_fees = Counter(int(r["source_units"]) for r in requests if r["request_index"] == "1")
assert source_fees == {430041: 48}

rational_records = [json.loads(line) for line in read(HERE / "observed_rational_completed_units_df3e500eac31c649b9afa3fc285b3d5428ed157ced94e2a63c462ff6bc92f69f.jsonl").splitlines()]
rational_rows = [r for r in rational_records if "method" in r and "invoice" in r]
rational_groups = defaultdict(list)
for row in rational_rows:
    rational_groups[row.get("case", row.get("request_id"))].append({
        "method": row["method"], "status": row["status"],
        "error": row.get("error"), "total_units": row["invoice"]["total_units"]})
assert len(rational_rows) == 29
rational_integrity = {"observed_rows": 29, "declared_rows": 30, "matches_summary": False,
                      "missing_expected_case": "O-ADD-PORTFOLIO final recovery"}

out = {"scope": "Read-only transcription and saved-counter arithmetic; no worker or policy execution.",
       "principal_clock_credit": 0, "status": "TRANSCRIPTIONS_PASS_RATIONAL_RECORD_INCOMPLETE",
       "rational_integrity": rational_integrity,
       "primary_table_values_compared": 48, "prefix_values_compared": 12,
       "pruning_table_values_compared": 30,
       "consumer_bill_plus_reserve_counts": threshold_counts,
       "pruning_request_patterns": dict(pruning_counts),
       "direct_receiver_saved_work": {k: dict(v) for k, v in sorted(screening.items())},
       "first_request_source_fees": dict(source_fees),
       "rational_saved_outcomes": dict(rational_groups), "inputs": INPUTS}
for path, record in INPUTS.items():
    raw = (ROOT / path).read_bytes()
    assert len(raw) == record["bytes"] and hashlib.sha256(raw).hexdigest() == record["sha256"]
out["all_inputs_unchanged"] = True
target = HERE / "transcription_readback_v2.json"
with target.open("x") as handle:
    json.dump(out, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps({k: out[k] for k in ("status", "primary_table_values_compared", "prefix_values_compared",
                                      "pruning_table_values_compared", "consumer_bill_plus_reserve_counts",
                                      "pruning_request_patterns", "direct_receiver_saved_work", "all_inputs_unchanged")},
                 sort_keys=True))
