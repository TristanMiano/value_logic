"""Finite developmental contrasts for analytic simplifications and sharpness."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json
import time
import traceback
from audit_inputs import encoded
from cert_audit import produce
from range_service import CheckedRange
from service_probe import exact_source

HERE = Path(__file__).resolve().parent


def problem_strings(value):
    if isinstance(value, (int, F)):
        return str(F(value))
    if isinstance(value, list):
        return [problem_strings(x) for x in value]
    if isinstance(value, dict):
        return {k: problem_strings(v) for k, v in value.items()}
    return value


def offset_case(name, lower, upper, offsets, future, bands):
    # Unknown max-affine intercepts. Negation translates to the min contract.
    lower, upper, future = list(map(F, lower)), list(map(F, upper)), list(map(F, future))
    offsets = [list(map(F, row)) for row in offsets]
    bands = [(F(a), F(b)) for a, b in bands]
    generators = [dict(A=[[1], [-1]], b=[u, -l], c=[-1], d=-d)
                  for l, u, d in zip(lower, upper, future)]
    receipts = [dict(lo=-b, hi=-a, forms=[dict(c=[-1], d=-v) for v in row])
                for row, (a, b) in zip(offsets, bands)]
    caps = [min([upper[i]] + [b - row[i] for row, (a, b) in zip(offsets, bands)])
            for i in range(len(lower))]
    expected = []
    if all(l <= u for l, u in zip(lower, caps)):
        choices = [[i for i in range(len(lower)) if a-row[i] <= caps[i]]
                   for row, (a, b) in zip(offsets, bands)]
        if all(choices):
            low = max([max(d+l for d, l in zip(future, lower))] +
                      [min(future[i]+max(lower[i], a-row[i]) for i in allowed)
                       for row, (a, b), allowed in zip(offsets, bands, choices)])
            high = max(d+u for d, u in zip(future, caps))
            expected = [[-high, -low]]
    return encoded(dict(name=name, kind='offset',
                        problem=problem_strings(dict(generators=generators, receipts=receipts)),expected=expected))


def noisy_sharp(k):
    r = k // 2
    eps = F(1, 16*(k+1)*(1 << k))
    a, b = [], []
    for j in range(k):
        row = [F(0)] * k
        row[j] = 1
        a.extend([row, [-v for v in row]])
        b.extend([F(1), F(0)])
    generators = []
    for i, size in enumerate([r, k-r]):
        generators.append(dict(A=a+[[1]*k, [-1]*k], b=b+[size+eps, -size+eps],
                               c=[1 << j for j in range(k)] if i == 0 else [0]*k,
                               d=1 if i == 0 else (1 << k)+2))
    receipts = []
    for j in range(k):
        c = [0] * k
        c[j] = 1
        receipts.append(dict(lo=0, hi=eps, forms=[dict(c=c, d=0), dict(c=c, d=0)]))
    return encoded(dict(name=f'noisy_sharp_{k}', kind='sharp', k=k,
                        expected_components=comb(k, r),
                        problem=problem_strings(dict(generators=generators, receipts=receipts))))


def inputs():
    rows = [
        offset_case('offset_no_history',[-2,0],[3,4],[],[1,-2],[]),
        offset_case('offset_one_block',[0],[4],[[1],[2]],[3],[[2,3],[3,4]]),
        offset_case('offset_different_witnesses',[0,0],[3,3],[[0,-2],[-2,0]],
                    [0,1],[[2,3],[2,3]]),
        offset_case('offset_fractional',['-1/2',0,'1/4'],['3/2',2,'7/4'],
                    [[0,'1/3',-1],['1/2',-1,0]],['1/7','-2/3','1/5'],
                    [['3/4','5/4'],['1','7/4']]),
        offset_case('offset_lower_impossible',[0,0],[1,1],[[0,0]],[0,0],[[2,3]]),
        offset_case('offset_upper_impossible',[1,0],[2,1],[[0,0]],[0,0],[[-1,0]]),
    ]
    old = [json.loads(line) for line in (HERE/'audit_records.jsonl').read_text(encoding='utf-8').splitlines()]
    problem = next(x['problem'] for x in old if x['name'] == 'noisy_envelope')
    problem['generators'].append(dict(A=[['1','0'],['-1','0'],['0','1'],['0','-1']],
                                     b=['1','0','1','0'], c=['1/2','-3/2'], d='0'))
    for j, obs in enumerate(problem['receipts']):
        obs['forms'].append(dict(c=['-1','0'] if j == 0 else ['0','-1'], d='0'))
    rows.append(dict(name='envelope_third_piece',kind='revision',problem=problem,
                     expected=[['-3/2','-197/200']]))
    rows.extend(noisy_sharp(k) for k in range(2, 7))
    return rows


def main():
    freeze = json.loads((HERE/'control_freeze.json').read_text(encoding='utf-8'))
    for name, expected in freeze['sha256'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == expected
    cases = inputs()
    (HERE/'control_inputs.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    summaries = []
    with (HERE/'control_records.jsonl').open('x',encoding='utf-8') as output:
        for case in cases:
            before = time.perf_counter_ns()
            certificate = produce(case['problem'])
            elapsed = time.perf_counter_ns()-before
            service = CheckedRange(case['problem'], certificate)
            ranges = service.ranges()
            if 'expected' in case:
                assert ranges == case['expected'], (case['name'],ranges,case['expected'])
            else:
                assert len(ranges) == case['expected_components']
                assert all(F(a)<F(b) for a,b in ranges)
                assert all(F(ranges[j+1][0])-F(ranges[j][1]) > F(7,8)
                           for j in range(len(ranges)-1))
            points = sorted({q for a,b in ranges for q in [F(a), F(b), (F(a)+F(b))/2]})
            witnesses = [service.source(str(q)) for q in points]
            for witness in witnesses:
                exact_source(case['problem'],witness)
            summary = dict(name=case['name'],components=len(ranges),witnesses=len(witnesses),
                           production_ns=elapsed)
            summaries.append(summary)
            output.write(json.dumps(dict(case=case,certificate=certificate,witnesses=witnesses,
                                         summary=summary),sort_keys=True)+'\n')
            output.flush()
    result = dict(status='PASS',label='DEVELOPMENT, same-model',cases=summaries)
    (HERE/'control_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        (HERE/'control_failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise
