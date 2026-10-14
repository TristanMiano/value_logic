"""Original clauses, independent scan choices and compatible-world checks."""
from itertools import product
from pathlib import Path
import json
import sys
import graph_cover_service as service
gc=service.gc;g01=service.g01;Meter=service.Meter;ROOT=service.HERE/'gc02'

def run(name,arm,prefix=False):
    design=json.loads((ROOT/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==name);label=name+'_'+arm;override=json.loads((ROOT/'attempts.json').read_text())['overrides'].get(label,{})
    directory=ROOT/(label if prefix else override.get('selected_directory',label));request_name=name if prefix else override.get('request_case_name',name)
    evidence=json.loads((ROOT/f'{name}_evidence.json').read_text());data=json.loads((directory/'source.json').read_text());compiled=service.compile_source(case,data,evidence['cut'],evidence['geometry'],Meter());rows=service.rows(case,data)
    state=service.State(data,compiled,'anchor' if arm=='anchor' else'scan',Meter());receipts=[];index=fee=audits=units=world_checks=original_clause_checks=0
    with(directory/'trace.jsonl').open() as f:
        for line in f:
            item=json.loads(line)
            if item['kind']=='header':
                assert item==dict(kind='header',source=data['identity'],arm=arm,price=compiled['A'],tau=compiled['tau'],cut=evidence['cut']['identity']);continue
            request=f'{request_name}-{arm}-{index}';query=state.select()
            if item['kind']=='audit':
                assert query is not None;r=item['receipt'];assert r['request']==request and r['coordinate']==query and r['value']==rows[index][query]
                receipts.append(r);state.observe(query,r['value'])
                assert min(state.G,compiled['Q'])==gc.utility(data,state.known,compiled['K'],Meter())
            elif item['kind']=='output':
                assert query is None and item['request']==request;decision=item['decision'];assert decision==service.proposal(data,compiled,state.known,Meter())
                known=service.check(data,compiled,receipts,request,decision,Meter());coefficients=[0]*len(data['supports'])
                if decision['kind']=='repair':
                    mask=decision['model']
                    for clause in data['hard']:
                        assert any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in clause);original_clause_checks+=1
                    for feature in data['features']:
                        if not any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in feature['clause']):coefficients[feature['node']]+=feature['scale']
                candidates=product(*[(v,) if v is not None else(0,data['H']) if i<data['nodes'] else(0,compiled['A']) for i,v in enumerate(known)]) if data['nodes']==8 else[rows[index]]
                worst=0
                for world in candidates:
                    opt=world[-1]+sum(2*w*min(world[a],world[b]) for a,b,w in data['edges']);cost=compiled['A'] if decision['kind']=='replace' else sum(c*z for c,z in zip(coefficients,world));worst=max(worst,cost-min(compiled['A'],opt));world_checks+=1
                assert worst<=decision['bound']<=compiled['tau'];paid=sum(r['fee'] for r in receipts);assert paid==item['base_fee'] and len(receipts)==item['physical_audits']
                fee+=paid;audits+=len(receipts);units+=item['named_units'];index+=1;receipts=[];state=service.State(data,compiled,'anchor' if arm=='anchor' else'scan',Meter())
            else:raise ValueError('Unknown trace event')
    record=dict(status='retained_incomplete_prefix' if prefix else'complete',outputs=index,base_audit_fee_completed_outputs=fee,physical_receipts_completed_outputs=audits,named_completed_service_units=units,remaining_physical_receipts=len(receipts),remaining_physical_fee=sum(r['fee'] for r in receipts),original_clause_checks=original_clause_checks,world_checks=world_checks,world_scope='all compatible endpoint corners' if data['nodes']==8 else'actual hidden world plus admitted cut/geometry proof',trace_sha256=g01.sha(directory/'trace.jsonl'),physical_new_audits=0)
    if not prefix:
        saved=json.loads((directory/'result.json').read_text());assert index==64 and not receipts
        assert(index,fee,audits,units+saved['setup_units'])==tuple(saved[k] for k in('outputs','base_audit_fee','physical_audits','named_units'))
    else:
        assert not(directory/'result.json').exists();record['unknown_costs']=['incomplete request computation','failed native CPU/wall','unassigned memory/economic conversion']
    suffix='_failed_prefix' if prefix else'';g01.save(ROOT/f'{label}{suffix}_reconstruction.json',record);print(label,suffix,index,world_checks,flush=True)

if __name__=='__main__':run(sys.argv[1],sys.argv[2],len(sys.argv)>3)
