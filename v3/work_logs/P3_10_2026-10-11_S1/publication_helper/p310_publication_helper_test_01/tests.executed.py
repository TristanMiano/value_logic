"""Offline functional/cross-Git tests; no remote call, Git object or index write.

The real repository is read only for immutable baseline objects and prior
publication payloads/receipts. No inventory of current P3-10 files is prepared.
"""
import argparse
from contextlib import redirect_stdout
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import io
import json
from pathlib import Path
import traceback


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    root = Path("/workspace/scratch/095cdac579b7")
    output = Path(args.out).resolve()
    output.mkdir(parents=True, exist_ok=False)
    helper_path = root / "p310_publication_prepare.py"
    spec = importlib.util.spec_from_file_location("p310_publication_prepare", helper_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.write_new(output / "helper.tested.py", helper_path.read_bytes())
    module.write_new(output / "tests.executed.py", Path(__file__).read_bytes())
    module.write_json(output / "start.json", {"utc": datetime.now(timezone.utc).isoformat(), "kind": "OFFLINE PUBLICATION HELPER TEST; NO SCIENTIFIC OR REMOTE EXECUTION", "helper_sha256": sha256(helper_path.read_bytes()).hexdigest(), "principal_credit_ns": 0})
    checks, sources, logs = [], [], []

    def check(label, value):
        checks.append({"check": label, "pass": bool(value)})
        assert value, label

    def read(path):
        data = path.read_bytes()
        sources.append({"path": str(path), "bytes": len(data), "sha256": sha256(data).hexdigest()})
        return data

    def call(function, **kwargs):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = function(argparse.Namespace(**kwargs))
        logs.append({"function": function.__name__, "stdout": buffer.getvalue(), "result": result})
        return result

    def expected_failure(label, function):
        try:
            function()
        except ValueError as error:
            checks.append({"check": label, "pass": True, "expected_rejection": str(error)})
        else:
            check(label, False)

    real_reader_class = module.GitReader
    real_reader = real_reader_class(root / "value_logic")
    initial_head = real_reader.head()
    initial_index = real_reader.index_identity()
    try:
        check("initial real HEAD equals designated base", initial_head == module.DEFAULT_BASE)
        base_tree, base_files = real_reader.baseline(module.DEFAULT_BASE)
        check("actual baseline root and path count", base_tree == "3900e2333e1324af72b0b7f51764bfecc79794ba" and len(base_files) == 8373)
        root_id, root_body = module.make_tree(base_files)
        check("root body matches native Git object", root_body == real_reader.run("cat-file", "tree", base_tree))
        check("native hash-object agrees on root tree", real_reader.run("hash-object", "-t", "tree", "--stdin", data=root_body).strip().decode() == root_id)
        blob_cases = [b"", b"CRLF\r\nno final LF", b"\xef\xbb\xbfUTF-8 BOM\r\n", "λ/漢字/🙂\n".encode(), b"\x00\xff\x80binary", b"\x89PNG\r\n\x1a\n\0fixture"]
        for i, data in enumerate(blob_cases):
            check("native exact blob hash " + str(i), real_reader.run("hash-object", "--no-filters", "--stdin", data=data).strip().decode() == module.git_id("blob", data))
        expected_failure("write-capable Git command rejected by reader", lambda: real_reader.run("hash-object", "-w", "--stdin", data=b"not installed"))

        # All completed P3-09 upload/overlay objects have independent saved SHA
        # expectations plus observed returned receipts.
        upload_index = json.loads(read(root / "p309_upload_index.json"))
        receipts = {r["index"]: r for r in json.loads(read(root / "p309_upload_receipts.json"))}
        legacy_blobs = set()
        for row in upload_index:
            payload = json.loads(read(Path(row["path"])))
            if row["kind"] == "tree":
                actual = module.content_tree_id(payload["tree_elements"])
                legacy_blobs.update(e["path"] for e in payload["tree_elements"])
            else:
                data = module.base64.b64decode(payload["content"], validate=True)
                actual = module.git_id("blob", data)
                legacy_blobs.add(actual)
            check("prior P3-09 upload/receipt " + str(row["index"]), actual == row["expected_sha"] == receipts[row["index"]]["sha"] and receipts[row["index"]]["verified"])
        check("all 20 uploads and 164 distinct blobs checked", len(upload_index) == 20 and len(legacy_blobs) == 164)
        prior = json.loads(read(root / "p309_publish_state.json"))
        original_tree, original_files = real_reader.baseline(prior["base_commit"])
        check("prior immutable baseline tree", original_tree == prior["base_tree"])
        tree_index = json.loads(read(root / "p309_tree_index.json"))
        tree_receipts = {r["index"]: r for r in json.loads(read(root / "p309_tree_receipts.json"))}
        previous, current = original_tree, dict(original_files)
        for row in tree_index:
            payload = json.loads(read(Path(row["path"])))
            check("prior overlay base " + str(row["index"]), payload["base_tree_sha"] == row["base_tree"] == previous)
            for entry in payload["tree_elements"]:
                current[entry["path"]] = {k: entry[k] for k in ["mode", "type", "sha"]}
            previous = module.make_tree(current)[0]
            check("prior overlay/receipt " + str(row["index"]), previous == row["expected_tree"] == tree_receipts[row["index"]]["sha"])
        check("prior final tree exact", previous == prior["tree_sha"] == base_tree and current == base_files)
        api_path = root / "value_logic/v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/publication_preflight_v1/remote_commit_get_receipt.json"
        commit, raw_commit = module.remote_commit_payload(read(api_path))
        check("prior API-created commit bytes exact", commit["sha"] == initial_head and raw_commit == real_reader.run("cat-file", "commit", initial_head))
        check("prior API commit native hash", real_reader.run("hash-object", "-t", "commit", "--stdin", data=raw_commit).strip().decode() == initial_head)

        # Synthetic worktree, including deletion/file-to-directory conversion.
        # The injected read-only facade is used ONLY for these offline cases.
        work = output / "synthetic_worktree"
        work.mkdir()
        old_data = {"keep.txt": b"baseline\r\n", "old.txt": b"old\n", "gone.txt": b"gone", "swap": b"file becomes directory", "run.sh": b"#!/bin/sh\necho fixture\n", "a/file": b"a", "a.c": b"c"}
        old_modes = {p: "100644" for p in old_data}
        synthetic_base = {p: {"mode": old_modes[p], "type": "blob", "sha": module.git_id("blob", data)} for p, data in old_data.items()}
        old_by_id = {module.git_id("blob", b): b for b in old_data.values()}
        for name, data in old_data.items():
            if name not in {"gone.txt", "swap"}:
                module.write_new(work / name, data)
        (work / "old.txt").write_bytes(b"modified\r\n")
        (work / "run.sh").chmod(0o755)
        unicode_data = b"\xef\xbb\xbf" + "λ漢字\r\nlast line".encode("utf-8")
        new_data = {"duplicate.txt": old_data["keep.txt"], "unicode.md": unicode_data, "unicode_copy.md": unicode_data, "image.PNG": b"\x89PNG\r\n\x1a\n\0offline fixture", "large.json": b'{"value":"' + b"x" * 2500 + b'"}', "nul.bin": b"a\0b", "invalid_utf8.bin": b"\xff\x80bytes", "swap/nested.txt": b"new directory member", ".ignored.tmp": b"must stay untracked and ignored"}
        for name, data in new_data.items():
            module.write_new(work / name, data)
        (work / "link").symlink_to("keep.txt")

        class OfflineReader:
            def __init__(self, repo):
                self.repo = Path(repo).resolve()
                assert self.repo == work

            def head(self):
                return "1" * 40

            def index_identity(self):
                return {"bytes": 0, "sha256": sha256(b"").hexdigest()}

            def baseline(self, commit):
                assert commit == "1" * 40
                return module.make_tree(synthetic_base)[0], synthetic_base

            def paths(self):
                current = {str(p.relative_to(work)) for p in work.rglob("*") if (p.is_file() or p.is_symlink()) and p.name != ".ignored.tmp"}
                return current | set(synthetic_base)

            def run(self, command, *args, **kwargs):
                assert command == "cat-file" and args[0] == "blob"
                return old_by_id[args[1]]

        module.GitReader = OfflineReader
        prepare_args = dict(repo=str(work), base="1" * 40, repository="example/offline-test", cap_bytes=1024, entry_cap=2, overlay_cap=3)
        expected_failure("deletions are refused by default", lambda: call(module.prepare, **prepare_args, out=str(output / "expected_deletion_denial"), allow_deletions=False))
        plan_dir = output / "synthetic_plan"
        call(module.prepare, **prepare_args, out=str(plan_dir), allow_deletions=True)
        call(module.verify, plan=str(plan_dir), working_tree=True)
        plan_root, plan, indexes = module.load_plan(plan_dir)
        inventory = json.loads((plan_dir / "inventory.json").read_bytes())
        blobs = {r["sha"]: r for r in json.loads((plan_dir / "blob_index.json").read_bytes())}
        check("baseline and cross-file deduplication", plan["baseline_reused_blobs"] == 2 and len(blobs[module.git_id("blob", unicode_data)]["paths"]) == 2)
        check("all new path and mode identities preserved", any(r["path"] == "run.sh" and r["mode"] == "100755" for r in inventory) and any(r["path"] == "link" and r["mode"] == "120000" for r in inventory))
        check("ignored file excluded", all(r["path"] != ".ignored.tmp" for r in inventory))
        check("two explicit deletions retained", plan["deleted_paths"] == 2)
        for row in indexes["upload"]:
            payload = json.loads((plan_dir / row["path"]).read_bytes())
            if row["kind"] == "tree":
                check("synthetic inline cap/entry cap " + str(row["index"]), row["request_bytes"] <= 1024 and len(payload["tree_elements"]) <= 2)
            else:
                check("synthetic binary/oversize base64 " + str(row["index"]), payload["encoding"] == "base64")
        check("large UTF-8 object is an individual base64 request", any(r["reason"] == "oversized UTF-8 blob, exact base64" for r in indexes["upload"]))

        results_dir = output / "synthetic_tool_results"
        results_dir.mkdir()

        def tool_result(name, identity, **extra):
            body = {"sha": identity, "synthetic_fixture": True}
            wrapped = {"content": [{"type": "text", "text": "Action completed."}], "structuredContent": {"content": json.dumps(body), "structuredContent": {"content": json.dumps(body)}}, **extra}
            path = results_dir / name
            module.write_json(path, wrapped)
            return str(path)

        early_overlay = tool_result("early_overlay.json", indexes["overlay"][0]["expected_sha"])
        check("unverified overlay predecessor denied with retained result", call(module.record, plan=str(plan_dir), phase="overlay", index=0, result=early_overlay) == 2)
        first_upload = indexes["upload"][0]
        wrong = tool_result("wrong_sha.json", "0" * 40)
        check("wrong upload SHA rejected", call(module.record, plan=str(plan_dir), phase="upload", index=0, result=wrong) == 2)
        flagged = tool_result("error_flag.json", first_upload["expected_sha"], isError=True)
        check("error flag wins over matching SHA", call(module.record, plan=str(plan_dir), phase="upload", index=0, result=flagged) == 2)
        for row in indexes["upload"]:
            path = tool_result("upload_" + str(row["index"]) + ".json", row["expected_sha"])
            check("resumable valid upload " + str(row["index"]), call(module.record, plan=str(plan_dir), phase="upload", index=row["index"], result=path) == 0)
        call(module.status_report, plan=str(plan_dir), limit=4, out=str(output / "progress_after_uploads.json"))
        status = json.loads((output / "progress_after_uploads.json").read_bytes())
        check("status advances to first unverified overlay", status["next_phase"] == "overlay" and status["next"][0]["index"] == 0)
        for row in indexes["overlay"]:
            path = tool_result("overlay_" + str(row["index"]) + ".json", row["expected_sha"])
            check("dependent valid overlay " + str(row["index"]), call(module.record, plan=str(plan_dir), phase="overlay", index=row["index"], result=path) == 0)
        call(module.status_report, plan=str(plan_dir), limit=4, out=str(output / "completed_receipt_status.json"))
        status = json.loads((output / "completed_receipt_status.json").read_bytes())
        check("all receipt phases complete without publication claim", status["status"] == "UPLOAD_AND_OVERLAY_RECEIPTS_COMPLETE" and status["publication_or_ref_verified"] is False)
        call(module.verify, plan=str(plan_dir), working_tree=True)

        before = (work / "old.txt").read_bytes()
        (work / "old.txt").write_bytes(b"changed after plan")
        expected_failure("later working-byte change rejected", lambda: call(module.verify, plan=str(plan_dir), working_tree=True))
        (work / "old.txt").write_bytes(before)
        extra = work / "new_after_plan.txt"
        extra.write_bytes(b"post-plan path")
        expected_failure("later new file rejected", lambda: call(module.verify, plan=str(plan_dir), working_tree=True))
        extra.unlink()
        first_payload = plan_dir / first_upload["path"]
        before_payload = first_payload.read_bytes()
        first_payload.write_bytes(before_payload + b" ")
        expected_failure("modified request bytes rejected", lambda: call(module.verify, plan=str(plan_dir), working_tree=False))
        first_payload.write_bytes(before_payload)
        call(module.verify, plan=str(plan_dir), working_tree=True)

        message = "Synthetic commit, never created remotely"
        raw_expected = ("tree " + plan["final_tree"] + "\nparent " + "1" * 40 + "\nauthor A <a@example.invalid> 0 +0000\ncommitter B <b@example.invalid> 1 +0000\n\n" + message + "\n").encode()
        fake_commit = {"sha": module.git_id("commit", raw_expected), "tree": {"sha": plan["final_tree"]}, "parents": [{"sha": "1" * 40}], "author": {"name": "A", "email": "a@example.invalid", "date": "1970-01-01T00:00:00Z"}, "committer": {"name": "B", "email": "b@example.invalid", "date": "1970-01-01T00:00:01Z"}, "message": message, "verification": {"signature": None, "payload": None, "reason": "unsigned"}}
        fake_path = output / "synthetic_commit_response.json"
        module.write_json(fake_path, fake_commit)
        install = output / "future_install_instructions"
        call(module.commit_payload, plan=str(plan_dir), response=str(fake_path), out=str(install))
        check("remote metadata and terminal newline reconstructed", (install / "commit.raw").read_bytes() == raw_expected)
        check("no temporary index actually installed", not (install / "temporary.index").exists())
        check("synthetic native commit hash", real_reader.run("hash-object", "-t", "commit", "--stdin", data=raw_expected).strip().decode() == fake_commit["sha"])
        fake_commit["verification"]["signature"] = "synthetic signed case"
        expected_failure("signed commit cannot be silently reconstructed unsigned", lambda: module.remote_commit_payload(json.dumps(fake_commit).encode()))
        expected_failure("output within checkout prohibited", lambda: module.outside_checkout(work / "bad_output", work))
        expected_failure("unsafe repository path prohibited", lambda: module.safe_path("../escape"))
        check("all intentional receipt failures retained", len(list((plan_dir / "receipts").glob("*/*/attempt_*/receipt.json"))) == len(indexes["upload"]) + len(indexes["overlay"]) + 3)

        module.GitReader = real_reader_class
        check("real HEAD unchanged", real_reader.head() == initial_head)
        check("real index exact bytes unchanged", real_reader.index_identity() == initial_index)
        module.write_json(output / "function_logs.json", logs)
        result = {"status": "PASS", "completed_utc": datetime.now(timezone.utc).isoformat(), "helper_sha256": sha256(helper_path.read_bytes()).hexdigest(), "checks_total": len(checks), "checks": checks, "prior_uploads_checked": 20, "prior_blobs_checked": 164, "prior_overlays_checked": 3, "real_baseline_paths_reconstructed": len(base_files), "prior_remote_commit_reconstructed": initial_head, "synthetic_upload_requests": len(indexes["upload"]), "synthetic_overlay_requests": len(indexes["overlay"]), "sources": sources, "real_head_before_and_after": initial_head, "real_index_before_and_after": initial_index, "live_p310_inventory_prepared": False, "network_calls": 0, "git_data_writes": 0, "paid_or_scientific_executions": 0, "principal_research_credit_ns": 0}
        module.write_json(output / "results.json", result)
        print(json.dumps({"status": "PASS", "checks": len(checks), "result_sha256": sha256((output / "results.json").read_bytes()).hexdigest(), "helper_sha256": result["helper_sha256"]}))
    except BaseException as error:
        module.GitReader = real_reader_class
        module.write_json(output / "failure.json", {"recorded_utc": datetime.now(timezone.utc).isoformat(), "type": type(error).__name__, "message": str(error), "traceback": traceback.format_exc(), "checks": checks, "function_logs": logs, "sources": sources, "network_calls": 0, "git_data_writes": 0})
        raise


if __name__ == "__main__":
    main()
