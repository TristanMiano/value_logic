"""Check local Markdown references, including verified historical relocations."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.evidence_paths import MANIFEST, load_entries, resolve as resolve_evidence
from v3.checks.math_markdown import mask_literals, mask_literals_and_math
from verification.archive_origins import MANIFEST as ORIGINS_MANIFEST, load_namespaces


LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "data:", "app://")


@dataclass(frozen=True)
class BrokenLink:
    source: Path
    target: str
    line: int
    detail: str


def github_slug(text: str) -> str:
    """Approximate GitHub's stable heading slug for this repository's headings."""

    text = unescape(re.sub(r"<[^>]+>", "", text)).strip().lower()
    text = LINK.sub(lambda match: match.group(0)[1:match.group(0).index("]")], text)
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    # GitHub replaces each space, rather than collapsing runs. In particular,
    # deleting an em dash in "A — B" leaves two spaces and hence two hyphens.
    return text.replace(" ", "-")


class _HTMLAnchors(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value is not None and (key == "id" or (tag == "a" and key == "name")):
                self.anchors.add(value)


def heading_slugs(path: Path) -> set[str]:
    original = path.read_text(encoding="utf-8")
    text = mask_literals(original, inline=False)
    counts: dict[str, int] = {}
    slugs: set[str] = set()
    for heading in HEADING.findall(text):
        base = github_slug(heading)
        candidate = base
        count = counts.get(base, 0)
        while candidate in slugs:
            count += 1
            candidate = f"{base}-{count}"
        counts[base] = count
        slugs.add(candidate)
    custom = _HTMLAnchors()
    custom.feed(mask_literals_and_math(original))
    return slugs | custom.anchors


def markdown_files(root: Path) -> tuple[Path, ...]:
    return tuple(
        path
        for path in root.rglob("*.md")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    )


def check_links(root: Path) -> list[BrokenLink]:
    root = root.resolve()
    broken: list[BrokenLink] = []
    slug_cache: dict[Path, set[str]] = {}
    try:
        namespaces = load_namespaces(root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [BrokenLink(root / ORIGINS_MANIFEST, "", 1,
                           f"invalid document origin manifest: {exc}")]
    relocations: set[str] = set()
    if (root / MANIFEST).exists():
        try:
            relocations = {entry["original_path"] for entry in load_entries(root)}
        except (OSError, ValueError, KeyError, TypeError) as exc:
            return [BrokenLink(root / MANIFEST, "", 1,
                               f"invalid evidence relocation manifest: {exc}")]
    for source in markdown_files(root):
        text = source.read_text(encoding="utf-8")
        prose = mask_literals_and_math(text)
        relative_source = source.relative_to(root).as_posix()
        logical_source = root / namespaces.origins.get(relative_source, relative_source)
        for match in LINK.finditer(prose):
            before = prose[:match.start()]
            if (len(before)-len(before.rstrip("\\"))) % 2:
                continue
            raw = match.group(1).strip()
            # Markdown permits an optional title after a whitespace separator.
            target = raw.split(maxsplit=1)[0].strip("<>") if raw else ""
            if not target or target.lower().startswith(EXTERNAL_SCHEMES):
                continue
            resolved_target = namespaces.link_corrections.get(relative_source, {}).get(target, target)
            path_part, separator, fragment = resolved_target.partition("#")
            decoded_path = unquote(path_part)
            assembled_origin = namespaces.fragment_origins.get(
                f"{relative_source}#{unquote(fragment)}"
            ) if not decoded_path else None
            historical_root = next((prefix for prefix in namespaces.checkout_roots.get(relative_source, ())
                                    if decoded_path.startswith(prefix)), None)
            if assembled_origin:
                destination = root / assembled_origin
            elif historical_root:
                destination = (root / decoded_path[len(historical_root):]).resolve()
            else:
                # Self-fragments refer to this archived content, while relative
                # paths retain the verified document's original source context.
                destination = source if not decoded_path else (logical_source.parent / decoded_path).resolve()
            logical_suffix = destination.suffix.lower()
            line = text.count("\n", 0, match.start()) + 1
            try:
                destination.relative_to(root)
            except ValueError:
                broken.append(BrokenLink(source, target, line, "target escapes repository"))
                continue
            if not destination.exists():
                original = destination.relative_to(root).as_posix()
                if original not in relocations:
                    broken.append(BrokenLink(source, target, line, "target does not exist"))
                    continue
                try:
                    destination = resolve_evidence(original, repo=root)
                except (OSError, ValueError, KeyError, TypeError) as exc:
                    broken.append(BrokenLink(source, target, line,
                                             f"relocated target cannot be verified: {exc}"))
                    continue
            # Object filenames have no extension; retain the historical target type.
            if separator and fragment and logical_suffix == ".md":
                if destination not in slug_cache:
                    slug_cache[destination] = heading_slugs(destination)
                slugs = slug_cache[destination]
                if unquote(fragment) not in slugs:
                    broken.append(BrokenLink(source, target, line, "heading anchor does not exist"))
    return broken


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    broken = check_links(args.root)
    if broken:
        for item in broken:
            try:
                source = item.source.relative_to(args.root.resolve())
            except ValueError:
                source = item.source
            print(f"{source}:{item.line}: {item.target}: {item.detail}", file=sys.stderr)
        print(f"Found {len(broken)} broken local Markdown link(s).", file=sys.stderr)
        return 1
    print(f"Local Markdown links OK ({len(markdown_files(args.root.resolve()))} files checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
