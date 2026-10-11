"""DEVELOPMENT: rational minimax actions with weighted-MaxSAT separation.

Codex (GPT-6), 2026-10-11. Exactness of deployed upper bounds trusts RC2 and
its native solver; tiny instances are independently enumerated as a probe.
All timings/counters are priced search observations, not a polynomial claim.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
from math import lcm
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'s01'))
if os.environ.get('VL_SAT_DEPS'):
    sys.path.insert(0, os.environ['VL_SAT_DEPS'])
from region_probe import minmax
from pysat.formula import WCNF
from pysat.examples.rc2 import RC2
from pysat.solvers import Minisat22


def compatible(x, clauses):
    return all(any(x[abs(lit)-1] == int(lit > 0) for lit in c) for c in clauses)


def loss(x, actions):
    return tuple(F(b)+sum(w*bit for w,bit in zip(weights,x)) for b,weights in actions)


def row(x, actions):
    values = loss(x, actions)
    return tuple(v-min(values) for v in values)


def initial_model(n, clauses):
    with Minisat22(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None
        model = set(solver.get_model() or [])
        x = tuple(int(i+1 in model) for i in range(n))
        assert compatible(x, clauses)
        return x


def separate(n, clauses, actions, p):
    best, calls, maxbits = None, 0, 0
    for a in range(len(actions)):
        constant = sum(p[b]*actions[b][0] for b in range(len(actions)))-actions[a][0]
        coeff = [sum(p[b]*actions[b][1][i] for b in range(len(actions)))-actions[a][1][i] for i in range(n)]
        denominator = lcm(*(v.denominator for v in [constant]+coeff))
        ints = [int(v*denominator) for v in coeff]
        maxbits = max(maxbits, denominator.bit_length(), *(abs(v).bit_length() for v in ints))
        formula = WCNF()
        for c in clauses:
            formula.append(c)
        for i, value in enumerate(ints):
            if value:
                formula.append([i+1 if value > 0 else -(i+1)], weight=abs(value))
        with RC2(formula, solver='m22') as solver:
            model = solver.compute()
            calls += 1
            if model is None:
                raise ValueError('Empty source in separation')
            points = set(model)
            x = tuple(int(i+1 in points) for i in range(n))
            value = constant+F(sum(max(0,c) for c in ints)-solver.cost, denominator)
        assert compatible(x, clauses)
        actual = sum(p[b]*loss(x,actions)[b] for b in range(len(actions)))-loss(x,actions)[a]
        assert actual == value
        if best is None or value > best[0]:
            best = value, x
    return dict(upper=best[0],witness=best[1],maxsat_calls=calls,largest_integer_bits=maxbits)


def generate(n, clauses, actions, retained=(), max_iterations=32):
    start = time.perf_counter_ns()
    seed = initial_model(n,clauses)
    if seed is None:
        return dict(status='empty_source',elapsed_ns=time.perf_counter_ns()-start,source_sat_calls=1)
    # Full admission here; lazy clause-edit membership is a next integration.
    pool = list(dict.fromkeys(x for x in retained if compatible(x,clauses)))
    admitted = len(pool)
    if not pool:
        pool.append(seed)
    records, systems, calls, largest = [], 0, 0, 0
    for _ in range(max_iterations):
        rows = tuple(dict.fromkeys(row(x,actions) for x in pool))
        p, lower, count = minmax(rows)
        systems += count
        sep = separate(n,clauses,actions,p)
        calls += sep['maxsat_calls']
        largest = max(largest,sep['largest_integer_bits'])
        records.append(dict(action=p,lower=lower,upper=sep['upper'],witness=sep['witness'],pool_size=len(pool),unique_rows=len(rows)))
        assert sep['upper'] >= lower
        if sep['upper'] == lower:
            status = 'closed_gap'
            break
        assert sep['witness'] not in pool
        pool.append(sep['witness'])
    else:
        status = 'iteration_cap_unfinished'
    return dict(status=status,action=p,lower=lower,upper=sep['upper'],pool=pool,
                retained_admitted=admitted,retained_rejected=len(retained)-admitted,
                rounds=records,lp_systems=systems,maxsat_calls=calls,source_sat_calls=1,
                largest_integer_bits=largest,elapsed_ns=time.perf_counter_ns()-start)


def exhaustive(n, clauses, actions):
    start = time.perf_counter_ns()
    worlds = [x for x in product((0,1),repeat=n) if compatible(x,clauses)]
    if not worlds:
        return dict(status='empty_source',elapsed_ns=time.perf_counter_ns()-start)
    rows = tuple(dict.fromkeys(row(x,actions) for x in worlds))
    p,value,systems = minmax(rows)
    return dict(status='solved',value=value,action=p,worlds=worlds,unique_rows=len(rows),
                lp_systems=systems,elapsed_ns=time.perf_counter_ns()-start)


def main(output):
    assert not output.exists()
    started = time.monotonic_ns()
    result = dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',seed=8403,
                  start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                  sources={str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (Path(__file__).resolve(),HERE.parent/'s01/region_probe.py')},
                  upper_bound_trust='RC2/MiniSat22 exact solver; independent enumeration only for stated tiny instances')
    try:
        rng = random.Random(8403)
        cases = []
        for n in (3,4,5):
            for trial in range(2):
                clauses = []
                for _ in range(n):
                    variables = rng.sample(range(1,n+1),2)
                    clauses.append([v if rng.randrange(2) else -v for v in variables])
                actions = [(3*n,[rng.randrange(-2,3) for _ in range(n)]) for _ in range(3)]
                pool = []
                versions = [clauses,clauses+[[1]],clauses,clauses+[[-1]]]
                for version,current in enumerate(versions):
                    cold = generate(n,current,actions)
                    warm = generate(n,current,actions,pool)
                    full = exhaustive(n,current,actions)
                    if full['status'] == 'empty_source':
                        assert cold['status'] == warm['status'] == 'empty_source'
                    else:
                        for got in (cold,warm):
                            assert got['status'] == 'closed_gap'
                            assert got['lower'] == got['upper'] == full['value']
                            actual = max(sum(p*v for p,v in zip(got['action'],row(x,actions))) for x in full['worlds'])
                            assert actual == got['upper']
                        pool = warm['pool']
                    cases.append(dict(n=n,trial=trial,version=version,clauses=current,actions=actions,
                                      cold=cold,warm=warm,full=full))
        # Exact revision witnesses: shrink invalidates old lower evidence;
        # expansion invalidates an old action's upper guarantee.
        actions = [(0,[1]),(1,[-1])]
        unrestricted = generate(1,[],actions)
        restricted = generate(1,[[-1]],actions,unrestricted['pool'])
        expanded_upper = separate(1,[],actions,restricted['action'])
        assert unrestricted['lower'] == F(1,2)
        assert restricted['upper'] == 0 and expanded_upper['upper'] == 1
        empty = generate(1,[[1],[-1]],actions)
        assert empty['status'] == 'empty_source' and 'action' not in empty
        result.update(status='complete',cases=cases,
                      revision_witness=dict(unrestricted=unrestricted,restricted=restricted,
                                            old_action_after_expansion=expanded_upper,empty=empty))
    except Exception:
        result.update(status='failed',failure=traceback.format_exc())
        raise
    finally:
        result['elapsed_ns'] = time.monotonic_ns()-started
        result['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ('cases','revision_witness')}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
