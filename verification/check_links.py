"""Check local Markdown references, including verified historical relocations."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from urllib.parse import unquote

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.evidence_paths import MANIFEST, load_entries, resolve as resolve_evidence


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

    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return re.sub(r"[ ]+", "-", text)


def heading_slugs(path: Path) -> set[str]:
    counts: dict[str, int] = {}
    slugs: set[str] = set()
    for heading in HEADING.findall(path.read_text(encoding="utf-8")):
        base = github_slug(heading)
        count = counts.get(base, 0)
        counts[base] = count + 1
        slugs.add(base if count == 0 else f"{base}-{count}")
    return slugs


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
    relocations: set[str] = set()
    if (root / MANIFEST).exists():
        try:
            relocations = {entry["original_path"] for entry in load_entries(root)}
        except (OSError, ValueError, KeyError, TypeError) as exc:
            return [BrokenLink(root / MANIFEST, "", 1,
                               f"invalid evidence relocation manifest: {exc}")]
    for source in markdown_files(root):
        text = source.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            raw = match.group(1).strip()
            # Markdown permits an optional title after a whitespace separator.
            target = raw.split(maxsplit=1)[0].strip("<>")
            if not target or target.lower().startswith(EXTERNAL_SCHEMES):
                continue
            path_part, separator, fragment = target.partition("#")
            decoded_path = unquote(path_part)
            destination = source if not decoded_path else (source.parent / decoded_path).resolve()
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
                slugs = slug_cache.setdefault(destination, heading_slugs(destination))
                if unquote(fragment).lower() not in slugs:
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
