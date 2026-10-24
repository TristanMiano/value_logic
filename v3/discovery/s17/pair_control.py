"""Scalar old-primal/dual reuse control; DEVELOPMENT, Codex (GPT-6).

One-dimensional exploratory optimization on a compact angle interval. Its
value is a proposed strong comparator, not an exact global certificate.
"""
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
import numpy as np
import scipy
from scipy.optimize import minimize_scalar

HERE=Path(__file__).resolve().parent
OUT=HERE/'pair_control_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
start=perf_counter_ns()
ratio=3+2*np.sqrt(2)

def pieces(angle):
    m=np.sin(angle)**2
    cross=np.sin(2*angle)
    A=2-m+cross
    B=1+m+cross
    return m,A,B

def simple(angle):
    m,A,B=pieces(angle)
    return A-1/B

def combined(angle):
    m,A,B=pieces(angle)
    return A-max(1/B,A/ratio)

rows=[]
for name,fun in [('primal_dual',simple),('with_pair_ratio',combined)]:
    sol=minimize_scalar(lambda x:-fun(x),bounds=(0,np.pi/2),method='bounded',
                        options={'xatol':1e-14,'maxiter':200})
    assert sol.success
    candidates=[(float(fun(x)),float(x)) for x in (0,np.pi/2,sol.x)]
    value,angle=max(candidates)
    m,A,B=pieces(angle)
    rows.append(dict(control=name,value=value,angle=angle,m=float(m),A=float(A),B=float(B),
                     pair_ratio=float(ratio),iterations=sol.nit,success=bool(sol.success)))
record=dict(status='PASS',rows=rows,elapsed_ns=perf_counter_ns()-start,
            versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='Two exploratory scalar optimizations; universal comparator validity follows from its variational derivation, but these numerical maxima are not exact upper certificates.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(record))
