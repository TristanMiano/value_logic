"""Saved actual totals and source-bound rejection controls; no acquisitions."""
from pathlib import Path
import copy
import json
import graph_cover_service as service
HERE=Path(__file__).resolve().parent;root=HERE/'gc02';design=json.loads((root/'design.json').read_text());overrides=json.loads((root/'attempts.json').read_text())['overrides'];totals={};rows=[];negative=[]
for case in design['cases']:
    name=case['name'];record=dict(name=name,arms={});e=json.loads((root/f'{name}_evidence.json').read_text());data=e['source'];compiled=service.compile_source(case,data,e['cut'],e['geometry'],service.Meter())
    for arm in design['arms']:
        label=name+'_'+arm;directory=root/overrides.get(label,{}).get('selected_directory',label);r=json.loads((directory/'result.json').read_text());checked=json.loads((root/f'{label}_reconstruction.json').read_text());assert checked['status']=='complete'
        values={k:r[k] for k in('outputs','base_audit_fee','physical_audits','named_units','setup_units','observed_max_fee')};record['arms'][arm]=values
        t=totals.setdefault(arm,{k:0 for k in values})
        for k,v in values.items():
            if k=='observed_max_fee':t[k]=max(t[k],v)
            else:t[k]+=v
        if arm!='lazy':continue
        receipts=[]
        for line in(directory/'trace.jsonl').read_text().splitlines():
            event=json.loads(line)
            if event['kind']=='audit':receipts.append(event['receipt'])
            if event['kind']!='output':continue
            for kind in('wrong_source','wrong_request','wrong_fee','changed_bound','wrong_action'):
                bad=copy.deepcopy(event['decision']);rs=copy.deepcopy(receipts);c=copy.deepcopy(compiled)
                if kind=='wrong_source':c['source']='wrong'
                elif kind=='wrong_request':rs[0]['request']='wrong';rs[0]=service.g01.seal({k:v for k,v in rs[0].items() if k!='identity'})
                elif kind=='wrong_fee':rs[0]['fee']+=1;rs[0]=service.g01.seal({k:v for k,v in rs[0].items() if k!='identity'})
                elif kind=='changed_bound':bad['bound']+=1
                else:bad['model']=0;bad['kind']='repair'
                try:service.check(data,c,rs,event['request'],bad,service.Meter())
                except ValueError:negative.append(dict(case=name,kind=kind))
                else:raise AssertionError('Invalid persistent action accepted')
            break
    assert record['arms']['lazy']==record['arms']['ordinary_lazy']
    assert all(record['arms']['lazy'][k]==record['arms']['scan'][k] for k in('outputs','base_audit_fee','physical_audits','observed_max_fee'))
    rows.append(record)
prefix=json.loads((root/'n32_clique_scan_failed_prefix_reconstruction.json').read_text());selected=json.loads((root/'n32_clique_scan_retry2/result.json').read_text());known=dict(outputs=prefix['outputs'],physical_fee=prefix['base_audit_fee_completed_outputs']+prefix['remaining_physical_fee'],physical_receipts=prefix['physical_receipts_completed_outputs']+prefix['remaining_physical_receipts'],named_units_lower=prefix['named_completed_service_units']+selected['setup_units'],unknown_costs=prefix['unknown_costs'])
service.g01.save(root/'summary.json',dict(stage='DEVELOPMENT',selected_complete_totals=totals,cases=rows,additional_failed_acquisition_prefix=known,negative_controls=negative,complete_sat_calls=0,actual_source_resolution_steps=12,not_full_economic_cost=True))
print(json.dumps(dict(totals=totals,failed=known,negative_controls=len(negative)),indent=2))
