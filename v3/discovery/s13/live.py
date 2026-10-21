"""Administrative closed-interval report; never starts or changes a clock."""
from pathlib import Path
import json

p=Path(__file__).resolve().parent
raw=json.loads((p/'actuals.json').read_text())
dispositions=json.loads((p/'dispositions.json').read_text())['entries']
excluded=sum(e['elapsed_ns'] for e in dispositions if e['raw_mode'] in ('D','L','E')
             and e['effective_mode'] not in ('D','L','E'))
credited=raw['research_ns']-excluded
target=raw['session_config']['session_research_target_ns']
print(json.dumps(dict(observed=raw['observed'],closed_research_ns=credited,
                     closed_research_minutes=credited/60e9,excluded_ns=excluded,
                     fresh_remaining_ns=max(0,target-credited),
                     fresh_remaining_minutes=max(0,target-credited)/60e9,
                     open_segment=raw['open_segment'],
                     note='No open-interval credit; raw cycle remaining_floor_ns is not the fresh session floor.')))
