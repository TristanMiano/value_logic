"""Development screen: exact coverage-menu polytopes and homogeneous shortcut."""
from itertools import combinations
from pathlib import Path
import hashlib, json, random, sys, time, traceback
import anchor_range_check as ar

HERE=Path(__file__).resolve().parent

def table(menu,k):
    out={}
    for t in range(1<<k):
        values=[v for mask,v in menu if mask&t==t]
        if values: out[t]=(min(values),max(values))
    return out

def shortcut(tab,k,n):
    if k==0: return [tab[0]]
    if any(1<<j not in tab for j in range(k)): return []
    lower=min(tab[1<<j][0] for j in range(k))
    upper=min(tab[1<<j][1] for j in range(k))
    if n>k or any((1<<a)|(1<<b) in tab for a,b in combinations(range(k),2)):
        lower=tab[0][0]
    return [(lower,upper)]

def inputs():
    rng=random.Random(191933); rows=[]
    for trial in range(180):
        k=trial%7; n=max(1,k+trial%2)
        menu=sorted(set((rng.randrange(1<<k),rng.randrange(-20,21))
                        for _ in range(1+trial%14)))
        rows.append(dict(kind='homogeneous',k=k,menus=[menu]*n))
    for k,n in ((2,2),(3,3),(4,2),(4,4),(6,2),(6,3),(6,6),(8,2),(8,4)):
        r=k//n
        masks=[sum(1<<a for a in c) for c in combinations(range(k),r)]
        for repeat in range(12):
            costs=list(range(n*len(masks))); rng.shuffle(costs)
            menus=[list(zip(masks,costs[i*len(masks):(i+1)*len(masks)])) for i in range(n)]
            rows.append(dict(kind='exact_cover',k=k,menus=menus))
    return rows

def run():
    rows=inputs(); blob=(json.dumps(rows,indent=2)+'\n').encode()
    (HERE/'menu_range_inputs.json').write_bytes(blob)
    out=[]; homogeneous=0; checks=0; maxima={}
    for index,row in enumerate(rows):
        k=row['k']; tabs=[table(m,k) for m in row['menus']]; n=len(tabs)
        actual=ar.anchored(tabs,k)['ranges']
        if row['kind']=='homogeneous':
            expected=shortcut(tabs[0],k,n)
            assert actual==expected,(index,actual,expected)
            homogeneous+=1
        if n**k<=20000:
            expected,_=ar.brute(tabs,k)
            assert actual==expected,(index,actual,expected)
            checks+=1
        key=f'{row["kind"]}:k{k}:n{n}'
        if key not in maxima or len(actual)>maxima[key]['components']:
            maxima[key]=dict(case=index,components=len(actual),ranges=actual)
        out.append(dict(case=index,components=len(actual)))
    return dict(cases=len(rows),homogeneous_checks=homogeneous,
                assignment_crosschecks=checks,input_sha256=hashlib.sha256(blob).hexdigest(),
                maxima=maxima,rows=out)

if __name__=='__main__':
    start=time.monotonic_ns()
    result=dict(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    try: result.update(status='COMPLETED_SCREEN',results=run())
    except Exception:
        result.update(status='FAILED',traceback=traceback.format_exc())
    result['elapsed_ns']=time.monotonic_ns()-start
    (HERE/'menu_range_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k!='results'}))
    if result['status']=='FAILED': sys.exit(1)
