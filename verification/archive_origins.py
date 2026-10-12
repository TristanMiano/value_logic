"""Verify the original link namespaces of immutable Markdown copies.

This metadata is a content-bound source-context registry, not a list of links to
ignore. A consumer must still check every referenced destination and fragment.
It does not alter the physical links GitHub renders in the archived copy.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from tools.evidence_paths import relative_path, under


MANIFEST = "tools/document_origins.json"
SCHEMA = "value_logic.document_origins.v1"


@dataclass(frozen=True)
class Namespaces:
    origins: dict[str, str]
    checkout_roots: dict[str, tuple[str, ...]]
    fragment_origins: dict[str, str]
    link_corrections: dict[str, dict[str, str]]


def _digest(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError(f"invalid SHA-256: {value!r}")
    return value


def _at(value: Any, pointer: list[str | int]) -> Any:
    if not isinstance(pointer, list):
        raise ValueError("a provenance pointer must be an array")
    for part in pointer:
        if isinstance(value, list):
            if type(part) is not int or part < 0:
                raise ValueError("invalid array index in provenance pointer")
        elif isinstance(value, dict):
            if not isinstance(part, str):
                raise ValueError("invalid object key in provenance pointer")
        else:
            raise ValueError("provenance pointer enters a scalar")
        try:
            value = value[part]
        except (KeyError, IndexError) as exc:
            raise ValueError(f"missing provenance pointer component: {part!r}") from exc
    return value


def load_namespaces(root: Path) -> Namespaces:
    """Load verified namespaces, failing closed on stale or malformed bindings.

    Absence of the registry supplies no archive exceptions. The caller then
    checks every document in its physical namespace, as for an ordinary repo.
    """
    root = root.resolve()
    manifest_path = root / MANIFEST
    if not manifest_path.exists():
        return Namespaces({}, {}, {}, {})
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA:
        raise ValueError("unsupported document origin schema")
    entries = manifest["entries"]
    if not isinstance(entries, list):
        raise ValueError("document origins must be an array")

    # A large frozen manifest may bind many copies. Read and hash each actual
    # provenance file once in this load, but verify every pointer separately.
    contents: dict[str, tuple[str, bytes]] = {}
    parsed: dict[str, Any] = {}

    def bound_bytes(path: str, expected: str) -> bytes:
        relative_path(path)
        expected = _digest(expected)
        if path not in contents:
            raw = under(root, path).read_bytes()
            contents[path] = hashlib.sha256(raw).hexdigest(), raw
        digest, raw = contents[path]
        if digest != expected:
            raise ValueError(f"content identity mismatch: {path}")
        return raw

    def evidence(item: dict) -> Any:
        path = item["path"]
        raw = bound_bytes(path, item["sha256"])
        if path not in parsed:
            parsed[path] = json.loads(raw)
        return _at(parsed[path], item["pointer"])

    def context_passage(context: dict, stored: str) -> None:
        context_raw = bound_bytes(context["path"], context["sha256"]).decode("utf-8")
        if "pointer" in context:
            context_raw = _at(json.loads(context_raw), context["pointer"])
        passage = context["passage"]
        if (not isinstance(context_raw, str) or not isinstance(passage, str)
                or not passage.strip() or passage not in context_raw):
            raise ValueError(f"source-context passage is unavailable: {stored}")

    origins: dict[str, str] = {}
    fragment_origins: dict[str, str] = {}
    for entry in entries:
        stored, origin = entry["stored_path"], entry["origin_path"]
        relative_path(stored)
        relative_path(origin)
        if stored in origins:
            raise ValueError(f"duplicate document origin: {stored}")
        if stored == origin:
            raise ValueError(f"redundant document origin: {stored}")
        current_digest = _digest(entry["sha256"])
        bound_bytes(stored, current_digest)
        digest = _digest(entry.get("origin_sha256", current_digest))
        if not under(root, origin).is_file():
            raise ValueError(f"original document is unavailable: {origin}")
        receipts = entry["provenance"]
        if not isinstance(receipts, list) or not receipts:
            raise ValueError(f"no origin evidence for {stored}")
        for receipt in receipts:
            record = evidence(receipt)
            kind = receipt["kind"]
            if kind == "mapping-key":
                pointer = receipt["pointer"]
                valid = bool(pointer) and pointer[-1] == origin and record == digest
            elif kind == "mapping-key-record":
                pointer = receipt["pointer"]
                valid = (bool(pointer) and pointer[-1] == origin
                         and isinstance(record, dict) and record.get("sha256") == digest)
            elif kind.startswith("record:"):
                _, path_key, hash_key = kind.split(":")
                valid = (isinstance(record, dict) and record.get(path_key) == origin
                         and record.get(hash_key) == digest)
            elif kind == "fields":
                valid = (_at(record, receipt["origin_pointer"]) == origin
                         and _at(record, receipt["sha256_pointer"]) == digest)
            elif kind == "source-context":
                # Some preserved review artifacts are excerpts, not copies of
                # an entire live file. The original and excerpt identities may
                # be in separate signed records. Their relationship is stated
                # explicitly in the hash-bound review passage below; do not
                # mislabel this as full-file byte equality.
                identity = evidence(receipt["identity"])
                if "origin_key" in receipt:
                    origin_bound = (receipt["origin_key"] == origin
                                    and isinstance(record, dict) and origin in record)
                else:
                    origin_bound = _at(record, receipt["origin_pointer"]) == origin
                valid = origin_bound and identity == digest
                context_passage(receipt["context"], stored)
            elif kind == "captured-source-tree":
                # The signed review describes these named in-progress source
                # copies, and its inventory binds the full stored path and
                # bytes. This is per-file evidence, never a `source/` heuristic.
                prefix = receipt["capture_prefix"]
                relative_path(prefix)
                valid = (bool(receipt["pointer"]) and receipt["pointer"][-1] == stored
                         and stored == f"{prefix}/{origin}"
                         and isinstance(record, dict) and record.get("sha256") == digest)
                context_passage(receipt["context"], stored)
            else:
                raise ValueError(f"unsupported origin evidence kind: {kind}")
            if not valid:
                raise ValueError(f"provenance does not bind source bytes to origin: {stored}")
        for transform in entry.get("transforms", []):
            record = evidence(transform)
            if (not isinstance(record, dict)
                    or record.get("path") != stored
                    or record.get("before_sha256") != digest):
                raise ValueError(f"broken historical document transformation chain: {stored}")
            digest = _digest(record.get("after_sha256"))
        if digest != current_digest:
            raise ValueError(f"historical transformation chain does not reach current bytes: {stored}")
        origins[stored] = origin
        for fragment in entry.get("assembled_fragments", []):
            if (not isinstance(fragment, str) or not fragment or "#" in fragment
                    or not any(r["kind"] == "source-context" for r in receipts)):
                raise ValueError(f"assembled fragment lacks explicit source-context evidence: {stored}")
            fragment_origins[f"{stored}#{fragment}"] = origin

    # Resolve exact-copy chains without assuming that any unregistered nested
    # directory is a checkout. Cycles have no meaningful source namespace.
    resolved: dict[str, str] = {}
    for stored in origins:
        seen = {stored}
        origin = origins[stored]
        while origin in origins:
            if origin in seen:
                raise ValueError(f"cyclic document origins: {stored}")
            seen.add(origin)
            origin = origins[origin]
        resolved[stored] = origin

    checkout_roots: dict[str, tuple[str, ...]] = {}
    for checkout in manifest.get("checkout_roots", []):
        prefix = checkout["prefix"]
        if (not isinstance(prefix, str) or not prefix.startswith("sandbox:/")
                or not prefix.endswith("/") or "\\" in prefix):
            raise ValueError("invalid historical checkout prefix")
        receipt = checkout["provenance"]
        if evidence(receipt) != prefix.removeprefix("sandbox:").rstrip("/"):
            raise ValueError("historical checkout prefix does not match observed cwd")
        for source in checkout["sources"]:
            path = source["path"]
            bound_bytes(path, source["sha256"])
            if prefix in checkout_roots.get(path, ()):
                raise ValueError(f"duplicate historical checkout scope: {path}")
            checkout_roots[path] = (*checkout_roots.get(path, ()), prefix)

    link_corrections: dict[str, dict[str, str]] = {}
    for correction in manifest.get("link_corrections", []):
        source = correction["source"]
        digest = _digest(correction["sha256"])
        bound_bytes(source, digest)
        target, replacement = correction["target"], correction["replacement"]
        if not isinstance(target, str) or not isinstance(replacement, str):
            raise ValueError("a recorded link correction must contain strings")
        old_path, old_separator, old_fragment = target.partition("#")
        new_path, new_separator, new_fragment = replacement.partition("#")
        record = evidence(correction["provenance"])
        # This compatibility is limited to an explicitly recorded anchor-only
        # correction of this exact before-copy. It cannot redirect arbitrary
        # paths, exempt a missing link, or borrow another document's edit.
        if (not old_separator or not new_separator or not old_fragment or not new_fragment
                or old_path != new_path or target == replacement
                or not isinstance(record, dict)
                or record.get("path") != resolved.get(source, source)
                or record.get("before_sha256") != digest
                or record.get("substitutions", {}).get(f"#{old_fragment}") != f"#{new_fragment}"):
            raise ValueError(f"unsupported or mismatched recorded link correction: {source}")
        if target in link_corrections.get(source, {}):
            raise ValueError(f"duplicate recorded link correction: {source}")
        link_corrections.setdefault(source, {})[target] = replacement

    return Namespaces(resolved, checkout_roots, fragment_origins, link_corrections)


def load_origins(root: Path) -> dict[str, str]:
    """Return root-relative stored-path → original-path strings after validation."""
    return load_namespaces(root).origins
