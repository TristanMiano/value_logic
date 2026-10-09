"""Read-only final preservation/binding check; no policy or label execution.

ChatGPT (GPT-6 Astra Pro), 2026-10-09. The script hashes opaque private
payloads for preservation but never deserializes their scientific contents.
Public-only certificate calculations have separate, already sealed audits.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[4]
SESSION = ROOT / 'v3/work_logs/R_P3_B_A_2026-10-09_S1'
HERE = Path(__file__).resolve().parent
BASE = '6ce7391b6a41c6c19397b00ce7b6a2d9b228b9a4'


def digest(data):
    return sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text())


def check_bytes(data, length, expected):
    assert len(data) == length
    assert digest(data) == expected


def main():
    archive_rows = []
    for path in sorted(SESSION.rglob('*.zip')):
        raw = path.read_bytes()
        if path.name == 'raw_traces_v1.zip':
            m = load(path.parent / 'raw_archive_manifest_v2.json')
            check_bytes(raw, m['archive_bytes'], m['archive_sha256'])
            entries = [(e['archive_path'], e['bytes'], e['sha256']) for e in m['files']]
            manifest_name = 'RAW_EVIDENCE_MANIFEST.json'
        elif path.name in ('public_raw.zip', 'evaluation_raw.zip'):
            m = load(path.with_name(path.stem + '_manifest.json'))
            check_bytes(raw, m['archive_bytes'], m['archive_sha256'])
            entries = [(e['name'], e['bytes'], e['sha256']) for e in m['manifest']['entries']]
            manifest_name = 'MANIFEST.json'
        else:
            m = load(path.with_name(path.stem + '_manifest.json'))
            check_bytes(raw, m['bytes'], m['sha256'])
            entries = [(m['member'], m['member_bytes'], m['member_sha256'])]
            manifest_name = None
        with zipfile.ZipFile(path) as z:
            names = [e[0] for e in entries] + ([manifest_name] if manifest_name else [])
            assert sorted(z.namelist()) == sorted(names)
            assert len(names) == len(set(names))
            assert z.testzip() is None
            if manifest_name:
                inner = json.loads(z.read(manifest_name))
                if manifest_name == 'MANIFEST.json':
                    assert inner == m['manifest']
                else:
                    assert inner['files'] == m['files']
                    assert digest(z.read(manifest_name)) == m['embedded_manifest_sha256']
            for name, size, sha in entries:
                check_bytes(z.read(name), size, sha)
        archive_rows.append(dict(path=str(path.relative_to(ROOT)), sha256=digest(raw),
                                 bytes=len(raw), payloads=len(entries),
                                 payload_bytes=sum(e[1] for e in entries), status='PASS'))

    # All old tracked material is byte-identical except the active plan, whose
    # authorized status change is finalized at the administrative boundary.
    old_files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT).decode().splitlines()
    allowed = {'v3/plan.v1.json', 'TODO_v3.md', 'v3/README.md', 'v3/claim_ledger.md', 'v3/time_ledger.csv'}
    preserved = []
    for rel in old_files:
        if rel in allowed:
            continue
        old = subprocess.check_output(['git', 'show', BASE + ':' + rel], cwd=ROOT)
        now = (ROOT / rel).read_bytes()
        assert now == old, rel
        preserved.append(rel)

    expected = {
        'v3/checks/07_selective_feedback.py': 'f872ec2eb07df4722720763730932c33055e380f0ab76ddc3c848d79a5e70f48',
        'v3/checks/07_selective_feedback_allocation.py': 'eaf79ecb0c4b297ffeec3de4026a025fabc23058ec3c119abe5fdd23434da070',
        'v3/checks/07_selective_feedback_service.py': '68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32',
        'v3/checks/07_computation_adapter.py': '06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615',
    }
    for rel, sha in expected.items():
        assert digest((ROOT / rel).read_bytes()) == sha, rel
    reviewed = HERE / 'proof_agent'
    assert (ROOT / 'v3/checks/07_selective_feedback.py').read_bytes() == (reviewed / 'core_v1_2_source_reviewed.py').read_bytes()
    assert (ROOT / 'v3/checks/07_selective_feedback_allocation.py').read_bytes() == (reviewed / 'adaptive_allocation_source_initial.py').read_bytes()
    main_text = (ROOT / 'v3/derivations/07_selective_feedback.md').read_text()
    old_main = (reviewed / 'main_derivation_scope_corrected_snapshot.md').read_text()
    assert main_text.split('## 14.')[0].rstrip() == old_main.rstrip()

    old_overlay = load(ROOT / 'v3/checkpoints/B_1.v1.json')
    new_overlay = load(ROOT / 'v3/checkpoints/B_1_R_P3_B_A.v1.json')
    old_duties = {x['id']: x for x in old_overlay['duties']}
    assert len(new_overlay['duties']) == len(old_duties) == 21
    assert {x['id'] for x in new_overlay['duties']} == set(old_duties)
    for duty in new_overlay['duties']:
        assert duty['prior_status'] == old_duties[duty['id']]['status']
    assert new_overlay['next_task'] == 'P3-08' and new_overlay['next_task_started'] is False
    assert not new_overlay['experimental_freeze_created']
    assert not new_overlay['final_evaluation_exposed']

    result = dict(status='PASS', recorded_utc=datetime.now(timezone.utc).isoformat(),
                  base_commit=BASE, source_sha256=digest(Path(__file__).read_bytes()),
                  scope='Preservation and current source bindings; no new policy, label, diagnostic or confidence-coverage experiment.',
                  archives=archive_rows, archived_payloads=sum(r['payloads'] for r in archive_rows),
                  archived_payload_bytes=sum(r['payload_bytes'] for r in archive_rows),
                  preserved_old_files=len(preserved), old_scientific_files_unchanged=True,
                  current_sources=expected, main_review_extent='Sections 1–13 byte-identical after stripping trailing whitespace',
                  inherited_duties=21, P3_08_started=False,
                  private_payload_handling='Opaque bytes hashed only; no scientific contents deserialized.',
                  failures=[])
    (HERE / 'final_evidence_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('archives', 'current_sources')}))


if __name__ == '__main__':
    main()
