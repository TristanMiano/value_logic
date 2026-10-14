"""Versioned confidence-only ablation of frozen cs01, isolated by arm.
DEVELOPMENT, Codex (GPT-6), 2026-10-14.
"""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util
import json
import subprocess
import sys
import time
import g01
import mixture_interval as mi

HERE=Path(__file__).resolve().parent
ROOT=HERE/'mi02'
spec=importlib.util.spec_from_file_location('frozen_cs',HERE/'cs01/impl.py')
service=importlib.util.module_from_spec(spec);spec.loader.exec_module(service)
service.base.confidence=mi.confidence
service.VERSION='s08-continuum-mixture-service-v2'


def child(name,arm):
    design=json.loads((ROOT/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==name)
    assert arm in design['arms'] and not(ROOT/f'{name}_{arm}.jsonl').exists()
    data=service.source(case['costs']);rows=service.ms.draw(data['n'],case['r'],1024,case['seed'])
    result=service.run_arm(ROOT,case,data,rows,arm);g01.save(ROOT/f'{name}_{arm}_result.json',result)


def parent():
    ROOT.mkdir(exist_ok=False);(ROOT/'impl.py').write_bytes(Path(__file__).read_bytes())
    prior=json.loads((HERE/'cs01/design.json').read_text());design={**prior,'version':service.VERSION,'arms':['learner','ordinary_learner'],
        'source_sha256':g01.sha(__file__),'declaration_sha256':g01.sha(HERE/'mixture_interval.md'),
        'confidence_sha256':g01.sha(HERE/'mixture_interval.py'),'frozen_service_sha256':g01.sha(HERE/'cs01/impl.py'),
        'created_utc':datetime.now(timezone.utc).isoformat(),'exposure':'Same exposed cs01 rows; confidence-only ablation'}
    g01.save(ROOT/'design.json',design);result=dict(status='running',cases=[])
    for case in design['cases']:
        record=dict(name=case['name'],arms={})
        for arm in design['arms']:
            success=False
            for attempt in range(1,5):
                # A partial action trace needs a deliberate disposition, not automatic replacement.
                if (ROOT/f"{case['name']}_{arm}.jsonl").exists():raise RuntimeError('Partial exposed arm; preserve and inspect')
                begin=datetime.now(timezone.utc).isoformat();clock=time.perf_counter_ns()
                with (ROOT/f"{case['name']}_{arm}_attempt{attempt}.txt").open('w') as log:
                    proc=subprocess.run([sys.executable,'-X','faulthandler',__file__,'child',case['name'],arm],stdout=log,stderr=log)
                with (ROOT/'processes.jsonl').open('a') as log:
                    log.write(json.dumps(dict(case=case['name'],arm=arm,attempt=attempt,begin_utc=begin,
                        elapsed_ns=time.perf_counter_ns()-clock,returncode=proc.returncode,python=sys.version))+'\n')
                if proc.returncode==0:success=True;break
                print('Preserved failed process',case['name'],arm,attempt,proc.returncode,flush=True)
            if not success:raise RuntimeError('Repeated unit failure; inspect')
            record['arms'][arm]=json.loads((ROOT/f"{case['name']}_{arm}_result.json").read_text())
            g01.save(ROOT/'progress.json',dict(completed=result['cases'],current=record))
        for key in ('base_audit_fee','physical_audits','named_units','learning_samples','stop_before_request','selected_policies'):
            assert record['arms']['learner'][key]==record['arms']['ordinary_learner'][key]
        result['cases'].append(record);g01.save(ROOT/'results.json',result)
        print(case['name'],record['arms']['learner']['base_audit_fee'],record['arms']['learner']['learning_samples'],flush=True)
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat());g01.save(ROOT/'results.json',result)


if __name__=='__main__':
    if len(sys.argv)>1:child(sys.argv[2],sys.argv[3])
    else:parent()
