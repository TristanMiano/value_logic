"""Close P3-08's stopped observed clock and append the existing ledger.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. Administrative, no research.
Refuses repeated closure and any change to the inspected baseline ledger.
"""
from pathlib import Path
from decimal import Decimal, getcontext
from hashlib import sha256
import csv
import importlib.util
import io
import json

getcontext().prec = 50
ROOT = Path(__file__).resolve().parents[3]
S = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('p308_clock', S / 'clock.py')
cl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cl)


def h(b): return sha256(b).hexdigest()
def mins(n): return f'{Decimal(n) / Decimal(60000000000):.12f}'
def secs(n): return f'{Decimal(n) / Decimal(1000000000):.9f}'
def save(p, value):
    with p.open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def main():
    assert json.loads((S / 'clock_state.json').read_text()) is None
    assert not (S / 'actuals.json').exists(), 'Already closed; no duplicate credit.'
    recovery = json.loads((S / 'recovery/state.json').read_text())
    forecast = json.loads((S / 'forecast.json').read_text())
    prior_path = ROOT / 'v3/work_logs/R_P3_B_A_2026-10-09_S1/actuals.json'
    prior_bytes = prior_path.read_bytes()
    assert h(prior_bytes) == recovery['prior_actuals_sha256']
    prior = json.loads(prior_bytes)
    assert prior['phase_research_ns'] == 45270901966800
    assert prior['phase_measured_engaged_ns'] == 51615754683964
    segments = cl.effective_segments()
    events = cl.read_records(S / 'clocks.jsonl')
    assert events[-1]['command'] == 'stop'
    categories = {mode: sum(s['elapsed_ns'] for s in segments if s['mode'] == mode)
                  for mode in ('D', 'L', 'E', 'O', 'wait', 'idle', 'unmeasured', 'recovery')}
    research = sum(categories[k] for k in ('D', 'L', 'E'))
    assert research >= 5400000000000
    engaged = research + categories['O']
    lanes = {lane: sum(s['elapsed_ns'] for s in segments if s['lane'] == lane and s['mode'] in ('D', 'L', 'E'))
             for lane in ('R', 'X')}
    assert sum(lanes.values()) == research
    assert all(4 * n >= research for n in lanes.values())
    paired_lanes = {k: prior['lane_research_ns'][k] + lanes[k] for k in lanes}
    paired_research = prior['research_ns'] + research
    assert sum(paired_lanes.values()) == paired_research
    assert all(4 * n >= paired_research for n in paired_lanes.values())
    identities = set()
    cadence_gaps = []
    for s in segments:
        identity = (s['runtime'], s['start_monotonic_ns'], s['end_monotonic_ns'])
        assert identity not in identities
        identities.add(identity)
        assert s['elapsed_ns'] == s['end_monotonic_ns'] - s['start_monotonic_ns']
        if s['mode'] not in ('D', 'L', 'E', 'O'):
            continue
        points = sorted(set([s['start_monotonic_ns'], s['end_monotonic_ns']] +
                            [e['monotonic_ns'] for e in events if s['start_monotonic_ns'] <= e['monotonic_ns'] <= s['end_monotonic_ns']]))
        cadence_gaps.extend(b-a for a, b in zip(points, points[1:]))
    assert max(cadence_gaps, default=0) <= 900000000000
    for left, right in zip(segments, segments[1:]):
        assert left['end_monotonic_ns'] == right['start_monotonic_ns']
    ledger = ROOT / 'v3/time_ledger.csv'
    base = ledger.read_bytes()
    assert len(base) == recovery['prior_ledger_bytes'] == 167557
    assert h(base) == recovery['prior_ledger_sha256']
    assert base.endswith(b'\n')
    reader = csv.DictReader(io.StringIO(base.decode()))
    fields = reader.fieldnames
    assert fields == ['task_id','attempt_id','session_id','mode','lane','start_utc','end_utc',
                      'elapsed_seconds','engaged_seconds','tool_wait_seconds','idle_seconds',
                      'unmeasured_seconds','forecast_seconds','artifact','status']
    old_rows = list(reader)
    assert len(old_rows) == 398 and not any(r['task_id'] == 'P3-08' for r in old_rows)
    v2sha = h((ROOT / 'v2/time_ledger.csv').read_bytes())
    assert v2sha == '5c71a4727f1cb7e03565f1c495b0c63b351863583120f0ec5684aca48bd122c6'
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
    seen = set()
    for s in segments:
        mode, n = s['mode'], s['elapsed_ns']
        active = mode in ('D', 'L', 'E', 'O')
        expected = forecast['central_minutes'][mode] * 60 if active and mode not in seen else 0
        seen.add(mode)
        writer.writerow(dict(task_id='P3-08', attempt_id='P3-08-1', session_id='2026-10-10-S1',
            mode=mode, lane=s['lane'], start_utc=s['start_utc'], end_utc=s['end_utc'],
            elapsed_seconds=secs(n), engaged_seconds=secs(n if active else 0),
            tool_wait_seconds=secs(n if mode == 'wait' else 0), idle_seconds=secs(n if mode == 'idle' else 0),
            unmeasured_seconds=secs(n if mode in ('unmeasured', 'recovery') else 0),
            forecast_seconds=str(expected), artifact='v3/work_logs/P3_08_2026-10-10_S1.md',
            status='Closed observed principal interval; DEVELOPMENT; '+s['note']))
    appended = out.getvalue().encode()
    combined = base + appended
    receipt = dict(base_bytes=len(base), base_sha256=h(base), base_rows=len(old_rows),
                   append_bytes=len(appended), append_rows=len(segments), append_sha256=h(appended),
                   result_sha256=h(combined), prior_bytes_preserved=True)
    phase = prior['phase_research_ns'] + research
    remaining = max(0, 57600000000000-phase)
    actuals = dict(schema='value_logic.p308.actuals.v1', stage='DEVELOPMENT', task='P3-08',
        attempt='P3-08-1', session='2026-10-10-S1', contributor='ChatGPT (GPT-6 Astra Pro)',
        base_commit=recovery['remote_main'], clock_stopped=True, runtime=cl.RUNTIME,
        recorded_start_utc=events[0]['utc'], recorded_end_utc=events[-1]['utc'],
        research_ns=research, research_minutes=mins(research), task_research_ns=research,
        task_research_minutes=mins(research), protected_research_floor_minutes=90,
        research_floor_satisfied=True, task_floor_margin_ns=research-5400000000000,
        task_remaining_floor_ns=0, prior_verified_task_research_ns=0,
        historical_recredit_ns=0, parallel_reviewer_credit_ns=0,
        prior_clock_recovery='Entry found no earlier P3-08 clock. Four additive context-recovery dispositions and one conservative failed-switch disposition preserve raw observations and forfeit inseparable tails.',
        total_engaged_ns=engaged, total_engaged_minutes=mins(engaged),
        category_ns=categories, category_minutes={k: mins(v) for k, v in categories.items()},
        lane_research_ns=lanes, lane_research_minutes={k: mins(v) for k, v in lanes.items()},
        lane_percent={k: str(Decimal(v)*100/Decimal(research)) for k, v in lanes.items()},
        two_cycle_lane_ns=paired_lanes, two_cycle_research_ns=paired_research,
        two_cycle_lane_floor_satisfied=True, lane_repair_emergency=False,
        prior_phase_research_ns=prior['phase_research_ns'],
        prior_phase_measured_engaged_ns=prior['phase_measured_engaged_ns'],
        phase_research_ns=phase, phase_research_minutes=mins(phase),
        phase_measured_engaged_ns=prior['phase_measured_engaged_ns']+engaged,
        phase_remaining_floor_ns=remaining, phase_remaining_floor_minutes=mins(remaining),
        next_phase_checkpoint_minutes=960, new_phase_checkpoint_crossed=False,
        maximum_observed_active_gap_ns=max(cadence_gaps), cadence_violations=[],
        forecast_central_minutes=forecast['central_minutes'], forecast_high_minutes=forecast['high_minutes'],
        forecast_error_minutes={k: str(Decimal(categories[k])/Decimal(60000000000)-Decimal(v))
                                for k, v in forecast['central_minutes'].items()},
        forecast_error_scope='Measured closed intervals only; O excludes all later unmeasured publication work and is not total administration cost.',
        recurrence_reserve_consumed_minutes=0,
        ledger=receipt, phase_two_ledger_sha256=v2sha,
        accounting_source_sha256=h(Path(__file__).read_bytes()),
        publication_tail='After the observed stop, all further status integration, manifests, packaging, transfer, remote verification and response are conservatively unmeasured with zero additional engaged or research credit. No elapsed duration is inferred.',
        status='COMPLETE at finite owned-broker, paid-reporting and separate structural implementation scopes; P3-09 unstarted; P3-C/D unattempted; optional recurrences unselected.')
    # Every arithmetic/identity guard precedes the one append mutation.
    with ledger.open('ab') as f: f.write(appended)
    assert ledger.read_bytes() == combined and combined[:len(base)] == base
    with (S / 'ledger_append.csv').open('xb') as f: f.write(appended)
    save(S / 'ledger_append_receipt.json', receipt)
    with (S / 'effective_segments.jsonl').open('x') as f:
        for s in segments: f.write(json.dumps(s)+'\n')
    save(S / 'actuals.json', actuals)
    save(S / 'boundary_accounting.json', dict(status='PASS', stage='DEVELOPMENT',
        clock_closed=True, research90_satisfied=True, research_ns=research,
        phase_research_ns=phase, ledger_prior_bytes_preserved=True, effective_segments=len(segments),
        all_segment_arithmetic_exact=True, no_duplicate_intervals=True,
        all_lanes_reconcile=True, two_cycle_lane_floor_satisfied=True,
        historical_and_parallel_recredit_ns=0, cadence_violations=[],
        phase_two_ledger_unchanged=True,
        original_clock_events_sha256=h((S / 'clocks.jsonl').read_bytes()),
        raw_segments_sha256=h((S / 'segments.jsonl').read_bytes()),
        dispositions_sha256=h((S / 'clock_dispositions.jsonl').read_bytes()),
        effective_segments_sha256=h((S / 'effective_segments.jsonl').read_bytes())))
    print(json.dumps({k: actuals[k] for k in ('research_ns','research_minutes','total_engaged_minutes',
        'category_minutes','lane_percent','phase_research_minutes','phase_remaining_floor_minutes','ledger')}, indent=2))


if __name__ == '__main__': main()
