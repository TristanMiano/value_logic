"""Small DEVELOPMENT algebra screen; Codex (GPT-6), 2026-10-22.

No empirical workload claim. Output is immutable after the first execution.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform
import sys
import time

HERE = Path(__file__).resolve().parent
OUT = HERE / 'reliance_probe.json'
assert not OUT.exists(), 'Preserve an executed result; use a new version for a changed probe.'
start_ns = time.perf_counter_ns()
started = datetime.now(timezone.utc).isoformat()
panels = 0
worst = []
for lam in [F(1, 100), F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(1)]:
    factor = (1 + lam)**2 / (4 * lam)
    max_seen = F(0)
    for denominator in range(1, 24):
        for qnum in range(denominator + 1):
            q = F(qnum, denominator)
            for cnum in range(qnum, denominator + 1):
                c = F(cnum, denominator)
                p = min(F(1), lam/q) if q else F(1)
                correct = 1-p+p*c
                adverse = 1+p*q
                assert adverse <= 1+lam
                assert correct <= factor*c
                if c:
                    max_seen = max(max_seen, correct/c)
                panels += 1
    q = 2*lam/(1+lam)
    p = lam/q
    correct = 1-p+p*q
    adverse = 1+p*q
    assert correct/q == factor
    assert adverse == 1+lam
    worst.append(dict(lambda_=str(lam), q=str(q), p=str(p),
                      correct_fee=str(correct), adverse_fee=str(adverse),
                      exact_ratio=str(factor), maximum_grid_ratio=str(max_seen)))
result = dict(status='PASS', label='DEVELOPMENT, same-model finite algebra screen',
              contributor='Codex (GPT-6)', started_utc=started,
              ended_utc=datetime.now(timezone.utc).isoformat(),
              runtime_ns=time.perf_counter_ns()-start_ns,
              python=sys.version, platform=platform.platform(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              panels=panels, one_bit_equalities=worst,
              scope='Abstract certificate fee panels; not a full service or runtime comparison.')
OUT.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(result, indent=2))
