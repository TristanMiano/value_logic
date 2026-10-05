"""ND01 supplementary mechanism analysis on hash-identical existing data.

No trained weights, registered alignments or study artifacts are modified.
No new population seeds, fits, or selected validation methods are introduced.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-05.
"""
from __future__ import annotations

import datetime
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from v2.experiments import freeze as F, neural as N
from v2.experiments.neural_diagnostic_v1 import runner as R


HERE = Path(__file__).resolve().parent
RUN = F.ROOT / "v2/work_logs/F15_ND01_v1_run1"
METHODS = ("frozen_original", "binary_global", "fractional_mask")


def exact_rref(matrix):
    a = [row.copy() for row in matrix]
    if not a or not a[0]:
        return a, []
    pivots, row = [], 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        divisor = a[row][column]
        a[row] = [x / divisor for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][column]:
                coefficient = a[i][column]
                a[i] = [x - coefficient * y for x, y in zip(a[i], a[row])]
        pivots.append(column)
        row += 1
        if row == len(a):
            break
    return a, pivots


def geometry(net):
    bounds = [(Fraction(-1), Fraction(1)), (Fraction(-1), Fraction(1)),
              (Fraction(1, 2), Fraction(2)), (Fraction(1, 2), Fraction(2))]
    inactive, active, variable, units = [], [], [], []
    for j in range(32):
        weights = [Fraction.from_float(float(x)) for x in net.w[:, j]]
        lower = upper = Fraction.from_float(float(net.b[j]))
        for w, (lo, hi) in zip(weights, bounds):
            lower += w * (lo if w >= 0 else hi)
            upper += w * (hi if w >= 0 else lo)
        group = "always_inactive" if upper <= 0 else "always_active" if lower >= 0 else "variable"
        {"always_inactive": inactive, "always_active": active, "variable": variable}[group].append(j)
        units.append({"unit": j, "classification": group,
                      "preactivation_min_exact": str(lower), "preactivation_max_exact": str(upper),
                      "preactivation_min": float(lower), "preactivation_max": float(upper)})
    matrix = [[Fraction.from_float(float(net.w[i, j])) for j in active] for i in range(4)]
    reduced, pivots = exact_rref(matrix)
    null = None
    description = None
    exact_vector = [Fraction(0)] * 32
    if inactive:
        exact_vector[inactive[0]] = Fraction(1)
        description = {"type": "globally_inactive_coordinate", "unit": inactive[0]}
    else:
        free = next((j for j in range(len(active)) if j not in pivots), None)
        if free is not None:
            exact_vector[active[free]] = Fraction(1)
            for row, pivot in enumerate(pivots):
                exact_vector[active[pivot]] = -reduced[row][free]
            assert all(sum(matrix[i][j] * exact_vector[active[j]] for j in range(len(active))) == 0
                       for i in range(4))
            description = {"type": "exact_dependency_of_always_active_affine_coordinates",
                           "free_unit": active[free]}
    if description is not None:
        scale = max(abs(x) for x in exact_vector)
        null = np.asarray([float(x / scale) for x in exact_vector])
        null /= np.linalg.norm(null)
        description.update({"exact_unnormalized_vector": [str(x) for x in exact_vector],
                            "unit_vector": null.tolist(),
                            "scope": "analytic real-valued ReLU function with stored binary64 coefficients on the declared input box; floating-point execution checked separately"})
    return {"units": units, "always_inactive": inactive, "always_active": active,
            "variable": variable, "exact_active_weight_rank": len(pivots),
            "hidden_difference_rank_upper_bound": min(32, len(variable) + len(pivots)),
            "guaranteed_nullspace_dimension_lower_bound": max(0, 32 - len(variable) - len(pivots)),
            "null_direction": description}, null


def masks_for(fitted):
    result = {"fractional_mask": np.asarray(fitted["mask"]["values"], dtype=np.float64)}
    for name, subset in (("binary_global", fitted["binary_global"]["subset"]),
                         ("frozen_original", fitted["original_subset"])):
        result[name] = np.zeros(32)
        result[name][subset] = 1
    return result


def projector_for(mask, v, null):
    a = mask * v
    deficit = float(np.sum(mask * (1 - mask) * v ** 2))
    if null is None:
        return {"constructed": False, "reason": "No analytic null direction found by the declared supplementary geometry construction."}, None
    b = float((2 * a - v) @ null)
    if deficit == 0:
        shift = 0.0
    else:
        denominator = np.sqrt(b * b + 4 * deficit) + abs(b)
        shift = (1.0 if b >= 0 else -1.0) * 2 * deficit / denominator
    coefficient = a + shift * null
    norm2 = float(coefficient @ coefficient)
    projector = np.outer(coefficient, coefficient) / norm2 if norm2 else np.zeros((32, 32))
    actual_coefficient = projector @ v
    record = {"constructed": True, "fractional_coefficient": a.tolist(),
              "projector_coefficient": coefficient.tolist(), "null_shift": shift,
              "full_coefficient_sphere_deficit": deficit,
              "projector_sphere_equality_error": float(abs(coefficient @ v - norm2)),
              "projector_symmetry_max_error": float(np.max(abs(projector - projector.T))),
              "projector_idempotence_max_error": float(np.max(abs(projector @ projector - projector))),
              "projector_head_coefficient_max_error": float(np.max(abs(actual_coefficient - coefficient))),
              "projector_rank": 1 if norm2 else 0,
              "new_fit": False, "DAS_executed": False,
              "jointly_orthogonal_role_projectors_claimed": False,
              "interpretation": "algebraic per-role output equivalence through an analytic activation-difference null direction; not newly identified native structure"}
    return record, actual_coefficient


def mean_square(x):
    return float(np.mean(x * x))


def analyze():
    wall, cpu = time.perf_counter(), time.process_time()
    checked = R.verify(RUN)
    if checked["prepared_units_verified"] != 15 or checked["evaluation_units_verified"] != 15:
        raise RuntimeError("All registered study preparations and evaluations must be complete before this analysis.")
    cfg, source_cfg, originals, bound = R.verify_freeze()
    prep_manifest = F.load_json(RUN / "preparation_complete.json")
    eval_manifest = F.load_json(RUN / "evaluation_complete.json")
    prep = {(u["kind"], u["index"]): F.load_json(RUN / u["file"]) for u in prep_manifest["units"]}
    ev = {(u["kind"], u["index"]): F.load_json(RUN / u["file"]) for u in eval_manifest["units"]}
    coverage, decomposition, geometries, projectors, compositions, provenance, quadratics = [], [], [], [], [], [], []
    candidate_scores = 0
    discovery_regenerated = validation_regenerated = 0
    for index in range(5):
        net = N.MLP.from_dict(originals[index]["network"])
        soft, search = prep[("soft_mask", index)], prep[("search", index)]
        geo, null = geometry(net)
        geo["model_index"] = index
        geometries.append(geo)
        model_pairs, role_masks, role_projector_coefficients = [], [], []
        for role in (0, 1):
            fitted = soft["roles"][role]
            masks = masks_for(fitted)
            role_masks.append(masks)
            discovery, generated = N.make_pairs(source_cfg, soft["discovery_seed"],
                cfg["soft_mask"]["discovery_pairs_per_stratum"], role, 100 + 10 * role)
            base, donor = N._stack_pairs(discovery)
            pair_hash = N.array_hash(base, donor)
            if pair_hash != soft["discovery_pair_hashes"][role] or pair_hash != search["selection_data_hashes"]["role_pairs"][role]:
                raise ArithmeticError("Regenerated discovery pairs differ from the registered shared population.")
            hb, hd = net.hidden(base), net.hidden(donor)
            expected = N.high_prediction(base, donor, role, "identity")
            target = np.log(expected) - np.log1p(-expected) - (hb @ net.v + net.beta)
            a = (hd - hb) * net.v
            if N.array_hash(a, target) != fitted["discovery_matrix_hash"]:
                raise ArithmeticError("Regenerated discovery quadratic input hash changed.")
            gram = a.T @ a / len(a)
            gram = (gram + gram.T) * .5
            linear, constant = a.T @ target / len(a), float(np.mean(target ** 2))
            if N.array_hash(gram, linear, np.asarray([constant])) != fitted["binary_global"]["quadratic_coefficients_hash"]:
                raise ArithmeticError("Regenerated quadratic coefficients changed.")
            global_value = fitted["binary_global"]["direct_discovery_logit_mse"]
            quadratics.append({"model_index": index, "role": role, "gram": gram.tolist(),
                "linear": linear.tolist(), "constant": constant, "matrix_hash": fitted["discovery_matrix_hash"],
                "quadratic_hash": fitted["binary_global"]["quadratic_coefficients_hash"]})
            for family, records in search["candidate_pools"].items():
                pool = records[role]["candidate_pool"]
                candidate_masks = np.zeros((len(pool), 32))
                candidate_masks[np.arange(len(pool))[:, None], np.asarray(pool)] = 1
                values = np.einsum("bi,ij,bj->b", candidate_masks, gram, candidate_masks, optimize=True) - 2 * (candidate_masks @ linear) + constant
                candidate_scores += len(pool)
                for budget in (128, 1024):
                    best_index = int(np.argmin(values[:budget]))
                    best_value = float(values[best_index])
                    for selector in ("frozen_mse", "robust"):
                        name = f"{family}/budget_{budget}/{selector}"
                        selected = search["alignments"][name]["roles"][role]["selected_index"]
                        selected_value = float(values[selected])
                        coverage.append({"model_index": index, "role": role, "family": family,
                            "budget": budget, "selector": selector, "selected_index": selected,
                            "selected_discovery_logit_mse": selected_value,
                            "best_pool_logit_index_analysis_only": best_index,
                            "best_pool_discovery_logit_mse": best_value,
                            "global_binary_discovery_logit_mse": global_value,
                            "selection_objective_gap": selected_value - best_value,
                            "candidate_coverage_gap": best_value - global_value,
                            "total_excess_over_global": selected_value - global_value,
                            "pool_attains_global_within_1e_minus_10": best_value <= global_value + 1e-10,
                            "new_pool_winner_validated_or_adopted": False})
            pairs, validation_generation = N.make_pairs(source_cfg, soft["validation_seed"],
                cfg["soft_mask"]["validation_pairs_per_stratum"], role, 200 + 10 * role)
            validation_hash = N.array_hash(*N._stack_pairs(pairs))
            if (validation_hash != ev[("soft_mask", index)]["validation_pair_hashes"][role]
                    or validation_hash != ev[("search", index)]["validation_data_hashes"]["role_pairs"][role]):
                raise ArithmeticError("Regenerated validation pairs differ from the registered shared population.")
            model_pairs.append(pairs)
            projection, projection_coefficient = projector_for(masks["fractional_mask"], net.v, null)
            projection.update({"model_index": index, "role": role,
                "validation_logit_equivalence_max_error": 0.0, "validation_null_difference_max_abs": 0.0})
            role_projector_coefficients.append(projection_coefficient)
            for stratum in N.STRATA:
                base, donor = pairs[stratum]
                hb, hd = net.hidden(base), net.hidden(donor)
                delta_hidden = hd - hb
                jb, jd = N.action_costs(base), N.action_costs(donor)
                base_z = hb @ net.v + net.beta
                optimal_z = np.log(jb[:, 0]) - np.log(jb[:, 1])
                sign = 1 if role == 0 else -1
                ell_b, ell_d = sign * np.log(jb[:, role]), sign * np.log(jd[:, role])
                expected = N.high_prediction(base, donor, role, "identity")
                expected_z = np.log(expected) - np.log1p(-expected)
                e = base_z - optimal_z
                for method, mask in masks.items():
                    coefficient = net.v * mask
                    phi_b, phi_d = hb @ coefficient, hd @ coefficient
                    delta_r = (phi_d - ell_d) - (phi_b - ell_b)
                    actual_z = base_z + delta_hidden @ coefficient
                    total = actual_z - expected_z
                    identity_error = float(np.max(abs(total - e - delta_r)))
                    if identity_error > 1e-11:
                        raise ArithmeticError("Native-head error decomposition failed.")
                    actual = N.sigmoid(actual_z)
                    energies = np.mean((delta_hidden * coefficient) ** 2, axis=0)
                    energy_sum = float(energies.sum())
                    participation = energy_sum ** 2 / float(energies @ energies) if energy_sum else 0.0
                    decomposition.append({"model_index": index, "role": role, "stratum": stratum,
                        "method": method, "n": len(base), "base_logit_mse": mean_square(e),
                        "contribution_residual_change_mse": mean_square(delta_r),
                        "twice_cross_moment": float(2 * np.mean(e * delta_r)),
                        "total_logit_mse": mean_square(total),
                        "decomposition_max_identity_error": identity_error,
                        "probability_mae": float(np.mean(abs(actual - expected))),
                        "base_probability_mae": float(np.mean(abs(N.sigmoid(base_z) - N.optimal_probability(base)))),
                        "unchanged_target_output_effect_rms": float(np.sqrt(np.mean((actual - N.sigmoid(base_z)) ** 2))) if stratum == "equal_target" else None,
                        "native_coordinate_change_second_moments": energies.tolist(),
                        "native_energy_participation_count": participation,
                        "energy_ignores_cross_coordinate_cancellation": True})
                if projection_coefficient is not None:
                    projection["validation_logit_equivalence_max_error"] = max(
                        projection["validation_logit_equivalence_max_error"],
                        float(np.max(abs(delta_hidden @ (projection_coefficient - masks["fractional_mask"] * net.v)))))
                    projection["validation_null_difference_max_abs"] = max(
                        projection["validation_null_difference_max_abs"], float(np.max(abs(delta_hidden @ null))))
            projectors.append(projection)
            discovery_regenerated += len(N.STRATA) * cfg["soft_mask"]["discovery_pairs_per_stratum"]
            validation_regenerated += len(N.STRATA) * cfg["soft_mask"]["validation_pairs_per_stratum"]
            provenance.append({"model_index": index, "role": role, "discovery_pair_hash": pair_hash,
                "validation_pair_hash": validation_hash, "discovery_generation_work": generated,
                "validation_generation_work": validation_generation,
                "same_arrays_regenerated_not_new_independent_population": True})
        # Secondary joint panel: existing role0 near bases/donors, role1 near
        # donors. This combination is not claimed to satisfy a frozen stratum.
        base, donor0 = model_pairs[0]["mixed_near"]
        donor1 = model_pairs[1]["mixed_near"][1]
        hb, h0, h1 = net.hidden(base), net.hidden(donor0), net.hidden(donor1)
        j0, j1 = N.action_costs(donor0)[:, 0], N.action_costs(donor1)[:, 1]
        target = j0 / (j0 + j1)
        for method in METHODS:
            m0, m1 = role_masks[0][method], role_masks[1][method]
            h01 = (1 - m1) * ((1 - m0) * hb + m0 * h0) + m1 * h1
            h10 = (1 - m0) * ((1 - m1) * hb + m1 * h1) + m0 * h0
            z01, z10 = h01 @ net.v + net.beta, h10 @ net.v + net.beta
            predicted_difference = (h1 - h0) @ (net.v * m0 * m1)
            identity_error = float(np.max(abs(z01 - z10 - predicted_difference)))
            if identity_error > 1e-11:
                raise ArithmeticError("Two-donor affine commutator identity failed.")
            p01, p10 = N.sigmoid(z01), N.sigmoid(z10)
            compositions.append({"model_index": index, "method": method, "n": len(base),
                "panel": "existing_role0_mixed_near_bases_and_donors_plus_existing_role1_mixed_near_donors",
                "frozen_joint_stratum_claimed": False, "secondary_development_only": True,
                "order_logit_rms": float(np.sqrt(mean_square(z01 - z10))),
                "order_probability_rms": float(np.sqrt(mean_square(p01 - p10))),
                "order_probability_max_abs": float(np.max(abs(p01 - p10))),
                "role0_then_role1_joint_probability_mae": float(np.mean(abs(p01 - target))),
                "role1_then_role0_joint_probability_mae": float(np.mean(abs(p10 - target))),
                "commutator_identity_max_error": identity_error,
                "overlap_product_mass": float(np.sum(m0 * m1)),
                "nonzero_overlap_count": int(np.count_nonzero(m0 * m1 > 1e-10)),
                "commutator_native_coefficient": (net.v * m0 * m1).tolist(),
                "panel_inputs_hash": N.array_hash(base, donor0, donor1)})
        if all(x is not None for x in role_projector_coefficients):
            q0, q1 = role_projector_coefficients
            geo["constructed_role_projector_coefficient_dot_product"] = float(q0 @ q1)
            geo["constructed_role_projector_coefficient_cosine"] = float((q0 @ q1) / max(np.linalg.norm(q0) * np.linalg.norm(q1), 1e-30))
    return {"schema": "f15-nd01-mechanism-analysis-v1", "development_only": True,
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "contributor": "ChatGPT (GPT-6 Astra Pro)", "script_sha256": F.file_digest(__file__),
        "freeze": bound, "preparation_manifest_sha256": F.file_digest(RUN / "preparation_complete.json"),
        "evaluation_manifest_sha256": F.file_digest(RUN / "evaluation_complete.json"),
        "candidate_objective_coverage": coverage, "error_decomposition": decomposition,
        "network_geometry": geometries, "constructed_projector_equivalence": projectors,
        "secondary_composition": compositions, "regeneration_provenance": provenance,
        "discovery_quadratics": quadratics,
        "resource": {"wall_seconds": time.perf_counter() - wall,
            "cpu_seconds": time.process_time() - cpu,
            "existing_discovery_pairs_regenerated": discovery_regenerated,
            "existing_validation_pairs_regenerated": validation_regenerated,
            "additional_independent_populations": 0, "new_fits": 0,
            "saved_candidate_logit_scores_computed": candidate_scores,
            "new_validation_method_selection": False}}


def main():
    destination = HERE / "mechanism_results.json"
    if destination.exists():
        raise FileExistsError("Preserve the existing analysis output; do not silently overwrite it.")
    result = analyze()
    F.write_json(destination, result, exclusive=True)
    with Path(str(destination) + ".sha256").open("x") as handle:
        handle.write(F.file_digest(destination) + "\n")
    print(json.dumps({"output": str(destination), "sha256": F.file_digest(destination),
        "coverage_rows": len(result["candidate_objective_coverage"]),
        "decomposition_rows": len(result["error_decomposition"]),
        "geometries": len(result["network_geometry"]), "resource": result["resource"]}, indent=2))


if __name__ == "__main__":
    main()
