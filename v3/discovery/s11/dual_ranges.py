"""Cheap range/measurement screen, not an empirical calibration trial."""
from pathlib import Path
from fractions import Fraction as F
import json
import math

root=Path(__file__).resolve().parent
records=[]
paths=sorted((root/'if01').glob('c*.json'))+sorted((root/'if02').glob('c12*.json'))+ [root/'if02'/'c13_upper_only.json']
for path in paths:
    record=json.loads(path.read_text(encoding='utf-8'))
    cert=record.get('compact',record.get('proposal'))
    prices=[[F(x) for x in row] for row in cert['prices']]
    ranges=[max(row)-min(row) for row in prices]
    R=sum(ranges,F(0))
    fees=list(map(F,record['fees']))
    average_fee=sum((r*c for r,c in zip(ranges,fees)),F(0))/R if R else F(0)
    C=F(record['fallback'])
    U=F(cert['upper'])
    margin=C-U
    # Prospective precision example only: half the currently predicted margin.
    eps=margin/2
    N=math.ceil(float(R*R/(2*eps*eps))*math.log(20)) if eps>0 and R else None
    records.append({'path':path.relative_to(root).as_posix(),'n':record['n'],'R':str(R),
                    'positive_ranges':sum(r>0 for r in ranges),'upper':str(U),'fallback':str(C),
                    'margin':str(margin),'importance_average_fee':str(average_fee),
                    'delta':0.05,'precision_half_margin':str(eps) if eps>0 else None,
                    'fixed_N_sufficient':N,'calibration_fee_bound':None if N is None else str(N*average_fee)})
out={'contributor':'Codex (GPT-6)','scope':'Range-based fixed-horizon calibration forecast; no samples drawn or bills paid. Requires stationary expectation for future-use interpretation.','records':records}
with (root/'dual_ranges.json').open('x',encoding='utf-8',newline='\n') as f:
    f.write(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
