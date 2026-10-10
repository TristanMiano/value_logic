#!/usr/bin/env python3
"""Read-only baseline/blob and completed-artifact preservation observer.

Contributor: ChatGPT (GPT-6 Astra Pro), October 10, 2026. Administration.
No worker/checker imports or executions; no git mutation; zero clock credit.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import os
import stat
import subprocess
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
SESSION = ROOT / 'v3/work_logs/R_P3_B_B_2026-10-10_S1'
BASE = '33c6d6795aac894bd3cf8575e44f1d6f38f6ae56'
TREE = '0dbec24dfc68172a31aaa4a524fd5d1f2c199b67'
ALLOWED = frozenset(('TODO_v3.md', 'v3/plan.v1.json', 'v3/README.md',
                     'v3/claim_ledger.md', 'v3/time_ledger.csv'))
RUNS = {
    'primary_v5': (317, '555d0af18e958053f06b14940e6a725d28514877191a0982d976c91eb210254e'),
    'secondary_pruning_v1': (148, '76d3f28bf30edee6e19e5edbdff6a7bb0927032744dd54bf5bd57005c33f90b1'),
    'actual_consumer_cap_v1': (288, '01e88137a200c02385f1039fb146083780bf66a76900dee62f67d655460ccd4f'),
    'rational_service_v1_retry1': (30, '13dd3b33ca4dafbb287f9f2e61d452517eae42a6b5e7014fe855d20352e630e8')}
EXCEPTION_DIGEST = 'df3e500eac31c649b9afa3fc285b3d5428ed157ced94e2a63c462ff6bc92f69f'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, sort_keys=True, indent=2) + '\n').encode('ascii'))


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout


def ledger_report():
    base = git('show', BASE + ':v3/time_ledger.csv')
    current = (ROOT / 'v3/time_ledger.csv').read_bytes()
    prefix = current.startswith(base)
    result = {'baseline_bytes': len(base), 'current_bytes': len(current),
        'baseline_sha256': sha(base), 'current_sha256': sha(current),
        'baseline_is_exact_byte_prefix': prefix, 'append_present': len(current) > len(base),
        'baseline_ends_with_newline': base.endswith(b'\n')}
    if prefix:
        before = list(csv.reader(io.StringIO(base.decode('utf-8'))))
        after = list(csv.reader(io.StringIO(current.decode('utf-8'))))
        appended = after[len(before):]
        result.update(header=before[0], baseline_data_rows=len(before) - 1,
            current_data_rows=len(after) - 1, appended_rows=len(appended),
            appended_task_ids=sorted({r[0] for r in appended}),
            appended_rows_match_header_width=all(len(r) == len(before[0]) for r in appended),
            baseline_csv_rows_preserved=after[:len(before)] == before,
            appended_suffix_sha256=sha(current[len(base):]))
    return result


def baseline_scan(out):
    require(git('rev-parse', '--show-object-format').strip() == b'sha1', 'Unexpected git format.')
    require(git('rev-parse', BASE + '^{tree}').strip().decode('ascii') == TREE, 'Base tree mismatch.')
    entries = []
    for raw in git('ls-tree', '-r', '-z', '--full-tree', BASE).split(b'\0'):
        if raw:
            meta, name = raw.split(b'\t', 1)
            mode, kind, oid = meta.decode('ascii').split()
            require(kind == 'blob', 'Non-blob baseline entry needs explicit handling.')
            entries.append((mode, oid, os.fsdecode(name)))
    require(len(entries) == 5659 and len({p for _, _, p in entries}) == 5659, 'Baseline file count.')
    proc = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    records = []
    try:
        for mode, oid, name in entries:
            proc.stdin.write((oid + '\n').encode('ascii'))
            proc.stdin.flush()
            header = proc.stdout.readline().decode('ascii').strip().split()
            require(len(header) == 3 and header[:2] == [oid, 'blob'], 'Malformed git object response.')
            size = int(header[2])
            path = ROOT / name
            exists = path.exists() or path.is_symlink()
            current = None
            actual_mode = None
            if exists:
                info = path.lstat()
                if stat.S_ISLNK(info.st_mode):
                    current = io.BytesIO(os.fsencode(os.readlink(path)))
                    actual_mode = '120000'
                elif stat.S_ISREG(info.st_mode):
                    current = path.open('rb')
                    actual_mode = '100755' if info.st_mode & 0o111 else '100644'
            left_hash, right_hash = hashlib.sha256(), hashlib.sha256()
            same, remaining, actual_bytes = current is not None, size, 0
            while remaining:
                amount = min(remaining, 1024 * 1024)
                old = proc.stdout.read(amount)
                require(len(old) == amount, 'Truncated base object.')
                now = b'' if current is None else current.read(amount)
                left_hash.update(old)
                right_hash.update(now)
                actual_bytes += len(now)
                same = same and old == now
                remaining -= amount
            if current is not None:
                while extra := current.read(1024 * 1024):
                    same = False
                    right_hash.update(extra)
                    actual_bytes += len(extra)
                current.close()
            require(proc.stdout.read(1) == b'\n', 'Malformed base-object delimiter.')
            records.append({'path': name, 'base_blob': oid, 'base_mode': mode,
                'current_mode': actual_mode, 'base_bytes': size, 'current_bytes': actual_bytes if exists else None,
                'base_sha256': left_hash.hexdigest(),
                'current_sha256': right_hash.hexdigest() if current is not None else None,
                'exists': exists, 'byte_identical': same, 'mode_identical': mode == actual_mode,
                'permitted_content_edit': name in ALLOWED})
        proc.stdin.close()
        require(proc.wait(timeout=30) == 0, 'Base object reader failed.')
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
    missing = [r['path'] for r in records if not r['exists']]
    changed = [r['path'] for r in records if not r['byte_identical']]
    unexpected = [p for p in changed if p not in ALLOWED]
    modes = [r['path'] for r in records if not r['mode_identical']]
    result = {'base_commit': BASE, 'base_tree': TREE, 'tracked_files': len(records),
        'comparison': 'Literal chunk-by-chunk working bytes versus git cat-file base blob bytes.',
        'permitted_paths': sorted(ALLOWED), 'changed_paths': changed,
        'missing_paths': missing, 'unexpected_changed_paths': unexpected,
        'mode_changes': modes,
        'protected_paths': len(records) - len(ALLOWED),
        'protected_byte_identical': sum(r['byte_identical'] for r in records if r['path'] not in ALLOWED),
        'p308_session_paths_preserved': sum(r['byte_identical'] for r in records
            if r['path'].startswith('v3/work_logs/P3_08_2026-10-10_S1')),
        'base_content_bytes': sum(r['base_bytes'] for r in records), 'records': records}
    save(out / 'baseline_blobs.json', result)
    require(not missing and not unexpected and not modes, 'Baseline preservation violation; see per-path report.')
    return result


def source_copies(directory, manifest, summary):
    require(manifest['source_hashes'] == summary['source_hashes'], 'Source declarations disagree.')
    records = []
    for relative, expected in manifest['source_hashes'].items():
        raw = (directory / 'sources' / relative).read_bytes()
        live = (ROOT / relative).read_bytes()
        require(sha(raw) == expected, 'Captured source changed: ' + relative)
        require(raw == live, 'Live source/input differs from preserved run copy: ' + relative)
        records.append({'path': relative, 'bytes': len(raw), 'sha256': expected, 'live_byte_equal': True})
    for row in json.loads(manifest['worker_source_record'])['sources']:
        raw = (directory / 'sources' / row['path']).read_bytes()
        require(sha(raw) == row['sha256'] and len(raw) == row['bytes'], 'Worker source record mismatch.')
    return records


def complete_run(name, count, expected):
    directory = SESSION / 'development' / name
    summary_raw = (directory / 'summary.json').read_bytes()
    summary = json.loads(summary_raw)
    require(summary['status'] == 'PASS' and summary['units'] == count, 'Incomplete run: ' + name)
    manifest_raw = (directory / 'manifest.json').read_bytes()
    manifest = json.loads(manifest_raw)
    units_raw = (directory / 'completed_units.jsonl').read_bytes()
    require(sha(manifest_raw) == summary['manifest_sha256'], 'Manifest seal changed: ' + name)
    require(sha(units_raw) == summary['completed_units_sha256'] == expected, 'Unit seal changed: ' + name)
    units = [json.loads(line) for line in units_raw.splitlines()]
    require(len(units) == count, 'Unit count changed: ' + name)
    statuses = Counter(row['status'] for row in units)
    require(statuses['DELIVERED'] == summary['counts']['delivered']
            and statuses['NO_CURRENT_CERTIFICATE'] == summary['counts']['failed_delivery'],
            'Outcome counts disagree: ' + name)
    sources = source_copies(directory, manifest, summary)
    packets, references = {}, 0
    for row in units:
        for ref in row.get('observed_packet_references', []):
            require(ref['path'] == 'blobs/' + ref['sha256'] + '.json', 'Unexpected packet path.')
            if ref['path'] not in packets:
                raw = (directory / ref['path']).read_bytes()
                require(sha(raw) == ref['sha256'], 'Packet changed: ' + name + '/' + ref['path'])
                packets[ref['path']] = len(raw)
            require(packets[ref['path']] == ref['bytes'], 'Packet length changed.')
            references += 1
    return {'run': name, 'status': 'PASS', 'units': len(units), 'unit_status_counts': dict(statuses),
        'unit_bytes': len(units_raw), 'units_sha256': sha(units_raw),
        'summary_sha256': sha(summary_raw), 'manifest_sha256': sha(manifest_raw),
        'source_copies': sources, 'unique_packet_files': len(packets), 'packet_references': references}


def preserved_exception():
    original = SESSION / 'development/rational_service_v1'
    observed = SESSION / 'reviews/receiver_reconstruction/synthesis_review_v1'
    units_raw = (original / 'completed_units.jsonl').read_bytes()
    summary_raw = (original / 'summary.json').read_bytes()
    summary = json.loads(summary_raw)
    manifest_raw = (original / 'manifest.json').read_bytes()
    manifest = json.loads(manifest_raw)
    copy_units = observed / ('observed_rational_completed_units_' + EXCEPTION_DIGEST + '.jsonl')
    copy_summary = observed / 'observed_rational_summary.json'
    note = json.loads((observed / 'rational_integrity_observation_v1.json').read_bytes())
    actual_count = len(units_raw.splitlines())
    require(actual_count == 29 and sha(units_raw) == EXCEPTION_DIGEST, 'Original exception changed.')
    require(summary['units'] == 30 and summary['completed_units_sha256'] != EXCEPTION_DIGEST,
            'Original mismatch was repaired or replaced.')
    require(sha(manifest_raw) == summary['manifest_sha256'], 'Original manifest changed.')
    require(copy_units.read_bytes() == units_raw and copy_summary.read_bytes() == summary_raw,
            'Synthesis observation copies differ from preserved originals.')
    require(note['observed_rows'] == 29 and note['observed_sha256'] == EXCEPTION_DIGEST
            and note['declared_rows'] == 30 and note['declared_sha256'] == summary['completed_units_sha256']
            and note['classification'] == 'EVIDENCE_DIGEST_AND_COUNT_MISMATCH', 'Observation note changed.')
    sources = source_copies(original, manifest, summary)
    return {'status': 'DOCUMENTED_EXCEPTION_PRESERVED', 'run': 'rational_service_v1',
        'observed_units': actual_count, 'observed_bytes': len(units_raw),
        'observed_units_sha256': sha(units_raw), 'summary_declared_units': summary['units'],
        'summary_declared_units_sha256': summary['completed_units_sha256'],
        'summary_sha256': sha(summary_raw), 'manifest_sha256': sha(manifest_raw),
        'source_copies': sources, 'observation_copies_byte_identical': True,
        'observation_note_sha256': sha((observed / 'rational_integrity_observation_v1.json').read_bytes()),
        'completed_30_unit_evidence': False, 'repaired_or_edited': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--ledger-only', action='store_true')
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / 'audit.py').write_bytes(Path(__file__).read_bytes())
    (out / 'plan.md').write_bytes((HERE / 'plan.md').read_bytes())
    report = {'stage': 'ADMINISTRATIVE_OBSERVER', 'clock_credit': 0,
              'worker_or_checker_executions': 0, 'created_utc': datetime.now(timezone.utc).isoformat(),
              'base_commit': BASE, 'base_tree': TREE, 'reader_sha256': sha(Path(__file__).read_bytes())}
    try:
        if not args.ledger_only:
            baseline = baseline_scan(out)
            report['baseline'] = {k: v for k, v in baseline.items() if k != 'records'}
            report['completed_runs'] = [complete_run(name, *values) for name, values in RUNS.items()]
            report['documented_exception'] = preserved_exception()
        ledger = ledger_report()
        report['ledger'] = ledger
        require(ledger['baseline_is_exact_byte_prefix'], 'Baseline ledger is not an exact byte prefix.')
        require(ledger['baseline_csv_rows_preserved'] and ledger['appended_rows_match_header_width'],
                'Ledger CSV schema or prior rows changed.')
        report['status'] = ('PASS_WITH_DOCUMENTED_EXCEPTION' if ledger['append_present']
                            else 'PASS_PRESERVATION_LEDGER_APPEND_PENDING')
        if args.ledger_only:
            report['status'] = 'PASS_LEDGER_PREFIX_AND_APPEND' if ledger['append_present'] else 'LEDGER_APPEND_PENDING'
    except BaseException as failure:
        report['status'] = 'FAIL'
        report['error'] = {'type': type(failure).__name__, 'message': str(failure),
                           'traceback': traceback.format_exc()}
    save(out / 'audit.json', report)
    save(out / 'files.sha256.json', {p.name: sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()})
    concise = {k: v for k, v in report.items() if k not in ('completed_runs', 'documented_exception')}
    if 'completed_runs' in report:
        concise['completed_runs'] = [{k: v for k, v in r.items() if k != 'source_copies'}
                                     for r in report['completed_runs']]
    if 'documented_exception' in report:
        concise['documented_exception'] = {k: v for k, v in report['documented_exception'].items()
                                           if k != 'source_copies'}
    print(json.dumps(concise, sort_keys=True))
    if report['status'] == 'FAIL':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
