"""Administrative active pointers; no research credit and no old actuals rewrite."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3]
note=('**Active recurrence — October 23, 2026:** '
      '[s15](v3/discovery/s15/session.md) has a fresh four-hour commitment. '
      'PR 16 is verified merged. The prior s14 totals below remain historical.\n\n')
p=ROOT/'TODO_v3.md';s=p.read_bytes().decode('utf-8');a,b=s.split('\n',1)
assert '[s15]' not in s[:500]
p.write_bytes((a+'\n\n'+note+b.lstrip('\r\n')).encode('utf-8'))
p=ROOT/'v3/plan.v1.json';obj=json.loads(p.read_bytes())
obj['active_session']='v3/discovery/s15/session.md'
obj['discovery_program']['current_cycle']['session']='v3/discovery/s15/session.md'
obj['discovery_program']['current_cycle']['clock_active']=True
obj['discovery_program']['current_cycle']['session_status']='active_four_hour_commitment'
obj['discovery_program']['current_cycle']['actuals']='v3/discovery/s15/actuals.json'
p.write_bytes((json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
p=ROOT/'v3/discovery/CONTINUE.md';s=p.read_bytes().decode('utf-8');a,b=s.split('\n',1)
active=('**ACTIVE SESSION: s15**, started October 23, 2026 from verified merged PR 16.\n'
        'Read [s15 scope](s15/session.md), raw actuals and dispositions before\n'
        'resuming its four-hour floor. Do not start a duplicate clock. The s14\n'
        'handoff below is inherited background and its clock remains closed.\n\n')
p.write_bytes((a+'\n\n'+active+b.lstrip('\r\n')).encode('utf-8'))
print('s15 active pointers recorded; prior scientific actuals unchanged.')
