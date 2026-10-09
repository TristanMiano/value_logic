"""Independent exact public-record reconstruction; no policy/service or truth calls.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC, R-P3-B-A.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,math,zipfile
P=Path(__file__).resolve().parent
ROOT=P.parents[4]
source=P/'public_stage_001/result.json'
result=json.loads(source.read_text())
assert result['status']=='PASS' and len(result['rows'])==23
rows=[]
reads=[]
for arm in result['rows']:
    binding=arm['input_bindings']
    arc=ROOT/binding['archive']['path']
    assert hashlib.sha256(arc.read_bytes()).hexdigest()==binding['archive']['sha256']
    inputs={}
    with zipfile.ZipFile(arc) as z:
        for member in binding['members']:
            name=member['member']
            if not name.endswith(('transcript.jsonl','purchase_invoices.jsonl','allocation_records.jsonl')):continue
            assert 'private' not in name and 'evaluator' not in name
            data=z.read(name)
            assert hashlib.sha256(data).hexdigest()==member['sha256']
            inputs[Path(name).name]=[json.loads(line) for line in data.splitlines()]
            reads.append({'archive':str(arc.relative_to(ROOT)),'member':name,'sha256':member['sha256']})
    t,b=arm['T'],arm['B'];m=t//b
    receipt={r['query_id']:r for r in inputs['purchase_invoices.jsonl']}
    expected_selected=[]
    total_ht=total_selected=total_g_ht=F(0)
    for row in inputs['transcript.jsonl']:
        a=row['issued_dyadic_probability'];q=F(a['numerator'],a['denominator'])
        assert 0<=q<=1
        if not row['purchased']:
            assert 'purchased_label' not in row
            continue
        r=receipt[row['query']['query_id']]
        assert r['answer']==row['purchased_label'] and r['checked'] and r['status']=='success'
        y=F(r['answer']);d=q*(1-y)+(1-q)*y
        if arm['kind']=='uniform':inverse=F(b)
        else:
            al=inputs['allocation_records.jsonl'][row['block']]
            assert al['selected']==row['index']%b
            count=b+1 if al['selected']==al['favorite'] else 1
            inverse=F(2*b,count)
        total_ht+=inverse*d;total_selected+=d
        total_g_ht+=inverse*(d-q*(1-q))
        expected_selected.append(row['block'])
    assert sorted(expected_selected)==list(range(m))
    u=total_ht-total_selected;a=total_g_ht
    assert u==F(arm['U_selected_total']) and a==F(arm['A_selected_total'])
    rs=arm['S']*(math.isqrt(2*m)+(math.isqrt(2*m)**2<2*m))
    ra=math.isqrt(2*(t-m))+(math.isqrt(2*(t-m))**2<2*(t-m))
    assert rs==arm['sampling_radius'] and ra==arm['action_radius']
    assert F(arm['conditional_action_mean_upper_clipped'])==min(t-m,u+rs)
    assert F(arm['realized_terminal_upper_clipped'])==min(t-m,u+rs+ra)
    assert F(arm['immutable_brier_upper_clipped'])==min(t,a+rs)
    rows.append({'name':arm['name'],'status':'PASS','purchased_labels':m,'U':str(u),'A':str(a),'sampling_radius':rs,'action_radius':ra})
out={'status':'PASS','scope':'Independent formulas reconstructed directly from the23 saved public transcripts, selected receipts and ticket allocations. No private evaluator input, policy execution, service call or truth calculation. Not a coverage experiment.','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checked_result_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'rows':rows,'member_reads':reads,'total_purchased_labels':sum(r['purchased_labels'] for r in rows),'formula_difference':'Reconstruct U as Horvitz-Thompson full conditional loss minus purchased conditional loss, and Brier via d-q(1-q); no import of the first-stage calculator.'}
p=P/'principal_basic_audit.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','arms':len(rows),'labels':out['total_purchased_labels'],'private_reads':0}))
