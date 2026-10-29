"""Read-only publication integrity checks. Does not rerun scientific probes."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[3];H=ROOT/'v3/discovery/s20'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=0; errors=[]
for base in [H,ROOT/'v3/confirmation/v19a']:
 for p in base.rglob('*.json'):
  d=read(p)
  if not isinstance(d,dict):continue
  if isinstance(d.get('sha256'),dict):
   for name,h in d['sha256'].items():
    q=ROOT/name if name.startswith('v3/') else p.parent/name
    if not q.is_file() or sha(q)!=h:errors.append((str(p.relative_to(ROOT)),name))
    checks+=1
  if 'records_sha256' in d:
   q=p.parent/({'audit_results.json':'audit_records.jsonl','component_result.json':'component_records.jsonl.gz'}.get(p.name,'records.jsonl.gz'))
   if not q.exists():q=p.parent/'records.jsonl'
   if not q.exists() or sha(q)!=d['records_sha256']:errors.append((str(p),'records'))
   checks+=1
for stem,source in [('layer','Layer'),('mask','Mask'),('mask_complete','MaskComplete')]:
 p=ROOT/'v3/confirmation/v19a';d=read(p/(stem+'_seal.json'))
 for key,name in [('source_sha256',source+'.lean'),('runner_sha256',stem+'_check.py'),('scope_sha256',stem+'_scope.md')]:
  assert sha(p/name)==d[key];checks+=1
original=read(ROOT/'v3/confirmation/v19a/freeze.json');exitseal=read(ROOT/'v3/confirmation/v19a/exit_manifest.json')
assert len(original['sha256'])==24 and len(exitseal['sha256'])==60
ledger=read(H/'ledger_append.json');raw=(ROOT/'v3/time_ledger.csv').read_bytes();assert hashlib.sha256(raw[:ledger['prefix_bytes']]).hexdigest()==ledger['prefix_sha256']
oldjson=subprocess.check_output(['git','show','54685b9b55039e2513d1aeda263841ed43fa82cd:v3/discovery/recurrences.json']);new=read(ROOT/'v3/discovery/recurrences.json');old= json.loads(oldjson);assert len(old['rows'])==29 and len(new['rows'])==30 and new['rows'][:29]==old['rows']
oldmd=subprocess.check_output(['git','show','54685b9b55039e2513d1aeda263841ed43fa82cd:v3/discovery/recurrences.md']);newmd=(ROOT/'v3/discovery/recurrences.md').read_bytes()
assert all(line in newmd for line in oldmd.splitlines(keepends=True) if line.startswith(b'| '))
a=read(H/'effective_actuals.json');assert a['research_ns']==a['discovery_research_ns']+a['confirmation_research_ns']>=14400000000000
for row in new['rows'][-1:]:
 assert row['research_ns']==a['discovery_research_ns'];assert row['cumulative_research_ns']==a['program_research_ns']
 assert row['metric_values']['sha256']==sha(H/'progress_metrics.json')
 for item in row['metric_sources']:assert sha(ROOT/'v3/discovery'/item['path'])==item['sha256']
result=dict(status='PASS' if not errors else 'FAIL',hash_references_checked=checks,original_freeze_files=24,exit_seal_files=60,historical_rows_preserved=29,ledger_prefix_preserved=True,errors=errors,note='Integrity only; no scientific reruns or new research credit.')
(H/'integrity.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2));assert not errors
