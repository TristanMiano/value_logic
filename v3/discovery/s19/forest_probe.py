"""Small precommitted development panel for sparse receipt inference."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,random,sys,time,traceback
import forest_solver as tree
import exact_flat_probe as lin
import anchor_range_check as ar

HERE=Path(__file__).resolve().parent

def box(d):
    rows=[]
    for i in range(d):
        a=[0]*d; a[i]=1; rows.append(a+[1])
        a=[0]*d; a[i]=-1; rows.append(a+[0])
    return rows

def inputs():
    rng=random.Random(191936); cases=[]
    for trial in range(72):
        n=1+trial%5; k=trial%6; dims=[1+(trial+i)%2 for i in range(n)]
        groups=[]; parent=list(range(n+k))
        def root(a):
            while parent[a]!=a: a=parent[a]
            return a
        for j in range(k):
            order=list(range(n)); rng.shuffle(order); chosen=[]
            for i in order:
                a,b=root(i),root(n+j)
                if a!=b:
                    parent[a]=b; chosen.append(i)
                if len(chosen)>=1+trial%3: break
            groups.append(chosen)
        if trial%2:
            missing=[(j,i) for j in range(k) for i in range(n) if i not in groups[j]]
            rng.shuffle(missing)
            for j,i in missing[:trial%3]: groups[j].append(i)
        bases=[box(d) for d in dims]
        for i,d in enumerate(dims):
            if d==2: bases[i].append([1,1,Q(3,2)])
        gs=[{i:[rng.randrange(-2,3) for _ in range(dims[i])]+[rng.randrange(3)]
             for i in group} for group in groups]
        vals=[min(lin.evaluate(g,[Q(1,4)]*dims[i]) for i,g in group.items()) for group in gs]
        eps=Q(trial%2,3)
        los=[v-eps for v in vals]; his=[v+eps for v in vals]
        if k and trial%5==0: his[-1]-=Q(1,2); los[-1]=his[-1]-Q(1,3)
        fs=[[rng.randrange(-3,4) for _ in range(d)]+[rng.randrange(4)] for d in dims]
        cases.append(dict(bases=bases,gs=gs,los=los,his=his,fs=fs,kind='seeded'))
    for t in (1,2):
        bases=[box(t)]+[box(1) for _ in range(t)]; gs=[]
        for j in range(t):
            a=[0]*t; a[j]=1; b=[-x for x in a]
            gs.extend([{0:a+[0],j+1:[1,0]},{0:b+[1],j+1:[-1,1]}])
        cases.append(dict(bases=bases,gs=gs,los=[Q(0)]*(2*t),his=[Q(0)]*(2*t),
                          fs=[[2**j for j in range(t)]+[0]]+[[0,2**t] for _ in range(t)],
                          kind='tight',expected=[(Q(v),Q(v)) for v in range(2**t)]))
    return cases

def tables(case,counts):
    base=tree.base_rows(case); k=len(case['gs']); result=[]
    for i,f in enumerate(case['fs']):
        tab={}
        for mask in range(1<<k):
            if any(mask&1<<j and i not in case['gs'][j] for j in range(k)): continue
            rows=base[i]+[tree.upper_row(case,j,i) for j in range(k) if mask&1<<j]
            vs=lin.vertices(rows,(),len(f)-1); counts['reference_local_slices']+=1
            if vs:
                vals=[lin.evaluate(f,x) for x in vs]; tab[mask]=(min(vals),max(vals))
        result.append(tab)
    return result

def run():
    cases=inputs(); blob=(json.dumps(lin.encode(cases),indent=2)+'\n').encode()
    (HERE/'forest_inputs.json').write_bytes(blob)
    counts={'reference_local_slices':0}; results=[]; forests=0; empty=0; witnesses=0
    for index,case in enumerate(cases):
        got=tree.cycle_range(case,counts)
        expected=ar.anchored(tables(case,counts),len(case['gs']))['ranges']
        assert got['ranges']==expected,(index,got,expected)
        if case['kind']=='tight': assert got['ranges']==case['expected']
        assert len(got['ranges'])<=1<<got['rank']
        if got['rank']==0:
            forests+=1; assert len(got['ranges'])<=1
        empty+=not got['ranges']; witnesses+=got['witnesses']
        results.append(dict(case=index,**got))
    return dict(cases=len(cases),forests=forests,empty=empty,source_witnesses=witnesses,
                input_sha256=hashlib.sha256(blob).hexdigest(),counts=counts,rows=results)

if __name__=='__main__':
    plan=json.loads((HERE/'forest_plan.json').read_text())
    for name,digest in plan['dependencies'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
    assert not (HERE/'forest_result.json').exists()
    started=time.monotonic_ns()
    try: result=dict(status='PASS',results=run())
    except Exception: result=dict(status='FAIL',traceback=traceback.format_exc())
    result['elapsed_ns']=time.monotonic_ns()-started
    (HERE/'forest_result.json').write_bytes((json.dumps(lin.encode(result),indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k!='results'}))
    if result['status']=='FAIL': sys.exit(1)
