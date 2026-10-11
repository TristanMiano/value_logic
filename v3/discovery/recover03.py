"""Administrative recovery after invalid client mark killed s02 clock.

Codex (GPT-6), 2026-10-11. No research credit for this operation.
"""
import csv
from datetime import datetime, timezone
import json
from pathlib import Path

root = Path('v3/discovery/s02')
raw = json.loads((root/'actuals.json').read_text(encoding='utf-8'))
eff = json.loads((root/'effective_actuals.json').read_text(encoding='utf-8'))
note = {
    'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'interrupted_clock_runtime_dead',
    'last_closed_boundary': raw['open_segment'],
    'last_report_observation': raw['observed'],
    'unclosed_interval_credit_ns': 0,
    'gap_duration': 'unknown; no cross-runtime subtraction',
    'cause': 'Recovery sent mark O with lane X, but nonresearch modes require lane -. Server assertion terminated runtime before writing a boundary.',
    'disposition': 'Preserve raw records. Entire unclosed interval from 23:15:11.008254 UTC and recovery excluded. New session s03 continues same C001 with closed effective actuals only.'
}
assert not (root/'interruption.json').exists()
(root/'interruption.json').write_text(json.dumps(note,indent=2)+'\n',encoding='utf-8')
eff.update(status='interrupted', open_segment=None, interruption='v3/discovery/s02/interruption.json')
(root/'effective_actuals.json').write_text(json.dumps(eff,indent=2)+'\n',encoding='utf-8')
with Path('v3/time_ledger.csv').open('a',encoding='utf-8',newline='') as f:
    csv.writer(f,lineterminator='\n').writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s02','unmeasured','',note['recorded_utc'],note['recorded_utc'],0,0,0,0,0,0,'v3/discovery/s02/interruption.json','Notice only: dead runtime open interval excluded; unknown duration, zero credit.'])
p=Path('v3/plan.v1.json'); plan=json.loads(p.read_text(encoding='utf-8'))
pr=plan['discovery_program']; c=pr['current_cycle']
pr['research_ns']=eff['program_research_ns']; c['research_ns']=eff['cycle_research_ns']
c['remaining_research_floor_ns']=eff['remaining_floor_ns']; c['clock_active']=False
c['session_status']='interrupted_clock_runtime_dead'
p.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'cycle_research_ns':eff['cycle_research_ns'],'remaining_floor_ns':eff['remaining_floor_ns']}))
