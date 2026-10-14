from pathlib import Path
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE/'fs01'
for case in json.loads((ROOT/'design.json').read_text())['cases']:
    for attempt in range(1,5):
        with(ROOT/f"{case['name']}_check{attempt}.txt").open('w') as out:
            code=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',str(HERE/'check_fs01.py'),case['name']],stdout=out,stderr=out).returncode
        print(case['name'],attempt,code,flush=True)
        if code==0:break
    else:raise RuntimeError('Repeated checking failure')
