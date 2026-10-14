from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
import dependence_hull as h
root=Path(__file__).resolve().parent
out=root/'dep03';out.mkdir()
files=['dependence_hull.py','check_dep_hulls.py','dependence_hulls.md']
(out/'design.json').write_text(json.dumps({'contributor':'Codex (GPT-6)','created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'stage':'DEVELOPMENT','quotas':list(range(1,13)),'lengths':list(range(1,33)),'marginals':[[9000,9000,6001],[1,1,1],[8,1,1]],'hashes':{f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
for f in files:(out/f).write_bytes((root/f).read_bytes())
diagnostic=0
def check(row,P,Q):
    global diagnostic
    D=sum(P);k=row['k'];primal=row['primal'];weights=[F(*r['weight']) for r in primal]
    assert sum(weights)==1 and all(w>=0 for w in weights)
    assert all(a>=0 and b>=0 and a+b<=k for a,b in (r['state'] for r in primal))
    assert sum(w*r['state'][0] for w,r in zip(weights,primal))==F(k*P[1],D)
    assert sum(w*r['state'][1] for w,r in zip(weights,primal))==F(k*P[2],D)
    primal_value=sum(w for w,r in zip(weights,primal) if r['state'][0]+2*r['state'][1]<Q)
    a,b,c=[F(*v) for v in row['dual']]
    for i in range(k+1):
        for j in range(k-i+1):
            assert a+b*i+c*j>=int(i+2*j<Q)
            diagnostic+=8
    assert primal_value==F(*row['upper'])==a+b*F(k*P[1],D)+c*F(k*P[2],D)
    diagnostic+=40+20*len(primal)
before=json.loads((root/'dep01/results.json').read_text());after=json.loads((root/'dep02/results.json').read_text())
for a,b in zip(before['rows'],after['rows']):
    check(b,h.P,h.Q);assert F(*a['upper'])==F(*b['upper'])
rows=[]
with (out/'certificates.jsonl').open('w') as f:
    for P in [(9000,9000,6001),(1,1,1),(8,1,1)]:
        h.P=P;h.D=sum(P)
        for Q in range(1,13):
            h.Q=Q
            for k in range(1,33):
                row=h.solve(k);check(row,P,Q);record={'P':P,'Q':Q,**row};f.write(json.dumps(record)+'\n');rows.append(record)
        print('complete',P,flush=True)
result={'status':'pass','certificates':len(rows),'dep02_equalities':13,'dep01_compile_units':before['named_units'],'dep02_compile_units':after['named_units'],'dep03_compile_units':sum(r['named_units'] for r in rows),'diagnostic_units':diagnostic,'physical_acquisitions':0,'scope':'Compiler comparison and exact global moment-certificate checking; no complete-cost or paid-service claim.'}
(out/'checked.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
