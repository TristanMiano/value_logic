# Guarded P3-07 delivery helpers

These are operational publication helpers. They apply an already-reviewed final
package to `TristanMiano/value_logic` and verify normal Git publication. They do
not create scientific conclusions, infer time, calculate Research90 credit,
select a new phase, or start P3-B/P3-08. The principal builds the final ZIP and
manifest after closing the research integration and accounting.

## P3-07 build boundary

The principal owns final accounting, the complete payload, final ZIP creation
and publication. Preparation of these helpers does not build a final ZIP or
create an application receipt. [build_delivery.py](build_delivery.py) is adapted
from the preserved P3-06 builder and must be invoked only after final closure.
It never commits or pushes.

The builder requires the inspected base commit
`c7386f115bf60a9eb3a419515c844b81fc6ba073`, a stopped `clock_state.json`, finalized
P3-07 `actuals.json` with `research_floor_satisfied: true` and the supplied
`research_ns: 5411261238724`, `readiness_audit.md`, and a passing
`reviews/boundary_accounting_review.json` for this task and base. The supplied
research total is 90.187687312067 minutes at the displayed precision; the builder
uses the final actuals' display and does not infer or grant credit.

The base time ledger is exactly **132,993 bytes**, SHA-256
`6bcac52c02ed1a154646422352e2bdd3b66d734a808e118cac5b697c85503bf4`.
The final ledger must equal those exact base bytes plus `ledger_append.csv`.
Its append hash, row count **and byte count** are read from final
`actuals["ledger"]` and checked against the actual CSV bytes. No final row count
is hardcoded. The whole-ledger hash must also match actuals.

Both builder and Python application helper restrict ordinary target operations
to these paths:

| Target | Permitted operation scope |
|---|---|
| `v3/checks/07_*`, `v3/derivations/07_*`, `v3/literature/07_*` | New P3-07 artifacts; no preimage at the declared base. |
| `v3/work_logs/P3_07_2026-10-09_S1/` and its sibling `.md` worklog | New P3-07 session artifacts; no preimage at the declared base. |
| `TODO_v3.md`, `v3/README.md`, `v3/claim_ledger.md`, `v3/plan.v1.json` | Guarded project-control operations with exact before/after identities. |
| `v3/time_ledger.csv` | The dedicated append-only operation, never an ordinary file entry. |
| New JSON receipt under this session's `publication/` directory | Runtime-generated application record, never a prebuilt file entry. |

The repository root `README.md` is preserved. Earlier task sources, documents,
worklogs and receipts are outside the permitted target scope. The builder also
rejects any unexpected changed or untracked target and requires a new output
directory outside the checkout. Guards use explicit runtime checks rather than
Python assertions, so optimization does not disable these preconditions.

## Running a final package

Keep the final ZIP and its extracted root helpers outside the target checkout.
Use a full clone with clean `main`, an existing Git identity, and working GitHub
authentication. Staged, modified and untracked files must be resolved before
application. The scripts do not store credentials or change Git identity,
authentication, hooks, or PowerShell execution policy.
Environment variables selecting another Git repository, index, object directory
or namespace must be unset; this helper operates on the normal checkout and
index only.

The delivery message must provide the ZIP's SHA-256 independently. In PowerShell,
substitute the actual paths and the 64-character hash from that message:

```powershell
.\Apply-And-Push.ps1 `
  -Repository 'C:\work\value_logic' `
  -PackageZip 'C:\Downloads\value_logic_P3_07_delivery.zip' `
  -ExpectedZipSha256 'REPLACE_WITH_THE_DELIVERED_64_CHARACTER_SHA256'
```

An optional `-CheckOnly` performs package and repository preflight, including a
fresh fetch, without updating the worktree, committing or pushing. Supply
`-Python 'C:\Path\To\python.exe'` if automatic discovery does not select the
desired Python 3.10-or-later installation. The PowerShell wrapper requires
PowerShell 5.1 or later and Git must be on `PATH`.

The portable equivalent is:

```text
python apply_package.py --repo /path/to/value_logic --package /path/to/delivery.zip --zip-sha256 DELIVERED_SHA256
```

The wrapper checks the outer ZIP hash and checks both extracted helper files
against their root members in that ZIP before invoking Python. Python repeats
the ZIP check, validates every archive member against the manifest, checks its
own source bytes against the packaged helper, and applies only declared target
paths. Hashes bind the delivered bytes; they do not constitute proof or author
authentication.

## Final ZIP and manifest contract

The root of the ZIP must contain `manifest.json`, `apply_package.py`, and
`Apply-And-Push.ps1`. Payload bytes live under `payload/`. Additional readable
delivery files are allowed if included in the manifest's member hash map. ZIP
directory entries are optional; links, special files, duplicate files,
noncanonical paths, traversal and case-ambiguous paths are rejected. The helper
reads members directly without extracting the archive into the checkout.

[manifest.schema.json](manifest.schema.json) describes the JSON shape. The Python
helper additionally enforces path, mode, hash, cross-field, CSV and Git-history
conditions. The top-level fields are:

| Field | Required meaning |
|---|---|
| `schema` | Exactly `value_logic.p307.delivery.v1`. |
| `package_id` | Stable ID beginning `value-logic-p307-`, followed by lowercase ASCII letters, digits and hyphens. Do not reuse an ID for changed manifest bytes. |
| `repository` | Exactly `https://github.com/TristanMiano/value_logic.git`. |
| `branch` | Exactly `main`. |
| `base_commit` | The inspected full 40-character Git commit ID. It must remain an ancestor of both local and freshly fetched remote main. |
| `commit_subject` | One printable line, at most 200 characters. |
| `receipt_path` | A new JSON path under this P3-07 `publication/` directory, conventionally `applied_package.json`. It must be absent at the base and fresh-application parent. |
| `members` | Map from every ZIP file name except `manifest.json` to the SHA-256 of its exact uncompressed bytes. Include both root helpers and every payload or support file. |
| `files` | List of guarded regular-file operations within the P3-07 target scope above; new artifact paths require null preimages, while the four controls may have preimages. Excludes the time ledger and generated application receipt. |
| `ledger` | The dedicated append-only operation described below. |

Each `files` entry has exactly these fields:

```json
{
  "path": "v3/derivations/07_example.md",
  "before_sha256": null,
  "before_mode": null,
  "after_sha256": "SHA256_OF_EXACT_PAYLOAD_BYTES",
  "after_mode": "100644",
  "payload": "payload/v3/derivations/07_example.md"
}
```

This is a structural example with a placeholder hash, not a usable manifest.
For a permitted control-file replacement, set `before_sha256` to the base Git blob's SHA-256 and
`before_mode` to its Git mode. Only `100644` and `100755` are supported. A missing
file uses null hash and mode. A permitted control-file deletion has null `after_sha256`, `after_mode`
and `payload`, with a present preimage. For each present postimage, its hash
must match both the referenced payload bytes and the member hash map.

The base and current preimages are checked as **Git blob bytes**, independently
of a clean checkout's CRLF conversion. Staged blobs are checked again after Git
filters and executable-mode handling; committed blobs are audited before a
push. Existing Windows reparse-point ancestors and symlink targets are rejected.
No claim of a Windows runtime test accompanies this implementation.

For the final ledger operation, supply exactly:

```json
{
  "path": "v3/time_ledger.csv",
  "base_sha256": "SHA256_OF_BASE_GIT_LEDGER_BLOB",
  "base_bytes": 12345,
  "append_payload": "payload/ledger_append.csv",
  "append_sha256": "SHA256_OF_EXACT_HEADERLESS_APPEND",
  "append_rows": 12
}
```

The numbers and hashes above are placeholders. The append is UTF-8 CSV without
a header. A nonempty append and the existing ledger must end in a newline. CSV
parsing supports quoted fields and embedded newlines. New rows require complete
`task_id`, `attempt_id`, `session_id`, `start_utc`, and `end_utc` fields, with
timezone-bearing timestamps and an end no earlier than its start.

The current ledger must retain the entire exact base blob as a byte prefix.
Intervening appended rows are preserved verbatim. Duplicate interval identities
are rejected after UTC timestamp normalization, regardless of changes to mode,
lane, status, artifact or numeric credit fields. The identity consists of task,
attempt, session, start and end. Nonempty intervals in the same task, attempt
and session must not overlap; touching half-open endpoints are permitted.
Every new row is checked against previous relevant rows and other new rows.
Partial or complete presence of the append without a verified application commit
is a conflict, not an invitation to append again. The helper does not recompute
the scientific meaning of the credit fields.

Compute the outer ZIP hash only after all members and the manifest are final.
Do not insert the outer ZIP's checksum into a member of that same ZIP. The
runtime application receipt is generated after verification and is not a
prebuilt payload file.

## Preserving current main and retrying publication

Fresh application fetches `origin/main`, verifies base ancestry and every touched
preimage on that current remote tree, then fast-forwards the clean local main if
needed. Changes to unrelated files survive. An appended ledger tail may also
survive under the dedicated ledger rule. A changed touched preimage or a new-path
collision aborts before the fast-forward or payload writes. Unrelated unpublished
local commits are not automatically pushed.

The helper stages only declared targets and its generated receipt. It checks
that all other staged tree entries equal the chosen application parent. The
receipt records the package ID, raw-manifest SHA-256, base and actual parent
commit, exact output hashes, and actual ledger prefix and append hashes/sizes.
The commit carries matching package and manifest trailers. The receipt describes
local application; **remote publication is established separately by fetched Git
ancestry**. A normal, non-forced push targets the exact audited local commit ID.

| Situation | Result |
|---|---|
| First valid application | One application commit, one ledger append, then normal push and remote-ancestry verification. |
| Repeated package already published | Verify the original application commit in remote history; do not append, commit or push again. Later published revisions to package files remain intact. |
| Push rejected or response uncertain | Retain the local commit. Fetch and inspect remote ancestry even if the push reported failure. Exit 3 if publication cannot be established. |
| Retry with unchanged remote | Push the already-verified local commit; no second application or append. |
| Retry after unrelated remote advance | Recheck remote touched preimages and ledger prefix. Create a guarded ordinary merge retaining both histories; resolve only the dedicated ledger append from verified remote bytes plus the original append. Keep the original application commit and its receipt. |
| Retry after a touched-path conflict | Stop before merging; retain the existing local application commit for review. |
| Reused package ID with different manifest | Stop. A changed delivery needs a distinct ID. |

A retry merge may add an integration commit when remote main advanced; it does
not create a duplicate application commit. Its resulting tree is audited against
the new remote parent plus the exact package changes. The original receipt
continues to describe the original application, while the merge records the
integration of intervening remote work. Successful publication requires the
audited pushed commit to be in subsequently fetched remote-main ancestry.

No path in the helper invokes force push, stash, reset or clean. Existing Git
hooks remain enabled. A failed commit normally restores only the helper's own
uncommitted writes after checking their current bytes and index entries. If a
hook or another process changes them, those changes are preserved for manual
review rather than overwritten. A hook-modified committed tree is not pushed.
Do not concurrently edit the checkout while applying it. A lock in the Git
directory prevents simultaneous helper invocations; an interrupted process can
leave a stale lock requiring inspection before another attempt.

## Evidence and scope

The test driver [test_apply_package.py](test_apply_package.py) executes the real
Python CLI against newly created, temporary local bare remotes. The override is
unavailable through PowerShell and requires both an explicit Python fixture
argument and environment acknowledgement. The checkout and bare remote must
sit inside a marked fixture directory. Tests configure identities only in those
temporary repositories and use no GitHub authentication.

Each invocation writes a new `test_runs/run_NNN/` directory containing the exact
helper and test source snapshots, their hashes, results and captured test output.
Earlier results and source versions are preserved. These runs are operational
packaging work, with zero principal Research90 credit. No test commits or pushes
the live Value Logic checkout. PowerShell availability and the absence of a
Windows runtime test are recorded separately in each result.

The implementation is adapted from the preserved, previously tested
[P3-06 helper](../../P3_06_2026-10-09_S1/publication/README.md). Its guarded
preimage, append-only ledger, retry and publication-verification behavior is
retained. This adaptation changes the P3-07 identifiers and adds the explicit
P3-07 target allowlist, with fixture paths updated to the permitted scope.
The inherited tests are run once for this adaptation, with only focused tests
for the new target restriction added. No old receipt or test artifact is copied
into this session. The operational review records the exact tested source
hashes and result. Windows execution remains untested.
