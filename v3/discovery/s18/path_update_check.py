"""Small s18 DEVELOPMENT check of the ordinary edge-increase identity."""
from pathlib import Path
import hashlib
import json
import platform
import random
import time

started = time.perf_counter_ns()
rng = random.Random(1820)
infinity = float('inf')
updates = scans = 0
for d in range(2,9):
    for case in range(20):
        c = [[0 if i != j else infinity for j in range(d)] for i in range(d)]
        p = [row[:] for row in c]
        for step in range(25):
            a,b = rng.sample(range(d),2)
            c[a][b] += rng.randrange(1,4)
            before_a = [p[i][a] for i in range(d)]
            before_b = p[b][:]
            for i in range(d):
                for j in range(d):
                    p[i][j] = max(p[i][j],min(before_a[i],c[a][b],before_b[j]))
                    scans += 1
            full = [row[:] for row in c]
            for k in range(d):
                for i in range(d):
                    for j in range(d):
                        full[i][j] = max(full[i][j],min(full[i][k],full[k][j]))
            assert p == full
            updates += 1
result = dict(status='PASS',attribution='Codex (GPT-6), DEVELOPMENT, same-model',
              python=platform.python_version(),elapsed_ns=time.perf_counter_ns()-started,
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              traces=140,edge_updates=updates,incremental_entry_updates=scans,
              limitation='Ordinary algorithm identity screen, not a speed benchmark or independent confirmation.')
with Path(__file__).with_name('path_update_result.json').open('x',encoding='utf-8') as out:
    json.dump(result,out,indent=2)
print(json.dumps(result))
