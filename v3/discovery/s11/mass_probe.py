"""DEVELOPMENT lower-mass source screen, Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
from query_flip import signs,compact_plan
from robust_flip import regret_oracle,point_source,policy_value


def case(index):
    root=Path(__file__).resolve().parent
    path=root/'rf01'/('c07a0.json' if index==0 else 'c08a0.json')
    data=json.loads(path.read_text(encoding='utf-8'))
    m,r,H=data['m'],data['r'],data['horizon']
    p0=list(map(F,data['mass']))
    w,f,q=(tuple(map(F,data[key])) for key in ('weights','flip_fee','query_fee'))
    rows=[(F(row['fee']),tuple(map(F,row['coefficients']))) for row in data['proposal']]
    box=[[(F(lo),F(hi)) for lo,hi in row] for row in data['box']]
    results=[]
    for eps in (F(0),F(1,4),F(1)):
        candidates=[]
        for zstar in range(1 if eps==0 else 2**r):
            mass=[(1-eps)*p+eps*int(z==zstar) for z,p in enumerate(p0)]
            src={'m':m,'r':r,'cells':signs(r),'mass':mass}
            R,action,witness,adversary,counts=regret_oracle(src,rows,w,f,q,H,box)
            exact=compact_plan(point_source(src,witness),w,f,q,H)[0]
            assert policy_value(src,rows,w,witness)-exact==R
            checks=0
            if index==0:
                upper=F(0)
                for vals in product(*(tuple(sorted(set(pair))) for row in box for pair in row)):
                    mu=[list(vals[t*(m-r):(t+1)*(m-r)]) for t in range(2**r)]
                    opt=compact_plan(point_source(src,mu),w,f,q,H)[0]
                    upper=max(upper,policy_value(src,rows,w,mu)-opt)
                    checks+=1
                assert upper==R
            candidates.append({'mass_vertex':zstar,'mass':list(map(str,mass)),'regret':str(R),
                               'witness':[[str(x) for x in row] for row in witness],
                               'corner_checks':checks,'oracle_counts':counts})
        worst=max(candidates,key=lambda c:F(c['regret']))
        results.append({'epsilon':str(eps),'worst_regret':worst['regret'],'worst_vertex':worst['mass_vertex'],'candidates':candidates})
    assert all(F(results[i]['worst_regret'])<=F(results[i+1]['worst_regret']) for i in range(len(results)-1))
    return {'case':index,'input':path.relative_to(root).as_posix(),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'm':m,'r':r,'horizon':H,'results':results,
            'scope':'Exact worst regret over a lower-bounded cell-mass simplex and conditional-mean boxes; all source premises stipulated.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case);result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['dependencies']={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('query_flip.py','robust_flip.py')}
    with args.out.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**result,'results':[{k:v for k,v in row.items() if k!='candidates'} for row in result['results']]}))


if __name__=='__main__':main()
