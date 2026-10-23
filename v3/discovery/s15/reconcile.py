"""Reconcile closed s15 observations. Administrative; never starts a clock."""
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
getcontext().prec = 45
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def minutes(n): return str(Decimal(n) / Decimal(60000000000))

raw = read(HERE/'actuals.json')
assert raw['status'] == 'closed' and raw['open_segment'] is None
segments = [json.loads(s) for s in (HERE/'segments.jsonl').read_text().splitlines()]
modes, purposes, lanes = Counter(), Counter(), Counter()
lookup = {}
for s in segments:
    assert s['start']['runtime'] == s['end']['runtime']
    assert s['elapsed_ns'] == s['end']['monotonic_ns'] - s['start']['monotonic_ns'] >= 0
    key = (s['start']['monotonic_ns'], s['end']['monotonic_ns'])
    assert key not in lookup
    lookup[key] = s
    mode, ns = s['effective_mode'], s['elapsed_ns']
    modes[mode] += ns
    if mode in ('D', 'L', 'E'):
        purposes[s['start']['purpose']] += ns
        lanes[s['start']['lane']] += ns
assert dict(modes) == {k:v for k,v in raw['closed_ns'].items() if v}
dispositions = read(HERE/'dispositions.json')
# Explicit O/context intervals are recovery, not engaged administration.
for s in segments:
    if s['effective_mode'] == 'O' and s['start']['purpose'] == 'context':
        dispositions.append(dict(start_monotonic_ns=s['start']['monotonic_ns'],
            end_monotonic_ns=s['end']['monotonic_ns'], elapsed_ns=s['elapsed_ns'],
            raw_mode='O', effective_mode='unmeasured',
            reason='Explicit context/recovery interval; excluded from total engaged time as well as research.'))
seen, corrections = set(), []
for number,d in enumerate(dispositions, 1):
    key = (d['start_monotonic_ns'], d['end_monotonic_ns'])
    assert key not in seen
    seen.add(key)
    s=lookup[key]; ns=d['elapsed_ns']
    assert s['elapsed_ns']==ns and s['effective_mode']==d['raw_mode']
    modes[d['raw_mode']]-=ns; modes[d['effective_mode']]+=ns
    if d['raw_mode'] in ('D','L','E'):
        purposes[s['start']['purpose']]-=ns; lanes[s['start']['lane']]-=ns
    if d['effective_mode'] in ('D','L','E'):
        purposes[d.get('effective_purpose',s['start']['purpose'])]+=ns
        lanes[d.get('effective_lane',s['start']['lane'])]+=ns
    corrections.append(dict(number=number, disposition=d, segment=s))
assert min(modes.values()) >= 0
research = sum(modes[m] for m in ('D','L','E'))
assert sum(purposes.values()) == sum(lanes.values()) == research
target=14400000000000
assert research >= target
prior=read(HERE.parent/'s14/effective_actuals.json')
assert raw['session_config']['prior_program_research_ns']==prior['program_research_ns']
result=dict(contributor='Codex (GPT-6)', status='closed_author_directed_four_hour_handoff',
    clock_active=False, research_closed_utc='2026-10-23T19:11:50.215867+00:00',
    clock_closed_utc=raw['observed']['utc'], research_ns=research,
    session_research_ns=research, session_target_ns=target,
    session_overshoot_ns=research-target, closed_ns=dict(modes),
    purpose_ns=dict(purposes), lane_ns=dict(lanes), segment_count=len(segments),
    runtime=raw['observed']['runtime'], historical_phase_ns=prior['historical_phase_ns'],
    prior_program_research_ns=prior['program_research_ns'],
    prior_phase_research_ns=prior['phase_research_ns'],
    program_research_ns=prior['program_research_ns']+research,
    cycle_research_ns=prior['cycle_research_ns']+research,
    phase_research_ns=prior['phase_research_ns']+research,
    total_engaged_ns=research+modes['O'], publication_research_credit_ns=0,
    applied_dispositions=corrections,
    source_hashes={name:sha(HERE/name) for name in
        ('actuals.json','events.jsonl','segments.jsonl','dispositions.json','session_config.json')},
    note='Sixteen interrupted or mixed research intervals excluded in full; no research reclassification credit; explicit O/context intervals also excluded from total engagement. Recorded O is partial administration, not all publication time. D/L boundaries and purpose allocation are coarse engaged estimates, not processor attribution. No overlapping probe-runtime credit is added.')
for key in ('research','program_research','cycle_research','phase_research','total_engaged'):
    result[key+'_minutes']=minutes(result[key+'_ns'])
result['mode_minutes']={k:minutes(v) for k,v in modes.items()}
result['purpose_percent']={k:str(Decimal(v)*100/Decimal(research)) for k,v in purposes.items()}
result['lane_percent']={k:str(Decimal(v)*100/Decimal(research)) for k,v in lanes.items()}
(HERE/'effective_actuals.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
ledger=ROOT/'v3/time_ledger.csv'
marker='s15 effective disposition correction;'
existing=ledger.read_text(encoding='utf-8')
if marker not in existing:
    with ledger.open('a',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        for c in corrections:
            d,s=c['disposition'],c['segment']
            sec=str(Decimal(d['elapsed_ns'])/Decimal(1000000000))
            writer.writerow(['P3-SEARCH-01','P3-SEARCH-01-C001',
                f"s15-correction-{c['number']}",d['effective_mode'],d.get('effective_lane',''),s['start']['utc'],
                s['end']['utc'],sec,sec if d['effective_mode'] in ('D','L','E','O') else '0',
                '0','0',sec if d['effective_mode']=='unmeasured' else '0','0',
                'v3/discovery/s15/effective_actuals.json',
                marker+' replaces raw matching segment, not additive time; '+d['reason']])
else:
    assert existing.count(marker)==len(corrections)
print(json.dumps({k:result[k] for k in ('research_ns','research_minutes',
    'program_research_ns','program_research_minutes','phase_research_ns',
    'phase_research_minutes','mode_minutes','purpose_percent','lane_percent','segment_count')},indent=2))
