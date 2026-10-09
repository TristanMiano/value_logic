"""Reproducible DEVELOPMENT evidence for the P3-07 paid controller.

All full-information profiling, reference labels and self-audit rollouts are
charged as evidence procurement. Exact population enumeration is a separately
priced diagnostic/comparator, not an input to sampled-profile selection.
The seeded trace is a development realization; the theorem assumes IID draws.
The finite population permits direct checking of realized interval coverage.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import random
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("_p307_controller", HERE / "07_paid_reasoning.py")
C = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = C
spec.loader.exec_module(C)
A = C.A
VERSION = "p307-paid-development-v2"
PROFILE_SEED, AUDIT_SEED = 307083, 307081
PRIMES = (17, 31, 47, 61, 97)
POPULATION = tuple((p, a) for p in PRIMES for a in range(1, p))
LAW = "uniform-248-public-euler-queries-v1"
CHECKPOINTS = (128, 256, 512, 1024)
PRICES = {
    "low": C.price_vector(1, 1, F(1, 5), F(1, 1000)),
    "high": C.price_vector(100, 100, 20, F(1, 1000)),
    "false_positive_expensive": C.price_vector(100, 1, 20, F(1, 1000)),
    "false_negative_expensive": C.price_vector(1, 100, 20, F(1, 1000)),
    "zero_task": C.price_vector(0, 0, 0, F(1, 1000)),
    "storage_expensive": C.price_vector(100, 100, 20, F(1, 1000), F(1, 10)),
}


def write(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + "\n")


def record_resources(counter, result):
    counter.update(result["meter"]["by_category"])


def query(index, identity):
    p, a = POPULATION[index]
    return A.Query(identity, a, (p - 1) // 2, p, 1)


def source_hashes():
    return {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in ("07_computation_adapter.py", "07_paid_reasoning.py",
                         "07_paid_reasoning_development.py")}


def actual_scope(hashes):
    return replace(C.modular_scope(LAW),
                   controller=C.VERSION + "@sha256:" + hashes["07_paid_reasoning.py"],
                   adapter=A.VERSION + "@sha256:" + hashes["07_computation_adapter.py"],
                   law=LAW + "@generator-sha256:" + hashes["07_paid_reasoning_development.py"])


def registry_startup(meter):
    """Identical standalone startup for sampled and exhaustive profiling."""
    names = ("07_computation_adapter.py", "07_paid_reasoning.py", "07_paid_reasoning_development.py")
    sizes = [(HERE / name).stat().st_size for name in names]
    if sum(sizes) > 512000:
        raise C.Rejected("Source registry exceeds the fixed half-megabyte admission cap.")
    source_words = sum((size + 7) // 8 for size in sizes)
    meter.pay_many((("profile", "source_registry_read_and_hash_words", 2 * source_words),
                    ("profile", "public_population_construction", 4 * len(POPULATION)),
                    ("storage", "public_population_word_write", 2 * len(POPULATION))))
    return source_hashes()


def evaluate_row(index, identity, procurement, *, reference=False):
    q = query(index, identity)
    results = [C.run_policy(q, p) for p in C.CATALOGUE]
    for result in results:
        record_resources(procurement, result)
    answer = results[-1]["answer"]
    if answer is None or answer["answer"] not in (0, 1):
        raise AssertionError("The declared full solver failed to acquire a checked label.")
    label = answer["answer"]
    if reference and label != int(pow(q.a, q.n, q.m) == q.r):
        raise AssertionError("Independent private pow audit disagrees with checked answer.")
    features = tuple(C.features_from_checked_label(r, label) for r in results)
    base = features[0]
    paired = tuple(tuple(b - x for b, x in zip(base, row)) for row in features)
    return {"index": index, "query": {"a": q.a, "n": q.n, "m": q.m, "r": q.r},
            "label": label, "features": features, "paired": paired,
            "actions": [r["action"] for r in results],
            "statuses": [r["status"] for r in results],
            "initial_reports": [r["initial_report"] for r in results]}


def acquire_profiles(scope, out):
    rng = random.Random(PROFILE_SEED)
    evidence = Counter({c: 0 for c in A.CATEGORIES})
    meter = A.Meter(9_000_000)
    registry_startup(meter)
    builder = C.ProfileBuilder(scope, tuple(p.name for p in C.CATALOGUE), C.FEATURES,
                               tuple(C.paired_ranges(p) for p in C.CATALOGUE),
                               CHECKPOINTS, F(1, 20), meter)
    profiles = {}
    with (out / "profile_rows.jsonl").open("x") as trace:
        for i in range(1, 1025):
            meter.pay_many((("profile", "uniform_index_draw", 1),
                            ("storage", "sampled_query_word_read", 4)))
            index = rng.randrange(len(POPULATION))
            row = evaluate_row(index, "profile-" + str(i), evidence)
            meter.pay("profile", "checked_label_and_feature_interpretation", 4 * len(C.FEATURES) * len(C.CATALOGUE))
            builder.add(row["paired"], meter)
            trace.write(json.dumps(row) + "\n")
            if i in CHECKPOINTS:
                profiles[i] = builder.freeze(meter, tuple(evidence[c] for c in A.CATEGORIES))
                write(out / ("profile_" + str(i) + ".json"), profiles[i].record())
    return profiles, {"executed_policy_resources": dict(evidence),
                      "profile_build_meter": meter.snapshot(),
                      "total_resources": dict(zip(A.CATEGORIES, profiles[1024].setup_resources))}


def enumerate_population(scope, out):
    evidence = Counter({c: 0 for c in A.CATEGORIES})
    meter = A.Meter(9_000_000)
    registry_startup(meter)
    sums = [[0] * len(C.FEATURES) for _ in C.CATALOGUE]
    paired_sums = [[0] * len(C.FEATURES) for _ in C.CATALOGUE]
    labels, statuses = Counter(), Counter()
    with (out / "population_rows.jsonl").open("x") as trace:
        for i in range(len(POPULATION)):
            row = evaluate_row(i, "population-" + str(i), evidence, reference=True)
            meter.pay_many((("profile", "population_row_feature_and_sum", 5 * len(C.FEATURES) * len(C.CATALOGUE)),
                            ("check", "independent_private_reference_pow", 1),
                            ("storage", "population_sum_word_write", len(C.FEATURES) * len(C.CATALOGUE))))
            # The reference pow is a distinct oracle primitive diagnostic, not
            # the deployment computation tariff. It is never used by selection.
            labels[row["label"]] += 1
            statuses.update(row["statuses"])
            for j, fs in enumerate(row["features"]):
                for k, x in enumerate(fs):
                    sums[j][k] += x
                    paired_sums[j][k] += row["paired"][j][k]
            trace.write(json.dumps(row) + "\n")
    meter.pay_many((("profile", "exact_profile_finalize_validate_and_retain", 2 * C.PROFILE_WORD_BOUND),
                    ("storage", "exact_profile_retained_words", C.PROFILE_WORD_BOUND)))
    means = tuple(tuple(F(v, len(POPULATION)) for v in row) for row in sums)
    paired = tuple(tuple(F(v, len(POPULATION)) for v in row) for row in paired_sums)
    resources = {c: evidence[c] + meter.by_category[c] for c in A.CATEGORIES}
    result = {"size": len(POPULATION), "labels": dict(labels), "statuses": dict(statuses),
              "feature_means": dict(zip((p.name for p in C.CATALOGUE), means)),
              "paired_means": dict(zip((p.name for p in C.CATALOGUE), paired)),
              "resources": resources,
              "standalone_startup": "Same source registry and public population construction as sampled profiling; exact table has a charged final retention bundle.",
              "reference_primitive_boundary": "Private pow counts are diagnostic call counts, not a comparable deployable tariff. Removing those calls leaves a paid exact population profile from checked adapter outcomes."}
    write(out / "population_exact.json", result)
    return means, paired, result


def assess_profiles(profiles, scope, means, true_paired, out):
    coverage, selections = [], []
    for n, profile in profiles.items():
        meter = A.Meter(20000)
        intervals, radius = C.profile_intervals(profile, scope, meter)
        bad = [(profile.names[i], C.FEATURES[j], str(true_paired[i][j]), list(map(str, intervals[i][j])))
               for i in range(len(profile.names)) for j in range(len(C.FEATURES))
               if not intervals[i][j][0] <= true_paired[i][j] <= intervals[i][j][1]]
        coverage.append({"n": n, "coverage_holds_exactly": not bad, "bad_cells": bad,
                         "radius": radius, "diagnostic_check_meter": meter.snapshot()})
        if bad:
            raise AssertionError("This realized development profile misses its exact population mean.")
        for price_name, prices in PRICES.items():
            exact_costs = {p.name: C.total_cost(mu, prices) for p, mu in zip(C.CATALOGUE, means)}
            setup = sum((prices[3+j] * v for j, v in enumerate(profile.setup_resources)), F(0))
            for horizon in (1, 64, 10000):
                result = C.select(profile, scope, prices, horizon, setup_to_recover=setup)
                name = result["policy"]
                true_gain = horizon * (exact_costs["fallback"] - exact_costs[name])
                all_in = true_gain - F(result["assessment_cost"]) - setup
                if F(result["conditional_batch_lower_gain"]) > true_gain:
                    raise AssertionError("Selected certificate exceeds exact cohort gain.")
                if F(result["all_in_lower_gain"]) > all_in:
                    raise AssertionError("All-in certificate exceeds exact all-in gain.")
                ordinary = C.select(profile, scope, prices, horizon, setup_to_recover=setup)
                if ordinary != result:
                    raise AssertionError("Same-interface ordinary controller differs.")
                selections.append({"profile_n": n, "price": price_name, "prices": list(map(str, prices)),
                                   "selection": result, "exact_policy_costs": exact_costs,
                                   "exact_best_policy": min(exact_costs, key=exact_costs.get),
                                   "true_batch_gain_before_assessment": true_gain,
                                   "true_all_in_gain": all_in, "ordinary_controller_equal": True})
    write(out / "coverage.json", coverage)
    write(out / "selections.json", selections)
    return coverage, selections


def self_audit(profile, scope, out, hashes):
    prices, batch_size, n_audit = PRICES["high"], 16, 256
    evidence = Counter({c: 0 for c in A.CATEGORIES})
    meter = A.Meter(9_000_000)
    registry_startup(meter)
    preflight = C.select(profile, scope, prices, batch_size)
    record_resources(evidence, preflight)
    selected_policy = next(p for p in C.CATALOGUE if p.name == preflight["policy"])
    closure = {"source_hashes": hashes, "profile_id": profile.identity,
               "scope": scope.record(), "prices": list(map(str, prices)),
               "batch_size": batch_size, "n_audit": n_audit, "seed": AUDIT_SEED,
               "reset": "new adapter/cache per query; fixed profile and selector per episode",
               "selected_policy_before_audit": selected_policy.record(),
               "assessment_limit": 20000, "harness_version": VERSION,
               "audit_role": "Fresh development audit after closure fixed; no subsequent tuning may reuse this as independent evidence."}
    meter.pay_many((("profile", "audit_closure_identity_copy_and_hash", 2 * C.PROFILE_WORD_BOUND),
                    ("storage", "audit_closure_retention", C.PROFILE_WORD_BOUND)))
    closure["identity"] = C.digest(closure)
    closure["frozen_utc_before_first_audit_row"] = datetime.now(timezone.utc).isoformat()
    write(out / "self_audit_closure.json", closure)
    audit_scope = C.Scope(C.VERSION + "@" + closure["identity"], A.VERSION,
                          "fixed-whole-controller-batch-vs-fallback", C.FEATURE_VERSION,
                          LAW + ";16-independent-query-batches", scope.initial_state,
                          scope.sampler_contract, "fresh-audit-whole-episode-no-updates")
    bounds = []
    for i, name in enumerate(C.FEATURES):
        if i == 0:
            bounds.append((-batch_size, 0) if selected_policy.unresolved_action == 1 else (0, 0))
        elif i == 1:
            bounds.append((-batch_size, 0) if selected_policy.unresolved_action == 0 else (0, 0))
        elif i == 2:
            bounds.append((0, batch_size))
        else:
            category = A.CATEGORIES[i-3]
            cap = batch_size * C.POLICY_BUDGET if category in {"admission", "solve", "check", "acquisition", "storage"} and selected_policy.transactions else 0
            if category in {"assessment", "storage"}:
                cap += 20000
            bounds.append((-cap, 0))
    builder = C.ProfileBuilder(audit_scope, ("frozen_controller",), C.FEATURES,
                               (tuple(bounds),), (n_audit,), F(1, 20), meter)
    rng = random.Random(AUDIT_SEED)
    costs = Counter()
    with (out / "self_audit_rows.jsonl").open("x") as trace:
        for episode in range(n_audit):
            selection = C.select(profile, scope, prices, batch_size)
            if selection["policy"] != selected_policy.name:
                raise AssertionError("Frozen fixed-price selection changed within audit.")
            record_resources(evidence, selection)
            controller_features = [0] * len(C.FEATURES)
            baseline_features = [0] * len(C.FEATURES)
            exact_features = [0] * len(C.FEATURES)
            for j, category in enumerate(A.CATEGORIES):
                controller_features[j+3] += selection["meter"]["by_category"][category]
            indices = []
            for within in range(batch_size):
                meter.pay("profile", "fresh_audit_uniform_index_draw", 1)
                index = rng.randrange(len(POPULATION))
                indices.append(index)
                q = query(index, "audit-" + str(episode) + "-" + str(within))
                run = C.run_policy(q, selected_policy)
                baseline = C.run_policy(q, C.CATALOGUE[0])
                exact = C.run_policy(q, C.CATALOGUE[-1])
                for result in (run, baseline, exact):
                    record_resources(evidence, result)
                label = exact["answer"]["answer"]
                for accumulator, result in ((controller_features, run), (baseline_features, baseline), (exact_features, exact)):
                    for k, v in enumerate(C.features_from_checked_label(result, label)):
                        accumulator[k] += v
                meter.pay("profile", "audit_checked_label_feature_read", 4 * 3 * len(C.FEATURES))
            paired = tuple(b-x for b,x in zip(baseline_features, controller_features))
            builder.add((paired,), meter)
            for name, fs in (("controller", controller_features), ("fallback", baseline_features), ("charged_exact", exact_features)):
                costs[name] += C.total_cost(fs, prices)
            trace.write(json.dumps({"episode": episode, "indices": indices,
                                    "controller_features": controller_features,
                                    "baseline_features": baseline_features,
                                    "charged_exact_features": exact_features, "paired": paired}) + "\n")
    audit_profile = builder.freeze(meter, tuple(evidence[c] for c in A.CATEGORIES))
    resources = audit_profile.setup_resources
    certmeter = A.Meter(20000)
    intervals, radius = C.profile_intervals(audit_profile, audit_scope, certmeter)
    lower = C.lower_scores(audit_profile, intervals, prices, certmeter)[0]
    result = {"closure": closure, "audit_profile": audit_profile.record(), "radius": radius,
              "lower_gain_per_batch": lower, "positive_fresh_audit_certificate": lower > 0,
              "observed_total_costs": dict(costs),
              "observed_mean_costs_per_batch": {k:v/n_audit for k,v in costs.items()},
              "procurement_resources": dict(zip(A.CATEGORIES, resources)),
              "final_audit_check_meter": certmeter.snapshot(),
              "boundary": "Own frozen version, fixed high-price cold episode law only. Audit procurement is additional setup, not included in deployment gain. Seeded development realization; no final evaluation claim."}
    write(out / "self_audit.json", result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    (out / "sources").mkdir()
    hashes = source_hashes()
    for name in hashes:
        (out / "sources" / name).write_bytes((HERE / name).read_bytes())
    manifest = {"schema":"value_logic.p307.development_run.v1", "stage":"DEVELOPMENT",
                "version":VERSION, "started_utc":datetime.now(timezone.utc).isoformat(),
                "source_hashes":hashes, "command":sys.argv, "python":sys.version,
                "platform":platform.platform(), "law":LAW, "population_size":len(POPULATION),
                "profile_seed":PROFILE_SEED, "audit_seed":AUDIT_SEED,
                "prospective_plan":"v3/work_logs/P3_07_2026-10-09_S1/development/plan_v2.json"}
    write(out / "manifest.json", manifest)
    start = time.perf_counter_ns()
    result = {"status":"FAIL"}
    try:
        scope = actual_scope(hashes)
        profiles, setup = acquire_profiles(scope, out)
        print("Profile complete", flush=True)
        means, paired, population = enumerate_population(scope, out)
        print("Exact population audit complete", flush=True)
        coverage, selections = assess_profiles(profiles, scope, means, paired, out)
        print("Coverage and repricing complete", flush=True)
        audit = self_audit(profiles[1024], scope, out, hashes)
        result.update(status="PASS", profile_setup=setup,
                      coverage_checks=len(coverage), selections=len(selections),
                      population_size=population["size"], labels=population["labels"],
                      self_audit_positive=audit["positive_fresh_audit_certificate"],
                      self_audit_lower_gain_per_batch=str(audit["lower_gain_per_batch"]))
    except Exception as exc:
        result.update(error=repr(exc), traceback=traceback.format_exc())
    result.update(elapsed_ns=time.perf_counter_ns()-start,
                  finished_utc=datetime.now(timezone.utc).isoformat(), source_hashes=hashes)
    write(out / "result.json", result)
    print(json.dumps(result, indent=2), flush=True)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
