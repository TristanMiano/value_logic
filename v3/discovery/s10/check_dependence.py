from pathlib import Path
from fractions import Fraction as F
import json
ROOT=Path(__file__).resolve().parent/"dep01"
data=json.loads((ROOT/"results.json").read_text());D=24001;P=[9000,9000,6001];Q=6
upper=[];independent=[];perfect=[];dist=[F(1)]+[F(0)]*Q;negatives=0
def check(row):
    k=row["k"];weights=[F(*x["weight"]) for x in row["primal"]];states=[x["state"] for x in row["primal"]]
    assert all(w>=0 for w in weights) and sum(weights)==1
    assert all(a>=0 and b>=0 and a+b<=k for a,b in states)
    assert sum(w*s[0] for w,s in zip(weights,states))==F(k*P[1],D)
    assert sum(w*s[1] for w,s in zip(weights,states))==F(k*P[2],D)
    objective=sum(w for w,s in zip(weights,states) if s[0]+2*s[1]<Q)
    a,b,c=map(lambda v:F(*v),row["dual"])
    for i in range(k+1):
        for j in range(k-i+1): assert a+b*i+c*j>=int(i+2*j<Q)
    assert objective==a+b*F(k*P[1],D)+c*F(k*P[2],D)==F(*row["upper"])
for row in data["rows"]:
    check(row);k=row["k"];upper.append(F(*row["upper"]));independent.append(1-dist[Q]);perfect.append(sum(F(P[s],D) for s in range(3) if k*s<Q))
    assert independent[-1]<=upper[-1] and perfect[-1]<=upper[-1]
    bad=json.loads(json.dumps(row));bad["dual"][0]=[-1,1]
    try: check(bad)
    except AssertionError: negatives+=1
    else: raise AssertionError('accepted invalid plane')
    next=[F(0)]*(Q+1)
    for s,prob in enumerate(dist):
        for t,p in enumerate(P):next[min(Q,s+t)]+=prob*F(p,D)
    dist=next
assert all(upper[i]>=upper[i+1] for i in range(12))
schedules={"unit":[1]*12,"alternating":[1,2]*6,"sorted123":[1]*4+[2]*4+[3]*4};comparisons=[]
def enc(x):return [x.numerator,x.denominator]
for name,fees in schedules.items():
    for C in [12,24,48]:
        rows=[]
        for k in range(13):
            if sum(fees[:k])>C:continue
            robust=sum(fees[j]*upper[j] for j in range(k))+C*upper[k]
            product=sum(fees[j]*independent[j] for j in range(k))+C*independent[k]
            correlated=sum(fees[j]*perfect[j] for j in range(k))+C*perfect[k]
            rows.append({"length":k,"robust":enc(robust),"product":enc(product),"perfect_correlation":enc(correlated)})
        best=min(rows,key=lambda r:F(*r["robust"]));naive=min(rows,key=lambda r:F(*r["product"]))
        comparisons.append({"schedule":name,"C":C,"rows":rows,"robust_choice":best,"product_choice":naive})
result={"status":"pass","certificates":len(upper),"negative_controls":negatives,"comparisons":comparisons,"compiled_named_units":data["named_units"],"scope":"Exact count-marginal primal/dual bounds; prefix invoice is conservative and may not be jointly sharp; no paid streams."}
(ROOT/"checked.json").write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({**result,"comparisons":[{k:v for k,v in row.items() if k!='rows'} for row in comparisons]},indent=2))
