"""DEVELOPMENT fixed tuning, four already exposed streams, no extra queries."""
from pathlib import Path
import argparse
import hashlib
import json
import random
from local_service import stream,Oracle,T
from free_core import FreeLearner


def case(index):
    worlds,fees,threshold=stream(index);n=len(fees)
    learner=FreeLearner(n,fees,T,random.Random(22000+index))
    bill=0;queries=0;digest=hashlib.sha256();updates=[]
    for world in worlds:
        oracle=Oracle(world,fees);iterator=learner.sample();total=0;executed=[];j=None;kind=None
        while total<threshold and len(executed)<n:
            i,j,kind=next(iterator);executed.append(i);total+=oracle.buy(i,'execution')
        result=learner.update(j,kind if total>=threshold else None)
        digest.update(json.dumps([executed,result]).encode());bill+=oracle.bill['execution']
        queries+=oracle.purchases['execution'];assert oracle.bill['feedback']==0
        if result is not None:updates.append(result)
    root=Path(__file__).resolve().parent;oldpath=root/'ls01'/('c%02da0.json'%index)
    old=json.loads(oldpath.read_text(encoding='utf-8'))
    worldhash=hashlib.sha256(json.dumps(worlds,separators=(',',':')).encode()).hexdigest()
    assert worldhash==old['worlds_sha256']
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'n':n,'threshold':threshold,
       'rounds':T,'execution_fees':bill,'feedback_fees':0,'total_query_fees':bill,
       'execution_receipts':queries,'feedback_receipts':0,'worlds_sha256':worldhash,
       'sampling_seed':22000+index,'gamma':learner.gamma,'eta':learner.eta,
       'counts':learner.counts,'matrix_counts':learner.tree.counts,
       'execution_data_reads':queries,'threshold_additions':queries,
       'trajectory_sha256':digest.hexdigest(),'nonzero_update_advice':updates,
       'final_logweights':learner.tree.logweights,'comparison_input':oldpath.relative_to(root).as_posix(),
       'comparison_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),
       'older_query_bills':{a['kind']:a['total_query_fees'] for a in old['arms']},
       'hashes':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in
       ('free_core.py','free_service.py','matching_core.py','local_service.py')},
       'scope':'Exposed developmental reuse, fixed tuning declared before this run. Ordinary equivalent ties. Compute unpriced.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','execution_fees','execution_receipts','gamma','eta','counts','matrix_counts','older_query_bills')}))
