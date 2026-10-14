"""Derive a static versioned service from the executed ac02 harness."""
from pathlib import Path
p=Path(__file__).resolve().parent
old=(p/'anchor_service.py').read_text()
run=old[old.index('def run('):old.index("if __name__=='__main__':")]
run=run.replace("if arm in('cover','ordinary_cover'):","if arm in('budget','ordinary_budget','cover'):")
run=run.replace("pd=root/(case['name']+'_policy')","pd=root/(case['name']+('_cover_policy' if arm=='cover' else '_budget_policy'))")
prefix='''"""bc02 frozen paid budget policy, Codex (GPT-6), DEVELOPMENT."""
from pathlib import Path
import json
import random
import sys
import time
import anchor_cover as ac
import budget_cover as bc
from anchor_service import rows
op=ac.op;safe=ac.safe;Meter=ac.Meter;g01=ac.g01;HERE=ac.HERE

def compile_budget(case,geometry):
    data=op.source(case);meter=Meter();op.admit(case,data,geometry,meter);Q=case['H']*sum(case['weights']);C=case['fees'][-1]
    planner=bc.Planner(data['supports'],case['fees'],Q,lambda s,m:ac.utility(case,s,m),1);nodes={}
    def visit(state):
        key=op.state_key(state)
        if key in nodes:return nodes[key]['value']
        b=C-sum(case['fees'][i] for i,v in enumerate(state[:-1]) if v is not None)
        query=planner.choose(state,b);meter.pay('compilation','selected_budget_policy_state',12+len(state))
        if query is None:nodes[key]=dict(value=0,action=ac.action(case,state,meter));return 0
        values=[]
        for v in data['supports'][query]:
            child=list(state);child[query]=v;values.append(visit(tuple(child)));meter.pay('compilation','selected_budget_policy_response',7+len(state))
        value=case['fees'][query]+max(values);nodes[key]=dict(value=value,query=query);return value
    initial=(None,)*len(data['supports']);value=visit(initial);meter.pay('preparation','all_actual_lookahead_states',planner.meter.total)
    assert value<=2*C
    return dict(source=data['identity'],price=case['A'],tau=Q,root=op.state_key(initial),value=value,nodes=nodes),dict(invoice=meter.record(),states=len(nodes),lookahead_states=planner.value.cache_info().currsize)

def prepare(root):
    root.mkdir(exist_ok=False);design=json.loads((HERE/'ac02/design.json').read_text());design['arms']=['budget','ordinary_budget','cover','anchor']
    for j,case in enumerate(design['cases']):case['seed']=8141740+j
    design.update(source_sha256=g01.sha(__file__),dependencies={name:g01.sha(HERE/name) for name in('budget_cover.py','anchor_service.py','anchor_cover.py','observation_policy.py','policy_safety.py','partial_star.py','frontier_service.py','replacement_frontier.py','action_audits.py','g01.py','joint_guard.py')})
    g01.save(root/'design.json',design);(root/'impl.py').write_bytes(Path(__file__).read_bytes());(root/'declaration.md').write_bytes((HERE/'budget_service.md').read_bytes())
    for name in design['dependencies']:(root/name).write_bytes((HERE/name).read_bytes())
    for case in design['cases']:
        geometry=json.loads((HERE/'op01'/f"{case['name']}_geometry.json").read_text());g01.save(root/f"{case['name']}_geometry.json",geometry)
        for label,builder in [('budget',compile_budget),('cover',ac.compile_policy)]:
            directory=root/(case['name']+'_'+label+'_policy');directory.mkdir();policy,prep=builder(case,geometry);meter=Meter();checked=safe.check(case,policy,geometry,meter)
            g01.save(directory/'preparation.json',prep);g01.save(directory/'checking.json',dict(**checked,invoice=meter.record()));g01.save(directory/'policy.json',policy)
    print('prepared bc02',flush=True)

'''
main=old[old.index("if __name__=='__main__':"):]
(p/'budget_service.py').write_text(prefix+run+main)
checker=(p/'check_ac02.py').read_text().replace('import anchor_service as service','import budget_service as service').replace("/'ac02'","/'bc02'").replace("if arm in('cover','ordinary_cover')", "if arm in('budget','ordinary_budget','cover')").replace("(name+'_policy')","(name+('_cover_policy' if arm=='cover' else '_budget_policy'))")
(p/'check_bc02.py').write_text(checker)
