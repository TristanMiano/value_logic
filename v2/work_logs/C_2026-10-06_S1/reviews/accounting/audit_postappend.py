"""Independent Gate C postappend accounting audit; no experiment imports.

Contributor: ChatGPT (GPT-6 Astra Pro), separate accounting reviewer.
Reconstructs event state, then globally partitions the observed interval.
Writes only a new accounting_postappend_review.json in this directory.
"""
from collections import defaultdict
import csv
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import io
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
SESSION = OUT.parents[1]
REPO = SESSION.parents[2]
BASE = "de7b456d08f383e72dfcabd278c183db324fdf16"
NANO = 10**9
CUTOFF = 2930128283158
CUTOFF_UTC = "2026-10-06T08:46:43.787810+00:00"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(name):
    return json.loads((SESSION/name).read_text())


def lines(name):
    return [json.loads(s) for s in (SESSION/name).read_text().splitlines()]


def mins(n):
    with localcontext() as c:
        c.prec = 80
        return str(Decimal(n) / (60*NANO))


def seconds(n):
    return f"{n//NANO}.{n%NANO:09d}"


def main():
    output = OUT / "accounting_postappend_review.json"
    assert not output.exists(), "Preserve existing audit output."
    events, saved = lines("clocks.jsonl"), lines("segments.jsonl")
    baseline, actual, integrity, forecast = (load(n) for n in ("baseline.json", "actuals.json", "ledger_integrity.json", "forecast.json"))
    assert load("clock_state.json") is None
    assert events[0]["command"] == "start" and events[-1]["command"] == "stop"
    assert all(type(e["monotonic_ns"]) is int and e["runtime"] == "linux-GateC-S1" for e in events)
    assert all(a["monotonic_ns"] < b["monotonic_ns"] for a,b in zip(events,events[1:]))
    observed = {e["monotonic_ns"]:e["utc"] for e in events}
    assert observed[CUTOFF] == CUTOFF_UTC
    state, reconstructed = None, []
    for e in events:
        cmd, args = e["command"], e["args"]
        if cmd == "check":
            assert state is not None
            continue
        if state is not None:
            reconstructed.append(dict(state,end_utc=e["utc"],end_monotonic_ns=e["monotonic_ns"],elapsed_ns=e["monotonic_ns"]-state["start_monotonic_ns"]))
        if cmd == "stop":
            state = None
        else:
            if cmd == "pause":
                mode,lane,note = args[0],""," ".join(args[1:])
                assert mode in ("wait","recovery")
            else:
                assert cmd in ("start","switch","resume")
                mode,lane,note = args[0],"" if args[1]=="-" else args[1]," ".join(args[2:])
                assert (mode=="O" and lane=="") or (mode in ("D","L","E") and lane in ("R","X"))
            state = dict(mode=mode,lane=lane,note=note,start_utc=e["utc"],start_monotonic_ns=e["monotonic_ns"],runtime=e["runtime"])
    assert state is None and reconstructed == saved
    exclusions=lines("exclusions.jsonl")
    spans=sorted((e["start_monotonic_ns"],e["end_monotonic_ns"],e["reason"]) for e in exclusions)
    assert all(a in observed and b in observed and a<b for a,b,_ in spans)
    assert all(a[1] <= b[0] for a,b in zip(spans,spans[1:]))
    assert all(sum(s["start_monotonic_ns"]<=a<b<=s["end_monotonic_ns"] for s in saved)==1 for a,b,_ in spans)
    # Independent global sweep, rather than the serializer's per-segment cuts.
    edges=sorted({s[k] for s in saved for k in ("start_monotonic_ns","end_monotonic_ns")} | {x for a,b,_ in spans for x in (a,b)})
    effective=[]
    expected_rows=[]
    totals=dict.fromkeys(("D","L","E","O","tool_wait","recovery_unobserved","paused_recovery"),0)
    lane_totals={"R":0,"X":0}
    for a,b in zip(edges,edges[1:]):
        owners=[(i,s) for i,s in enumerate(saved) if s["start_monotonic_ns"]<=a<b<=s["end_monotonic_ns"]]
        assert len(owners)==1
        i,s=owners[0]
        covered=[reason for x,y,reason in spans if x<=a<b<=y]
        assert len(covered)<=1
        size=b-a
        credit=waiting=unknown=0
        mode,lane=s["mode"],s["lane"]
        if covered:
            category="recovery_unobserved";mode="O";lane="";unknown=size
        elif mode=="recovery":
            category="paused_recovery";mode="O";lane="";unknown=size
        elif mode=="wait":
            category="tool_wait";mode="O";lane="";waiting=size
        else:
            category=mode;credit=size
            if mode in ("D","L","E"):
                assert b<=CUTOFF
                lane_totals[lane]+=size
            checks=sorted(t for t in observed if a<=t<=b)
            assert checks[0]==a and checks[-1]==b
            assert max(y-x for x,y in zip(checks,checks[1:]))<=900*NANO
        totals[category]+=size
        effective.append(dict(raw_segment_index=i,start_monotonic_ns=a,end_monotonic_ns=b,elapsed_ns=size,engaged_ns=credit,tool_wait_ns=waiting,unmeasured_ns=unknown,category=category,effective_mode=mode,effective_lane=lane))
        note="assessment complete; author decision pending; "+category+"; "+s["note"]
        if covered:note+="; exclusion: "+covered[0]
        expected_rows.append(dict(task_id="Gate C",attempt_id="C_1",session_id="2026-10-06-S1",mode=mode,lane=lane,start_utc=observed[a],end_utc=observed[b],elapsed_seconds=seconds(size),engaged_seconds=seconds(credit),tool_wait_seconds=seconds(waiting),idle_seconds="0",unmeasured_seconds=seconds(unknown),forecast_seconds="",artifact="v2/work_logs/C_2026-10-06_S1.md",status=note))
    assert effective==actual["effective_segment_accounting"]
    assert totals==actual["mode_and_exclusion_ns"] and lane_totals==actual["lane_ns"]
    research=sum(totals[m] for m in ("D","L","E"));engaged=research+totals["O"]
    excluded=sum(totals[m] for m in ("tool_wait","recovery_unobserved","paused_recovery"))
    elapsed=edges[-1]-edges[0]
    assert elapsed==engaged+excluded and research==sum(lane_totals.values())
    assert all(actual[k]==v for k,v in [("elapsed_ns",elapsed),("engaged_ns",engaged),("research_ns",research),("excluded_ns",excluded),("research_cutoff_monotonic_ns",CUTOFF),("research_cutoff_utc",CUTOFF_UTC),("accounting_cutoff_monotonic_ns",events[-1]["monotonic_ns"]),("accounting_cutoff_utc",events[-1]["utc"]),("raw_segment_count",len(saved))])
    assert actual["minutes_decimal"]=={k:mins(v) for k,v in totals.items()}
    assert actual["lane_minutes_decimal"]=={k:mins(v) for k,v in lane_totals.items()}
    assert actual["research_minutes_decimal"]==mins(research) and actual["engaged_minutes_decimal"]==mins(engaged) and actual["excluded_minutes_decimal"]==mins(excluded)
    assert actual["protected_minimum"] is None and actual["concurrent_agent_minutes_credited"]==0 and actual["author_decision"]=="PENDING"
    prior=subprocess.run(["git","show",BASE+":v2/time_ledger.csv"],cwd=REPO,capture_output=True,check=True).stdout
    current=(REPO/"v2/time_ledger.csv").read_bytes();append=(SESSION/"ledger_append.csv").read_bytes()
    assert len(prior)==265648 and sha(prior)=="2ddbbff7ccbc4c76bd15f3c26a58273be562ba21f6967b9d1d87feab7958c8fa"
    assert current==prior+append
    reader=csv.DictReader(io.StringIO(prior.decode()));fields=reader.fieldnames;old_rows=list(reader)
    app_rows=list(csv.DictReader(io.StringIO(append.decode()),fieldnames=fields))
    assert app_rows==expected_rows and len(old_rows)==1096 and len(app_rows)==9
    assert len(list(csv.DictReader(io.StringIO(current.decode()))))==1105
    for row in app_rows:
        assert Decimal(row["elapsed_seconds"])==sum(Decimal(row[k]) for k in ("engaged_seconds","tool_wait_seconds","idle_seconds","unmeasured_seconds"))
    assert datetime.fromisoformat(old_rows[-1]["end_utc"].replace("Z","+00:00"))<=datetime.fromisoformat(app_rows[0]["start_utc"])
    for k,v in [("ledger_prior_bytes",len(prior)),("ledger_prior_rows",len(old_rows)),("ledger_prior_sha256",sha(prior)),("ledger_append_bytes",len(append)),("ledger_append_sha256",sha(append)),("ledger_final_sha256",sha(current)),("ledger_rows_added",len(app_rows)),("ledger_final_rows",1105)]:assert actual[k]==v
    for k,v in [("prior_bytes_preserved",len(prior)),("prior_rows",len(old_rows)),("prior_sha256",sha(prior)),("append_sha256",sha(append)),("final_sha256",sha(current)),("rows_added",len(app_rows)),("final_rows",1105)]:assert integrity[k]==v
    assert all(integrity[k] is True for k in ("prior_bytes_equal","observed_time_exactly_partitioned","exclusions_contained_and_nonoverlapping","clock_stopped"))
    with localcontext() as c:
        c.prec=80
        entry=Decimal(baseline["post_b_1_entry_minutes_decimal"])
        close=entry+Decimal(engaged)/(60*NANO);remaining=Decimal(960)-close
        post=dict(entry_minutes_decimal=str(entry),close_minutes_decimal=str(close),remaining_minutes_decimal=str(remaining),checkpoint_minutes=960,checkpoint_reached=close>=960,recurrence_clock_reset=False,inherited_declared_minus_historical_csv_seconds_decimal=baseline["inherited_declared_minus_historical_csv_seconds_decimal"])
        assert post==actual["post_b_1"]
        lane_percent={k:str(Decimal(n)*100/research) for k,n in lane_totals.items()}
        errors={which:{**{k:str(Decimal(n)/(60*NANO)-Decimal(forecast[which+"_minutes"][k])) for k,n in totals.items() if k in ("D","L","E","O")},"engaged":str(Decimal(engaged)/(60*NANO)-forecast[which+"_minutes"]["engaged"]),"research":str(Decimal(research)/(60*NANO)-forecast[which+"_minutes"]["research"])} for which in ("central","high")}
    assert actual["central_forecast_minutes"]==forecast["central_minutes"] and actual["high_forecast_minutes"]==forecast["high_minutes"]
    for name,expected in actual["input_sha256"].items():assert sha((SESSION/name).read_bytes())==expected
    assert post["inherited_declared_minus_historical_csv_seconds_decimal"]=="0.000073995"
    input_files=[SESSION/n for n in ("clock.py","close_accounting.py","baseline.json","forecast.json","clocks.jsonl","segments.jsonl","exclusions.jsonl","clock_state.json","actuals.json","ledger_append.csv","ledger_integrity.json")]
    report={"status":"PASS","reviewer":"ChatGPT (GPT-6 Astra Pro), separate Gate C accounting reviewer","observed_utc":datetime.now(timezone.utc).isoformat(),"source_commit":BASE,"event_count":len(events),"raw_segments_reconstructed":len(reconstructed),"effective_intervals_verified":len(effective),"exclusions_verified":len(spans),"notes_modes_lanes_and_endpoints_match":True,"research_cutoff_monotonic_ns":CUTOFF,"research_cutoff_utc":CUTOFF_UTC,"no_research_credit_after_cutoff":True,"clock_stopped":True,"stop_monotonic_ns":events[-1]["monotonic_ns"],"stop_utc":events[-1]["utc"],"largest_adjacent_observation_gap_ns":max(b["monotonic_ns"]-a["monotonic_ns"] for a,b in zip(events,events[1:])),"mode_and_exclusion_ns":totals,"minutes_decimal":{k:mins(v) for k,v in totals.items()},"research_ns":research,"research_minutes_decimal":mins(research),"engaged_ns":engaged,"engaged_minutes_decimal":mins(engaged),"excluded_ns":excluded,"excluded_minutes_decimal":mins(excluded),"elapsed_ns":elapsed,"elapsed_minutes_decimal":mins(elapsed),"lane_ns":lane_totals,"lane_percent":lane_percent,"forecast_errors_minutes_decimal":errors,"post_b_1":post,"ledger":{"prior_bytes":len(prior),"prior_rows":len(old_rows),"prior_sha256":sha(prior),"append_bytes":len(append),"appended_rows":len(app_rows),"append_sha256":sha(append),"final_bytes":len(current),"final_rows":1105,"final_sha256":sha(current),"original_prefix_exactly_preserved":True},"effective_segment_accounting":effective,"all_appended_fields_match_independent_reconstruction":True,"input_sha256_matches_actuals":True,"concurrent_principal_minutes_added":0,"final_administrative_tail_credited":False,"historical_scientific_reruns":0,"gate_C_author_decision":"PENDING; arithmetic does not enact the recommended pass","input_records":[{"path":p.relative_to(REPO).as_posix(),"bytes":len(p.read_bytes()),"sha256":sha(p.read_bytes())} for p in input_files]}
    output.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ("status","event_count","raw_segments_reconstructed","effective_intervals_verified","engaged_minutes_decimal","research_minutes_decimal","post_b_1","ledger")},indent=2))


if __name__ == "__main__":
    main()
