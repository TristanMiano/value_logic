"""Runtime-only amendment of the exposed CNF selector, Codex (GPT-6)."""
from pathlib import Path
import argparse,hashlib,json,platform,sys
root=Path(__file__).resolve().parent
deps=root.parents[2]/'dist'/'s11sat312'
sys.path.insert(0,str(deps))
import pysat
import pysat.solvers
import pysolvers
from cnf_select import case
assert sys.version_info[:2]==(3,12)
assert Path(pysat.__file__).is_relative_to(deps)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();assert a.case in (4,5)
    result=case(a.case)
    result['amendment']={'kind':'runtime-only','python':platform.python_version(),'pysat':pysat.__version__,
       'wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'package_sha256':{Path(v).name:hashlib.sha256(Path(v).read_bytes()).hexdigest() for v in (pysat.__file__,pysat.solvers.__file__,pysolvers.__file__)}}
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':a.case,'name':result['name'],'queries':result['query_variables'],
      'selector_reads':result['selector_model_bit_reads'],'arms':[{'reuse':v['reuse'],'counts':v['counts'],
      'new_masks':len(v['distinct_new_masks']),'menus':[len(h.get('valid_masks',[])) for h in v['histories']],
      'elapsed_ns':v['elapsed_ns']} for v in result['arms']]}))
