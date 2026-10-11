#!/usr/bin/env python3
"""Independent exact reconciliation of saved gate-architecture diagnostics.

Uses binary raw sums and the pooled raw-sum minimum, then independently checks
the projection cross term. Imports no producer, principal observer, lineage
reader, generator, truth function, scorer or analysis implementation.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import traceback


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
W = HERE.parents[2]
OLD = REPO / "v3/experiments/final_v1"
NEW = REPO / "v3/experiments/final_v1_amended_A1"
AUTHOR = "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction"
SIGNATURES = ((0, 1, 1, 1, 0, 0), (0, 1, 1, 1, 0, 1))
FIELDS = ("irreducible_sum", "monotonicity_penalty_sum", "relaxed_oracle_sum",
          "actual_brier_sum", "excess_over_relaxed_oracle_sum")
CHECKS = Counter()
READS = {}


def require(condition, label, detail=None):
    CHECKS[label] += 1
    if not condition:
        raise AssertionError((label, detail))


def read_bytes(path, expected=None):
    data = path.read_bytes()
    digest = sha256(data).hexdigest()
    require(expected is None or digest == expected, "source_digest", str(path))
    READS[str(path.relative_to(REPO))] = {"bytes": len(data), "sha256": digest}
    return data


def read(path, expected=None):
    return json.loads(read_bytes(path, expected))


def rat(value):
    if isinstance(value, list):
        require(len(value) == 2 and all(type(x) is int for x in value) and value[1] > 0,
                "rational_pair_type")
        return F(value[0], value[1])
    require(type(value) in (int, str), "exact_number_type")
    return F(value)


def encode(value):
    if isinstance(value, F):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def save(path, value):
    with path.open("x") as handle:
        json.dump(encode(value), handle, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")


def key(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def mean(values):
    require(len(values) > 0, "nonempty_mean")
    return sum(values, F(0)) / len(values)


def projected_forecast(weights, signature):
    raw = F(sum(w * a for w, a in zip(weights, signature)), sum(weights))
    return F((raw * 65536).__floor__(), 65536)


def group_stats(rows, q, signature):
    ys = [row["truth"] for row in rows]
    n, k = len(ys), sum(ys)
    mu = F(k, n) if n else None
    # Binary raw second moment is k. This avoids the principal centered formula.
    residual = F(k) - F(k * k, n) if n else F(0)
    actual = n * q * q - 2 * k * q + k
    gap = n * q * q - 2 * k * q + F(k * k, n) if n else F(0)
    require(actual == residual + gap == sum(((q - y) ** 2 for y in ys), F(0)),
            "raw_group_second_moment")
    return {"signature": list(signature), "positions": n, "true_count": k,
            "false_count": n - k, "empirical_mean": mu, "actual_forecast": q,
            "irreducible_sum": residual, "actual_brier_sum": actual,
            "unconstrained_fit_gap_sum": gap, "indices": [row["index"] for row in rows]}


def block_stats(data, weights, block_number, reported):
    require(len(data) == 4 and [r["index"] for r in data] == list(range(4 * block_number, 4 * block_number + 4)),
            "all_four_block_positions", block_number)
    forecasts = [projected_forecast(weights, sig) for sig in SIGNATURES]
    require(0 <= forecasts[0] <= forecasts[1] <= 1, "actual_monotone_probability_pair")
    groups = []
    for sig, q in zip(SIGNATURES, forecasts):
        members = [row for row in data if row["signature"] == sig]
        require(all(row["base"] == row["issued"] == q for row in members), "group_constant_actual_forecasts")
        groups.append(group_stats(members, q, sig))
    require(sum(g["positions"] for g in groups) == 4, "two_signature_partition_complete")
    require(reported["groups"] == encode(groups), "every_reported_group_field", block_number)
    n0, n1 = (g["positions"] for g in groups)
    mu0, mu1 = (g["empirical_mean"] for g in groups)
    k = sum(g["true_count"] for g in groups)
    irreducible = sum((g["irreducible_sum"] for g in groups), F(0))
    reversed_order = bool(n0 and n1 and mu0 > mu1)
    if reversed_order:
        pooled = F(k, 4)
        fitted = [pooled, pooled]
        # A pooled fit is one group with raw second moment k.
        oracle = F(k) - F(k * k, 4)
        delta = mu0 - mu1
        multiplier = F(n0 * n1, 2) * delta
    else:
        fitted = [mu0 if n0 else mu1, mu1 if n1 else mu0]
        oracle, multiplier = irreducible, F(0)
    penalty = oracle - irreducible
    actual = sum((g["actual_brier_sum"] for g in groups), F(0))
    excess = actual - oracle
    distance = sum((g["positions"] * (forecasts[i] - fitted[i]) ** 2 for i, g in enumerate(groups)), F(0))
    cross = (F(n0 * n1, 2) * (mu0 - mu1) * (forecasts[1] - forecasts[0])) if reversed_order else F(0)
    require(0 <= irreducible <= oracle <= 1 and penalty >= 0 and excess >= 0,
            "exact_hindsight_lower_bound")
    require(excess == distance + cross and cross >= 0 and actual == irreducible + penalty + excess,
            "independent_projection_cross_term")
    require(sum((g["true_count"] - 2 * fitted[i] * g["true_count"] + g["positions"] * fitted[i] ** 2
                 for i, g in enumerate(groups)), F(0)) == oracle,
            "fitted_pair_raw_objective")
    require(0 <= fitted[0] <= fitted[1] <= 1 and multiplier >= 0 and
            2 * n0 * (fitted[0] - (mu0 if n0 else fitted[0])) + multiplier == 0 and
            2 * n1 * (fitted[1] - (mu1 if n1 else fitted[1])) - multiplier == 0 and
            multiplier * (fitted[0] - fitted[1]) == 0,
            "independent_order_projection_stationarity")
    expected = {"block": block_number, "groups": groups,
                "order_violation_in_empirical_means": reversed_order,
                "pooled_if_needed": fitted, "KKT_multiplier": multiplier,
                "irreducible_sum": irreducible, "monotonicity_penalty_sum": penalty,
                "relaxed_oracle_sum": oracle, "actual_brier_sum": actual,
                "excess_over_relaxed_oracle_sum": excess}
    require(reported == encode(expected), "every_reported_block_field", block_number)
    return {**expected, "projection_distance_sum": distance, "projection_cross_term_sum": cross}


def main():
    out = HERE / "run_01"
    out.mkdir(exist_ok=False)
    save(out / "start.json", {"signed_by": AUTHOR, "started_at_utc": datetime.now(timezone.utc).isoformat(),
         "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(), "principal_clock_seconds": 0,
         "scope": "independent saved-data gate decomposition and sealed-score reconciliation"})
    try:
        reported = read(W / "gate_architecture_observation_A1/results.json",
                        "553c91374ac015cd65f83325301e79f341d2198efe24adc0e318951bd1543fc1")
        numeric = read(W / "numeric_observation_A1/results.json",
                       "8f7e34aef5060b43bccb2447f87238c3b3c864c5a2e375d317472827567da82f")
        principal_source = read_bytes(W / "gate_architecture_observer.py",
                                      "5224c7a3993863e55d01d1d9845660566c3637a852da6415e9932251d07db9b6")
        principal_derivation = read_bytes(W / "gate_architecture_derivation.md",
                                          "4824a27987bf36369d01d08d11bbeefbe387bc48a59df28f699a6d0c762d9bc2")
        (out / "principal_observer.reviewed.py").write_bytes(principal_source)
        (out / "principal_derivation.reviewed.md").write_bytes(principal_derivation)
        require(reported["status"] == numeric["status"] == "PASS" and
                reported["source_sha256"] == sha256(principal_source).hexdigest() and
                reported["derivation_sha256"] == sha256(principal_derivation).hexdigest() and
                reported["numeric_result_sha256"] == "8f7e34aef5060b43bccb2447f87238c3b3c864c5a2e375d317472827567da82f",
                "principal_completed_source_bindings")
        require(all(reported[name] is False for name in ("causal_selector_claim", "fitted_oracle_deployed",
                    "frozen_endpoint_replacement", "new_population_or_paid_execution")), "declared_scope_flags")
        manifest = read(REPO / "v3/experiments/frozen_v1/manifest.json",
                        "69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70")
        schedule = read(REPO / "v3/experiments/frozen_v1/schedule.json", manifest["schedule_sha256"])
        amendment = read(REPO / "v3/experiments/amendments/P3_10_A1/manifest.json",
                         "36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359")
        composite = read(NEW / "composite_public.json",
                         "8807dd7a3d1ce4c69e81660f3923f7ee879b493d217ecd2dbab18613b5c96b34")
        inputs = read(NEW / "input_reference.json",
                      "ca71a625448cf27009c07a3241880afc6751d1a912965266435c802aee774548")
        evaluation = read(NEW / "stages/evaluation/complete.json")
        require(evaluation["stage"] == "evaluation" and evaluation["expected_units"] == evaluation["completed_units"] == 500
                and len(evaluation["seals"]) == 500 and len(composite["seals"]) == 500,
                "completed_composite_and_evaluation_indices")
        require(evaluation["binding"]["amendment_manifest_sha256"] == reported["amendment_lineage"]["manifest_sha256"] ==
                "36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359" and
                reported["amendment_lineage"]["original_public_stage_complete"] is False and
                reported["amendment_lineage"]["original_failed_prefix_cost"] == "unknown",
                "amended_lineage_scope")
        groups = {g["id"]: g for g in schedule["groups"] if g["arm"] == "broker" and g["recipe"]["family"] == "gate_transfer"}
        units = [u for u in schedule["units"] if u["group_id"] in groups and u["engine"] in ("broker", "mirror")]
        observations = {r["unit_id"]: r for r in reported["records"]}
        nums = {r["unit_id"]: r for r in numeric["per_episode"]}
        numeric_bindings = {r["unit_id"]: r for r in numeric["sealed_source_bindings"]}
        refs = {r["unit_id"]: r for r in composite["seals"]}
        input_refs = {r["unit_id"]: r for r in inputs["seals"]}
        score_refs = {r["unit_id"]: r for r in evaluation["seals"]}
        require(len(groups) == 2 and len(units) == len(observations) == len(reported["records"]) == reported["scheduled_parents"] == 42
                and set(observations) == {u["id"] for u in units}, "exact_42_parent_roster")
        require(len(nums) == len(numeric_bindings) == 126, "pinned_numeric_parent_index")
        tapes = {}
        for gid in groups:
            ref = input_refs[gid]
            require(ref["evidence_class"] == "original_prospective_input", "original_input_class")
            seal = read(REPO / ref["origin_root"] / ref["seal_path"], ref["seal_sha256"])
            require(seal["result_sha256"] == ref["result_sha256"], "input_seal_result_link")
            tape = read(REPO / ref["origin_root"] / ref["result_path"], ref["result_sha256"])
            require(tape["value"]["group_id"] == gid and tape["value"]["horizon"] == 128 and len(tape["value"]["queries"]) == 128,
                    "complete_original_gate_tape")
            tapes[gid] = tape["value"]["queries"]
        records, population_content, populations = [], {}, {}
        all_cross_terms = []
        for unit in units:
            uid, gid = unit["id"], unit["group_id"]
            require(next(s for s in unit["segments"] if s["name"] == "transfer") == {"name": "transfer", "start": 64, "stop": 128},
                    "frozen_transfer_slice", uid)
            ref, bound, nr, rr = refs[uid], numeric_bindings[uid], nums[uid], observations[uid]
            require(ref["origin_root"] == "v3/experiments/final_v1" and ref["evidence_class"] == "original_prospective_unchanged_public_record"
                    and ref["result_sha256"] == bound["public_result_sha256"], "original_public_binding", uid)
            public_seal = read(REPO / ref["origin_root"] / ref["seal_path"], ref["seal_sha256"])
            require(public_seal["result_sha256"] == bound["public_result_sha256"], "public_seal_result_link", uid)
            public = read(REPO / ref["origin_root"] / ref["result_path"], bound["public_result_sha256"])
            score_ref = score_refs["score-" + uid]
            score_seal = read(NEW / score_ref["path"], score_ref["sha256"])
            require(score_seal["result_sha256"] == bound["score_result_sha256"] and
                    score_seal["identity"]["binding"] == evaluation["binding"], "score_seal_result_link", uid)
            scored = read(NEW / "stages/evaluation/units" / ("score-" + uid) / "attempt_01/result.json", bound["score_result_sha256"])
            require(public["unit"] == unit and scored["unit"] == dict(unit, id="score-" + uid, public_unit_id=uid),
                    "exact_scheduled_public_and_score_unit", uid)
            require(scored["value"]["public_result_sha256"] == bound["public_result_sha256"] and
                    public["value"]["input_result_sha256"] == scored["value"]["input_result_sha256"] == bound["input_result_sha256"] == input_refs[gid]["result_sha256"],
                    "full_original_input_public_score_binding", uid)
            episode, score = public["value"]["paid_result"]["episode"], scored["value"]["score"]
            require(episode["status"] == "success" and episode["rounds_closed"] == 128 and score["validity_pass"] is True and score["full_horizon"] is True
                    and nr["status"] == "audited" and rr["status"] == "available", "complete_available_parent", uid)
            trace = episode["trace"]
            nrows = [row for block in nr["blocks"] for row in block["rows"]]
            require(len(trace) == len(nrows) == 128 and len(episode["blocks"]) == len(nr["blocks"]) == 32 and
                    [r["index"] for r in trace] == [r["index"] for r in nrows] == list(range(128)), "complete_episode_chronology", uid)
            full_keys = []
            for row, query in zip(trace, tapes[gid]):
                require(row["claim_key"] == [query["semantics_version"], query["source_version"], query["variables"], query["clauses"]]
                        and row["query_id"] == query["query_id"], "trace_full_key_matches_original_tape", [uid, row["index"]])
                full_keys.append(key(row["claim_key"]))
            require(len(set(full_keys[64:])) == 64 and not set(full_keys[64:]).intersection(full_keys[:64]),
                    "suffix_unique_and_disjoint_from_prefix", uid)
            data = []
            for row, nrow, full_key in zip(trace[64:], nrows[64:], full_keys[64:]):
                y, p, issued = nrow["truth"], rat(row["base_q"]), rat(row["emitted_q"])
                sig = tuple(row["advice"])
                require(type(y) is int and y in (0, 1) and sig in SIGNATURES and 0 <= p <= 1 and 0 <= issued <= 1,
                        "binary_label_advice_probability_domains", [uid, row["index"]])
                require(nrow["first_occurrence"] is True and nrow["prior_known"] is False and row["hard_before"] == "unresolved",
                        "first_occurrence_no_prior_hard_receipt", [uid, row["index"]])
                require((p - y) ** 2 == rat(nrow["base_brier"]) and (issued - y) ** 2 == rat(nrow["live_brier"]),
                        "independent_numeric_truth_brier_link", [uid, row["index"]])
                require(row["block"] == row["index"] // 4, "current_block_identity")
                data.append({"index": row["index"], "truth": y, "base": p, "issued": issued, "signature": sig, "key": full_key})
            common = [{k: row[k] for k in ("index", "truth", "signature", "key")} for row in data]
            require(gid not in population_content or population_content[gid] == common, "same_population_labels_keys_signatures", uid)
            population_content[gid] = common
            require(len(rr["blocks"]) == 16 and rr["planned_suffix_positions"] == rr["closed_suffix_positions"] == 64 and
                    rr["group_id"] == gid and rr["configuration_id"] == unit["configuration_id"], "reported_parent_identity_and_denominator", uid)
            blocks = []
            for j in range(16):
                b = j + 16
                public_block, numeric_block = episode["blocks"][b], nr["blocks"][b]
                weights = public_block["weights_before"]
                require(public_block["block"] == numeric_block["block"] == b and weights == numeric_block["weights_before"] and
                        public_block["weights_after"] == numeric_block["weights_after"] and len(weights) == 6 and
                        all(type(x) is int and x > 0 for x in weights) and sum(weights) == 6 * 65536,
                        "positive_fixed_mass_weights_bound_to_numeric", [uid, b])
                block = block_stats(data[4*j:4*j+4], weights, b, rr["blocks"][j])
                blocks.append(block)
                all_cross_terms.append(block["projection_cross_term_sum"])
            totals = {field: sum((b[field] for b in blocks), F(0)) for field in FIELDS}
            means = {field: value / 64 for field, value in totals.items()}
            require(rr["totals"] == encode(totals) and rr["means"] == encode(means), "every_reported_parent_total_and_mean", uid)
            suffix = score["segments"]["transfer"]
            require(suffix["start"] == 64 and suffix["stop"] == 128 and suffix["full_horizon"] is True and
                    suffix["horizon"] == suffix["rounds_closed"] == suffix["forecast_readouts"] == 64 and
                    rat(suffix["base_issued_brier_sum"]) == rat(suffix["issued_brier_sum"]) == totals["actual_brier_sum"] and
                    rat(suffix["base_brier_mean"]) == rat(suffix["brier_mean"]) == means["actual_brier_sum"],
                    "all_sealed_suffix_brier_sums_and_means", uid)
            population = {"group_id": gid, "positions": 64, "blocks": 16, "true_count": sum(row["truth"] for row in data),
                "order_violating_blocks": sum(b["order_violation_in_empirical_means"] for b in blocks),
                "mixed_label_signature_groups": sum(g["true_count"] > 0 and g["false_count"] > 0 for b in blocks for g in b["groups"]),
                "present_signature_groups": sum(g["positions"] > 0 for b in blocks for g in b["groups"]),
                "absent_signature_groups": sum(g["positions"] == 0 for b in blocks for g in b["groups"]),
                "oracle_means": {field: means[field] for field in FIELDS[:3]},
                "block_profiles": [{"block": b["block"], "counts": [[g["positions"], g["true_count"]] for g in b["groups"]],
                    **{field: b[field] for field in FIELDS[:3]}} for b in blocks]}
            require(gid not in populations or populations[gid] == population, "population_oracle_invariant_across_policy_seed_slots", uid)
            populations[gid] = population
            records.append({"unit_id": uid, "group_id": gid, "configuration_id": unit["configuration_id"], "seed": unit["seed"],
                "totals": totals, "means": means, "projection_cross_term_sum": sum((b["projection_cross_term_sum"] for b in blocks), F(0)),
                "projection_distance_sum": sum((b["projection_distance_sum"] for b in blocks), F(0)),
                "block_reconstructions": blocks})
        reported_populations = {p["group_id"]: p for p in reported["populations"]}
        require(len(reported["populations"]) == len(reported_populations) == 2 and reported_populations == encode(populations)
                and reported["unique_population_count"] == 2 and reported["unique_population_blocks"] == 32,
                "all_distinct_population_fields")
        by_config = defaultdict(list)
        for record in records:
            by_config[record["configuration_id"]].append(record)
        reported_aggregates = {r["configuration_id"]: r for r in reported["aggregates"]}
        require(len(by_config) == len(reported["aggregates"]) == len(reported_aggregates) == 7 and set(by_config) == set(reported_aggregates),
                "all_seven_configurations")
        aggregates = []
        for config, rows in sorted(by_config.items()):
            cells = defaultdict(list)
            for row in rows:
                cells[row["group_id"]].append(row)
            require(len(rows) == 6 and len(cells) == 2 and all(len(rs) == 3 and {r["seed"] for r in rs} == {3091001,3091002,3091003} for rs in cells.values()),
                    "exact_seed_then_population_hierarchy", config)
            means = {field: mean([mean([r["means"][field] for r in rs]) for rs in cells.values()]) for field in FIELDS}
            rr = reported_aggregates[config]
            require(rr["means"] == encode(means) and rr["planned_parents"] == rr["available_parents"] == 6 and
                    len(rr["unit_ids"]) == 6 and set(rr["unit_ids"]) == {r["unit_id"] for r in rows}, "all_reported_hierarchical_aggregates", config)
            require(means["irreducible_sum"] == F(197, 1536) and means["monotonicity_penalty_sum"] == F(11, 512)
                    and means["relaxed_oracle_sum"] == F(115, 768) and means["actual_brier_sum"] == sum((means[f] for f in (FIELDS[0], FIELDS[1], FIELDS[4])), F(0)),
                    "advertised_common_terms_and_exact_sum", config)
            aggregates.append({"configuration_id": config, "parents": 6, "means": means,
                "projection_cross_term_mean": mean([mean([r["projection_cross_term_sum"] / 64 for r in rs]) for rs in cells.values()]),
                "projection_distance_mean": mean([mean([r["projection_distance_sum"] / 64 for r in rs]) for rs in cells.values()])})
        require(sum(p["order_violating_blocks"] for p in populations.values()) == 8 and
                sum(p["mixed_label_signature_groups"] for p in populations.values()) == 26, "advertised_unique_structural_counts")
        require(reported["checks_total"] == sum(reported["checks_by_kind"].values()) == 15752, "reported_check_census_arithmetic")
        result = {"schema": "p310.independent-gate-architecture-review.v1", "status": "PASS", "signed_by": AUTHOR,
            "completed_at_utc": datetime.now(timezone.utc).isoformat(), "principal_clock_seconds": 0,
            "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(), "parents_checked": 42,
            "per_parent_suffix_positions": 64, "forecast_truth_pairs_checked": 2688, "block_instances_checked": 672,
            "group_instances_checked": 1344, "sealed_suffix_scores_checked": 42, "configurations_checked": 7,
            "distinct_populations": 2, "distinct_population_blocks": 32, "distinct_label_positions": 128,
            "projection_cross_term_positive_instances": sum(x > 0 for x in all_cross_terms),
            "checks_by_kind": dict(CHECKS), "checks_total": sum(CHECKS.values()), "records": records,
            "populations": list(populations.values()), "aggregates": aggregates, "read_bindings": READS,
            "GA01_status": "closed_by_source_clarification_and_independent_full_key_checks",
            "scope": "Exact saved-data reconstruction under the relaxed block-specific monotone two-signature class; no new truth evaluator, paid execution, deployed comparator, causal claim, endpoint replacement, gate change or principal clock credit."}
        save(out / "results.json", result)
        print(json.dumps({k: v for k, v in result.items() if k not in ("records", "populations", "read_bindings")}, default=encode, sort_keys=True))
    except BaseException as error:
        save(out / "failure.json", {"status": "REVIEW_OBSERVER_FAILURE", "signed_by": AUTHOR,
            "error_type": type(error).__name__, "error": str(error), "traceback": traceback.format_exc(),
            "checks_by_kind": dict(CHECKS), "read_bindings": READS, "principal_clock_seconds": 0,
            "official_files_modified": False})
        raise


if __name__ == "__main__":
    main()
