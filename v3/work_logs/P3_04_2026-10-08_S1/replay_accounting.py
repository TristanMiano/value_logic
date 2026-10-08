#!/usr/bin/env python3
"""Replay closed P3-04 observation intervals; never create or infer clock time."""
from __future__ import annotations
import argparse
from collections import Counter
from decimal import Decimal, ROUND_HALF_EVEN
import csv
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path

BASE='688ff3b6c2f10a70d83c58a9ca7610cd32cb5e21'
BASE_RESEARCH=16770123676163
BASE_ENGAGED=20679685797109
BASE_LEDGER_BLOB='4ab14148f6c518dea2be8bc245beb91d971e846e'
BASE_LEDGER_BYTES=54245
FLOOR=5400000000000
PHASE_FLOOR=57600000000000
SESSION='v3/work_logs/P3_04_2026-10-08_S1'
FIELDS='task_id,attempt_id,session_id,mode,lane,start_utc,end_utc,elapsed_seconds,engaged_seconds,tool_wait_seconds,idle_seconds,unmeasured_seconds,forecast_seconds,artifact,status'.split(',')


def minutes(ns:int)->str:
    return str((Decimal(ns)/Decimal(60000000000)).quantize(Decimal('0.000000000001'),rounding=ROUND_HALF_EVEN))


def seconds(ns:int)->str:
    return f'{ns//1000000000}.{ns%1000000000:09d}'


def replay(root:Path):
    events=[json.loads(line) for line in (root/'clocks.jsonl').read_text().splitlines() if line]
    ds=json.loads((root/'clock_dispositions.json').read_text())
    if not events or events[-1]['event']!='stop':raise ValueError('Clock must have a durable stop observation')
    categories=Counter();lanes=Counter();segments=[];cadence=[]
    for a,b in zip(events,events[1:]):
        if a['runtime']!=b['runtime']:raise ValueError('Unbridged runtime change')
        start,end=a['monotonic_ns'],b['monotonic_ns']
        if end<start:raise ValueError('Nonmonotonic observed time')
        contained=[d for d in ds if d['runtime']==a['runtime'] and d['start_monotonic_ns']<=start and end<=d['end_monotonic_ns']]
        if len(contained)>1:raise ValueError('Overlapping dispositions')
        for d in ds:
            overlaps=max(start,d['start_monotonic_ns'])<min(end,d['end_monotonic_ns'])
            if overlaps and d not in contained:raise ValueError('Disposition must align with observed boundaries')
        mode=contained[0]['effective_mode'] if contained else a['mode']
        lane='' if contained else a['lane']
        ns=end-start
        if mode not in ('D','L','E','O','wait','idle','recovery','unmeasured'):raise ValueError('Unknown mode')
        if mode in ('D','L','E'):
            if lane not in ('R','X'):raise ValueError('Research interval lacks a lane')
            lanes[lane]+=ns
            if ns>900000000000:cadence.append({'start':a['utc'],'end':b['utc'],'elapsed_ns':ns})
        categories[mode]+=ns
        segments.append({'start_utc':a['utc'],'end_utc':b['utc'],'start_monotonic_ns':start,'end_monotonic_ns':end,
             'elapsed_ns':ns,'runtime':a['runtime'],'mode':mode,'lane':lane,'note':a['note'],
             'disposition_id':contained[0]['id'] if contained else None})
    research=sum(categories[m] for m in ('D','L','E'));engaged=research+categories['O']
    out={'schema':'value_logic.p304.actuals.v1','task':'P3-04','attempt':'P3-04-1','session':'2026-10-08-S1',
         'contributor':'ChatGPT (GPT-6 Astra Pro)','base_commit':BASE,'clock_stopped':True,'cutoff':events[-1],
         'research_ns':research,'research_minutes':minutes(research),'research_floor_ns':FLOOR,
         'remaining_task_floor_ns':max(0,FLOOR-research),'research_floor_satisfied':research>=FLOOR,
         'measured_engaged_ns':engaged,'measured_engaged_minutes':minutes(engaged),
         'category_ns':dict(categories),'category_minutes':{k:minutes(v) for k,v in categories.items()},
         'lane_ns':dict(lanes),'lane_minutes':{k:minutes(v) for k,v in lanes.items()},
         'phase_research_ns':BASE_RESEARCH+research,'phase_research_minutes':minutes(BASE_RESEARCH+research),
         'phase_measured_engaged_ns':BASE_ENGAGED+engaged,'phase_measured_engaged_minutes':minutes(BASE_ENGAGED+engaged),
         'phase_remaining_floor_ns':PHASE_FLOOR-BASE_RESEARCH-research,
         'phase_remaining_floor_minutes':minutes(PHASE_FLOOR-BASE_RESEARCH-research),
         'base_ledger_blob':BASE_LEDGER_BLOB,'base_ledger_bytes':BASE_LEDGER_BYTES,
         'cadence_violations':cadence,'effective_segments':segments,'disposition_count':len(ds),
         'post_cutoff_administration_credited_ns':0,'concurrent_effort_credited_ns':0,
         'forecast_file':'forecast.json','forecast_research_central_minutes':110,'forecast_research_high_minutes':180,
         'forecast_qualification':'Mode subdivisions are forecasts, not separate floors; O and waits separate.',
         'cycle_scope':'Cycle II remains incomplete. Task R/X amounts are recorded; completed two-cycle lane compliance is not asserted.',
         'publication_status':'NOT_PUBLISHED; guarded local package requires application and normal push',
         'ledger_status':'APPEND_PREPARED_NOT_POSTED; one guarded append on the exact base'}
    text=io.StringIO(newline='');writer=csv.DictWriter(text,fieldnames=FIELDS,lineterminator='\n')
    forecast_seconds={'D':'3900.000000000','L':'1200.000000000','E':'1500.000000000','O':'900.000000000'}
    for s in segments:
        mode=s['mode'];ns=s['elapsed_ns'];d={k:'0.000000000' for k in FIELDS}
        d.update(task_id='P3-04',attempt_id='P3-04-1',session_id='2026-10-08-S1',mode=mode,lane=s['lane'],
            start_utc=s['start_utc'],end_utc=s['end_utc'],elapsed_seconds=seconds(ns),
            engaged_seconds=seconds(ns if mode in ('D','L','E','O') else 0),
            tool_wait_seconds=seconds(ns if mode=='wait' else 0),idle_seconds=seconds(ns if mode=='idle' else 0),
            unmeasured_seconds=seconds(ns if mode in ('recovery','unmeasured') else 0),
            forecast_seconds=forecast_seconds.get(mode,'0.000000000'),artifact=SESSION+'.md',
            status='Closed P3-04 observation; finite semantics task complete; P3-05 unstarted; '+
                (s['disposition_id']+'; ' if s['disposition_id'] else '')+s['note'])
        writer.writerow(d)
    append=text.getvalue().encode('utf-8')
    out.update(append_bytes=len(append),append_rows=len(segments),append_sha256=hashlib.sha256(append).hexdigest(),
               raw_clocks_sha256=hashlib.sha256((root/'clocks.jsonl').read_bytes()).hexdigest(),
               dispositions_sha256=hashlib.sha256((root/'clock_dispositions.json').read_bytes()).hexdigest())
    return out,append


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    root=Path(__file__).resolve().parent;obj,append=replay(root)
    if args.write:
        for name in ('actuals.json','ledger_append.csv'):
            if (root/name).exists():raise ValueError('Refusing to overwrite finalized accounting')
        (root/'actuals.json').write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
        (root/'ledger_append.csv').write_bytes(append)
    elif (root/'actuals.json').exists():
        if obj!=json.loads((root/'actuals.json').read_text()) or append!=(root/'ledger_append.csv').read_bytes():
            raise ValueError('Finalized accounting differs from the observed replay')
    print(json.dumps({k:obj[k] for k in ('research_minutes','measured_engaged_minutes','phase_research_minutes',
        'phase_remaining_floor_minutes','research_floor_satisfied','append_rows','cadence_violations')},indent=2))


if __name__=='__main__':main()
