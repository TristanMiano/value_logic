"""Targeted same-model nonblind review of the frozen analytic comparator v2.

No solver or broad experiment rerun. Reconstructs saved classes, meters,
identity, population agreement and selections. Instruments the construction
prefix using saved representative fixtures and stops before reference access.
Unmeasured reviewer time; zero principal Research90 credit.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import isqrt
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
WORKLOG = HERE.parent.parent
ROOT = WORKLOG.parents[2]
RUN = WORKLOG / "development/analytic_profile_run_v2"
REFERENCE = WORKLOG / "development/run_v3/population_rows.jsonl"
SNAPSHOT = RUN / "sources"
SPEC = importlib.util.spec_from_file_location("analytic_review_frozen_v2", SNAPSHOT / "07_analytic_profile.py")
P = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = P
SPEC.loader.exec_module(P)
D, C, A = P.D, P.C, P.A


def read(path):
    return json.loads(path.read_text())


def filehash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("ascii")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def zero():
    return Counter({c: 0 for c in A.CATEGORIES})


def meter_checks(meter):
    assert meter["total"] == sum(meter["by_category"].values()) == sum(meter["operations"].values())
    assert meter["remaining"] == meter["limit_total"] - meter["total"] >= 0
    categories = zero()
    for key, units in meter["operations"].items():
        categories[key.split(".", 1)[0]] += units
    assert categories == meter["by_category"]
    assert all(0 <= meter["by_category"][c] <= meter["category_limits"][c] for c in A.CATEGORIES)
    if "partitions" in meter:
        assert sum(m["limit_total"] for m in meter["partitions"]) <= meter["limit_total"]
        assert sum(m["total"] for m in meter["partitions"]) == meter["total"]
        merged = zero()
        for part in meter["partitions"]:
            meter_checks(part)
            merged.update(part["by_category"])
        assert merged == meter["by_category"]


def main():
    profile = read(RUN / "analytic_profile.json")
    result = read(RUN / "result.json")
    plan = read(WORKLOG / "development/analytic_profile_plan_v2.json")
    expected_hashes = profile["source_hashes"]
    assert expected_hashes == result["source_hashes"] == profile["core"]["source_hashes"]
    assert expected_hashes["07_analytic_profile.py"] == plan["source_sha256"] == "3acc5db6d65c6dcec75c3d7c46bd648d2f17371102211d0c15e3cdc787aae209"
    for name, expected in expected_hashes.items():
        assert filehash(SNAPSHOT / name) == filehash(ROOT / "v3/checks" / name) == expected
        population_source = REFERENCE.parent / "sources" / name
        if population_source.exists():
            assert filehash(population_source) == expected
    assert datetime.fromisoformat(plan["frozen_utc"]) < datetime.fromisoformat(profile["frozen_utc_before_reference_read"])
    assert result["reference_sha256"] == filehash(REFERENCE)
    assert profile["version"] == result["version"] == P.VERSION
    assert tuple(D.PRIMES) == (17, 31, 47, 61, 97)
    assert profile["law"] == D.LAW == "uniform-248-public-euler-queries-v1"

    core = profile["core"]
    assert len(canonical(core)) == profile["core_bytes"] == 5680 <= 8*C.PROFILE_WORD_BOUND
    assert digest(core) == profile["identity"] == result["profile_id"] == "a084e5129427a85fbaedf445205062ebdfb242a7a84b2b4cd9f3fb930ae0fa54"
    for key in ("version", "source_hashes", "law", "size", "means", "total_resources"):
        assert core[key] == profile[key]
    assert core["classes"] == [{key:g[key] for key in ("prime", "kind", "size", "positive", "negative", "feature_sums")} for g in profile["classes"]]

    resource_sum = zero()
    predicted_sums = [[0]*14 for _ in range(6)]
    class_rows, representatives = [], {}
    total_size = total_positive = 0
    for group in profile["classes"]:
        prime, kind = group["prime"], group["kind"]
        assert prime >= 5 and prime % 2 == 1
        assert all(prime % divisor for divisor in range(2, isqrt(prime)+1))
        n = (prime-1)//2
        minus_positive = int(n%2 == 0)
        expected = {"one": (1, 1, 1), "minus_one": (prime-1, 1, minus_positive), "ordinary": (2, prime-3, n-1-minus_positive)}[kind]
        assert (group["representative"], group["size"], group["positive"]) == expected
        assert group["negative"] == group["size"]-group["positive"]
        total_size += group["size"]
        total_positive += group["positive"]
        reconstructed = []
        for pi, (policy, run) in enumerate(zip(C.CATALOGUE, group["representative_runs"])):
            assert run["policy"] == policy.name and run["initial_report"] == "1/2"
            meter_checks(run["meter"])
            assert run["meter"]["limit_total"] == 1024 and run["meter"]["denials"] == 0
            resource_sum.update(run["meter"]["by_category"])
            if run["status"] == "checked_answer":
                assert run["answer"] is not None and run["action"] == run["answer"]["answer"]
                errors = (0, 0, 0)
            elif policy.unresolved_action == 0:
                errors = (0, group["positive"], 0)
            elif policy.unresolved_action == 1:
                errors = (group["negative"], 0, 0)
            else:
                errors = (0, 0, group["size"])
            row = errors + tuple(group["size"]*run["meter"]["by_category"][c] for c in A.CATEGORIES)
            reconstructed.append(list(row))
            for j, value in enumerate(row):
                predicted_sums[pi][j] += value
            representatives[(prime, kind, policy.name)] = run
        assert reconstructed == group["feature_sums"]
        class_rows.append({key:group[key] for key in ("prime", "kind", "representative", "size", "positive", "negative")})
    assert total_size == profile["size"] == 248 and total_positive == 124
    assert len(class_rows) == profile["class_count"] == result["class_count"] == 15
    assert len(representatives) == profile["representative_policy_runs"] == result["representative_policy_runs"] == 90
    assert resource_sum == profile["representative_execution_resources"]
    assert sum(resource_sum.values()) == 9223

    source_words = sum(((SNAPSHOT / name).stat().st_size+7)//8 for name in expected_hashes)
    model = profile["model_meter"]
    meter_checks(model)
    expected_model_ops = {
        "profile.analytic_registry_read_hash_words": 2*source_words,
        "profile.source_bound_class_model_construction": 2048,
        "storage.class_model_retention": 1024,
        "check.prime_hypothesis_loop_setup": 4*5,
        "check.trial_division_for_prime_hypothesis": 2*sum(isqrt(p)-1 for p in D.PRIMES),
        "profile.class_size_label_count_and_query_construction": 16*15,
        "profile.class_feature_and_sum_arithmetic": 4*14*90,
        "storage.class_feature_read_write": 2*14*90,
        "profile.analytic_profile_finalize_validate_hash": 2*8192,
        "storage.analytic_profile_retention": 8192,
    }
    assert model["operations"] == expected_model_ops and model["events"] == 138 and model["denials"] == 0
    assert model["total"] == 55358
    acquisition = resource_sum.copy()
    acquisition.update(model["by_category"])
    assert acquisition == profile["total_resources"] == core["total_resources"]
    assert sum(acquisition.values()) == result["total_procurement_units"] == 64581

    raw = [json.loads(line) for line in REFERENCE.read_text().splitlines()]
    expected_population = tuple((p, a) for p in (17,31,47,61,97) for a in range(1, p))
    assert len(raw) == 248
    by_class = defaultdict(lambda: [[0]*14 for _ in range(6)])
    class_labels = Counter()
    actual_sums = [[0]*14 for _ in range(6)]
    resource_completion_rows = 0
    for index, row in enumerate(raw):
        prime, base = expected_population[index]
        assert row["index"] == index and row["query"] == {"a":base, "n":(prime-1)//2, "m":prime, "r":1}
        kind = "one" if base == 1 else "minus_one" if base == prime-1 else "ordinary"
        assert row["label"] in (0,1)
        class_labels[(prime, kind)] += row["label"]
        for pi, policy in enumerate(C.CATALOGUE):
            representative = representatives[(prime, kind, policy.name)]
            fs = row["features"][pi]
            assert fs[3:] == [representative["meter"]["by_category"][c] for c in A.CATEGORIES]
            assert row["statuses"][pi] == representative["status"]
            assert row["initial_reports"][pi] == representative["initial_report"]
            action = row["actions"][pi]
            assert fs[:3] == [int(action==1 and row["label"]==0), int(action==0 and row["label"]==1), int(action is None)]
            for j, value in enumerate(fs):
                by_class[(prime, kind)][pi][j] += value
                actual_sums[pi][j] += value
            resource_completion_rows += 1
    assert resource_completion_rows == result["checked_query_policy_resource_and_completion_rows"] == 1488
    for group in profile["classes"]:
        key = (group["prime"], group["kind"])
        assert class_labels[key] == group["positive"]
        assert by_class[key] == group["feature_sums"]
    assert actual_sums == predicted_sums
    means = tuple(tuple(F(value, 248) for value in row) for row in actual_sums)
    assert [list(map(str,row)) for row in means] == profile["means"]
    population_exact = read(REFERENCE.parent / "population_exact.json")
    assert all(tuple(F(x) for x in population_exact["feature_means"][p.name]) == means[i] for i,p in enumerate(C.CATALOGUE))

    selections = []
    for selection in result["selections"]:
        prices = D.PRICES[selection["price"]]
        meter = selection["meter"]
        meter_checks(meter)
        assert meter["operations"] == {"assessment.analytic_price_readout_multiply_add_and_max": 4*6*14+4*6+128, "storage.analytic_profile_price_word_read": 3*6*14}
        assert meter["total"] == 740 and meter["denials"] == 0
        costs = tuple(sum((price*value for price,value in zip(prices,row)), F(0)) for row in means)
        assert {p.name:str(costs[i]) for i,p in enumerate(C.CATALOGUE)} == selection["exact_costs"]
        chosen = min(range(6), key=lambda i:(costs[i], i))
        assert selection["policy"] == C.CATALOGUE[chosen].name
        setup = sum((prices[j+3]*acquisition[c] for j,c in enumerate(A.CATEGORIES)), F(0))
        online = sum((prices[j+3]*meter["by_category"][c] for j,c in enumerate(A.CATEGORIES)), F(0))
        assert F(selection["setup_cost"]) == setup and F(selection["assessment_cost"]) == online
        for horizon in (64,10000):
            assert F(selection[f"all_in_gain_H{horizon}"]) == horizon*(costs[0]-costs[chosen])-setup-online
        selections.append({key:selection[key] for key in ("price","policy","setup_cost","assessment_cost","all_in_gain_H64","all_in_gain_H10000")})
    assert len(selections) == len(D.PRICES) == 6

    identity_sensitivity = []
    for key in ("means", "class_count", "resources", "driver_source", "analytic_source", "law"):
        candidate = deepcopy(core)
        if key == "means": candidate["means"][0][0] = "1"
        elif key == "class_count": candidate["classes"][0]["positive"] += 1
        elif key == "resources": candidate["total_resources"]["profile"] += 1
        elif key == "driver_source": candidate["source_hashes"]["07_paid_reasoning_development.py"] = "0"*64
        elif key == "analytic_source": candidate["source_hashes"]["07_analytic_profile.py"] = "0"*64
        else: candidate["law"] = "different_population_law"
        assert digest(candidate) != profile["identity"]
        identity_sensitivity.append(key)

    # Exercise the actual construction prefix with saved representative fixtures,
    # proving that no retained reference row is needed to produce this core.
    probe_out = HERE / "construction_before_reference_v2"
    original_run, original_read, original_write, original_argv = C.run_policy, Path.read_text, P.write, sys.argv
    events, fixture_calls = [], []
    class StopAtReference(Exception):
        pass
    def fixture(query, policy):
        prime, base = query.m, query.a
        kind = "one" if base==1 else "minus_one" if base==prime-1 else "ordinary"
        assert base == {"one":1,"minus_one":prime-1,"ordinary":2}[kind]
        assert query.n == (prime-1)//2 and query.r == 1
        fixture_calls.append((prime,kind,policy.name))
        return deepcopy(representatives[(prime,kind,policy.name)])
    def observe_write(path, value):
        if path.name == "analytic_profile.json":
            assert len(fixture_calls) == 90 and value["identity"] == profile["identity"]
            assert canonical(value["core"]) == canonical(core)
            events.append("core_frozen_and_written")
        return original_write(path,value)
    def guarded_read(path, *args, **kwargs):
        if path == REFERENCE:
            assert events == ["core_frozen_and_written"]
            stored = json.loads(original_read(probe_out / "analytic_profile.json"))
            assert stored["core"] == core and stored["identity"] == profile["identity"]
            events.append("first_reference_read_attempt")
            raise StopAtReference()
        return original_read(path,*args,**kwargs)
    try:
        C.run_policy, Path.read_text, P.write = fixture, guarded_read, observe_write
        sys.argv = [str(SNAPSHOT / "07_analytic_profile.py"), "--out", str(probe_out), "--reference", str(REFERENCE)]
        try:
            P.main()
        except StopAtReference:
            pass
        else:
            raise AssertionError("Probe failed to stop at the reference boundary.")
    finally:
        C.run_policy, Path.read_text, P.write, sys.argv = original_run, original_read, original_write, original_argv
    assert events == ["core_frozen_and_written", "first_reference_read_attempt"]
    assert len(fixture_calls) == len(set(fixture_calls)) == 90
    for name, expected in expected_hashes.items():
        assert filehash(ROOT / "v3/checks" / name) == expected

    evidence_paths = [RUN/"analytic_profile.json", RUN/"result.json", REFERENCE, REFERENCE.parent/"population_exact.json", WORKLOG/"development/analytic_profile_plan_v1.json", WORKLOG/"development/analytic_profile_plan_v2.json"]
    return {
        "status": "ANALYTIC_V2_SAVED_NUMERICS_IDENTITY_CHARGES_AND_PRE_REFERENCE_FREEZE_PASS",
        "review_type": "Same-model targeted nonblind independent source/evidence review, with a separately delegated class/resource proof review.",
        "source_hashes": expected_hashes,
        "source_snapshots_and_root_match_at_start_and_finish": True,
        "core_identity": profile["identity"], "core_bytes": profile["core_bytes"],
        "identity_sensitive_to": identity_sensitivity,
        "class_counts": class_rows,
        "population_size": 248, "positive_labels": 124, "resource_completion_rows_reconstructed": resource_completion_rows,
        "all_class_sums_and_feature_means_match": True,
        "representative_policy_runs": 90, "representative_resource_units": sum(resource_sum.values()),
        "model_operations": expected_model_ops, "model_resource_units": model["total"],
        "profile_procurement_resources": dict(acquisition), "profile_procurement_units": sum(acquisition.values()),
        "each_readout_units": 740, "six_readout_units": 4440,
        "selections": selections,
        "construction_prefix_probe": {"events": events, "saved_fixtures_used": len(fixture_calls), "solver_calls_executed": 0, "reference_rows_read": 0, "core_exactly_matches_saved": True},
        "boundaries": ["Theorems and source-specific path-class proof are prerequisites, not newly machine-checked algebra.", "Human theorem/program development and physical Python/CPU time are unquantified.", "The 1488-row retained-reference validation is an external development audit; it is not included in the 64581-unit profile bill.", "The numerical profile is frozen before the reference is opened; later assertion success gates the harness PASS result but does not update means or selection arithmetic.", "Core identity binds scientific numerical fields; raw snapshots and timestamps remain unbound audit instrumentation.", "This is a fixed same-process comparator, not an arbitrary received-profile admission API.", "No new individual label oracle is inferred from class positive counts."],
        "evidence_sha256": {str(path.relative_to(ROOT)):filehash(path) for path in evidence_paths},
        "principal_research90_credit_seconds": 0,
    }


if __name__ == "__main__":
    result = main()
    with (HERE / "analytic_reconstruction_results_v2.json").open("x") as stream:
        json.dump(result,stream,indent=2,sort_keys=True)
        stream.write("\n")
    print(json.dumps({key:value for key,value in result.items() if key not in ("class_counts","evidence_sha256","model_operations")},indent=2,sort_keys=True))
