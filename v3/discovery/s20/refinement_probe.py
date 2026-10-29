"""Compare the sharp formula to all compatible finite supports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time
import traceback
from refinement_gap import assess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
POINTS = ['-1','0','1','2','3']
CUTS = ['0','2']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bracket(known, possible):
    return {key:[[POINTS[j],POINTS[j]] for j in ids]
            for key,ids in (('inner',known),('outer',possible))}


def gaps(values, support):
    worst = [max(values[j][a] for j in support) for a in range(len(values[0]))]
    return [v-min(worst) for v in worst]


def main():
    dest = HERE/'refine_runs'/sys.argv[1]
    dest.mkdir(parents=True,exist_ok=False)
    freeze_path = HERE/'refinement_freeze.json'
    freeze = json.loads(freeze_path.read_text())
    for name,expected in freeze['sha256'].items():
        assert sha(ROOT/name) == expected,name
    (dest/'freeze.json').write_bytes(freeze_path.read_bytes())
    inputs = json.loads((HERE/'refinement_inputs.json').read_text())
    started = time.perf_counter_ns()
    counts = dict(brackets=0,supports=0,action_bounds=0,strict_improvements=0,
                  newly_certified_actions=0,support_witnesses=0)
    try:
        with gzip.open(dest/'records.jsonl.gz','wt',encoding='utf-8') as out:
            for case in inputs:
                for criterion in ('loss','regret'):
                    values = [list(map(F,row)) for row in case['values']]
                    if criterion == 'regret':
                        values = [[v-min(row) for v in row] for row in values]
                    m = len(values[0])
                    for state in product(range(3),repeat=5):
                        known = [j for j,s in enumerate(state) if s == 2]
                        possible = [j for j,s in enumerate(state) if s >= 1]
                        if not possible:
                            continue
                        unknown = sorted(set(possible)-set(known))
                        exact = [F(0)]*m
                        supports = 0
                        for bits in product((0,1),repeat=len(unknown)):
                            support = known+[j for j,bit in zip(unknown,bits) if bit]
                            if not support:
                                continue
                            actual = gaps(values,support)
                            exact = [max(a,b) for a,b in zip(exact,actual)]
                            supports += 1
                        result = assess(bracket(known,possible),CUTS,case['values'],criterion)
                        got = list(map(F,result['sharp_improvement_bounds']))
                        old = list(map(F,result['improvement_bounds']))
                        assert got == exact
                        assert all(a <= b for a,b in zip(got,old))
                        assert result['sharp_certified_optimal_actions'] == [a for a,v in enumerate(exact) if v == 0]
                        assert result['smallest_sharp_gap_action'] == min(range(m),key=lambda a:(exact[a],a))
                        for a,witness in enumerate(result['sharp_support_witnesses']):
                            support = witness['support']
                            assert support and set(known) <= set(support) <= set(possible)
                            assert gaps(values,support)[a] == exact[a]
                            counts['support_witnesses'] += 1
                        counts['brackets'] += 1
                        counts['supports'] += supports
                        counts['action_bounds'] += m
                        counts['strict_improvements'] += sum(a < b for a,b in zip(got,old))
                        counts['newly_certified_actions'] += sum(a == 0 < b for a,b in zip(got,old))
                        out.write(json.dumps(dict(case=case['name'],criterion=criterion,
                            known=known,possible=possible,exact=list(map(str,exact)),
                            old=list(map(str,old)),witnesses=result['sharp_support_witnesses']),sort_keys=True)+'\n')
            fixture = assess(bracket([0,1],[0,1,2]),CUTS,inputs[0]['values'])
            assert fixture['improvement_bounds'][0] == '2'
            assert fixture['sharp_improvement_bounds'][0] == '0'
            safety = assess(bracket([0,1],[0,1]),CUTS,inputs[1]['values'])
            assert safety['sharp_improvement_bounds'] == ['0','0']
            assert safety['upper'] == ['10','10']
            invalid = [
                lambda: assess(bracket([], [0]),CUTS,inputs[0]['values'],'unspecified'),
                lambda: assess(bracket([], [0]),CUTS,[['0']]),
                lambda: assess(bracket([1], [0]),CUTS,inputs[0]['values']),
            ]
            rejects = []
            for op in invalid:
                try: op()
                except ValueError as error: rejects.append(str(error))
                else: raise AssertionError('invalid input accepted')
            empty = assess(bracket([],[]),CUTS,inputs[0]['values'])
            assert empty['status'] == 'INCONSISTENT_BRACKET'
        result = dict(status='PASS',label='DEVELOPMENT; exact finite enumeration',**counts,
            fixture=fixture,safety_counterexample=safety,invalid_rejections=rejects,
            elapsed_ns=time.perf_counter_ns()-started,freeze_sha256=sha(freeze_path),
            records_sha256=sha(dest/'records.jsonl.gz'))
        (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:result[k] for k in ('status',*counts,'elapsed_ns')}))
    except BaseException as error:
        (dest/'failure.json').write_text(json.dumps(dict(status='FAIL',error=repr(error),
            traceback=traceback.format_exc(),elapsed_ns=time.perf_counter_ns()-started),indent=2)+'\n')
        raise


if __name__ == '__main__':
    main()
