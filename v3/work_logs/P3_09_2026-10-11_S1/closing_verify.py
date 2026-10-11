"""Administrative P3-09 closure verification; no scientific worker is executed.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11. Run after stopped accounting.
The official verify command reads the prepared freeze; it does not run stages.
"""
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import csv
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    entry = json.loads((HERE / 'entry_manifest.json').read_text())
    actuals = json.loads((HERE / 'actuals.json').read_text())
    plan = json.loads((ROOT / 'v3/plan.v1.json').read_text())
    assert json.loads((HERE / 'clock_state.json').read_text()) is None
    protected = [f for f in entry['files'] if f['path'] not in entry['allowed_existing_edits']]
    for item in protected:
        path = ROOT / item['path']
        assert path.is_file() or path.is_symlink(), item['path']
        data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
        oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        mode = '120000' if path.is_symlink() else ('100755' if path.stat().st_mode & 0o111 else '100644')
        assert oid == item['git_sha'] and mode == item['mode'], item['path']
    assert len(entry['files']) == 7998 and len(protected) == 7993
    ledger = (ROOT / 'v3/time_ledger.csv').read_bytes()
    original = subprocess.check_output(['git', 'show', entry['base_commit'] + ':v3/time_ledger.csv'], cwd=ROOT)
    appended = (HERE / 'ledger_append.csv').read_bytes()
    assert ledger == original + appended
    assert len(original) == entry['ledger']['bytes'] == 192395
    assert digest(original) == entry['ledger']['sha256'] == actuals['ledger']['base_sha256']
    assert digest(ledger) == actuals['ledger']['result_sha256']
    assert digest(appended) == actuals['ledger']['append_sha256']
    rows = list(csv.DictReader(io.StringIO(ledger.decode())))
    research_ns = sum(int(Decimal(r['engaged_seconds']) * 1_000_000_000)
                      for r in rows if r['mode'] in ('D', 'L', 'E'))
    assert research_ns == actuals['phase_research_ns'] == 59_750_867_877_502
    current = {c['id']: c for c in plan['chunks']}
    assert current['P3-09']['status'] == 'complete' and current['P3-10']['status'] == 'unstarted'
    assert plan['next_task'] == 'P3-10' and plan['active_session'] is None
    assert plan['experimental_freeze_created'] and not plan['final_evaluation_exposed']
    assert plan['observed_progress']['research_ns'] == research_ns
    assert plan['observed_progress']['measured_engaged_ns'] == actuals['phase_measured_engaged_ns']
    assert len([c for c in plan['completed_research_checkpoints'] if c['minutes'] == 960]) == 1
    assert not (ROOT / 'v3/experiments/final_v1').exists()
    command = ['python', '-E', '-S', '-B', '-X', 'pycache_prefix=/dev/null/value_logic_p309',
               'v3/experiments/p309_freeze.py', 'verify']
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=True)
    verified = json.loads(result.stdout)
    assert verified['status'] == 'VERIFIED' and not verified['final_exposure_present']
    assert verified['manifest_sha256'] == actuals['freeze_manifest_sha256']
    frozen = ROOT / 'v3/experiments/frozen_v1'
    manifest = json.loads((frozen / 'manifest.json').read_text())
    assert len(manifest['sources']) == 50
    assert len(json.loads((frozen / 'methods.json').read_text())['methods']) == 114
    assert json.loads((frozen / 'receipt.json').read_text())['final_population_generated'] is False
    assert json.loads((frozen / 'checks.json').read_text())['final_population_generated'] is False
    assert manifest['expected_groups'] == 12 and manifest['expected_public_units'] == 500
    files = [ROOT / p for p in ['TODO_v3.md', 'v3/README.md', 'v3/claim_ledger.md',
             'v3/experiments/protocol.md', 'v3/work_logs/P3_09_2026-10-11_S1.md']]
    files += sorted(HERE.glob('*.md'))
    spec = importlib.util.spec_from_file_location('p309_markdown_guard', ROOT / 'v3/checks/math_markdown.py')
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    math_spans = 0
    links = 0
    for path in files:
        content = path.read_text()
        for start, end, kind, body in guard.math_spans(content):
            math_spans += 1
            assert not kind.startswith('legacy') and r'\operatorname' not in body, path
            if str(path.relative_to(ROOT)).startswith('v3/'):
                assert kind != 'display', path
                assert kind != 'inline' or (body.startswith('`') and body.endswith('`')), path
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if '://' in target or target.startswith(('#', 'mailto:', 'sandbox:')):
                continue
            target = target.split('#', 1)[0]
            if target:
                resolved = (path.parent / target).resolve()
                assert resolved.is_relative_to(ROOT)
                assert resolved.exists() or resolved == HERE / 'closing_verification.json', (path, target)
                links += 1
    record = {
        'schema': 'value_logic.p309.closing_verification.v1',
        'contributor': 'ChatGPT (GPT-6 Astra Pro)',
        'verified_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'PASS', 'scope': 'Administrative readback; zero additional research credit',
        'entry_commit': entry['base_commit'], 'entry_files': len(entry['files']),
        'protected_files_byte_and_mode_identical': len(protected),
        'allowed_existing_edits': entry['allowed_existing_edits'],
        'ledger': actuals['ledger'], 'phase_research_ns_reconstructed_from_ledger': research_ns,
        'phase_two_ledger_sha256': digest((ROOT / 'v2/time_ledger.csv').read_bytes()),
        'clock_stopped': True, 'P3_09_status': 'complete', 'P3_10_status': 'unstarted',
        'next_task': 'P3-10', 'final_root_absent': True,
        'official_verify_command': command, 'official_verify': verified,
        'official_verify_stderr_bytes': len(result.stderr),
        'frozen_source_files': 50, 'frozen_method_representations': 114,
        'markdown': {'files': len(files), 'local_links_checked': links, 'math_spans': math_spans,
                     'scope': 'Local targets and portable math delimiters; no live rendering or proof-checking claim'},
        'actuals_sha256': digest((HERE / 'actuals.json').read_bytes()),
        'verification_source_sha256': digest(Path(__file__).read_bytes())}
    out = HERE / 'closing_verification.json'
    assert not out.exists(), 'Preserve any earlier verification; use a versioned receipt.'
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'PASS', 'protected_files': len(protected),
                      'ledger_rows': len(rows), 'local_links': links, 'freeze': verified}))


if __name__ == '__main__':
    main()
