"""Independent public-archive reconstruction of centered and two-sided reports.
ChatGPT (GPT-6 Astra Pro), 2026-10-09. No calculator/controller/service imports.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,math,zipfile
P=Path(__file__).resolve().parent;ROOT=P.parents[4]
inputs=[P/'centered_public_stage_001/result.json',P/'two_sided_public_stage_001/result.json']
center,two=[json.loads(p.read_text()) for p in inputs]
assert center['status']==two['status']=='PASS'
second={r['name']:r for r in two['rows']};rows=[];reads=[]
def ceilroot(x):
    s=math.isqrt(x)
    return s if s*s==x else s+1
for arm in center['rows']:
    binding=arm['input_bindings'];arc=ROOT/binding['archive']['path'];raw={}
    assert hashlib.sha256(arc.read_bytes()).hexdigest()==binding['archive']['sha256']
    with zipfile.ZipFile(arc) as z:
        for item in binding['members']:
            name=item['member'];leaf=Path(name).name
            if leaf not in ('transcript.jsonl','purchase_invoices.jsonl','allocation_records.jsonl'):continue
            assert 'private' not in name and 'evaluator' not in name
            data=z.read(name);assert hashlib.sha256(data).hexdigest()==item['sha256']
            raw[leaf]=[json.loads(x) for x in data.splitlines()]
            reads.append({'archive':str(arc.relative_to(ROOT)),'member':name,'sha256':item['sha256']})
    tr=raw['transcript.jsonl'];receipts={r['query_id']:r for r in raw['purchase_invoices.jsonl']}
    t,b,m=arm['T'],arm['B'],arm['m'];n=t-m
    q=[F(r['issued_dyadic_probability']['numerator'],r['issued_dyadic_probability']['denominator']) for r in tr]
    variance=sum((x*(1-x) for x in q),F(0))
    ht_residual=selected_residual=selected_d=Q=F(0)
    for k in range(m):
        inv=[F(b)]*b
        if arm['kind']=='adaptive':
            favorite=raw['allocation_records.jsonl'][k]['favorite']
            inv=[F(2*b,b+1) if j==favorite else F(2*b) for j in range(b)]
        widths=[abs(1-2*q[k*b+j])*inv[j] for j in range(b)]
        Q+=max(widths)**2
        sel=[j for j in range(b) if tr[k*b+j]['purchased']]
        assert len(sel)==1;j=sel[0];r=tr[k*b+j];x=q[k*b+j]
        y=receipts[r['query']['query_id']]['answer'];assert y==r['purchased_label']
        loss=(1-y)*x+y*(1-x);res=loss-F(1,2)
        selected_d+=loss;selected_residual+=res;ht_residual+=inv[j]*res
    uc=F(n,2)+ht_residual-selected_residual;ac=F(t,2)-variance+ht_residual
    assert uc==F(arm['U_centered_total']) and ac==F(arm['A_centered_total'])
    assert Q==F(arm['Q_realized_predictable_width_sum'])
    assert ac-uc==selected_d-variance==F(arm['shared_deviation_public_correction'])
    R=arm['S']*ceilroot(2*m);rho=Q/R+F(R,2);ra=ceilroot(2*n)
    assert R==arm['baseline_integer_sampling_radius_R'] and rho==F(arm['sampling_radius'])
    assert F(arm['fixed_lambda'])==F(8,R) and rho<=R
    vmax=sum((max(q[i],1-q[i]) for i in range(t) if not tr[i]['purchased']),F(0))
    vmin=sum((min(q[i],1-q[i]) for i in range(t) if not tr[i]['purchased']),F(0))
    fmax=sum((max(x*x,(1-x)*(1-x)) for x in q),F(0))
    fmin=sum((min(x*x,(1-x)*(1-x)) for x in q),F(0))
    assert F(arm['conditional_action_mean_upper_clipped'])==max(F(0),min(vmax,uc+rho))
    assert F(arm['immutable_brier_upper_clipped'])==max(F(0),min(fmax,ac+rho))
    assert F(arm['realized_terminal_upper_clipped'])==max(F(0),min(F(n),uc+rho+ra))
    rtwo=Q/R+F(5*R,8);atwo=ceilroot((5*n+1)//2);r2=second[arm['name']]
    assert F(r2['two_sided_sampling_radius'])==rtwo and r2['two_sided_action_radius']==atwo
    targets={'conditional_action_mean':(uc,rtwo,vmin,vmax),'immutable_brier':(ac,rtwo,fmin,fmax),'realized_terminal_errors':(uc,rtwo+atwo,F(0),F(n))}
    empty=[]
    for name,(mu,rad,lo,hi) in targets.items():
        observed=r2['intervals'][name];a=max(lo,mu-rad);z=min(hi,mu+rad)
        assert F(observed['lower'])==a and F(observed['upper'])==z
        assert observed['empty']==(a>z)
        if a>z:empty.append(name)
    assert empty==r2['empty_intersections']
    tests={'brier_lower_above_T_over_4':F(r2['intervals']['immutable_brier']['lower'])>F(t,4),'conditional_upper_below_n_over_2':F(r2['intervals']['conditional_action_mean']['upper'])<F(n,2),'conditional_lower_above_n_over_2':F(r2['intervals']['conditional_action_mean']['lower'])>F(n,2)}
    assert r2['certificate_labels']=={k:None if empty else v for k,v in tests.items()}
    rows.append({'name':arm['name'],'status':'PASS','uc':str(uc),'ac':str(ac),'Q':str(Q),'rho':str(rho),'two_sided_radius':str(rtwo),'certificate_labels':r2['certificate_labels'],'empty':empty})
assert len(rows)==23
out={'status':'PASS','scope':'Independent direct reconstruction from all23 public trace/receipt/allocation archives; no private inputs, policy/service/label/RNG execution, or import of the diagnostic implementation. Mathematical coverage remains a fair-bit premise, not tested by these seeds.','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_results':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'rows':rows,'public_member_reads':reads,'private_member_reads':0,'counts':{k:sum(r['certificate_labels'][k] is True for r in rows) for k in rows[0]['certificate_labels']}}
p=P/'principal_centered_audit.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','arms':23,'counts':out['counts'],'private_reads':0}))
