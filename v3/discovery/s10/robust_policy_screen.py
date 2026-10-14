from pathlib import Path
from fractions import Fraction as F
import json,hashlib
root=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def encode(x):return [x.numerator,x.denominator]
P=[9000,9000,6001];D=sum(P)
def survival(k,Q):
    if Q<=0:return F(0)
    if Q>2*k:return F(1)
    h=Q-1;x=F(k*P[1],D);y=F(k*P[2],D)
    values=[F(1),(2*k-x-2*y)/(2*k-h),(k-y)/(k-h//2)]
    if h<k:values.append((k-x-y)/(k-h))
    return min(values)
rows=[]
for case in read(root/'sf01/design.json')['cases']:
    if case['stratum']!='near6':continue
    setup=read(root/'sf01'/case['name']/'scalar_prefix/setup.json');a=setup['initial']['a'];Q=setup['quota'];C=setup['C'];queries=setup['queries'];fees=setup['fees']
    order=sorted((i for i,q in enumerate(queries) if a[q['coordinate']] in (1,2)),key=lambda i:(fees[i],i))
    best=F(0 if Q==0 else C);chosen=[];paid=F(0);spent=0;certificates=[];units=12+len(order)**2+len(order)
    for k,index in enumerate(order,1):
        if spent+fees[index]>C:break
        spent+=fees[index];paid+=fees[index]*survival(k-1,Q);upper=paid+C*survival(k,Q);units+=100
        if upper<best:best=upper;chosen=order[:k]
        certificates.append({'length':k,'upper':encode(upper),'survival':encode(survival(k,Q)),'listed_fee':spent})
    original=setup['policy'];product=F(int(original['numerator']),int(original['denominator'])) if 'numerator' in original else None
    rows.append({'source':case['name'],'quota':Q,'fallback_fee':C,'robust_upper':encode(best),'selected_queries':chosen,'named_compile_units':units,'certificates':certificates,'original_product_policy':original,'actual_new_purchases':0,'scope':'Analytical policy compilation on an already exposed source duty; predicted fees are not measured purchases.'})
result={'status':'complete','contributor':'Codex (GPT-6)','source_hash':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'rows':rows,'duties':len(rows),'nontrivial_duties':sum(r['quota']>0 for r in rows),'nontrivial_strict_fee_bounds':sum(r['quota']>0 and F(*r['robust_upper'])<r['fallback_fee'] for r in rows),'compile_units':sum(r['named_compile_units'] for r in rows),'physical_acquisitions':0}
(root/'robust_policy_screen.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}));print([(r['source'],r['fallback_fee'],len(r['selected_queries']),round(float(F(*r['robust_upper'])),4)) for r in rows if r['quota']>0])
