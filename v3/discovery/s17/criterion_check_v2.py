"""New block diameter criterion screen; Codex (GPT-6), DEVELOPMENT."""
from pathlib import Path
from time import perf_counter_ns
from fractions import Fraction as F
import ast
import hashlib
import json
import platform
import numpy as np
import sympy as sp

HERE=Path(__file__).resolve().parent
OUT=HERE/'criterion_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
SOURCE=HERE/'paired_probe.py'
tree=ast.parse(SOURCE.read_text(encoding='utf-8'))
namespace={}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef))],type_ignores=[]),str(SOURCE),'exec'),namespace)
prior=json.loads((HERE/'pair_radius_result.json').read_text())
unit=next(r for r in prior['radii'] if r['radius']=='1')
qlo,qhi=map(F,unit['q_interval'])
llo,lhi=1/(1+qhi),1/(1+qlo)
assert F(22,85)<llo<lhi<F(5,14)
start=perf_counter_ns()
q=float((qlo+qhi)/2)
a=np.sqrt(q)
lam=1/(1+q)
g=4*a*(1+a*a)/((1+(a-1)**2)*(1+(a+1)**2))
z=sp.symbols('lambda',real=True)
C=sp.diag(sp.Rational(1,10),sp.Rational(3,10))
c=sp.ones(2,1)/sp.sqrt(2)
s=(c.T*C*c)[0]
m=(c.T*C*C*c)[0]
b0=(c.T*C*(sp.eye(2)-C).inv()*c)[0]
b=(z*C-C*C)*c
A=z*s-m
D=z-(b.T*C*c)[0]/A
assert sp.cancel(D-(b.T*C.inv()*b)[0]/A)==0
assert sp.cancel(1-D-(b.T*(sp.eye(2)-C).inv()*b)[0]/A-(1-z)*(s-(1-z)*b0)/A)==0
assert sp.cancel((b.T*(C-C*C).inv()*b)[0]-A-(1-z)*((1-z)*b0-s))==0
Cnum=np.array(C,dtype=float)
cnum=np.ones(2)/np.sqrt(2)
bnum=(lam*Cnum-Cnum@Cnum)@cnum
Anum=lam*float(s)-float(m)
Bnum=bnum/np.sqrt(Anum)
Dnum=lam-bnum@Cnum@cnum/Anum
S0=np.block([[Cnum,Bnum[:,None]],[Bnum[None,:],np.array([[Dnum]])]])
v=np.r_[cnum,0.]
assert np.linalg.norm(S0@S0@v-lam*S0@v)<1e-14
rows=[]
for delta in (1e-2,1e-4,1e-6,1e-8):
    S=(1-delta)*S0+delta*np.diag([.1,.3,.5])
    eig,U=np.linalg.eigh(S)
    assert min(eig)>0 and max(eig)<1 and np.max(np.abs(S[:2,:2]-Cnum))<1e-15
    singular=np.sqrt(1/eig-1)
    contrast=float((U.T@v)**2@(1/(1+(singular-1)**2)-1/(1+(singular+1)**2)))
    gap=g*float(s)-contrast
    assert gap>=-1e-12
    rows.append(dict(delta=delta,contrast=contrast,gap_to_sharp_supremum=gap,
                     source_norm=float(max(singular)),resolvent_eigenvalues=eig.tolist()))
assert rows[-1]['gap_to_sharp_supremum']<1e-6
controls=[]
for diag,should_equal in [([.1,.3],True),([.1,.4],False)]:
    block=np.diag(diag)
    ordinary=namespace['paired'](block,[cnum,cnum],[1.,1.])
    universal=g*float(cnum@block@cnum)
    gap=universal-ordinary['value']
    assert ordinary['status'] in ('optimal','optimal_inaccurate') and ordinary['max_constraint_violation']<5e-7
    assert abs(gap)<1e-6 if should_equal else gap>1e-4
    controls.append(dict(diagonal=diag,criterion_predicts_equality=should_equal,
                         universal_bound=universal,ordinary=ordinary,gap=gap))
record=dict(status='PASS',symbolic_identities=3,contact_interval=[str(llo),str(lhi)],
            approaching_sequence=rows,ordinary_controls=controls,elapsed_ns=perf_counter_ns()-start,
            python=platform.python_version(),numpy=np.__version__,sympy=sp.__version__,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            kernel_source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            coefficient_evidence_sha256=hashlib.sha256((HERE/'pair_radius_result.json').read_bytes()).hexdigest(),
            scope='Three exact Schur identities, exact criterion signs, four floating finite witnesses and two approximate SDPs. Strict gap theorem is in pair_criterion.md; floating gaps are not rigorous numerical bounds.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',last_witness=rows[-1],gaps=[r['gap'] for r in controls],elapsed_ns=record['elapsed_ns'])))

