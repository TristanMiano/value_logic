"""Reconstruct existing direct-LP advice without re-solving or new exposure."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
from query_flip import signs
from direct_lp import build
from lp_certificate import lower_bound

root=Path(__file__).resolve().parent
results=[]
for index in range(4):
    oldpath=root/'dl01'/('c%02da0.json'%index);old=json.loads(oldpath.read_text())
    inp=root/old['input'];data=json.loads(inp.read_text())
    assert hashlib.sha256(inp.read_bytes()).hexdigest()==old['input_sha256']
    m,r,H=data['m'],data['r'],data['H']
    src={'m':m,'r':r,'cells':signs(r),'mass':list(map(F,data['mass']))}
    w,f,q=(tuple(map(F,data[key])) for key in ('weights','flip_fee','query_fee'))
    box=[[(F(lo),F(hi)) for lo,hi in row] for row in data['box']]
    _,eq,beq,ub,bub,bounds,c,_=build(src,w,f,q,H,box)
    raw=old['raw_dual_advice']
    L,certificate=lower_bound(eq,beq,ub,bub,bounds,c,raw['lambda'],raw['nu'])
    U=F(old['upper']);assert L<=U
    results.append({'case':index,'input':oldpath.relative_to(root).as_posix(),
                    'input_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),
                    'lower':str(L),'upper':str(U),'gap':str(U-L),'certificate':certificate})
    print(json.dumps({'case':index,'lower':float(L),'upper':float(U),'gap':float(U-L),'lower_bits':certificate['bound_bits']}))
result={'cases':results,'scope':'Common-grid exact reconstruction of existing advice; no LP rerun.',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependencies':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ('direct_lp.py','lp_certificate.py','policy_flow.py')}}
with (root/'dl01_grid.json').open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
