"""One bounded DEVELOPMENT extension; preserves prior frozen probe sources."""
from pathlib import Path
import hashlib
import json
import sys
import time
from variable_probe import expected_oracle, recurrence

HERE=Path(__file__).resolve().parent


def main():
    start=time.perf_counter_ns()
    n,cap=5,3
    row=expected_oracle(n,cap,0,False,state_cap=60000)
    r,_=recurrence(n,cap)
    row.update(n=n,cap=cap,overhead=0,target='parity',prefix_mean=str(n+r))
    result=dict(status='COMPLETED',contributor='Codex (GPT-6)',scope='DEVELOPMENT',
                python=sys.version,elapsed_ns=time.perf_counter_ns()-start,
                hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                        for name in ['prefix_extension.py','variable_probe.py','parity_price_probe.py']},
                result=row,
                limitations='Single bounded oracle screen. State-cap completion is inconclusive, '
                'not a failed scientific assertion or support for all-size optimality.')
    (HERE/'prefix_extension.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
