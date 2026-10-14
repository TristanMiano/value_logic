"""Environment amendment cs01-env-1: resume only unfinished units under Python 3.12.14."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util
import json
import sys
import traceback

HERE=Path(__file__).resolve().parent
ROOT=HERE/'cs01'
spec=importlib.util.spec_from_file_location('frozen_continuum_service',ROOT/'impl.py')
service=importlib.util.module_from_spec(spec);spec.loader.exec_module(service)
design=json.loads((ROOT/'design.json').read_text());progress=json.loads((ROOT/'progress.json').read_text())
result=dict(status='running',cases=progress['completed'])
try:
    for case in design['cases'][len(result['cases']):]:
        record=progress['current'] if case['name']==progress['current']['name'] else dict(name=case['name'],arms={})
        data=service.source(case['costs']);rows=service.ms.draw(data['n'],case['r'],design['requests'],case['seed'])
        for arm in design['arms']:
            if arm in record['arms']:continue
            if (ROOT/f"{case['name']}_{arm}.jsonl").exists():raise RuntimeError('Unexpected exposed unfinished arm requires disposition')
            print(case['name'],arm,flush=True)
            record['arms'][arm]=service.run_arm(ROOT,case,data,rows,arm)
            service.g01.save(ROOT/'progress.json',dict(completed=result['cases'],current=record))
        for key in ('base_audit_fee','physical_audits','named_units','learning_samples','stop_before_request','selected_policies'):
            assert record['arms']['learner'][key]==record['arms']['ordinary_learner'][key]
        result['cases'].append(record);service.g01.save(ROOT/'results.json',result)
    result.update(status='complete_after_runtime_amendment',completed_utc=datetime.now(timezone.utc).isoformat(),
        failed_prefix_cost='two unknown prefixes; see environment_amendment.json', runtime_amendment='CPython 3.12.14')
    service.g01.save(ROOT/'results.json',result)
except BaseException:
    (ROOT/'resume_failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
    raise
