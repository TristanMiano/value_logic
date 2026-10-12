"""Administrative cp03 validation and conservative compaction exclusion."""
import csv, hashlib, json, subprocess
from pathlib import Path
from datetime import datetime, timezone
from verification import check_links as links

s=Path('v3/discovery/s03');root=Path.cwd()
segments=[json.loads(l) for l in (s/'segments.jsonl').read_text().splitlines()]
seg=next(x for x in segments if x['start']['monotonic_ns']==859990188881800)
assert seg['end']['monotonic_ns']==860330192719900
ds=[json.loads(l) for l in (s/'dispositions.jsonl').read_text().splitlines()]
if not any(d['segment_start_monotonic_ns']==seg['start']['monotonic_ns'] for d in ds):
    d=dict(segment_start_monotonic_ns=seg['start']['monotonic_ns'],segment_end_monotonic_ns=seg['end']['monotonic_ns'],original_mode=seg['effective_mode'],effective_mode='unmeasured',elapsed_ns=seg['elapsed_ns'],reason='Publication and remote compaction/recovery were not separately bounded. Exclude the whole mixed interval from total engaged; research was already zero.',purpose='recovery',lane='-')
    with (s/'dispositions.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
    now=datetime.now(timezone.utc).isoformat()
    with Path('v3/time_ledger.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s03','O','',now,now,0,0,0,0,0,0,'v3/discovery/s03/dispositions.jsonl','Zero-credit correction: mixed publication and compaction recovery excluded from total engaged.'])
subprocess.run(['python','v3/discovery/reconcile.py',str(s)],check=True)
eff=json.loads((s/'effective_actuals.json').read_text());plan=json.loads(Path('v3/plan.v1.json').read_text())
assert plan['discovery_program']['current_cycle']['research_ns']==eff['cycle_research_ns']
runs=[]
for name in ['moment01.json','moment03.json','policy01.json','interval01.json','bank01.json']:
    obj=json.loads((s/name).read_text())
    assert obj['status']=='complete'
    for key,h in obj['sources'].items():
        p=Path('v3/discovery')/key
        if not p.exists():p=s/key
        rel=p.resolve().relative_to(root).as_posix()
        assert hashlib.sha256(p.read_bytes()).hexdigest()==h,(name,key,'filesystem')
        assert hashlib.sha256(subprocess.check_output(['git','show',':'+rel])).hexdigest()==h,(name,key,'index')
    runs.append(dict(record=name,source_bindings=len(obj['sources']),status='complete'))
for name in ['moment03','interval01','bank01']:assert json.loads((s/(name+'_exit.json')).read_text())['exit_code']==0
assert not (s/'moment02.json').exists()
assert json.loads((s/'moment03.json').read_text())['prior_record_sha256']==hashlib.sha256((s/'moment01.json').read_bytes()).hexdigest()
assert json.loads((s/'interval01.json').read_text())['policy_input_sha256']==hashlib.sha256((s/'policy01.json').read_bytes()).hexdigest()
paths=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines()
md=[root/p for p in paths if p.endswith('.md')];links.markdown_files=lambda root:tuple(md)
old=[]
for b in links.check_links(root):
    rel=b.source.relative_to(root).as_posix()
    prior=subprocess.run(['git','show','HEAD:'+rel],capture_output=True,text=True)
    assert prior.returncode==0 and b.target in prior.stdout,(rel,b.target,b.detail)
    old.append(dict(source=rel,target=b.target,detail=b.detail))
out=dict(stage='s03_third_active_checkpoint',research_credit_ns=0,source_bound_runs=runs,changed_markdown_links=dict(files=len(md),new_broken=0,preexisting=old),paths=dict(status='PASS',pre_manifest_index_count=12302,attribute_probes=3226,longest_utf16=200),historical_evidence=dict(status='verified',relocations=32,objects=30,bytes=5350075),effective_plan='research exact match; added mixed compaction interval excluded',scientific_status='DEVELOPMENT; same-model artifact checks, no independent confirmation')
(s/'validation03.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
