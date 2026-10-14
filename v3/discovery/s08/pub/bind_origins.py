"""Bind the original namespaces of three executed declaration copies."""
from pathlib import Path
import json,hashlib,sys
root=Path(__file__).resolve().parents[4];sys.path.insert(0,str(root))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
pairs=[('aa01','action_audits.md'),('dr01','decision_regions.md'),('gf01','nominal_bank.md')];records=[]
for run,name in pairs:
 stored=root/'v3/discovery/s08'/run/'declaration.md';origin=root/'v3/discovery/s08'/name
 assert stored.read_text(encoding='utf-8').replace('\\operatorname{','\\mathrm{')==origin.read_text(encoding='utf-8').replace('\\operatorname{','\\mathrm{')
 records.append(dict(path=origin.relative_to(root).as_posix(),sha256=sha(stored),stored_path=stored.relative_to(root).as_posix(),live_sha256=sha(origin),verification='Exact text match after documented operator-macro normalization; original relative namespace retained.'))
record=root/'v3/discovery/s08/pub/origin_bindings.json';save(record,dict(contributor='Codex (GPT-6)',research_credit_ns=0,files=records))
p=root/'tools/document_origins.json';doc=json.loads(p.read_text(encoding='utf-8'))
for i,r in enumerate(records):
 assert not any(x['stored_path']==r['stored_path'] for x in doc['entries'])
 doc['entries'].append(dict(stored_path=r['stored_path'],sha256=r['sha256'],origin_path=r['path'],provenance=[dict(path=record.relative_to(root).as_posix(),sha256=sha(record),pointer=['files',i],kind='record:path:sha256')],basis='Executed declaration copy; closing binding checks its original source namespace while preserving raw scientific bytes.'))
save(p,doc)
from verification.math_views import view_text,origins_for
mp=root/'tools/math_views.json';m=json.loads(mp.read_text(encoding='utf-8'));entry=next(x for x in m['entries'] if x['view_path']=='docs/math/s08_aa01.md')
(root/entry['view_path']).write_bytes(view_text(root,entry['source_path'],entry['view_path'],origins_for(root)).encode('utf-8'));entry['view_sha256']=sha(root/entry['view_path']);save(mp,m)
print('bound',len(records),'declaration namespaces; rederived aa01 view')
