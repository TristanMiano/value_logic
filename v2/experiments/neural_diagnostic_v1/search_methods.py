"""F15-ND01 development comparison of extraction from fixed F15 networks.

Authored by ChatGPT (GPT-6 Astra Pro).  This module never trains a network and
never writes a file.  The caller must durably save and validate *all five*
``prepare_one`` returns before calling ``evaluate_one`` even once.  All results
are development diagnostics, with descriptive paired moments rather than a new
confirmatory interpretation of the F15 endpoint.

``cfg`` contains the unchanged F14 neural configuration under ``neural`` plus
the diagnostic settings documented by ``effective_settings``.  Search and
validation have disjoint seeds.  Each proposal family produces one 1024-member
pool per cost role.  Both budget prefixes and both selection objectives reuse
that pool and its already computed scores; actual and logical costs are separate.
"""
from __future__ import annotations

import copy
import itertools
import time
from typing import Any

import numpy as np

from v2.experiments import neural as N


FAMILIES = (
    "cost_corr", "uniform", "permuted_cost_corr", "log_cost_corr",
    "positive_contribution_cov",
)
SELECTORS = ("frozen_mse", "robust")
DEFAULT_SEARCH_SEEDS = (1510601, 1510602, 1510603, 1510604, 1510605)
DEFAULT_VALIDATION_SEEDS = (1510691, 1510692, 1510693, 1510694, 1510695)
SCHEMA_PREPARED = "f15-nd01-fixed-model-search-prepared-v1"
SCHEMA_EVALUATED = "f15-nd01-fixed-model-search-evaluated-v1"


def effective_settings(cfg: dict[str, Any]) -> dict[str, Any]:
    """Resolve the deliberately small public configuration interface.

    Diagnostic keys are flat.  The original neural configuration is retained
    unchanged: only the sample counts explicitly passed to its pure generators
    differ, if specified in this new development plan.
    """
    base = copy.deepcopy(cfg.get("neural", N.defaults()))
    N.validate_config(base)
    settings = {
        "neural": base,
        "search_seeds": list(cfg.get("search_seeds", DEFAULT_SEARCH_SEEDS)),
        "validation_seeds": list(cfg.get("validation_seeds", DEFAULT_VALIDATION_SEEDS)),
        "proposal_families": list(cfg.get("proposal_families", FAMILIES)),
        "budget_prefixes": list(cfg.get("budget_prefixes", (128, 1024))),
        "selectors": list(cfg.get("selectors", SELECTORS)),
        "search_candidate_count": cfg.get("search_candidate_count", 1024),
        "fit_samples": cfg.get("fit_samples", 1024),
        "selection_pairs_per_stratum": cfg.get("selection_pairs_per_stratum", 128),
        "validation_pairs_per_stratum": cfg.get("validation_pairs_per_stratum", 8192),
        "task_validation_samples": cfg.get("task_validation_samples", 8192),
        "mae_scale": cfg.get("mae_scale", 0.05),
        "near_disagreement_scale": cfg.get("near_disagreement_scale", 0.35),
        "far_disagreement_scale": cfg.get("far_disagreement_scale", 0.10),
    }
    if settings["proposal_families"] != list(FAMILIES):
        raise ValueError("F15-ND01 requires its five prespecified proposal families in order.")
    if settings["selectors"] != list(SELECTORS):
        raise ValueError("F15-ND01 requires frozen_mse and robust selectors in order.")
    if settings["budget_prefixes"] != [128, 1024] or settings["search_candidate_count"] != 1024:
        raise ValueError("F15-ND01 compares the nested 128 and 1024 proposal budgets.")
    for key in ("fit_samples", "selection_pairs_per_stratum",
                "validation_pairs_per_stratum", "task_validation_samples"):
        if not isinstance(settings[key], int) or settings[key] <= 0:
            raise ValueError(f"{key} must be a positive integer.")
    for key, expected in (("mae_scale", 0.05), ("near_disagreement_scale", 0.35),
                          ("far_disagreement_scale", 0.10)):
        if settings[key] != expected:
            raise ValueError(f"F15-ND01 retains the declared {key}={expected} normalization.")
    if len(settings["search_seeds"]) != 5 or len(settings["validation_seeds"]) != 5:
        raise ValueError("One search seed and one validation seed are required for each of five fixed models.")
    all_seeds = [*settings["search_seeds"], *settings["validation_seeds"],
                 *base["model_seeds"], *base["evaluation_seeds"],
                 base["development_seed"], base["development_evaluation_seed"]]
    if any(not isinstance(seed, int) for seed in all_seeds) or len(all_seeds) != len(set(all_seeds)):
        raise ValueError("Original, development search, and validation seed streams must be disjoint integers.")
    return settings


def _network(network: dict[str, Any]) -> N.MLP:
    net = N.MLP.from_dict(network)
    if net.w.shape != (4, 32) or net.b.shape != (32,) or net.v.shape != (32,):
        raise ValueError("Require the original four-input, 32-hidden-unit network.")
    if not all(np.isfinite(a).all() for a in (net.w, net.b, net.v)) or not np.isfinite(net.beta):
        raise ValueError("Network parameters must be finite.")
    return net


def _absolute_correlations(hidden: np.ndarray, target: np.ndarray) -> np.ndarray:
    hc, yc = hidden - hidden.mean(axis=0), target - target.mean()
    denominator = np.sqrt(np.sum(hc ** 2, axis=0) * np.sum(yc ** 2))
    return np.divide(np.abs(hc.T @ yc), denominator,
                     out=np.zeros(hidden.shape[1]), where=denominator > 1e-12)


def _proposal_pool(net: N.MLP, hidden: np.ndarray, costs: np.ndarray,
                   permuted_costs: np.ndarray, settings: dict[str, Any],
                   seed: int, family: str, role: int) -> tuple[list[list[int]], dict[str, Any]]:
    base = settings["neural"]
    proposal_cfg = {**base, "candidate_count": settings["search_candidate_count"]}
    signed_log_target = (1 if role == 0 else -1) * np.log(costs[:, role])
    fraction, width = base["proposal_uniform_mixture"], hidden.shape[1]
    uniform_fallback = False
    if family in ("cost_corr", "uniform", "permuted_cost_corr"):
        target = permuted_costs[:, role] if family == "permuted_cost_corr" else costs[:, role]
        original_control = "random" if family == "uniform" else "aligned"
        pool = N.candidate_pool(hidden, target, proposal_cfg, seed, original_control, role)
        scores = _absolute_correlations(hidden, target)
        weights = (np.ones(width) / width if family == "uniform" else
                   fraction / width + (1 - fraction) * (scores + 1e-12) / np.sum(scores + 1e-12))
        target_name = "permuted_J" if family == "permuted_cost_corr" else "J"
        score_definition = "uniform" if family == "uniform" else "absolute_Pearson_correlation(hidden_j, target)"
    else:
        if family == "log_cost_corr":
            scores = _absolute_correlations(hidden, signed_log_target)
            weights = fraction / width + (1 - fraction) * (scores + 1e-12) / np.sum(scores + 1e-12)
            score_definition = "absolute_Pearson_correlation(hidden_j, signed_log_J)"
        elif family == "positive_contribution_cov":
            contributions = hidden * net.v
            centered_target = signed_log_target - signed_log_target.mean()
            covariance = ((contributions - contributions.mean(axis=0)).T @ centered_target) / len(hidden)
            target_variance = float(np.mean(centered_target ** 2))
            scores = np.maximum(covariance, 0) / max(target_variance, 1e-12)
            uniform_fallback = not bool(np.any(scores > 0))
            weights = (np.ones(width) / width if uniform_fallback else
                       fraction / width + (1 - fraction) * scores / scores.sum())
            score_definition = "max(population_covariance(v_j*hidden_j, signed_log_J),0)/population_variance(signed_log_J)"
        else:
            raise ValueError(f"Unknown proposal family {family!r}.")
        target_name = "signed_log_J"
        rng = N._rng(seed, 50 + role)
        pool = [] if uniform_fallback else [sorted(np.argsort(-scores, kind="stable")[:base["subset_size"]].tolist())]
        while len(pool) < settings["search_candidate_count"]:
            pool.append(sorted(rng.choice(width, size=base["subset_size"], replace=False,
                                          p=None if uniform_fallback else weights).tolist()))
    return pool, {
        "family": family, "role": role, "target": target_name,
        "score_definition": score_definition, "scores": scores.tolist(),
        "sampling_weights": weights.tolist(), "uniform_mixture": fraction,
        "uniform_fallback": uniform_fallback, "rng_stream": 50 + role,
        "rng_coupling": "same seed and stream across proposal families, family-specific proposal weights",
        "first_candidate": "uniform_draw" if family == "uniform" or uniform_fallback else "stable_top_eight_scores",
        "duplicates_consume_budget": True,
        "unique_candidates": len({tuple(candidate) for candidate in pool}),
        "pool_hash": N.canonical_hash(pool),
    }


def _pair_cache(net: N.MLP, pairs: dict[str, tuple[np.ndarray, np.ndarray]], role: int) -> dict[str, Any]:
    result = {}
    for stratum in N.STRATA:
        base, donor = pairs[stratum]
        hb, hd = net.hidden(base), net.hidden(donor)
        base_logit = hb @ net.v + net.beta
        result[stratum] = {
            "hb": hb, "hd": hd, "delta_hidden": hd - hb,
            "base_logit": base_logit, "base_probability": N.sigmoid(base_logit),
            "donor_probability": N.sigmoid(hd @ net.v + net.beta),
            "base_optimal": N.optimal_probability(base),
            "expected": N.high_prediction(base, donor, role, "identity"),
        }
    return result


def _selection_arrays(cache: dict[str, Any]) -> dict[str, np.ndarray]:
    return {key: np.concatenate([cache[s][key] for s in N.STRATA], axis=0)
            for key in ("delta_hidden", "base_logit", "base_probability", "base_optimal", "expected")}


def _candidate_score(net: N.MLP, subset: list[int], arrays: dict[str, np.ndarray],
                     settings: dict[str, Any], decoder_nmse: float) -> dict[str, Any]:
    probability = N.sigmoid(arrays["base_logit"] + arrays["delta_hidden"][:, subset] @ net.v[subset])
    n = settings["selection_pairs_per_stratum"]
    error = probability - arrays["expected"]
    error_by_stratum = error.reshape(len(N.STRATA), n)
    disagreement = ((probability >= 0.5) != (arrays["expected"] >= 0.5)).reshape(len(N.STRATA), n)
    maes = np.mean(np.abs(error_by_stratum), axis=1)
    mses = np.mean(error_by_stratum ** 2, axis=1)
    disagreements = disagreement.mean(axis=1)
    equal_index = N.STRATA.index("equal_target")
    effects = (probability - arrays["base_probability"]).reshape(len(N.STRATA), n)
    equal_effect = float(np.sqrt(np.mean(effects[equal_index] ** 2)))
    normalized = [*(maes / settings["mae_scale"]).tolist(),
                  float(disagreements[N.STRATA.index("mixed_near")] / settings["near_disagreement_scale"]),
                  float(disagreements[N.STRATA.index("mixed_far")] / settings["far_disagreement_scale"])]
    return {
        "probability_mse": float(np.mean(error ** 2)),
        "effect_mse": float(np.mean(((probability - arrays["base_probability"]) -
                                      (arrays["expected"] - arrays["base_optimal"])) ** 2)),
        "decoder_nmse": decoder_nmse,
        "robust_max_normalized_error": max(normalized),
        "robust_normalized_components": normalized,
        "equal_target_output_effect_rms": equal_effect,
        "per_stratum": {stratum: {
            "mae": float(maes[i]), "mse": float(mses[i]),
            "decision_disagreement": float(disagreements[i]),
            "unchanged_target_output_effect_rms": equal_effect if stratum == "equal_target" else None,
        } for i, stratum in enumerate(N.STRATA)},
    }


def _choose_candidate(scores: list[dict[str, Any]], selector: str, tolerance: float) -> int:
    if selector == "frozen_mse":
        return N._choose_candidate(scores, tolerance)
    if selector != "robust":
        raise ValueError(f"Unknown selector {selector!r}.")
    best = 0
    keys = ("robust_max_normalized_error", "probability_mse", "equal_target_output_effect_rms")
    for index in range(1, len(scores)):
        for key in keys:
            delta = scores[index][key] - scores[best][key]
            if abs(delta) <= tolerance:
                continue
            if delta < 0:
                best = index
            break
    return best


def _alignment_key(family: str, budget: int, selector: str) -> str:
    return f"{family}/budget_{budget}/{selector}"


def _original_check(original: dict[str, Any], settings: dict[str, Any], index: int) -> N.MLP:
    if index not in range(5):
        raise ValueError("Model index must be zero through four.")
    if original.get("artifact_hash") != N.canonical_hash({k: v for k, v in original.items() if k != "artifact_hash"}):
        raise ValueError("Original F15 prepared artifact hash mismatch.")
    if original.get("config_hash") != N.canonical_hash(settings["neural"]):
        raise ValueError("The diagnostic base must equal the original frozen neural configuration.")
    if original.get("config") != settings["neural"]:
        raise ValueError("Original F15 saved configuration differs from the diagnostic's frozen base.")
    if original.get("discovery_seed") != settings["neural"]["model_seeds"][index]:
        raise ValueError("Original model and requested index do not match.")
    if original.get("evaluation_generated") is not False:
        raise ValueError("Require the original pre-evaluation discovery artifact.")
    return _network(original["network"])


def prepare_one(original_prepared: dict[str, Any], cfg: dict[str, Any], index: int) -> dict[str, Any]:
    """Search a saved ordinary-trained F15 model; generate no validation data."""
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    settings = effective_settings(cfg)
    net = _original_check(original_prepared, settings, index)
    seed = settings["search_seeds"][index]
    inputs = N.sample_inputs(N._rng(seed, 10), settings["fit_samples"])
    hidden, costs = net.hidden(inputs), N.concepts(inputs, "identity")
    permuted_costs = costs[N._rng(seed, 61).permutation(len(costs))]
    pairs, generation, caches = [], [], []
    for role in (0, 1):
        p, generated = N.make_pairs(settings["neural"], seed,
                                    settings["selection_pairs_per_stratum"], role, 100 + 10 * role)
        pairs.append(p)
        generation.append(generated)
        caches.append(_pair_cache(net, p, role))
    arrays = [_selection_arrays(cache) for cache in caches]
    pools, alignments = {}, {}
    decoder_fits = candidate_evaluations = 0
    for family in settings["proposal_families"]:
        pools[family] = []
        for role in (0, 1):
            pool, proposal = _proposal_pool(net, hidden, costs, permuted_costs, settings, seed, family, role)
            decoder_target = permuted_costs[:, role] if family == "permuted_cost_corr" else costs[:, role]
            scores, decoders = [], []
            for subset in pool:
                decoder, nmse = N.fit_decoder(hidden, decoder_target, subset,
                                              settings["neural"]["decoder_ridge"])
                scores.append(_candidate_score(net, subset, arrays[role], settings, nmse))
                decoders.append(decoder)
                decoder_fits += 1
                candidate_evaluations += 1
            pools[family].append({"role": role, "proposal": proposal,
                                   "candidate_pool": pool, "candidate_scores": scores})
            for budget in settings["budget_prefixes"]:
                for selector in settings["selectors"]:
                    name = _alignment_key(family, budget, selector)
                    if name not in alignments:
                        alignments[name] = {"family": family, "budget": budget, "selector": selector,
                                            "g_id": "identity", "roles": []}
                    chosen = _choose_candidate(scores[:budget], selector,
                                                settings["neural"]["ranking_tie_tolerance"])
                    subset = pool[chosen]
                    contribution = hidden[:, subset] @ net.v[subset]
                    signed_log_target = (1 if role == 0 else -1) * np.log(costs[:, role])
                    alignments[name]["roles"].append({
                        "role": role, "selected_index": chosen, "subset": subset,
                        "decoder": decoders[chosen], "selection_score": scores[chosen],
                        "log_contribution_offset": float(np.mean(contribution - signed_log_target)),
                        "logical_candidate_evaluations": budget, "logical_decoder_fits": budget,
                    })
    for alignment in alignments.values():
        alignment["overlap"] = sorted(set(alignment["roles"][0]["subset"]) &
                                       set(alignment["roles"][1]["subset"]))
        alignment["mean_selection_probability_mse"] = float(np.mean([
            role["selection_score"]["probability_mse"] for role in alignment["roles"]]))
    logical_candidates = len(FAMILIES) * 2 * len(SELECTORS) * sum(settings["budget_prefixes"])
    selection_rows_per_role = len(N.STRATA) * settings["selection_pairs_per_stratum"]
    result = {
        "schema": SCHEMA_PREPARED, "development_only": True, "model_index": index,
        "config_hash": N.canonical_hash(cfg), "config": copy.deepcopy(cfg),
        "effective_settings": settings,
        "source_original_artifact_hash": original_prepared["artifact_hash"],
        "source_original_config_hash": original_prepared["config_hash"],
        "source_model_seed": original_prepared["discovery_seed"],
        "source_network_hash": N.canonical_hash(original_prepared["network"]),
        "network": copy.deepcopy(original_prepared["network"]),
        "network_hash": N.canonical_hash(original_prepared["network"]),
        "original_f15_identity_subsets": [copy.deepcopy(r["subset"])
                                         for r in original_prepared["alignments"]["identity/aligned"]["roles"]],
        "search_seed": seed, "validation_seed": settings["validation_seeds"][index],
        "candidate_pools": pools, "alignments": alignments,
        "selection_pair_generation": generation,
        "selection_data_hashes": {"fit_inputs": N.array_hash(inputs),
                                  "permuted_cost_targets": N.array_hash(permuted_costs),
                                  "role_pairs": [N.array_hash(*N._stack_pairs(p)) for p in pairs]},
        "evaluation_generated": False,
        "resource": {
            "new_training_steps": 0, "new_network_training_labels": 0,
            "fixed_networks": 1, "proposal_families": len(FAMILIES),
            "role_pools": len(FAMILIES) * 2, "logical_alignment_variants": len(alignments),
            "candidate_evaluations_actual": candidate_evaluations,
            "decoder_fits_actual": decoder_fits,
            "candidate_evaluations_logical_without_shared_scores": logical_candidates,
            "decoder_fits_logical_without_shared_scores": logical_candidates,
            "selection_pair_evaluations_actual": candidate_evaluations * selection_rows_per_role,
            "selection_pair_evaluations_logical_without_shared_scores": logical_candidates * selection_rows_per_role,
            "fit_hidden_forward_examples_actual": settings["fit_samples"],
            "selection_hidden_forward_examples_actual": 4 * selection_rows_per_role,
            "selected_coordinate_blocks_unique": sum(len({tuple(a["roles"][r]["subset"])
                                                            for a in alignments.values()}) for r in (0, 1)),
            "reuse_policy": "1024 scores per family/role serve both nested budget prefixes and both selectors; duplicate proposals still consume a candidate evaluation and decoder fit",
            "wall_seconds": time.perf_counter() - started_wall,
            "cpu_seconds": time.process_time() - started_cpu,
        },
    }
    result["artifact_hash"] = N.canonical_hash(result)
    validate_prepared(result, cfg, index)
    return result


def validate_prepared(prepared: dict[str, Any], cfg: dict[str, Any], index: int) -> None:
    """Read-only structural/hash checks; never draw any random samples."""
    settings = effective_settings(cfg)
    if index not in range(5) or prepared.get("model_index") != index:
        raise ValueError("Prepared model index mismatch.")
    if prepared.get("schema") != SCHEMA_PREPARED or prepared.get("evaluation_generated") is not False:
        raise ValueError("Require a pre-validation F15-ND01 prepared artifact.")
    if prepared.get("config_hash") != N.canonical_hash(cfg) or prepared.get("config") != cfg:
        raise ValueError("Diagnostic preparation/configuration mismatch.")
    if prepared.get("effective_settings") != settings:
        raise ValueError("Effective settings mismatch.")
    unhashed = {key: value for key, value in prepared.items() if key != "artifact_hash"}
    if prepared.get("artifact_hash") != N.canonical_hash(unhashed):
        raise ValueError("Diagnostic prepared artifact hash mismatch.")
    _network(prepared["network"])
    network_hash = N.canonical_hash(prepared["network"])
    if network_hash != prepared.get("network_hash") or network_hash != prepared.get("source_network_hash"):
        raise ValueError("The prepared network must be byte-equivalent in canonical JSON to its saved F15 source.")
    if prepared.get("source_model_seed") != settings["neural"]["model_seeds"][index]:
        raise ValueError("Prepared network source/index mismatch.")
    if prepared.get("search_seed") != settings["search_seeds"][index] or prepared.get("validation_seed") != settings["validation_seeds"][index]:
        raise ValueError("Prepared seed assignment mismatch.")
    expected_keys = {_alignment_key(f, b, s) for f in FAMILIES
                     for b in settings["budget_prefixes"] for s in SELECTORS}
    if set(prepared["alignments"]) != expected_keys or set(prepared["candidate_pools"]) != set(FAMILIES):
        raise ValueError("Incomplete prepared family/budget/selector product.")
    for family in FAMILIES:
        if len(prepared["candidate_pools"][family]) != 2:
            raise ValueError("Each candidate family must have two role pools.")
        for role, pool_record in enumerate(prepared["candidate_pools"][family]):
            pool, scores = pool_record["candidate_pool"], pool_record["candidate_scores"]
            if pool_record["role"] != role or len(pool) != 1024 or len(scores) != 1024:
                raise ValueError("Candidate pool length or role mismatch.")
            if N.canonical_hash(pool) != pool_record["proposal"]["pool_hash"]:
                raise ValueError("Candidate pool hash mismatch.")
            if any(subset != sorted(set(subset)) or len(subset) != 8 or
                   any(not isinstance(unit, int) or unit < 0 or unit >= 32 for unit in subset)
                   for subset in pool):
                raise ValueError("Every candidate must contain exactly eight distinct hidden coordinates.")
            for budget in settings["budget_prefixes"]:
                for selector in SELECTORS:
                    alignment = prepared["alignments"][_alignment_key(family, budget, selector)]
                    if len(alignment["roles"]) != 2:
                        raise ValueError("Every selected alignment requires both roles.")
                    selection = alignment["roles"][role]
                    chosen = _choose_candidate(scores[:budget], selector,
                                                settings["neural"]["ranking_tie_tolerance"])
                    if selection["role"] != role or selection["selected_index"] != chosen:
                        raise ValueError("Saved selection differs from the declared discovery ranking.")
                    if selection["subset"] != pool[chosen] or selection["selection_score"] != scores[chosen]:
                        raise ValueError("Saved selection does not match the candidate pool/score.")
                    if selection["decoder"]["subset"] != selection["subset"] or len(selection["decoder"]["coefficient"]) != 8:
                        raise ValueError("Decoder/subset mismatch.")


def _subset_validation(net: N.MLP, subset: list[int], cache: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    metrics, raw = {}, {}
    for stratum in N.STRATA:
        row = cache[stratum]
        probability = N.sigmoid(row["base_logit"] + row["delta_hidden"][:, subset] @ net.v[subset])
        expected, base_probability = row["expected"], row["base_probability"]
        effects = probability - base_probability
        expected_effects = expected - row["base_optimal"]
        metric = N._basic_error(probability, expected)
        metric.update({
            "decision_disagreement": float(np.mean((probability >= 0.5) != (expected >= 0.5))),
            "base_prediction": N._basic_error(base_probability, row["base_optimal"]),
            "adjusted_effect_rmse": float(np.sqrt(np.mean((effects - expected_effects) ** 2))),
            "expected_effect_rms": float(np.sqrt(np.mean(expected_effects ** 2))),
            "observed_effect_rms": float(np.sqrt(np.mean(effects ** 2))),
            "unchanged_target_output_effect_rms": float(np.sqrt(np.mean(effects ** 2))) if stratum == "equal_target" else None,
            "no_swap": N._basic_error(base_probability, expected),
            "whole_layer_swap": N._basic_error(row["donor_probability"], expected),
        })
        metrics[stratum] = metric
        raw[stratum] = {"probability": probability, "absolute_error": np.abs(probability - expected)}
    return metrics, raw


def _role_summary(metrics: dict[str, Any], settings: dict[str, Any]) -> dict[str, Any]:
    components = [*[metrics[s]["mae"] / settings["mae_scale"] for s in N.STRATA],
                  metrics["mixed_near"]["decision_disagreement"] / settings["near_disagreement_scale"],
                  metrics["mixed_far"]["decision_disagreement"] / settings["far_disagreement_scale"]]
    return {
        "equal_stratum_mean_mae": float(np.mean([metrics[s]["mae"] for s in N.STRATA])),
        "equal_stratum_mean_mse": float(np.mean([metrics[s]["mse"] for s in N.STRATA])),
        "worst_stratum_mae": max(metrics[s]["mae"] for s in N.STRATA),
        "robust_normalized_components": components,
        "robust_max_normalized_error": max(components),
        "unchanged_target_output_effect_rms": metrics["equal_target"]["unchanged_target_output_effect_rms"],
        "descriptive_error_and_decision_thresholds_met": max(components) <= 1,
        "interpretation": "point-estimate diagnostic only; neither confidence-qualified adequacy nor the complete F15 support criterion",
    }


def _paired_comparison(raw: dict[str, Any], candidate: str, reference: str) -> dict[str, Any]:
    roles = []
    for role in (0, 1):
        improvements = [raw[reference][role][s]["absolute_error"] - raw[candidate][role][s]["absolute_error"]
                        for s in N.STRATA]
        roles.append({
            "role": role,
            "strata": {s: N._comparison_statistics(improvement) for s, improvement in zip(N.STRATA, improvements)},
            "pooled_equal_strata": N._comparison_statistics(np.concatenate(improvements)),
        })
    return {
        "candidate": candidate, "reference": reference,
        "positive_improvement_favors": "candidate",
        "theoretical_pairwise_range": [-1, 1],
        "inference": "descriptive sufficient moments; fixed stratification is retained; no confirmatory interval or support claim",
        "roles": roles,
    }


def evaluate_one(prepared: dict[str, Any], cfg: dict[str, Any], index: int) -> dict[str, Any]:
    """Validate saved choices on fresh development rows; never search or fit.

    A per-model hash check cannot enforce the cross-model temporal gate.  The
    caller is responsible for the durable all-five preparation manifest before
    invoking this function for any model, and for recording first exposure.
    """
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    validate_prepared(prepared, cfg, index)
    settings = effective_settings(cfg)
    seed, n = prepared["validation_seed"], settings["validation_pairs_per_stratum"]
    net = _network(prepared["network"])
    pairs, generation, caches = [], [], []
    for role in (0, 1):
        p, generated = N.make_pairs(settings["neural"], seed, n, role, 200 + 10 * role)
        pairs.append(p)
        generation.append(generated)
        caches.append(_pair_cache(net, p, role))
    inputs = N.sample_inputs(N._rng(seed, 300), settings["task_validation_samples"])
    hidden, task_target = net.hidden(inputs), N.optimal_probability(inputs)
    learned = N.sigmoid(hidden @ net.v + net.beta)
    costs = N.concepts(inputs, "identity")
    task = N._basic_error(learned, task_target)
    regrets = np.where(learned >= 0.5, costs[:, 1], costs[:, 0]) - costs.min(axis=1)
    task["mean_decision_regret"] = float(np.mean(regrets))
    task["max_decision_regret"] = float(np.max(regrets))
    evaluated, raw, subset_cache = {}, {}, {}
    for name, alignment in prepared["alignments"].items():
        role_metrics, role_summaries, raw[name] = [], [], []
        decoder_errors, log_errors = [], []
        for role, selection in enumerate(alignment["roles"]):
            key = (role, tuple(selection["subset"]))
            if key not in subset_cache:
                subset_cache[key] = _subset_validation(net, selection["subset"], caches[role])
            metrics, raw_role = subset_cache[key]
            role_metrics.append(copy.deepcopy(metrics))
            role_summaries.append(_role_summary(metrics, settings))
            raw[name].append(raw_role)
            decoder_errors.append(float(np.sqrt(np.mean((N.decode(hidden, selection["decoder"]) - costs[:, role]) ** 2)) /
                                        max(float(np.std(costs[:, role])), 1e-12)))
            contribution = hidden[:, selection["subset"]] @ net.v[selection["subset"]]
            signed_log_target = (1 if role == 0 else -1) * np.log(costs[:, role])
            log_errors.append(float(np.sqrt(np.mean((contribution - signed_log_target -
                                                     selection["log_contribution_offset"]) ** 2))))
        evaluated[name] = {
            "family": alignment["family"], "budget": alignment["budget"],
            "selector": alignment["selector"], "g_id": "identity", "overlap": alignment["overlap"],
            "selected_subsets": [r["subset"] for r in alignment["roles"]],
            "roles": role_metrics, "role_summaries": role_summaries,
            "observational_decoder_nrmse": decoder_errors,
            "observational_log_contribution_rmse": log_errors,
            "observational_metrics_are_not_causal_support": True,
        }
    matched, budget_comparisons, selector_comparisons, family_comparisons = {}, {}, {}, {}
    for family in FAMILIES:
        for budget in settings["budget_prefixes"]:
            for selector in SELECTORS:
                name = _alignment_key(family, budget, selector)
                matched[name] = {control: _paired_comparison(raw, name, _alignment_key(control, budget, selector))
                                 for control in ("uniform", "permuted_cost_corr") if control != family}
            key = f"{family}/budget_{budget}"
            selector_comparisons[key] = _paired_comparison(raw, _alignment_key(family, budget, "robust"),
                                                          _alignment_key(family, budget, "frozen_mse"))
        for selector in SELECTORS:
            key = f"{family}/{selector}"
            budget_comparisons[key] = _paired_comparison(raw, _alignment_key(family, 1024, selector),
                                                        _alignment_key(family, 128, selector))
    for candidate, reference in itertools.combinations(FAMILIES, 2):
        for budget in settings["budget_prefixes"]:
            for selector in SELECTORS:
                key = f"{candidate}_versus_{reference}/budget_{budget}/{selector}"
                family_comparisons[key] = _paired_comparison(raw, _alignment_key(candidate, budget, selector),
                                                            _alignment_key(reference, budget, selector))
    unique_blocks = len(subset_cache)
    rows_per_role = len(N.STRATA) * n
    result = {
        "schema": SCHEMA_EVALUATED, "development_only": True, "model_index": index,
        "config_hash": N.canonical_hash(cfg), "prepared_artifact_hash": prepared["artifact_hash"],
        "source_original_artifact_hash": prepared["source_original_artifact_hash"],
        "network_hash": prepared["network_hash"], "source_model_seed": prepared["source_model_seed"],
        "search_seed": prepared["search_seed"], "validation_seed": seed,
        "task": task, "evaluated": evaluated,
        "matched_control_comparisons": matched, "budget_comparisons": budget_comparisons,
        "selector_comparisons": selector_comparisons, "family_comparisons": family_comparisons,
        "pair_generation": generation,
        "validation_data_hashes": {"task_inputs": N.array_hash(inputs),
                                   "role_pairs": [N.array_hash(*N._stack_pairs(p)) for p in pairs]},
        "evaluation_generated": True,
        "resource": {
            "new_training_steps": 0, "new_network_training_labels": 0,
            "validation_searches": 0, "validation_decoder_fits": 0,
            "validation_pairs_generated": 2 * rows_per_role,
            "validation_hidden_forward_examples_actual": 4 * rows_per_role + len(inputs),
            "task_examples": len(inputs), "unique_selected_role_subsets_evaluated": unique_blocks,
            "intervention_pair_evaluations_actual": unique_blocks * rows_per_role,
            "intervention_pair_evaluations_logical_without_subset_reuse": len(evaluated) * 2 * rows_per_role,
            "logical_alignment_variants": len(evaluated),
            "reuse_policy": "all selected methods share the same independent stratified validation rows; identical role/subset predictions are evaluated once and reused without extra evidence credit",
            "wall_seconds": time.perf_counter() - started_wall,
            "cpu_seconds": time.process_time() - started_cpu,
        },
    }
    result["artifact_hash"] = N.canonical_hash(result)
    return result
