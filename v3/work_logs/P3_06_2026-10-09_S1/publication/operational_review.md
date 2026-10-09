# P3-06 guarded delivery: operational verification

Date: 2026-10-09. Author: ChatGPT (GPT-6 Astra Pro), delegated implementation
owner. Scope: publication helpers only. This is operational packaging work,
not scientific research or principal Research90 credit. The final scientific
manifest, payload and ZIP remain the principal's separate integration output.

## Deliverables and contract

- [Apply-And-Push.ps1](Apply-And-Push.ps1): PowerShell 5.1+ wrapper requiring an
  independently supplied outer ZIP SHA-256, binding extracted companion bytes
  to the verified archive, and invoking the portable helper.
- [apply_package.py](apply_package.py): Python 3.10+ standard-library helper.
- [manifest.schema.json](manifest.schema.json): structural manifest schema;
  additional semantic checks are enforced by the helper.
- [README.md](README.md): final-package construction, application and retry
  instructions, exact ledger semantics and platform limits.
- [test_apply_package.py](test_apply_package.py): actual Git/CLI fixture tests.

The ZIP root contains `manifest.json` and both helpers. Every non-manifest ZIP
file is included in `members`. The schema is `value_logic.p306.delivery.v1`.
Only `TristanMiano/value_logic` on GitHub and branch `main` are accepted for
normal use. The local test override is explicit, marked, environment-gated,
and confined to temporary local bare remotes; PowerShell does not expose it.

## Final executed verification

[run_005/results.json](test_runs/run_005/results.json) records **31 tests passed,
zero failures and zero errors**. The test run took approximately 9.34 seconds on
Python 3.12.14 and Git 2.51.1. This elapsed runtime is an operational program
observation, not principal engaged research time. Each case invoked the actual
portable helper against temporary Git repositories and local bare remotes.

The current sources were reread and matched the executed snapshot hashes:

| Source | SHA-256 |
|---|---|
| `apply_package.py` | `56a14c3e94fee64a034c34d330b7c135c60fe5e0db635227dc8b3f73a365fd5a` |
| `Apply-And-Push.ps1` | `37bec280b6eabb424179dd6b026cf9b70f891e2f65588fff773a30c01c31dadc` |
| `test_apply_package.py` | `bcaf8f0fa0937ccd97df9705d0218ee83d0a42cb3a755cc659ce99a4cc7ced5d` |

The manifest schema parsed as JSON, and its six regular-expression constraints
compiled successfully. The Python helper performs its semantic validation
without requiring a JSON-schema package.

| Behavior checked | Observation |
|---|---|
| Fresh apply and repeated identical package | One application commit and one exact ledger append; second application makes neither again. |
| Fresh unrelated remote advance, including an appended ledger row | Unrelated file and exact ledger bytes preserved; application receipt binds the actual advanced parent and prefix. |
| Touched-file conflict, changed historical ledger prefix, ignored new-file collision | Abort before payload writes or fast-forward; original local state retained. |
| Staged changes and untracked files | Dirty checkout rejected unchanged. |
| Wrong ZIP hash, changed member bytes with a recomputed outer ZIP hash, changed companion helper | Rejected before repository mutation. |
| Duplicate relabelled interval, partial previous append, overlapping interval | Rejected; no duplicate time added. |
| Rejected push followed by retry | Original local application commit retained and reused, without another ledger append or application commit. |
| Rejected push followed by unrelated remote file and ledger advance | Guarded merge retains both histories and appends the package rows once. Repeating afterward makes no additional commit. |
| Rejected push followed by touched-file conflict | Local package commit retained; no merge or remote overwrite. |
| Later published changes to a package file | Repeated package locates and verifies the original application, then preserves the later revision. |
| Unrelated unpublished local commit, incorrect base ancestry, unapproved local remote | Rejected without publishing unrelated work. |
| Commit hook rejection without new edits | Only the helper's own writes are restored, including a declared deletion. |
| Failed initial or retry commit hook that edits/stages a target | Hook edits remain in both worktree and index; nothing is published. |
| Retry merge hook adding an undeclared committed file | Post-commit tree audit blocks publication and rejects subsequent automatic retry of that modified merge. |
| CRLF checkout and disabled executable-bit discovery | Git blob hashes and explicit index modes remain correct. These are Linux Git fixtures, not Windows runtime tests. |
| Existing helper lock and nine Git environment overrides | Rejected without disturbing the ordinary or alternate index. |
| Traversal target and reused package ID with different manifest bytes | Rejected before any new application. |
| Check-only mode | Fetches and verifies, without fast-forward, application commit or push. |

## Independent review and preserved development history

An independent agent selectively reviewed the preserved P3-05 delivery prose and
application receipts, then read the new helper. The older installer source was
not present in the checkout or uploaded checkpoint, and no source audit of it is
claimed. The new protocol retains the distinction between local application and
verified remote publication.

The static review identified and led to repairs for four concrete boundaries:

1. Compare normalized path objects for Git-for-Windows slash conventions.
2. Check Windows reparse attributes even on Python versions lacking
   `Path.is_junction`.
3. Audit target bytes and index entries before rollback so a failed hook's edits
   are preserved; apply the analogous check before aborting a retry merge.
4. Reject environment variables selecting a different Git repository or index.

The reviewer confirmed the first three repairs in source. The fourth was then
implemented and exercised against all nine rejected override variables. The
owner also added archive-to-helper source binding, explicit retry-merge tree
audits, and an invocation lock. No independent execution or Windows execution
is attributed to the static reviewer.

Earlier successful runs remain preserved with their exact sources and results:
run_001 tested 19 cases, run_002 24, run_003 25, and run_004 30. They are historical
development evidence; their passing tests did not cover every later-discovered
boundary. No failed run was removed or overwritten; no executable test run in
this sequence failed.

## Operational limits

`pwsh` was not available. No PowerShell parser execution, Windows filesystem
execution or live GitHub push was performed. The PowerShell wrapper was inspected
as source; the portable helper was executed on Linux. The scripts rely on the
user's installed Git and existing authentication and keep hooks enabled.
Unexpected edits during application require preservation and manual review;
the checkout should not be edited concurrently. A retained local application
commit is not itself evidence of remote publication.

Only this `publication/` directory and temporary local fixtures were written by
this packaging task. No live-repository commit or push, root phase/status update,
clock edit or ledger edit was performed. No P3-07 work was started.
