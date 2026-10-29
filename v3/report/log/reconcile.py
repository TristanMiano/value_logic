"""Additive P3-12 clock reconciliation. Does not alter original observations."""
from pathlib import Path
from collections import Counter
from decimal import Decimal
import csv,hashlib,io,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
raw=read(HERE/'actuals.json')
assert raw['status']=='closed' and raw['open_segment'] is None
segments=[json.loads(x) for x in (HERE/'segments.jsonl').read_text(encoding='utf-8').splitlines()]
dispositions=read(HERE/'dispositions.json')
bykey={(d['start_monotonic_ns'],d['end_monotonic_ns']):d for d in dispositions}
rawmodes=Counter();modes=Counter();matched=[]
for s in segments:
    start,end=s['start'],s['end'];n=s['elapsed_ns']
    assert start['runtime']==end['runtime']==raw['observed']['runtime']
    assert end['monotonic_ns']-start['monotonic_ns']==n
    mode=s['effective_mode'];rawmodes[mode]+=n
    d=bykey.get((start['monotonic_ns'],end['monotonic_ns']))
    if d:
        assert n==d['elapsed_ns'] and mode==d['raw_mode'];matched.append((d,s));mode=d['effective_mode']
    modes[mode]+=n
assert len(matched)==len(dispositions)
assert dict(rawmodes)=={k:v for k,v in raw['closed_ns'].items() if v}
research=sum(modes[k] for k in ('D','L','E'))
def minutes(n):return str(Decimal(n)/Decimal(60000000000))
result={'status':'CLOSED','task':'P3-12','contributor':'Codex (GPT-6)','research_ns':research,'research_minutes':minutes(research),'closed_ns':dict(modes),'runtime':raw['observed']['runtime'],'segment_count':len(segments),'closed_utc':raw['observed']['utc'],'discovery_research_credit_ns':0,'program_research_ns':raw['session_config']['prior_program_research_ns'],'phase_research_ns':raw['session_config']['prior_phase_research_ns']+research,'dispositions':dispositions,'note':'No floor. Compaction crossing excluded in full. Metadata checks, ordinary prose/build work, executed reconstruction, compilation and visual QA received no research credit. No machine runtime added. Later publication remains uncredited.'}
result['phase_research_minutes']=minutes(result['phase_research_ns'])
(HERE/'effective_actuals.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
ledger=ROOT/'v3/time_ledger.csv';existing=ledger.read_bytes();marker='P3-12 additive reconciliation;';rows=[]
for i,(d,s) in enumerate(matched,1):
    for mode,sign in [(d['raw_mode'],-1),(d['effective_mode'],1)]:
        sec=str(Decimal(sign*s['elapsed_ns'])/1000000000)
        rows.append(['P3-12','P3-12-S1',f'P3-12-exclude-{i}',mode,'R' if mode in ('D','L','E') else '',s['start']['utc'],s['end']['utc'],sec,sec if mode in ('D','L','E','O') else '0','0','0',sec if mode=='unmeasured' else '0','0','v3/report/log/effective_actuals.json',marker+d['reason']])
if marker.encode() not in existing:
    buf=io.StringIO(newline='');csv.writer(buf,lineterminator='\n').writerows(rows)
    with ledger.open('ab') as f:f.write(buf.getvalue().encode())
    (HERE/'ledger_append.json').write_bytes((json.dumps({'prefix_bytes':len(existing),'prefix_sha256':hashlib.sha256(existing).hexdigest(),'append_rows':len(rows)},indent=2)+'\n').encode())
else:
    record=read(HERE/'ledger_append.json');assert existing.count(marker.encode())==len(rows)
    assert hashlib.sha256(existing[:record['prefix_bytes']]).hexdigest()==record['prefix_sha256']
print(json.dumps({k:result[k] for k in ['research_ns','research_minutes','phase_research_minutes','program_research_ns']}))
