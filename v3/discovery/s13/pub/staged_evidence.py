"""Check the Git index against the closing scientific manifest."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[4]
HERE=ROOT/'v3/discovery/s13'
m=json.loads((HERE/'manifest.json').read_text())
items=m['files']
query=''.join(':v3/discovery/s13/'+x['path']+'\n' for x in items).encode()
out=subprocess.check_output(['git','cat-file','--batch'],input=query,cwd=ROOT)
offset=0
for item in items:
    end=out.index(b'\n',offset);header=out[offset:end].decode();offset=end+1
    _,kind,size=header.split();assert kind=='blob'
    size=int(size);blob=out[offset:offset+size];offset+=size+1
    assert size==item['bytes'] and hashlib.sha256(blob).hexdigest()==item['sha256'],item['path']
assert offset==len(out)
rows=[line for line in (ROOT/'v3/discovery/recurrences.md').read_text(encoding='utf-8').splitlines() if line.startswith('| ') and '/checkpoint.md)' in line or line.startswith('| ') and ('/cp0' in line or '/interruption.json)' in line or '/effective_actuals.json)' in line)]
assert len(rows)==23,len(rows)
assert all(len(line.split('|'))==16 for line in rows)
print(json.dumps(dict(status='PASS',staged_manifest_files=len(items),table_data_rows=len(rows),table_columns=14),indent=2))
