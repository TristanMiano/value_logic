"""Read-only closing identity checks; --write-manifest binds current s17 files.

Digest lookup is exhaustive for every top-level *_sha256 execution field:
unresolved digests fail, rather than silently skipping unfamiliar result names.
This checks recorded identity, not mathematical truth or independent confirmation.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DISC=HERE.parent
BASE='e709bc316c352547242fbb43b4fcd6d7ce97927b'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def gitfile(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)

pool=list(HERE.glob('*'))+list((DISC/'s16').glob('*'))+[DISC/'s10/clock_source.py']
byhash={}
for p in pool:
    if p.is_file() and p.suffix in ('.py','.json','.jsonl') and p.name!='manifest.json':
        byhash.setdefault(sha(p),[]).append(p)
bindings=[]
for p in sorted(HERE.glob('*.json')):
    if p.name=='manifest.json':continue
    obj=read(p)
    if not isinstance(obj,dict):continue
    for field,digest in obj.items():
        if not field.endswith('_sha256'):continue
        assert isinstance(digest,str) and len(digest)==64,(p.name,field)
        targets=byhash.get(digest,[])
        assert targets,('unresolved execution digest',p.name,field,digest)
        if field in ('source_sha256','script_sha256','probe_sha256'):
            targets=[x for x in targets if x.parent==HERE and x.suffix=='.py']
            assert len(targets)==1,('ambiguous or absent executed source',p.name,field)
        bindings.append(dict(record=p.name,field=field,
            inputs=[x.relative_to(ROOT).as_posix() for x in targets],sha256=digest))
    for field in ('source_hashes','hashes','dependencies'):
        values=obj.get(field,{})
        assert isinstance(values,dict),(p.name,field)
        for name,digest in values.items():
            target=ROOT/name if name.startswith('v3/') else HERE/name
            assert isinstance(digest,str) and sha(target)==digest,(p.name,field,name)
            bindings.append(dict(record=p.name,field=field,input=name,sha256=digest))

a=read(HERE/'effective_actuals.json')
assert not a['clock_active'] and a['research_ns']==14423719000000
assert a['program_research_ns']==152369325241147 and a['phase_research_ns']==217537207282996
assert sum(a['closed_ns'][x] for x in ('D','L','E'))==a['research_ns']
assert sum(a['purpose_ns'].values())==sum(a['lane_ns'].values())==a['research_ns']
segments=[json.loads(x) for x in (HERE/'segments.jsonl').read_text().splitlines() if x.strip()]
assert len(segments)==a['segment_count']==178
for s in segments:
    assert s['start']['runtime']==s['end']['runtime']==a['runtime']
    assert s['elapsed_ns']==s['end']['monotonic_ns']-s['start']['monotonic_ns']
metrics=read(HERE/'progress_metrics.json')
for item in metrics['sources']:assert sha(DISC/item['path'])==item['sha256'],item['path']
table=read(DISC/'recurrences.json');row=table['rows'][-1]
assert len(table['rows'])==27 and row['id']=='s17_cp01'
assert row['research_ns']==a['research_ns']
assert row['time_evidence']['sha256']==sha(HERE/'effective_actuals.json')
assert row['metric_values']['sha256']==sha(HERE/'progress_metrics.json')
oldbytes=gitfile('v3/discovery/recurrences.json')
assert json.loads(oldbytes)['rows']==table['rows'][:26]
def raw_rows(blob):
    s=blob.decode('utf-8');i=s.index('[',s.index('"rows"'))+1;out=[];decoder=json.JSONDecoder()
    while True:
        while s[i].isspace() or s[i]==',':i+=1
        if s[i]==']':return out
        _,end=decoder.raw_decode(s,i);out.append(s[i:end]);i=end
assert raw_rows(oldbytes)==raw_rows((DISC/'recurrences.json').read_bytes())[:26]
oldmd=gitfile('v3/discovery/recurrences.md').decode('utf-8')
newmd=(DISC/'recurrences.md').read_text(encoding='utf-8')
for line in oldmd.splitlines():
    if line.startswith('| '):assert line in newmd,line[:60]
assert (ROOT/'v3/time_ledger.csv').read_bytes().startswith(gitfile('v3/time_ledger.csv'))
plan=read(ROOT/'v3/plan.v1.json')
assert plan['active_session'] is None
assert plan['discovery_program']['research_ns']==a['program_research_ns']
assert plan['observed_progress']['research_ns']==a['phase_research_ns']
assert plan['discovery_program']['next_portfolio_review_minutes']==6000

def session_files():
    names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--','v3/discovery/s17'],cwd=ROOT,text=True).splitlines()
    return sorted(set(name for name in names if name not in
        ('v3/discovery/s17/manifest.json','v3/discovery/s17/publication.md') and
        not name.startswith('v3/discovery/s17/pub/')))
names=session_files()
if '--write-manifest' in sys.argv:
    files=[dict(path=(ROOT/name).relative_to(HERE).as_posix(),sha256=sha(ROOT/name),bytes=(ROOT/name).stat().st_size) for name in names]
    manifest=dict(contributor='Codex (GPT-6)',classification='DEVELOPMENT',
        note='Closing source/output/note/clock identity. Publication and pub logs excluded to avoid circularity. No independent confirmation.',
        files=files,execution_bindings=bindings)
    (HERE/'manifest.json').write_bytes((json.dumps(manifest,indent=2)+'\n').encode('utf-8'))
manifest=read(HERE/'manifest.json')
assert [str((HERE/x['path']).relative_to(ROOT)).replace('\\','/') for x in manifest['files']]==names
for item in manifest['files']:
    p=HERE/item['path'];assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes'],p
assert manifest['execution_bindings']==bindings
index_count=0
if '--index' in sys.argv:
    entries=subprocess.check_output(['git','ls-files','--stage','--','v3/discovery/s17'],cwd=ROOT,text=True).splitlines()
    for entry in entries:
        metadata,name=entry.split('\t',1);_,digest,stage=metadata.split();assert stage=='0',name
        blob=(ROOT/name).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()==digest,('index differs',name)
        index_count+=1
print(json.dumps(dict(status='PASS',manifest_files=len(manifest['files']),
    execution_input_bindings=len(bindings),prior_rows_byte_preserved=26,
    prior_ledger_prefix_preserved=True,recurrence_rows=27,research_ns=a['research_ns'],
    index_bound_files=index_count),indent=2))
