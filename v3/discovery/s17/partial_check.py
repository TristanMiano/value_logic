"""Exact disjunctive information example; Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import importlib.util
import json
import platform
HERE=Path(__file__).resolve().parent
OUT=HERE/'partial_result.json'
CHECKER=HERE.parent/'s16'/'block_check.py'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
spec=importlib.util.spec_from_file_location('s16checker',CHECKER)
ck=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ck)
start=perf_counter_ns()
rows=[]
for name,diag,t,expected in [('C1',['1/100','61/100'],'2','below'),
                            ('C2',['3/10','3/10'],'1','below'),
                            ('convex_hull',['91/400','151/400'],'1','unresolved')]:
    C=[[diag[0],'0'],['0',diag[1]]]
    certificate=dict(schema='response-block-v1',source_id='s17-disjunction-'+name,
                     dimension=2,C_minus=C,C_plus=C,V=[['1/2','1/2'],['1/2','1/2']],
                     edit_squared='1/2',t_lower='1',t_upper=t,threshold='603/1000')
    checked=ck.verify(certificate)
    assert checked['verdict']==expected
    rows.append(dict(case=name,certificate=certificate,checked=checked))
assert F(rows[0]['checked']['upper'])==F(3388,6345)<F(3,5)
assert F(rows[1]['checked']['upper'])==F(3,5)
assert F(rows[2]['checked']['upper'])==F(121,200)>F(603,1000)
s=(F(91,400)+F(151,400))/2
m=(F(91,400)**2+F(151,400)**2)/2
assert s==F(121,400) and m==F(15541,160000)<s/3
record=dict(status='PASS',cases=rows,
            attainment_premise=dict(s=str(s),m=str(m),upper_cap_criterion='m < s/3',
                                    theorem_dependency='proof.md section 7 and parameter_cases.md'),
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
            scope='Exact certificates and cap premise; the finite adverse source comes from the stated theorem, not the checker verdict alone.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',upper=[r['checked']['upper'] for r in rows],elapsed_ns=record['elapsed_ns'])))
