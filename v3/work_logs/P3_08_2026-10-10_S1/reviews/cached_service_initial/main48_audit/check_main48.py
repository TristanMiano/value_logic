"""Read-only sealed selected-receipt-reuse v1 audit; no service invocation."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
WORK = HERE.parents[2]
BASE = WORK / "development/selected_receipt_reuse/main_v1"
RUN = BASE / "run"


def read(p): return json.loads(p.read_text())
def digest(p): return sha256(p.read_bytes()).hexdigest()
def pair(v): return [v.numerator,v.denominator]
def ops(m): return Counter({(x["category"],x["operation"]):x["units"] for x in m["operations"]})


def check_meter(m):
    assert len(m["operations"]) == len(ops(m))
    assert m["total"] == sum(ops(m).values()) == sum(m["by_category"].values())
    assert all(sum(v for (category,_),v in ops(m).items() if category == c) == amount for c,amount in m["by_category"].items())


def nested_ops(m,prefix):
    return Counter({(c,o[len(prefix):]):n for (c,o),n in ops(m).items() if o.startswith(prefix)})


def run():
    for source in read(HERE/"plan.json")["sources"]:
        assert digest(ROOT/source["path"]) == source["sha256"]
    for directory,name in [(RUN,"public_seal.json"),(RUN/"private","seal.json")]:
        for source in read(directory/name)["files"]:
            assert digest(directory/source["path"]) == source["sha256"]
            if "bytes" in source:
                assert (directory/source["path"]).stat().st_size == source["bytes"]
    before,after = read(RUN/"source_before.json"),read(RUN/"source_after.json")
    assert before["sources"] == after["sources"]
    for source in before["sources"]:
        assert digest(BASE/"source"/source["path"]) == source["sha256"]
    for source in read(HERE.parent/"plan.json")["sources"]:
        if source["path"].startswith("v3/experiments/") or source["path"].startswith("v3/checks/"):
            assert digest(BASE/"source"/source["path"]) == source["sha256"]
    target_file = read(RUN/"private/truth.json")
    assert target_file["public_seal_sha256"] == digest(RUN/"public_seal.json")
    truths = target_file["answers"]
    inputs = read(RUN/"public_inputs.json")
    score_file = read(RUN/"private/scores.json")
    scores = {x["run_id"]:x for x in score_file["runs"]}
    index = {x["run_id"]:x for x in read(RUN/"public_index.json")["records"]}
    records,groups = {},defaultdict(dict)
    positions = invoices = cold_invoices = cache_hits = 0
    with gzip.open(RUN/"public_records.jsonl.gz","rb") as stream:
        for line in stream:
            record = json.loads(line)
            rid,cfg,e = record["run_id"],record["configuration"],record["episode"]
            assert rid not in records and sha256(line.rstrip(b"\n")).hexdigest() == index[rid]["record_sha256"]
            records[rid] = record
            assert all(scores[rid][key] == value for key,value in index[rid].items())
            target = truths[cfg["scenario"]]
            assert e["status"] == "success" and e["all_path_funded"] and e["successful_quota_contract"]
            assert len(e["trace"]) == len(target) and e["purchases"] == len(e["invoices"]) == e["contract"]["quota"]
            assert e["meter"]["total"] == index[rid]["local_units"]
            assert record["source_invoice"]["total"] == index[rid]["source_units"]
            assert index[rid]["cold_units"] == index[rid]["local_units"]+index[rid]["source_units"]
            assert index[rid]["additional_report_units"] == record["report_source_invoice"]["total"]+record["report"]["meter"]["total"]
            for sources,meter in [(record["sources"],record["source_invoice"]),(record["report_sources"],record["report_source_invoice"])]:
                assert all(digest(BASE/"source"/s["path"]) == s["sha256"] for s in sources)
                expected = sum(2*((s["bytes"]+7)//8)+(s["bytes"]+72)//64 for s in sources)
                assert meter["total"] == expected
                check_meter(meter)
            check_meter(e["meter"]);check_meter(record["report"]["meter"])
            parent_expected = Counter()
            for inv in e["invoices"]:
                check_meter(inv["resources"])
                parent_expected.update(ops(inv["resources"]))
            assert nested_ops(e["meter"],"selected_provider:") == parent_expected
            errors = 0
            flive = fbase = vlive = F()
            for i,(row,y,raw) in enumerate(zip(e["trace"],target,inputs[cfg["scenario"]])):
                assert row["index"] == i and row["query_id"] == raw["query_id"]
                assert row["claim_key"] == [raw["semantics_version"],raw["source_version"],raw["variables"],raw["clauses"]]
                errors += row["terminal_action"] != y
                q,q0 = F(*row["emitted_q"]),F(*row["base_q"])
                flive += (q-y)**2;fbase += (q0-y)**2
                if not row["selected"]: vlive += q if y == 0 else 1-q
                if row["purchased_label"] is not None: assert row["purchased_label"] == y
                if row["hard_after"]["status"] == "checked": assert row["hard_after"]["answer"] == y
            assert errors == scores[rid]["terminal_errors"] and pair(flive) == scores[rid]["issued_brier"]
            report = record["report"]
            assert report["status"] == "success" and report["confidence_eligible"]
            assert fbase-flive == F(*report["corrections"]["F"])
            assert flive-F(*report["live_centers"]["F"]) == vlive-F(*report["live_centers"]["V"])
            audit = record["service_audit"]
            if cfg["provider"] == "cold":
                assert audit is None and index[rid]["physical_cold_calls"] == e["purchases"] and index[rid]["checked_cache_hits"] == 0
            else:
                assert audit["cache_kind"] == cfg["provider"] and audit["capacity"] == 64
                assert audit["logical_selected_calls"] == e["purchases"] == len(audit["requests"])
                # Reconstruct fresh FIFO state from this episode's selected
                # calls only; neither public evaluation labels nor prior
                # episodes initialize it.
                cache = []
                observed_cold = observed_hits = 0
                for call,inv in zip(audit["requests"],e["invoices"]):
                    assert call["adapter_receipt"] == inv and call["query_id"] == inv["query_id"]
                    assert call["status"] == inv["status"] == "success" and inv["checked"] is True
                    assert inv["provider"] == "owned_cached_cnf_receipt" and inv["provider_version"] == "p308-selected-receipt-cache-v1"
                    key = json.dumps(inv["claim_key"],separators=(",",":"))
                    hit = key in cache
                    assert call["cache_hit"] == hit
                    if hit:
                        observed_hits += 1
                        assert call["cold_receipt"] is None
                        assert not nested_ops(inv["resources"],"selected_cache_cold_provider:")
                    else:
                        observed_cold += 1
                        child = call["cold_receipt"]
                        assert child is not None and child["status"] == "success" and child["checked"] is True
                        assert child["provider"] == "bounded_cnf_checked" and child["provider_version"] == "p308-bounded-cnf-services-v1.1"
                        assert all(child[k] == inv[k] for k in ["query_id","claim_key","answer"])
                        check_meter(child["resources"])
                        assert nested_ops(inv["resources"],"selected_cache_cold_provider:") == ops(child["resources"])
                        cache.append(key)
                        if len(cache)>audit["capacity"]: cache.pop(0)
                        cold_invoices += 1
                    cache_hits += hit
                assert observed_cold == audit["physical_cold_calls"] == index[rid]["physical_cold_calls"]
                assert observed_hits == audit["checked_cache_hits"] == index[rid]["checked_cache_hits"]
                assert observed_cold+observed_hits == e["purchases"]
            groups[(cfg["scenario"],cfg["seed"],cfg["selector"],cfg["hard"])][cfg["provider"]] = record
            positions += len(e["trace"]);invoices += len(e["invoices"])
    assert len(records) == len(index) == len(scores) == 48 and len(groups) == 16
    pairs = []
    for key,group in groups.items():
        plain = group["cold"]
        for kind in ("linear","hashed"):
            r = group[kind]
            for field in ["trace","blocks","weights","random_bits_consumed","purchases","hard_state"]:
                assert plain["episode"][field] == r["episode"][field]
            for field in ["intervals","live_centers","reference_centers","corrections","reference_corrections","sampling_radius","action_radius","Q","R","deterministic_envelopes","n_live"]:
                assert plain["report"][field] == r["report"][field]
            assert plain["report"]["meter"]["total"] == r["report"]["meter"]["total"]
            delta = plain["episode"]["meter"]["total"]-r["episode"]["meter"]["total"]
            calls = plain["episode"]["purchases"]-r["service_audit"]["physical_cold_calls"]
            pair_row = {"plain_run":plain["run_id"],"reuse_run":r["run_id"],"local_units_saved":delta,"physical_calls_saved":calls}
            matching = [x for x in score_file["paired_coupling_checks"] if x["reuse_run"] == r["run_id"]]
            assert len(matching) == 1 and all(matching[0][k] == v for k,v in pair_row.items())
            pairs.append(pair_row)
    summaries = []
    for scenario in sorted({key[0] for key in groups}):
        for selector in ("uniform","tickets"):
            for kind in ("linear","hashed"):
                ps = [x for x in pairs if x["reuse_run"].startswith(scenario+"__"+selector+"__") and x["reuse_run"].endswith("__"+kind)]
                if not ps: continue
                saves,calls = [x["local_units_saved"] for x in ps],[x["physical_calls_saved"] for x in ps]
                summaries.append({"scenario":scenario,"selector":selector,"kind":kind,"pairs":len(ps),
                                  "units_saved_range":[min(saves),max(saves)],"calls_saved_range":[min(calls),max(calls)]})
    result = {"runs":len(records),"trace_positions":positions,"logical_selected_invoices":invoices,
              "cold_child_invoices_in_cached_arms":cold_invoices,"cached_arm_hits":cache_hits,"coupled_pairs":len(pairs),
              "positive_unit_savings":sum(x["local_units_saved"]>0 for x in pairs),
              "negative_unit_savings":sum(x["local_units_saved"]<0 for x in pairs),
              "all_pairs_fewer_physical_calls":all(x["physical_calls_saved"]>0 for x in pairs),
              "source_units":sorted({r["source_invoice"]["total"] for r in records.values()}),
              "pairs":pairs,"group_summaries":summaries}
    return result


if __name__ == "__main__":
    result = {"stage":"DEVELOPMENT","started_utc":datetime.now(timezone.utc).isoformat(),
              "script_sha256":digest(Path(__file__)),"research_credit_seconds":0,"policy_or_report_reruns":False}
    try:
        result["summary"] = run();result["pass"] = True
    except Exception:
        result["pass"] = False;result["exception"] = traceback.format_exc()
    result["finished_utc"] = datetime.now(timezone.utc).isoformat()
    with (HERE/"results.json").open("x") as f:json.dump(result,f,indent=2,sort_keys=True);f.write("\n")
    print(json.dumps({k:v for k,v in result.items() if k != "summary"}|{"summary":{k:v for k,v in result.get("summary",{}).items() if k not in ["pairs"]}},sort_keys=True))
    raise SystemExit(0 if result["pass"] else 1)
