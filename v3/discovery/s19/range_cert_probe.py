"""Development producer and corruption probes for rational range certificates."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import copy, hashlib, json, sys, time, traceback
import anchor_range_check as geometry
import value_set_check as old
import range_cert_verify as verifier

HERE=Path(__file__).resolve().parent

def encode(v):
    if isinstance(v,Q): return str(v)
    if isinstance(v,dict): return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [encode(x) for x in v]
    return v

def decode_case(c):
    return dict(polys=[[tuple(map(Q,p)) for p in poly] for poly in c['polys']],
                hs=[tuple(map(Q,h)) for h in c['hs']],los=list(map(Q,c['los'])),
                his=list(map(Q,c['his'])),objs=[(tuple(map(Q,h)),Q(d)) for h,d in c['objs']])

def hrep(poly):
    if len(poly)<3:
        rows=[(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),(Q(0),Q(-1))]
        rhs=[max(geometry.dot(a,p) for p in poly) for a in rows]
        if len(poly)==2:
            a,b=poly; normal=(b[1]-a[1],a[0]-b[0])
            rows.extend([normal,tuple(-v for v in normal)])
            rhs.extend([geometry.dot(normal,a),-geometry.dot(normal,a)])
        return rows,rhs
    rows=[]; rhs=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        normal=(b[1]-a[1],a[0]-b[0]); rows.append(normal); rhs.append(geometry.dot(normal,a))
    return rows,rhs

def problem_of(c):
    gs=[]
    for poly,(h,d) in zip(c['polys'],c['objs']):
        rows,rhs=hrep(poly); gs.append(dict(A=rows,b=rhs,c=h,d=d))
    rs=[dict(lo=a,hi=b,forms=[dict(c=h,d=Q(0)) for _ in gs]) for h,a,b in zip(c['hs'],c['los'],c['his'])]
    return encode(dict(generators=gs,receipts=rs))

def own_constraints(problem,i,mask):
    g=problem['generators'][i]; rows=[list(map(Q,r)) for r in g['A']]; rhs=list(map(Q,g['b']))
    for j,r in enumerate(problem['receipts']):
        h=list(map(Q,r['forms'][i]['c'])); off=Q(r['forms'][i]['d'])
        rows.append([-v for v in h]); rhs.append(off-Q(r['lo']))
        if mask>>j&1: rows.append(h); rhs.append(Q(r['hi'])-off)
    return rows,rhs,list(map(Q,g['c'])),Q(g['d'])

def solve(columns,target):
    if not columns: return [] if all(v==0 for v in target) else None
    width=len(columns); matrix=[[columns[j][i] for j in range(width)]+[target[i]] for i in range(len(target))]
    pivot=0; pivots=[]
    for col in range(width):
        row=next((r for r in range(pivot,len(matrix)) if matrix[r][col]),None)
        if row is None: return None
        matrix[pivot],matrix[row]=matrix[row],matrix[pivot]
        v=matrix[pivot][col]; matrix[pivot]=[x/v for x in matrix[pivot]]
        for r in range(len(matrix)):
            if r!=pivot:
                v=matrix[r][col]
                matrix[r]=[a-v*b for a,b in zip(matrix[r],matrix[pivot])]
        pivots.append(pivot); pivot+=1
    if any(all(v==0 for v in row[:-1]) and row[-1]!=0 for row in matrix): return None
    return [matrix[r][-1] for r in pivots]

def conic(columns,target,allowed=None):
    if all(v==0 for v in target): return [Q(0)]*len(columns)
    indices=list(range(len(columns))) if allowed is None else allowed
    for size in range(1,min(len(target),len(indices))+1):
        for ids in combinations(indices,size):
            z=solve([columns[i] for i in ids],target)
            if z is not None and all(v>=0 for v in z):
                dense=[Q(0)]*len(columns)
                for i,v in zip(ids,z): dense[i]=v
                return dense
    raise RuntimeError('no conic certificate found')

def objective_dual(rows,rhs,c,x):
    active=[i for i,(a,b) in enumerate(zip(rows,rhs)) if geometry.dot(a,x)==b]
    return conic(rows,c,active)

def produce(c):
    problem=problem_of(c); tabs,ends=geometry.local_tables(**c); faces=[]
    for i,table in enumerate(tabs):
        row=[]
        for mask in range(1<<len(c['hs'])):
            a,b,h,off=own_constraints(problem,i,mask)
            if mask not in table:
                z=conic([r+[v] for r,v in zip(a,b)],[Q(0)]*len(h)+[Q(-1)])
                row.append(dict(kind='empty',dual=z))
            else:
                lo,hi=table[mask]; x,y=ends[i][mask]
                row.append(dict(kind='bounded',lo=lo,hi=hi,xlo=x,xhi=y,
                                dlo=objective_dual(a,b,[-v for v in h],x),
                                dhi=objective_dual(a,b,h,y)))
        faces.append(row)
    ranges=geometry.anchored(tabs,len(c['hs']))['ranges']
    assert ranges==old.dp(tabs,len(c['hs']))[-1].get((1<<len(c['hs']))-1,[])
    certificate=encode(dict(problem_sha256=verifier.digest(problem),faces=faces,ranges=ranges))
    return problem,certificate


def box3(empty=False):
    axes=[[Q(int(j==i)) for j in range(3)] for i in range(3)]
    rows=[]
    for a in axes: rows.extend([a,[-v for v in a]])
    target=[Q(1),Q(2),Q(3)]; level=Q(2) if empty else Q(0)
    problem=encode(dict(generators=[dict(A=rows,b=[Q(1)]*6,c=target,d=Q(1))],
                        receipts=[dict(lo=level,hi=level,forms=[dict(c=axes[0],d=Q(0))])]))
    faces=[]
    for mask in range(2):
        a,b,c,d=own_constraints(problem,0,mask)
        if empty:
            faces.append(dict(kind='empty',dual=conic([r+[v] for r,v in zip(a,b)],[Q(0)]*3+[Q(-1)])))
        else:
            x=[Q(0),Q(-1),Q(-1)]; y=[Q(0) if mask else Q(1),Q(1),Q(1)]
            faces.append(dict(kind='bounded',lo=geometry.dot(c,x)+d,hi=geometry.dot(c,y)+d,
                              xlo=x,xhi=y,dlo=objective_dual(a,b,[-v for v in c],x),
                              dhi=objective_dual(a,b,c,y)))
    cert=encode(dict(problem_sha256=verifier.digest(problem),faces=[faces],ranges=[] if empty else [(Q(-4),Q(6))]))
    return problem,cert

def corruptions(problem,certificate):
    items=[]
    c=copy.deepcopy(certificate); c['faces'][0].pop(); items.append(('missing_face',problem,c))
    c=copy.deepcopy(certificate)
    if c['ranges']: c['ranges'][0][1]=str(Q(c['ranges'][0][1])+Q(1,5))
    else: c['ranges']=[['0','0']]
    items.append(('invented_range',problem,c))
    p=copy.deepcopy(problem); p['generators'][0]['d']=str(Q(p['generators'][0]['d'])+1)
    items.append(('wrong_problem',p,certificate))
    bounded=next(((i,j) for i,row in enumerate(certificate['faces']) for j,e in enumerate(row) if e['kind']=='bounded'),None)
    if bounded:
        i,j=bounded
        c=copy.deepcopy(certificate); c['faces'][i][j]['hi']=str(Q(c['faces'][i][j]['hi'])+Q(1,7))
        items.append(('wrong_endpoint',problem,c))
        c=copy.deepcopy(certificate); c['faces'][i][j]['dhi'][0]='-1'
        items.append(('negative_dual',problem,c))
        coord=next((h for h,v in enumerate(problem['generators'][i]['c']) if Q(v)),None)
        if coord is not None:
            c=copy.deepcopy(certificate); v=c['faces'][i][j]['xhi'][coord]
            c['faces'][i][j]['xhi'][coord]=str(Q(v)+1)
            items.append(('wrong_primal',problem,c))
    empty=next(((i,j) for i,row in enumerate(certificate['faces']) for j,e in enumerate(row) if e['kind']=='empty'),None)
    if empty:
        i,j=empty; c=copy.deepcopy(certificate)
        c['faces'][i][j]['dual']=['0']*len(c['faces'][i][j]['dual'])
        items.append(('false_empty',problem,c))
    if len(certificate['ranges'])>1:
        c=copy.deepcopy(certificate); c['ranges'].pop()
        items.append(('deleted_component',problem,c))
    return items

def run():
    raw=(HERE/'anchor_range_inputs.json').read_bytes(); cases=json.loads(raw)
    jobs=[('polygon_'+str(i),decode_case(c)) for i,c in enumerate(cases[:40])]
    for eps in (Q(0),Q(1,10)):
        jobs.append(('gap_'+str(eps),dict(polys=[[(Q(0),Q(1)),(Q(2),Q(0))],[(Q(0),Q(2)),(Q(1),Q(0))]],
                    hs=[(Q(1),Q(0)),(Q(0),Q(1))],los=[-eps]*2,his=[eps]*2,objs=[((Q(1),Q(1)),Q(0))]*2)))
    records=[]; checks=[]; rejected={}; production_ns=0; verification_ns=0
    for name,c in jobs:
        t=time.perf_counter_ns(); p,cert=produce(c); production_ns+=time.perf_counter_ns()-t
        t=time.perf_counter_ns(); check=verifier.verify(p,cert); verification_ns+=time.perf_counter_ns()-t
        records.append(dict(origin=name,problem=p,certificate=cert)); checks.append(check)
    for empty in (False,True):
        t=time.perf_counter_ns(); p,cert=box3(empty); production_ns+=time.perf_counter_ns()-t
        t=time.perf_counter_ns(); check=verifier.verify(p,cert); verification_ns+=time.perf_counter_ns()-t
        records.append(dict(origin='box3_empty' if empty else 'box3',problem=p,certificate=cert)); checks.append(check)
    for record in records:
        for kind,p,c in corruptions(record['problem'],record['certificate']):
            try: verifier.verify(p,c)
            except (ValueError,KeyError,TypeError,ZeroDivisionError): rejected[kind]=rejected.get(kind,0)+1
            else: raise AssertionError(('corruption accepted',record['origin'],kind))
    bundle=(json.dumps(records,indent=2)+'\n').encode()
    (HERE/'range_cert_bundles.json').write_bytes(bundle)
    return dict(bundles=len(records),bounded_faces=sum(c['bounded_faces'] for c in checks),
                infeasible_faces=sum(c['infeasible_faces'] for c in checks),
                dual_entries=sum(c['dual_entries'] for c in checks),
                inconsistent_sources=sum(c['status']=='INCONSISTENT_SOURCE' for c in checks),
                rejected_mutations=rejected,mutation_total=sum(rejected.values()),
                source_input_sha256=hashlib.sha256(raw).hexdigest(),
                bundle_sha256=hashlib.sha256(bundle).hexdigest(),bundle_bytes=len(bundle),
                production_ns=production_ns,verification_ns=verification_ns,checks=checks)

if __name__=='__main__':
    plan=json.loads((HERE/'range_cert_plan.json').read_text())
    for name,sha in plan['sources'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==sha,name
    assert hashlib.sha256((HERE/'anchor_range_inputs.json').read_bytes()).hexdigest()==plan['input_sha256']
    assert not (HERE/'range_cert_result.json').exists()
    start=time.perf_counter_ns()
    try:
        result=dict(status='PASS',python=sys.version,results=run(),runtime_ns=time.perf_counter_ns()-start)
        (HERE/'range_cert_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
        print(json.dumps({k:v for k,v in result.items() if k!='results'}))
        print(json.dumps({k:v for k,v in result['results'].items() if k!='checks'}))
    except Exception:
        failure=dict(status='FAIL',traceback=traceback.format_exc(),runtime_ns=time.perf_counter_ns()-start)
        (HERE/'range_cert_failure.json').write_bytes((json.dumps(failure,indent=2)+'\n').encode())
        raise
