"""Reconcile this closed session without rewriting raw observations/ledger.

Codex (GPT-6), 2026-10-11. Administrative work, zero research credit.
"""
import csv
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path

root = Path(__file__).resolve().parent
raw_path = root / 'observed_actuals.json'
assert not raw_path.exists(), 'Already reconciled; inspect instead of repeating.'
raw_path.write_bytes((root / 'actuals.json').read_bytes())
raw = json.loads(raw_path.read_text())
assert raw['status'] == 'closed' and raw['open_segment'] is None
segments = [json.loads(x) for x in (root / 'segments.jsonl').read_text().splitlines()]
dispositions = [json.loads(x) for x in (root / 'dispositions.jsonl').read_text().splitlines()]
overrides = {x['segment_index']:x for x in dispositions}
totals = dict.fromkeys(raw['closed_ns'], 0)
for i, s in enumerate(segments):
    assert s['start']['runtime'] == s['end']['runtime'] == raw['observed']['runtime']
    assert s['elapsed_ns'] == s['end']['monotonic_ns']-s['start']['monotonic_ns']
    mode = s['effective_mode']
    if i in overrides:
        d = overrides[i]
        assert mode == d['original_mode']
        mode = d['effective_mode']
    totals[mode] += s['elapsed_ns']
assert sum(totals.values()) == sum(raw['closed_ns'].values())
research = sum(totals[k] for k in ('D','L','E'))
assert research == raw['research_ns']
effective = dict(raw, closed_ns=totals,
                 exact_research_minutes=str(Decimal(research)/Decimal(60_000_000_000)),
                 exact_remaining_floor_minutes=str(Decimal(raw['remaining_floor_ns'])/Decimal(60_000_000_000)),
                 exact_phase_research_minutes=str(Decimal(raw['phase_research_ns'])/Decimal(60_000_000_000)),
                 exact_mode_minutes={k:str(Decimal(v)/Decimal(60_000_000_000)) for k,v in totals.items()},
                 raw_actuals='v3/discovery/s01/observed_actuals.json',
                 dispositions='v3/discovery/s01/dispositions.jsonl',
                 clock_source_sha256=hashlib.sha256((root/'clock_source.py').read_bytes()).hexdigest(),
                 session_status='closed_for_execution_context_continuation', cycle_status='in_progress',
                 cycle_floor_satisfied=False, monetary_resource_cost='unknown')
(root/'actuals.json').write_text(json.dumps(effective, indent=2)+'\n', encoding='utf-8')
line = io.StringIO(newline='')
csv.writer(line, lineterminator='\n').writerow([
    'P3-SEARCH-01','P3-SEARCH-01-C001','s01','correction','',raw['observed']['utc'],raw['observed']['utc'],
    0,0,0,0,0,0,'v3/discovery/s01/dispositions.jsonl',
    'Zero additional credit. Raw segment 19 reclassified D to E; use effective actuals. Original rows retained.'])
with Path('v3/time_ledger.csv').open('ab') as f:
    f.write(line.getvalue().encode('utf-8'))
print(json.dumps(effective, indent=2))
