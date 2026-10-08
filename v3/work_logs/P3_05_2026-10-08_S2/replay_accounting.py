"""Replay observed, same-runtime segments. No prior lost-session time is inferred."""
from pathlib import Path
from decimal import Decimal, localcontext
import csv,io,json,hashlib,sys
NS=10**9
MIN=60*NS
FIELDS='task_id,attempt_id,session_id,mode,lane,start_utc,end_utc,elapsed_seconds,engaged_seconds,tool_wait_seconds,idle_seconds,unmeasured_seconds,forecast_seconds,artifact,status'.split(',')

def amount(n,d):
    with localcontext() as c:
        c.prec=40
        return format(Decimal(n)/Decimal(d),'.12f' if d==MIN else '.9f')

def replay(root):
    root=Path(root)
    clocks=[json.loads(x) for x in (root/'clocks.jsonl').read_text().splitlines()]
    disp={x['segment_index']:x for x in json.loads((root/'clock_dispositions.json').read_text())}
    base=json.loads((root/'accounting_base.json').read_text())
    assert clocks[-1]['mode']=='STOP'
    totals={};lanes={};segments=[];violations=[];rows=[]
    for i,(a,b) in enumerate(zip(clocks,clocks[1:])):
        assert a['runtime']==b['runtime']
        assert type(a['monotonic_ns']) is int and type(b['monotonic_ns']) is int
        ns=b['monotonic_ns']-a['monotonic_ns'];assert ns>=0
        mode=disp.get(i,{}).get('effective_mode',a['mode']);lane=disp.get(i,{}).get('effective_lane',a['lane'])
        if ns>900*NS:
            violations.append(i);mode='unmeasured';lane=''
        engaged=ns if mode in ('D','L','E','O') else 0
        totals[mode]=totals.get(mode,0)+ns
        if mode in ('D','L','E'):lanes[lane]=lanes.get(lane,0)+ns
        note=disp.get(i,{}).get('reason',a['note'])
        rows.append(dict(zip(FIELDS,['P3-05','P3-05-R1','2026-10-08-S2',mode,lane,a['utc'],b['utc'],amount(ns,NS),amount(engaged,NS),
                      amount(ns if mode=='wait' else 0,NS),amount(ns if mode=='idle' else 0,NS),
                      amount(ns if mode not in ('D','L','E','O','wait','idle') else 0,NS),'0',
                      'v3/work_logs/P3_05_2026-10-08_S2.md','IN PROGRESS; '+note])))
        segments.append({'index':i,'mode':mode,'lane':lane,'ns':ns,'start_utc':a['utc'],'end_utc':b['utc']})
    research=sum(totals.get(k,0) for k in ('D','L','E'));engaged=research+totals.get('O',0)
    buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=FIELDS,lineterminator='\n');w.writerows(rows);append=buf.getvalue().encode()
    result=dict(schema='value_logic.p305.actuals.v1',base_commit=base['base_commit'],clock_stopped=True,
                task='P3-05',attempt='P3-05-R1',session='2026-10-08-S2',research_ns=research,research_minutes=amount(research,MIN),
                task_research_ns=research,prior_attempt_research='UNVERIFIED_MISSING_CLOCKS',historical_recredit_ns=0,
                task_remaining_floor_ns=max(0,base['task_floor_ns']-research),
                task_remaining_floor_minutes=amount(max(0,base['task_floor_ns']-research),MIN),
                research_floor_satisfied=research>=base['task_floor_ns'],
                total_engaged_ns=engaged,total_engaged_minutes=amount(engaged,MIN),
                phase_research_ns=base['phase_research_ns']+research,phase_research_minutes=amount(base['phase_research_ns']+research,MIN),
                phase_measured_engaged_ns=base['phase_measured_engaged_ns']+engaged,
                phase_remaining_floor_ns=base['phase_floor_ns']-base['phase_research_ns']-research,
                phase_remaining_floor_minutes=amount(base['phase_floor_ns']-base['phase_research_ns']-research,MIN),
                category_ns=totals,category_minutes={k:amount(v,MIN) for k,v in totals.items()},lane_research_ns=lanes,
                cadence_violations=violations,segments=segments,append_rows=len(rows),append_bytes=len(append),
                append_sha256=hashlib.sha256(append).hexdigest(),posting='PREPARED_NOT_POSTED',publication='NOT_PUBLISHED',
                task_status='IN_PROGRESS',post_cutoff_administration_credit_ns=0)
    return result,append

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    result,append=replay(root)
    if '--write' in sys.argv:
        for name,data in [('actuals.json',(json.dumps(result,indent=2)+'\n').encode()),('ledger_append.csv',append)]:
            with (root/name).open('xb') as f:f.write(data)
    else:
        assert result==json.loads((root/'actuals.json').read_text())
        assert append==(root/'ledger_append.csv').read_bytes()
    print(json.dumps({k:v for k,v in result.items() if k in ['research_minutes','task_remaining_floor_minutes','phase_research_minutes','phase_remaining_floor_minutes','category_minutes','append_rows','cadence_violations']},indent=2))
