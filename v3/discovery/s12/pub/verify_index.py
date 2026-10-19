"""Check the staged closing evidence and unchanged historical boundaries."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[4]
HERE=ROOT/'v3/discovery/s12'
manifest=json.loads((HERE/'manifest.json').read_text())
paths=['v3/discovery/s12/'+r['path'] for r in manifest['files']]
raw=subprocess.check_output(['git','cat-file','--batch'],input=''.join(':'+p+'\n' for p in paths).encode(),cwd=ROOT)
pos=0
for path,record in zip(paths,manifest['files']):
    end=raw.index(b'\n',pos);header=raw[pos:end].split();assert header[1]==b'blob',(path,header)
    size=int(header[2]);data=raw[end+1:end+1+size];pos=end+size+2
    assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256'],path
    assert (ROOT/path).read_bytes()==data,path
assert pos==len(raw)
table=(ROOT/'v3/discovery/recurrences.md').read_text(encoding='utf-8')
blocks=[];block=[]
for line in table.splitlines()+['']:
    if line.startswith('|'): block.append(line)
    elif block: blocks.append(block);block=[]
assert len(blocks)==1 and len(blocks[0])==24
assert all(len(line.split('|'))-2==14 for line in blocks[0])
ledger=(ROOT/'v3/time_ledger.csv').read_bytes()
old=subprocess.check_output(['git','show','b815009c1fcc458b85bd83129f2ab23c554e65eb:v3/time_ledger.csv'],cwd=ROOT)
assert ledger.startswith(old)
print(json.dumps({'status':'PASS','staged_manifest_files':len(paths),'staged_evidence_bytes':sum(r['bytes'] for r in manifest['files']),'recurrence_tables':1,'recurrence_rows':22,'columns':14,'old_ledger_prefix_preserved':True},indent=2))
