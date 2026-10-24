"""Exact decision and precision audit; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
from time import perf_counter_ns

HERE=Path(__file__).resolve().parent
CHECKER=HERE.parent/'s16'/'block_check.py'
spec=importlib.util.spec_from_file_location('preserved_checker',CHECKER)
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def main():
    output=HERE/'decision_result.json'
    if output.exists():
        raise SystemExit('Refusing to overwrite an observed result.')
    start=perf_counter_ns()
    fixture=HERE.parent/'s16'/'block_receipt.json'
    base=json.loads(fixture.read_text())
    threshold=F(base['threshold'])
    assert F(100,221)<threshold<F(100,181)
    results=[]
    for factor in (1,64,128):
        delta=F(factor,100000)
        lo=[[str(F(1,10)-delta),'0'],['0',str(F(9,10)-delta)]]
        hi=[[str(F(1,10)+delta),'0'],['0',str(F(9,10)+delta)]]
        receipt=dict(base,C_minus=lo,C_plus=hi)
        answer=checker.verify(receipt)
        t=F(receipt['t_upper']); E=F(receipt['edit_squared'])
        d=t-E-E/t
        direct=(1+t)/2*sum(z/(1+d*z) for z in (F(1,10)+delta,F(9,10)+delta))
        assert direct==F(answer['upper'])
        assert answer['verdict']==('below' if factor in (1,64) else 'unresolved')
        results.append(dict(factor=factor,scalar_half_width=str(F(2,5)*delta),
                            matrix_half_width=str(delta),result=answer,
                            upper_margin=str(threshold-direct),receipt=receipt))
    record=dict(status='PASS',cases=results,
                scalar_only_feasible_values=['100/221','100/181'],
                threshold=str(threshold),
                precision_statement='64-fold looser absolute scalar half-width (six binary bits) still certifies this decision; no measured cost reduction.',
                elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
                fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest())
    output.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(status=record['status'],elapsed_ns=record['elapsed_ns'],
                         cases=[dict(factor=c['factor'],upper=float(F(c['result']['upper'])),
                                     verdict=c['result']['verdict']) for c in results])))


if __name__=='__main__':
    main()
