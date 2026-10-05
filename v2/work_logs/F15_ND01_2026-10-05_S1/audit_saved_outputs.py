"""Independent ND01 saved-artifact, chronology and descriptive-statistics audit.

Reads completed artifacts without importing experiment modules, drawing input
populations, fitting models, or selecting replacement alignments. Contributor:
ChatGPT (GPT-6 Astra Pro), independent ND01 protocol audit sub-agent.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SESSION = Path(__file__).resolve().parent
RUN = ROOT / "v2/work_logs/F15_ND01_v1_run1"
HERE = ROOT / "v2/experiments/neural_diagnostic_v1"
KINDS = ("calibration", "search", "soft_mask")
STRATA = ("mixed_near", "mixed_far", "preserve_other", "equal_target", "scale_separating")
MASKS = ("fractional_mask", "rounded_top8", "binary_global", "frozen_original")
EXPECTED = [(kind, index) for kind in KINDS for index in range(5)]
SELF_HASH_SCHEMAS = {
    "f14-neural-discovery-v1", "f15-nd01-fixed-model-search-prepared-v1",
    "f15-nd01-fixed-model-search-evaluated-v1", "f15-nd01-soft-mask-prepared-v1",
    "f15-nd01-soft-mask-validation-v1",
}


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    checks = 0
    hashed = {}

    def require(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(message)

    def close(a, b, message, atol=1e-11):
        require(math.isfinite(float(a)) and math.isfinite(float(b))
                and math.isclose(a, b, rel_tol=1e-11, abs_tol=atol), message)

    def read(path, expected=None):
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        hashed[str(path.relative_to(ROOT))] = {"bytes": len(raw), "sha256": digest}
        if expected is not None:
            require(digest == expected, f"Registered hash mismatch: {path}")
        sidecar = Path(str(path) + ".sha256")
        if sidecar.exists():
            require(sidecar.read_text().strip() == digest, f"Sidecar mismatch: {path}")
        return json.loads(raw)

    manifest = read(HERE / "freeze.json", "9c15af55b83d7edf134542a9c70bcc0f087c6f4f6491f993361a27493b5cf24c")
    config = read(HERE / "config.json", "d65ffe53ca95362599cc785495676a0e84bf003278d760e92a2a7bf8cba1667a")
    for item in [*manifest["files"], *manifest["source_prepared"]]:
        raw = (ROOT / item["path"]).read_bytes()
        require(len(raw) == item["bytes"] and hashlib.sha256(raw).hexdigest() == item["sha256"],
                f"Frozen dependency/source changed: {item['path']}")
    original_manifest = read(ROOT / "v2/experiments/freeze.v1.json",
                             "b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c")
    for name, item in original_manifest["files"].items():
        raw = (ROOT / name).read_bytes()
        require(len(raw) == item["bytes"] and hashlib.sha256(raw).hexdigest() == item["sha256"],
                f"Original F14 file changed: {name}")
    # Check every completed JSON or stage/event record, including both outer
    # artifact hashes and its recorded SHA sidecar.
    run_files = []
    for path in sorted(RUN.rglob("*.json")):
        require(Path(str(path) + ".sha256").is_file(), f"Missing sidecar: {path}")
        data = read(path)
        # Stage events use artifact_hash as a reference to a prepared unit.
        # Only actual model preparation/evaluation objects carry self-hashes.
        if isinstance(data, dict) and data.get("schema") in SELF_HASH_SCHEMAS:
            require(data["artifact_hash"] == canonical_hash({k: v for k, v in data.items() if k != "artifact_hash"}),
                    f"Internal artifact hash mismatch: {path}")
        run_files.append(str(path.relative_to(RUN)))

    preparation = read(RUN / "preparation_complete.json")
    evaluation = read(RUN / "evaluation_complete.json")
    exposure = read(RUN / "evaluation_exposure.json", evaluation["evaluation_exposure_sha256"])
    require([(u["kind"], u["index"]) for u in preparation["units"]] == EXPECTED, "Incomplete preparation registry")
    require([(u["kind"], u["index"]) for u in evaluation["units"]] == EXPECTED, "Incomplete evaluation registry")
    require(preparation["evaluation_generated"] is False, "Preparation marked evaluation-exposed")
    require(exposure["all_15_prepared_durable_reloaded_validated"] is True, "Global preparation gate missing")
    require(exposure["prepared_units"] == preparation["units"], "Exposure changed prepared unit registry")
    preparation_hash = hashlib.sha256((RUN / "preparation_complete.json").read_bytes()).hexdigest()
    require(exposure["preparation_manifest_sha256"] == preparation_hash, "Exposure preparation binding differs")
    require(preparation["freeze"] == evaluation["freeze"] == exposure["freeze"], "Stage freeze binding differs")
    require(preparation["freeze"]["manifest_sha256"] == manifest_hash(), "Stage manifest identity differs")

    events = {}
    for stage, record in (("preparation", preparation), ("evaluation", evaluation)):
        events[stage] = [read(RUN / item["file"], item["sha256"]) for item in record["events"]]
        times = [datetime.fromisoformat(item["utc"]) for item in events[stage]]
        require(times == sorted(times), f"Unordered stage events: {stage}")
        require(all(record["freeze"]["manifest_sha256"] == event["freeze_sha256"] for event in events[stage]),
                "Event freeze identity differs")
    gates = [e for e in events["evaluation"] if e["event"] == "global_15_unit_validation_gate_passed"]
    require(len(gates) == 1 and gates[0]["unit_count"] == 15, "Evaluation global gate count differs")
    durable = [e for e in events["preparation"] if e["event"] == "unit_durable_validated"]
    started = [e for e in events["evaluation"] if e["event"] == "unit_started"]
    require(len(durable) == len(started) == 15, "Expected 15 durable preparations and evaluation starts")
    last_durable = max(datetime.fromisoformat(e["utc"]) for e in durable)
    prep_complete = datetime.fromisoformat(preparation["completed_utc"])
    gate_time = datetime.fromisoformat(gates[0]["utc"])
    exposed_time = datetime.fromisoformat(exposure["utc"])
    first_unit = min(datetime.fromisoformat(e["utc"]) for e in started)
    require(last_durable <= prep_complete <= gate_time <= exposed_time <= first_unit,
            "Global preparation/gate/exposure chronology violated")

    prepared = {}
    evaluated = {}
    for unit in preparation["units"]:
        key = unit["kind"], unit["index"]
        value = read(RUN / unit["file"], unit["sha256"])
        require(value["artifact_hash"] == unit["artifact_hash"], "Prepared inner identity differs")
        prepared[key] = value
    for unit in evaluation["units"]:
        key = unit["kind"], unit["index"]
        value = read(RUN / unit["file"], unit["sha256"])
        expected_prepared = prepared[key]["artifact_hash"]
        actual_prepared = value["discovery_artifact_hash"] if key[0] == "calibration" else value["prepared_artifact_hash"]
        require(actual_prepared == unit["prepared_artifact_hash"] == expected_prepared, "Evaluation preparation identity differs")
        evaluated[key] = value
    for event in durable:
        key = event["kind"], event["model_index"]
        require(event["artifact_hash"] == prepared[key]["artifact_hash"],
                "Durable event references a different prepared artifact")
        unit = next(u for u in preparation["units"] if (u["kind"], u["index"]) == key)
        require(event["file_sha256"] == unit["sha256"], "Durable event file hash differs")

    def moments(cell, mean_expected, count_expected):
        require(cell["n"] == count_expected, "Paired count mismatch")
        close(cell["mean_paired_absolute_error_improvement"], mean_expected, "Paired mean differs from marginal MAEs")
        close(cell["sum"] / cell["n"], cell["mean_paired_absolute_error_improvement"], "Paired sum/mean mismatch")
        require(-1 - 1e-12 <= cell["minimum"] <= cell["mean_paired_absolute_error_improvement"] + 1e-12,
                "Paired lower bound mismatch")
        require(cell["mean_paired_absolute_error_improvement"] <= cell["maximum"] + 1e-12 <= 1 + 2e-12,
                "Paired upper bound mismatch")
        require(cell["sum"] ** 2 / cell["n"] - 1e-9 <= cell["sum_squares"] <= cell["n"] + 1e-9,
                "Paired moments violate bounded variance inequality")
        reconstructed_variance = (cell["sum_squares"] - cell["sum"] ** 2 / cell["n"]) / (cell["n"] - 1)
        close(cell["sample_variance"], reconstructed_variance, "Paired sample variance mismatch")

    summaries = []
    for index in range(5):
        discovery = prepared[("search", index)]
        result = evaluated[("search", index)]
        soft_prepared = prepared[("soft_mask", index)]
        soft = evaluated[("soft_mask", index)]
        require(result["development_only"] and soft["development_only"], "Expanded analysis lost development status")
        require(result["resource"]["validation_searches"] == result["resource"]["validation_decoder_fits"] == 0,
                "Search fitted on validation")
        require(soft["resource"]["validation_fitting_steps"] == 0, "Mask fit on validation")
        require(result["network_hash"] == soft["original_network_hash"], "Search/mask source weights differ")
        require(discovery["selection_data_hashes"]["role_pairs"] == soft_prepared["discovery_pair_hashes"],
                "Search/mask discovery arrays differ")
        require(result["validation_data_hashes"]["role_pairs"] == soft["validation_pair_hashes"],
                "Search/mask validation arrays differ")
        require(set(result["evaluated"]) == set(discovery["alignments"]) and len(result["evaluated"]) == 20,
                "Incomplete 20-variant comparison")
        unique = set()
        for name, variant in result["evaluated"].items():
            require(variant["selected_subsets"] == [r["subset"] for r in discovery["alignments"][name]["roles"]],
                    "Validation selected another subset")
            for role in (0, 1):
                unique.add((role, tuple(variant["selected_subsets"][role])))
                cells = variant["roles"][role]
                require(set(cells) == set(STRATA) and all(cells[s]["n"] == 8192 for s in STRATA), "Missing validation stratum")
                summary = variant["role_summaries"][role]
                close(summary["equal_stratum_mean_mae"], sum(cells[s]["mae"] for s in STRATA) / 5, "Search pooled MAE mismatch")
                close(summary["equal_stratum_mean_mse"], sum(cells[s]["mse"] for s in STRATA) / 5, "Search pooled MSE mismatch")
                close(summary["worst_stratum_mae"], max(cells[s]["mae"] for s in STRATA), "Search worst-stratum mismatch")
                expected_components = [*[cells[s]["mae"] / 0.05 for s in STRATA],
                                       cells["mixed_near"]["decision_disagreement"] / 0.35,
                                       cells["mixed_far"]["decision_disagreement"] / 0.10]
                require(len(expected_components) == len(summary["robust_normalized_components"]), "Robust component count mismatch")
                for observed, expected in zip(summary["robust_normalized_components"], expected_components):
                    close(observed, expected, "Validation robust component mismatch")
                close(summary["robust_max_normalized_error"], max(expected_components), "Robust maximum mismatch")
                require(summary["descriptive_error_and_decision_thresholds_met"] == (max(expected_components) <= 1),
                        "Descriptive threshold label differs")
        require(result["resource"]["unique_selected_role_subsets_evaluated"] == len(unique), "Unique-subset resource count mismatch")
        require(discovery["resource"]["candidate_evaluations_actual"] == discovery["resource"]["decoder_fits_actual"] == 5 * 2 * 1024,
                "Actual fixed search budget differs")
        require(discovery["resource"]["candidate_evaluations_logical_without_shared_scores"] == 5 * 2 * 2 * (128 + 1024),
                "Logical independent-method search budget differs")

        comparisons = list(result["budget_comparisons"].values()) + list(result["selector_comparisons"].values()) + list(result["family_comparisons"].values())
        comparisons += [c for controls in result["matched_control_comparisons"].values() for c in controls.values()]
        for comparison in comparisons:
            candidate, reference = comparison["candidate"], comparison["reference"]
            require(comparison["positive_improvement_favors"] == "candidate", "Improvement sign convention changed")
            for role, group in enumerate(comparison["roles"]):
                require(group["role"] == role, "Paired role order differs")
                deltas = []
                for stratum in STRATA:
                    delta = result["evaluated"][reference]["roles"][role][stratum]["mae"] - result["evaluated"][candidate]["roles"][role][stratum]["mae"]
                    deltas.append(delta)
                    moments(group["strata"][stratum], delta, 8192)
                moments(group["pooled_equal_strata"], sum(deltas) / 5, 5 * 8192)
                close(group["pooled_equal_strata"]["sum"], sum(group["strata"][s]["sum"] for s in STRATA), "Pooled paired sum mismatch")
                close(group["pooled_equal_strata"]["sum_squares"], sum(group["strata"][s]["sum_squares"] for s in STRATA), "Pooled paired square-sum mismatch")

        require(tuple(soft["methods"]) == MASKS and len(soft["rows"]) == 40 and len(soft["pooled_rows"]) == 8,
                "Incomplete four-mask method product")
        by = {(row["role"], row["method"], row["stratum"]): row for row in soft["rows"]}
        for pooled in soft["pooled_rows"]:
            cells = [by[(pooled["role"], pooled["method"], s)] for s in STRATA]
            require(all(row["n"] == 8192 for row in cells) and pooled["n"] == 40960, "Mask counts differ")
            for field in ("mae", "mse", "logit_mse", "decision_agreement"):
                close(pooled[field], sum(row[field] for row in cells) / 5, f"Mask pooled {field} mismatch")
        for cell in soft["paired_comparisons"]:
            role, stratum = cell["role"], cell["stratum"]
            expected = by[(role, cell["comparator"], stratum)]["mae"] - by[(role, cell["method"], stratum)]["mae"]
            moments(cell, expected, 8192)
            require(cell["formal_support_assessed"] is False, "Mask diagnostic became confirmatory")
        for role in soft_prepared["roles"]:
            mask = role["mask"]["values"]
            require(len(mask) == 32 and all(0 <= x <= 1 for x in mask) and abs(sum(mask) - 8) <= 1e-12,
                    "Saved fractional mask infeasible")
            binary = role["binary_global"]
            require(binary["enumerated_subsets"] == 10518300 and len(binary["subset"]) == len(set(binary["subset"])) == 8,
                    "Binary global enumeration capacity/count differs")
            require(binary["discovery_matrix_hash"] == role["discovery_matrix_hash"], "Binary and fractional objectives use different arrays")
            require(binary["direct_discovery_logit_mse"] + binary["objective_recomputation_allowed_discrepancy"] >= role["certificate"]["relaxed_optimum_lower_bound"],
                    "Binary optimum violates fractional numerical lower bound")
        summaries.append({"model_index": index, "search_variants": 20, "search_role_strata": 200,
                          "mask_role_method_strata": 40, "descriptive_paired_comparisons": len(comparisons),
                          "source_model_and_discovery_validation_hashes_match": True})

    output = {"schema": "f15-nd01-independent-saved-output-audit-v1", "passed": True,
              "checks": checks, "registered_execution_files": len(manifest["files"]),
              "original_frozen_files": len(original_manifest["files"]), "prepared_units": 15,
              "evaluation_units": 15, "hashed_run_json_count": len(run_files),
              "stage_attempts": {"preparation": preparation["attempt"], "evaluation": evaluation["attempt"]},
              "chronology": {"last_prepared_unit_durable_utc": last_durable.isoformat(),
                             "preparation_complete_utc": prep_complete.isoformat(),
                             "evaluation_global_gate_utc": gate_time.isoformat(),
                             "exposure_utc": exposed_time.isoformat(), "first_evaluation_unit_started_utc": first_unit.isoformat()},
              "model_summaries": summaries, "inputs": hashed,
              "scope": "Hash and temporal audit plus independent aggregation, paired-moment, constraint and resource reconstruction from saved sufficient statistics. No new study inputs, parameter updates, alignments or outcomes generated. This does not independently reconstruct each raw neural probability from inputs.",
              "reviewer": "ChatGPT (GPT-6 Astra Pro), independent nd01_protocol_audit sub-agent"}
    raw = (json.dumps(output, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    path = SESSION / "audit_saved_outputs.json"
    if args.check:
        require(path.read_bytes() == raw, "Independent audit no longer reproduces from saved outputs")
    else:
        with path.open("xb") as handle:
            handle.write(raw)
        Path(str(path) + ".sha256").write_text(hashlib.sha256(raw).hexdigest() + "\n")
    print(json.dumps({"passed": True, "checks": checks, "hash_valid_run_json": len(run_files),
                      "prepared_units": 15, "evaluation_units": 15, "check_mode": args.check}))


def manifest_hash():
    return hashlib.sha256((HERE / "freeze.json").read_bytes()).hexdigest()


if __name__ == "__main__":
    main()
