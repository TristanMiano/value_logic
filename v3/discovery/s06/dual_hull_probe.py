#!/usr/bin/env python3
"""Actual rational LP proposals for a warranted uncertain cohort weight hull.

ChatGPT (GPT-6 Astra Pro), DEVELOPMENT. Retrospective representation query,
not a new acquisition controller or held-out validation. All own raw cuts and
witnesses are admitted afresh. No source outcome probabilities are supplied.
"""
from datetime import datetime,timezone
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import time

import cohort_hull
import cut_dual as dual
import native_repair as native
import native_stream
import rup_bridge_v2 as rup
import vertex_repair as vertex
from vertex_probe import jsonable

HERE=Path(__file__).resolve().parent


def run(output):
    if output.exists():
        raise FileExistsError('Preserve proposals and admission receipts')
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    meter=native.kernel.Meter()
    trace=json.loads((HERE/'rup_stream_results.json').read_text())
    cost=json.loads((HERE/'joint_source.json').read_text())
    # Public menu only: no hidden cohort outcome is read by the calculation.
    modes=cost['possible_cost_modes']; n=cost['cohort_size']
    public=dict(possible_cost_modes=modes,cohort_size=n)
    hull=cohort_hull.generators(modes,[list(range(len(modes)))]*n,meter,max_generators=256)
    if hull['status']!='complete':
        raise ValueError('Unresolved weight-hull construction')
    vertices=hull['vertices']; m=len(vertices[0]); price=6*n; tau=n//2
    lo=[min(v[j] for v in vertices) for j in range(m)]
    hi=[max(v[j] for v in vertices) for j in range(m)]
    archive,initial,admission=native_stream.admit_existing_cache()
    files=['dual_hull_probe.py','cut_dual.py','rup_bridge_v2.py','vertex_repair.py','cohort_hull.py','rup_stream_results.json','joint_source.json']
    for name in files:
        size=(HERE/name).stat().st_size
        meter.pay('input_admission','read_eight_byte_words',(size+7)//8)
        meter.pay('input_admission','hash_blocks',(size+72)//64)
    result=dict(status='running',evidence='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                start_utc=datetime.now(timezone.utc).isoformat(),hashes={name:native.sha(HERE/name) for name in files},
                public_cost_contract=public|dict(source_id=native.kernel.digest(public),target='Cohort sum',
                  warrant='Every one of the eight fixed rows belongs to the declared six-mode set; convex source enlargement, no population inference or mode law'),
                hull=hull,price=price,tolerance=tau,box=dict(lower=lo,upper=hi),initial_admission=admission,
                arms=[],new_SAT_IHS_proof_or_audit_calls=0,
                scope='Query each completed RUP arm own paid cut/witness bank over the initial uncertain cohort hull. All new LP proposals and compilation/checking are paid; this is not chronological replay of either acquisition controller.')
    def save():
        output.write_text(json.dumps(jsonable(result),indent=2)+'\n')
    save()
    for arm in trace['arms']:
        engines={}
        for purchase in arm['purchases']:
            row=purchase['row']
            for event in purchase['response']['events']:
                if event['kind']!='separate_rup_proof_provider':
                    continue
                raw=event['purchase']
                if raw.get('raw_proof') is None:
                    continue
                if row not in engines:
                    engines[row]=dual.PersistentCutDual(archive['instances'][row])
                engines[row].add_export(raw)
        rows=[]
        for row,engine in sorted(engines.items()):
            instance=archive['instances'][row]
            bank=arm['final_cache']['rows'][row]
            witnesses=[]
            for w in bank['witnesses']:
                got=native.profile_kernel.compile_witness(instance,w['model'],meter)
                if got['violation_mask']!=w['violation_mask']:
                    raise ValueError('Changed witness mask')
                witnesses.append(w)
            # Strong common initial evidence remains available to every path.
            base_profile=dict(row=row,source_identity=instance['identity'],witnesses=witnesses,trees=initial[row]['trees'])
            base=vertex.Regions([base_profile],vertices,price,tau,meter)
            initial_bound=base.best(0,tuple(range(len(vertices))),'single_proof')['bound']
            initial_lowers=[]
            for v in vertices:
                initial_lowers.append(max([0]+[min(vertex.dot(z,v,meter) for z in t['leaf_masks']) for t in initial[row]['trees']]))
            proposals=[]
            for v in vertices:
                cert,call=engine.propose(v)
                proposals.append(dict(certificate=cert,call=call))
            # This separately charged reference rebuilds the Boolean objective
            # relaxation from the very same freshly admitted cuts.
            projection=rup.compile_cut_supports(instance,engine.cuts,meter)
            projected_lowers=[max(old,min(vertex.dot(z,v,meter) for z in projection['leaf_masks'])) for old,v in zip(initial_lowers,vertices)]
            dual_lowers=[]
            for old,v in zip(initial_lowers,vertices):
                dual_lowers.append(max([old]+[dual.point_lower(p['certificate'],v,meter,integral=True) for p in proposals]))
            if any(l>p for l,p in zip(dual_lowers,projected_lowers)):
                raise ValueError('Dual lower exceeds its same-cut Boolean relaxation')
            box_bounds=[initial_bound]; fixed_hull_bounds=[initial_bound]
            stitched=[]; reference=[]
            for w in witnesses+[None]:
                mask=None if w is None else w['violation_mask']
                for p in proposals:
                    cert=p['certificate']
                    box_bounds.append(dual.fixed_box_bound(cert,mask,lo,hi,price,meter))
                    # Unrounded continuous dual is a globally valid concave
                    # lower function; its fixed-action gap is convex on hull.
                    lower=[dual.point_lower(cert,v,meter,integral=False) for v in vertices]
                    fixed_hull_bounds.append(vertex.anchor_certificate(mask,vertices,lower,price,meter))
                stitched.append(vertex.anchor_certificate(mask,vertices,dual_lowers,price,meter))
                reference.append(vertex.anchor_certificate(mask,vertices,projected_lowers,price,meter))
            box_bound=min(box_bounds); fixed_hull=min(fixed_hull_bounds)
            stitch=min(stitched); projected=min(reference)
            if not projected<=stitch<=fixed_hull<=box_bound:
                raise ValueError('Representation hierarchy failed')
            rows.append(dict(row=row,structural_source_id=engine.source_id,admitted_cuts=engine.cuts,
                             checked_witness_models=[w['model'] for w in witnesses],initial_tree_bound=initial_bound,
                             initial_vertex_lowers=initial_lowers,proposals=proposals,projection=projection,
                             integer_dual_vertex_lowers=dual_lowers,integer_projection_vertex_lowers=projected_lowers,
                             same_vertex_lower=sum(l==p for l,p in zip(dual_lowers,projected_lowers)),
                             bounds=dict(box=box_bound,fixed_hull=fixed_hull,stitched_dual=stitch,projected=projected),
                             closes=dict(box=box_bound<=tau,fixed_hull=fixed_hull<=tau,stitched_dual=stitch<=tau,projected=projected<=tau),
                             dual_invoice=engine.meter.record()))
        summary=dict(source_banks=len(rows),new_LP_calls=sum(len(r['proposals']) for r in rows),
                     vertex_lower_matches=sum(r['same_vertex_lower'] for r in rows),
                     strict_hull_over_box=sum(r['bounds']['fixed_hull']<r['bounds']['box'] for r in rows),
                     strict_stitch_over_fixed_hull=sum(r['bounds']['stitched_dual']<r['bounds']['fixed_hull'] for r in rows),
                     closures={k:sum(r['closes'][k] for r in rows) for k in ('box','fixed_hull','stitched_dual','projected')},
                     dual_declared_units=sum(r['dual_invoice']['total'] for r in rows))
        result['arms'].append(dict(mode=arm['mode'],rows=rows,summary=summary))
        save()
    result.update(status='passed',end_utc=datetime.now(timezone.utc).isoformat(),shared_invoice=meter.record(),
                  total_declared_units=admission['total_declared_units']+meter.total+sum(a['summary']['dual_declared_units'] for a in result['arms']),
                  timing=dict(wall_ns=time.perf_counter_ns()-wall,process_ns=time.process_time_ns()-cpu),
                  accounting='Initial raw admission, all new cut/witness checking, LP-row setup/objective updates, rational checking, hull construction, reference projection and queries included in named units. New continuous LP CPU/wall measurements retained individually; no conversion to economic cost or prospective runtime law. JSON/host storage not fully tariffed.')
    save()
    print(json.dumps(jsonable(dict(arms=[dict(mode=a['mode'],**a['summary']) for a in result['arms']],total=result['total_declared_units']))))


if __name__=='__main__':
    run(Path(sys.argv[1]))
