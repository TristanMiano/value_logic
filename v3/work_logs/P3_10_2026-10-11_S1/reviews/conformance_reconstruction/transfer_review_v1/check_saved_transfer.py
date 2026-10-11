#!/usr/bin/env python3
"""Independent read-only check of post-outcome transfer moment interpretation.

Contributor: ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction.
Uses raw first/second moments rather than the principal centered-moment routine.
No frozen code or observer is imported or executed; no truth function is called.
Every parent and scheduled slice is retained and reconciled to sealed scores.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import traceback

HERE = Path(__file__).resolve().parent
W = HERE.parents[2]
REPO = HERE.parents[5]
READS = {}
CHECKS = Counter()
AUTHOR = "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path, expected=None):
    data = path.read_bytes()
    got = sha(data)
    if expected is not None:
        assert got == expected, str(path)
    READS[path.relative_to(REPO).as_posix()] = {"bytes": len(data), "sha256": got}
    return json.loads(data)


def require(condition, name, detail=None):
    CHECKS[name] += 1
    if not condition:
        raise AssertionError((name, detail))


def rat(x):
    return F(*x) if isinstance(x, list) else F(x)


def encode(value):
    if isinstance(value, F):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def save(path, value):
    with path.open("x") as file:
        json.dump(encode(value), file, indent=2, sort_keys=True, allow_nan=False)
        file.write("\n")


def mean(xs):
    assert xs
    return sum(xs, F(0)) / len(xs)


def raw_moments(ps, ys):
    require(len(ps) == len(ys) > 0, "nonempty_equal_moment_denominators")
    n = len(ps)
    sy, sp, sp2, spy = sum(ys), sum(ps, F(0)), sum((p*p for p in ps), F(0)), sum((p*y for p, y in zip(ps, ys)), F(0))
    mp, my = sp/n, F(sy, n)
    vp, cov = sp2/n-mp*mp, spy/n-mp*my
    brier = (sp2-2*spy+sy)/n
    result = {"mean_forecast": mp, "mean_truth": my, "label_variance": my*(1-my),
              "squared_mean_bias": (mp-my)**2, "forecast_variance": vp,
              "truth_covariance": cov, "negative_twice_covariance": -2*cov,
              "brier_mean": brier}
    require(result["label_variance"] + result["squared_mean_bias"] + vp - 2*cov == brier,
            "raw_moment_identity")
    return result


def hmean(rows, get):
    groups = defaultdict(list)
    for row in rows:
        groups[row["group_id"]].append(get(row))
    return mean([mean(values) for values in groups.values()])


def main():
    out = HERE / "run_01"
    out.mkdir(exist_ok=False)
    save(out / "start.json", {"contributor": AUTHOR, "started_utc": datetime.now(timezone.utc).isoformat(),
         "source_sha256": sha(Path(__file__).read_bytes()), "principal_clock_credit_seconds": 0})
    try:
        numeric = read(W / "numeric_observation_A1/results.json", "8f7e34aef5060b43bccb2447f87238c3b3c864c5a2e375d317472827567da82f")
        reported = read(W / "transfer_failure_observation_A1/results.json", "a8965c3529347dfb78a342ad83a70f08185459a10a2f9fad50fa6f4cb869895d")
        manifest = read(REPO / "v3/experiments/frozen_v1/manifest.json", "69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70")
        schedule = read(REPO / "v3/experiments/frozen_v1/schedule.json", manifest["schedule_sha256"])
        composite = read(REPO / "v3/experiments/final_v1_amended_A1/composite_public.json", reported["amendment_lineage"]["composite_public_sha256"])
        require(reported["numeric_result_sha256"] == sha((W / "numeric_observation_A1/results.json").read_bytes()), "numeric_binding")
        require(reported["source_sha256"] == sha((W / "transfer_failure_observer.py").read_bytes()) == "ba4193ff74091beca59bae51a0527018521d4d0c509c04eb6ab1d549d4460cc9", "principal_source_binding")
        require(reported["derivation_sha256"] == sha((W / "transfer_failure_derivation.md").read_bytes()) == "c5a5c19a085603ee1a986d1c3036fb842d4a1dd9bbb6b4a0ba44d80dbb21db32", "principal_derivation_binding")
        require(numeric["status"] == reported["status"] == "PASS", "completed_observer_sources")
        units = [u for u in schedule["units"] if u["arm"] == "broker" and u["engine"] in ("broker", "mirror")]
        groups = {g["id"]: g for g in schedule["groups"] if g["arm"] == "broker"}
        bindings = {r["unit_id"]: r for r in numeric["sealed_source_bindings"]}
        nums = {r["unit_id"]: r for r in numeric["per_episode"]}
        parents = {r["unit_id"]: r for r in reported["parents"]}
        refs = {r["unit_id"]: r for r in composite["seals"]}
        observed_rows = {(r["unit_id"], r["slice"]): r for r in reported["per_episode_slices"]}
        expected_ids = [u["id"] for u in units]
        require(len(units) == len(parents) == len(nums) == len(bindings) == 126 and set(expected_ids) == set(parents) == set(nums) == set(bindings), "full_126_parent_roster")
        require(len(reported["parents"]) == 126 and len(reported["per_episode_slices"]) == len(observed_rows) == 336, "no_duplicate_report_rows")
        records, population_data, boundaries = [], {}, []
        for unit in units:
            uid, gid = unit["id"], unit["group_id"]
            group, nr, parent, bound = groups[gid], nums[uid], parents[uid], bindings[uid]
            require(nr["status"] == parent["status"] == "audited", "actual_parent_available", uid)
            ref = refs[uid]
            require(ref["evidence_class"] == "original_prospective_unchanged_public_record" and ref["result_sha256"] == bound["public_result_sha256"], "original_public_record_link", uid)
            public = read(REPO / ref["origin_root"] / ref["result_path"], bound["public_result_sha256"])
            score_path = REPO / "v3/experiments/final_v1_amended_A1/stages/evaluation/units" / ("score-" + uid) / "attempt_01/result.json"
            scored = read(score_path, bound["score_result_sha256"])
            score = scored["value"]["score"]
            require(public["unit"] == unit and scored["unit"] == dict(unit, id="score-" + uid, public_unit_id=uid), "scheduled_unit_identity", uid)
            require(scored["value"]["public_result_sha256"] == bound["public_result_sha256"] and
                    scored["value"]["input_result_sha256"] == public["value"]["input_result_sha256"] == bound["input_result_sha256"], "score_public_input_links", uid)
            require(score["validity_pass"] is True and score["full_horizon"] is True, "complete_scored_parent", uid)
            trace = public["value"]["paid_result"]["episode"]["trace"]
            nrows = [r for block in nr["blocks"] for r in block["rows"]]
            horizon = group["recipe"]["horizon"]
            require(len(trace) == len(nrows) == horizon and [r["index"] for r in trace] == [r["index"] for r in nrows] == list(range(horizon)), "full_chronology", uid)
            data, seen = [], set()
            for row, nrow in zip(trace, nrows):
                y, p = nrow["truth"], rat(row["base_q"])
                advice = row["advice"]
                require(type(y) is int and y in (0, 1) and 0 <= p <= 1 and len(advice) == 6 and all(type(x) is int and x in (0, 1) for x in advice), "row_domains", uid)
                q = F(sum(advice), 6)
                require((p-y)**2 == rat(nrow["base_brier"]) and (q-y)**2 == rat(nrow["frozen_equal_brier"]), "exact_numeric_row_brier_agreement", [uid, row["index"]])
                key = json.dumps(row["claim_key"], sort_keys=True, separators=(",", ":"))
                first = key not in seen
                seen.add(key)
                require(nrow["first_occurrence"] is first and nrow["selected"] == row["selected"], "first_and_selected_agreement", uid)
                data.append({"index": row["index"], "base": p, "equal": q, "truth": y,
                             "signature": tuple(advice), "key": key, "first": first, "selected": row["selected"]})
            shared = [{k: r[k] for k in ("index", "truth", "signature", "key", "first")} for r in data]
            require(gid not in population_data or population_data[gid] == shared, "shared_population_content", uid)
            population_data[gid] = shared
            selections = {s["name"]: [r for r in data if s["start"] <= r["index"] < s["stop"]] for s in unit["segments"]}
            selections["first_occurrence"] = [r for r in data if r["first"]]
            for name, rows in selections.items():
                result = observed_rows[(uid, name)]
                ys = [r["truth"] for r in rows]
                base = raw_moments([r["base"] for r in rows], ys)
                equal = raw_moments([r["equal"] for r in rows], ys)
                pieces = {k: equal[k]-base[k] for k in ("squared_mean_bias", "forecast_variance", "negative_twice_covariance")}
                delta = equal["brier_mean"]-base["brier_mean"]
                expected = {"base_moments": base, "equal_moments": equal, "a2_difference": delta,
                            "a2_contributions": pieces, "denominator": len(rows), "true_count": sum(ys)}
                require(all(result[k] == encode(v) for k, v in expected.items()), "all_reported_slice_moments", [uid, name])
                private = score["first_occurrence"] if name == "first_occurrence" else score["segments"][name]
                require(private["full_horizon"] is True and private["horizon"] == len(rows) and
                        rat(private["base_brier_mean"]) == base["brier_mean"] and rat(private["uniform_brier_mean"]) == equal["brier_mean"], "all_sealed_score_slice_briers", [uid, name])
                if name == "first_occurrence":
                    require(private["indices"] == [r["index"] for r in rows], "private_first_indices", uid)
                selected = [r for r in rows if r["selected"]]
                require(result["selected_count"] == len(selected) and result["selected_true_count"] == sum(r["truth"] for r in selected) and
                        result["selected_true_fraction"] == encode(F(sum(r["truth"] for r in selected), len(selected)) if selected else None), "selected_feedback_summary", [uid, name])
                records.append({"unit_id": uid, "group_id": gid, "configuration_id": unit["configuration_id"],
                                "family": group["recipe"]["family"], "slice": name, **expected,
                                "selected_count": len(selected), "selected_true_count": sum(r["truth"] for r in selected)})
            require(len(parent["block_profiles"]) == len(nr["blocks"]), "complete_block_profiles", uid)
            for profile, block in zip(parent["block_profiles"], nr["blocks"]):
                i = block["block"]
                rows = data[4*i:4*i+4]
                chosen = [r for r in rows if r["selected"]]
                require(len(chosen) == 1 and profile["block"] == i and profile["weights_before"] == block["weights_before"] and
                        profile["weights_after"] == block["weights_after"] and profile["mean_base"] == encode(mean([r["base"] for r in rows])) and
                        profile["true_count"] == sum(r["truth"] for r in rows) and profile["selected_truth"] == chosen[0]["truth"], "block_profile_values", [uid, i])
            if group["recipe"]["family"] == "gate_transfer":
                before, final = nr["blocks"][16]["weights_before"], nr["blocks"][-1]["weights_after"]
                require(before == nr["blocks"][15]["weights_after"], "unreset_transfer_boundary", uid)
                boundaries.append({"unit_id": uid, "group_id": gid, "configuration_id": unit["configuration_id"],
                                   "weights_at_transfer": [F(x, sum(before)) for x in before],
                                   "weights_at_end": [F(x, sum(final)) for x in final]})
        require(set(observed_rows) == {(r["unit_id"], r["slice"]) for r in records} and len(records) == 336, "all_prespecified_slices")

        release = read(HERE.parent / "completion_release_A1.json")
        analysis_dir = REPO / "v3/experiments/final_v1_amended_A1/stages/analysis/units/all-frozen-endpoints/attempt_01"
        seal = read(analysis_dir / "seal.json", release["analysis_seal_sha256"])
        analysis = read(analysis_dir / "result.json", seal["result_sha256"])
        primary = {(r["family"], r["configuration_id"]): r for r in analysis["value"]["broker"]["configuration_means"]}
        aggregates = []
        for reported_aggregate in reported["aggregates"]:
            family, conf, name = (reported_aggregate[k] for k in ("family", "configuration_id", "slice"))
            rows = [r for r in records if (r["family"], r["configuration_id"], r["slice"]) == (family, conf, name)]
            require(len(rows) == reported_aggregate["planned_episodes"] == reported_aggregate["available_episodes"] == 6 and
                    reported_aggregate["complete_parent_denominator"] is True and not reported_aggregate["missing_unit_ids"], "full_aggregate_denominator", [family, conf, name])
            by_group = Counter(r["group_id"] for r in rows)
            require(len(by_group) == 2 and set(by_group.values()) == {3}, "two_populations_three_seed_slots", [family, conf, name])
            delta = hmean(rows, lambda r: r["a2_difference"])
            pieces = {k: hmean(rows, lambda r: r["a2_contributions"][k]) for k in reported_aggregate["a2_contributions"]}
            require(encode(delta) == reported_aggregate["a2_difference"] and encode(pieces) == reported_aggregate["a2_contributions"] and sum(pieces.values(), F(0)) == delta, "all_hierarchical_differences", [family, conf, name])
            for key, value in reported_aggregate["base_moments"].items():
                require(encode(hmean(rows, lambda r: r["base_moments"][key])) == value, "all_hierarchical_base_moments", [family, conf, name, key])
            frozen = next(r for r in primary[(family, conf)]["prespecified_slices"] if r["slice"] == name)
            require(frozen["complete_primary_denominator"] is True and frozen["planned_episodes"] == 6 and rat(frozen["uniform_minus_base_brier"]) == delta, "frozen_primary_A2_agreement", [family, conf, name])
            aggregates.append({"family": family, "configuration_id": conf, "slice": name,
                               "a2_difference": delta, "a2_contributions": pieces,
                               "base_moments": {k: hmean(rows, lambda r: r["base_moments"][k]) for k in rows[0]["base_moments"]},
                               "equal_moments": {k: hmean(rows, lambda r: r["equal_moments"][k]) for k in rows[0]["equal_moments"]}})
        require(len(aggregates) == len({(r["family"], r["configuration_id"], r["slice"]) for r in records}) == 56, "all_56_aggregate_cells")

        signatures = {(r["group_id"], r["slice"]): r for r in reported["population_advice_signatures"]}
        expected_signature_ids = set()
        for gid, data in population_data.items():
            selections = {"whole": data, "first_occurrence": [r for r in data if r["first"]]}
            split = groups[gid]["recipe"]["prefix_length"]
            if split:
                selections.update(prefix=data[:split], transfer=data[split:])
            for name, rows in selections.items():
                expected_signature_ids.add((gid, name))
                rec = signatures[(gid, name)]
                bins = defaultdict(list)
                for row in rows:
                    bins[row["signature"]].append(row)
                strata = []
                for sig, vals in sorted(bins.items()):
                    n, k = len(vals), sum(r["truth"] for r in vals)
                    # Direct least-squares minimum: sum(y^2) - sum(y)^2/n.
                    minimum = F(k) - F(k*k, n)
                    strata.append({"advice_signature": list(sig), "positions": n, "true_count": k, "false_count": n-k,
                                   "empirical_true_fraction": F(k, n), "unique_full_keys": len({r["key"] for r in vals}),
                                   "retrospective_best_constant_brier_sum": minimum})
                require(rec["signature_strata"] == encode(strata) and rec["positions"] == len(rows) and rec["true_count"] == sum(r["truth"] for r in rows) and
                        rec["unique_full_keys"] == len({r["key"] for r in rows}) and rec["retrospective_signature_fit_brier_mean"] == encode(sum((r["retrospective_best_constant_brier_sum"] for r in strata), F(0))/len(rows)) and
                        rec["fitted_oracle_is_deployed_comparator"] is False, "all_signature_diagnostics", [gid, name])
        require(set(signatures) == expected_signature_ids and len(signatures) == len(reported["population_advice_signatures"]) == 16, "all_signature_slices")
        result = {"schema": "value_logic.p310.independent_transfer_interpretation_review.v1", "status": "PASS",
                  "contributor": AUTHOR, "finished_utc": datetime.now(timezone.utc).isoformat(),
                  "principal_clock_credit_seconds": 0, "source_sha256": sha(Path(__file__).read_bytes()),
                  "parents_checked": 126, "parent_slices_checked": 336, "moment_records_checked": 672,
                  "frozen_primary_aggregate_cells_checked": 56, "population_signature_slices_checked": 16,
                  "checks_by_kind": dict(CHECKS), "aggregates": aggregates, "gate_boundaries": boundaries,
                  "read_bindings": READS,
                  "scope": "Independent saved-data reconciliation; no paid rerun, truth call, causal identification, deployed fitted comparator, or primary endpoint change."}
        save(out / "results.json", result)
        print(json.dumps({k: v for k, v in result.items() if k not in ("aggregates", "gate_boundaries", "read_bindings")}, sort_keys=True))
    except BaseException as error:
        save(out / "failure.json", {"status": "REVIEW_OBSERVER_FAILURE", "type": type(error).__name__,
             "message": str(error), "traceback": traceback.format_exc(), "read_bindings": READS,
             "principal_clock_credit_seconds": 0, "official_files_modified": False})
        raise


if __name__ == "__main__":
    main()
