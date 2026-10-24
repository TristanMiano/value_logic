"""Exact finite-source square-root precision obstruction; DEVELOPMENT.

Codex (GPT-6). Four constructed scales, not an empirical performance panel.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import importlib.util
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'precision_result_v2.json'
CHECKER=HERE.parent/'s16'/'block_check.py'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
spec=importlib.util.spec_from_file_location('block_check_precision',CHECKER)
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
start=perf_counter_ns()
rows=[]
for R in (8,32,128,512):
    q=F(R*R)
    CA=[1/(1+q),q*q/(1+q*q)]
    CB=[1/(1+q*q),q*q/(1+q*q)]
    # M_A=diag(R,R^-2), N_A=[[R,0],[-1,R^-2]].
    # Invert I+N_A*N_A^T with an independent two-by-two formula.
    a=1+q; b=F(-R); d=2+1/(q*q)
    determinant=a*d-b*b
    actual=(a+d-2*b)/(2*determinant)
    assert actual==(q+3+1/(q*q)+2*R)/(2*(q+2+(q+1)/(q*q)))
    assert actual>=F(1,2)+F(1,2*R)
    t=q+1
    au=1+t; du=t-1-1/t
    upper=sum(au*x/(1+du*x) for x in CB)/2
    assert upper<=F(1,2)+1/q+1/(q*q)
    gap=actual-upper
    distance=CA[0]-CB[0]
    assert gap>=F(1,4*R)>0
    assert distance>0 and distance<=1/q
    assert gap*gap>=distance/16
    threshold=(actual+upper)/2
    def receipt(diagonal,label):
        matrix=[[str(diagonal[0]),'0'],['0',str(diagonal[1])]]
        return dict(schema='response-block-v1',source_id=label,dimension=2,
                    C_minus=matrix,C_plus=matrix,
                    V=[['1/2','1/2'],['1/2','1/2']],edit_squared='1',
                    t_lower='2',t_upper=str(t),threshold=str(threshold))
    rb=receipt(CB,f'precision-B-R{R}')
    ra=receipt(CA,f'precision-A-R{R}')
    vb=checker.verify(rb); va=checker.verify(ra)
    assert vb['verdict']=='below' and F(vb['upper'])==upper
    assert va['verdict']!='below' and F(va['upper'])>=actual
    rows.append(dict(R=R,A_source_diagonal=[str(R),str(1/q)],
                     B_source_diagonal=[str(q),str(1/q)],
                     A_edit=[['0','0'],['-1','0']],edit_norm_squared='1',
                     A_block_diagonal=list(map(str,CA)),B_block_diagonal=list(map(str,CB)),
                     distance=str(distance),A_feasible_value=str(actual),
                     B_upper=str(upper),separation=str(gap),
                     separation_over_distance=str(gap/distance),
                     threshold=str(threshold),A_receipt=ra,A_result=va,
                     B_receipt=rb,B_result=vb))
record=dict(status='PASS',rows=rows,elapsed_ns=perf_counter_ns()-start,
            python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
            scope='Four exact constructed finite-source instances; universal scaling rests on the accompanying algebra, not enumeration.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',elapsed_ns=record['elapsed_ns'],rows=[
    dict(R=r['R'],distance=float(F(r['distance'])),separation=float(F(r['separation'])),
         ratio=float(F(r['separation_over_distance']))) for r in rows])))
