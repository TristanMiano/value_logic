"""Audit recorded cycle-II timing against same-file monotonic endpoints."""
import csv
import hashlib
import io
import json
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = 'd50905e89be0741feb9a1993fefb5db3424f957d'
raw = subprocess.run(['git', 'show', BASE + ':v2/time_ledger.csv'],
                     cwd=ROOT, check=True, capture_output=True).stdout
rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8'))))
selected = [(i, r) for i, r in enumerate(rows, 2)
            if r['task_id'] in {'F05', 'F06', 'F07', 'F08', 'F09', 'F10'}]
totals = defaultdict(lambda: defaultdict(float))
lanes = defaultdict(float)
issues, unmatched, verified, intervals = [], [], [], []
clock_cache = {}


def stamp(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def readings(path):
    if path not in clock_cache:
        result = {}
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            obj = json.loads(line)
            if 'utc' not in obj:
                continue
            if 'ticks' in obj:
                value, freq = obj['ticks'], obj['frequency']
            else:
                value = obj.get('monotonic_ns', obj.get('mono_ns'))
                freq = 1e9
            if value is not None:
                result[stamp(obj['utc'])] = (value, freq)
        clock_cache[path] = result
    return clock_cache[path]


for i, row in selected:
    task, mode = row['task_id'], row['mode']
    credit = float(row['engaged_seconds'] or 0)
    elapsed = float(row['elapsed_seconds'] or 0)
    totals[task][mode] += credit
    if mode not in ('D', 'L', 'E') or credit <= 0:
        continue
    lanes[row['lane']] += credit
    a, b = stamp(row['start_utc']), stamp(row['end_utc'])
    intervals.append((a, b, i))
    if b < a or credit > elapsed + .005:
        issues.append({'row': i, 'problem': 'credit outside elapsed bounds'})
    prefix = task + '_' + row['session_id'].replace('-S', '_S').replace('-public', '_public')
    paths = list((ROOT / 'v2/work_logs').glob(prefix + '*clock.jsonl'))
    paths += list((ROOT / 'v2/work_logs' / prefix).glob('*clock*.jsonl'))
    match = False
    for path in paths:
        data = readings(path)
        if a in data and b in data and data[a][1] == data[b][1]:
            seconds = (data[b][0] - data[a][0]) / data[a][1]
            if abs(seconds - elapsed) <= .005:
                verified.append({'row': i, 'path': path.relative_to(ROOT).as_posix()})
                match = True
                break
    if not match:
        unmatched.append({'row': i, 'task': task, 'session': row['session_id'],
                          'start': row['start_utc'], 'end': row['end_utc']})
intervals.sort()
for prev, nxt in zip(intervals, intervals[1:]):
    if nxt[0] < prev[1]:
        issues.append({'rows': [prev[2], nxt[2]], 'problem': 'overlapping research intervals'})
floors = {'F05': ('D', 60), 'F06': ('D', 90), 'F07': ('D', 90),
          'F08': ('D', 90), 'F09': ('D', 60), 'F10': ('L', 45)}
mode_totals = {m: sum(v[m] for v in totals.values()) for m in ('D', 'L', 'E')}
research = sum(mode_totals.values())
report = {
    'base_commit': BASE, 'input_bytes': len(raw), 'input_sha256': hashlib.sha256(raw).hexdigest(),
    'historical_rows': len(rows), 'cycle_II_rows': len(selected),
    'recorded_mode_minutes': {t: {m: n / 60 for m, n in v.items()} for t, v in totals.items()},
    'floor_checks': {t: {'mode': m, 'required_minutes': n,
                        'recorded_minutes': totals[t][m] / 60, 'met': totals[t][m] >= n * 60}
                     for t, (m, n) in floors.items()},
    'cycle_II_research_minutes': research / 60,
    'cycle_II_mode_percent': {m: 100 * n / research for m, n in mode_totals.items()},
    'cycle_II_lane_percent': {l: 100 * n / research for l, n in lanes.items()},
    'positive_research_rows': len(intervals), 'monotonic_elapsed_matches': len(verified),
    'matches': verified, 'unmatched_rows': unmatched, 'accounting_issues': issues,
    'limits': 'Recorded work-block audit, not independent observation of past cognition. '
              'Original credit/exclusions retained; empty durations remain unknown. '
              'Only pair endpoints in the same raw file and frequency; no cross-boot subtraction. '
              'Gate A retains the F01-F04 audit; this report adds F05-F10, excluding Gate B.'
}
(ROOT / 'v2/checkpoints/B_1_timing_review.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k != 'matches'}, indent=2))
raise SystemExit(bool(unmatched or issues or not all(v['met'] for v in report['floor_checks'].values())))
