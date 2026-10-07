"""P3-03 exact accounting and preservation; ChatGPT (GPT-6 Astra Pro), 2026-10-07.

preview is read-only; finalize appends once after the principal clock stops;
verify is read-only after finalization. This script verifies the task floor but does not infer scientific validity from time.
"""
from __future__ import annotations
import csv
from decimal import Decimal, localcontext
import fcntl
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
TASK, ATTEMPT, SESSION = 'P3-03', 'P3-03-1', '2026-10-07-S1'
LOG = 'v3/work_logs/P3_03_2026-10-07_S1.md'
ENGAGED, RESEARCH = {'D','L','E','O'}, {'D','L','E'}
MINUTE, SECOND = 60_000_000_000, 1_000_000_000
FIELDS = 'task_id,attempt_id,session_id,mode,lane,start_utc,end_utc,elapsed_seconds,engaged_seconds,tool_wait_seconds,idle_seconds,unmeasured_seconds,forecast_seconds,artifact,status'.split(',')
spec = importlib.util.spec_from_file_location('p303_clock', HERE/'clock.py')
clock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clock)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text())

def dump(value):
    return json.dumps(value,indent=2,sort_keys=True)+'\n'

def minutes(n):
    with localcontext() as c:
        c.prec=40
        return format(Decimal(n)/Decimal(MINUTE), '.12f')

def seconds(n):
    return f'{n//SECOND}.{n%SECOND:09d}'

def inputs():
    names=['baseline.json','forecast.json','attempt_started.json','environment.json','clock.py',
           'close_task.py','clocks.jsonl','segments.jsonl','clock_state.json']
    if (HERE/'clock_dispositions.jsonl').exists():names.append('clock_dispositions.jsonl')
    return {name:digest((HERE/name).read_bytes()) for name in names}

def audit():
    base=read_json(HERE/'baseline.json'); forecast=read_json(HERE/'forecast.json')
    events=clock.read_records(HERE/'clocks.jsonl')
    raw=clock.read_records(HERE/'segments.jsonl'); parts=clock.effective_segments()
    state=read_json(HERE/'clock_state.json')
    assert events and events[0]['command']=='start'
    assert all(e['runtime']==clock.RUNTIME for e in events)
    assert all(a['monotonic_ns']<b['monotonic_ns'] for a,b in zip(events,events[1:]))
    event_points={e['monotonic_ns']:e['utc'] for e in events}
    for i,s in enumerate(raw):
        assert s['runtime']==clock.RUNTIME and s['elapsed_ns']>0
        assert event_points[s['start_monotonic_ns']]==s['start_utc']
        assert event_points[s['end_monotonic_ns']]==s['end_utc']
        if i:assert raw[i-1]['end_monotonic_ns']==s['start_monotonic_ns'], 'Unaccounted stopped gap'
    totals={m:0 for m in ['D','L','E','O','wait','idle','unmeasured','recovery']};lanes={'R':0,'X':0}
    for s in parts:
        assert s['mode'] in totals
        assert s['lane'] in ('R','X') if s['mode'] in RESEARCH else s['lane']==''
        totals[s['mode']]+=s['elapsed_ns']
        if s['mode'] in RESEARCH:lanes[s['lane']]+=s['elapsed_ns']
    windows=[]
    for a,b in zip(events,events[1:]):
        n=sum(max(0,min(b['monotonic_ns'],s['end_monotonic_ns'])-max(a['monotonic_ns'],s['start_monotonic_ns'])) for s in parts if s['mode'] in ENGAGED)
        windows.append(n)
    assert max(windows,default=0)<=15*MINUTE, 'Engaged observation cadence exceeded'
    for name,wanted in base['protected_files'].items():
        data=(REPO/name).read_bytes()
        assert len(data)==wanted['bytes'] and digest(data)==wanted['sha256'],name
    changed=set(subprocess.check_output(['git','diff','--name-only',base['source_tree']],cwd=REPO,text=True).splitlines())
    changed.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines())
    allowed={'TODO_v3.md','README.md','v3/README.md','v3/claim_ledger.md','v3/plan.v1.json',
             'v3/time_ledger.csv',LOG,'v3/STYLE.md','.github/workflows/math-markdown.yml',
             'v3/checks/math_markdown.py','v3/derivations/03_logical_uncertainty.md',
             'v3/derivations/03_refinement_extensions.md','v3/literature/03_bounded_sources.md'}
    allowed.update(base['prior_markdown_files'])
    allowed.update(base['preexisting_untracked'])
    assert all(n in allowed or n.startswith('v3/work_logs/P3_03_2026-10-07_S1/')
               or n.startswith('v3/checks/03_') for n in changed), sorted(changed-allowed)
    for name,wanted in base['preexisting_untracked'].items():
        data=(REPO/name).read_bytes()
        assert len(data)==wanted['bytes'] and digest(data)==wanted['sha256'], name
    ledger=(REPO/'v3/time_ledger.csv').read_bytes();prefix=ledger[:base['prior_ledger_bytes']]
    assert len(prefix)==base['prior_ledger_bytes'] and digest(prefix)==base['prior_ledger_sha256']
    assert prefix.endswith(b'\n')
    old=list(csv.DictReader(io.StringIO(prefix.decode())))
    assert list(old[0])==FIELDS and not any(r['attempt_id']==ATTEMPT for r in old)
    prior_research=sum(int(Decimal(r['engaged_seconds'])*SECOND) for r in old if r['mode'] in RESEARCH)
    prior_engaged=sum(int(Decimal(r['engaged_seconds'])*SECOND) for r in old if r['mode'] in ENGAGED)
    assert prior_research==base['prior_phase3_research_ns'] and prior_engaged==base['prior_phase3_engaged_ns']
    buf=io.StringIO(newline='');writer=csv.DictWriter(buf,fieldnames=FIELDS,lineterminator='\n');seen=set()
    for s in parts:
        mode=s['mode'];n=s['elapsed_ns'];central=forecast['central_minutes']
        fc=central.get('expected_waits' if mode=='wait' else mode,0)*60 if mode not in seen else 0
        seen.add(mode)
        writer.writerow(dict(task_id=TASK,attempt_id=ATTEMPT,session_id=SESSION,mode=mode,lane=s['lane'],
            start_utc=s['start_utc'],end_utc=s['end_utc'],elapsed_seconds=seconds(n),
            engaged_seconds=seconds(n if mode in ENGAGED else 0),tool_wait_seconds=seconds(n if mode=='wait' else 0),
            idle_seconds=seconds(n if mode=='idle' else 0),unmeasured_seconds=seconds(n if mode in {'unmeasured','recovery'} else 0),
            forecast_seconds=str(fc),artifact=LOG,status='complete' if mode in ENGAGED else 'excluded'))
    suffix=buf.getvalue().encode()
    assert ledger in (prefix,prefix+suffix), 'Ledger is neither source prefix nor the exact current append'
    research=sum(totals[m] for m in RESEARCH);engaged=sum(totals[m] for m in ENGAGED)
    prior_gate=read_json(REPO/'v3/work_logs/P3_A_2026-10-07_S1/actuals.json')
    cycle={k:prior_gate['cycle_I_observed_lane_ns'][k]+lanes[k] for k in lanes}
    total_cycle=sum(cycle.values())
    payload=dict(schema='value_logic.P3-03.actuals.v1',task=TASK,attempt=ATTEMPT,session=SESSION,
        contributor='ChatGPT (GPT-6 Astra Pro)',source_commit=base['source_commit'],source_tree=base['source_tree'],
        runtime=clock.RUNTIME,first_observation_utc=events[0]['utc'],last_observation_utc=events[-1]['utc'],
        clock_stopped=state is None,category_ns=totals,category_minutes={k:minutes(v) for k,v in totals.items()},
        research_ns=research,research_minutes=minutes(research),engaged_ns=engaged,engaged_minutes=minutes(engaged),
        excluded_ns=sum(v for k,v in totals.items() if k not in ENGAGED),lane_research_ns=lanes,
        lane_fraction={k:str(Decimal(v)/Decimal(research)) if research else None for k,v in lanes.items()},
        observed_cycles_I_and_II_lane_ns=cycle,observed_cycles_at_least_25_percent_each=all(4*v>=total_cycle for v in cycle.values()),
        cycle_scope='Completed Cycle I plus the observed P3-03 part of Cycle II; no completed two-cycle compliance is inferred.',
        protected_research_floor_ns=90*MINUTE,protected_floor_met=research>=90*MINUTE,
        remaining_task_research_ns=max(0,90*MINUTE-research),scientific_status_inferred_from_time=False,
        phase3_research_ns=prior_research+research,phase3_research_minutes=minutes(prior_research+research),
        phase3_engaged_ns=prior_engaged+engaged,phase3_engaged_minutes=minutes(prior_engaged+engaged),
        remaining_phase3_research_ns=max(0,960*MINUTE-prior_research-research),
        remaining_phase3_research_minutes=minutes(max(0,960*MINUTE-prior_research-research)),
        first_240_minute_checkpoint_reached=prior_research+research>=240*MINUTE,
        first_240_minute_checkpoint_overshoot_ns=max(0,prior_research+research-240*MINUTE),
        forecast_research_delta_ns={name:research-forecast[name+'_research_minutes']*MINUTE for name in ('central','high')},
        publication_after_cutoff_time_credit_ns=0,
        maximum_engaged_between_observations_ns=max(windows,default=0),cadence_violations=[],
        extra_agent_time_credited_ns=0,open_time_credited_ns=0,post_stop_administration_credited_ns=0,
        raw_segment_count=len(raw),effective_segment_count=len(parts),effective_segments=parts,
        disposition_count=len(clock.read_records(HERE/'clock_dispositions.jsonl')),
        forecast=forecast,input_sha256=inputs(),prior_ledger_bytes=len(prefix),prior_ledger_sha256=digest(prefix),
        prior_ledger_rows=len(old),append_bytes=len(suffix),append_sha256=digest(suffix),appended_rows=len(parts),
        final_ledger_bytes=len(prefix+suffix),final_ledger_sha256=digest(prefix+suffix),
        protected_files_checked=len(base['protected_files']),preservation_pass=True,
        ledger_relation='source_prefix_only' if ledger==prefix else 'exact_append')
    return payload,prefix,suffix

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'preview'
    assert mode in ('preview','finalize','verify')
    a,prefix,suffix=audit()
    if mode=='finalize':
        assert a['clock_stopped'] and a['protected_floor_met'] and a['ledger_relation']=='source_prefix_only'
        assert not any((HERE/n).exists() for n in ['actuals.json','ledger_append.csv','finalize.lock','finalization'])
        lock=HERE/'finalize.lock'
        with lock.open('x') as f:f.write('P3-03 one-time finalization\n')
        stage=HERE/'finalization';stage.mkdir()
        (stage/'prepared.json').write_text(dump(a))
        with (HERE/'ledger_append.csv').open('xb') as f:f.write(suffix)
        path=REPO/'v3/time_ledger.csv'
        with path.open('r+b') as f:
            fcntl.flock(f,fcntl.LOCK_EX)
            assert f.read()==prefix and inputs()==a['input_sha256']
            f.seek(0,os.SEEK_END);assert f.write(suffix)==len(suffix);f.flush();os.fsync(f.fileno())
        a.update(finalized=True,ledger_relation='exact_append',finalized_utc=datetime.now(timezone.utc).isoformat())
        with (HERE/'actuals.json').open('x') as f:f.write(dump(a))
        (stage/'result.json').write_text(dump({'status':'finalized','actuals_sha256':digest((HERE/'actuals.json').read_bytes())}))
        lock.unlink()
    elif mode=='verify':
        saved=read_json(HERE/'actuals.json');assert saved['finalized'] is True
        assert a['clock_stopped'] and a['ledger_relation']=='exact_append'
        assert not (HERE/'finalize.lock').exists()
        assert all(saved[k]==v for k,v in a.items()), 'Actuals differ from current exact replay'
        assert (HERE/'ledger_append.csv').read_bytes()==suffix
        result=read_json(HERE/'finalization/result.json')
        assert result['status']=='finalized' and result['actuals_sha256']==digest((HERE/'actuals.json').read_bytes())
    keys=['research_ns','research_minutes','engaged_ns','engaged_minutes','category_minutes','lane_research_ns',
          'observed_cycles_at_least_25_percent_each','phase3_research_minutes','phase3_engaged_minutes','remaining_phase3_research_minutes',
          'maximum_engaged_between_observations_ns','protected_files_checked','ledger_relation','clock_stopped','appended_rows']
    print(dump(dict(status='PASS',mode=mode,**{k:a[k] for k in keys})))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
