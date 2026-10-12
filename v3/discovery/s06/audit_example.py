#!/usr/bin/env python3
"""Constructive opposite acquisition regime: one actual audit selects a repair."""
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
import time
import anchor_quotes as aq
import joint_repair as jr
import native_repair as native
from vertex_probe import jsonable

HERE=Path(__file__).resolve().parent


def run(output):
    if output.exists():raise FileExistsError('Preserve actual observation')
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    meter=native.kernel.Meter()
    # Same public two-variable repair formula as the earlier contract example;
    # this separate cost source and candidate assignments are declared before
    # any cell is observed. It is a constructed illustration, not validation.
    old=json.loads((HERE/'contract_results.json').read_text())
    instance=old['tiny_source']
    data=dict(possible_cost_modes=[[0,2],[2,0]],cohort_size=1,hidden_modes=[1],
              target='One fixed synthetic row; no outcome probabilities',logical_source_id=instance['identity'])
    data['source_identity']=native.kernel.digest(data)
    witness=[native.profile_kernel.compile_witness(instance,model,meter) for model in (1,2)]
    masks=[w['violation_mask'] for w in witness]
    costs=jr.CostState(data['possible_cost_modes'],1,data['source_identity'],meter)
    oracle=jr.CostOracle(data)
    # Nonnegative objective gives the checked trivial lower0; no solver status.
    lowers=[0,0]
    quote=aq.audit_quote(masks,costs.modes,costs.possible,lowers,3,0,0,meter)
    assert quote['before']==2 and quote['worst_bound']==0
    fixed=[]
    for mask in masks:
        q=aq.audit_quote([mask],costs.modes,costs.possible,lowers,3,0,0,meter)
        assert q['guaranteed_gain']==0
        fixed.append(q)
    result=dict(status='running',evidence='DEVELOPMENT constructed source',contributor='ChatGPT (GPT-6 Astra Pro)',
                start_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=native.sha(__file__),
                dependencies={name:native.sha(HERE/name) for name in ['anchor_quotes.py','source_anchor.py','joint_repair.py','contract_results.json']},
                declared_source=data,candidate_models=[1,2],checked_witnesses=witness,quote=quote,fixed_action_quotes=fixed,
                price=3,tolerance=0,new_logical_or_LP_calls=0,new_external_observations=0)
    output.write_text(json.dumps(jsonable(result),indent=2)+'\n')
    receipt=oracle.audit(0,0)
    costs.observe(receipt)
    answer=aq.best(masks,costs.modes,costs.possible,lowers,3,meter)
    assert answer['bound']==0 and answer['mask']==2
    result.update(status='complete',actual_observation=receipt,answer=answer,
                  new_external_observations=1,observation_external_price=None,provider_software_units=4,
                  invoice=meter.record(),end_utc=datetime.now(timezone.utc).isoformat(),
                  timing=dict(wall_ns=time.perf_counter_ns()-wall,process_ns=time.process_time_ns()-cpu),
                  scope='Supplied candidate assignments are explicitly checked and charged. The cost-source support is a synthetic design premise, not learned population calibration. One actual cell audit selects an already checked fixed repair; no hidden value was used to select the audit.')
    output.write_text(json.dumps(jsonable(result),indent=2)+'\n')
    print(json.dumps(jsonable(dict(status=result['status'],bound=answer['bound'],model=2,new_observations=1,software_units=meter.total+4))))


if __name__=='__main__':run(Path(sys.argv[1]))
