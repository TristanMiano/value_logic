"""Exact predeclared branching repair witnesses. Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json


def valid(x):
    return not x[0] or (x[1] and x[2])


def run():
    worlds = [x for x in product((0, 1), repeat=3) if valid(x)]
    def masks(cell, cap):
        return [b for b in product((0, 1), repeat=3) if sum(b) <= cap
                and all(valid(tuple(a^v for a, v in zip(x, b))) for x in cell)]
    root = masks(worlds, 2)
    low = masks([x for x in worlds if x[0] == 0], 1)
    high = masks([x for x in worlds if x[0] == 1], 1)
    assert root == [(0, 0, 0)]
    assert set(low) == {(0, 0, 0), (0, 1, 0), (0, 0, 1)}
    assert set(high) == {(0, 0, 0), (1, 0, 0)}
    def release(x, b):
        return F(0) if b is None else F(sum(2*(a^v)-1 for a, v in zip(x, b)))
    policies = [('root', b) for b in [None]+root]
    policies += [('query', a, b) for a, b in product([None]+low, [None]+high)]
    costs = [[release(x, p[1]) if p[0] == 'root' else
              F(1, 4)+release(x, p[1+x[0]]) for x in worlds] for p in policies]
    assert len(policies) == 14
    benchmark = [min(row[i] for row in costs) for i in range(5)]
    assert benchmark == [F(-3), F(-11,4), F(-11,4), F(-3,4), F(0)]
    gaps = [[row[i]-benchmark[i] for i in range(5)] for row in costs]
    weights = [F(0)]*14
    weights[policies.index(('root', (0,0,0)))] = F(7,12)
    for b in [(0,1,0),(0,0,1)]:
        weights[policies.index(('query', b, None))] = F(5,24)
    primal = [sum(w*row[i] for w,row in zip(weights,gaps)) for i in range(5)]
    assert primal == list(map(lambda a:F(a,48), [45,89,89,49,89]))
    dual = [F(0),F(11,24),F(11,24),F(0),F(1,12)]
    dual_costs = [sum(a*b for a,b in zip(dual,row)) for row in gaps]
    assert min(dual_costs) == max(primal) == F(89,48)
    nq_primal = [F(5,16)*gaps[0][i]+F(11,16)*gaps[1][i] for i in range(5)]
    nq_dual = [F(0),F(3,8),F(3,8),F(0),F(1,4)]
    assert max(nq_primal) == min(sum(a*b for a,b in zip(nq_dual,row))
                                   for row in gaps[:2]) == F(33,16)
    return dict(contributor='Codex (GPT-6)', status='DEVELOPMENT_PASS',
                worlds=worlds, policies=len(policies), benchmark=list(map(str,benchmark)),
                full_regrets=list(map(str,primal)), dual_policy_values=list(map(str,dual_costs)),
                full_optimum='89/48', no_query_optimum='33/16', reduction_fraction='10/99',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',type=int,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    assert args.case == 0 and not args.out.exists()
    result=run()
    args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
