"""Rational LP epigraph controls for the continuous computation gap."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time
import traceback
import scipy.optimize
from lp_witness import minimize
import continuous_gap as method

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    dest = HERE/'continuous_runs'/sys.argv[1]
    dest.mkdir(parents=True,exist_ok=False)
    freeze_path = HERE/'continuous_freeze.json'
    freeze = json.loads(freeze_path.read_text())
    for name,expected in freeze['sha256'].items():
        assert sha(ROOT/name) == expected,name
    (dest/'freeze.json').write_bytes(freeze_path.read_bytes())
    calls = 0
    original = scipy.optimize.linprog
    def counted(*args,**kwargs):
        nonlocal calls
        calls += 1
        return original(*args,**kwargs)
    scipy.optimize.linprog = counted
    started = time.perf_counter_ns()
    outputs = []
    try:
        inputs = json.loads((HERE/'continuous_inputs.json').read_text())
        for case in inputs:
            knots = list(map(F,case['knots']))
            values = [list(map(F,row)) for row in case['losses']]
            inner = [tuple(map(F,row)) for row in case['bracket']['inner']]
            m = len(values[0])
            known = [q for lo,hi in inner for q in [lo,hi]+[x for x in knots if lo <= x <= hi]]
            lower = [max(method.value(knots,values,q,b) for q in known) if known else None for b in range(m)]
            exact = [F(0)]*m
            controls = []
            for a in range(m):
                for b in range(m):
                    if a == b:
                        continue
                    for i,(lo,hi) in enumerate(zip(knots,knots[1:])):
                        sa,da = method.affine(knots,values,i,a)
                        sb,db = method.affine(knots,values,i,b)
                        rows = [[F(1),F(0)],[F(-1),F(0)],[sb,F(-1)]]
                        rhs = [hi,-lo,-db]
                        if lower[b] is not None:
                            rows.append([F(0),F(-1)]);rhs.append(-lower[b])
                        result = minimize(rows,rhs,[-sa,F(1)])
                        assert result['kind'] == 'optimum'
                        v = da-result['value']
                        exact[a] = max(exact[a],v)
                        controls.append(dict(a=a,b=b,piece=i,value=str(v),
                            point=list(map(str,result['point'])),dual=list(map(str,result['dual']))))
            result = method.assess(case['bracket'],case['knots'],case['losses'])
            assert list(map(F,result['sharp_improvement_bounds'])) == exact
            for a,w in enumerate(result['witnesses']):
                q = F(w['q'])
                worst = [method.value(knots,values,q,b) if lower[b] is None else max(lower[b],method.value(knots,values,q,b)) for b in range(m)]
                assert worst[a]-min(worst) == exact[a]
            outputs.append(dict(name=case['name'],result=result,controls=controls))
        assert outputs[0]['result']['sharp_improvement_bounds'] == ['0','13/4']
        assert outputs[0]['result']['witnesses'][1]['q'] == '3/4'
        fixed = inputs[0]
        rejects = []
        for bracket,knots,losses in (
            (fixed['bracket'],list(reversed(fixed['knots'])),fixed['losses']),
            (dict(inner=[],outer=[['-2','2']]),fixed['knots'],fixed['losses']),
            (fixed['bracket'],fixed['knots'],[['0']]),
        ):
            try: method.assess(bracket,knots,losses)
            except ValueError as error: rejects.append(str(error))
            else: raise AssertionError('invalid input accepted')
        result = dict(status='PASS',label='DEVELOPMENT; exact LP controls',outputs=outputs,
            optimizer_calls=calls,candidate_evaluations=sum(r['result']['candidate_evaluations'] for r in outputs),
            invalid_rejections=rejects,elapsed_ns=time.perf_counter_ns()-started,
            freeze_sha256=sha(freeze_path))
        (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('status','optimizer_calls','candidate_evaluations','elapsed_ns')}))
    except BaseException as error:
        (dest/'failure.json').write_text(json.dumps(dict(status='FAIL',error=repr(error),traceback=traceback.format_exc(),elapsed_ns=time.perf_counter_ns()-started),indent=2)+'\n')
        raise


if __name__ == '__main__':
    main()
