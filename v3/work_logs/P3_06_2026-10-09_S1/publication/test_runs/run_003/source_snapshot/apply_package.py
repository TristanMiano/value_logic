#!/usr/bin/env python3
"""Guarded, idempotent P3-06 delivery; Python >= 3.10, Git, standard library only.

This helper does not measure research time. It never creates an append from a
clock: it applies only the manifest's already-reviewed CSV bytes. See README.md.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

VERSION = "p306-delivery-v1"
SCHEMA = "value_logic.p306.delivery.v1"
REPOSITORY = "https://github.com/TristanMiano/value_logic.git"
PUBLICATION = "v3/work_logs/P3_06_2026-10-09_S1/publication/"
LEDGER = "v3/time_ledger.csv"
FIXTURE_MARKER = "value_logic.p306.local_test_fixture.v1\n"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
KEY_COLUMNS = ("task_id", "attempt_id", "session_id", "start_utc", "end_utc")


class GuardError(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise GuardError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key.")
        result[key] = value
    return result


def parse_json(data):
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object)
    except (ValueError, UnicodeError) as exc:
        raise GuardError("Invalid UTF-8 JSON.") from exc


def keys(value, required, label):
    need(type(value) is dict and set(value) == set(required), "Unexpected fields in " + label + ".")


def sha(value, nullable=False):
    need((nullable and value is None) or (type(value) is str and HEX64.fullmatch(value)), "Invalid SHA-256 value.")


def safe_path(value):
    need(type(value) is str and 0 < len(value) < 2000, "Invalid relative path.")
    need(not any(c in value for c in '\\:<>"|?*') and not any(ord(c) < 32 for c in value), "Unsafe path characters.")
    path = PurePosixPath(value)
    need(bool(path.parts) and not path.is_absolute() and str(path) == value, "Noncanonical relative path.")
    reserved = {"con", "prn", "aux", "nul"} | {"com" + str(i) for i in range(1, 10)} | {"lpt" + str(i) for i in range(1, 10)}
    for part in path.parts:
        need(part not in {".", ".."} and part.casefold() != ".git", "Unsafe path component.")
        need(part == part.rstrip(" .") and part.split(".")[0].casefold() not in reserved, "Windows-ambiguous path.")
    return value


def check_aliases(paths):
    seen = {}
    files = set(paths)
    for value in paths:
        parts = PurePosixPath(value).parts
        for count in range(1, len(parts) + 1):
            prefix = "/".join(parts[:count])
            folded = prefix.casefold()
            need(folded not in seen or seen[folded] == prefix, "Case-ambiguous paths.")
            seen[folded] = prefix
            need(count == len(parts) or prefix not in files, "File/directory path collision.")


class Package:
    def __init__(self, archive, expected_sha256):
        sha(expected_sha256)
        archive = Path(archive).resolve(strict=True)
        raw_zip = archive.read_bytes()
        need(digest(raw_zip) == expected_sha256, "ZIP SHA-256 does not match the independently supplied value.")
        self.zip_sha256 = expected_sha256
        try:
            with zipfile.ZipFile(io.BytesIO(raw_zip)) as z:
                entries = z.infolist()
                names = [i.filename for i in entries if not i.is_dir()]
                need(len(names) == len(set(names)), "Duplicate ZIP member.")
                need(len(names) <= 40000 and sum(i.file_size for i in entries) <= 1024 ** 3, "ZIP exceeds delivery size limits.")
                for entry in entries:
                    safe_path(entry.filename.rstrip("/") if entry.is_dir() else entry.filename)
                    kind = stat.S_IFMT(entry.external_attr >> 16)
                    need(kind in (0, stat.S_IFREG, stat.S_IFDIR), "ZIP links and special files are forbidden.")
                check_aliases(names)
                need("manifest.json" in names, "ZIP has no root manifest.json.")
                manifest_raw = z.read("manifest.json")
                self.manifest_sha256 = digest(manifest_raw)
                m = parse_json(manifest_raw)
                keys(m, ("schema", "package_id", "repository", "branch", "base_commit", "commit_subject", "receipt_path", "members", "files", "ledger"), "manifest")
                need(m["schema"] == SCHEMA and m["repository"] == REPOSITORY and m["branch"] == "main", "Wrong schema, repository or branch.")
                need(type(m["package_id"]) is str and re.fullmatch(r"value-logic-p306-[a-z0-9-]{1,100}", m["package_id"]), "Invalid package ID.")
                need(type(m["base_commit"]) is str and HEX40.fullmatch(m["base_commit"]), "Invalid base commit.")
                subject = m["commit_subject"]
                need(type(subject) is str and 1 <= len(subject) <= 200 and all(ord(c) >= 32 for c in subject), "Invalid commit subject.")
                receipt = safe_path(m["receipt_path"])
                need(receipt.startswith(PUBLICATION) and receipt.endswith(".json"), "Receipt must be a JSON file in this P3-06 publication directory.")
                need(type(m["members"]) is dict and set(m["members"]) == set(names) - {"manifest.json"}, "Manifest must hash every non-manifest ZIP file, with no extras.")
                self.members = {}
                for name, expected in m["members"].items():
                    safe_path(name)
                    sha(expected)
                    value = z.read(name)
                    need(digest(value) == expected, "ZIP member hash mismatch: " + name)
                    self.members[name] = value
                need("apply_package.py" in self.members and "Apply-And-Push.ps1" in self.members, "ZIP must include both delivery helpers at its root.")
                need(Path(__file__).read_bytes() == self.members["apply_package.py"], "The running Python helper differs from the helper in the verified ZIP.")
        except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
            if isinstance(exc, GuardError):
                raise
            raise GuardError("Cannot read the ZIP package.") from exc
        self.m = m
        self.files = {}
        need(type(m["files"]) is list, "files must be a list.")
        for entry in m["files"]:
            keys(entry, ("path", "before_sha256", "before_mode", "after_sha256", "after_mode", "payload"), "file entry")
            path = safe_path(entry["path"])
            need(path not in (LEDGER, receipt) and path not in self.files, "Duplicate or reserved target path.")
            for prefix in ("before", "after"):
                sha(entry[prefix + "_sha256"], nullable=True)
                mode = entry[prefix + "_mode"]
                need(mode in (None, "100644", "100755"), "Only regular Git files are supported.")
                need((mode is None) == (entry[prefix + "_sha256"] is None), "Mode/hash absence mismatch.")
            if entry["after_sha256"] is None:
                need(entry["before_sha256"] is not None and entry["payload"] is None, "Invalid deletion.")
            else:
                payload = safe_path(entry["payload"])
                need(payload.startswith("payload/") and payload in self.members, "Missing payload member.")
                need(digest(self.members[payload]) == entry["after_sha256"], "Payload does not match postimage.")
            self.files[path] = entry
        led = m["ledger"]
        keys(led, ("path", "base_sha256", "base_bytes", "append_payload", "append_sha256", "append_rows"), "ledger operation")
        need(led["path"] == LEDGER, "The ledger must use the dedicated append operation.")
        sha(led["base_sha256"])
        sha(led["append_sha256"])
        need(type(led["base_bytes"]) is int and led["base_bytes"] > 0, "Invalid ledger base size.")
        need(type(led["append_rows"]) is int and led["append_rows"] >= 0, "Invalid ledger append row count.")
        payload = safe_path(led["append_payload"])
        need(payload.startswith("payload/") and payload in self.members, "Missing ledger append payload.")
        self.append = self.members[payload]
        need(digest(self.append) == led["append_sha256"], "Ledger append hash mismatch.")
        self.targets = sorted([*self.files, LEDGER, receipt])
        check_aliases(self.targets)


class Repo:
    def __init__(self, path, fixture_root=None):
        self.path = Path(path).resolve(strict=True)
        self.env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
        self.blob_cache = {}
        need(Path(self.git("rev-parse", "--show-toplevel").decode().strip()).resolve() == self.path, "Repository must be its top-level working directory.")
        need(self.git("symbolic-ref", "--quiet", "--short", "HEAD").decode().strip() == "main", "A checked-out main branch is required.")
        need(self.git("rev-parse", "--is-shallow-repository").strip() == b"false", "A full repository is required to verify base ancestry.")
        for state in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
            state_path = self.git("rev-parse", "--git-path", state).decode().strip()
            absolute = Path(state_path) if Path(state_path).is_absolute() else self.path / state_path
            need(not absolute.exists(), "Finish or abort the existing Git operation before applying this package.")
        self.clean()
        fetch_urls = self.git("remote", "get-url", "--all", "origin").decode().splitlines()
        push_urls = self.git("remote", "get-url", "--push", "--all", "origin").decode().splitlines()
        need(len(fetch_urls) == len(push_urls) == 1, "Exactly one origin fetch URL and one push URL are required.")
        if fixture_root is not None:
            root = Path(fixture_root).resolve(strict=True)
            need(os.environ.get("VALUE_LOGIC_P306_LOCAL_FIXTURE") == "1", "Test fixture override requires the explicit test environment acknowledgement.")
            need((root / "FIXTURE_ONLY").read_text(encoding="utf-8") == FIXTURE_MARKER, "Missing local test fixture marker.")
            remote = root / "remote.git"
            need(self.path.is_relative_to(root) and self.path != root, "Test checkout must be inside the marked fixture directory.")
            need(all(Path(url).is_absolute() and Path(url).resolve() == remote for url in fetch_urls + push_urls), "Test override accepts only this fixture's local bare remote.")
            need(self.git("--git-dir=" + str(remote), "rev-parse", "--is-bare-repository").strip() == b"true", "Test remote is not bare.")
        else:
            allowed = {
                "https://github.com/TristanMiano/value_logic", REPOSITORY,
                "git@github.com:TristanMiano/value_logic", "git@github.com:TristanMiano/value_logic.git",
                "ssh://git@github.com/TristanMiano/value_logic", "ssh://git@github.com/TristanMiano/value_logic.git",
            }
            need(all(url in allowed for url in fetch_urls + push_urls), "Origin fetch and push must both name TristanMiano/value_logic on github.com, without embedded credentials.")

    def command(self, *args, data=None, timeout=120):
        try:
            return subprocess.run(["git", "--literal-pathspecs", "-C", str(self.path), *args], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.env, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise GuardError("Git command unavailable or timed out: " + args[0]) from exc

    def git(self, *args, data=None):
        result = self.command(*args, data=data)
        need(result.returncode == 0, "Git command failed: " + args[0] + ". Resolve Git configuration/authentication or repository state and retry; raw command output is not logged.")
        return result.stdout

    def clean(self):
        need(not self.git("status", "--porcelain=v1", "-z", "--untracked-files=all"), "Clean main required: staged, modified and untracked files must be resolved first.")

    def head(self, ref="HEAD"):
        value = self.git("rev-parse", "--verify", ref).decode().strip()
        need(HEX40.fullmatch(value), "Unsupported Git object format.")
        return value

    def ancestor(self, old, new):
        result = self.command("merge-base", "--is-ancestor", old, new)
        need(result.returncode in (0, 1), "Cannot establish Git ancestry.")
        return result.returncode == 0

    def fetch(self):
        self.git("fetch", "--no-tags", "origin", "refs/heads/main:refs/remotes/origin/main")
        return self.head("refs/remotes/origin/main")

    def tree(self, rev):
        raw = self.git("ls-tree", "-r", "-z", "--full-tree", rev)
        result = {}
        for line in raw.split(b"\0"):
            if line:
                info, name = line.split(b"\t", 1)
                mode, kind, oid = info.decode("ascii").split()
                result[name.decode("utf-8")] = (mode, kind, oid)
        return result

    def blob(self, tree, path):
        entry = tree.get(path)
        if entry is None:
            return None
        need(entry[0] in ("100644", "100755") and entry[1] == "blob", "Touched paths must be regular files: " + path)
        oid = entry[2]
        if oid not in self.blob_cache:
            self.blob_cache[oid] = self.git("cat-file", "blob", oid)
        return self.blob_cache[oid]

    def stage(self, paths):
        self.git("add", "--pathspec-from-file=-", "--pathspec-file-nul", data=b"\0".join(p.encode() for p in paths) + b"\0")


def timestamp(value):
    try:
        result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        need(result.tzinfo is not None, "Ledger timestamps must include a timezone.")
        return result.astimezone(dt.timezone.utc)
    except (TypeError, ValueError) as exc:
        raise GuardError("Invalid ledger timestamp.") from exc


def csv_rows(raw, header=None):
    try:
        rows = list(csv.reader(io.StringIO(raw.decode("utf-8"), newline=""), strict=True))
    except (UnicodeError, csv.Error) as exc:
        raise GuardError("Invalid UTF-8 CSV ledger bytes.") from exc
    if header is None:
        need(bool(rows), "Empty ledger.")
        header, rows = rows[0], rows[1:]
        need(len(header) == len(set(header)) and all(c in header for c in KEY_COLUMNS), "Invalid ledger header.")
    need(all(len(row) == len(header) for row in rows), "Ledger row width/header mismatch.")
    return header, [dict(zip(header, row)) for row in rows]


def interval_key(row):
    start, end = timestamp(row["start_utc"]), timestamp(row["end_utc"])
    need(end >= start, "Ledger interval ends before it begins.")
    return (row["task_id"], row["attempt_id"], row["session_id"], start, end)


def ledger_after(package, base, current):
    led = package.m["ledger"]
    need(base is not None and len(base) == led["base_bytes"] and digest(base) == led["base_sha256"], "Ledger base preimage mismatch.")
    need(current is not None and current.startswith(base), "Current ledger no longer preserves the exact base prefix.")
    need(current.endswith(b"\n") and (not package.append or package.append.endswith(b"\n")), "Ledger prefix and nonempty append must end with a newline.")
    header, old_rows = csv_rows(current)
    _, new_rows = csv_rows(package.append, header)
    need(len(new_rows) == led["append_rows"], "Ledger append row count mismatch.")
    groups = {(r["task_id"], r["attempt_id"], r["session_id"]) for r in new_rows}
    old_keys = []
    for row in old_rows:
        if (row["task_id"], row["attempt_id"], row["session_id"]) in groups:
            old_keys.append(interval_key(row))
    fresh = []
    for row in new_rows:
        key = interval_key(row)
        need(all(row[c] for c in KEY_COLUMNS), "Append rows require complete interval identities.")
        for other in old_keys + fresh:
            need(key != other, "Duplicate ledger interval identity, including relabelled time, is forbidden.")
            if key[:3] == other[:3]:
                need(not (key[3] < other[4] and other[3] < key[4]), "Overlapping ledger intervals in the same attempt/session are forbidden.")
        fresh.append(key)
    return current + package.append


def check_images(repo, tree, package, prefix):
    for path, entry in package.files.items():
        value = repo.blob(tree, path)
        expected = entry[prefix + "_sha256"]
        need((None if value is None else digest(value)) == expected, "Touched-path " + prefix + "image conflict: " + path)
        need((None if value is None else tree[path][0]) == entry[prefix + "_mode"], "Touched-path mode conflict: " + path)


def preflight(repo, package, candidate):
    base_tree, tree = repo.tree(package.m["base_commit"]), repo.tree(candidate)
    check_aliases([*tree, *[p for p in package.targets if p not in tree]])
    check_images(repo, base_tree, package, "before")
    check_images(repo, tree, package, "before")
    receipt_path = package.m["receipt_path"]
    need(receipt_path not in base_tree and receipt_path not in tree, "An unrecognized application receipt already exists.")
    base_ledger, current_ledger = repo.blob(base_tree, LEDGER), repo.blob(tree, LEDGER)
    after_ledger = ledger_after(package, base_ledger, current_ledger)
    need(tree.get(LEDGER, (None,))[0] == "100644", "Ledger must be a nonexecutable regular Git file.")
    return tree, current_ledger, after_ledger


def workspace_targets(repo, package, tree):
    for name in package.targets:
        target = repo.path / name
        for parent in [target, *target.parents]:
            if parent == repo.path:
                break
            need(not parent.is_symlink(), "Symlink/reparse-point target ancestry is forbidden: " + name)
            if os.path.lexists(parent):
                attributes = getattr(parent.lstat(), "st_file_attributes", 0)
                need(not attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400), "Windows reparse-point target ancestry is forbidden: " + name)
            if hasattr(parent, "is_junction"):
                need(not parent.is_junction(), "Junction target ancestry is forbidden: " + name)
        if name not in tree:
            need(not os.path.lexists(target), "A new target collides with an existing or ignored local path: " + name)
        else:
            need(target.is_file(), "Tracked target is not a regular working-tree file: " + name)


def atomic_write(path, value, mode, created_dirs):
    missing = []
    parent = path.parent
    while not parent.exists():
        missing.append(parent)
        parent = parent.parent
    for directory in reversed(missing):
        directory.mkdir()
        created_dirs.append(directory)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".p306-write-", dir=path.parent, delete=False) as out:
            temporary = Path(out.name)
            out.write(value)
            out.flush()
            os.fsync(out.fileno())
        os.chmod(temporary, 0o755 if mode == "100755" else 0o644)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def expected_outputs(package, ledger):
    return {**{p: e["after_sha256"] for p, e in package.files.items()}, LEDGER: digest(ledger)}


def verify_staged(repo, package, parent_tree, ledger, receipt_bytes):
    staged = repo.tree(repo.git("write-tree").decode().strip())
    verify_tree(repo, package, staged, parent_tree, ledger, receipt_bytes)


def verify_tree(repo, package, staged, parent_tree, ledger, receipt_bytes):
    check_images(repo, staged, package, "after")
    need(repo.blob(staged, LEDGER) == ledger, "Git filters, hooks or changes altered the expected ledger bytes.")
    need(repo.blob(staged, package.m["receipt_path"]) == receipt_bytes, "Git filters, hooks or changes altered the expected receipt bytes.")
    allowed = set(package.targets)
    need(all(parent_tree.get(p) == staged.get(p) for p in set(parent_tree) | set(staged) if p not in allowed), "Unexpected staged changes outside the manifest.")


def rollback_uncommitted(repo, package, original_tree, original_worktree, owned_index, written, created_dirs):
    # Restore only this helper's declared paths. No reset, clean, stash or force.
    index_tree = repo.tree(repo.git("write-tree").decode().strip())
    # Audit every candidate before restoring any of them. A hook or concurrent
    # editor must not lose changes merely because a commit command failed.
    for name in package.targets:
        target = repo.path / name
        if os.path.lexists(target):
            need(not target.is_symlink() and target.is_file(), "Unexpected target type during rollback; preserve current files and review manually.")
            actual = target.read_bytes()
        else:
            actual = None
        need(actual in (original_worktree.get(name), written.get(name, original_worktree.get(name))), "A hook or concurrent edit changed a target; current worktree and index are preserved for manual review.")
        need(index_tree.get(name) in (original_tree.get(name), owned_index.get(name, original_tree.get(name))), "A hook or concurrent edit changed the index; current worktree and index are preserved for manual review.")
    indexed = [p for p in package.targets if p in index_tree or p in original_tree]
    if indexed:
        data = b"\0".join(p.encode() for p in indexed) + b"\0"
        repo.git("restore", "--source=HEAD", "--staged", "--pathspec-from-file=-", "--pathspec-file-nul", data=data)
    tracked = [p for p in package.targets if p in original_tree]
    if tracked:
        repo.git("restore", "--source=HEAD", "--worktree", "--pathspec-from-file=-", "--pathspec-file-nul", data=b"\0".join(p.encode() for p in tracked) + b"\0")
    for name, value in written.items():
        target = repo.path / name
        if name not in original_tree and target.exists():
            need(not target.is_symlink() and target.is_file() and target.read_bytes() == value, "A newly written file changed concurrently; manual recovery is required.")
            target.unlink()
    for directory in reversed(created_dirs):
        try:
            directory.rmdir()
        except OSError:
            pass


def apply_new(repo, package, candidate, tree, current_ledger, ledger):
    workspace_targets(repo, package, tree)
    original_worktree = {p: (repo.path / p).read_bytes() for p in package.targets if p in tree}
    receipt = {
        "schema": "value_logic.p306.applied.v1", "helper_version": VERSION,
        "package_id": package.m["package_id"], "manifest_sha256": package.manifest_sha256,
        "base_commit": package.m["base_commit"], "before_commit": candidate,
        "applied_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "outputs_sha256": expected_outputs(package, ledger),
        "ledger_prefix_sha256": digest(current_ledger), "ledger_prefix_bytes": len(current_ledger),
        "ledger_append_sha256": digest(package.append), "ledger_append_bytes": len(package.append),
        "ledger_appended_rows": package.m["ledger"]["append_rows"],
        "publication": "Local application only; remote ancestry must be checked separately.",
    }
    receipt_bytes = canonical(receipt)
    written, created_dirs, owned_index = {}, [], {}
    try:
        for name, entry in package.files.items():
            if entry["after_sha256"] is None:
                (repo.path / name).unlink()
                written[name] = None
            else:
                value = package.members[entry["payload"]]
                atomic_write(repo.path / name, value, entry["after_mode"], created_dirs)
                written[name] = value
        atomic_write(repo.path / LEDGER, ledger, "100644", created_dirs)
        written[LEDGER] = ledger
        name = package.m["receipt_path"]
        atomic_write(repo.path / name, receipt_bytes, "100644", created_dirs)
        written[name] = receipt_bytes
        repo.stage(package.targets)
        owned_index = repo.tree(repo.git("write-tree").decode().strip())
        for mode in ("100644", "100755"):
            paths = [p for p, entry in package.files.items() if entry["after_mode"] == mode]
            if mode == "100644":
                paths += [LEDGER, name]
            if paths:
                repo.git("update-index", "--chmod=" + ("+x" if mode == "100755" else "-x"), "-z", "--stdin", data=b"\0".join(p.encode() for p in paths) + b"\0")
                owned_index = repo.tree(repo.git("write-tree").decode().strip())
        verify_staged(repo, package, tree, ledger, receipt_bytes)
        message = package.m["commit_subject"] + "\n\nValue-Logic-Package: " + package.m["package_id"] + "\nValue-Logic-Manifest-SHA256: " + package.manifest_sha256 + "\n"
        repo.git("commit", "--file=-", data=message.encode())
    except BaseException:
        if repo.head() == candidate:
            rollback_uncommitted(repo, package, tree, original_worktree, owned_index, written, created_dirs)
        raise
    repo.clean()
    commit = find_applied(repo, package, repo.head())
    need(commit == repo.head(), "New commit failed the application audit; it was not pushed.")
    return commit


def find_applied(repo, package, rev):
    marker = "Value-Logic-Package: " + package.m["package_id"]
    candidates = repo.git("log", "--format=%H", "--fixed-strings", "--grep=" + marker, rev).decode().splitlines()
    matches = []
    for commit in candidates:
        message = repo.git("show", "-s", "--format=%B", commit).decode().splitlines()
        if marker in message:
            need("Value-Logic-Manifest-SHA256: " + package.manifest_sha256 in message, "Package ID already belongs to a different manifest.")
            matches.append(commit)
    need(len(matches) <= 1, "Multiple application commits for the same package are in this history.")
    if not matches:
        return None
    commit = matches[0]
    parents = repo.git("show", "-s", "--format=%P", commit).decode().split()
    need(len(parents) == 1, "Original application must be a single-parent commit.")
    tree, before_tree = repo.tree(commit), repo.tree(parents[0])
    raw = repo.blob(tree, package.m["receipt_path"])
    need(raw is not None, "Package commit has no receipt.")
    receipt = parse_json(raw)
    need(type(receipt) is dict, "Application receipt must be a JSON object.")
    need(receipt.get("schema") == "value_logic.p306.applied.v1" and receipt.get("package_id") == package.m["package_id"] and receipt.get("manifest_sha256") == package.manifest_sha256, "Application receipt identity mismatch.")
    need(receipt.get("base_commit") == package.m["base_commit"] and receipt.get("before_commit") == parents[0] and repo.ancestor(package.m["base_commit"], parents[0]), "Application receipt ancestry mismatch.")
    _, current_ledger, expected_ledger = preflight(repo, package, parents[0])
    check_images(repo, tree, package, "after")
    need(repo.blob(tree, LEDGER) == expected_ledger, "Committed ledger does not equal the verified prefix plus append.")
    need(receipt.get("outputs_sha256") == expected_outputs(package, expected_ledger), "Receipt output hashes mismatch.")
    checks = {
        "ledger_prefix_sha256": digest(current_ledger), "ledger_prefix_bytes": len(current_ledger),
        "ledger_append_sha256": digest(package.append), "ledger_append_bytes": len(package.append),
        "ledger_appended_rows": package.m["ledger"]["append_rows"],
    }
    need(all(receipt.get(k) == v for k, v in checks.items()), "Receipt ledger accounting mismatch.")
    need(all(tree.get(p) == before_tree.get(p) for p in set(tree) | set(before_tree) if p not in package.targets), "Application commit includes undeclared changes.")
    return commit


def allowed_retry_commits(repo, package, remote, applied):
    for commit in repo.git("rev-list", remote + "..HEAD").decode().splitlines():
        if commit == applied:
            continue
        verify_retry_merge(repo, package, commit)


def verify_retry_merge(repo, package, commit):
    lines = repo.git("show", "-s", "--format=%B", commit).decode().splitlines()
    parents = repo.git("show", "-s", "--format=%P", commit).decode().split()
    need(len(parents) == 2 and "Value-Logic-Retry-Merge: " + package.m["package_id"] in lines and "Value-Logic-Manifest-SHA256: " + package.manifest_sha256 in lines, "Unrelated unpublished local commits would be pushed; reconcile them separately.")
    remote_tree, _, ledger = preflight(repo, package, parents[1])
    receipt_bytes = repo.blob(repo.tree(parents[0]), package.m["receipt_path"])
    need(receipt_bytes is not None, "Retry merge parent has no receipt.")
    verify_tree(repo, package, repo.tree(commit), remote_tree, ledger, receipt_bytes)


def reconcile_retry(repo, package, remote):
    remote_tree, _, ledger = preflight(repo, package, remote)
    before = repo.head()
    receipt_bytes = repo.blob(repo.tree(before), package.m["receipt_path"])
    need(receipt_bytes is not None, "Retry receipt is missing from local main.")
    try:
        result = repo.command("merge", "--no-ff", "--no-commit", remote)
        if result.returncode:
            conflicts = repo.git("diff", "--name-only", "--diff-filter=U", "-z").decode().strip("\0").split("\0")
            need(conflicts == [LEDGER], "Retry merge has a conflict beyond the dedicated ledger append.")
        atomic_write(repo.path / LEDGER, ledger, "100644", [])
        repo.stage([LEDGER])
        verify_staged(repo, package, remote_tree, ledger, receipt_bytes)
        message = "Reconcile P3-06 delivery with advanced main\n\nValue-Logic-Retry-Merge: " + package.m["package_id"] + "\nValue-Logic-Manifest-SHA256: " + package.manifest_sha256 + "\n"
        repo.git("commit", "--file=-", data=message.encode())
    except BaseException:
        if repo.head() == before:
            repo.command("merge", "--abort")
        raise
    repo.clean()
    need(repo.ancestor(remote, repo.head()), "Retry merge did not retain current remote ancestry.")
    verify_retry_merge(repo, package, repo.head())
    return repo.head()


def publish(repo, package, applied, disposition):
    push_head = repo.head()
    need(repo.ancestor(applied, push_head), "Verified package commit is not in local main ancestry.")
    repo.clean()
    try:
        result = repo.command("push", "--porcelain", "origin", push_head + ":refs/heads/main")
        push_code = result.returncode
    except GuardError:
        push_code = None
    # A failed response can follow a successful server update. Never infer the
    # publication result from the exit status alone, or replay on that basis.
    try:
        remote_after = repo.fetch()
        published = repo.ancestor(push_head, remote_after)
    except GuardError:
        remote_after, published = None, False
    return {
        "status": "published" if published else "committed_pending_push",
        "disposition": disposition, "package_id": package.m["package_id"],
        "manifest_sha256": package.manifest_sha256, "application_commit": applied,
        "local_head": push_head, "remote_head": remote_after, "push_exit_code": push_code,
        "message": "Remote main contains the verified application." if published else "Local commit retained. Resolve remote/authentication conditions and rerun the same package; do not reapply or append manually.",
    }


@contextlib.contextmanager
def delivery_lock(repo):
    git_dir = Path(repo.git("rev-parse", "--absolute-git-dir").decode().strip())
    path = git_dir / "value_logic_p306_delivery.lock"
    value = canonical({"schema": "value_logic.p306.delivery_lock.v1", "pid": os.getpid()})
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise GuardError("A delivery lock already exists in the Git directory. Check for another running helper or an interrupted invocation before removing a stale lock.") from exc
    try:
        with os.fdopen(descriptor, "wb") as out:
            out.write(value)
        yield
    finally:
        if path.exists() and path.read_bytes() == value:
            path.unlink()


def run(args):
    package = Package(args.package, args.zip_sha256)
    repo = Repo(args.repo, args.test_fixture_root)
    with delivery_lock(repo):
        repo.clean()
        return run_locked(repo, package, args)


def run_locked(repo, package, args):
    head, remote = repo.head(), repo.fetch()
    base = package.m["base_commit"]
    need(repo.ancestor(base, head) and repo.ancestor(base, remote), "Both local and current remote main must descend from the declared GitHub base.")
    local_applied = find_applied(repo, package, head)
    remote_applied = find_applied(repo, package, remote)
    if remote_applied:
        need(local_applied in (None, remote_applied), "Local and remote contain different application commits for this package.")
        disposition = "already_published"
        if head != remote:
            if repo.ancestor(head, remote):
                if not args.check_only:
                    repo.git("merge", "--ff-only", remote)
            else:
                disposition = "already_published_local_history_preserved"
        return {"status": "verified_only" if args.check_only else "already_published", "disposition": disposition, "package_id": package.m["package_id"], "application_commit": remote_applied, "manifest_sha256": package.manifest_sha256, "remote_head": remote, "message": "Existing verified application found in remote ancestry; no append, application commit or push repeated."}
    if local_applied:
        allowed_retry_commits(repo, package, remote, local_applied)
        if not repo.ancestor(remote, head):
            preflight(repo, package, remote)
        if args.check_only:
            return {"status": "verified_only", "disposition": "retry_ready", "application_commit": local_applied, "remote_head": remote}
        if not repo.ancestor(remote, head):
            reconcile_retry(repo, package, remote)
        return publish(repo, package, local_applied, "retry_without_reapplying")
    need(repo.ancestor(head, remote), "Unpublished or divergent local commits are present; no unrelated local work will be pushed.")
    tree, current_ledger, ledger = preflight(repo, package, remote)
    workspace_targets(repo, package, repo.tree(head))
    if args.check_only:
        return {"status": "verified_only", "disposition": "new_apply_ready", "package_id": package.m["package_id"], "manifest_sha256": package.manifest_sha256, "remote_head": remote, "ledger_appended_rows": package.m["ledger"]["append_rows"]}
    if head != remote:
        repo.git("merge", "--ff-only", remote)
    repo.clean()
    need(repo.head() == remote, "Local main changed during preflight.")
    applied = apply_new(repo, package, remote, tree, current_ledger, ledger)
    return publish(repo, package, applied, "new_application")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, help="Final ZIP path; keep it outside the target checkout.")
    parser.add_argument("--zip-sha256", required=True, help="SHA-256 supplied independently with the final ZIP.")
    parser.add_argument("--repo", required=True, help="Top-level path of the clean main checkout.")
    parser.add_argument("--check-only", action="store_true", help="Verify package and current Git preconditions; fetch only, no worktree update, commit or push.")
    parser.add_argument("--test-fixture-root", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        result = run(args)
        print(json.dumps(result, sort_keys=True, indent=2))
        return 3 if result["status"] == "committed_pending_push" else 0
    except (GuardError, OSError, UnicodeError) as exc:
        print(json.dumps({"status": "aborted", "helper_version": VERSION, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
