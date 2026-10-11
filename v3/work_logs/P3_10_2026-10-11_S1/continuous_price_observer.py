"""Exact supplemental fixed-record price regions for completed P3-10 results.

Contributor: ChatGPT (GPT-6 Astra Pro), principal /root, 2026-10-11.
Reads sealed score records and independently forms hierarchical affine means.
Does not import a frozen module, change a price-sensitive policy, rerun any
method, or extrapolate the native-price catalogue. Raw score reconstruction is
separately supplied by the independent broker reviewer.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import time
import traceback

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FINAL = REPO / "v3/experiments/final_v1_amended_A1"
from amended_lineage_reader import Lineage
LINEAGE = None
CHECKS = Counter()
READS = {}


def stamp():
    return {"utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns(),
            "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()}


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    READS[str(path.relative_to(REPO))] = sha(path)
    return json.loads(path.read_text())


def require(condition, name, detail):
    CHECKS[name] += 1
    if not condition:
        raise AssertionError(f"{name}: {detail}")


def rat(value):
    return F(*value) if isinstance(value, (tuple, list)) else F(value)


def encode(value):
    if isinstance(value, F):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def save(path, value):
    with path.open("x") as file:
        json.dump(encode(value), file, indent=2, sort_keys=True, allow_nan=False)
        file.write("\n")


def sealed(stage, identifier):
    require(LINEAGE is not None, "amended_lineage_barrier", identifier)
    return LINEAGE.record(stage, identifier)[0]

def region(candidate, ordinary, epsilon, strict=False):
    """Intersect all rational inequalities without a grid or tolerance."""
    lower, upper = F(0), None
    lower_closed, upper_closed = True, True
    lower_sources, upper_sources = ["nonnegative_price_domain"], []
    constraints, impossible = [], []
    for line in ordinary:
        da, db = line["a"] - candidate["a"], line["b"] - candidate["b"]
        row = {"ordinary_configuration_id": line["id"], "intercept_difference": da,
               "slope_difference": db, "threshold": epsilon,
               "comparison": ">" if strict else ">="}
        if db == 0:
            satisfied = da > epsilon if strict else da >= epsilon
            row.update(kind="constant", satisfied=satisfied)
            if not satisfied:
                impossible.append(line["id"])
        else:
            bound = (epsilon - da) / db
            row.update(kind="lower" if db > 0 else "upper", boundary=bound, closed=not strict)
            if db > 0:
                if bound > lower:
                    lower, lower_closed, lower_sources = bound, not strict, [line["id"]]
                elif bound == lower:
                    lower_closed = lower_closed and not strict
                    lower_sources.append(line["id"])
            else:
                if upper is None or bound < upper:
                    upper, upper_closed, upper_sources = bound, not strict, [line["id"]]
                elif bound == upper:
                    upper_closed = upper_closed and not strict
                    upper_sources.append(line["id"])
        constraints.append(row)
    empty = bool(impossible) or (upper is not None and (lower > upper or
                                (lower == upper and not (lower_closed and upper_closed))))
    return {"empty": empty, "lower": lower, "upper": upper,
            "upper_unbounded": upper is None, "lower_closed": lower_closed,
            "upper_closed": upper_closed if upper is not None else False,
            "lower_binding_constraints": lower_sources, "upper_binding_constraints": upper_sources,
            "impossible_constant_constraints": impossible, "constraints": constraints}


def membership(reg, price):
    if reg["empty"] or price < reg["lower"] or (price == reg["lower"] and not reg["lower_closed"]):
        return False
    return reg["upper"] is None or price < reg["upper"] or (price == reg["upper"] and reg["upper_closed"])


def value(line, price):
    return line["a"] + price * line["b"]


def minimizing(lines, price):
    best = min(value(line, price) for line in lines)
    return best, sorted(line["id"] for line in lines if value(line, price) == best)


def lower_envelope(lines):
    cuts = {F(0)}
    for i, left in enumerate(lines):
        for right in lines[i + 1:]:
            if left["b"] != right["b"]:
                crossing = (right["a"] - left["a"]) / (left["b"] - right["b"])
                if crossing >= 0:
                    cuts.add(crossing)
    cuts = sorted(cuts)
    points = [{"price": cut, "minimum": minimizing(lines, cut)[0], "ties": minimizing(lines, cut)[1]} for cut in cuts]
    intervals = []
    for index, left in enumerate(cuts):
        right = cuts[index + 1] if index + 1 < len(cuts) else None
        interior = (left + right) / 2 if right is not None else left + 1
        intervals.append({"lower": left, "upper": right, "open": True,
                          "ties": minimizing(lines, interior)[1]})
    active_points = []
    for index, point in enumerate(points):
        left_ties = intervals[index - 1]["ties"] if index else None
        right_ties = intervals[index]["ties"]
        if index == 0 or left_ties != right_ties or point["ties"] != right_ties:
            active_points.append(point)
    active_intervals = []
    for index, point in enumerate(active_points):
        right = active_points[index + 1]["price"] if index + 1 < len(active_points) else None
        interior = (point["price"] + right) / 2 if right is not None else point["price"] + 1
        active_intervals.append({"lower": point["price"], "upper": right, "open": True,
                                 "ties": minimizing(lines, interior)[1]})
    return {"distinct_cut_prices_including_zero": len(cuts), "active_boundary_points": active_points,
            "active_open_intervals": active_intervals,
            "minimizers_anywhere": sorted({identifier for point in points for identifier in point["ties"]}
                                         | {identifier for interval in intervals for identifier in interval["ties"]})}


def hierarchy(rows, getter):
    populations = defaultdict(list)
    for unit, score in rows:
        populations[unit["group_id"]].append(getter(unit, score))
    return sum((sum(values, F(0)) / len(values) for values in populations.values()), F(0)) / len(populations)


def main():
    global LINEAGE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    before = stamp()
    try:
        LINEAGE = Lineage()
        schedule = read(REPO / "v3/experiments/frozen_v1/schedule.json")
        config_path = REPO / "v3/experiments/protocol.v1.json"
        require(sha(config_path) == "dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f",
                "unchanged_machine_protocol", str(config_path))
        config = read(config_path)
        analysis = sealed("analysis", "all-frozen-endpoints")["value"]
        economic_complete = analysis["complete_outer_attempt_economic_claim_permitted"]
        families = {g["id"]: g["recipe"]["family"] for g in schedule["groups"] if g["arm"] == "broker"}
        buckets = defaultdict(list)
        for unit in schedule["units"]:
            if unit["arm"] != "broker":
                continue
            wrapper = sealed("evaluation", "score-" + unit["id"])
            require(wrapper["unit"] == dict(unit, id="score-" + unit["id"], public_unit_id=unit["id"]),
                    "frozen_score_unit", unit["id"])
            score = wrapper["value"]["score"]
            bucket = (families[unit["group_id"]], canonical(unit["stakes"]).decode().strip(), unit["configuration_id"])
            buckets[bucket].append((unit, score))
        cells = defaultdict(list)
        for (family, stakes, identifier), rows in sorted(buckets.items()):
            valid = all(score["full_horizon"] is True and score["validity_pass"] is True
                        and type(score["cold_units"]) is int and score["horizon"] > 0 for _, score in rows)
            line = {"id": identifier, "family": family, "stakes": json.loads(stakes),
                    "group_ids": sorted({unit["group_id"] for unit, _ in rows}),
                    "planned_executions": len(rows), "method_kind": rows[0][0]["method_kind"],
                    "complete": valid, "a": None, "b": None, "unit_ids": [unit["id"] for unit, _ in rows]}
            planned_native_prices = set()
            for unit, score in rows:
                native = (F(unit["parameters"].get("unit_price", "0")) /
                          max(rat(unit["stakes"]["fp"]), rat(unit["stakes"]["fn"]))) if unit["engine"] == "ordinary" else None
                planned_native_prices.add(native)
                require((None if score["native_price_normalized"] is None else rat(score["native_price_normalized"])) == native,
                        "scheduled_native_price_binding", unit["id"])
            require(len(planned_native_prices) == 1, "one_native_price_per_configuration", identifier)
            line["native_price_normalized"] = next(iter(planned_native_prices))
            if valid:
                def action(unit, score):
                    fp, fn = rat(unit["stakes"]["fp"]), rat(unit["stakes"]["fn"])
                    return (fp * score["false_positives"] + fn * score["false_negatives"]) / (score["horizon"] * max(fp, fn))
                line.update(a=hierarchy(rows, action), b=hierarchy(rows, lambda unit, score: F(score["cold_units"], score["horizon"])))
            cells[(family, stakes, tuple(line["group_ids"]))].append(line)
        frozen_cells = defaultdict(list)
        for row in analysis["broker"]["catalogue_comparisons"]:
            if row["selection"] == "fixed_record_repricing":
                frozen_cells[(row["family"], canonical(row["stakes"]).decode().strip(), tuple(row["group_ids"]))].append(row)
        require(set(frozen_cells) == set(cells), "complete_fixed_record_grid_cell_roster", sorted(frozen_cells))
        records = []
        epsilon = rat(config["analysis"]["loss_improvement_threshold"])
        require(epsilon == F(1, 100), "unchanged_practical_threshold", epsilon)
        for cell_key, lines in sorted(cells.items()):
            family, stakes, groups = cell_key
            ordinary = [line for line in lines if line["method_kind"] == "ordinary"]
            candidates = [line for line in lines if line["method_kind"] == "candidate"]
            complete = bool(ordinary) and all(line["complete"] for line in lines)
            record = {"family": family, "stakes": json.loads(stakes), "group_ids": groups,
                      "lines": lines, "complete_declared_cell": complete,
                      "complete_outer_attempt_economic_claim_permitted": economic_complete,
                      "candidate_regions": [], "frozen_grid_rows_checked": 0}
            expected_prices = {rat(p) for p in config["analysis"]["repricing_grid"]}
            expected_prices.update(line["native_price_normalized"] for line in lines if line["native_price_normalized"] is not None)
            actual_prices = [rat(row["price_normalized_per_unit"]) for row in frozen_cells[cell_key]]
            require(len(actual_prices) == len(set(actual_prices)) == len(expected_prices)
                    and set(actual_prices) == expected_prices,
                    "complete_distinct_frozen_price_roster", [family, stakes])
            record["frozen_grid_prices_required"] = sorted(expected_prices)
            if complete:
                for frozen in frozen_cells[cell_key]:
                    price = rat(frozen["price_normalized_per_unit"])
                    observed = frozen["whole_configuration_objectives"]
                    require(set(observed) == {line["id"] for line in lines}, "unchanged_complete_grid_catalogue", [family, price])
                    for line in lines:
                        require(value(line, price) == rat(observed[line["id"]]), "independent_grid_objective", [family, line["id"], price])
                    minimum, ties = minimizing(ordinary, price)
                    require(minimum == rat(frozen["distinct_ordinary_minimum"]["value"])
                            and ties == sorted(frozen["distinct_ordinary_minimum"]["ties"]),
                            "independent_grid_minimum_and_ties", [family, price])
                    record["frozen_grid_rows_checked"] += 1
                record["distinct_ordinary_lower_envelope"] = lower_envelope(ordinary)
                record["all_recorded_configuration_lower_envelope"] = lower_envelope(lines)
                prices = [rat(row["price_normalized_per_unit"]) for row in frozen_cells[cell_key]]
                for candidate in candidates:
                    weak = region(candidate, ordinary, F(0))
                    strict = region(candidate, ordinary, F(0), strict=True)
                    practical = region(candidate, ordinary, epsilon)
                    alias = dict(candidate, id="ordinary_identical_alias:" + candidate["id"])
                    alias_practical = region(candidate, ordinary + [alias], epsilon)
                    alias_strict = region(candidate, ordinary + [alias], F(0), strict=True)
                    require(alias_practical["empty"] and alias_strict["empty"], "ordinary_identity_positive_obstruction", candidate["id"])
                    for price in prices:
                        delta = minimizing(ordinary, price)[0] - value(candidate, price)
                        require(membership(weak, price) == (delta >= 0)
                                and membership(strict, price) == (delta > 0)
                                and membership(practical, price) == (delta >= epsilon),
                                "region_membership_matches_frozen_prices", [candidate["id"], price])
                    record["candidate_regions"].append({"configuration_id": candidate["id"],
                        "weak_nonnegative_region": weak, "strict_positive_region": strict,
                        "practical_region_threshold_1_100": practical,
                        "ordinary_alias_practical_region_empty": alias_practical["empty"],
                        "ordinary_alias_strict_region_empty": alias_strict["empty"],
                        "primary_grid_prices_in_practical_region": [p for p in prices if membership(practical, p)],
                        "positive_price_regions_are_only_completed_path_diagnostics_if_outer_cost_unknown": not economic_complete})
            records.append(record)
        result = {"schema": "value_logic.p310.continuous_price_observer.v1", "status": "PASS",
                  "contributor": "ChatGPT (GPT-6 Astra Pro)", "start": before, "end": stamp(),
                  "amendment_lineage": LINEAGE.receipt, "source_sha256": sha(Path(__file__)), "read_sha256": READS, "checks_by_kind": dict(CHECKS),
                  "cells": records, "selection": "fixed_record_repricing only",
                  "price_domain": "all exact nonnegative normalized unit prices",
                  "ordinary_catalogue_scope": "the full frozen distinct ordinary catalogue within each original stake/population cell",
                  "unchanged_frozen_grid_primary": True, "deployed_oracle": False,
                  "new_policy_execution": False, "sampling_inference": False,
                  "economic_gate": "At positive price, unknown interrupted-attempt costs prohibit an end-to-end economic claim even when a completed-path interval is nonempty."}
        save(out / "results.json", result)
        print(json.dumps({"status": "PASS", "cells": len(records), "configurations": sum(map(len, cells.values())),
                          "candidate_regions": sum(len(row["candidate_regions"]) for row in records),
                          "strict_nonempty": sum(not c["strict_positive_region"]["empty"] for row in records for c in row["candidate_regions"]),
                          "practical_nonempty": sum(not c["practical_region_threshold_1_100"]["empty"] for row in records for c in row["candidate_regions"]),
                          "checks_total": sum(CHECKS.values())}, indent=2))
    except BaseException as error:
        save(out / "failure.json", {"status": "OBSERVER_FAILURE", "start": before, "end": stamp(),
            "amendment_lineage": LINEAGE.receipt, "source_sha256": sha(Path(__file__)), "error_type": type(error).__name__, "error": str(error),
            "traceback": traceback.format_exc(), "checks_completed": dict(CHECKS), "scientific_stage_failure": False})
        raise


if __name__ == "__main__":
    main()
