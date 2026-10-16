"""Administration only: retain a dead clock and resume the SAME s11 commitment."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, os, subprocess, sys, time

root=Path(__file__).resolve().parent
raw=json.loads((root/'actuals.json').read_text())
dispositions=json.loads((root/'dispositions.json').read_text())['entries']
excluded=sum(x['elapsed_ns'] for x in dispositions)
earned=raw['research_ns']-excluded
part=root/'c2';part.mkdir(exist_ok=False)
config=dict(raw['session_config'])
config.update(prior_cycle_research_ns=config['prior_cycle_research_ns']+earned,
              prior_program_research_ns=config['prior_program_research_ns']+earned,
              session_research_target_ns=config['session_research_target_ns']-earned,
              note='Second resident runtime of s11; same author commitment. Parent closed segments only, after dispositions. Never subtract readings across runtimes.')
(part/'session_config.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')
record={'contributor':'Codex (GPT-6)','observed_utc':datetime.now(timezone.utc).isoformat(),
        'reason':'Agent sent O with lane X. The clock requires lane - for O and exited at its validation assertion. This is an identified command error, not an attributed CPU failure.',
        'old_runtime':raw['observed']['runtime'],'old_open_segment':raw['open_segment'],
        'old_open_segment_research_credit_ns':0,'old_open_segment_duration':'unmeasured; no end observation in that runtime',
        'old_raw_closed_research_ns':raw['research_ns'],'closed_context_dispositions_ns':excluded,
        'old_effective_closed_research_ns':earned,'remaining_s11_research_ns':config['session_research_target_ns'],
        'old_actuals_sha256':hashlib.sha256((root/'actuals.json').read_bytes()).hexdigest(),
        'continuation_clock':'c2','new_recurrence':False,
        'scope':'All recovery, context gap, dependency installation and packaging excluded. Original observations remain unchanged.'}
(root/'clock_recovery.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
with (part/'server.log').open('xb') as log:
    subprocess.Popen([sys.executable,'-u',str(root.parent/'s10'/'clock_source.py'),'serve',str(part)],
                     stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
for _ in range(100):
    if (part/'control.tmp').exists():break
    time.sleep(.02)
assert (part/'control.tmp').exists()
print(json.dumps(record,indent=2))
