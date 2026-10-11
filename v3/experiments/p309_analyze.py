"""Exact prospective finite-cohort analysis; no policies or generators imported.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
This is a descriptive fixed-catalogue evaluator, not a deployed policy selector.
"""
from __future__ import annotations

from fractions import Fraction as F
import json

import p309_lifecycle as L


def fraction(value):
    return F(*value) if isinstance(value, (list, tuple)) else F(value)


def pair(value):
    if value is None:
        return None
    value = fraction(value)
    return [value.numerator, value.denominator]


def mean(values):
    if not values or any(value is None for value in values):
        return None
    return sum((fraction(value) for value in values), F(0)) / len(values)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def rows_from_seals(schedule, completed):
    expected = {unit["id"]: unit for unit in schedule["units"]}
    if len(expected) != len(schedule["units"]):
        raise L.IntegrityError("Analysis schedule contains duplicate public units.")
    rows = {}
    for row in completed:
        score_unit = row["unit"]
        public_id = score_unit["public_unit_id"]
        if public_id not in expected or public_id in rows:
            raise L.IntegrityError("Unknown or duplicated scored unit.")
        if score_unit != dict(expected[public_id], id="score-" + public_id, public_unit_id=public_id):
            raise L.IntegrityError("Scoring unit changed the frozen public configuration.")
        score = row["result"]["value"]["score"]
        if not isinstance(score, dict):
            raise L.IntegrityError("Scoring result is not a structured record.")
        rows[public_id] = {"unit": expected[public_id], "score": score}
    if set(rows) != set(expected):
        raise L.IntegrityError("Analysis requires every scheduled private-score seal.")
    return [rows[unit["id"]] for unit in schedule["units"]]


def hierarchical_mean(rows, value):
    """Equal public-population weight, then equal fixed seed-slot weight.

    A deterministic comparator contributes its single exact value per public
    population, with no invented independent replicas.
    """
    grouped = {}
    for row in rows:
        grouped.setdefault(row["unit"]["group_id"], []).append(value(row))
    return mean([mean(values) for values in grouped.values()])


def common_stakes_action_loss(score, stakes):
    if score.get("full_horizon") is not True or score.get("validity_pass") is not True:
        return None
    fp, fn = fraction(stakes["fp"]), fraction(stakes["fn"])
    horizon = score["horizon"]
    if horizon <= 0 or max(fp, fn) <= 0:
        raise L.IntegrityError("Common action comparison has invalid units.")
    return (fp * score["false_positives"] + fn * score["false_negatives"]) / (horizon * max(fp, fn))


def broker_slice_summaries(config, bucket):
    """Prespecified slices retain every parent episode and its denominator."""
    names = {"first_occurrence"}
    for row in bucket:
        names.update(segment["name"] for segment in row["unit"].get("segments", []))
    summaries = []
    for name in sorted(names):
        selected = []
        for row in bucket:
            unit, score = row["unit"], row["score"]
            if name == "first_occurrence":
                values = score.get("first_occurrence")
                expected = values.get("horizon") if values else None
            else:
                segments = [segment for segment in unit.get("segments", []) if segment["name"] == name]
                if len(segments) != 1:
                    raise L.IntegrityError("One fixed slice is not scheduled for every configuration episode.")
                expected = segments[0]["stop"] - segments[0]["start"]
                values = score.get("segments", {}).get(name)
            parent_complete = score.get("full_horizon") is True and score.get("validity_pass") is True
            usable = bool(parent_complete and values and values.get("full_horizon") is True)
            if values and values.get("horizon") != expected:
                raise L.IntegrityError("A scored slice changed its scheduled denominator.")
            selected.append({"unit": unit, "values": values or {}, "usable": usable,
                "denominator": {"unit_id": unit["id"], "scheduled_positions": expected,
                    "closed_positions": values.get("rounds_closed") if values else None,
                    "parent_complete_and_valid": parent_complete, "usable_full_slice": usable}})
        complete = all(row["usable"] for row in selected)
        def metric(field):
            return hierarchical_mean(selected, lambda row: row["values"].get(field) if row["usable"] else None)
        fields = {field: pair(metric(field)) for field in (
            "brier_mean", "base_brier_mean", "uniform_brier_mean", "action_loss_mean")}
        readouts = {}
        for field in ("constant_half_brier_mean", "equal_mixture_brier_mean", "dyadic_equal_mixture_brier_mean",
                      "same_hard_mask_half_brier_mean", "same_hard_mask_equal_mixture_brier_mean"):
            readouts[field] = pair(hierarchical_mean(selected, lambda row:
                (row["values"].get("forecast_readouts") or {}).get(field) if row["usable"] else None))
        readouts["expert_brier_means"] = [pair(hierarchical_mean(selected, lambda row:
            (row["values"].get("forecast_readouts") or {}).get("expert_brier_means", [None] * 6)[index]
            if row["usable"] else None)) for index in range(6)]
        delta = (fraction(fields["uniform_brier_mean"]) - fraction(fields["base_brier_mean"])) \
            if fields["uniform_brier_mean"] is not None and fields["base_brier_mean"] is not None else None
        denominators = [row["denominator"] for row in selected]
        summaries.append({"slice": name, "planned_episodes": len(selected),
            "complete_primary_denominator": complete, "per_episode_denominators": denominators,
            "known_scheduled_positions": sum(row["scheduled_positions"] for row in denominators
                if type(row["scheduled_positions"]) is int),
            "unknown_scheduled_denominator_episodes": sum(row["scheduled_positions"] is None for row in denominators),
            "means": fields, "forecast_readout_means": readouts,
            "uniform_minus_base_brier": pair(delta),
            "practical_learning_effect": bool(complete and delta is not None
                and delta >= fraction(config["analysis"]["loss_improvement_threshold"])),
            "weighting": "equal scheduled seed slots within population, then equal populations; no pooled-position reweighting",
            "scope": "A complete slice of an incomplete or invalid parent cannot establish a primary positive effect; recorded-hard-mask readouts are descriptive."})
    return summaries


def broker_report_summary(config, bucket):
    """A5 compares all scheduled reports with their own deterministic bounds."""
    requested = [row for row in bucket if row["unit"].get("engine") in ("broker", "mirror")]
    if not requested:
        return {"requested": False, "planned_reports": 0, "endpoints": {}}
    reports = []
    for row in requested:
        score = row["score"]
        report = score.get("paid_report_comparison") or {"status": "missing", "endpoints": {}}
        reports.append({"unit": row["unit"], "report": report,
            "parent_valid_and_complete": score.get("validity_pass") is True and score.get("full_horizon") is True,
            "optional_units": score.get("optional_reporting_units")})
    endpoints = {}
    for name in ("V", "F", "Z"):
        def endpoint(row):
            return row["report"].get("endpoints", {}).get(name, {})
        def usable(row):
            return (row["parent_valid_and_complete"] and row["report"].get("status") == "success"
                    and endpoint(row).get("status") == "success")
        complete = all(usable(row) for row in reports)
        fields = {field: pair(hierarchical_mean(reports, lambda row:
            endpoint(row).get(field) if usable(row) else None)) for field in (
                "deterministic_width_per_horizon", "width_per_horizon", "normalized_width_reduction",
                "normalized_lower_endpoint_gain", "normalized_upper_endpoint_gain")}
        reduction = fields["normalized_width_reduction"]
        endpoints[name] = {"complete_report_denominator": complete, "means": fields,
            "usable_reports": sum(usable(row) for row in reports),
            "unavailable_unit_ids": [row["unit"]["id"] for row in reports if not usable(row)],
            "practical_width_reduction": bool(complete and reduction is not None
                and fraction(reduction) >= fraction(config["analysis"]["report_width_improvement_threshold"]))}
    known = [row["optional_units"] for row in reports if type(row["optional_units"]) is int]
    return {"requested": True, "planned_reports": len(reports),
        "status_by_unit": [{"unit_id": row["unit"]["id"], "status": row["report"].get("status"),
            "parent_valid_and_complete": row["parent_valid_and_complete"]} for row in reports],
        "mean_additional_units": pair(hierarchical_mean(reports, lambda row: row["optional_units"])),
        "known_total_additional_units": sum(known), "unknown_fee_reports": len(reports) - len(known),
        "endpoints": endpoints, "empirical_coverage_claim": False,
        "scope": "Whole scheduled configuration; no successful-report-only denominator; negative gains retained, conflicts unusable."}


def broker_analysis(config, group_map, rows):
    buckets = {}
    for row in rows:
        unit = row["unit"]
        group = group_map[unit["group_id"]]
        family = group["recipe"]["family"]
        key = (family, encoded(unit.get("stakes", {})), unit["configuration_id"])
        buckets.setdefault(key, []).append(row)
    summaries = []
    for (family, stakes_key, configuration), bucket in sorted(buckets.items()):
        unit = bucket[0]["unit"]
        complete = all(row["score"].get("full_horizon") is True
                       and row["score"].get("validity_pass") is True for row in bucket)
        def metric(field):
            return hierarchical_mean(bucket, lambda row: row["score"].get(field))
        fields = {key: pair(metric(key)) for key in (
            "brier_mean", "action_loss_mean", "base_brier_mean", "uniform_brier_mean",
            "cold_units", "local_units", "optional_reporting_units")}
        per_request_units = hierarchical_mean(bucket, lambda row:
            F(row["score"]["cold_units"], row["score"]["horizon"])
            if isinstance(row["score"].get("cold_units"), int) and row["score"].get("horizon", 0) > 0 else None)
        known_costs = [row["score"].get("cold_units") for row in bucket]
        native_prices = {encoded(row["score"].get("native_price_normalized")) for row in bucket}
        if len(native_prices) != 1:
            raise L.IntegrityError("One fixed configuration has inconsistent native normalized prices.")
        learning_delta = None
        if fields["base_brier_mean"] is not None and fields["uniform_brier_mean"] is not None:
            learning_delta = fraction(fields["uniform_brier_mean"]) - fraction(fields["base_brier_mean"])
        summaries.append({"family": family, "stakes": json.loads(stakes_key),
            "configuration_id": configuration, "method": unit["method"],
            "method_kind": unit["method_kind"], "engine": unit.get("engine"),
            "group_ids": sorted({row["unit"]["group_id"] for row in bucket}),
            "planned_executions": len(bucket), "scored_executions": len(bucket),
            "complete_episodes": sum(row["score"].get("full_horizon") is True for row in bucket),
            "complete_primary_denominator": complete,
            "executed_policy_seed_slots": [row["unit"].get("seed") for row in bucket],
            "deterministic_control_replication": "single result per population is an exact analytic weight, not independent evidence",
            "known_total_executed_cold_units": sum(value for value in known_costs if isinstance(value, int)),
            "unknown_cost_episodes": sum(not isinstance(value, int) for value in known_costs),
            "missing_or_incomplete_unit_ids": [row["unit"]["id"] for row in bucket
                if row["score"].get("full_horizon") is not True or row["score"].get("validity_pass") is not True],
            "means": fields, "mean_cold_units_per_request": pair(per_request_units),
            "native_price_normalized": json.loads(next(iter(native_prices))),
            "uniform_minus_base_brier": pair(learning_delta),
            "practical_learning_effect": bool(complete and learning_delta is not None
                and learning_delta >= fraction(config["analysis"]["loss_improvement_threshold"])),
            "learning_comparator": "frozen equal-weight original expert advice; no adaptive hard-mask regret claim",
            "prespecified_slices": broker_slice_summaries(config, bucket),
            "paid_reporting": broker_report_summary(config, bucket)})
    cells = {}
    for summary in summaries:
        key = (summary["family"], encoded(summary["stakes"]), tuple(summary["group_ids"]))
        cells.setdefault(key, []).append(summary)
    catalogue = []
    for (family, stakes_key, group_ids), cell in sorted(cells.items()):
        prices = {fraction(value) for value in config["analysis"]["repricing_grid"]}
        prices.update(fraction(row["native_price_normalized"]) for row in cell
                      if row["native_price_normalized"] is not None)
        for price in sorted(prices):
            for selection in ("fixed_record_repricing", "native_price_catalogue"):
                eligible = []
                for row in cell:
                    price_sensitive = row["method"].startswith("ordinary_combo")
                    if selection == "native_price_catalogue" and price_sensitive and (
                            row["native_price_normalized"] is None or fraction(row["native_price_normalized"]) != price):
                        continue
                    eligible.append(row)
                costs = {}
                for row in eligible:
                    if (row["complete_primary_denominator"] and row["means"]["action_loss_mean"] is not None
                            and row["mean_cold_units_per_request"] is not None and row["unknown_cost_episodes"] == 0):
                        costs[row["configuration_id"]] = fraction(row["means"]["action_loss_mean"]) + price * fraction(row["mean_cold_units_per_request"])
                ordinary_ids = [row["configuration_id"] for row in eligible if row["method_kind"] == "ordinary"]
                all_ordinary_ids = [row["configuration_id"] for row in eligible if row["method_kind"] in ("ordinary", "mirror")]
                def minimum(ids):
                    if not ids or any(identifier not in costs for identifier in ids):
                        return {"value": None, "ties": [], "complete_catalogue": False}
                    value = min(costs[identifier] for identifier in ids)
                    return {"value": pair(value), "ties": [identifier for identifier in ids if costs[identifier] == value],
                            "complete_catalogue": True}
                distinct = minimum(ordinary_ids)
                candidates = []
                for row in eligible:
                    if row["method_kind"] != "candidate":
                        continue
                    value = costs.get(row["configuration_id"])
                    delta = (fraction(distinct["value"]) - value) if value is not None and distinct["value"] is not None else None
                    candidates.append({"configuration_id": row["configuration_id"], "objective": pair(value),
                        "distinct_ordinary_minus_candidate": pair(delta),
                        "practical_effect": bool(delta is not None and delta >= fraction(config["analysis"]["loss_improvement_threshold"])),
                        "ordinary_identical_configuration_objective": pair(value),
                        "ordinary_alias_scope": "same finite kernel, public path and invoice; numerical re-interpretation adds no independent execution"})
                alias_ids = all_ordinary_ids + [row["configuration_id"] for row in eligible if row["method_kind"] == "candidate"]
                catalogue.append({"family": family, "stakes": json.loads(stakes_key), "group_ids": list(group_ids),
                    "price_normalized_per_unit": pair(price), "selection": selection,
                    "whole_configuration_objectives": {key: pair(value) for key, value in sorted(costs.items())},
                    "distinct_ordinary_minimum": distinct, "ordinary_including_mirror_minimum": minimum(all_ordinary_ids),
                    "ordinary_including_identical_kernel_aliases": minimum(alias_ids),
                    "candidate_comparisons": candidates, "deployed_catalogue_oracle": False,
                    "objective": "mean normalized action loss plus normalized unit price times mean cold units per request"})
    by_id = {row["unit"]["id"]: row for row in rows}
    pairings = []
    pairing_buckets = {}
    for row in rows:
        unit, score = row["unit"], row["score"]
        for relation, target_id in unit.get("pairing", {}).items():
            if relation not in ("base_id", "cold_id", "identity_of", "stakes_reference") or target_id is None:
                continue
            if target_id not in by_id:
                raise L.IntegrityError("A frozen broker pairing target is missing.")
            target = by_id[target_id]["score"]
            comparisons = {}
            for field in ("brier_mean", "action_loss_mean", "cold_units", "local_units", "optional_reporting_units"):
                left, right = score.get(field), target.get(field)
                comparisons[field + "_target_minus_current"] = pair(fraction(right) - fraction(left)) if left is not None and right is not None else None
            common_current = common_stakes_action_loss(score, unit["stakes"])
            common_target = common_stakes_action_loss(target, unit["stakes"])
            # Re-score both action paths under ONE objective. Subtracting their
            # originally reported means would confound asymmetric stakes with
            # a change in decisions, even for two identical action sequences.
            comparisons["action_loss_mean_target_minus_current"] = pair(common_target - common_current) \
                if common_current is not None and common_target is not None else None
            current_price = fraction(score["native_price_normalized"]) if score.get("native_price_normalized") is not None else F(0)
            objective_delta = None
            if common_current is not None and common_target is not None and score.get("cold_units") is not None and target.get("cold_units") is not None:
                if score["horizon"] != target["horizon"]:
                    raise L.IntegrityError("Paired public episodes have different horizons.")
                objective_delta = common_target - common_current + current_price * F(target["cold_units"] - score["cold_units"], score["horizon"])
            comparisons["common_native_objective_target_minus_current"] = pair(objective_delta)
            fingerprints = {key: score.get(key) == target.get(key)
                            for key in ("base_path_sha256", "delivered_path_sha256", "action_path_sha256")
                            if score.get(key) is not None and target.get(key) is not None}
            identity = None
            full_pair = bool(score.get("full_horizon") and target.get("full_horizon")
                             and score.get("validity_pass") is True and target.get("validity_pass") is True)
            required = ("base_path_sha256",) if relation == "base_id" else (
                ("base_path_sha256", "delivered_path_sha256", "action_path_sha256")
                if relation in ("cold_id", "identity_of") else ())
            coupling_pass = all(fingerprints.get(key) is True for key in required) if full_pair and required else None
            if relation == "base_id" and coupling_pass:
                coupling_pass = (fraction(score["brier_mean"]) <= fraction(target["brier_mean"])
                                 and common_current <= common_target)
            equal_output = bool(full_pair and fingerprints.get("delivered_path_sha256") is True
                                and fingerprints.get("action_path_sha256") is True
                                and comparisons["brier_mean_target_minus_current"] == [0, 1]
                                and comparisons["action_loss_mean_target_minus_current"] == [0, 1])
            cost_ratio = F(score["cold_units"], target["cold_units"]) if (full_pair
                and type(score.get("cold_units")) is int and type(target.get("cold_units")) is int
                and target["cold_units"] > 0) else None
            if relation == "identity_of":
                identity = (full_pair and all(value == [0, 1] for value in comparisons.values())
                            and coupling_pass is True)
            record = {"unit_id": unit["id"], "relation": relation, "target_id": target_id,
                             "differences": comparisons, "path_equalities": fingerprints,
                             "ordinary_identity_pass": identity,
                             "coupling_pass": coupling_pass, "required_path_equalities": list(required),
                             "complete_pair": full_pair, "equal_delivered_output": equal_output,
                             "common_stakes": unit["stakes"], "common_normalized_price": pair(current_price),
                             "current_action_loss_under_common_stakes": pair(common_current),
                             "target_action_loss_under_common_stakes": pair(common_target),
                             "cold_cost_ratio_current_to_target": pair(cost_ratio),
                             "practical_equal_output_cost_saving": bool(equal_output and cost_ratio is not None
                                  and cost_ratio <= fraction(config["analysis"]["saving_ratio_threshold"])),
                             "pairing_scope": "exact preserved broker paths only; other shared seeds do not imply shared feedback"}
            pairings.append(record)
            family = group_map[unit["group_id"]]["recipe"]["family"]
            pairing_buckets.setdefault((family, unit["configuration_id"], relation), []).append(
                {"unit": unit, "record": record, "current_units": score.get("cold_units"), "target_units": target.get("cold_units")})
    paired_means = []
    for (family, configuration, relation), bucket in sorted(pairing_buckets.items()):
        action_delta = hierarchical_mean(bucket, lambda row: row["record"]["differences"]["action_loss_mean_target_minus_current"])
        objective_delta = hierarchical_mean(bucket, lambda row: row["record"]["differences"]["common_native_objective_target_minus_current"])
        current_cost = hierarchical_mean(bucket, lambda row: row["current_units"])
        target_cost = hierarchical_mean(bucket, lambda row: row["target_units"])
        ratio = current_cost / target_cost if current_cost is not None and target_cost is not None and target_cost > 0 else None
        complete = all(row["record"]["complete_pair"] for row in bucket)
        equal = complete and all(row["record"]["equal_delivered_output"] for row in bucket)
        paired_means.append({"family": family, "configuration_id": configuration, "relation": relation,
            "paired_executions": len(bucket), "complete_denominator": complete,
            "common_stakes": bucket[0]["record"]["common_stakes"],
            "common_normalized_price": bucket[0]["record"]["common_normalized_price"],
            "mean_action_improvement": pair(action_delta), "mean_common_objective_improvement": pair(objective_delta),
            "practical_action_effect": bool(complete and action_delta is not None and action_delta >= fraction(config["analysis"]["loss_improvement_threshold"])),
            "practical_priced_effect": bool(complete and objective_delta is not None and objective_delta >= fraction(config["analysis"]["loss_improvement_threshold"])),
            "every_pair_equal_delivered_output": equal, "mean_cold_cost_ratio": pair(ratio),
            "practical_equal_output_cost_saving": bool(equal and ratio is not None and ratio <= fraction(config["analysis"]["saving_ratio_threshold"]))})
    return {"configuration_means": summaries, "catalogue_comparisons": catalogue,
            "paired_records": pairings, "paired_configuration_effects": paired_means,
            "coupling_violations": [row["unit_id"] for row in pairings
                if row["coupling_pass"] is False or row["ordinary_identity_pass"] is False],
            "ordinary_identity_violations": [row["unit_id"] for row in pairings if row["ordinary_identity_pass"] is False],
            "coupling_unavailable_pairs": [row["unit_id"] for row in pairings if row["required_path_equalities"] and row["coupling_pass"] is None],
            "per_unit_scores": rows,
            "inferential_status": "exact descriptive fixed finite cohort; no IID, p-value or seed-coverage inference"}


def certificate_analysis(config, group_map, rows):
    cells = {}
    for row in rows:
        unit = row["unit"]
        family = group_map[unit["group_id"]]["recipe"]["family"]
        # Both each stream and its prespecified family aggregate are retained.
        for scope in (unit["group_id"], "family:" + family):
            key = (scope, unit["recipient"], unit["budget_condition"])
            cells.setdefault(key, []).append(row)
    summaries, comparisons = [], []
    for (scope, recipient, budget), cell in sorted(cells.items()):
        methods = {}
        for row in cell:
            methods.setdefault(row["unit"]["method"], []).append(row)
        aggregates = []
        for method, bucket in sorted(methods.items()):
            expected, delivered = set(), set()
            known_cost, unknown = 0, 0
            valid = True
            category_totals = {}
            tariff_totals = {}
            categories_complete = True
            for row in bucket:
                score = row["score"]
                all_ids, delivered_ids = score["all_request_ids"], score["delivered_request_ids"]
                if len(set(all_ids)) != len(all_ids) or len(set(delivered_ids)) != len(delivered_ids):
                    raise L.IntegrityError("Duplicate certificate request IDs.")
                if expected.intersection(all_ids) or not set(delivered_ids).issubset(all_ids):
                    raise L.IntegrityError("Certificate request domains overlap or delivered IDs escape scope.")
                if score["request_count"] != len(all_ids):
                    raise L.IntegrityError("Certificate request denominator disagrees with IDs.")
                expected.update(all_ids)
                delivered.update(delivered_ids)
                valid = valid and score.get("validity_pass") is True
                units = score.get("total_units")
                if type(units) is int and units >= 0:
                    known_cost += units
                else:
                    unknown += 1
                for category, value in score.get("category_totals", {}).items():
                    category_totals[category] = category_totals.get(category, 0) + value
                for category, value in score.get("tariff_category_totals", {}).items():
                    tariff_totals[category] = tariff_totals.get(category, 0) + value
                categories_complete = categories_complete and score.get("category_totals_complete", not unknown) is True
            aggregate = {"scope": scope, "recipient": recipient, "budget_condition": budget,
                         "method": method, "method_kind": bucket[0]["unit"]["method_kind"],
                         "planned_histories": len(bucket), "request_count": len(expected),
                         "all_request_ids": sorted(expected), "delivered_request_ids": sorted(delivered),
                         "delivered_count": len(delivered), "failed_count": len(expected - delivered),
                         "validity_pass": valid, "complete_service": valid and delivered == expected,
                         "known_all_attempt_units": known_cost, "unknown_cost_histories": unknown,
                         "total_units": known_cost if unknown == 0 else None,
                         "category_totals": category_totals,
                         "category_coordinate_convention": "producer+consumer partitions total; output/storage/source overlap and must not be added as another bill",
                         "tariff_category_totals": tariff_totals,
                         "category_totals_complete": categories_complete}
            aggregates.append(aggregate)
            summaries.append(aggregate)
        universes = {tuple(row["all_request_ids"]) for row in aggregates}
        if len(universes) != 1:
            raise L.IntegrityError("Competing certificate methods have unequal scheduled request universes.")
        for left in aggregates:
            for right in aggregates:
                if left["method"] == right["method"]:
                    continue
                covered_left, covered_right = set(left["delivered_request_ids"]), set(right["delivered_request_ids"])
                costs_known = left["total_units"] is not None and right["total_units"] is not None
                admissible = left["validity_pass"] and right["validity_pass"] and costs_known
                superset = covered_left.issuperset(covered_right)
                nonempty = bool(covered_left)
                weak = bool(admissible and nonempty and superset and left["total_units"] <= right["total_units"])
                practical = bool(admissible and nonempty and superset and right["total_units"] > 0
                    and F(left["total_units"], right["total_units"]) <= fraction(config["analysis"]["saving_ratio_threshold"]))
                comparisons.append({"scope": scope, "recipient": recipient, "budget_condition": budget,
                    "left": left["method"], "right": right["method"], "coverage_superset": superset,
                    "identical_coverage": covered_left == covered_right, "both_complete": left["complete_service"] and right["complete_service"],
                    "left_weakly_dominates": weak, "left_practical_cost_dominance": practical,
                    "left_to_right_total_cost_ratio": pair(F(left["total_units"], right["total_units"]))
                        if costs_known and right["total_units"] > 0 else None,
                    "right_minus_left_total_units": right["total_units"] - left["total_units"] if costs_known else None,
                    "componentwise_named_diagnostic_dominance": bool(admissible and nonempty and superset
                        and left["category_totals_complete"] and right["category_totals_complete"]
                        and bool(left["category_totals"])
                        and set(left["category_totals"]) == set(right["category_totals"])
                        and all(left["category_totals"][key] <= right["category_totals"][key] for key in left["category_totals"])),
                    "componentwise_primitive_tariff_dominance": bool(admissible and nonempty and superset
                        and left["category_totals_complete"] and right["category_totals_complete"]
                        and bool(left["tariff_category_totals"] or right["tariff_category_totals"])
                        and all(left["tariff_category_totals"].get(key, 0) <= right["tariff_category_totals"].get(key, 0)
                                for key in set(left["tariff_category_totals"]) | set(right["tariff_category_totals"])))})
    return {"complete_histories": summaries, "coverage_cost_comparisons": comparisons,
            "per_unit_scores": rows, "tariff_scope": "Option B declared total invoice; no CNF-word exchange rate"}


def conformance_analysis(rows):
    return {"planned_units": len(rows), "scored_units": len(rows),
            "valid_units": sum(row["score"].get("validity_pass") is True for row in rows),
            "all_exact_obligations_pass": all(row["score"].get("validity_pass") is True for row in rows),
            "failed_unit_ids": [row["unit"]["id"] for row in rows if row["score"].get("validity_pass") is not True],
            "per_unit_scores": rows,
            "scope": "previously exposed structural and information-theorem conformance; not unseen-policy transfer"}


def analyze(config, schedule, completed, *, execution_audit):
    rows = rows_from_seals(schedule, completed)
    group_map = {group["id"]: group for group in schedule["groups"]}
    arms = {arm: [row for row in rows if row["unit"]["arm"] == arm]
            for arm in ("broker", "certificates", "conformance")}
    broker = broker_analysis(config, group_map, arms["broker"])
    certificates = certificate_analysis(config, group_map, arms["certificates"])
    complete_outer_cost = execution_audit["complete_outer_paid_attempt_accounting"]
    for comparison in certificates["coverage_cost_comparisons"]:
        comparison["completed_path_cost_threshold_met"] = comparison["left_practical_cost_dominance"]
        comparison["left_practical_cost_dominance"] = comparison["left_practical_cost_dominance"] and complete_outer_cost
    for comparison in broker["catalogue_comparisons"]:
        for candidate in comparison["candidate_comparisons"]:
            candidate["completed_path_practical_effect"] = candidate["practical_effect"]
            if fraction(comparison["price_normalized_per_unit"]) > 0:
                candidate["practical_effect"] = candidate["practical_effect"] and complete_outer_cost
    for comparison in broker["paired_records"] + broker["paired_configuration_effects"]:
        comparison["completed_path_equal_output_cost_threshold_met"] = comparison["practical_equal_output_cost_saving"]
        comparison["practical_equal_output_cost_saving"] = comparison["practical_equal_output_cost_saving"] and complete_outer_cost
        if "practical_priced_effect" in comparison:
            comparison["completed_path_priced_threshold_met"] = comparison["practical_priced_effect"]
            if fraction(comparison["common_normalized_price"]) > 0:
                comparison["practical_priced_effect"] = comparison["practical_priced_effect"] and complete_outer_cost
    return {"schema": "value_logic.p309.analysis.v1", "stage": "P3-10-FINAL-FINITE-COHORT",
            "freeze_id": config["freeze_id"], "configuration_sha256": L.digest(config),
            "expected_score_units": len(schedule["units"]), "received_score_units": len(rows),
            "broker": broker,
            "certificates": certificates,
            "conformance": conformance_analysis(arms["conformance"]),
            "execution_attempt_audit": execution_audit,
            "complete_outer_attempt_economic_claim_permitted": execution_audit["complete_outer_paid_attempt_accounting"],
            "cost_interpretation": "thresholds on sealed completed paths do not establish complete outer-attempt savings when an interrupted prefix has unknown cost",
            "cross_tariff_total": None, "five_empirical_wins_required": False,
            "contribution_decision": "requires later scoped interpretation and author gate; no automatic phase completion"}


def selfcheck():
    """DEVELOPMENT arithmetic and denominator counterexamples only."""
    checks = []
    assert mean([F(1, 3), F(2, 3)]) == F(1, 2)
    assert mean([None, F(1)]) is None
    checks.append("exact fractions and missing means")
    # Mean of per-seed minima is zero, but every whole fixed policy costs1/2.
    policy_a, policy_b = [F(0), F(1)], [F(1), F(0)]
    assert min(mean(policy_a), mean(policy_b)) == F(1, 2)
    assert mean([min(a, b) for a, b in zip(policy_a, policy_b)]) == 0
    checks.append("whole-policy catalogue minimum differs from hindsight switching")
    assert hierarchical_mean([
        {"unit": {"group_id": "dev-one"}, "x": F(1)},
        {"unit": {"group_id": "dev-two"}, "x": F(0)},
        {"unit": {"group_id": "dev-two"}, "x": F(0)}], lambda row: row["x"]) == F(1, 2)
    checks.append("equal population weighting is not unequal execution weighting")
    same_actions = {"full_horizon": True, "validity_pass": True, "horizon": 2,
                    "false_positives": 1, "false_negatives": 0}
    old = common_stakes_action_loss(same_actions, {"fp": [1, 1], "fn": [1, 1]})
    new = common_stakes_action_loss(same_actions, {"fp": [1, 2], "fn": [3, 2]})
    assert old - new == F(1, 3)
    assert new - common_stakes_action_loss(same_actions, {"fp": [1, 2], "fn": [3, 2]}) == 0
    checks.append("identical actions cannot improve merely by changing stake normalization")
    config = {"analysis": {"saving_ratio_threshold": [19, 20],
        "loss_improvement_threshold": [1, 100], "report_width_improvement_threshold": [1, 100]}}
    def slice_row(identifier, group, value, complete=True):
        metrics = {"horizon": 2, "rounds_closed": 2, "full_horizon": True,
            "brier_mean": pair(value), "base_brier_mean": pair(value),
            "uniform_brier_mean": [1, 1], "action_loss_mean": pair(value)}
        return {"unit": {"id": identifier, "group_id": group,
                "segments": [{"name": "whole", "start": 0, "stop": 2}]},
            "score": {"full_horizon": complete, "validity_pass": True,
                "first_occurrence": metrics, "segments": {"whole": metrics}}}
    slices = broker_slice_summaries(config, [slice_row("a", "one", F(1)),
        slice_row("b", "two", F(0)), slice_row("c", "two", F(0))])
    assert all(row["means"]["brier_mean"] == [1, 2] and row["known_scheduled_positions"] == 6 for row in slices)
    incomplete = broker_slice_summaries(config, [slice_row("a", "one", F(0), False)])
    assert all(row["means"]["brier_mean"] is None and not row["practical_learning_effect"] for row in incomplete)
    checks.append("slice weights keep populations equal and incomplete parents cannot supply positive primary effects")
    endpoint = {"status": "success", "deterministic_width_per_horizon": [1, 1],
        "width_per_horizon": [99, 100], "normalized_width_reduction": [1, 100],
        "normalized_lower_endpoint_gain": [1, 100], "normalized_upper_endpoint_gain": [0, 1]}
    report_row = {"unit": {"id": "report-a", "group_id": "dev-report", "engine": "broker"},
        "score": {"full_horizon": True, "validity_pass": True, "optional_reporting_units": 17,
            "paid_report_comparison": {"status": "success", "endpoints": {key: endpoint for key in ("V", "F", "Z")}}}}
    reporting = broker_report_summary(config, [report_row])
    assert all(row["practical_width_reduction"] for row in reporting["endpoints"].values())
    failed_report = {"unit": dict(report_row["unit"], id="report-b"),
        "score": dict(report_row["score"], optional_reporting_units=3, paid_report_comparison={"status": "failed"})}
    reporting = broker_report_summary(config, [report_row, failed_report])
    assert reporting["known_total_additional_units"] == 20
    assert all(row["means"]["normalized_width_reduction"] is None and not row["practical_width_reduction"]
               for row in reporting["endpoints"].values())
    checks.append("paid-report exact threshold is inclusive and a failed report preserves its fee and scheduled denominator")
    group_map = {"dev-group": {"recipe": {"family": "explicit-development-sets"}}}
    def row(method, ids, bill):
        return {"unit": {"group_id": "dev-group", "recipient": "fresh", "budget_condition": "dev",
                         "method": method, "method_kind": "ordinary"},
                "score": {"all_request_ids": ["dev-1", "dev-2"], "delivered_request_ids": ids,
                          "request_count": 2, "total_units": bill, "validity_pass": True,
                          "category_totals": {"all": bill}}}
    result = certificate_analysis(config, group_map, [row("a", ["dev-1"], 90), row("b", ["dev-2"], 100)])
    assert not any(value["left_practical_cost_dominance"] for value in result["coverage_cost_comparisons"])
    checks.append("equal success counts with different request IDs are incomparable")
    result = certificate_analysis(config, group_map, [row("a", [], 0), row("b", [], 100)])
    assert not any(value["left_practical_cost_dominance"] for value in result["coverage_cost_comparisons"])
    checks.append("empty delivered service cannot manufacture an economic success")
    result = certificate_analysis(config, group_map, [row("a", ["dev-1", "dev-2"], 95), row("b", ["dev-1"], 100)])
    assert any(value["left"] == "a" and value["left_practical_cost_dominance"] for value in result["coverage_cost_comparisons"])
    checks.append("exact five-percent threshold and coverage superset")
    try:
        rows_from_seals({"units": [{"id": "dev-required"}]}, [])
    except L.IntegrityError:
        checks.append("missing expected private score blocks aggregate analysis")
    else:
        raise AssertionError("Missing score accepted.")
    return {"stage": "DEVELOPMENT", "status": "PASS", "final_population_generated": False,
            "fixture_scope": "explicit rational arrays and request-ID sets only", "checks": checks, "passed": len(checks)}
