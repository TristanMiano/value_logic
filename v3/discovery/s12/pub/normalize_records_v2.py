"""Restore unchanged baseline lines byte-for-byte in mixed-newline reports."""
from pathlib import Path
from difflib import SequenceMatcher
import json
import subprocess

root=Path(__file__).resolve().parents[4]
names=['TODO_v3.md','v3/plan.v1.json','v3/discovery/P3_SEARCH_01.md',
       'v3/discovery/candidates.md','v3/discovery/recurrences.md']
out=[]
for name in names:
    old=subprocess.check_output(['git','show','b815009c1fcc458b85bd83129f2ab23c554e65eb:'+name],cwd=root).splitlines(keepends=True)
    path=root/name;current=path.read_bytes().splitlines(keepends=True)
    key=lambda lines:[s.rstrip(b'\r\n') for s in lines]
    matcher=SequenceMatcher(None,key(old),key(current),autojunk=False)
    rebuilt=[];reused=0
    for tag,i,j,k,l in matcher.get_opcodes():
        if tag=='equal': rebuilt.extend(old[i:j]);reused+=j-i
        else: rebuilt.extend(current[k:l])
    assert key(rebuilt)==key(current)
    path.write_bytes(b''.join(rebuilt))
    out.append(dict(path=name,unchanged_lines_preserved=reused))
print(json.dumps(out,indent=2))
