"""Full frozen-endpoint calibration on five known, compiled cost layouts.

F15-ND01 DEVELOPMENT ONLY.  These are function-equivalent gauges of one
constructed network, not ordinarily trained model replicates.  Search and
assessment call the unchanged F14 modules; the known subsets never enter
search.  The caller must durably save, reload, hash, and validate ALL FIVE
prepared artifacts before calling ``evaluate_one`` for any index.

Contributor: ChatGPT (GPT-6 Astra Pro), F15-ND01.
"""
from __future__ import annotations

import copy
import math
import time
from typing import Any

import numpy as np

from .. import analysis as A
from .. import calibration as C
from .. import neural as N


MODEL_SEEDS = [1511601, 1511602, 1511603, 1511604, 1511605]
EVALUATION_SEEDS = [1511691, 1511692, 1511693, 1511694, 1511695]
LAYOUT_STREAM = 9000
EVIDENCE_TYPE = "constructed_cost_layout_full_endpoint_development_only"


def _config(config: dict[str, Any]) -> dict[str, Any]:
    """Require the frozen settings, with only the declared stream seeds changed."""
    c = N.validate_config(config)
    expected = N.defaults()
    expected["model_seeds"] = MODEL_SEEDS.copy()
    expected["evaluation_seeds"] = EVALUATION_SEEDS.copy()
    if c != expected or config.get("analysis") != A.defaults():
        raise ValueError("Calibration requires the unchanged frozen settings and declared diagnostic seeds.")
    return c


def _index(index: int) -> None:
    if type(index) is not int or not 0 <= index < len(MODEL_SEEDS):
        raise ValueError("Calibration index must name one of the five declared layouts.")


def _compiled_layout(c: dict[str, Any], seed: int):
    original, original_subsets, uniform_bound = C.compiled_cost_network()
    rng = N._rng(seed, LAYOUT_STREAM)
    permutation = rng.permutation(c["width"])
    scales = np.exp(rng.uniform(math.log(c["gauge_scale_min"]),
                               math.log(c["gauge_scale_max"]), c["width"]))
    transformed = original.gauge(permutation, scales)
    inverse = np.argsort(permutation)
    subsets = [sorted(inverse[subset].tolist()) for subset in original_subsets]
    layout = {"stream": LAYOUT_STREAM, "permutation": permutation.tolist(),
              "scales": scales.tolist(), "original_known_subsets": original_subsets,
              "known_subsets": subsets, "uniform_probability_error_bound": uniform_bound,
              "same_constructed_function_across_layouts": True,
              "independent_ordinary_training_replicates": False,
              "known_subsets_injected_into_search": False}
    return original, transformed, layout


def prepare_one(config: dict[str, Any], index: int) -> dict[str, Any]:
    """Construct and discover one layout using discovery streams only.

    ``config`` is the complete calibration subconfiguration with ``neural``
    and ``analysis`` keys.  This function does not train or write files.
    """
    c = _config(config)
    _index(index)
    seed = c["model_seeds"][index]
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    original, net, layout = _compiled_layout(c, seed)
    initial = N.MLP.initialize(c["width"], N._rng(seed, 0))
    inputs = N.sample_inputs(N._rng(seed, 10), c["fit_samples"])
    layout["discovery_function_gauge_max_error"] = float(np.max(
        np.abs(original.probability(inputs) - net.probability(inputs))))
    if layout["discovery_function_gauge_max_error"] > c["gauge_tolerance"]:
        raise ArithmeticError("Compiled layout did not preserve its ordinary function.")

    pairs, generation, wrong_pairs, wrong_generation = [], [], [], []
    for role in (0, 1):
        p, resource = N.make_pairs(c, seed, c["selection_pairs_per_stratum"],
                                   role, 100 + 10 * role)
        wrong, wrong_resource = N.make_pairs(c, seed, c["selection_pairs_per_stratum"],
                                             role, 130 + 10 * role)
        pairs.append(p)
        generation.append(resource)
        wrong_pairs.append(wrong)
        wrong_generation.append(wrong_resource)

    alignments = {}
    for g_id in N.G_FAMILY:
        for control in N.SEARCH_CONTROLS:
            selected_net = initial if control == "untrained" else net
            alignments[f"{g_id}/{control}"] = N.search_alignment(
                selected_net, c, seed, g_id, control, inputs, pairs, wrong_pairs)
    selected_alternative = min(N.G_FAMILY[1:], key=lambda g: (
        alignments[f"{g}/aligned"]["mean_selection_probability_mse"], N.G_FAMILY.index(g)))

    searches = len(N.G_FAMILY) * len(N.SEARCH_CONTROLS) * 2
    fits = searches * c["candidate_count"]
    result = {
        # This shape is accepted by the unchanged evaluator, but the metadata
        # honestly records construction and zero ordinary training.
        "schema": "f14-neural-discovery-v1", "discovery_seed": seed,
        "config_hash": N.canonical_hash(c), "config": copy.deepcopy(c),
        "network": net.to_dict(), "untrained_network": initial.to_dict(),
        "training": {"steps": 0, "batch_size": 0, "stochastic_outcome_labels": 0,
                     "expected_cost_training_labels": 0,
                     "parameter_count": int(net.w.size + net.b.size + net.v.size + 1),
                     "parameter_bytes": int(net.w.nbytes + net.b.nbytes + net.v.nbytes + 8),
                     "construction": "compiled_cost_network_then_positive_gauge_and_permutation",
                     "configured_ordinary_training_steps_not_executed": c["training_steps"],
                     "untrained_control": "direct_frozen_MLP_initializer_at_seed_stream_0"},
        "alignments": alignments, "selected_alternative": selected_alternative,
        "selection_pair_generation": generation,
        "wrong_donor_generation": wrong_generation,
        "selection_data_hashes": {
            "decoder_inputs": N.array_hash(inputs),
            "role_pairs": [N.array_hash(*N._stack_pairs(p)) for p in pairs],
            "wrong_donor_role_pairs": [N.array_hash(*N._stack_pairs(p)) for p in wrong_pairs]},
        "evaluation_generated": False,
        "diagnostic": {"evidence_type": EVIDENCE_TYPE, "development_only": True,
                       "layout_index": index, "learned_structure_evidence": False,
                       "ordinary_training_steps": 0, "layout": layout},
        "resource": {
            "hypotheses": len(N.G_FAMILY), "controls_per_hypothesis": len(N.SEARCH_CONTROLS),
            "role_searches": searches, "candidate_evaluations": fits, "decoder_fits": fits,
            "input_hidden_forward_examples_per_search": c["fit_samples"]
                + 4 * len(N.STRATA) * c["selection_pairs_per_stratum"],
            "additional_wrong_donor_hidden_examples": len(N.G_FAMILY) * 2
                * len(N.STRATA) * c["selection_pairs_per_stratum"],
            "selection_pair_evaluations": fits * len(N.STRATA)
                * c["selection_pairs_per_stratum"],
            "alternative_family_search_multiplier": len(N.G_FAMILY) - 1,
            "wall_seconds": time.perf_counter() - started_wall,
            "cpu_seconds": time.process_time() - started_cpu}}
    result["artifact_hash"] = N.canonical_hash(result)
    validate_prepared(result, config, index)
    return result


def validate_prepared(prepared: dict[str, Any], config: dict[str, Any], index: int) -> bool:
    """Validate a durable reload without pretending that compilation is training.

    The frozen ordinary-training validator deliberately rejects zero-step
    networks.  This separate validator checks construction, the direct
    initializer, each selected alignment, the complete search budget and hash.
    It does not generate an evaluation or discovery population.
    """
    c = _config(config)
    _index(index)
    seed = c["model_seeds"][index]
    if (prepared.get("schema") != "f14-neural-discovery-v1"
            or prepared.get("discovery_seed") != seed
            or prepared.get("evaluation_generated") is not False
            or prepared.get("config") != c
            or prepared.get("config_hash") != N.canonical_hash(c)):
        raise ValueError("Calibration discovery identity, config or split changed.")
    unhashed = {k: v for k, v in prepared.items() if k != "artifact_hash"}
    if prepared.get("artifact_hash") != N.canonical_hash(unhashed):
        raise ValueError("Calibration discovery artifact hash mismatch.")
    _, expected_net, expected_layout = _compiled_layout(c, seed)
    expected_initial = N.MLP.initialize(c["width"], N._rng(seed, 0))
    if (prepared.get("network") != expected_net.to_dict()
            or prepared.get("untrained_network") != expected_initial.to_dict()):
        raise ValueError("Compiled network or direct untrained initializer changed.")
    diagnostic = prepared.get("diagnostic", {})
    if (diagnostic.get("evidence_type") != EVIDENCE_TYPE
            or diagnostic.get("development_only") is not True
            or diagnostic.get("layout_index") != index
            or diagnostic.get("learned_structure_evidence") is not False
            or diagnostic.get("ordinary_training_steps") != 0):
        raise ValueError("Compiled development-only evidence label changed.")
    layout = diagnostic.get("layout", {})
    if any(layout.get(k) != v for k, v in expected_layout.items()):
        raise ValueError("Known layout or its transported oracle subsets changed.")
    discrepancy = layout.get("discovery_function_gauge_max_error", float("nan"))
    if not math.isfinite(discrepancy) or not 0 <= discrepancy <= c["gauge_tolerance"]:
        raise ValueError("Invalid recorded discovery gauge check.")
    training = prepared.get("training", {})
    if any(training.get(k) != 0 for k in (
            "steps", "batch_size", "stochastic_outcome_labels", "expected_cost_training_labels")):
        raise ValueError("Compiled calibration must honestly record zero training.")
    names = {f"{g}/{control}" for g in N.G_FAMILY for control in N.SEARCH_CONTROLS}
    if set(prepared.get("alignments", {})) != names:
        raise ValueError("A required searched hypothesis or control is missing.")
    for name, alignment in prepared["alignments"].items():
        if (f"{alignment['g_id']}/{alignment['control']}" != name
                or [r["role"] for r in alignment["roles"]] != [0, 1]):
            raise ValueError("Alignment identity or role order changed.")
        for role in alignment["roles"]:
            subset = role["subset"]
            if (len(subset) != c["subset_size"] or len(set(subset)) != len(subset)
                    or any(type(i) is not int or not 0 <= i < c["width"] for i in subset)):
                raise ValueError("Selected calibration subset violates frozen capacity.")
            decoder = role["decoder"]
            if (decoder["subset"] != subset or len(decoder["coefficient"]) != len(subset)
                    or not all(math.isfinite(float(x)) for x in
                               [*decoder["coefficient"], decoder["intercept"]])):
                raise ValueError("Calibration decoder is inconsistent or nonfinite.")
            selected = role["selected_index"]
            if (type(selected) is not int or not 0 <= selected < c["candidate_count"]
                    or len(role["candidate_pool"]) != c["candidate_count"]
                    or len(role["candidate_scores"]) != c["candidate_count"]
                    or role["candidate_evaluations"] != c["candidate_count"]
                    or role["decoder_fits"] != c["candidate_count"]
                    or role["candidate_pool"][selected] != subset):
                raise ValueError("Calibration selection or matched search budget changed.")
            if selected != N._choose_candidate(role["candidate_scores"], c["ranking_tie_tolerance"]):
                raise ValueError("Saved selection does not follow the frozen scoring rule.")
            if role["selection_score"] != role["candidate_scores"][selected]:
                raise ValueError("Selected calibration score does not match its candidate.")
        expected_overlap = sorted(set(alignment["roles"][0]["subset"])
                                  & set(alignment["roles"][1]["subset"]))
        if alignment["overlap"] != expected_overlap:
            raise ValueError("Alignment overlap record is inconsistent.")
    expected_alternative = min(N.G_FAMILY[1:], key=lambda g: (
        prepared["alignments"][f"{g}/aligned"]["mean_selection_probability_mse"],
        N.G_FAMILY.index(g)))
    if prepared["selected_alternative"] != expected_alternative:
        raise ValueError("Selected alternative did not follow the frozen discovery rule.")
    expected_fits = len(N.G_FAMILY) * len(N.SEARCH_CONTROLS) * 2 * c["candidate_count"]
    if (prepared["resource"]["candidate_evaluations"] != expected_fits
            or prepared["resource"]["decoder_fits"] != expected_fits):
        raise ValueError("Calibration aggregate search budget changed.")
    return True


def _oracle_accuracy(prepared: dict[str, Any], result: dict[str, Any], c: dict[str, Any]):
    """Report known-subset accuracy on hash-identical evaluation arrays.

    Regeneration here repeats deterministic generator work; it introduces no
    additional independent population and never changes searched alignments.
    It is separately charged and logged.  Oracle subsets are not assessed as
    though they had won the guided search or its matched-control comparisons.
    """
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    seed, n = result["evaluation_seed"], result["pairs_per_stratum"]
    net = N.MLP.from_dict(prepared["network"])
    layout = prepared["diagnostic"]["layout"]
    subsets = layout["known_subsets"]
    bound = layout["uniform_probability_error_bound"]
    rows, hashes, generations = [], [], []
    for role in (0, 1):
        pairs, generation = N.make_pairs(c, seed, n, role, 200 + 10 * role)
        pair_hash = N.array_hash(*N._stack_pairs(pairs))
        if pair_hash != result["evaluation_data_hashes"]["role_pairs"][role]:
            raise ValueError("Oracle did not receive the exact searched-evaluation pairs.")
        hashes.append(pair_hash)
        generations.append(generation)
        for stratum in N.STRATA:
            base, donor = pairs[stratum]
            hb, hd = net.hidden(base), net.hidden(donor)
            actual = N._swap_probabilities(net, hb, hd, subsets[role])
            expected = N.high_prediction(base, donor, role, "identity")
            ordinary = N.sigmoid(hb @ net.v + net.beta)
            metrics = N._basic_error(actual, expected)
            searched = result["alignments"]["identity/aligned"]["roles"][role][stratum]
            rows.append({
                "role": role, "stratum": stratum, "known_subset": subsets[role],
                "metrics": metrics,
                "unchanged_target_output_effect_rms": float(np.sqrt(np.mean(
                    (actual - ordinary) ** 2))) if stratum == "equal_target" else None,
                "uniform_probability_error_bound": bound,
                "uniform_bound_satisfied": metrics["max_absolute_error"] <= bound,
                "searched_identity_mae": searched["mae"],
                "searched_minus_oracle_mae": searched["mae"] - metrics["mae"],
                "searched_subset_matches_known_subset":
                    prepared["alignments"]["identity/aligned"]["roles"][role]["subset"]
                    == subsets[role]})
    return {"development_only": True, "known_subsets_selected_by_construction": True,
            "complete_endpoint_assessed_for_oracle": False,
            "same_searched_evaluation_arrays_hash_verified": True,
            "evaluation_role_pair_hashes": hashes, "rows": rows,
            "all_uniform_bounds_satisfied": all(r["uniform_bound_satisfied"] for r in rows),
            "pair_regeneration": generations,
            "resource": {"wall_seconds": time.perf_counter() - started_wall,
                         "cpu_seconds": time.process_time() - started_cpu,
                         "repeated_pair_examples": 2 * len(N.STRATA) * n,
                         "additional_independent_populations": 0,
                         "alignment_searches": 0, "decoder_fits": 0}}


def evaluate_one(prepared: dict[str, Any], config: dict[str, Any], index: int) -> dict[str, Any]:
    """Run the unchanged evaluator and attach a separately labelled oracle check.

    The caller owns the global durable-preparation gate.  A single-artifact
    function cannot establish that the other four models have been saved.
    """
    c = _config(config)
    _index(index)
    validate_prepared(prepared, config, index)
    result = N.evaluate_neural(prepared, config, c["evaluation_seeds"][index])
    result["diagnostic"] = {
        "evidence_type": EVIDENCE_TYPE, "development_only": True,
        "layout_index": index, "ordinary_training_steps": 0,
        "learned_structure_evidence": False,
        "searched_endpoint_unchanged": True,
        "same_constructed_function_across_layouts": True,
        "independent_ordinary_training_replicates": False}
    result["oracle_known_subset_accuracy"] = _oracle_accuracy(prepared, result, c)
    return result


def assess(results: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    """Apply all 560 frozen interval rows, retaining honest DEVELOPMENT status."""
    c = _config(config)
    if (len(results) != len(c["evaluation_seeds"])
            or [r["evaluation_seed"] for r in results] != c["evaluation_seeds"]):
        raise ValueError("All five calibration layouts must be evaluated in declared order.")
    for index, result in enumerate(results):
        if (result["pairs_per_stratum"] != c["evaluation_pairs_per_stratum"]
                or result["task"]["n"] != c["task_evaluation_samples"]):
            raise ValueError("Calibration must use the complete frozen evaluation counts.")
        diagnostic = result.get("diagnostic", {})
        if (diagnostic.get("evidence_type") != EVIDENCE_TYPE
                or diagnostic.get("development_only") is not True
                or diagnostic.get("layout_index") != index
                or diagnostic.get("ordinary_training_steps") != 0
                or diagnostic.get("learned_structure_evidence") is not False):
            raise ValueError("Calibration result lost its constructed development provenance.")
    assessment = A.neural_assessment(results, config, development=True)
    supported = assessment["supported_prespecified_replicates"]
    assessment["diagnostic"] = {
        "evidence_type": EVIDENCE_TYPE,
        "calibration_complete_endpoint_layouts": supported,
        "calibration_complete_endpoint_threshold": config["analysis"]["minimum_supported_model_replicates"],
        "calibration_complete_endpoint_met":
            supported >= config["analysis"]["minimum_supported_model_replicates"]
            and all(m["numerical_controls_valid"] for m in assessment["models"]),
        "complete_endpoint_uses_searched_alignments_and_all_frozen_controls": True,
        "oracle_accuracy_is_separate_from_complete_endpoint": True,
        "same_constructed_function_across_layouts": True,
        "independent_ordinary_training_replicates": False,
        "learned_structure_evidence": False,
        "changes_original_F15_result": False}
    return assessment
