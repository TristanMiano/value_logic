"""Explicit common-grid amendment to robust_game.py; preserve original evidence."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import robust_game as game

DENOMINATOR=1048576


def grid_distribution(raw):
    clipped=[max(F(0),F(float(x))) for x in raw]
    total=sum(clipped,F(0));assert total>0
    scaled=[x*DENOMINATOR/total for x in clipped]
    units=[x.numerator//x.denominator for x in scaled]
    remaining=DENOMINATOR-sum(units)
    order=sorted(range(len(units)),key=lambda i:(scaled[i]-units[i],-i),reverse=True)
    for i in order[:remaining]:units[i]+=1
    result=[F(x,DENOMINATOR) for x in units]
    assert all(x>=0 for x in result) and sum(result)==1
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    game.distribution=grid_distribution
    result=game.case(args.case)
    result['probability_grid']=DENOMINATOR
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['dependencies']={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('robust_game.py','query_flip.py','robust_flip.py')}
    last=result['history'][-1]
    result['max_final_mixture_bits']=max(max(F(x).numerator.bit_length(),F(x).denominator.bit_length()) for x in last['alpha']+last['beta'])
    with args.out.open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','m','status','nominal_regret','elapsed_ns','max_final_mixture_bits')}|{k:last[k] for k in ('iteration','policies','scenarios','upper','lower','gap')}))


if __name__=='__main__':main()
