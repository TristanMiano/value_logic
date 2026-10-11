"""Verify, locate, or export historical snapshots relocated for Windows checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys


REPO = Path(__file__).resolve().parents[1]
MANIFEST = "v3/evidence/relocations.v1.json"


def relative_path(value: str) -> PurePosixPath:
    """Accept only a portable, repository-relative path, never a traversal."""
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError(f"Invalid relative path: {value!r}")
    parts = value.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise ValueError(f"Invalid relative path: {value!r}")
    return PurePosixPath(value)


def under(root: Path, relative: str) -> Path:
    path = root.joinpath(*relative_path(relative).parts)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes its root: {relative}")
    return path


def load_entries(repo: Path = REPO) -> list[dict]:
    manifest = json.loads((repo / MANIFEST).read_text(encoding="utf-8"))
    if manifest.get("schema") != "value_logic.evidence_relocations.v1":
        raise ValueError("Unsupported evidence relocation manifest")
    entries = manifest["entries"]
    seen = set()
    for entry in entries:
        original = entry["original_path"]
        relative_path(original)
        if original in seen:
            raise ValueError(f"Duplicate original path: {original}")
        seen.add(original)
        digest = entry["sha256"]
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"Invalid SHA-256 for {original}")
        if entry["stored_path"] != f"v3/evidence/objects/{digest}":
            raise ValueError(f"Unexpected object location for {original}")
        if not re.fullmatch(r"[0-9a-f]{40}", entry["git_blob"]):
            raise ValueError(f"Invalid Git blob ID for {original}")
        if entry["mode"] not in ("100644", "100755"):
            raise ValueError(f"Unsupported file mode for {original}")
        if type(entry["bytes"]) is not int or entry["bytes"] < 0:
            raise ValueError(f"Invalid byte count for {original}")
    if manifest["relocated_paths"] != len(entries):
        raise ValueError("Relocation count does not match entries")
    return entries


def verified_bytes(repo: Path, entry: dict) -> bytes:
    data = under(repo, entry["stored_path"]).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if (len(data), hashlib.sha256(data).hexdigest(), blob) != (
        entry["bytes"], entry["sha256"], entry["git_blob"]
    ):
        raise ValueError(f"Stored evidence does not match its identity: {entry['original_path']}")
    return data


def verify(repo: Path = REPO) -> dict:
    entries = load_entries(repo)
    for entry in entries:
        verified_bytes(repo, entry)
    return {
        "status": "verified",
        "relocated_paths": len(entries),
        "unique_objects": len({e["stored_path"] for e in entries}),
        "original_bytes": sum(e["bytes"] for e in entries),
    }


def resolve(original: str, repo: Path = REPO) -> Path:
    relative_path(original)
    for entry in load_entries(repo):
        if entry["original_path"] == original:
            verified_bytes(repo, entry)
            return under(repo, entry["stored_path"])
    raise ValueError(f"No relocated snapshot has this original path: {original}")


def materialize(destination: Path, repo: Path = REPO) -> dict:
    """Export only relocated entries; refuse conflicting files and the live repo."""
    repo, destination = repo.resolve(), destination.resolve()
    if destination.is_relative_to(repo):
        raise ValueError("Choose a short destination outside the working repository")
    planned = []
    for entry in load_entries(repo):
        data = verified_bytes(repo, entry)
        target = under(destination, entry["original_path"])
        if target.resolve().is_relative_to(repo):
            raise ValueError("Export target would enter the working repository")
        if os.name == "nt" and len(str(target).encode("utf-16-le")) // 2 > 259:
            raise ValueError("Export path is too long; use a shorter destination, e.g. C:\\vl-replay")
        for parent in target.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Destination parent is not a directory: {parent}")
        if target.exists():
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError(f"Existing destination differs; nothing overwritten: {target}")
            planned.append((entry, target, data, False))
        else:
            planned.append((entry, target, data, True))
    targets = {target for _, target, _, _ in planned}
    if any(parent in targets for target in targets for parent in target.parents):
        raise ValueError("Export targets conflict: a file would also be a parent directory")
    # Verify every input and destination before writing any files.
    for entry, target, data, create in planned:
        if create:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as output:
                output.write(data)
            target.chmod(0o755 if entry["mode"] == "100755" else 0o644)
    return {
        "status": "materialized",
        "destination": str(destination),
        "created": sum(create for _, _, _, create in planned),
        "already_identical": sum(not create for _, _, _, create in planned),
        "scope": "relocated snapshots only; no scientific experiment executed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("verify", help="check all stored bytes, SHA-256 and Git blob identities")
    locate = sub.add_parser("resolve", help="print the verified current path of one historical snapshot")
    locate.add_argument("original_path")
    export = sub.add_parser("materialize", help="export relocated files to their original paths outside this repo")
    export.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "verify":
            result = verify()
        elif args.command == "resolve":
            print(resolve(args.original_path))
            return 0
        else:
            result = materialize(args.destination)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Evidence paths: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
