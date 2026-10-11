"""Append exact stopped-clock P3-09 actuals, preserving all prior ledger bytes.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11. Administrative observer.
No scientific worker is imported or run; raw clocks/dispositions are immutable.
"""
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path
import csv
import hashlib
import importlib.util
import io
import json
import subprocess

getcontext().prec = 48
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = 'f2a240b87d4df07ac91874b092db20b8c4378889'
TASK = 'P3-09'
ATTEMPT = 'P3-09-1'
SESSION = '2026-10-11-S1'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def minutes(ns):
    return format(Decimal(ns) / Decimal(60_000_000_000), '.12f')


def seconds(ns):
    return format(Decimal(ns) / Decimal(1_000_000_000), '.9f')


def save(name, data):
    path = HERE / name
    assert not path.exists(), f'Refuse to overwrite {path}'
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def main():
    assert json.loads((HERE / 'clock_state.json').read_text()) is None
    assert not (HERE / 'actuals.json').exists()
    spec = importlib.util.spec_from_file_location('p309_accounting_clock', HERE / 'clock.py')
    clock = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(clock)
    segments = clock.effective_segments()
    events = clock.read_records(HERE / 'clocks.jsonl')
    assert events[-1]['command'] == 'stop'
    totals = {k: 0 for k in ('D', 'L', 'E', 'O', 'wait', 'idle', 'unmeasured', 'recovery')}
    lanes = {'R': 0, 'X': 0}
    gaps, violations = [], []
    for part in segments:
        totals[part['mode']] += part['elapsed_ns']
        if part['mode'] in ('D', 'L', 'E'):
            lanes[part['lane']] += part['elapsed_ns']
        if part['mode'] in ('D', 'L', 'E', 'O'):
            points = sorted({part['start_monotonic_ns'], part['end_monotonic_ns']} | {
                e['monotonic_ns'] for e in events if e['runtime'] == part['runtime']
                and part['start_monotonic_ns'] <= e['monotonic_ns'] <= part['end_monotonic_ns']})
            for left, right in zip(points, points[1:]):
                gaps.append(right - left)
                if right - left > 900_000_000_000:
                    violations.append({'raw_segment_index': part['raw_segment_index'], 'gap_ns': right-left})
    assert not violations, violations
    research = sum(totals[k] for k in ('D', 'L', 'E'))
    engaged = research + totals['O']
    assert research >= 3_600_000_000_000 and research == sum(lanes.values())
    assert research == 3_647_044_290_715
    assert not (ROOT / 'v3/experiments/final_v1').exists()
    assert sha((ROOT / 'v3/experiments/frozen_v1/manifest.json').read_bytes()) == '69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70'
    base_plan = json.loads(subprocess.check_output(['git', 'show', BASE + ':v3/plan.v1.json'], cwd=ROOT))
    prior = base_plan['observed_progress']
    prior_actuals = json.loads((ROOT / prior['source']).read_bytes())
    two_lanes = {k: lanes[k] + prior_actuals['lane_research_ns'][k] for k in lanes}
    two_total = sum(two_lanes.values())
    assert all(4 * n >= two_total for n in two_lanes.values())
    ledger = ROOT / 'v3/time_ledger.csv'
    original = subprocess.check_output(['git', 'show', BASE + ':v3/time_ledger.csv'], cwd=ROOT)
    assert ledger.read_bytes() == original, 'Unexpected ledger edit or duplicate append.'
    assert original.endswith(b'\n')
    assert len(original) == 192395
    assert sha(original) == 'a9e1d458690b7b29790f71a7f86cb2f2987fad311991d160810af07758153e2a'
    writer_buffer = io.StringIO(newline='')
    writer = csv.writer(writer_buffer, lineterminator='\n')
    for part in segments:
        elapsed = part['elapsed_ns']
        admitted = part['mode'] in ('D', 'L', 'E', 'O')
        excluded = part['mode'] in ('unmeasured', 'recovery')
        status = 'Closed observed principal interval; PREPARATION; ' + part['note']
        if 'disposition_id' in part:
            status += '; disposition=' + part['disposition_id']
        writer.writerow([TASK, ATTEMPT, SESSION, part['mode'], part['lane'],
                         part['start_utc'], part['end_utc'], seconds(elapsed),
                         seconds(elapsed if admitted else 0),
                         seconds(elapsed if part['mode'] == 'wait' else 0),
                         seconds(elapsed if part['mode'] == 'idle' else 0),
                         seconds(elapsed if excluded else 0), 0,
                         'v3/work_logs/R_P3_B_B_2026-10-11_S1.md', status])
    appended = writer_buffer.getvalue().encode('utf-8')
    phase_research = prior['research_ns'] + research
    remaining = max(0, 57_600_000_000_000 - phase_research)
    forecast = json.loads((HERE / 'forecast.json').read_text())
    actuals = {
        'schema': 'value_logic.p309.actuals.v1', 'stage': 'PREPARATION',
        'task': TASK, 'attempt': ATTEMPT, 'session': SESSION,
        'contributor': 'ChatGPT (GPT-6 Astra Pro)', 'base_commit': BASE,
        'clock_stopped': True, 'runtime': clock.RUNTIME,
        'recorded_start_utc': events[0]['utc'], 'recorded_end_utc': events[-1]['utc'],
        'research_ns': research, 'research_minutes': minutes(research),
        'task_research_ns': research, 'task_research_minutes': minutes(research),
        'protected_research_floor_minutes': 60, 'research_floor_satisfied': True,
        'task_floor_margin_ns': research - 3_600_000_000_000, 'task_remaining_floor_ns': 0,
        'prior_verified_task_research_ns': 0, 'historical_recredit_ns': 0,
        'parallel_reviewer_credit_ns': 0,
        'total_engaged_ns': engaged, 'total_engaged_minutes': minutes(engaged),
        'category_ns': totals, 'category_minutes': {k: minutes(v) for k, v in totals.items()},
        'lane_research_ns': lanes, 'lane_research_minutes': {k: minutes(v) for k, v in lanes.items()},
        'lane_percent': {k: str(Decimal(100) * v / research) for k, v in lanes.items()},
        'two_cycle_lane_ns': two_lanes, 'two_cycle_research_ns': two_total,
        'two_cycle_lane_floor_satisfied': True, 'lane_repair_emergency': False,
        'prior_phase_research_ns': prior['research_ns'],
        'prior_phase_measured_engaged_ns': prior['measured_engaged_ns'],
        'phase_research_ns': phase_research, 'phase_research_minutes': minutes(phase_research),
        'phase_measured_engaged_ns': prior['measured_engaged_ns'] + engaged,
        'phase_remaining_floor_ns': remaining, 'phase_remaining_floor_minutes': minutes(remaining),
        'next_phase_checkpoint_minutes': None, 'new_phase_checkpoint_crossed': True,
        'phase_research_floor_satisfied': remaining == 0,
        'phase_floor_overshoot_ns': phase_research - 57_600_000_000_000,
        'checkpoint_record': 'v3/work_logs/P3_09_2026-10-11_S1/checkpoint_960.md',
        'maximum_observed_active_gap_ns': max(gaps), 'cadence_violations': violations,
        'forecast_central_minutes': forecast['central_minutes'],
        'forecast_high_minutes': forecast['high_minutes'],
        'forecast_error_minutes': {k: str(Decimal(totals[k])/Decimal(60_000_000_000)-v)
                                   for k, v in forecast['central_minutes'].items()},
        'forecast_error_scope': 'Closed measured intervals only; subsequent publication administration is unmeasured and credited zero.',
        'additional_recurrence_selected': False,
        'clock_dispositions': {'count': len(clock.read_records(HERE / 'clock_dispositions.jsonl')),
                               'rule': 'Three additive recovery dispositions exclude unobserved tails; raw clocks and segments remain intact.'},
        'ledger': {'base_bytes': len(original), 'base_sha256': sha(original),
                   'base_rows': len(original.splitlines())-1,
                   'append_bytes': len(appended), 'append_rows': len(segments),
                   'append_sha256': sha(appended), 'result_sha256': sha(original+appended),
                   'prior_bytes_preserved': True},
        'clock_source_sha256': sha((HERE / 'clock.py').read_bytes()),
        'accounting_source_sha256': sha(Path(__file__).read_bytes()),
        'phase_two_ledger_sha256': sha((ROOT / 'v2/time_ledger.csv').read_bytes()),
        'publication_tail': 'After the observed stop, status integration, final manifests, transfer, remote verification and response are unmeasured with zero additional engaged or research credit.',
        'status': 'COMPLETE at prospective finite challenge freeze scope; P3-10 unstarted; P3-C/D unattempted; Option C and R-P3-N01 unselected; no final exposure.',
        'experimental_freeze_created': True, 'final_evaluation_exposed': False,
        'freeze_manifest_sha256': sha((ROOT / 'v3/experiments/frozen_v1/manifest.json').read_bytes()),
        'freeze_protocol_sha256': sha((ROOT / 'v3/experiments/protocol.v1.json').read_bytes())}
    save('effective_segments.json', segments)
    (HERE / 'ledger_append.csv').write_bytes(appended)
    with ledger.open('ab') as stream:
        stream.write(appended)
    assert ledger.read_bytes() == original + appended
    save('actuals.json', actuals)
    print(json.dumps({k: actuals[k] for k in ('research_ns', 'research_minutes', 'total_engaged_minutes',
                                             'phase_research_minutes', 'phase_remaining_floor_minutes',
                                             'maximum_observed_active_gap_ns', 'cadence_violations')}))


if __name__ == '__main__':
    main()
