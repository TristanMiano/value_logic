"""DEVELOPMENT one declared model-splitting selector, Codex (GPT-6)."""
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import argparse
import hashlib
import json
from cnf_repair import run_arm,satisfies


def select(worlds,n):
    chosen=[];trace=[];reads=0
    for step in range(2):
        scores=[]
        for j in range(1,n+1):
            if j in chosen:continue
            cells=Counter(tuple(bool(x&(1<<(v-1))) for v in chosen+[j]) for x in worlds)
            reads+=len(worlds)*(len(chosen)+1)
            scores.append((sum(v*v for v in cells.values()),j,sorted(cells.values())))
        score,j,cells=min(scores);chosen.append(j)
        trace.append({'selected':j,'partition_square_sum':score,'cell_sizes':cells,
                      'all_scores':[{'variable':j,'score':v,'cell_sizes':c} for v,j,c in scores]})
    return chosen,trace,reads


def case(index):
    root=Path(__file__).resolve().parent;oldpath=root/'cr01'/('c%02da0.json'%index)
    old=json.loads(oldpath.read_text(encoding='utf-8'));n=old['n'];worlds=old['source_models']
    source_key=next(k for k in old['inputs'] if k.endswith('source.json') or k.endswith('design.json'))
    source_path=root.parent/source_key
    assert hashlib.sha256(source_path.read_bytes()).hexdigest()==old['inputs'][source_key]
    source=json.loads(source_path.read_text(encoding='utf-8'))
    if 'sources' in source:source=next(v['source'] for v in source['sources'] if v['source']['name']==old['name'])
    assert all(satisfies(x,source['hard']) for x in worlds)
    query_vars,trace,reads=select(worlds,n)
    histories=sorted(([v*s for v,s in zip(query_vars,values) if s] for values in product((-1,0,1),repeat=2)),key=lambda h:(len(h),h))
    masks=[0]+[1<<j for j in range(n)]+[sum(1<<j for j in pair) for pair in combinations(range(n),2)]
    arms=[run_arm(source,worlds,masks,histories,reuse) for reuse in (False,True)]
    for a,b in zip(arms[0]['histories'],arms[1]['histories']):assert a.get('valid_masks')==b.get('valid_masks')
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'name':old['name'],'n':n,
        'query_variables':query_vars,'selector_trace':trace,'selector_model_bit_reads':reads,
        'source_models':worlds,'source_model_count':len(worlds),'arms':arms,
        'historical_source_admission':old['historical_source_admission'],'physical_truth_purchases':0,
        'input':oldpath.relative_to(root).as_posix(),'input_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependencies':{'cnf_repair.py':hashlib.sha256((root/'cnf_repair.py').read_bytes()).hexdigest()},
        'scope':'One unweighted logical-model partition heuristic on exposed sources. No inferred source probabilities or complete-cost claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':a.case,'name':result['name'],'queries':result['query_variables'],
      'selector_reads':result['selector_model_bit_reads'],'arms':[{'reuse':v['reuse'],'counts':v['counts'],
      'new_masks':len(v['distinct_new_masks']),'menus':[len(h.get('valid_masks',[])) for h in v['histories']],
      'elapsed_ns':v['elapsed_ns']} for v in result['arms']]}))
