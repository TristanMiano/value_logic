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
                       and row["score"].get("validity_pass", True) is True for row in bucket)
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
            "missing_or_incomplete_unit_ids": [row["unit"]["id"] for row in bucket if not row["score"].get("full_horizon")],
            "means": fields, "mean_cold_units_per_request": pair(per_request_units),
            "native_price_normalized": json.loads(next(iter(native_prices))),
            "uniform_minus_base_brier": pair(learning_delta),
            "practical_learning_effect": bool(complete and learning_delta is not None
                and learning_delta >= fraction(config["analysis"]["loss_improvement_threshold"])),
            "learning_comparator": "frozen equal-weight original expert advice; no adaptive hard-mask regret claim"})
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
            fingerprints = {key: score.get(key) == target.get(key)
                            for key in ("base_path_sha256", "delivered_path_sha256", "action_path_sha256")
                            if score.get(key) is not None and target.get(key) is not None}
            identity = None
            if relation == "identity_of":
                identity = (all(value == [0, 1] for value in comparisons.values())
                            and bool(fingerprints) and all(fingerprints.values()))
            pairings.append({"unit_id": unit["id"], "relation": relation, "target_id": target_id,
                             "differences": comparisons, "path_equalities": fingerprints,
                             "ordinary_identity_pass": identity,
                             "pairing_scope": "exact preserved broker paths only; other shared seeds do not imply shared feedback"})
    return {"configuration_means": summaries, "catalogue_comparisons": catalogue,
            "paired_records": pairings, "per_unit_scores": rows,
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
                if isinstance(units, int) and units >= 0:
                    known_cost += units
                else:
                    unknown += 1
                for category, value in score.get("category_totals", {}).items():
                    category_totals[category] = category_totals.get(category, 0) + value
            aggregate = {"scope": scope, "recipient": recipient, "budget_condition": budget,
                         "method": method, "method_kind": bucket[0]["unit"]["method_kind"],
                         "planned_histories": len(bucket), "request_count": len(expected),
                         "all_request_ids": sorted(expected), "delivered_request_ids": sorted(delivered),
                         "delivered_count": len(delivered), "failed_count": len(expected - delivered),
                         "validity_pass": valid, "complete_service": valid and delivered == expected,
                         "known_all_attempt_units": known_cost, "unknown_cost_histories": unknown,
                         "total_units": known_cost if unknown == 0 else None,
                         "category_totals": category_totals}
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
                    "componentwise_resource_dominance": bool(admissible and nonempty and superset
                        and set(left["category_totals"]) == set(right["category_totals"])
                        and all(left["category_totals"][key] <= right["category_totals"][key] for key in left["category_totals"]))})
    return {"complete_histories": summaries, "coverage_cost_comparisons": comparisons,
            "per_unit_scores": rows, "tariff_scope": "Option B declared total invoice; no CNF-word exchange rate"}


def conformance_analysis(rows):
    return {"planned_units": len(rows), "scored_units": len(rows),
            "valid_units": sum(row["score"].get("validity_pass") is True for row in rows),
            "all_exact_obligations_pass": all(row["score"].get("validity_pass") is True for row in rows),
            "failed_unit_ids": [row["unit"]["id"] for row in rows if row["score"].get("validity_pass") is not True],
            "per_unit_scores": rows,
            "scope": "previously exposed structural and information-theorem conformance; not unseen-policy transfer"}


def analyze(config, schedule, completed):
    rows = rows_from_seals(schedule, completed)
    group_map = {group["id"]: group for group in schedule["groups"]}
    arms = {arm: [row for row in rows if row["unit"]["arm"] == arm]
            for arm in ("broker", "certificates", "conformance")}
    return {"schema": "value_logic.p309.analysis.v1", "stage": "P3-10-FINAL-FINITE-COHORT",
            "freeze_id": config["freeze_id"], "configuration_sha256": L.digest(config),
            "expected_score_units": len(schedule["units"]), "received_score_units": len(rows),
            "broker": broker_analysis(config, group_map, arms["broker"]),
            "certificates": certificate_analysis(config, group_map, arms["certificates"]),
            "conformance": conformance_analysis(arms["conformance"]),
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
    config = {"analysis": {"saving_ratio_threshold": [19, 20]}}
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
