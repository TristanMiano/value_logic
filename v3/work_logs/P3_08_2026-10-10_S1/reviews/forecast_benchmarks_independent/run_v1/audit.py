"""Independent sealed-record arithmetic, never imports a P3-08 calculator.

Same-model nonblind DEVELOPMENT audit, 2026-10-10; zero principal credit.
Only reads sealed inputs/outputs and computes evaluator-side diagnostics.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import argparse
import ast
import gzip
import hashlib
import json
import shutil


EXPERTS = ("constant_unsat", "constant_sat", "sparse_sat",
           "unit_consistency_sat", "pure_coverage_sat", "literal_balance_sat")
COMPARISONS = ("base_minus_half", "base_minus_best_fixed_expert",
               "base_minus_static_equal_exact", "base_minus_static_equal_dyadic",
               "live_minus_matched_half", "live_minus_matched_best_expert",
               "live_minus_matched_static_equal_exact", "live_minus_matched_static_equal_dyadic")
CHECKS = Counter()


def require(condition, name):
    if not condition:
        raise AssertionError(name)
    CHECKS[name] += 1


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def freeze(value):
    return tuple(map(freeze, value)) if isinstance(value, list) else value


def total(predictions, truths):
    # Binary y makes y**2=y. This quadratic expansion is an independently
    # coded Brier total, rather than a call to the production analyzer.
    return sum((p*p - 2*p*y + y for p, y in zip(predictions, truths)), Fraction(0))


def binary_advice(query):
    clauses = query["clauses"]
    literals = [v for clause in clauses for v in clause]
    positive = {v for v in literals if v > 0}
    negative = {-v for v in literals if v < 0}
    units = {clause[0] for clause in clauses if len(clause) == 1}
    pure_literals = (positive-negative) | {-v for v in negative-positive}
    return (0, 1, int(len(clauses) <= 3*query["variables"]),
            int(not any(-v in units for v in units)),
            int(all(any(v in pure_literals for v in clause) for clause in clauses)),
            int(sum(v > 0 for v in literals) >= sum(v < 0 for v in literals)))


def signs(rows, fields):
    result = {}
    for field in fields:
        values = [Fraction(*r[field]) for r in rows]
        result[field] = {"strictly_better": sum(v < 0 for v in values),
                         "equal": sum(v == 0 for v in values),
                         "strictly_worse": sum(v > 0 for v in values)}
    return result


def reconstruct(record, tapes, truths, private_scores):
    episode, config = record["episode"], record["configuration"]
    trace, contract = episode["trace"], episode["contract"]
    tape, labels = tapes[record["scenario"]], truths[record["scenario"]]
    require(episode["status"] == "success" and len(trace) == len(tape) == len(labels)
            == contract["horizon"], "complete_horizon")
    require(config["hard"] is episode["hard_enabled"], "fixed_hard_mode")
    require(contract["expert_count"] == 6 and contract["action_bits"] == 16,
            "published_expert_and_precision_domain")
    require(episode["hard_state"]["withdrawals"] == 0
            and episode["hard_state"]["generation"] == 0
            and episode["hard_state"]["conflicts"] == 0, "fixed_epoch_no_conflict")
    denominator = 2**contract["action_bits"]
    block_size = contract["block_size"]
    first_weights = [2**contract["state_bits"]] * 6
    require(episode["blocks"][0]["weights_before"] == first_weights,
            "initial_equal_weights")
    known, invoice_at = {}, 0
    base, live, means, dyadics, mask, advice_rows = [], [], [], [], [], []
    new_selected = known_selected = 0
    for i, (row, query, y) in enumerate(zip(trace, tape, labels)):
        require(type(y) is int and y in (0, 1), "binary_truth")
        key = (query["semantics_version"], query["source_version"], query["variables"],
               freeze(query["clauses"]))
        scope = tuple(row["scope"])
        require(row["index"] == i and row["query_id"] == query["query_id"]
                and freeze(row["claim_key"]) == key, "trace_public_query_binding")
        require(scope == tuple(episode["scope"]) and scope[:2] == key[:2],
                "trace_scope_binding")
        hard = config["hard"] and (scope, key) in known
        require(row["hard_before"] == ("checked" if hard else "unresolved"),
                "chronological_preissue_hard_mask")
        require(row["base_q"][1] == row["emitted_q"][1] == denominator,
                "unreduced_dyadic_denominator")
        q = Fraction(*row["base_q"])
        require(0 <= q <= 1, "forecast_probability_bounds")
        emitted = Fraction(known[(scope, key)]) if hard else q
        require(Fraction(*row["emitted_q"]) == emitted, "preissue_forecast_override")
        if hard:
            require(known[(scope, key)] == y, "prior_checked_truth_agrees")
        advice = binary_advice(query)
        require(tuple(row["advice"]) == advice, "six_public_feature_experts")
        require(all(type(a) is int and a in (0, 1) for a in row["advice"]),
                "binary_advice")
        k = sum(advice)
        mean, dyadic = Fraction(k, 6), Fraction((denominator*k)//6, denominator)
        weights = episode["blocks"][i//block_size]["weights_before"]
        require(len(weights) == 6 and all(type(w) is int and w > 0 for w in weights),
                "stored_weight_domain")
        require(row["base_q"][0] == denominator*sum(w*a for w,a in zip(weights,advice))//sum(weights),
                "stored_weight_forecast_formula")
        if i < block_size:
            require(q == dyadic, "static_dyadic_is_initial_broker_prediction")
        require(0 <= mean-dyadic < Fraction(1, denominator), "dyadic_floor_error")
        mask.append(hard)
        base.append(q)
        live.append(emitted)
        means.append(mean)
        dyadics.append(dyadic)
        advice_rows.append(advice)
        selected = row["selected"]
        require(type(selected) is bool and selected == (i % block_size ==
                episode["blocks"][i//block_size]["selected"]), "selected_position")
        if selected:
            receipt = episode["invoices"][invoice_at]
            invoice_at += 1
            require(receipt["query_id"] == query["query_id"] and freeze(receipt["claim_key"]) == key
                    and receipt["status"] == "success" and receipt["checked"] is True
                    and receipt["provider"] == "bounded_cnf_checked"
                    and receipt["provider_version"] == "p308-bounded-cnf-services-v1.1"
                    and receipt["answer"] == row["purchased_label"] == y, "selected_receipt_binding")
            if hard:
                known_selected += 1
            else:
                new_selected += 1
            if config["hard"]:
                known[(scope, key)] = y
        else:
            require(row["purchased_label"] is None, "no_unselected_receipt")
        after = config["hard"] and (scope, key) in known
        require(row["hard_after"]["status"] == ("checked" if after else "unresolved")
                and row["hard_after"]["answer"] == (known[(scope,key)] if after else None),
                "postissue_hard_state")
    require(invoice_at == len(episode["invoices"]) == contract["quota"], "complete_quota")
    require(len(known) == episode["hard_state"]["active_entries"]
            == episode["hard_state"]["entries_retained"] <= contract["hard_capacity"],
            "terminal_hard_store")
    hard_count = sum(mask)
    matched = lambda predictions: [Fraction(y) if h else p for h,p,y in zip(mask,predictions,labels)]
    experts = dict(zip(EXPERTS, [sum(a[j] != y for a,y in zip(advice_rows,labels)) for j in range(6)]))
    matched_experts = dict(zip(EXPERTS, [sum((not h) and a[j] != y
        for h,a,y in zip(mask,advice_rows,labels)) for j in range(6)]))
    b, l = total(base,labels), total(live,labels)
    half, mhalf = Fraction(len(labels),4), Fraction(len(labels)-hard_count,4)
    exact, dyadic = total(means,labels), total(dyadics,labels)
    mexact, mdyadic = total(matched(means),labels), total(matched(dyadics),labels)
    best, mbest = min(experts.values()), min(matched_experts.values())
    expected = {"run_id":record["run_id"], "scenario":record["scenario"], "configuration":config,
        "horizon":len(labels), "current_hard_before_issue":hard_count,
        "base_brier":pair(b), "live_brier":pair(l), "constant_half_brier":pair(half),
        "matched_hard_half_brier":pair(mhalf), "fixed_expert_brier":experts,
        "matched_hard_expert_brier":matched_experts, "hindsight_best_expert_brier":best,
        "matched_hindsight_best_expert_brier":mbest, "base_minus_half":pair(b-half),
        "base_minus_best_fixed_expert":pair(b-best), "live_minus_matched_half":pair(l-mhalf),
        "live_minus_matched_best_expert":pair(l-mbest), "static_equal_exact_brier":pair(exact),
        "static_equal_dyadic_brier":pair(dyadic), "matched_static_equal_exact_brier":pair(mexact),
        "matched_static_equal_dyadic_brier":pair(mdyadic), "base_minus_static_equal_exact":pair(b-exact),
        "base_minus_static_equal_dyadic":pair(b-dyadic),
        "live_minus_matched_static_equal_exact":pair(l-mexact),
        "live_minus_matched_static_equal_dyadic":pair(l-mdyadic),
        "free_perfect_foresight_brier":[0,1], "free_oracle_is_deployable_control":False}
    private = private_scores[record["run_id"]]
    require(private["base_issued_brier"] == pair(b) and private["issued_brier"] == pair(l),
            "independent_brier_matches_prior_private_score")
    require(l <= b, "valid_hard_override_never_increases_brier")
    diagnostics = {"new_selected_after_issue":new_selected, "already_known_selected":known_selected,
        "best_fixed_experts":[name for name,value in experts.items() if value == best],
        "best_matched_experts":[name for name,value in matched_experts.items() if value == mbest]}
    return expected, diagnostics


def run(repo, out):
    repo, out = repo.resolve(), out.resolve()
    require(not out.exists(), "fresh_review_output")
    out.mkdir(parents=True)
    session = repo/"v3/work_logs/P3_08_2026-10-10_S1"
    archive = session/"development/common_v2/run"
    archived_source = session/"development/common_v2/source"
    benchmark = session/"development/forecast_benchmarks"
    tracked = set()
    def track(path):
        tracked.add(path)
        return path
    public_seal = read(track(archive/"public_seal.json"))
    private_seal = read(track(archive/"private/seal.json"))
    for directory, seal in ((archive,public_seal),(archive/"private",private_seal)):
        for entry in seal["files"]:
            path = track(directory/entry["path"])
            require(sha(path) == entry["sha256"], "sealed_payload_hash")
            require("bytes" not in entry or path.stat().st_size == entry["bytes"], "sealed_payload_bytes")
    before = read(archive/"source_before.json")["sources"]
    after = read(archive/"source_after.json")["sources"]
    require(before == after, "archived_policy_source_closure_unchanged")
    for entry in before:
        path = track(archived_source/entry["path"])
        require(sha(path) == entry["sha256"] and path.stat().st_size == entry["bytes"],
                "archived_policy_source_hash")
        target = out/"source"/entry["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path,target)
    for filename in ("analysis_contract.md", "v2_amendment.md"):
        source = track(benchmark/filename)
        shutil.copyfile(source, out/filename)
    manifest = read(track(benchmark/"run_v2/manifest.json"))
    for entry in manifest["files"]:
        path = track(benchmark/"run_v2"/entry["path"])
        require(sha(path) == entry["sha256"] and path.stat().st_size == entry["bytes"],
                "benchmark_v2_manifest")
    analyzer = track(repo/"v3/experiments/p308_forecast_benchmarks.py")
    require(analyzer.read_bytes() == (benchmark/"run_v2/p308_forecast_benchmarks.py").read_bytes(),
            "current_benchmark_equals_saved_v2")
    shutil.copyfile(analyzer,out/"source/v3/experiments/p308_forecast_benchmarks.py")
    for origin in (Path(__file__).resolve(), Path(__file__).with_name("plan.md").resolve()):
        track(origin)
        shutil.copyfile(origin,out/origin.name)
    def observed_manifest():
        return [{"path":str(p.relative_to(repo)), "bytes":p.stat().st_size,"sha256":sha(p)}
                for p in sorted(tracked)]
    observed_before = observed_manifest()
    (out/"input_manifest_before.json").write_text(json.dumps(observed_before,indent=2)+"\n")
    # Bind public advice labels by parsing the tuple, without importing CNF.
    tree = ast.parse((archived_source/"v3/experiments/p308_cnf.py").read_text())
    names = [ast.literal_eval(node.value) for node in tree.body if isinstance(node,ast.Assign)
             and any(isinstance(t,ast.Name) and t.id == "EXPERT_NAMES" for t in node.targets)]
    require(names == [EXPERTS], "expert_name_order")
    truth_record = read(archive/"private/truth.json")
    require(truth_record["public_seal_sha256"] == sha(archive/"public_seal.json")
            and truth_record["created_after_public_seal"] is True
            and truth_record["evaluator_only"] is True, "private_truth_public_binding")
    truths = truth_record["answers"]
    tapes = read(archive/"public_inputs.json")["tapes"]
    scores = read(archive/"private/scores.json")["runs"]
    private_scores = {r["run_id"]:r for r in scores}
    public_index = read(archive/"public_index.json")
    index = {r["run_id"]:r for r in public_index["records"]}
    require(len(index) == public_index["count"] == len(public_index["records"]), "unique_public_index")
    sealed_records = []
    with gzip.open(archive/"public_records.jsonl.gz","rt") as stream:
        for line in stream:
            record = json.loads(line)
            entry = index[record["run_id"]]
            require(hashlib.sha256(line.rstrip("\n").encode()).hexdigest() == entry["record_sha256"],
                    "individual_public_record_hash")
            require(entry["configuration"] == record["configuration"] and entry["scenario"] == record["scenario"],
                    "public_index_record_binding")
            sealed_records.append(record)
    require(len(sealed_records) == len({r["run_id"] for r in sealed_records}) == len(index),
            "exact_public_record_membership")
    records = [r for r in sealed_records if r["configuration"]["kind"] == "broker"]
    result = read(benchmark/"run_v2/results.json")
    reported = {r["run_id"]:r for r in result["records"]}
    require(set(reported) == {r["run_id"] for r in records} and len(reported) == len(result["records"])
            == result["record_count"] == 63, "exact_benchmark_record_membership")
    for field, path in (("public_seal_sha256",archive/"public_seal.json"),
                        ("private_seal_sha256",archive/"private/seal.json"),
                        ("private_truth_sha256",archive/"private/truth.json")):
        require(result[field] == sha(path), "benchmark_result_seal_binding")
    require(result["records_are_not_independent_trials"] is True
            and result["policy_runs_added"] == result["new_paid_benchmark_deployments"] == 0,
            "benchmark_scope_flags")
    reconstructed, diagnostics, grouped = [], {}, defaultdict(list)
    trace_positions = 0
    for record in records:
        expected, detail = reconstruct(record,tapes,truths,private_scores)
        require(set(expected) == set(reported[record["run_id"]]), "exact_benchmark_field_membership")
        for field,value in expected.items():
            require(reported[record["run_id"]][field] == value, "benchmark_field:"+field)
        reconstructed.append(expected)
        diagnostics[record["run_id"]] = detail
        config = record["configuration"]
        grouped[(record["scenario"],config["selector"],config["seed"])].append((record,expected))
        trace_positions += len(record["episode"]["trace"])
    require(signs(reconstructed,COMPARISONS) == result["summary"], "all_record_summary")
    require(len(grouped) == 18, "eighteen_configurations")
    compact = []
    for key,members in sorted(grouped.items()):
        scenario, selector, seed = key
        require(len(members) == (4 if selector == "uniform" else 3), "source_variant_count")
        first_trace = members[0][0]["episode"]["trace"]
        for record,_ in members:
            trace = record["episode"]["trace"]
            require([(r["base_q"],r["advice"],r["selected"],r["purchased_label"],r["propensity"])
                     for r in trace] == [(r["base_q"],r["advice"],r["selected"],r["purchased_label"],r["propensity"])
                     for r in first_trace], "configuration_base_path_equivalence")
        item = {"scenario":scenario, "selector":selector, "seed":seed,
                "source_record_ids":[r["run_id"] for r,_ in members]}
        for hard,tag in ((False,"hard_off"),(True,"hard_on")):
            matches = [(r,e) for r,e in members if r["configuration"]["hard"] is hard]
            require(len(matches) == (2 if hard or selector == "uniform" else 1), "hard_mode_variant_count")
            chosen = matches[0][1]
            for _,other in matches:
                require({k:v for k,v in other.items() if k not in ("run_id","configuration")} ==
                        {k:v for k,v in chosen.items() if k not in ("run_id","configuration")},
                        "within_hard_mode_score_equivalence")
            item[tag] = chosen
        compact.append(item)
    compact_summary = {
        "base_18_configurations":signs([r["hard_off"] for r in compact],COMPARISONS[:4]),
        "live_hard_off_18_configurations":signs([r["hard_off"] for r in compact],COMPARISONS[4:]),
        "live_hard_on_18_configurations":signs([r["hard_on"] for r in compact],COMPARISONS[4:])}
    adverse = [{"scenario":r["scenario"],"selector":r["selector"],"seed":r["seed"],
                "hard_before_count":r["hard_on"]["current_hard_before_issue"],
                **{field:r["hard_on"][field] for field in COMPARISONS[4:]}}
               for r in compact if any(Fraction(*r["hard_on"][field]) > 0 for field in COMPARISONS[4:])]
    observed_after = observed_manifest()
    require(observed_before == observed_after, "all_observed_sources_and_inputs_unchanged")
    (out/"input_manifest_after.json").write_text(json.dumps(observed_after,indent=2)+"\n")
    output = {"stage":"DEVELOPMENT", "version":"forecast-independent-v1", "pass":True,
        "principal_credit_seconds":0, "policy_runs_added":0, "private_truth_reads_authorized":True,
        "public_record_count":len(sealed_records), "broker_record_count":len(records),
        "trace_positions_checked":trace_positions, "configuration_count":len(compact),
        "configurations_are_not_independent_trials":True,
        "check_counts":dict(sorted(CHECKS.items())), "total_checks":sum(CHECKS.values()),
        "all_record_summary":signs(reconstructed,COMPARISONS), "compact_summary":compact_summary,
        "compact_configurations":compact, "hard_on_adverse_configurations":adverse,
        "record_diagnostics":diagnostics, "reconstructed_records":reconstructed}
    (out/"results.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({k:output[k] for k in ("pass","total_checks","trace_positions_checked",
                     "configuration_count","compact_summary","hard_on_adverse_configurations")},indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,default=Path.cwd())
    parser.add_argument("--out",type=Path,required=True)
    args = parser.parse_args()
    try:
        run(args.repo,args.out)
    except Exception as exc:
        if args.out.exists():
            (args.out/"failure.json").write_text(json.dumps({"pass":False,"error":repr(exc),
                "checks_before_failure":dict(CHECKS)},indent=2)+"\n")
        raise
