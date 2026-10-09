#!/usr/bin/env python3
"""Actual CLI tests against marked temporary local bare remotes; never GitHub."""
from __future__ import annotations

import contextlib
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
HELPER = HERE / "apply_package.py"
RECEIPT = "v3/work_logs/P3_06_2026-10-09_S1/publication/applied_package.json"
LEDGER = "v3/time_ledger.csv"
HEADER = "task_id,attempt_id,session_id,mode,lane,start_utc,end_utc,elapsed_seconds,engaged_seconds,tool_wait_seconds,idle_seconds,unmeasured_seconds,forecast_seconds,artifact,status\n"
BASE_ROW = "P3-05,P3-05-1,2026-10-08-S1,O,,2026-10-08T00:00:00+00:00,2026-10-08T00:00:10+00:00,10,10,0,0,0,10,v3/old.md,prior\n"
APPEND = ("P3-06,P3-06-1,2026-10-09-S1,E,R,2026-10-09T00:00:00+00:00,2026-10-09T00:00:10+00:00,10,10,0,0,0,10,v3/new.md,first\n"
          "P3-06,P3-06-1,2026-10-09-S1,D,R,2026-10-09T00:00:10+00:00,2026-10-09T00:00:20+00:00,10,10,0,0,0,10,v3/new.md,second\n").encode()
UNRELATED_ROW = "OTHER,OTHER-1,2026-10-09-S2,O,,2026-10-09T01:00:00+00:00,2026-10-09T01:00:10+00:00,10,10,0,0,0,10,v3/other.md,unrelated\n".encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(path, *args, data=None):
    result = subprocess.run(["git", "-C", str(path), *args], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return result.stdout


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


class Fixture:
    def __init__(self, root):
        self.root = root
        self.root.joinpath("FIXTURE_ONLY").write_text("value_logic.p306.local_test_fixture.v1\n", encoding="utf-8")
        self.remote, self.repo, self.seed = root / "remote.git", root / "checkout", root / "seed"
        subprocess.run(["git", "init", "--bare", "-b", "main", str(self.remote)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "init", "-b", "main", str(self.seed)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.identity(self.seed)
        write(self.seed / "control.txt", b"base control\n")
        write(self.seed / LEDGER, (HEADER + BASE_ROW).encode())
        git(self.seed, "add", "control.txt", LEDGER)
        git(self.seed, "commit", "-m", "Fixture base")
        self.base = git(self.seed, "rev-parse", "HEAD").decode().strip()
        git(self.seed, "remote", "add", "origin", str(self.remote))
        git(self.seed, "push", "origin", "main")
        subprocess.run(["git", "clone", str(self.remote), str(self.repo)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.identity(self.repo)
        self.base_ledger = (HEADER + BASE_ROW).encode()
        self.members = {"apply_package.py": HELPER.read_bytes(), "Apply-And-Push.ps1": (HERE / "Apply-And-Push.ps1").read_bytes(), "payload/control.txt": b"P3-06 control\n", "payload/new.txt": b"new evidence\n", "payload/ledger_append.csv": APPEND}
        self.manifest = {
            "schema": "value_logic.p306.delivery.v1", "package_id": "value-logic-p306-local-test-v1",
            "repository": "https://github.com/TristanMiano/value_logic.git", "branch": "main", "base_commit": self.base,
            "commit_subject": "Apply verified P3-06 fixture", "receipt_path": RECEIPT,
            "members": {p: sha(v) for p, v in self.members.items()},
            "files": [
                {"path": "control.txt", "before_sha256": sha(b"base control\n"), "before_mode": "100644", "after_sha256": sha(self.members["payload/control.txt"]), "after_mode": "100644", "payload": "payload/control.txt"},
                {"path": "new.txt", "before_sha256": None, "before_mode": None, "after_sha256": sha(self.members["payload/new.txt"]), "after_mode": "100644", "payload": "payload/new.txt"},
            ],
            "ledger": {"path": LEDGER, "base_sha256": sha(self.base_ledger), "base_bytes": len(self.base_ledger), "append_payload": "payload/ledger_append.csv", "append_sha256": sha(APPEND), "append_rows": 2},
        }
        self.package = root / "delivery.zip"
        self.save()

    def identity(self, path):
        git(path, "config", "user.name", "P3-06 local test fixture")
        git(path, "config", "user.email", "fixture@example.invalid")
        git(path, "config", "commit.gpgsign", "false")

    def save(self):
        with zipfile.ZipFile(self.package, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("manifest.json", json.dumps(self.manifest, sort_keys=True, indent=2) + "\n")
            for name, value in self.members.items():
                z.writestr(name, value)
        self.zip_sha = sha(self.package.read_bytes())

    def call(self, *extra, override=True, expected_sha=None):
        cmd = [sys.executable, str(HELPER), "--repo", str(self.repo), "--package", str(self.package), "--zip-sha256", expected_sha or self.zip_sha]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        if override:
            cmd += ["--test-fixture-root", str(self.root)]
            env["VALUE_LOGIC_P306_LOCAL_FIXTURE"] = "1"
        result = subprocess.run(cmd + list(extra), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=60)
        text = (result.stdout or result.stderr).decode()
        try:
            output = json.loads(text)
        except ValueError:
            output = {"unparsed": text}
        return result.returncode, output

    def head(self):
        return git(self.repo, "rev-parse", "HEAD").decode().strip()

    def remote_head(self):
        return git(self.seed, "ls-remote", "origin", "refs/heads/main").decode().split()[0]

    def status(self):
        return git(self.repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")

    def ledger(self):
        return git(self.repo, "show", "HEAD:" + LEDGER)

    def advance(self, *, touched=False, ledger=False, raw_append=None):
        git(self.seed, "fetch", "origin")
        git(self.seed, "merge", "--ff-only", "origin/main")
        name = "control.txt" if touched else "unrelated.txt"
        write(self.seed / name, b"intervening repository change\n")
        paths = [name]
        if ledger or raw_append is not None:
            with (self.seed / LEDGER).open("ab") as out:
                out.write(raw_append if raw_append is not None else UNRELATED_ROW)
            paths += [LEDGER]
        git(self.seed, "add", "--", *paths)
        git(self.seed, "commit", "-m", "Unrelated or conflicting fixture advance")
        git(self.seed, "push", "origin", "main")

    def reject_pushes(self):
        hook = self.remote / "hooks" / "pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)

    def allow_pushes(self):
        (self.remote / "hooks" / "pre-receive").unlink()

    def applications(self):
        return git(self.repo, "log", "--format=%H", "--fixed-strings", "--grep=Value-Logic-Package: " + self.manifest["package_id"]).decode().splitlines()


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="value-logic-p306-fixture-")
        self.f = Fixture(Path(self.temp.name))

    def tearDown(self):
        self.temp.cleanup()

    def success(self, expected="published"):
        code, out = self.f.call()
        self.assertEqual((code, out.get("status")), (0, expected), out)
        self.assertEqual(self.f.status(), b"")
        return out

    def rejected_unchanged(self, *extra, override=True, expected_sha=None):
        before = (self.f.head(), self.f.status(), (self.f.repo / LEDGER).read_bytes(), (self.f.repo / "control.txt").read_bytes())
        code, out = self.f.call(*extra, override=override, expected_sha=expected_sha)
        self.assertEqual((code, out.get("status")), (2, "aborted"), out)
        self.assertEqual((self.f.head(), self.f.status(), (self.f.repo / LEDGER).read_bytes(), (self.f.repo / "control.txt").read_bytes()), before)
        return out

    def test_new_apply_and_idempotence(self):
        out = self.success()
        first = self.f.head()
        self.assertEqual(first, self.f.remote_head())
        self.assertEqual(self.f.ledger(), self.f.base_ledger + APPEND)
        self.assertEqual(out["application_commit"], first)
        self.success("already_published")
        self.assertEqual(self.f.head(), first)
        self.assertEqual(len(self.f.applications()), 1)
        self.assertEqual(self.f.ledger(), self.f.base_ledger + APPEND)

    def test_check_only_does_not_apply_or_fast_forward(self):
        self.f.advance(ledger=True)
        before = self.f.head()
        code, out = self.f.call("--check-only")
        self.assertEqual((code, out.get("status")), (0, "verified_only"), out)
        self.assertEqual(self.f.head(), before)
        self.assertEqual(self.f.ledger(), self.f.base_ledger)

    def test_unrelated_advance_and_ledger_append_preserved(self):
        self.f.advance(ledger=True)
        previous_remote = self.f.remote_head()
        self.success()
        self.assertEqual(self.f.ledger(), self.f.base_ledger + UNRELATED_ROW + APPEND)
        self.assertEqual((self.f.repo / "unrelated.txt").read_bytes(), b"intervening repository change\n")
        receipt = json.loads((self.f.repo / RECEIPT).read_bytes())
        self.assertEqual(receipt["before_commit"], previous_remote)
        self.assertEqual(receipt["ledger_prefix_bytes"], len(self.f.base_ledger + UNRELATED_ROW))

    def test_touched_path_conflict_before_fast_forward(self):
        self.f.advance(touched=True)
        self.rejected_unchanged()

    def test_dirty_tracked_and_untracked_state(self):
        write(self.f.repo / "control.txt", b"user edits\n")
        git(self.f.repo, "add", "control.txt")
        write(self.f.repo / "user-untracked.txt", b"keep\n")
        self.rejected_unchanged()

    def test_tampered_zip_external_hash(self):
        self.rejected_unchanged(expected_sha="0" * 64)

    def test_tampered_member_even_with_new_zip_hash(self):
        self.f.members["payload/control.txt"] = b"tampered\n"
        self.f.save()
        self.rejected_unchanged()

    def test_duplicate_interval_relabel_is_rejected(self):
        first = APPEND.splitlines(keepends=True)[0].replace(b",E,R,", b",O,,").replace(b",first\n", b",renamed\n")
        self.f.advance(raw_append=first)
        self.rejected_unchanged()

    def test_partial_append_without_receipt_is_rejected(self):
        self.f.advance(raw_append=APPEND.splitlines(keepends=True)[0])
        self.rejected_unchanged()

    def test_overlapping_different_end_time_is_rejected(self):
        row = APPEND.splitlines(keepends=True)[0].replace(b"00:00:10", b"00:00:05")
        self.f.advance(raw_append=row)
        self.rejected_unchanged()

    def test_rejected_push_then_retry_uses_same_commit(self):
        self.f.reject_pushes()
        code, out = self.f.call()
        self.assertEqual((code, out.get("status")), (3, "committed_pending_push"), out)
        first = self.f.head()
        self.assertNotEqual(first, self.f.remote_head())
        self.f.allow_pushes()
        self.success()
        self.assertEqual(self.f.head(), first)
        self.assertEqual(len(self.f.applications()), 1)
        self.assertEqual(self.f.ledger(), self.f.base_ledger + APPEND)

    def test_failed_push_then_unrelated_remote_and_ledger_advance(self):
        self.f.reject_pushes()
        code, out = self.f.call()
        self.assertEqual(code, 3, out)
        original_application = self.f.head()
        self.f.allow_pushes()
        self.f.advance(ledger=True)
        self.success()
        self.assertEqual(self.f.applications(), [original_application])
        self.assertEqual(self.f.ledger(), self.f.base_ledger + UNRELATED_ROW + APPEND)
        self.assertEqual((self.f.repo / "unrelated.txt").read_bytes(), b"intervening repository change\n")
        merged_head = self.f.head()
        self.success("already_published")
        self.assertEqual(self.f.head(), merged_head)

    def test_failed_push_then_touched_remote_conflict(self):
        self.f.reject_pushes()
        code, out = self.f.call()
        self.assertEqual(code, 3, out)
        self.f.allow_pushes()
        self.f.advance(touched=True)
        self.rejected_unchanged()
        self.assertEqual(self.f.ledger(), self.f.base_ledger + APPEND)

    def test_later_published_touched_changes_are_not_overwritten(self):
        self.success()
        original = self.f.head()
        self.f.advance(touched=True, ledger=True)
        self.success("already_published")
        self.assertEqual(self.f.applications(), [original])
        self.assertEqual((self.f.repo / "control.txt").read_bytes(), b"intervening repository change\n")
        self.assertEqual(self.f.ledger(), self.f.base_ledger + APPEND + UNRELATED_ROW)

    def test_non_github_remote_requires_marked_explicit_fixture_override(self):
        self.rejected_unchanged(override=False)

    def test_unrelated_unpublished_local_commit_not_pushed(self):
        write(self.f.repo / "local.txt", b"user local commit\n")
        git(self.f.repo, "add", "local.txt")
        git(self.f.repo, "commit", "-m", "User local work")
        self.rejected_unchanged()
        self.assertEqual(self.f.remote_head(), self.f.base)

    def test_commit_hook_rejection_rolls_back_owned_writes(self):
        hook = self.f.repo / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        self.rejected_unchanged()
        self.assertFalse((self.f.repo / "new.txt").exists())
        self.assertFalse((self.f.repo / RECEIPT).exists())

    def test_git_blob_hashes_with_crlf_checkout(self):
        git(self.f.repo, "config", "core.autocrlf", "true")
        (self.f.repo / "control.txt").unlink()
        (self.f.repo / LEDGER).unlink()
        git(self.f.repo, "restore", "--worktree", "control.txt", LEDGER)
        self.assertIn(b"\r\n", (self.f.repo / LEDGER).read_bytes())
        self.success()
        self.assertEqual(self.f.ledger(), self.f.base_ledger + APPEND)
        self.success("already_published")

    def test_executable_postimage_mode_is_explicit(self):
        self.f.manifest["files"][1]["after_mode"] = "100755"
        self.f.save()
        git(self.f.repo, "config", "core.fileMode", "false")
        self.success()
        self.assertTrue(git(self.f.repo, "ls-tree", "HEAD", "new.txt").startswith(b"100755"))

    def test_wrong_base_ancestry_is_rejected(self):
        git(self.f.repo, "switch", "-c", "fixture-side")
        write(self.f.repo / "side.txt", b"side history\n")
        git(self.f.repo, "add", "side.txt")
        git(self.f.repo, "commit", "-m", "Side base is not main ancestor")
        side = self.f.head()
        git(self.f.repo, "switch", "main")
        self.f.manifest["base_commit"] = side
        self.f.save()
        self.rejected_unchanged()

    def test_retry_merge_hook_cannot_publish_undeclared_file(self):
        self.f.reject_pushes()
        code, out = self.f.call()
        self.assertEqual(code, 3, out)
        self.f.allow_pushes()
        self.f.advance()
        remote_before = self.f.remote_head()
        hook = self.f.repo / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\nprintf 'hook addition\\n' > hook-extra.txt\ngit add hook-extra.txt\n", encoding="utf-8")
        hook.chmod(0o755)
        code, out = self.f.call()
        self.assertEqual((code, out.get("status")), (2, "aborted"), out)
        self.assertEqual(self.f.remote_head(), remote_before)
        self.assertEqual(len(self.f.applications()), 1)
        self.assertEqual(self.f.status(), b"")
        self.rejected_unchanged()

    def test_companion_helper_must_match_verified_zip(self):
        self.f.members["apply_package.py"] += b"\n# altered archive helper\n"
        self.f.manifest["members"]["apply_package.py"] = sha(self.f.members["apply_package.py"])
        self.f.save()
        self.rejected_unchanged()

    def test_traversal_target_rejected_before_mutation(self):
        self.f.manifest["files"][1]["path"] = "../outside.txt"
        self.f.save()
        self.rejected_unchanged()
        self.assertFalse((self.f.root / "outside.txt").exists())

    def test_existing_delivery_lock_blocks_duplicate_invocation(self):
        lock = self.f.repo / ".git" / "value_logic_p306_delivery.lock"
        lock.write_bytes(b"another invocation\n")
        self.rejected_unchanged()
        self.assertEqual(lock.read_bytes(), b"another invocation\n")


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"test": test.id().split(".")[-1], "status": "PASS"})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append({"test": test.id().split(".")[-1], "status": "FAIL", "detail": "".join(traceback.format_exception(*err))})

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append({"test": test.id().split(".")[-1], "status": "ERROR", "detail": "".join(traceback.format_exception(*err))})


def main():
    runs = HERE / "test_runs"
    runs.mkdir(exist_ok=True)
    index = 1
    while (runs / ("run_%03d" % index)).exists():
        index += 1
    target = runs / ("run_%03d" % index)
    snapshot = target / "source_snapshot"
    snapshot.mkdir(parents=True)
    hashes = {}
    for name in ("apply_package.py", "Apply-And-Push.ps1", "test_apply_package.py"):
        raw = (HERE / name).read_bytes()
        (snapshot / name).write_bytes(raw)
        hashes[name] = sha(raw)
    start = time.monotonic()
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DeliveryTests)
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=RecordingResult).run(suite)
    report = {
        "schema": "value_logic.p306.delivery_tests.v1", "result": "PASS" if result.wasSuccessful() else "FAIL",
        "tests_run": result.testsRun, "failed": len(result.failures), "errors": len(result.errors),
        "elapsed_seconds_operational_only": time.monotonic() - start,
        "principal_research_credit_seconds": 0, "live_repository_committed_or_pushed": False,
        "remotes": "marked temporary local bare fixtures only", "source_sha256": hashes,
        "python": sys.version, "git": subprocess.run(["git", "--version"], capture_output=True, text=True, check=True).stdout.strip(),
        "pwsh_available": shutil.which("pwsh") is not None, "windows_runtime_tested": False,
        "cases": result.records,
    }
    (target / "results.json").write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (target / "test_output.txt").write_text(stream.getvalue(), encoding="utf-8")
    print(json.dumps({"result": report["result"], "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "evidence": str(target)}, indent=2))
    if not result.wasSuccessful():
        print(stream.getvalue())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
