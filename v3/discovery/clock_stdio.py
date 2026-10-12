"""Principal discovery clock over retained stdin; ChatGPT (GPT-6 Astra Pro), 2026-10-12.

Adapted from clock.py (Codex GPT-6); accounting semantics preserved.
Run serve DIR in a retained exec session; send one JSON request per line.
This transport avoids per-command loopback isolation in the ChatGPT executor.

One resident process makes every UTC/monotonic observation in a session.
init DIR; mark DIR MODE LANE PURPOSE NOTE; report DIR; end DIR NOTE.
Open/unobserved intervals receive no credit. Never resume a dead process:
preserve its records, exclude its open interval, and create a new session.
"""
import csv
from datetime import datetime, timezone
import io
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import uuid


def save(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def append(path, value):
    with path.open('a', encoding='utf-8', newline='') as f:
        f.write(json.dumps(value) + '\n')


def serve(root):
    config = json.loads((root / 'session_config.json').read_text(encoding='utf-8'))
    runtime = f'python-pid-{os.getpid()}-{uuid.uuid4()}'
    state = None
    totals = dict.fromkeys(['D', 'L', 'E', 'O', 'wait', 'idle', 'unmeasured'], 0)
    purposes, lanes = {}, {}
    print(json.dumps({'ready': True, 'runtime': runtime}), flush=True)
    for line in sys.stdin:
        request = json.loads(line)
        command = request['command']
        now = dict(utc=datetime.now(timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(), runtime=runtime)
        if command in ('mark', 'end'):
            mode, lane, purpose = request.get('mode'), request.get('lane'), request.get('purpose')
            if command == 'mark':
                assert mode in totals
                assert lane in ('R', 'X') if mode in ('D', 'L', 'E') else lane == '-'
            append(root / 'events.jsonl', dict(now, **request))
            if state is not None:
                elapsed = now['monotonic_ns'] - state['monotonic_ns']
                # A boundary gap over 15 minutes lacks the required
                # observation cadence; exclude it rather than guess.
                effective = state['mode'] if elapsed <= 900_000_000_000 else 'unmeasured'
                segment = dict(start=state, end=now, elapsed_ns=elapsed, effective_mode=effective,
                               disposition='observed' if effective == state['mode'] else 'cadence_gap_excluded')
                append(root / 'segments.jsonl', segment)
                totals[effective] += elapsed
                if effective in ('D', 'L', 'E'):
                    purposes[state['purpose']] = purposes.get(state['purpose'], 0) + elapsed
                    lanes[state['lane']] = lanes.get(state['lane'], 0) + elapsed
                engaged = elapsed if effective in ('D', 'L', 'E', 'O') else 0
                def seconds(ns):
                    return f'{ns // 10**9}.{ns % 10**9:09d}'
                line = io.StringIO(newline='')
                csv.writer(line, lineterminator='\n').writerow([
                    'P3-SEARCH-01', config['cycle'], root.name, effective,
                    state['lane'] if effective in ('D', 'L', 'E') else '',
                    state['utc'], now['utc'], seconds(elapsed), seconds(engaged),
                    seconds(elapsed if effective == 'wait' else 0),
                    seconds(elapsed if effective == 'idle' else 0),
                    seconds(elapsed if effective == 'unmeasured' else 0), 0,
                    root.relative_to(Path.cwd()).as_posix() + '/session.md',
                    state['purpose'] + ': ' + state['note'] + '; ' + segment['disposition']])
                with Path('v3/time_ledger.csv').open('ab') as ledger:
                    ledger.write(line.getvalue().encode('utf-8'))
            state = None if command == 'end' else dict(now, mode=mode, lane=lane, purpose=purpose, note=request['note'])
        research = sum(totals[m] for m in ('D', 'L', 'E'))
        result = dict(observed=now, closed_ns=totals, research_ns=research,
                      session_config=config,
                      session_research_ns=research,
                      cycle_research_ns=config['prior_cycle_research_ns']+research,
                      program_research_ns=config['prior_program_research_ns']+research,
                      research_minutes=research / 60e9, total_engaged_ns=research + totals['O'],
                      purpose_ns=purposes, lane_ns=lanes,
                      floor_ns=config['cycle_floor_ns'],
                      remaining_floor_ns=max(0, config['cycle_floor_ns']-config['prior_cycle_research_ns']-research),
                      historical_phase_ns=65_167_882_041_849,
                      phase_research_ns=65_167_882_041_849+config['prior_program_research_ns']+research,
                      open_segment=state, status='closed' if command == 'end' else 'active')
        save(root / 'actuals.json', result)
        print(json.dumps(result), flush=True)
        if command == 'end':
            break

def main():
    command, directory = sys.argv[1:]
    assert command == 'serve', 'Use retained stdin JSON requests.'
    serve(Path(directory).resolve())


if __name__ == '__main__':
    main()
