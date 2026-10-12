#!/usr/bin/env python3
"""Publication-only Git-bound scope of the unchanged local link checker.

ChatGPT (GPT-6 Astra Pro). No scientific acquisition or research clock credit.
Run from any cwd, supplying a new output path. Isolated snapshots retain exact
Markdown, relocation manifest and relocated object bytes; other tracked files
are existence-only. These are precisely the bytes/existence facts inspected by
verification.check_links. No frozen file is edited and no semantic suite runs.
"""
from collections import Counter
from difflib import SequenceMatcher
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from tools.evidence_paths import MANIFEST
from verification.check_links import check_links, markdown_files


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def tree(ref):
    entries = {}
    for record in git('ls-tree', '-rz', ref).split(b'\0'):
        if not record:
            continue
        header, name = record.split(b'\t', 1)
        mode, kind, oid = header.decode().split()
        if mode not in ('100644', '100755') or kind != 'blob':
            raise ValueError('This checker snapshot requires regular Git files')
        entries[name.decode()] = dict(mode=mode, oid=oid)
    return entries


def blobs(oids):
    order = sorted(set(oids))
    result = subprocess.run(['git', '-C', str(ROOT), 'cat-file', '--batch'],
                            input=('\n'.join(order)+'\n').encode(),
                            capture_output=True, check=True)
    data, cursor, answer = result.stdout, 0, {}
    for requested in order:
        end = data.index(b'\n', cursor)
        oid, kind, size = data[cursor:end].decode().split()
        if oid != requested or kind != 'blob':
            raise ValueError('Unexpected Git object response')
        cursor = end+1
        body = data[cursor:cursor+int(size)]
        if hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest() != oid:
            raise ValueError('Git blob identity mismatch')
        answer[oid] = body
        cursor += int(size)+1
    if cursor != len(data):
        raise ValueError('Unconsumed Git object output')
    return answer


def normalize(root, items):
    return sorted([dict(source=i.source.relative_to(root).as_posix(), line=i.line,
                        target=i.target, detail=i.detail) for i in items],
                  key=lambda i:(i['source'], i['line'], i['target'], i['detail']))


def summary(items):
    return dict(broken_links=len(items), affected_sources=len({i['source'] for i in items}),
                by_detail=dict(sorted(Counter(i['detail'] for i in items).items())),
                normalized_failures_sha256=sha(canonical(items)))


def compare(base, later, evidence):
    original = Counter((i['source'], i['line'], i['target'], i['detail']) for i in base['failures'])
    maps = {}
    changed = []
    for name, entry in later['entries'].items():
        if not name.endswith('.md'):
            continue
        old = base['entries'].get(name)
        if old == entry:
            continue
        newer = evidence[entry['oid']].decode('utf-8').splitlines(keepends=True)
        if old is None:
            mapping = {}
        else:
            older = evidence[old['oid']].decode('utf-8').splitlines(keepends=True)
            mapping = {new_line+offset+1:old_line+offset+1
                       for old_line,new_line,length in SequenceMatcher(a=older,b=newer,autojunk=False).get_matching_blocks()
                       for offset in range(length)}
        maps[name] = mapping
        changed.append(dict(source=name, change='added' if old is None else 'modified',
                            new_lines=sum(line not in mapping for line in range(1,len(newer)+1))))
    inherited, introduced, changed_sources, changed_lines, added_sources = [], [], [], [], []
    for item in later['failures']:
        name, line = item['source'], item['line']
        base_line = maps[name].get(line) if name in maps else line
        key = (name,base_line,item['target'],item['detail'])
        row = item | dict(base_line=base_line)
        if base_line is not None and original[key]:
            original[key] -= 1
            inherited.append(row)
        else:
            introduced.append(row)
        if name in maps:
            changed_sources.append(row)
            if base_line is None:
                changed_lines.append(row)
            if name not in base['entries']:
                added_sources.append(row)
    return dict(base=base['ref'], later=later['ref'], inherited_failures=len(inherited),
                introduced_failures=introduced, unmatched_base_failures=sum(original.values()),
                failures_on_added_markdown=added_sources,
                failures_on_modified_or_added_markdown=changed_sources,
                failures_on_changed_lines=changed_lines,
                changed_markdown=changed,
                line_scope='Exact equal-line blocks map later lines to base; each matched source/line/target/detail failure consumes one baseline occurrence.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--base', default='13bca720c5e978928eee3cf155bd335fa4a099a1')
    parser.add_argument('--first-published', default='f28d760')
    parser.add_argument('--head', default='6211f8fbe37a7f34a27354250be9b0d099bf7bb4')
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Preserve earlier publication evidence')
    specs = [('base',args.base), ('first_published',args.first_published), ('head',args.head)]
    snapshots = {}
    for label, ref in specs:
        resolved = git('rev-parse',ref+'^{commit}').decode().strip()
        snapshots[label] = dict(ref=resolved, entries=tree(resolved))
    manifest_path = Path(MANIFEST).as_posix()
    manifests = blobs(s['entries'][manifest_path]['oid'] for s in snapshots.values())
    needed = set()
    for value in snapshots.values():
        entries = value['entries']
        manifest = json.loads(manifests[entries[manifest_path]['oid']])
        exact = {name for name in entries if name.lower().endswith('.md')}
        exact.add(manifest_path)
        exact.update(e['stored_path'] for e in manifest['entries'])
        value['exact_paths'] = exact
        needed.update(entries[name]['oid'] for name in exact)
    evidence = blobs(needed)
    dependencies = ['verification/check_links.py','tools/evidence_paths.py']
    dependency_blobs = blobs(s['entries'][name]['oid'] for s in snapshots.values() for name in dependencies)
    for name in dependencies:
        if len({s['entries'][name]['oid'] for s in snapshots.values()}) != 1:
            raise ValueError('Checker/admission source differs across revisions')
        oid = snapshots['head']['entries'][name]['oid']
        if (ROOT/name).read_bytes() != dependency_blobs[oid]:
            raise ValueError('Working checker differs from frozen Git source')
    scratch = Path(tempfile.mkdtemp(prefix='s06_links_'))
    for label,value in snapshots.items():
        destination = scratch/label
        destination.mkdir()
        for name,entry in value['entries'].items():
            path = destination/name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(evidence[entry['oid']] if name in value['exact_paths'] else b'')
        value['failures'] = normalize(destination,check_links(destination))
        value['markdown_sources'] = len(markdown_files(destination))
        (scratch/(label+'_failures.json')).write_text(json.dumps(value['failures'],indent=2)+'\n')
    working = normalize(ROOT,check_links(ROOT))
    report = dict(schema='value_logic.s06.publication_links.v1',
                  contributor='ChatGPT (GPT-6 Astra Pro)', research_credit_minutes=0,
                  new_solver_proof_LP_or_audit_calls=0, semantic_suite_rerun=False,
                  method='Unchanged repository link checker on isolated Git-object views. Exact Markdown/relocation bytes; regular existence-only files elsewhere. No symlinks/submodules. Equal-line maps distinguish inherited failures from edited lines.',
                  implementation_sha256=sha(Path(__file__).read_bytes()),
                  unchanged_checker_dependencies={name:dict(git_blob=snapshots['head']['entries'][name]['oid'],sha256=sha((ROOT/name).read_bytes())) for name in dependencies},
                  snapshots={label:dict(ref=s['ref'],tracked_files=len(s['entries']),markdown_sources=s['markdown_sources'],**summary(s['failures'])) for label,s in snapshots.items()},
                  base_to_first=compare(snapshots['base'],snapshots['first_published'],evidence),
                  base_to_head=compare(snapshots['base'],snapshots['head'],evidence),
                  first_to_head=compare(snapshots['first_published'],snapshots['head'],evidence),
                  working_tree=summary(working),
                  working_tree_matches_head=working==snapshots['head']['failures'],
                  scratch_evidence=str(scratch),
                  limits='This classifies link-gate failures only. It does not repair historical snapshots, run scientific experiments or prove a complete CI pass.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(output=str(args.output.resolve()),snapshots=report['snapshots'],
                          inherited_head=report['base_to_head']['inherited_failures'],
                          introduced_head=len(report['base_to_head']['introduced_failures']),
                          changed_line_failures=len(report['base_to_head']['failures_on_changed_lines']),
                          changed_document_failures=report['base_to_head']['failures_on_modified_or_added_markdown'],
                          working_tree_matches_head=report['working_tree_matches_head'],scratch=str(scratch)),indent=2))


if __name__=='__main__':
    main()
