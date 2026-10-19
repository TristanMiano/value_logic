"""Read-only evidence checks, with an explicit administrative manifest writer."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
bindings=[]
for p in sorted(HERE.glob('*.json')):
    obj=read(p)
    if not isinstance(obj,dict): continue
    source=p.with_suffix('.py')
    if 'source_sha256' in obj and source.exists():
        assert sha(source)==obj['source_sha256'],source
        bindings.append(dict(record=p.name,input=source.name,sha256=sha(source)))
    for field in ('hashes','dependencies'):
        vals=obj.get(field,{})
        if not isinstance(vals,dict): continue
        for name,digest in vals.items():
            target=HERE/name
            if not isinstance(digest,str) or len(digest)!=64: continue
            assert target.exists() and sha(target)==digest,(p.name,field,name)
            bindings.append(dict(record=p.name,input=name,sha256=digest))
a=read(HERE/'effective_actuals.json')
assert a['research_ns']==14422390000000 and not a['clock_active']
table=read(HERE.parent/'recurrences.json')
assert len(table['rows'])==22 and table['rows'][-1]['id']=='s12_cp01'
assert table['rows'][-1]['research_ns']==a['research_ns']
assert table['rows'][-1]['time_evidence']['sha256']==sha(HERE/'effective_actuals.json')
assert table['rows'][-1]['metric_values']['sha256']==sha(HERE/'progress_metrics.json')
base='b815009c1fcc458b85bd83129f2ab23c554e65eb'
old_bytes=subprocess.check_output(['git','show',base+':v3/discovery/recurrences.json'],cwd=ROOT)
old=json.loads(old_bytes)
assert old['rows']==table['rows'][:21]
# Raw row substrings are also preserved, not just their decoded meanings.
def raw_rows(blob):
    s=blob.decode('utf-8');i=s.index('"rows"');i=s.index('[',i)+1;out=[];decoder=json.JSONDecoder()
    while True:
        while s[i].isspace() or s[i]==',':i+=1
        if s[i]==']':return out
        _,end=decoder.raw_decode(s,i);out.append(s[i:end]);i=end
assert raw_rows(old_bytes)==raw_rows((HERE.parent/'recurrences.json').read_bytes())[:21]
old_ledger=subprocess.check_output(['git','show',base+':v3/time_ledger.csv'],cwd=ROOT)
assert (ROOT/'v3/time_ledger.csv').read_bytes().startswith(old_ledger)
if '--write-manifest' in sys.argv:
    names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',
        'v3/discovery/s12'],cwd=ROOT,text=True).splitlines()
    files=[]
    for name in sorted(set(names)):
        p=ROOT/name;rel=p.relative_to(HERE).as_posix()
        if rel in ('manifest.json','publication.md') or rel.startswith('pub/'):continue
        assert p.is_file()
        files.append(dict(path=rel,sha256=sha(p),bytes=p.stat().st_size))
    manifest=dict(contributor='Codex (GPT-6)',classification='DEVELOPMENT',
        note='Closing source/output/note/clock binding. Administrative publication record and pub logs excluded to avoid circularity. Hashes establish identity, not independent scientific confirmation.',
        files=files,execution_bindings=bindings)
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
manifest=read(HERE/'manifest.json')
for item in manifest['files']:
    p=HERE/item['path'];assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes'],p
print(json.dumps(dict(status='PASS',manifest_files=len(manifest['files']),
    execution_input_bindings=len(bindings),prior_rows_byte_preserved=21,
    prior_ledger_prefix_preserved=True,recurrence_rows=22,research_ns=a['research_ns']),indent=2))
