"""Retain every optional formal-reconstruction compiler attempt."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for name, digest in json.loads((HERE/'freeze.json').read_text(encoding='utf-8'))['sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
text = (HERE/'Projection.lean').read_text(encoding='utf-8')
assert not re.search(r'\b(sorry|admit|unsafe)\b|^\s*axiom\s', text, re.M)
attempts = HERE/'lean_attempts'
attempts.mkdir(exist_ok=True)
number = 1
while (attempts/f'a{number:02}.lean').exists() or (attempts/f'a{number:02}.json').exists():
    number += 1
source = attempts/f'a{number:02}.lean'
source.write_bytes((HERE/'Projection.lean').read_bytes())
control = json.loads((HERE/'lean_control.tmp').read_text(encoding='utf-8'))
record = dict(attempt=number, source=source.relative_to(ROOT).as_posix(),
              sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              scope_sha256=hashlib.sha256((HERE/'formal_scope.md').read_bytes()).hexdigest(),
              created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              command=['lean', source.relative_to(ROOT).as_posix()], status='STARTED')
path = attempts/f'a{number:02}.json'
path.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
began = time.monotonic_ns()
try:
    result = subprocess.run([control['binary'], str(source)], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8', timeout=60)
    record.update(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr,
                  runtime_ns=time.monotonic_ns()-began,
                  status='PASS' if result.returncode == 0 else 'COMPILER_FAILURE')
except subprocess.TimeoutExpired as error:
    record.update(status='TIMEOUT',runtime_ns=time.monotonic_ns()-began,
                  stdout=str(error.stdout),stderr=str(error.stderr))
path.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:record.get(key) for key in
                  ('attempt','status','exit_code','runtime_ns','source','sha256')}))
