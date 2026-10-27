"""Precommitted development check of the monotone covering adapter."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json,math,random,sys,time,traceback
import monotone_subset as mono
import fast_subset_probe as old
import anchor_range_check as ar

HERE=Path(__file__).resolve().parent

def inputs():
    rng=random.Random(191935)
    rows=[row for row in product((-1,0,1),repeat=4) if mono.decreasing(row,2)]
    cases=[(2,f,g) for f in rows for g in rows]
    for trial in range(240):
        k=trial%9; size=1<<k
        pair=[]
        for side in range(2):
            row=[rng.choice((-math.inf,-2,-1,0,0,1,2,math.inf)) for _ in range(size)]
            for bit in range(k):
                flag=1<<bit
                for mask in range(size):
                    if mask&flag: row[mask]=min(row[mask],row[mask^flag])
            pair.append(row)
        cases.append((k,*pair))
    return cases,len(rows)**2

def run():
    cases,exhaustive=inputs()
    blob=(json.dumps([(k,list(map(str,f)),list(map(str,g))) for k,f,g in cases],
                     separators=(',',':'))+'\n').encode()
    (HERE/'monotone_subset_inputs.json').write_bytes(blob)
    counts={}; splits=0
    for k,f,g in cases:
        got,back=mono.maxmin(f,g,k,counts)
        expected=[-x for x in old.direct([-x for x in f],[-x for x in g],k)]
        assert got==expected,(k,f,g,got,expected)
        for mask,left in enumerate(back):
            assert left&mask==left and min(f[left],g[mask^left])==got[mask]
            splits+=1
    try: mono.maxmin([0,1],[0,0],1)
    except ValueError: pass
    else: raise AssertionError('Nonmonotone input accepted')
    old.fast=mono
    rows=old.decode(json.loads((HERE/'anchor_range_inputs.json').read_text()))
    expected=json.loads((HERE/'anchor_range_result.json').read_text())['results']['rows']
    witnesses=0
    for index,case in enumerate(rows):
        tabs,ends=ar.local_tables(**case)
        result=old.anchored_fast(tabs,len(case['hs']),counts)
        assert result['ranges']==[tuple(Q(x) for x in p) for p in expected[index]['ranges']]
        for lo,hi in result['ranges']:
            for q in sorted({lo,hi,(lo+hi)/2}):
                xs=ar.recover(result,tabs,ends,q)
                assert all(ar.contains(poly,x) for poly,x in zip(case['polys'],xs))
                assert all(a<=min(ar.dot(h,x) for x in xs)<=b
                           for h,a,b in zip(case['hs'],case['los'],case['his']))
                assert min(ar.dot(obj[0],x)+obj[1] for obj,x in zip(case['objs'],xs))==q
                witnesses+=1
    return dict(kernel_cases=len(cases),exhaustive_monotone_ternary_k2=exhaustive,
                seeded_cases=240,split_checks=splits,polygon_cases=len(rows),
                source_witnesses=witnesses,input_sha256=hashlib.sha256(blob).hexdigest(),**counts)

if __name__=='__main__':
    plan=json.loads((HERE/'monotone_subset_plan.json').read_text())
    for name,digest in plan['dependencies'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
    assert not (HERE/'monotone_subset_result.json').exists()
    started=time.monotonic_ns()
    try: result=dict(status='PASS',results=run())
    except Exception: result=dict(status='FAIL',traceback=traceback.format_exc())
    result['elapsed_ns']=time.monotonic_ns()-started
    (HERE/'monotone_subset_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result))
    if result['status']=='FAIL': sys.exit(1)
