#!/usr/bin/env python3
"""Reuse admitted scalar anchors while replaying paid cost observations."""
from datetime import datetime,timezone
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import time

import cut_dual as dual
import joint_check as checker
import native_repair as native
import native_stream
import rup_bridge_v2 as rup
import source_anchor
import vertex_repair as vertex
from vertex_probe import jsonable

HERE=Path(__file__).resolve().parent
PREFIXES=(0,4,8,12,14)


def run(output):
    if output.exists():
        raise FileExistsError('Preserve anchor transport evidence')
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    meter=native.kernel.Meter()
    source=json.loads((HERE/'joint_source.json').read_text())
    logical=json.loads((HERE/'rup_stream_results.json').read_text())
    prior=json.loads((HERE/'dual_hull_results.json').read_text())
    joint=json.loads((HERE/'joint_v2_results.json').read_text())
    audit_arm=next(a for a in joint['arms'] if a['policy']=='audit_first')
    if len(audit_arm['audit_receipts'])!=14:
        raise ValueError('Changed fixed observation menu')
    if prior['status']!='passed' or prior['hashes']['rup_stream_results.json']!=native.sha(HERE/'rup_stream_results.json'):
        raise ValueError('Changed prior cut source')
    archive,initial,admission=native_stream.admit_existing_cache()
    files=['source_anchor.py','source_anchor_probe.py','joint_source.json','joint_v2_results.json','dual_hull_results.json','rup_stream_results.json','cut_dual.py','rup_bridge_v2.py']
    for name in files:
        size=(HERE/name).stat().st_size
        meter.pay('replay_admission','read_eight_byte_words',(size+7)//8)
        meter.pay('replay_admission','hash_blocks',(size+72)//64)
    modes=source['possible_cost_modes']; n=source['cohort_size']; price=6*n; tau=n//2
    vertices=prior['hull']['vertices']
    vertex_to_mode=[modes.index([w//n for w in v]) for v in vertices]
    if any(v!=[n*x for x in modes[k]] for v,k in zip(vertices,vertex_to_mode)):
        raise ValueError('Scalar anchors differ from the declared full-cohort mode objectives')
    costs=checker.Observations(source,meter)
    states=[]
    for count in range(15):
        if count in PREFIXES:
            states.append(dict(prefix=count,possible=[list(p) for p in costs.possible],receipt_ids=[r['receipt_id'] for r in costs.receipts]))
        if count<14:
            costs.observe(audit_arm['audit_receipts'][count])
    result=dict(status='running',evidence='DEVELOPMENT retrospective source-refinement query',contributor='ChatGPT (GPT-6 Astra Pro)',
                start_utc=datetime.now(timezone.utc).isoformat(),hashes={name:native.sha(HERE/name) for name in files},
                source_id=source['source_identity'],prefix_menu=PREFIXES,states=states,price=price,tolerance=tau,
                initial_admission=admission,arms=[],new_LP_SAT_IHS_proof_or_audit_calls=0,
                historical_observations_rechecked=14,
                scope='Every representation receives the same recorded audit-first source observations and each logical arm own admitted final cuts/witnesses. New scalar-anchor evaluation only, not an executed acquisition controller or a chronological combination of the earlier experiments.')
    def save():
        output.write_text(json.dumps(jsonable(result),indent=2)+'\n')
    save()
    for prior_arm in prior['arms']:
        arm=next(a for a in logical['arms'] if a['mode']==prior_arm['mode'])
        rows=[]
        for saved in prior_arm['rows']:
            row=saved['row']; instance=archive['instances'][row]
            cuts=[]
            for purchase in arm['purchases']:
                if purchase['row']!=row:
                    continue
                for event in purchase['response']['events']:
                    if event['kind']=='separate_rup_proof_provider' and event['purchase'].get('raw_proof') is not None:
                        checked=rup.check_export(instance,event['purchase'],meter)
                        if not any(c['receipt_id']==checked['receipt_id'] for c in cuts):
                            cuts.append(checked)
            if [c['receipt_id'] for c in cuts]!=[c['receipt_id'] for c in saved['admitted_cuts']]:
                raise ValueError('Changed admitted cut bank')
            certs=[]
            for proposal in saved['proposals']:
                old=proposal['certificate']
                got=dual.rational_dual(cuts,old['multipliers'],native.structural_id(instance),meter)
                if got!=old:
                    raise ValueError('Unreconstructable rational dual')
                certs.append(got)
            lowers=[]
            for v in vertices:
                initial_lower=max([0]+[min(vertex.dot(z,v,meter) for z in t['leaf_masks']) for t in initial[row]['trees']])
                lowers.append(max([initial_lower]+[dual.point_lower(c,v,meter,integral=True) for c in certs]))
            if lowers!=saved['integer_dual_vertex_lowers']:
                raise ValueError('Changed anchor lower values')
            ordered=[None]*len(modes)
            for lower,k in zip(lowers,vertex_to_mode):
                ordered[k]=lower
            witnesses=[]
            for w in arm['final_cache']['rows'][row]['witnesses']:
                checked=native.profile_kernel.compile_witness(instance,w['model'],meter)
                if checked['violation_mask']!=w['violation_mask']:
                    raise ValueError('Changed fixed action')
                witnesses.append(w)
            answers=[]
            previous=None
            for state in states:
                options=[]
                for w in witnesses+[None]:
                    mask=None if w is None else w['violation_mask']
                    b=source_anchor.bound(mask,modes,state['possible'],ordered,price,meter)
                    options.append(dict(model=None if w is None else w['model'],mask=mask,**b))
                best=min(options,key=lambda r:(r['bound'],r['mask'] is None,-1 if r['model'] is None else r['model']))
                if previous is not None and best['bound']>previous:
                    raise ValueError('Sound observed refinement should not weaken retained source-anchor certificate')
                if state['prefix']==0 and best['bound']!=F(saved['bounds']['stitched_dual']):
                    raise ValueError('Initial six-anchor and row-transport certificates differ')
                previous=best['bound']
                answers.append(dict(prefix=state['prefix'],answer=best,checked=best['bound']<=tau,
                                    unresolved_rows=sum(len(p)>1 for p in state['possible'])))
            rows.append(dict(row=row,admitted_cut_ids=[c['receipt_id'] for c in cuts],mode_anchor_lowers=ordered,answers=answers))
        summary=dict(source_banks=len(rows),query_states=sum(len(r['answers']) for r in rows),
                     closures_by_prefix={str(prefix):sum(a['checked'] for r in rows for a in r['answers'] if a['prefix']==prefix) for prefix in PREFIXES},
                     strict_refinements=sum(r['answers'][-1]['answer']['bound']<r['answers'][0]['answer']['bound'] for r in rows))
        result['arms'].append(dict(mode=prior_arm['mode'],rows=rows,summary=summary))
        save()
    result.update(status='passed',end_utc=datetime.now(timezone.utc).isoformat(),invoice=meter.record(),
                  total_declared_units=meter.total+admission['total_declared_units'],
                  timing=dict(wall_ns=time.perf_counter_ns()-wall,process_ns=time.process_time_ns()-cpu),
                  accounting='All reused raw cuts, rational multipliers, scalar anchor values, checked actions and actual observation receipts are admitted; replay read/check/evaluation units plus raw initial admission charged. No new source purchases, LP solves, hull-generator enumeration or objective-mask projection. Prior acquisition prices remain historical and native/storage economic costs uncalibrated.')
    save()
    print(json.dumps(jsonable(dict(arms=[dict(mode=a['mode'],**a['summary']) for a in result['arms']],total=result['total_declared_units']))))


if __name__=='__main__':
    run(Path(sys.argv[1]))
