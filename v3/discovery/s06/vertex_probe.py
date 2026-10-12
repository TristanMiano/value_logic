#!/usr/bin/env python3
"""Paid anchor-proof example and fixed finite audit-planning rehearsal."""
from datetime import datetime,timezone
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import sys
import time

import native_repair as native
import native_stream
import rup_bridge_v2 as rup
import vertex_repair as vr

HERE=Path(__file__).resolve().parent


def jsonable(x):
    if isinstance(x,F):
        return str(x)
    if isinstance(x,dict):
        return {str(k):jsonable(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):
        return [jsonable(v) for v in x]
    return x


def run(output):
    if output.exists():
        raise FileExistsError('Preserve executed acquisition and planning evidence')
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    meter=native.kernel.Meter()
    # Source and menu specified before either paid proof call. Both soft
    # violations are forced; only the original variables are checked as witness.
    tiny=dict(variables=2,hard=[[1],[2]],soft=[dict(weight=1,clause=[-1]),dict(weight=1,clause=[-2])],
              public_incumbent=3,objective_max=2)
    tiny['identity']=native.kernel.digest(tiny)
    vertices=[[1,0],[0,1]]
    witness=native.profile_kernel.compile_witness(tiny,3,meter)
    result=dict(status='running',evidence='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                start_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=native.sha(__file__),
                vertex_sha256=native.sha(vr.__file__),rup_sha256=native.sha(rup.__file__),
                tiny=dict(source=tiny,vertices=vertices,price=2,tolerance=0,witness=witness,
                          planned_queries=[dict(weights=v,budget=0) for v in vertices],purchases=[]),
                new_external_cost_observations=0,new_IHS_calls=0,new_branch_calls=0)
    def save():
        output.write_text(json.dumps(jsonable(result),indent=2)+'\n')
    save()
    lowers=[]
    for vertex in vertices:
        call=rup.purchase(tiny,vertex,0)
        result['tiny']['purchases'].append(call)
        save()
        if call['status']!='UNSAT':
            raise ValueError('Anchor attempt unresolved; preserve the actual receipt')
        checked=rup.check_export(tiny,call,meter)
        assert checked['weights']==vertex
        lowers.append(checked)
    bound=vr.anchor_certificate(witness['violation_mask'],vertices,[r['checked_lower'] for r in lowers],2,meter)
    assert bound==0
    # q=e_i, q.z>=1 directly means z_i=1. The following weak single-proof
    # profiles are derived analytically, with no Boolean-mask enumeration.
    weak=dict(row='tiny',source_identity=tiny['identity'],
              witnesses=[witness|dict(receipt_id=native.kernel.digest(witness))],
              trees=[dict(leaf_masks=[1],receipt_id=lowers[0]['receipt_id']),
                     dict(leaf_masks=[2],receipt_id=lowers[1]['receipt_id'])])
    meter.pay('tiny_cut_transport','unit_coordinate_cut_implies_forced_violation',2)
    regions=vr.Regions([weak],vertices,2,0,meter)
    old=regions.best(0,(0,1),'single_proof')
    new=regions.best(0,(0,1),'stitched')
    assert old['bound']==1 and new['bound']==0
    # Focused arithmetic illustrates true convex-gap continuation; it is not
    # the admission argument and not a logical optimum search.
    interpolation=[]
    for n in range(11):
        lam=F(n,10)
        weights=[lam,1-lam]
        lower=lam*lowers[0]['checked_lower']+(1-lam)*lowers[1]['checked_lower']
        gap=vr.dot(witness['violation_mask'],weights,meter)-min(F(2),lower)
        assert gap==0
        interpolation.append(dict(lambda_first=lam,weights=weights,interpolated_lower=lower,gap=gap))
    result['tiny'].update(admitted_anchor_cuts=lowers,uniform_anchor_bound=bound,
                          single_proof=old,stitched=new,interpolation=interpolation,
                          objective_masks_enumerated=0,
                          acquisition_invoice=sum(p['invoice']['declared_units_excluding_native_search'] for p in result['tiny']['purchases']))
    save()
    # Public planning source deliberately has N=1. It is NOT the eight-row
    # realized source, a replay of that controller, or an actual audit trace.
    data=json.loads((HERE/'joint_source.json').read_text())
    modes=data['possible_cost_modes']
    archive,initial,admission=native_stream.admit_existing_cache()
    region=vr.Regions(initial,modes,6,F(1,2),meter)
    summaries=[]
    plans=[]
    for method in ('single_proof','stitched'):
        for row in range(len(initial)):
            planner=vr.AuditPlan(region,[row],method)
            root=planner.solve()
            unresolved_modes=[h for h in range(len(modes)) if region.best(row,(h,),method)['bound']>F(1,2)]
            full=region.best(row,tuple(range(len(modes))),method)
            summaries.append(dict(method=method,row=row,initial_bound=full['bound'],
                                  worst_audit_count=root['cost'],status=root['status'],
                                  unresolved_singleton_modes=unresolved_modes,states=len(planner.memo)))
            # Every public path in the quoted policy is reconstructed, using
            # table outcomes; these are hypothetical branches, never audits.
            for h in range(len(modes)):
                state=root
                visited=[]
                while state['status']=='audit':
                    j=state['coordinate']
                    outcome=F(modes[h][j])
                    choices=dict(state['branches'])
                    next_subset=choices[outcome]
                    assert h in next_subset and len(next_subset)<len(state['subset'])
                    visited.append(j)
                    state=planner.memo[next_subset]
                if root['cost'] is not None:
                    assert state['status']=='stop' and len(visited)<=root['cost']
                    assert all(a['bound']<=F(1,2) for a in state['actions'])
            plans.append(dict(method=method,row=row,root=root,states=planner.record()))
        shared=vr.AuditPlan(region,range(len(initial)),method)
        shared_root=shared.solve()
        plans.append(dict(method=method,row='all',root=shared_root,states=shared.record()))
    # Every nonempty version space uses the same candidate actions and checked
    # proofs in both evaluations. Stitching must be at least as strong.
    subset_checks=0
    strict=0
    for mask in range(1,1<<len(modes)):
        subset=tuple(h for h in range(len(modes)) if mask&(1<<h))
        for row in range(len(initial)):
            a=region.best(row,subset,'single_proof')
            b=region.best(row,subset,'stitched')
            assert b['bound']<=a['bound']
            strict+=b['bound']<a['bound']
            subset_checks+=1
    result.update(public_planning_source=dict(cohort_size=1,possible_cost_modes=modes,price=6,tolerance='1/2',
                  source_identity=native.kernel.digest(dict(cohort_size=1,modes=modes)),
                  parent_public_menu_sha256=native.sha(HERE/'joint_source.json'),
                  scope='Known single-row mode menu; exact worst-case unit observation count, no prior. Declared audit price is one observation unit, not a full economic quote.'),
                  initial_admission=admission,summaries=summaries,plans=plans,
                  focused_checks=dict(nonempty_subset_row_comparisons=subset_checks,strict_stitch_improvements=strict,
                                      hypothetical_paths_checked=2*16*len(modes),new_observations=0),
                  invoice=meter.record(),new_RUP_native_calls=2,status='complete',
                  end_utc=datetime.now(timezone.utc).isoformat(),
                  timing=dict(wall_ns=time.perf_counter_ns()-wall,process_ns=time.process_time_ns()-cpu))
    save()
    print(json.dumps(jsonable(dict(tiny_bound=bound,tiny_acquisition_units=result['tiny']['acquisition_invoice'],
                 summaries=summaries,checks=result['focused_checks'],invoice=meter.total))))


if __name__=='__main__':
    run(Path(sys.argv[1]))
