"""Close Gate D's observed principal clock and append exact ledger intervals.

Contributor: ChatGPT (GPT-6 Astra Pro). Administrative accounting only.
Requires a stopped clock; refuses existing outputs or a changed ledger prefix.
"""
import csv
from decimal import Decimal, localcontext
import hashlib
import io
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
LEDGER = REPO / 'v2/time_ledger.csv'
NS = 10**9


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_lines(name):
    p = ROOT / name
    return [json.loads(line) for line in p.read_text().splitlines()] if p.exists() else []


def seconds(n):
    assert isinstance(n,int) and n >= 0
    return f'{n//NS}.{n%NS:09d}'


def minutes(n):
    with localcontext() as c:
        c.prec = 80
        return str(Decimal(n)/Decimal(60*NS))


def main():
    assert json.loads((ROOT/'clock_state.json').read_text()) is None, 'Stop the observed clock first.'
    for name in ['actuals.json','ledger_append.csv','ledger_integrity.json']:
        assert not (ROOT/name).exists(), f'Preserve existing output: {name}'
    baseline = json.loads((ROOT/'baseline.json').read_text())
    forecast = json.loads((ROOT/'forecast.json').read_text())
    old = LEDGER.read_bytes()
    assert len(old) == baseline['ledger_bytes'] and sha(old) == baseline['ledger_sha256']
    assert old.endswith(b'\n')
    reader = csv.DictReader(io.StringIO(old.decode()))
    fields, previous = reader.fieldnames, list(reader)
    assert len(previous) == baseline['ledger_rows']
    assert not any(r['task_id'] == 'D' or r['attempt_id'] == 'D_1' for r in previous)
    events, segments, exclusions = (read_lines(n) for n in ['clocks.jsonl','segments.jsonl','exclusions.jsonl'])
    assert events[0]['command'] == 'start' and events[-1]['command'] == 'stop'
    assert all(e['runtime'] == 'linux-GateD-S1' for e in events)
    assert all(a['monotonic_ns'] < b['monotonic_ns'] for a,b in zip(events,events[1:]))
    transitions = [e for e in events if e['command'] != 'check']
    assert len(segments) == len(transitions)-1
    observed = {e['monotonic_ns']:e['utc'] for e in events}
    research_segments = [s for s in segments if s['mode'] in ['D','L','E']]
    research_cutoff = max(s['end_monotonic_ns'] for s in research_segments)
    research_cutoff_utc = observed[research_cutoff]
    for s,a,b in zip(segments,transitions,transitions[1:]):
        assert s['runtime'] == a['runtime'] == b['runtime']
        assert s['start_monotonic_ns'] == a['monotonic_ns'] and s['end_monotonic_ns'] == b['monotonic_ns']
        assert s['start_utc'] == a['utc'] and s['end_utc'] == b['utc']
        assert s['elapsed_ns'] == b['monotonic_ns']-a['monotonic_ns'] > 0
        if a['command'] == 'pause':
            assert s['mode'] == a['args'][0] and s['lane'] == ''
        else:
            assert s['mode'] == a['args'][0]
            assert s['lane'] == ('' if a['args'][1] == '-' else a['args'][1])
    exclusions.sort(key=lambda e:e['start_monotonic_ns'])
    for i,e in enumerate(exclusions):
        left,right = e['start_monotonic_ns'],e['end_monotonic_ns']
        assert left in observed and right in observed and left < right
        assert i == 0 or exclusions[i-1]['end_monotonic_ns'] <= left
        assert sum(s['start_monotonic_ns'] <= left < right <= s['end_monotonic_ns'] for s in segments) == 1
    totals = dict.fromkeys(['D','L','E','O','tool_wait','recovery_unobserved','paused_recovery'],0)
    lanes, rows, effective = {'R':0,'X':0}, [], []
    for index,s in enumerate(segments):
        start,end = s['start_monotonic_ns'],s['end_monotonic_ns']
        ex = [e for e in exclusions if start <= e['start_monotonic_ns'] < e['end_monotonic_ns'] <= end]
        cuts = sorted({start,end,*[e['start_monotonic_ns'] for e in ex],*[e['end_monotonic_ns'] for e in ex]})
        for left,right in zip(cuts,cuts[1:]):
            n = right-left
            covering = [e for e in ex if e['start_monotonic_ns'] <= left < right <= e['end_monotonic_ns']]
            assert len(covering) <= 1
            engaged = waiting = unmeasured = 0
            mode,lane = s['mode'],s['lane']
            if covering:
                category='recovery_unobserved'; unmeasured=n; mode='O'; lane=''
            elif mode == 'recovery':
                category='paused_recovery'; unmeasured=n; mode='O'; lane=''
            elif mode == 'wait':
                category='tool_wait'; waiting=n; mode='O'; lane=''
            else:
                assert mode in ['D','L','E','O']
                assert (mode == 'O' and lane == '') or (mode != 'O' and lane in lanes)
                category=mode; engaged=n
                ticks=sorted({left,right,*[t for t in observed if left<t<right]})
                assert max(b-a for a,b in zip(ticks,ticks[1:])) <= 900*NS
                if lane: lanes[lane] += n
            totals[category] += n
            note='Gate D assessment complete; author phase decision pending; '+category+'; '+s['note']
            if covering: note+='; exclusion: '+covering[0]['reason']
            row=dict(zip(fields,['D','D_1','2026-10-06-S1',mode,lane,
                observed[left],observed[right],seconds(n),seconds(engaged),seconds(waiting),'0',
                seconds(unmeasured),'','v2/work_logs/D_2026-10-06_S1.md',note]))
            assert Decimal(row['elapsed_seconds']) == sum(Decimal(row[k]) for k in
                ['engaged_seconds','tool_wait_seconds','idle_seconds','unmeasured_seconds'])
            rows.append(row)
            effective.append({'raw_segment_index':index,'start_monotonic_ns':left,'end_monotonic_ns':right,
                'elapsed_ns':n,'engaged_ns':engaged,'tool_wait_ns':waiting,'unmeasured_ns':unmeasured,
                'category':category,'effective_mode':mode,'effective_lane':lane})
    research=sum(totals[k] for k in ['D','L','E'])
    engaged=research+totals['O']
    elapsed=events[-1]['monotonic_ns']-events[0]['monotonic_ns']
    excluded=sum(totals[k] for k in ['tool_wait','recovery_unobserved','paused_recovery'])
    assert research == sum(lanes.values()) and elapsed == engaged+excluded
    assigned_forecasts = set()
    for row in rows:
        mode = row['mode']
        if Decimal(row['engaged_seconds']) > 0 and mode not in assigned_forecasts:
            row['forecast_seconds'] = str(forecast['central_minutes'][mode] * 60)
            assigned_forecasts.add(mode)
    assert assigned_forecasts <= {'D','L','E','O'}
    assert assigned_forecasts == {k for k in ['D','L','E','O'] if totals[k] > 0}
    out=io.StringIO(newline='')
    csv.DictWriter(out,fieldnames=fields,lineterminator='\n').writerows(rows)
    append=out.getvalue().encode()
    with localcontext() as c:
        c.prec=80
        entry=Decimal(forecast['post_b_1_entry_minutes'])
        close=entry+Decimal(engaged)/Decimal(60*NS)
        remaining=Decimal(1920)-close
        post={'entry_minutes_decimal':str(entry),'close_minutes_decimal':str(close),
            'remaining_minutes_decimal':str(remaining),'checkpoint_minutes':1920,
            'previous_checkpoint_minutes':960,'previous_checkpoint_completed_in_F17':True,
            'checkpoint_reached':close>=1920,'automatic_next_phase_authorized':False,'recurrence_clock_reset':False,
            'inherited_declared_minus_historical_csv_seconds_decimal':'0.000073995'}
    actuals={'task':'D','attempt':'D_1','session':'2026-10-06-S1','runtime':'linux-GateD-S1',
        'contributor':'ChatGPT (GPT-6 Astra Pro)','source_commit':baseline['head'],
        'task_status':'COMPLETE_AT_FINAL_AUDIT_SCOPE','gate_c_author_decision':'PASS','gate_d_evaluator_recommendation':'PASS','gate_d_author_decision':'PENDING','protected_minimum':None,
        'start_utc':events[0]['utc'],'accounting_cutoff_utc':events[-1]['utc'],
        'accounting_cutoff_monotonic_ns':events[-1]['monotonic_ns'],
        'research_cutoff_monotonic_ns':research_cutoff,'research_cutoff_utc':research_cutoff_utc,
        'elapsed_ns':elapsed,'mode_and_exclusion_ns':totals,'lane_ns':lanes,
        'minutes_decimal':{k:minutes(v) for k,v in totals.items()},
        'lane_minutes_decimal':{k:minutes(v) for k,v in lanes.items()},
        'research_ns':research,'research_minutes_decimal':minutes(research),
        'engaged_ns':engaged,'engaged_minutes_decimal':minutes(engaged),
        'excluded_ns':excluded,'excluded_minutes_decimal':minutes(excluded),
        'post_b_1':post,'concurrent_agent_minutes_credited':0,
        'central_forecast_minutes':forecast['central_minutes'],'high_forecast_minutes':forecast['high_minutes'],
        'forecast_error_minutes_decimal': {mode: minutes(totals[mode] - forecast['central_minutes'][mode]*60*NS) for mode in ['D','L','E','O']},
        'raw_segment_count':len(segments),'ledger_rows_added':len(rows),
        'ledger_prior_rows':len(previous),'ledger_final_rows':len(previous)+len(rows),
        'ledger_prior_bytes':len(old),'ledger_prior_sha256':sha(old),
        'ledger_append_bytes':len(append),'ledger_append_sha256':sha(append),
        'ledger_final_sha256':sha(old+append),'effective_segment_accounting':effective,
        'final_administrative_tail':'After cutoff, independent accounting checks, rendering exact actuals into status documents, final link/status checks, commit/push, optional ZIP transfer and chat are uncredited; no further research is claimed.',
        'input_sha256':{name:sha((ROOT/name).read_bytes()) for name in
            ['clock.py','close_accounting.py','forecast.json','baseline.json','clocks.jsonl','segments.jsonl','exclusions.jsonl','clock_state.json']}}
    (ROOT/'ledger_append.csv').write_bytes(append)
    (ROOT/'actuals.json').write_text(json.dumps(actuals,indent=2,sort_keys=True)+'\n')
    with LEDGER.open('ab') as f:
        f.write(append); f.flush(); os.fsync(f.fileno())
    current=LEDGER.read_bytes()
    assert current == old+append and current[:len(old)] == old
    integrity={'status':'pass','prior_rows':len(previous),'rows_added':len(rows),
        'final_rows':len(previous)+len(rows),'prior_bytes_preserved':len(old),
        'prior_sha256':sha(old),'append_sha256':sha(append),'final_sha256':sha(current),
        'prior_bytes_equal':True,'observed_time_exactly_partitioned':True,
        'exclusions_contained_and_nonoverlapping':True,'clock_stopped':True}
    (ROOT/'ledger_integrity.json').write_text(json.dumps(integrity,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'pass','engaged_minutes':minutes(engaged),
        'research_minutes':minutes(research),'ledger_rows_added':len(rows),'post_b_1':post},indent=2))


if __name__ == '__main__':
    main()
