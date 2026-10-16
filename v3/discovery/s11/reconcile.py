"""Reconcile s11's two runtimes, preserving the dead runtime. Zero research credit."""
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path
import csv
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
getcontext().prec=45
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def minutes(ns): return str(Decimal(ns)/Decimal(60000000000))

recovery=read(HERE/'clock_recovery.json')
assert sha(HERE/'actuals.json')==recovery['old_actuals_sha256']
modes=Counter(); purposes=Counter(); lanes=Counter(); parts=[]; corrections=[]
hashes={}; total_segments=0
for directory in (HERE,HERE/'c2'):
    part=directory.relative_to(HERE).as_posix()
    raw=read(directory/'actuals.json')
    if directory==HERE:
        assert raw['status']=='active' and raw['open_segment']==recovery['old_open_segment']
    else:
        assert raw['status']=='closed' and raw['open_segment'] is None
    local=Counter(); lp=Counter(); ll=Counter(); lookup={}
    segments=[json.loads(line) for line in (directory/'segments.jsonl').read_text().splitlines()]
    for s in segments:
        assert s['start']['runtime']==s['end']['runtime']
        assert s['elapsed_ns']==s['end']['monotonic_ns']-s['start']['monotonic_ns']>=0
        key=(s['start']['monotonic_ns'],s['end']['monotonic_ns'])
        assert key not in lookup
        lookup[key]=s
        mode=s['effective_mode'];ns=s['elapsed_ns'];local[mode]+=ns
        if mode in ('D','L','E'):
            lp[s['start']['purpose']]+=ns;ll[s['start']['lane']]+=ns
    assert dict(local)=={k:v for k,v in raw['closed_ns'].items() if v}
    seen=set()
    for j,d in enumerate(read(directory/'dispositions.json')['entries'],1):
        key=(d['start_monotonic_ns'],d['end_monotonic_ns'])
        assert key not in seen;seen.add(key)
        s=lookup[key];ns=d['elapsed_ns']
        assert s['elapsed_ns']==ns and s['effective_mode']==d['raw_mode']
        local[d['raw_mode']]-=ns;local[d['effective_mode']]+=ns
        if d['raw_mode'] in ('D','L','E'):
            assert d['effective_mode'] not in ('D','L','E')
            lp[s['start']['purpose']]-=ns;ll[s['start']['lane']]-=ns
        corrections.append(dict(part=part,number=j,disposition=d,segment=s))
    assert min(local.values())>=0
    research=sum(local[k] for k in ('D','L','E'))
    if directory==HERE: assert research==recovery['old_effective_closed_research_ns']
    parts.append(dict(directory=part,runtime=segments[0]['start']['runtime'],
        raw_status=raw['status'],closed_segments=len(segments),research_ns=research,
        closed_ns=dict(local),unclosed_segment_credit_ns=0))
    modes.update(local);purposes.update(lp);lanes.update(ll);total_segments+=len(segments)
    for name in ('actuals.json','events.jsonl','segments.jsonl','dispositions.json','session_config.json'):
        path=directory/name;hashes[path.relative_to(HERE).as_posix()]=sha(path)
prior=read(HERE.parent/'s10/effective_actuals.json')
research=sum(modes[k] for k in ('D','L','E'));target=14400000000000
assert research>=target
result=dict(contributor='Codex (GPT-6)',status='closed_author_directed_four_hour_handoff',
    clock_active=False,research_closed_utc='2026-10-16T04:31:32.823678+00:00',
    clock_closed_utc='2026-10-16T04:31:33.129541+00:00',
    research_ns=research,session_research_ns=research,session_target_ns=target,
    session_overshoot_ns=research-target,closed_ns=dict(modes),purpose_ns=dict(purposes),
    lane_ns=dict(lanes),parts=parts,segment_count=total_segments,
    historical_phase_ns=prior['historical_phase_ns'],
    prior_program_research_ns=prior['program_research_ns'],
    prior_phase_research_ns=prior['phase_research_ns'],
    program_research_ns=prior['program_research_ns']+research,
    cycle_research_ns=prior['cycle_research_ns']+research,
    phase_research_ns=prior['phase_research_ns']+research,
    total_engaged_ns=research+modes['O'],publication_research_credit_ns=0,
    applied_dispositions=corrections,source_hashes=hashes,
    dead_runtime_open_segment=recovery['old_open_segment'],
    dead_runtime_open_duration='unmeasured; no matched end in original runtime',
    dead_runtime_open_research_credit_ns=0,
    note='Sum closed matched intervals within each runtime only. Six complete context intervals excluded; sixth refresh in the dead unclosed segment has zero credit and unknown duration. No cross-runtime subtraction. Recorded O is partial administration, not all publication time.')
for key in ('research','program_research','cycle_research','phase_research','total_engaged'):
    result[key+'_minutes']=minutes(result[key+'_ns'])
result['mode_minutes']={k:minutes(v) for k,v in modes.items()}
result['purpose_percent']={k:str(Decimal(v)*100/Decimal(research)) for k,v in purposes.items()}
(HERE/'effective_actuals.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
ledger=ROOT/'v3/time_ledger.csv';marker='s11 effective disposition correction;'
if marker not in ledger.read_text(encoding='utf-8'):
    with ledger.open('a',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        for c in corrections:
            d=c['disposition'];s=c['segment'];sec=str(Decimal(d['elapsed_ns'])/Decimal(1000000000))
            writer.writerow(['P3-SEARCH-01','P3-SEARCH-01-C001',
                f"s11-{c['part']}-correction-{c['number']}",d['effective_mode'],'',
                s['start']['utc'],s['end']['utc'],sec,'0','0','0',sec,'0',
                'v3/discovery/s11/effective_actuals.json',
                marker+' replaces raw matching segment, not additive time; '+d['reason']])
print(json.dumps({k:result[k] for k in ('research_ns','research_minutes','program_research_ns',
    'program_research_minutes','phase_research_ns','phase_research_minutes','closed_ns',
    'purpose_percent','segment_count')},indent=2))
