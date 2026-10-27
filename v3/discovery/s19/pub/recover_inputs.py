"""Recover only deterministic input bytes from two frozen generators.

Administration/identity check: no policy, proof machine, test or result is rerun.
The stored input digests predate this publication-time materialization.
"""
import ast
import hashlib
import json
from pathlib import Path

H=Path(__file__).resolve().parent.parent
for stem,stop,var in [('proof_credit','worst','cases'),('proof_machine','costs','schedules')]:
 source=H/(stem+'_check.py');tree=ast.parse(source.read_text())
 main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
 cut=next(i for i,n in enumerate(main.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==stop for t in n.targets))
 main.body=main.body[:cut]+[ast.Return(value=ast.Name(id=var,ctx=ast.Load()))]
 tree.body=[n for n in tree.body if not isinstance(n,ast.If)]
 ast.fix_missing_locations(tree)
 ns={'__name__':'input_identity_only','__file__':str(source)}
 exec(compile(tree,str(source),'exec'),ns)
 blob=json.dumps(ns['serial'](ns['main']()),sort_keys=True,separators=(',',':')).encode()
 result=json.loads((H/(stem+'_result.json')).read_text())
 assert hashlib.sha256(blob).hexdigest()==result['input_sha256']
 target=H/(stem+'_inputs.json')
 if target.exists():assert target.read_bytes()==blob
 else:target.write_bytes(blob)
 print(stem,len(blob),result['input_sha256'])
