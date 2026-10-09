"""Independent finite audit of the preserved P3-06 scalar implementation.

All output is development. This script never edits the loaded source and writes
only a fresh result. Independent review time is not principal Research90 time.
Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation reviewer.
"""
from __future__ import annotations

import argparse
import dataclasses
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import platform
import sys
import time
import traceback

sys.dont_write_bytecode = True


def frozen(value):
    """Detached state fingerprint, including nested copy objects."""
    if isinstance(value, F):
        return ("fraction", value.numerator, value.denominator)
    if dataclasses.is_dataclass(value):
        return (type(value).__name__, tuple((f.name, frozen(getattr(value, f.name)))
                                            for f in dataclasses.fields(value)))
    if isinstance(value, dict):
        return ("dict", tuple(sorted(((repr(k), frozen(v)) for k, v in value.items()))))
    if isinstance(value, (list, tuple)):
        return (type(value).__name__, tuple(map(frozen, value)))
    if isinstance(value, set):
        return ("set", tuple(sorted(map(repr, value))))
    if hasattr(value, "__dict__"):
        return (type(value).__name__, frozen(vars(value)))
    return value


def norm(vector):
    return sum((value * value for value in vector), F(0))


def features(pred, bins, alpha, beta):
    p, w = pred.probability, pred.weight
    return tuple(w * alpha * (q - p) for q in pred.expert_values) + tuple(
        w * beta * max(F(0), 1 - bins * abs(p - F(j, bins)))
        for j in range(bins + 1))


def fractions_in(value):
    if isinstance(value, F):
        yield value
    elif dataclasses.is_dataclass(value):
        for field in dataclasses.fields(value):
            yield from fractions_in(getattr(value, field.name))
    elif isinstance(value, dict):
        for item in value.values():
            yield from fractions_in(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from fractions_in(item)


def fraction_sizes(value):
    values = list(fractions_in(value))
    return {
        "fraction_occurrences": len(values),
        "max_numerator_bits": max((abs(q.numerator).bit_length() for q in values), default=0),
        "max_denominator_bits": max((q.denominator.bit_length() for q in values), default=0),
        "sum_numerator_denominator_bits": sum(abs(q.numerator).bit_length() +
                                               q.denominator.bit_length() for q in values),
    }


def primes(count):
    result = []
    n = 101
    while len(result) < count:
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            result.append(n)
        n += 1
    return result


def run(module):
    checks = []
    details = {}

    def check(group, name, condition, **evidence):
        checks.append({"group": group, "name": name, "passed": bool(condition), **evidence})

    def reject_unchanged(group, name, obj, call):
        before = frozen(obj)
        error = None
        try:
            call()
        except Exception as exc:
            error = {"type": type(exc).__name__, "message": str(exc)}
        after = frozen(obj)
        check(group, name, error is not None and before == after,
              rejected=error is not None, state_unchanged=before == after, error=error)

    names = ("zero", "one")
    expert_values = {"zero": 0, "one": 1}

    # These cases target the state transition contract, not only exception type.
    for label in (None, -1, 2, False, True, 1.0, F(1), "1"):
        forecaster = module.Forecaster(names)
        forecaster.issue("pending", expert_values)
        reject_unchanged("input_atomicity", "forecaster_label_" + repr(label), forecaster,
                         lambda: forecaster.reveal("pending", label))
        pool = module.DelayedPool(names)
        pool.issue("pending", expert_values)
        reject_unchanged("input_atomicity", "pool_label_" + repr(label), pool,
                         lambda: pool.reveal("pending", label))

    invalid_issues = [
        ("empty_query", {"query": ""}),
        ("integer_query", {"query": 7}),
        ("unhashable_query", {"query": []}),
        ("negative_weight", {"weight": -1}),
        ("boolean_weight", {"weight": True}),
        ("float_weight", {"weight": 0.5}),
        ("undefined_fraction", {"weight": "1/0"}),
        ("zero_tolerance", {"tolerance": 0}),
        ("negative_tolerance", {"tolerance": -1}),
        ("boolean_tolerance", {"tolerance": True}),
        ("negative_budget", {"max_bisections": -1}),
        ("boolean_budget", {"max_bisections": True}),
        ("float_budget", {"max_bisections": 1.5}),
        ("missing_expert", {"experts": {"zero": 0}}),
        ("extra_expert", {"experts": {"zero": 0, "one": 1, "extra": 0}}),
        ("negative_expert", {"experts": {"zero": -1, "one": 1}}),
        ("large_expert", {"experts": {"zero": 2, "one": 1}}),
        ("boolean_expert", {"experts": {"zero": True, "one": 1}}),
        ("float_expert", {"experts": {"zero": 0.5, "one": 1}}),
    ]
    for name, change in invalid_issues:
        args = {"query": "bad", "experts": expert_values, **change}
        forecaster = module.Forecaster(names)
        reject_unchanged("input_atomicity", "forecaster_" + name, forecaster,
                         lambda: forecaster.issue(**args))
        pool = module.DelayedPool(names)
        reject_unchanged("input_atomicity", "pool_fresh_" + name, pool,
                         lambda: pool.issue(**args))
        pool = module.DelayedPool(names)
        pool.issue("existing", expert_values)
        reject_unchanged("input_atomicity", "pool_busy_" + name, pool,
                         lambda: pool.issue(**args))

    for name, ctor in [
        ("empty_experts", lambda cls: cls(())),
        ("zero_bins", lambda cls: cls(names, bins=0)),
        ("zero_alpha", lambda cls: cls(names, alpha=0)),
        ("empty_scope", lambda cls: cls(names, scope="")),
        ("nonstring_scope", lambda cls: cls(names, scope=7)),
    ]:
        for cls in (module.Forecaster, module.DelayedPool):
            error = None
            try:
                ctor(cls)
            except Exception as exc:
                error = type(exc).__name__
            check("constructor_validation", cls.__name__ + "_" + name,
                  error is not None, error=error)

    source_names = ["zero", "one"]
    alias_f = module.Forecaster(source_names)
    alias_f.issue("alias", expert_values)
    source_names.append("external_edit")
    alias_before = frozen(alias_f)
    alias_error = None
    try:
        alias_f.reveal("alias", 1)
    except Exception as exc:
        alias_error = {"type": type(exc).__name__, "message": str(exc)}
    check("input_aliasing", "caller_names_detached", tuple(alias_f.experts) == names,
          stored_names=list(alias_f.experts))
    check("input_aliasing", "caller_edit_does_not_break_settlement", alias_error is None,
          error=alias_error, state_changed_on_failure=frozen(alias_f) != alias_before,
          pending_cleared=alias_f.pending is None, settled=len(alias_f.history))

    # Returned predictions, mappings, reports and stale feedback have distinct roles.
    f = module.Forecaster(names)
    mapping = dict(expert_values)
    pred = f.issue("first", mapping)
    preserved = frozen(pred)
    mapping["zero"] = 1
    check("report_identity", "expert_mapping_detached", pred.expert_values == (F(0), F(1)))
    f.reveal("first", 0)
    f.issue("second", expert_values)
    reject_unchanged("report_identity", "stale_feedback", f, lambda: f.reveal("first", 1))
    check("report_identity", "old_prediction_unchanged", frozen(pred) == preserved)
    reject_unchanged("report_identity", "pending_blocks_new_issue", f,
                     lambda: f.issue("third", expert_values))
    f.reveal("second", 1)
    reject_unchanged("report_identity", "query_reuse", f,
                     lambda: f.issue("first", expert_values))

    # Direct two-outcome increments reconstruct R from admitted history, never
    # calling implementation _features, _score or squared_norm.
    alpha, beta, bins = F(2, 3), F(5, 4), 3
    weights = (F(0), F(1), F(1, 17), F(19), F(1, 2), F(3))
    counts = {"rounds": 0, "two_outcome_checks": 0, "allowance_positive": 0,
              "budget_exhausted": 0, "boundary_with_large_score": 0}
    for outcomes in product((0, 1), repeat=6):
        f = module.Forecaster(("zero", "one", "past"), bins, alpha, beta)
        for t, y in enumerate(outcomes):
            q = {"zero": 0, "one": 1,
                 "past": F(sum(outcomes[:t]) + 1, t + 2)}
            before = [F(0)] * (3 + bins + 1)
            for old, label in f.history:
                phi_old = features(old, bins, alpha, beta)
                before = [r + (label - old.probability) * value
                          for r, value in zip(before, phi_old)]
            tolerance = F(1, 257)
            p = f.issue(str(t), q, weights[t], tolerance, (0, 1, 8, 12)[t % 4])
            phi = features(p, bins, alpha, beta)
            score = sum((r * value for r, value in zip(before, phi)), F(0))
            score += (1 - 2 * p.probability) * norm(phi) / 2
            deltas = []
            for possible in (0, 1):
                after = [r + (possible - p.probability) * value
                         for r, value in zip(before, phi)]
                delta = norm(after) - norm(before) - p.probability * (1 - p.probability) * norm(phi)
                deltas.append(delta)
                check("potential", "two_outcome_increment", delta <= p.allowance,
                      path="".join(map(str, outcomes)), round=t, outcome=possible)
                counts["two_outcome_checks"] += 1
            check("potential", "exact_worst_outcome_allowance", p.allowance == max(deltas))
            check("potential", "source_feature_score_agreement", tuple(p.features) == phi and p.score == score)
            check("potential", "score_work_accounting", p.score_evaluations <= p.bisections + 3)
            counts["rounds"] += 1
            counts["allowance_positive"] += p.allowance > 0
            counts["budget_exhausted"] += not p.tolerance_met
            counts["boundary_with_large_score"] += p.probability in (0, 1) and abs(score) > tolerance
            f.reveal(str(t), y)
            direct_own = sum((old.weight * (old.probability - label) ** 2
                              for old, label in f.history), F(0))
            check("potential", "loss_recomputed_from_immutable_reports", f.own_loss == direct_own)
    details["independent_potential"] = counts

    # A hidden label may differ across two environments without affecting a new
    # report until that label is actually admitted to the copy used for the report.
    pools = [module.DelayedPool(names, bins=2) for _ in range(2)]
    for pool in pools:
        pool.issue("common", expert_values)
        pool.issue("hidden", expert_values)
        pool.reveal("common", 0)
    issued = [pool.issue("before_hidden_reveal", expert_values) for pool in pools]
    check("delay", "unrevealed_label_noninterference", frozen(issued[0]) == frozen(issued[1]))
    old_reports = [pool.audit() for pool in pools]
    old_snapshots = list(map(frozen, old_reports))
    for pool, label in zip(pools, (0, 1)):
        pool.reveal("hidden", label)
    issued_after = [pool.issue("after_hidden_reveal", expert_values) for pool in pools]
    check("delay", "admitted_label_can_change_report", issued_after[0].probability != issued_after[1].probability)
    check("delay", "audit_snapshots_detached", list(map(frozen, old_reports)) == old_snapshots)
    for pool in pools:
        report = pool.audit()
        check("delay", "pending_unscored", report["pending"] == 2 and report["settled"] == 2)
        reject_unchanged("delay", "pool_duplicate_feedback", pool, lambda: pool.reveal("hidden", 0))

    # Quantify exact-rational growth at fixed search budget, instead of treating
    # a rational operation count as a fixed-bit resource bound.
    growth = []
    prime_list = primes(4 * 128)
    for profile in ("dyadic", "fixed_nondyadic", "fresh_prime_denominators"):
        f = module.Forecaster(("a", "b", "c"), bins=4)
        score_calls = total_bisections = missed = 0
        began = time.monotonic_ns()
        for t in range(128):
            if profile == "dyadic":
                qs = {"a": 0, "b": 1, "c": F((3 * t + 1) % 17, 16)}
                weight = F(1 + t % 4, 2)
            elif profile == "fixed_nondyadic":
                qs = {key: F((3 * t + j + 1) % (d + 1), d)
                      for j, (key, d) in enumerate(zip(("a", "b", "c"), (7, 11, 17)))}
                weight = F(1 + t % 3, 13)
            else:
                qs = {key: F((d // 3 + t + j) % d, d)
                      for j, (key, d) in enumerate(zip(("a", "b", "c"), prime_list[4 * t:4 * t + 3]))}
                denominator = prime_list[4 * t + 3]
                weight = F(denominator - 1, denominator)
            pred = f.issue("growth-" + str(t), qs, weight, tolerance=F(1, 65537), max_bisections=12)
            score_calls += pred.score_evaluations
            total_bisections += pred.bisections
            missed += not pred.tolerance_met
            f.reveal(pred.query, int(pred.probability < F(1, 2)))
            if t + 1 in (16, 32, 64, 128):
                growth.append({"profile": profile, "rounds": t + 1,
                    "elapsed_execution_ns": time.monotonic_ns() - began,
                    "score_evaluations": score_calls, "bisections": total_bisections,
                    "tolerance_not_met_count": missed,
                    "latest_probability": str(pred.probability),
                    "latest_probability_denominator_bits": pred.probability.denominator.bit_length(),
                    "certificate_state": fraction_sizes({
                        "residual": f.residual, "variance": f.variance,
                        "allowance": f.allowance, "own_loss": f.own_loss,
                        "expert_losses": f.expert_losses, "expert_distances": f.expert_distances}),
                    "retained_history": fraction_sizes(f.history),
                    "latest_report": fraction_sizes(pred)})
                check("growth", "dyadic_search_resolution_bound",
                      pred.probability.denominator.bit_length() <= 14,
                      profile=profile, rounds=t + 1)
    details["rational_growth"] = growth
    details["growth_measurement_scope"] = (
        "Sizes are for exposed exact certificate state and retained reports, not every transient "
        "multiplication value or Python heap bytes. Timings cover this deterministic development "
        "run on the reported interpreter; no uniform bit-cost claim follows.")

    failed = [c for c in checks if not c["passed"]]
    mathematical_failures = [c for c in failed if c["group"] in ("potential", "delay", "growth")]
    return {"status": "MATH_FAIL" if mathematical_failures else ("API_FINDINGS" if failed else "PASS"),
            "checks": len(checks), "failed_checks": failed,
            "passed_by_group": {group: sum(c["passed"] for c in checks if c["group"] == group)
                                for group in sorted({c["group"] for c in checks})},
            "total_by_group": {group: sum(c["group"] == group for c in checks)
                               for group in sorted({c["group"] for c in checks})},
            "mathematical_failures": mathematical_failures, "details": details}


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=Path, default=here.parent / "preserved_rerun_v1/defensive_forecasting.py")
    parser.add_argument("--output", type=Path, default=here / "audit_result.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Refusing to overwrite an existing audit result.")
    source = args.module.resolve()
    source_bytes = source.read_bytes()
    spec = importlib.util.spec_from_file_location("independently_audited_defensive_forecasting", source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    began = time.monotonic_ns()
    start_utc = datetime.now(timezone.utc).isoformat()
    try:
        result = run(module)
    except Exception:
        result = {"status": "AUDIT_EXECUTION_FAILED", "traceback": traceback.format_exc()}
    result.update({"schema": "value_logic.p306.independent_implementation_audit_result.v1",
        "start_utc": start_utc, "end_utc": datetime.now(timezone.utc).isoformat(),
        "execution_ns": time.monotonic_ns() - began,
        "python": platform.python_version(), "platform": platform.platform(),
        "source_path": str(source), "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_unchanged": source.read_bytes() == source_bytes,
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "contributor": "ChatGPT (GPT-6 Astra Pro), independent implementation reviewer",
        "research_time_credit_ns": 0,
        "scope": "Finite development audit; neither final evaluation nor historical clock recovery."})
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": result.get("checks"),
                      "failed_checks": len(result.get("failed_checks", [])),
                      "execution_ns": result["execution_ns"], "result": str(args.output)}))
    return 1 if result["status"] in ("MATH_FAIL", "AUDIT_EXECUTION_FAILED") else 0


if __name__ == "__main__":
    raise SystemExit(main())
