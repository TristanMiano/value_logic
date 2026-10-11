#!/usr/bin/env python3
"""Check the repository's portable Markdown math conventions.

This is a narrow delimiter/macro guard, not a TeX renderer or proof checker.
Literal inline code and non-math fenced code are deliberately left alone.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def escaped(text: str, at: int) -> bool:
    n = 0
    while at and text[at - 1] == "\\":
        at -= 1
        n += 1
    return n % 2 == 1


def math_spans(text: str):
    """Yield (start, end, kind, body); ignore Markdown literal code."""
    at = 0
    while at < len(text):
        if at == 0 or text[at - 1] == "\n":
            fence = re.match(r" {0,3}(`{3,}|~{3,})([^\n]*)\n", text[at:])
            if fence:
                marker, info = fence.groups()
                body_start = at + fence.end()
                closing = re.compile(r"(?m)^ {0,3}" + re.escape(marker[0]) +
                                     "{" + str(len(marker)) + r",}[ \t]*(?:\n|$)")
                end = closing.search(text, body_start)
                stop = end.end() if end else len(text)
                if info.strip() == "math":
                    yield at, stop, "math_fence", text[body_start:end.start() if end else len(text)]
                at = stop
                continue
        if text[at] == "`" and not escaped(text, at):
            run = re.match(r"`+", text[at:]).group()
            end = text.find(run, at + len(run))
            at = len(text) if end < 0 else end + len(run)
            continue
        if not escaped(text, at):
            found = False
            for opening, closing, kind in [(r"\(", r"\)", "legacy_inline"),
                                            (r"\[", r"\]", "legacy_display"),
                                            ("$$", "$$", "display"),
                                            ("$", "$", "inline")]:
                if not text.startswith(opening, at):
                    continue
                if kind == "inline" and (at + 1 == len(text) or text[at + 1].isspace()):
                    continue
                end = text.find(closing, at + len(opening))
                while end >= 0 and escaped(text, end):
                    end = text.find(closing, end + len(closing))
                if end < 0:
                    continue
                if kind == "inline" and (text[end - 1].isspace() or "\n\n" in text[at:end]):
                    continue
                yield at, end + len(closing), kind, text[at + len(opening):end]
                at = end + len(closing)
                found = True
                break
            if found:
                continue
        at += 1


def portable_body(body: str) -> str:
    # Starred argmin is the only starred use in the audited repository.
    body = re.sub(r"\\operatorname\*\{argmin\}", r"\\mathop{\\mathrm{argmin}}\\limits", body)
    return re.sub(r"\\operatorname\s*\{", r"\\mathrm{", body)


def transform(text: str, protect: bool = False) -> str:
    out, previous = [], 0
    for start, end, kind, body in math_spans(text):
        out.append(text[previous:start])
        body = portable_body(body)
        if kind == "legacy_inline" or (protect and kind == "inline"):
            if body.startswith("`") and body.endswith("`"):
                body = body[1:-1]
            replacement = "$`" + body + "`$"
        elif protect and kind in ("legacy_display", "display"):
            # A fenced math block protects TeX row separators and escaped
            # braces from Markdown's own backslash processing.
            prefix = text[text.rfind("\n", 0, start) + 1:start]
            indent = prefix if prefix.isspace() else ""
            replacement = "```math\n" + body.strip("\n") + "\n" + indent + "```"
            if prefix.strip():
                replacement = "\n\n" + replacement
            if end < len(text) and text[end] != "\n":
                replacement += "\n\n"
        elif kind == "legacy_display":
            replacement = "$$\n" + body.strip("\n") + "\n$$"
            if start and text[start - 1] != "\n":
                replacement = "\n\n" + replacement
            if end < len(text) and text[end] != "\n":
                replacement += "\n\n"
        else:
            original = text[start:end]
            replacement = portable_body(original)
        out.append(replacement)
        previous = end
    out.append(text[previous:])
    return "".join(out)


def paths(root: Path):
    names = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        cwd=root, text=True).splitlines()
    return [root / name for name in sorted(set(names)) if (root / name).is_file()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="Apply only the documented portable notation substitutions")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--protect-path", action="append", default=[],
                        help="File or directory whose existing math also receives Markdown code protection")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    changed, issues, count = [], [], 0
    for path in paths(root):
        before = path.read_text()
        spans = list(math_spans(before))
        count += len(spans)
        relative = str(path.relative_to(root))
        for start, end, kind, body in spans:
            problems = []
            if kind.startswith("legacy"):
                problems.append("legacy math delimiter")
            if r"\operatorname" in body:
                problems.append("unsupported operatorname macro")
            if relative.startswith("v3/") and kind == "display":
                problems.append("use a math fence to protect TeX from Markdown parsing")
            if relative.startswith("v3/") and kind == "inline" and not (body.startswith("`") and body.endswith("`")):
                problems.append("use dollar-backtick protection for inline TeX")
            if problems:
                issues.append(dict(path=str(path.relative_to(root)),
                                   line=before.count("\n", 0, start) + 1, problems=problems))
        protect = relative.startswith("v3/") or any(relative == p or relative.startswith(p.rstrip("/") + "/")
                      for p in args.protect_path)
        after = transform(before, protect=protect)
        if after != before:
            changed.append(dict(path=str(path.relative_to(root)),
                                before_sha256=hashlib.sha256(before.encode()).hexdigest(),
                                after_sha256=hashlib.sha256(after.encode()).hexdigest(),
                                legacy_inline=sum(s[2] == "legacy_inline" for s in spans),
                                legacy_display=sum(s[2] == "legacy_display" for s in spans),
                                protect_math=protect,
                                operatorname=sum(s[3].count(r"\operatorname") for s in spans)))
            if args.fix:
                path.write_text(after)
    receipt = dict(checker="math-markdown-v2", scope="Markdown source conventions; no live GitHub rendering or mathematical validation claim",
                   files_scanned=len(paths(root)), math_spans=count, changed_files=changed,
                   issues_before=issues, fixed=args.fix)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        with args.receipt.open("x") as f:
            json.dump(receipt, f, indent=2)
            f.write("\n")
    print(json.dumps({k: v for k, v in receipt.items() if k not in ["changed_files", "issues_before"]} |
                     dict(changed_file_count=len(changed), issue_count=len(issues))))
    if not args.fix and issues:
        for item in issues[:20]:
            print(json.dumps(item))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
