"""DEVELOPMENT: one-column geometry and a rank-minimal compression dilation."""
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import math
import platform
import numpy as np
from scipy.optimize import minimize_scalar

here=Path(__file__).resolve().parent
out=here/'rank_probe.json'
assert not out.exists(), 'Preserve original evidence.'
start=perf_counter_ns()

def one_column(a):
    p=a/math.sqrt(10)
    q=math.sqrt(1.9*a*a-1)
    def loss(theta):
        x=p+math.cos(theta);y=q+math.sin(theta)
        return 1-x*x/(1+x*x+y*y)
    grid=np.linspace(-math.pi,math.pi,1001)
    idx=min(range(1001),key=lambda j:loss(grid[j]))
    lo=grid[max(0,idx-1)];hi=grid[min(1000,idx+1)]
    opt=minimize_scalar(loss,bounds=(lo,hi),method='bounded',
                        options={'xatol':1e-13})
    return {'a':a,'loss':float(opt.fun),'theta':float(opt.x)}

geometry=[one_column(float(a)) for a in np.geomspace(1,1000,45)]
assert min(row['loss'] for row in geometry)>.45+1e-5
assert geometry[0]['loss']==min(row['loss'] for row in geometry)

dilations=[]
for lams in ([.1,.9],[.2,.4,.8],[1,.3,.7]):
    C=np.diag(lams);H=np.eye(len(lams))-C
    c=np.ones(len(lams))/math.sqrt(len(lams))
    s=float(c@C@c);m0=float(c@C@C@c);Q=s-m0
    for tau in (.01,.25,.9):
        b=math.sqrt(tau/Q)*C@H@c
        d=1-float(b@np.linalg.pinv(H)@b)
        S=np.block([[C,b[:,None]],[b[None,:],np.array([[d]])]])
        vals=np.linalg.eigvalsh(S)
        rank=int(np.linalg.matrix_rank(np.eye(len(S))-S,tol=1e-9))
        expected=int(np.linalg.matrix_rank(H,tol=1e-9))
        target=np.r_[c,0]
        assert vals.min()>0 and vals.max()<1+1e-10
        assert rank==expected
        assert abs(float(target@S@S@target)-(m0+tau*Q))<1e-10
        dilations.append({'lambdas':list(lams),'tau':tau,'source_rank':rank,
                          'dimension':len(S),'min_eigenvalue':float(vals.min())})

result={'status':'PASS','scope':'45 geometric samples, 9 rank-minimal dilations; no global optimization proof',
        'python':platform.python_version(),'numpy':np.__version__,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'elapsed_ns':perf_counter_ns()-start,'one_column':geometry,'dilations':dilations}
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'first':geometry[0],
                  'last':geometry[-1],'dilations':len(dilations),
                  'elapsed_ns':result['elapsed_ns']}))
