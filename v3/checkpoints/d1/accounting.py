"""Reconstruct P3-D's baseline accounting without changing historical records.

The ledger mixes raw observations, replacement notices and additive entries.
Its research columns cannot be naively summed. Saved dispositions are applied
to their exact same-runtime intervals; the published actuals are checked, not
used as substitutes for that reconstruction.
"""
from collections import Counter
from decimal import Decimal
from pathlib import Path
import csv, hashlib, io, json, subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
BASE = '650534dbb23493f6a44357bc2ec0b40597bcbb2e'
hashes = {}

def raw(path):
    data = subprocess.check_output(['git', 'show', BASE+':'+path], cwd=ROOT)
    assert (ROOT/path).read_bytes() == data, path
    hashes[path] = hashlib.sha256(data).hexdigest()
    return data

def read(path): return json.loads(raw(path))
def mins(n): return str(Decimal(n)/Decimal(60000000000))

def main():
    # These operational files may acquire an additive audit update later.
    p = json.loads(subprocess.check_output(['git','show',BASE+':v3/plan.v1.json'],cwd=ROOT))
    ledger_bytes = subprocess.check_output(['git','show',BASE+':v3/time_ledger.csv'],cwd=ROOT)
    naive = Counter()
    for r in csv.DictReader(io.StringIO(ledger_bytes.decode())):
        if r['mode'] in ('D','L','E'):
            value = Decimal(r['engaged_seconds'])*1000000000
            assert value == int(value)
            naive[r['task_id']] += int(value)
    chunks = []
    for c in p['chunks'] + p['completed_recurrences']:
        a = read(c['actuals'])
        n = a.get('task_research_ns', a['research_ns'])
        assert n == c['research_ns'] == naive[c['id']], c['id']
        floor = c['research_floor_minutes']*60000000000
        assert n >= floor
        chunks.append(dict(task=c['id'],research_ns=n,minutes=mins(n),floor_ns=floor,
                           margin_ns=n-floor,actuals=c['actuals']))
    gates = []
    for key in ('P3-A','P3-B'):
        c=p['gates'][key]; a=read(c['actuals'])
        assert a['research_ns']==c['research_ns']==naive[key]
        gates.append(dict(task=key,research_ns=c['research_ns'],floor_ns=0,actuals=c['actuals']))

    sessions=[]; total=0; confirmation=0; segment_count=0
    for i in range(1,21):
        if i==9: continue  # No s09 research session: numbering is not elapsed work.
        name=f's{i:02}'; parent='v3/discovery/'+name+'/'
        if i==4:
            a=read(parent+'effective_actuals.json')
            assert a['effective_research_ns']==0 and a['excluded_open_segment']
            sessions.append(dict(session=name,research_ns=0,discovery_ns=0,open_interval_credit_ns=0))
            continue
        a=read(parent+('actuals.json' if i==1 else 'effective_actuals.json'))
        parts=['','c2/'] if i==11 else ['']
        modes=Counter(); lookup={}; raw_research=0
        for part in parts:
            records=[json.loads(line) for line in raw(parent+part+'segments.jsonl').decode().splitlines()]
            for s in records:
                st,en=s['start'],s['end']; n=s['elapsed_ns']
                assert st['runtime']==en['runtime'] and n==en['monotonic_ns']-st['monotonic_ns']>=0
                key=(st['monotonic_ns'],en['monotonic_ns'])
                assert key not in lookup
                lookup[key]=s; modes[s['effective_mode']]+=n;segment_count+=1
                if s['effective_mode'] in ('D','L','E'):raw_research+=n
        dispositions=a.get('applied_dispositions',[])+a.get('mode_reclassifications',[])
        if i==1:
            for d in [json.loads(line) for line in raw(parent+'dispositions.jsonl').decode().splitlines()]:
                s=records[d['segment_index']]
                dispositions.append(dict(d,start_monotonic_ns=s['start']['monotonic_ns'],
                    end_monotonic_ns=s['end']['monotonic_ns'],elapsed_ns=s['elapsed_ns']))
        seen=set()
        for item in dispositions:
            d=item.get('disposition',item)
            key=(d.get('start_monotonic_ns',d.get('segment_start_monotonic_ns')),
                 d.get('end_monotonic_ns',d.get('segment_end_monotonic_ns')))
            assert key not in seen;seen.add(key)
            n=d['elapsed_ns']; old=d.get('raw_mode',d.get('original_mode'))
            assert n==key[1]-key[0]
            if d.get('partial_raw_segment'):
                matches=[s for (lo,hi),s in lookup.items() if lo<=key[0]<key[1]<=hi]
                assert len(matches)==1
                s=matches[0]
            else:
                s=lookup[key];assert n==s['elapsed_ns']
            assert old==s['effective_mode'],(name,key)
            modes[old]-=n;modes[d['effective_mode']]+=n
        assert {k:v for k,v in modes.items() if v}=={k:v for k,v in a['closed_ns'].items() if v},name
        n=sum(modes[k] for k in ('D','L','E'));assert n==a['research_ns']
        conf=a.get('confirmation_research_ns',0);disc=n-conf
        total+=disc;confirmation+=conf
        assert i==1 or total==a['program_research_ns'],name
        # Strict interpretation, even where early hourly handoffs said "approximately".
        floor=0 if i<=3 else (3600000000000 if i in (5,6,7) else 7200000000000 if i==10 else 14400000000000)
        sessions.append(dict(session=name,research_ns=n,discovery_ns=disc,confirmation_ns=conf,
            research_minutes=mins(n),raw_research_ns=raw_research,disposition_count=len(dispositions),
            closed_ns=dict(modes),session_floor_ns=floor,cutoff_margin_ns=n-floor,
            program_ns=total,source=parent+('actuals.json' if i==1 else 'effective_actuals.json')))
    assert total==p['discovery_program']['research_ns']==190167144973347
    assert confirmation==p['chunks'][-1]['research_ns']==5424657572500
    initial=sum(s['research_ns'] for s in sessions if s['session'] in ('s01','s02','s03'))
    assert initial>=14400000000000
    # A later continuation first pays any unpaid earlier balance; prior surplus
    # is never banked against a fresh minimum and no interval is counted twice.
    debt=0;carry=[]
    for s in sessions:
        if not s.get('session_floor_ns'):continue
        before=debt;debt=max(0,debt+s['session_floor_ns']-s['research_ns'])
        if before or debt:carry.append(dict(session=s['session'],prior_debt_ns=before,remaining_debt_ns=debt))
    assert debt==0
    report=read('v3/report/log/effective_actuals.json')
    assert report['research_ns']==p['report_task']['research_ns']==naive['P3-12']
    phase=sum(c['research_ns'] for c in chunks)+sum(g['research_ns'] for g in gates)+total+report['research_ns']
    assert phase==p['observed_progress']['research_ns']==261256655669296
    delta=sum(naive.values())-phase
    assert delta==naive['P3-SEARCH-01']-total==28955469006108
    p10=read('v3/work_logs/P3_10_2026-10-11_S1/actuals.json')
    assert hashlib.sha256((ROOT/'v2/time_ledger.csv').read_bytes()).hexdigest()==p10['phase_two_ledger_sha256']
    out=dict(status='PASS',baseline=BASE,chunk_floors=chunks,technical_gates=gates,
        discovery_sessions=sessions,checked_same_runtime_segments=segment_count,
        initial_cycle_floor_ns=14400000000000,initial_s01_s03_research_ns=initial,
        strict_hourly_carry=carry,outstanding_floor_ns=debt,
        discovery_research_ns=total,confirmation_research_ns=confirmation,
        report_research_ns=report['research_ns'],phase_before_audit_ns=phase,
        phase_before_audit_minutes=mins(phase),phase_floor_ns=57600000000000,
        naive_ledger_sum_ns=sum(naive.values()),naive_overcount_ns=delta,
        naive_overcount_minutes=mins(delta),source_sha256=hashes,
        explanation='Historical raw observations include intervals later excluded or reclassified by replacement notices. Effective actuals reproduce exactly from same-runtime segments and those dispositions. No historical total is changed; no new credit is assigned. P3-11 is subtracted from s20 discovery and counted once in phase. An s07 shortfall under a strict 60-minute reading is fully discharged by later continuation surplus through s10, without borrowing earlier surplus.')
    (HERE/'accounting.json').write_bytes((json.dumps(out,indent=2)+'\n').encode())
    print(json.dumps({k:out[k] for k in ['status','checked_same_runtime_segments','discovery_research_ns','phase_before_audit_ns','naive_overcount_ns','strict_hourly_carry','outstanding_floor_ns']}))

if __name__=='__main__':main()
