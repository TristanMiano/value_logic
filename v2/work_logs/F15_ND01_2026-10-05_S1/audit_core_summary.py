"""Independently check the report's core counts/means and calibration labels.

Reads saved artifacts only. Contributor: ChatGPT (GPT-6 Astra Pro), ND01 audit.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[3]
SESSION = Path(__file__).resolve().parent
ANALYSIS = ROOT / "v2/experiments/F15_ND01_analysis"
RUN = ROOT / "v2/work_logs/F15_ND01_v1_run1/evaluation_attempt_1"


def main():
    checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(message)

    def close(a, b, message):
        check(math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12), message)

    summary_path = ANALYSIS / "core_summary.json"
    summary_bytes = summary_path.read_bytes()
    x = json.loads(summary_bytes)
    check(x["development_only"] and x["original_F15_result_unchanged"], "Evidence status differs")
    expected_counts = {"calibration_interval_rows": 560, "calibration_oracle_rows": 50,
                       "calibration_searched_rows": 1000, "constructed_function_equivalent_layouts": 5,
                       "fixed_ordinary_models": 5, "mask_methods": 4, "mask_rows": 200,
                       "search_rows": 1000, "search_variants": 20}
    check(x["counts"] == expected_counts, "Cartesian population counts differ")
    tables = []
    for item in x["table_manifest"]:
        path = ANALYSIS / item["file"]
        raw = path.read_bytes()
        check(len(raw) == item["bytes"] and hashlib.sha256(raw).hexdigest() == item["sha256"], "Table hash mismatch")
        count = sum(1 for _ in csv.DictReader(raw.decode().splitlines()))
        expected = {"calibration_rows.csv": 1050, "mask_rows.csv": 200, "search_rows.csv": 1000}[path.name]
        check(count == expected, "Exported CSV count mismatch")
        tables.append({"file": item["file"], "rows": count, "sha256": item["sha256"]})

    searches = [json.loads((RUN / f"search_{i}_evaluation.json").read_text()) for i in range(5)]
    masks = [json.loads((RUN / f"soft_mask_{i}_evaluation.json").read_text()) for i in range(5)]
    for reported in x["search"]["variants"]:
        roles = [r for result in searches for r in result["evaluated"][reported["method"]]["role_summaries"]]
        close(reported["mean_mae"], mean(r["equal_stratum_mean_mae"] for r in roles), "Search summary MAE differs")
        close(reported["mean_role_worst_stratum_mae"], mean(r["worst_stratum_mae"] for r in roles), "Search worst MAE differs")
        point_flags = [r["descriptive_error_and_decision_thresholds_met"] for r in roles]
        check(reported["roles_meeting_all_error_and_decision_point_thresholds"] == sum(point_flags), "Search role count differs")
        check(reported["models_with_both_roles_meeting_point_thresholds"] == sum(all(point_flags[2*i:2*i+2]) for i in range(5)), "Search model count differs")
        check(reported["formal_support_assessed"] is False and reported["point_thresholds_are_not_complete_F15_endpoint"] is True,
              "Search summary incorrectly became full support")
    for reported in x["masks"]["methods"]:
        method = reported["method"]
        point_flags, pooled = [], []
        for result in masks:
            for role in (0, 1):
                rows = [r for r in result["rows"] if r["role"] == role and r["method"] == method]
                close(len(rows), 5, "Missing mask strata")
                point_flags.append(all(r["mae"] <= .05 for r in rows) and
                    all(r["decision_disagreement"] <= (.35 if r["stratum"] == "mixed_near" else .10)
                        for r in rows if r["stratum"] in ("mixed_near", "mixed_far")))
                pooled.append(mean(r["mae"] for r in rows))
        close(reported["mean_mae"], mean(pooled), "Mask summary MAE differs")
        check(reported["roles_meeting_all_error_and_decision_point_thresholds"] == sum(point_flags), "Mask role count differs")
        check(reported["models_with_both_roles_meeting_point_thresholds"] == sum(all(point_flags[2*i:2*i+2]) for i in range(5)), "Mask model count differs")
        check(reported["formal_support_assessed"] is False and reported["point_thresholds_are_not_complete_F15_endpoint"] is True,
              "Mask summary incorrectly became full support")

    assessment = json.loads((RUN / "calibration_assessment.json").read_text())
    original_intervals = {}

    def walk(value):
        if isinstance(value, dict):
            if all(k in value for k in ("id", "mean", "n", "radius", "lower", "upper", "sample_range")):
                if value["id"] in original_intervals:
                    check(original_intervals[value["id"]] == value, "Repeated interval ID has different contents")
                original_intervals[value["id"]] = value
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(assessment)
    check(len(original_intervals) == 560, "Original 560 intervals were not recovered")
    seen = set()
    statuses = dict(supported=0, inconclusive=0, violated=0)
    for row in x["calibration"]["interval_rows"]:
        key = row["id"]
        check(key not in seen and key in original_intervals, "Missing/duplicate summary interval")
        seen.add(key)
        for field in ("mean", "n", "radius", "lower", "upper"):
            close(row[field], original_intervals[key][field], "Summary interval differs from original")
        if key.endswith("/base_normalized_regret"):
            direction, threshold = "at_most", .05 / 1.375
        elif key.endswith("/disagreement"):
            direction, threshold = "at_most", .10 if "/mixed_far/" in key else .35
        elif key.endswith("/separating_frequency"):
            direction, threshold = "at_least", .90
        elif key.endswith("/advantage") or key.endswith("/same_identity_subset_advantage"):
            direction, threshold = "at_least", .01
        else:
            direction, threshold = "at_most", .05
        check(row["direction"] == direction, "Interval threshold direction differs")
        close(row["threshold"], threshold, "Interval threshold differs")
        if direction == "at_most":
            status = "supported" if row["upper"] <= threshold else "violated" if row["lower"] > threshold else "inconclusive"
        else:
            status = "supported" if row["lower"] >= threshold else "violated" if row["upper"] < threshold else "inconclusive"
        check(row["status"] == status, "Three-way interval status differs")
        statuses[status] += 1
    check(seen == set(original_intervals), "Summary omitted interval IDs")
    check(x["calibration"]["all_interval_status_counts"] == {**statuses, "n": 560}, "Interval status totals differ")
    check(x["calibration"]["complete_endpoint_layouts"] == 0, "Complete calibration count differs")
    identity = next(r for r in x["calibration"]["hypothesis_outcome_counts"] if r["hypothesis"] == "identity")
    check(identity["adequate_layouts"] == 5 and identity["selective_layouts"] == 0, "Calibration adequacy/selectivity differs")

    output = {"schema": "f15-nd01-independent-core-summary-audit-v1", "passed": True,
              "checks": checks, "core_summary_sha256": hashlib.sha256(summary_bytes).hexdigest(),
              "counts": expected_counts, "tables": tables, "calibration_interval_status_counts": statuses,
              "scope": "Independent check of all exported table counts/hashes, 20 search and four mask aggregate means and distinct role/model counts, and all560 calibration interval values/thresholds/statuses against original saved evaluations. No populations, model fits or selections generated.",
              "reviewer": "ChatGPT (GPT-6 Astra Pro), independent ND01 protocol audit"}
    path = SESSION / "audit_core_summary.json"
    with path.open("x") as handle:
        json.dump(output, handle, indent=2)
        handle.write("\n")
    Path(str(path) + ".sha256").write_text(hashlib.sha256(path.read_bytes()).hexdigest() + "\n")
    print(json.dumps({"passed": True, "checks": checks, "core_summary_sha256": output["core_summary_sha256"]}))


if __name__ == "__main__":
    main()
