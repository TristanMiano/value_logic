"""Check F14 raw-byte transport with Git's Windows-style newline setting.

This is a temporary local Git fixture, not a Windows runtime/hardware test or
a project commit. Contributor: ChatGPT (GPT-6 Astra Pro), F14.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

from v2.experiments import freeze as F


def run(args, cwd):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f'{args!r}: {result.returncode}\n{result.stdout}\n{result.stderr}')
    return result.stdout.strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    begin = time.perf_counter()
    paths = F.manifest_paths(F.DEFAULT_CONFIG)
    with tempfile.TemporaryDirectory(prefix='f14-transport-') as directory:
        root = Path(directory); original = root/'source'; clone = root/'clone'
        original.mkdir()
        for path in paths:
            target = original/path.relative_to(F.ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        # A disposable development manifest, not the final project freeze.
        F.create_manifest(destination=original/'v2/experiments/freeze.v1.json')
        run(['git', 'init', '-q'], original)
        run(['git', 'config', 'core.autocrlf', 'true'], original)
        run(['git', 'add', '.'], original)
        run(['git', '-c', 'user.name=F14 transport fixture',
             '-c', 'user.email=f14-fixture@example.invalid', 'commit', '-qm',
             'Disposable raw-byte transport fixture'], original)
        run(['git', '-c', 'core.autocrlf=true', 'clone', '-q', str(original), str(clone)], root)
        attrs = run(['git', 'check-attr', 'text', '--',
                     *[str(p.relative_to(F.ROOT)) for p in paths]], clone)
        assert all(line.endswith(': text: unset') for line in attrs.splitlines()), attrs
        mismatches = [str(p.relative_to(F.ROOT)) for p in paths
                      if sha(p) != sha(clone/p.relative_to(F.ROOT))]
        assert not mismatches, mismatches
        verified = json.loads(run([sys.executable, '-m', 'v2.experiments.freeze', 'verify'], clone))
        assert verified['verified'] is True
        report = {'schema': 'F14-git-byte-transport-development-v1', 'passed': True,
                  'frozen_files_checked': len(paths), 'raw_byte_mismatches': mismatches,
                  'checkout_core_autocrlf': True, 'all_frozen_text_attributes_unset': True,
                  'cloned_manifest_verification': verified,
                  'git_version': run(['git', '--version'], original),
                  'windows_runtime_test': False, 'evaluation_generated': False,
                  'scope': 'fresh Git checkout transport with core.autocrlf=true on current Linux host',
                  'wall_seconds': time.perf_counter()-begin}
        F.write_json(Path(args.out), report, exclusive=True)
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
