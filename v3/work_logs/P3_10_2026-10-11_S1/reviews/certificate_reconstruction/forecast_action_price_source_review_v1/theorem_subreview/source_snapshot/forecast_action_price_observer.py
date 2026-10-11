"""Exact post-outcome W/C/issued-Brier sensitivity from saved summary records.

ChatGPT (GPT-6 Astra Pro), principal /root, 2026-10-11. No paid execution.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import time

W = Path(__file__).resolve().parent
SOURCE = W / "reviews/broker_reconstruction/findings_tables_A1.json"
PIN = "94f41a247f9fade238028608a221fac39d0a8be56af857de5a4c0c1d8640c3ae"
OUT = W / "forecast_action_price_observation_A1"


def frac(pair):
    assert isinstance(pair, list) and len(pair) == 2
    assert all(type(v) is int for v in pair) and pair[1] > 0
    return F(*pair)


def encode(v):
    if isinstance(v, F):
        return [v.numerator, v.denominator]
    if isinstance(v, dict):
        return {k: encode(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [encode(x) for x in v]
    return v


def vector(row):
    assert row["complete_primary_denominator"] and row["unknown_cost_episodes"] == 0
    assert row["complete_episodes"] == row["planned_executions"] == row["scored_executions"]
    assert not row["missing_or_incomplete_unit_ids"]
    return {"W": frac(row["means"]["action_loss_mean"]),
            "C": frac(row["mean_cold_units_per_request"]),
            "B": frac(row["means"]["brier_mean"])}


def add_scaled(destination, source, scale):
    for k, v in source.items():
        destination[k] = destination.get(k, F(0)) + scale*v


def eliminate(constraints):
    """Eliminate mu with nonnegative exact combinations and retain proof terms."""
    lows, ups, projected = [], [], []
    by_id = {r["id"]: r for r in constraints}
    for r in constraints:
        if r["b"] > 0:
            ups.append(r)
        elif r["b"] < 0:
            lows.append(r)
        else:
            projected.append({"a": r["a"], "d": r["d"], "combination": {r["id"]: F(1)}})
    for lo in lows:
        for up in ups:
            kl, ku = -1/lo["b"], 1/up["b"]
            projected.append({"a": kl*lo["a"]+ku*up["a"],
                              "d": kl*lo["d"]+ku*up["d"],
                              "combination": {lo["id"]: kl, up["id"]: ku}})
    lower = upper = None
    lower_record = upper_record = impossible = None
    for r in projected:
        combination = r["combination"]
        assert all(k >= 0 for k in combination.values())
        assert sum(k*by_id[i]["a"] for i, k in combination.items()) == r["a"]
        assert sum(k*by_id[i]["b"] for i, k in combination.items()) == 0
        assert sum(k*by_id[i]["d"] for i, k in combination.items()) == r["d"]
        if r["a"] > 0:
            bound = r["d"]/r["a"]
            if upper is None or bound < upper:
                upper, upper_record = bound, r
        elif r["a"] < 0:
            bound = r["d"]/r["a"]
            if lower is None or bound > lower:
                lower, lower_record = bound, r
        elif r["d"] < 0:
            impossible = r
    certificate = None
    if impossible is not None:
        certificate = impossible["combination"]
    elif lower is not None and upper is not None and lower > upper:
        certificate = {}
        add_scaled(certificate, lower_record["combination"], -1/lower_record["a"])
        add_scaled(certificate, upper_record["combination"], 1/upper_record["a"])
    if certificate is not None:
        assert all(k >= 0 for k in certificate.values())
        aa = sum(k*by_id[i]["a"] for i, k in certificate.items())
        bb = sum(k*by_id[i]["b"] for i, k in certificate.items())
        dd = sum(k*by_id[i]["d"] for i, k in certificate.items())
        assert aa == bb == 0 and dd < 0
        return {"feasible": False, "lambda_lower": lower, "lambda_upper": upper,
                "projected_inequalities": projected,
                "contradiction": {"nonnegative_multipliers": certificate,
                                  "weighted_a": aa, "weighted_b": bb, "weighted_rhs": dd},
                "witness": None}
    assert lower is not None and lower >= 0
    x = (lower+upper)/2 if upper is not None else lower+1
    lower_y = [(r["d"]-r["a"]*x)/r["b"] for r in lows]
    upper_y = [(r["d"]-r["a"]*x)/r["b"] for r in ups]
    yl = max(lower_y)
    yu = min(upper_y) if upper_y else None
    assert yu is None or yl <= yu
    y = (yl+yu)/2 if yu is not None else yl+1
    assert x >= 0 and y >= 0
    slacks = {r["id"]: r["d"]-r["a"]*x-r["b"]*y for r in constraints}
    assert all(v >= 0 for v in slacks.values())
    return {"feasible": True, "lambda_lower": lower, "lambda_upper": upper,
            "projected_inequalities": projected, "contradiction": None,
            "witness": {"lambda": x, "mu": y, "slacks": slacks,
                        "strict_against_all_ordinary": all(v > 0 for i, v in slacks.items() if not i.startswith("axis:")),
                        "ordinary_ties": [i for i, v in slacks.items() if v == 0 and not i.startswith("axis:")]}}


def vertices(constraints):
    good = {}
    for r, s in combinations(constraints, 2):
        det = r["a"]*s["b"]-s["a"]*r["b"]
        if det == 0:
            continue
        x = (r["d"]*s["b"]-s["d"]*r["b"])/det
        y = (r["a"]*s["d"]-s["a"]*r["d"])/det
        if all(t["a"]*x+t["b"]*y <= t["d"] for t in constraints):
            good[(x, y)] = {"lambda": x, "mu": y,
                            "tight_constraints": [t["id"] for t in constraints if t["a"]*x+t["b"]*y == t["d"]]}
    return [good[k] for k in sorted(good)]


def main():
    started = {"utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns()}
    OUT.mkdir(exist_ok=False)
    (OUT/"start.json").write_text(json.dumps(started, indent=2)+"\n")
    try:
        data = SOURCE.read_bytes()
        assert sha256(data).hexdigest() == PIN
        j = json.loads(data)
        assert j["complete_outer_attempt_economic_claim_permitted"] is False
        rows = j["all_configuration_summaries"]
        assert len(rows) == 76
        excluded = [r["configuration_id"] for r in rows if r["stakes"] != {"fn": [1,1], "fp": [1,1]}]
        assert len(excluded) == 4
        symmetric = [r for r in rows if r["stakes"] == {"fn": [1,1], "fp": [1,1]}]
        cases = []
        witness_id = {"cheap_null": "exact_dpll", "mixed": "proof_dpll_fallback1", "gate_transfer": "probability_cost"}
        for family in ["cheap_null", "mixed", "gate_transfer"]:
            group = [r for r in symmetric if r["family"] == family]
            ordinary = [r for r in group if r["method_kind"] == "ordinary"]
            candidates = [r for r in group if r["method_kind"] == "candidate"]
            mirrors = [r for r in group if r["method_kind"] == "mirror"]
            assert len(group) == 24 and len(ordinary) == 19 and len(candidates) == 4 and len(mirrors) == 1
            for c in candidates:
                cv = vector(c)
                controls = [{"id": r["configuration_id"], **vector(r)} for r in ordinary]
                constraints = [{"id": "axis:lambda", "a": F(-1), "b": F(0), "d": F(0)},
                               {"id": "axis:mu", "a": F(0), "b": F(-1), "d": F(0)}]
                for o in controls:
                    constraints.append({"id": o["id"], "a": cv["C"]-o["C"],
                                        "b": cv["B"]-o["B"], "d": o["W"]-cv["W"]})
                ov = next(o for o in controls if o["id"] == witness_id[family])
                a, d, g = cv["W"]-ov["W"], cv["C"]-ov["C"], ov["B"]-cv["B"]
                assert a > 0 and d > 0 and g > 0
                result = eliminate(constraints)
                vv = vertices(constraints)
                assert bool(vv) == result["feasible"]
                direct_dominators = [o["id"] for o in controls if all(o[k] <= cv[k] for k in ["W","C","B"])
                                     and any(o[k] < cv[k] for k in ["W","C","B"])]
                if result["witness"] is not None:
                    point = result["witness"]
                    kc = cv["W"]+point["lambda"]*cv["C"]+point["mu"]*cv["B"]
                    ko = {o["id"]: o["W"]+point["lambda"]*o["C"]+point["mu"]*o["B"] for o in controls}
                    assert all(kc <= v for v in ko.values())
                    point["candidate_K"] = kc
                    point["ordinary_K"] = ko
                convex = None
                if not result["feasible"]:
                    multipliers = result["contradiction"]["nonnegative_multipliers"]
                    mass = sum(v for k, v in multipliers.items() if not k.startswith("axis:"))
                    assert mass > 0
                    weights = {k: v/mass for k, v in multipliers.items() if not k.startswith("axis:") and v > 0}
                    assert sum(weights.values()) == 1
                    by_id = {o["id"]: o for o in controls}
                    combined = {k: sum(w*by_id[i][k] for i, w in weights.items()) for k in ["W","C","B"]}
                    assert combined["W"] < cv["W"] and combined["C"] <= cv["C"] and combined["B"] <= cv["B"]
                    convex = {"weights": weights, "combined_record_coordinates": combined,
                              "candidate_minus_combination": {k: cv[k]-combined[k] for k in ["W","C","B"]},
                              "paid_randomized_meta_controller_executed": False}
                cases.append({"family": family, "candidate_id": c["configuration_id"], "candidate": cv,
                              "distinct_ordinary_count": 19, "ordinary": controls,
                              "mirror_id": mirrors[0]["configuration_id"],
                              "terminal_witness": {"id": ov["id"], "action_gap": a, "cost_gap": d,
                                                   "forecast_gap": g, "mu_intercept": a/g, "mu_slope": d/g},
                              "direct_three_coordinate_dominators": direct_dominators,
                              "ordinary_convex_certificate": convex,
                              "constraints": constraints, "vertices": vv, **result})
        assert len(cases) == 12
        obj = {"schema": "P3-10-fixed-path-forecast-action-price-v1", "status": "PASS_SCOPED",
               "contributor": "ChatGPT (GPT-6 Astra Pro), principal /root", "start": started,
               "end": {"utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns()},
               "source": {"path": str(SOURCE.relative_to(W)), "bytes": len(data), "sha256": PIN},
               "observer_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "derivation_sha256": sha256((W/"forecast_action_price_derivation.md").read_bytes()).hexdigest(),
               "scope": "Post-outcome sensitivity of saved symmetric-stakes whole-configuration means; not a new paid endpoint",
               "objective": "W + lambda * complete_cold_terminal_units_per_request + mu * issued_brier_mean",
               "excluded_asymmetric_configuration_ids": excluded,
               "optional_reporting_fees_included": False, "global_positive_end_to_end_economic_gate": False,
               "independent_policy_or_source_samples_claimed": False,
               "new_paid_executions": 0, "cases": cases,
               "feasible_candidate_cells": sum(r["feasible"] for r in cases),
               "strict_witness_candidate_cells": sum(bool(r["witness"] and r["witness"]["strict_against_all_ordinary"]) for r in cases),
               "empty_candidate_cells_with_exact_contradictions": sum(not r["feasible"] for r in cases)}
        (OUT/"results.json").write_text(json.dumps(encode(obj), indent=2)+"\n")
        print(json.dumps({k: obj[k] for k in ["status", "feasible_candidate_cells", "strict_witness_candidate_cells", "empty_candidate_cells_with_exact_contradictions"]}))
    except BaseException as exc:
        (OUT/"failure.json").write_text(json.dumps({"type": type(exc).__name__, "message": str(exc),
            "utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns()}, indent=2)+"\n")
        raise


if __name__ == "__main__":
    main()
