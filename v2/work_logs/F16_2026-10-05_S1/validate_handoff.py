"""Validate the F16 handoff's immutable inputs and new document links.

Contributor: ChatGPT (GPT-6 Astra Pro). No scientific stage or test-suite rerun.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
BASE='6ef27f20e3ac0920953a27dd84d6c91a021ba58f'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO).decode()
def link_targets(text):
 # Evidence notes include formulas whose bracket syntax resembles links.
 # Code blocks and code spans are literal text, not link destinations.
 visible=re.sub(r'(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[ \t]*$', '',text)
 visible=re.sub(r'(?m)^(?: {4}|\t).*$', '',visible)
 visible=re.sub(r'(`+).*?\1', '',visible,flags=re.S)
 return set(re.findall(r'\[[^\]\n]*\]\(([^\s)]+)\)',visible))
def main():
 out=ROOT/'readiness_audit.json';assert not out.exists()
 freezes=[]
 for rel,expected,count in [
  ('v2/experiments/freeze.v1.json','b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c',34),
  ('v2/experiments/neural_diagnostic_v1/freeze.json','9c15af55b83d7edf134542a9c70bcc0f087c6f4f6491f993361a27493b5cf24c',47)]:
  p=REPO/rel;assert digest(p)==expected
  d=json.loads(p.read_text());f=d['files']
  entries=[dict(v,path=k) for k,v in f.items()] if isinstance(f,dict) else f
  assert len(entries)==count
  for item in entries:
   q=REPO/item['path'];assert q.stat().st_size==item['bytes'] and digest(q)==item['sha256'],item['path']
  freezes.append({'path':rel,'sha256':expected,'registered_files_verified':count})
 inv=json.loads((ROOT/'reviews/integrity/inventory_before.json').read_text())
 assert len(inv['files'])==973
 for item in inv['files']:
  p=REPO/item['path'];assert p.stat().st_size==item['bytes'] and digest(p)==item['sha256'],item['path']
 evidence=json.loads((ROOT/'evidence_summary_attempt1.json').read_text())
 for rel,item in evidence['inputs'].items():
  p=ROOT/rel;assert digest(p)==item['sha256'] and p.stat().st_size==item['bytes'],rel
 current=set(git('diff','--name-only',BASE).splitlines())|set(git('ls-files','--others','--exclude-standard').splitlines())
 checked_links=[];bad=[]
 for rel in sorted(current):
  if not rel.endswith('.md'):continue
  p=REPO/rel;new=p.read_text()
  old_result=subprocess.run(['git','show',BASE+':'+rel],cwd=REPO,capture_output=True,text=True)
  old=old_result.stdout if old_result.returncode==0 else ''
  for target in sorted(link_targets(new)-link_targets(old)):
   if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
   local=target.split('#',1)[0]
   if not local:continue
   exists=(p.parent/local).resolve().exists()
   checked_links.append({'file':rel,'target':target,'exists':exists})
   if not exists:bad.append(checked_links[-1])
 assert not bad,bad
 for rel in ['TODO_v2.md','v2/work_logs/F16_2026-10-05_S1.md']:
  assert not re.search(r'F16_(?:ENGAGED|POST_B|OVERHEAD|TOOL_WAIT|RECOVERY|ACCOUNTING|LEDGER)_', (REPO/rel).read_text()),rel
 assert '- [x] **F16 —' in (REPO/'TODO_v2.md').read_text()
 assert '- [ ] **Gate C —' in (REPO/'TODO_v2.md').read_text()
 assert not (REPO/'v2/checkpoints/C_1.md').exists() and not (REPO/'v2/checkpoints/D_1.md').exists()
 assert not git('diff','--name-only',BASE,'--','v2/experiments').strip()
 report=(REPO/'v2/derivations/07_adversarial_review.md').read_text()
 assert len(re.findall(r'^\| F16-O\d+ \|',report,re.M))==31
 actuals=json.loads((ROOT/'actuals.json').read_text())
 ledger=(REPO/'v2/time_ledger.csv').read_bytes()
 assert hashlib.sha256(ledger).hexdigest()==actuals['ledger_final_sha256']
 assert hashlib.sha256(ledger[:actuals['ledger_prior_bytes']]).hexdigest()==actuals['ledger_prior_sha256']
 whitespace_snapshots={
  'v2/work_logs/F16_2026-10-05_S1/math_checks/attempt1_stdout.txt':'671b8af080acd1970f29ece7fb1932525f4b9b64e52b159408c877019bd38034',
  'v2/work_logs/F16_2026-10-05_S1/reviews/coherent_upper_audit.md':'3145feac4e415f7e09f9b6277d3f7bfe8011761b4c9dc0dc2aca69137615e347',
  'v2/work_logs/F16_2026-10-05_S1/reviews/core/source_uncertainty_boundary_audit.md':'202595ba2202f7295b7f7218d45eb68178eed00851361b16206dd1b6c7a21118'}
 for rel,expected in whitespace_snapshots.items():assert digest(REPO/rel)==expected
 whitespace=subprocess.run(['git','diff','--check',BASE],cwd=REPO,capture_output=True,text=True)
 assert whitespace.returncode==2 and not whitespace.stderr
 subprocess.run(['git','diff','--check',BASE,'--','.',
                 *[':(exclude)'+p for p in whitespace_snapshots]],cwd=REPO,check=True)
 result={'status':'pass','contributor':'ChatGPT (GPT-6 Astra Pro)','scope':'Final byte/link/accounting-reference checks; no experiment or suite rerun.',
         'source_base':BASE,'freezes':freezes,'saved_scientific_files_unchanged':973,
         'saved_evidence_inputs_verified':len(evidence['inputs']),'new_relative_links_checked':checked_links,
         'objection_dispositions':31,'ledger_final_sha256':actuals['ledger_final_sha256'],
         'gates_C_D_attempted':False,'F15_ND02_started':False,
         'current_changed_or_new_files':sorted(current),
         'whitespace_check':{'default_exit_code':whitespace.returncode,'default_output':whitespace.stdout,
             'all_other_changed_files_pass':True,'preserved_snapshot_sha256':whitespace_snapshots,
             'disposition':'Keep intentional Markdown hard breaks in two signed audit snapshots and raw stdout final blank lines byte-identical. These three hash-locked evidence files alone are excepted from the whitespace-only check; all byte, link and accounting checks still apply.'}}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'pass','frozen_file_counts':[34,47],'saved_scientific_files':973,
                   'new_relative_links_checked':len(checked_links),'objections':31}))
if __name__=='__main__':main()
