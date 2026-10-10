"""Independent read-only DEVELOPMENT audit of sealed common_v2 records.

Same-model, nonblind reviewer; no policy imports or policy reruns. The saved
truth tape is the evaluator target, not an independently re-proved SAT oracle.
Only this review directory receives output. Zero principal research credit.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = HERE.parent.parent / "development/common_v2"
RUN = BASE / "run"
checks = []


def check(name, condition):
    checks.append({"name": name, "pass": bool(condition)})
    if not condition:
        raise AssertionError(name)


def read(path):
    return json.loads(path.read_text())


def pair(value):
    value = F(value)
    return [value.numerator, value.denominator]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def operation_counter(meter):
    return Counter({(x["category"], x["operation"]): x["units"]
                    for x in meter["operations"]})


def validate_meter(meter, name):
    ops = meter["operations"]
    check(name + ":unique_operations", len({(x["category"], x["operation"]) for x in ops}) == len(ops))
    check(name + ":operation_sum", sum(x["units"] for x in ops) == meter["total"])
    check(name + ":category_sum", sum(meter["by_category"].values()) == meter["total"])
    for category, total in meter["by_category"].items():
        check(name + ":category_" + category,
              sum(x["units"] for x in ops if x["category"] == category) == total)


def metrics(trace, truth):
    actual = Counter()
    fractions = defaultdict(F)
    for i, (row, y) in enumerate(zip(trace, truth)):
        check("ordered_row:" + str(i), row["index"] == i)
        action, base_action = row["terminal_action"], row["base_terminal"]
        q, q0 = F(*row["emitted_q"]), F(*row["base_q"])
        actual["terminal_errors"] += action != y
        actual["base_terminal_errors"] += base_action != y
        actual["false_positives"] += action == 1 and y == 0
        actual["false_negatives"] += action == 0 and y == 1
        actual["known_wrong"] += row["hard_after"]["status"] == "checked" and row["hard_after"]["answer"] != y
        if row["purchased_label"] is not None:
            check("purchased_truth:" + str(i), row["purchased_label"] == y)
        fractions["issued_brier"] += (y-q)**2
        fractions["base_issued_brier"] += (y-q0)**2
        if not row["selected"]:
            fractions["lottery_mean_diagnostic"] += q if y == 0 else 1-q
            fractions["base_lottery_mean_diagnostic"] += q0 if y == 0 else 1-q0
    return dict(actual) | {k: pair(v) for k, v in fractions.items()}


def purpose_summary(episode):
    result = defaultdict(lambda: {"calls": 0, "success": 0, "failure": 0,
                                  "units": 0, "failed_units": 0, "indices": []})
    for invoice in episode["invoices"]:
        row = result[invoice["purpose"]]
        failed = invoice["status"] != "success"
        row["calls"] += 1
        row["success"] += not failed
        row["failure"] += failed
        row["units"] += invoice["resources"]["total"]
        row["failed_units"] += failed * invoice["resources"]["total"]
        row["indices"].append(invoice["index"])
    return dict(result)


def run():
    plan = read(HERE / "plan.json")
    for source in plan["manifest"]:
        path = ROOT / source["path"]
        check("bound_source:" + source["path"], digest(path) == source["sha256"])
    for directory, filename in [(RUN, "public_seal.json"), (RUN / "private", "seal.json")]:
        for source in read(directory / filename)["files"]:
            path = directory / source["path"]
            check("seal:" + str(path.relative_to(BASE)), digest(path) == source["sha256"])
            if "bytes" in source:
                check("seal_size:" + source["path"], path.stat().st_size == source["bytes"])
    before, after = read(RUN / "source_before.json"), read(RUN / "source_after.json")
    check("source_versions_unchanged", before["sources"] == after["sources"])
    for source in before["sources"]:
        check("frozen_source:" + source["path"], digest(BASE / "source" / source["path"]) == source["sha256"])
    truth_file = read(RUN / "private/truth.json")
    check("truth_binds_public_seal", truth_file["public_seal_sha256"] == digest(RUN / "public_seal.json"))
    truth = truth_file["answers"]
    inputs = read(RUN / "public_inputs.json")["tapes"]
    scores_file = read(RUN / "private/scores.json")
    scores = {x["run_id"]: x for x in scores_file["runs"]}
    index_file = read(RUN / "public_index.json")
    index = {x["run_id"]: x for x in index_file["records"]}
    check("score_index_unique_count", len(scores) == len(index) == index_file["count"] == 186)
    records = {}
    total_positions = total_invoices = report_count = 0
    with gzip.open(RUN / "public_records.jsonl.gz", "rb") as archive:
        for line in archive:
            record = json.loads(line)
            rid, e = record["run_id"], record["episode"]
            check("record_hash:" + rid, sha256(line.rstrip(b"\n")).hexdigest() == index[rid]["record_sha256"])
            check("unique_record:" + rid, rid not in records)
            records[rid] = record
            check("index_score_fields:" + rid, all(scores[rid][k] == v for k, v in index[rid].items()))
            check("complete_episode:" + rid, e["status"] == "success" and len(e["trace"]) == len(truth[record["scenario"]]))
            check("purchases_count:" + rid, e["purchases"] == len(e["invoices"]) == scores[rid]["purchases"])
            check("local_source_cold:" + rid, scores[rid]["local_units"] == e["meter"]["total"] and
                  scores[rid]["source_units"] == record["common_source_invoice"]["total"] and
                  scores[rid]["cold_units"] == e["meter"]["total"] + record["common_source_invoice"]["total"])
            check("same_public_queries:" + rid, all(
                row["query_id"] == raw["query_id"] and row["claim_key"] ==
                [raw["semantics_version"], raw["source_version"], raw["variables"], raw["clauses"]]
                for row, raw in zip(e["trace"], inputs[record["scenario"]])))
            for source in record["common_sources"]:
                check("procured_source:" + rid + ":" + source["path"],
                      digest(BASE / "source" / source["path"]) == source["sha256"])
            source_bill = sum(2*((x["bytes"]+7)//8) + (x["bytes"]+72)//64 for x in record["common_sources"])
            check("procurement_arithmetic:" + rid, source_bill == scores[rid]["source_units"])
            validate_meter(record["common_source_invoice"], "source_meter:" + rid)
            validate_meter(e["meter"], "episode_meter:" + rid)
            all_provider_ops = Counter()
            for j, invoice in enumerate(e["invoices"]):
                validate_meter(invoice["resources"], "invoice_meter:" + rid + ":" + str(j))
                all_provider_ops.update(operation_counter(invoice["resources"]))
                row = next(row for row in e["trace"] if row["query_id"] == invoice["query_id"])
                y = truth[record["scenario"]][row["index"]]
                check("invoice_key_binding:" + rid + ":" + str(j), invoice["claim_key"] == row["claim_key"])
                if invoice["status"] == "success":
                    check("invoice_answer_binding:" + rid + ":" + str(j), invoice["checked"] is True and invoice["answer"] == y)
                else:
                    check("failed_invoice_no_answer:" + rid + ":" + str(j), invoice["checked"] is False and invoice["answer"] is None)
            prefix = "ordinary_provider:" if record["configuration"]["kind"] == "ordinary" else "selected_provider:"
            parent_provider = Counter({(x["category"], x["operation"][len(prefix):]): x["units"]
                for x in e["meter"]["operations"] if x["operation"].startswith(prefix)})
            check("provider_cost_exactly_absorbed:" + rid, parent_provider == all_provider_ops)
            reconstructed = metrics(e["trace"], truth[record["scenario"]])
            check("all_score_metrics:" + rid, all(scores[rid][k] == v for k, v in reconstructed.items()))
            check("known_wrong_zero:" + rid, reconstructed["known_wrong"] == 0)
            optional = record["optional_reporting"]
            if optional is None:
                check("no_optional_bill:" + rid, scores[rid]["optional_reporting_units"] is None and scores[rid]["report_audit"] is None)
            else:
                report_count += 1
                check("optional_bill:" + rid, scores[rid]["optional_reporting_units"] == optional["additional_units"])
                report, audit = optional["report"], scores[rid]["report_audit"]
                check("report_success:" + rid, report["status"] == "success")
                values = {"F": F(*reconstructed["issued_brier"]), "V": F(*reconstructed["lottery_mean_diagnostic"]), "Z": F(reconstructed["terminal_errors"])}
                diffs = {"F": F(*reconstructed["base_issued_brier"])-values["F"],
                         "V": F(*reconstructed["base_lottery_mean_diagnostic"])-values["V"],
                         "Z": reconstructed["base_terminal_errors"]-values["Z"]}
                check("report_exact_corrections:" + rid, all(diffs[k] == (F(report["corrections"][k]) if k == "Z" else F(*report["corrections"][k])) for k in diffs))
                check("report_shared_residual:" + rid, values["V"]-F(*report["live_centers"]["V"]) == values["F"]-F(*report["live_centers"]["F"]))
                coverage = {k: F(*report["intervals"][k]["lower"]) <= v <= F(*report["intervals"][k]["upper"]) for k,v in values.items()}
                check("report_audit_fields:" + rid, audit["exact_corrections_pass"] and audit["shared_residual_pass"] and audit["coverage_diagnostic_only"] == coverage and
                      audit["confidence_conflicts"] == {k:v["confidence_conflict"] for k,v in report["intervals"].items()})
            total_positions += len(e["trace"])
            total_invoices += len(e["invoices"])
    check("complete_record_set", set(records) == set(index) == set(scores))

    analysis = read(BASE / "analysis_v1/result.json")
    check("analysis_score_binding", analysis["score_sha256"] == digest(RUN / "private/scores.json"))
    check("analysis_source_binding", analysis["analysis_source_sha256"] == digest(BASE / "analysis_v1/p308_analyze.py") == digest(HERE / "p308_analyze_snapshot.py"))
    pairs = []
    for rid, record in records.items():
        method = record["configuration"]["method"]
        if method not in ("value_uniform", "value_tickets", "exact_cache", "ordinary_combo"):
            continue
        hashed_id = rid.replace("__"+method+"__", "__"+method+"_hashed__")
        a, b = record["episode"], records[hashed_id]["episode"]
        semantic_fields = ["trace", "blocks", "invoices", "weights", "random_bits_consumed", "purchases", "status", "rounds_closed"]
        if record["configuration"]["kind"] == "ordinary":
            semantic_fields += ["cost_history", "cache_hits", "successful_purchases", "known_terminal_rounds", "feedback_updates", "provider_failures"]
        for field in semantic_fields:
            check("hash_full_semantics:" + rid + ":" + field, a[field] == b[field])
        costdiff = a["meter"]["total"]-b["meter"]["total"]
        item = {"linear_run":rid, "hashed_run":hashed_id, "kind":record["configuration"]["kind"],
                "equal_fields":semantic_fields, "rounds":len(a["trace"]), "linear_minus_hashed_units":costdiff}
        pairs.append(item)
        if item["kind"] == "broker":
            match = [x for x in analysis["candidate_index_pairs"] if x["scenario"] == record["scenario"] and x["seed"] == record["configuration"]["seed"] and x["selector"] == record["configuration"]["selector"]]
            finite_id = rid.replace("__value_", "__finite_")
            for field in ["blocks", "invoices", "weights", "random_bits_consumed"]:
                check("retained_base_semantics:" + rid + ":" + field, records[finite_id]["episode"][field] == a[field])
            for row0, row1 in zip(records[finite_id]["episode"]["trace"],a["trace"]):
                check("retained_base_row:" + rid + ":" + str(row0["index"]), all(row0[k] == row1[k] for k in ["base_q","base_action","base_terminal","selected","purchased_label","propensity","advice"]))
        else:
            match = [x for x in analysis["ordinary_index_pairs"] if x["scenario"] == record["scenario"] and x["configuration"] == record["configuration"]]
        check("analysis_hash_difference:" + rid, len(match) == 1 and match[0]["linear_minus_hashed_units"] == costdiff)

    rows = list(scores.values())
    baseline_methods = {"proof_enumeration","proof_dpll","exact_enumeration","exact_dpll","exact_cache","exact_cache_hashed","no_compute_0","no_compute_1"}
    native_details = []
    for comparison in analysis["native_price_catalogue_comparisons"]:
        price, seed, scenario = F(*comparison["price"]), comparison["seed"], comparison["scenario"]
        eligible = []
        for row in rows:
            cfg = row["configuration"]
            if row["scenario"] != scenario:
                continue
            if cfg["method"] in baseline_methods:
                check("deterministic_baseline_seed", cfg["seed"] == 11)
            elif cfg["seed"] != seed:
                continue
            if cfg["method"] in {"ordinary_combo", "ordinary_combo_hashed"} and F(cfg["unit_price"]) != price:
                continue
            eligible.append(row)
        costs = {x["run_id"]: F(x["terminal_errors"]) + price*(x["local_units"]+x["source_units"]) for x in eligible}
        minimum = min(costs.values())
        ordinary = {x["run_id"]: costs[x["run_id"]] for x in eligible if x["configuration"]["kind"] == "ordinary"}
        omin = min(ordinary.values())
        check("native_price_exact:" + scenario + ":" + str(seed) + ":" + str(price),
              F(*comparison["best_catalogue_cost"]) == minimum and
              set(comparison["best_catalogue_records"]) == {k for k,v in costs.items() if v == minimum} and
              F(*comparison["best_distinct_ordinary_cost"]) == omin and
              set(comparison["best_distinct_ordinary_records"]) == {k for k,v in ordinary.items() if v == omin})
        native_details.append({"scenario":scenario,"seed":seed,"price":pair(price),"eligible_count":len(eligible),"costs":{k:pair(v) for k,v in costs.items()},"best_cost":pair(minimum)})
    groups = defaultdict(list)
    for row in rows:
        groups[(row["scenario"],row["configuration"]["method"],row["configuration"].get("unit_price","fixed"))].append(row)
    check("summary_group_count", len(groups) == len(analysis["seed_summaries"]))
    for summary in analysis["seed_summaries"]:
        group = groups[(summary["scenario"],summary["method"],summary["policy_price"])]
        check("summary_group_size", summary["run_count"] == len(group))
        for field, scorefield in [("errors","terminal_errors"),("local_units","local_units")]:
            data = [x[scorefield] for x in group]
            check("summary_values:" + str((summary["scenario"],summary["method"],summary["policy_price"],field)),
                  summary["mean_"+field] == pair(F(sum(data),len(data))) and summary["min_"+field] == min(data) and summary["max_"+field] == max(data))
        check("summary_brier", summary["mean_issued_brier"] == pair(sum((F(*x["issued_brier"]) for x in group),F())/len(group)))
    for threshold in analysis["hard_path_repricing_thresholds"]:
        cfg = threshold
        live_id = f'{cfg["scenario"]}__{cfg["method"]}__seed{cfg["seed"]}__pricefixed'
        selector = "uniform" if "uniform" in cfg["method"] else "tickets"
        base_id = f'{cfg["scenario"]}__finite_{selector}__seed{cfg["seed"]}__pricefixed'
        errors = scores[base_id]["terminal_errors"]-scores[live_id]["terminal_errors"]
        units = scores[live_id]["local_units"]-scores[base_id]["local_units"]
        check("fixed_path_threshold:" + live_id, threshold["saved_errors"] == errors and threshold["extra_units"] == units and threshold["strict_fixed_record_benefit_if_lambda_below"] == pair(F(errors,units)))

    target_ids = ["repeat_online__ordinary_combo_hashed__seed11__price0", "repeat_online__ordinary_combo_hashed__seed11__price1_100000"]
    a, b = [records[x]["episode"] for x in target_ids]
    target = {"run_ids": target_ids, "scores": [scores[x] for x in target_ids],
              "purposes": [purpose_summary(e) for e in (a,b)],
              "episode_scalars": [{k:v for k,v in e.items() if isinstance(v,(int,float,bool))} for e in (a,b)],
              "cost_histories": [e["cost_history"] for e in (a,b)]}
    target["field_differences"] = {}
    for field in sorted(a["trace"][0].keys() | b["trace"][0].keys()):
        different = [{"index":i,"lower":x.get(field),"higher":y.get(field)}
                     for i,(x,y) in enumerate(zip(a["trace"],b["trace"])) if x.get(field) != y.get(field)]
        if different:
            target["field_differences"][field] = different
    first = next(i for i,(x,y) in enumerate(zip(a["trace"],b["trace"])) if x != y)
    target["first_different_row"] = {"index":first,"lower":a["trace"][first],"higher":b["trace"][first]}
    firstblock = next(i for i,(x,y) in enumerate(zip(a["blocks"],b["blocks"])) if x != y)
    target["first_different_block"] = {"index":firstblock,"lower":a["blocks"][firstblock],"higher":b["blocks"][firstblock]}
    invoice_diffs = []
    for i in range(len(a["trace"])):
        aa = [x for x in a["invoices"] if x["index"] == i]
        bb = [x for x in b["invoices"] if x["index"] == i]
        if aa != bb:
            invoice_diffs.append({"index":i,"lower":aa,"higher":bb})
    target["invoice_differences"] = invoice_diffs
    ao, bo = operation_counter(a["meter"]), operation_counter(b["meter"])
    target["operation_cost_changes"] = [{"category":k[0],"operation":k[1],"lower":ao[k],"higher":bo[k],"delta":bo[k]-ao[k]}
        for k in sorted(ao.keys() | bo.keys()) if ao[k] != bo[k]]
    target["category_changes"] = {k:b["meter"]["by_category"][k]-v for k,v in a["meter"]["by_category"].items()}
    provider_totals = [sum(x["resources"]["total"] for x in e["invoices"]) for e in (a,b)]
    failure_totals = [sum(x["resources"]["total"] for x in e["invoices"] if x["status"] != "success") for e in (a,b)]
    target["cost_decomposition"] = {"provider_total":provider_totals,"failed_provider_total":failure_totals,
        "successful_provider_total":[t-f for t,f in zip(provider_totals,failure_totals)],
        "nonprovider_local_total":[e["meter"]["total"]-t for e,t in zip((a,b),provider_totals)]}
    key_string = lambda key: json.dumps(key,separators=(",",":"))
    successful = [{key_string(x["claim_key"]):x for x in e["invoices"] if x["status"] == "success"} for e in (a,b)]
    key_changes = []
    for key in sorted(successful[0].keys() | successful[1].keys()):
        left,right = successful[0].get(key),successful[1].get(key)
        brief = lambda x: None if x is None else {k:x[k] for k in ["index","query_id","purpose","answer"]}|{"units":x["resources"]["total"]}
        if brief(left) != brief(right):
            key_changes.append({"key":json.loads(key),"lower":brief(left),"higher":brief(right),
                "all_occurrences":[x["index"] for x in a["trace"] if key_string(x["claim_key"]) == key]})
    target["successful_key_acquisition_changes"] = key_changes
    error_positions = [i for i,x in enumerate(b["trace"]) if x["terminal_action"] != truth["repeat_online"][i]]
    target["higher_error_rows"] = [{"index":i,"truth":truth["repeat_online"][i],"lower":a["trace"][i],"higher":b["trace"][i]} for i in error_positions]
    check("target_errors_and_units", [scores[x]["terminal_errors"] for x in target_ids] == [0,1] and [scores[x]["local_units"] for x in target_ids] == [2189022,2192224])
    check("target_first_divergence", first == 3 and firstblock == 0)
    check("target_same_selectors", [x["selected"] for x in a["trace"]] == [x["selected"] for x in b["trace"]])
    check("target_first_fee_decision", F(60632,100000) > F(21846,65536) and F(4160,100000) <= F(21846,65536))
    check("target_cost_decomposition", provider_totals == [1731449,1739641] and failure_totals == [64955,101613] and error_positions == [78])
    with (HERE / "target_trace_explanation.json").open("x") as stream:
        json.dump(target,stream,indent=2,sort_keys=True);stream.write("\n")
    with (HERE / "pair_and_catalogue_details.json").open("x") as stream:
        json.dump({"index_pairs":pairs,"native_price_details":native_details},stream,indent=2,sort_keys=True);stream.write("\n")
    return {"runs":len(records),"trace_positions":total_positions,"provider_invoices":total_invoices,
            "optional_reports_reconciled":report_count,"candidate_full_semantic_pairs":sum(x["kind"] == "broker" for x in pairs),
            "ordinary_full_semantic_pairs":sum(x["kind"] == "ordinary" for x in pairs),
            "native_price_comparisons":len(native_details),"summary_groups":len(groups),
            "fixed_path_thresholds":len(analysis["hard_path_repricing_thresholds"]),
            "score_sha256":digest(RUN / "private/scores.json"),"analyzer_sha256":digest(HERE / "p308_analyze_snapshot.py"),
            "target_first_divergence":first,"target_error_positions":error_positions,"target_cost_decomposition":target["cost_decomposition"]}


if __name__ == "__main__":
    outcome = {"stage":"DEVELOPMENT","started_utc":datetime.now(timezone.utc).isoformat(),
               "script_sha256":digest(Path(__file__)),"research_credit_seconds":0}
    try:
        outcome["summary"] = run()
        outcome["pass"] = True
    except Exception:
        outcome["pass"] = False
        outcome["exception"] = traceback.format_exc()
    outcome["finished_utc"] = datetime.now(timezone.utc).isoformat()
    outcome["checks_passed"] = sum(x["pass"] for x in checks)
    outcome["checks_failed"] = [x for x in checks if not x["pass"]]
    with (HERE / "results.json").open("x") as stream:
        json.dump(outcome,stream,indent=2,sort_keys=True);stream.write("\n")
    print(json.dumps(outcome,sort_keys=True))
    raise SystemExit(0 if outcome["pass"] else 1)
