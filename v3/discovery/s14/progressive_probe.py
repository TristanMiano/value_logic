"""One-defect audit screen; Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import time

out=Path(__file__).with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()
panels=[]
choices=0
for g in (1,3,7):
    H=g+1
    best={a:None for a in range(1,g+1)}
    # Before the first hit every observation is negative. Its deterministic
    # query order is represented by a word of target/non-target classes.
    for target_pattern in range(1,2**g):
        a=target_pattern.bit_count()
        last=target_pattern.bit_length()
        for labels in range(2**H):
            choices+=1
            nxt={0:[None]*(H+2),1:[None]*(H+2)}
            for b in (0,1):
                for t in range(H,0,-1):
                    nxt[b][t]=t if (labels>>(t-1))&1==b else nxt[b][t+1]
            endpoints=[nxt[(target_pattern>>(j-1))&1][j]
                       for j in range(1,last+1)]
            final=nxt[0][last]
            if final is None or any(x is None for x in endpoints):
                continue
            total=sum(endpoints)+(g+1-last)*final
            q=F(total,g+1)
            best[a]=q if best[a] is None else min(best[a],q)
    rows=[]
    for a in range(1,g+1):
        expected=a-F(a*(a-1),2*(g+1))+F(1,g+1)
        assert best[a]==expected
        total=0
        for defect in range(g+1):
            if 1<=defect<a:
                count=defect
            elif defect==a:
                count=a+1
            else:
                count=a
            decoded=count!=a
            assert decoded==(1<=defect<=a)
            total+=count
        assert F(total,g+1)==expected
        rows.append({'support':a,'optimal_queries':expected,
                     'zero_query_bayes_error':F(min(a,g+1-a),g+1)})
    panels.append({'g':g,'rows':rows})

refinements=[]
for r in (3,4,5,6):
    g=2**r-1
    k=g-r
    lossy=g+F(2**k-1,2)
    repair=F(g+2,2)
    direct=k+F(2**k-1,2)+r+F(2**r-1,2)
    assert lossy+repair==direct+1
    assert g+1<=g+2**k-1
    assert k+2**k-1<=g+2**k-1
    assert r+2**r-1<=g+2**k-1
    refinements.append({'r':r,'g':g,'lossy_queries':lossy,
                        'exact_repair_queries':repair,'two_prefix_queries':direct,
                        'extra_queries_at_exact_completion':1})
result={'status':'PASS','contributor':'Codex (GPT-6)',
        'scope':'enumerated class-order/count-label choices for g=1,3,7; exact refinement formulas',
        'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
        'choices_examined':choices,'panels':panels,'refinements':refinements,
        'ordinary_equivalent':'identical conventional query/readout algorithms tie',
        'complete_cost_or_cpu_gain':False,'elapsed_ns':time.perf_counter_ns()-clock,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2,default=str))
