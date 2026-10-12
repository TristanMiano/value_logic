"""Administrative source/index and changed-link checks for cp07."""
import hashlib,json,subprocess
from pathlib import Path
from verification import check_links as links
root=Path.cwd();s=root/'v3/discovery/s03';runs=[]
for name in ['graph02','failure01','capped01','retry01']:
 obj=json.loads((s/(name+'.json')).read_text());assert obj['status']=='complete'
 for key,h in obj['sources'].items():
  p=s/key;rel=p.relative_to(root).as_posix()
  assert hashlib.sha256(p.read_bytes()).hexdigest()==h,(name,key,'filesystem')
  assert hashlib.sha256(subprocess.check_output(['git','show',':'+rel])).hexdigest()==h,(name,key,'index')
 assert json.loads((s/(name+'_exit.json')).read_text())['exit_code']==0
 runs.append(dict(record=name+'.json',source_bindings=len(obj['sources']),status='complete'))
graph=json.loads((s/'graph02.json').read_text());failure=json.loads((s/'graph01_failure.json').read_text())
assert all(graph['sources'][k]==v for k,v in failure['sources'].items())
assert hashlib.sha256((s/'graph_inputs01.json').read_bytes()).hexdigest()==graph['input_sha256']
assert json.loads((s/'graph01_exit.json').read_text())['exit_code']==-1073741819
assert json.loads((s/'graph01_retry_exit.json').read_text())['exit_code']==1
assert json.loads((s/'graph_inputs01_exit.json').read_text())['exit_code']==0
paths=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines()
md=[root/p for p in paths if p.endswith('.md')];links.markdown_files=lambda root:tuple(md)
old=[]
for b in links.check_links(root):
 rel=b.source.relative_to(root).as_posix();prior=subprocess.run(['git','show','HEAD:'+rel],capture_output=True,text=True)
 assert prior.returncode==0 and b.target in prior.stdout,(rel,b.target,b.detail)
 old.append(dict(source=rel,target=b.target,detail=b.detail))
eff=json.loads((s/'effective_actuals.json').read_text());plan=json.loads((root/'v3/plan.v1.json').read_text())
assert plan['discovery_program']['current_cycle']['research_ns']==eff['cycle_research_ns']
assert plan['discovery_program']['research_ns']==eff['program_research_ns'] and eff['remaining_floor_ns']==0
assert plan['observed_progress']['research_ns']==eff['phase_research_ns']
out=dict(stage='s03_seventh_active_checkpoint',research_credit_ns=0,source_bound_runs=runs,failure_preservation='Both original Python graph failures and same-input implementation amendment retained',changed_markdown_links=dict(files=len(md),new_broken=0,preexisting=old),effective_plan='exact research match; cycle active beyond satisfied floor',scientific_status='DEVELOPMENT; same-model checks, no independent confirmation')
(s/'validation07.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
