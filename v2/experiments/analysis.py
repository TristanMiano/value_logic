"""Prospective F14 result rules. These do not select alignments or tune models.

Intervals use Hoeffding's bounded independent-sample inequality, conditional
on the already frozen model/alignment. Shared pairs across different metrics
are allowed; the finite family is covered by a union bound.
Contributor: ChatGPT (GPT-6 Astra Pro), F14.
"""
from __future__ import annotations

import math
from collections import Counter
from fractions import Fraction as Q
from itertools import permutations

from . import neural as N


def defaults():
    return {
        "familywise_alpha": 0.05,
        "maximum_interval_rows": 560,
        "interval": "two_sided_hoeffding_union_bound",
        "intervention_mae_max": 0.05,
        "base_probability_mae_max": 0.05,
        "conditional_base_probability_mae_max": 0.05,
        "adjusted_effect_mae_max": 0.10,
        "base_decision_regret_max": 0.05,
        "far_decision_disagreement_max": 0.10,
        "near_decision_disagreement_max": 0.35,
        "matched_control_advantage_min": 0.01,
        "same_subset_scale_advantage_min": 0.01,
        "scale_separating_frequency_min": 0.90,
        "minimum_supported_model_replicates": 4,
        "composition_primary": False,
        "worldwide_novelty_assessed": False,
        "retention_useful_min_distinct_cases": 4,
        "retention_useful_min_distinct_seeds": 2,
        "retention_useful_requires_price_and_program_edit": True,
        "retention_useful_requires_uncertain_selective_case": True,
        "retention_useful_requires_approximate_selected_cost": True,
    }


def bounded_interval(mean, n, *, lower=0.0, upper=1.0, alpha=0.05, family=560):
    """Simultaneous two-sided interval for a bounded-sample mean."""
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("An observed positive integer sample count is required.")
    if not all(math.isfinite(float(x)) for x in (mean, lower, upper, alpha)):
        raise ValueError("Nonfinite statistics cannot receive a confidence bound.")
    if not lower < upper or not 0 < alpha < 1 or type(family) is not int or family <= 0:
        raise ValueError("Invalid bounds or finite claim family.")
    if not lower-1e-12 <= mean <= upper+1e-12:
        raise ValueError("Observed mean lies outside its declared range.")
    radius = (upper-lower)*math.sqrt(math.log(2*family/alpha)/(2*n))
    return {"mean": float(mean), "n": n, "sample_range": [lower, upper],
            "radius": radius, "lower": max(lower, float(mean)-radius),
            "upper": min(upper, float(mean)+radius)}


def _comparison(row):
    n = row["n"]
    if type(n) is not int or n <= 0:
        raise ValueError("A comparison requires a positive integer pair count.")
    mean, total = row["mean_paired_absolute_error_improvement"], row["sum"]
    values = [mean, total, row["sum_squares"], row["minimum"], row["maximum"]]
    if not all(math.isfinite(float(v)) for v in values):
        raise ValueError("Nonfinite paired comparison.")
    if not (-1-1e-12 <= row["minimum"] <= mean+1e-12
            and mean <= row["maximum"]+1e-12 <= 1+2e-12):
        raise ValueError("Paired error improvement lies outside [-1,1].")
    if not math.isclose(total/n, mean, rel_tol=1e-10, abs_tol=1e-12):
        raise ValueError("Paired comparison mean disagrees with its sum/count.")
    if not -1e-10 <= row["sum_squares"] <= n+1e-10:
        raise ValueError("Invalid bounded-comparison sum of squares.")
    if row["sum_squares"]+1e-10 < total*total/n:
        raise ValueError("Comparison moments violate the variance inequality.")
    return mean, n


def _pooled(comparisons):
    for row in comparisons:
        _comparison(row)
    counts = [row["n"] for row in comparisons]
    if not counts or len(set(counts)) != 1:
        raise ValueError("The prospective mixture requires equally sized strata.")
    n = sum(counts)
    return sum(row["sum"] for row in comparisons)/n, n


def _numerical_controls(result, nc):
    """Numerical controls fail closed; a copied boolean is not evidence."""
    tolerance = nc["gauge_tolerance"]
    expected_errors = {"observational_probability", "intervention_probability", "decoder_value"}
    gauges = result.get("gauges_by_g", {})
    if set(gauges) != set(N.G_FAMILY):
        return False
    for gauge in gauges.values():
        errors = gauge.get("errors", {})
        if (set(errors) != expected_errors or gauge.get("refits") != 0
                or gauge.get("tolerance") != tolerance or gauge.get("passed") is not True):
            return False
        if any(not math.isfinite(float(e)) or not 0 <= e <= tolerance for e in errors.values()):
            return False
        if sorted(gauge.get("permutation", [])) != list(range(nc["width"])):
            return False
        scales = gauge.get("scales", [])
        if len(scales) != nc["width"] or any(not math.isfinite(float(s)) or
                not nc["gauge_scale_min"] <= s <= nc["gauge_scale_max"] for s in scales):
            return False
    for name in ("global_scale_prediction_error", "global_scale_decoder_error"):
        value = result.get(name, float("nan"))
        if not math.isfinite(float(value)) or not 0 <= value <= tolerance:
            return False
    witness = result.get("unused_duplicate_witness", {})
    values = [witness.get(k, float("nan")) for k in
              ("decoder_max_error", "unused_logit_effect_max", "used_logit_effect_max")]
    return (all(math.isfinite(float(x)) for x in values)
            and 0 <= values[0] <= tolerance and 0 <= values[1] <= tolerance
            and values[2] > tolerance
            and witness.get("decoding_passes_and_unused_causal_use_fails") is True
            and result.get("resource", {}).get("alignment_refits") == 0)


def neural_assessment(results, config, *, development=False):
    """Apply frozen criteria, retaining every planned model and control.

    Development records exercise reporting only; their classifications are
    not prospective empirical evidence, regardless of the numerical label.
    """
    c = config["analysis"]
    nc = config["neural"]
    expected_seeds = nc["evaluation_seeds"]
    if not development:
        if len(results) != len(expected_seeds):
            raise ValueError("Missing model evaluation; report an incomplete run.")
        if [r["evaluation_seed"] for r in results] != expected_seeds:
            raise ValueError("Evaluation seeds/order differ from the frozen protocol.")
    if not results:
        raise ValueError("No evaluation records supplied.")
    rows, models = [], []
    alpha, family = c["familywise_alpha"], c["maximum_interval_rows"]

    def add(key, mean, n, lo=0.0, hi=1.0):
        if len(rows) >= family:
            raise ValueError("The frozen simultaneous-claim family was exceeded.")
        row = dict(bounded_interval(mean, n, lower=lo, upper=hi,
                                    alpha=alpha, family=family), id=key)
        rows.append(row)
        return row

    for mi, result in enumerate(results):
        prefix = f"model{mi}"
        n = result["pairs_per_stratum"]
        if not development and n != nc["evaluation_pairs_per_stratum"]:
            raise ValueError("Pair count differs from the frozen evaluation count.")
        task = result["task"]
        if not development and task["n"] != nc["task_evaluation_samples"]:
            raise ValueError("Task evaluation count differs from its freeze.")
        bmae = add(f"{prefix}/base_mae", task["mae"], task["n"])
        regret_bound = task["decision_regret_bound"]
        if regret_bound != 1.375:
            raise ValueError("Unregistered task-regret normalization.")
        if not math.isclose(task["mean_normalized_decision_regret"]*regret_bound,
                            task["mean_decision_regret"], rel_tol=1e-10, abs_tol=1e-12):
            raise ValueError("Task regret and its normalization disagree.")
        bregret = add(f"{prefix}/base_normalized_regret",
                      task["mean_normalized_decision_regret"], task["n"])
        task_ready = (bmae["upper"] <= c["base_probability_mae_max"]
                      and bregret["upper"]*regret_bound <= c["base_decision_regret_max"])
        numerical_ok = _numerical_controls(result, nc)
        conditional_base = []
        for role in (0, 1):
            cells = {}
            for stratum in N.STRATA:
                metric = result["alignments"]["identity/aligned"]["roles"][role][stratum]["base_prediction"]
                if metric["n"] != n:
                    raise ValueError("Conditional baseline must use every matched pair.")
                cells[stratum] = add(f"{prefix}/conditional_base/{role}/{stratum}/mae", metric["mae"], n)
            conditional_base.append(cells)
        hypotheses = {}
        for g in N.G_FAMILY:
            aligned = result["alignments"][f"{g}/aligned"]
            role_outcomes = []
            for role in (0, 1):
                absolute, decisions, control_advantages = {}, {}, {}
                for stratum in N.STRATA:
                    metric = aligned["roles"][role][stratum]
                    if metric["n"] != n:
                        raise ValueError("Unequal or missing stratum sample count.")
                    absolute[stratum] = add(f"{prefix}/{g}/{role}/{stratum}/mae",
                                              metric["mae"], n)
                for stratum in ("mixed_near", "mixed_far"):
                    metric = aligned["roles"][role][stratum]
                    decisions[stratum] = add(f"{prefix}/{g}/{role}/{stratum}/disagreement",
                                               1-metric["decision_agreement"], n)
                for control in N.SEARCH_CONTROLS[1:]:
                    cells = result["matched_control_comparisons_by_g"][g][control]
                    selected = [cells[f"{role}/{s}"] for s in N.STRATA]
                    if any(x["n"] != n for x in selected):
                        raise ValueError("Control does not use the matched pair count.")
                    mean, pooled_n = _pooled(selected)
                    control_advantages[control] = add(f"{prefix}/{g}/{role}/{control}/advantage",
                                                        mean, pooled_n, -1.0, 1.0)
                effect_bounds = {s: min(2.0, absolute[s]["upper"]+conditional_base[role][s]["upper"])
                                 for s in N.STRATA}
                adequate = (all(x["upper"] <= c["intervention_mae_max"] for x in absolute.values())
                            and all(x["upper"] <= c["conditional_base_probability_mae_max"]
                                    for x in conditional_base[role].values())
                            and all(x <= c["adjusted_effect_mae_max"] for x in effect_bounds.values())
                            and decisions["mixed_far"]["upper"] <= c["far_decision_disagreement_max"]
                            and decisions["mixed_near"]["upper"] <= c["near_decision_disagreement_max"])
                selective = all(x["lower"] >= c["matched_control_advantage_min"]
                                for x in control_advantages.values())
                violated = any(x["lower"] > c["intervention_mae_max"] for x in absolute.values())
                role_outcomes.append({"absolute_and_decision_criteria": adequate,
                    "matched_control_specificity": selective,
                    "mae_tolerance_falsified_in_a_stratum": violated,
                    "absolute": absolute, "decisions": decisions,
                    "conditional_base": conditional_base[role],
                    "derived_adjusted_effect_mae_upper": effect_bounds,
                    "control_advantages": control_advantages})
            hypotheses[g] = {"roles": role_outcomes,
                "adequate": all(r["absolute_and_decision_criteria"] for r in role_outcomes),
                "selective": all(r["matched_control_specificity"] for r in role_outcomes)}
        scales = {}
        for g in N.G_FAMILY[1:]:
            scales[g] = []
            for role in (0, 1):
                metric = result["alternative_comparisons"][g][f"{role}/scale_separating"]
                if (metric["total_pairs"] != n or metric["separating_pairs"] != n
                        or not math.isclose(metric["separating_fraction"], 1.0, abs_tol=1e-12)):
                    raise ValueError("Every frozen scale-separating pair must be retained.")
                frequency = add(f"{prefix}/{g}/{role}/separating_frequency",
                                metric["separating_fraction"], metric["total_pairs"])
                comparison = metric["same_identity_subset_comparison"]
                if comparison is None or comparison["n"] != n or n < nc["g_min_separating_pairs"]:
                    # A missing cell may not be replaced by a favorable interval.
                    raise ValueError("Insufficient predeclared scale-separating pairs.")
                _comparison(comparison)
                advantage = add(f"{prefix}/{g}/{role}/same_identity_subset_advantage",
                                comparison["mean_paired_absolute_error_improvement"],
                                comparison["n"], -1.0, 1.0)
                scales[g].append({"frequency": frequency, "advantage": advantage,
                    "distinguished": frequency["lower"] >= c["scale_separating_frequency_min"]
                        and advantage["lower"] >= c["same_subset_scale_advantage_min"]})
        scale_specific = all(r["distinguished"] for group in scales.values() for r in group)
        identity = hypotheses["identity"]
        if not numerical_ok:
            disposition = "numerical_or_protocol_failure"
        elif not task_ready:
            disposition = "task_underlearned_at_frozen_criterion"
        elif identity["adequate"] and identity["selective"] and scale_specific:
            disposition = "expected_cost_interchange_supported_at_declared_scope"
        elif identity["adequate"]:
            disposition = "interchange_adequate_but_not_discriminated_from_controls_or_scales"
        elif any(hypotheses[g]["adequate"] and hypotheses[g]["selective"] for g in N.G_FAMILY[1:]):
            disposition = "competing_cost_scale_supported_original_not_supported"
        else:
            disposition = "specified_subset_hypothesis_not_supported_at_frozen_thresholds"
        models.append({"evaluation_seed": result["evaluation_seed"], "disposition": disposition,
            "task_ready": task_ready, "numerical_controls_valid": numerical_ok,
            "base_probability_interval": bmae, "base_normalized_regret_interval": bregret,
            "hypotheses": hypotheses, "same_subset_scale_tests": scales,
            "unique_absolute_cost_representation_claim": False,
            "joint_constructive_abstraction_claim": False,
            "composition": result["composition"]})
    supported = sum(m["disposition"] == "expected_cost_interchange_supported_at_declared_scope"
                    for m in models)
    if len(rows) != 112*len(results):
        raise ValueError("The implementation's interval family differs from the frozen table.")
    return {"schema": "f14-neural-assessment-v1", "development_only": development,
            "interval_family_cap": family, "actual_interval_rows": len(rows),
            "familywise_alpha": alpha, "models": models,
            "supported_prespecified_replicates": supported,
            "pilot_support_criterion_met": not development
                and supported >= c["minimum_supported_model_replicates"]
                and all(m["numerical_controls_valid"] for m in models),
            "scope": "conditional on these frozen models and the stipulated independent pair generators",
            "generalization_to_other_training_seeds_claim": False,
            "worldwide_novelty_assessed": False}


def retention_assessment(results, config, *, development=False):
    """Exact finite-case accounting, without a population or speed claim.

    Correctness is necessary. The separate application criterion asks for
    useful, nonconstant native derivations and a selective uncertain case.
    Meeting it does not independently establish novelty or unique capability.
    """
    from . import retention as R
    rc, ac = config["retention"], config["analysis"]
    seeds = rc["development_seeds"] if development else rc["evaluation_seeds"]
    expected = [(s, v) for s in seeds for v in rc["variants"]]
    if [(r["seed"], r["variant"]) for r in results] != expected:
        raise ValueError("Every frozen retention case is required in its declared order.")
    tau, epsilon = Q(rc["numeric_tolerance"]), Q(rc["decision_regret_tolerance"])

    def quality_vector(item):
        """Task quality, including refusals; literal equality is not admission."""
        nr, scoring = item["native"], item["scoring"]
        counts = Counter(a["status"] for a in item["numeric"])
        return {
            "numeric": [{"order": list(a["order"]), "status": a["status"],
                "interval": [str(Q(a["lower"])), str(Q(a["upper"]))],
                "estimate": None if a["estimate"] is None else str(Q(a["estimate"])),
                "absolute_error": None if e is None else str(Q(e))}
                for a, e in zip(item["numeric"], scoring["numeric_errors"])],
            "numeric_coverage": {s: counts[s] for s in ("exact", "approximate", "refused")},
            "all_numeric_queries_admitted": counts["refused"] == 0,
            "decision": {"status": item["decision_status"],
                "certified": not item["refused"],
                "selected_index": item["selected_index"], "executed_index": item["executed_index"],
                "coherent_worst_regret": str(Q(item["coherent_worst_regret"])),
                "realized_regret": str(Q(scoring["realized_regret"])),
                "actual_executed_cost": str(Q(scoring["actual_executed_cost"])),
                "oracle_best_cost": str(Q(scoring["full_information_oracle_best_cost"]))},
            "native": {"status": nr["status"], "certificate_role": nr["certificate_role"],
                "candidate_order": list(nr["candidate_order"]),
                "retained_fiber_valid": nr["semantic_valid"],
                "upper_bound": str(Q(nr["upper_bound"])),
                "full_source_value": str(Q(scoring["full_source_semantic_value"])),
                "full_source_valid": scoring["full_source_semantic_valid"]}}

    def acquisition_vector(item):
        r = item["resources"]
        return {"pre_repair": dict(item["pre_repair"]),
            "calls": r["acquisition_calls"],
            "scalar_measurements": r["acquisition_scalar_measurements"],
            "kinds": list(r["acquisition_kinds"]),
            "path_world_executions": r["acquisition_path_world_executions"],
            "transferred_bytes": r["acquisition_transferred_bytes"]}

    # Information equivalence constrains arithmetic, the fixed deterministic
    # decision/acquisition policy, and native semantic targets. Proof budgets,
    # representations and caching can affect availability without changing that
    # information; native receipt equality is therefore reported separately.
    equivalent_groups = (("fresh", "cached_proof", "full_joint"),
                         ("tailored", "exact_intervals"))
    numeric, decisions, native, cache = Counter(), Counter(), Counter(), Counter()
    useful_cases, useful_seeds, useful_variants = set(), set(), set()
    uncertain_selective, approximate_uncertain_selective, approximate_useful, losses = [], [], [], []
    paired_rows, equivalence_rows, strata = [], [], {}
    for case in results:
        expected_methods = [(a, m) for a in rc["access_regimes"] for m in rc["methods"]]
        if [(r["access"], r["method"]) for r in case["methods"]] != expected_methods:
            raise ValueError("Missing, reordered or duplicated ordinary control.")
        scount = strata.setdefault(case["variant"], Counter())
        for item in case["methods"]:
            row_key = {"seed": case["seed"], "variant": case["variant"],
                       "method": item["method"], "access": item["access"]}
            if len(item["numeric"]) != 6 or len(item["scoring"]["numeric_errors"]) != 6:
                raise ValueError("Every requested order must retain a numerical disposition.")
            orders = list(permutations(range(3), 2 if case["variant"] == "program_edit" else 3))
            if [tuple(a["order"]) for a in item["numeric"]] != orders:
                raise ValueError("Numeric order identities differ from the declared query family.")
            options = orders+[None]
            for key in ("selected", "executed"):
                index = item[f"{key}_index"]
                value = None if item[key] is None else tuple(item[key])
                if type(index) is not int or not 0 <= index < len(options) or value != options[index]:
                    raise ValueError("Decision index and its declared program disagree.")
            if not item["refused"] and item["selected_index"] != item["executed_index"]:
                raise ValueError("A certified decision must execute its selected program.")
            for answer, error in zip(item["numeric"], item["scoring"]["numeric_errors"]):
                lo, hi = Q(answer["lower"]), Q(answer["upper"])
                expected_status = "exact" if lo == hi else "approximate" if hi-lo <= 2*tau else "refused"
                if lo > hi or answer["status"] != expected_status:
                    raise ValueError("Incorrect exact/approximate/refusal disposition.")
                if expected_status == "refused":
                    if answer["estimate"] is not None or error is not None:
                        raise ValueError("A refused numeric query cannot supply an admitted estimate.")
                elif (answer["estimate"] is None or Q(answer["estimate"]) != (lo+hi)/2
                      or error is None or not 0 <= Q(error) <= tau
                      or (expected_status == "exact" and Q(error) != 0)):
                    raise ValueError("False numerical admission or inconsistent midpoint.")
                numeric[expected_status] += 1
                scount[f"numeric_{expected_status}"] += 1
            regret = Q(item["scoring"]["realized_regret"])
            if regret != Q(item["scoring"]["actual_executed_cost"])-Q(item["scoring"]["full_information_oracle_best_cost"]):
                raise ValueError("Realized regret disagrees with actual and oracle losses.")
            if regret < 0 or item["useful_decision"] != (not item["refused"]):
                raise ValueError("Invalid regret or refusal accounting.")
            expected_decision = ("refusal_to_fallback" if item["refused"] else
                                 "certified_fallback" if item["executed"] is None else "certified_order")
            if item["decision_status"] != expected_decision:
                raise ValueError("Certified fallback and refusal must be distinguished.")
            if (item["useful_decision"] and regret > epsilon) or (item["refused"] and item["executed"] is not None):
                raise ValueError("False useful-decision guarantee or omitted fallback.")
            if (Q(item["coherent_worst_regret"]) > epsilon) != item["refused"]:
                raise ValueError("Decision disposition contradicts its coherent bound.")
            if Q(item["coherent_worst_regret"]) < 0 or (not item["refused"] and regret > Q(item["coherent_worst_regret"])):
                raise ValueError("Coherent regret bound cannot be negative or miss certified realized regret.")
            decisions[item["decision_status"]] += 1
            scount[item["decision_status"]] += 1
            nr = item["native"]
            bound = Q(nr["upper_bound"])
            full_value = Q(item["scoring"]["full_source_semantic_value"])
            if (item["scoring"]["full_source_semantic_valid"] != (full_value <= 0)
                    or full_value > bound):
                raise ValueError("Full-source semantic truth contradicts its value or retained bound.")
            if nr["semantic_valid"] != (bound <= 0):
                raise ValueError("Native semantic flag contradicts its fiber bound.")
            if nr["status"] == "received" and (bound > 0 or not item["scoring"]["full_source_semantic_valid"]):
                raise ValueError("A received current proof cannot contradict the actual source.")
            if nr["status"] not in ("received", "insufficient_current_request", "unavailable_budget"):
                raise ValueError("Unknown native disposition.")
            native[nr["status"]] += 1
            cache[nr["cache"]] += 1
            if item["scoring"]["full_source_semantic_valid"] and not nr["semantic_valid"]:
                scount["full_law_valid_but_retained_fiber_not_valid"] += 1
            useful = (case["variant"] in ("small_price", "small_negative_price", "large_price",
                       "large_negative_price", "program_edit") and item["decision_status"] == "certified_order"
                       and nr["certificate_role"] == "selected_order"
                       and nr["candidate_order"] == item["executed"] and nr["status"] == "received"
                       and bound <= -tau and nr["source_premises_used"] >= 2)
            if nr["useful_derivation_candidate"] != useful:
                raise ValueError("The useful derivation must certify the executed revised order.")
            if useful:
                useful_cases.add((case["seed"], case["variant"]))
                useful_seeds.add(case["seed"])
                useful_variants.add(case["variant"])
                if (item["method"] in ("tailored", "exact_intervals")
                        and item["access"] == "no_reacquisition"
                        and item["resources"]["fiber_vertex_count"] > 1):
                    uncertain_selective.append(row_key)
                    if item["numeric"][item["executed_index"]]["status"] == "approximate":
                        approximate_uncertain_selective.append(row_key)
            if (item["decision_status"] == "certified_order" and
                    item["numeric"][item["executed_index"]]["status"] == "approximate"):
                approximate_useful.append(row_key)
            if regret > epsilon:
                losses.append(dict(row_key, regret=str(regret), decision_status=item["decision_status"]))
        for access in rc["access_regimes"]:
            cells = [x for x in case["methods"] if x["access"] == access]
            fresh = next(x for x in cells if x["method"] == "fresh")
            qualities = {item["method"]: quality_vector(item) for item in cells}
            acquisitions = {item["method"]: acquisition_vector(item) for item in cells}
            for group in equivalent_groups:
                reference = group[0]
                for method in group[1:]:
                    left, right = qualities[reference], qualities[method]
                    ordinary_equal = all(left[k] == right[k] for k in
                                         ("numeric", "numeric_coverage", "decision"))
                    semantic_equal = all(left["native"][k] == right["native"][k]
                        for k in left["native"] if k != "status")
                    acquisition_equal = acquisitions[reference] == acquisitions[method]
                    if not (ordinary_equal and semantic_equal and acquisition_equal):
                        raise ValueError(f"Equal-information controls disagree: {reference}/{method}, "
                            f"seed {case['seed']}, {case['variant']}, {access}.")
                    equivalence_rows.append({"seed": case["seed"], "variant": case["variant"],
                        "access": access, "reference": reference, "method": method,
                        "ordinary_quality_and_acquisition_equal": True,
                        "native_semantic_target_equal": True,
                        "native_receipt_status_equal": left["native"]["status"] == right["native"]["status"]})
            for item in cells:
                r, f = item["resources"], fresh["resources"]
                quality, fresh_quality = qualities[item["method"]], qualities["fresh"]
                both_admit = all(q["all_numeric_queries_admitted"] and q["decision"]["certified"]
                                 for q in (quality, fresh_quality))
                both_prove_selected = all(q["native"]["status"] == "received"
                    and q["native"]["certificate_role"] == "selected_order"
                    for q in (quality, fresh_quality))
                paired_rows.append({"seed": case["seed"], "variant": case["variant"],
                    "access": access, "method": item["method"],
                    "resident_plus_archive_bytes_difference_from_fresh": r["resident_plus_archive_bytes"]-f["resident_plus_archive_bytes"],
                    "arithmetic_ns_difference_from_fresh": r["one_update_arithmetic_ns"]-f["one_update_arithmetic_ns"],
                    "native_inclusive_ns_difference_from_fresh": r["one_update_total_ns"]-f["one_update_total_ns"],
                    "regret_difference_from_fresh": str(Q(item["scoring"]["realized_regret"])-Q(fresh["scoring"]["realized_regret"])),
                    "method_quality": quality, "fresh_quality": fresh_quality,
                    "quality_vector_equal_to_fresh": quality == fresh_quality,
                    "both_admit_all_numeric_queries_and_certify_decision": both_admit,
                    "both_receive_selected_order_proof": both_prove_selected,
                    "both_admit_numeric_decision_and_selected_order_proof": both_admit and both_prove_selected,
                    "method_acquisition": acquisitions[item["method"]],
                    "fresh_acquisition": acquisitions["fresh"],
                    "fixed_information_contract": "each declared payload and common access capability; different payloads contain different information"})
    has_price = any("price" in v for v in useful_variants)
    application = (len(useful_cases) >= ac["retention_useful_min_distinct_cases"]
        and len(useful_seeds) >= ac["retention_useful_min_distinct_seeds"]
        and has_price and "program_edit" in useful_variants and bool(uncertain_selective)
        and bool(approximate_uncertain_selective))
    return {"schema": "f14-retention-assessment-v2", "development_only": development,
        "case_count": len(results), "method_rows": len(paired_rows), "numeric_dispositions": dict(numeric),
        "decision_dispositions": dict(decisions), "native_dispositions": dict(native),
        "cache_dispositions": dict(cache), "strata": {s: dict(c) for s, c in strata.items()},
        "validated_admissions_on_recorded_cases": True,
        "useful_distinct_cases": len(useful_cases), "useful_distinct_seeds": len(useful_seeds),
        "useful_revision_variants": sorted(useful_variants),
        "uncertain_selective_useful_cases": uncertain_selective,
        "uncertain_approximate_selective_useful_cases": approximate_uncertain_selective,
        "approximate_numeric_with_certified_order": approximate_useful,
        "loss_above_tolerance_including_refusal": losses,
        "bounded_application_criterion_met": application and not development,
        "paired_resource_and_decision_comparisons": paired_rows,
        "equal_information_control_comparisons": equivalence_rows,
        "quality_comparison_semantics": {
            "literal_quality_equality_can_include_equal_refusals": True,
            "admitted_services_require": "all six numerical queries admitted, certified ordinary decision, current selected-order proof",
            "certified_fallback_is_an_admitted_decision": True,
            "diagnostic_option_proof_is_not_a_selected_fallback_proof": True,
            "equal_information_groups": [list(g) for g in equivalent_groups],
            "equivalence_requires": "exact intervals/dispositions/errors, deterministic decisions and coherent/actual regret, native semantic target, fixed acquisition policy outputs",
            "native_receipt_equality_is_reported_not_assumed": True,
            "proof_size_cache_behavior_and_compute_may_differ": True},
        "speed_superiority_required": False, "novelty_criterion_independently_established": False,
        "population_generalization_claim": False,
        "scope": "all named methods on this finite generated population, with exact supplied source facts"}
