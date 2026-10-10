"""Independent crossing-cell reconstruction; DEVELOPMENT, no policy execution.

Contributor: ChatGPT (GPT-6 Astra Pro), ordinary-controls reviewer, 2026-10-10.
Uses only captured JSON evidence, exact arithmetic, and the Python standard
library. Neither analyzed module is imported. Zero research-clock credit.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import traceback


HERE = Path(__file__).resolve().parent
SEEDS = (11, 29, 47)
SCENARIOS = ("cold_mixed", "repeat_online", "cheap_structure")
DETERMINISTIC = frozenset((
    "proof_enumeration", "proof_dpll", "exact_enumeration", "exact_dpll",
    "exact_cache", "exact_cache_hashed", "no_compute_0", "no_compute_1",
))
SOURCE_UNITS = 50115


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pair(value):
    return None if value is None else [value.numerator, value.denominator]


def unpack(value):
    return None if value is None else Fraction(*value)


def frozen(configuration):
    # Structural grouping retains every value, without depending on a record ID.
    return tuple(sorted((key, json.dumps(value, sort_keys=True,
                        separators=(",", ":")))
                        for key, value in configuration.items()))


def identity(scenario, family, configuration):
    return scenario, family, frozen(configuration)


def group_label(family, configuration):
    # This is only the analyzer's display label, never the grouping identity.
    return family + "/" + json.dumps(configuration, sort_keys=True)


def read_json(path):
    return json.loads(Path(path).read_text())


def verify_inputs():
    manifest = read_json(HERE / "input_manifest.json")
    for row in manifest["files"]:
        path = HERE / row["snapshot"]
        assert path.stat().st_size == row["bytes"], row
        assert sha(path) == row["sha256"], row
    assert sha(HERE / "plan.md") == manifest["review_plan_sha256"]
    assert sha(Path(__file__)) == manifest["independent_checker_sha256"]
    for directory in ("run_v1", "mean_run_v1"):
        base = HERE / "inputs" / directory
        bound = read_json(base / "manifest.json")
        assert bound["stage"] == "DEVELOPMENT"
        assert {row["path"] for row in bound["files"]} == {
            "results.json", "p308_price_envelope.py" if directory == "run_v1"
            else "p308_mean_price_envelope.py"}
        for row in bound["files"]:
            assert (base / row["path"]).stat().st_size == row["bytes"]
            assert sha(base / row["path"]) == row["sha256"]
    for name, directory in (("p308_price_envelope.py", "run_v1"),
                            ("p308_mean_price_envelope.py", "mean_run_v1")):
        assert (HERE / "inputs" / "live_source" / name).read_bytes() == (
            HERE / "inputs" / directory / name).read_bytes()
    return manifest


def reconstruct(source, recorded):
    rows = source["lines"]
    assert len(rows) == 234
    assert len({r["record"] for r in rows}) == len(rows)
    assert source["common_source_units"] == SOURCE_UNITS
    assert source["stage"] == "DEVELOPMENT" and source["policy_runs_added"] == 0
    partitions = defaultdict(list)
    configurations = {}
    for row in rows:
        family = row["record"].split("/", 1)[0]
        assert family in ("common_v2", "reuse_v1_1")
        cfg = row["configuration"]
        assert cfg["seed"] == row["seed"] and row["seed"] in SEEDS
        assert cfg.get("scenario", row["scenario"]) == row["scenario"]
        assert row["scenario"] in SCENARIOS
        broker = family == "reuse_v1_1" or cfg["kind"] == "broker"
        deterministic = (family == "common_v2" and cfg["kind"] == "ordinary"
                         and cfg["method"] in DETERMINISTIC)
        assert row["deterministic_across_seeds"] is deterministic
        assert row["ordinary_kernel_equivalent"] is broker
        assert row["ordinary_control"] is (not broker)
        assert row["recorded_acquisition_price"] == cfg.get("unit_price")
        assert row["source_procurement_transfer"] == (
            1841 if family == "common_v2" else 0)
        for field in ("terminal_errors", "local_units", "cold_units_current_common_bundle"):
            assert type(row[field]) is int and row[field] >= 0
        assert row["cold_units_current_common_bundle"] == row["local_units"] + SOURCE_UNITS
        cfg_without_seed = {key: value for key, value in cfg.items() if key != "seed"}
        ident = identity(row["scenario"], family, cfg_without_seed)
        configurations[ident] = cfg_without_seed
        partitions[ident].append(row)
    assert len(partitions) == 102
    archived = {}
    for row in recorded["mean_lines"]:
        ident = identity(row["scenario"], row["family"], row["configuration"])
        assert ident not in archived
        archived[ident] = row
    omitted_archived = {}
    for row in recorded["omitted_incomplete_groups"]:
        ident = identity(row["scenario"], row["family"], row["configuration"])
        assert ident not in omitted_archived
        omitted_archived[ident] = row
    retained, omitted = [], []
    seed_catalogues = defaultdict(dict)
    for ident, group in sorted(partitions.items()):
        scenario, family, _ = ident
        cfg = configurations[ident]
        seeds = sorted(row["seed"] for row in group)
        classification = {row["deterministic_across_seeds"] for row in group}
        assert len(classification) == 1
        deterministic = next(iter(classification))
        if deterministic:
            assert len(group) == 1 and seeds == [11]
            expanded = [group[0]] * len(SEEDS)
        elif seeds == list(SEEDS):
            expanded = sorted(group, key=lambda row: row["seed"])
        else:
            assert seeds == [11] and family == "reuse_v1_1"
            assert scenario in ("cold_mixed", "cheap_structure")
            assert cfg["hard"] is True
            assert cfg["selector"] in ("uniform", "tickets")
            assert cfg["provider"] in ("cold", "linear", "hashed")
            expected = {"scenario": scenario, "family": family,
                        "configuration": cfg, "seeds": seeds,
                        "reason": "No complete three-seed stochastic configuration; no imputation."}
            assert expected == omitted_archived.pop(ident)
            assert ident not in archived
            omitted.append(expected)
            continue
        errors = Fraction(sum(row["terminal_errors"] for row in expanded), len(SEEDS))
        cold = Fraction(sum(row["cold_units_current_common_bundle"] for row in expanded), len(SEEDS))
        expected = {"key": group_label(family, cfg), "scenario": scenario,
                    "family": family, "configuration": cfg,
                    "records": [row["record"] for row in group],
                    "deterministic_reuse": deterministic,
                    "mean_errors": pair(errors), "mean_cold_units": pair(cold),
                    "ordinary_control": group[0]["ordinary_control"],
                    "ordinary_kernel_equivalent": group[0]["ordinary_kernel_equivalent"]}
        assert expected == archived.pop(ident), ident
        assert {row["ordinary_control"] for row in group} == {expected["ordinary_control"]}
        assert {row["ordinary_kernel_equivalent"] for row in group} == {expected["ordinary_kernel_equivalent"]}
        uid = f"{scenario}:{len(retained):03d}"
        retained.append({"review_uid": uid, **expected})
        for seed, row in zip(SEEDS, expanded):
            assert uid not in seed_catalogues[(scenario, seed)]
            seed_catalogues[(scenario, seed)][uid] = {
                "record": row["record"], "errors": row["terminal_errors"],
                "cold_units": row["cold_units_current_common_bundle"]}
    assert not archived and not omitted_archived
    assert len(retained) == 90 and len(omitted) == 12
    assert sum(row["deterministic_reuse"] for row in retained) == 24
    assert sum(len(row["records"]) for row in retained) == 222
    assert sum(map(len, seed_catalogues.values())) == 270
    assert Counter(row["scenario"] for row in retained) == {
        "cold_mixed": 26, "repeat_online": 38, "cheap_structure": 26}
    return retained, omitted, seed_catalogues


def crossing_audit(scenario, lines, archived, seed_catalogues):
    assert archived["configuration_count"] == len(lines)
    by_uid = {row["review_uid"]: row for row in lines}
    coefficients = {uid: (unpack(row["mean_errors"]), unpack(row["mean_cold_units"]))
                    for uid, row in by_uid.items()}
    crossings = {Fraction(0)}
    for (e1, c1), (e2, c2) in itertools.combinations(coefficients.values(), 2):
        if c1 != c2:
            crossing = (e2-e1)/(c1-c2)
            if crossing >= 0:
                crossings.add(crossing)
    points = sorted(crossings)
    atoms = []
    for index, point in enumerate(points):
        atoms.append(("point", point, point, point))
        next_point = points[index+1] if index+1 < len(points) else None
        atoms.append(("open_cell" if next_point is not None else "tail",
                      point, next_point,
                      (point+next_point)/2 if next_point is not None else point+1))
    membership = defaultdict(list)
    cells = []
    for index, (kind, low, high, witness) in enumerate(atoms):
        values = {uid: e+witness*c for uid, (e, c) in coefficients.items()}
        best = min(values.values())
        winners = sorted(uid for uid, value in values.items() if value == best)
        local_values = {uid: e+witness*(c-SOURCE_UNITS)
                        for uid, (e, c) in coefficients.items()}
        assert winners == sorted(uid for uid, value in local_values.items()
                                 if value == min(local_values.values()))
        for uid in winners:
            membership[uid].append(index)
        cells.append({"kind": kind, "lambda_min": pair(low), "lambda_max": pair(high),
                      "witness": pair(witness), "objective_at_witness": pair(best),
                      "winner_uids": winners})
    frontier = []
    recorded_frontier = {row["key"]: row for row in archived["frontier"]}
    assert len(recorded_frontier) == len(archived["frontier"])
    for uid, active in membership.items():
        assert active == list(range(active[0], active[-1]+1)), uid
        first, last = atoms[active[0]], atoms[active[-1]]
        assert first[0] == "point" and last[0] in ("point", "tail")
        low, high = first[1], last[2]
        row = by_uid[uid]
        expected = {"key": row["key"], "lambda_min": pair(low), "lambda_max": pair(high),
                    "positive_width": high is None or high > low,
                    "mean_errors": row["mean_errors"], "mean_cold_units": row["mean_cold_units"],
                    "ordinary_control": row["ordinary_control"],
                    "ordinary_kernel_equivalent": row["ordinary_kernel_equivalent"]}
        assert expected == recorded_frontier.pop(row["key"]), uid
        assert expected["ordinary_control"] is True
        assert expected["ordinary_kernel_equivalent"] is False
        if not expected["positive_width"]:
            assert low == high == 0
        frontier.append({"review_uid": uid, **expected})
    assert not recorded_frontier
    assert all(not row["ordinary_kernel_equivalent"]
               for row in lines if row["review_uid"] in membership)
    # A crossing can be irrelevant to the lower envelope. Check the complete
    # archived active set at every point/cell rather than only frontier witnesses.
    for cell in cells:
        witness = unpack(cell["witness"])
        claimed = sorted(row["review_uid"] for row in frontier
                         if unpack(row["lambda_min"]) <= witness and
                         (row["lambda_max"] is None or witness <= unpack(row["lambda_max"])))
        assert claimed == cell["winner_uids"]
    price = Fraction(1, 30000)
    config_values = {uid: e+price*c for uid, (e, c) in coefficients.items()}
    seed_results = []
    for seed in SEEDS:
        catalogue = seed_catalogues[(scenario, seed)]
        assert set(catalogue) == set(by_uid)
        values = {uid: row["errors"]+price*row["cold_units"]
                  for uid, row in catalogue.items()}
        best = min(values.values())
        winners = sorted(uid for uid, value in values.items() if value == best)
        seed_results.append({"seed": seed, "catalogue_size": len(catalogue),
                             "minimum": pair(best), "winner_uids": winners,
                             "winner_records": [catalogue[uid]["record"] for uid in winners]})
    for uid, value in config_values.items():
        direct_average = sum(Fraction(seed_catalogues[(scenario, seed)][uid]["errors"])
                             + price*seed_catalogues[(scenario, seed)][uid]["cold_units"]
                             for seed in SEEDS) / len(SEEDS)
        assert direct_average == value
    best_mean = min(config_values.values())
    fixed_winners = sorted(uid for uid, value in config_values.items() if value == best_mean)
    mean_minima = sum(unpack(row["minimum"]) for row in seed_results) / len(SEEDS)
    gap = best_mean-mean_minima
    assert gap >= 0
    assert archived["price"] == pair(price)
    assert archived["fixed_configuration_minimum_mean"] == pair(best_mean)
    assert set(archived["fixed_winners"]) == {by_uid[uid]["key"] for uid in fixed_winners}
    assert archived["per_seed_minima"] == [row["minimum"] for row in seed_results]
    assert archived["mean_per_seed_minimum"] == pair(mean_minima)
    assert archived["hindsight_configuration_selection_gap"] == pair(gap)
    return {"scenario": scenario, "configuration_count": len(lines),
            "crossing_points": len(points), "point_and_cell_evaluations": len(atoms),
            "frontier_count": len(frontier),
            "positive_width_count": sum(row["positive_width"] for row in frontier),
            "broker_frontier_count_including_zero_ties": 0,
            "frontier": sorted(frontier, key=lambda row: (unpack(row["lambda_min"]), row["key"])),
            "cells": cells, "price": pair(price),
            "fixed_configuration_minimum_mean": pair(best_mean),
            "fixed_winner_uids": fixed_winners, "per_seed_same_catalogue": seed_results,
            "mean_per_seed_minimum": pair(mean_minima),
            "hindsight_configuration_selection_gap": pair(gap)}


def main(out):
    out = Path(out).resolve()
    assert not out.exists(), out
    started = datetime.now(timezone.utc).isoformat()
    manifest = verify_inputs()
    source = read_json(HERE / "inputs/run_v1/results.json")
    recorded = read_json(HERE / "inputs/mean_run_v1/results.json")
    assert recorded["source_sha256"] == sha(HERE / "inputs/run_v1/results.json")
    assert recorded["stage"] == "DEVELOPMENT"
    assert recorded["source_records"] == 234 and recorded["configuration_count"] == 90
    assert recorded["new_policy_runs"] == 0
    assert recorded["fair_bit_expectation_or_population_claim"] is False
    assert recorded["seedwise_selector_is_deployable"] is False
    retained, omitted, seed_catalogues = reconstruct(source, recorded)
    scenario_records = {row["scenario"]: row for row in recorded["scenarios"]}
    assert len(scenario_records) == 3 and set(scenario_records) == set(SCENARIOS)
    results = [crossing_audit(scenario,
               [row for row in retained if row["scenario"] == scenario],
               scenario_records[scenario], seed_catalogues) for scenario in SCENARIOS]
    assert verify_inputs() == manifest
    ended = datetime.now(timezone.utc).isoformat()
    detailed = {"reconstructed_mean_lines": retained, "omitted_incomplete_groups": omitted,
                "scenarios": results}
    summary = {"status": "PASS", "stage": "DEVELOPMENT", "reviewer": "ordinary_controls",
               "model": "ChatGPT (GPT-6 Astra Pro)", "same_model_nonblind": True,
               "principal_research_seconds": 0, "agent_research_seconds": 0,
               "policy_runs_added": 0, "private_scorer_runs_added": 0,
               "analyzed_modules_imported": False,
               "execution_start_utc": started, "execution_end_utc": ended,
               "checker_sha256": sha(Path(__file__)),
               "input_manifest_sha256": sha(HERE / "input_manifest.json"),
               "upstream_result_sha256": sha(HERE / "inputs/run_v1/results.json"),
               "mean_result_sha256": sha(HERE / "inputs/mean_run_v1/results.json"),
               "input_records": 234, "initial_configuration_groups": 102,
               "retained_configurations": 90, "retained_stochastic_configurations": 66,
               "reused_deterministic_configurations": 24,
               "omitted_incomplete_groups": 12, "retained_physical_records": 222,
               "expanded_seed_line_appearances": 270,
               "same_catalogue_on_both_sides": True,
               "no_broker_mean_optimal_for_any_nonnegative_price_including_ties": True,
               "new_expectation_estimate_or_deployable_selector": False,
               "scenarios": [{key: value for key, value in row.items()
                              if key not in ("cells", "frontier")} for row in results]}
    out.mkdir(parents=True)
    for name, data in (("details.json", detailed), ("results.json", summary)):
        (out / name).write_text(json.dumps(data, indent=2)+"\n")
    (out / "check_mean_envelope.py").write_bytes(Path(__file__).read_bytes())
    (out / "manifest.json").write_text(json.dumps({"stage": "DEVELOPMENT", "files": [
        {"path": path.name, "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(out.iterdir())]}, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        main(args.out)
    except Exception:
        # Preserve a failed verification without altering any analyzed evidence.
        failure = HERE / "failure.json"
        if not failure.exists():
            failure.write_text(json.dumps({"stage": "DEVELOPMENT", "status": "FAIL",
                "time_utc": datetime.now(timezone.utc).isoformat(),
                "checker_sha256": sha(Path(__file__)), "traceback": traceback.format_exc()},
                indent=2)+"\n")
        raise
