"""F15-ND01 development-only continuous coordinate-mask diagnostic.

The original trained network and its affine output head remain fixed.  A mask
in [0, 1]^32 with mass eight mixes donor hidden coordinates into the base.
Discovery minimizes mean logit squared error with projected gradient descent.
Its convex first-order gap bounds this finite discovery objective only; it is
not a lower bound for probability MAE or for an unseen population.

The caller must durably save, reload, hash and validate all diagnostic
preparations before generating ANY validation population.  This module neither
writes files nor enforces that cross-model durability gate itself.

Contributor: ChatGPT (GPT-6 Astra Pro), F15-ND01.
"""
from __future__ import annotations

import copy
import math
import time
from typing import Any

import numpy as np

from .. import neural as N
from . import binary_global as B


EVIDENCE_TYPE = "continuous_coordinate_mask_development_only"
METHODS = ("fractional_mask", "rounded_top8", "binary_global", "frozen_original")


def defaults() -> dict[str, Any]:
    """The complete prospective soft-mask settings, copied into ND01's freeze."""
    return {
        "discovery_seeds": [1510601, 1510602, 1510603, 1510604, 1510605],
        "validation_seeds": [1510691, 1510692, 1510693, 1510694, 1510695],
        "discovery_pairs_per_stratum": 128,
        "validation_pairs_per_stratum": 8192,
        "discovery_stream_base": 100,
        "validation_stream_base": 200,
        "role_stream_stride": 10,
        "hypothesis": "identity",
        "mask_mass": 8,
        "objective": "equal_stratum_mean_logit_squared_error",
        "optimizer": "projected_gradient_fixed_lipschitz_step",
        "initial_mask": "uniform_mass_over_width",
        "max_iterations": 10000,
        "duality_gap_tolerance": 1e-8,
        "projection_bisection_iterations": 80,
        "feasibility_tolerance": 1e-12,
        "checkpoint_iterations": [0, 1, 10, 100, 1000, 10000],
        "rounding": "largest_eight_mask_values_stable_index_ties",
        "fractional_count_tolerance": 1e-10,
        "formal_probability_support_assessed": False,
        "technical_superposition_assessed": False,
        "native_head_retained": True,
        "binary_global": True,
        "binary_global_width": 32,
        "binary_global_mass": 8,
        "binary_global_expected_subsets": 10518300,
        "binary_global_objective": "same_finite_discovery_logit_squared_error",
        "binary_global_tie_policy": B.TIE_POLICY,
        "binary_global_recomputation_tolerance": 1e-10,
        "binary_global_flags": B.FLAGS.copy(),
    }


def _settings(config: dict[str, Any], index: int,
              diagnostic_config: dict[str, Any] | None = None):
    c = N.validate_config(config)
    s = defaults() if diagnostic_config is None else diagnostic_config
    if c != N.defaults() or s != defaults():
        raise ValueError("Soft-mask diagnostic settings differ from the declared ND01 settings.")
    if type(index) is not int or not 0 <= index < 5:
        raise ValueError("Soft-mask model index must be one of the five frozen models.")
    return c, s


def _logit(probability: np.ndarray) -> np.ndarray:
    p = np.asarray(probability, dtype=np.float64)
    if not np.isfinite(p).all() or np.any((p <= 0) | (p >= 1)):
        raise ValueError("The high-level intervention probability must lie strictly inside (0, 1).")
    return np.log(p) - np.log1p(-p)


def project_capped_simplex(value: np.ndarray, mass: int, iterations: int = 80):
    """Euclidean projection: m_i = clip(value_i - lambda, 0, 1).

    Bisection is followed by a deterministic, roundoff-sized mass correction.
    No optimization or validation outcomes affect its fixed iteration budget.
    """
    value = np.asarray(value, dtype=np.float64)
    if value.ndim != 1 or not np.isfinite(value).all() or not 0 < mass < len(value):
        raise ValueError("Projection requires a finite vector and a proper positive mass.")
    lo, hi = float(np.min(value) - 1.0), float(np.max(value))
    for _ in range(iterations):
        mid = (lo + hi) * 0.5
        if float(np.sum(np.clip(value - mid, 0.0, 1.0))) > mass:
            lo = mid
        else:
            hi = mid
    result = np.clip(value - (lo + hi) * 0.5, 0.0, 1.0)
    difference = float(mass - np.sum(result))
    # Preserve the constraint numerically without another optimizer step.
    for j in range(len(result)):
        if difference == 0.0:
            break
        change = min(difference, 1.0 - result[j]) if difference > 0 else max(difference, -result[j])
        result[j] += change
        difference = float(mass - np.sum(result))
    return result


def _mask_record(mask: np.ndarray, tolerance: float):
    return {
        "values": mask.tolist(), "mass": float(np.sum(mask)),
        "minimum": float(np.min(mask)), "maximum": float(np.max(mask)),
        "nonzero_count": int(np.count_nonzero(mask > tolerance)),
        "fractional_count": int(np.count_nonzero((mask > tolerance) & (mask < 1 - tolerance))),
        "one_count": int(np.count_nonzero(mask >= 1 - tolerance)),
        "count_tolerance": tolerance,
    }


def fit_mask(a: np.ndarray, target: np.ndarray, settings: dict[str, Any]):
    """Fit a convex quadratic and retain a numerical first-order certificate.

    With gradient g, min_{s in capped simplex} g.s is the sum of the eight
    smallest entries of g.  Convexity gives f(m)-gap <= f* <= f(m) for a
    feasible iterate.  Bounds use float64, not certified interval arithmetic.
    The same lower bound applies to binary masks for this discovery logit MSE.
    """
    a, target = np.asarray(a, dtype=np.float64), np.asarray(target, dtype=np.float64)
    if (a.ndim != 2 or target.shape != (len(a),) or not len(a)
            or not np.isfinite(a).all() or not np.isfinite(target).all()):
        raise ValueError("Nonfinite or incompatible discovery least-squares arrays.")
    n, width = a.shape
    mass = settings["mask_mass"]
    gram, linear = a.T @ a / n, a.T @ target / n
    gram = (gram + gram.T) * 0.5
    eigenvalues = np.linalg.eigvalsh(gram)
    lipschitz = float(2 * max(float(eigenvalues[-1]), 0.0))
    mask = np.full(width, mass / width, dtype=np.float64)
    checkpoints = []

    def state(iteration: int):
        residual = a @ mask - target
        objective = float(np.mean(residual ** 2))
        gradient = 2 * (gram @ mask - linear)
        order = np.argsort(gradient, kind="stable")
        gap = float(gradient @ mask - np.sum(gradient[order[:mass]]))
        if gap < -settings["feasibility_tolerance"]:
            raise ArithmeticError("Negative first-order gap beyond numerical tolerance.")
        gap = max(gap, 0.0)
        return {"iteration": iteration, "objective": objective, "duality_gap": gap,
                "relaxed_optimum_lower_bound": max(0.0, objective - gap),
                "relaxed_optimum_upper_bound": objective,
                "mass_error": float(abs(np.sum(mask) - mass)),
                "gradient_linear_minimizer_subset": sorted(order[:mass].tolist())}

    current = state(0)
    checkpoints.append(current)
    performed = 0
    for iteration in range(1, settings["max_iterations"] + 1):
        if current["duality_gap"] <= settings["duality_gap_tolerance"]:
            break
        if lipschitz <= 0.0:
            raise ArithmeticError("Nonzero gradient gap with zero quadratic Lipschitz constant.")
        gradient = 2 * (gram @ mask - linear)
        mask = project_capped_simplex(mask - gradient / lipschitz, mass,
                                      settings["projection_bisection_iterations"])
        performed = iteration
        # Gap from the small quadratic avoids a 640-by-32 product every step.
        gradient = 2 * (gram @ mask - linear)
        gap = float(gradient @ mask - np.sum(np.sort(gradient, kind="stable")[:mass]))
        if gap < -settings["feasibility_tolerance"]:
            raise ArithmeticError("Negative first-order gap beyond numerical tolerance.")
        current = {"duality_gap": max(gap, 0.0)}
        if (iteration in settings["checkpoint_iterations"]
                or current["duality_gap"] <= settings["duality_gap_tolerance"]):
            current = state(iteration)
            checkpoints.append(current)
    final = state(performed)
    if checkpoints[-1]["iteration"] != performed:
        checkpoints.append(final)
    if (np.min(mask) < 0 or np.max(mask) > 1
            or final["mass_error"] > settings["feasibility_tolerance"]):
        raise ArithmeticError("Final mask violates the capped-simplex constraint.")
    rounded = sorted(np.argsort(-mask, kind="stable")[:mass].tolist())
    return {
        "mask": _mask_record(mask, settings["fractional_count_tolerance"]),
        "rounded_subset": rounded,
        "discovery_objective": final["objective"],
        "certificate": {**final, "scope": "finite_discovery_logit_mse",
                        "binary_mask_lower_bound": final["relaxed_optimum_lower_bound"],
                        "probability_mae_lower_bound_claimed": False,
                        "validation_population_bound_claimed": False,
                        "certified_interval_arithmetic": False},
        "optimizer": {"method": settings["optimizer"], "iterations": performed,
                      "max_iterations": settings["max_iterations"],
                      "duality_gap_tolerance": settings["duality_gap_tolerance"],
                      "duality_gap_converged": final["duality_gap"] <= settings["duality_gap_tolerance"],
                      "lipschitz_constant": lipschitz,
                      "gram_minimum_eigenvalue": float(eigenvalues[0]),
                      "checkpoints": checkpoints},
        "discovery_matrix_hash": N.array_hash(a, target),
        "discovery_rows": n,
    }


def _verify_original(original: dict[str, Any], c: dict[str, Any], index: int):
    unhashed = {k: v for k, v in original.items() if k != "artifact_hash"}
    if (original.get("artifact_hash") != N.canonical_hash(unhashed)
            or original.get("config_hash") != N.canonical_hash(c)
            or original.get("config") != c
            or original.get("discovery_seed") != c["model_seeds"][index]
            or original.get("evaluation_generated") is not False):
        raise ValueError("Original F15 preparation identity or hash mismatch.")


def prepare_one(original: dict[str, Any], config: dict[str, Any], index: int,
                diagnostic_config: dict[str, Any] | None = None):
    """Prepare both masks on new discovery pairs; generate no validation data."""
    c, s = _settings(config, index, diagnostic_config)
    _verify_original(original, c, index)
    wall, cpu = time.perf_counter(), time.process_time()
    net = N.MLP.from_dict(original["network"])
    seed = s["discovery_seeds"][index]
    roles, hashes, generations = [], [], []
    for role in (0, 1):
        pairs, generation = N.make_pairs(c, seed, s["discovery_pairs_per_stratum"], role,
                                         s["discovery_stream_base"] + s["role_stream_stride"] * role)
        base, donor = N._stack_pairs(pairs)
        hb, hd = net.hidden(base), net.hidden(donor)
        base_z = hb @ net.v + net.beta
        expected_z = _logit(N.high_prediction(base, donor, role, "identity"))
        a, target = (hd - hb) * net.v, expected_z - base_z
        fitted = fit_mask(a, target, s)
        fitted["binary_global"] = B.solve_discovery(a, target, s)
        fitted["role"] = role
        fitted["original_subset"] = copy.deepcopy(original["alignments"]["identity/aligned"]["roles"][role]["subset"])
        roles.append(fitted)
        hashes.append(N.array_hash(base, donor))
        generations.append(generation)
    result = {
        "schema": "f15-nd01-soft-mask-prepared-v1", "evidence_type": EVIDENCE_TYPE,
        "development_only": True, "model_index": index,
        "original_model_seed": c["model_seeds"][index],
        "original_prepared_artifact_hash": original["artifact_hash"],
        "original_network_hash": N.canonical_hash(original["network"]),
        "network": copy.deepcopy(original["network"]),
        "frozen_neural_config_hash": N.canonical_hash(c),
        "diagnostic_config": copy.deepcopy(s), "diagnostic_config_hash": N.canonical_hash(s),
        "discovery_seed": seed, "validation_seed": s["validation_seeds"][index],
        "discovery_pair_hashes": hashes, "discovery_pair_generation": generations,
        "roles": roles, "evaluation_generated": False,
        "native_head_retained": True, "new_training_steps": 0,
        "resource": {"wall_seconds": time.perf_counter() - wall,
                     "cpu_seconds": time.process_time() - cpu,
                     "fitted_masks": 2, "discovery_pairs": 2 * len(N.STRATA) * s["discovery_pairs_per_stratum"],
                     "hidden_forward_examples": 4 * len(N.STRATA) * s["discovery_pairs_per_stratum"],
                     "optimizer_iterations": sum(r["optimizer"]["iterations"] for r in roles),
                     "binary_subsets_enumerated": sum(r["binary_global"]["enumerated_subsets"] for r in roles),
                     "solver_child_cpu_seconds": sum(
                         r["binary_global"]["resource"]["child_user_cpu_seconds"]
                         + r["binary_global"]["resource"]["child_system_cpu_seconds"] for r in roles)},
    }
    result["artifact_hash"] = N.canonical_hash(result)
    validate_prepared(result, original, config, index, s)
    return result


def validate_prepared(prepared: dict[str, Any], original: dict[str, Any],
                      config: dict[str, Any], index: int,
                      diagnostic_config: dict[str, Any] | None = None):
    """Validate a reloaded preparation without generating any input arrays."""
    c, s = _settings(config, index, diagnostic_config)
    if (prepared.get("schema") != "f15-nd01-soft-mask-prepared-v1"
            or prepared.get("evidence_type") != EVIDENCE_TYPE
            or prepared.get("development_only") is not True
            or prepared.get("model_index") != index
            or prepared.get("diagnostic_config") != s
            or prepared.get("diagnostic_config_hash") != N.canonical_hash(s)
            or prepared.get("frozen_neural_config_hash") != N.canonical_hash(c)
            or prepared.get("original_model_seed") != c["model_seeds"][index]
            or prepared.get("discovery_seed") != s["discovery_seeds"][index]
            or prepared.get("validation_seed") != s["validation_seeds"][index]
            or prepared.get("evaluation_generated") is not False
            or prepared.get("native_head_retained") is not True
            or prepared.get("new_training_steps") != 0):
        raise ValueError("Soft-mask preparation identity, configuration or split mismatch.")
    unhashed = {k: v for k, v in prepared.items() if k != "artifact_hash"}
    if (prepared.get("artifact_hash") != N.canonical_hash(unhashed)
            or prepared.get("original_network_hash") != N.canonical_hash(prepared["network"])):
        raise ValueError("Soft-mask preparation hash mismatch.")
    net = N.MLP.from_dict(prepared["network"])
    if (net.w.shape != (4, 32) or net.b.shape != (32,) or net.v.shape != (32,)
            or not all(np.isfinite(x).all() for x in (net.w, net.b, net.v))
            or not math.isfinite(net.beta)):
        raise ValueError("Soft-mask preparation network shape or finiteness mismatch.")
    _verify_original(original, c, index)
    if (prepared["original_prepared_artifact_hash"] != original["artifact_hash"]
            or prepared["network"] != original["network"]):
        raise ValueError("Soft-mask network differs from the original F15 model.")
    if len(prepared.get("roles", [])) != 2 or len(prepared.get("discovery_pair_hashes", [])) != 2:
        raise ValueError("Soft-mask preparation lacks a complete role or pair-hash record.")
    for role, fitted in enumerate(prepared["roles"]):
        mask = np.asarray(fitted["mask"]["values"], dtype=np.float64)
        if (fitted["role"] != role or mask.shape != (32,) or not np.isfinite(mask).all()
                or np.any((mask < 0) | (mask > 1))
                or abs(float(np.sum(mask)) - s["mask_mass"]) > s["feasibility_tolerance"]
                or fitted["mask"] != _mask_record(mask, s["fractional_count_tolerance"])):
            raise ValueError("Saved continuous mask is inconsistent or infeasible.")
        expected_rounded = sorted(np.argsort(-mask, kind="stable")[:s["mask_mass"]].tolist())
        if fitted["rounded_subset"] != expected_rounded:
            raise ValueError("Saved rounded mask does not follow the declared rule.")
        subset = fitted["original_subset"]
        if (len(subset) != 8 or len(set(subset)) != 8
                or any(type(j) is not int or not 0 <= j < 32 for j in subset)):
            raise ValueError("Original subset is not an eight-coordinate mask.")
        if subset != original["alignments"]["identity/aligned"]["roles"][role]["subset"]:
            raise ValueError("Original subset differs from frozen F15 discovery selection.")
        certificate, optimizer = fitted["certificate"], fitted["optimizer"]
        if (not 0 <= optimizer["iterations"] <= s["max_iterations"]
                or not 0 <= certificate["relaxed_optimum_lower_bound"] <= certificate["relaxed_optimum_upper_bound"]
                or certificate["objective"] != fitted["discovery_objective"]
                or certificate["relaxed_optimum_upper_bound"] != fitted["discovery_objective"]
                or optimizer["duality_gap_converged"] != (certificate["duality_gap"] <= s["duality_gap_tolerance"])):
            raise ValueError("Soft-mask saved optimization certificate is inconsistent.")
        B.validate_result(fitted["binary_global"], s)
        if fitted["binary_global"]["discovery_matrix_hash"] != fitted["discovery_matrix_hash"]:
            raise ValueError("Binary and fractional masks did not fit identical discovery arrays.")
        if (fitted["binary_global"]["direct_discovery_logit_mse"]
                + fitted["binary_global"]["objective_recomputation_allowed_discrepancy"]
                < certificate["relaxed_optimum_lower_bound"]):
            raise ValueError("Exhaustive binary objective violates the relaxed numerical lower bound.")
    return True


def evaluate_one(prepared: dict[str, Any], original: dict[str, Any],
                 config: dict[str, Any], index: int,
                 diagnostic_config: dict[str, Any] | None = None):
    """Evaluate saved masks on the predeclared new development validation pairs."""
    c, s = _settings(config, index, diagnostic_config)
    validate_prepared(prepared, original, config, index, s)
    wall, cpu = time.perf_counter(), time.process_time()
    net = N.MLP.from_dict(prepared["network"])
    seed = s["validation_seeds"][index]
    rows, pooled_rows, comparisons, hashes, generations = [], [], [], [], []
    for role in (0, 1):
        pairs, generation = N.make_pairs(c, seed, s["validation_pairs_per_stratum"], role,
                                         s["validation_stream_base"] + s["role_stream_stride"] * role)
        hashes.append(N.array_hash(*N._stack_pairs(pairs)))
        generations.append(generation)
        fitted = prepared["roles"][role]
        masks = {"fractional_mask": np.asarray(fitted["mask"]["values"], dtype=np.float64)}
        for method, subset in (("rounded_top8", fitted["rounded_subset"]),
                               ("binary_global", fitted["binary_global"]["subset"]),
                               ("frozen_original", fitted["original_subset"])):
            masks[method] = np.zeros(c["width"], dtype=np.float64)
            masks[method][subset] = 1.0
        pooled = {method: {"actual": [], "expected": [], "logit_error": []} for method in METHODS}
        for stratum in N.STRATA:
            base, donor = pairs[stratum]
            hb, hd = net.hidden(base), net.hidden(donor)
            base_z = hb @ net.v + net.beta
            expected = N.high_prediction(base, donor, role, "identity")
            expected_z = _logit(expected)
            base_p, optimal_base_p = N.sigmoid(base_z), N.optimal_probability(base)
            absolute_errors = {}
            for method in METHODS:
                actual_z = base_z + ((hd - hb) * net.v) @ masks[method]
                actual = N.sigmoid(actual_z)
                logit_error = actual_z - expected_z
                metrics = N._basic_error(actual, expected)
                metrics.update({
                    "model_index": index, "role": role, "stratum": stratum, "method": method,
                    "logit_mse": float(np.mean(logit_error ** 2)),
                    "logit_rmse": float(np.sqrt(np.mean(logit_error ** 2))),
                    "decision_disagreement": 1.0 - metrics["decision_agreement"],
                    "adjusted_effect_rmse": float(np.sqrt(np.mean(((actual - base_p) - (expected - optimal_base_p)) ** 2))),
                    "expected_effect_rms": float(np.sqrt(np.mean((expected - optimal_base_p) ** 2))),
                    "observed_effect_rms": float(np.sqrt(np.mean((actual - base_p) ** 2))),
                    "unchanged_target_output_effect_rms": float(np.sqrt(np.mean((actual - base_p) ** 2))) if stratum == "equal_target" else None,
                    "base_prediction": N._basic_error(base_p, optimal_base_p),
                    "no_swap": N._basic_error(base_p, expected),
                    "whole_layer_swap": N._basic_error(N.sigmoid(hd @ net.v + net.beta), expected),
                    "output_hash": N.array_hash(actual, expected, actual_z, expected_z),
                })
                rows.append(metrics)
                absolute_errors[method] = np.abs(actual - expected)
                pooled[method]["actual"].append(actual)
                pooled[method]["expected"].append(expected)
                pooled[method]["logit_error"].append(logit_error)
            for comparator in ("rounded_top8", "binary_global", "frozen_original"):
                improvement = absolute_errors[comparator] - absolute_errors["fractional_mask"]
                comparisons.append({"model_index": index, "role": role, "stratum": stratum,
                    "method": "fractional_mask", "comparator": comparator,
                    **N._comparison_statistics(improvement),
                    "improvement_hash": N.array_hash(improvement), "formal_support_assessed": False})
        for method in METHODS:
            actual = np.concatenate(pooled[method]["actual"])
            expected = np.concatenate(pooled[method]["expected"])
            logit_error = np.concatenate(pooled[method]["logit_error"])
            pooled_rows.append({"model_index": index, "role": role, "method": method,
                                "weighting": "equal_five_strata", **N._basic_error(actual, expected),
                                "logit_mse": float(np.mean(logit_error ** 2)),
                                "logit_rmse": float(np.sqrt(np.mean(logit_error ** 2)))})
    result = {
        "schema": "f15-nd01-soft-mask-validation-v1", "evidence_type": EVIDENCE_TYPE,
        "development_only": True, "model_index": index,
        "prepared_artifact_hash": prepared["artifact_hash"],
        "original_prepared_artifact_hash": prepared["original_prepared_artifact_hash"],
        "original_network_hash": prepared["original_network_hash"],
        "diagnostic_config_hash": prepared["diagnostic_config_hash"],
        "validation_seed": seed, "validation_pairs_per_stratum": s["validation_pairs_per_stratum"],
        "validation_pair_hashes": hashes, "validation_pair_generation": generations,
        "methods": list(METHODS), "rows": rows, "pooled_rows": pooled_rows,
        "paired_comparisons": comparisons, "formal_support_assessed": False,
        "technical_superposition_assessed": False, "native_utility_representation_claimed": False,
        "intervention_family": "fractional_coordinate_mask_fixed_native_head_mass_eight",
        "resource": {"wall_seconds": time.perf_counter() - wall,
                     "cpu_seconds": time.process_time() - cpu,
                     "validation_pairs": 2 * len(N.STRATA) * s["validation_pairs_per_stratum"],
                     "hidden_forward_examples": 4 * len(N.STRATA) * s["validation_pairs_per_stratum"],
                     "mask_pair_evaluations": len(METHODS) * 2 * len(N.STRATA) * s["validation_pairs_per_stratum"],
                     "new_training_steps": 0, "validation_fitting_steps": 0},
    }
    result["artifact_hash"] = N.canonical_hash(result)
    return result
