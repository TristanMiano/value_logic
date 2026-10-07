#!/usr/bin/env python3
"""DEVELOPMENT: P3-02 probability certificates using the unchanged v2 kernel.

This checks supplied rational fixtures and proof witnesses, not general proof
search, a frozen challenge, empirical calibration, or production coverage.
The v2/verification model/native wrappers target the old quartic experiment;
their underlying F06/F07/F08 tooling is reused with explicit P3 source scopes.
Run from the repository root with Python 3.10+ and the standard library.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import sys
import traceback

# Do not create bytecode files in inherited phase-two directories.
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as H
from v2.checks import f08_unit_characterization as U


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    payload = json.dumps(K.serial(value), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def rejection(call, exception_type, message_fragment):
    try:
        call()
    except exception_type as exc:
        require(message_fragment in str(exc), "Unexpected rejection reason: " + str(exc))
        return {"status": "rejected_as_required", "exception": type(exc).__name__,
                "reason": str(exc)}
    raise AssertionError("The invalid proof or multiplier was accepted.")


def receipt(ctx, proof, new, budget, unit, points, *, case="h"):
    """Bind an independently specified literal target to its checked root."""
    expected = H.request(ctx, case, new, K.num(0, unit), F(budget), unit)
    root = H.receive(ctx, proof, expected)
    require(root.budget == F(budget), "Unexpected exact fixture budget.")
    audit = H.audit_points(ctx, proof, points)
    return {
        "status": "accepted",
        "context_id": K.fingerprint(ctx),
        "request": K.serial(expected),
        "root_budget": str(root.budget),
        "root_unit": K.infer(root.new, ctx.signature),
        "proof_nodes": len(proof.steps),
        "rules_used": sorted({step.rule for step in proof.steps}),
        "proof_sha256": digest(proof),
        "proof": K.serial(proof),
        "finite_reference_audit": audit,
    }


def binary_context(reverse=False):
    p, y = K.src("p"), K.src("y")
    conversions = [K.Conversion("event_gap", "P", "U", F(4))]
    if reverse:
        conversions.append(K.Conversion("recover_probability", "U", "P", F(1, 4)))
    sig = K.Signature("P3-02-known-binary-loss-development-v1", ("P", "U"),
                      (("p", "P"), ("y", "U")), tuple(conversions))
    priced = K.convert("event_gap", p)
    rows = (
        K.Row(K.scale(-1, p), K.num(0, "P")),
        K.Row(p, K.num(1, "P")),
        K.Row(K.sub(y, priced), K.num(1, "U")),
        K.Row(K.sub(priced, y), K.num(-1, "U")),
        K.Row(y, K.num(3, "U")),
        K.Row(K.scale(-1, y), K.num(-2, "U")),
    )
    ctx = K.Context(sig, "known-loss-interval-observation", "development-r1",
                    (K.Case("h", rows, (("p", F(3, 8)), ("y", F(5, 2)))),))
    ctx.validate()
    return ctx


def binary_proof(ctx, sign, reverse=False):
    b = K.Builder(ctx, "h")
    rows = (3, 4) if sign == 1 else (2, 5)
    root = b.add(b.row(rows[0]), b.row(rows[1]))
    target = K.convert("event_gap", K.src("p"))
    if sign == -1:
        target = K.scale(-1, target)
    root = b.rewrite(root, target, K.num(0, "U"))
    if reverse:
        root = b.conversion("recover_probability", root)
        target = K.src("p") if sign == 1 else K.scale(-1, K.src("p"))
        root = b.rewrite(root, target, K.num(0, "P"))
    return b.proof(root), target


BINARY_POINTS = [
    {"p": F(1, 4), "y": F(2)},
    {"p": F(3, 8), "y": F(5, 2)},
    {"p": F(1, 2), "y": F(3)},
]


def check_one_way():
    ctx = binary_context()
    results = []
    for sign, budget in ((1, F(2)), (-1, F(-1))):
        proof, target = binary_proof(ctx, sign)
        results.append(receipt(ctx, proof, target, budget, "U", BINARY_POINTS))

    reduced = U.unit_reduct(ctx, "P")
    point = {"p": F(3, 4), "y": F(5, 2)}
    require(len(reduced.cases[0].rows) == 2, "Foreign-unit rows survived P reduct.")
    require(H.case_feasible(reduced, "h", point), "Reduct countermodel is infeasible.")
    require(not H.case_feasible(ctx, "h", point), "Countermodel also satisfies full source.")
    value = H.value(K.src("p"), reduced.signature, point)
    require(value > F(1, 2), "Reduct point does not refute the probability bound.")

    # Numerical scaling stays in U; an attempted bare rewrite into P is invalid.
    b = K.Builder(ctx, "h")
    root = b.add(b.row(3), b.row(4))
    root = b.scale(F(1, 4), root)
    root = b.rewrite(root, K.src("p"), K.num(0, "P"))
    invalid = b.proof(root)
    rejected = rejection(lambda: K.check(ctx, invalid), K.ProofError,
                         "Conclusion or budget does not follow")
    return {
        "name": "one_way_loss_bounds_and_probability_obstruction",
        "status": "passed", "context": K.serial(ctx), "accepted_targets": results,
        "inverse_rewrite": rejected,
        "reduct_countermodel": {
            "point": K.serial(point), "feasible_in_P_reduct": True,
            "feasible_in_full_context": False, "target_value": str(value),
            "requested_upper_bound": "1/2", "retained_rows": 2,
            "nonderivability_basis": "F08 target-unit-reduct theorem plus this witness; no exhaustive proof search",
        },
    }


def check_reverse():
    ctx = binary_context(reverse=True)
    require("U" in U.paths_to(ctx.signature, "P"), "Declared reverse path missing.")
    results = []
    for sign, budget in ((1, F(1, 2)), (-1, F(-1, 4))):
        proof, target = binary_proof(ctx, sign, reverse=True)
        results.append(receipt(ctx, proof, target, budget, "P", BINARY_POINTS))
    return {
        "name": "declared_reciprocal_calibration",
        "status": "passed", "context": K.serial(ctx), "accepted_targets": results,
        "probability_interval": ["1/4", "1/2"],
        "premise": "The U-to-P factor 1/4 is explicitly declared for this calibrated scope.",
    }


def full_law_context():
    p1, p2, p3 = (K.src(name) for name in ("p1", "p2", "p3"))
    total = K.add(K.add(p1, p2), p3)
    l1 = K.add(p1, K.scale(2, p2))
    l2 = K.add(p2, K.scale(3, p3))
    sig = K.Signature(
        "P3-02-known-finite-losses-development-v1", ("P", "U"),
        (("p1", "P"), ("p2", "P"), ("p3", "P")),
        (K.Conversion("unit_loss", "P", "U", F(1)),
         K.Conversion("calibrated_numerical_return", "U", "P", F(1))),
    )
    rows = [K.Row(total, K.num(1, "P")),
            K.Row(K.scale(-1, total), K.num(-1, "P"))]
    rows.extend(K.Row(K.scale(-1, p), K.num(0, "P")) for p in (p1, p2, p3))
    for term in (l1, l2):
        cost = K.convert("unit_loss", term)
        rows.extend((K.Row(cost, K.num(F(5, 4), "U")),
                     K.Row(K.scale(-1, cost), K.num(F(-5, 4), "U"))))
    point = {"p1": F(1, 4), "p2": F(1, 2), "p3": F(1, 4)}
    ctx = K.Context(sig, "two-exact-loss-observations", "development-r1",
                    (K.Case("h", tuple(rows), tuple(point.items())),))
    ctx.validate()
    return ctx, point


def check_full_law():
    ctx, point = full_law_context()
    converted, origins = U.converted_context(ctx, "P")
    recipes = (
        ("p1", 1, F(1, 4), {0: F(3, 2), 6: F(1, 2), 8: F(1, 2)}),
        ("p1", -1, F(-1, 4), {1: F(3, 2), 5: F(1, 2), 7: F(1, 2)}),
        ("p2", 1, F(1, 2), {1: F(3, 4), 5: F(3, 4), 7: F(1, 4)}),
        ("p2", -1, F(-1, 2), {0: F(3, 4), 6: F(3, 4), 8: F(1, 4)}),
        ("p3", 1, F(1, 4), {0: F(1, 4), 6: F(1, 4), 7: F(1, 4)}),
        ("p3", -1, F(-1, 4), {1: F(1, 4), 5: F(1, 4), 8: F(1, 4)}),
    )
    results = []
    for name, sign, budget, chosen in recipes:
        weights = tuple(chosen.get(i, F(0)) for i in range(len(converted.cases[0].rows)))
        require(all(weight >= 0 for weight in weights), "Fixture has a negative multiplier.")
        target = K.src(name) if sign == 1 else K.scale(-1, K.src(name))
        local = U.affine_certificate(converted, "h", target, K.num(0, "P"), budget, weights)
        b = K.Builder(converted, "h")
        b.steps = list(local.steps)
        global_root = b.all_cases((local.root,))
        expected = H.request(ctx, None, target, K.num(0, "P"), budget, "P")
        proof = U.receive_converted(ctx, b.proof(global_root), expected)
        out = receipt(ctx, proof, target, budget, "P", [point], case=None)
        out["converted_source_multipliers"] = [str(weight) for weight in weights]
        out["target_name"] = name
        out["orientation"] = "upper" if sign == 1 else "lower"
        results.append(out)
    require(point["p1"] + 2 * point["p2"] == F(5, 4), "First semantic loss mismatch.")
    require(point["p2"] + 3 * point["p3"] == F(5, 4), "Second semantic loss mismatch.")
    require(sum(point.values()) == 1, "Law is not normalized.")
    return {
        "name": "normalized_full_law_from_two_known_loss_rows",
        "status": "passed", "context": K.serial(ctx),
        "converted_row_origins": K.serial(origins),
        "measurement_rows": [[1, 2, 0], [0, 1, 3]],
        "measurement_values": ["5/4", "5/4"],
        "recovered_law": K.serial(point), "accepted_targets": results,
    }


def check_negative_multipliers():
    ctx = binary_context()
    b = K.Builder(ctx, "h")
    invalid_root = b.scale(-1, b.row(1))
    invalid = b.proof(invalid_root)
    native = rejection(lambda: K.check(ctx, invalid), K.ProofError,
                       "Nonnegative rational scale required")
    point = BINARY_POINTS[1]
    last = invalid.steps[invalid.root]
    actual = H.value(last.new, ctx.signature, point) - H.value(last.old, ctx.signature, point)
    require(H.case_feasible(ctx, "h", point) and actual > last.budget,
            "The negative-scale mutation should have a genuine feasible refutation.")

    full, _ = full_law_context()
    converted, _ = U.converted_context(full, "P")
    weights = (F(-1),) + (F(0),) * (len(converted.cases[0].rows) - 1)
    affine = rejection(
        lambda: U.affine_certificate(converted, "h", K.src("p1"), K.num(0, "P"), F(1), weights),
        H.AuditError, "Negative affine multiplier",
    )
    return {
        "name": "unsound_negative_inequality_multipliers",
        "status": "passed", "native_scale_mutation": native,
        "affine_emitter_negative_weight": affine,
        "feasible_refutation": {"point": K.serial(point), "actual_difference": str(actual),
                                 "invalid_budget": str(last.budget)},
    }


def check_common_scale_thresholds():
    v1, v2 = K.src("v1"), K.src("v2")
    total = K.add(v1, v2)
    rows = (K.Row(K.scale(-1, v1), K.num(-2)), K.Row(v1, K.num(3)),
            K.Row(K.scale(-1, v2), K.num(-1)), K.Row(v2, K.num(2)))
    ctx = K.context(("v1", "v2"), rows, {"v1": 2, "v2": 1},
                    scope="P3-02-common-positive-stake-threshold-development-v1")
    points = [{"v1": F(a), "v2": F(b)} for a in (2, 3) for b in (1, 2)]
    recipes = (
        ("positive_denominator", K.scale(-1, total), F(-3), (F(1), F(0), F(1), F(0))),
        ("probability_at_least_one_half", K.sub(K.scale(F(1, 2), total), v1),
         F(0), (F(1, 2), F(0), F(0), F(1, 2))),
        ("probability_at_most_three_quarters", K.sub(v1, K.scale(F(3, 4), total)),
         F(0), (F(0), F(1, 4), F(3, 4), F(0))),
    )
    results = []
    for name, target, budget, weights in recipes:
        proof = U.affine_certificate(ctx, "h", target, K.num(0), budget, weights)
        out = receipt(ctx, proof, target, budget, "U", points)
        out["target_name"] = name
        out["source_multipliers"] = [str(weight) for weight in weights]
        results.append(out)
    ratios = [point["v1"] / (point["v1"] + point["v2"]) for point in points]
    require(min(ratios) == F(1, 2) and max(ratios) == F(3, 4), "Endpoint ratios changed.")
    return {
        "name": "fixed_probability_threshold_as_loss_unit_affine_sign",
        "status": "passed", "context": K.serial(ctx), "accepted_targets": results,
        "external_probability_interval": ["1/2", "3/4"],
        "external_calibration_premise": "v_i=s*p_i for one shared constant positive stake and an exhaustive normalized partition",
        "scope": "Native receipts prove U-unit affine signs and S>=3. Ratio interpretation is external; no native division or P-unit root is claimed.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        previous = json.loads(output.read_text(encoding="utf-8"))
        require(previous.get("schema") == "P3-02-native-probability-development-v1",
                "Refusing to overwrite an unrelated evidence file.")
    else:
        previous = {"schema": "P3-02-native-probability-development-v1", "runs": []}
    dependencies = (
        "v2/checks/f05_semantics.py", "v2/checks/f06_inference_rules.py",
        "v2/checks/f07_soundness.py", "v2/checks/f08_unit_characterization.py",
        "v2/checks/f06_source_transport.py", "v2/checks/f06_derived_cases.py",
        "v3/checks/02_native_probability_check.py",
    )
    run = {
        "evidence_class": "DEVELOPMENT",
        "contributor": "ChatGPT (GPT-6 Astra Pro), internal delegated implementation check",
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(), "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable, "argv": list(getattr(sys, "orig_argv", sys.argv)),
        "cwd": str(Path.cwd()), "additional_research_time_credit": 0,
        "direct_tooling_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                  for name in dependencies},
        "inspected_experiment_wrappers": {
            "paths": ["v2/verification/native.py", "v2/verification/model.py"],
            "disposition": "Their quartic-experiment input schema is not reused. This script uses the unchanged underlying F06/F07/F08 tooling with declared P3 fixtures.",
        },
        "groups": [],
    }
    failure = None
    try:
        for check in (check_one_way, check_reverse, check_full_law,
                      check_negative_multipliers, check_common_scale_thresholds):
            run["groups"].append(check())
        run["status"] = "passed"
        run["accepted_native_targets"] = sum(len(group.get("accepted_targets", [])) for group in run["groups"])
        run["expected_rejections"] = 3
        run["scope"] = "Five supplied rational development groups, thirteen accepted target receipts, three expected rejections, and an explicit reduct countermodel; no broad production or empirical claim."
    except Exception as exc:
        failure = exc
        run["status"] = "failed"
        run["failure"] = {"exception": type(exc).__name__, "message": str(exc),
                          "traceback": traceback.format_exc()}
    previous["runs"].append(run)
    previous["latest_status"] = run["status"]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(previous, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": run["status"], "completed_groups": len(run["groups"]),
                      "accepted_native_targets": run.get("accepted_native_targets", 0),
                      "expected_rejections": run.get("expected_rejections", 0),
                      "output": str(output)}, sort_keys=True))
    if failure is not None:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
