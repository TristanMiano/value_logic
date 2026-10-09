"""Build the final P3-06 delta archive from reviewed, closed working files.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09. Operational work only.
Usage: python build_delivery.py /absolute/new/output/directory
The output directory must not already exist. This never commits or publishes.
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
BASE = "646f9ece1a2d57eb2029fd27f8df9d9ceb54f2f7"
SESSION = "v3/work_logs/P3_06_2026-10-09_S1"
PUBLICATION = SESSION + "/publication"


def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def names(data):
    return {p.decode("utf-8") for p in data.split(b"\0") if p}


def main():
    out = Path(sys.argv[1]).resolve()
    assert not out.exists(), "Preserve earlier packages; choose a new output directory."
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert json.loads((REPO / SESSION / "clock_state.json").read_text()) is None
    actuals = json.loads((REPO / SESSION / "actuals.json").read_text())
    assert actuals["research_ns"] == 5_412_656_302_543 and actuals["research_floor_satisfied"]
    assert (REPO / SESSION / "reviews/boundary_accounting_review.json").is_file()
    ledger_path = "v3/time_ledger.csv"
    append_path = SESSION + "/ledger_append.csv"
    receipt_path = PUBLICATION + "/applied_package.json"
    assert not (REPO / receipt_path).exists()
    base_ledger = git("show", BASE + ":" + ledger_path)
    append = (REPO / append_path).read_bytes()
    assert len(base_ledger) == 120635
    assert sha(base_ledger) == "8bfb7af2a22551ee18e35b144661dd2e1bf27713027336c4bda6d6ab17a8df4c"
    assert (REPO / ledger_path).read_bytes() == base_ledger + append
    assert sha(append) == actuals["ledger"]["append_sha256"]
    append_rows = list(csv.reader(io.StringIO(append.decode(), newline=""), strict=True))
    assert len(append_rows) == actuals["ledger"]["append_rows"] == 28
    tree = {}
    for record in git("ls-tree", "-r", "-z", "--full-tree", BASE).split(b"\0"):
        if record:
            meta, path = record.split(b"\t", 1)
            tree[path.decode()] = tuple(meta.decode().split())
    selected = names(git("diff", "--name-only", "--no-renames", "-z", BASE, "--"))
    selected |= names(git("ls-files", "--others", "--exclude-standard", "-z"))
    selected.discard(ledger_path)
    controls = {"TODO_v3.md", "v3/README.md", "v3/claim_ledger.md", "v3/plan.v1.json"}
    prefixes = (SESSION+"/", "v3/checks/06_", "v3/derivations/06_", "v3/literature/06_")
    unexpected = sorted(p for p in selected if p not in controls and p != SESSION+".md" and not p.startswith(prefixes))
    assert not unexpected, ("Unexpected changes require review", unexpected)
    assert append_path in selected and receipt_path not in selected
    assert (REPO / "README.md").read_bytes() == git("show", BASE+":README.md")
    members = {name:(REPO / PUBLICATION / name).read_bytes() for name in ("apply_package.py", "Apply-And-Push.ps1")}
    members["README.md"] = ("""# Value Logic P3-06 verified delivery

This is a guarded change package for TristanMiano/value_logic, based on main
646f9ece1a2d57eb2029fd27f8df9d9ceb54f2f7. It contains new and changed files,
the preserved original checkpoint evidence, exact clocks and the 28-row ledger
append. Existing repository files are obtained from the checked base, not
replaced by a partial recovery snapshot.

P3-06 is complete at its finite declared scope. Research90 is satisfied by
90.210938375717 observed minutes. P3-N01 remains NOT YET SUPPORTED; P3-07 and
later gates are unstarted. All experiments remain development.

Keep this ZIP and both root helper files outside a clean clone of main. Obtain
the ZIP SHA-256 from the delivery message. From PowerShell, use:

```powershell
.\\Apply-And-Push.ps1 -Repository 'C:\\work\\value_logic' `
  -PackageZip 'C:\\Downloads\\value_logic_P3_06_delivery.zip' `
  -ExpectedZipSha256 'THE_64_CHARACTER_HASH_IN_THE_DELIVERY_MESSAGE'
```

Add -CheckOnly for a read-only preflight with a fresh remote fetch. Python
3.10+, Git and PowerShell 5.1+ are required. Existing authentication and Git
identity are used. No execution-policy or credential changes are made.

The helper checks the exact ZIP, all members, touched Git blobs and ledger
intervals. It preserves unrelated main changes and valid intervening ledger
appends, rejects touched conflicts, and supports retry of an already-created
application commit. It never force-pushes. A local receipt is not by itself
proof of remote publication. The Python CLI has 31 local bare-Git tests;
PowerShell was source-reviewed, not executed on Windows. The delivered archive
receives a separate full-payload extraction/application check.

Read payload/v3/work_logs/P3_06_2026-10-09_S1.md for the research record and
payload/v3/work_logs/P3_06_2026-10-09_S1/publication/README.md for detailed
conflict, retry and package semantics. The manifest hashes every other member.
""").encode()
    files = []
    for path in sorted(selected):
        source = REPO / path
        assert not source.is_symlink()
        old = tree.get(path)
        if old:
            before_mode, kind, oid = old
            assert kind == "blob" and before_mode in ("100644", "100755")
            before_sha = sha(git("cat-file", "blob", oid))
        else:
            before_mode = before_sha = None
        if source.exists():
            assert source.is_file()
            data = source.read_bytes()
            payload = "payload/" + path
            members[payload] = data
            after_sha = sha(data)
            after_mode = "100755" if source.stat().st_mode & stat.S_IXUSR else "100644"
        else:
            assert old is not None
            payload = after_sha = after_mode = None
        files.append(dict(path=path, before_sha256=before_sha, before_mode=before_mode,
                          after_sha256=after_sha, after_mode=after_mode, payload=payload))
    manifest = dict(schema="value_logic.p306.delivery.v1", package_id="value-logic-p306-completion-20261009-v1",
                    repository="https://github.com/TristanMiano/value_logic.git", branch="main", base_commit=BASE,
                    commit_subject="Complete P3-06 forecasting research and preserve recovery evidence",
                    receipt_path=receipt_path, members={p:sha(b) for p,b in sorted(members.items())}, files=files,
                    ledger=dict(path=ledger_path, base_sha256=sha(base_ledger), base_bytes=len(base_ledger),
                                append_payload="payload/"+append_path, append_sha256=sha(append), append_rows=len(append_rows)))
    import jsonschema
    jsonschema.validate(manifest, json.loads((REPO / PUBLICATION / "manifest.schema.json").read_text()))
    manifest_bytes = (json.dumps(manifest, sort_keys=True, indent=2)+"\n").encode()
    for entry in files:
        source = REPO / entry["path"]
        assert (not source.exists()) if entry["after_sha256"] is None else sha(source.read_bytes()) == entry["after_sha256"]
    out.mkdir(parents=True)
    archive = out / "value_logic_P3_06_delivery.zip"
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted({"manifest.json":manifest_bytes, **members}.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    archive_sha = sha(archive.read_bytes())
    spec = importlib.util.spec_from_file_location("p306_delivery", REPO / PUBLICATION / "apply_package.py")
    helper = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helper
    spec.loader.exec_module(helper)
    package = helper.Package(archive, archive_sha)
    assert helper.ledger_after(package, base_ledger, base_ledger) == base_ledger + append
    for name in ("apply_package.py", "Apply-And-Push.ps1", "README.md"):
        (out / name).write_bytes(members[name])
    (out / "manifest.json").write_bytes(manifest_bytes)
    result = dict(archive=str(archive), zip_sha256=archive_sha, zip_bytes=archive.stat().st_size,
                  manifest_sha256=sha(manifest_bytes), ordinary_file_operations=len(files),
                  archive_members=len(members)+1, ledger_append_rows=len(append_rows))
    (out / "build_result.json").write_text(json.dumps(result, indent=2)+"\n")
    (out / "value_logic_P3_06_delivery.sha256").write_text(archive_sha+"  "+archive.name+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
