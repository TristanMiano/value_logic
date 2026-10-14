"""Reconstruct durable cs01 evidence after observed host/interpreter failures.
One case per fresh process; no new physical acquisitions. Codex (GPT-6).
"""
from ast import literal_eval
from fractions import Fraction as F
from pathlib import Path
import copy
import json
import sys
import g01
import continuum_policy as cp
import continuum_service as service

HERE=Path(__file__).resolve().parent
ROOT=HERE/'cs01'


def load_proof(raw):
    result=dict(raw);result['coefficients']=list(map(F,raw['coefficients']));certs=[]
    for old in raw['evaluations']:
        cert=dict(old);cert['rho']=F(cert['rho']);cert['bound']=F(cert['bound'])
        cert['tables']={name:{literal_eval(key):F(v) for key,v in table.items()} for name,table in cert['tables'].items()}
        certs.append(cert)
    result['evaluations']=certs;return result


def run(name):
    design=json.loads((ROOT/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==name)
    summary=next(c for c in json.loads((ROOT/'results.json').read_text())['cases'] if c['name']==name)
    data=service.source(case['costs']);rows=service.ms.draw(data['n'],case['r'],design['requests'],case['seed'])
    result=dict(name=name,stage='DEVELOPMENT reconstruction',physical_new_audits=0,arms={},negative_controls=[])
    for arm in design['arms']:
        saved=summary['arms'][arm];bankfile=ROOT/f'{name}_{arm}_bank.json';polynomials={};roots={};table=[]
        if arm!='full':
            raw=json.loads(bankfile.read_text());assert raw['source']==data['identity'] and F(raw['epsilon'])==service.EPSILON
            for r,record in raw['policies'].items():
                key=int(r);roots[key]={literal_eval(k):v for k,v in record['roots'].items()};proof=load_proof(record['proof'])
                cp.check_polynomial(data['audit_costs'],roots[key],proof);polynomials[key]=proof['coefficients']
            for old in raw['table']:
                table.append(dict(interval=list(map(F,old['interval'])),local={int(k):list(map(F,v)) for k,v in old['local'].items()},
                    upper={int(k):F(v) for k,v in old['upper'].items()},allowed=old['allowed']))
            if table:service.check_table(polynomials,table,arm in ('learner','ordinary_learner'),service.Meter())
        count=fee=audits=samples=repeats=0;records=[];plan=None;last_receipts=[];current_interval=[F(0),F(1)];frozen=False
        with (ROOT/f'{name}_{arm}.jsonl').open() as stream:
            header=json.loads(next(stream));assert header['source']==data['identity'] and header['arm']==arm
            if arm!='full':assert header['bank_sha256']==g01.sha(bankfile)
            for line in stream:
                record=json.loads(line);kind=record['kind']
                if kind=='decision_epoch':
                    assert record['before_request']==count and record['samples']==samples
                    if arm=='plugin':
                        estimate=F(repeats,samples) if samples else F(1,2)
                        assert F(record['estimate'])==estimate
                        expected=min(polynomials,key=lambda r:(cp.evaluate(polynomials[r],estimate),r))
                        assert record['selected']==expected
                    else:
                        if arm!='static':
                            lo,hi=service.base.confidence(samples,repeats,1,service.Meter())
                            current_interval=[max(current_interval[0],lo),min(current_interval[1],hi)]
                        assert list(map(F,record['interval']))==current_interval
                        selected,bound,frozen,bins=service.table_select(table,current_interval,arm!='static',service.Meter())
                        assert (record['selected'],F(record['fee_upper']),record['certified_epsilon_optimal'],record['intersected_bins'])==(selected,bound,frozen,bins)
                elif kind=='plan':
                    assert not records;plan=record;assert record['request']==f'{name}-{arm}-{count}'
                elif kind=='audit':
                    receipt=record['receipt'];unsealed={k:v for k,v in receipt.items() if k!='identity'}
                    assert receipt['identity']==g01.kernel.digest(unsealed)
                    assert receipt['source']==data['identity'] and receipt['request']==plan['request']
                    assert receipt['sequence']==len(records) and receipt['node']not in {r['node'] for r in records}
                    assert receipt['base_fee']==case['costs'][receipt['node']] and receipt['value']==rows[count][receipt['node']]
                    records.append(receipt)
                elif kind=='output':
                    assert record['request']==plan['request'];assignment=record['action']['assignment'];known={r['node']:r['value'] for r in records}
                    # Independent direct source decoding, all compatible local values.
                    for edge in range(data['n']-1):
                        chosen=[]
                        for pair in range(2):
                            left=bool(assignment>>(4*edge+2*pair)&1);right=bool(assignment>>(4*edge+2*pair+1)&1)
                            assert left!=right;chosen.append(edge if left else edge+1)
                        for a in ([known[edge]] if edge in known else [0,1,2]):
                            for b in ([known[edge+1]] if edge+1 in known else [0,1,2]):
                                values={edge:a,edge+1:b}
                                assert sum(values[i] for i in chosen)==2*min(a,b)
                        assert chosen==record['action']['selected'][2*edge:2*edge+2]
                    paid=sum(r['base_fee'] for r in records)
                    assert record['base_fee']==paid and record['physical_audits']==len(records)
                    fee+=paid;audits+=len(records);last_receipts=records;records=[];count+=1
                elif kind=='pair_count':
                    assert record['request']==count-1 and not frozen
                    assert last_receipts[0]['value']==1 and abs(last_receipts[0]['node']-last_receipts[1]['node'])==1
                    assert record['first']==last_receipts[0]['identity'] and record['next']==last_receipts[1]['identity']
                    samples+=1;repeats+=int(last_receipts[1]['value']==1)
                    assert (record['samples'],record['repeats'])==(samples,repeats)
                else:raise ValueError(kind)
        assert not records and count==saved['outputs']==design['requests']
        assert (fee,audits,samples,repeats)==tuple(saved[k] for k in ('base_audit_fee','physical_audits','learning_samples','repeats'))
        result['arms'][arm]=dict(outputs=count,physical_receipts=audits,fee=fee,learning_samples=samples,
            checked_polynomials=len(polynomials),checked_bins=len(table),trace_sha256=g01.sha(ROOT/f'{name}_{arm}.jsonl'))
        if arm=='learner':
            for label,mutant in [('missing_bin',copy.deepcopy(table[:-1])),('changed_endpoint',copy.deepcopy(table)),('changed_mask',copy.deepcopy(table)),('changed_fee',copy.deepcopy(table))]:
                if label=='changed_endpoint':mutant[0]['interval'][0]=F(1,128)
                if label=='changed_mask':mutant[0]['allowed']=[2]
                if label=='changed_fee':mutant[0]['upper'][1]+=1
                rejected=False
                try:service.check_table(polynomials,mutant,True,service.Meter())
                except ValueError:rejected=True
                assert rejected;result['negative_controls'].append(dict(kind=label,rejected=True))
    result['status']='complete';g01.save(ROOT/f'{name}_reconstruction.json',result)
    print(json.dumps(dict(name=name,outputs=sum(v['outputs'] for v in result['arms'].values()),status='checked')))


if __name__=='__main__':run(sys.argv[1])
