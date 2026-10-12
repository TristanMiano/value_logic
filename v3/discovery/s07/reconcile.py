"""Rebuild effective clock totals without altering raw session observations."""
from copy import deepcopy
from decimal import Decimal, getcontext
import hashlib
import json
from pathlib import Path

getcontext().prec = 40
ROOT = Path(__file__).parent


def read(name):
    return json.loads((ROOT / name).read_text())


def main():
    raw = read('actuals.json')
    dispositions = read('dispositions.json')['overrides']
    segments = [json.loads(x) for x in (ROOT/'segments.jsonl').read_text().splitlines()]
    assert raw['status']=='closed' and raw['open_segment'] is None
    prior=json.loads((ROOT.parent/'s06'/'effective_actuals.json').read_text())
    assert raw['session_config']['prior_program_research_ns']==prior['program_research_ns']
    assert raw['session_config']['prior_cycle_research_ns']==prior['cycle_research_ns']
    assert sum(s['elapsed_ns'] for s in segments)==sum(raw['closed_ns'].values())
    assert all(s['start']['runtime']==s['end']['runtime']==raw['observed']['runtime'] for s in segments)
    assert hashlib.sha256((ROOT/'clock_source.py').read_bytes()).hexdigest() == raw['session_config']['clock_source_sha256']
    effective = deepcopy(raw)
    prior_end = None
    for correction in sorted(dispositions, key=lambda d:d['start_monotonic_ns']):
        lo, hi = correction['start_monotonic_ns'], correction['end_monotonic_ns']
        assert lo < hi and hi-lo == correction['elapsed_ns']
        assert prior_end is None or prior_end <= lo
        prior_end = hi
        covered = 0
        for segment in segments:
            a,b = segment['start']['monotonic_ns'],segment['end']['monotonic_ns']
            overlap = max(0,min(hi,b)-max(lo,a))
            if not overlap:
                continue
            assert segment['effective_mode']==correction['raw_mode']
            mode = correction['raw_mode']
            effective['closed_ns'][mode] -= overlap
            effective['closed_ns'][correction['effective_mode']] += overlap
            if mode in ('D','L','E'):
                effective['purpose_ns'][segment['start']['purpose']] -= overlap
                effective['lane_ns'][segment['start']['lane']] -= overlap
            covered += overlap
        assert covered == hi-lo
    research = sum(effective['closed_ns'][m] for m in ('D','L','E'))
    assert all(v>=0 for v in effective['closed_ns'].values())
    assert sum(effective['purpose_ns'].values()) == sum(effective['lane_ns'].values()) == research
    assert sum(effective['closed_ns'].values()) == sum(raw['closed_ns'].values())
    effective.update(research_ns=research,session_research_ns=research,
                     cycle_research_ns=raw['session_config']['prior_cycle_research_ns']+research,
                     program_research_ns=raw['session_config']['prior_program_research_ns']+research,
                     phase_research_ns=raw['historical_phase_ns']+raw['session_config']['prior_program_research_ns']+research,
                     total_engaged_ns=research+effective['closed_ns']['O'],
                     research_minutes=str(Decimal(research)/Decimal(60_000_000_000)))
    effective['raw_actuals']='actuals.json'
    effective['applied_dispositions']=dispositions
    effective['hourly_target_ns']=3_600_000_000_000
    effective['hourly_overshoot_ns']=research-effective['hourly_target_ns']
    effective['clock_active']=False
    effective['status']='closed_author_directed_hourly_handoff'
    effective['research_closed_utc']=max(s['end']['utc'] for s in segments if s['start']['mode'] in ('D','L','E'))
    effective['publication_research_credit_ns']=0
    effective['note']='Raw ledger and clock files are preserved. Effective totals apply these exclusions. Administration after clock close and all publication receive no research credit. No concurrent-agent time is added.'
    for key in ('cycle_research_ns','program_research_ns','phase_research_ns','total_engaged_ns'):
        effective[key.replace('_ns','_minutes')]=str(Decimal(effective[key])/Decimal(60_000_000_000))
    effective['mode_minutes']={k:str(Decimal(v)/Decimal(60_000_000_000)) for k,v in effective['closed_ns'].items()}
    effective['source_hashes']={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                              for name in ('actuals.json','events.jsonl','segments.jsonl','dispositions.json','clock_source.py')}
    (ROOT/'effective_actuals.json').write_text(json.dumps(effective,indent=2)+'\n')
    print(json.dumps({k:effective[k] for k in ('research_ns','research_minutes','program_research_ns','program_research_minutes','phase_research_ns','phase_research_minutes','total_engaged_ns','mode_minutes')}))


if __name__=='__main__':
    main()
