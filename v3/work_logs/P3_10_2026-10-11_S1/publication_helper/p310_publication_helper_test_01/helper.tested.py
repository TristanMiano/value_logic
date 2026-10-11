#!/usr/bin/env python3
"""P3-10 exact-byte publication preparation, with no network or Git-data writes.

Creates fresh plans outside the checkout only when `prepare` is explicitly run.
Other commands audit a plan, retain actual tool results, report resumable progress,
or reconstruct a remote commit payload without installing it. No command here
moves a ref, writes an index/object, invokes a paid method, or publishes anything.

Contributor: ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction.
Publication preparation contributes zero principal research/engagement credit.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import traceback

DEFAULT_REPO = "/workspace/scratch/095cdac579b7/value_logic"
DEFAULT_BASE = "ea3e20dd9889c2ee22141c17390595867d33d8ab"
DEFAULT_REMOTE = "TristanMiano/value_logic"
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
MODES = {"100644", "100755", "120000"}
SCHEMA = "value_logic.p310.publication_plan.v1"


def utc():
    return datetime.now(timezone.utc).isoformat()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_id(kind, data):
    require(kind in {"blob", "tree", "commit"}, "Unsupported Git object type")
    return hashlib.sha1(kind.encode("ascii") + b" " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def payload_bytes(obj):
    # No universal-newline conversion, Unicode normalization, or appended LF.
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def fsync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_new(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    fsync_dir(path.parent)


def write_json(path, obj):
    write_new(path, (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


def outside_checkout(path, repo):
    path, repo = Path(path).resolve(), Path(repo).resolve()
    require(path != repo and not path.is_relative_to(repo), "Output must be outside the checkout")
    return path


def safe_path(name):
    require(isinstance(name, str) and name and not name.startswith("/"), "Invalid repository path")
    name.encode("utf-8", "strict")
    require("\0" not in name, "NUL in repository path")
    parts = name.split("/")
    require(all(x not in {"", ".", "..", ".git"} for x in parts), "Unsafe repository path: " + repr(name))
    return name


def file_record(path):
    b = Path(path).read_bytes()
    return {"bytes": len(b), "sha256": sha256(b)}


class GitReader:
    """A fixed read-only command surface; -w/--write is never accepted."""

    def __init__(self, repo):
        self.repo = Path(repo).resolve()

    def run(self, command, *args, data=None):
        require(command in {"rev-parse", "ls-tree", "ls-files", "cat-file", "hash-object"}, "Git mutation command prohibited")
        require("-w" not in args and "--write" not in args, "Git object writes prohibited")
        env = os.environ.copy()
        for key in ["GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE"]:
            env.pop(key, None)
        env["GIT_OPTIONAL_LOCKS"] = "0"
        argv = ["git", "--no-optional-locks", "--literal-pathspecs", "-c", "core.fsmonitor=false", "-C", str(self.repo), command, *args]
        result = subprocess.run(argv, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
        require(result.returncode == 0, "Read-only Git command failed: " + repr(argv) + ": " + result.stderr.decode("utf-8", "replace"))
        return result.stdout

    def baseline(self, commit):
        require(SHA_RE.fullmatch(commit), "Baseline must be a full SHA-1 commit ID")
        require(self.run("rev-parse", "--show-object-format").strip() == b"sha1", "Only the repository's SHA-1 Git format is supported")
        require(Path(os.fsdecode(self.run("rev-parse", "--show-toplevel").strip())).resolve() == self.repo, "Git worktree resolves elsewhere")
        tree = self.run("rev-parse", "--verify", commit + "^{tree}").decode("ascii").strip()
        entries = {}
        for row in self.run("ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
            if not row:
                continue
            metadata, raw_name = row.split(b"\t", 1)
            mode, kind, identity = metadata.decode("ascii").split()
            name = safe_path(raw_name.decode("utf-8", "strict"))
            require(kind == "blob" and mode in MODES, "Unsupported gitlink or mode in baseline: " + name)
            require(name not in entries, "Duplicate baseline path")
            entries[name] = {"mode": mode, "type": kind, "sha": identity}
        rebuilt, _ = make_tree(entries)
        require(rebuilt == tree, "Baseline tree reconstruction mismatch (empty trees or unsupported path structure may be present)")
        return tree, entries

    def head(self):
        return self.run("rev-parse", "--verify", "HEAD").decode("ascii").strip()

    def paths(self):
        require(not self.run("ls-files", "--unmerged", "-z"), "Unmerged index entries need explicit resolution before preparation")
        data = self.run("ls-files", "--cached", "--others", "--exclude-standard", "-z")
        return {safe_path(x.decode("utf-8", "strict")) for x in data.split(b"\0") if x}

    def index_identity(self):
        name = Path(os.fsdecode(self.run("rev-parse", "--git-path", "index").strip()))
        if not name.is_absolute():
            name = self.repo / name
        return file_record(name) if name.exists() else None


def make_tree(flat):
    """Return a Git tree ID and exact root body without writing any Git object."""
    root = {}
    for path, entry in flat.items():
        safe_path(path)
        require(entry["mode"] in MODES and entry["type"] == "blob" and SHA_RE.fullmatch(entry["sha"]), "Invalid flat-tree entry")
        node = root
        parts = path.split("/")
        for part in parts[:-1]:
            require(part not in node or isinstance(node[part], dict), "File/directory conflict: " + path)
            node = node.setdefault(part, {})
        require(parts[-1] not in node, "Duplicate or directory/file conflict: " + path)
        node[parts[-1]] = (entry["mode"], entry["sha"])

    def fold(node):
        encoded = []
        for name, value in node.items():
            raw_name = name.encode("utf-8")
            if isinstance(value, dict):
                child_id, _ = fold(value)
                encoded.append((raw_name + b"/", b"40000 " + raw_name + b"\0" + bytes.fromhex(child_id)))
            else:
                mode, identity = value
                encoded.append((raw_name + b"\0", mode.encode("ascii") + b" " + raw_name + b"\0" + bytes.fromhex(identity)))
        body = b"".join(value for _, value in sorted(encoded))
        return git_id("tree", body), body

    return fold(root)


def signature(path):
    try:
        s = path.lstat()
    except FileNotFoundError:
        return None
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def read_node(repo, name):
    path = repo / safe_path(name)
    for ancestor in path.parents:
        if ancestor == repo:
            break
        require(not ancestor.is_symlink(), "Refusing to traverse a symlink parent: " + name)
    before = signature(path)
    if before is None:
        return None, None, before
    mode = before[2]
    if stat.S_ISDIR(mode):
        return None, None, before
    if stat.S_ISLNK(mode):
        data = os.readlink(os.fsencode(path))
        git_mode = "120000"
    else:
        require(stat.S_ISREG(mode), "Unsupported special filesystem object: " + name)
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            with os.fdopen(fd, "rb") as stream:
                require(signature(path) == before, "File changed before read: " + name)
                data = stream.read()
        except BaseException:
            # fdopen owns fd once constructed.
            raise
        git_mode = "100755" if mode & stat.S_IXUSR else "100644"
    require(signature(path) == before, "File changed during read: " + name)
    return git_mode, data, before


def inventory_worktree(reader, baseline, out, allow_deletions=False):
    repo = reader.repo
    first_paths = reader.paths()
    paths = sorted(first_paths | set(baseline), key=lambda p: p.encode("utf-8"))
    stamps, changes, blobs = {}, [], {}
    known_base = {v["sha"] for v in baseline.values()}
    checked_reuse = {}
    for name in paths:
        mode, data, stamp = read_node(repo, name)
        stamps[name] = stamp
        old = baseline.get(name)
        if data is None:
            require(old is not None, "Untracked path disappeared during inventory: " + name)
            require(allow_deletions, "Deletion requires --allow-deletions: " + name)
            changes.append({"path": name, "action": "delete", "mode": old["mode"], "type": "blob", "sha": None, "bytes": 0, "sha256": None, "baseline": old})
            continue
        identity = git_id("blob", data)
        if old and old["sha"] == identity and old["mode"] == mode:
            continue
        content_hash = sha256(data)
        if identity in blobs:
            require(blobs[identity]["sha256"] == content_hash and blobs[identity]["bytes"] == len(data), "Git ID collision with different exact bytes")
        else:
            known = identity in known_base
            if known:
                base_data = reader.run("cat-file", "blob", identity)
                require(base_data == data, "Baseline Git-ID reuse does not preserve exact bytes")
                checked_reuse[identity] = sha256(base_data)
            raw_path = "blobs/" + identity
            write_new(out / raw_path, data)
            blobs[identity] = {"sha": identity, "sha256": content_hash, "bytes": len(data), "snapshot": raw_path, "known_in_base": known, "paths": []}
        blobs[identity]["paths"].append(name)
        changes.append({"path": name, "action": "modify" if old else "add", "mode": mode, "type": "blob", "sha": identity, "bytes": len(data), "sha256": content_hash, "baseline": old})
    require(reader.paths() == first_paths, "Git-reported path roster changed during inventory")
    for name, stamp in stamps.items():
        require(signature(repo / name) == stamp, "File changed during inventory window: " + name)
    # All deletions precede all additions, so file/directory replacements can be
    # represented across dependent API overlay batches without prefix conflicts.
    changes.sort(key=lambda r: (r["action"] != "delete", -r["path"].count("/") if r["action"] == "delete" else 0, r["path"].encode("utf-8")))
    return changes, blobs, {"paths": first_paths, "stamps": stamps, "checked_base_reuse": checked_reuse}


def content_tree_id(elements):
    flat = {}
    for e in elements:
        require(e.get("type") == "blob" and e.get("mode") == "100644", "Unexpected content-upload tree entry")
        identity = git_id("blob", e["content"].encode("utf-8"))
        require(e["path"] == identity, "Content-addressed upload path differs from blob ID")
        require(identity not in flat, "Duplicate content-upload tree entry")
        flat[identity] = {"type": "blob", "mode": "100644", "sha": identity}
    return make_tree(flat)[0]


def prepare_batches(out, repository, baseline_tree, baseline, changes, blobs, cap_bytes, entry_cap, overlay_cap):
    require(cap_bytes >= 512 and 1 <= entry_cap <= 128 and 1 <= overlay_cap <= 128, "Invalid batch limits")
    upload_index, overlay_index = [], []
    batch = []
    size = len(payload_bytes({"repository_full_name": repository, "tree_elements": []}))
    empty_size = size

    def emit_upload(kind, payload, expected, identities, reason):
        body = payload_bytes(payload)
        index = len(upload_index)
        name = "upload_batches/" + f"{index:04d}.json"
        write_new(out / name, body)
        upload_index.append({"index": index, "kind": kind, "path": name, "expected_sha": expected, "blob_shas": identities, "blob_count": len(identities), "request_bytes": len(body), "request_sha256": sha256(body), "reason": reason, "exceeds_inline_cap": len(body) > cap_bytes})

    def flush():
        nonlocal batch, size
        if batch:
            payload = {"repository_full_name": repository, "tree_elements": batch}
            require(len(payload_bytes(payload)) == size and size <= cap_bytes, "Inline sizing inconsistency")
            emit_upload("tree", payload, content_tree_id(batch), [e["path"] for e in batch], "exact UTF-8 content")
            batch, size = [], empty_size

    for identity in sorted(blobs):
        row = blobs[identity]
        if row["known_in_base"]:
            continue
        data = (out / row["snapshot"]).read_bytes()
        require(git_id("blob", data) == identity and sha256(data) == row["sha256"], "Snapshot differs before batching")
        png = data.startswith(b"\x89PNG\r\n\x1a\n") or any(p.lower().endswith(".png") for p in row["paths"])
        try:
            value = data.decode("utf-8", "strict")
            require(value.encode("utf-8") == data, "UTF-8 round-trip mismatch")
        except UnicodeDecodeError:
            value = None
        binary = png or b"\0" in data or value is None
        entry = None if binary else {"path": identity, "mode": "100644", "type": "blob", "content": value}
        entry_size = None if entry is None else len(payload_bytes(entry))
        oversized = entry_size is not None and empty_size + entry_size > cap_bytes
        if binary or oversized:
            flush()
            payload = {"repository_full_name": repository, "content": base64.b64encode(data).decode("ascii"), "encoding": "base64"}
            emit_upload("blob", payload, identity, [identity], "PNG/binary exact bytes" if binary else "oversized UTF-8 blob, exact base64")
        else:
            added = entry_size + (1 if batch else 0)
            if batch and (size + added > cap_bytes or len(batch) == entry_cap):
                flush()
                added = entry_size
            batch.append(entry)
            size += added
    flush()

    current = dict(baseline)
    previous = baseline_tree
    for first in range(0, len(changes), overlay_cap):
        rows = changes[first:first + overlay_cap]
        elements = []
        for row in rows:
            name = row["path"]
            elements.append({"path": name, "mode": row["mode"], "type": "blob", "sha": row["sha"]})
            if row["sha"] is None:
                require(name in current, "Deleting absent base path")
                del current[name]
            else:
                current[name] = {"mode": row["mode"], "type": "blob", "sha": row["sha"]}
        expected, _ = make_tree(current)
        payload = {"repository_full_name": repository, "base_tree_sha": previous, "tree_elements": elements}
        body = payload_bytes(payload)
        index = len(overlay_index)
        name = "overlay_batches/" + f"{index:04d}.json"
        write_new(out / name, body)
        overlay_index.append({"index": index, "kind": "tree", "path": name, "base_tree": previous, "expected_sha": expected, "paths": len(elements), "request_bytes": len(body), "request_sha256": sha256(body)})
        previous = expected
    patch = b"".join(((r["mode"] + " " + r["sha"]) if r["sha"] else ("0 " + "0" * 40)).encode("ascii") + b"\t" + r["path"].encode("utf-8") + b"\0" for r in changes)
    write_new(out / "index_updates.z", patch)
    write_json(out / "upload_index.json", upload_index)
    write_json(out / "overlay_index.json", overlay_index)
    return upload_index, overlay_index, previous, len(current)


def prepare(args):
    reader = GitReader(args.repo)
    out = outside_checkout(args.out, reader.repo)
    out.mkdir(parents=True, exist_ok=False)
    helper = Path(__file__).read_bytes()
    write_new(out / "helper.reviewed.py", helper)
    write_json(out / "start.json", {"started_utc": utc(), "scope": "local publication preparation only", "repo": str(reader.repo), "base_commit": args.base, "helper_sha256": sha256(helper), "research_credit_ns": 0, "network_calls": 0, "git_data_writes": 0})
    try:
        require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repository), "Invalid repository_full_name")
        head, index_before = reader.head(), reader.index_identity()
        require(head == args.base, "Local HEAD differs from the intended baseline; inspect before preparing a new plan")
        tree, baseline = reader.baseline(args.base)
        write_json(out / "baseline_paths.json", [{"path": p, **e} for p, e in sorted(baseline.items())])
        changes, blobs, window = inventory_worktree(reader, baseline, out, args.allow_deletions)
        write_json(out / "inventory.json", changes)
        write_json(out / "blob_index.json", [blobs[k] for k in sorted(blobs)])
        uploads, overlays, final_tree, final_paths = prepare_batches(out, args.repository, tree, baseline, changes, blobs, args.cap_bytes, args.entry_cap, args.overlay_cap)
        require(reader.head() == head and reader.index_identity() == index_before, "HEAD/index changed during preparation")
        require(reader.paths() == window["paths"], "Path roster changed during batching")
        for name, stamp in window["stamps"].items():
            require(signature(reader.repo / name) == stamp, "Working file changed during batching: " + name)
        core = {"repository_full_name": args.repository, "base_commit": args.base, "base_tree": tree, "final_tree": final_tree, "inventory_sha256": file_record(out / "inventory.json")["sha256"], "upload_index_sha256": file_record(out / "upload_index.json")["sha256"], "overlay_index_sha256": file_record(out / "overlay_index.json")["sha256"]}
        artifacts = []
        for path in sorted(out.rglob("*")):
            if path.is_file():
                artifacts.append({"path": str(path.relative_to(out)), **file_record(path)})
        plan = {"schema": SCHEMA, "plan_id": sha256(canonical(core)), "status": "PREPARED_NOT_PUBLISHED", "prepared_utc": utc(), "repo": str(reader.repo), **core, "helper_sha256": sha256(helper), "baseline_paths": len(baseline), "final_paths": final_paths, "changed_paths": len(changes), "deleted_paths": sum(r["sha"] is None for r in changes), "changed_logical_bytes": sum(r["bytes"] for r in changes), "distinct_changed_blobs": len(blobs), "baseline_reused_blobs": sum(r["known_in_base"] for r in blobs.values()), "new_distinct_blobs": sum(not r["known_in_base"] for r in blobs.values()), "new_distinct_bytes": sum(r["bytes"] for r in blobs.values() if not r["known_in_base"]), "upload_requests": len(uploads), "overlay_requests": len(overlays), "inline_request_byte_cap": args.cap_bytes, "inline_entry_cap": args.entry_cap, "overlay_entry_cap": args.overlay_cap, "largest_request_bytes": max([r["request_bytes"] for r in uploads + overlays], default=0), "individual_requests_over_inline_cap": [r for r in uploads if r["exceeds_inline_cap"]], "index_identity_before_and_after": index_before, "allow_deletions": args.allow_deletions, "artifacts": artifacts, "assumptions": ["Only Git-listed tracked and nonignored untracked paths are included; no ignore rules are changed.", "Individual file reads and ending stat/roster checks are stable observations, not a global filesystem lock.", "Root must finish accounting before prepare and verify --working-tree before publication.", "Base64 preserves bytes but expands large requests; no remote size/rate/authentication claim is made.", "Published files/trees retain exact bytes and modes; commit/ref operations are separate."], "network_calls": 0, "git_data_writes": 0, "principal_research_credit_ns": 0}
        write_json(out / "plan.json", plan)
        write_new(out / "plan.sha256", (file_record(out / "plan.json")["sha256"] + "\n").encode("ascii"))
        print(json.dumps({k: plan[k] for k in ["status", "plan_id", "changed_paths", "new_distinct_blobs", "new_distinct_bytes", "upload_requests", "overlay_requests", "largest_request_bytes", "final_tree"]}))
    except BaseException as error:
        write_json(out / "failure.json", {"recorded_utc": utc(), "type": type(error).__name__, "message": str(error), "traceback": traceback.format_exc(), "scope": "local preparation; nothing uploaded or written to Git"})
        raise


def load_plan(path):
    root = Path(path).resolve()
    data = (root / "plan.json").read_bytes()
    require(sha256(data) == (root / "plan.sha256").read_text().strip(), "Plan seal mismatch")
    plan = json.loads(data)
    require(plan["schema"] == SCHEMA, "Unexpected plan schema")
    outside_checkout(root, plan["repo"])
    indexes = {}
    for phase, name in [("upload", "upload_index.json"), ("overlay", "overlay_index.json")]:
        raw = (root / name).read_bytes()
        require(sha256(raw) == plan[phase + "_index_sha256"], "Request index binding mismatch")
        indexes[phase] = json.loads(raw)
    return root, plan, indexes


def wrapper_nodes(value, depth=0):
    """Unwrap known MCP/API envelopes; never collect nested tree/parent SHAs."""
    if depth > 14:
        return
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except (ValueError, TypeError):
            return
        yield from wrapper_nodes(decoded, depth + 1)
    elif isinstance(value, dict):
        yield value
        for key in ["response", "structuredContent", "result", "data", "body"]:
            if key in value:
                yield from wrapper_nodes(value[key], depth + 1)
        content = value.get("content")
        if isinstance(content, str):
            yield from wrapper_nodes(content, depth + 1)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    yield from wrapper_nodes(block.get("text", ""), depth + 1)


def response_identity(raw):
    try:
        obj = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        return None, "Tool result was not JSON"
    nodes = list(wrapper_nodes(obj))
    error = any(n.get("isError") is True or n.get("error") or n.get("errors") or (isinstance(n.get("status"), str) and n["status"] in {"error", "failed", "failure"}) or (isinstance(n.get("status_code"), int) and n["status_code"] >= 400) for n in nodes)
    identities = {n["sha"] for n in nodes if isinstance(n.get("sha"), str) and SHA_RE.fullmatch(n["sha"])}
    if error:
        return None, "Tool/API error flag present"
    if len(identities) != 1:
        return None, "Expected exactly one unambiguous top-level response SHA; observed " + str(len(identities))
    return identities.pop(), None


def receipt_progress(root, plan, indexes):
    verified = {"upload": set(), "overlay": set()}
    for phase in verified:
        for row in indexes[phase]:
            directory = root / "receipts" / phase / f"{row['index']:04d}"
            if not directory.exists():
                continue
            for metadata_path in sorted(directory.glob("attempt_*/receipt.json")):
                metadata = json.loads(metadata_path.read_bytes())
                if not metadata.get("verified"):
                    continue
                require(metadata["plan_id"] == plan["plan_id"] and metadata["request_sha256"] == row["request_sha256"] and metadata["expected_sha"] == row["expected_sha"], "Receipt scope mismatch")
                raw = (metadata_path.parent / "tool_result.json").read_bytes()
                require(sha256(raw) == metadata["tool_result_sha256"], "Saved raw tool result changed")
                observed, error = response_identity(raw)
                require(error is None and observed == row["expected_sha"], "Verified receipt no longer reproduces")
                verified[phase].add(row["index"])
    for index in sorted(verified["overlay"]):
        require(len(verified["upload"]) == len(indexes["upload"]) and all(i in verified["overlay"] for i in range(index)), "Overlay receipt lacks verified upload/predecessor dependencies")
    return verified


def record(args):
    root, plan, indexes = load_plan(args.plan)
    require(0 <= args.index < len(indexes[args.phase]), "Request index out of range")
    row = indexes[args.phase][args.index]
    request = (root / row["path"]).read_bytes()
    require(sha256(request) == row["request_sha256"], "Request bytes changed")
    directory = root / "receipts" / args.phase / f"{args.index:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    count = 1
    while True:
        attempt = directory / f"attempt_{count:04d}"
        try:
            attempt.mkdir()
            break
        except FileExistsError:
            count += 1
    raw = sys.stdin.buffer.read() if args.result == "-" else Path(args.result).read_bytes()
    write_new(attempt / "tool_result.json", raw)
    observed, error = response_identity(raw)
    progress = receipt_progress(root, plan, indexes)
    dependencies = args.phase == "upload" or (len(progress["upload"]) == len(indexes["upload"]) and all(i in progress["overlay"] for i in range(args.index)))
    if not dependencies:
        error = "Overlay result retained, but upload/predecessor receipts are not yet all verified; record this same result again after completing the receipt chain"
    if error is None and observed != row["expected_sha"]:
        error = "Returned SHA differs from the independently computed request identity"
    metadata = {"schema": "value_logic.p310.publication_receipt.v1", "recorded_utc": utc(), "plan_id": plan["plan_id"], "phase": args.phase, "index": args.index, "attempt": count, "request_sha256": row["request_sha256"], "expected_sha": row["expected_sha"], "returned_sha": observed, "tool_result_sha256": sha256(raw), "dependencies_verified": dependencies, "verified": error is None, "error": error, "network_call_made_by_helper": False}
    write_json(attempt / "receipt.json", metadata)
    print(json.dumps({"verified": metadata["verified"], "receipt": str(attempt / "receipt.json"), "returned_sha": observed, "error": error}))
    return 0 if metadata["verified"] else 2


def status_report(args):
    require(args.limit >= 1, "Status limit must be positive")
    root, plan, indexes = load_plan(args.plan)
    done = receipt_progress(root, plan, indexes)
    pending = {p: [r for r in indexes[p] if r["index"] not in done[p]] for p in indexes}
    phase = "upload" if pending["upload"] else ("overlay" if pending["overlay"] else None)
    next_rows = pending[phase][:(args.limit if phase == "upload" else 1)] if phase else []
    result = {"plan_id": plan["plan_id"], "status": "UPLOAD_AND_OVERLAY_RECEIPTS_COMPLETE" if phase is None else "PENDING", "verified": {p: len(v) for p, v in done.items()}, "total": {p: len(v) for p, v in indexes.items()}, "next_phase": phase, "next": [{**r, "absolute_path": str(root / r["path"])} for r in next_rows], "publication_or_ref_verified": False}
    if args.out:
        write_json(outside_checkout(args.out, plan["repo"]), result)
    print(json.dumps(result))


def verify(args):
    root, plan, indexes = load_plan(args.plan)
    for row in plan["artifacts"]:
        require(file_record(root / row["path"]) == {"bytes": row["bytes"], "sha256": row["sha256"]}, "Plan artifact changed: " + row["path"])
    base = {r["path"]: {k: r[k] for k in ["mode", "type", "sha"]} for r in json.loads((root / "baseline_paths.json").read_bytes())}
    require(make_tree(base)[0] == plan["base_tree"], "Baseline tree mismatch")
    inventory = json.loads((root / "inventory.json").read_bytes())
    blobs = {r["sha"]: r for r in json.loads((root / "blob_index.json").read_bytes())}
    covered = []
    for row in indexes["upload"]:
        payload = json.loads((root / row["path"]).read_bytes())
        require(payload["repository_full_name"] == plan["repository_full_name"], "Request repository mismatch")
        if row["kind"] == "tree":
            require("base_tree_sha" not in payload, "Temporary content tree must not use a repository base tree")
            expected = content_tree_id(payload["tree_elements"])
            ids = [e["path"] for e in payload["tree_elements"]]
            for e in payload["tree_elements"]:
                require(e["content"].encode("utf-8") == (root / blobs[e["path"]]["snapshot"]).read_bytes(), "UTF-8 payload changed bytes")
            require(row["request_bytes"] <= plan["inline_request_byte_cap"], "Inline cap exceeded")
        else:
            require(payload["encoding"] == "base64", "Individual binary/large blob is not base64")
            raw = base64.b64decode(payload["content"], validate=True)
            expected = git_id("blob", raw)
            ids = [expected]
            require(raw == (root / blobs[expected]["snapshot"]).read_bytes(), "Base64 payload changed bytes")
        require(expected == row["expected_sha"] and ids == row["blob_shas"], "Upload identity mismatch")
        covered.extend(ids)
    require(len(covered) == len(set(covered)) and set(covered) == {s for s, r in blobs.items() if not r["known_in_base"]}, "New-blob upload coverage mismatch")
    current, previous, represented = dict(base), plan["base_tree"], []
    for row in indexes["overlay"]:
        payload = json.loads((root / row["path"]).read_bytes())
        require(payload["repository_full_name"] == plan["repository_full_name"] and payload["base_tree_sha"] == previous == row["base_tree"], "Overlay chain mismatch")
        for element in payload["tree_elements"]:
            require("content" not in element, "Repository overlay must use only SHAs")
            represented.append(element)
            if element["sha"] is None:
                require(element["path"] in current, "Overlay deletes an absent path")
                del current[element["path"]]
            else:
                current[element["path"]] = {k: element[k] for k in ["mode", "type", "sha"]}
        previous = make_tree(current)[0]
        require(previous == row["expected_sha"], "Overlay tree ID mismatch")
    require(represented == [{k: r[k] for k in ["path", "mode", "type", "sha"]} for r in inventory], "Overlay paths differ from inventory")
    require(previous == plan["final_tree"] and len(current) == plan["final_paths"], "Final tree mismatch")
    if args.working_tree:
        reader = GitReader(plan["repo"])
        require(reader.head() == plan["base_commit"], "HEAD advanced; review the new base before publication")
        path_roster = reader.paths()
        require(path_roster | set(base) == set(base) | set(current), "Working-tree path roster differs from prepared plan")
        index_before = reader.index_identity()
        stamps = {}
        for name in sorted(set(base) | set(current)):
            mode, data, stamp = read_node(reader.repo, name)
            stamps[name] = stamp
            if name not in current:
                require(data is None, "Deleted path reappeared: " + name)
            else:
                require(data is not None and mode == current[name]["mode"] and git_id("blob", data) == current[name]["sha"], "Working-tree bytes/mode differ: " + name)
                if current[name]["sha"] in blobs:
                    require(sha256(data) == blobs[current[name]["sha"]]["sha256"], "Working-tree SHA-256 differs: " + name)
        require(reader.index_identity() == index_before and reader.head() == plan["base_commit"], "HEAD/index changed during verification")
        require(reader.paths() == path_roster, "Path roster changed during verification")
        for name, stamp in stamps.items():
            require(signature(reader.repo / name) == stamp, "File changed during verification window: " + name)
    print(json.dumps({"status": "VERIFIED_LOCAL_PLAN", "plan_id": plan["plan_id"], "final_tree": previous, "working_tree_checked": args.working_tree, "remote_or_publication_checked": False}))


def remote_commit_payload(raw_response):
    nodes = [n for n in wrapper_nodes(json.loads(raw_response)) if isinstance(n.get("sha"), str) and isinstance(n.get("tree"), dict) and isinstance(n.get("author"), dict) and isinstance(n.get("committer"), dict) and isinstance(n.get("parents"), list) and isinstance(n.get("message"), str)]
    unique = {canonical(n): n for n in nodes}
    require(len(unique) == 1, "Expected one unambiguous Git-commit API object")
    commit = next(iter(unique.values()))
    require(SHA_RE.fullmatch(commit["sha"]), "Invalid remote commit ID")
    verification = commit.get("verification") or {}
    require(not verification.get("signature"), "Signed/extra-header commits require an independently obtained exact raw commit; do not guess or drop signatures")

    def person(label):
        p = commit[label]
        require(all(x not in p["name"] + p["email"] for x in ["\n", "\r", "\0"]), "Multiline commit identity unsupported")
        date = datetime.fromisoformat(p["date"].replace("Z", "+00:00"))
        require(date.tzinfo is not None and date.microsecond == 0, "Commit identity requires integral seconds and an explicit timezone")
        return label + " " + p["name"] + " <" + p["email"] + "> " + str(int(date.timestamp())) + " " + date.strftime("%z")

    tree = commit["tree"]["sha"]
    parents = [p["sha"] for p in commit["parents"]]
    require(SHA_RE.fullmatch(tree) and all(SHA_RE.fullmatch(p) for p in parents), "Invalid tree/parent identity")
    header = "\n".join(["tree " + tree, *["parent " + p for p in parents], person("author"), person("committer")]) + "\n\n"
    exact = (header + commit["message"]).encode("utf-8")
    candidates = [exact, exact + b"\n"]
    if isinstance(verification.get("payload"), str):
        candidates.append(verification["payload"].encode("utf-8"))
    matches = {candidate for candidate in candidates if git_id("commit", candidate) == commit["sha"]}
    require(len(matches) == 1, "Author/date/message fields do not reproduce the remote commit; exact original timezone, encoding, headers or terminal bytes may be missing")
    return commit, matches.pop()


def commit_payload(args):
    root, plan, _ = load_plan(args.plan)
    out = outside_checkout(args.out, plan["repo"])
    out.mkdir(parents=True, exist_ok=False)
    raw_response = Path(args.response).read_bytes()
    write_new(out / "remote_response.json", raw_response)
    try:
        commit, raw = remote_commit_payload(raw_response)
        require(commit["tree"]["sha"] == plan["final_tree"] and [p["sha"] for p in commit["parents"]] == [plan["base_commit"]], "Remote commit does not have the intended tree and sole baseline parent")
        write_new(out / "commit.raw", raw)
        write_json(out / "identity.json", {"remote_commit": commit["sha"], "tree": commit["tree"]["sha"], "parents": [p["sha"] for p in commit["parents"]], "commit_raw_sha256": sha256(raw), "remote_response_sha256": sha256(raw_response), "reconstructed_utc": utc(), "plan_id": plan["plan_id"], "installed_locally": False, "ref_updated": False})
        # These are instructions for a later authorized phase, never executed here.
        blobs = json.loads((root / "blob_index.json").read_bytes())
        git = ["git", "-C", plan["repo"]]
        temporary_index = str(out / "temporary.index")
        commands = [{"argv": git + ["hash-object", "-w", "--no-filters", "--stdin"], "stdin_file": str(root / r["snapshot"]), "expected_stdout": r["sha"]} for r in blobs if not r["known_in_base"]]
        commands += [
            {"argv": git + ["read-tree", plan["base_tree"]], "env": {"GIT_INDEX_FILE": temporary_index}, "requires_index_path_initially_absent": True},
            {"argv": git + ["update-index", "-z", "--index-info"], "env": {"GIT_INDEX_FILE": temporary_index}, "stdin_file": str(root / "index_updates.z")},
            {"argv": git + ["write-tree"], "env": {"GIT_INDEX_FILE": temporary_index}, "expected_stdout": plan["final_tree"]},
            {"argv": git + ["hash-object", "-t", "commit", "-w", "--stdin"], "stdin_file": str(out / "commit.raw"), "expected_stdout": commit["sha"]},
        ]
        write_json(out / "local_materialization_instructions.json", {"scope": "Future authorized local object installation only; NOT executed", "commands": commands, "working_files_changed": False, "normal_index_changed": False, "branch_ref_move_included": False, "warning": "These future commands write Git objects and a separate temporary index. Verify every expected SHA. Moving HEAD/main or synchronizing the normal index is a separate explicit operation after remote ref verification."})
        print(json.dumps({"status": "REMOTE_COMMIT_BYTES_RECONSTRUCTED_NOT_INSTALLED", "remote_commit": commit["sha"], "raw_file": str(out / "commit.raw")}))
    except BaseException as error:
        write_json(out / "failure.json", {"recorded_utc": utc(), "type": type(error).__name__, "message": str(error), "traceback": traceback.format_exc(), "git_data_writes": 0})
        raise


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    q = sub.add_parser("prepare", help="After final accounting, snapshot intended files and prepare exact API payloads outside the checkout")
    q.add_argument("--repo", default=DEFAULT_REPO)
    q.add_argument("--base", default=DEFAULT_BASE)
    q.add_argument("--repository", default=DEFAULT_REMOTE)
    q.add_argument("--out", required=True)
    q.add_argument("--cap-bytes", type=int, default=3_000_000)
    q.add_argument("--entry-cap", type=int, default=128)
    q.add_argument("--overlay-cap", type=int, default=128)
    q.add_argument("--allow-deletions", action="store_true")
    q.set_defaults(func=prepare)
    q = sub.add_parser("verify", help="Verify frozen plan bytes/identities; optionally compare current working files")
    q.add_argument("--plan", required=True)
    q.add_argument("--working-tree", action="store_true")
    q.set_defaults(func=verify)
    q = sub.add_parser("record", help="Preserve an actual saved tool result and verify its request-bound SHA")
    q.add_argument("--plan", required=True)
    q.add_argument("--phase", choices=["upload", "overlay"], required=True)
    q.add_argument("--index", type=int, required=True)
    q.add_argument("--result", required=True, help="Raw tool-result JSON file, or - for stdin")
    q.set_defaults(func=record)
    q = sub.add_parser("status", help="Reconstruct resumable progress; emits payload paths, never their large contents")
    q.add_argument("--plan", required=True)
    q.add_argument("--limit", type=int, default=4)
    q.add_argument("--out")
    q.set_defaults(func=status_report)
    q = sub.add_parser("commit-payload", help="After Git-commit GET, reconstruct exact unsigned remote bytes and emit future local-install instructions only")
    q.add_argument("--plan", required=True)
    q.add_argument("--response", required=True)
    q.add_argument("--out", required=True)
    q.set_defaults(func=commit_payload)
    return p


def main():
    args = parser().parse_args()
    return args.func(args) or 0


if __name__ == "__main__":
    raise SystemExit(main())
