"""br02 paid complete scalar proofs; Codex (GPT-6), DEVELOPMENT."""
from itertools import product
from pathlib import Path
import copy
import json
import sys
import g01
HERE=Path(__file__).resolve().parent;Meter=g01.kernel.Meter
def original():return g01.seal(dict(row='br02-triangle',variables=3,hard=[[1,2],[2,3],[3,1]],soft=[dict(weight=1,clause=[-i]) for i in(1,2,3)],public_incumbent=3,objective_max=3))
def transport(source,models,box,query,receipt,claimed,meter):
    if source!=original():raise ValueError('Wrong original source')
    a=[0]*3
    for model in models:
        g01.kernel.checked_objective(source,model,meter)
        for i in range(3):a[i]+=int(bool(model>>i&1))
    m=len(models);q=[a[i]*(u-l)+m*l for i,(l,u) in enumerate(box)]
    expected=copy.deepcopy(source);expected.pop('identity');expected['soft']=[dict(weight=v,clause=[-i-1]) for i,v in enumerate(q)];expected['objective_max']=sum(q);expected=g01.seal(expected)
    if query!=expected or receipt['source_id']!=g01.kernel.digest(query) or receipt['receipt_id']!=g01.kernel.digest({k:v for k,v in receipt.items() if k!='receipt_id'}):raise ValueError('Wrong transformed source/objective/receipt')
    if receipt['provider_response']['status']!='UNSAT' or claimed!=receipt['budget']+1:raise ValueError('Wrong scalar lower')
    g01.kernel.check_negative(query,receipt['budget'],receipt['provider_response']['proof'],meter);meter.pay('transport','original_features_count_box_and_nonnegative_objective',36+6*len(models))
    return sum(a[i]*box[i][1] for i in range(3))-claimed
def prepare(root):
    root.mkdir(exist_ok=False);cases=[]
    for j,box in enumerate([[(0,2)]*3,[(1,1),(0,2),(1,2)],[(0,1),(1,2),(2,2)]]):
        for models in([3],[3,5,6]):cases.append(dict(name=f'b{j}_m{len(models)}',box=box,models=models))
    g01.save(root/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases,source_sha256=g01.sha(__file__),provider_sha256=g01.sha(g01.complete.__file__),kernel_sha256=g01.sha(g01.kernel.__file__),physical_audits=0));(root/'impl.py').write_bytes(Path(__file__).read_bytes());(root/'declaration.md').write_bytes((HERE/'box_bridge.md').read_bytes())
def run(root,case):
    directory=root/case['name'];directory.mkdir(exist_ok=False);source=original();models=case['models'];box=case['box'];m=len(models);a=[sum(int(bool(mask>>i&1)) for mask in models) for i in range(3)];q=[a[i]*(u-l)+m*l for i,(l,u) in enumerate(box)]
    query=copy.deepcopy(source);query.pop('identity');query['soft']=[dict(weight=w,clause=[-i-1]) for i,w in enumerate(q)];query['objective_max']=sum(q);query=g01.seal(query)
    meter=Meter();lower=sum(sorted(q)[:2]);meter.pay('proposal','two_of_three_scalar_bound_and_query_preparation',24+len(q)*3);g01.save(directory/'inputs.json',dict(original=source,query=query,case=case,proposed_lower=lower))
    receipt=g01.complete.execute_complete(query,lower-1);g01.save(directory/'receipt.json',receipt);bound=transport(source,models,box,query,receipt,lower,meter)
    corners=0;worst=0
    for world in product(*[(l,u) for l,u in box]):
        optimum=m*min(sum(world[i] for i in range(3) if mask>>i&1) for mask in(3,5,6,7));worst=max(worst,sum(a[i]*world[i] for i in range(3))-optimum);corners+=1
    assert worst==bound;negative=[]
    for label in('source','objective','lower'):
        s=copy.deepcopy(source);qq=copy.deepcopy(query);ll=lower
        if label=='source':s['row']='wrong'
        elif label=='objective':qq['soft'][0]['weight']+=1
        else:ll+=1
        try:transport(s,models,box,qq,receipt,ll,Meter())
        except ValueError:negative.append(label)
        else:raise AssertionError('Wrong transport accepted')
    g01.save(directory/'results.json',dict(status='complete',regret_bound=bound,scalar_lower=lower,corner_checks=corners,negative_controls=negative,local_invoice=meter.record(),complete_call_units=receipt['total_operation_units'],actual_complete_calls=1,physical_audits=0));print(case['name'],bound,receipt['total_operation_units'],flush=True)
if __name__=='__main__':
    root=HERE/'br02'
    if sys.argv[1]=='prepare':prepare(root)
    else:run(root,next(c for c in json.loads((root/'design.json').read_text())['cases'] if c['name']==sys.argv[1]))
