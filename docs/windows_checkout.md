# Windows checkout recovery and portable evidence

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 11, 2026.
Repair baseline: `af0ebbde86cc545120dc95db99a03b674c3539ae`.

## What caused the error

Nested review snapshots repeated full repository paths inside other snapshots.
The longest tracked path was 243 UTF-16 code units relative to the root, or
279 at `C:\Users\trist\projects\value_logic`. Five files and three implicit
`.gitattributes` lookups exceeded the classic 259-unit usable full-path limit.
Git downloaded the objects successfully, then could not create some files.

The repair moves 32 snapshot locations exceeding the new 200-unit relative
budget into 30 immutable objects under `v3/evidence/objects/`. Every original
snapshot byte is retained, including duplicate identities; canonical sources
remain at their existing paths. The longest remaining tracked path or attribute
lookup is 200 units, or 236 at the checkout root above.

The [relocation manifest](../v3/evidence/relocations.v1.json) binds each old
location to its current object, SHA-256, original Git blob ID, file mode, byte
count and canonical source at migration. The archive's `.gitattributes` prevents
line-ending conversion. Frozen scientific records, results, historical manifests
and research clocks are unchanged. This repair credits no research time.

## Recover the interrupted pull

In PowerShell, enable long paths for this clone and inspect its state:

```powershell
Set-Location 'C:\Users\trist\projects\value_logic'
git config --local core.longpaths true
git status --short --branch
```

If status shows only the branch heading, retrieve the repaired main:

```powershell
git pull --ff-only
git status --short --branch
git log -1 --oneline
```

If status lists modified, deleted or untracked files, or the pull refuses to
proceed, keep that checkout and clone into a new, empty, shorter directory:

```powershell
git clone -c core.longpaths=true --branch main https://github.com/TristanMiano/value_logic.git 'C:\Users\trist\projects\vlfix'
if ($LASTEXITCODE -ne 0) { throw "Clone did not complete." }
Set-Location 'C:\Users\trist\projects\vlfix'
git status --short --branch
git log -1 --oneline
```

The original directory retains any local edits and interrupted-checkout residue.
Open the successful checkout in Codex. Bring across any needed unpublished work
after comparing it with the original directory.

## Locate or reproduce historical snapshots

```text
python tools/evidence_paths.py verify
python tools/evidence_paths.py resolve ORIGINAL_REPOSITORY_RELATIVE_PATH
python tools/evidence_paths.py materialize --destination C:\vl-replay
```

`resolve` prints the verified current file location for an old path in the
manifest. Objects have no extension; their original filenames are in the map.
Historical manifests and references retain their original path identifiers.
The local Markdown checker recognizes mapped targets and checks their archived
bytes and heading anchors. GitHub still renders the preserved original URLs.
For an old relative link to a moved snapshot, resolve its repository-relative
target or view the baseline commit.

`materialize` exports **only the 32 relocated snapshots**, with their original
directory structure, into a short directory outside the working repository.
It verifies bytes before writing, accepts identical existing files and refuses
conflicts. It does not reconstruct a complete execution environment or rerun
an experiment. Historical checkers may bind original roots, source trees and
exclusive output directories; use the baseline commit and its recorded runtime
in an isolated checkout for a full historical replay. Do not add the exported
long paths back to the tracked tree.

## Prevent a recurrence

Use short output paths and avoid recursive repository copies within review
directories. Stage intended changes, then run:

```text
python tools/check_repo_paths.py
python tools/check_repo_paths.py --checkout-root C:\Users\trist\projects\value_logic
python tools/evidence_paths.py verify
python -m unittest verification.test_repo_paths verification.test_evidence_paths verification.test_relocated_links
```

The guard checks the Git index, including virtual ancestor `.gitattributes`
lookups and UTF-16 lengths. `--ref REV` checks a saved revision. The 200-unit
relative budget leaves room for a checkout prefix up to 59 units, including
its separator, under the classic 259-unit file-path limit. For a longer root,
use `--checkout-root` to check that location explicitly. CI runs the guard,
archive verification and focused regression tests on Linux and Windows.

## Official references

- [Git for Windows: long paths and core.longpaths](https://gitforwindows.org/git-cannot-create-a-file-or-directory-with-a-long-path.html)
- [Git clone: configuration applied before the initial checkout](https://git-scm.com/docs/git-clone)
- [Microsoft: maximum file path limitation](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation)
