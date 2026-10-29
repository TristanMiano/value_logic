"""End-to-end source/evidence/decision binding checks on exposed examples."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time
import traceback
from decision_service import DecisionService
from cert_audit import source_value

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CUTS = ['-5/4','-6/5']
LOSSES = [['0','1'],['10','1'],['10','1'],['10','1'],['0','1']]
SIGNALS = list(range(5))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    dest = HERE/'integration_runs'/sys.argv[1]
    dest.mkdir(parents=True,exist_ok=False)
    freeze_path = HERE/'integration_freeze.json'
    freeze = json.loads(freeze_path.read_text())
    for name,expected in freeze['sha256'].items():
        assert sha(ROOT/name) == expected,name
    (dest/'freeze.json').write_bytes(freeze_path.read_bytes())
    started = time.perf_counter_ns()
    try:
        inputs = json.loads((HERE/'audit_inputs.json').read_text())
        problem = next(r['problem'] for r in inputs if r['name'] == 'noisy_envelope')
        original = deepcopy(problem)
        service = DecisionService(problem)
        digest = service.problem_sha256
        outputs = [service.assess(CUTS,LOSSES,SIGNALS,1)]
        assert outputs[-1]['status'] == 'CONDITIONAL_ON_NONEMPTY_SOURCE'
        assert outputs[-1]['observation']['ideal_baseline_observation_upper'] == '0'
        assert outputs[-1]['observation']['sharp_improvement_upper'] == '1'
        problem['generators'][0]['b'][0] = '-1000'
        assert service.problem_sha256 == digest
        work = service.propagate(2)
        outputs.append(service.assess(CUTS,LOSSES,SIGNALS,0))
        assert outputs[-1]['status'] == 'CONDITIONAL_ON_NONEMPTY_SOURCE'
        assert outputs[-1]['computation']['sharp_certified_optimal_actions'] == [0]
        assert outputs[-1]['observation']['sharp_improvement_upper'] == '0'
        assert not outputs[-1]['bracket']['exact']
        assert outputs[0]['decision_sha256'] != outputs[1]['decision_sha256']
        rejects = []
        for points,binding in (([['1/5','1'],['1','4/5']],'wrong'),
                               ([['1/5','1'],['1','1']],digest)):
            before = service.evidence_state(); rev = service.revision
            try: service.add_source(points,binding)
            except ValueError as error: rejects.append(str(error))
            else: raise AssertionError('invalid source accepted')
            assert service.evidence_state() == before and service.revision == rev
        for source in ([['1/5','1'],['1','4/5']],[['1','1/5'],['4/5','1']]):
            service.add_source(source,digest)
            outputs.append(service.assess(CUTS,LOSSES,SIGNALS,0))
            assert outputs[-1]['status'] == 'CHECKED_DECISION'
        source_checks = 0
        for output in outputs:
            for cell,witness in output.get('known_cell_sources',{}).items():
                q = source_value(original,[list(map(F,x)) for x in witness['source']])
                assert q == F(witness['q'])
                assert (int(cell) == 0 and q < F(CUTS[0])) or (int(cell) == 4 and q > F(CUTS[1]))
                source_checks += 1
        snapshot = deepcopy(outputs[-1])
        outputs[-1]['computation']['sharp_improvement_bounds'][0] = '999'
        assert service.assess(CUTS,LOSSES,SIGNALS,0) == snapshot
        outputs[-1] = snapshot
        inconsistent = DecisionService(next(r['problem'] for r in inputs if r['name'] == 'inconsistent_constant'))
        bad_work = inconsistent.propagate(2)
        bad = inconsistent.assess(CUTS,LOSSES,SIGNALS,0)
        assert bad['status'] == 'INCONSISTENT_SOURCE' and not bad['mathematical_source_nonempty_proved']
        result = dict(status='PASS',label='DEVELOPMENT; exposed end-to-end examples',
            outputs=outputs,inconsistency=bad,propagation=work,inconsistent_propagation=bad_work,
            source_checks=source_checks,invalid_rejections=rejects,optimizer_calls=0,
            elapsed_ns=time.perf_counter_ns()-started,freeze_sha256=sha(freeze_path))
        (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('status','source_checks','invalid_rejections','optimizer_calls','elapsed_ns')}))
    except BaseException as error:
        (dest/'failure.json').write_text(json.dumps(dict(status='FAIL',error=repr(error),traceback=traceback.format_exc(),elapsed_ns=time.perf_counter_ns()-started),indent=2)+'\n')
        raise


if __name__ == '__main__':
    main()
