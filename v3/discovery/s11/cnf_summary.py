"""Read retained outputs; no new solver run or truth acquisition."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent;rows=[]
for i in range(6):
    menu_path=root/('cr02' if i<4 else 'cr03')/('c%02da0.json'%i)
    result_path=root/('cd01' if i<4 else 'cd02')/('c%02da0.json'%i)
    menu=json.loads(menu_path.read_text());data=json.loads(result_path.read_text())
    by={v['arm']:v for v in data['results']};full=by['full'];row={'case':i,'name':data['name'],
      'models':menu['source_model_count'],'query_variables':menu['query_variables'],
      'new_masks':len(menu['arms'][0]['distinct_new_masks']),'selector_model_bit_reads':menu['selector_model_bit_reads'],
      'native_calls':[v['counts']['native_calls'] for v in menu['arms']],
      'inputs':{p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (menu_path,result_path)},
      'regret_enclosures':{k:{p:v[p] for p in ('lower','upper','gap')} for k,v in by.items()}}
    row['certified_relative_reduction']={k:str(1-F(full['upper'])/F(by[k]['lower'])) if F(by[k]['lower'])>0 else None for k in ('static_menu','no_query')}
    row['full_policy_world_ranges']={k:[str(min(F(v[k]) for v in full['world_metrics'])),str(max(F(v[k]) for v in full['world_metrics']))] for k in ('expected_queries','expected_flips','new_menu_use_probability')}
    rows.append(row)
result={'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','rows':rows,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (root/'cnf_results.json').open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(result,indent=2)+'\n')
for r in rows:
    print(r['name'],r['query_variables'],r['new_masks'],
      {k:tuple(float(F(v[p])) for p in ('lower','upper')) for k,v in r['regret_enclosures'].items()},
      {k:None if v is None else float(F(v)) for k,v in r['certified_relative_reduction'].items()},r['full_policy_world_ranges'])
