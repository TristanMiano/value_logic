"""DEVELOPMENT: matched regret-tolerance services and bounded SAT encoding.

Codex (GPT-6), 2026-10-11. UNSAT warrants trust local MiniSat22; no external
proof checker. Shared nonempty source provenance is a caller precondition.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
from math import lcm
import hashlib
import json
from pathlib import Path
import random
import sys
import time
import traceback

from decision_probe import compatible, row
from pysat.solvers import Minisat22


def neg(lit):
    return not lit if type(lit) is bool else -lit


def threshold(n, weighted, target):
    """CNF extension iff sum(weight * literal_truth) >= target.

    Unary threshold DP, O(n*target) states; declared pseudo-polynomial.
    """
    assert 0 < target <= sum(w for _,w in weighted) <= 10000
    clauses, next_var = [], n
    def emit(*lits):
        clean = set()
        for lit in lits:
            if type(lit) is bool:
                if lit:
                    return
                continue
            if -lit in clean:
                return
            clean.add(lit)
        clauses.append(sorted(clean))
    previous = [True]+[False]*target
    for literal,weight in weighted:
        current = [True]
        for s in range(1,target+1):
            a, b = previous[s], previous[max(0,s-weight)]
            if a is True or b is False or (type(a) is type(b) and a == b):
                z = a
            elif a is False and b is True:
                z = literal
            else:
                next_var += 1
                z = next_var
                # z <=> a or (literal and b)
                emit(neg(a),z)
                emit(-literal,neg(b),z)
                emit(-z,a,literal)
                emit(-z,a,b)
            current.append(z)
        previous = current
    emit(previous[target])
    return clauses,next_var-n


def affine(actions,p,a):
    constant = sum(q*act[0] for q,act in zip(p,actions))-actions[a][0]
    coeff = [sum(q*act[1][i] for q,act in zip(p,actions))-actions[a][1][i] for i in range(len(actions[0][1]))]
    return constant,coeff


def box_bound(actions,p,fixed):
    return max(c+sum(w*fixed[i] if i in fixed else max(F(0),w) for i,w in enumerate(weights))
               for c,weights in (affine(actions,p,a) for a in range(len(actions))))


def violation(n,clauses,actions,p,epsilon,fixed=None):
    """Exact existence of a violating source world; source already nonempty
    unless this is an explicitly allowed delta-region emptiness check.
    """
    fixed = fixed or {}
    calls = encoded = variables = 0
    for a in range(len(actions)):
        constant,coeff = affine(actions,p,a)
        for i,bit in fixed.items():
            constant += coeff[i]*bit
            coeff[i] = F(0)
        denominator = lcm(*(v.denominator for v in [constant,epsilon]+coeff))
        ints = [int(v*denominator) for v in coeff]
        weighted = [(i+1 if value>0 else -(i+1),abs(value)) for i,value in enumerate(ints) if value]
        target = int((epsilon-constant)*denominator)+sum(-v for v in ints if v<0)+1
        if target > sum(w for _,w in weighted):
            continue
        extras, aux = ([],0) if target <= 0 else threshold(n,weighted,target)
        hard = list(clauses)+[[i+1 if bit else -(i+1)] for i,bit in fixed.items()]+extras
        encoded += len(extras)
        variables += aux
        with Minisat22(bootstrap_with=hard) as solver:
            calls += 1
            if solver.solve():
                model = set(solver.get_model() or [])
                x = tuple(int(i+1 in model) for i in range(n))
                assert compatible(x,clauses) and all(x[i]==bit for i,bit in fixed.items())
                assert sum(q*v for q,v in zip(p,row(x,actions))) > epsilon
                return dict(accepted=False,witness=x,sat_calls=calls,encoded_clauses=encoded,auxiliary_variables=variables)
    return dict(accepted=True,sat_calls=calls,encoded_clauses=encoded,auxiliary_variables=variables)


def full_tolerance(n,clauses,actions,p,epsilon):
    started = time.perf_counter_ns()
    result = violation(n,clauses,actions,p,epsilon)
    return dict(result,elapsed_ns=time.perf_counter_ns()-started)


def delta_tolerance(n,old,index,actions,p,old_upper,epsilon):
    started = time.perf_counter_ns()
    assert old_upper <= epsilon
    removed = old[index]
    rest = old[:index]+old[index+1:]
    if removed in rest or any(-lit in removed for lit in removed):
        result = dict(accepted=True,route='same_source',sat_calls=0,encoded_clauses=0,auxiliary_variables=0)
    else:
        fixed = {abs(lit)-1:int(lit<0) for lit in removed}
        upper = box_bound(actions,p,fixed)
        if upper <= epsilon:
            result = dict(accepted=True,route='box_guard',delta_box_upper=upper,sat_calls=0,encoded_clauses=0,auxiliary_variables=0)
        else:
            result = dict(violation(n,rest,actions,p,epsilon,fixed),route='delta_sat',delta_box_upper=upper)
    return dict(result,elapsed_ns=time.perf_counter_ns()-started)


def encoding_checks():
    rng, assignments = random.Random(8405), 0
    for n in range(1,7):
        for _ in range(6):
            weighted = [(i+1 if rng.randrange(2) else -(i+1),rng.randrange(1,5)) for i in range(n)]
            target = rng.randrange(1,sum(w for _,w in weighted)+1)
            clauses,_ = threshold(n,weighted,target)
            with Minisat22(bootstrap_with=clauses) as solver:
                for x in product((0,1),repeat=n):
                    expected = sum(w for lit,w in weighted if x[abs(lit)-1]==int(lit>0)) >= target
                    got = solver.solve(assumptions=[i+1 if bit else -(i+1) for i,bit in enumerate(x)])
                    assert got == expected, (n,weighted,target,x,got,expected)
                    assignments += 1
    return assignments


def main(output):
    assert not output.exists()
    started = time.monotonic_ns()
    source = Path(__file__).with_name('delta01.json')
    result = dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                  start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  input_record=dict(path=source.name,sha256=hashlib.sha256(source.read_bytes()).hexdigest()),
                  timing_scope='matched warm tolerance queries; old warranted action/source certificate is shared pre-existing input; includes guard/threshold construction/solver calls, excludes import and harness')
    try:
        result['encoding_assignments'] = encoding_checks()
        cases=[]
        for index,case in enumerate(json.loads(source.read_text())['cases']):
            n,old,actions = case['n'],case['request']['clauses'],case['request']['actions']
            removed = case['removed_index']
            rest = old[:removed]+old[removed+1:]
            p = tuple(F(v) for v in case['action'])
            old_upper,actual_upper = F(case['old_upper']),F(case['full']['upper'])
            for slack in (F(0),F(1,2)):
                epsilon = old_upper+slack
                full = full_tolerance(n,rest,actions,p,epsilon)
                delta = delta_tolerance(n,old,removed,actions,p,old_upper,epsilon)
                assert full['accepted'] == delta['accepted'] == (actual_upper <= epsilon)
                cases.append(dict(input_case=index,n=n,epsilon=epsilon,full=full,delta=delta))
        result.update(status='complete',cases=cases)
    except Exception:
        result.update(status='failed',failure=traceback.format_exc())
        raise
    finally:
        result['elapsed_ns'] = time.monotonic_ns()-started
        result['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='cases'}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
