"""Exact closed-clock reconciliation. Administration, zero new research credit."""
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path
import copy,csv,hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];getcontext().prec=45
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
raw=read(HERE/'actuals.json');assert raw['status']=='closed' and raw['open_segment'] is None
segments=[json.loads(l) for l in (HERE/'segments.jsonl').read_text().splitlines()]
modes=Counter();lanes=Counter();purposes=Counter();lookup={}
for s in segments:
    assert s['start']['runtime']==s['end']['runtime']
    assert s['elapsed_ns']==s['end']['monotonic_ns']-s['start']['monotonic_ns']
    key=(s['start']['monotonic_ns'],s['end']['monotonic_ns']);assert key not in lookup;lookup[key]=s
    mode=s['effective_mode'];ns=s['elapsed_ns'];modes[mode]+=ns
    if mode in('D','L','E'):lanes[s['start']['lane']]+=ns;purposes[s['start']['purpose']]+=ns
assert dict(modes)=={k:v for k,v in raw['closed_ns'].items() if v}
entries=read(HERE/'dispositions.json')['entries'];seen=set()
for d in entries:
    key=(d['start_monotonic_ns'],d['end_monotonic_ns']);assert key not in seen;seen.add(key)
    s=lookup[key];assert s['elapsed_ns']==d['elapsed_ns'] and s['effective_mode']==d['raw_mode']
    ns=d['elapsed_ns'];modes[d['raw_mode']]-=ns;modes[d['effective_mode']]+=ns
    if d['raw_mode'] in ('D','L','E') and d['effective_mode'] not in ('D','L','E'):
        lanes[s['start']['lane']]-=ns;purposes[s['start']['purpose']]-=ns
research=sum(modes[k] for k in ('D','L','E'));target=raw['session_config']['session_research_target_ns']
assert research>=target
effective=copy.deepcopy(raw)
effective.update(closed_ns={k:modes[k] for k in raw['closed_ns']},research_ns=research,session_research_ns=research,cycle_research_ns=raw['session_config']['prior_cycle_research_ns']+research,program_research_ns=raw['session_config']['prior_program_research_ns']+research,total_engaged_ns=research+modes['O'],purpose_ns=dict(purposes),lane_ns=dict(lanes),raw_actuals='actuals.json',applied_dispositions=entries,clock_active=False,research_closed_utc='2026-10-14T22:26:55.832669+00:00',session_target_ns=target,session_overshoot_ns=research-target,publication_research_credit_ns=0,status='closed_author_directed_two_hour_handoff',segment_count=len(segments),note='One resident runtime. Two research context-refresh intervals and one setup interval excluded from research; another O context gap excluded from engagement. No s09, helper, stale clock or publication credit.')
effective['phase_research_ns']=effective['historical_phase_ns']+effective['program_research_ns']
for prefix,key in [('research','research_ns'),('cycle_research','cycle_research_ns'),('program_research','program_research_ns'),('phase_research','phase_research_ns'),('total_engaged','total_engaged_ns')]:effective[prefix+'_minutes']=str(Decimal(effective[key])/Decimal(60000000000))
effective['mode_minutes']={k:str(Decimal(v)/Decimal(60000000000)) for k,v in effective['closed_ns'].items()}
effective['source_hashes']={p:sha(HERE/p) for p in ('actuals.json','events.jsonl','segments.jsonl','dispositions.json','clock_source.py','session_config.json')}
(HERE/'effective_actuals.json').write_text(json.dumps(effective,indent=2)+'\n',encoding='utf-8')
ledger=ROOT/'v3/time_ledger.csv';marker='s10 effective disposition correction;'
if marker not in ledger.read_text(encoding='utf-8'):
    with ledger.open('a',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        for j,d in enumerate(entries,1):
            ns=d['elapsed_ns'];sec=f'{Decimal(ns)/Decimal(1000000000):.9f}';s=lookup[d['start_monotonic_ns'],d['end_monotonic_ns']]
            writer.writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s10-correction-'+str(j),d['effective_mode'],s['start']['lane'] if d['effective_mode']!='unmeasured' else'',s['start']['utc'],s['end']['utc'],sec,'0','0','0',sec if d['effective_mode']=='unmeasured' else'0','0','v3/discovery/s10/effective_actuals.json',marker+' replaces matching raw classification, not additive time; '+d['reason']])
print(json.dumps({k:effective[k] for k in ('research_ns','research_minutes','cycle_research_ns','cycle_research_minutes','phase_research_ns','phase_research_minutes','closed_ns','segment_count')},indent=2))
