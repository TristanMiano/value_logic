"""Administrative cp08 source, clock and changed-link checks."""
import hashlib,json,subprocess
from pathlib import Path
from verification import check_links as links
root=Path.cwd();s=root/'v3/discovery/s03';runs=[]
for name in ['censor02','censor_diag01','censor_repair01','biased01','hinge02']:
 obj=json.loads((s/(name+'.json')).read_text());assert obj['status']=='complete'
 for key,h in obj['sources'].items():
  p=s/key;rel=p.relative_to(root).as_posix()
  assert hashlib.sha256(p.read_bytes()).hexdigest()==h,(name,key,'filesystem')
  assert hashlib.sha256(subprocess.check_output(['git','show',':'+rel])).hexdigest()==h,(name,key,'index')
 assert json.loads((s/(name+'_exit.json')).read_text())['exit_code']==0
 if 'input_sha256' in obj:assert hashlib.sha256((s/'censor02.json').read_bytes()).hexdigest()==obj['input_sha256']
 runs.append(dict(record=name+'.json',source_bindings=len(obj['sources']),status='complete'))
assert json.loads((s/'censor01.json').read_text())==''
assert json.loads((s/'censor01_exit.json').read_text())['exit_code']==0
assert json.loads((s/'hinge01_exit.json').read_text())['exit_code']==1
paths=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();md=[root/p for p in paths if p.endswith('.md')];links.markdown_files=lambda root:tuple(md)
old=[]
for b in links.check_links(root):
 rel=b.source.relative_to(root).as_posix();prior=subprocess.run(['git','show','HEAD:'+rel],capture_output=True,text=True)
 assert prior.returncode==0 and b.target in prior.stdout,(rel,b.target,b.detail)
 old.append(dict(source=rel,target=b.target,detail=b.detail))
eff=json.loads((s/'effective_actuals.json').read_text());plan=json.loads((root/'v3/plan.v1.json').read_text())
assert plan['discovery_program']['current_cycle']['research_ns']==eff['cycle_research_ns']
assert plan['discovery_program']['research_ns']==eff['program_research_ns'] and eff['remaining_floor_ns']==0
assert plan['observed_progress']['research_ns']==eff['phase_research_ns']
out=dict(stage='s03_eighth_active_checkpoint',research_credit_ns=0,source_bound_runs=runs,failure_preservation='Malformed censor01 despite exit zero, hinge01 assertion exit 1, and both explicit same-input repairs retained',changed_markdown_links=dict(files=len(md),new_broken=0,preexisting=old),effective_plan='exact research match; active beyond floor',scientific_status='DEVELOPMENT; no independent confirmation')
(s/'validation08.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
