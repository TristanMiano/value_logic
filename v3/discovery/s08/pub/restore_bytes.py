"""Restore unchanged CRLF-only checkout copies to exact HEAD blob bytes."""
from pathlib import Path
import hashlib,json,subprocess
root=Path(__file__).resolve().parents[4]
files=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0');changed=set(subprocess.check_output(['git','diff','--name-only'],cwd=root).decode().splitlines());candidates=[]
for name in files:
    p=root/name
    if name and name not in changed and p.is_file() and p.suffix in('.md','.json','.jsonl','.py','.txt','.csv','.yaml','.yml','.toml'):
        b=p.read_bytes()
        if b'\r\n' in b:candidates.append((name,b))
proc=subprocess.run(['git','cat-file','--batch'],input=''.join('HEAD:'+name+'\n' for name,b in candidates).encode(),cwd=root,stdout=subprocess.PIPE,check=True);data=proc.stdout;offset=0;record=[]
for name,b in candidates:
    end=data.index(b'\n',offset);header=data[offset:end].split();size=int(header[-1]);g=data[end+1:end+1+size];offset=end+2+size
    if b!=g and b.replace(b'\r\n',b'\n')==g:
        (root/name).write_bytes(g);record.append(dict(path=name,before_sha256=hashlib.sha256(b).hexdigest(),restored_git_blob=header[0].decode(),after_sha256=hashlib.sha256(g).hexdigest()))
(Path(__file__).parent/'restored_checkout_bytes.json').write_text(json.dumps(dict(reason='CRLF-only working-copy conversion; exact committed bytes restored; modified paths excluded',files=record,research_credit_ns=0),indent=2)+'\n')
print('restored',len(record))
