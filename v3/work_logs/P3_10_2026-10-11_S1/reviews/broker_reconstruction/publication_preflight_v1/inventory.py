"""Read-only publication inventory; writes only its new owned output directory.

No Git index/object/ref mutation, network access, scientific imports, or replay.
The entire output directory is excluded from the inventory to avoid recursion.
"""
import base64
import collections
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import urllib.parse
import zlib

ROOT = Path('/workspace/scratch/095cdac579b7/value_logic')
OUT = Path(__file__).resolve().parent
EXCLUDE = OUT.relative_to(ROOT).as_posix() + '/'
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
COMMANDS = []

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def git(*args):
    start = utc()
    p = subprocess.run(['git', '--no-optional-locks', *args], cwd=ROOT,
                       env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    COMMANDS.append({'argv': ['git', '--no-optional-locks', *args],
                     'start_utc': start, 'end_utc': utc(), 'returncode': p.returncode,
                     'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
                     'stderr': p.stderr.decode('utf-8', 'replace')})
    if p.returncode:
        raise RuntimeError('read-only Git command failed: ' + repr(args))
    return p.stdout

def status():
    raw = git('status', '--porcelain=v1', '-z', '--untracked-files=all')
    cells = raw.split(b'\0')
    result = []
    i = 0
    while i < len(cells):
        row = cells[i]
        i += 1
        if not row:
            continue
        state = row[:2].decode('ascii')
        path = row[3:].decode('utf-8')
        r = {'path': path, 'status': state}
        if 'R' in state or 'C' in state:
            r['old_path'] = cells[i].decode('utf-8')
            i += 1
        if not path.startswith(EXCLUDE):
            result.append(r)
    return sorted(result, key=lambda x: x['path'])

def binding(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}

def save(name, obj):
    with (OUT / name).open('x', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')

started = utc()
head_before = git('rev-parse', 'HEAD').decode().strip()
baseline = {}
for row in git('ls-tree', '-r', '-z', '--full-tree', 'HEAD').split(b'\0'):
    if not row:
        continue
    meta, path = row.split(b'\t', 1)
    mode, typ, oid = meta.decode().split()
    baseline[path.decode('utf-8')] = {'mode': mode, 'type': typ, 'git_oid': oid}
baseline_blobs = {r['git_oid'] for r in baseline.values() if r['type'] == 'blob'}
before = status()
files = []
issues = []
unique = {}
for item in before:
    p = ROOT / item['path']
    row = dict(item)
    row['baseline'] = baseline.get(item['path'])
    try:
        s0 = p.lstat()
        if stat.S_ISREG(s0.st_mode):
            raw = p.read_bytes()
            mode = '100755' if s0.st_mode & 0o111 else '100644'
            typ = 'regular'
        elif stat.S_ISLNK(s0.st_mode):
            raw = os.readlink(p).encode('utf-8')
            mode = '120000'
            typ = 'symlink'
        else:
            issues.append({'path': item['path'], 'issue': 'nonregular path'})
            files.append(row)
            continue
        s1 = p.lstat()
        stable = (s0.st_size, s0.st_mtime_ns, s0.st_ino, s0.st_mode) == (
            s1.st_size, s1.st_mtime_ns, s1.st_ino, s1.st_mode)
        oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        row.update({'type': typ, 'mode': mode, 'bytes': len(raw),
                    'mtime_ns': s1.st_mtime_ns, 'sha256': hashlib.sha256(raw).hexdigest(),
                    'git_oid': oid, 'exists_in_base_tree': oid in baseline_blobs,
                    'stable_during_read': stable})
        if not stable:
            issues.append({'path': item['path'], 'issue': 'changed during read'})
        if oid not in unique:
            try:
                content = raw.decode('utf-8')
                utf8 = True
                # Exact payload-only serialized string sizes; tree metadata adds overhead.
                json_chars = len(json.dumps(content, ensure_ascii=False))
                json_bytes = len(json.dumps(content, ensure_ascii=False).encode('utf-8'))
            except UnicodeDecodeError:
                utf8 = False
                json_chars = json_bytes = None
            unique[oid] = {'git_oid': oid, 'sha256': row['sha256'], 'bytes': len(raw),
                           'representative_path': item['path'], 'path_count': 0,
                           'exists_in_base_tree': oid in baseline_blobs,
                           'utf8': utf8, 'json_content_chars': json_chars,
                           'json_content_utf8_bytes': json_bytes,
                           'base64_chars': 4 * ((len(raw) + 2) // 3),
                           'independent_zlib_level6_bytes': len(zlib.compress(raw, 6))}
        unique[oid]['path_count'] += 1
    except FileNotFoundError:
        row['missing'] = True
        if 'D' not in item['status']:
            issues.append({'path': item['path'], 'issue': 'missing during read'})
    files.append(row)

after = status()
head_after = git('rev-parse', 'HEAD').decode().strip()
if before != after:
    before_by = {r['path']: r for r in before}
    after_by = {r['path']: r for r in after}
    issues.append({'issue': 'status path/state set changed during scan',
                   'added': sorted(after_by.keys() - before_by.keys()),
                   'removed': sorted(before_by.keys() - after_by.keys()),
                   'changed': sorted(p for p in before_by.keys() & after_by.keys()
                                     if before_by[p] != after_by[p])})
if head_before != head_after:
    issues.append({'issue': 'HEAD changed during scan'})
for row in files:
    if 'mtime_ns' not in row:
        continue
    try:
        current = (ROOT / row['path']).lstat()
        if (current.st_mtime_ns, current.st_size) != (row['mtime_ns'], row['bytes']):
            issues.append({'path': row['path'], 'issue': 'changed after its read before scan end'})
    except FileNotFoundError:
        issues.append({'path': row['path'], 'issue': 'removed after read'})

new = [r for r in unique.values() if not r['exists_in_base_tree']]
groups = collections.defaultdict(lambda: {'paths': 0, 'bytes': 0})
for row in files:
    p = row['path']
    if p.startswith('v3/experiments/final_v1/'):
        group = 'v3/experiments/final_v1/'
    elif p.startswith('v3/experiments/final_v1_amended_A1/'):
        group = 'v3/experiments/final_v1_amended_A1/'
    elif p.startswith('v3/experiments/amendments/'):
        group = 'v3/experiments/amendments/'
    elif p.startswith('v3/work_logs/P3_10_2026-10-11_S1/'):
        parts = p.split('/')
        group = '/'.join(parts[:4]) + ('/' if len(parts) > 4 else '')
    else:
        group = p
    groups[group]['paths'] += 1
    groups[group]['bytes'] += row.get('bytes', 0)

summary = {
    'schema': 'value_logic.P3-10.read_only_publication_inventory.v1',
    'reviewer': '/root/freeze_review', 'principal_research_credit_ns': 0,
    'started_utc': started, 'completed_utc': utc(), 'repository': str(ROOT),
    'head_before': head_before, 'head_after': head_after,
    'scope': 'Current Git-reported modified, staged and untracked nonignored paths; own preflight directory excluded. Point-in-time and not final closure.',
    'excluded_prefix': EXCLUDE,
    'ignored_files_policy': 'Not inventoried as publishable by default; no ignore rules changed.',
    'status_counts': dict(collections.Counter(r['status'] for r in files)),
    'changed_or_new_paths': len(files), 'total_bytes': sum(r.get('bytes', 0) for r in files),
    'base_tracked_paths': len(baseline), 'base_unique_blob_oids': len(baseline_blobs),
    'changed_unique_blob_count': len(unique),
    'changed_unique_blob_bytes': sum(r['bytes'] for r in unique.values()),
    'reused_base_unique_blob_count': sum(r['exists_in_base_tree'] for r in unique.values()),
    'reused_base_path_count': sum(r.get('exists_in_base_tree', False) for r in files),
    'new_unique_blob_count': len(new), 'new_unique_blob_bytes': sum(r['bytes'] for r in new),
    'new_unique_utf8_blob_count': sum(r['utf8'] for r in new),
    'new_unique_nonutf8_blob_count': sum(not r['utf8'] for r in new),
    'new_unique_base64_chars': sum(r['base64_chars'] for r in new),
    'new_unique_zlib_level6_bytes': sum(r['independent_zlib_level6_bytes'] for r in new),
    'zlib_caveat': 'Independent blob compression estimate only, not a Git pack size or transport measurement.',
    'new_unique_files_ge_1MiB': sum(r['bytes'] >= 2**20 for r in new),
    'new_unique_files_ge_10MiB': sum(r['bytes'] >= 10 * 2**20 for r in new),
    'new_unique_files_ge_50MiB': sum(r['bytes'] >= 50 * 2**20 for r in new),
    'new_unique_files_ge_100MiB': sum(r['bytes'] >= 100 * 2**20 for r in new),
    'sha_only_tree_batches_at_128_paths': (len(files) + 127) // 128,
    'groups': dict(sorted(groups.items())),
    'largest_new_unique_blobs': sorted(new, key=lambda r: (-r['bytes'], r['git_oid']))[:25],
    'issues': issues, 'path_state_snapshot_stable': before == after,
    'head_stable': head_before == head_after,
    'read_only_commands': COMMANDS,
}
save('inventory.json', {'summary': summary, 'files': files,
                         'unique_blobs': sorted(unique.values(), key=lambda r: r['git_oid'])})
save('summary.json', summary)
save('status_before.json', before)
save('status_after.json', after)
save('baseline_paths.json', baseline)
print(json.dumps({k: v for k, v in summary.items() if k not in ('read_only_commands', 'largest_new_unique_blobs', 'groups')}, indent=2))
print('GROUPS', json.dumps(summary['groups']))
print('LARGEST', json.dumps(summary['largest_new_unique_blobs'][:12], indent=2))
