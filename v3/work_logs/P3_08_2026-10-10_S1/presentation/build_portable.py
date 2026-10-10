"""Administrative portable Markdown copies; never rewrites scientific inputs.

Uses the existing guard's exact transform, with source-bound relative-link
relocation. No renderer, policy execution, proof check or research credit.
"""
from collections import Counter
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
SESSION = ROOT / "v3/work_logs/P3_08_2026-10-10_S1"
OUT = SESSION / "presentation"
GUARD_PATH = ROOT / "v3/checks/math_markdown.py"
spec = importlib.util.spec_from_file_location("p308_portable_math_guard", GUARD_PATH)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path):
    return path.relative_to(ROOT).as_posix()


def write_new(path, text):
    assert path.is_relative_to(OUT), path
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8") as stream:
        stream.write(text)


def json_new(path, value):
    write_new(path,json.dumps(value,indent=2,ensure_ascii=False)+"\n")


def ignored_tree(parts):
    return any(p in {"source","sources","source_snapshot","source_before","source_after",
                     "source_capture","inputs","u08_source"}
               or re.match(r"^(?:v\d+_)?run(?:_v\d.*)?$",p)
               or re.match(r"^nonfavorite_v\d",p) for p in parts)


def canonical_paths():
    selected = {ROOT/"v3/experiments/development.md", ROOT/"v3/checkpoints/B_1_P3_08.md",
                ROOT/"v3/work_logs/P3_08_2026-10-10_S1.md"}
    selected.update((ROOT/"v3/derivations").glob("08_*.md"))
    selected.update(SESSION.glob("*.md"))
    for path in (SESSION/"reviews").rglob("*.md"):
        parts = path.relative_to(SESSION/"reviews").parts
        if not ignored_tree(parts[:-1]) and "plan" not in path.stem:
            selected.add(path)
    selected.update(SESSION/p for p in (
        "development/structural/analysis_v4_1.md",
        "development/structural/tariff_v4_1_scope_note.md",
        "development/price_envelope/mean_analysis.md"))
    return sorted(p for p in selected if p.is_file())


def destination(path):
    if path.is_relative_to(SESSION):
        return OUT/path.relative_to(SESSION)
    if path.parent == ROOT/"v3/experiments":
        return OUT/"main"/path.name
    if path.parent == ROOT/"v3/derivations":
        return OUT/"derivations"/path.name
    if path.parent == ROOT/"v3/checkpoints":
        return OUT/"checkpoints"/path.name
    return OUT/"work_log"/path.name


def issues_for(text, name):
    issues = []
    for start,end,kind,body in guard.math_spans(text):
        problems = []
        if kind.startswith("legacy"):
            problems.append("legacy math delimiter")
        if r"\operatorname" in body:
            problems.append("unsupported operatorname macro")
        if name.startswith("v3/") and kind == "display":
            problems.append("use a math fence to protect TeX from Markdown parsing")
        if name.startswith("v3/") and kind == "inline" and not (body.startswith("`") and body.endswith("`")):
            problems.append("use dollar-backtick protection for inline TeX")
        if problems:
            issues.append({"path":name,"line":text.count("\n",0,start)+1,"problems":problems})
    return issues


def literal_intervals(text):
    """Ordinary/code-protected inline code and every fenced code block."""
    result, at = [], 0
    while at < len(text):
        if at == 0 or text[at-1] == "\n":
            fence = re.match(r" {0,3}(`{3,}|~{3,})([^\n]*)\n",text[at:])
            if fence:
                marker = fence.group(1)
                close = re.compile(r"(?m)^ {0,3}"+re.escape(marker[0])+"{"+str(len(marker))+r",}[ \t]*(?:\n|$)")
                ending = close.search(text,at+fence.end())
                stop = ending.end() if ending else len(text)
                result.append((at,stop)); at = stop; continue
        if text[at] == "`" and not guard.escaped(text,at):
            marker = re.match(r"`+",text[at:]).group()
            end = text.find(marker,at+len(marker))
            stop = end+len(marker) if end >= 0 else len(text)
            result.append((at,stop)); at=stop; continue
        at += 1
    return result


def link_spans(text):
    literals = literal_intervals(text)
    inside = lambda n:any(a <= n < b for a,b in literals)
    candidates = []
    for match in re.finditer(r"\]\(",text):
        if inside(match.start()) or guard.escaped(text,match.start()):
            continue
        # Require an actual opening label bracket on this line. Inline code
        # in a link label is allowed; a complete link inside code is ignored.
        opening = text.rfind("[",text.rfind("\n",0,match.start())+1,match.start())
        if opening < 0 or guard.escaped(text,opening):
            continue
        at = match.end()
        while at < len(text) and text[at] in " \t\n":
            at += 1
        candidates.append((at,"inline"))
    for match in re.finditer(r"(?m)^ {0,3}\[([^\]\n]+)\]:[ \t]*",text):
        if not inside(match.start()) and not match.group(1).startswith("^"):
            candidates.append((match.end(),"reference"))
    result = []
    for at,kind in candidates:
        if at >= len(text):
            continue
        angle = text[at] == "<"
        start = at+1 if angle else at
        if angle:
            end = text.find(">",start)
            if end < 0:
                continue
        else:
            end,depth = start,0
            while end < len(text):
                char = text[end]
                if char == "\\" and end+1 < len(text):
                    end += 2; continue
                if char.isspace():
                    break
                if char == "(":
                    depth += 1
                elif char == ")":
                    if depth == 0:
                        break
                    depth -= 1
                end += 1
        if end > start:
            result.append((start,end,text[start:end],kind))
    return sorted(set(result))


def logical_destination(origin, target):
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
        return None
    path = Path(os.path.abspath(origin.parent/unquote(parsed.path))) if parsed.path else origin
    return path,parsed.query,parsed.fragment,parsed.path.endswith("/")


def relocate_links(text, original, copied):
    substitutions,records = [],[]
    for start,end,target,kind in link_spans(text):
        resolved = logical_destination(original,target)
        if resolved is None:
            continue
        path,query,fragment,trailing = resolved
        new_path = os.path.relpath(path,copied.parent).replace(os.sep,"/")
        if trailing and not new_path.endswith("/"):
            new_path += "/"
        encoded = quote(new_path,safe="/!$&'()*+,;=:@-._~")
        replacement = urlunsplit(("","",encoded,query,fragment))
        check = logical_destination(copied,replacement)
        assert check[:3] == resolved[:3],(target,replacement,resolved,check)
        substitutions.append((start,end,replacement))
        records.append({"kind":kind,"original_target":target,"portable_target":replacement,
            "resolved_original_path":relative(path) if path.is_relative_to(ROOT) else str(path),
            "query":query,"fragment":fragment,"target_exists":path.exists()})
    after=text
    for start,end,replacement in reversed(substitutions):
        after = after[:start]+replacement+after[end:]
    return after,records


def existing_files():
    names = subprocess.check_output(["git","ls-files","--cached","--others","--exclude-standard","-z"],cwd=ROOT).split(b"\0")
    return sorted({ROOT/name.decode() for name in names if name
                   and (ROOT/name.decode()).is_file() and not (ROOT/name.decode()).is_relative_to(OUT)})


def base_markdown(commit):
    names = [n for n in subprocess.check_output(["git","ls-tree","-r","--name-only",commit],cwd=ROOT,text=True).splitlines() if n.endswith(".md")]
    data = subprocess.check_output(["git","cat-file","--batch"],cwd=ROOT,
        input=("\n".join(commit+":"+n for n in names)+"\n").encode())
    output,at = {},0
    for name in names:
        end=data.index(b"\n",at)
        size=int(data[at:end].split()[-1]); at=end+1
        output[name]=data[at:at+size].decode(); at+=size+1
    assert at == len(data)
    return output


def main():
    assert ROOT.joinpath("v3/STYLE.md").is_file(),ROOT
    originals = existing_files()
    before = [{"path":relative(p),"bytes":p.stat().st_size,"sha256":sha(p)} for p in originals]
    json_new(OUT/"original_preservation_before.json",before)
    canonical = canonical_paths()
    entries=[]
    for original in canonical:
        text=original.read_text()
        protected=guard.transform(text,protect=True)
        entry={"original_path":relative(original),"original_sha256":sha(original),
            "original_bytes":original.stat().st_size,"original_guard_issues":issues_for(text,relative(original)),
            "notation_transform_changes_source":protected != text}
        if protected != text:
            copied=destination(original)
            body,links=relocate_links(protected,original,copied)
            original_link=os.path.relpath(original,copied.parent).replace(os.sep,"/")
            banner=("> **Portable display copy — notation only.**\n>\n"
                f"> Original: [{relative(original)}]({original_link})  \n"
                f"> Original SHA-256: `{entry['original_sha256']}`.\n>\n"
                "> Generated with the unchanged math guard's `transform(protect=True)`,\n"
                "> plus relocation of relative links to their original destinations.\n"
                "> The original scientific document remains unchanged. This is a source-notation\n"
                "> check, with no live-render or new mathematical validation claim.\n\n")
            expected=banner+body
            write_new(copied,expected)
            assert copied.read_text() == expected
            assert not issues_for(expected,relative(copied)),relative(copied)
            assert guard.transform(expected,protect=True) == expected,relative(copied)
            assert logical_destination(copied,original_link)[0] == original
            entry.update({"portable_path":relative(copied),"portable_sha256":sha(copied),
                "portable_bytes":copied.stat().st_size,"relocated_links":links,
                "exact_declared_transform":True,"portable_guard_issues":[],
                "portable_transform_idempotent":True})
        else:
            entry.update({"portable_path":None,"disposition":"Original already uses the guarded notation; direct original link retained."})
        entries.append(entry)
    copies=[e for e in entries if e["portable_path"]]
    index=["# P3-08 portable mathematical display copies\n",
        "Administrative presentation copies; zero research credit. Original scientific evidence remains unchanged.\n",
        f"Inspected {len(entries)} canonical documents. Only the {len(copies)} documents needing an actual notation substitution have display copies. Existing guarded originals remain direct links.\n",
        "Every display copy names the original path and SHA-256. Its mathematical source uses the existing guard's exact protected transform; relative links still lead to the original targets. No browser or live-render validation was performed.\n",
        "The focused display-copy check and the repository-wide check have separate outcomes in [receipt.json](receipt.json). Retained original/source history can still make the global check fail.\n",
        "## Display copies\n", "| Original | Portable display copy |\n| --- | --- |"]
    for entry in copies:
        orig=ROOT/entry["original_path"]; copied=ROOT/entry["portable_path"]
        index.append(f"| [{entry['original_path']}]({os.path.relpath(orig,OUT)}) | [{copied.relative_to(OUT).as_posix()}]({copied.relative_to(OUT).as_posix()}) |")
    index += ["\n## Already guarded canonical originals\n"]
    for entry in entries:
        if entry["portable_path"] is None:
            index.append(f"- [{entry['original_path']}]({os.path.relpath(ROOT/entry['original_path'],OUT)})")
    index += ["\n## Verification records\n",
        "- [Presentation receipt and complete canonical mappings](receipt.json)",
        "- [Global read-only guard receipt](global_guard_readonly.json)",
        "- [Base-commit guard comparison](base_guard_comparison.json)",
        "- [Preserved original inventory before](original_preservation_before.json)",
        "- [Preserved original inventory after](original_preservation_after.json)",
        "- [Administrative plan](plan.md)",
        "- [Copy builder](build_portable.py)"]
    write_new(OUT/"index.md","\n".join(index)+"\n")
    # This is the actual unchanged global CLI, used without --fix.
    completed=subprocess.run([sys.executable,str(GUARD_PATH),"--receipt",str(OUT/"global_guard_readonly.json")],
        cwd=ROOT,text=True,capture_output=True)
    write_new(OUT/"global_guard_readonly.stdout.txt",completed.stdout)
    write_new(OUT/"global_guard_readonly.stderr.txt",completed.stderr)
    assert completed.returncode in (0,1),completed.stderr
    global_receipt=json.loads((OUT/"global_guard_readonly.json").read_text())
    assert global_receipt["fixed"] is False
    recomputed=[issue for path in guard.paths(ROOT) for issue in issues_for(path.read_text(),relative(path))]
    assert recomputed == global_receipt["issues_before"]
    assert not any(i["path"].startswith(relative(OUT)+"/") for i in recomputed)
    commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    guard_at_base=subprocess.check_output(["git","show",commit+":v3/checks/math_markdown.py"],cwd=ROOT)
    assert hashlib.sha256(guard_at_base).hexdigest() == sha(GUARD_PATH)
    base=base_markdown(commit)
    base_issues=[issue for name,text in sorted(base.items()) for issue in issues_for(text,name)]
    issue_key=lambda i:(i["path"],i["line"],tuple(i["problems"]))
    base_keys={issue_key(i) for i in base_issues}
    canonical_names={relative(p) for p in canonical}
    classified=Counter()
    for issue in recomputed:
        name=issue["path"]
        if name in base:
            category="unchanged_base_file" if (ROOT/name).read_text() == base[name] else "changed_base_file"
        elif ignored_tree(Path(name).parts[:-1]):
            category="new_preserved_run_or_source_copy"
        elif name in canonical_names:
            category="new_preserved_canonical_original"
        else:
            category="new_other_preserved_markdown"
        classified[category] += 1
    comparison={"method":"Read-only HEAD Markdown blobs; same unchanged guard math_spans and exact issue predicates.",
        "base_commit":commit,"guard_sha256":sha(GUARD_PATH),"base_files_scanned":len(base),
        "base_issue_count":len(base_issues),"base_issues":base_issues,
        "current_files_scanned":global_receipt["files_scanned"],"current_issue_count":len(recomputed),
        "current_issues_identical_to_base":sum(issue_key(i) in base_keys for i in recomputed),
        "current_issues_by_preservation_category":dict(classified),
        "portable_presentation_issue_count":0,"global_exit_code":completed.returncode,
        "global_status":"PASS" if completed.returncode == 0 else "FAIL — retained originals/history have source-convention findings; no originals repaired.",
        "original_preservation_has_user_precedence":True,"no_live_render_validation":True}
    json_new(OUT/"base_guard_comparison.json",comparison)
    after=[{"path":relative(p),"bytes":p.stat().st_size,"sha256":sha(p)} for p in originals]
    assert before == after,"An original file changed during the administrative capture."
    json_new(OUT/"original_preservation_after.json",after)
    receipt={"stage":"DEVELOPMENT presentation only","research_credit_seconds":0,"policy_runs_added":0,
        "guard_sha256":sha(GUARD_PATH),"style_sha256":sha(ROOT/"v3/STYLE.md"),
        "builder_sha256":sha(Path(__file__).resolve()),"guard_transform":"transform(original_text, protect=True)",
        "additional_transform":"Original-source banner and source-preserving ordinary relative Markdown target relocation.",
        "canonical_documents_inspected":len(entries),"portable_copies_created":len(copies),
        "original_files_preservation_verified":len(before),"originals_unchanged":before==after,
        "frozen_duplicate_trees_copied":0,"focused_portable_guard":"PASS",
        "focused_portable_issue_count":0,"global_guard_exit_code":completed.returncode,
        "global_guard_issue_count":len(recomputed),"base_guard_issue_count":len(base_issues),
        "global_guard_findings":dict(classified),"global_pass_claimed":completed.returncode==0,
        "live_render_validation_performed":False,"relative_link_destinations_verified":sum(len(e.get("relocated_links",[])) for e in entries),
        "preexisting_missing_original_targets":[{"original":e["original_path"],**link}
             for e in entries for link in e.get("relocated_links",[]) if not link["target_exists"]],
        "index_sha256":sha(OUT/"index.md"),"canonical_documents":entries}
    json_new(OUT/"receipt.json",receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k not in {"canonical_documents","preexisting_missing_original_targets"}},indent=2))


if __name__ == "__main__":
    main()
