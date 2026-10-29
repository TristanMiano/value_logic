"""Administrative optional tool setup from an official, digest-pinned release.

Installs only inside a new temporary directory; does not change PATH or the
user's toolchain. Binaries are not repository evidence or research output.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
import time
import urllib.request

HERE = Path(__file__).resolve().parent
URL = 'https://github.com/leanprover/lean4/releases/download/v4.35.0/lean-4.35.0-windows.tar.zst'
EXPECTED = '893fde3f52b48c647e3edcf33844cbb61f8ef70fcd88e0536bfc83f29844081e'

if (HERE / 'lean_control.tmp').exists():
    raise RuntimeError('A local installation record already exists; inspect it rather than replace it')
began = time.monotonic_ns()
root = Path(tempfile.mkdtemp(prefix='vl-lean435-')).resolve()
archive = root / 'lean.tar.zst'
with urllib.request.urlopen(URL, timeout=60) as response, archive.open('xb') as output:
    while chunk := response.read(1024 * 1024):
        output.write(chunk)
digest = hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest()
assert digest == EXPECTED, 'Official GitHub release digest mismatch'
listing = subprocess.run(['tar', '-tf', str(archive)], capture_output=True, text=True, check=True)
for member in listing.stdout.splitlines():
    target = (root / member).resolve()
    assert target.is_relative_to(root), 'Archive path escapes new temporary directory'
subprocess.run(['tar', '-xf', str(archive), '-C', str(root)], check=True)
binary = root / 'lean-4.35.0-windows/bin/lean.exe'
version = subprocess.run([str(binary), '--version'], capture_output=True, text=True, check=True)
(HERE / 'lean_control.tmp').write_text(json.dumps({'root':str(root),'binary':str(binary)},indent=2)+'\n',encoding='utf-8')
(HERE / 'lean_environment.json').write_text(json.dumps({
    'source':URL,'archive_sha256':digest,'archive_bytes':archive.stat().st_size,
    'version':version.stdout.strip(),'setup_elapsed_ns':time.monotonic_ns()-began,
    'note':'Administrative installation in a new local temporary directory; no research credit; no PATH change.'
},indent=2)+'\n',encoding='utf-8')
print(version.stdout.strip())
