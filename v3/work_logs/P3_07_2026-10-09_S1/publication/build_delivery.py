"""Build a final P3-07 delta archive from reviewed, closed working files.

Adapted from the retained P3-06 builder. Contributor: ChatGPT (GPT-6 Astra Pro),
2026-10-09. Operational work only, with zero principal Research90 credit.
Usage: python build_delivery.py /absolute/new/output/directory
The output directory must be new and outside the checkout. This never commits
or publishes. Final invocation belongs to the principal after accounting closes.
"""
from pathlib import Path
import csv
import hashlib
import importlib.util
import io
import json
import stat
import subprocess
import sys
import zipfile

REPO = Path(__file__).resolve().parents[4]
BASE = "c7386f115bf60a9eb3a419515c844b81fc6ba073"
SESSION = "v3/work_logs/P3_07_2026-10-09_S1"
PUBLICATION = SESSION + "/publication"
BASE_LEDGER_BYTES = 132_993
BASE_LEDGER_SHA256 = "6bcac52c02ed1a154646422352e2bdd3b66d734a808e118cac5b697c85503bf4"
EXPECTED_RESEARCH_NS = 5_411_261_238_724
CONTROLS = {"TODO_v3.md", "v3/README.md", "v3/claim_ledger.md", "v3/plan.v1.json"}
NEW_PREFIXES = (SESSION + "/", "v3/checks/07_", "v3/derivations/07_", "v3/literature/07_")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def names(data):
    return {p.decode("utf-8") for p in data.split(b"\0") if p}


def allowed_target(path):
    return path in CONTROLS or path == SESSION + ".md" or path.startswith(NEW_PREFIXES)


def final_records():
    require(json.loads((REPO / SESSION / "clock_state.json").read_text()) is None,
            "The principal clock must be stopped before final packaging.")
    actuals = json.loads((REPO / SESSION / "actuals.json").read_text())
    require(actuals.get("schema") == "value_logic.p307.actuals.v1", "Wrong actuals schema.")
    require(actuals.get("task") == "P3-07" and actuals.get("base_commit") == BASE,
            "Actuals must identify this P3-07 task and inspected base.")
    require(actuals.get("clock_stopped") is True, "Actuals must record a stopped clock.")
    require(type(actuals.get("research_ns")) is int and actuals["research_ns"] == EXPECTED_RESEARCH_NS,
            "Actuals differ from the principal's stated final research total.")
    require(actuals.get("research_floor_satisfied") is True, "Actuals must satisfy Research90.")
    require(isinstance(actuals.get("research_minutes"), str) and actuals["research_minutes"],
            "Use the finalized actuals' displayed research minutes.")
    readiness = REPO / SESSION / "readiness_audit.md"
    require(readiness.is_file() and readiness.stat().st_size > 0, "Readiness review is required.")
    accounting_path = REPO / SESSION / "reviews/boundary_accounting_review.json"
    require(accounting_path.is_file(), "Final boundary/accounting review is required.")
    accounting = json.loads(accounting_path.read_text())
    require(accounting.get("verdict") == "PASS", "Boundary/accounting review must pass.")
    require(accounting.get("task") == "P3-07" and accounting.get("base_commit") == BASE,
            "Boundary/accounting review must identify this task and base.")
    return actuals


def main():
    require(len(sys.argv) == 2, "Usage: python build_delivery.py /absolute/new/output/directory")
    out = Path(sys.argv[1]).resolve()
    require(not out.exists(), "Preserve earlier packages; choose a new output directory.")
    require(not out.is_relative_to(REPO), "Keep delivery outputs outside the checkout.")
    require(git("rev-parse", "HEAD").decode().strip() == BASE, "Checkout HEAD differs from the inspected base.")
    actuals = final_records()
    ledger_path = "v3/time_ledger.csv"
    append_path = SESSION + "/ledger_append.csv"
    receipt_path = PUBLICATION + "/applied_package.json"
    require(not (REPO / receipt_path).exists(), "An application receipt cannot be a prebuilt payload.")
    base_ledger = git("show", BASE + ":" + ledger_path)
    append = (REPO / append_path).read_bytes()
    require(len(base_ledger) == BASE_LEDGER_BYTES and sha(base_ledger) == BASE_LEDGER_SHA256,
            "The base time-ledger prefix differs from the reviewed bytes.")
    final_ledger = (REPO / ledger_path).read_bytes()
    require(final_ledger == base_ledger + append, "The working ledger must equal base plus the exact append.")
    ledger_actuals = actuals["ledger"]
    require(ledger_actuals.get("base_bytes") == len(base_ledger)
            and ledger_actuals.get("base_sha256") == sha(base_ledger), "Actuals base-ledger identity mismatch.")
    require(type(ledger_actuals.get("append_bytes")) is int
            and ledger_actuals["append_bytes"] == len(append), "Actuals append-byte count mismatch.")
    require(sha(append) == ledger_actuals.get("append_sha256"), "Actuals append hash mismatch.")
    require(sha(final_ledger) == ledger_actuals.get("result_sha256"), "Actuals final-ledger hash mismatch.")
    append_rows = list(csv.reader(io.StringIO(append.decode("utf-8"), newline=""), strict=True))
    require(type(ledger_actuals.get("append_rows")) is int
            and len(append_rows) == ledger_actuals["append_rows"] > 0,
            "The final append's row count must match actuals; no row count is hardcoded.")
    tree = {}
    for record in git("ls-tree", "-r", "-z", "--full-tree", BASE).split(b"\0"):
        if record:
            meta, path = record.split(b"\t", 1)
            tree[path.decode()] = tuple(meta.decode().split())
    selected = names(git("diff", "--name-only", "--no-renames", "-z", BASE, "--"))
    selected |= names(git("ls-files", "--others", "--exclude-standard", "-z"))
    selected.discard(ledger_path)
    unexpected = sorted(p for p in selected if not allowed_target(p))
    require(not unexpected, "Unexpected changed paths require review: " + repr(unexpected))
    require(append_path in selected and receipt_path not in selected, "Missing append or unexpected receipt payload.")
    require((REPO / "README.md").read_bytes() == git("show", BASE + ":README.md"), "Preserve the root README.")
    new_preimages = sorted(p for p in selected if p not in CONTROLS and p in tree)
    require(not new_preimages, "P3-07 artifacts must be new at the base: " + repr(new_preimages))
    members = {name: (REPO / PUBLICATION / name).read_bytes()
               for name in ("apply_package.py", "Apply-And-Push.ps1")}
    members["README.md"] = f"""# Value Logic P3-07 guarded delivery

This is a guarded change package for TristanMiano/value_logic, based on main
{BASE}. It contains reviewed P3-07 sources, documentation, worklog evidence,
the permitted project-control updates, and the exact {len(append_rows)}-row,
{len(append)}-byte time-ledger append. The root repository README is preserved.

The finalized principal actuals record {actuals['research_minutes']} observed
Research90 minutes. This builder does not infer time or grant research credit.
Read the included readiness and accounting reviews for the final task judgment.
All experiments remain development. This package does not start P3-B, P3-08,
or any later research task.

Keep this ZIP and both root helper files outside a clean clone of main. Obtain
the ZIP SHA-256 from the delivery message. From PowerShell, use:

```powershell
.\\Apply-And-Push.ps1 -Repository 'C:\\work\\value_logic' `
  -PackageZip 'C:\\Downloads\\value_logic_P3_07_delivery.zip' `
  -ExpectedZipSha256 'THE_64_CHARACTER_HASH_IN_THE_DELIVERY_MESSAGE'
```

Add -CheckOnly for package/repository preflight with a fresh remote fetch and
no worktree application. Python 3.10+, Git and PowerShell 5.1+ are required.
Existing authentication and Git identity are used. No execution-policy or
credential changes are made.

The helper checks the exact ZIP, all members, the P3-07 target allowlist,
touched Git blobs and ledger intervals. It preserves unrelated main changes
and valid intervening ledger appends, rejects touched conflicts, and supports
retry of an already-created application commit. It never force-pushes. A local
receipt is not proof of remote publication. Guarded-helper tests use temporary
local bare Git remotes. PowerShell has not been executed on Windows.

Read payload/{SESSION}.md for the research record and
payload/{PUBLICATION}/README.md for package, conflict and retry semantics.
The manifest hashes every other member. The final full-payload check and
publication verification are separate principal-owned operational steps.
""".encode("utf-8")
    files = []
    for path in sorted(selected):
        source = REPO / path
        require(not source.is_symlink(), "A payload target cannot be a symlink: " + path)
        old = tree.get(path)
        if old:
            before_mode, kind, oid = old
            require(kind == "blob" and before_mode in ("100644", "100755"), "Unsupported base Git entry: " + path)
            before_sha = sha(git("cat-file", "blob", oid))
        else:
            before_mode = before_sha = None
        if source.exists():
            require(source.is_file(), "Payload must be a regular file: " + path)
            data = source.read_bytes()
            payload = "payload/" + path
            members[payload] = data
            after_sha = sha(data)
            after_mode = "100755" if source.stat().st_mode & stat.S_IXUSR else "100644"
        else:
            require(old is not None, "A missing payload has no base preimage: " + path)
            payload = after_sha = after_mode = None
        files.append(dict(path=path, before_sha256=before_sha, before_mode=before_mode,
                          after_sha256=after_sha, after_mode=after_mode, payload=payload))
    manifest = dict(schema="value_logic.p307.delivery.v1", package_id="value-logic-p307-completion-20261009-v1",
                    repository="https://github.com/TristanMiano/value_logic.git", branch="main", base_commit=BASE,
                    commit_subject="Complete P3-07 paid-reasoning research and preserve bounded evidence",
                    receipt_path=receipt_path, members={p: sha(b) for p, b in sorted(members.items())}, files=files,
                    ledger=dict(path=ledger_path, base_sha256=sha(base_ledger), base_bytes=len(base_ledger),
                                append_payload="payload/" + append_path, append_sha256=sha(append),
                                append_rows=len(append_rows)))
    # The tested Package class validates the complete manifest contract below.
    # Final packaging does not depend on an optional JSON Schema engine.
    manifest_bytes = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode()
    for entry in files:
        source = REPO / entry["path"]
        unchanged = (not source.exists()) if entry["after_sha256"] is None else sha(source.read_bytes()) == entry["after_sha256"]
        require(unchanged, "Payload changed during final packaging: " + entry["path"])
    require((REPO / ledger_path).read_bytes() == final_ledger, "Ledger changed during final packaging.")
    out.mkdir(parents=True)
    archive = out / "value_logic_P3_07_delivery.zip"
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted({"manifest.json": manifest_bytes, **members}.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    archive_sha = sha(archive.read_bytes())
    spec = importlib.util.spec_from_file_location("p307_delivery", REPO / PUBLICATION / "apply_package.py")
    helper = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helper
    spec.loader.exec_module(helper)
    package = helper.Package(archive, archive_sha)
    require(helper.ledger_after(package, base_ledger, base_ledger) == base_ledger + append,
            "The package's guarded ledger result differs from the finalized append.")
    for name in ("apply_package.py", "Apply-And-Push.ps1", "README.md"):
        (out / name).write_bytes(members[name])
    (out / "manifest.json").write_bytes(manifest_bytes)
    result = dict(archive=str(archive), zip_sha256=archive_sha, zip_bytes=archive.stat().st_size,
                  manifest_sha256=sha(manifest_bytes), ordinary_file_operations=len(files),
                  archive_members=len(members) + 1, ledger_append_rows=len(append_rows),
                  ledger_append_bytes=len(append), research_ns=actuals["research_ns"])
    (out / "build_result.json").write_text(json.dumps(result, indent=2) + "\n")
    (out / "value_logic_P3_07_delivery.sha256").write_text(archive_sha + "  " + archive.name + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
