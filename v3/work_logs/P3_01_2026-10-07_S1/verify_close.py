"""Read-only P3-01 closing verification; ChatGPT (GPT-6 Astra Pro), 2026-10-07.
Run from repository root; does not finalize or mutate accounting.
"""
import sys
import json, re, hashlib, subprocess, platform
from pathlib import Path
from urllib.parse import unquote, urlsplit
from datetime import datetime, timezone
root = Path.cwd()
report = {"observed_utc":datetime.now(timezone.utc).isoformat(), "python":platform.python_version(), "mode":"read_only_administrative_no_experiment_rerun"}
snapshots = {}
def read(p):
    p = Path(p)
    data = p.read_bytes()
    snapshots[str(p)] = hashlib.sha256(data).hexdigest()
    return data.decode("utf-8")
def run(*args):
    p=subprocess.run(args, text=True, capture_output=True)
    return {"command":list(args),"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
json_files=sorted(Path("v3").rglob("*.json"))
json_errors=[]
for p in json_files:
    try: json.loads(read(p))
    except Exception as e: json_errors.append({"file":str(p),"error":str(e)})
report["json_syntax"]={"files":len(json_files),"errors":json_errors}
md_files=sorted(Path("v3").rglob("*.md"))+[Path("TODO_v3.md")]
def unfence(text):
    out=[]; fence=None
    for line in text.splitlines():
        m=re.match(r"^\s*(`{3,}|~{3,})",line)
        if m:
            ch=m.group(1)[0]
            if fence is None: fence=ch
            elif fence==ch: fence=None
            out.append("")
        else: out.append(line if fence is None else "")
    return "\n".join(out)
def anchors(text):
    found=set(); counts={}; uncertain=[]
    for line in unfence(text).splitlines():
        m=re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$",line)
        if not m: continue
        title=m.group(1)
        if not title.isascii() or re.search(r"[<>\\$]",title):
            uncertain.append(title); continue
        title=re.sub(r"\[([^]]+)\]\([^)]*\)",r"\1",title)
        slug=re.sub(r"[^a-z0-9_\-\s]","",title.lower())
        slug=re.sub(r"\s","-",slug)
        n=counts.get(slug,0); counts[slug]=n+1
        found.add(slug if n==0 else f"{slug}-{n}")
    found.update(re.findall(r'<a\s+(?:name|id)=["\x27]([^"\x27]+)',text))
    return found,uncertain
link_records=[]; missing=[]; anchor_ok=[]; anchor_limits=[]
inline=re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]*>|[^\s)]+)(?:\s+[\"\x27][^\n]*[\"\x27])?\s*\)")
reference=re.compile(r"^ {0,3}\[[^]\n]+\]:\s*(<[^>]*>|\S+)",re.M)
for p in md_files:
    body=unfence(read(p))
    for m in list(inline.finditer(body))+list(reference.finditer(body)):
        target=m.group(1).strip("<>")
        u=urlsplit(target)
        if u.scheme or u.netloc: continue
        local=unquote(u.path)
        dest=(root/local.lstrip("/")) if local.startswith("/") else (root/p.parent/local)
        dest=dest.resolve()
        rec={"from":str(p),"target":target,"resolved":str(dest.relative_to(root)) if dest.is_relative_to(root) else str(dest)}
        link_records.append(rec)
        if not dest.exists():
            missing.append(rec); continue
        if u.fragment:
            if dest.suffix.lower()!=".md":
                anchor_limits.append(dict(rec,reason="non-Markdown target")); continue
            known,uncertain=anchors(read(dest))
            if unquote(u.fragment) in known: anchor_ok.append(rec)
            else: anchor_limits.append(dict(rec,reason="not confirmed by conservative ASCII ATX/explicit-anchor check",non_ascii_or_special_headings=len(uncertain)))
report["markdown"]={"files":len(md_files),"local_links":len(link_records),"missing_targets":missing,"confirmed_anchors":len(anchor_ok),"anchor_limits":anchor_limits,"parser_limits":"Inline/reference-definition links outside fenced code; conservative ASCII ATX and explicit HTML anchors; not a full renderer or external URL audit."}
index=json.loads(read("v3/foundations/01_contract.v1.json"))
duties_text=read("v3/foundations/01_desiderata.md")
duty_rows=re.findall(r"^\| ([A-Z]\d{2}) / ([^|]+)\|",duties_text,re.M)
duty_map={}
for duty,qs in duty_rows:
    qs=re.sub(r"Q([1-5])[–-]Q([1-5])",lambda m:",".join("Q"+str(i) for i in range(int(m[1]),int(m[2])+1)),qs)
    duty_map[duty]=set(re.findall(r"Q[1-5]",qs))
sources=set(re.findall(r"^\| (S\d+) \|",read("v3/literature/01_source_contracts.md"),re.M))
examples=set(re.findall(r"^## (EX\d+)\b",read("v3/foundations/01_separating_examples.md"),re.M))
examples.update(re.findall(r"^## (CB\d+)\b",read("v3/foundations/01_composition_boundaries.md"),re.M))
gc_text=read("v3/work_logs/P3_01_2026-10-07_S1/reviews/genuine_counterpossible_target.md")
if re.search(r"^## 2\. Finite request GC01$",gc_text,re.M): examples.add("GC01")
main=read("v3/foundations/01_problem_contract.md")
ordinary=set(re.findall(r"\bO-[A-Z]+\b",main))
refs=[]; association_differences=[]
for q in index["questions"]:
    qid=q["id"]
    for name in q["duties"]:
        if name not in duty_map: refs.append({"question":qid,"kind":"missing duty","id":name})
        elif qid not in duty_map[name]: association_differences.append({"question":qid,"duty":name,"difference":"index includes; duty row does not associate"})
    for name in q["development_examples"]:
        if name not in examples: refs.append({"question":qid,"kind":"missing example definition","id":name})
    for name in q["comparators"]:
        if name not in sources|ordinary: refs.append({"question":qid,"kind":"missing comparator definition","id":name})
    for name,qs in duty_map.items():
        if qid in qs and name not in q["duties"]: association_differences.append({"question":qid,"duty":name,"difference":"duty row associates; index omits"})
doc_missing=[{"key":k,"path":v} for k,v in index["canonical_documents"].items() if not Path(v).is_file()]
report["semantic_index"]={"question_ids":[q["id"] for q in index["questions"]],"question_ids_exact":sorted(q["id"] for q in index["questions"])==["Q1","Q2","Q3","Q4","Q5"],"duty_definitions":len(duty_map),"source_definitions":len(sources),"example_definitions":sorted(examples),"missing_references":refs,"missing_canonical_documents":doc_missing,"question_duty_association_differences":association_differences}
e=index["development_evidence"]; saved=json.loads(read(e["record"])); start=json.loads(read(e["record"]+".started.json"))
script_path=Path(saved["command"][1]); script_hash=hashlib.sha256(script_path.read_bytes()).hexdigest(); snapshots[str(script_path)]=script_hash
provenance={"status":saved["status"],"failure":saved["failure"],"groups":len(saved["groups"]),"all_groups_pass":all(g["status"]=="PASS" for g in saved["groups"]),"assertions":saved["assertions"],"summed_group_assertions":sum(g["assertions"] for g in saved["groups"]),"script_path":str(script_path),"current_script_sha256":script_hash,"saved_script_sha256":saved["script_sha256"],"index_script_sha256":e["script_sha256"],"start_marker_script_sha256":start["script_sha256"],"saved_result_sha256":hashlib.sha256(Path(e["record"]).read_bytes()).hexdigest(),"development_only":saved["data_class"]=="development" and saved["frozen_evaluation"] is False}
provenance["consistent_11_3449"]=len(saved["groups"])==e["groups"]==11 and saved["assertions"]==e["assertions"]==sum(g["assertions"] for g in saved["groups"])==3449
provenance["all_script_hashes_match"]=len({script_hash,saved["script_sha256"],e["script_sha256"],start["script_sha256"]})==1
report["saved_development_result"]=provenance
git=[run("git","diff","--name-only"),run("git","diff","--cached","--name-only"),run("git","ls-files","--others","--exclude-standard"),run("git","diff","--check")]
changed=set()
for r in git[:3]: changed.update(r["stdout"].splitlines())
unexpected=sorted(p for p in changed if p!="TODO_v3.md" and not p.startswith("v3/"))
report["git"]={"commands":git,"unexpected_paths_outside_phase_three":unexpected,"root_README_or_phase_two_changes":[p for p in changed if p=="README.md" or p=="TODO_v2.md" or p=="paper_v2.md" or p.startswith("v2/")],"phase_three_only":not unexpected}
changed_during=[]
for p,digest in snapshots.items():
    if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=digest: changed_during.append(p)
report["snapshot_changed_during_validation"]=changed_during
report["snapshot_hashes"]={p:d for p,d in snapshots.items() if not p.startswith("/")}
report["limits"]=["No experiment or legacy tests rerun.","No clock closure, ledger arithmetic or gate assessment performed.","Question/duty association differences require human disposition; existence checks alone do not validate scientific claims.","Later edits and closing artifacts require root final diff/link check.","Active bookkeeping JSON files were parsed only at the read snapshot; no accounting conclusion follows."]

# Final closure checks: exact saved ledger replay, current controls, and preservation.
import importlib.util
sp=importlib.util.spec_from_file_location('p301_accounting', Path(__file__).with_name('accounting.py'))
am=importlib.util.module_from_spec(sp); sp.loader.exec_module(am)
audit=am.audit()[0]
actual_path=Path(__file__).with_name('actuals.json')
actual=json.loads(actual_path.read_text())
plan=json.loads(Path('v3/plan.v1.json').read_text())
exposure=json.loads(Path(__file__).with_name('exposure_completion.json').read_text())
base=json.loads(Path(__file__).with_name('baseline.json').read_text())
checks={
 'exact_replay_matches_actual_research':audit['research_ns']==actual['research_ns'],
 'exact_replay_matches_actual_engaged':audit['engaged_ns']==actual['engaged_ns'],
 'clock_stopped':audit['open_segment'] is None,
 'floor_met':audit['protected_research_floor_met'],
 'one_exact_append':audit['ledger_relation']=='already_matches_this_attempt_append',
 'actuals_finalized':actual['finalized'] is True,
 'P3_01_complete':next(x for x in plan['chunks'] if x['id']=='P3-01')['status']=='complete',
 'later_chunks_unstarted':all(x['status']=='unstarted' for x in plan['chunks'] if x['id']!='P3-01'),
 'gates_unattempted':all(x['status']=='unattempted' for x in plan['gates'].values()),
 'next_P3_02':plan['next_task']=='P3-02',
 'novelty_unsupported':plan['contribution_status']=='NOT YET SUPPORTED',
 'no_final_exposure':not plan['experimental_freeze_created'] and not plan['final_evaluation_exposed'],
 'exposure_closed':exposure['administrative_close']=='complete',
 'root_README_bytes_preserved':hashlib.sha256(Path('README.md').read_bytes()).hexdigest()==base['files']['README.md']['sha256'],
}
# The three preclose Unicode/em-dash headings were manually inspected in the saved audit.
known_manual={(r['from'],r['target']) for r in json.loads(Path(__file__).with_name('reviews').joinpath('artifact_integrity_preclose.json').read_text())['result']['markdown']['anchor_limits']}
unknown_anchors=[r for r in report['markdown']['anchor_limits'] if (r['from'],r['target']) not in known_manual]
deferred_outputs={str(Path(__file__).with_name(n).resolve().relative_to(Path.cwd())) for n in ('final_validation.json','artifact_hashes.json')}
report['generated_output_targets']={'paths':sorted(deferred_outputs),'scope':'The receipt and final manifest are created after this read-only input validation and checked for existence/hash consistency before publication.'}
checks.update({
 'no_missing_input_files':not [r for r in report['markdown']['missing_targets'] if r['resolved'] not in deferred_outputs],
 'no_new_unresolved_anchor':not unknown_anchors,
 'json_parses':not report['json_syntax']['errors'],
 'semantic_references':not report['semantic_index']['missing_references'] and not report['semantic_index']['missing_canonical_documents'],
 'duty_associations':not report['semantic_index']['question_duty_association_differences'],
 'five_questions':report['semantic_index']['question_ids_exact'],
 'saved_development_provenance':provenance['consistent_11_3449'] and provenance['all_script_hashes_match'] and provenance['all_groups_pass'] and provenance['development_only'],
 'phase_three_change_scope':report['git']['phase_three_only'],
 'git_diff_check':all(g['returncode']==0 for g in report['git']['commands']),
 'snapshot_stable':not changed_during,
})
report['closure_checks']=checks
report['accounting']={k:actual[k] for k in ['research_ns','engaged_ns','excluded_ns','phase3_research_ns','phase3_engaged_ns','ledger_rows_appended','ledger_after_sha256','closed_effective_segments','disposition_count']}
report['new_anchor_limits']=unknown_anchors
report['command']=[sys.executable, str(Path(__file__).relative_to(Path.cwd()))]
report['classification']='administrative final artifact and accounting validation; not an experiment or gate'
report['limits']=['Markdown parser is not a full renderer or external URL audit.', 'Three inherited em-dash heading anchors use the explicitly saved manual check.', 'Semantic ID checks do not prove mathematical claims.', 'No scientific execution or legacy suite rerun.', 'Final manifest is generated after this read-only snapshot; Git publication verifies its exact staged tree separately.']
report['status']='PASS' if all(checks.values()) else 'FAIL'
print(json.dumps(report,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
