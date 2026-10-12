#!/usr/bin/env python3
"""Focused source/translation/RUP boundary checks; no fixture optimum gates."""
import copy
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
import time

import rup_bridge_v2 as bridge
from native_repair import kernel,sha

HERE=Path(__file__).resolve().parent


def source(n,hard,soft):
    v=dict(variables=n,hard=hard,soft=[dict(clause=c,weight=w) for c,w in soft],
           public_incumbent=0,objective_max=sum(w for _,w in soft))
    v['identity']=kernel.digest(v)
    return v


def extension(encoded,instance,model):
    values={j+1:bool(model&(1<<j)) for j in range(instance['variables'])}
    for z,soft in zip(encoded['violation_variables'],instance['soft']):
        values[z]=not any(values[abs(l)]==(l>0) for l in soft['clause'])
    def value(token):
        return token if type(token) is bool else values[token]
    for node in encoded['nodes']:
        z=encoded['violation_variables'][node['index']]
        values[node['variable']]=value(node['when_one'] if values[z] else node['when_zero'])
    return values


def run(output):
    if output.exists():
        raise FileExistsError('Preserve checks and actual calls')
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    meter=kernel.Meter()
    # Clause semantics, zero weights, tautologies, empty soft clause, and the
    # two threshold terminal cases are real translation obligations.
    cases=[source(3,[[1,2],[-2,3]],[([-1],2),([2,-3],3),([],0),([1,-1],4)]),
           source(2,[[1,2]],[([-1],0),([-2],3)])]
    semantic=[]
    for instance in cases:
        weights=[s['weight'] for s in instance['soft']]
        for budget in (-1,0,2,3,sum(weights),sum(weights)+1):
            e=bridge.encode(instance,weights,budget,meter)
            for model in range(1<<instance['variables']):
                values=extension(e,instance,model)
                holds=all(any(values[abs(l)]==(l>0) for l in c) for c in e['clauses'])
                feasible=all(any(values[abs(l)]==(l>0) for l in c) for c in instance['hard'])
                actual=sum(w for z,w in zip(e['violation_variables'],weights) if values[z])
                assert holds==(feasible and actual<=budget)
            semantic.append(dict(source=instance['identity'],budget=budget,assignments=1<<instance['variables'],
                                 cnf_clauses=len(e['clauses']),auxiliary_variables=len(e['nodes'])))
    probe=json.loads((HERE/'proof_cap_results.json').read_text())
    checked_probe=bridge.check_rup(probe['encoding']['full_cnf'],probe['proof_lines'],4,meter)
    rejected=[]
    for name,clauses,proof,n in [
        ('non_RUP_addition',[[1,2]],['1 0','0'],2),
        ('missing_empty',[[1],[-1]],[],1),
        ('unbound_variable',[[1],[-1]],['3 0','0'],1)]:
        try:
            bridge.check_rup(clauses,proof,n,meter)
        except ValueError as exc:
            rejected.append(dict(case=name,reason=str(exc)))
        else:
            raise AssertionError(name)
    # New source-bound positive and negative calls; no diagnostic optimum.
    tiny=source(2,[[1,2]],[([-1],2),([-2],3)])
    queries=[dict(weights=[2,3],budget=1),dict(weights=[2,3],budget=2),
             dict(weights=[0,3],budget=0),dict(weights=[2,3],budget=1,limits=dict(checking_units=1))]
    result=dict(status='running',evidence='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                start_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=sha(__file__),
                bridge_sha256=sha(bridge.__file__),source=tiny,planned_queries=queries,
                semantics=semantic,existing_export_recheck=checked_probe,rejected=rejected,calls=[])
    output.write_text(json.dumps(result,indent=2)+'\n')
    for q in queries:
        r=bridge.purchase(tiny,q['weights'],q['budget'],q.get('limits'))
        result['calls'].append(r)
        output.write_text(json.dumps(result,indent=2)+'\n')
    assert [r['status'] for r in result['calls']]==['UNSAT','SAT','SAT','UNRESOLVED']
    admitted=bridge.check_export(tiny,result['calls'][0],meter)
    projection=bridge.compile_cut_supports(tiny,[admitted],meter)
    assert projection['leaf_masks']==[1,2]
    # A consumer derives its cut from checked raw bytes, not a saved checked
    # flag. Altering the saved summary cannot strengthen the admitted cut.
    modified=copy.deepcopy(result['calls'][0])
    modified['checked_lower_receipt']['budget']=9999
    independently=bridge.check_export(tiny,modified,meter)
    assert independently['budget']==1 and independently==admitted
    result.update(status='PASS',new_native_calls=sum(r['native_calls'] for r in result['calls']),
                  new_branch_provider_calls=0,replay_native_calls=0,projection=projection,
                  declaration='Finite semantic checks plus actual SAT/UNSAT/export/cap paths. No runtime comparison or independent validation set.',
                  check_invoice=meter.record(),timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','new_native_calls','projection','timing')}))


if __name__=='__main__':
    run(Path(sys.argv[1]))
