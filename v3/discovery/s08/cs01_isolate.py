"""Preserve completed units and isolate remaining arms after runtime crashes."""
from pathlib import Path
from datetime import datetime,timezone
import json
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE/'cs01'
design=json.loads((ROOT/'design.json').read_text());progress=json.loads((ROOT/'progress.json').read_text())
result=dict(status='running_after_process_isolation',cases=progress['completed'])
def save(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
for case in design['cases'][len(result['cases']):]:
    record=progress['current'] if case['name']==progress['current']['name'] else dict(name=case['name'],arms={})
    for arm in design['arms']:
        if arm in record['arms']:continue
        output=ROOT/f"{case['name']}_{arm}_result.json"
        if output.exists():raise RuntimeError('Existing result needs deliberate recovery')
        begin=datetime.now(timezone.utc).isoformat();clock=time.perf_counter_ns()
        with (ROOT/f"{case['name']}_{arm}_process.txt").open('w') as log:
            proc=subprocess.run([sys.executable,'-X','faulthandler',str(HERE/'cs01_unit.py'),case['name'],arm],stdout=log,stderr=log)
        with (ROOT/'isolated_processes.jsonl').open('a') as log:
            log.write(json.dumps(dict(case=case['name'],arm=arm,begin_utc=begin,end_utc=datetime.now(timezone.utc).isoformat(),
                wall_ns=time.perf_counter_ns()-clock,returncode=proc.returncode,runtime=sys.version))+'\n')
        print(case['name'],arm,proc.returncode,flush=True)
        if proc.returncode:raise RuntimeError('Isolated unit failed; inspect without automatic retry')
        record['arms'][arm]=json.loads(output.read_text())
        save(ROOT/'progress.json',dict(completed=result['cases'],current=record))
    for key in ('base_audit_fee','physical_audits','named_units','learning_samples','stop_before_request','selected_policies'):
        assert record['arms']['learner'][key]==record['arms']['ordinary_learner'][key]
    result['cases'].append(record);save(ROOT/'results.json',result)
result.update(status='complete_after_runtime_amendment_and_process_isolation',completed_utc=datetime.now(timezone.utc).isoformat(),
    failed_prefix_cost='three unknown preparation prefixes; see environment_amendment.json and isolation_amendment.json')
save(ROOT/'results.json',result)
