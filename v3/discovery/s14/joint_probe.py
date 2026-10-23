"""Exact binary block-completion screen, Codex (GPT-6), DEVELOPMENT."""
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import time

path=Path(__file__)
out=path.with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()

def rank(rows):
    piv={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p in piv:row^=piv[p]
            else:
                piv[p]=row
                break
    return len(piv)

def kernel(rows,n):
    result=set()
    for a in range(1<<len(rows)):
        v=0
        for i,row in enumerate(rows):
            if a>>i&1:v^=row
        if not v:result.add(a)
    return result

groups_checked=matrices_checked=rule_checks=0
for r in range(1,4):
    for n in range(1,4):
        for d in range(r+1):
            for s in range(n+1):
                groups=defaultdict(list)
                for z in range(1<<(r*n)):
                    rows=tuple((z>>(i*n))&((1<<n)-1) for i in range(r))
                    C=tuple(row&((1<<s)-1) for row in rows)
                    Y=rows[:d]
                    groups[(C,Y)].append(rows)
                    matrices_checked+=1
                for (C,Y),completions in groups.items():
                    low=rank(C)+rank(Y)-rank(C[:d])
                    high=min(rank(Y)+r-d,rank(C)+n-s)
                    observed=[rank(rows) for rows in completions]
                    assert min(observed)==low and max(observed)==high
                    common=set(range(1<<r))
                    for rows in completions:common&=kernel(rows,n)
                    if s<n:
                        predicted=kernel(Y,n)  # coefficients in first d rows
                    else:
                        predicted=kernel(C,n)
                    assert common==predicted
                    groups_checked+=1
                    rule_checks+=1

result=dict(status='PASS',attribution='Codex (GPT-6)',started_utc=started,
            ended_utc=datetime.now(timezone.utc).isoformat(),
            elapsed_ns=time.perf_counter_ns()-clock,
            source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            dimensions='1<=r,N<=3; every row/column cutoff including zero',
            completed_matrix_occurrences=matrices_checked,
            distinct_receipt_groups=groups_checked,common_rule_checks=rule_checks,
            scope='Every binary completion in these dimensions only; '
                  'no theorem novelty or acquisition-cost claim.')
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
