"""Independent numerical checks using only manufactured generic arrays.

No F15 model is loaded and no experiment input/pair generator is invoked.
Contributor: ChatGPT (GPT-6 Astra Pro), independent ND01 protocol audit.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from v2.experiments import neural as N
from v2.experiments.neural_diagnostic_v1 import calibration_endpoint as C
from v2.experiments.neural_diagnostic_v1 import search_methods as S
from v2.experiments.neural_diagnostic_v1 import soft_mask as M


def main():
    checks = []

    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)

    cfg_path = ROOT / "v2/experiments/neural_diagnostic_v1/config.json"
    cfg = json.loads(cfg_path.read_text())
    settings = S.effective_settings(cfg["search"])
    C._config(cfg["calibration"])
    check("soft_mask_config_equals_declared_defaults", cfg["soft_mask"] == M.defaults())
    check("search_and_soft_discovery_seeds_match", settings["search_seeds"] == cfg["soft_mask"]["discovery_seeds"])
    check("search_and_soft_validation_seeds_match", settings["validation_seeds"] == cfg["soft_mask"]["validation_seeds"])
    check("search_and_soft_discovery_counts_match", settings["selection_pairs_per_stratum"] == cfg["soft_mask"]["discovery_pairs_per_stratum"])
    check("search_and_soft_validation_counts_match", settings["validation_pairs_per_stratum"] == cfg["soft_mask"]["validation_pairs_per_stratum"])
    calibration_seeds = cfg["calibration"]["neural"]["model_seeds"] + cfg["calibration"]["neural"]["evaluation_seeds"]
    original = settings["neural"]
    other_seeds = (settings["search_seeds"] + settings["validation_seeds"] + original["model_seeds"]
                   + original["evaluation_seeds"] + [original["development_seed"], original["development_evaluation_seed"]])
    check("calibration_seeds_disjoint_from_all_other_populations", not set(calibration_seeds) & set(other_seeds))

    projected = M.project_capped_simplex(np.array([1.2, 0.7, 0.2, -0.3]), 2)
    check("capped_simplex_known_solution", np.max(np.abs(projected - [1.0, 0.75, 0.25, 0.0])) < 1e-12)
    check("capped_simplex_feasible", abs(projected.sum() - 2.0) < 1e-12 and np.all((0 <= projected) & (projected <= 1)))
    for name, target, optimum in (
            ("binary", np.r_[np.ones(8), np.zeros(24)], 0.0),
            ("fractional", np.r_[np.full(16, 0.5), np.zeros(16)], 0.0),
            ("positive_minimum", np.full(32, -0.25), 0.25)):
        fitted = M.fit_mask(np.eye(32), target, M.defaults())
        certificate = fitted["certificate"]
        check(f"quadratic_{name}_known_optimum", abs(fitted["discovery_objective"] - optimum) < 1e-12)
        check(f"quadratic_{name}_gap_brackets_optimum", certificate["relaxed_optimum_lower_bound"] <= optimum + 1e-12
              and certificate["relaxed_optimum_upper_bound"] >= optimum - 1e-12)
        check(f"quadratic_{name}_gap_converged", fitted["optimizer"]["duality_gap_converged"])
        check(f"quadratic_{name}_scope", certificate["scope"] == "finite_discovery_logit_mse"
              and not certificate["probability_mae_lower_bound_claimed"] and not certificate["validation_population_bound_claimed"])

    x = np.linspace(-0.4, 0.4, 33)
    hidden = np.column_stack([(i + 1) * (x + 1.0) for i in range(32)])
    costs = np.column_stack([np.exp(x), np.exp(-x)])
    permuted = costs[::-1]
    v = np.r_[np.ones(16), -np.ones(16)]
    net = N.MLP(np.zeros((4, 32)), np.zeros(32), v, 0.0)
    generic_seed = 999001  # Synthetic proposal test only; no experiment population.
    for family, original_control, target in (
            ("cost_corr", "aligned", costs[:, 0]),
            ("uniform", "random", costs[:, 0]),
            ("permuted_cost_corr", "aligned", permuted[:, 0])):
        pool, record = S._proposal_pool(net, hidden, costs, permuted, settings, generic_seed, family, 0)
        original_prefix = N.candidate_pool(hidden, target, {**original, "candidate_count": 128}, generic_seed, original_control, 0)
        check(f"{family}_literal_128_prefix", pool[:128] == original_prefix)
        check(f"{family}_full_budget", len(pool) == 1024)
        check(f"{family}_valid_size8_subsets", all(len(s) == 8 and len(set(s)) == 8 and all(0 <= i < 32 for i in s) for s in pool))
        check(f"{family}_recorded_pool_hash", record["pool_hash"] == N.canonical_hash(pool))
    pool, record = S._proposal_pool(net, hidden, costs, permuted, settings, generic_seed, "positive_contribution_cov", 0)
    positive_scores = np.asarray(record["scores"])
    check("positive_covariance_respects_native_output_sign", np.all(positive_scores[:16] > 0) and np.all(positive_scores[16:] == 0))
    check("positive_covariance_weights_normalize", abs(sum(record["sampling_weights"]) - 1.0) < 1e-12)
    check("positive_covariance_retains_uniform_floor", min(record["sampling_weights"]) >= 0.25 / 32 - 1e-12)
    zero_head = N.MLP(net.w.copy(), net.b.copy(), np.zeros(32), 0.0)
    fallback, record = S._proposal_pool(zero_head, hidden, costs, permuted, settings, generic_seed, "positive_contribution_cov", 0)
    uniform, _ = S._proposal_pool(zero_head, hidden, costs, permuted, settings, generic_seed, "uniform", 0)
    check("zero_head_covariance_has_literal_uniform_fallback", record["uniform_fallback"] and fallback == uniform)

    manufactured_scores = [
        {"probability_mse": 0.001, "effect_mse": 0.001, "decoder_nmse": 0.1,
         "robust_max_normalized_error": 1.2, "equal_target_output_effect_rms": 0.1},
        {"probability_mse": 0.002, "effect_mse": 0.002, "decoder_nmse": 0.2,
         "robust_max_normalized_error": 0.8, "equal_target_output_effect_rms": 0.2}]
    check("frozen_selector_uses_mean_MSE", S._choose_candidate(manufactured_scores, "frozen_mse", 1e-12) == 0)
    check("robust_selector_uses_worst_normalized_requirement", S._choose_candidate(manufactured_scores, "robust", 1e-12) == 1)
    tie = [{**manufactured_scores[1], "probability_mse": 0.003}, manufactured_scores[1]]
    check("robust_selector_MSE_tiebreak", S._choose_candidate(tie, "robust", 1e-12) == 1)

    n = 2
    arrays = {"delta_hidden": np.linspace(-0.3, 0.4, 10 * 32).reshape(10, 32),
              "base_logit": np.linspace(-0.2, 0.1, 10),
              "base_probability": np.linspace(0.42, 0.55, 10),
              "base_optimal": np.linspace(0.40, 0.54, 10),
              "expected": np.linspace(0.35, 0.70, 10)}
    subset = list(range(8))
    score = S._candidate_score(net, subset, arrays, {**settings, "selection_pairs_per_stratum": n}, 0.0)
    z = arrays["base_logit"] + sum(arrays["delta_hidden"][:, j] * v[j] for j in subset)
    probabilities = 1.0 / (1.0 + np.exp(-z))
    differences = probabilities - arrays["expected"]
    maes = [float(np.mean(np.abs(differences[i * n:(i + 1) * n]))) for i in range(5)]
    disagreement = [(probabilities[i * n:(i + 1) * n] >= 0.5) != (arrays["expected"][i * n:(i + 1) * n] >= 0.5) for i in range(5)]
    components = [*[value / 0.05 for value in maes], float(np.mean(disagreement[0])) / 0.35, float(np.mean(disagreement[1])) / 0.10]
    check("candidate_score_native_swap_matches_literal_sum", abs(score["probability_mse"] - float(np.mean(differences ** 2))) < 1e-12)
    check("candidate_score_robust_components_match_definition", np.max(np.abs(np.asarray(score["robust_normalized_components"]) - components)) < 1e-12)
    check("candidate_score_robust_max_matches_definition", abs(score["robust_max_normalized_error"] - max(components)) < 1e-12)
    equal_slice = slice(3 * n, 4 * n)
    equal_effect = float(np.sqrt(np.mean((probabilities[equal_slice] - arrays["base_probability"][equal_slice]) ** 2)))
    check("candidate_score_equal_target_effect_is_relative_to_native_base", abs(score["equal_target_output_effect_rms"] - equal_effect) < 1e-12)

    raw = {name: [{stratum: {"absolute_error": np.array([0.1, 0.2]) + offset} for stratum in N.STRATA} for _ in range(2)]
           for name, offset in (("candidate", 0.0), ("reference", 0.05))}
    comparison = S._paired_comparison(raw, "candidate", "reference")
    check("paired_comparison_positive_favors_candidate", comparison["positive_improvement_favors"] == "candidate"
          and all(abs(row["pooled_equal_strata"]["mean_paired_absolute_error_improvement"] - 0.05) < 1e-12 for row in comparison["roles"]))
    check("paired_comparison_counts_no_cartesian_inflation", all(row["pooled_equal_strata"]["n"] == 10 for row in comparison["roles"]))

    sources = [cfg_path, Path(C.__file__), Path(S.__file__), Path(M.__file__), Path(__file__)]
    result = {"schema": "f15-nd01-independent-generic-primitive-checks-v1",
              "utc": datetime.now(timezone.utc).isoformat(), "passed": all(c["passed"] for c in checks),
              "check_count": len(checks), "checks": checks,
              "scope": "Synthetic generic arrays only; no F15 network loaded, no experiment discovery or validation generator called, no intervention outcomes from a study population observed.",
              "generic_proposal_seed": generic_seed,
              "source_hashes": [{"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in sources],
              "reviewer": "ChatGPT (GPT-6 Astra Pro), independent nd01_protocol_audit sub-agent"}
    output = Path(__file__).with_name("audit_primitive_checks.json")
    raw_output = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    with output.open("xb") as handle:
        handle.write(raw_output)
    Path(str(output) + ".sha256").write_text(hashlib.sha256(raw_output).hexdigest() + "\n")
    print(json.dumps({"passed": result["passed"], "check_count": len(checks), "experiment_populations_generated": 0}))


if __name__ == "__main__":
    main()
