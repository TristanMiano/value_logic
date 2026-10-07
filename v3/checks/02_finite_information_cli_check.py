"""One prospectively scoped P3-02 DEVELOPMENT interface check.

ChatGPT (GPT-6 Astra Pro), 2026-10-07. Exercises the actual CLI, external
input binding, certificate verification, a target decoder and exclusive
output preservation. This is not a second exhaustive scientific corpus.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
GENERATOR=HERE/'02_finite_information_audit.py'
VERIFIER=HERE/'02_finite_information_verify.py'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_rows(rows):
    return [[F(x) for x in row] for row in rows]


def dot(a,b):
    assert len(a)==len(b)
    return sum((x*y for x,y in zip(a,b)),F(0))


def run(output):
    output=output.resolve()
    if output.exists():
        raise SystemExit('Refusing to overwrite an existing interface result.')
    folder=output.parent/(output.stem+'_files')
    folder.mkdir()  # An existing attempt is preserved and must be reconciled.
    request_path=folder/'input.json'
    artifact_path=folder/'certificate.json'
    request={'n_states':3,'losses':[[0,1,0]],'targets':[[1,0,0]],
             'calibration':'unknown_affine'}
    request_path.write_text(json.dumps(request,indent=2)+'\n')
    paths=[Path(__file__).resolve(),GENERATOR,VERIFIER]
    versions={str(p.relative_to(ROOT)):digest(p) for p in paths}
    start_ns=time.monotonic_ns()
    before=resource.getrusage(resource.RUSAGE_CHILDREN)
    result={'stage':'development','status':'running',
            'script_path':str(paths[0].relative_to(ROOT)),
            'script_sha256':versions[str(paths[0].relative_to(ROOT))],
            'dependencies':versions,'python':platform.python_version(),
            'start_utc':datetime.now(timezone.utc).isoformat(),
            'start_monotonic_ns':start_ns,'steps':[],
            'scope':'one prospectively declared CLI example; no final challenge'}

    def command(label,argv,expect_success=True):
        begin=time.monotonic_ns()
        step={'label':label,'argv':argv,'start_utc':datetime.now(timezone.utc).isoformat(),
              'start_monotonic_ns':begin,'expected_success':expect_success}
        proc=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True)
        finish=time.monotonic_ns()
        step.update(returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr,
                    end_utc=datetime.now(timezone.utc).isoformat(),
                    end_monotonic_ns=finish,elapsed_ns=finish-begin)
        result['steps'].append(step)
        assert (proc.returncode==0)==expect_success,step
        return proc

    try:
        generator_args=[sys.executable,str(GENERATOR),'--input',str(request_path),
                        '--output',str(artifact_path)]
        command('generate',generator_args)
        record=json.loads(artifact_path.read_text())
        # This is a separate provenance/input check, not performed by verify().
        assert record['execution']['input_sha256']==digest(request_path)
        assert record['execution']['script_sha256']==versions[str(GENERATOR.relative_to(ROOT))]
        assert record['n_states']==request['n_states']
        assert record['calibration']==request['calibration']
        assert exact_rows(record['losses'])==exact_rows(request['losses'])
        assert exact_rows(record['targets'])==exact_rows(request['targets'])
        result['external_input_binding']='passed: bytes hash and parsed declared problem agree'
        result['input_path']=str(request_path.relative_to(ROOT))
        result['input_sha256']=digest(request_path)
        assert not record['all_targets_recoverable']
        assert not record['full_law_recoverable']
        repair=record['repair']
        assert repair['minimum_extra_raw_queries']==2
        assert exact_rows(repair['extra_loss_rows'])==exact_rows([[1,2,1],[1,1,0]])
        command('independent_arithmetic_verifier',
                [sys.executable,str(VERIFIER),str(artifact_path)])
        cert=repair['repaired_target_certificates'][0]
        assert cert['kind']=='ratio_of_scaled_linear_targets'
        normalizer=[F(x) for x in cert['normalizer_coefficients']]
        numerator=[F(x) for x in cert['numerator_coefficients']]
        all_rows=exact_rows(record['losses']+repair['extra_loss_rows'])
        examples=[]
        for p,scale,offset in [([F(1,2),F(1,4),F(1,4)],F(2),F(0)),
                               ([F(1,2),F(1,8),F(3,8)],F(2),F(1,4))]:
            values=[scale*dot(row,p)+offset for row in all_rows]
            differences=[v-values[0] for v in values[1:]]
            denominator=dot(normalizer,differences)
            decoded=dot(numerator,differences)/denominator
            assert denominator==scale and decoded==p[0]==F(1,2)
            assert values==[F(1,2),F(5,2),F(3,2)]
            examples.append({'p':list(map(str,p)),'scale':str(scale),'offset':str(offset),
                             'raw_values':list(map(str,values)),
                             'decoded_scale':str(denominator),'decoded_target':str(decoded)})
        result['target_examples']=examples
        artifact_hash=digest(artifact_path)
        command('expected_existing_output_refusal',generator_args,expect_success=False)
        assert digest(artifact_path)==artifact_hash
        result['artifact_path']=str(artifact_path.relative_to(ROOT))
        result['artifact_sha256']=artifact_hash
        result['existing_output_preserved']=True
        assert versions=={str(p.relative_to(ROOT)):digest(p) for p in paths}
        result['status']='passed'
    except Exception as exc:
        result['status']='failed'
        result['failure']={'type':type(exc).__name__,'message':str(exc)}
    end_ns=time.monotonic_ns()
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    result.update(end_utc=datetime.now(timezone.utc).isoformat(),
                  end_monotonic_ns=end_ns,elapsed_ns=end_ns-start_ns,
                  child_user_cpu_seconds=after.ru_utime-before.ru_utime,
                  child_system_cpu_seconds=after.ru_stime-before.ru_stime)
    with output.open('x') as stream:
        json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps({k:result[k] for k in ['status','elapsed_ns','child_user_cpu_seconds',
                                          'child_system_cpu_seconds']}))
    if result['status']!='passed':
        print(json.dumps(result['failure']))
        raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
