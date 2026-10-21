"""Exact binary-channel screen; expected under5s, no execution-cost claim."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import random
import time

HERE=Path(__file__).resolve().parent


def risk(channel,prior,loss):
    return sum(min(sum(prior[s]*channel[s][j]*row[s] for s in range(2))
                   for row in loss) for j in range(len(channel[0])))


def main():
    began=time.perf_counter_ns()
    rng=random.Random(2026102104)
    rows=[tuple(map(lambda x:F(x,4),(a,b,4-a-b)))
          for a in range(5) for b in range(5-a)]
    losses=[[(0,1),(1,0)],[(0,3),(2,0),(1,1)]]
    losses += [[tuple(rng.randrange(9) for _ in range(2)) for _ in range(4)]
               for _ in range(8)]
    counts=dict(channels=0,q_zero=0,q_one=0,strictly_partial=0,
                kernel_entries=0,bayes_risk_checks=0,strict_risk_improvements=0)
    for plus in rows:
        for minus in rows:
            a=[min(p,m) for p,m in zip(plus,minus)]
            q=1-sum(a)
            null=(a if q==1 else [x/(1-q) for x in a])
            if q==1:
                null=[F(1),F(0),F(0)]
            reveal=[]
            for row in (plus,minus):
                reveal.append([(x-z)/q for x,z in zip(row,a)] if q else
                              [F(1),F(0),F(0)])
            assert all(x>=0 for row in [null]+reveal for x in row)
            assert all(sum(row)==1 for row in [null]+reveal)
            erasure=[[1-q,q,0],[1-q,0,q]]
            kernel=[null]+reveal
            for s,row in enumerate((plus,minus)):
                for j,value in enumerate(row):
                    assert sum(erasure[s][k]*kernel[k][j] for k in range(3))==value
                    counts['kernel_entries']+=1
            for p in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
                prior=[p,1-p]
                for loss in losses:
                    old=risk([plus,minus],prior,loss)
                    new=risk(erasure,prior,loss)
                    no=risk([[1],[1]],prior,loss)
                    full=risk([[1,0],[0,1]],prior,loss)
                    assert new==(1-q)*no+q*full
                    assert new<=old<=no
                    counts['bayes_risk_checks']+=1
                    counts['strict_risk_improvements']+=new<old
            counts['channels']+=1
            counts['q_zero']+=q==0
            counts['q_one']+=q==1
            counts['strictly_partial']+=0<q<1
    result=dict(status='PASS',contributor='Codex (GPT-6)',seed=2026102104,
                counts=counts,elapsed_ns=time.perf_counter_ns()-began,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='finite ordinary garbling/decision identities; invoice price theorem not retested')
    (HERE/'frontier_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':
    main()
