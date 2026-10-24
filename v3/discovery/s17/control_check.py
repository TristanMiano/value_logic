"""Exact stronger-control comparison, DEVELOPMENT, Codex (GPT-6)."""
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
    output=HERE/'control_result.json'
    if output.exists():
        raise SystemExit('Refusing to overwrite an observed result.')
    start=perf_counter_ns()
    R=F(415769,1000000)
    rlo,rhi=F(403,625),F(64481,100000)
    assert rlo*rlo<R<rhi*rhi
    jlo=F(50129681,100000000)+F(291,5000)*rlo
    jhi=F(50129681,100000000)+F(291,5000)*rhi
    def derivative(r):
        return -F(14127,500000)+F(3,50)*r-F(297693,50000000)/r
    dlo,dhi=derivative(rlo),derivative(rhi)
    assert -F(1,800)<dlo<dhi<F(1,800)
    assert jlo>F(5388,10000) and jhi<F(539,1000)
    lower_certificate=F(5388,10000)-F(1,230400)
    assert lower_certificate>F(1077,2000)
    base=json.loads((HERE.parent/'s16'/'block_receipt.json').read_text())
    cases=[]
    for factor in (1,32,64):
        delta=F(factor,100000)
        receipt=dict(base,threshold='1077/2000',
                     C_minus=[[str(F(1,10)-delta),'0'],['0',str(F(9,10)-delta)]],
                     C_plus=[[str(F(1,10)+delta),'0'],['0',str(F(9,10)+delta)]])
        result=checker.verify(receipt)
        assert result['verdict']==('below' if factor in (1,32) else 'unresolved')
        cases.append(dict(factor=factor,scalar_half_width=str(F(2,5)*delta),
                          matrix_half_width=str(delta),receipt=receipt,result=result))
    record=dict(status='PASS',sqrt_squared=str(R),sqrt_bracket=[str(rlo),str(rhi)],
                alpha='97/100',objective_bracket=[str(jlo),str(jhi)],
                derivative_bracket=[str(dlo),str(dhi)],
                strong_convexity_mu='9/50',two_scalar_optimum_lower=str(lower_certificate),
                original_threshold='539/1000',new_threshold='1077/2000',cases=cases,
                scope='Exact development comparison, conditional on the s14 two-scalar attainment argument and s17 block bound; no empirical savings.',
                elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest())
    output.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(status=record['status'],elapsed_ns=record['elapsed_ns'],
                         two_scalar_lower=float(lower_certificate),
                         cases=[dict(factor=c['factor'],upper=float(F(c['result']['upper'])),verdict=c['result']['verdict']) for c in cases])))


if __name__=='__main__':
    main()
