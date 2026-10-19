"""Preserve the baseline line endings of mutable reporting files only."""
from pathlib import Path
import json
import subprocess

root=Path(__file__).resolve().parents[4]
names=['TODO_v3.md','v3/plan.v1.json','v3/discovery/P3_SEARCH_01.md',
       'v3/discovery/candidates.md','v3/discovery/recurrences.md']
out=[]
for name in names:
    old=subprocess.check_output(['git','show','b815009c1fcc458b85bd83129f2ab23c554e65eb:'+name],cwd=root)
    path=root/name;current=path.read_bytes()
    if old.count(b'\r\n')==old.count(b'\n') and b'\n' in old:
        normalized=current.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
        path.write_bytes(normalized)
        out.append(dict(path=name,baseline='CRLF',changed=current!=normalized))
    else:
        out.append(dict(path=name,baseline='LF_or_mixed',changed=False))
print(json.dumps(out,indent=2))
