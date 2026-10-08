#!/usr/bin/env python3
"""Replay exact observed S3 clocks and exclusions without recrediting prior work."""
from __future__ import annotations
from pathlib import Path
from decimal import Decimal,localcontext
import csv,io,json,hashlib,sys
NS=10**9; MIN=60*NS
FIELDS='task_id,attempt_id,session_id,mode,lane,start_utc,end_utc,elapsed_seconds,engaged_seconds,tool_wait_seconds,idle_seconds,unmeasured_seconds,forecast_seconds,artifact,status'.split(',')

def amount(n,d):
    with localcontext() as c:
        c.prec=40
        return format(Decimal(n)/Decimal(d),'.12f' if d==MIN else '.9f')

def replay(root):
    root=Path(root)
    clocks=[json.loads(x) for x in (root/'clocks.jsonl').read_text().splitlines()]
    exclusions=json.loads((root/'clock_dispositions.json').read_text())['dispositions']
    base=json.loads((root/'accounting_base.json').read_text())
    assert clocks[-1]['mode']=='stop'
    assert len({x['runtime'] for x in clocks})==1
    utc={x['monotonic_ns']:x['utc'] for x in clocks}
    assert len(utc)==len(clocks)
    for x in exclusions:
        assert x['runtime']==clocks[0]['runtime']
        assert x['start_monotonic_ns'] in utc and x['end_monotonic_ns'] in utc
        assert x['start_monotonic_ns']<x['end_monotonic_ns']
    totals={};lanes={};segments=[];rows=[];violations=[]
    for i,(a,b) in enumerate(zip(clocks,clocks[1:])):
        lo,hi=a['monotonic_ns'],b['monotonic_ns'];assert type(lo)is int and type(hi)is int and lo<hi
        cuts={lo,hi}
        for x in exclusions:
            cuts.update(t for t in [x['start_monotonic_ns'],x['end_monotonic_ns']] if lo<t<hi)
        boundaries=sorted(cuts)
        for left,right in zip(boundaries,boundaries[1:]):
            matched=[x for x in exclusions if x['start_monotonic_ns']<=left and right<=x['end_monotonic_ns']]
            assert len(matched)<=1
            mode=matched[0]['effective_mode'] if matched else a['mode']
            lane=a['lane'] if mode in ('D','L','E') else ''
            note=matched[0]['reason'] if matched else a['note'];ns=right-left
            if mode in ('D','L','E','O') and ns>900*NS:
                violations.append({'raw_segment':i,'ns':ns});mode='unmeasured';lane=''
            assert mode in ('D','L','E','O','wait','recovery','unmeasured','idle')
            assert mode not in ('D','L','E') or lane in ('R','X')
            totals[mode]=totals.get(mode,0)+ns
            if mode in ('D','L','E'):lanes[lane]=lanes.get(lane,0)+ns
            engaged=ns if mode in ('D','L','E','O') else 0
            segment={'raw_segment':i,'mode':mode,'lane':lane,'start_monotonic_ns':left,'end_monotonic_ns':right,'start_utc':utc[left],'end_utc':utc[right],'ns':ns,'exclusion_id':matched[0]['id'] if matched else None}
            segments.append(segment)
            row=['P3-05','P3-05-R1','2026-10-08-S3',mode,lane,utc[left],utc[right],amount(ns,NS),amount(engaged,NS),amount(ns if mode=='wait' else 0,NS),amount(ns if mode=='idle' else 0,NS),amount(ns if mode in ('unmeasured','recovery') else 0,NS),'0','v3/work_logs/P3_05_2026-10-08_S3.md','Closed S3 observation; scientific completion recorded separately; '+note]
            rows.append(dict(zip(FIELDS,row)))
    research=sum(totals.get(k,0) for k in ('D','L','E'));engaged=research+totals.get('O',0)
    task=base['prior_verifiable_task_research_ns']+research;remaining=max(0,base['task_floor_ns']-task)
    buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=FIELDS,lineterminator='\n');w.writerows(rows);append=buf.getvalue().encode()
    result={'schema':'value_logic.p305.s3.actuals.v1','base_commit':base['base_commit'],'clock_stopped':True,'task':'P3-05','attempt':'P3-05-R1','session':'2026-10-08-S3','research_ns':research,'research_minutes':amount(research,MIN),'prior_verified_task_research_ns':base['prior_verifiable_task_research_ns'],'task_research_ns':task,'task_research_minutes':amount(task,MIN),'prior_attempt_research':'UNVERIFIED_MISSING_CLOCKS','historical_recredit_ns':0,'task_remaining_floor_ns':remaining,'task_remaining_floor_minutes':amount(remaining,MIN),'research_floor_satisfied':task>=base['task_floor_ns'],'task_floor_margin_ns':task-base['task_floor_ns'],'total_engaged_ns':engaged,'total_engaged_minutes':amount(engaged,MIN),'phase_research_ns':base['phase_research_ns']+research,'phase_research_minutes':amount(base['phase_research_ns']+research,MIN),'phase_measured_engaged_ns':base['phase_measured_engaged_ns']+engaged,'phase_remaining_floor_ns':base['phase_floor_ns']-base['phase_research_ns']-research,'phase_remaining_floor_minutes':amount(base['phase_floor_ns']-base['phase_research_ns']-research,MIN),'category_ns':totals,'category_minutes':{k:amount(v,MIN) for k,v in totals.items()},'lane_research_ns':lanes,'lane_research_minutes':{k:amount(v,MIN) for k,v in lanes.items()},'cadence_violations':violations,'segments':segments,'append_rows':len(rows),'append_bytes':len(append),'append_sha256':hashlib.sha256(append).hexdigest(),'posting':'PREPARED_NOT_POSTED','publication':'NOT_PUBLISHED','task_status':'COMPLETE' if not remaining else 'IN_PROGRESS','completion_scope':'finite_counterfactual_transport_and_checked_reuse','post_cutoff_administration_credit_ns':0}
    return result,append

if __name__=='__main__':
    root=Path(__file__).resolve().parent;result,append=replay(root)
    if '--write' in sys.argv:
        for name,data in [('actuals.json',(json.dumps(result,indent=2)+'\n').encode()),('ledger_append.csv',append)]:
            with (root/name).open('xb') as f:f.write(data)
    else:
        assert result==json.loads((root/'actuals.json').read_text())
        assert append==(root/'ledger_append.csv').read_bytes()
    print(json.dumps({k:result[k] for k in ['research_minutes','task_research_minutes','phase_research_minutes','phase_remaining_floor_minutes','category_minutes','append_rows','cadence_violations']},indent=2))
