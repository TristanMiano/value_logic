"""Read-only Gate C entry accounting and scientific-byte audit.

Contributor: ChatGPT (GPT-6 Astra Pro), separate accounting/integrity reviewer.
Writes only its own new review artifacts; does not execute experimental code.
"""
from collections import defaultdict
import csv
from datetime import datetime, timezone
from decimal import Decimal, getcontext
import hashlib
import io
import json
from pathlib import Path
import subprocess
import time

getcontext().prec = 80
ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE = "de7b456d08f383e72dfcabd278c183db324fdf16"
D = Decimal
ZERO = D(0)
EXPECTED_LEDGER_SHA = "2ddbbff7ccbc4c76bd15f3c26a58273be562ba21f6967b9d1d87feab7958c8fa"
GROUPS = [
    ("N01", "N01-A1", "N01_2026-10-02_S1", [("D+L", 60)]),
    ("N01", "R-N01-01-C3", "N01R_2026-10-02_S1", [("D+L", 120)]),
    ("F11", "R-N01-01-C1", "F11_2026-10-03_S1", [("E", 60)]),
    ("F12", "R-N01-01-C2", "F12_2026-10-03_S1", [("E", 60)]),
    ("F13", "R-N01-01-F13-A", "F13_2026-10-04_S1", [("D", 60), ("D+L+E", 90)]),
    ("C4", "R-N01-01-C4-A", "C4_2026-10-04_S1", [("D+L+E", 60)]),
    ("F14", "F14-A", "F14_2026-10-04_S1", [("D+L+E", 90)]),
    ("F15", "F15-A", "F15_2026-10-04_S1", [("E", 60)]),
    ("F15-ND01", "F15-ND01-A1", "F15_ND01_2026-10-05_S1", [("D+L+E", 90)]),
    ("F16", "F16-A1", "F16_2026-10-05_S1", [("D", 60), ("D+L+E", 90)]),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def file_record(path):
    p = ROOT / path
    b = p.read_bytes()
    return {"path": str(path), "bytes": len(b), "sha256": sha(b)}


def dec(n):
    return str(n)


def aggregate(rows):
    modes = {m: sum((D(r["engaged_seconds"] or "0") for r in rows if r["mode"] == m), ZERO) for m in ("D", "L", "E", "O")}
    research = sum((modes[m] for m in ("D", "L", "E")), ZERO)
    lanes = {l: sum((D(r["engaged_seconds"] or "0") for r in rows if r["mode"] in ("D", "L", "E") and r["lane"] == l), ZERO) for l in ("R", "X")}
    assert sum(lanes.values(), ZERO) == research
    return {
        "row_count": len(rows),
        "mode_seconds_exact": {k: dec(v) for k, v in modes.items()},
        "mode_minutes_decimal": {k: dec(v / 60) for k, v in modes.items()},
        "research_seconds_exact": dec(research),
        "research_minutes_decimal": dec(research / 60),
        "engaged_seconds_exact": dec(sum(modes.values(), ZERO)),
        "engaged_minutes_decimal": dec(sum(modes.values(), ZERO) / 60),
        "lane_seconds_exact": {k: dec(v) for k, v in lanes.items()},
        "lane_minutes_decimal": {k: dec(v / 60) for k, v in lanes.items()},
        "research_mode_percent": {k: dec(modes[k] / research * 100) for k in ("D", "L", "E")},
        "research_lane_percent": {k: dec(v / research * 100) for k, v in lanes.items()},
        "positive_research_rows": sum(r["mode"] in ("D", "L", "E") and D(r["engaged_seconds"] or "0") > 0 for r in rows),
    }


def combine_lanes(*stats):
    r = sum((D(s["research_seconds_exact"]) for s in stats), ZERO)
    lanes = {k: sum((D(s["lane_seconds_exact"][k]) for s in stats), ZERO) for k in ("R", "X")}
    return {"research_seconds_exact": dec(r), "lane_seconds_exact": {k: dec(v) for k, v in lanes.items()}, "lane_percent": {k: dec(v / r * 100) for k, v in lanes.items()}, "both_lanes_at_least_25_percent": all(4 * v >= r for v in lanes.values())}


def stamp(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def main():
    started_utc = datetime.now(timezone.utc).isoformat()
    started_ns = time.monotonic_ns()
    names = ["historical_timing.json", "scientific_hash_checks.json"]
    assert not any((OUT / n).exists() for n in names), "Preserve prior results; do not silently overwrite."
    raw = subprocess.run(["git", "show", BASE + ":v2/time_ledger.csv"], cwd=ROOT, check=True, capture_output=True).stdout
    assert len(raw) == 265648 and sha(raw) == EXPECTED_LEDGER_SHA
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    assert len(rows) == 1096
    current_raw = (ROOT / "v2/time_ledger.csv").read_bytes()
    assert current_raw[:len(raw)] == raw
    assert current_raw == raw, "This preliminary audit expects no Gate C append yet."
    baseline = load("v2/work_logs/C_2026-10-06_S1/baseline.json")
    assert baseline["source_commit"] == BASE and baseline["ledger_sha256"] == sha(raw)
    assert baseline["ledger_rows"] == len(rows) and baseline["ledger_bytes"] == len(raw)
    selected = []
    groups = []
    row_checks = []
    issues = []
    sources = []
    serialization_differences = []
    intervals = []
    for task, attempt, folder, floors in GROUPS:
        matches = [(i, r) for i, r in enumerate(rows, 2) if r["task_id"] == task and r["attempt_id"] == attempt]
        assert matches
        rr = [r for _, r in matches]
        selected.extend(rr)
        a = aggregate(rr)
        a.update({"task": task, "attempt": attempt, "folder": "v2/work_logs/" + folder})
        a["floors"] = []
        for required_modes, minimum in floors:
            value = sum((D(a["mode_seconds_exact"][m]) for m in required_modes.split("+")), ZERO)
            a["floors"].append({"modes": required_modes, "minimum_minutes": minimum, "observed_seconds_exact": dec(value), "observed_minutes_decimal": dec(value / 60), "margin_seconds_exact": dec(value - minimum * 60), "satisfied": value >= minimum * 60})
        clock_path = "v2/work_logs/" + folder + "/clocks.jsonl"
        events = [json.loads(s) for s in (ROOT / clock_path).read_text(encoding="utf-8-sig").splitlines()]
        event_index = {}
        endpoint_source = {}
        observed = []
        for e in events:
            if "utc" not in e:
                continue
            if "ticks" in e:
                reading, frequency = int(e["ticks"]), int(e["frequency"])
            else:
                reading, frequency = e.get("monotonic_ns", e.get("mono_ns")), 10**9
            if reading is None:
                continue
            event_index[e["utc"]] = (reading, frequency)
            endpoint_source[e["utc"]] = "top-level recorded clock event"
            if "boundary_utc" in e and "boundary_monotonic_ns" in e:
                event_index[e["boundary_utc"]] = (e["boundary_monotonic_ns"], 10**9)
                endpoint_source[e["boundary_utc"]] = "explicit nested recovery boundary in clocks.jsonl"
            if isinstance(e.get("boundary"), dict) and "monotonic_ns" in e["boundary"]:
                b = e["boundary"]
                event_index[b["utc"]] = (b["monotonic_ns"], 10**9)
                endpoint_source[b["utc"]] = "explicit nested recovery boundary in clocks.jsonl"
            observed.append((reading, frequency))
        # One F14 recovery boundary is retained in its segment record rather
        # than a standalone event. The same-file exclusion event corroborates
        # its UTC label and exact elapsed duration. Do not manufacture a new
        # observation or require old files to use this audit's preferred schema.
        if folder == "F14_2026-10-04_S1":
            segment_path = "v2/work_logs/" + folder + "/segments.jsonl"
            saved_segments = [json.loads(s) for s in (ROOT / segment_path).read_text().splitlines()]
            for e in events:
                if e.get("command") != "recovery_exclusion" or "excluded_seconds" not in e:
                    continue
                matches_boundary = [s for s in saved_segments if s["mode"] == "recovery" and s["end_utc"] == e["utc"]]
                assert len(matches_boundary) == 1
                b = matches_boundary[0]
                assert b["end_monotonic_ns"] == e["monotonic_ns"]
                assert b["end_monotonic_ns"] - b["start_monotonic_ns"] == D(str(e["excluded_seconds"])) * 10**9
                assert b["start_utc"].split("T", 1)[1].split("+", 1)[0] in " ".join(e.get("args", []))
                event_index[b["start_utc"]] = (b["start_monotonic_ns"], 10**9)
                endpoint_source[b["start_utc"]] = "saved same-runtime segment boundary corroborated by exact clock-event recovery exclusion"
            sources.append(file_record(segment_path))
        gaps = [D(b[0]-x[0])/x[1] for x,b in zip(observed, observed[1:]) if x[1] == b[1]]
        a["clock_event_count"] = len(events)
        a["largest_adjacent_observation_gap_seconds"] = dec(max(gaps, default=ZERO))
        sources.append(file_record(clock_path))
        actual_path = "v2/work_logs/" + folder + "/actuals.json"
        actual = load(actual_path)
        sources.append(file_record(actual_path))
        if isinstance(actual.get("engaged_minutes"), dict):
            reported_modes = actual["engaged_minutes"]
        else:
            reported_modes = actual.get("minutes", actual.get("minutes_decimal"))
        mode_error = {k: abs(D(str(reported_modes[k])) - D(a["mode_minutes_decimal"][k])) for k in ("D", "L", "E", "O")}
        a["actuals_mode_display_absolute_difference_minutes"] = {k: dec(v) for k, v in mode_error.items()}
        assert all(v <= D("0.0000005") for v in mode_error.values())
        for i, r in matches:
            e = D(r["elapsed_seconds"] or "0")
            c = D(r["engaged_seconds"] or "0")
            parts = sum((D(r[k] or "0") for k in ("engaged_seconds", "tool_wait_seconds", "idle_seconds", "unmeasured_seconds")), ZERO)
            delta = parts - e
            # Historical Windows CSV fields were independently rounded to 0.1 microsecond.
            if delta != 0:
                serialization_differences.append({"row": i, "partition_minus_elapsed_seconds": dec(delta)})
            if c < 0 or c > e or abs(delta) > D("0.0000005"):
                issues.append({"row": i, "problem": "invalid credit or partition", "partition_delta": dec(delta)})
            if r["start_utc"] not in event_index or r["end_utc"] not in event_index:
                issues.append({"row": i, "problem": "missing same-file observed endpoint"})
                continue
            start, sf = event_index[r["start_utc"]]
            end, ef = event_index[r["end_utc"]]
            delta_elapsed = D(end-start)/sf - e
            if sf != ef or end < start or abs(delta_elapsed) > D("0.0000000005"):
                issues.append({"row": i, "problem": "elapsed does not match recorded monotonic endpoints", "delta_seconds": dec(delta_elapsed)})
            row_checks.append({"row": i, "task": task, "attempt": attempt, "clock_path": clock_path, "elapsed_seconds_exact": dec(e), "monotonic_elapsed_difference_seconds": dec(delta_elapsed), "start_endpoint_source":endpoint_source[r["start_utc"]], "end_endpoint_source":endpoint_source[r["end_utc"]]})
            if c > 0:
                intervals.append((stamp(r["start_utc"]), stamp(r["end_utc"]), i, r["mode"]))
            if r["mode"] in ("D", "L", "E") and c > 0 and r["lane"] not in ("R", "X"):
                issues.append({"row": i, "problem": "research credit missing lane"})
        groups.append(a)
    intervals.sort()
    for prev, nxt in zip(intervals, intervals[1:]):
        if prev[1] > nxt[0]:
            issues.append({"rows": [prev[2], nxt[2]], "problem": "overlapping positive engaged intervals"})
    cycle_i = aggregate([r for r in rows if r["task_id"] in ["F01","F02","F03","F04"]])
    cycle_ii = aggregate([r for r in rows if r["task_id"] in ["F05","F06","F07","F08","F09","F10"]])
    required_iii = aggregate([r for r in selected if r["task_id"] in ["F11","F12","F13","F14","F15","F16"]])
    broad_iii = aggregate(selected)
    for prior, prefix_size, expected in [("v2/checkpoints/A_1_timing_review.json",78295,"baa3852d0e063ad6fa580d8be73236a5ec8575fbb8945956336faf204bf7a458"),("v2/checkpoints/B_1_timing_review.json",154563,"3c2726ff685ef15c82817a0f9fac32fc99fc59fdd143f056304f9b71bcf741a5")]:
        assert sha(raw[:prefix_size]) == expected
        sources.append(file_record(prior))
    f16 = load("v2/work_logs/F16_2026-10-05_S1/actuals.json")
    assert f16["ledger_final_sha256"] == sha(raw) and f16["ledger_final_rows"] == len(rows)
    f16stats = groups[-1]
    assert all(D(f16stats["mode_seconds_exact"][m]) * 10**9 == f16["mode_and_exclusion_ns"][m] for m in ("D","L","E","O"))
    declared = D(baseline["post_b_1_entry_minutes_decimal"])
    assert declared == D(f16["post_b_1"]["close_minutes_decimal"])
    difference_seconds = declared * 60 - D(broad_iii["engaged_seconds_exact"])
    assert abs(difference_seconds - D("0.000073995")) < D("1e-40")
    timing = {
        "contributor": "ChatGPT (GPT-6 Astra Pro), separate Gate C accounting/integrity reviewer",
        "source_commit": BASE,
        "ledger": {"bytes":len(raw),"rows":len(rows),"sha256":sha(raw),"current_matches_source_exactly":True},
        "cycle_I":cycle_i,"cycle_II":cycle_ii,"cycle_III_required_F11_F16":required_iii,"cycle_III_broader_post_B_before_Gate_C":broad_iii,
        "two_cycle_lane_checks":{"I_plus_II":combine_lanes(cycle_i,cycle_ii),"II_plus_required_III":combine_lanes(cycle_ii,required_iii),"II_plus_broader_III":combine_lanes(cycle_ii,broad_iii)},
        "groups":groups,"all_recorded_floors_satisfied":all(f["satisfied"] for g in groups for f in g["floors"]),
        "row_endpoint_checks":row_checks,"same_file_monotonic_endpoint_matches":len(row_checks),"positive_engaged_rows_checked_for_overlap":len(intervals),"issues":issues,
        "historical_partition_serialization_differences":serialization_differences,
        "mode_display_rounding_tolerance_minutes":"0.0000005","historical_partition_rounding_tolerance_seconds":"0.0000005",
        "post_b_1":{"authorized_entry_minutes_decimal":str(declared),"historical_csv_engaged_seconds_exact":broad_iii["engaged_seconds_exact"],"inherited_declared_minus_csv_seconds_decimal":dec(difference_seconds),"preserved_inherited_discrepancy_seconds":"0.000073995","remaining_to_960_minutes_decimal":str(D(960)-declared),"no_reset":True},
        "Gate_C_final_accounting":"Pending stopped raw clock and actuals; this audit credits no Gate C or concurrent-agent time.",
        "input_records":sources,
        "started_utc":started_utc,
    }

    manifest_checks = []
    for path, expected, count in [("v2/experiments/freeze.v1.json","b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c",34),("v2/experiments/neural_diagnostic_v1/freeze.json","9c15af55b83d7edf134542a9c70bcc0f087c6f4f6491f993361a27493b5cf24c",47)]:
        record = file_record(path)
        assert record["sha256"] == expected
        manifest = load(path)
        files = ([dict(v,path=k) for k,v in manifest["files"].items()] if isinstance(manifest["files"],dict) else manifest["files"])
        assert len(files) == count
        checks=[]
        for f in files:
            found=file_record(f["path"])
            checks.append(dict(found,expected_bytes=f["bytes"],expected_sha256=f["sha256"],matches=found["bytes"]==f["bytes"] and found["sha256"]==f["sha256"]))
        manifest_checks.append(dict(record,registered_count=count,all_registered_match=all(c["matches"] for c in checks),members=checks))
    inventory_path = "v2/work_logs/F16_2026-10-05_S1/reviews/integrity/inventory_before.json"
    inventory = load(inventory_path)
    assert len(inventory["files"]) == 973
    checks=[]
    for f in inventory["files"]:
        found=file_record(f["path"])
        checks.append(dict(found,expected_sha256=f["sha256"],expected_bytes=f["bytes"],matches=found["sha256"]==f["sha256"] and found["bytes"]==f["bytes"]))
    run_checks=[]
    for run in ("v2/work_logs/F15_v1_run1","v2/work_logs/F15_ND01_v1_run1"):
        sidecars=[]
        for p in sorted((ROOT/run).rglob("*.sha256")):
            target=p.with_suffix("")
            found=file_record(target.relative_to(ROOT).as_posix())
            expected=p.read_text().strip().split()[0]
            sidecars.append(dict(found,expected_sha256=expected,matches=found["sha256"]==expected))
        run_checks.append({"run":run,"sidecar_count":len(sidecars),"matching_sidecars":sum(c["matches"] for c in sidecars),"exceptions":[c for c in sidecars if not c["matches"]],"sidecars":sidecars,"attempt_directories":sorted(p.name for p in (ROOT/run).glob("*_attempt_*") if p.is_dir())})
    recovered=file_record("v2/work_logs/F15_2026-10-04_S1/retention_results_recovered.json")
    recovered["matches_original_aggregate_sidecar"] = recovered["sha256"] == "0b0d9f79a7e74ddecef52bf5d20654eb433a5472d66cc3df63f84ae27dd04691" and recovered["bytes"]==15833616
    reports=[file_record(p) for p in ("v2/experiments/results.md","v2/experiments/F15_ND01_results.md")]
    scientific={"source_commit":BASE,"contributor":timing["contributor"],"method":"Direct standard-library byte reads and SHA256, no import or invocation of experiment code","registered_freezes":manifest_checks,"inventory_source":file_record(inventory_path),"inventory_count":len(checks),"inventory_all_match":all(c["matches"] for c in checks),"inventory_checks":checks,"runs":run_checks,"exact_recovery":recovered,"reports":reports,"scientific_stage_executions":0,"principal_concurrent_minutes_added":0,"started_utc":started_utc}
    assert not issues and timing["all_recorded_floors_satisfied"]
    assert all(c["all_registered_match"] for c in manifest_checks) and scientific["inventory_all_match"]
    assert [c["matching_sidecars"] for c in run_checks] == [180,103]
    assert run_checks[0]["exceptions"][0]["path"] == "v2/work_logs/F15_v1_run1/evaluation_attempt_1/retention_results.json"
    assert recovered["matches_original_aggregate_sidecar"]
    for record in (timing,scientific):
        record["finished_utc"]=datetime.now(timezone.utc).isoformat()
        record["check_process_wall_ns"]=time.monotonic_ns()-started_ns
    for n,record in zip(names,(timing,scientific)):
        (OUT/n).write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"historical_timing":file_record((OUT/names[0]).relative_to(ROOT).as_posix()),"scientific_hash_checks":file_record((OUT/names[1]).relative_to(ROOT).as_posix()),"post_B_rows":len(selected),"endpoint_matches":len(row_checks),"floors_all_satisfied":timing["all_recorded_floors_satisfied"],"issues":issues,"scientific_inventory_matches":len(checks),"sidecars_matches":[r["matching_sidecars"] for r in run_checks]},indent=2))


if __name__ == "__main__":
    main()
