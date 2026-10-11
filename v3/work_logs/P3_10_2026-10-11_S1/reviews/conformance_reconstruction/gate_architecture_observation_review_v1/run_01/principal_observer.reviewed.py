"""Post-outcome restricted-architecture decomposition of saved gate forecasts.

ChatGPT (GPT-6 Astra Pro), principal /root, 2026-10-11.
No paid run, truth evaluator, generator, policy change or frozen-module import.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import os
import time
import traceback

from amended_lineage_reader import Lineage

HERE = Path(__file__).resolve().parent
COUNTS = Counter()
SIGNATURES = [(0, 1, 1, 1, 0, 0), (0, 1, 1, 1, 0, 1)]


def stamp():
    return {"utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns(),
            "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(value, name, detail=None):
    COUNTS[name] += 1
    if not value:
        raise AssertionError(f"{name}: {detail}")


def rat(value):
    return F(*value) if isinstance(value, (tuple, list)) else F(value)


def encode(value):
    if isinstance(value, F):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(x) for x in value]
    return value


def save(path, value):
    with path.open("x") as stream:
        json.dump(encode(value), stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def claim_key(row):
    return json.dumps(row["claim_key"], sort_keys=True, separators=(",", ":"))


def analyze_block(rows, truth_rows, weight_record):
    require(len(rows) == len(truth_rows) == 4, "four_position_block")
    require(len({r["block"] for r in rows}) == 1 and rows[0]["block"] == weight_record["block"],
            "same_saved_block")
    weights = weight_record["weights_before"]
    require(len(weights) == 6 and all(type(w) is int and w > 0 for w in weights)
            and sum(weights) == 6 * 65536, "positive_fixed_mass_weights")
    forecasts = [F(sum(w * a for w, a in zip(weights, sig)) // 6, 65536) for sig in SIGNATURES]
    require(0 <= forecasts[0] <= forecasts[1] <= 1, "mixture_implies_weak_order")
    groups = []
    for group_index, signature in enumerate(SIGNATURES):
        members = [(row, truth) for row, truth in zip(rows, truth_rows) if tuple(row["advice"]) == signature]
        n = len(members)
        for row, truth in members:
            require(row["index"] == truth["index"] and truth["first_occurrence"] is True
                    and truth["prior_known"] is False and row["hard_before"] == "unresolved",
                    "suffix_is_first_key_without_hard_override", row["index"])
            require(rat(row["base_q"]) == rat(row["emitted_q"]) == forecasts[group_index],
                    "within_block_signature_forecast", row["index"])
            require((forecasts[group_index] - truth["truth"]) ** 2 == rat(truth["base_brier"])
                    == rat(truth["live_brier"]), "saved_numeric_row_agreement")
        true_count = sum(t["truth"] for _, t in members)
        mu = F(true_count, n) if n else None
        residual = n * mu * (1 - mu) if n else F(0)
        actual = sum(((forecasts[group_index] - t["truth"]) ** 2 for _, t in members), F(0))
        fit_gap = n * (forecasts[group_index] - mu) ** 2 if n else F(0)
        require(actual == residual + fit_gap, "within_group_square_decomposition")
        groups.append({"signature": signature, "positions": n, "true_count": true_count,
                       "false_count": n - true_count, "empirical_mean": mu,
                       "actual_forecast": forecasts[group_index], "irreducible_sum": residual,
                       "actual_brier_sum": actual, "unconstrained_fit_gap_sum": fit_gap,
                       "indices": [r["index"] for r, _ in members]})
    require(sum(g["positions"] for g in groups) == 4, "only_two_gate_advice_signatures")
    n0, n1 = [g["positions"] for g in groups]
    mu0, mu1 = [g["empirical_mean"] for g in groups]
    violated = n0 > 0 and n1 > 0 and mu0 > mu1
    if violated:
        pooled = F(sum(g["true_count"] for g in groups), 4)
        fitted = [pooled, pooled]
        penalty = F(n0 * n1, 4) * (mu0 - mu1) ** 2
        multiplier = 2 * n0 * (mu0 - pooled)
    else:
        fitted = [mu0 if n0 else mu1, mu1 if n1 else mu0]
        penalty, multiplier = F(0), F(0)
    require(0 <= fitted[0] <= fitted[1] <= 1 and multiplier >= 0, "oracle_primal_dual_feasibility")
    require(2 * n0 * (fitted[0] - (mu0 if n0 else fitted[0])) + multiplier == 0
            and 2 * n1 * (fitted[1] - (mu1 if n1 else fitted[1])) - multiplier == 0
            and multiplier * (fitted[0] - fitted[1]) == 0,
            "exact_convex_KKT_certificate")
    irreducible = sum((g["irreducible_sum"] for g in groups), F(0))
    actual = sum((g["actual_brier_sum"] for g in groups), F(0))
    oracle = sum((g["irreducible_sum"] + g["positions"] * (fitted[i] - g["empirical_mean"]) ** 2
                  for i, g in enumerate(groups) if g["positions"]), F(0))
    require(oracle == irreducible + penalty, "closed_form_monotonicity_penalty")
    excess = actual - oracle
    require(excess >= 0 and actual == irreducible + penalty + excess, "three_part_brier_decomposition")
    return {"block": rows[0]["block"], "groups": groups, "order_violation_in_empirical_means": bool(violated),
            "pooled_if_needed": fitted, "KKT_multiplier": multiplier,
            "irreducible_sum": irreducible, "monotonicity_penalty_sum": penalty,
            "relaxed_oracle_sum": oracle, "actual_brier_sum": actual,
            "excess_over_relaxed_oracle_sum": excess}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--numeric", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    start = stamp()
    try:
        lineage = Lineage()
        numeric_path = Path(args.numeric)
        require(digest(numeric_path) == "8f7e34aef5060b43bccb2447f87238c3b3c864c5a2e375d317472827567da82f",
                "pinned_independent_numeric_result")
        numeric = json.loads(numeric_path.read_text())
        require(numeric["status"] == "PASS", "independent_numeric_pass")
        numeric_rows = {r["unit_id"]: [x for block in r["blocks"] for x in block["rows"]]
                        for r in numeric["per_episode"]}
        gate_groups = {g["id"] for g in lineage.schedule["groups"]
                       if g["arm"] == "broker" and g["recipe"]["family"] == "gate_transfer"}
        require(len(gate_groups) == 2, "two_prespecified_gate_populations")
        records, populations = [], {}
        fields = ("irreducible_sum", "monotonicity_penalty_sum", "relaxed_oracle_sum",
                  "actual_brier_sum", "excess_over_relaxed_oracle_sum")
        for unit in lineage.schedule["units"]:
            if unit["group_id"] not in gate_groups or unit["engine"] not in ("broker", "mirror"):
                continue
            result, _ = lineage.record("public", unit["id"])
            episode = result["value"]["paid_result"]["episode"]
            require(episode["status"] == "success" and episode["rounds_closed"] == 128,
                    "complete_gate_parent", unit["id"])
            require([s for s in unit["segments"] if s["name"] == "transfer"] ==
                    [{"name": "transfer", "start": 64, "stop": 128}], "prespecified_transfer_slice")
            rows, truths = episode["trace"], numeric_rows[unit["id"]]
            require(len(rows) == len(truths) == 128 and [r["index"] for r in truths] == list(range(128)),
                    "full_numeric_horizon")
            suffix_keys, prefix_keys = {claim_key(r) for r in rows[64:]}, {claim_key(r) for r in rows[:64]}
            require(len(suffix_keys) == 64 and not suffix_keys.intersection(prefix_keys), "unique_new_full_keys")
            blocks = [analyze_block(rows[i:i + 4], truths[i:i + 4], episode["blocks"][i // 4])
                      for i in range(64, 128, 4)]
            totals = {field: sum((b[field] for b in blocks), F(0)) for field in fields}
            population = {"group_id": unit["group_id"], "positions": 64, "blocks": 16,
                          "true_count": sum(r["truth"] for r in truths[64:]),
                          "order_violating_blocks": sum(b["order_violation_in_empirical_means"] for b in blocks),
                          "mixed_label_signature_groups": sum(g["true_count"] > 0 and g["false_count"] > 0
                                                               for b in blocks for g in b["groups"]),
                          "present_signature_groups": sum(g["positions"] > 0 for b in blocks for g in b["groups"]),
                          "absent_signature_groups": sum(g["positions"] == 0 for b in blocks for g in b["groups"]),
                          "oracle_means": {field: totals[field] / 64 for field in fields[:3]},
                          "block_profiles": [{"block": b["block"], "counts": [[g["positions"], g["true_count"]] for g in b["groups"]],
                                              "irreducible_sum": b["irreducible_sum"], "monotonicity_penalty_sum": b["monotonicity_penalty_sum"],
                                              "relaxed_oracle_sum": b["relaxed_oracle_sum"]} for b in blocks]}
            if unit["group_id"] in populations:
                require(populations[unit["group_id"]] == population, "same_oracle_population_across_policies")
            else:
                populations[unit["group_id"]] = population
            scored, _ = lineage.record("evaluation", "score-" + unit["id"])
            score = scored["value"]["score"]["segments"]["transfer"]
            require(score["full_horizon"] and score["horizon"] == score["rounds_closed"] == 64
                    and rat(score["base_issued_brier_sum"]) == rat(score["issued_brier_sum"]) == totals["actual_brier_sum"],
                    "sealed_suffix_brier_agreement", unit["id"])
            records.append({"unit_id": unit["id"], "group_id": unit["group_id"],
                            "configuration_id": unit["configuration_id"], "status": "available",
                            "planned_suffix_positions": 64, "closed_suffix_positions": 64,
                            "blocks": blocks, "totals": totals, "means": {k: v / 64 for k, v in totals.items()}})
        require(len(records) == 42 and len(populations) == 2, "complete_gate_numerical_roster")
        grouped = defaultdict(list)
        for record in records:
            grouped[record["configuration_id"]].append(record)
        aggregates = []
        for configuration, rows in sorted(grouped.items()):
            require(len(rows) == 6, "six_prescribed_policy_population_slots")
            values = {}
            for field in fields:
                cells = defaultdict(list)
                for row in rows:
                    cells[row["group_id"]].append(row["means"][field])
                require(len(cells) == 2 and all(len(v) == 3 for v in cells.values()), "frozen_seed_population_hierarchy")
                values[field] = sum((sum(v, F(0)) / 3 for v in cells.values()), F(0)) / 2
            aggregates.append({"configuration_id": configuration, "planned_parents": 6, "available_parents": 6,
                               "means": values, "weighting": "equal three seed slots within population, then equal two populations",
                               "unit_ids": [r["unit_id"] for r in rows]})
        final = {"schema": "value_logic.p310.gate_architecture_decomposition.v1", "status": "PASS",
                 "contributor": "ChatGPT (GPT-6 Astra Pro)", "start": start, "end": stamp(),
                 "source_sha256": digest(Path(__file__)), "derivation_sha256": digest(HERE / "gate_architecture_derivation.md"),
                 "numeric_result_sha256": digest(numeric_path), "amendment_lineage": lineage.receipt,
                 "research_class": "post-outcome saved-data interpretation", "fitted_oracle_deployed": False,
                 "frozen_endpoint_replacement": False, "causal_selector_claim": False,
                 "new_population_or_paid_execution": False, "scheduled_parents": 42, "records": records,
                 "unique_population_count": 2, "unique_population_blocks": 32, "populations": list(populations.values()),
                 "aggregates": aggregates, "checks_by_kind": dict(COUNTS), "checks_total": sum(COUNTS.values()),
                 "scope": "Lower bound only for relaxed block-specific monotone two-signature forecasts; all labels used retrospectively. Not an online attainable comparator or lower bound for arbitrary CNF reasoning."}
        save(output / "results.json", final)
        print(json.dumps({"status": "PASS", "parents": len(records), "population_blocks": 32,
                          "checks_total": sum(COUNTS.values()), "results_sha256": digest(output / "results.json")}, indent=2))
    except BaseException as error:
        save(output / "failure.json", {"status": "OBSERVER_FAILURE", "start": start, "end": stamp(),
             "source_sha256": digest(Path(__file__)), "error_type": type(error).__name__, "error": str(error),
             "traceback": traceback.format_exc(), "checks_completed": dict(COUNTS), "scientific_stage_failure": False})
        raise


if __name__ == "__main__":
    main()
