"""Bounded source-level F17 navigation, delimiter and evidence-binding check.

Contributor: ChatGPT (GPT-6 Astra Pro), same-model internal review.
No scientific execution, live-URL access, Markdown rendering or PDF inspection.
The parser covers the Markdown forms found in this fixed report and reports
unparsed link-shaped forms instead of silently claiming general GFM support.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit


EXPECTED_REPORT_SHA = "18c45d7df537c6e8a076793c9e38412e5c8d887995ba041d2ee9cbf51971bc8d"
REFERENCE_KEYS = [
    ("ruspini", "Ruspini1991"), ("ai", "CousotCousot1977"),
    ("kozen", "Kozen1981"), ("semiring", "BistarelliMontanariRossi1997"),
    ("qar", "MardarePanangadenPlotkin2016"), ("rll", "BacciEtAl2026"),
    ("desirability", "MirandaZaffalon2022v2"), ("polyhedra", "FouilheMonniauxPerin2013"),
    ("acc", "AlbertArenasPuebla2006"), ("preservation", "RanzatoTapparo2006v3"),
    ("decision", "BoutilierEtAl2006"), ("chain", "GasanovaNicklasson2024"),
    ("ordering", "HappachHellersteinLidbetter2022"), ("recovery", "EttehadFoucart2021"),
    ("center", "ParuchuriChatterjee2023v1"), ("choquet17", "OliveiraRomanoDuarte2017"),
    ("choquet22", "deOliveiraDuarteRomano2022"), ("causal", "GeigerEtAl2021"),
    ("das", "GeigerEtAl2024DAS"), ("probes", "HewittLiang2019"),
    ("superposition", "ElhageEtAl2022"), ("illusion", "MakelovEtAl2024"),
    ("reply", "WuEtAl2024v1"), ("hoeffding", "Hoeffding1963"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def line_at(text, offset):
    return text.count("\n", 0, offset) + 1


def blank(text):
    return "".join("\n" if c == "\n" else " " for c in text)


def unescaped(text, position):
    backslashes = 0
    position -= 1
    while position >= 0 and text[position] == "\\":
        backslashes += 1
        position -= 1
    return backslashes % 2 == 0


def mask_code(text, issues):
    lines = text.splitlines(keepends=True)
    masked = []
    opened = None
    blocks = []
    for number, line in enumerate(lines, 1):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\n"))
        if opened is None and match:
            opened = (match[1][0], len(match[1]), number, match[2].strip())
            masked.append(blank(line))
        elif opened is not None:
            masked.append(blank(line))
            if match and match[1][0] == opened[0] and len(match[1]) >= opened[1] and not match[2].strip():
                blocks.append({"start_line": opened[2], "end_line": number, "info": opened[3]})
                opened = None
        else:
            masked.append(line)
    if opened:
        issues.append({"kind": "unclosed_code_fence", "line": opened[2]})
    value = "".join(masked)
    spans = []
    chars = list(value)
    runs = list(re.finditer(r"`+", value))
    index = 0
    while index < len(runs):
        opening = runs[index]
        if not unescaped(value, opening.start()):
            index += 1
            continue
        end = index + 1
        while end < len(runs) and len(runs[end][0]) != len(opening[0]):
            end += 1
        if end == len(runs):
            issues.append({"kind": "unmatched_inline_code_delimiter", "line": line_at(value, opening.start())})
            break
        closing = runs[end]
        spans.append({"start_line": line_at(value, opening.start()), "end_line": line_at(value, closing.start())})
        chars[opening.start():closing.end()] = blank(value[opening.start():closing.end()])
        index = end + 1
    return "".join(chars), blocks, spans


def anchor_inventory(text):
    """GFM-compatible slugging for inspected plain-text ATX headings.

    Linked heading targets in this report use only ASCII words, spaces,
    punctuation and decimal section numbers. General rich-heading rendering
    is deliberately outside this check's guarantee.
    """
    explicit = re.findall(r'<a\b[^>]*\b(?:id|name)=["\']([^"\']+)["\'][^>]*>', text)
    headings = []
    seen = Counter()
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^ {0,3}(#{1,6})\s+(.+?)(?:\s+#+\s*)?$", line)
        if not match:
            continue
        title = html.unescape(match[2])
        title = re.sub(r"<[^>]*>", "", title)
        title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", title)
        title = title.replace("`", "")
        lowered = title.lower()
        stem = "".join(c for c in lowered if c.isspace() or c in "_-" or unicodedata.category(c)[0] in "LNM")
        stem = stem.replace(" ", "-")
        slug = stem if seen[stem] == 0 else f"{stem}-{seen[stem]}"
        seen[stem] += 1
        headings.append({"line": number, "level": len(match[1]), "title": match[2], "slug": slug})
    return {"explicit": explicit, "headings": headings,
            "ids": explicit + [h["slug"] for h in headings]}


def math_inventory(text, issues):
    delimiters = re.compile(r"\$\$|\$|\\[\[\]()]" )
    opened = None
    spans = []
    close_for = {"$": "$", "$$": "$$", "\\(": "\\)", "\\[": "\\]"}
    for match in delimiters.finditer(text):
        if not unescaped(text, match.start()):
            continue
        token = match[0]
        if opened is None:
            if token not in close_for:
                issues.append({"kind": "orphan_math_closer", "line": line_at(text, match.start()), "token": token})
            else:
                opened = match
        elif token == close_for[opened[0]]:
            content = text[opened.end():match.start()]
            stack = []
            for pos, c in enumerate(content):
                if c in "{}" and unescaped(content, pos):
                    if c == "{":
                        stack.append(pos)
                    elif stack:
                        stack.pop()
                    else:
                        issues.append({"kind": "orphan_math_brace", "line": line_at(text, opened.end() + pos)})
            if stack:
                issues.append({"kind": "unclosed_math_brace", "line": line_at(text, opened.end() + stack[-1])})
            environments = []
            environment_stack = []
            for env in re.finditer(r"\\(begin|end)\{([^}]+)\}", content):
                if env[1] == "begin":
                    environment_stack.append(env[2])
                    environments.append(env[2])
                elif not environment_stack or environment_stack.pop() != env[2]:
                    issues.append({"kind": "mismatched_math_environment", "environment": env[2], "line": line_at(text, opened.end() + env.start())})
            if environment_stack:
                issues.append({"kind": "unclosed_math_environment", "environments": environment_stack})
            spans.append({"delimiter": opened[0], "start_line": line_at(text, opened.start()),
                          "end_line": line_at(text, match.start()), "environments": environments})
            opened = None
        else:
            issues.append({"kind": "mixed_math_delimiters", "line": line_at(text, match.start()),
                           "open": opened[0], "found": token})
    if opened is not None:
        issues.append({"kind": "unclosed_math_delimiter", "line": line_at(text, opened.start()), "token": opened[0]})
    return spans


def hashed_bindings(node, trail="$", output=None):
    if output is None:
        output = []
    if isinstance(node, dict):
        if "path" in node and "sha256" in node:
            output.append((trail, node))
        for key, value in node.items():
            hashed_bindings(value, f"{trail}.{key}", output)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            hashed_bindings(value, f"{trail}[{index}]", output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument("--out", type=Path, default=Path(__file__).with_name("result.json"))
    args = parser.parse_args()
    root = args.repo_root.resolve()
    issues = []
    report_path = root / "paper_v2.md"
    map_path = root / "v2/reporting/F17_v1/claim_map.json"
    bib_path = root / "v2/reporting/F17_v1/references.bib"
    report_bytes, map_bytes, bib_bytes = [p.read_bytes() for p in [report_path, map_path, bib_path]]
    report = report_bytes.decode("utf-8")
    claim_map = json.loads(map_bytes)
    bibliography = bib_bytes.decode("utf-8")
    if sha(report_bytes) != EXPECTED_REPORT_SHA:
        issues.append({"kind": "unexpected_report_snapshot", "actual": sha(report_bytes)})
    masked, code_blocks, inline_code = mask_code(report, issues)
    anchors = anchor_inventory(masked)
    duplicate_anchors = [key for key, count in Counter(anchors["ids"]).items() if count > 1]
    if duplicate_anchors:
        issues.append({"kind": "duplicate_anchors", "ids": duplicate_anchors})
    math = math_inventory(masked, issues)

    # No nested labels, destination spaces or reference-style forms occur here.
    pattern = re.compile(r"(?<!!)\[([^]\n]*)\]\(([^)\s]+)\)")
    matches = list(pattern.finditer(masked))
    if len(matches) != masked.count("]("):
        issues.append({"kind": "unparsed_inline_link_form", "parsed": len(matches), "link_shaped": masked.count("](")})
    if re.search(r"^\s*\[[^]]+\]:", masked, re.M):
        issues.append({"kind": "reference_style_links_require_additional_parser"})
    links = []
    citations = Counter()
    for match in matches:
        label, target = match.groups()
        parsed = urlsplit(target)
        row = {"line": line_at(masked, match.start()), "label": label, "target": target}
        if parsed.scheme or parsed.netloc:
            row["kind"] = "external_syntax_only"
            if parsed.scheme not in {"https", "http"} or not parsed.netloc:
                issues.append({"kind": "unexpected_external_link", **row})
        else:
            path = unquote(parsed.path)
            fragment = unquote(parsed.fragment)
            destination = (report_path.parent / path).resolve() if path else report_path
            row.update(kind="local_file" if path else "same_document_anchor", exists=destination.exists())
            if not destination.exists():
                issues.append({"kind": "missing_local_target", **row})
            if fragment:
                target_anchors = anchors if not path else anchor_inventory(destination.read_text(encoding="utf-8")) if destination.is_file() else {"ids": [], "headings": [], "explicit": []}
                row["fragment_resolves"] = fragment in target_anchors["ids"]
                if not row["fragment_resolves"]:
                    issues.append({"kind": "unresolved_local_fragment", **row})
                if path:
                    row["matched_headings"] = [h for h in target_anchors["headings"] if h["slug"] == fragment]
                    row["target_sha256"] = sha(destination.read_bytes()) if destination.is_file() else None
                elif fragment.startswith("ref-"):
                    citations[fragment] += 1
        links.append(row)

    expected_anchors = ["ref-" + short for short, _ in REFERENCE_KEYS]
    found_references = [a for a in anchors["explicit"] if a.startswith("ref-")]
    bib_keys = re.findall(r"^@[A-Za-z]+\{([^,]+),", bibliography, re.M)
    if found_references != expected_anchors:
        issues.append({"kind": "reference_anchor_set_or_order", "actual": found_references})
    if bib_keys != [key for _, key in REFERENCE_KEYS]:
        issues.append({"kind": "bibliography_key_set_or_order", "actual": bib_keys})
    if set(citations) != set(expected_anchors):
        issues.append({"kind": "citation_coverage", "uncited": sorted(set(expected_anchors) - set(citations)), "undefined": sorted(set(citations) - set(expected_anchors))})
    braces = []
    for pos, c in enumerate(bibliography):
        if c in "{}" and unescaped(bibliography, pos):
            if c == "{":
                braces.append(pos)
            elif braces:
                braces.pop()
            else:
                issues.append({"kind": "orphan_bibliography_brace", "line": line_at(bibliography, pos)})
    if braces:
        issues.append({"kind": "unclosed_bibliography_brace", "line": line_at(bibliography, braces[-1])})

    main_sections = [re.match(r"(\d+)\.", h["title"])[1] for h in anchors["headings"] if h["level"] == 2 and re.match(r"\d+\.", h["title"])]
    sections = set()
    for h in anchors["headings"]:
        m = re.match(r"(\d+(?:\.\d+)*)(?:\.\s|\s)", h["title"])
        if m:
            sections.add(m[1])
    if main_sections != [str(i) for i in range(1, 15)]:
        issues.append({"kind": "main_section_sequence", "actual": main_sections})
    tags = re.findall(r"\\tag\{([^}]+)\}", masked)
    theorems = re.findall(r"\*\*Theorem (\d+)", masked)
    if tags != [str(i) for i in range(1, 26)]:
        issues.append({"kind": "equation_tag_sequence", "actual": tags})
    if theorems != [str(i) for i in range(1, 6)]:
        issues.append({"kind": "theorem_sequence", "actual": theorems})
    placeholder_re = re.compile(r"\b(?:TODO|TBD|FIXME|XXX|PLACEHOLDER|TK|citation needed|INSERT HERE|draft note|editorial note)\b|\?\?\?", re.I)
    placeholders = [{"line": line_at(masked, m.start()), "marker": m[0]} for m in placeholder_re.finditer(masked)]
    if placeholders:
        issues.append({"kind": "editorial_placeholder_markers", "matches": placeholders})

    claims = claim_map["claims"]
    ids = [c["id"] for c in claims]
    if len(claims) != 42 or len(set(ids)) != 42 or claim_map["claim_count"] != 42:
        issues.append({"kind": "claim_group_count_or_uniqueness", "count": len(claims), "unique": len(set(ids))})
    for claim in claims:
        if not claim.get("evidence"):
            issues.append({"kind": "claim_without_evidence", "id": claim["id"]})
        locator = claim["report_locator"]
        section_field = locator.get("sections", [])
        section_ids = section_field if isinstance(section_field, list) else re.findall(r"(?<![\d.])\d+(?:\.\d+)*(?![\d.])", section_field)
        for section in section_ids:
            if section not in sections:
                issues.append({"kind": "claim_section_locator", "id": claim["id"], "section": section})
        for tag in locator.get("equations", []):
            if str(tag) not in tags:
                issues.append({"kind": "claim_equation_locator", "id": claim["id"], "equation": tag})
        if "theorem" in locator and str(locator["theorem"]) not in theorems:
            issues.append({"kind": "claim_theorem_locator", "id": claim["id"], "theorem": locator["theorem"]})
    bindings = []
    for location, record in hashed_bindings(claim_map):
        path = root / record["path"]
        row = {"json_location": location, "path": record["path"], "expected_sha256": record["sha256"]}
        if path.is_file():
            data = path.read_bytes()
            row.update(actual_sha256=sha(data), actual_bytes=len(data), hash_matches=sha(data) == record["sha256"])
            if "bytes" in record:
                row["bytes_match"] = len(data) == record["bytes"]
            if not row["hash_matches"] or row.get("bytes_match") is False:
                issues.append({"kind": "evidence_binding_mismatch", **row})
        else:
            issues.append({"kind": "missing_hashed_evidence", **row})
        bindings.append(row)
    fragment_groups = []
    for fragment in claim_map["fragments"]:
        originals = json.loads((root / fragment["path"]).read_text())["claims"]
        original_ids = [c.get("id", c.get("claim_id")) for c in originals]
        mapped = [c for c in claims if c["source_fragment"] == fragment["path"]]
        matched = original_ids == [c["id"] for c in mapped]
        fragment_groups.append({"path": fragment["path"], "group_count": len(mapped), "ids_match_in_order": matched})
        if not matched:
            issues.append({"kind": "fragment_group_mismatch", "path": fragment["path"]})
    if report_path.read_bytes() != report_bytes or map_path.read_bytes() != map_bytes or bib_path.read_bytes() != bib_bytes:
        issues.append({"kind": "input_changed_during_check"})

    result = {
        "schema": "F17-source-navigation-check-v1",
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "principal_concurrent_credit_minutes": 0,
        "status": "PASS_SCOPED" if not issues else "DEFECTS_FOUND",
        "scope": "Fixed-report source navigation, observed Markdown syntax, bibliography keys, claim-group structure and every path/SHA256 binding directly contained in claim_map.json.",
        "limits": ["No GitHub/Markdown/PDF rendered display inspection.", "No network access or external URL liveness check.", "No new scientific tests, experiment or semantic/proof review.", "No general GFM or TeX parser guarantee; linked heading targets use determinable plain-text slugs.", "Placeholder check is an explicit marker scan, not a proof that every possible editorial issue is absent.", "Claim-map locator checks verify section/equation/theorem existence, not the truth of their claims; historical source locators are not newly substantively reread."],
        "inputs": [{"path": str(p.relative_to(root)), "bytes": len(b), "sha256": sha(b)} for p, b in [(report_path, report_bytes), (map_path, map_bytes), (bib_path, bib_bytes)]],
        "script": {"path": str(Path(__file__).resolve().relative_to(root)), "sha256": sha(Path(__file__).read_bytes())},
        "headings": anchors["headings"], "duplicate_anchors": duplicate_anchors,
        "links": links, "link_counts": dict(Counter(row["kind"] for row in links)),
        "reference_anchors": found_references, "citation_uses": dict(citations),
        "citation_use_count": sum(citations.values()), "bibliography_keys": bib_keys,
        "reference_to_key": {"ref-" + short: key for short, key in REFERENCE_KEYS},
        "code_blocks": code_blocks, "inline_code_spans": inline_code,
        "math_span_counts": dict(Counter(m["delimiter"] for m in math)), "math_spans": math,
        "equation_tags": tags, "theorem_numbers": theorems, "placeholder_matches": placeholders,
        "claim_group_count": len(claims), "unique_claim_ids": len(set(ids)),
        "fragment_groups": fragment_groups,
        "evidence_binding_occurrences": len(bindings),
        "unique_hashed_paths": len({r["path"] for r in bindings}),
        "evidence_bindings": bindings, "issues": issues,
        "scientific_execution": False, "gate_D_performed": False,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": result["status"], "result_path": str(args.out),
                      "sha256": sha(args.out.read_bytes()), "links": result["link_counts"],
                      "references": len(found_references), "citation_uses": sum(citations.values()),
                      "claim_groups": len(claims), "hash_bindings": len(bindings),
                      "unique_hashed_paths": result["unique_hashed_paths"], "issues": issues}, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
