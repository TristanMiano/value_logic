#!/usr/bin/env python3
"""Replay S2's new repair clock only; never append the S1 Research90 interval.
Python 3.10+, standard library. A --write refuses existing finalized outputs.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json
from pathlib import Path
from decimal import Decimal
from datetime import datetime
FIELDS='task_id,attempt_id,session_id,mode,lane,start_utc,end_utc,elapsed_seconds,engaged_seconds,tool_wait_seconds,idle_seconds,unmeasured_seconds,forecast_seconds,artifact,status'.split(',')
SESSION='v3/work_logs/P3_04_2026-10-08_S2'
def seconds(ns):return f'{ns//10**9}.{ns%10**9:09d}'
def minutes(ns):return f'{Decimal(ns)/Decimal(60_000_000_000):.12f}'
def replay(root):
    raw=(root/'clocks.jsonl').read_bytes();dispraw=(root/'clock_dispositions.json').read_bytes()
    events=[json.loads(s) for s in raw.splitlines()];ds=json.loads(dispraw)
    forecast=json.loads((root/'forecast.json').read_bytes());base=json.loads((root/'accounting_base.json').read_bytes())
    if not events or events[0]['event']!='start' or events[-1]['event']!='stop':raise ValueError('Clock not closed.')
    replacements={}
    for d in ds:
        if d['end_index']!=d['start_index']+1 or d['start_index'] in replacements:raise ValueError('Overlapping or non-adjacent disposition.')
        replacements[d['start_index']]=d
    segments=[];categories={k:0 for k in ('D','L','E','O','unmeasured','wait','recovery','idle')};lanes={'R':0,'X':0};cadence=[]
    for i,(a,b) in enumerate(zip(events,events[1:])):
        if a['runtime']!=b['runtime']:raise ValueError('Cross-runtime subtraction forbidden.')
        ns=b['monotonic_ns']-a['monotonic_ns']
        if ns<0:raise ValueError('Nonmonotone clock.')
        if abs((datetime.fromisoformat(b['utc'])-datetime.fromisoformat(a['utc'])).total_seconds()-ns/1e9)>1:raise ValueError('UTC/monotonic mismatch.')
        mode=a['mode'];note=a['note'];disposition=None
        if i in replacements:
            d=replacements[i];mode=d['classification'];note=d['note'];disposition=d['id']
        if mode not in categories:raise ValueError('Unknown mode.')
        lane=a['lane'] if mode in ('D','L','E') else ''
        if mode in ('D','L','E','O') and ns>900_000_000_000:cadence.append(i)
        if lane not in ('','R','X') or mode in ('D','L','E') and not lane:raise ValueError('Research lane missing.')
        categories[mode]+=ns
        if lane:lanes[lane]+=ns
        segments.append({'index':i,'mode':mode,'lane':lane,'start_utc':a['utc'],'end_utc':b['utc'],'start_monotonic_ns':a['monotonic_ns'],'end_monotonic_ns':b['monotonic_ns'],'runtime':a['runtime'],'elapsed_ns':ns,'disposition':disposition,'note':note})
    research=sum(categories[k] for k in ('D','L','E'));engaged=research+categories['O'];combined=research+base['original_research_ns']
    text=io.StringIO(newline='');writer=csv.DictWriter(text,fieldnames=FIELDS,lineterminator='\n')
    for s in segments:
        mode=s['mode'];ns=s['elapsed_ns'];row={k:'0.000000000' for k in FIELDS}
        row.update(task_id='P3-04',attempt_id='P3-04-1',session_id='2026-10-08-S2',mode=mode,lane=s['lane'],
            start_utc=s['start_utc'],end_utc=s['end_utc'],elapsed_seconds=seconds(ns),engaged_seconds=seconds(ns if mode in ('D','L','E','O') else 0),
            tool_wait_seconds=seconds(ns if mode=='wait' else 0),idle_seconds=seconds(ns if mode=='idle' else 0),unmeasured_seconds=seconds(ns if mode in ('unmeasured','recovery') else 0),
            forecast_seconds=seconds(forecast['central_minutes'].get(mode,0)*60_000_000_000),artifact=SESSION+'.md',status='New S2 evidence repair; no duplicate S1 credit; '+(s['disposition']+'; ' if s['disposition'] else '')+s['note'])
        writer.writerow(row)
    append=text.getvalue().encode('utf-8');pr=base['phase_research_ns']+research;pe=base['phase_measured_engaged_ns']+engaged
    out={'schema':'value_logic.p304.repair_actuals.v1','task':'P3-04','attempt':'P3-04-1','session':'2026-10-08-S2','contributor':'ChatGPT (GPT-6 Astra Pro)',
         'base_commit':base['base_commit'],'base_ledger_blob':base['base_ledger_blob'],'base_ledger_bytes':base['base_ledger_bytes'],'clock_stopped':True,
         'research_ns':research,'research_minutes':minutes(research),'measured_engaged_ns':engaged,'measured_engaged_minutes':minutes(engaged),
         'original_research_ns':base['original_research_ns'],'task_research_ns':combined,'task_research_minutes':minutes(combined),'research_floor_satisfied':combined>=5400000000000,
         'additional_research_floor_ns':0,'remaining_task_floor_ns':max(0,5400000000000-combined),'category_ns':categories,'category_minutes':{k:minutes(v) for k,v in categories.items()},
         'lane_ns':lanes,'lane_minutes':{k:minutes(v) for k,v in lanes.items()},'phase_research_ns':pr,'phase_research_minutes':minutes(pr),
         'phase_measured_engaged_ns':pe,'phase_measured_engaged_minutes':minutes(pe),'phase_remaining_floor_ns':max(0,57600000000000-pr),
         'phase_remaining_floor_minutes':minutes(max(0,57600000000000-pr)),'effective_segments':segments,'cadence_violations':cadence,
         'append_bytes':len(append),'append_rows':len(segments),'append_sha256':hashlib.sha256(append).hexdigest(),'raw_clocks_sha256':hashlib.sha256(raw).hexdigest(),
         'dispositions_sha256':hashlib.sha256(dispraw).hexdigest(),'concurrent_effort_credited_ns':0,'post_cutoff_administration_credited_ns':0,
         'cutoff':events[-1],'forecast':'forecast.json','cycle_scope':'Cycle II still incomplete; no completed two-cycle compliance inferred.',
         'ledger_status':'S2_APPEND_PREPARED_NOT_POSTED; S1 already posted on base','publication_status':'ZIP prepared for user apply and ordinary push; no direct write'}
    return out,append

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args();root=Path(__file__).resolve().parent;out,append=replay(root)
    if a.write:
        for name in ('actuals.json','ledger_append.csv'):
            if (root/name).exists():raise ValueError('Refusing finalized-output overwrite.')
        (root/'actuals.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');(root/'ledger_append.csv').write_bytes(append)
    else:
        if out!=json.loads((root/'actuals.json').read_bytes()) or append!=(root/'ledger_append.csv').read_bytes():raise ValueError('Saved accounting differs.')
    print(json.dumps({k:out[k] for k in ('research_minutes','task_research_minutes','measured_engaged_minutes','phase_research_minutes','phase_remaining_floor_minutes','append_rows','cadence_violations')},indent=2))
if __name__=='__main__':main()
