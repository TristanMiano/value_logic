"""Administrative source/index and changed-link checks for active cp06."""
import hashlib,json,subprocess
from pathlib import Path
from verification import check_links as links
root=Path.cwd();s=root/'v3/discovery/s03';runs=[]
for name in ['portfolio01','affine01','rank01','report01','transport01']:
    obj=json.loads((s/(name+'.json')).read_text());assert obj['status']=='complete'
    for key,h in obj['sources'].items():
        p=s/key;rel=p.relative_to(root).as_posix()
        assert hashlib.sha256(p.read_bytes()).hexdigest()==h,(name,key,'filesystem')
        assert hashlib.sha256(subprocess.check_output(['git','show',':'+rel])).hexdigest()==h,(name,key,'index')
    exit_name=name+('_retry_exit.json' if name=='report01' else '_exit.json')
    assert json.loads((s/exit_name).read_text())['exit_code']==0
    runs.append(dict(record=name+'.json',source_bindings=len(obj['sources']),status='complete',exit_record=exit_name))
failure=json.loads((s/'report01_failure.json').read_text());report=json.loads((s/'report01.json').read_text())
assert failure['sources']==report['sources']
assert json.loads((s/'report01_exit.json').read_text())['exit_code']==1
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
out=dict(stage='s03_sixth_active_checkpoint',research_credit_ns=0,source_bound_runs=runs,
    failure_preservation='report01 original exit 1 and one successful unchanged-source retry retained',
    changed_markdown_links=dict(files=len(md),new_broken=0,preexisting=old),
    effective_plan='exact research match; cycle active beyond satisfied floor',scientific_status='DEVELOPMENT; same-model checks, no independent confirmation')
(s/'validation06.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
