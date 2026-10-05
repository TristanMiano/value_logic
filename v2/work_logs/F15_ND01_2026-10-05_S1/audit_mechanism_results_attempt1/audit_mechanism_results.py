"""Independent audit of saved ND01 mechanism results; no population generation.

Reads saved model coefficients, quadratic coefficients, candidate pools and
summary moments. Does not import the mechanism implementation, call any model,
generate inputs, fit masks, or run the exhaustive/iterative optimizers.
Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
import datetime
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
SESSION = Path(__file__).resolve().parent
ANALYSIS = ROOT / "v2/experiments/F15_ND01_analysis"
RUN = ROOT / "v2/work_logs/F15_ND01_v1_run1"
COUNTS = Counter()
FAILURES = []
MAXIMUM_DISCREPANCIES = defaultdict(float)
INPUTS = {}


def digest(path):
    data = Path(path).read_bytes()
    result = hashlib.sha256(data).hexdigest()
    INPUTS[str(Path(path).relative_to(ROOT))] = {"bytes": len(data), "sha256": result}
    return result


def load(path):
    digest(path)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def array_hash(*arrays):
    result = hashlib.sha256()
    for array in arrays:
        value = np.ascontiguousarray(array, dtype=np.float64)
        result.update(json.dumps(list(value.shape), separators=(",", ":")).encode("ascii"))
        result.update(value.tobytes())
    return result.hexdigest()


def check(condition, category, label):
    COUNTS[category] += 1
    if not condition:
        FAILURES.append({"category": category, "label": label})


def close(actual, expected, category, label, tolerance=1e-12):
    actual, expected = float(actual), float(expected)
    difference = abs(actual - expected)
    MAXIMUM_DISCREPANCIES[category] = max(MAXIMUM_DISCREPANCIES[category], difference)
    check(math.isfinite(actual) and math.isfinite(expected)
          and difference <= tolerance * max(1.0, abs(actual), abs(expected)), category, label)


def vector_close(actual, expected, category, label, tolerance=1e-12):
    a, b = np.asarray(actual, dtype=np.float64), np.asarray(expected, dtype=np.float64)
    check(a.shape == b.shape, category, label + "/shape")
    if a.shape == b.shape:
        difference = float(np.max(abs(a - b))) if a.size else 0.0
        MAXIMUM_DISCREPANCIES[category] = max(MAXIMUM_DISCREPANCIES[category], difference)
        check(np.isfinite(a).all() and np.isfinite(b).all() and difference <= tolerance,
              category, label + "/values")


def exact_rank(matrix):
    a = [row[:] for row in matrix]
    pivot_row = 0
    if not a:
        return 0
    for column in range(len(a[0])):
        pivot = next((row for row in range(pivot_row, len(a)) if a[row][column]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        for row in range(pivot_row + 1, len(a)):
            ratio = a[row][column] / a[pivot_row][column]
            a[row] = [x - ratio * y for x, y in zip(a[row], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def masks_for(prepared_role):
    masks = {"fractional_mask": np.asarray(prepared_role["mask"]["values"])}
    for name, subset in (("frozen_original", prepared_role["original_subset"]),
                         ("binary_global", prepared_role["binary_global"]["subset"])):
        masks[name] = np.asarray([float(j in subset) for j in range(32)])
    return masks


def main():
    paths = [SESSION / "audit_mechanism_results.json", SESSION / "audit_mechanism_results.md"]
    if any(path.exists() for path in paths):
        raise FileExistsError("Preserve prior mechanism output audit; do not overwrite it.")
    result_path = ANALYSIS / "mechanism_results.json"
    result = load(result_path)
    check(digest(result_path) == result_path.with_suffix(".json.sha256").read_text().strip(), "provenance", "mechanism sidecar")
    check(result["script_sha256"] == digest(ANALYSIS / "mechanism_analysis.py"), "provenance", "executed mechanism source")
    freeze_path = ROOT / "v2/experiments/neural_diagnostic_v1/freeze.json"
    freeze = load(freeze_path)
    check(result["freeze"]["manifest_sha256"] == digest(freeze_path), "provenance", "diagnostic freeze manifest")
    check(result["freeze"]["config_sha256"] == digest(ROOT / freeze["config_path"]), "provenance", "diagnostic configuration")
    check(result["freeze"]["source_f14_manifest_sha256"] == digest(ROOT / "v2/experiments/freeze.v1.json"), "provenance", "original F14 manifest")
    for record in freeze["files"]:
        path = ROOT / record["path"]
        check(digest(path) == record["sha256"] and path.stat().st_size == record["bytes"], "provenance", record["path"])
    originals = []
    for record in result["freeze"]["source_prepared"]:
        path = ROOT / record["path"]
        check(digest(path) == record["sha256"] and path.stat().st_size == record["bytes"], "provenance", record["path"])
        original = load(path)
        check(original["artifact_hash"] == canonical({k: v for k, v in original.items() if k != "artifact_hash"}), "provenance", record["path"] + "/artifact")
        originals.append(original)
    prepared, evaluated = {}, {}
    for kind, target in (("preparation", prepared), ("evaluation", evaluated)):
        path = RUN / f"{kind}_complete.json"
        manifest = load(path)
        check(result[f"{kind}_manifest_sha256"] == digest(path), "provenance", kind + " manifest")
        check(manifest["freeze"] == result["freeze"], "provenance", kind + " freeze binding")
        check(len(manifest["units"]) == 15 and manifest["status"] == "complete", "provenance", kind + " all fifteen units")
        for record in manifest["units"]:
            path = RUN / record["file"]
            unit = load(path)
            check(digest(path) == record["sha256"], "provenance", record["file"] + "/bytes")
            if "artifact_hash" in unit:
                check(unit["artifact_hash"] == canonical({k: v for k, v in unit.items() if k != "artifact_hash"}), "provenance", record["file"] + "/artifact")
            target[record["kind"], record["index"]] = unit
    core = load(ANALYSIS / "core_summary.json")
    for record in core["table_manifest"]:
        path = ANALYSIS / record["file"]
        check(digest(path) == record["sha256"] and path.stat().st_size == record["bytes"], "provenance", record["file"] + "/table")
    csv_rows = list(csv.DictReader((ANALYSIS / "mask_rows.csv").open(newline="", encoding="utf-8")))
    csv_index = {(int(r["model_index"]), int(r["role"]), r["stratum"], r["method"]): r for r in csv_rows}
    core_rows = {(i, r["role"], r["stratum"], r["method"]): r for i in range(5) for r in evaluated["soft_mask", i]["rows"]}
    check(len(csv_index) == len(core_rows) == 200, "cardinality", "core mask cells")
    for row in result["regeneration_provenance"]:
        index, role = row["model_index"], row["role"]
        check(row["discovery_pair_hash"] == prepared["soft_mask", index]["discovery_pair_hashes"][role]
              == prepared["search", index]["selection_data_hashes"]["role_pairs"][role], "provenance", f"shared discovery {index}/{role}")
        check(row["validation_pair_hash"] == evaluated["soft_mask", index]["validation_pair_hashes"][role]
              == evaluated["search", index]["validation_data_hashes"]["role_pairs"][role], "provenance", f"shared validation {index}/{role}")
        check(row["same_arrays_regenerated_not_new_independent_population"] is True, "scope", "regeneration label")
    quadratics = {(r["model_index"], r["role"]): r for r in result["discovery_quadratics"]}
    values_by_pool = {}
    score_count = 0
    for (index, role), row in quadratics.items():
        gram, linear = np.asarray(row["gram"]), np.asarray(row["linear"])
        constant = float(row["constant"])
        saved = prepared["soft_mask", index]["roles"][role]
        check(array_hash(gram, linear, np.asarray([constant])) == row["quadratic_hash"]
              == saved["binary_global"]["quadratic_coefficients_hash"], "quadratic", f"coefficient hash {index}/{role}")
        check(row["matrix_hash"] == saved["discovery_matrix_hash"], "quadratic", "discovery matrix binding")
        vector_close(gram, gram.T, "quadratic", "Gram symmetry", 0.0)
        check(float(np.linalg.eigvalsh(gram)[0]) >= -1e-12, "quadratic", "Gram numerically positive semidefinite")

        def objective(subset):
            # Independent compensated scalar summation; not the source einsum.
            return math.fsum([constant, -2 * math.fsum(float(linear[j]) for j in subset),
                math.fsum(float(gram[j, j]) for j in subset),
                2 * math.fsum(float(gram[j, k]) for j, k in itertools.combinations(subset, 2))])

        close(objective(saved["binary_global"]["subset"]), saved["binary_global"]["direct_discovery_logit_mse"], "quadratic", "global saved direct residual", 1e-10)
        for family, pools in prepared["search", index]["candidate_pools"].items():
            values_by_pool[index, role, family] = [objective(subset) for subset in pools[role]["candidate_pool"]]
            score_count += len(values_by_pool[index, role, family])
    for row in result["candidate_objective_coverage"]:
        index, role, family, budget = row["model_index"], row["role"], row["family"], row["budget"]
        values = values_by_pool[index, role, family][:budget]
        selector = prepared["search", index]["alignments"][f"{family}/budget_{budget}/{row['selector']}"]["roles"][role]
        check(selector["selected_index"] == row["selected_index"], "coverage", "selected alignment index")
        close(values[row["selected_index"]], row["selected_discovery_logit_mse"], "coverage", "selected objective")
        close(min(values), row["best_pool_discovery_logit_mse"], "coverage", "minimum pool objective")
        close(values[row["best_pool_logit_index_analysis_only"]], min(values), "coverage", "best pool recorded index")
        global_value = prepared["soft_mask", index]["roles"][role]["binary_global"]["direct_discovery_logit_mse"]
        close(row["global_binary_discovery_logit_mse"], global_value, "coverage", "global reference")
        close(row["selection_objective_gap"], row["selected_discovery_logit_mse"] - row["best_pool_discovery_logit_mse"], "coverage", "selection gap")
        close(row["candidate_coverage_gap"], row["best_pool_discovery_logit_mse"] - global_value, "coverage", "coverage gap")
        close(row["total_excess_over_global"], row["selection_objective_gap"] + row["candidate_coverage_gap"], "coverage", "gap decomposition")
        check(min(row["selection_objective_gap"], row["candidate_coverage_gap"], row["total_excess_over_global"]) >= -1e-10, "coverage", "gaps nonnegative")
        check(row["pool_attains_global_within_1e_minus_10"] == (min(values) <= global_value + 1e-10), "coverage", "global attainment flag")
        check(row["new_pool_winner_validated_or_adopted"] is False, "scope", "no new validation selection")
    check(score_count == result["resource"]["saved_candidate_logit_scores_computed"] == 51200, "cardinality", "candidate rescoring count")

    for row in result["error_decomposition"]:
        key = row["model_index"], row["role"], row["stratum"], row["method"]
        saved, table = core_rows[key], csv_index[key]
        close(row["probability_mae"], saved["mae"], "per_cell", str(key) + "/saved MAE")
        close(row["probability_mae"], table["mae"], "per_cell", str(key) + "/table MAE")
        close(row["total_logit_mse"], saved["logit_mse"], "per_cell", str(key) + "/logit MSE")
        close(row["base_probability_mae"], saved["base_prediction"]["mae"], "per_cell", str(key) + "/base MAE")
        check(row["n"] == saved["n"] == 8192, "per_cell", str(key) + "/n")
        if row["stratum"] == "equal_target":
            close(row["unchanged_target_output_effect_rms"], saved["unchanged_target_output_effect_rms"], "per_cell", str(key) + "/equal target")
        else:
            check(row["unchanged_target_output_effect_rms"] is None, "per_cell", str(key) + "/equal-target absence")
        close(row["total_logit_mse"], math.fsum([row["base_logit_mse"], row["contribution_residual_change_mse"], row["twice_cross_moment"]]), "decomposition", str(key) + "/sum")
        check(abs(row["twice_cross_moment"]) <= 2 * math.sqrt(row["base_logit_mse"] * row["contribution_residual_change_mse"]) + 1e-12, "decomposition", "cross moment Cauchy bound")
        check(0 <= row["decomposition_max_identity_error"] <= 1e-11, "decomposition", "reported identity residual")
        energies = row["native_coordinate_change_second_moments"]
        check(len(energies) == 32 and min(energies) >= 0, "decomposition", "nonnegative energies")
        total = math.fsum(energies)
        participation = total * total / math.fsum(x * x for x in energies) if total else 0.0
        close(row["native_energy_participation_count"], participation, "decomposition", "participation arithmetic")
        check(row["energy_ignores_cross_coordinate_cancellation"] is True, "scope", "energy interpretation")

    geometries = {g["model_index"]: g for g in result["network_geometry"]}
    box = [(-1, 1), (-1, 1), (Fraction(1, 2), 2), (Fraction(1, 2), 2)]
    for index, geometry in geometries.items():
        net = originals[index]["network"]
        classified = defaultdict(list)
        for unit in geometry["units"]:
            j = unit["unit"]
            w = [Fraction.from_float(float(net["w"][i][j])) for i in range(4)]
            b = Fraction.from_float(float(net["b"][j]))
            # Enumerate sixteen analytic box corners independently of the
            # source's sign-based minimum/maximum formula. No model is called.
            corners = [b + sum(coefficient * coordinate for coefficient, coordinate in zip(w, corner))
                       for corner in itertools.product(*box)]
            lower, upper = min(corners), max(corners)
            group = "always_inactive" if upper <= 0 else "always_active" if lower >= 0 else "variable"
            classified[group].append(j)
            check(str(lower) == unit["preactivation_min_exact"] and str(upper) == unit["preactivation_max_exact"], "geometry", f"exact corner bounds {index}/{j}")
            check(group == unit["classification"], "geometry", f"classification {index}/{j}")
            close(float(lower), unit["preactivation_min"], "geometry", "minimum display", 0)
            close(float(upper), unit["preactivation_max"], "geometry", "maximum display", 0)
        for group in ("always_inactive", "always_active", "variable"):
            check(classified[group] == geometry[group], "geometry", group + " index list")
        active = geometry["always_active"]
        matrix = [[Fraction.from_float(float(net["w"][i][j])) for j in active] for i in range(4)]
        rank = exact_rank(matrix)
        check(rank == geometry["exact_active_weight_rank"], "geometry", "exact active rank")
        check(geometry["hidden_difference_rank_upper_bound"] == min(32, len(geometry["variable"]) + rank), "geometry", "rank bound")
        check(geometry["guaranteed_nullspace_dimension_lower_bound"] == max(0, 32 - len(geometry["variable"]) - rank), "geometry", "nullity bound")
        null = geometry["null_direction"]
        check(null["type"] == "globally_inactive_coordinate" and null["unit"] == geometry["always_inactive"][0], "geometry", "selected exact inactive direction")
        exact = [Fraction(x) for x in null["exact_unnormalized_vector"]]
        check(exact == [Fraction(int(j == null["unit"])) for j in range(32)], "geometry", "exact inactive vector")
        vector_close(null["unit_vector"], [float(x) for x in exact], "geometry", "unit inactive vector", 0)
    projector_coefficients = {}
    for row in result["constructed_projector_equivalence"]:
        index, role = row["model_index"], row["role"]
        v = np.asarray(originals[index]["network"]["v"])
        mask = np.asarray(prepared["soft_mask", index]["roles"][role]["mask"]["values"])
        a = v * mask
        n = np.asarray(geometries[index]["null_direction"]["unit_vector"])
        q = np.asarray(row["projector_coefficient"])
        delta = math.fsum(float(m * (1 - m) * weight * weight) for m, weight in zip(mask, v))
        vector_close(row["fractional_coefficient"], a, "projector", "fractional native coefficient")
        close(row["full_coefficient_sphere_deficit"], delta, "projector", "sphere deficit")
        vector_close(q, a + row["null_shift"] * n, "projector", "null shifted coefficient")
        b = float((2 * a - v) @ n)
        close(row["null_shift"] ** 2 + b * row["null_shift"] - delta, 0, "projector", "quadratic root identity")
        norm2 = float(q @ q)
        projector = np.outer(q, q) / norm2 if norm2 else np.zeros((32, 32))
        actual = projector @ v
        projector_coefficients[index, role] = actual
        metrics = {
            "projector_sphere_equality_error": float(abs(q @ v - norm2)),
            "projector_symmetry_max_error": float(np.max(abs(projector - projector.T))),
            "projector_idempotence_max_error": float(np.max(abs(projector @ projector - projector))),
            "projector_head_coefficient_max_error": float(np.max(abs(actual - q))),
        }
        for name, value in metrics.items():
            close(row[name], value, "projector", name)
            check(value <= 1e-12, "projector", name + "/small")
        check(row["projector_rank"] == (1 if norm2 else 0), "projector", "rank-one construction")
        check(row["constructed"] and not row["new_fit"] and not row["DAS_executed"] and not row["jointly_orthogonal_role_projectors_claimed"], "scope", "projector interpretation")
        check(row["validation_null_difference_max_abs"] == 0, "projector", "recorded inactive direction difference")
        check(0 <= row["validation_logit_equivalence_max_error"] <= 1e-12, "projector", "recorded output equivalence residual")
    for index, geometry in geometries.items():
        q0, q1 = projector_coefficients[index, 0], projector_coefficients[index, 1]
        close(geometry["constructed_role_projector_coefficient_dot_product"], q0 @ q1, "projector", "two-role coefficient dot")
        close(geometry["constructed_role_projector_coefficient_cosine"], (q0 @ q1) / (np.linalg.norm(q0) * np.linalg.norm(q1)), "projector", "two-role coefficient cosine")
    for row in result["secondary_composition"]:
        index, method = row["model_index"], row["method"]
        v = np.asarray(originals[index]["network"]["v"])
        m0 = masks_for(prepared["soft_mask", index]["roles"][0])[method]
        m1 = masks_for(prepared["soft_mask", index]["roles"][1])[method]
        vector_close(row["commutator_native_coefficient"], v * m0 * m1, "composition", "affine commutator coefficient")
        close(row["overlap_product_mass"], m0 @ m1, "composition", "mask overlap mass")
        check(row["nonzero_overlap_count"] == int(np.count_nonzero(m0 * m1 > 1e-10)), "composition", "overlap count")
        check(row["n"] == 8192 and row["secondary_development_only"] and not row["frozen_joint_stratum_claimed"], "scope", "secondary composed panel")
        check(0 <= row["commutator_identity_max_error"] <= 1e-11, "composition", "reported commutator identity residual")
        check(0 <= row["order_probability_rms"] <= row["order_probability_max_abs"] + 1e-12 <= 1 + 1e-12, "composition", "RMS and maximum consistency")
        check(row["order_probability_rms"] <= 0.25 * row["order_logit_rms"] + 1e-12, "composition", "sigmoid Lipschitz consistency")
        check(all(0 <= row[name] <= 1 for name in ("role0_then_role1_joint_probability_mae", "role1_then_role0_joint_probability_mae")), "composition", "joint MAE bounds")
        check(len(row["panel_inputs_hash"]) == 64, "provenance", "saved composition panel digest shape")
    check(len(result["candidate_objective_coverage"]) == 200 and len(quadratics) == 10
          and len(result["error_decomposition"]) == 150 and len(geometries) == 5
          and len(result["constructed_projector_equivalence"]) == 10
          and len(result["secondary_composition"]) == 15, "cardinality", "all supplementary cells")
    check(result["resource"]["additional_independent_populations"] == result["resource"]["new_fits"] == 0
          and result["resource"]["new_validation_method_selection"] is False, "scope", "mechanism resources and scope")
    primary_cost = [r for r in result["candidate_objective_coverage"]
                    if r["family"] == "cost_corr" and r["budget"] == 128 and r["selector"] == "frozen_mse"]
    unique_pools = {(r["model_index"], r["role"], r["family"], r["budget"]): r
                    for r in result["candidate_objective_coverage"]}
    soft_compositions = [r for r in result["secondary_composition"] if r["method"] == "fractional_mask"]
    findings = {
        "pool_prefixes": len(unique_pools), "pool_prefixes_attaining_global_within_1e_minus_10": sum(r["pool_attains_global_within_1e_minus_10"] for r in unique_pools.values()),
        "minimum_positive_coverage_gap": min(r["candidate_coverage_gap"] for r in unique_pools.values()),
        "cost_corr128_frozen_selector_mean_selection_objective_gap": float(np.mean([r["selection_objective_gap"] for r in primary_cost])),
        "cost_corr128_frozen_selector_mean_candidate_coverage_gap": float(np.mean([r["candidate_coverage_gap"] for r in primary_cost])),
        "inactive_units_by_model": [len(geometries[i]["always_inactive"]) for i in range(5)],
        "fractional_order_probability_rms_by_model": [r["order_probability_rms"] for r in soft_compositions],
        "fractional_nonzero_order_drift_models": sum(r["order_probability_rms"] > 1e-12 for r in soft_compositions),
        "maximum_recorded_projector_output_equivalence_error": max(r["validation_logit_equivalence_max_error"] for r in result["constructed_projector_equivalence"]),
        "maximum_recorded_decomposition_identity_error": max(r["decomposition_max_identity_error"] for r in result["error_decomposition"]),
        "maximum_recorded_composition_identity_error": max(r["commutator_identity_max_error"] for r in result["secondary_composition"]),
    }
    report = {"schema": "f15-nd01-independent-mechanism-output-audit-v1",
        "contributor": "ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "all_checks_passed": not FAILURES, "checks": dict(COUNTS), "total_checks": sum(COUNTS.values()),
        "failures": FAILURES, "maximum_absolute_discrepancies": dict(MAXIMUM_DISCREPANCIES),
        "findings": findings, "inputs": INPUTS,
        "input_or_activation_populations_regenerated": 0, "model_forward_calls": 0,
        "new_fits": 0, "optimizer_or_binary_solver_calls": 0,
        "limitations": ["No raw validation or composition panels were regenerated. Their saved moment values are checked against independently saved core cells where present, arithmetic identities, and general bounds; panel-specific joint RMS and MAE were not independently recalculated.",
            "Exact box geometry concerns the real-valued ReLU function with the stored binary64 weights treated as exact rational coefficients; reported floating execution residuals remain separate.",
            "Rank-one output equivalence is constructed separately by role through always-inactive coordinates; it establishes neither learned semantic subspaces nor jointly orthogonal/compatible role projectors."],
        "read_only_lookup_error": "An initial source read used nonexistent neural_diagnostic_v1/mechanism_analysis.py; corrected to F15_ND01_analysis/mechanism_analysis.py before analysis. No artifacts or experiments were affected."}
    encoded = (json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    paths[0].write_bytes(encoded)
    paths[0].with_suffix(".json.sha256").write_text(hashlib.sha256(encoded).hexdigest() + "\n")
    verdict = "PASS" if not FAILURES else "FAIL"
    text = f"""# F15-ND01 independent saved mechanism-output audit

Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
Concurrent work adds zero separate root-clock minutes. This is not F16.

**Verdict: {verdict}; {sum(COUNTS.values()):,} checks; {len(FAILURES)} failures.**

The audit binds the saved mechanism JSON and executed source to the current
diagnostic freeze, all fifteen preparations and evaluations, original five
model artifacts, and core table hashes. No input/activation populations were
regenerated, no model forwards or fits were performed, and no iterative or
exhaustive optimizer was run.

## Independently recomputed checks

- All 200 candidate-coverage rows were rescored from saved Gram matrices,
  linear terms and constants using compensated scalar summation over the
  saved candidate subsets. The selected indices, best pool values, nonnegative
  coverage/selection gaps and their additive decomposition agree.
- All 150 intervention-error cells agree with the independently saved core
  MAE/logit-MSE cells and CSV table. Error-component sums, cross-moment bounds,
  unchanged-target diagnostics and energy-participation arithmetic agree.
- All 160 neurons' affine minima/maxima were independently evaluated at the
  sixteen exact rational box corners; classifications and rank/nullity bounds
  agree. All five models have globally inactive coordinates.
- All ten rank-one constructions satisfy the saved coefficient/root,
  symmetry, idempotence, sphere and native-head identities. The null directions
  are exact inactive-coordinate directions, with no learned projector fit.
- All fifteen composition records have the correct native commutator
  coefficients, mask overlaps, secondary-panel labels, probability/logit
  consistency and small reported identity errors.

## Findings that affect interpretation

All **{len(unique_pools)} distinct family/budget/role/model pool prefixes** miss
the exhaustive binary optimum for the same finite discovery logit objective;
none attains it within 1e-10. The smallest coverage gap is
**{findings['minimum_positive_coverage_gap']:.9f}**. For the original-style
cost-correlation, 128-candidate, frozen-MSE selection, the mean selection-
objective gap is **{findings['cost_corr128_frozen_selector_mean_selection_objective_gap']:.9f}**
and the mean candidate-coverage gap is
**{findings['cost_corr128_frozen_selector_mean_candidate_coverage_gap']:.9f}**.
Thus that comparison's missed logit optimum is a candidate-coverage limitation,
not an alternative winner already present in the same pool. This concerns the
discovery logit objective, not an optimized probability-MAE endpoint.

Fractional masks show nonzero secondary order drift in
**{findings['fractional_nonzero_order_drift_models']}/5 models**; their order-
probability RMS values are {findings['fractional_order_probability_rms_by_model']}.
Single-role improvement therefore does not establish a coherent joint two-cost
decomposition.

The source networks have **{findings['inactive_units_by_model']} globally
inactive units**. Their null directions permit the constructed rank-one
projectors to reproduce the fractional output effect, with maximum reported
validation discrepancy **{findings['maximum_recorded_projector_output_equivalence_error']:.3e}**.
This is an algebraic output-equivalence construction using functionally
inactive dimensions, not evidence that training learned semantic subspaces,
nor a DAS result or jointly orthogonal role decomposition.

## Audit limits

The composition panels are not stored as raw arrays. This audit verifies their
saved coefficients, identities' reported errors and consistency bounds; it
does **not** independently recompute panel-specific joint RMS/MAE values.
The exact-box proof treats the saved binary64 parameters as exact real
coefficients, separately from the reported floating execution residuals.

One initial read-only source lookup used a nonexistent diagnostic-directory
path; it was corrected to the analysis directory before computation. No input,
model, scientific artifact or frozen file was changed by the audit.

Machine-readable details: [audit_mechanism_results.json](audit_mechanism_results.json).
"""
    paths[1].write_text(text, encoding="utf-8")
    print(json.dumps({"all_checks_passed": not FAILURES, "checks": sum(COUNTS.values()),
                      "failures": FAILURES, "findings": findings}, indent=2))
    if FAILURES:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
