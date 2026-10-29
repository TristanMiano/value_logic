"""Frozen developmental audit of the unchanged s19 exact range verifier."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import platform
import sys
import time
import traceback
from lp_witness import dot, extrema, minimize
from audit_inputs import encoded

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SPEC=importlib.util.spec_from_file_location('s19_range_verifier',HERE.parent/'s19/range_cert_verify.py')
V=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(V)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_inequalities(problem,i,mask):
    g=problem['generators'][i]
    rows=[list(map(F,row)) for row in g['A']];rhs=list(map(F,g['b']))
    for j,obs in enumerate(problem['receipts']):
        form=obs['forms'][i];h=list(map(F,form['c']));off=F(form['d'])
        rows += [[-v for v in h]];rhs += [off-F(obs['lo'])]
        if mask & (1<<j):
            rows += [h];rhs += [F(obs['hi'])-off]
    return rows,rhs,list(map(F,g['c'])),F(g['d'])


def merged(intervals):
    result=[]
    for lo,hi in sorted(intervals):
        if result and lo<=result[-1][1]:
            result[-1]=(result[-1][0],max(hi,result[-1][1]))
        else:
            result.append((lo,hi))
    return result


def assignments(faces,k):
    n=len(faces)
    for owners in product(range(n),repeat=k):
        masks=[0]*n
        for j,i in enumerate(owners):
            masks[i] |= 1<<j
        entries=[faces[i][mask] for i,mask in enumerate(masks)]
        if all(e['kind']=='bounded' for e in entries):
            yield masks,entries


def exhaustive_range(faces,k):
    # Each product branch has a continuous minimum with these two extrema.
    return merged([(min(F(e['lo']) for e in es),min(F(e['hi']) for e in es))
                   for _,es in assignments(faces,k)])


def source_value(problem,source):
    assert len(source)==len(problem['generators'])
    for g,x in zip(problem['generators'],source):
        assert len(x)==len(g['c'])
        assert all(dot(list(map(F,row)),x)<=F(b) for row,b in zip(g['A'],g['b']))
    for obs in problem['receipts']:
        value=min(dot(list(map(F,f['c'])),x)+F(f['d']) for f,x in zip(obs['forms'],source))
        assert F(obs['lo'])<=value<=F(obs['hi'])
    return min(dot(list(map(F,g['c'])),x)+F(g['d']) for g,x in zip(problem['generators'],source))


def source_at(problem,faces,q):
    for masks,es in assignments(faces,len(problem['receipts'])):
        if min(F(e['lo']) for e in es)<=q<=min(F(e['hi']) for e in es):
            anchor=min(range(len(es)),key=lambda i:F(es[i]['lo']))
            points=[list(map(F,e['xhi'])) for e in es]
            e=es[anchor];lo=F(e['lo']);hi=F(e['hi'])
            if lo==hi:
                points[anchor]=list(map(F,e['xlo']))
            else:
                ratio=(q-lo)/(hi-lo)
                points[anchor]=[F(a)+ratio*(F(b)-F(a)) for a,b in zip(e['xlo'],e['xhi'])]
            assert source_value(problem,points)==q
            return dict(q=q,source=points,assignment=masks,anchor=anchor)
    raise AssertionError('no source in independent assignment reconstruction')


def produce(problem):
    faces=[]
    for i in range(len(problem['generators'])):
        row=[]
        for mask in range(1<<len(problem['receipts'])):
            a,b,c,d=local_inequalities(problem,i,mask)
            row.append(extrema(a,b,c,d))
        faces.append(row)
    ranges=exhaustive_range(faces,len(problem['receipts']))
    return encoded(dict(problem_sha256=V.digest(problem),faces=faces,ranges=ranges))


def mutations(problem,cert):
    output=[]
    c=copy.deepcopy(cert);c['faces'][0].pop();output.append(('missing_face',problem,c))
    c=copy.deepcopy(cert);c['problem_sha256']='0'*64;output.append(('wrong_binding',problem,c))
    c=copy.deepcopy(cert)
    if c['ranges']:
        c['ranges'][0][0]=str(F(c['ranges'][0][0])-1)
    else:
        c['ranges']=[['0','0']]
    output.append(('invented_range',problem,c))
    bounded=next(((i,t) for i,row in enumerate(cert['faces']) for t,e in enumerate(row)
                  if e['kind']=='bounded'),None)
    if bounded is not None:
        i,t=bounded;e=cert['faces'][i][t]
        c=copy.deepcopy(cert);c['faces'][i][t]['hi']=str(F(e['hi'])+1)
        output.append(('wrong_endpoint',problem,c))
        c=copy.deepcopy(cert);c['faces'][i][t]['xlo'].append('0')
        output.append(('wrong_dimension',problem,c))
        c=copy.deepcopy(cert);c['faces'][i][t]['dhi'][0]='-1'
        output.append(('negative_dual',problem,c))
        p=copy.deepcopy(problem);p['generators'][i]['d']=str(F(p['generators'][i]['d'])+1)
        c=copy.deepcopy(cert);c['problem_sha256']=V.digest(p)
        output.append(('changed_offset_rebound',p,c))
        p=copy.deepcopy(problem)
        p['generators'][i]['b'][0]=str(dot(list(map(F,p['generators'][i]['A'][0])),list(map(F,e['xlo'])))-1)
        c=copy.deepcopy(cert);c['problem_sha256']=V.digest(p)
        output.append(('changed_row_rebound',p,c))
        if problem['receipts']:
            p=copy.deepcopy(problem);obs=p['receipts'][0];form=obs['forms'][i]
            bad=dot(list(map(F,form['c'])),list(map(F,e['xlo'])))+F(form['d'])+1
            obs['lo']=str(bad);obs['hi']=str(bad+1)
            c=copy.deepcopy(cert);c['problem_sha256']=V.digest(p)
            output.append(('changed_receipt_rebound',p,c))
    empty=next(((i,t) for i,row in enumerate(cert['faces']) for t,e in enumerate(row)
                if e['kind']=='empty'),None)
    if empty is not None:
        i,t=empty;c=copy.deepcopy(cert)
        c['faces'][i][t]['dual']=['0']*len(c['faces'][i][t]['dual'])
        output.append(('false_empty',problem,c))
    if len(cert['ranges'])>1:
        c=copy.deepcopy(cert);c['ranges'].pop();output.append(('lost_component',problem,c))
    return output


def joint_rows(problem,owners,anchor,band):
    dims=[len(g['c']) for g in problem['generators']];starts=[];total=0
    for d in dims:
        starts.append(total);total+=d
    rows=[];rhs=[]
    def add(i,c,b):
        row=[F(0)]*total;row[starts[i]:starts[i]+dims[i]]=list(map(F,c))
        rows.append(row);rhs.append(F(b))
    for i,g in enumerate(problem['generators']):
        for c,b in zip(g['A'],g['b']):add(i,c,b)
    for j,obs in enumerate(problem['receipts']):
        for i,form in enumerate(obs['forms']):
            add(i,[-F(v) for v in form['c']],F(form['d'])-F(obs['lo']))
        i=owners[j];form=obs['forms'][i]
        add(i,form['c'],F(obs['hi'])-F(form['d']))
    for i,g in enumerate(problem['generators']):
        add(i,[-F(v) for v in g['c']],F(g['d'])-band[0])
    g=problem['generators'][anchor];add(anchor,g['c'],band[1]-F(g['d']))
    return rows,rhs,dims,starts,total


def direct_band(problem,band):
    n=len(problem['generators']);k=len(problem['receipts']);proofs=[]
    for owners in product(range(n),repeat=k):
        for anchor in range(n):
            a,b,dims,starts,total=joint_rows(problem,owners,anchor,band)
            proof=minimize(a,b,[F(0)]*total)
            proofs.append(dict(owners=owners,anchor=anchor,proof=proof))
            if proof['kind']=='optimum':
                source=[proof['point'][s:s+d] for s,d in zip(starts,dims)]
                val=source_value(problem,source);assert band[0]<=val<=band[1]
                return dict(band=band,feasible=True,lp_calls=len(proofs),proofs=proofs)
    return dict(band=band,feasible=False,lp_calls=len(proofs),proofs=proofs)


def run():
    frozen=json.loads((HERE/'audit_freeze.json').read_text(encoding='utf-8'))
    for name,value in frozen['sha256'].items():
        assert sha(ROOT/name)==value, 'freeze mismatch: '+name
    record_path=HERE/'audit_records.jsonl';result_path=HERE/'audit_results.json'
    if record_path.exists() or result_path.exists():raise RuntimeError('refuse to overwrite executed evidence')
    cases=json.loads((HERE/'audit_inputs.json').read_text(encoding='utf-8'))
    summaries=[];rejects={};direct=[];start=time.perf_counter_ns()
    for item in cases:
        p=item['problem']
        if 'known_source' in item:source_value(p,[list(map(F,x)) for x in item['known_source']])
        before=time.perf_counter_ns();cert=produce(p);production_ns=time.perf_counter_ns()-before
        before=time.perf_counter_ns();check=V.verify(p,cert);verification_ns=time.perf_counter_ns()-before
        if 'expected' in item:assert check['ranges']==item['expected'],item['name']
        witnesses=[]
        for lo,hi in check['ranges']:
            for q in sorted(set((F(lo),F(hi),(F(lo)+F(hi))/2))):
                witnesses.append(source_at(p,cert['faces'],q))
        failures=[]
        for name,pp,cc in mutations(p,cert):
            try:V.verify(pp,cc)
            except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError) as error:
                rejects[name]=rejects.get(name,0)+1;failures.append(dict(kind=name,error=str(error)))
            else:raise AssertionError('accepted targeted corruption: '+name)
        record=dict(name=item['name'],problem=p,certificate=cert,check=check,
                    witnesses=witnesses,mutations=failures,production_ns=production_ns,
                    verification_ns=verification_ns)
        with record_path.open('a',encoding='utf-8') as f:f.write(json.dumps(encoded(record),sort_keys=True)+'\n')
        summary=dict(name=item['name'],dimensions=[len(g['c']) for g in p['generators']],
                     receipts=len(p['receipts']),ranges=check['ranges'],
                     bounded=check['bounded_faces'],empty=check['infeasible_faces'],
                     source_witnesses=len(witnesses),mutations=len(failures),
                     certificate_bytes=len(json.dumps(cert,separators=(',',':')).encode()),
                     production_ns=production_ns,verification_ns=verification_ns)
        summaries.append(summary);print(json.dumps({k:summary[k] for k in ('name','bounded','empty','source_witnesses')}),flush=True)
        if item['name']=='noisy_envelope':
            bands=[(F(-281,200),F(-281,200)),(F(-11,8),F(-11,8)),
                   (F(-5,4),F(-6,5)),(F(-221,200),F(-43,40)),
                   (F(-2),F(-3,2)),(F(-1),F(-9,10)),(F(-2),F(0))]
            for band in bands:
                answer=direct_band(p,band)
                expected=any(F(a)<=band[1] and band[0]<=F(b) for a,b in check['ranges'])
                assert answer['feasible']==expected
                direct.append(answer)
    import scipy
    result=dict(status='PASS',classification='same-model DEVELOPMENT, not independent confirmation',
                cases=summaries,case_count=len(summaries),mutations_rejected=rejects,
                direct_bands=direct,elapsed_ns=time.perf_counter_ns()-start,
                environment=dict(python=sys.version,platform=platform.platform(),scipy=scipy.__version__),
                freeze_sha256=sha(HERE/'audit_freeze.json'),records_sha256=sha(record_path))
    result_path.write_text(json.dumps(encoded(result),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='PASS',cases=len(summaries),mutations=sum(rejects.values()),
                         direct_bands=len(direct))),flush=True)


if __name__=='__main__':
    try:run()
    except Exception:
        failure=HERE/'audit_failure.txt'
        with failure.open('a',encoding='utf-8') as f:f.write(traceback.format_exc()+'\n')
        raise
