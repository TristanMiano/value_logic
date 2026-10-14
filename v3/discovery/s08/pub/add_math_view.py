"""Preserve the executed aa01 declaration; add its mechanically derived view."""
from pathlib import Path
import sys,json,hashlib
root=Path(__file__).resolve().parents[4];sys.path.insert(0,str(root))
from verification.math_views import view_text,origins_for
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
source='v3/discovery/s08/aa01/declaration.md';design=root/'v3/discovery/s08/aa01/design.json'
assert sha(root/source)==json.loads(design.read_text())['declaration_sha256']
record=root/'v3/discovery/s08/pub/declaration_binding.json'
save(record,dict(contributor='Codex (GPT-6)',scope='Executed aa01 scientific declaration preserved at publication',research_credit_ns=0,design_path=design.relative_to(root).as_posix(),design_sha256=sha(design),design_hash_field='declaration_sha256',files=[dict(path=source,sha256=sha(root/source))]))
view='docs/math/s08_aa01.md';content=view_text(root,source,view,origins_for(root)).encode();(root/view).write_bytes(content)
p=root/'tools/math_views.json';doc=json.loads(p.read_text());assert not any(x['source_path']==source for x in doc['entries'])
doc['entries'].append(dict(source_path=source,source_sha256=sha(root/source),view_path=view,view_sha256=sha(root/view),preservation=dict(kind='scientific-record',path=record.relative_to(root).as_posix(),sha256=sha(record),pointer=['files',0],path_pointer=['path'],sha256_pointer=['sha256'],path_base=''),preservation_reason='Actual executed aa01 design declaration hash verified in the closing source binding; raw declaration preserved.'))
save(p,doc);print(source,'->',view)
