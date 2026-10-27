"""Exposed development cases for compact forest upper certificates."""
from fractions import Fraction as Q
from pathlib import Path
from math import inf
import copy,hashlib,json,time,traceback,sys
import forest_solver as tree
import forest_probe as panel
import exact_flat_probe as lin
import range_cert_probe as conic
import forest_cert_verify as check

HERE=Path(__file__).resolve().parent

def produce(case):
    case=check.decode(lin.encode({k:case[k] for k in ('bases','gs','los','his','fs')}))
    kept,extra=tree.spanning(case)
    if extra: raise ValueError('forest only')
    model=tree.Forest(case,kept); problem=lin.encode({k:case[k] for k in ('bases','gs','los','his','fs')})
    _,parent,children,order=check.orientation(check.decode(problem)); messages={}; n=len(case['bases'])
    for i in order:
        par=None if parent[i] is None else parent[i]-n
        cap=min((model.caps(h,j)[0]['value'] for j,hs in children[i] for h in hs),default=inf)
        ts={j:max((model.caps(h,j)[1]['value'] for h in hs),default=-inf) for j,hs in children[i]}
        group={}
        for variant,entry in zip(('A','B'),model.caps(i,par)):
            if entry is None: continue
            r=entry['value']; rs=list(model.q[i])
            if variant=='B': rs.append(tree.upper_row(case,par,i))
            if r==-inf and cap==-inf: proof=dict(kind='child_empty')
            elif r!=-inf and cap==r: proof=dict(kind='child_cap')
            else:
                rs.extend(tree.upper_row(case,j,i) for j,t in ts.items() if t<=r)
                d=len(case['fs'][i])-1; vs=lin.vertices(rs,(),d)
                if not vs:
                    proof=dict(kind='empty',dual=conic.conic(rs,[Q(0)]*d+[Q(-1)]))
                else:
                    if r==-inf: raise ValueError('false infeasibility')
                    f=case['fs'][i]; x=max(vs,key=lambda x:lin.evaluate(f,x))
                    lam=conic.objective_dual([row[:-1] for row in rs],[row[-1] for row in rs],f[:-1],x)
                    proof=dict(kind='dual',dual=lam)
            group[variant]=dict(value=None if r==-inf else r,x=entry['x'],proof=proof)
        messages[str(i)]=group
    upper=model.upper()
    cert=lin.encode(dict(problem_sha256=check.digest(problem),messages=messages,upper=None if upper is None else upper[0]))
    return problem,cert

def cases():
    out=[c for c in panel.inputs() if not tree.spanning(c)[1]]
    # A child can attain the threshold only while meeting its parent predicate;
    # imposing the parent's own predicate above that threshold makes P empty.
    out.append(dict(bases=[[[1,1],[-1,0]],[[1,1],[-1,0]]],
                    gs=[{0:[0,1],1:[1,0]}],los=[Q(0)],his=[Q(1,2)],fs=[[0,2],[1,0]]))
    # Leaf infeasibility, and its propagation to a separate parent message.
    out.append(dict(bases=[[[1,1],[-1,0]],[[1,1],[-1,0]]],
                    gs=[{0:[1,0],1:[1,0]}],los=[Q(2)],his=[Q(3)],fs=[[1,0],[1,0]]))
    return out

def mutations(problem,cert):
    c=copy.deepcopy(cert); c['messages'].pop(next(iter(c['messages']))); yield 'missing',problem,c
    p=copy.deepcopy(problem); p['fs'][0][-1]=str(Q(p['fs'][0][-1])+1); yield 'binding',p,cert
    c=copy.deepcopy(cert); c['upper']='0' if c['upper'] is None else str(Q(c['upper'])+1); yield 'answer',problem,c
    es=[(i,t,e) for i,g in cert['messages'].items() for t,e in g.items()]
    finite=next(((i,t,e) for i,t,e in es if e['value'] is not None),None)
    if finite:
        i,t,e=finite; c=copy.deepcopy(cert); c['messages'][i][t]['value']=str(Q(e['value'])-1); yield 'bound',problem,c
        c=copy.deepcopy(cert); c['messages'][i][t]['x'][0]='1000000'; yield 'primal',problem,c
    dual=next(((i,t,e) for i,t,e in es if e['proof'].get('dual')),None)
    if dual:
        i,t,e=dual; c=copy.deepcopy(cert); c['messages'][i][t]['proof']['dual'][0]='-1'; yield 'dual',problem,c

def run():
    bundles=[]; kinds={}; corrupt={}; messages=0
    for case in cases():
        p,c=produce(case); answer,ks=check.verify(p,c); bundles.append(dict(problem=p,certificate=c))
        for k,v in ks.items(): kinds[k]=kinds.get(k,0)+v
        messages+=sum(len(g) for g in c['messages'].values())
        for kind,pbad,cbad in mutations(p,c):
            try: check.verify(pbad,cbad)
            except (ValueError,KeyError,TypeError): corrupt[kind]=corrupt.get(kind,0)+1
            else: raise ValueError('accepted corruption '+kind)
    blob=(json.dumps(bundles,indent=2)+'\n').encode(); (HERE/'forest_cert_bundle.json').write_bytes(blob)
    return dict(cases=len(bundles),messages=messages,proof_kinds=kinds,rejected=corrupt,
                bundle_sha256=hashlib.sha256(blob).hexdigest(),bundle_bytes=len(blob))

if __name__=='__main__':
    plan=json.loads((HERE/'forest_cert_plan.json').read_text())
    for name,digest in plan['dependencies'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
    assert not (HERE/'forest_cert_result.json').exists()
    started=time.monotonic_ns()
    try: result=dict(status='PASS',results=run())
    except Exception: result=dict(status='FAIL',traceback=traceback.format_exc())
    result['elapsed_ns']=time.monotonic_ns()-started
    (HERE/'forest_cert_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result))
    if result['status']=='FAIL': sys.exit(1)
