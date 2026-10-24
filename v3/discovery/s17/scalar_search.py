"""Finite exact rational parameter search for the existing response checker.

Codex (GPT-6), DEVELOPMENT. This is conventional ternary search on the
proved unimodal scalar families. It does not change the bounded checker.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import importlib.util
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'scalar_search_result.json'
CHECKER=HERE.parent/'s16'/'block_check.py'
spec=importlib.util.spec_from_file_location('s16checker',CHECKER)
ck=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ck)


def search(C,V,E,gamma):
    assert E>0 and 0<gamma<1
    n=len(C)
    I=ck.identity(n)
    assert ck.positive(C,True) and ck.positive(ck.add(I,C,-1),True)
    assert ck.positive(V) and sum(V[i][i] for i in range(n))==1
    lip=E+2
    cap_lo,cap_hi=E,E+1
    cap_steps=0
    while lip*(cap_hi-cap_lo)>gamma/4:
        mid=(cap_lo+cap_hi)/2
        if mid*mid>=E*(1+mid):
            cap_hi=mid
        else:
            cap_lo=mid
        cap_steps+=1
    assert cap_hi*cap_hi>=E*(1+cap_hi)
    T=E+1+4*E/gamma
    counters={'denominator_inversions':0,'objective_evaluations':0}

    def evaluate(t,upper):
        assert t>=cap_hi
        a,d=1+t,t-E-E/t
        den=ck.add(I,C,d) if upper else ck.add([[a*z for z in row] for row in I],C,-d)
        value=ck.weighted_trace(V,ck.mul(C,ck.inverse(den)))
        counters['denominator_inversions']+=1
        counters['objective_evaluations']+=1
        return a*value if upper else value

    results=[]
    for upper in (False,True):
        left,right=cap_hi,T
        steps=0
        while lip*(right-left)>gamma/4:
            x=(2*left+right)/3
            y=(left+2*right)/3
            vx,vy=evaluate(x,upper),evaluate(y,upper)
            if vx==vy:
                left,right=x,y
            elif (vx<vy)==upper:
                right=y
            else:
                left=x
            steps+=1
        t=(left+right)/2
        value=evaluate(t,upper)
        results.append(dict(t=str(t),value=str(value),steps=steps,
                            final_parameter_width=str(right-left)))
    assert counters['denominator_inversions']==2*sum(r['steps'] for r in results)+2
    return dict(lower=results[0],upper=results[1],cap_bisections=cap_steps,
                cap_interval=list(map(str,(cap_lo,cap_hi))),horizon=str(T),
                gamma=str(gamma),counts=counters)


if __name__=='__main__':
    if OUT.exists():
        raise SystemExit('Refusing to overwrite observed evidence.')
    start=perf_counter_ns()
    equal=[[F(1,2)]*2 for _ in range(2)]
    cases=[('exact_scalar',[[F(9,10)]],[[F(1)]],F(1,100),F(1,2),'above'),
           ('small_edit_block',[[F(1,10),F(0)],[F(0),F(9,10)]],equal,F(1,100),F(539,1000),'below'),
           ('cancellation_control',[[F(1,1601),F(0)],[F(0),F(9,10)]],equal,F(9),F(3,5),'below')]
    rows=[]
    for name,C,V,E,threshold,expected in cases:
        gamma=F(1,4096)
        result=search(C,V,E,gamma)
        encode=lambda A:[[str(x) for x in row] for row in A]
        cert=dict(schema='response-block-v1',source_id='s17-search-'+name,
                  dimension=len(C),C_minus=encode(C),C_plus=encode(C),V=encode(V),
                  edit_squared=str(E),t_lower=result['lower']['t'],
                  t_upper=result['upper']['t'],threshold=str(threshold))
        checked=ck.verify(cert)
        assert checked['verdict']==expected
        if name=='exact_scalar':
            true_lower,true_upper=F(900,1069),F(900,949)
            assert 0<=true_lower-F(checked['lower'])<gamma/2
            assert 0<=F(checked['upper'])-true_upper<gamma/2
        rows.append(dict(case=name,search=result,certificate=cert,checked=checked))
        print(json.dumps(dict(case=name,verdict=checked['verdict'],
              lower=float(F(checked['lower'])),upper=float(F(checked['upper'])),
              counts=result['counts'])))
    record=dict(status='PASS',cases=rows,elapsed_ns=perf_counter_ns()-start,
                python=platform.python_version(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
                scope='Three exact finite search/certificate screens; external premises assumed, no completeness for the fixed bit-limited format, no speedup claim.')
    OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(status='PASS',elapsed_ns=record['elapsed_ns'])))
