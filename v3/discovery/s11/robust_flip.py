"""DEVELOPMENT common-source regret oracle; Codex (GPT-6).

Fixed query-cell masses, independent conditional-mean intervals, fixed prices.
Compare exact corner enumeration on small cases; retain a single source witness.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import random
import time

from query_flip import compact_plan, matches, signs, source, unrestricted_plan


def summarize_policy(src, solve, flip_fee, query_fee, H):
    rows = []
    for z in src['cells']:
        h, k, fee = (0,)*src['r'], H, F(0)
        while True:
            action = solve(h, k)[1]
            if action[0] == 'query':
                j = action[1]
                fee += query_fee[j]
                h = tuple(z[t] if t == j else h[t] for t in range(src['r']))
                k -= 1
            else:
                s = [0]*src['m']
                if action[0] == 'terminal_1':
                    chosen = action[1]
                    s = [-1 if i in chosen else 1 for i in range(src['m'])]
                    fee += sum((flip_fee[i] for i in chosen), F(0))
                rows.append((fee, tuple(s)))
                break
    return rows


def point_source(src, means):
    return {**src, 'moments': [[p*x for x in row] for p, row in zip(src['mass'], means)]}


def policy_value(src, rows, weights, means):
    return sum((p*(fee + sum((w*s*x for w,s,x in zip(weights, coeff, z+tuple(mu))), F(0)))
                for z,p,(fee,coeff),mu in zip(src['cells'],src['mass'],rows,means)), F(0))


def independent_law(src, means):
    law = {}
    for z,p,mu in zip(src['cells'],src['mass'],means):
        for y in signs(src['m']-src['r']):
            probability = p
            for yi, mi in zip(y,mu):
                probability *= (1+yi*mi)/2
            if probability:
                law[z+y] = probability
    assert sum(law.values()) == 1
    return law


def regret_oracle(src, rows, weights, flip_fee, query_fee, H, box):
    m, r = src['m'], src['r']
    counts = dict(contexts=0, support_terms=0, flip_keys_sorted=0, query_options=0)

    @lru_cache(None)
    def leaf(h):
        counts['contexts'] += 1
        ids = [t for t,z in enumerate(src['cells']) if matches(z,h)]
        mass = sum((src['mass'][t] for t in ids),F(0))
        common_fee = sum((src['mass'][t]*rows[t][0] for t in ids),F(0))
        W = {s:[F(0)]*m for s in (-1,0,1)}
        for t in ids:
            z,p = src['cells'][t],src['mass'][t]
            for s in (-1,0,1):
                for i in range(m):
                    c = weights[i]*(rows[t][1][i]-s)
                    val = c*z[i] if i < r else max(c*box[t][i-r][0],c*box[t][i-r][1])
                    W[s][i] += p*val
                    counts['support_terms'] += 1
        return mass, common_fee, W

    @lru_cache(None)
    def solve(h,k):
        mass, fee, W = leaf(h)
        best, action = fee+sum(W[0]), ('terminal_0',)
        gains = sorted(((W[-1][i]-W[1][i]-flip_fee[i]*mass,i) for i in range(m)),reverse=True)
        counts['flip_keys_sorted'] += m
        chosen = tuple(i for gain,i in gains[:k] if gain>0)
        stopping = fee+sum(W[1])+sum((gain for gain,i in gains[:k] if gain>0),F(0))
        if stopping > best:
            best,action = stopping, ('terminal_1',chosen)
        if k:
            for j in range(r):
                if h[j]:
                    continue
                counts['query_options'] += 1
                total = -query_fee[j]*mass
                for o in (-1,1):
                    child = tuple(o if i==j else h[i] for i in range(r))
                    total += solve(child,k-1)[0]
                if total > best:
                    best,action = total, ('query',j)
        return best,action

    value,action = solve((0,)*r,H)
    adversary_rows = summarize_policy(src,solve,flip_fee,query_fee,H)
    witness = []
    for t in range(len(src['cells'])):
        row = []
        for i in range(r,m):
            c = weights[i]*(rows[t][1][i]-adversary_rows[t][1][i])
            lo,hi = box[t][i-r]
            row.append(hi if c>0 else lo)
        witness.append(row)
    assert policy_value(src,rows,weights,witness)-policy_value(src,adversary_rows,weights,witness) == value
    return value, action, witness, adversary_rows, counts


def case(index):
    large = index >= 8
    m,r,H = (101,4,6) if large else ((4,2,2) if index==7 else (3,1,1+index%3))
    src = source(m,r,700+index)
    rng = random.Random(900+index)
    weights = tuple(F(rng.choice((-2,-1,1,2))) for _ in range(m))
    flip_fee = tuple(F(rng.randrange(1,5),4) for _ in range(m))
    query_fee = (F(1,8),)*r
    nominal = [[x/p for x in row] for p,row in zip(src['mass'],src['moments'])]
    plan = compact_plan(src,weights,flip_fee,query_fee,H)
    rows = summarize_policy(src,plan[4],flip_fee,query_fee,H)
    if index in (0,8):
        # A legal fallible proposal that declines every intervention.
        rows = [(F(0),(0,)*m) for _ in src['cells']]
    box = [[(max(F(-1),mu-F(rng.randrange(1,4),4)), min(F(1),mu+F(rng.randrange(1,4),4)))
            for mu in row] for row in nominal]
    if index == 1:
        box = [[(mu,mu) for mu in row] for row in nominal]
    start = time.perf_counter_ns()
    bound, action, witness, adversary, counts = regret_oracle(src,rows,weights,flip_fee,query_fee,H,box)
    elapsed = time.perf_counter_ns()-start
    opt = compact_plan(point_source(src,witness),weights,flip_fee,query_fee,H)[0]
    assert policy_value(src,rows,weights,witness)-opt == bound
    assert bound >= 0
    corner_count, unrestricted_count = 0,0
    corner_max = None
    if not large:
        endpoints = [tuple(sorted(set(pair))) for row in box for pair in row]
        for values in product(*endpoints):
            mu = [list(values[t*(m-r):(t+1)*(m-r)]) for t in range(2**r)]
            candidate_value = policy_value(src,rows,weights,mu)
            corner_opt = compact_plan(point_source(src,mu),weights,flip_fee,query_fee,H)[0]
            if index in (0,2,5):
                unrestricted_value,_ = unrestricted_plan(independent_law(src,mu),weights,flip_fee,query_fee,H)
                assert unrestricted_value == corner_opt
                unrestricted_count += 1
            regret = candidate_value-corner_opt
            corner_max = regret if corner_max is None else max(corner_max,regret)
            corner_count += 1
        assert corner_max == bound, (index,corner_max,bound)
    tighter = [[((lo+mu)/2,(hi+mu)/2) for (lo,hi),mu in zip(row,mus)] for row,mus in zip(box,nominal)]
    tight_bound = regret_oracle(src,rows,weights,flip_fee,query_fee,H,tighter)[0]
    assert tight_bound <= bound
    extreme = all(all(abs(s)==1 for s in row[1]) for row in rows)
    induced = None
    if extreme:
        worst = [[hi if weights[i+r]*rows[t][1][i+r]>0 else lo for i,(lo,hi) in enumerate(row)] for t,row in enumerate(box)]
        induced_opt = compact_plan(point_source(src,worst),weights,flip_fee,query_fee,H)[0]
        induced = policy_value(src,rows,weights,worst)-induced_opt
        assert induced == bound
    return {'case':index,'m':m,'r':r,'horizon':H,'regret':str(bound),'refined_regret':str(tight_bound),
            'corner_count':corner_count,'unrestricted_corner_checks':unrestricted_count,
            'ordinary_induced_scenario_applicable':extreme,'induced_regret':None if induced is None else str(induced),
            'root_adversary_action':action,'counts':counts,'elapsed_ns':elapsed,
            'zero_terminal_cells':sum(all(s==0 for s in row[1]) for row in rows),
            'mass':list(map(str,src['mass'])),'weights':list(map(str,weights)),
            'flip_fee':list(map(str,flip_fee)),'query_fee':list(map(str,query_fee)),
            'proposal':[{'fee':str(fee),'coefficients':s} for fee,s in rows],
            'box':[[[str(lo),str(hi)] for lo,hi in row] for row in box],
            'witness':[[str(x) for x in row] for row in witness],
            'adversary':[{'fee':str(fee),'coefficients':s} for fee,s in adversary],
            'scope':'Exact fixed-policy box regret; source acquisition and global minimax policy design excluded.'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',type=int,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    assert not args.out.exists()
    result=case(args.case)
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['planner_sha256']=hashlib.sha256(Path(__file__).with_name('query_flip.py').read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('box','witness','proposal','adversary','mass','weights','flip_fee','query_fee')}))


if __name__=='__main__':
    main()
