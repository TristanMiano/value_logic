"""Restore existing active-document line endings without changing content."""
from pathlib import Path
import subprocess
from difflib import SequenceMatcher
root=Path(__file__).resolve().parents[4]
base='5d15dae2a6bc0903ff0589e242c9d9a3450ad9b5'
for name in ('TODO_v3.md','v3/README.md','v3/claim_ledger.md','v3/discovery/CONTINUE.md',
             'v3/discovery/P3_SEARCH_01.md','v3/discovery/candidates.md','v3/discovery/recurrences.md','v3/plan.v1.json'):
    old=subprocess.check_output(['git','show',base+':'+name],cwd=root)
    current=(root/name).read_bytes()
    old_lines=old.splitlines(keepends=True)
    new_lines=current.splitlines(keepends=True)
    old_keys=[line.rstrip(b'\r\n') for line in old_lines]
    new_keys=[line.rstrip(b'\r\n') for line in new_lines]
    pieces=[]
    for tag,i,j,k,l in SequenceMatcher(None,old_keys,new_keys,autojunk=False).get_opcodes():
        if tag=='equal':pieces.extend(old_lines[i:j])
        elif tag in ('replace','insert'):pieces.extend(line+b'\n' for line in new_keys[k:l])
    changed=b''.join(pieces)
    assert changed.replace(b'\r\n',b'\n')==current.replace(b'\r\n',b'\n')
    (root/name).write_bytes(changed)
    print(name,'preserved unchanged baseline bytes; new lines LF')
