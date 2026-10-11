#!/usr/bin/env python3
"""Exact arithmetic on saved summary/price JSON; no scientific imports or runs."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time
import traceback

ROOT = Path("/workspace/scratch/095cdac579b7/value_logic")
W = ROOT / "v3/work_logs/P3_10_2026-10-11_S1"
OWN = W / "reviews/certificate_reconstruction/forecast_action_price_review_v1"
OUT = OWN / "independent_observation_v1"
REVIEWER = "ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction"
PIN = "94f41a247f9fade238028608a221fac39d0a8be56af857de5a4c0c1d8640c3ae"
RESULT_PIN = "0fa171400460af35bfe2839c3493a30fdfab81811357c08838ec92eb4257a751"
checks = []


def eq(label, actual, expected):
    checks.append({"id": label, "pass": actual == expected})
    if actual != expected:
        raise AssertionError(f"{label}: {actual!r} != {expected!r}")


def q(pair):
    if not (isinstance(pair, list) and len(pair) == 2
            and all(type(x) is int for x in pair) and pair[1] > 0):
        raise ValueError("Expected an exact rational pair")
    return Q(*pair)


def encode(value):
    if isinstance(value, Q):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def save(path, value):
    with path.open("x", encoding="utf-8") as f:
        json.dump(encode(value), f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vector(row):
    return {"W": q(row["means"]["action_loss_mean"]),
            "C": q(row["mean_cold_units_per_request"]),
            "B": q(row["means"]["brier_mean"])}


def decode_vector(v):
    return {k: q(v[k]) for k in ["W", "C", "B"]}


def vertices(rows):
    """Eliminate x in each boundary pair, then substitute and check every row."""
    found, nonsingular = {}, 0
    for (_, a, b, d), (_, aa, bb, dd) in combinations(rows, 2):
        det = a * bb - aa * b
        if not det:
            continue
        nonsingular += 1
        y = (a * dd - aa * d) / det
        x = (d - b*y) / a if a else (dd - bb*y) / aa
        if all(av*x + bv*y <= dv for _, av, bv, dv in rows):
            found[(x, y)] = sorted(i for i, av, bv, dv in rows if av*x + bv*y == dv)
    return found, nonsingular


def projection(rows):
    """Project affine lower/upper graphs, independently of multiplier records."""
    lower_graphs = [(i, -a/b, d/b) for i, a, b, d in rows if b < 0]
    upper_graphs = [(i, -a/b, d/b) for i, a, b, d in rows if b > 0]
    projected = [(a, d) for _, a, b, d in rows if not b]
    projected += [(ls-us, ut-lt) for _, ls, lt in lower_graphs for _, us, ut in upper_graphs]
    low = max((d/a for a, d in projected if a < 0), default=None)
    high = min((d/a for a, d in projected if a > 0), default=None)
    constant_bad = any(a == 0 and d < 0 for a, d in projected)
    feasible = not constant_bad and not (low is not None and high is not None and low > high)
    return low, high, feasible, lower_graphs, upper_graphs, len(projected)


def run():
    enrollment = json.loads((OWN / "enrollment.json").read_text())
    for item in enrollment["files"]:
        eq("source.sha:" + item["path"], sha(ROOT / item["path"]), item["sha256"])
        eq("snapshot.sha:" + item["path"], sha(ROOT / item["snapshot"]), item["sha256"])
    source = W / "reviews/broker_reconstruction/findings_tables_A1.json"
    paid_result = W / "forecast_action_price_observation_A1/results.json"
    eq("summary.pin", sha(source), PIN)
    eq("result.pin", sha(paid_result), RESULT_PIN)
    summary, result = json.loads(source.read_text()), json.loads(paid_result.read_text())
    eq("global.summary.gate", summary["complete_outer_attempt_economic_claim_permitted"], False)
    eq("global.result.gate", result["global_positive_end_to_end_economic_gate"], False)
    eq("optional.report.fees", result["optional_reporting_fees_included"], False)
    eq("new.paid.runs", result["new_paid_executions"], 0)
    eq("result.status", result["status"], "PASS_SCOPED")
    eq("result.observer", result["observer_sha256"], sha(W / "forecast_action_price_observer.py"))
    eq("result.derivation", result["derivation_sha256"], sha(W / "forecast_action_price_derivation.md"))
    eq("result.summary", result["source"]["sha256"], PIN)
    all_rows = summary["all_configuration_summaries"]
    eq("all.configuration.count", len(all_rows), 76)
    eq("all.scoped.ids.unique", len({(r["family"], r["configuration_id"]) for r in all_rows}), 76)
    eq("no.axis.prefix.collision", any(r["configuration_id"].startswith("axis:") for r in all_rows), False)
    denominators = []
    for r in all_rows:
        key = r["family"] + ":" + r["configuration_id"]
        n = r["planned_executions"]
        eq(key + ":complete", r["complete_primary_denominator"], True)
        eq(key + ":episode.counts", [r["complete_episodes"], r["scored_executions"], len(r["executed_policy_seed_slots"])], [n, n, n])
        eq(key + ":unknown.cost", r["unknown_cost_episodes"], 0)
        eq(key + ":missing", r["missing_or_incomplete_unit_ids"], [])
        whole = [s for s in r["prespecified_slices"] if s["slice"] == "whole"]
        eq(key + ":one.whole", len(whole), 1)
        whole = whole[0]
        eq(key + ":whole.complete", whole["complete_primary_denominator"], True)
        eq(key + ":whole.planned", whole["planned_episodes"], n)
        den = whole["per_episode_denominators"]
        eq(key + ":whole.parents", len(den), n)
        eq(key + ":whole.unique.parents", len({d["unit_id"] for d in den}), n)
        horizons = {d["scheduled_positions"] for d in den}
        eq(key + ":common.horizon", len(horizons), 1)
        horizon = next(iter(horizons))
        eq(key + ":complete.parent.positions", all(d["closed_positions"] == d["scheduled_positions"] and d["parent_complete_and_valid"] and d["usable_full_slice"] for d in den), True)
        eq(key + ":scheduled.positions", sum(d["scheduled_positions"] for d in den), whole["known_scheduled_positions"])
        groups = Counter(d["unit_id"].split("__", 1)[0] for d in den)
        eq(key + ":group.identities", sorted(groups), sorted(r["group_ids"]))
        eq(key + ":group.count", len(groups), 2)
        eq(key + ":balanced.seeds", set(groups.values()), {n // 2})
        v = vector(r)
        eq(key + ":W.whole", v["W"], q(whole["means"]["action_loss_mean"]))
        eq(key + ":B.whole", v["B"], q(whole["means"]["brier_mean"]))
        eq(key + ":mean.cold", q(r["means"]["cold_units"]), Q(r["known_total_executed_cold_units"], n))
        eq(key + ":C.normalized", v["C"], Q(r["known_total_executed_cold_units"], n*horizon))
        denominators.append({"family": r["family"], "configuration_id": r["configuration_id"],
                             "planned_parents": n, "population_count": 2, "scheduled_positions_per_parent": horizon,
                             "known_terminal_cold_units": r["known_total_executed_cold_units"],
                             "optional_report_fee_mean_excluded": q(r["means"]["optional_reporting_units"])})
    symmetric = [r for r in all_rows if r["stakes"] == {"fn": [1, 1], "fp": [1, 1]}]
    excluded = [r for r in all_rows if r["stakes"] != {"fn": [1, 1], "fp": [1, 1]}]
    eq("symmetric.rows", len(symmetric), 72)
    eq("asymmetric.rows", len(excluded), 4)
    eq("asymmetric.exclusions", result["excluded_asymmetric_configuration_ids"], [r["configuration_id"] for r in excluded])
    cases = result["cases"]
    eq("candidate.cells", len(cases), 12)
    eq("candidate.cell.ids.unique", len({(c["family"], c["candidate_id"]) for c in cases}), 12)
    final_cells, rosters, pair_count, vertex_count = [], [], 0, 0
    for family in ["cheap_null", "mixed", "gate_transfer"]:
        group = [r for r in symmetric if r["family"] == family]
        ordinary = {r["configuration_id"]: r for r in group if r["method_kind"] == "ordinary"}
        candidates = {r["configuration_id"]: r for r in group if r["method_kind"] == "candidate"}
        mirrors = {r["configuration_id"]: r for r in group if r["method_kind"] == "mirror"}
        eq(family + ":rosters", [len(group), len(ordinary), len(candidates), len(mirrors)], [24, 19, 4, 1])
        eq(family + ":all.candidates", sorted(c["candidate_id"] for c in cases if c["family"] == family), sorted(candidates))
        ov = {i: vector(r) for i, r in ordinary.items()}
        rosters.append({"family": family, "ordinary_ids": sorted(ordinary), "candidate_ids": sorted(candidates),
                       "excluded_identity_mirrors": [{"id": i, "coordinates": vector(r), "reason": "Recorded kernel identity retained separately"} for i, r in mirrors.items()]})
        for c in [c for c in cases if c["family"] == family]:
            key = family + ":" + c["candidate_id"]
            cv = vector(candidates[c["candidate_id"]])
            eq(key + ":candidate.coordinates", decode_vector(c["candidate"]), cv)
            eq(key + ":ordinary.count", [c["distinct_ordinary_count"], len(c["ordinary"])], [19, 19])
            eq(key + ":ordinary.coordinates", {o["id"]: decode_vector(o) for o in c["ordinary"]}, ov)
            eq(key + ":mirror", c["mirror_id"], next(iter(mirrors)))
            rows = [("axis:lambda", Q(-1), Q(0), Q(0)), ("axis:mu", Q(0), Q(-1), Q(0))]
            rows += [(i, cv["C"]-o["C"], cv["B"]-o["B"], o["W"]-cv["W"]) for i, o in ov.items()]
            by_id = {i: (a, b, d) for i, a, b, d in rows}
            eq(key + ":constraint.count", len(c["constraints"]), 21)
            eq(key + ":constraints", {r["id"]: tuple(q(r[k]) for k in ["a", "b", "d"]) for r in c["constraints"]}, by_id)
            t = c["terminal_witness"]
            original = ov[t["id"]]
            a, d, g = cv["W"]-original["W"], cv["C"]-original["C"], original["B"]-cv["B"]
            eq(key + ":positive.gaps", a > 0 and d > 0 and g > 0, True)
            eq(key + ":witness.gaps", tuple(q(t[k]) for k in ["action_gap", "cost_gap", "forecast_gap"]), (a, d, g))
            eq(key + ":witness.price.line", tuple(q(t[k]) for k in ["mu_intercept", "mu_slope"]), (a/g, d/g))
            direct = sorted(i for i, o in ov.items() if all(o[k] <= cv[k] for k in cv) and any(o[k] < cv[k] for k in cv))
            eq(key + ":direct.dominators", sorted(c["direct_three_coordinate_dominators"]), direct)
            vv, nonsingular = vertices(rows)
            pair_count += nonsingular
            vertex_count += len(c["vertices"])
            saved_vv = {(q(v["lambda"]), q(v["mu"])): sorted(v["tight_constraints"]) for v in c["vertices"]}
            eq(key + ":all.vertices", saved_vv, vv)
            eq(key + ":vertices.unique", len(saved_vv), len(c["vertices"]))
            low, high, feasible, lower_graphs, upper_graphs, projected_count = projection(rows)
            eq(key + ":projection.lower", None if c["lambda_lower"] is None else q(c["lambda_lower"]), low)
            eq(key + ":projection.upper", None if c["lambda_upper"] is None else q(c["lambda_upper"]), high)
            eq(key + ":projection.feasible", c["feasible"], feasible)
            eq(key + ":vertices.feasible", bool(vv), feasible)
            eq(key + ":projected.count", len(c["projected_inequalities"]), projected_count)
            for index, p in enumerate(c["projected_inequalities"]):
                weights = {i: q(v) for i, v in p["combination"].items()}
                eq(key + f":projection.{index}.positive", all(v >= 0 for v in weights.values()), True)
                combined = tuple(sum((v*by_id[i][k] for i, v in weights.items()), Q(0)) for k in range(3))
                eq(key + f":projection.{index}.identity", combined, (q(p["a"]), Q(0), q(p["d"])))
            cell = {"family": family, "candidate_id": c["candidate_id"], "candidate": cv, "ordinary_controls": 19,
                    "vertices": [{"lambda": x, "mu": y, "tight_ids": tight} for (x, y), tight in sorted(vv.items())],
                    "feasible": feasible, "lambda_lower": low, "lambda_upper": high,
                    "terminal_witness": {"id": t["id"], "W_gap": a, "C_gap": d, "B_gap": g, "mu_intercept": a/g, "mu_slope": d/g},
                    "direct_coordinate_dominators": direct}
            if feasible:
                eq(key + ":no.contradiction", c["contradiction"], None)
                eq(key + ":no.convex.certificate", c["ordinary_convex_certificate"], None)
                witness = c["witness"]
                x, y = q(witness["lambda"]), q(witness["mu"])
                eq(key + ":nonnegative.witness", x >= 0 and y >= 0, True)
                slacks = {i: d-a*x-b*y for i, a, b, d in rows}
                eq(key + ":slacks", {i: q(v) for i, v in witness["slacks"].items()}, slacks)
                eq(key + ":nonnegative.slacks", all(v >= 0 for v in slacks.values()), True)
                ordinary_slacks = {i: slacks[i] for i in ordinary}
                eq(key + ":strict.label", witness["strict_against_all_ordinary"], all(v > 0 for v in ordinary_slacks.values()))
                eq(key + ":ties", sorted(witness["ordinary_ties"]), sorted(i for i, v in ordinary_slacks.items() if v == 0))
                kc = cv["W"]+x*cv["C"]+y*cv["B"]
                ko = {i: o["W"]+x*o["C"]+y*o["B"] for i, o in ov.items()}
                eq(key + ":candidate.K", q(witness["candidate_K"]), kc)
                eq(key + ":ordinary.K", {i: q(v) for i, v in witness["ordinary_K"].items()}, ko)
                eq(key + ":K.gap.identity", {i: v-kc for i, v in ko.items()}, ordinary_slacks)
                expected_x = (low+high)/2 if high is not None else low+1
                yl = max(s*x+t for _, s, t in lower_graphs)
                yu = min((s*x+t for _, s, t in upper_graphs), default=None)
                expected_y = (yl+yu)/2 if yu is not None else yl+1
                eq(key + ":relative.interior.witness", (x, y), (expected_x, expected_y))
                cell["strict_witness"] = {"lambda": x, "mu": y, "minimum_ordinary_slack": min(ordinary_slacks.values()),
                                          "tight_ordinary_ids": witness["ordinary_ties"],
                                          "positive_ordinary_slacks": sum(v > 0 for v in ordinary_slacks.values())}
            else:
                eq(key + ":no.feasible.witness", c["witness"], None)
                proof = c["contradiction"]
                weights = {i: q(v) for i, v in proof["nonnegative_multipliers"].items()}
                eq(key + ":Farkas.nonnegative", all(v >= 0 for v in weights.values()), True)
                combined = tuple(sum((v*by_id[i][k] for i, v in weights.items()), Q(0)) for k in range(3))
                eq(key + ":Farkas.identity", combined, tuple(q(proof[k]) for k in ["weighted_a", "weighted_b", "weighted_rhs"]))
                eq(key + ":Farkas.zero.coefficients", combined[:2], (Q(0), Q(0)))
                eq(key + ":Farkas.negative.rhs", combined[2] < 0, True)
                mass = sum((v for i, v in weights.items() if i in ordinary), Q(0))
                eq(key + ":Farkas.ordinary.positive.mass", mass > 0, True)
                normalized = {i: v/mass for i, v in weights.items() if i in ordinary and v > 0}
                combo = {k: sum((v*ov[i][k] for i, v in normalized.items()), Q(0)) for k in cv}
                convex = c["ordinary_convex_certificate"]
                eq(key + ":convex.weights", {i: q(v) for i, v in convex["weights"].items()}, normalized)
                eq(key + ":convex.mass", sum(normalized.values(), Q(0)), Q(1))
                eq(key + ":convex.coordinates", decode_vector(convex["combined_record_coordinates"]), combo)
                gaps = {k: cv[k]-combo[k] for k in cv}
                eq(key + ":convex.gaps", decode_vector(convex["candidate_minus_combination"]), gaps)
                eq(key + ":convex.order", gaps["W"] > 0 and gaps["C"] >= 0 and gaps["B"] >= 0, True)
                eq(key + ":convex.unpaid", convex["paid_randomized_meta_controller_executed"], False)
                cell["empty_certificate"] = {"nonnegative_multipliers": weights, "negative_rhs": combined[2],
                                             "convex_weights": normalized, "candidate_minus_combination": gaps,
                                             "combined_coordinates": combo}
            final_cells.append(cell)
    feasible_count = sum(c["feasible"] for c in final_cells)
    strict_count = sum(c.get("strict_witness", {}).get("positive_ordinary_slacks") == 19 for c in final_cells)
    eq("all.feasible.cells", result["feasible_candidate_cells"], feasible_count)
    eq("all.strict.cells", result["strict_witness_candidate_cells"], strict_count)
    eq("all.empty.cells", result["empty_candidate_cells_with_exact_contradictions"], 12-feasible_count)
    for item in enrollment["files"]:
        eq("unchanged.at.end:" + item["path"], sha(ROOT / item["path"]), item["sha256"])
    return {"status": "PASS", "source_summary_sha256": PIN, "principal_result_sha256": RESULT_PIN,
            "configuration_count": 76, "symmetric_configuration_count": 72,
            "planned_parents_all_configurations": sum(r["planned_executions"] for r in all_rows),
            "planned_parents_symmetric": sum(r["planned_executions"] for r in symmetric),
            "excluded_asymmetric": [{"family": r["family"], "configuration_id": r["configuration_id"], "stakes": r["stakes"], "reason": "Different action stakes"} for r in excluded],
            "rosters": rosters, "denominators": denominators, "cells": final_cells,
            "feasible_cells": feasible_count, "strict_witness_cells": strict_count, "empty_cells": 12-feasible_count,
            "vertices_verified": vertex_count, "nonsingular_boundary_pairs_examined": pair_count,
            "ordinary_constraints": 228, "axis_constraints": 24,
            "scientific_worker_truth_generator_scorer_analyzer_calls": 0, "principal_research_credit_seconds": 0,
            "global_positive_end_to_end_economic_gate": False, "optional_reporting_fees_included": False,
            "scope": "Post-outcome fixed saved W/C/issued-Brier coordinates; symmetric stakes, complete cold terminal bills per scheduled position. No changed paid trajectory."}


def main():
    OUT.mkdir(exist_ok=False)
    started, clock = datetime.now(timezone.utc).isoformat(), time.perf_counter_ns()
    failed = False
    try:
        result = run()
    except Exception as exc:
        failed = True
        (OUT / "failure_traceback.txt").write_text(traceback.format_exc(), encoding="utf-8")
        result = {"status": "OBSERVER_FAILURE_PRESERVED", "error_type": type(exc).__name__, "error": str(exc)}
    result.update({"schema": "p310.independent_forecast_price_certificate_check.v1", "reviewer": REVIEWER,
                   "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
                   "elapsed_ns": time.perf_counter_ns()-clock, "checks": len(checks),
                   "failed_checks": sum(not c["pass"] for c in checks), "principal_research_credit_seconds": 0})
    save(OUT / "results.json", result)
    save(OUT / "check_log.json", checks)
    save(OUT / "run_manifest.json", {"source_path": str(Path(__file__).relative_to(ROOT)),
         "source_sha256": sha(Path(__file__)), "source_bytes": Path(__file__).stat().st_size,
         "files": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size}
                   for p in sorted(OUT.iterdir()) if p.is_file()]})
    print(json.dumps({k: result[k] for k in ["status", "checks", "failed_checks", "elapsed_ns"]}, sort_keys=True))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
