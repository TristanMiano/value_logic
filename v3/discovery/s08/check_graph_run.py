"""Cold per-case reconstruction; all failed attempts remain in log files."""
from pathlib import Path
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent
for series in('gs01','gs02'):
    for case in json.loads((HERE/series/'design.json').read_text())['cases']:
        for attempt in range(1,5):
            with(HERE/series/f"{case['name']}_check{attempt}.txt").open('w') as out:
                code=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',str(HERE/'check_graph_services.py'),series,case['name']],stdout=out,stderr=out).returncode
            print(series,case['name'],attempt,code,flush=True)
            if code==0:break
        else:raise RuntimeError('Repeated reconstruction failure')
