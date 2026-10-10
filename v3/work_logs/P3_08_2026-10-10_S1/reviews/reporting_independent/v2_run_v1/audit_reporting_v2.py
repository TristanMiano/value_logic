"""Independent public-only reporter-v2 reconstruction. P3-08 DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-10. No production calculator generates
expected values; no private audit/score file or unpurchased truth evaluator
is read. The fixed hard policy comes from the public method configuration.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction as F
import gzip
import importlib
import json
from pathlib import Path
import shutil
import sys

from audit_reporting import (IdentityOnly, ceil_root, differences, encode,
                             finite_bounds, fingerprint, frozen, save, utc)

VERSION = "p308-reporting-v2-independent-v1"


def expected_public(episode, hard_mode, basis, radius_rule):
    """Direct section-2/3/4 formulas, using public selected labels only."""
    if type(hard_mode) is not bool:
        raise ValueError("The independent policy flag must be Boolean")
    contract = episode["contract"]
    t, b, m = contract["horizon"], contract["block_size"], len(episode["blocks"])
    known = {}
    ref_u = ref_a = raw_df = raw_dv = ref_df = ref_dv = F(0)
    raw_dz = n_live = 0
    vmin = vmax = fmin = fmax = qtotal = F(0)
    selected_live_brier = unselected_live_variance = F(0)
    masks = []
    for k, block in enumerate(episode["blocks"]):
        # This copy belongs to the independent evaluator only. It freezes
        # earlier-block keys independently of the production timestamp code.
        entry_answers = dict(known)
        width = F(0)
        chosen, favorite = block["selected"], block["favorite"]
        for i in range(b):
            row = episode["trace"][k*b+i]
            key = frozen(row["claim_key"])
            q, qlive = F(*row["base_q"]), F(*row["emitted_q"])
            pi = F(1, b) if contract["selector"] == "uniform" else F(b+1 if i==favorite else 1, 2*b)
            assert F(*row["propensity"]) == pi
            assert F(*block["propensities"][i]) == pi
            h0 = hard_mode and key in entry_answers
            h1 = hard_mode and key in known
            assert row["hard_before"] == ("checked" if h1 else "unresolved")
            assert not h0 or h1
            assert qlive == (known[key] if h1 else q)
            reference_known = h0 and basis == "snapshot"
            a = F(0) if reference_known else F(1, 2)
            variance = F(0) if reference_known else q*(1-q)
            ref_a += a-variance
            if i != chosen:
                ref_u += a
                unselected_live_variance += qlive*(1-qlive)
            if h1:
                label = known[key]
                loss = q+(1-2*q)*label
                brier = (q-label)**2
                raw_df += brier
                if not reference_known:
                    ref_df += brier
                if i != chosen:
                    raw_dv += loss
                    raw_dz += row["base_action"] != label
                    if not reference_known:
                        ref_dv += loss
            elif i != chosen:
                n_live += 1
                vmin += min(q, 1-q)
                vmax += max(q, 1-q)
            known_label = known[key] if h1 else None
            if i == chosen:
                invoice = episode["invoices"][k]
                assert frozen(invoice["claim_key"]) == key
                label = invoice["answer"]
                assert type(label) is int and label in (0, 1)
                residual = F(0) if reference_known else q+(1-2*q)*label-F(1, 2)
                ref_u += (1/pi-1)*residual
                ref_a += residual/pi
                if key in known:
                    assert known[key] == label
                known[key] = known_label = label
                selected_live_brier += (qlive-label)**2
            if known_label is None:
                fmin += min(qlive**2, (1-qlive)**2)
                fmax += max(qlive**2, (1-qlive)**2)
            else:
                fmin += (qlive-known_label)**2
                fmax += (qlive-known_label)**2
            width = max(width, F(0) if reference_known else abs(1-2*q)/pi)
            masks.append({"row": k*b+i, "H0": h0, "H1": h1,
                          "reference_known": reference_known, "selected": i==chosen})
        qtotal += width**2
    live_u, live_a = ref_u-ref_dv, ref_a-ref_df
    assert live_a-live_u == selected_live_brier-unselected_live_variance
    s = b if contract["selector"] == "uniform" else 2*b
    rstar = s*ceil_root(2*m)
    if radius_rule == "fixed":
        rates, c = [rstar], 5
    else:
        rates = [s]
        while rates[-1] < rstar:
            rates.append(2*rates[-1])
        if rstar not in rates:
            rates.append(rstar)
        c = 0
        while 2**c < 80*len(rates):
            c += 1
    radius_by_rate = {r: qtotal/r+F(c*r, 8) for r in rates}
    radius = min(radius_by_rate.values())
    minimizers = sorted(r for r, value in radius_by_rate.items() if value == radius)
    action_radius = ceil_root((5*n_live+1)//2)

    def interval(center, amount, lower, upper):
        lo, hi = max(center-amount, lower), min(center+amount, upper)
        return {"lower": lo, "upper": hi, "confidence_conflict": lo > hi}

    if n_live == 0:
        assert fmin == fmax
        intervals = {"V": interval(F(0),F(0),F(0),F(0)),
                     "F": interval(fmin,F(0),fmin,fmax),
                     "Z": interval(F(0),F(0),F(0),F(0))}
    else:
        intervals = {"V": interval(live_u,radius,vmin,vmax),
                     "F": interval(live_a,radius,fmin,fmax),
                     "Z": interval(live_u,radius+action_radius,F(0),F(n_live))}
    result = {"reference_basis": basis, "radius_rule": radius_rule,
              "reference_centers": {"V":ref_u,"F":ref_a},
              "live_centers": {"V":live_u,"F":live_a},
              "corrections": {"V":raw_dv,"F":raw_df,"Z":raw_dz},
              "reference_corrections": {"V":ref_dv,"F":ref_df},
              "Q":qtotal,"sampling_radius":radius,"action_radius":action_radius,
              "n_live":n_live,"exact_all_remaining_known":n_live==0,
              "original_fixed_R":rstar,"predeclared_rates":rates,
              "sampling_log_allowance":c,"intervals":intervals,
              "deterministic_envelopes":{"V":[vmin,vmax],"F":[fmin,fmax],"Z":[F(0),F(n_live)]},
              "rows_read":t,"purchased_labels_read":m,"retained_checked_keys":len(known),
              "hard_mode":hard_mode,
              "hard_mode_source":"owned_fixed_policy_flag" if "hard_enabled" in episode else "legacy_owned_store_count",
              "audit":{"masks":masks,"minimizing_rates":minimizers,
                       "radius_by_rate":radius_by_rate,
                       "public_center_difference":live_a-live_u,
                       "selected_brier_minus_unselected_variance":selected_live_brier-unselected_live_variance}}
    if basis == "base":
        result["base_centers"] = dict(result["reference_centers"])
    return result


def compare_one(expected, actual):
    errors = differences(expected, actual)
    if actual.get("status") != "success":
        errors.append({"field":"status","actual":actual.get("status"),"detail":actual.get("failure_detail")})
    if actual.get("R") not in expected["audit"]["minimizing_rates"]:
        errors.append({"field":"R","actual":actual.get("R"),"minimizers":expected["audit"]["minimizing_rates"]})
    if expected["reference_basis"] == "snapshot" and "base_centers" in actual:
        errors.append({"field":"base_centers","reason":"snapshot must not rename its reference a raw-base center"})
    return errors


def run(repo, out):
    if out.exists():
        raise FileExistsError("Use a fresh output directory")
    common = repo/"v3/work_logs/P3_08_2026-10-10_S1/development/common_v1/run"
    replay = repo/"v3/work_logs/P3_08_2026-10-10_S1/development/reporting_v2"
    source_plan = json.loads((replay/"run/plan_and_sources.json").read_text())
    public_seal = json.loads((replay/"run/public_seal.json").read_text())
    source_paths = [x["path"] for x in source_plan["sources"]]
    sources = [fingerprint(replay/"source"/p,p) for p in source_paths]
    assert sources == source_plan["sources"]
    archive_input = fingerprint(common/"public_records.jsonl.gz", "common_v1/run/public_records.jsonl.gz")
    archive_reports = fingerprint(replay/"run/public_reports.jsonl.gz", "reporting_v2/run/public_reports.jsonl.gz")
    input_seal = fingerprint(common/"public_seal.json", "common_v1/run/public_seal.json")
    assert archive_input["sha256"] == public_seal["input_public_archive_sha256"]
    assert archive_reports["sha256"] == public_seal["output_sha256"]
    assert input_seal["sha256"] == public_seal["input_public_seal_sha256"]
    out.mkdir(parents=True)
    for relative in source_paths:
        dst = out/"source"/relative
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(replay/"source"/relative,dst)
    for name in ("audit_reporting_v2.py","audit_reporting.py","v2_plan.md"):
        shutil.copyfile(Path(__file__).with_name(name),out/name)
    save(out/"manifest_before.json",{"stage":"DEVELOPMENT","created_utc":utc(),"version":VERSION,
         "sources":sources,"inputs":[archive_input,archive_reports,input_seal],
         "source_public_seal":fingerprint(replay/"run/public_seal.json","reporting_v2/run/public_seal.json"),
         "checker":fingerprint(Path(__file__),"audit_reporting_v2.py"),
         "shared_audit_helpers":fingerprint(Path(__file__).with_name("audit_reporting.py"),"audit_reporting.py"),
         "runtime":sys.version,"principal_time_credit_seconds":0,
         "read_boundary":"sealed public archives, public seals, source files only; private files not read"})
    episodes = {}
    with gzip.open(common/"public_records.jsonl.gz","rt") as archive:
        for line in archive:
            row=json.loads(line)
            if row["configuration"]["kind"]=="broker":
                episodes[row["run_id"]]=row
    reports=[]
    with gzip.open(replay/"run/public_reports.jsonl.gz","rt") as archive:
        for line in archive:
            reports.append(json.loads(line))
    completed=[]
    def complete(name,passed,detail):
        row={"case":name,"passed":bool(passed),"detail":detail}
        completed.append(row)
        with (out/"completed.jsonl").open("a") as handle:
            handle.write(json.dumps(encode(row),sort_keys=True)+"\n")
    expected_rows=[]
    for row in reports:
        record=episodes[row["run_id"]]
        expected=expected_public(record["episode"],record["configuration"]["hard"],row["basis"],row["radius"])
        errors=compare_one(expected,row["report"])
        expected_rows.append({"run_id":row["run_id"],"basis":row["basis"],"radius":row["radius"],
                              "expected":expected,"actual_report":row["report"],"differences":errors})
        complete(row["run_id"]+"__"+row["basis"]+"__"+row["radius"],not errors,
                 {"differences":errors,"n_live":expected["n_live"],"report_units":row["report"]["meter"]["total"],
                  "peak_bits":row["report"].get("peak_integer_bits")})
    with gzip.open(out/"independent_expected_and_reports.jsonl.gz","wt") as archive:
        for row in expected_rows:
            archive.write(json.dumps(encode(row),sort_keys=True)+"\n")
    sys.path.insert(0,str(out/"source/v3/experiments"))
    reporter=importlib.import_module("p308_reporting")
    service=importlib.import_module("p308_cnf")
    identity=IdentityOnly(service)
    hard_record=next(x for x in episodes.values() if x["configuration"]["hard"]
                     and any(r["hard_before"]=="checked" and r["block"]>0 for r in x["episode"]["trace"]))
    soft_record=next(x for x in episodes.values() if not x["configuration"]["hard"])
    focused=[]
    def subject(name,record,mutation=None,basis="snapshot",radius="grid",want_success=False):
        episode=deepcopy(record["episode"])
        if mutation:
            mutation(episode)
        actual=reporter.report_owned_episode(identity,episode,basis=basis,radius=radius)
        errors=[]
        if want_success:
            expected=expected_public(episode,record["configuration"]["hard"],basis,radius)
            errors=compare_one(expected,actual)
        else:
            if actual["status"]!="failed" or actual["confidence_eligible"]:
                errors.append({"rejection_missing":True})
        focused.append({"case":name,"input_episode":episode,"basis":basis,"radius":radius,
                        "actual_report":actual,"errors":errors})
        complete(name,not errors,{"status":actual["status"],"errors":errors,
                                 "failure":actual.get("failure_detail"),"spent":actual["meter"]["total"]})
    subject("explicit_hard_true",hard_record,lambda e:e.__setitem__("hard_enabled",True),want_success=True)
    subject("explicit_hard_false",soft_record,lambda e:e.__setitem__("hard_enabled",False),want_success=True)
    subject("explicit_mode_contradicts_hard_rows",hard_record,lambda e:e.__setitem__("hard_enabled",False))
    subject("explicit_mode_not_boolean",hard_record,lambda e:e.__setitem__("hard_enabled",1))
    subject("legacy_mode_false_store_count",hard_record,lambda e:e["hard_state"].__setitem__("entries_retained",0))
    subject("legacy_mode_wrong_final_key_count",hard_record,
            lambda e:e["hard_state"].__setitem__("entries_retained",e["hard_state"]["entries_retained"]+1))
    def suppress_prior_hard(e):
        row=next(r for r in e["trace"] if r["hard_before"]=="checked" and r["block"]>0)
        row["hard_before"]="unresolved"
        row["emitted_q"]=list(row["base_q"])
        row["prospective_action"]=row["base_action"]
        if not row["selected"]:
            row["terminal_action"]=row["prospective_action"]
    subject("H0_one_H1_zero_rejected",hard_record,suppress_prior_hard)
    subject("unknown_basis_rejected",hard_record,basis="live")
    subject("unknown_radius_rejected",hard_record,radius="optimized")
    old_smoke=repo/"v3/work_logs/P3_08_2026-10-10_S1/development/reporting_smoke_v1/public_results.json"
    smoke=next(x for x in json.loads(old_smoke.read_text()) if x["selector"]=="tickets" and x["hard"])
    smoke_record={"episode":smoke["episode"],"configuration":{"hard":True}}
    subject("grid_deduplicates_original_power_of_two_rate",smoke_record,want_success=True)
    save(out/"focused_boundary_checks.json",focused)
    # The old generous row/global cost allowances still dominate v2's paid
    # extra reference arithmetic and <=9 rate candidates. Cross products use
    # the independent 215-bit contract bound, conservatively 229 symbolically.
    bounds=finite_bounds((out/"source/v3/experiments/p308_reporting.py").read_text())
    # The prior exact named table is for the fixed-rate construction. Reuse
    # its source-call tariff count and loose center argument, not that table
    # as if it were a grid-radius bound.
    bounds.pop("finite_contract_table")
    bounds.pop("largest_named_magnitude_bits")
    bounds["center_and_correction_coarse_prebits"]=bounds["conservative_all_preoperation_bits"]
    bounds["conservative_all_preoperation_bits"]=229
    bounds["basis_note"]="snapshot baseline/variance prefixes remain bounded by the old sum-of-absolute-terms envelope"
    bounds["radius_comparison_prebits"]={"public_contract_maximum":215,"coarse_symbolic":229}
    bounds["grid_J_maximum"]=9
    save(out/"finite_cost_and_width_bounds.json",bounds)
    complete("v2_cost_and_width_bound",bounds["funding_cap_sufficient"] and 229<reporter.MAX_BITS,
             {"per_row_integer_calls":bounds["per_row_integer_call_sites_counting_both_branches"],
              "report_cap_bound":bounds["total_report_tariff_bound"],"coarse_prebits":229})
    after=[fingerprint(replay/"source"/p,p) for p in source_paths]
    snapshot=[fingerprint(out/"source"/p,p) for p in source_paths]
    source_equal=sources==after==snapshot
    save(out/"manifest_after.json",{"created_utc":utc(),"source_snapshot_unchanged":source_equal,
                                     "sources":after,"audit_source_copy":snapshot})
    complete("source_closure_unchanged",source_equal,{})
    grouped={}
    for row in expected_rows:
        grouped.setdefault(row["run_id"],{})[(row["basis"],row["radius"])]=row
    descriptive=[]
    for run_id, group in grouped.items():
        base=group[("base","fixed")]["expected"]
        snap=group[("snapshot","fixed")]["expected"]
        sg=group[("snapshot","grid")]["expected"]
        assert snap["Q"]<=base["Q"]
        assert snap["corrections"]==base["corrections"]==sg["corrections"]
        descriptive.append({"run_id":run_id,"Q_snapshot_strictly_smaller":snap["Q"]<base["Q"],
                            "snapshot_grid_radius_vs_base_fixed":(sg["sampling_radius"]>base["sampling_radius"])-(sg["sampling_radius"]<base["sampling_radius"]),
                            "snapshot_grid_radius_vs_snapshot_fixed":(sg["sampling_radius"]>snap["sampling_radius"])-(sg["sampling_radius"]<snap["sampling_radius"])})
    save(out/"public_width_comparisons.json",descriptive)
    summary={"stage":"DEVELOPMENT","version":VERSION,"subject_version":reporter.VERSION,
             "formula_comparisons":len(reports),"owned_episodes":len(episodes),
             "completed_checks":len(completed),"passed_checks":sum(x["passed"] for x in completed),
             "failures":[x for x in completed if not x["passed"]],
             "maximum_observed_integer_bits":max(x["report"]["peak_integer_bits"] for x in reports),
             "report_unit_range":[min(x["report"]["meter"]["total"] for x in reports),max(x["report"]["meter"]["total"] for x in reports)],
             "strict_snapshot_Q_reductions":sum(x["Q_snapshot_strictly_smaller"] for x in descriptive),
             "public_only":True,"private_score_reads":0,"principal_time_credit_seconds":0,
             "prospective_coverage_claim":False,
             "reproduce":"python "+str(Path(__file__))+" "+str(repo)+" /tmp/p308_reporter_v2_independent_replay"}
    save(out/"summary.json",summary)
    print(json.dumps(summary,indent=2))
    return summary


if __name__=="__main__":
    result=run(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
    raise SystemExit(bool(result["failures"]))
