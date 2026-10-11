"""Administrative effective-clock view; leaves raw observations untouched.

Codex (GPT-6), 2026-10-11. Safe to rerun after new closed observations.
Ledger correction notices are separate publication actions, not added here.
"""
from decimal import Decimal
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
raw = json.loads((root/'actuals.json').read_text())
segments = [json.loads(line) for line in (root/'segments.jsonl').read_text().splitlines()]
path = root/'dispositions.jsonl'
dispositions = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
overrides = {(d['segment_start_monotonic_ns'],d['segment_end_monotonic_ns']):d for d in dispositions}
totals = dict.fromkeys(raw['closed_ns'],0)
purposes, lanes, applied = {}, {}, []
for s in segments:
    assert s['start']['runtime'] == s['end']['runtime'] == raw['observed']['runtime']
    assert s['elapsed_ns'] == s['end']['monotonic_ns']-s['start']['monotonic_ns']
    mode, purpose, lane = s['effective_mode'],s['start']['purpose'],s['start']['lane']
    key = s['start']['monotonic_ns'],s['end']['monotonic_ns']
    if key in overrides:
        d = overrides[key]
        assert mode == d['original_mode'] and s['elapsed_ns'] == d['elapsed_ns']
        mode, purpose, lane = d['effective_mode'],d.get('purpose',purpose),d.get('lane',lane)
        applied.append(d)
    totals[mode] += s['elapsed_ns']
    if mode in ('D','L','E'):
        purposes[purpose] = purposes.get(purpose,0)+s['elapsed_ns']
        lanes[lane] = lanes.get(lane,0)+s['elapsed_ns']
assert len(applied) == len(overrides)
assert sum(totals.values()) == sum(raw['closed_ns'].values())
research = sum(totals[m] for m in ('D','L','E'))
config = raw['session_config']
cycle = config['prior_cycle_research_ns']+research
program = config['prior_program_research_ns']+research
effective = dict(raw,closed_ns=totals,research_ns=research,session_research_ns=research,
                 cycle_research_ns=cycle,program_research_ns=program,
                 research_minutes=research/60e9,total_engaged_ns=research+totals['O'],
                 purpose_ns=purposes,lane_ns=lanes,
                 remaining_floor_ns=max(0,config['cycle_floor_ns']-cycle),
                 phase_research_ns=raw['historical_phase_ns']+program,
                 applied_dispositions=applied,raw_actuals=(root/'actuals.json').as_posix(),
                 note='Closed observed intervals only; no credit for open interval. Explicit dispositions override raw modes without modifying raw files.')
for field in ('research','cycle_research','program_research','remaining_floor','phase_research'):
    effective['exact_'+field+'_minutes'] = str(Decimal(effective[field+'_ns'])/Decimal(60_000_000_000))
(root/'effective_actuals.json').write_text(json.dumps(effective,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:effective[k] for k in ('status','exact_research_minutes','exact_cycle_research_minutes','exact_remaining_floor_minutes')}))
