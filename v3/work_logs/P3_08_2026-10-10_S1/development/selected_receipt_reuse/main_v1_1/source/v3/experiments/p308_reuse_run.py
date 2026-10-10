"""Public-first DEVELOPMENT comparison of paid selected-receipt cache reuse.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
Run from a copied complete source closure. Every episode has a fresh service.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import platform
import sys

import p308_run as R
import p308_cached_service as A
import p308_broker as B
import p308_cnf as S
import p308_reporting as P
from p308_common import C, REPO, canonical, fraction_record, registry_setup

VERSION = "p308-selected-receipt-comparison-v1"
CORE_SOURCES = R.CORE_SOURCES + ("v3/experiments/p308_cached_service.py",)
ALL_SOURCES = R.ALL_SOURCES + ("v3/experiments/p308_cached_service.py",
                              "v3/experiments/p308_reuse_run.py")


def manifest():
    return [{"path":p,"bytes":(REPO/p).stat().st_size,"sha256":R.sha(REPO/p)} for p in ALL_SOURCES]


def jobs():
    for scenario in ("repeat_online","cold_mixed","cheap_structure"):
        for seed in R.SEEDS if scenario == "repeat_online" else (11,):
            for selector in ("uniform","tickets"):
                for hard in (False,True) if scenario == "repeat_online" else (True,):
                    for provider in ("cold","linear","hashed"):
                        yield dict(scenario=scenario,seed=seed,selector=selector,hard=hard,provider=provider)


def public_run(out):
    out = Path(out).resolve()
    out.mkdir(parents=True,exist_ok=False)
    before=manifest()
    R.save(out/"source_before.json",{"stage":"DEVELOPMENT","created_utc":R.utc(),"sources":before})
    R.save(out/"plan.json",{"stage":"DEVELOPMENT","version":VERSION,"jobs":list(jobs()),
        "derivation":"v3/derivations/08_selected_receipt_reuse.md","python":sys.version,
        "platform":platform.platform(),"core_sources":CORE_SOURCES,
        "inputs_previously_exposed_in_common_v2":True,"policy_truth_access":False,
        "ordinary_mirror_has_identical_adapter_access":True,"final_freeze":False,
        "fair_bits_verified_by_seeds":False,"public_execution_before_private_scoring":True})
    tapes=R.cohorts()
    R.save(out/"public_inputs.json",{s:[q.record() for q in tape] for s,tape in tapes.items()})
    index=[]
    with (out/"public_records.jsonl.gz").open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=0) as archive:
            for job in jobs():
                tape=tapes[job["scenario"]]
                source_meter=C.CostMeter()
                sources=registry_setup([REPO/p for p in CORE_SOURCES],source_meter)
                service=S if job["provider"] == "cold" else A.CachedService(cache_kind=job["provider"])
                contract=B.Contract(len(tape),selector=job["selector"],hard_index="hashed" if job["hard"] else "linear")
                episode=B.execute(service,tape,contract,seed=job["seed"],hard=job["hard"],purchase_solver="dpll",
                                  unit_limit=C.MAX_UNITS-source_meter.total)
                report_meter=C.CostMeter()
                report_sources=registry_setup([REPO/"v3/experiments/p308_reporting.py"],report_meter)
                report=P.report_owned_episode(service,episode,basis="snapshot",radius="grid",
                        unit_limit=C.MAX_UNITS-source_meter.total-episode["meter"]["total"]-report_meter.total)
                service_audit=None if job["provider"] == "cold" else service.audit_record()
                run_id=f"{job['scenario']}__{job['selector']}__hard{int(job['hard'])}__seed{job['seed']}__{job['provider']}"
                row={"stage":"DEVELOPMENT","run_id":run_id,"configuration":job,"episode":episode,
                     "source_invoice":source_meter.snapshot(),"sources":sources,"service_audit":service_audit,
                     "report":report,"report_source_invoice":report_meter.snapshot(),"report_sources":report_sources}
                encoded=canonical(row).encode();archive.write(encoded+b"\n")
                ix={"run_id":run_id,"configuration":job,"record_sha256":hashlib.sha256(encoded).hexdigest(),
                    "status":episode["status"],"rounds_closed":episode["rounds_closed"],
                    "logical_receipts":episode["purchases"],
                    "physical_cold_calls":episode["purchases"] if service_audit is None else service_audit["physical_cold_calls"],
                    "checked_cache_hits":0 if service_audit is None else service_audit["checked_cache_hits"],
                    "local_units":episode["meter"]["total"],"source_units":source_meter.total,
                    "cold_units":episode["meter"]["total"]+source_meter.total,
                    "additional_report_units":report_meter.total+report["meter"]["total"]}
                index.append(ix);print(canonical(ix),flush=True)
    after=manifest();assert before==after
    R.save(out/"source_after.json",{"stage":"DEVELOPMENT","created_utc":R.utc(),"unchanged":True,"sources":after})
    R.save(out/"public_index.json",{"stage":"DEVELOPMENT","count":len(index),"records":index})
    files=("plan.json","public_inputs.json","public_records.jsonl.gz","public_index.json","source_before.json","source_after.json")
    R.save(out/"public_seal.json",{"stage":"DEVELOPMENT","sealed_utc":R.utc(),"private_scoring_performed":False,
        "files":[{"path":p,"sha256":R.sha(out/p),"bytes":(out/p).stat().st_size} for p in files]})
    return {"stage":"DEVELOPMENT","public_rows":len(index),"all_success":all(r["status"]=="success" for r in index)}


def score(out):
    out=Path(out).resolve();dest=out/"private";dest.mkdir(exist_ok=False)
    seal=json.loads((out/"public_seal.json").read_text())
    assert all(R.sha(out/r["path"])==r["sha256"] for r in seal["files"])
    inputs=json.loads((out/"public_inputs.json").read_text())
    truth={s:[R.independent_truth(q) for q in tape] for s,tape in inputs.items()}
    R.save(dest/"truth.json",{"stage":"DEVELOPMENT","evaluator_only":True,"answers":truth,
                              "public_seal_sha256":R.sha(out/"public_seal.json")})
    ix={r["run_id"]:r for r in json.loads((out/"public_index.json").read_text())["records"]}
    records={};scores=[];groups={}
    with gzip.open(out/"public_records.jsonl.gz","rt") as f:
        for line in f:
            r=json.loads(line);run_id=r["run_id"];records[run_id]=r
            assert hashlib.sha256(line.rstrip("\n").encode()).hexdigest()==ix[run_id]["record_sha256"]
            e=r["episode"];job=r["configuration"];ys=truth[job["scenario"]]
            assert e["status"]=="success" and len(e["trace"])==len(ys)
            assert all(row["index"]==i for i,row in enumerate(e["trace"]))
            errors=sum(row["terminal_action"]!=y for row,y in zip(e["trace"],ys))
            f_live=sum(((F(*row["emitted_q"])-y)**2 for row,y in zip(e["trace"],ys)),F(0))
            f_base=sum(((F(*row["base_q"])-y)**2 for row,y in zip(e["trace"],ys)),F(0))
            v_live=sum((F(*row["emitted_q"])+(1-2*F(*row["emitted_q"]))*y
                        for row,y in zip(e["trace"],ys) if not row["selected"]),F(0))
            for row,y in zip(e["trace"],ys):
                if row["purchased_label"] is not None: assert row["purchased_label"]==y
                if row["hard_after"]["status"]=="checked": assert row["hard_after"]["answer"]==y
            report=r["report"];assert report["status"]=="success"
            assert f_base-f_live==F(*report["corrections"]["F"])
            assert f_live-F(*report["live_centers"]["F"])==v_live-F(*report["live_centers"]["V"])
            if r["service_audit"] is not None:
                a=r["service_audit"]
                assert a["logical_selected_calls"]==e["purchases"]==len(e["invoices"])
                assert a["physical_cold_calls"]+a["checked_cache_hits"]==e["purchases"]
            scores.append({**ix[run_id],"terminal_errors":errors,"issued_brier":fraction_record(f_live),
                "exact_corrections_and_shared_residual_pass":True,"full_horizon":True})
            key=(job["scenario"],job["seed"],job["selector"],job["hard"])
            groups.setdefault(key,{})[job["provider"]]=r
    pairs=[]
    for key,group in groups.items():
        plain=group["cold"]
        for kind in ("linear","hashed"):
            cached=group[kind];a,b=plain["episode"],cached["episode"]
            assert a["trace"]==b["trace"] and a["blocks"]==b["blocks"]
            assert a["weights"]==b["weights"] and a["random_bits_consumed"]==b["random_bits_consumed"]
            for field in ("intervals","live_centers","corrections","reference_corrections","sampling_radius","action_radius","Q"):
                assert plain["report"][field]==cached["report"][field]
            pairs.append({"plain_run":plain["run_id"],"reuse_run":cached["run_id"],
                "exact_mathematical_path_equal":True,"same_public_performance_report":True,
                "local_units_saved":a["meter"]["total"]-b["meter"]["total"],
                "physical_calls_saved":a["purchases"]-cached["service_audit"]["physical_cold_calls"]})
    assert len(scores)==48 and len(pairs)==32
    R.save(dest/"scores.json",{"stage":"DEVELOPMENT","runs":scores,"paired_coupling_checks":pairs,
        "coverage_established_by_development":False,"ordinary_mirror_can_use_identical_service":True})
    R.save(dest/"seal.json",{"stage":"DEVELOPMENT","scored_utc":R.utc(),
        "sources_unchanged":manifest()==json.loads((out/"source_before.json").read_text())["sources"],
        "files":[{"path":p,"sha256":R.sha(dest/p)} for p in ("truth.json","scores.json")]})
    return {"stage":"DEVELOPMENT","scored_rows":48,"coupled_pairs":32,"all_complete":True}


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("command",choices=("public","score"));parser.add_argument("--out",required=True)
    args=parser.parse_args();print(canonical(public_run(args.out) if args.command=="public" else score(args.out)))
