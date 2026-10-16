"""Six prospective small boundary cases for the direct LP; DEVELOPMENT."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import random
import time
from scipy.optimize import linprog
from query_flip import source,compact_plan,unrestricted_plan
from robust_flip import point_source,policy_value,independent_law,regret_oracle
from policy_flow import realize
from direct_lp import build,sparse
from lp_certificate import lower_bound


def case(index):
    m,r,H=((2,0,0),(3,0,2),(3,1,1),(4,2,3),(4,1,5),(3,2,2))[index]
    src=source(m,r,2200+index);rng=random.Random(3200+index)
    if index==5:
        mass=[F(0),F(1,6),F(1,3),F(1,2)];src['mass']=mass
    w=tuple(F(rng.choice((-2,-1,0,1,2))) for _ in range(m))
    f=tuple(F(rng.randrange(4),4) for _ in range(m))
    q=tuple(F(rng.randrange(3),5) for _ in range(r))
    box=[]
    for _ in range(2**r):
        row=[]
        for _ in range(m-r):
            ends=sorted((F(rng.randrange(-4,5),4),F(rng.randrange(-4,5),4)))
            row.append(tuple(ends))
        box.append(row)
    start=time.perf_counter_ns()
    arch,eq,beq,ub,bub,bounds,c,names=build(src,w,f,q,H,box)
    lp=linprog(list(map(float,c)),A_ub=sparse(ub,len(c)),b_ub=list(map(float,bub)),
               A_eq=sparse(eq,len(c)),b_eq=list(map(float,beq)),
               bounds=[(float(lo),float(hi)) for lo,hi in bounds],method='highs')
    assert lp.success,lp.message
    realization,rows,local=realize(src,f,q,H,lp.x,arch)
    U,_,witness,_,counts=regret_oracle(src,rows,w,f,q,H,box)
    L,certificate=lower_bound(eq,beq,ub,bub,bounds,c,lp.ineqlin.marginals,lp.eqlin.marginals)
    assert L<=U,(L,U)
    corner_max=None;corners=0;unrestricted=0
    for vals in product(*(tuple(sorted(set(pair))) for row in box for pair in row)):
        mu=[list(vals[z*(m-r):(z+1)*(m-r)]) for z in range(2**r)]
        optimum=compact_plan(point_source(src,mu),w,f,q,H)[0]
        if corners<8:
            full,_=unrestricted_plan(independent_law(src,mu),w,f,q,H)
            assert full==optimum,(full,optimum)
            unrestricted+=1
        regret=policy_value(src,rows,w,mu)-optimum
        corner_max=regret if corner_max is None else max(corner_max,regret)
        corners+=1
    assert corner_max==U,(corner_max,U)
    return {'case':index,'m':m,'r':r,'H':H,'mass':list(map(str,src['mass'])),
            'weights':list(map(str,w)),'flip_fee':list(map(str,f)),'query_fee':list(map(str,q)),
            'box':[[list(map(str,pair)) for pair in row] for row in box],
            'variables':len(c),'numeric_value':lp.fun,'lower':str(L),'upper':str(U),'gap':str(U-L),
            'corners':corners,'unrestricted_checks':unrestricted,'dual_certificate':certificate,
            'raw_primal_advice':list(map(float,lp.x)),
            'final_rows':[{'fee':str(fee),'coefficients':list(map(str,coeff))} for fee,coeff in rows],
            'local_policy':local,'elapsed_ns':time.perf_counter_ns()-start,
            'scope':'Development boundary screen; upper checked at every interval corner, up to eight full interleaved planners per case.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case);result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['dependencies']={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('direct_lp.py','lp_certificate.py','policy_flow.py','query_flip.py','robust_flip.py','robust_game.py','robust_game_grid.py')}
    with args.out.open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','m','r','H','lower','upper','gap','corners','unrestricted_checks','elapsed_ns')}))


if __name__=='__main__':main()
