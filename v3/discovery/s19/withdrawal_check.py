"""Exact development of withdrawal-price profiles; no truth diagnosis."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib, heapq, json, random, sys, time, traceback
import anchor_range_check as a

HERE = Path(__file__).resolve().parent


def decode(x):
    if isinstance(x,str): return Q(x)
    if isinstance(x,list): return tuple(decode(v) for v in x)
    if isinstance(x,dict): return {k:decode(v) for k,v in x.items()}
    return x


def subsets(case, weights):
    k = len(weights)
    records, intervals, splits, slices, assignments = [], [], 0, 0, 0
    for mask in range(1<<k):
        js = [j for j in range(k) if mask>>j&1]
        c = dict(polys=case['polys'],objs=case['objs'],
                 **{key: [case[key][j] for j in js] for key in ('hs','los','his')})
        tabs, ends = a.local_tables(**c)
        result = a.anchored(tabs,len(js))
        reference, steps = a.brute(tabs,len(js))
        assert result['ranges'] == reference
        price = sum(weights[j] for j in range(k) if not(mask>>j&1))
        record = dict(mask=mask, price=price, case=c, tabs=tabs, ends=ends,
                      result=result, reference=reference)
        rid = len(records)
        records.append(record)
        intervals.extend((lo,hi,price,rid) for lo,hi in result['ranges'])
        splits += result['counts']['split_scans']
        slices += len(tabs)*(1<<len(js))
        assignments += steps
    assert splits == 3*len(case['polys'])*4**k
    assert slices == len(case['polys'])*3**k
    return records, intervals, dict(split_scans=splits, local_slice_entries=slices,
                                    reference_assignments=assignments)


def sweep(intervals):
    starts, ends = {}, {}
    for i,(lo,hi,price,rid) in enumerate(intervals):
        starts.setdefault(lo,[]).append(i)
        ends.setdefault(hi,[]).append(i)
    points = sorted(set(starts)|set(ends))
    active, heap, atoms = set(), [], []
    def best():
        while heap and heap[0][1] not in active:
            heapq.heappop(heap)
        return heap[0] if heap else (None,None)
    for pos,x in enumerate(points):
        for i in starts.get(x,[]):
            active.add(i)
            heapq.heappush(heap,(intervals[i][2],i))
        price,i = best()
        atoms.append(dict(lo=x,hi=x,closed=True,price=price,interval=i))
        for i in ends.get(x,[]): active.remove(i)
        if pos+1 < len(points):
            price,i = best()
            atoms.append(dict(lo=x,hi=points[pos+1],closed=False,price=price,interval=i))
    return atoms


def validate(case, weights):
    records, intervals, counts = subsets(case,weights)
    atoms = sweep(intervals)
    witnesses, impossible, cheaper_points = 0, 0, 0
    for index,atom in enumerate(atoms):
        q = (atom['lo']+atom['hi'])/2
        possible = [r['price'] for r in records if any(lo<=q<=hi for lo,hi in r['reference'])]
        expected = min(possible) if possible else None
        assert atom['price'] == expected, (q,atom,possible)
        if expected is None:
            impossible += 1
            continue
        rec = records[intervals[atom['interval']][3]]
        xs = a.recover(rec['result'],rec['tabs'],rec['ends'],q)
        assert all(a.contains(poly,x) for poly,x in zip(case['polys'],xs))
        assert all(lo <= min(a.dot(h,x) for x in xs) <= hi
                   for h,lo,hi in zip(rec['case']['hs'],rec['case']['los'],rec['case']['his']))
        assert min(a.dot(obj[0],x)+obj[1] for obj,x in zip(case['objs'],xs)) == q
        assert rec['price'] == sum(w for j,w in enumerate(weights) if not(rec['mask']>>j&1))
        witnesses += 1
        if atom['closed']:
            neighbors = [atoms[j]['price'] for j in (index-1,index+1) if 0<=j<len(atoms)]
            cheaper_points += any(v is None or expected<v for v in neighbors)
    return dict(atoms=len(atoms),witnesses=witnesses,impossible_atoms=impossible,
                endpoint_price_drops=cheaper_points,**counts), atoms


def run():
    allcases = decode(json.loads((HERE/'anchor_range_inputs.json').read_text()))
    rng = random.Random(191931)
    selected = list(range(40))
    inputs = [dict(index=i,weights=[str(Q(rng.randrange(6),3))
               for _ in allcases[i]['hs']]) for i in selected]
    raw = (json.dumps(inputs,separators=(',',':'))+'\n').encode()
    (HERE/'withdrawal_inputs.json').write_bytes(raw)
    rows=[]
    for item in inputs:
        row,_ = validate(allcases[item['index']],[Q(w) for w in item['weights']])
        rows.append(dict(index=item['index'],**row))
    delta,eps=Q(1,10),Q(1,10)
    bases=[[(0,1),(2,0)],[(0,2),(1,0)]]
    polys=[a.hull([(Q(x)+u,Q(y)+v) for x,y in base
                   for u in (Q(0),delta) for v in (Q(0),delta)]) for base in bases]
    gap=dict(polys=polys,hs=[(Q(1),Q(0)),(Q(0),Q(1))],los=[Q(0),Q(0)],
             his=[eps,eps],objs=[((Q(1),Q(1)),Q(20))]*2)
    worked,atoms=validate(gap,[Q(1),Q(2)])
    r,_,_=subsets(gap,[Q(1),Q(2)])
    assert r[-1]['result']['ranges'] == [(Q(21),Q(106,5)),(Q(219,10),Q(111,5))]
    mids=[d for d in atoms if d['lo']<Q(43,2)<d['hi']]
    assert len(mids)==1 and mids[0]['price']==1
    return dict(cases=len(rows), totals={key:sum(row[key] for row in rows) for key in rows[0] if key!='index'},
                rows=rows,worked=worked,worked_atoms=a.encoded(atoms),
                input_sha256=hashlib.sha256(raw).hexdigest())


if __name__=='__main__':
    plan=json.loads((HERE/'withdrawal_plan.json').read_text())
    for name,digest in plan['dependencies'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
    assert not (HERE/'withdrawal_result.json').exists()
    started=time.perf_counter_ns()
    try:
        result=dict(status='PASS',results=run(),python=sys.version)
        result['runtime_ns']=time.perf_counter_ns()-started
        (HERE/'withdrawal_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
        print(json.dumps({k:v for k,v in result.items() if k!='results'}))
        print(json.dumps({k:v for k,v in result['results'].items() if k not in ('rows','worked_atoms')}))
    except Exception:
        failure=dict(status='FAIL',traceback=traceback.format_exc(),runtime_ns=time.perf_counter_ns()-started)
        (HERE/'withdrawal_failure.json').write_bytes((json.dumps(failure,indent=2)+'\n').encode())
        raise
