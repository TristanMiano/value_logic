#!/usr/bin/env python3
"""Verify bindings of the S2 evidence bundle without rerunning historical tests.
A checksum is a content binding, not an external signature or correctness proof.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
S='v3/work_logs/P3_04_2026-10-08_S2'
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(root:Path):
    records=[]
    for run in ('attempt_1','composition_1'):
        d=root/S/'development'/run;m=json.loads((d/'manifest.json').read_bytes());r=json.loads((d/'summary.json').read_bytes())
        if not m['kind'].startswith('DEVELOPMENT') or m['historical_S1_evidence_recovered'] or r['status']!='PASS' or r['label']!='DEVELOPMENT' or r['error'] is not None:raise ValueError('Invalid evidence disposition.')
        for name,digest in m['source_sha256'].items():
            if Path(name).name!=name:raise ValueError('Unsafe source name.')
            if sha((d/name).read_bytes())!=digest or sha((root/'v3/checks'/name).read_bytes())!=digest:raise ValueError('Code/evidence binding mismatch: '+name)
        if run=='attempt_1' and sum(x['assertions'] for x in r['suites'])!=r['assertions']:raise ValueError('Suite count mismatch.')
        records.append({'run':run,'assertions':r['assertions'],'bound_sources':len(m['source_sha256'])})
    for edit in json.loads((root/S/'reviews/manuscript_edits.json').read_bytes()):
        old=(root/edit['pre_edit_snapshot']).read_bytes();new=(root/edit['path']).read_bytes()
        if sha(old)!=edit['before_sha256'] or sha(new)!=edit['after_sha256']:raise ValueError('Manuscript hash mismatch.')
        oldbody=old.decode().split('## 1.',1)[1];newbody=new.decode().split('## 1.',1)[1]
        if edit['path'].endswith('04_counterfactual_semantics.md'):
            oldbody=oldbody.split('## 11.',1)[0];newbody=newbody.split('## 11.',1)[0]
        if oldbody!=newbody:raise ValueError('Unexpected mathematical-body change.')
    spec=importlib.util.spec_from_file_location('p304_s2_replay',root/S/'replay_accounting.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    a,append=mod.replay(root/S)
    if a!=json.loads((root/S/'actuals.json').read_bytes()) or append!=(root/S/'ledger_append.csv').read_bytes():raise ValueError('Clock replay mismatch.')
    if a['cadence_violations'] or not a['research_floor_satisfied']:raise ValueError('Clock prerequisites failed.')
    return {'status':'PASS','runs':records,'mathematical_bodies_unchanged':True,'research_minutes_S2':a['research_minutes'],'S1_historical_runs_recovered':False,'scope':'Content bindings and exact recorded accounting; not new scientific execution or proof verification.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);a=p.parse_args();print(json.dumps(verify(a.root),indent=2))
