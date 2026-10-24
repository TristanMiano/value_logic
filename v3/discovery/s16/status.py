"""Read-only effective progress from closed observations; no clock or ledger write."""
from collections import Counter
from decimal import Decimal, getcontext
import json
from pathlib import Path

getcontext().prec = 40
here = Path(__file__).resolve().parent
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
raw = read(here/'actuals.json')
segments = [json.loads(s) for s in (here/'segments.jsonl').read_text().splitlines()]
lookup = {(s['start']['monotonic_ns'],s['end']['monotonic_ns']):s for s in segments}
modes = Counter()
for s in segments:
    assert s['start']['runtime'] == s['end']['runtime']
    assert s['elapsed_ns'] == s['end']['monotonic_ns']-s['start']['monotonic_ns']
    mode = s['effective_mode']
    if mode == 'O' and s['start']['purpose'] == 'context':
        mode = 'unmeasured'
    modes[mode] += s['elapsed_ns']
seen = set()
for d in read(here/'dispositions.json'):
    key = (d['start_monotonic_ns'],d['end_monotonic_ns'])
    assert key not in seen
    seen.add(key)
    s = lookup[key]
    assert s['effective_mode'] == d['raw_mode'] and s['elapsed_ns'] == d['elapsed_ns']
    modes[d['raw_mode']] -= d['elapsed_ns']
    modes[d['effective_mode']] += d['elapsed_ns']
assert min(modes.values()) >= 0
research = sum(modes[m] for m in ('D','L','E'))
target = raw['session_config']['session_research_target_ns']
result = dict(observed=raw['observed'],clock_status=raw['status'],
              effective_closed_ns=dict(modes),research_ns=research,target_ns=target,
              remaining_ns=max(0,target-research),
              research_minutes=str(Decimal(research)/Decimal(60000000000)),
              remaining_minutes=str(Decimal(max(0,target-research))/Decimal(60000000000)),
              open_segment=raw['open_segment'],
              note='Open interval earns no credit here. Read-only snapshot; final reconciliation appends ledger corrections.')
print(json.dumps(result,indent=2))
