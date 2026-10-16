"""Input-location-only amendment of the exposed finite decision prototype."""
from pathlib import Path
import argparse,hashlib,json
root=Path(__file__).resolve().parent
original=(root/'cnf_decision.py').read_bytes()
assert original.count(b"root/'cr02'")==1
executed=original.replace(b"root/'cr02'",b"root/'cr03'")
namespace={'__name__':'amended_cnf_decision','__file__':str(root/'cnf_decision.py')}
exec(compile(executed,str(root/'cnf_decision.py'),'exec'),namespace)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();assert a.case in (4,5)
    result=namespace['case'](a.case)
    result['amendment']={'kind':'input-location-only','original_sha256':hashlib.sha256(original).hexdigest(),
        'executed_source_sha256':hashlib.sha256(executed).hexdigest(),
        'wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'replacement':"root/'cr02' -> root/'cr03'"}
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':a.case,'name':result['name'],'results':[{k:v[k] for k in ('arm','lower','upper','gap','variables','world_inequalities','elapsed_ns')} for v in result['results']]}))
