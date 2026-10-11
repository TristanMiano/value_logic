#!/usr/bin/env python3
"""Exact postprocessing of the completed independent conformance observation.

Contributor: ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction.
No producer, paid worker, private scorer, analyzer, or observer is imported/run.
This compares saved independent results with the preserved pre-data expectations,
aggregates their exact declared costs, and extracts three hash-bound examples.
It writes exclusively into a fresh owned derived_v1 directory and preserves failure.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import traceback

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
READS = {}
AUTHOR = "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction"
MODES = ("known", "unknown_offset", "unknown_scale", "unknown_affine")


def binding(path):
    data = path.read_bytes()
    return {"path": path.relative_to(REPO).as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def read(path):
    got = binding(path)
    READS[got["path"]] = got
    return json.loads(path.read_bytes())


def save(path, value):
    with path.open("x") as file:
        json.dump(value, file, indent=2, sort_keys=True, allow_nan=False)
        file.write("\n")


def main():
    out = HERE / "derived_v1"
    out.mkdir(exist_ok=False)
    save(out / "start.json", {"contributor": AUTHOR,
         "started_utc": datetime.now(timezone.utc).isoformat(),
         "source": binding(Path(__file__)), "principal_clock_credit_seconds": 0,
         "scope": "Pure saved-result aggregation, pre-data expectation comparison, and example extraction"})
    try:
        result = read(HERE / "runs/attempt_01/result.json")
        start = read(HERE / "runs/attempt_01/start.json")
        theory = read(HERE / "theory_expectations_v1.json")
        release = read(HERE / "completion_release_A1.json")
        assert result["status"] == "PASS" and result["observer_version"] == 4
        assert start["observer_sha256"] == binding(HERE / "observer_v4.py")["sha256"] == "172aee16c019122fe3feaae12e0601cf41681f070a7ed7761c08fa7bedf227a8"
        assert release["principal_authorized_completed_stage_observation"] is True
        assert release["all_public_evaluation_analysis_complete"] is True
        assert release["amendment_manifest_sha256"] == "36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359"
        assert datetime.fromisoformat(theory["created_utc"]) < datetime.fromisoformat(release["recorded_utc"]) < datetime.fromisoformat(start["started_utc"])
        complete = read(REPO / "v3/experiments/final_v1_amended_A1/stages/analysis/complete.json")
        assert complete["expected_units"] == complete["completed_units"] == len(complete["seals"]) == 1
        seal_path = REPO / "v3/experiments/final_v1_amended_A1" / complete["seals"][0]["path"]
        seal = read(seal_path)
        assert READS[seal_path.relative_to(REPO).as_posix()]["sha256"] == release["analysis_seal_sha256"] == complete["seals"][0]["sha256"]

        observed = {(r["case_name"], r["calibration"]): r for r in result["rows"] if "calibration" in r}
        row_comparisons = []
        for expected in theory["expected_information_rows"]:
            actual = observed[(expected["case_name"], expected["calibration"])]
            assert all(actual[k] == v for k, v in expected.items())
            row_comparisons.append({**expected, "all_compared_fields_match": True,
                                    "unit_id": actual["unit_id"]})
        assert len(row_comparisons) == len(observed) == 36
        compared_summary = {}
        for key, value in theory["expected_information_summary"].items():
            if key.startswith("verifier_"):
                actual_key = key
            elif key == "minimum_extra_raw_queries_sum":
                actual_key = "information_minimum_extra_queries_sum"
            else:
                actual_key = "information_" + key
            assert result["summary"][actual_key] == value
            compared_summary[actual_key] = value

        structural = [r for r in result["rows"] if r["engine"] == "legacy_structural"]
        assert len(structural) == 18
        names = list(dict.fromkeys(r["case_name"] for r in structural))
        assert len(names) == 9
        per_method = {}
        for method in ("candidate", "ordinary"):
            rows = [r for r in structural if r["method"] == method]
            assert len(rows) == theory["expected_structural"]["per_method_exact_outputs"] == 9
            assert sum(r["decision_status"] == "INFEASIBLE" for r in rows) == theory["expected_structural"]["per_method_infeasible_complete_reports"] == 2
            assert sum(r["decision_status"] == "CHECKED_COMPLETE" for r in rows) == theory["expected_structural"]["per_method_nonempty_action_warrants"] == 7
            per_method[method] = {"scheduled_units": len(rows)}
            for key in ("cold_units", "local_units"):
                total = sum(r[key] for r in rows)
                per_method[method][key + "_sum"] = total
                per_method[method][key + "_mean"] = str(F(total, len(rows)))
        for name, (action, loss) in theory["expected_structural"]["routing_fixed_actions"].items():
            decision = result["structural_reconstructed_outputs"][name]["decision"]
            assert decision["action"] == action and decision["fixed_action_worst_loss"] == loss
        tied = result["structural_reconstructed_outputs"]["counterpossible_tied_minima"]
        assert len(tied["sources"][0]["models"]) == theory["expected_structural"]["tied_minima"] == 2
        external = result["structural_reconstructed_outputs"]["external_sources_not_repairs"]
        assert len(external["sources"]) == theory["expected_structural"]["external_source_cases"] == 2
        assert [s["optimal_rank"] for s in external["sources"]] == [["1"], ["2"]]
        assert all(len(s["models"]) == 2 for s in external["sources"])

        structural_table = []
        for name in names:
            methods = {r["method"]: r for r in structural if r["case_name"] == name}
            candidate, ordinary = methods["candidate"], methods["ordinary"]
            assert candidate["expected_output_sha256"] == ordinary["expected_output_sha256"]
            assert candidate["cold_units"] > ordinary["cold_units"]
            assert candidate["local_units"] > ordinary["local_units"]
            terminal = result["structural_reconstructed_outputs"][name]
            row = {"case_name": name, "decision": terminal["decision"],
                   "source_states": [{k: s[k] for k in ("source_id", "models", "optimal_rank")} for s in terminal["sources"]],
                   "candidate": {k: candidate[k] for k in ("cold_units", "local_units")},
                   "ordinary": {k: ordinary[k] for k in ("cold_units", "local_units")},
                   "exact_terminal_agreement": True}
            structural_table.append(row)
        per_method["candidate_minus_ordinary"] = {
            k + "_sum": per_method["candidate"][k + "_sum"] - per_method["ordinary"][k + "_sum"]
            for k in ("cold_units", "local_units")}
        per_method["candidate_over_ordinary"] = {
            k + "_ratio": str(F(per_method["candidate"][k + "_sum"], per_method["ordinary"][k + "_sum"]))
            for k in ("cold_units", "local_units")}

        information_names = list(dict.fromkeys(x["case_name"] for x in theory["expected_information_rows"]))
        information_table = []
        for name in information_names:
            modes = {mode: {k: observed[(name, mode)][k] for k in (
                "full_law_recoverable", "all_targets_recoverable", "target_count",
                "original_targets_recoverable", "original_targets_nonidentified",
                "minimum_extra_raw_queries", "repair_effective_deficit", "effective_rank",
                "normalization_augmented_rank", "counts")} for mode in MODES}
            information_table.append({"case_name": name, "modes": modes})
        rejections = [r for r in result["rows"] if "rejection_name" in r]
        assert len(rejections) == 6 and all(r["defect_observed"] for r in rejections)
        repair_counts = Counter(r["minimum_extra_raw_queries"] for r in observed.values())
        assert repair_counts == {0: 22, 1: 6, 2: 6, 3: 2}

        examples = []
        for suffix in ("rational_signed__unknown_scale", "partial_target_offset__unknown_affine", "brier_anchor__unknown_affine"):
            uid = "conformance_information__" + suffix
            paths = list((REPO / "v3/experiments/final_v1_amended_A1/stages/public/units" / uid).glob("attempt_*/result.json"))
            assert len(paths) == 1
            payload = read(paths[0])
            row = next(r for r in result["rows"] if r["unit_id"] == uid)
            assert READS[paths[0].relative_to(REPO).as_posix()]["sha256"] == row["public_result_sha256"]
            assert payload["unit"]["id"] == uid
            examples.append({"unit_id": uid, "source": READS[paths[0].relative_to(REPO).as_posix()],
                             "certificate": payload["value"]["paid_result"]["certificate"]})
        save(out / "certificate_examples.json", {"schema": "value_logic.p310.conformance_examples.v1",
             "contributor": AUTHOR, "scope": "Examples extracted from the already independently checked 36 certificates",
             "examples": examples})
        save(out / "theory_comparison.json", {"schema": "value_logic.p310.pre_data_theory_comparison.v1",
             "contributor": AUTHOR, "status": "PASS", "principal_clock_credit_seconds": 0,
             "rows_compared": row_comparisons, "summary_fields_compared": compared_summary,
             "structural_scheduled_units": 18, "structural_pre_data_expectations_match": True,
             "observer_attempts": 1, "observer_failures": 0, "producer_or_scorer_invocations": 0})
        tables = {"schema": "value_logic.p310.conformance_tables.v1", "contributor": AUTHOR,
                  "mode_order": list(MODES), "structural": structural_table,
                  "structural_cost_aggregates": per_method, "information": information_table,
                  "information_by_calibration": result["by_calibration"],
                  "repair_query_distribution": dict(sorted(repair_counts.items())),
                  "rejections": rejections, "scheduled_unit_denominator": 60}
        save(out / "tables.json", tables)
        lines = ["# Exact conformance tables", "", "## Structural outputs and declared costs", "",
                 "| Case | Decision / worst loss | Candidate cold | Ordinary cold | Candidate local | Ordinary local |",
                 "|---|---|---:|---:|---:|---:|"]
        for r in structural_table:
            d = r["decision"]
            label = "INFEASIBLE" if d["status"] == "INFEASIBLE" else d["action"] + " / " + d["fixed_action_worst_loss"]
            lines.append("| " + " | ".join([r["case_name"], label,
                f'{r["candidate"]["cold_units"]:,}', f'{r["ordinary"]["cold_units"]:,}',
                f'{r["candidate"]["local_units"]:,}', f'{r["ordinary"]["local_units"]:,}']) + " |")
        lines += ["", "## Information designs across calibration modes", "",
                  "Each cell is full-law recovery / all-target recovery / minimum extra raw queries. Y and N are exact logical verdicts. Modes follow the frozen roster.", "",
                  "| Design | Known | Unknown offset | Unknown scale | Unknown affine |", "|---|---|---|---|---|"]
        for row in information_table:
            cells = []
            for mode in MODES:
                r = row["modes"][mode]
                cells.append(("Y" if r["full_law_recoverable"] else "N") + " / " +
                             ("Y" if r["all_targets_recoverable"] else "N") + " / " + str(r["minimum_extra_raw_queries"]))
            lines.append("| " + " | ".join([row["case_name"]] + cells) + " |")
        with (out / "tables.md").open("x") as file:
            file.write("\n".join(lines) + "\n")
        save(out / "manifest.json", {"schema": "value_logic.p310.postprocessing_manifest.v1",
             "contributor": AUTHOR, "status": "PASS", "principal_clock_credit_seconds": 0,
             "finished_utc": datetime.now(timezone.utc).isoformat(), "source": binding(Path(__file__)),
             "read_bindings": READS,
             "outputs": [binding(p) for p in sorted(out.iterdir()) if p.is_file()],
             "frozen_or_final_files_modified": 0, "paid_or_private_methods_invoked": 0})
        print(json.dumps({"status": "PASS", "observed_units": 60, "theory_rows_matched": 36,
                          "repair_query_distribution": dict(sorted(repair_counts.items())),
                          "structural_cost_aggregates": per_method, "output": str(out)}, sort_keys=True))
    except BaseException as error:
        save(out / "failure.json", {"status": "POSTPROCESSING_FAILURE", "type": type(error).__name__,
             "message": str(error), "traceback": traceback.format_exc(), "read_bindings": READS,
             "official_evidence_modified": False, "principal_clock_credit_seconds": 0})
        raise


if __name__ == "__main__":
    main()
