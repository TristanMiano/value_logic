#!/usr/bin/env python3
"""Check tracked Git paths against the repository's Windows checkout budget."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import ntpath
from pathlib import Path
import subprocess
import sys
from typing import Iterable


RELATIVE_LIMIT = 200
FULL_PATH_LIMIT = 259  # The traditional 260-character limit includes the NUL.


def utf16_units(value: str) -> int:
    """Windows counts UTF-16 code units, not Python Unicode characters."""
    return len(value.encode("utf-16-le", errors="surrogatepass")) // 2


def tracked_paths(repo: Path, ref: str | None = None) -> list[str]:
    """Read the index by default, or a historical Git tree without checking it out."""
    command = ["git", "-C", str(repo)]
    if ref is None:
        command += ["ls-files", "--cached", "-z"]
    else:
        command += ["ls-tree", "-r", "-z", "--name-only", "--full-tree", ref, "--"]
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    return sorted({item.decode("utf-8", errors="surrogateescape")
                   for item in result.stdout.split(b"\0") if item})


def attribute_probes(paths: Iterable[str]) -> set[str]:
    """Include .gitattributes at the root and every tracked file's ancestors."""
    probes: set[str] = set()
    for path in paths:
        parts = path.split("/")
        for depth in range(len(parts)):
            probes.add("/".join(parts[:depth] + [".gitattributes"]))
    return probes


@dataclass(frozen=True)
class PathIssue:
    path: str
    kind: str
    relative_units: int
    full_units: int | None
    relative_overflow: bool
    full_overflow: bool


@dataclass(frozen=True)
class PathAudit:
    tracked_count: int
    probe_count: int
    max_relative_units: int
    max_full_units: int | None
    issues: tuple[PathIssue, ...]


def audit_paths(paths: Iterable[str], *, checkout_root: str | None = None,
                relative_limit: int = RELATIVE_LIMIT,
                full_limit: int = FULL_PATH_LIMIT) -> PathAudit:
    """Check files and virtual attribute lookups, including an optional root."""
    files = set(paths)
    probes = attribute_probes(files)
    candidates = {path: "attributes probe" for path in probes}
    candidates.update({path: "tracked file" for path in files})
    root = (ntpath.normpath(checkout_root).rstrip("\\/") + "\\"
            if checkout_root is not None else None)
    root_units = utf16_units(root) if root is not None else None
    issues = []
    maximum = 0
    for path, kind in sorted(candidates.items()):
        length = utf16_units(path)
        maximum = max(maximum, length)
        full = length + root_units if root_units is not None else None
        relative_overflow = length > relative_limit
        full_overflow = full is not None and full > full_limit
        if relative_overflow or full_overflow:
            issues.append(PathIssue(path, kind, length, full,
                                    relative_overflow, full_overflow))
    return PathAudit(len(files), len(probes), maximum,
                     maximum + root_units if root_units is not None else None,
                     tuple(issues))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path,
                        default=Path(__file__).resolve().parents[1],
                        help="repository to inspect (default: this repository)")
    parser.add_argument("--ref", help="inspect this Git revision/tree instead of the index")
    parser.add_argument("--checkout-root",
                        help=r"also check the full Windows path, e.g. C:\Users\trist\projects\value_logic")
    args = parser.parse_args(argv)
    if args.checkout_root is not None and not ntpath.isabs(args.checkout_root):
        parser.error("--checkout-root must be an absolute checkout directory")
    try:
        paths = tracked_paths(args.repo, args.ref)
    except subprocess.CalledProcessError as exc:
        print("Git path lookup failed: " + exc.stderr.decode("utf-8", errors="replace").strip(),
              file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Git path lookup failed: {exc}", file=sys.stderr)
        return 2
    audit = audit_paths(paths, checkout_root=args.checkout_root)
    status = "FAIL" if audit.issues else "PASS"
    print(f"{status}: {audit.tracked_count} tracked files; {audit.probe_count} attribute probes; "
          f"longest relative path {audit.max_relative_units}/{RELATIVE_LIMIT} UTF-16 units.")
    if audit.max_full_units is not None:
        print(f"Longest full Windows path: {audit.max_full_units}/{FULL_PATH_LIMIT} UTF-16 units.")
    for issue in audit.issues[:20]:
        limits = []
        if issue.relative_overflow:
            limits.append(f"relative {issue.relative_units}>{RELATIVE_LIMIT}")
        if issue.full_overflow:
            limits.append(f"full {issue.full_units}>{FULL_PATH_LIMIT}")
        print(f"  {issue.kind}: {', '.join(limits)}: {issue.path}")
    if len(audit.issues) > 20:
        print(f"  ... {len(audit.issues) - 20} additional incompatible paths.")
    return 1 if audit.issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
