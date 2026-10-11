"""Principal discovery clock; Codex (GPT-6), 2026-10-11.

One resident process makes every UTC/monotonic observation in a session.
init DIR; mark DIR MODE LANE PURPOSE NOTE; report DIR; end DIR NOTE.
Open/unobserved intervals receive no credit. Never resume a dead process:
preserve its records, exclude its open interval, and create a new session.
"""
import csv
from datetime import datetime, timezone
import io
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
    runtime = f'python-pid-{os.getpid()}-{uuid.uuid4()}'
    state = None
    totals = dict.fromkeys(['D', 'L', 'E', 'O', 'wait', 'idle', 'unmeasured'], 0)
    purposes, lanes = {}, {}
    with socket.socket() as server:
        server.bind(('127.0.0.1', 0))
        server.listen()
        save(root / 'control.tmp', {'port': server.getsockname()[1], 'runtime': runtime})
        while True:
            connection, _ = server.accept()
            with connection:
                request = json.loads(connection.makefile('rb').readline())
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
                            'P3-SEARCH-01', 'P3-SEARCH-01-C001', root.name, effective,
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
                              research_minutes=research / 60e9, total_engaged_ns=research + totals['O'],
                              purpose_ns=purposes, lane_ns=lanes,
                              floor_ns=14_400_000_000_000,
                              remaining_floor_ns=max(0, 14_400_000_000_000-research),
                              historical_phase_ns=65_167_882_041_849,
                              phase_research_ns=65_167_882_041_849+research,
                              open_segment=state, status='closed' if command == 'end' else 'active')
                save(root / 'actuals.json', result)
                connection.sendall((json.dumps(result) + '\n').encode())
                if command == 'end':
                    break


def main():
    command, directory, *args = sys.argv[1:]
    root = Path(directory).resolve()
    if command == 'serve':
        serve(root)
        return
    if command == 'init':
        root.mkdir(parents=True, exist_ok=True)
        assert not (root / 'events.jsonl').exists(), 'Inspect prior session; do not overwrite.'
        flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        with (root / 'server.log').open('ab') as log:
            subprocess.Popen([sys.executable, '-u', __file__, 'serve', str(root)],
                             stdout=log, stderr=log, creationflags=flags)
        for _ in range(100):
            if (root / 'control.tmp').exists():
                break
            time.sleep(.02)
        command = 'report'
    request = {'command': command}
    if command == 'mark':
        request.update(zip(('mode', 'lane', 'purpose'), args[:3]))
        request['note'] = ' '.join(args[3:])
    elif command == 'end':
        request['note'] = ' '.join(args)
    control = json.loads((root / 'control.tmp').read_text())
    with socket.create_connection(('127.0.0.1', control['port']), timeout=5) as client:
        client.sendall((json.dumps(request) + '\n').encode())
        print(client.makefile('r').readline().strip())


if __name__ == '__main__':
    main()
