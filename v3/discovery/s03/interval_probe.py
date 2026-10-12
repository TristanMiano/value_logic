"""Small graded-bet coverage and partial-computation checks. DEVELOPMENT."""
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
import hashlib,json,random,sys,time
from interval_bets import wealth,mixture,reject,interval
from policy_values import evaluate


def main(out):
    assert not out.exists();start=time.perf_counter_ns();coverage=[];domination=refinements=0
    for ys in product((F(0),F(1,2),F(1)),repeat=3):
        for T in (F(1),F(3,2),F(2)):
            if sum(ys)>T:continue
            for alpha in (F(1,2),F(1,3)):
                crossings=paths=0
                for order in permutations(range(3)):
                    for coins in product((0,1),repeat=3):
                        values=[];cross=False
                        for i,coin in zip(order,coins):
                            values.append(ys[i] if coin else ys[i]/2)
                            cross|=reject(values,3,T,alpha)
                        crossings+=int(cross);paths+=1
                rate=F(crossings,paths);assert rate<=alpha
                coverage.append({'truth':list(map(str,ys)),'null_total':str(T),'alpha':str(alpha),'paths':paths,'crossings':crossings,'exact_crossing_probability':str(rate)})
        for levels in product((0,1,2),repeat=3):
            partial=[y*F(level,2) for y,level in zip(ys,levels)]
            for end in range(1,4):
                v=mixture(partial[:end],3,sum(ys));full=mixture(ys[:end],3,sum(ys));assert v<=full;domination+=1
                for j in range(end):
                    better=list(partial[:end]);better[j]=ys[j];assert mixture(better,3,sum(ys))>=v;refinements+=1
    source=Path(__file__).with_name('policy01.json');data=json.loads(source.read_text());rng=random.Random(14815);bounds=0
    for row in data['cases']:
        poly={int(k):F(v) for k,v in row['polynomial'].items()};m=row['m'];order=list(range(m));rng.shuffle(order)
        for world in range(1<<m):
            true=evaluate(poly,world);known={};lo,hi=interval(poly,known);assert lo<=true<=hi
            for i in order:
                known[i]=-1 if world&(1<<i) else 1;newlo,newhi=interval(poly,known)
                assert lo<=newlo<=true<=newhi<=hi;lo,hi=newlo,newhi;bounds+=1
            assert lo==hi==true
    # Explicit complementarity: any proper parity prefix gives no interval gain.
    parity={31:F(1)}
    for n in range(5):assert interval(parity,{i:1 for i in range(n)})==(F(-1),F(1))
    assert interval(parity,{i:1 for i in range(5)})==(F(1),F(1))
    result={'status':'complete','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','python':sys.version,
            'sources':{p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ('interval_bets.py','interval_probe.py','policy_values.py')},
            'policy_input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'coverage':coverage,
            'domination_checks':domination,'monotone_refinements':refinements,'partial_bound_checks':bounds,'parity_prefix_checks':6,
            'elapsed_ns':time.perf_counter_ns()-start}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k] for k in ('status','domination_checks','monotone_refinements','partial_bound_checks','elapsed_ns')}))


if __name__=='__main__':main(Path(sys.argv[1]))
