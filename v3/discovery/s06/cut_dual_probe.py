#!/usr/bin/env python3
"""Expose a fixed retrospective reprice query menu to each arm's own cut bank."""
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
import time

import cut_dual as dual
import native_repair as native
import native_stream as stream

HERE=Path(__file__).resolve().parent


def run(output):
    if output.exists():
        raise FileExistsError('Preserve executed proposals')
    cpu,wall=time.process_time_ns(),time.perf_counter_ns()
    trace=json.loads((HERE/'rup_stream_results.json').read_text())
    archive,initial,admission=stream.admit_existing_cache()
    result=dict(status='running',evidence='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                start_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=native.sha(__file__),
                dual_sha256=native.sha(dual.__file__),source_sha256=native.sha(HERE/'rup_stream_results.json'),
                initial_admission=admission,arms=[],new_SAT_IHS_or_proof_calls=0,
                scope='Retrospective query rehearsal on each completed arm own paid RUP cut bank. Five public s05 recipes; all LP proposals are new paid calls. No historical controller replay or total-cost superiority claim.')
    def save():
        output.write_text(json.dumps(result,indent=2)+'\n')
    save()
    for arm in trace['arms']:
        engines={}
        final_projection={}
        for purchase in arm['purchases']:
            row=purchase['row']
            for event in purchase['response']['events']:
                if event['kind']!='separate_rup_proof_provider':
                    continue
                raw=event['purchase']
                if raw.get('checked_lower_receipt') is None:
                    continue
                if row not in engines:
                    engines[row]=dual.PersistentCutDual(archive['instances'][row])
                engines[row].add_export(raw)
                final_projection[row]=purchase['response']['checked_lower_receipt']['leaf_masks']
        records=[]
        for row,engine in sorted(engines.items()):
            bank=arm['final_cache']['rows'][row]
            for recipe,weights in native.profile_kernel.recipes([s['weight'] for s in archive['instances'][row]['soft']]):
                cert,call=engine.propose(weights)
                lower=dual.point_lower(cert,weights,engine.meter,integral=True)
                projected=min(sum(w for j,w in enumerate(weights) if z&(1<<j)) for z in final_projection[row])
                engine.meter.pay('rehearsal_comparison','projected_mask_point_query',len(weights)*len(final_projection[row]))
                assert lower<=projected
                choices=[]
                # W is the singleton supplied objective here. This also
                # checks the algebraic fixed-box bound agrees with the point
                # lower formula, without claiming uncertain-source coverage.
                for witness in bank['witnesses']:
                    z=witness['violation_mask']
                    value=sum(w for j,w in enumerate(weights) if z&(1<<j))
                    bound=dual.fixed_box_bound(cert,z,weights,weights,6,engine.meter)
                    expected=max(0,value-6,value-dual.point_lower(cert,weights,engine.meter))
                    assert bound==expected
                    choices.append(bound)
                choices.append(dual.fixed_box_bound(cert,None,weights,weights,6,engine.meter))
                records.append(dict(row=row,recipe=recipe,weights=weights,integer_dual_lower=lower,
                                    exact_cut_projection_lower=projected,point_match=lower==projected,
                                    minimum_fixed_certificate=str(min(choices)),tolerance_one_closed=min(choices)<=1,
                                    certificate=cert,call=call))
        invoices={str(row):engine.meter.record() for row,engine in engines.items()}
        result['arms'].append(dict(mode=arm['mode'],queries=records,invoice_by_source=invoices,
                                  summary=dict(source_banks=len(engines),new_LP_calls=len(records),
                                               point_matches=sum(r['point_match'] for r in records),
                                               fixed_tolerance_one_closures=sum(r['tolerance_one_closed'] for r in records),
                                               declared_units=sum(v['total'] for v in invoices.values())),
                                  persistent_scope='One continuous HiGHS model per admitted source; own checked cuts retained, objective updated across five recipes.'))
        save()
    result.update(status='complete',end_utc=datetime.now(timezone.utc).isoformat(),
                  timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))
    save()
    print(json.dumps([a['summary']|dict(mode=a['mode']) for a in result['arms']]))


if __name__=='__main__':
    run(Path(sys.argv[1]))
