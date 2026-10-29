"""Reconcile s20 without changing raw observations or previous ledger bytes."""
from collections import Counter
from decimal import Decimal, getcontext
from pathlib import Path
import csv, hashlib, io, json
getcontext().prec=45
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def minutes(n): return str(Decimal(n)/60000000000)
raw=read(HERE/'actuals.json'); assert raw['status']=='closed' and raw['open_segment'] is None
segments=[json.loads(s) for s in (HERE/'segments.jsonl').read_text().splitlines()]
dispositions=read(HERE/'dispositions.json'); bykey={}
for d in dispositions:
 key=(d['start_monotonic_ns'],d['end_monotonic_ns']); assert key not in bykey; bykey[key]=d
for s in segments:
 key=(s['start']['monotonic_ns'],s['end']['monotonic_ns'])
 if s['effective_mode']=='O' and s['start']['purpose']=='context' and key not in bykey:
  d=dict(start_monotonic_ns=key[0],end_monotonic_ns=key[1],elapsed_ns=s['elapsed_ns'],raw_mode='O',effective_mode='unmeasured',reason='Explicit context/recovery; excluded from engagement.'); dispositions.append(d); bykey[key]=d
modes=Counter(); rawmodes=Counter(); purposes=Counter(); lanes=Counter(); stages=read(HERE/'stages.json')['confirmation']; stage_ns=[0]*len(stages); corrections=[]; transfers=[]; seen=set()
for s in segments:
 a,b=s['start']['monotonic_ns'],s['end']['monotonic_ns']; key=(a,b); n=s['elapsed_ns']; assert key not in seen; seen.add(key)
 assert s['start']['runtime']==s['end']['runtime'] and n==b-a>=0
 mode=s['effective_mode']; rawmodes[mode]+=n
 if key in bykey:
  d=bykey[key]; assert d['elapsed_ns']==n and d['raw_mode']==mode
  mode=d['effective_mode']; corrections.append((d,s))
 modes[mode]+=n
 if mode not in ('D','L','E'): continue
 purposes[s['start']['purpose']]+=n; lanes[s['start']['lane']]+=n
 for i,st in enumerate(stages):
  x,y=st['start']['monotonic_ns'],st['end']['monotonic_ns']
  if max(a,x)<min(b,y):
   assert x<=a<=b<=y
   stage_ns[i]+=n; transfers.append(s)
assert set(bykey)<=seen
assert dict(rawmodes)=={k:v for k,v in raw['closed_ns'].items() if v}
research=sum(modes[m] for m in ('D','L','E')); confirm=sum(stage_ns); discovery=research-confirm
assert research>=14400000000000
assert sum(purposes.values())==sum(lanes.values())==research
assert confirm==read(ROOT/'v3/confirmation/v19a/actuals.json')['research_ns']==5424657572500
prior=read(HERE.parent/'s19/effective_actuals.json')
assert prior['program_research_ns']==raw['session_config']['prior_program_research_ns']
result=dict(contributor='Codex (GPT-6)',status='closed_selected_work_complete_author_checkpoint_pending',clock_active=False,research_closed_utc='2026-10-29T01:44:38.247939+00:00',clock_closed_utc=raw['observed']['utc'],research_ns=research,session_research_ns=research,session_target_ns=14400000000000,session_overshoot_ns=research-14400000000000,closed_ns=dict(modes),purpose_ns=dict(purposes),lane_ns=dict(lanes),segment_count=len(segments),runtime=raw['observed']['runtime'],historical_phase_ns=prior['historical_phase_ns'],prior_program_research_ns=prior['program_research_ns'],prior_phase_research_ns=prior['phase_research_ns'],program_research_ns=prior['program_research_ns']+discovery,cycle_research_ns=prior['cycle_research_ns']+discovery,phase_research_ns=prior['phase_research_ns']+research,discovery_research_ns=discovery,confirmation_research_ns=confirm,confirmation_interval_ns=stage_ns,total_engaged_ns=research+modes['O'],publication_research_credit_ns=0,applied_dispositions=dispositions,source_hashes={n:sha(HERE/n) for n in ['actuals.json','events.jsonl','segments.jsonl','dispositions.json','session_config.json','stages.json']},note='Whole uncertain intervals excluded. P3-11 counted once toward session/phase and zero toward discovery. Mode/purpose boundaries are coarse engagement observations; machine runtime is not added. Administration total is partial, with later publication uncredited.')
for k in ['research','program_research','cycle_research','phase_research','total_engaged','discovery_research','confirmation_research']: result[k+'_minutes']=minutes(result[k+'_ns'])
result['mode_minutes']={k:minutes(v) for k,v in modes.items()}
result['purpose_percent']={k:str(Decimal(v)*100/research) for k,v in purposes.items()}
result['lane_percent']={k:str(Decimal(v)*100/research) for k,v in lanes.items()}
(HERE/'effective_actuals.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
ledger=ROOT/'v3/time_ledger.csv'; existing=ledger.read_bytes(); marker='s20 additive reconciliation;'; rows=[]
def row(s,task,attempt,sid,mode,sign,note):
 sec=str(Decimal(sign*s['elapsed_ns'])/1000000000)
 return [task,attempt,sid,mode,s['start'].get('lane','') if mode in ('D','L','E') else '',s['start']['utc'],s['end']['utc'],sec,sec if mode in ('D','L','E','O') else '0',sec if mode=='wait' else '0','0',sec if mode=='unmeasured' else '0','0','v3/discovery/s20/effective_actuals.json',marker+note]
for i,(d,s) in enumerate(corrections,1):
 rows.append(row(s,'P3-SEARCH-01','P3-SEARCH-01-C001',f's20-exclude-{i}',d['raw_mode'],-1,' reverse raw interval; '+d['reason']))
 rows.append(row(s,'P3-SEARCH-01','P3-SEARCH-01-C001',f's20-exclude-{i}',d['effective_mode'],1,' apply explicit disposition; '+d['reason']))
for i,s in enumerate(transfers,1):
 rows.append(row(s,'P3-SEARCH-01','P3-SEARCH-01-C001',f's20-stage-{i}',s['effective_mode'],-1,' remove confirmation from discovery'))
 rows.append(row(s,'P3-11','P3-11-A1',f's20-stage-{i}',s['effective_mode'],1,' assign confirmation once to P3-11'))
if marker.encode() not in existing:
 buffer=io.StringIO(newline=''); csv.writer(buffer,lineterminator='\n').writerows(rows)
 with ledger.open('ab') as f: f.write(buffer.getvalue().encode())
 assert ledger.read_bytes()[:len(existing)]==existing
 (HERE/'ledger_append.json').write_text(json.dumps(dict(prefix_bytes=len(existing),prefix_sha256=hashlib.sha256(existing).hexdigest(),append_rows=len(rows),disposition_pairs=len(corrections),stage_pairs=len(transfers)),indent=2)+'\n')
else:
 assert existing.count(marker.encode())==len(rows)
 saved=read(HERE/'ledger_append.json'); assert hashlib.sha256(existing[:saved['prefix_bytes']]).hexdigest()==saved['prefix_sha256']
print(json.dumps({k:result[k] for k in ['research_minutes','confirmation_research_minutes','discovery_research_minutes','program_research_minutes','phase_research_minutes','mode_minutes','purpose_percent','lane_percent','segment_count']},indent=2))
