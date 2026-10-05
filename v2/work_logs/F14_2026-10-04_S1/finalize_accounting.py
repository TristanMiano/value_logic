"""Append F14's measured segments without rewriting historical ledger bytes.

Contributor: ChatGPT (GPT-6 Astra Pro). Administrative serialization only.
Run once after the principal clock is stopped. No research time is inferred.
"""
import csv
import hashlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]


def main():
    assert json.loads((ROOT / "clock_state.json").read_text()) is None
    segments = [json.loads(x) for x in (ROOT / "segments.jsonl").read_text().splitlines()]
    adjustments = [json.loads(x) for x in (ROOT / "adjustments.jsonl").read_text().splitlines()]
    starts = {s["start_monotonic_ns"] for s in segments}
    assert all(a["segment_start_monotonic_ns"] in starts for a in adjustments)
    totals = dict.fromkeys(("D", "L", "E", "O", "wait", "recovery"), 0.0)
    lanes = {"R": 0.0, "X": 0.0}
    forecast = {"D": 1800, "L": 1200, "E": 2400, "O": 900}
    seen_modes = set()
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    for segment in segments:
        elapsed = segment["elapsed_seconds"]
        excluded_wait = sum(a["observed_wait_seconds"] for a in adjustments
                            if a["segment_start_monotonic_ns"] == segment["start_monotonic_ns"])
        assert 0 <= excluded_wait <= elapsed
        mode = segment["mode"]
        measured = elapsed - excluded_wait
        totals[mode] += measured
        totals["wait"] += excluded_wait
        if segment["lane"] in lanes:
            lanes[segment["lane"]] += measured
        engaged = measured if mode in forecast else 0.0
        wait = excluded_wait + (elapsed if mode == "wait" else 0.0)
        unmeasured = elapsed if mode == "recovery" else 0.0
        ledger_mode = "E" if mode == "wait" else "O" if mode == "recovery" else mode
        forecast_seconds = forecast[mode] if mode in forecast and mode not in seen_modes else ""
        seen_modes.add(mode)
        status = ("complete; measured principal segment" if mode in forecast else
                  "excluded tool wait" if mode == "wait" else "excluded recovery; no engaged credit")
        status += "; " + segment["note"]
        writer.writerow(["F14", "F14-A", "2026-10-04-S1", ledger_mode,
                         segment["lane"], segment["start_utc"], segment["end_utc"],
                         f"{elapsed:.9f}", f"{engaged:.9f}", f"{wait:.9f}",
                         "0", f"{unmeasured:.9f}", forecast_seconds,
                         "v2/work_logs/F14_2026-10-04_S1.md", status])
    gaps = [(b["start_monotonic_ns"]-a["end_monotonic_ns"])/1e9
            for a, b in zip(segments, segments[1:])]
    assert all(g >= 0 for g in gaps), "overlapping principal segments"
    wall_seconds = (segments[-1]["end_monotonic_ns"]-segments[0]["start_monotonic_ns"])/1e9
    assert abs(wall_seconds-sum(totals.values())-sum(gaps)) < 1e-7
    minutes = {key: value/60 for key, value in totals.items()}
    research = sum(minutes[key] for key in ("D", "L", "E"))
    engaged = research+minutes["O"]
    assert research >= 90
    assert abs(sum(lanes.values())/60-research) < 1e-7
    cumulative = 534.976816+engaged
    replacements = {
        "F14_O_MINUTES": f"{minutes['O']:.6f}",
        "F14_O_DELTA": f"{minutes['O']-15:+.6f}",
        "F14_TOTAL_MINUTES": f"{engaged:.6f}",
        "F14_TOTAL_DELTA": f"{engaged-105:+.6f}",
        "F14_WAIT_MINUTES": f"{minutes['wait']:.6f}",
        "F14_WAIT_DELTA": f"{minutes['wait']-5:+.6f}",
        "F14_RECOVERY_MINUTES": f"{minutes['recovery']:.6f}",
        "F14_START_UTC": segments[0]["start_utc"],
        "F14_END_UTC": segments[-1]["end_utc"],
        "F14_WALL_MINUTES": f"{wall_seconds/60:.6f}",
        "F14_GAP_SECONDS": f"{sum(gaps):.9f}",
        "POST_B_TOTAL_MINUTES": f"{cumulative:.6f}",
        "POST_B_REMAINING_MINUTES": f"{960-cumulative:.6f}",
    }
    documents = [REPO / "TODO_v2.md", ROOT.parent / "F14_2026-10-04_S1.md"]
    document_texts = []
    for path in documents:
        content = path.read_text()
        assert "{{F14_TOTAL_MINUTES}}" in content, "already finalized"
        for key, value in replacements.items():
            content = content.replace("{{"+key+"}}", value)
        assert "{{F14_" not in content and "{{POST_B_" not in content
        document_texts.append((path, content))
    ledger = REPO / "v2/time_ledger.csv"
    prior = ledger.read_bytes()
    assert b"\nF14," not in prior and b'\n"F14",' not in prior
    assert prior.endswith(b"\n")
    appended = buffer.getvalue().encode("utf-8")
    actuals = {
        "schema": "F14-measured-actuals-v1", "status": "complete at prospective-freeze scope",
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "source_revision": "6ce41d7caaba8b66cf813fc5949a92f95d42766c",
        "start_utc": segments[0]["start_utc"], "accounting_cutoff_utc": segments[-1]["end_utc"],
        "runtime": "linux-F14-S1", "principal_segments": len(segments),
        "minutes": minutes, "research_minutes": research, "engaged_minutes": engaged,
        "lane_minutes": {k: v/60 for k, v in lanes.items()},
        "research_floor_minutes": 90, "research_floor_satisfied": True,
        "observed_wall_minutes": wall_seconds/60, "uncredited_transition_gap_seconds": sum(gaps),
        "uncredited_administrative_tail": "Final ledger serialization, commit/push handling and response after cutoff; not quantified or credited.",
        "uncredited_preclock_work": "Initial acquisition and focused repository orientation before first timing event.",
        "parallel_agent_minutes_added": 0,
        "central_forecast_minutes": {"D": 30, "L": 20, "E": 40, "O": 15, "engaged": 105, "wait": 5},
        "high_forecast_minutes": {"D": 45, "L": 30, "E": 60, "O": 20, "engaged": 155, "wait": 15},
        "central_forecast_error_minutes": {**{k: minutes[k]-v for k, v in {"D": 30, "L": 20, "E": 40, "O": 15, "wait": 5}.items()},
                                            "research": research-90, "engaged": engaged-105},
        "post_b_1": {"entry_minutes": 534.976816, "inherited_eight_hour_overshoot_minutes": 54.976816,
                     "close_minutes": cumulative, "next_checkpoint_minutes": 960,
                     "remaining_minutes": 960-cumulative, "recurrence_clock_reset": False},
        "ledger_prior_bytes": len(prior), "ledger_prior_sha256": hashlib.sha256(prior).hexdigest(),
        "ledger_append_sha256": hashlib.sha256(appended).hexdigest(), "ledger_rows_added": len(segments),
        "F15_started": False, "gate_C_D_attempted": False, "continuation_required": False,
    }
    ledger.write_bytes(prior+appended)
    assert ledger.read_bytes()[:len(prior)] == prior
    for path, content in document_texts:
        path.write_text(content)
    (ROOT / "actuals.json").write_text(json.dumps(actuals, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"research_minutes": research, "engaged_minutes": engaged,
                      "O_minutes": minutes["O"], "wait_minutes": minutes["wait"],
                      "recovery_minutes": minutes["recovery"], "post_b_close_minutes": cumulative,
                      "remaining_to_sixteen_hours": 960-cumulative, "ledger_rows_added": len(segments)}, indent=2))


if __name__ == "__main__":
    main()
