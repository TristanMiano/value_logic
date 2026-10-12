"""Exclude the mixed publication/compaction interval and recovery; no research."""
import csv,json,subprocess
from datetime import datetime,timezone
from pathlib import Path
s=Path('v3/discovery/s03')
segments=[json.loads(l) for l in (s/'segments.jsonl').read_text().splitlines()]
prior=[json.loads(l) for l in (s/'dispositions.jsonl').read_text().splitlines()]
with (s/'dispositions.jsonl').open('a') as f:
    for start in (866269030440200,866540485536500):
        assert not any(d['segment_start_monotonic_ns']==start for d in prior)
        seg=next(x for x in segments if x['start']['monotonic_ns']==start)
        f.write(json.dumps(dict(segment_start_monotonic_ns=start,segment_end_monotonic_ns=seg['end']['monotonic_ns'],original_mode=seg['effective_mode'],effective_mode='unmeasured',elapsed_ns=seg['elapsed_ns'],reason='Conservatively exclude mixed publication/compaction and recovery from total engaged; already zero research.',purpose='recovery',lane='-'))+'\n')
now=datetime.now(timezone.utc).isoformat()
with Path('v3/time_ledger.csv').open('a',newline='') as f:
    csv.writer(f,lineterminator='\n').writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s03','O','',now,now,0,0,0,0,0,0,'v3/discovery/s03/dispositions.jsonl','Zero-credit notice: conservatively exclude publication/compaction and recovery; research actuals unchanged.'])
subprocess.run(['python','v3/discovery/reconcile.py',str(s)],check=True)
eff=json.loads((s/'effective_actuals.json').read_text());prior=json.loads(Path('v3/discovery/s02/effective_actuals.json').read_text())
base=json.loads(subprocess.check_output(['git','show','920b717b59c781a6c6126dbbce0e5ab0cccf6bc0:v3/plan.v1.json']))
p=Path('v3/plan.v1.json');plan=json.loads(p.read_text())
plan['observed_progress']['measured_engaged_ns']=base['observed_progress']['measured_engaged_ns']+prior['total_engaged_ns']+eff['total_engaged_ns']
p.write_text(json.dumps(plan,indent=2)+'\n')
