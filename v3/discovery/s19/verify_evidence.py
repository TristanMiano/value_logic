"""Read-only identity/history checks; --write-manifest records closing bytes.

No scientific probes are rerun; hash identity is not mathematical confirmation.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

H=Path(__file__).resolve().parent;D=H.parent;ROOT=H.parents[2]
BASE='d1c7443f216ddb37c6083d5c503618d7a2441e97'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def gitfile(n):return subprocess.check_output(['git','show',BASE+':'+n],cwd=ROOT)
pool=list(H.glob('*'))+[D/'s10/clock_source.py']
byhash={}
for p in pool:
 if p.is_file() and p.suffix in ('.py','.json','.jsonl') and p.name!='manifest.json':byhash.setdefault(sha(p),[]).append(p)
embedded={}
for name in ['range_cert_bundles.json','forest_cert_bundle.json']:
 for i,item in enumerate(read(H/name)):
  digest=hashlib.sha256(json.dumps(item['problem'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
  assert item['certificate']['problem_sha256']==digest
  embedded.setdefault(digest,[]).append(name+'['+str(i)+'].problem')
bindings=[]
def walk(obj,record,location=''):
 if isinstance(obj,list):
  for i,v in enumerate(obj):walk(v,record,location+'['+str(i)+']')
 elif isinstance(obj,dict):
  for k,v in obj.items():
   field=location+'.'+k
   if k.endswith('_sha256'):
    assert isinstance(v,str) and len(v)==64,(record,field)
    if k=='problem_sha256':
     assert v in embedded,(record,field,'unknown problem')
     bindings.append(dict(record=record,field=field,embedded=embedded[v],sha256=v))
    else:
     targets=byhash.get(v,[]);assert targets,('unresolved digest',record,field,v)
     if k in ('source_sha256','script_sha256','probe_sha256'):
      targets=[p for p in targets if p.parent==H and p.suffix=='.py'];assert len(targets)==1
     bindings.append(dict(record=record,field=field,inputs=[p.relative_to(ROOT).as_posix() for p in targets],sha256=v))
   else:walk(v,record,field)
for p in sorted(H.glob('*.json')):
 if p.name=='manifest.json':continue
 obj=read(p);walk(obj,p.name)
 if isinstance(obj,dict):
  for field in ('source_hashes','hashes','dependencies','inputs','sources'):
   values=obj.get(field,{})
   if not isinstance(values,dict):continue
   for name,digest in values.items():
    target=ROOT/name if name.startswith('v3/') else H/name
    assert isinstance(digest,str) and sha(target)==digest,(p.name,field,name)
    bindings.append(dict(record=p.name,field=field,input=name,sha256=digest))

a=read(H/'effective_actuals.json')
assert not a['clock_active'] and a['research_ns']==14403095000000
assert a['program_research_ns']==181187017241147 and a['phase_research_ns']==246354899282996
assert sum(a['closed_ns'][x] for x in ('D','L','E'))==a['research_ns']
assert sum(a['purpose_ns'].values())==sum(a['lane_ns'].values())==a['research_ns']
segments=[json.loads(x) for x in (H/'segments.jsonl').read_text().splitlines() if x.strip()]
assert len(segments)==a['segment_count']==153
for s in segments:
 assert s['start']['runtime']==s['end']['runtime']==a['runtime']
 assert s['elapsed_ns']==s['end']['monotonic_ns']-s['start']['monotonic_ns']
assert len(read(H/'dispositions.json'))==21
metrics=read(H/'progress_metrics.json')
for item in metrics['sources']:assert sha(D/item['path'])==item['sha256']
table=read(D/'recurrences.json');row=table['rows'][-1]
assert len(table['rows'])==29 and row['id']=='s19_cp01'
assert table['rendered_table']['row_ids']==[r['id'] for r in table['rows']]
assert table['rendered_table']['latest_row_id']=='s19_cp01'
assert row['fixed_metrics']['families_total']['value']==row['cumulative_new_family_count']==36
assert row['research_ns']==a['research_ns']
assert row['time_evidence']['sha256']==sha(H/'effective_actuals.json')
assert row['metric_values']['sha256']==sha(H/'progress_metrics.json')
oldbytes=gitfile('v3/discovery/recurrences.json')
assert json.loads(oldbytes)['rows']==table['rows'][:28]
def raw_rows(blob):
 s=blob.decode('utf-8');i=s.index('[',s.index('"rows"'))+1;out=[];decoder=json.JSONDecoder()
 while True:
  while s[i].isspace() or s[i]==',':i+=1
  if s[i]==']':return out
  _,end=decoder.raw_decode(s,i);out.append(s[i:end]);i=end
assert raw_rows(oldbytes)==raw_rows((D/'recurrences.json').read_bytes())[:28]
newmd=(D/'recurrences.md').read_text(encoding='utf-8')
for line in gitfile('v3/discovery/recurrences.md').decode('utf-8').splitlines():
 if line.startswith('| '):assert line in newmd,line[:60]
assert (ROOT/'v3/time_ledger.csv').read_bytes().startswith(gitfile('v3/time_ledger.csv'))
plan=read(ROOT/'v3/plan.v1.json')
assert plan['active_session'] is None
assert plan['discovery_program']['research_ns']==a['program_research_ns']
assert plan['observed_progress']['research_ns']==a['phase_research_ns']
assert plan['discovery_program']['next_portfolio_review_minutes']==6000
names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--','v3/discovery/s19'],cwd=ROOT,text=True).splitlines()
names=sorted(set(n for n in names if n not in ('v3/discovery/s19/manifest.json','v3/discovery/s19/publication.md') and not n.startswith('v3/discovery/s19/pub/')))
if '--write-manifest' in sys.argv:
 files=[dict(path=(ROOT/n).relative_to(H).as_posix(),sha256=sha(ROOT/n),bytes=(ROOT/n).stat().st_size) for n in names]
 manifest=dict(contributor='Codex (GPT-6)',classification='DEVELOPMENT',
  note='Closing source/output/note/clock identity; publication/pub excluded. No independent confirmation.',files=files,execution_bindings=bindings)
 (H/'manifest.json').write_bytes((json.dumps(manifest,indent=2)+'\n').encode())
manifest=read(H/'manifest.json')
assert [(H/x['path']).relative_to(ROOT).as_posix() for x in manifest['files']]==names
for item in manifest['files']:
 p=H/item['path'];assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes'],p
assert manifest['execution_bindings']==bindings
index_count=0
if '--index' in sys.argv:
 entries=subprocess.check_output(['git','ls-files','--stage','--','v3/discovery/s19'],cwd=ROOT,text=True).splitlines()
 for entry in entries:
  metadata,name=entry.split('\t',1);_,digest,stage=metadata.split();assert stage=='0'
  blob=(ROOT/name).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()==digest,('index differs',name)
  index_count+=1
print(json.dumps(dict(status='PASS',manifest_files=len(manifest['files']),execution_input_bindings=len(bindings),
 prior_rows_byte_preserved=28,prior_ledger_prefix_preserved=True,recurrence_rows=29,research_ns=a['research_ns'],index_bound_files=index_count),indent=2))
