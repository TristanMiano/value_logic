#!/usr/bin/env python3
"""Chronological certificate rehearsal on actual joint receipts; zero purchases."""
import copy
from datetime import datetime,timezone
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import time

import cohort_hull as hull
import joint_check as checker
import native_stream
import native_repair as native
import vertex_repair as vertex
from vertex_probe import jsonable

HERE=Path(__file__).resolve().parent


def run(output):
    if output.exists():
        raise FileExistsError('Preserve executed replay')
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    meter=native.kernel.Meter()
    source=json.loads((HERE/'joint_source.json').read_text())
    trace=json.loads((HERE/'joint_v2_results.json').read_text())
    checker.require(trace['source_sha256']==native.sha(HERE/'joint_source.json'),'Cost source bytes changed')
    checker.require(source['source_identity']==native.kernel.digest({k:v for k,v in source.items() if k!='source_identity'}),'Cost source binding changed')
    checker.require(trace['implementation_sha256']==native.sha(HERE/'joint_repair_v2.py'),'Executed implementation changed')
    for name,value in trace['dependencies'].items():
        checker.require(value==native.sha(HERE/name),'Changed executed dependency')
    files=['joint_source.json','joint_v2_results.json','cohort_hull.py','vertex_repair.py','hull_replay.py','joint_check.py']
    for name in files:
        size=(HERE/name).stat().st_size
        meter.pay('replay_read','eight_byte_words',(size+7)//8)
        meter.pay('replay_read','hash_blocks',(size+72)//64)
    archive,initial,admission=native_stream.admit_existing_cache()
    checker.require(admission['hashes']==trace['initial_admission']['hashes'],'Changed historical admission')
    result=dict(status='running',evidence='DEVELOPMENT chronological certificate rehearsal',contributor='ChatGPT (GPT-6 Astra Pro)',
                start_utc=datetime.now(timezone.utc).isoformat(),hashes={name:native.sha(HERE/name) for name in files},
                initial_admission=admission,arms=[],new_provider_native_or_audit_calls=0,
                scope='Reconstruct actual observation and proof prefixes. Evaluate another certificate on the same paid evidence; do not change or claim replay of historical acquisition decisions. No hidden source values beyond already recorded audit checking.',
                proposed_generator_cap=256)
    def save():
        output.write_text(json.dumps(jsonable(result),indent=2)+'\n')
    save()
    for arm in trace['arms']:
        costs=checker.Observations(source,meter)
        profiles=copy.deepcopy(initial)
        hulls,records={},[]
        wc=pc=0
        def evaluate(row,request,event,recorded):
            key=tuple(tuple(q) for q in costs.possible)
            meter.pay('hull_lookup','full_observation_state_key',sum(len(q) for q in key)+len(key))
            if key not in hulls:
                hulls[key]=hull.generators(costs.modes,costs.possible,meter,max_generators=256)
            h=hulls[key]
            common=dict(request=request,row=row,after_event=event,hull_state_id=native.kernel.digest(key),
                        recorded_single_proof_bound=recorded['bound'],hull_status=h['status'])
            if h['status']!='complete':
                records.append(common|dict(stitched=None))
                return
            r=vertex.Regions([profiles[row]],h['vertices'],48,4,meter)
            subset=tuple(range(len(h['vertices'])))
            single=r.best(0,subset,'single_proof')
            stitched=r.best(0,subset,'stitched')
            checker.require(single['bound']==recorded['bound'],'Grouped hull differs from direct support certificate')
            checker.require(stitched['bound']<=single['bound'],'Stitching weakened a fixed-action bound')
            records.append(common|dict(generators=len(h['vertices']),single_proof=single,stitched=stitched,
                                      strict=stitched['bound']<single['bound'],
                                      extra_tolerance_closure=stitched['bound']<=4<single['bound']))
        for request in arm['requests']:
            row=request['row']
            evaluate(row,request['request'],None,request['before'])
            for event_id in request['event_indices']:
                event=arm['events'][event_id]
                if event['kind']=='cost_audit':
                    costs.observe(event['receipt'])
                else:
                    w,p=checker.check_purchase(archive['instances'][row],event,meter,event_id,profiles[row])
                    wc+=w;pc+=p
                checker.require(costs.snapshot()==event['cost_state_after'],'Chronological cost state changed')
                evaluate(row,request['request'],event_id,event['certificate_after'])
        checker.require(profiles==arm['final_profiles'],'Final admitted bank differs')
        checker.require(costs.snapshot()==arm['final_cost_state'],'Final observed cost state differs')
        allh=[dict(state_id=native.kernel.digest(key),possible=[list(v) for v in key],**h) for key,h in hulls.items()]
        summary=dict(states=len(records),hull_states=len(hulls),unresolved=sum(r['hull_status']!='complete' for r in records),
                     max_generator_product=max(h['group_product_size'] for h in hulls.values()),
                     max_distinct_generators=max(h.get('generating_points',0) for h in hulls.values()),
                     strict_bound_improvements=sum(r.get('strict',False) for r in records),
                     extra_tolerance_closures=sum(r.get('extra_tolerance_closure',False) for r in records),
                     witnesses_readmitted=wc,proofs_readmitted=pc,cost_observations_rechecked=len(costs.receipts))
        result['arms'].append(dict(policy=arm['policy'],summary=summary,hulls=allh,certificates=records))
        save()
    # The declared cap is an actual possible unresolved path, not evidence of
    # an action's quality; no source acquisition is needed for this arithmetic.
    lowcap=hull.generators(source['possible_cost_modes'],[list(range(6))]*8,meter,max_generators=5)
    checker.require(lowcap['status']=='unresolved' and lowcap['vertices'] is None,'Cap must not yield partial hull certificate')
    result.update(status='passed',cap_check=lowcap,invoice=meter.record(),
                  total_declared_units=meter.total+admission['total_declared_units'],
                  end_utc=datetime.now(timezone.utc).isoformat(),
                  timing=dict(wall_ns=time.perf_counter_ns()-wall,process_ns=time.process_time_ns()-cpu),
                  accounting='Named replay/compilation/check operations plus current raw admission. Prior acquisition is retained, never billed as new calls. Serialization/allocation and native memory are not fully economically priced.')
    save()
    print(json.dumps(jsonable(dict(arms=[dict(policy=a['policy'],**a['summary']) for a in result['arms']],
                                  total_declared_units=result['total_declared_units']))))


if __name__=='__main__':
    run(Path(sys.argv[1]))
