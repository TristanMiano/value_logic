"""Administrative byte preservation, manifest and closure checks; no research."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='131f534c55cbd2b366074e255d4075e08e0b0933'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))

# Preserve established newline conventions of mutable pointers; old source files
# are not edited. Newly written JSON values can otherwise produce mixed endings.
for name in ('TODO_v3.md','v3/claim_ledger.md','v3/discovery/CONTINUE.md',
             'v3/discovery/P3_SEARCH_01.md','v3/discovery/candidates.md',
             'v3/discovery/recurrences.json','v3/discovery/recurrences.md','v3/plan.v1.json'):
    p=ROOT/name
    original=subprocess.check_output(['git','show',f'{BASE}:{name}'],cwd=ROOT)
    current=p.read_bytes()
    if name.endswith('recurrences.md'):
        current=current.replace(b'\r\n',b'\n')
        current=current.replace(b'\n\n| **[s11 four-hour round]',b'\n| **[s11 four-hour round]')
    if b'\r\n' in original and b'\n' not in original.replace(b'\r\n',b''):
        current=current.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
    elif b'\r\n' not in original:
        current=current.replace(b'\r\n',b'\n')
    p.write_bytes(current)

old_bytes=subprocess.check_output(['git','show',f'{BASE}:v3/discovery/recurrences.json'],cwd=ROOT)
new_bytes=(HERE.parent/'recurrences.json').read_bytes()
old=json.loads(old_bytes); new=json.loads(new_bytes)
assert len(new['rows'])==21 and new['rows'][:20]==old['rows']
# Compare each historic row's exact serialization, not just its decoded value.
def row_bytes(data):
    text=data.decode('utf-8'); decoder=json.JSONDecoder()
    pos=text.index('"rows":')+len('"rows":')
    pos=text.index('[',pos)+1; result=[]
    while True:
        while text[pos].isspace() or text[pos]==',': pos+=1
        if text[pos]==']': return result
        _,end=decoder.raw_decode(text,pos)
        result.append(text[pos:end].encode('utf-8'));pos=end
assert row_bytes(old_bytes)==row_bytes(new_bytes)[:20]
old_md=subprocess.check_output(['git','show',f'{BASE}:v3/discovery/recurrences.md'],cwd=ROOT)
rows=[line for line in old_md.splitlines() if line.startswith(b'|')]
assert len(rows)==22
assert all(line in (HERE.parent/'recurrences.md').read_bytes().splitlines() for line in rows)
old_ledger=subprocess.check_output(['git','show',f'{BASE}:v3/time_ledger.csv'],cwd=ROOT)
assert (ROOT/'v3/time_ledger.csv').read_bytes().startswith(old_ledger)
a=read(HERE/'effective_actuals.json')
assert sum(r['research_ns'] for r in new['rows'])==a['program_research_ns']
assert a['phase_research_ns']==a['program_research_ns']+a['historical_phase_ns']
assert new['rows'][-1]['time_evidence']['sha256']==sha((HERE/'effective_actuals.json').read_bytes())
assert sha((HERE/'actuals.json').read_bytes())==read(HERE/'clock_recovery.json')['old_actuals_sha256']

excluded={'manifest.json','publication.md','prepare_evidence.py'}
records=[]
for p in sorted(HERE.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(HERE)
    if rel.parts[0] in ('pub','__pycache__') or '__pycache__' in rel.parts: continue
    if rel.as_posix() in excluded or p.suffix in ('.tmp','.pyc'): continue
    b=p.read_bytes();records.append(dict(path=rel.as_posix(),bytes=len(b),sha256=sha(b)))
manifest=dict(contributor='Codex (GPT-6)',status='development_closure_not_confirmation',
              base_commit=BASE,scope='Scientific source, declarations, results, all failed logs and both clocks. Administrative reports are included where immutable at closure.',
              excluded='Manifest itself, mutable publication metadata, this administrative generator, pub check logs/receipts, Python caches and ephemeral control.tmp files.',
              files=records)
out=HERE/'manifest.json'
if out.exists(): assert read(out)==manifest, 'Do not silently replace an existing closing manifest.'
else: out.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(historical_rows_byte_preserved=20,old_ledger_prefix_preserved=True,program_research_ns=a['program_research_ns'],manifest_files=len(records),manifest_bytes=sum(r['bytes'] for r in records)),indent=2))
