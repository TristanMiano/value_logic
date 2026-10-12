"""Additive clock dispositions after the next context recovery; no research."""
import csv,json,subprocess
from datetime import datetime,timezone
from pathlib import Path
s=Path('v3/discovery/s03')
segments=[json.loads(l) for l in (s/'segments.jsonl').read_text().splitlines()]
prior=[json.loads(l) for l in (s/'dispositions.jsonl').read_text().splitlines()]
changes={
    862833405237700:('D','generation','X','After the brief repair prototype, most of the interval derived parameter-family certificates. Dominant-mode correction only; no added research.'),
    863256376721500:('unmeasured','recovery','-','Mathematical derivation, retrieval and context compaction were not separately bounded. Exclude the whole mixed interval conservatively.'),
    863478975901500:('unmeasured','recovery','-','Recovery and current-state inspection after compaction are excluded from total engaged as well as research.')}
with (s/'dispositions.jsonl').open('a') as f:
    for start,(mode,purpose,lane,why) in changes.items():
        assert not any(d['segment_start_monotonic_ns']==start for d in prior)
        seg=next(x for x in segments if x['start']['monotonic_ns']==start)
        f.write(json.dumps(dict(segment_start_monotonic_ns=start,segment_end_monotonic_ns=seg['end']['monotonic_ns'],original_mode=seg['effective_mode'],effective_mode=mode,elapsed_ns=seg['elapsed_ns'],reason=why,purpose=purpose,lane=lane))+'\n')
now=datetime.now(timezone.utc).isoformat()
with Path('v3/time_ledger.csv').open('a',newline='') as f:
    csv.writer(f,lineterminator='\n').writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s03','O','',now,now,0,0,0,0,0,0,'v3/discovery/s03/dispositions.jsonl','Zero-credit notice: dominant-mode correction and conservative compaction/recovery exclusions.'])
subprocess.run(['python','v3/discovery/reconcile.py',str(s)],check=True)
