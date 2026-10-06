"""Administrative Gate C handoff audit; reads saved evidence, no experiments.

Contributor: ChatGPT (GPT-6 Astra Pro). Checks file targets of inline Markdown
links, not anchor rendering. Historical review snapshots remain historical.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
BASE = 'de7b456d08f383e72dfcabd278c183db324fdf16'
OUTPUT = ROOT / 'readiness_audit.json'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git',*args],cwd=REPO)


def links(path):
    fence = None
    visible = []
    for line in path.read_text().splitlines():
        stripped=line.lstrip()
        marker=re.match(r'^(`{3,}|~{3,})',stripped)
        if marker:
            run=marker.group(1)
            if fence is None: fence=run[0]
            elif run[0] == fence: fence=None
            continue
        if fence is not None or line.startswith('    ') or line.startswith('\t'):
            continue
        visible.append(re.sub(r'`+[^`]*`+', '', line))
    return re.findall(r'\[[^\]]*\]\(\s*<?([^\s()<>]+)>?(?:\s+[^)]*)?\)', '\n'.join(visible))


def main():
    number=int(sys.argv[1]) if len(sys.argv)>1 else 1
    attempt=ROOT/'handoff_checks'/f'attempt{number}'
    attempt.mkdir(parents=True,exist_ok=False)
    assert not OUTPUT.exists(), 'Preserve the previous final audit.'
    (attempt/'validator.py').write_bytes(Path(__file__).read_bytes())
    started=datetime.now(timezone.utc).isoformat()
    failures=[]
    integrity=json.loads((ROOT/'reviews/accounting/scientific_hash_checks.json').read_text())
    technical=json.loads((ROOT/'reviews/technical/source_manifest.json').read_text())
    entries=list(integrity['inventory_checks'])+list(technical['files'])
    for f in integrity['registered_freezes']:
        entries.append(f);entries.extend(f['members'])
    unique={e['path']:e for e in entries}
    for name,entry in unique.items():
        p=REPO/name
        if not p.is_file() or sha(p)!=entry['sha256'] or p.stat().st_size!=entry['bytes']:
            failures.append({'kind':'preserved_input_changed','path':name})
    a=json.loads((ROOT/'actuals.json').read_text())
    old=git('show',f'{BASE}:v2/time_ledger.csv')
    ledger=(REPO/'v2/time_ledger.csv').read_bytes()
    append=(ROOT/'ledger_append.csv').read_bytes()
    if ledger!=old+append or hashlib.sha256(ledger).hexdigest()!=a['ledger_final_sha256']:
        failures.append({'kind':'ledger_bytes'})
    if json.loads((ROOT/'clock_state.json').read_text()) is not None:
        failures.append({'kind':'clock_not_stopped'})
    assessment=json.loads((REPO/'v2/checkpoints/C_1_assessment.json').read_text())
    if not (assessment['assessment_complete'] and assessment['evaluator_recommendation']=='PASS'
            and assessment['author_decision']=='PENDING' and not assessment['gate_checkbox_checked']
            and assessment['next_task_selected'] is None and not assessment['gate_d_attempted']
            and not assessment['nd02_started']):
        failures.append({'kind':'decision_authority'})
    todo=(REPO/'TODO_v2.md').read_text()
    if '- [ ] **Gate C —' not in todo or '- [x] **Gate C —' in todo:
        failures.append({'kind':'gate_checkbox'})
    names=set(git('diff','--name-only',BASE).decode().splitlines())
    names.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
    allowed={'README.md','TODO_v2.md','v2/README.md','v2/verification/README.md',
        'v2/claim_ledger.md','v2/contribution_review.md','v2/contribution_plan.md','v2/time_ledger.csv',
        'v2/checkpoints/C_1.md','v2/checkpoints/C_1_assessment.json','v2/work_logs/C_2026-10-06_S1.md'}
    for name in sorted(names):
        if name not in allowed and not name.startswith('v2/work_logs/C_2026-10-06_S1/'):
            failures.append({'kind':'unexpected_changed_path','path':name})
    documents=[REPO/n for n in sorted(names) if n.endswith('.md')]
    checked=[]
    for path in documents:
        text=path.read_text()
        if '{{C1_' in text:
            failures.append({'kind':'unrendered_actuals','path':path.relative_to(REPO).as_posix()})
        for target in links(path):
            u=urlsplit(target)
            if u.scheme or not u.path:
                continue
            destination=(path.parent/unquote(u.path)).resolve()
            ok=destination.exists() or destination==OUTPUT
            checked.append({'source':path.relative_to(REPO).as_posix(),'target':target,'file_target_resolves':ok})
            if not ok: failures.append({'kind':'missing_local_link','source':str(path.relative_to(REPO)),'target':target})
    disposition=json.loads((ROOT/'whitespace_disposition.json').read_text())
    assert sha(REPO/disposition['path']) == disposition['sha256']
    full=subprocess.run(['git','diff','--cached','--check'],cwd=REPO,capture_output=True,text=True)
    whitespace=[{'command':['git','diff','--cached','--check'],
        'returncode':full.returncode,'stdout':full.stdout,'stderr':full.stderr,
        'disposition':'Exact raw Git-diff evidence is preserved; all other paths are checked below.'}]
    for args in [['diff','--check'],['diff','--cached','--check','--','.',':(exclude)'+disposition['path']]]:
        p=subprocess.run(['git',*args],cwd=REPO,capture_output=True,text=True)
        whitespace.append({'command':['git',*args],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        if p.returncode: failures.append({'kind':'whitespace','command':args})
    result={'status':'pass' if not failures else 'fail','started_utc':started,
        'completed_utc':datetime.now(timezone.utc).isoformat(),'attempt':number,'source_commit':BASE,
        'contributor':'ChatGPT (GPT-6 Astra Pro)','preserved_scientific_files':len(integrity['inventory_checks']),
        'existing_tracked_python_sources':len(technical['files']),'preserved_unique_input_files':len(unique),
        'registered_freeze_member_counts':[len(f['members']) for f in integrity['registered_freezes']],
        'ledger_prefix_preserved_bytes':len(old),'new_ledger_rows':a['ledger_rows_added'],
        'author_decision':'PENDING','gate_checkbox_unchecked':True,'new_task_selected':False,
        'new_scientific_executions':0,'markdown_documents_checked':len(documents),
        'inline_local_file_links_checked':len(checked),'link_scope':'File targets only; this result is a declared self-output.',
        'local_links':checked,'whitespace':whitespace,'whitespace_evidence_exception':disposition,'failures':failures,
        'validator_sha256':sha(Path(__file__)),
        'input_sha256':{n:sha(ROOT/n) for n in ['actuals.json','ledger_append.csv',
            'reviews/accounting/scientific_hash_checks.json','reviews/technical/source_manifest.json']}}
    (attempt/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    if failures:
        print(json.dumps({'status':'fail','failures':failures},indent=2))
        raise SystemExit(1)
    OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ['status','preserved_scientific_files','inline_local_file_links_checked','new_ledger_rows','author_decision']}))


if __name__ == '__main__':
    main()
