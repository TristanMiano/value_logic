"""Observed F17 clock. Contributor: ChatGPT (GPT-6 Astra Pro).

start/switch/resume MODE LANE NOTE; check NOTE; pause wait|recovery NOTE;
stop NOTE; report. Concurrent agent time is never added.
"""
from datetime import datetime, timezone
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parent
STATE = ROOT / 'clock_state.json'
EVENTS = ROOT / 'clocks.jsonl'
SEGMENTS = ROOT / 'segments.jsonl'


def records(name):
    p = ROOT / name
    return [json.loads(line) for line in p.read_text().splitlines()] if p.exists() else []


def main():
    command, *args = sys.argv[1:]
    state = json.loads(STATE.read_text()) if STATE.exists() else None
    if command == 'report':
        totals = dict.fromkeys(['D', 'L', 'E', 'O', 'wait', 'recovery'], 0)
        lanes = dict.fromkeys(['R', 'X'], 0)
        for s in records('segments.jsonl'):
            totals[s['mode']] += s['elapsed_ns']
            if s['lane'] in lanes:
                lanes[s['lane']] += s['elapsed_ns']
        for ex in records('exclusions.jsonl'):
            n = ex['end_monotonic_ns'] - ex['start_monotonic_ns']
            matching = [s for s in records('segments.jsonl') if s['start_monotonic_ns'] <= ex['start_monotonic_ns'] < ex['end_monotonic_ns'] <= s['end_monotonic_ns']]
            assert len(matching) == 1
            s = matching[0]
            totals[s['mode']] -= n
            totals['recovery'] += n
            if s['lane'] in lanes:
                lanes[s['lane']] -= n
        print(json.dumps({'closed_ns': totals, 'closed_minutes': {k:v/60e9 for k,v in totals.items()}, 'lane_ns': lanes, 'open_segment':state}, indent=2))
        return
    assert command in ['start', 'switch', 'resume', 'pause', 'check', 'stop']
    if command == 'start':
        assert not EVENTS.exists(), 'Preserve this attempt; inspect before resuming.'
    if command in ['start', 'switch', 'resume']:
        mode, lane, *note = args
        assert mode in ['D', 'L', 'E', 'O']
        assert (mode == 'O' and lane == '-') or (mode != 'O' and lane in ['R', 'X'])
        new_mode, new_lane, new_note = mode, '' if lane == '-' else lane, ' '.join(note)
    elif command == 'pause':
        category, *note = args
        assert category in ['wait', 'recovery']
        new_mode, new_lane, new_note = category, '', ' '.join(note)
    now = {'utc':datetime.now(timezone.utc).isoformat(), 'monotonic_ns':time.monotonic_ns(), 'runtime':'linux-F17-S1'}
    event = dict(now, command=command, args=args)
    with EVENTS.open('a') as f:
        f.write(json.dumps(event)+'\n')
    if command == 'check':
        print(json.dumps(event))
        return
    if state is not None:
        segment = dict(state, end_utc=now['utc'], end_monotonic_ns=now['monotonic_ns'], elapsed_ns=now['monotonic_ns']-state['start_monotonic_ns'])
        with SEGMENTS.open('a') as f:
            f.write(json.dumps(segment)+'\n')
    if command == 'stop':
        state = None
    else:
        state = {'mode':new_mode, 'lane':new_lane, 'note':new_note, 'start_utc':now['utc'], 'start_monotonic_ns':now['monotonic_ns'], 'runtime':now['runtime']}
    STATE.write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(event))


if __name__ == '__main__':
    main()
