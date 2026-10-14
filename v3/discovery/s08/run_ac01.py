"""Cold processes for the declared anchor-cover screen."""
from pathlib import Path
import json
import subprocess
import sys
import anchor_cover as ac
root=ac.HERE/'ac01'
if not root.exists():
    root.mkdir();design=json.loads((ac.HERE/'op01/design.json').read_text());design['source_sha256']=ac.g01.sha(ac.__file__);design['physical_audits']=0
    ac.g01.save(root/'design.json',design);(root/'impl.py').write_bytes(Path(ac.__file__).read_bytes());(root/'declaration.md').write_bytes((ac.HERE/'anchor_cover.md').read_bytes())
design=json.loads((root/'design.json').read_text())
for case in design['cases']:
    directory=root/case['name']
    if(directory/'screen.json').exists():continue
    if directory.exists():raise RuntimeError('Incomplete unit needs disposition')
    index=1
    while(root/f"{case['name']}_{index}.log").exists():index+=1
    with(root/f"{case['name']}_{index}.log").open('w') as log:
        p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={ac.HERE/"unused_cache"}','-X','faulthandler',str(ac.HERE/'anchor_cover.py'),str(root),case['name']],stdout=log,stderr=subprocess.STDOUT)
    print(case['name'],index,p.returncode,flush=True)
    if p.returncode:raise SystemExit(p.returncode)
