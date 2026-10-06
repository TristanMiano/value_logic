"""Close F16 from observed integer clocks and append, preserving ledger bytes.

Contributor: ChatGPT (GPT-6 Astra Pro). Administrative accounting only.
Run once after clock.py stop; no experiment or external operation is performed.
"""
import csv
from decimal import Decimal, localcontext
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
LEDGER = REPO / 'v2/time_ledger.csv'
NS_PER_SECOND = 10**9
NS_PER_MINUTE = 60 * NS_PER_SECOND
RECOVERY_PAUSES = {25194462035672, 27266802816921, 29780228623458, 32003510910507}
RESEARCH_CUTOFF = 31004665696319


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_lines(name):
    p = ROOT / name
    return [json.loads(line) for line in p.read_text().splitlines()] if p.exists() else []


def minutes(ns):
    with localcontext() as c:
        c.prec = 80
        return str(Decimal(ns) / Decimal(NS_PER_MINUTE))


def seconds(ns):
    return f'{ns // NS_PER_SECOND}.{ns % NS_PER_SECOND:09d}'


def main():
    assert json.loads((ROOT/'clock_state.json').read_text()) is None, 'Stop the principal clock first.'
    for name in ('actuals.json', 'ledger_append.csv', 'ledger_integrity.json'):
        assert not (ROOT/name).exists(), f'Preserve existing {name}; inspect before any resumption.'
    baseline = json.loads((ROOT/'ledger_baseline.json').read_text())
    old = LEDGER.read_bytes()
    assert len(old) == baseline['ledger_bytes'] and sha(old) == baseline['ledger_sha256']
    assert old.endswith(b'\n')
    reader = csv.DictReader(io.StringIO(old.decode()))
    fields = reader.fieldnames
    old_rows = list(reader)
    assert len(old_rows) == baseline['ledger_rows'] == 1006
    assert not any(r['task_id'] == 'F16' for r in old_rows)
    segments = read_lines('segments.jsonl')
    events = read_lines('clocks.jsonl')
    times = {e['monotonic_ns']: e['utc'] for e in events}
    assert all(a['end_monotonic_ns'] == b['start_monotonic_ns'] for a,b in zip(segments,segments[1:]))
    assert events[-1]['command'] == 'stop'
    adjustments = read_lines('adjustments.jsonl')
    reclassifications = read_lines('mode_reclassifications.jsonl')
    assert not adjustments and not reclassifications, 'This close implements the observed no-inline-adjustment record only.'
    exclusions = read_lines('recovery_exclusions.jsonl')
    transfers = read_lines('mode_transfers.jsonl')
    totals = dict.fromkeys(['D','L','E','O','tool_wait','recovery_unobserved','paused_recovery'],0)
    lanes = {'R':0,'X':0}
    rows, effective = [], []
    used_exclusions, used_transfers = set(), set()
    for index,s in enumerate(segments):
        start,end = s['start_monotonic_ns'],s['end_monotonic_ns']
        duration = end-start
        assert Decimal(str(s['elapsed_seconds']))*NS_PER_SECOND == Decimal(duration)
        ex = [e for e in exclusions if e['segment_start_monotonic_ns'] == start]
        ts = [t for t in transfers if t['segment_start_monotonic_ns'] == start]
        assert len(ex)<=1
        if ex:
            assert not ts and Decimal(str(ex[0]['seconds']))*NS_PER_SECOND==Decimal(duration)
            assert ex[0]['observed_end_monotonic_ns']==end
            used_exclusions.add(start)
        cuts = sorted({start,end,*[t['start_monotonic_ns'] for t in ts],*[t['end_monotonic_ns'] for t in ts]})
        assert cuts[0]==start and cuts[-1]==end
        for left,right in zip(cuts,cuts[1:]):
            assert left in times and right in times, 'Every accounting split must have an actual recorded clock event.'
            n = right-left
            mode,lane = s['mode'],s['lane']
            covering = [t for t in ts if t['start_monotonic_ns']<=left and right<=t['end_monotonic_ns']]
            assert len(covering)<=1
            transfer = covering[0] if covering else None
            if transfer:
                assert transfer['from_mode']==mode and transfer['from_lane']==lane
                mode,lane=transfer['mode'],transfer['lane']
                used_transfers.add((start,transfer['start_monotonic_ns']))
            engaged=tool_wait=unmeasured=0
            if ex or mode=='recovery':
                if mode=='recovery':
                    assert transfer and lane=='' and transfer['from_mode']=='O'
                totals['recovery_unobserved']+=n
                category='recovery_unobserved';unmeasured=n;ledger_mode='O';ledger_lane=''
            elif mode=='wait':
                ledger_mode='O';ledger_lane=''
                if start in RECOVERY_PAUSES:
                    totals['paused_recovery']+=n
                    category='paused_recovery';unmeasured=n
                else:
                    totals['tool_wait']+=n
                    category='tool_wait';tool_wait=n
            else:
                assert mode in 'DLEO'
                if mode in 'DLE': assert right<=RESEARCH_CUTOFF
                assert (mode=='O' and lane=='') or (mode in 'DLE' and lane in lanes)
                totals[mode]+=n;engaged=n;category=mode;ledger_mode=mode;ledger_lane=lane
                if lane in lanes:lanes[lane]+=n
            note = 'complete; '+category+'; '+s['note']
            if transfer:note+='; observed mode correction: '+transfer['reason']
            row=dict(zip(fields,['F16','F16-A1','2026-10-05-S1',ledger_mode,ledger_lane,
                 times[left],times[right],seconds(n),seconds(engaged),seconds(tool_wait),'0',
                 seconds(unmeasured),'','v2/work_logs/F16_2026-10-05_S1.md',note]))
            assert Decimal(row['elapsed_seconds'])==sum(Decimal(row[k]) for k in ['engaged_seconds','tool_wait_seconds','idle_seconds','unmeasured_seconds'])
            rows.append(row)
            effective.append({'raw_segment_index_zero_based':index,'start_monotonic_ns':left,'end_monotonic_ns':right,
                              'elapsed_ns':n,'engaged_ns':engaged,'tool_wait_ns':tool_wait,'unmeasured_ns':unmeasured,
                              'category':category,'effective_mode':ledger_mode,'effective_lane':ledger_lane,
                              'transfer':transfer,'raw_segment':s})
    assert used_exclusions=={e['segment_start_monotonic_ns'] for e in exclusions}
    assert used_transfers=={(t['segment_start_monotonic_ns'],t['start_monotonic_ns']) for t in transfers}
    research=sum(totals[k] for k in 'DLE');engaged=research+totals['O']
    elapsed=segments[-1]['end_monotonic_ns']-segments[0]['start_monotonic_ns']
    excluded=sum(totals[k] for k in ['tool_wait','recovery_unobserved','paused_recovery'])
    assert elapsed==engaged+excluded
    assert research==sum(lanes.values())
    assert totals['D']>=60*NS_PER_MINUTE and research>=90*NS_PER_MINUTE
    out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=fields,lineterminator='\n');writer.writerows(rows)
    append=out.getvalue().encode();new=old+append
    with localcontext() as c:
        c.prec=80
        entry=Decimal(baseline['post_b_1_entry_minutes_decimal'])
        close=entry+Decimal(engaged)/Decimal(NS_PER_MINUTE)
        remaining=Decimal(960)-close
        post={'entry_minutes_decimal':str(entry),'close_minutes_decimal':str(close),'remaining_minutes_decimal':str(remaining),
              'checkpoint_minutes':960,'checkpoint_reached':close>=960,'recurrence_clock_reset':False,
              'inherited_declared_minus_historical_csv_seconds_decimal':'0.000073995',
              'inherited_difference_disposition':'Pre-F16 rounded checkpoint carry; preserve authorized baseline and historical rows. No floor/checkpoint impact.'}
    result={'task':'F16','attempt':'F16-A1','session':'2026-10-05-S1','contributor':'ChatGPT (GPT-6 Astra Pro)',
            'runtime':'linux-F16-S1','source_commit':baseline['source_commit'],
            'start_utc':segments[0]['start_utc'],'accounting_cutoff_utc':events[-1]['utc'],
            'accounting_cutoff_monotonic_ns':events[-1]['monotonic_ns'],
            'research_cutoff_monotonic_ns':RESEARCH_CUTOFF,'research_cutoff_utc':times[RESEARCH_CUTOFF],
            'elapsed_ns':elapsed,'mode_and_exclusion_ns':totals,'lane_ns':lanes,
            'minutes_decimal':{k:minutes(v) for k,v in totals.items()},'lane_minutes_decimal':{k:minutes(v) for k,v in lanes.items()},
            'research_ns':research,'research_minutes_decimal':minutes(research),'engaged_ns':engaged,
            'engaged_minutes_decimal':minutes(engaged),'excluded_minutes_decimal':minutes(excluded),
            'floor_D60_pass':True,'floor_Research90_pass':True,'Research90_margin_ns':research-90*NS_PER_MINUTE,
            'concurrent_agent_minutes_credited':0,'O_satisfies_research_floor':False,
            'central_forecast_minutes':{'D':70,'L':15,'E':20,'O':15,'engaged':120,'research':105,'wait':5},
            'high_forecast_minutes':{'D':140,'L':30,'E':40,'O':30,'engaged':240,'research':210,'wait':15},
            'post_b_1':post,'raw_segment_count':len(segments),'ledger_rows_added':len(rows),
            'ledger_prior_rows':len(old_rows),'ledger_final_rows':len(old_rows)+len(rows),
            'ledger_prior_bytes':len(old),'ledger_prior_sha256':sha(old),
            'ledger_append_bytes':len(append),'ledger_append_sha256':sha(append),'ledger_final_sha256':sha(new),
            'effective_segment_accounting':effective,
            'final_administrative_tail':'After cutoff, final accounting audit, placeholder rendering, Git commit/push and chat handoff are uncredited. No additional research is claimed.',
            'input_sha256':{name:sha((ROOT/name).read_bytes()) for name in
                ['clocks.jsonl','segments.jsonl','recovery_exclusions.jsonl','mode_transfers.jsonl','ledger_baseline.json','forecast.json','clock.py','close_accounting.py']}}
    (ROOT/'ledger_append.csv').write_bytes(append)
    (ROOT/'actuals.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    with LEDGER.open('ab') as handle:handle.write(append)
    current=LEDGER.read_bytes()
    assert current==new and current[:len(old)]==old
    integrity={'status':'pass','prior_rows':len(old_rows),'rows_added':len(rows),'final_rows':len(old_rows)+len(rows),
               'prior_bytes_preserved':len(old),'prior_sha256':sha(old),'append_sha256':sha(append),'final_sha256':sha(current),
               'prior_bytes_equal':True,'segments_partition_observed_time':True,'elapsed_equals_engaged_plus_excluded':True}
    (ROOT/'ledger_integrity.json').write_text(json.dumps(integrity,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'pass','research_minutes':minutes(research),'engaged_minutes':minutes(engaged),
                      'rows_added':len(rows),'post_b_1':post},indent=2))


if __name__=='__main__':main()
