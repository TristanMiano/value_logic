"""Read-only research-evidence audit and administrative manifests."""
from pathlib import Path
import json,hashlib,re
HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
frozen=[];problems=[]
for p in sorted(HERE.glob('*/design.json')):
    d=read(p)
    for name,digest in d.get('hashes',{}).items():
        stored=p.parent/name
        if stored.is_file() and sha(stored)==digest:frozen.append({'design':p.relative_to(HERE).as_posix(),'path':stored.relative_to(HERE).as_posix(),'sha256':digest})
        else:problems.append({'design':p.relative_to(HERE).as_posix(),'name':name,'expected':digest,'actual':sha(stored) if stored.is_file() else None})
save(HERE/'freeze_audit.json',{'status':'pass' if not problems else 'needs_review','checked_bindings':len(frozen),'bindings':frozen,'problems':problems,'scope':'Design-hash copied modules/declarations; named exceptions require separate preserved bindings.'})
services=[]
for name in ['rc03','rc04','ds01','cp02','lp02','rr01','br01','wt02','sf01','rv01','rl01']:
    p=HERE/name/'checked.json';d=read(p);counts=d.get('counts',d)
    summaries=[read(x) for x in (HERE/name).glob('*/*/summary.json')]
    services.append({'id':name,'check':p.relative_to(HERE).as_posix(),'check_sha256':sha(p),'status':d['status'],'checked_outputs':counts.get('outputs'),'receipts':counts.get('receipts',counts.get('purchases')),'summary_files':len(summaries),'all_summaries_complete':all(s.get('status')=='complete' for s in summaries),'scope':'Separate development experiment; arms have their own information/cost menus and cannot be pooled into one advantage claim.'})
save(HERE/'run_inventory.json',{'contributor':'Codex (GPT-6)','stage':'DEVELOPMENT','services':services,'checked_paid_outputs':sum(s['checked_outputs'] for s in services),'checked_receipts':sum(s['receipts'] or 0 for s in services),'all_checks_pass':all(s['status'].startswith('pass') for s in services),'other_evidence':'See designs and source-specific results for algebraic, source compilation, patch and probability screens. Counts measure test breadth, not independent replication or success probability.'})
failed=[]
for p in sorted(HERE.rglob('failed.json')):
    d=read(p);failed.append({'path':p.relative_to(HERE).as_posix(),'sha256':sha(p),'error':d.get('error'),'invoice':d.get('invoice'),'physical_acquisitions':d.get('physical_acquisitions'),'scope':'Actual failed compilation prefix; preserved, not selected out of the resource record.'})
log_errors=[]
for p in sorted(HERE.rglob('*.log')):
    s=p.read_text(encoding='utf-8',errors='replace')
    if re.search(r'Traceback|AssertionError|SyntaxError|KeyError|Error:|Fatal Python',s):log_errors.append({'path':p.relative_to(HERE).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,'tail':s[-1600:]})
save(HERE/'failures.json',{'contributor':'Codex (GPT-6)','compilation_failures':failed,'known_failed_compilation_named_units':sum(x['invoice']['named_units'] for x in failed),'error_logs':log_errors,'additional_dispositions':[
 {'attempt':'startup.json','disposition':'Clock control.tmp startup race preserved; no pre-start research credit.'},
 {'attempt':'rc03/check01_error.log','disposition':'Deterministic checker syntax error; corrected checker version and successful second logs retained. No new physical acquisition in checking.'},
 {'attempt':'ds01/check01 through check05 and bindings01 through03','disposition':'Three seal-check failures, jitless process failure and filename/body mismatch retained. Instrumented checker and body binding checks pass. ds01/bindings_manifest.json explicitly records the anomalous name and correct duplicate. Cause unproven; native/failed diagnostic costs unknown.'},
 {'attempt':'cp02/check01.log','disposition':'Checker model-index order defect; corrected second reconstruction retained. Service outputs unchanged.'},
 {'attempt':'wt01 extraction','disposition':'extract_wt01.py assumed an absent archive member name after writing numeric09; v2 preserves original archive member names and hashes. Original failed script/prefix retained; archive/network prices unknown.'},
 {'attempt':'br01/check01.log','disposition':'Empty log and no confirmed completion: status unknown. Wrapped unchanged second check passes; do not invent its original exit status or CPU cause.'}],
 'failure_cost_policy':'All purchase receipts and failed compiler invoices preserved. Diagnostic failures create no new query receipts; their unmeasured host work remains unknown. No failed work is converted into a zero bill.'})
# Preserve the exact earlier source version bound by the three-score screen.
ts=HERE/'ts01';ts.mkdir(exist_ok=True);checked=read(HERE/'three_score_checked.json');snapshot=[]
block='''
For a fixed candidate order, each prefix can take the minimum only over types
actually present in that prefix. This can avoid an unused poorly sampled type
forcing its bound to zero. Each survival term then has its own valid common
lower law; summing the corresponding upper bounds remains conservative by
linearity. Choosing an order from past data is allowed, but changing the order
in response to current outcomes requires a new conditional analysis. Price the
search over orders explicitly.
'''
for name,digest in checked['source_hashes'].items():
    data=(HERE/name).read_bytes()
    if hashlib.sha256(data).hexdigest()!=digest:
        assert name=='correlated_learning.md';text=data.decode();assert block in text;data=text.replace(block,'',1).encode()
    assert hashlib.sha256(data).hexdigest()==digest
    target=ts/name
    if target.exists():assert target.read_bytes()==data
    else:target.write_bytes(data)
    snapshot.append({'path':name,'stored':target.relative_to(HERE).as_posix(),'sha256':digest})
save(ts/'binding.json',{'contributor':'Codex (GPT-6)','basis':'three_score_checked.json source_hashes bind the screened source. The correlated-learning snapshot removes only the later recorded elaboration; its exact prior hash is verified.','checked_sha256':sha(HERE/'three_score_checked.json'),'files':snapshot})
print(json.dumps({'freeze_bindings':len(frozen),'freeze_problems':problems,'paid_outputs':sum(s['checked_outputs'] for s in services),'failed_compilers':len(failed),'error_logs':len(log_errors),'source_snapshots':len(snapshot)},indent=2))
