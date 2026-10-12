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
import sys
from typing import Iterator


def escaped(text: str, at: int) -> bool:
    n = 0
    while at and text[at - 1] == "\\":
        at -= 1
        n += 1
    return n % 2 == 1


Span = tuple[int, int, str, str]


def _quote_prefix(line: str) -> tuple[str, str]:
    """Separate explicit block-quote containers without altering source offsets."""
    prefix = ""
    while match := re.match(r" {0,3}>[ \t]?", line):
        prefix += match.group()
        line = line[match.end():]
    return prefix, line


def _blocks(text: str) -> Iterator[Span]:
    """Recognize fences and indented code before scanning inline constructs.

    A fence needs the same marker and at least the opening run length to close.
    A backtick in a backtick-fence info string invalidates that opening. Ordinary
    list continuation indentation is not, by itself, an indented code block.
    """
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    i, list_indent, previous_blank = 0, 0, True
    while i < len(lines):
        quote, line = _quote_prefix(lines[i])
        indent = len(line) - len(line.lstrip(" "))
        marker = re.match(r" {0,3}(?:[-+*]|[0-9]{1,9}[.)])[ \t]+", line)
        if marker:
            list_indent = marker.end()
            content = line[marker.end():]
            prefix = quote + line[:marker.end()]
        else:
            if line.strip() and indent < list_indent:
                list_indent = 0
            remove = min(indent, list_indent)
            content, prefix = line[remove:], quote + line[:remove]
        fence = re.match(r" {0,3}(`{3,}|~{3,})([^\n\r]*)(?:\r?\n|\r|$)", content)
        if fence and not (fence[1][0] == "`" and "`" in fence[2]):
            run, info = fence[1], fence[2]
            closing = re.compile(r" {0,3}" + re.escape(run[0]) +
                                 "{" + str(len(run)) + r",}[ \t]*(?:\r?\n|\r|$)")
            j, body_end = i + 1, len(text)
            while j < len(lines):
                q, candidate = _quote_prefix(lines[j])
                if quote and (q.count(">") != quote.count(">")) and candidate.strip():
                    body_end = offsets[j]
                    break
                candidate_indent = len(candidate) - len(candidate.lstrip(" "))
                if list_indent and candidate.strip() and candidate_indent < list_indent:
                    body_end = offsets[j]
                    break
                candidate = candidate[min(candidate_indent, list_indent):]
                if closing.fullmatch(candidate):
                    body_end = offsets[j]
                    j += 1
                    break
                j += 1
            stop = offsets[j]
            kind = "math_fence" if info.strip() == "math" else "code_fence"
            yield offsets[i], stop, kind, text[offsets[i + 1]:body_end]
            i, previous_blank = j, False
            continue
        # Indented blocks cannot interrupt a paragraph. A tab at the left edge
        # is the ordinary four-column code indent; no tab expansion is applied
        # to the actual file bytes.
        code_indent = indent - list_indent
        if previous_blank and (code_indent >= 4 or (not list_indent and line.startswith("\t"))):
            j = i + 1
            while j < len(lines):
                q, candidate = _quote_prefix(lines[j])
                n = len(candidate) - len(candidate.lstrip(" "))
                if q.count(">") != quote.count(">") and candidate.strip():
                    break
                if candidate.strip() and n < list_indent + 4 and not candidate.startswith("\t"):
                    break
                j += 1
            yield offsets[i], offsets[j], "indented_code", text[offsets[i]:offsets[j]]
            i, previous_blank = j, True
            continue
        previous_blank = not line.strip()
        i += 1


def _inline_spans(text: str, start: int, stop: int) -> Iterator[Span]:
    at = start
    while at < stop:
        if text[at] == "`" and not escaped(text, at):
            run_end = at + 1
            while run_end < stop and text[run_end] == "`":
                run_end += 1
            width = run_end - at
            # An unmatched run is literal punctuation; it must not conceal
            # every later equation/link. Exact runs cannot end inside ``...``.
            closing = re.compile(r"(?<!`)`{" + str(width) + r"}(?!`)")
            paragraph = re.search(r"\n[ \t]*\n", text[run_end:stop])
            limit = run_end + paragraph.start() if paragraph else stop
            end = closing.search(text, run_end, limit)
            if end:
                yield at, end.end(), "inline_code", text[run_end:end.start()]
                at = end.end()
                continue
            at = run_end
            continue
        if not escaped(text, at):
            found = False
            for opening, closing, kind in [(r"\(", r"\)", "legacy_inline"),
                                            (r"\[", r"\]", "legacy_display"),
                                            ("$$", "$$", "display"),
                                            ("$`", "`$", "protected_inline"),
                                            ("$", "$", "inline")]:
                if not text.startswith(opening, at):
                    continue
                if kind == "inline" and (at + 1 == stop or text[at + 1].isspace()
                                           or text.startswith("$$", at)):
                    continue
                end = text.find(closing, at + len(opening), stop)
                while end >= 0 and escaped(text, end):
                    end = text.find(closing, end + len(closing), stop)
                if end < 0:
                    continue
                if kind in ("inline", "protected_inline", "legacy_inline") and re.search(
                        r"\n[ \t]*\n", text[at:end]):
                    continue
                if kind == "inline" and text[end - 1].isspace():
                    continue
                body = text[at + len(opening):end]
                if kind == "protected_inline":
                    kind, body = "inline", "`" + body + "`"
                yield at, end + len(closing), kind, body
                at = end + len(closing)
                found = True
                break
            if found:
                continue
        at += 1


def _spans(text: str) -> Iterator[Span]:
    previous = 0
    for block in _blocks(text):
        yield from _inline_spans(text, previous, block[0])
        yield block
        previous = block[1]
    yield from _inline_spans(text, previous, len(text))


def math_spans(text: str) -> Iterator[Span]:
    """Yield (start, end, kind, body); ignore Markdown literal code."""
    for span in _spans(text):
        if span[2] not in {"code_fence", "indented_code", "inline_code"}:
            yield span


def literal_spans(text: str, inline: bool = True) -> Iterator[tuple[int, int]]:
    """Yield Markdown literal blocks/spans, including block-level math fences.

    A math fence renders math, but its body is not Markdown heading/link text.
    Inline protected math remains intact here so heading slugs can use its text.
    """
    kinds = {"code_fence", "math_fence", "indented_code"} | ({"inline_code"} if inline else set())
    for start, end, kind, _ in _spans(text):
        if kind in kinds:
            yield start, end


def _masked(text: str, spans) -> str:
    result = list(text)
    for start, end in spans:
        for i in range(start, end):
            if result[i] not in "\r\n":
                result[i] = " "
    return "".join(result)


def mask_literals(text: str, inline: bool = True) -> str:
    """Hide code while retaining original character offsets and line breaks."""
    return _masked(text, literal_spans(text, inline=inline))


def mask_literals_and_math(text: str) -> str:
    """Hide code and math for prose link extraction, without moving any text."""
    return _masked(text, ((start, end) for start, end, _, _ in _spans(text)))


def portable_body(body: str) -> str:
    # Starred argmin is the only starred use in the audited repository.
    body = re.sub(r"\\operatorname\*\{argmin\}", r"\\mathop{\\mathrm{argmin}}\\limits", body)
    return re.sub(r"\\operatorname\s*\{", r"\\mathrm{", body)


def transform(text: str, protect: bool = False, spans=None) -> str:
    out, previous = [], 0
    for start, end, kind, body in math_spans(text) if spans is None else spans:
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


def text_issues(text: str, protect: bool = False, spans=None) -> list[dict]:
    """Report the same portable math rules for live files and derived views."""
    issues = []
    for start, _, kind, body in math_spans(text) if spans is None else spans:
        problems = []
        if kind.startswith("legacy"):
            problems.append("legacy math delimiter")
        if r"\operatorname" in body:
            problems.append("unsupported operatorname macro")
        if protect and kind == "display":
            problems.append("use a math fence to protect TeX from Markdown parsing")
        if protect and kind == "inline" and not (body.startswith("`") and body.endswith("`")):
            problems.append("use dollar-backtick protection for inline TeX")
        if problems:
            issues.append(dict(line=text.count("\n", 0, start) + 1, problems=problems))
    return issues


def paths(root: Path):
    names = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        cwd=root, text=True).splitlines()
    return [root / name for name in sorted(set(names)) if (root / name).is_file()]


def analyze_documents(root: Path, document_paths=None, protect_paths=()) -> dict:
    """Check live documents and verify every registered archival presentation.

    A frozen source is covered only after its scientific identity, derived-view
    identity, exact transformation, and view formatting all verify. An ordinary
    new violation remains an error; there is no failure baseline or path ignore.
    """
    root = root.resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from verification.math_views import verify_views
    views = verify_views(root)
    view_names = {entry["view_path"] for entry in views.values()}
    selected = paths(root) if document_paths is None else list(document_paths)
    changed, issues, preserved_issues, count = [], [], [], 0
    for path in selected:
        path = Path(path)
        if not path.is_absolute():
            path = root / path
        relative = path.relative_to(root).as_posix()
        before = path.read_text(encoding="utf-8")
        spans = list(math_spans(before))
        count += len(spans)
        protect = (relative.startswith("v3/") or relative in view_names or
                   any(relative == p or relative.startswith(p.rstrip("/") + "/")
                       for p in protect_paths))
        local_issues = [dict(path=relative, **problem)
                        for problem in text_issues(before, protect=protect, spans=spans)]
        if relative in views:
            preserved_issues.extend(dict(**problem, view_path=views[relative]["view_path"])
                                    for problem in local_issues)
            continue
        issues.extend(local_issues)
        after = transform(before, protect=protect, spans=spans)
        if after != before:
            changed.append(dict(path=relative,
                                before_sha256=hashlib.sha256(before.encode()).hexdigest(),
                                after_sha256=hashlib.sha256(after.encode()).hexdigest(),
                                legacy_inline=sum(s[2] == "legacy_inline" for s in spans),
                                legacy_display=sum(s[2] == "legacy_display" for s in spans),
                                protect_math=protect,
                                operatorname=sum(s[3].count(r"\operatorname") for s in spans)))
    return dict(checker="math-markdown-v3",
                scope="Portable Markdown math, with scientifically bound archival views; no live rendering or mathematical validation claim",
                files_scanned=len(selected), math_spans=count,
                changed_files=changed, issues_before=issues,
                preserved_source_issues=preserved_issues,
                verified_portable_views=len(views))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="Apply documented substitutions to explicitly selected active documents")
    parser.add_argument("--path", action="append", default=[],
                        help="Repository-relative file/directory to check; required for --fix")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--protect-path", action="append", default=[],
                        help="File or directory whose existing math also receives Markdown code protection")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[2]
    if args.fix and not args.path:
        parser.error("--fix requires an explicit --path; archived evidence must use a verified portable view")
    selected = paths(root)
    if args.path:
        selected = [path for path in selected if any(
            path.relative_to(root).as_posix() == p or
            path.relative_to(root).as_posix().startswith(p.rstrip("/") + "/") for p in args.path)]
        if not selected:
            parser.error("--path selected no Markdown files")
    try:
        receipt = analyze_documents(root, selected, args.protect_path)
        if args.fix:
            protected = {item["path"] for item in receipt["preserved_source_issues"]}
            if protected:
                raise ValueError("Refusing to rewrite scientifically bound sources: " + ", ".join(sorted(protected)))
            for item in receipt["changed_files"]:
                path = root / item["path"]
                before = path.read_text(encoding="utf-8")
                path.write_text(transform(before, protect=item["protect_math"]), encoding="utf-8")
        receipt["fixed"] = args.fix
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps(dict(checker="math-markdown-v3", status="INVALID_EVIDENCE", error=str(exc))))
        return 2
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        with args.receipt.open("x") as f:
            json.dump(receipt, f, indent=2)
            f.write("\n")
    issues = receipt["issues_before"]
    print(json.dumps({k: v for k, v in receipt.items() if k not in ["changed_files", "issues_before", "preserved_source_issues"]} |
                     dict(changed_file_count=len(receipt["changed_files"]), issue_count=len(issues),
                          preserved_source_issue_count=len(receipt["preserved_source_issues"])) ))
    if not args.fix and issues:
        for item in issues[:20]:
            print(json.dumps(item))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
