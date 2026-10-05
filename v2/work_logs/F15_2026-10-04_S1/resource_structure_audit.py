"""Audit F15 saved resource identities and describe nested cost components.

Contributor: ChatGPT (GPT-6 Astra Pro). This reads the original saved rows;
it does not benchmark again, rerun methods, create populations or optimize
the frozen implementation. Durations below remain observed local wall time.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import statistics
import sys


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "v2/work_logs/F15_v1_run1/evaluation_attempt_1"
checks = Counter()
inputs = []


def checked(path):
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert Path(str(path) + ".sha256").read_text().strip() == sha
    inputs.append({"path": str(path.relative_to(ROOT)), "bytes": len(raw), "sha256": sha})
    return json.loads(raw)


def require(test, kind, label):
    checks[kind] += 1
    assert test, f"{kind}: {label}"


def stats(values):
    values = list(values)
    return {"n": len(values), "sum": sum(values), "mean": statistics.mean(values),
            "median": statistics.median(values), "minimum": min(values), "maximum": max(values)}


def main():
    config = json.loads((ROOT / "v2/experiments/config.v1.json").read_text())
    cases = [checked(RUN / f"retention_{seed}_{variant}.json")
             for seed in config["retention"]["evaluation_seeds"]
             for variant in config["retention"]["variants"]]
    flat = []
    for case in cases:
        common = case["common_input_accounting"]
        require(common["observed_common_production_ns"] == common["generation_ns"] + common["input_serialization_ns"],
                "common_timer_identity", str((case["seed"], case["variant"])))
        for row in case["methods"]:
            r = row["resources"]
            label = f"{case['seed']}/{case['variant']}/{row['access']}/{row['method']}"
            require(r["initial_total_ns"] == r["initial_production_ns"] + r["initial_native_production_and_check_ns"],
                    "initial_timer_identity", label)
            arithmetic = sum(r[k] for k in ("source_archive_production_ns", "acquisition_ns", "update_and_solve_ns", "decision_ns"))
            require(arithmetic == r["one_update_arithmetic_ns"], "arithmetic_timer_identity", label)
            native_increment = r["current_context_production_ns"] + r["current_native_protocol_ns"]
            require(r["one_update_total_ns"] == arithmetic + native_increment, "native_increment_identity", label)
            native_subtotal = sum(r["native_substages_ns"].values())
            require(r["current_native_protocol_ns"] >= native_subtotal, "native_timer_nesting", label)
            for key, value in r["native_substages_ns"].items():
                require(value == row["native"][key], "native_timer_duplicate_agreement", label + "/" + key)
            require(r["one_case_method_plus_common_ns"] == common["observed_common_production_ns"] + r["initial_total_ns"] + r["one_update_total_ns"],
                    "complete_case_timer_identity", label)
            resident = r["retained_payload_bytes"] + r["cached_source_context_bytes"] + r["cached_proof_bytes"]
            require(resident == r["resident_bytes"], "resident_storage_identity", label)
            active = resident + sum(r[k] for k in ("current_source_context_bytes", "current_proof_bytes", "current_update_metadata_bytes", "schema_bytes"))
            require(active == r["active_serialized_upper_bytes"], "active_storage_identity", label)
            require(r["total_stored_serialized_upper_bytes"] == active + r["external_archive_bytes"], "stored_storage_identity", label)
            require(r["resident_plus_archive_bytes"] == resident + r["external_archive_bytes"], "resident_archive_identity", label)
            supplied = resident + common["old_source_input_bytes"] + r["schema_bytes"]
            require(r["initial_with_supplied_source_serialized_upper_bytes"] == supplied, "initial_exposure_storage_identity", label)
            require(r["peak_serialized_working_state_upper_bytes"] == max(supplied, active), "peak_declared_storage_identity", label)
            require(r["current_proof_bytes"] == row["native"]["proof_bytes"], "current_proof_storage_identity", label)
            require(r["initial_common_scalar_inputs"] == common["old_source_scalar_inputs"] == 8,
                    "initial_common_source_count", label)
            require(r["current_common_scalar_inputs"] == common["current_shared_scalar_inputs"] == (3 if case["variant"] == "known_marginals" else 0),
                    "current_common_source_count", label)
            require(all(type(value) is int and value >= 0 for key, value in r.items()
                        if (key.endswith("_ns") or key.endswith("_bytes")) and not isinstance(value, dict)),
                    "nonnegative_scalar_resources", label)
            if row["access"] == "no_reacquisition":
                require(r["external_archive_bytes"] == r["source_archive_production_ns"] == r["acquisition_calls"] == r["acquisition_ns"] == 0,
                        "no_reacquisition_resources", label)
            else:
                require(r["external_archive_bytes"] > 0 and r["source_archive_production_ns"] > 0,
                        "adaptive_archive_charged_when_unused", label)
            if row["method"] != "cached_proof":
                require(r["cached_source_context_bytes"] == r["cached_proof_bytes"] == r["initial_native_production_and_check_ns"] == row["native"]["cache_check_ns"] == 0,
                        "cache_only_charges", label)
            for h in (1, 4, 16, 64):
                require(r["horizon_arithmetic_ns"][str(h)] == r["initial_production_ns"] + h * arithmetic,
                        "arithmetic_horizon_identity", label + f"/{h}")
                require(r["horizon_compute_ns"][str(h)] == r["initial_total_ns"] + h * r["one_update_total_ns"],
                        "native_horizon_identity", label + f"/{h}")
                require(r["horizon_compute_plus_common_ns"][str(h)] == common["observed_common_production_ns"] + r["horizon_compute_ns"][str(h)],
                        "common_horizon_identity", label + f"/{h}")
            flat.append({"seed": case["seed"], "variant": case["variant"], "method": row["method"], "access": row["access"],
                         "cache": row["native"]["cache"], "native_status": row["native"]["status"],
                         "resources": r, "native_unallocated_ns": r["current_native_protocol_ns"] - native_subtotal})
    grouped = []
    for access in config["retention"]["access_regimes"]:
        for method in config["retention"]["methods"]:
            cells = [r for r in flat if r["access"] == access and r["method"] == method]
            fields = ("initial_production_ns", "initial_native_production_and_check_ns", "source_archive_production_ns",
                      "acquisition_ns", "update_and_solve_ns", "decision_ns", "current_context_production_ns",
                      "current_native_protocol_ns", "initial_total_ns", "one_update_arithmetic_ns", "one_update_total_ns")
            data = {k: stats(r["resources"][k] for r in cells) for k in fields}
            data.update({k: stats(r["resources"]["native_substages_ns"][k] for r in cells)
                         for k in ("cache_check_ns", "proof_production_ns", "receipt_check_ns")})
            data["native_unallocated_ns"] = stats(r["native_unallocated_ns"] for r in cells)
            grouped.append({"method": method, "access": access, "rows": len(cells), "components": data,
                            "receipt_check_share_of_current_native_total": data["receipt_check_ns"]["sum"] / data["current_native_protocol_ns"]["sum"],
                            "scope": "unfiltered descriptive observations; quality and access remain required for fair comparisons"})
    cached = []
    for access in config["retention"]["access_regimes"]:
        for status in ("received", "rejected_then_replacement"):
            cells = [r for r in flat if r["access"] == access and r["method"] == "cached_proof" and r["cache"] == status]
            cached.append({"access": access, "cache_status": status, "rows": len(cells),
                           "variants": dict(Counter(r["variant"] for r in cells)),
                           "cache_check_ns": stats(r["resources"]["native_substages_ns"]["cache_check_ns"] for r in cells),
                           "current_receipt_check_ns": stats(r["resources"]["native_substages_ns"]["receipt_check_ns"] for r in cells),
                           "replacement_proof_production_ns": stats(r["resources"]["native_substages_ns"]["proof_production_ns"] for r in cells)})
    total_method = sum(r["resources"]["initial_total_ns"] + r["resources"]["one_update_total_ns"] for r in flat)
    total_common = sum(c["common_input_accounting"]["observed_common_production_ns"] for c in cases)
    assigned_common = sum(r["resources"]["one_case_method_plus_common_ns"] for r in flat) - total_method
    require(assigned_common == 12 * total_common, "common_charge_multiplicity", "once physical versus twelve comparison assignments")
    output = {"schema": "F15-saved-resource-structure-audit-v1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
              "no_new_benchmark_or_population": True, "original_method_rows": len(flat),
              "checks": dict(checks), "checks_total": sum(checks.values()), "mismatches": 0,
              "physical_common_production_ns": total_common, "summed_method_stage_ns": total_method,
              "comparison_assigned_common_production_ns": assigned_common,
              "method_access_components": grouped, "cached_hit_and_rejection_components": cached,
              "interpretation": "Native residual time includes bound/request creation and result/proof serialization outside named subtimers. It is not missing from native or process totals. A cache hit still traverses the frozen current theorem/request reception path, so these results do not evaluate an optimized cache implementation.",
              "input_manifest": inputs, "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    raw = (json.dumps(output, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    path = HERE / "resource_structure_audit.json"
    if "--check" in sys.argv:
        assert path.read_bytes() == raw
    else:
        with path.open("xb") as handle:
            handle.write(raw)
        with Path(str(path) + ".sha256").open("x") as handle:
            handle.write(hashlib.sha256(raw).hexdigest() + "\n")
    print(json.dumps({"output": str(path.relative_to(ROOT)), "bytes": len(raw),
                      "sha256": hashlib.sha256(raw).hexdigest(), "checks": sum(checks.values()), "mismatches": 0}))


if __name__ == "__main__":
    main()
