"""Exact closed-clock reconciliation; administration, no research credit."""
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path
import copy,csv,hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];getcontext().prec=45
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
raw=read(HERE/'actuals.json');segments=[json.loads(l) for l in (HERE/'segments.jsonl').read_text().splitlines()];modes=Counter();lanes=Counter();purposes=Counter();lookup={}
for s in segments:
    assert s['start']['runtime']==s['end']['runtime'];assert s['elapsed_ns']==s['end']['monotonic_ns']-s['start']['monotonic_ns']
    key=(s['start']['monotonic_ns'],s['end']['monotonic_ns']);assert key not in lookup;lookup[key]=s
    mode=s['effective_mode'];ns=s['elapsed_ns'];modes[mode]+=ns
    if mode in('D','L','E'):lanes[s['start']['lane']]+=ns;purposes[s['start']['purpose']]+=ns
assert dict(modes)=={k:v for k,v in raw['closed_ns'].items() if v}
exclusions=read(HERE/'dispositions.json')['overrides'];changes=read(HERE/'mode_reclassifications.json')['overrides']
for d in exclusions+changes:
    s=lookup[d['start_monotonic_ns'],d['end_monotonic_ns']];assert s['elapsed_ns']==d['elapsed_ns'] and s['effective_mode']==d['raw_mode'];ns=d['elapsed_ns'];modes[d['raw_mode']]-=ns;modes[d['effective_mode']]+=ns
    if d['effective_mode']=='unmeasured':lanes[s['start']['lane']]-=ns;purposes[s['start']['purpose']]-=ns
research=sum(modes[k] for k in('D','L','E'));assert research==14402318580700 and research>=14400000000000
effective=copy.deepcopy(raw);effective.update(closed_ns={k:modes[k] for k in raw['closed_ns']},research_ns=research,session_research_ns=research,cycle_research_ns=raw['session_config']['prior_cycle_research_ns']+research,program_research_ns=raw['session_config']['prior_program_research_ns']+research,total_engaged_ns=research+modes['O'],purpose_ns=dict(purposes),lane_ns=dict(lanes),raw_actuals='actuals.json',applied_dispositions=exclusions,mode_reclassifications=changes,clock_active=False,research_closed_utc='2026-10-14T04:16:50.790658+00:00',session_target_ns=14400000000000,session_overshoot_ns=research-14400000000000,publication_research_credit_ns=0,status='closed_author_directed_four_hour_handoff',note='139 matched closed segments across two runtimes. No cross-runtime subtraction, stale open crash credit, concurrent-agent time or publication credit. Five mixed context-refresh intervals excluded. Raw bytes preserved.')
effective['phase_research_ns']=effective['historical_phase_ns']+effective['program_research_ns']
for prefix,key in [('research','research_ns'),('cycle_research','cycle_research_ns'),('program_research','program_research_ns'),('phase_research','phase_research_ns'),('total_engaged','total_engaged_ns')]:effective[prefix+'_minutes']=str(Decimal(effective[key])/Decimal(60000000000))
effective['mode_minutes']={k:str(Decimal(v)/Decimal(60000000000)) for k,v in effective['closed_ns'].items()}
effective['source_hashes']={p:sha(HERE/p) for p in('actuals.json','events.jsonl','segments.jsonl','dispositions.json','mode_reclassifications.json','clock_source.py','clock_resume.py','crash01_actuals.json')}
(HERE/'effective_actuals.json').write_text(json.dumps(effective,indent=2)+'\n',encoding='utf-8')
ledger=ROOT/'v3/time_ledger.csv';marker='s08 effective disposition correction;'
if marker not in ledger.read_text(encoding='utf-8'):
    with ledger.open('a',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        for j,d in enumerate(exclusions+changes,1):
            ns=d['elapsed_ns'];sec=f'{Decimal(ns)/Decimal(1000000000):.9f}';s=lookup[d['start_monotonic_ns'],d['end_monotonic_ns']]
            writer.writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s08-correction-'+str(j),d['effective_mode'],s['start']['lane'] if d['effective_mode']!='unmeasured' else'',d['start_utc'],d['end_utc'],sec,'0','0','0',sec if d['effective_mode']=='unmeasured' else'0','0','v3/discovery/s08/effective_actuals.json',marker+' replaces classification of matching raw segment; not additive time; '+d['reason']])
print(json.dumps({k:effective[k] for k in('research_ns','research_minutes','cycle_research_ns','cycle_research_minutes','phase_research_ns','phase_research_minutes','closed_ns')},indent=2))
