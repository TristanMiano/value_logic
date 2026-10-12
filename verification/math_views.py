"""Verify mechanically derived portable math views without rewriting evidence.

The source and view hashes are necessary but not sufficient: every view must
also equal the documented transformation of its preserved source. Archive
namespaces come only from the separately verified document-origin registry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.evidence_paths import MANIFEST as RELOCATIONS, load_entries, under, resolve, relative_path
from v3.checks.math_markdown import (
    literal_spans, mask_literals_and_math, math_spans, text_issues, transform,
)


MANIFEST = "tools/math_views.json"
SCHEMA = "value_logic.math_views.v1"
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def origins_for(root: Path) -> dict[str, str]:
    from verification.archive_origins import load_origins
    return load_origins(root)


def _relative(root: Path, source_parent: Path, target: Path) -> str:
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Document link escapes repository: {target}")
    return Path(os.path.relpath(target, source_parent)).as_posix()


def rebase_links(text: str, root: Path, origin_path: str, view_path: str,
                 source_path: str | None = None, namespaces=None) -> str:
    """Retarget actual prose links/images when the view moves directories.

    Inline/code/math examples are preserved literally. Titles and anchors are
    retained. Relocated evidence links point to the verified immutable object;
    the ordinary link guard remains responsible for target/anchor validation.
    """
    root = root.resolve()
    origin = under(root, origin_path)
    output = under(root, view_path)
    relocations = ({x["original_path"] for x in load_entries(root)}
                   if (root / RELOCATIONS).is_file() else set())
    prose = mask_literals_and_math(text)
    replacements = []
    for match in LINK.finditer(prose):
        before = prose[:match.start()]
        if (len(before) - len(before.rstrip("\\"))) % 2:
            continue
        start, end = match.span(1)
        raw = text[start:end]
        target_match = re.match(r"\s*(<[^>]*>|\S+)", raw)
        if not target_match:
            continue
        token = target_match.group(1)
        bracketed = token.startswith("<") and token.endswith(">")
        target = token[1:-1] if bracketed else token
        if namespaces is not None and source_path:
            target = namespaces.link_corrections.get(source_path, {}).get(target, target)
        parts = urlsplit(target)
        if namespaces is not None and source_path:
            for prefix in namespaces.checkout_roots.get(source_path, ()):
                if target.startswith(prefix):
                    suffix = urlsplit(target[len(prefix):])
                    path = _relative(root, origin.parent, under(root, unquote(suffix.path)))
                    target = urlunsplit(("", "", path, suffix.query, suffix.fragment))
                    parts = urlsplit(target)
                    break
        if parts.scheme or parts.netloc:
            continue
        if not parts.path:
            key = source_path + "#" + unquote(parts.fragment) if source_path else ""
            bound_fragment = namespaces.fragment_origins.get(key) if namespaces is not None else None
            if not bound_fragment:
                continue
            destination = under(root, bound_fragment)
        else:
            destination = (origin.parent / unquote(parts.path)).resolve()
        relative = destination.relative_to(root).as_posix()
        if not destination.is_file() and relative in relocations:
            destination = resolve(relative, repo=root)
        path = _relative(root, output.parent, destination)
        updated = urlunsplit(("", "", quote(path, safe="/._-~"), parts.query, parts.fragment))
        if bracketed:
            updated = "<" + updated + ">"
        replacements.append((start + target_match.start(1),
                             start + target_match.end(1), updated))
    for start, end, replacement in reversed(replacements):
        text = text[:start] + replacement + text[end:]
    return text


def portable_hard_breaks(text: str) -> str:
    """Use backslash hard breaks in prose without changing code/math literals.

    Two trailing spaces are valid Markdown hard breaks but fail the repository's
    whitespace gate. Blank lines and nonparagraph block markers are not breaks.
    """
    excluded = list(literal_spans(text)) + [(a, b) for a, b, _, _ in math_spans(text)]
    replacements = []
    for match in re.finditer(r" {2,}(?=\r?\n)", text):
        if any(a < match.end() and match.start() < b for a, b in excluded):
            continue
        prefix = text[text.rfind("\n", 0, match.start()) + 1:match.start()]
        if not prefix.strip() or re.match(r" {0,3}(?:#{1,6}(?:\s|$)|[-=_*]{3,}$|\|)", prefix):
            continue
        slashes = len(prefix) - len(prefix.rstrip("\\"))
        # An existing unpaired literal backslash needs its own escaping before
        # the final hard-break backslash is introduced.
        replacements.append((match.start(), match.end(), "\\" * (1 + slashes % 2)))
    for start, end, replacement in reversed(replacements):
        text = text[:start] + replacement + text[end:]
    return text


def view_text(root: Path, source_path: str, view_path: str,
              origins: dict[str, str], namespaces=None) -> str:
    source = under(root, source_path)
    body = transform(source.read_text(encoding="utf-8"), protect=True)
    body = portable_hard_breaks(body)
    if namespaces is None:
        from verification.archive_origins import load_namespaces
        namespaces = load_namespaces(root)
    body = rebase_links(body, root, origins.get(source_path, source_path), view_path,
                        source_path, namespaces)
    source_link = _relative(root, under(root, view_path).parent, source)
    notice = (
        "> **Portable math view.** [Preserved source](" + quote(source_link, safe="/._-~") +
        ") · [Formatting and provenance](../math_markdown.md).\n"
        "> Mathematical delimiters and the repository's operator notation are normalized;\n"
        "> relative links are rebased. The source's evidence bytes remain unchanged.\n\n"
    )
    return notice + body


def _at(value, pointer):
    if not isinstance(pointer, list):
        raise ValueError("A scientific-binding pointer must be an array")
    for part in pointer:
        if isinstance(value, list):
            if type(part) is not int or part < 0:
                raise ValueError("Invalid scientific-binding array index")
        elif isinstance(value, dict):
            if not isinstance(part, str):
                raise ValueError("Invalid scientific-binding object key")
        else:
            raise ValueError("Scientific-binding pointer enters a scalar")
        try:
            value = value[part]
        except (KeyError, IndexError) as exc:
            raise ValueError("Missing scientific-binding pointer component") from exc
    return value


def _preservation(root: Path, entry: dict, origins: dict[str, str], cache: dict) -> None:
    """Validate an existing scientific identity or a checked frozen-copy chain.

    An old formatting failure is not preservation evidence. Each reviewed entry
    names an actual experiment/review record and checks its path/hash fields.
    A relative record path is interpreted only at its own manifest directory.
    """
    name = entry["source_path"]
    preservation = entry.get("preservation")
    if not isinstance(preservation, dict):
        raise ValueError(f"Missing scientific preservation evidence: {name}")
    kind = preservation.get("kind")
    if kind == "archive-origin":
        if name not in origins or origins[name] != preservation.get("origin_path"):
            raise ValueError(f"No verified frozen-copy origin for {name}")
        return
    if kind not in {"scientific-record", "scientific-mapping"}:
        raise ValueError(f"Unsupported scientific preservation evidence: {name}")
    path = preservation["path"]
    if path not in cache:
        raw = under(root, path).read_bytes()
        cache[path] = digest(raw), json.loads(raw)
    sha, doc = cache[path]
    if sha != preservation["sha256"]:
        raise ValueError(f"Scientific preservation record hash mismatch: {path}")
    record = _at(doc, preservation["pointer"])
    if kind == "scientific-mapping":
        pointer = preservation["pointer"]
        recorded_path = pointer[-1] if pointer and isinstance(pointer[-1], str) else None
    else:
        recorded_path = _at(record, preservation["path_pointer"])
    if not isinstance(recorded_path, str):
        raise ValueError(f"Scientific record has no source path for {name}")
    relative_path(recorded_path)
    base = preservation.get("path_base", "")
    if base not in {"", Path(path).parent.as_posix()}:
        raise ValueError(f"Unsupported scientific record path base: {name}")
    bound_path = (Path(base) / recorded_path).as_posix()
    bound_sha = _at(record, preservation["sha256_pointer"])
    if (bound_path, bound_sha) != (name, entry["source_sha256"]):
        raise ValueError(f"Scientific record does not bind preserved source bytes: {name}")


def _entries(root: Path, origins: dict[str, str] | None = None):
    root = root.resolve()
    if not (root / MANIFEST).is_file():
        return [], {}, None
    doc = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    if doc.get("schema") != SCHEMA:
        raise ValueError("Unsupported portable-math-view manifest")
    from verification.archive_origins import load_namespaces
    namespaces = load_namespaces(root)
    # A supplied map is a test/consumer hint, not authority for an archive chain.
    if origins is not None and origins != namespaces.origins:
        raise ValueError("Portable views require the verified archive-origin map")
    origins = namespaces.origins
    source_names, view_names, cache = set(), set(), {}
    for entry in doc["entries"]:
        name, view = entry["source_path"], entry["view_path"]
        if name in source_names or view in view_names:
            raise ValueError(f"Duplicate portable-math source/view: {name}")
        if not view.startswith("docs/math/") or not view.endswith(".md"):
            raise ValueError(f"Unexpected portable math view location: {view}")
        if any(not SHA256.fullmatch(entry[key]) for key in ("source_sha256", "view_sha256")):
            raise ValueError(f"Invalid portable-math digest: {name}")
        source_data = under(root, name).read_bytes()
        if digest(source_data) != entry["source_sha256"]:
            raise ValueError(f"Preserved math source hash mismatch: {name}")
        _preservation(root, entry, origins, cache)
        if not text_issues(source_data.decode("utf-8"), protect=True):
            raise ValueError(f"Unnecessary archive formatting disposition: {name}")
        source_names.add(name)
        view_names.add(view)
    if source_names & view_names:
        raise ValueError("A portable view cannot itself be a preserved source")
    return doc["entries"], origins, namespaces


def verify_views(root: Path, origins: dict[str, str] | None = None) -> dict[str, dict]:
    entries, origins, namespaces = _entries(root, origins)
    verified = {}
    for entry in entries:
        name, view = entry["source_path"], entry["view_path"]
        view_data = under(root, view).read_bytes()
        if digest(view_data) != entry["view_sha256"]:
            raise ValueError(f"Portable math view hash mismatch: {view}")
        expected = view_text(root, name, view, origins, namespaces).encode("utf-8")
        if view_data != expected:
            raise ValueError(f"Portable view differs from its source transformation: {view}")
        problems = text_issues(view_data.decode("utf-8"), protect=True)
        if problems:
            raise ValueError(f"Portable view still violates math formatting: {view}: {problems}")
        verified[name] = entry
    return verified


def generate(root: Path) -> dict:
    """Materialize only registered, scientifically bound views, never sources.

    Source/provenance checks and exact derivation occur before any write. An
    existing differing view is rejected, even when its recorded hash is changed.
    Missing views may be reconstructed; no existing view is overwritten.
    """
    root = root.resolve()
    entries, origins, namespaces = _entries(root)
    pending = []
    for entry in entries:
        source_path, view_path = entry["source_path"], entry["view_path"]
        content = view_text(root, source_path, view_path, origins, namespaces).encode("utf-8")
        if digest(content) != entry["view_sha256"]:
            raise ValueError(f"Registered view identity differs from source transformation: {view_path}")
        problems = text_issues(content.decode("utf-8"), protect=True)
        if problems:
            raise ValueError(f"Transformation needs a real formatting repair: {source_path}: {problems}")
        path = under(root, view_path)
        if path.exists() and path.read_bytes() != content:
            raise ValueError(f"Existing portable view differs; refusing overwrite: {view_path}")
        pending.append((path, content))
    # Validate all planned transformations and conflicts before any file writes.
    for path, content in pending:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(content)
    verified = verify_views(root, origins)
    return dict(status="PASS", preserved_sources=len(verified), portable_views=len(pending),
                source_bytes_changed=0, research_credit_ns=0)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("generate", "verify"))
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    if args.command == "generate":
        result = generate(args.root)
    else:
        result = dict(status="PASS", preserved_sources=len(verify_views(args.root)),
                      source_bytes_changed=0, research_credit_ns=0)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
