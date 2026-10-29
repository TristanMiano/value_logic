"""Check baseline-aware observation bounds by finite policy enumeration."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time
import traceback
import incumbent_value as method
from observation_probe import reference, bracket, CUTS, SIGNALS, NAMES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
HAZARD = [['0','1'],['10','1'],['0','1'],['10','1'],['0','1']]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    dest = HERE/'incumbent_runs'/sys.argv[1]
    dest.mkdir(parents=True,exist_ok=False)
    freeze_path = HERE/'incumbent_freeze.json'
    freeze = json.loads(freeze_path.read_text())
    for name,expected in freeze['sha256'].items():
        assert sha(ROOT/name) == expected,name
    (dest/'freeze.json').write_bytes(freeze_path.read_bytes())
    inputs = [row for row in json.loads((HERE/'refinement_inputs.json').read_text()) if row['name'] in NAMES]
    inputs.append(dict(name='hazard_fallback',values=HAZARD))
    started = time.perf_counter_ns()
    counts = dict(brackets=0,support_controls=0,enumerated_policies=0,
                  action_bounds=0,strict_decomposition_improvements=0,
                  inspected_cell_action_options=0)
    try:
        with gzip.open(dest/'records.jsonl.gz','wt',encoding='utf-8') as out:
            for case in inputs:
                for criterion in ('loss','regret'):
                    values = [list(map(F,row)) for row in case['values']]
                    if criterion == 'regret':
                        values = [[v-min(row) for v in row] for row in values]
                    m = len(values[0])
                    for signals in SIGNALS:
                        control = {}
                        for mask in range(1,32):
                            support = [j for j in range(5) if mask & (1 << j)]
                            _,after,npolicies = reference(values,support,signals)
                            gains = [max(values[j][a] for j in support)-after for a in range(m)]
                            control[mask] = (gains,after)
                            counts['support_controls'] += 1
                            counts['enumerated_policies'] += npolicies
                        for state in product(range(3),repeat=5):
                            known = [j for j,s in enumerate(state) if s == 2]
                            possible = [j for j,s in enumerate(state) if s >= 1]
                            if not possible:
                                continue
                            kmask,pmask = [sum(1 << j for j in ids) for ids in (known,possible)]
                            admitted = [mask for mask in control if mask & kmask == kmask and mask | pmask == pmask]
                            expected = [max(control[mask][0][a] for mask in admitted) for a in range(m)]
                            result = method.assess(bracket(known,possible),CUTS,case['values'],signals,0,criterion)
                            actual = list(map(F,result['all_incumbent_upper_bounds']))
                            decomposition = list(map(F,result['decomposition_upper_bounds']))
                            assert actual == expected
                            assert all(a <= b for a,b in zip(actual,decomposition))
                            assert F(result['sharp_improvement_upper']) == expected[0]
                            for a,witness in enumerate(result['all_support_witnesses']):
                                support = witness['support']
                                mask = sum(1 << j for j in support)
                                assert mask in admitted and control[mask][0][a] == actual[a]
                                risk = max(values[j][witness['policy'][str(signals[j])]] for j in support)
                                assert risk <= F(witness['threshold_after'])
                            lower = F(result['guaranteed_improvement_lower'])
                            for mask in admitted:
                                support = [j for j in range(5) if mask & (1 << j)]
                                risk = max(values[j][result['implementable_outer_policy'][str(signals[j])]] for j in support)
                                if lower > 0:
                                    assert max(values[j][0] for j in support)-risk >= lower
                            counts['brackets'] += 1
                            counts['action_bounds'] += m
                            counts['strict_decomposition_improvements'] += sum(a < b for a,b in zip(actual,decomposition))
                            counts['inspected_cell_action_options'] += result['inspected_cell_action_options']
                            out.write(json.dumps(dict(case=case['name'],signals=signals,
                                known=known,possible=possible,result=result),sort_keys=True)+'\n')
            fixture = method.assess(bracket([],[0,1]),CUTS,HAZARD,list(range(5)),1)
            assert fixture['ideal_baseline_observation_upper'] == '0'
            assert fixture['sharp_improvement_upper'] == '1'
            opposing = next(row for row in inputs if row['name'] == 'optimal_not_safe')
            assert method.assess(bracket([0,1],[0,1]),CUTS,opposing['values'],list(range(5)),0)['sharp_improvement_upper'] == '10'
            rejects = []
            for incumbent in (None,2,True):
                try: method.assess(bracket([],[0]),CUTS,HAZARD,[0]*5,incumbent)
                except ValueError as error: rejects.append(str(error))
                else: raise AssertionError('invalid incumbent accepted')
        result = dict(status='PASS',label='DEVELOPMENT; exposed matrices plus fixed counterexample',**counts,
            baseline_counterexample=fixture,invalid_rejections=rejects,
            elapsed_ns=time.perf_counter_ns()-started,freeze_sha256=sha(freeze_path),
            records_sha256=sha(dest/'records.jsonl.gz'))
        (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('status',*counts,'elapsed_ns')}))
    except BaseException as error:
        (dest/'failure.json').write_text(json.dumps(dict(status='FAIL',error=repr(error),traceback=traceback.format_exc(),elapsed_ns=time.perf_counter_ns()-started),indent=2)+'\n')
        raise


if __name__ == '__main__':
    main()
