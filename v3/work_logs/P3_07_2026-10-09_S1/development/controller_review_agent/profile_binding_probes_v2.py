"""Retained focused v2 profile-binding and paid-construction probes."""
from dataclasses import replace
from fractions import Fraction as F
import json
from pathlib import Path

from implementation_probes_v2 import A, C, D, capture, profile_from_record, read

HERE = Path(__file__).resolve().parent


def main():
    profile = profile_from_record(read("profile_1024.json"))
    class MutableFeature:
        def __hash__(self):
            return hash(C.FEATURES[0])
        def __eq__(self, other):
            return other == C.FEATURES[0]
        def __str__(self):
            return C.FEATURES[0]
    identities = []
    for name, value in (("mutable_alias", MutableFeature()),
                        ("non_ascii", "fals\u00e9_positive"),
                        ("too_long", "x" * 65)):
        outcome = capture(lambda value=value: replace(profile,
            feature_names=(value,) + C.FEATURES[1:]))
        assert not outcome["returned"] and outcome["exception"] == "Rejected"
        identities.append(dict(case=name, **outcome))
    original_hash = C.sha256
    def forbidden_hash(*args, **kwargs):
        raise AssertionError("Cached profile identity unexpectedly rehashed")
    C.sha256 = forbidden_hash
    try:
        identity = profile.identity
        assert identity == profile.identity
    finally:
        C.sha256 = original_hash

    hashes = read("manifest.json")["source_hashes"]
    changed = dict(hashes, **{"07_paid_reasoning_development.py": "0" * 64})
    assert D.actual_scope(hashes) != D.actual_scope(changed)
    assert profile.scope == D.actual_scope(hashes)

    ranges = [[(0,0)] * len(C.FEATURES) for _ in C.CATALOGUE]
    sums = [[0] * len(C.FEATURES) for _ in C.CATALOGUE]
    ranges[2][2], sums[2][2] = (1,1), profile.n
    altered = replace(profile, ranges=tuple(tuple(row) for row in ranges),
        sums=tuple(tuple(row) for row in sums))
    altered_check = capture(lambda: C.select(altered, altered.scope, D.PRICES["high"], 1))
    assert not altered_check["returned"] and altered_check["exception"] == "Rejected"

    builder_meter = A.Meter(100000)
    builder = C.ProfileBuilder(profile.scope, profile.names, C.FEATURES,
        profile.ranges, (1,), F(1,20), builder_meter)
    good = tuple(tuple(0 for _ in C.FEATURES) for _ in C.CATALOGUE)
    bad = list(good)
    bad[-1] = bad[-1][:-1] + (1,)
    bad = tuple(bad)
    row_checks = []
    for name, row in (("valid", good), ("invalid_final_cell", bad)):
        empty_meter = A.Meter(0)
        outcome = capture(lambda row=row: builder.add(row, empty_meter))
        assert not outcome["returned"] and outcome["exception"] == "BudgetExhausted"
        assert empty_meter.total == 0 and builder.n == 0
        row_checks.append(dict(case=name, total=empty_meter.total, **outcome))
    before = builder_meter.total
    funded_bad = capture(lambda: builder.add(bad, builder_meter))
    assert not funded_bad["returned"] and funded_bad["exception"] == "Rejected"
    assert builder_meter.total-before == 421 and builder.n == 0
    assert all(value == 0 for row in builder.sums for value in row)
    builder.add(good, builder_meter)
    external = tuple(range(len(A.CATEGORIES)))
    before_freeze = builder_meter.total
    frozen = builder.freeze(builder_meter, external)
    assert builder_meter.total-before_freeze == 24576
    assert frozen.setup_resources == tuple(v+builder_meter.by_category[c] for v,c in zip(external,A.CATEGORIES))
    return dict(feature_identity_rejections=identities, cached_identity_no_rehash=True,
        driver_source_hash_changes_scope=True, exact_range_matrix_rejected=altered_check,
        zero_budget_row_checks=row_checks, funded_invalid_row=dict(charged=421, no_state_update=True),
        freeze=dict(charged=24576, includes_own_charges=True, setup_resources=frozen.setup_resources),
        source_hashes=hashes, principal_research90_credit_seconds=0)


if __name__ == "__main__":
    result = main()
    with (HERE / "profile_binding_probe_results_v2.json").open("x") as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(result, sort_keys=True, indent=2))
