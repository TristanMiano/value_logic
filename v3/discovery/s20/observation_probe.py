"""Exact finite policy enumeration versus threshold-cover observation value."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time
import traceback
import observation_value as method

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
POINTS = ['-1','0','1','2','3']
CUTS = ['0','2']
NAMES = {'joint_maxima','optimal_not_safe','seeded_0','one_action'}
SIGNALS = [[0]*5,list(range(5)),[0,1,0,1,2]]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bracket(known,possible):
    return {key:[[POINTS[j],POINTS[j]] for j in ids]
            for key,ids in (('inner',known),('outer',possible))}


def reference(values,support,signals):
    m = len(values[0])
    groups = sorted({signals[j] for j in support})
    before = min(max(values[j][a] for j in support) for a in range(m))
    after = None
    count = 0
    for actions in product(range(m),repeat=len(groups)):
        policy = dict(zip(groups,actions))
        risk = max(values[j][policy[signals[j]]] for j in support)
        after = risk if after is None else min(after,risk)
        count += 1
    return before,after,count


def main():
    dest = HERE/'observe_runs'/sys.argv[1]
    dest.mkdir(parents=True,exist_ok=False)
    freeze_path = HERE/'observation_freeze.json'
    freeze = json.loads(freeze_path.read_text())
    for name,expected in freeze['sha256'].items():
        assert sha(ROOT/name) == expected,name
    (dest/'freeze.json').write_bytes(freeze_path.read_bytes())
    inputs = [row for row in json.loads((HERE/'refinement_inputs.json').read_text()) if row['name'] in NAMES]
    assert len(inputs) == 4
    started = time.perf_counter_ns()
    counts = dict(brackets=0,support_controls=0,enumerated_policies=0,
                  support_uses=0,strict_upper_improvements=0,dp_transitions=0)
    try:
        with gzip.open(dest/'records.jsonl.gz','wt',encoding='utf-8') as out:
            for case in inputs:
                for criterion in ('loss','regret'):
                    values = [list(map(F,row)) for row in case['values']]
                    if criterion == 'regret':
                        values = [[v-min(row) for v in row] for row in values]
                    for signals in SIGNALS:
                        control = {}
                        for mask in range(1,32):
                            support = [j for j in range(5) if mask & (1 << j)]
                            before,after,npolicies = reference(values,support,signals)
                            b2,q2,policy = method.costs(values,support,signals)
                            assert (before,after) == (b2,q2)
                            assert max(values[j][policy[signals[j]]] for j in support) == after
                            control[mask] = (before,after)
                            counts['support_controls'] += 1
                            counts['enumerated_policies'] += npolicies
                        for state in product(range(3),repeat=5):
                            known = [j for j,s in enumerate(state) if s == 2]
                            possible = [j for j,s in enumerate(state) if s >= 1]
                            if not possible:
                                continue
                            kmask = sum(1 << j for j in known)
                            pmask = sum(1 << j for j in possible)
                            admitted = [mask for mask in control if mask & kmask == kmask and mask | pmask == pmask]
                            benefits = [control[mask][0]-control[mask][1] for mask in admitted]
                            result = method.assess(bracket(known,possible),CUTS,case['values'],signals,criterion)
                            sharp = F(result['sharp_improvement_upper'])
                            coarse = F(result['coarse_improvement_upper'])
                            lower = F(result['guaranteed_improvement_lower'])
                            assert sharp == max(benefits)
                            assert 0 <= lower <= min(benefits) <= sharp <= coarse
                            if len(set(signals)) == 1 or len(values[0]) == 1:
                                assert sharp == 0
                            witness = result['support_witness']
                            support = witness['support']
                            mask = sum(1 << j for j in support)
                            assert mask in admitted
                            before,after = control[mask]
                            assert before-after == sharp
                            assert (str(before),str(after)) == (witness['before'],witness['after'])
                            assert before >= F(witness['threshold_before'])
                            risk = max(values[j][witness['policy'][str(signals[j])]] for j in support)
                            assert risk <= F(witness['threshold_after'])
                            outer_policy = result['implementable_outer_policy']
                            for mask in admitted:
                                ids = [j for j in range(5) if mask & (1 << j)]
                                risk = max(values[j][outer_policy[str(signals[j])]] for j in ids)
                                assert risk <= F(result['outer_policy_worst_loss'])
                                if lower > 0:
                                    assert control[mask][0]-risk >= lower
                            counts['brackets'] += 1
                            counts['support_uses'] += len(admitted)
                            counts['strict_upper_improvements'] += sharp < coarse
                            counts['dp_transitions'] += result['dp_transitions']
                            out.write(json.dumps(dict(case=case['name'],signals=signals,result=result),sort_keys=True)+'\n')
            safety = next(row for row in inputs if row['name'] == 'optimal_not_safe')
            fixture = method.assess(bracket([0,1],[0,1]),CUTS,safety['values'],list(range(5)))
            assert fixture['sharp_improvement_upper'] == '10'
            assert fixture['guaranteed_improvement_lower'] == '10'
            rejected = []
            for operation in (
                lambda: method.assess(bracket([], [0]),CUTS,safety['values'],[0]),
                lambda: method.assess(bracket([], [0]),CUTS,safety['values'],[-1]*5),
                lambda: method.assess(bracket([1], [0]),CUTS,safety['values'],[0]*5),
            ):
                try: operation()
                except ValueError as error: rejected.append(str(error))
                else: raise AssertionError('bad input accepted')
            assert method.assess(bracket([],[]),CUTS,safety['values'],[0]*5)['status'] == 'INCONSISTENT_BRACKET'
        result = dict(status='PASS',label='DEVELOPMENT; exposed finite matrices',**counts,
                      observation_fixture=fixture,invalid_rejections=rejected,
                      elapsed_ns=time.perf_counter_ns()-started,freeze_sha256=sha(freeze_path),
                      records_sha256=sha(dest/'records.jsonl.gz'))
        (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('status',*counts,'elapsed_ns')}))
    except BaseException as error:
        (dest/'failure.json').write_text(json.dumps(dict(status='FAIL',error=repr(error),traceback=traceback.format_exc(),elapsed_ns=time.perf_counter_ns()-started),indent=2)+'\n')
        raise


if __name__ == '__main__':
    main()
