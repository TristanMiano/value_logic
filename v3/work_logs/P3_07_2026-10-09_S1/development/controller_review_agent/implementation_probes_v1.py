"""Focused independent probes of frozen root controller/driver v1.

No root source edits, no broad old-work reruns. Development only; agent time
unmeasured, zero principal Research90 credit.
"""
from dataclasses import replace
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE.parent / "run_v1"
SPEC = importlib.util.spec_from_file_location("controller_review_driver_v1",
    HERE / "source_snapshot_v1/07_paid_reasoning_development.py")
D = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = D
SPEC.loader.exec_module(D)
C, A = D.C, D.A


def profile_from_json(path):
    raw = json.loads(path.read_text())
    return C.Profile(C.Scope(**raw["scope"]), tuple(raw["names"]),
        tuple(raw["feature_names"]), tuple(tuple(tuple(pair) for pair in row) for row in raw["ranges"]),
        tuple(tuple(row) for row in raw["sums"]), raw["n"], tuple(raw["checkpoints"]),
        F(raw["delta"]), tuple(raw["setup_resources"]))


def capture(fn):
    try:
        return dict(returned=True, value=fn())
    except Exception as exc:
        return dict(returned=False, exception=type(exc).__name__, message=str(exc))


def main():
    profile = profile_from_json(RUN / "profile_1024.json")
    budget_rows = []
    for cap in (0, 1, 63, 64, 65, 224, 1000, 20000):
        item = capture(lambda cap=cap: C.select(profile, profile.scope, D.PRICES["high"], 1,
                                               assessment_limit=cap))
        if item["returned"]:
            result = item.pop("value")
            item.update(kind=result["kind"], policy=result["policy"], total=result["meter"]["total"])
        budget_rows.append(dict(assessment_limit=cap, **item))

    q = A.Query("review", 7, 47, 97, 1)
    terminal_rows = []
    for limit in (0, 1, 2, 64, 1024):
        run = C.run_policy(q, C.CATALOGUE[2], limit=limit)
        snapshot = run["meter"]
        terminal_rows.append(dict(limit=limit, status=run["status"], action=run["action"],
            total=snapshot["total"], category_limit_violations={category: quantity
                for category, quantity in snapshot["by_category"].items()
                if quantity > snapshot["category_limits"][category]},
            initial_report=run["initial_report"], events=snapshot["events"]))

    original_adapter = A.Adapter
    observed = []
    class ObservedAdapter(original_adapter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            observed.append(self)
    A.Adapter = ObservedAdapter
    try:
        timed = C.run_policy(q, C.CATALOGUE[3])
        adapter = observed[-1]
        timeout = dict(status=timed["status"], action=timed["action"],
            active_jobs_at_return=adapter.public_state()["active_jobs"],
            cancelled_release_units=timed["meter"]["operations"].get("storage.cancelled_job_release", 0),
            completed_release_units=timed["meter"]["operations"].get("storage.completed_job_release", 0),
            charged_units=timed["meter"]["total"])
    finally:
        A.Adapter = original_adapter

    hashes = json.loads((RUN / "manifest.json").read_text())["source_hashes"]
    other_hashes = dict(hashes, **{"07_paid_reasoning_development.py": "0" * 64})
    driver_scope_alias = D.actual_scope(hashes) == D.actual_scope(other_hashes)

    class MutableFeature:
        def __init__(self, feature):
            self.feature, self.rendered = feature, feature
        def __hash__(self):
            return hash(self.feature)
        def __eq__(self, other):
            return other == self.feature
        def __str__(self):
            return self.rendered
    alias = MutableFeature(C.FEATURES[0])
    aliased = replace(profile, feature_names=(alias,) + C.FEATURES[1:])
    first = C.select(aliased, aliased.scope, D.PRICES["zero_task"], 1)
    alias.rendered = "changed-after-freeze"
    second = C.select(aliased, aliased.scope, D.PRICES["zero_task"], 1)
    mutable_identity = dict(accepted=True, identity_changed=first["profile_id"] != second["profile_id"],
        same_meter=first["meter"] == second["meter"], kind=first["kind"])
    oversized = capture(lambda: replace(profile, feature_names=("x" * 1_000_000,) + C.FEATURES[1:]))
    oversized.pop("value", None)

    ranges = [[(0, 0)] * len(C.FEATURES) for _ in C.CATALOGUE]
    sums = [[0] * len(C.FEATURES) for _ in C.CATALOGUE]
    ranges[2][2], sums[2][2] = (1, 1), profile.n
    forged = replace(profile, ranges=tuple(tuple(row) for row in ranges),
                     sums=tuple(tuple(row) for row in sums))
    wrong_ranges = C.select(forged, forged.scope, D.PRICES["high"], 1)

    builder = C.ProfileBuilder(profile.scope, profile.names, profile.feature_names,
        profile.ranges, (1,), F(1, 20))
    valid = tuple(tuple(0 for _ in C.FEATURES) for _ in C.CATALOGUE)
    invalid = list(valid)
    invalid[-1] = invalid[-1][:-1] + (1,)
    validation = []
    for label, row in (("valid", valid), ("invalid_last_cell", tuple(invalid))):
        meter = A.Meter(0)
        result = capture(lambda row=row: builder.add(row, meter))
        result.pop("value", None)
        validation.append(dict(row=label, spent=meter.total, **result))

    # Reconcile existing rows only; do not execute the full experimental driver.
    expected_ranges = tuple(C.paired_ranges(policy) for policy in C.CATALOGUE)
    cumulative = [[0] * len(C.FEATURES) for _ in C.CATALOGUE]
    profile_rows, range_violations, preserved_prefixes = 0, [], []
    for line in (RUN / "profile_rows.jsonl").read_text().splitlines():
        row = json.loads(line)
        profile_rows += 1
        for i, values in enumerate(row["paired"]):
            for j, value in enumerate(values):
                lo, hi = expected_ranges[i][j]
                if not lo <= value <= hi:
                    range_violations.append((profile_rows, i, j, value))
                cumulative[i][j] += value
        if profile_rows in D.CHECKPOINTS:
            saved = profile_from_json(RUN / f"profile_{profile_rows}.json")
            assert saved.sums == tuple(tuple(row) for row in cumulative)
            preserved_prefixes.append(profile_rows)
    assert profile_rows == 1024
    audit = json.loads((RUN / "self_audit.json").read_text())
    audit_bounds = audit["audit_profile"]["ranges"][0]
    audit_sums = [0] * len(C.FEATURES)
    audit_rows, audit_range_violations = 0, []
    for line in (RUN / "self_audit_rows.jsonl").read_text().splitlines():
        row = json.loads(line)
        audit_rows += 1
        assert row["paired"] == [b - x for b, x in zip(row["baseline_features"], row["controller_features"])]
        for j, value in enumerate(row["paired"]):
            lo, hi = audit_bounds[j]
            if not lo <= value <= hi:
                audit_range_violations.append((audit_rows, j, value))
            audit_sums[j] += value
    assert audit_sums == audit["audit_profile"]["sums"][0]

    radius_rows = []
    for n in D.CHECKPOINTS:
        meter = A.Meter(1000)
        radius, k = C.certified_radius(n, 22, F(1, 20), 4, meter)
        assert 2 * n * radius * radius >= k and F(2 * 22 * 4, 1 << k) <= F(1, 20)
        radius_rows.append(dict(n=n, radius=str(radius), k=k, charged=meter.total))
    return dict(reviewed_controller_sha256=hashlib.sha256((HERE / "source_snapshot_v1/07_paid_reasoning.py").read_bytes()).hexdigest(),
        assessment_budget_edges=budget_rows, terminal_budget_edges=terminal_rows,
        unfinished_job_return=timeout, omitted_driver_hash_scope_alias=driver_scope_alias,
        mutable_feature_identity=mutable_identity, oversized_feature_accepted=oversized["returned"],
        inconsistent_ranges_accepted=dict(policy=wrong_ranges["policy"], lower_gain=wrong_ranges["lower_gain_per_query"],
            positive=wrong_ranges["positive_continuation_certificate"]),
        unfunded_profile_validation=validation,
        saved_evidence_reconciliation=dict(profile_rows=profile_rows, exact_prefix_sums=preserved_prefixes,
            profile_range_violations=range_violations, audit_rows=audit_rows, audit_range_violations=audit_range_violations,
            audit_sum_matches=True), integer_radius_checks=radius_rows,
        scope="Focused development implementation diagnostics and saved-data reconciliation; no full rerun.",
        principal_research90_credit_seconds=0)


if __name__ == "__main__":
    result = main()
    target = HERE / "implementation_probe_results_v1.json"
    with target.open("x") as stream:
        stream.write(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True, indent=2))
