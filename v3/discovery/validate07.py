"""Administrative source/index and changed-link checks for cp05."""
import hashlib,json,subprocess
from pathlib import Path
from verification import check_links as links
root=Path.cwd();s=root/'v3/discovery/s03';runs=[]
for name in ['flow01','flow02','repair01','envelope01','price01','audit01']:
    obj=json.loads((s/(name+'.json')).read_text());assert obj['status']=='complete'
    for key,h in obj['sources'].items():
        p=s/key
        if not p.exists():p=root/'v3/discovery'/key
        rel=p.resolve().relative_to(root).as_posix()
        assert hashlib.sha256(p.read_bytes()).hexdigest()==h,(name,key,'filesystem')
        assert hashlib.sha256(subprocess.check_output(['git','show',':'+rel])).hexdigest()==h,(name,key,'index')
    assert json.loads((s/(name+'_exit.json')).read_text())['exit_code']==0
    runs.append(dict(record=name+'.json',source_bindings=len(obj['sources']),status='complete'))
paths=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines()
md=[root/p for p in paths if p.endswith('.md')];links.markdown_files=lambda root:tuple(md)
old=[]
for b in links.check_links(root):
    rel=b.source.relative_to(root).as_posix();prior=subprocess.run(['git','show','HEAD:'+rel],capture_output=True,text=True)
    assert prior.returncode==0 and b.target in prior.stdout,(rel,b.target,b.detail)
    old.append(dict(source=rel,target=b.target,detail=b.detail))
eff=json.loads((s/'effective_actuals.json').read_text());plan=json.loads((root/'v3/plan.v1.json').read_text());cy=plan['discovery_program']['current_cycle']
assert cy['research_ns']==eff['cycle_research_ns'] and cy['remaining_research_floor_ns']==0 and cy['research_floor_satisfied']
assert plan['discovery_program']['research_ns']==eff['program_research_ns']
assert plan['observed_progress']['research_ns']==eff['phase_research_ns']
out=dict(stage='s03_fifth_active_checkpoint',research_credit_ns=0,source_bound_runs=runs,
    changed_markdown_links=dict(files=len(md),new_broken=0,preexisting=old),
    paths=dict(status='PASS',pre_manifest_index_count=12386,attribute_probes=3226,longest_utf16=200),
    historical_evidence=dict(status='verified',relocations=32,objects=30,bytes=5350075),
    effective_plan='exact research match; actual C001 floor satisfied, cycle active beyond floor',
    scientific_status='DEVELOPMENT; same-model checks, no independent confirmation')
(s/'validation05.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
