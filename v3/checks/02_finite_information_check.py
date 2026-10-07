"""Prospectively scoped DEVELOPMENT checks for the exact P3-02 companion.

ChatGPT (GPT-6 Astra Pro), 2026-10-07. This is not a final challenge.
All scientific certificates are checked arithmetically by a separate module.
A binary geometric oracle uses slopes/determinants and exhaustive available
repairs; the three-state corpus checks full explicit certificates, not ranks
against a second copy of the same row-reduction code. No random seeds.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
import platform
import resource
import sys
import time

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
MODES=('known','unknown_offset','unknown_scale','unknown_affine')


def import_path(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def binary_full_law(losses,mode):
    """Independent exact 2-state geometry; no generator or RREF use."""
    m=[[F(v) for v in row] for row in losses]
    if mode in {'unknown_offset','unknown_affine'}:
        m=[[r[0]-m[0][0],r[1]-m[0][1]] for r in m[1:]] if m else []
    if mode in {'known','unknown_offset'}:
        return any(a!=b for a,b in m)
    return any(a[0]*b[1]!=a[1]*b[0] for a,b in combinations(m,2))


def binary_repair_min(losses,mode):
    candidates=[[0,0],[1,0],[0,1]]
    for k in range(4):
        if any(binary_full_law(losses+list(extra),mode) for extra in combinations(candidates,k)):
            return k
    raise AssertionError('The binary reference/indicator menu should suffice.')


def requests():
    # Exact, fully declared finite corpus: 1+27+378 old 3-state row multisets.
    pool=list(product((-1,0,1),repeat=3))
    identity=[[1,0,0],[0,1,0],[0,0,1]]
    targets=(identity,[[1,0,0]],[[0,1,2]],[[1,0,0],[0,1,0]],[[7,7,7]],[])
    for m in range(3):
        for menu in combinations_with_replacement(pool,m):
            for mode in MODES:
                for C in targets:
                    yield 'three_state_certificates',{'n_states':3,'losses':[list(r) for r in menu],
                                                      'targets':C,'calibration':mode},None
    # The binary family has its own independent geometric repair oracle.
    pool=list(product((-1,0,1),repeat=2))
    for m in range(4):
        for menu in combinations_with_replacement(pool,m):
            losses=[list(r) for r in menu]
            for mode in MODES:
                expected={'full_law_recoverable':binary_full_law(losses,mode),
                          'minimum_extra_raw_queries':binary_repair_min(losses,mode)}
                yield 'binary_geometry',{'n_states':2,'losses':losses,'targets':[[1,0]],'calibration':mode},expected
    cases=[
        ('one_state_empty',{'n_states':1,'losses':[],'targets':[[1],[-3]]}),
        ('one_state_duplicate',{'n_states':1,'losses':[[7],[7]],'targets':[[1]]}),
        ('one_state_no_target',{'n_states':1,'losses':[],'targets':[]}),
        ('rational_signed',{'n_states':3,'losses':[['1/2','-2/3','7/5'],['1/4',0,'-1/2']],
                            'targets':[['2/7','-1/5','3/11'],[4,4,4]]}),
        ('brier_anchor',{'n_states':3,'losses':[['2/3','2/3','2/3'],[0,2,2],[2,0,2],[2,2,0]]}),
        ('four_state_basis',{'n_states':4,'losses':[[1,0,0,0],[0,1,0,0],[0,0,1,0]]}),
        ('zero_reference',{'n_states':3,'losses':[[0,0,0]],'targets':[[1,0,0]]}),
        ('partial_target_offset',{'n_states':3,'losses':[[0,1,0],[1,2,1],[1,1,0]],'targets':[[1,0,0]]}),
        ('larger_exact',{'n_states':8,'losses':[[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],
                                              [2,0,0,0,0,0,0,0]],
                         'targets':[[0,0,1,0,0,0,0,0],['1/3','-2/5',0,0,0,0,0,'7/11']]}),
    ]
    for name,request in cases:
        for mode in MODES:
            yield name,dict(request,calibration=mode),None


def run(output):
    if output.exists():
        raise SystemExit('Refusing to overwrite an existing development result.')
    progress=output.with_suffix('.progress.jsonl')
    paths=[Path(__file__).resolve(),HERE/'02_finite_information_audit.py',HERE/'02_finite_information_verify.py']
    versions={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    start_utc=datetime.now(timezone.utc).isoformat()
    start_ns=time.monotonic_ns()
    before=resource.getrusage(resource.RUSAGE_SELF)
    record={'stage':'development','status':'running','script_path':str(paths[0].relative_to(ROOT)),
            'script_sha256':versions[str(paths[0].relative_to(ROOT))],'dependencies':versions,
            'start_utc':start_utc,'start_monotonic_ns':start_ns,'argv':sys.argv,
            'python':platform.python_version(),'corpus':'deterministic fixed finite families; no final evaluation',
            'counts':{},'arithmetic_checks':{},'named_results':{},'expected_input_rejections':0,
            'expected_tamper_rejections':0}
    digest=hashlib.sha256()
    completed=0
    last_request=None
    last_artifact=None
    with progress.open('x') as log:
        log.write(json.dumps({'event':'started','utc':start_utc,'monotonic_ns':start_ns,'versions':versions})+'\n')
        log.flush()
        try:
            core=import_path('p3_02_generator',paths[1])
            check=import_path('p3_02_verifier',paths[2])
            for group,request,expected in requests():
                last_request=request
                last_artifact=core.jsonable(core.audit(request))
                counts=check.verify(last_artifact)
                if expected:
                    assert last_artifact['full_law_recoverable']==expected['full_law_recoverable']
                    assert last_artifact['repair']['minimum_extra_raw_queries']==expected['minimum_extra_raw_queries']
                record['counts'][group]=record['counts'].get(group,0)+1
                for k,v in counts.items():
                    record['arithmetic_checks'][k]=record['arithmetic_checks'].get(k,0)+v
                if group not in {'three_state_certificates','binary_geometry'}:
                    record['named_results'][group+'/'+request['calibration']]=last_artifact
                digest.update(json.dumps(last_artifact,sort_keys=True,separators=(',',':')).encode()+b'\n')
                completed+=1
                if completed%250==0:
                    log.write(json.dumps({'event':'checkpoint','utc':datetime.now(timezone.utc).isoformat(),
                                          'monotonic_ns':time.monotonic_ns(),'completed':completed,
                                          'certificate_digest':digest.hexdigest()})+'\n')
                    log.flush()
            base={'n_states':2,'losses':[],'targets':[[1,0]],'calibration':'known'}
            bad=[dict(base,n_states=0),dict(base,n_states=True),dict(base,losses=None),
                 dict(base,losses=[[0.0,1]]),dict(base,losses=[[True,1]]),
                 dict(base,losses=[[0,1,2]]),dict(base,calibration='arbitrary_monotone'),
                 dict(base,calibration=[]),dict(base,source='restricted'),
                 dict(base,targets=[[1]]),dict(base,losses=[['nan',0]]),dict(base,losses=[['1/0',0]])]
            for request in bad:
                try:
                    core.audit(request)
                except ValueError:
                    record['expected_input_rejections']+=1
                else:
                    raise AssertionError('An unsupported or inexact input was accepted.')
            def artifact(request):
                return core.jsonable(core.audit(request))
            tampered=[]
            positive=artifact({'n_states':2,'losses':[[1,0]],'targets':[[1,0]],'calibration':'known'})
            damaged=deepcopy(positive);damaged['target_certificates'][0]['constant']='1';tampered.append(damaged)
            damaged=deepcopy(positive);damaged['full_law_recoverable']=False;tampered.append(damaged)
            damaged=deepcopy(positive);damaged['all_targets_recoverable']=1;tampered.append(damaged)
            ratio=artifact({'n_states':2,'losses':[[1,0],[0,1]],'targets':[[1,0]],'calibration':'unknown_scale'})
            damaged=deepcopy(ratio);damaged['target_certificates'][0]['normalizer_coefficients']=['0','0'];tampered.append(damaged)
            negative=artifact({'n_states':3,'losses':[[0,1,2]],'targets':[[0,0,1]],'calibration':'unknown_affine'})
            damaged=deepcopy(negative);damaged['target_certificates'][0]['witness']['scale_q']='0';tampered.append(damaged)
            damaged=deepcopy(negative);damaged['target_certificates'][0]['witness']['q']=damaged['target_certificates'][0]['witness']['p'];tampered.append(damaged)
            damaged=deepcopy(negative);damaged['repair']['lower_bound_hidden_directions'][0]=['0']*3;tampered.append(damaged)
            damaged=deepcopy(negative);damaged['repair']['minimum_extra_raw_queries']+=1;tampered.append(damaged)
            damaged=deepcopy(negative);damaged['stage']='final';tampered.append(damaged)
            for candidate in tampered:
                try:
                    check.verify(candidate)
                except (check.InvalidCertificate,KeyError):
                    record['expected_tamper_rejections']+=1
                else:
                    raise AssertionError('A deliberately false certificate was accepted.')
            assert completed==10660,completed  # 9744 + 880 + 9 named groups * 4 modes.
            assert record['expected_input_rejections']==12
            assert record['expected_tamper_rejections']==9
            assert versions=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
            record['status']='passed'
        except Exception as exc:
            record['status']='failed'
            record['failure']={'type':type(exc).__name__,'message':str(exc),
                               'last_request':last_request,'last_artifact':last_artifact}
        end_ns=time.monotonic_ns()
        after=resource.getrusage(resource.RUSAGE_SELF)
        record.update(completed=completed,certificate_digest=digest.hexdigest(),
                      end_utc=datetime.now(timezone.utc).isoformat(),end_monotonic_ns=end_ns,
                      elapsed_ns=end_ns-start_ns,user_cpu_seconds=after.ru_utime-before.ru_utime,
                      system_cpu_seconds=after.ru_stime-before.ru_stime)
        log.write(json.dumps({'event':'completed','status':record['status'],'completed':completed,
                              'utc':record['end_utc'],'monotonic_ns':end_ns,'certificate_digest':digest.hexdigest()})+'\n')
        log.flush()
    with output.open('x') as stream:
        stream.write(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ('status','completed','counts','arithmetic_checks',
                                          'expected_input_rejections','expected_tamper_rejections','elapsed_ns')}))
    if record['status']!='passed':
        print(json.dumps(record['failure']))
        raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    run(args.output)
