"""Read-only s14 evidence checks; --write-manifest explicitly binds closing files."""
from pathlib import Path
import hashlib, json, subprocess, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DISC=HERE.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def resolve(name):
    if name.startswith('v3/'):return ROOT/name
    if name.split('/')[0] in ('s12','s13','s14'):return DISC/name
    return HERE/name
bindings=[]
for p in sorted(HERE.glob('*.json')):
    obj=read(p)
    if not isinstance(obj,dict):continue
    source=p.with_suffix('.py')
    for key in ('source_sha256','script_sha256'):
        if key in obj and source.exists():
            assert sha(source)==obj[key],(p.name,key)
            bindings.append(dict(record=p.name,input=source.name,sha256=sha(source)))
    for field in ('hashes','dependencies','dependency_sha256','source_hashes'):
        values=obj.get(field,{})
        if not isinstance(values,dict):continue
        for name,digest in values.items():
            if not isinstance(digest,str) or len(digest)!=64:continue
            target=resolve(name)
            assert target.exists() and sha(target)==digest,(p.name,field,name)
            bindings.append(dict(record=p.name,input=name,sha256=digest))
a=read(HERE/'effective_actuals.json')
assert a['research_ns']==14407076000000 and not a['clock_active']
assert a['program_research_ns']==109122750241147 and a['phase_research_ns']==174290632282996
metrics=read(HERE/'progress_metrics.json')
for item in metrics['sources']:
    assert sha(DISC/item['path'])==item['sha256'],item['path']
table=read(DISC/'recurrences.json')
assert len(table['rows'])==24 and table['rows'][-1]['id']=='s14_cp01'
assert table['rows'][-1]['research_ns']==a['research_ns']
assert table['rows'][-1]['time_evidence']['sha256']==sha(HERE/'effective_actuals.json')
assert table['rows'][-1]['metric_values']['sha256']==sha(HERE/'progress_metrics.json')
base='e2fa680858db59b502991789f21db18d4854d7ec'
old_bytes=subprocess.check_output(['git','show',base+':v3/discovery/recurrences.json'],cwd=ROOT)
old=json.loads(old_bytes)
assert old['rows']==table['rows'][:23]
def raw_rows(blob):
    s=blob.decode('utf-8');i=s.index('"rows"');i=s.index('[',i)+1;out=[];decoder=json.JSONDecoder()
    while True:
        while s[i].isspace() or s[i]==',':i+=1
        if s[i]==']':return out
        _,end=decoder.raw_decode(s,i);out.append(s[i:end]);i=end
assert raw_rows(old_bytes)==raw_rows((DISC/'recurrences.json').read_bytes())[:23]
old_md=subprocess.check_output(['git','show',base+':v3/discovery/recurrences.md'],cwd=ROOT).decode('utf-8')
new_md=(DISC/'recurrences.md').read_text(encoding='utf-8')
for line in old_md.splitlines():
    if line.startswith('| ') and ('s01/' in line or any(f's{i:02}/' in line for i in range(2,14))):
        assert line in new_md,line[:50]
old_ledger=subprocess.check_output(['git','show',base+':v3/time_ledger.csv'],cwd=ROOT)
assert (ROOT/'v3/time_ledger.csv').read_bytes().startswith(old_ledger)
if '--write-manifest' in sys.argv:
    names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--','v3/discovery/s14'],cwd=ROOT,text=True).splitlines()
    files=[]
    for name in sorted(set(names)):
        p=ROOT/name;rel=p.relative_to(HERE).as_posix()
        if rel in ('manifest.json','publication.md') or rel.startswith('pub/'):continue
        assert p.is_file()
        files.append(dict(path=rel,sha256=sha(p),bytes=p.stat().st_size))
    manifest=dict(contributor='Codex (GPT-6)',classification='DEVELOPMENT',
        note='Closing source/output/note/clock binding; publication and pub logs excluded to avoid circularity. Identity is not independent confirmation.',files=files,execution_bindings=bindings)
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
for item in read(HERE/'manifest.json')['files']:
    p=HERE/item['path'];assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes'],p
index_bound_files=0
if '--index' in sys.argv:
    entries=subprocess.check_output(['git','ls-files','--stage','--','v3/discovery/s14'],cwd=ROOT,text=True).splitlines()
    for entry in entries:
        metadata,name=entry.split('\t',1);mode,digest,stage=metadata.split()
        assert stage=='0',name
        blob=(ROOT/name).read_bytes()
        expected=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()
        assert expected==digest,('index bytes differ from working evidence',name)
        index_bound_files+=1
print(json.dumps(dict(status='PASS',manifest_files=len(read(HERE/'manifest.json')['files']),
    execution_input_bindings=len(bindings),prior_rows_byte_preserved=23,prior_ledger_prefix_preserved=True,
    recurrence_rows=24,research_ns=a['research_ns'],index_bound_files=index_bound_files),indent=2))
