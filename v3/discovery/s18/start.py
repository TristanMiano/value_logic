"""Start the fresh author-directed s18 clock once. Administrative work only."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
assert Path.cwd().resolve()==ROOT
assert not (HERE/'events.jsonl').exists() and not (HERE/'control.tmp').exists()
source=ROOT/'v3/discovery/s10/clock_source.py'
prior=json.loads((ROOT/'v3/discovery/s17/effective_actuals.json').read_text())
assert prior['program_research_ns']==152_369_325_241_147
assert prior['clock_active'] is False
config=dict(cycle='P3-SEARCH-01-C001',cycle_floor_ns=14_400_000_000_000,
            prior_cycle_research_ns=prior['cycle_research_ns'],
            prior_program_research_ns=prior['program_research_ns'],
            prior_effective_actuals='v3/discovery/s17/effective_actuals.json',
            contributor='Codex (GPT-6)',session_research_target_ns=14_400_000_000_000,
            authority='v3/decisions/2026-10-25_s18_broad_four_hours.md',
            clock_source='v3/discovery/s10/clock_source.py',
            clock_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            note='Fresh s18 session from merged main; old session closed. All setup and publication excluded.')
(HERE/'session_config.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8',newline='\n')
with (HERE/'server.log').open('xb') as log:
    subprocess.Popen([sys.executable,'-X','utf8','-u',str(source),'serve',str(HERE)],
                     stdout=log,stderr=log,cwd=ROOT,
                     creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
for _ in range(100):
    if (HERE/'control.tmp').exists():break
    time.sleep(.02)
assert (HERE/'control.tmp').exists(),'Inspect server.log; never restart blindly.'
print((HERE/'control.tmp').read_text())
