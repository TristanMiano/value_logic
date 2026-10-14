from pathlib import Path
from fractions import Fraction as F
import json
root=Path(__file__).resolve().parent
def bound(k,Q,P):
    D=sum(P);planes=[(F(1),F(0),F(0))]
    if 2*k-Q+1>0:
        d=2*k-Q+1;planes.append((F(2*k,d),F(-1,d),F(-2,d)))
    if k-Q+1>0:
        d=k-Q+1;planes.append((F(k,d),F(-1,d),F(-1,d)))
    if k-(Q-1)//2>0:
        d=k-(Q-1)//2;planes.append((F(k,d),F(0),F(-1,d)))
    best=min(planes,key=lambda c:c[0]+c[1]*F(k*P[1],D)+c[2]*F(k*P[2],D))
    return best[0]+best[1]*F(k*P[1],D)+best[2]*F(k*P[2],D),best,12+len(planes)*16
rows=[];equal=0;units=0;diagnostic=0;worst=F(0)
for line in (root/'dep03/certificates.jsonl').read_text().splitlines():
    item=json.loads(line);k,Q,P=item['k'],item['Q'],item['P'];value,plane,cost=bound(k,Q,P);exact=F(*item['upper']);assert value>=exact
    if value==exact:equal+=1
    for a in range(k+1):
        for b in range(k-a+1):
            assert plane[0]+plane[1]*a+plane[2]*b>=int(a+2*b<Q);diagnostic+=8
    units+=cost;worst=max(worst,value-exact)
    rows.append({'k':k,'Q':Q,'P':P,'upper':[value.numerator,value.denominator],'exact':item['upper'],'plane':[[x.numerator,x.denominator] for x in plane],'named_units':cost})
result={'status':'pass','contributor':'Codex (GPT-6)','certificates':len(rows),'exact_equalities':equal,'strictly_looser':len(rows)-equal,'max_additive_gap':[worst.numerator,worst.denominator],'formula_units':units,'independent_global_plane_check_units':diagnostic,'scope':'Post-exposure explanatory formula comparison, not an independent confirmation or new paid stream.','rows':rows}
(root/'cheap_dependence.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
