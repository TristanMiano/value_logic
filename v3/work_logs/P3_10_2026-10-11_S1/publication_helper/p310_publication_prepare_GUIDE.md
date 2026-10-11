# P3-10 publication preparation helper

Prepared by ChatGPT (GPT-6 Astra Pro), `/root/conformance_reconstruction`, 2026-10-11 UTC. Publication preparation has **zero principal research or engagement credit**. This helper makes no network calls and executes no writable Git command. It does not publish, change refs, write Git objects/indexes, or run scientific methods.

## Readiness and evidence

The reusable source is `/workspace/scratch/095cdac579b7/p310_publication_prepare.py`, SHA-256 **1e1e7adfd191364414c015605323c9fd42d56fadd8783b7491f2248bf0831dae**.

Offline test attempt 02 passed **86 checks**. Its results are `/workspace/scratch/095cdac579b7/p310_publication_helper_test_02/results.json`, SHA-256 **419196205958854eceb966df9290e07611f0d3cc0dff7763d12223177e310978**. The test retained exact helper/test snapshots, source bindings, logs, and synthetic receipts. It reconstructed all 20 P3-09 upload receipts covering 164 distinct blobs, all three dependent overlay trees, the 8,373-path immutable baseline tree, and the exact prior API-created commit. It also checked synthetic byte/mode preservation, baseline and cross-file deduplication, UTF-8 BOM/Unicode/CRLF, symlinks, binary and PNG-like data, oversized UTF-8, file-to-directory/deletion handling, failed-receipt retention, and later-plan-change rejection.

Attempt 01 remains preserved at `/workspace/scratch/095cdac579b7/p310_publication_helper_test_01/`. Its failure was a useful exact-commit reconstruction defect: GitHub's saved GET reports UTC dates, whereas the original commit records `-0700`. The revised helper accepts a reconstruction only when its complete Git commit SHA matches the remote SHA.

**No current P3-10 inventory has been prepared by this contributor.** Root must run `prepare` after its final accounting and preservation work. The preflight's older counts and tree ID are not final intended publication identities.

## Prepare and inspect the final intended tree

Use a fresh, exclusive output directory outside the checkout. Existing failed or superseded plans are retained, never overwritten.

```bash
python -B /workspace/scratch/095cdac579b7/p310_publication_prepare.py prepare --out /workspace/scratch/095cdac579b7/p310_publication_plan_v1
python -B /workspace/scratch/095cdac579b7/p310_publication_prepare.py verify --plan /workspace/scratch/095cdac579b7/p310_publication_plan_v1 --working-tree
python -B /workspace/scratch/095cdac579b7/p310_publication_prepare.py status --plan /workspace/scratch/095cdac579b7/p310_publication_plan_v1 --limit 4
```

Defaults are repository `TristanMiano/value_logic`, checkout `/workspace/scratch/095cdac579b7/value_logic`, baseline commit `ea3e20dd9889c2ee22141c17390595867d33d8ab`, inline JSON cap 3,000,000 bytes, inline tree entry cap 128, and SHA overlay entry cap 128. Deletions fail unless deliberately enabled with `--allow-deletions`; P3-10 should not need that option.

The roster includes baseline files plus Git-listed tracked and nonignored untracked files. Existing ignore rules remain in force. Exact source bytes go into content-addressed snapshots. Files already present as identical baseline blobs require no upload; duplicate new files share one upload. The final overlays reference all intended paths independently of this deduplication.

Root's publication scope remains a separate review requirement. Check `inventory.json` for exactly these five modified existing paths: `TODO_v3.md`, `v3/README.md`, `v3/claim_ledger.md`, `v3/plan.v1.json`, and `v3/time_ledger.csv`. Every other changed path should be an intended addition. Review the original/A1 evidence, all reviews, completion artifacts, and PNG path list. The intended PNG roster described by root has two unique PNG blobs plus a duplicate snapshot; deduplication must preserve each path while uploading each new blob once. This general helper does not silently whitelist or exclude files to make scope checks pass.

This read-only snippet checks the old-file boundary and displays PNG identities after preparation:

```python
import json
from pathlib import Path
p310_plan = Path('/workspace/scratch/095cdac579b7/p310_publication_plan_v1')
rows = json.loads((p310_plan / 'inventory.json').read_bytes())
permitted = {'TODO_v3.md', 'v3/README.md', 'v3/claim_ledger.md',
             'v3/plan.v1.json', 'v3/time_ledger.csv'}
assert {r['path'] for r in rows if r['baseline'] is not None} == permitted
assert not any(r['action'] == 'delete' for r in rows)
pngs = [{'path': r['path'], 'sha': r['sha'], 'bytes': r['bytes']}
        for r in rows if r['path'].lower().endswith('.png')]
assert len({r['sha'] for r in pngs}) == 2
print(json.dumps(pngs, indent=2))
```

`verify --working-tree` compares the complete planned tree against fresh raw file bytes/modes and checks ending roster, file-stat, HEAD, and index identities. Individual stable reads plus ending checks are not a filesystem-wide lock; stop other writers during the final preparation/publication window. A changed final file requires a new exclusive plan, not an edit to a sealed old request.

## Use prepared requests and retain actual tool results

| Request kind | Prepared content | Connector operation |
|---|---|---|
| Upload `tree` | Temporary content-addressed paths with exact UTF-8 `content` | `github_create_tree` |
| Upload `blob`, `encoding=utf-8` | One oversized valid text blob | `github_create_blob` |
| Upload `blob`, `encoding=base64` | One PNG or binary blob | `github_create_blob` |
| Overlay `tree` | Real repository paths, modes, SHA references, preceding `base_tree_sha` | `github_create_tree` |

Pass the parsed JSON request as the connector's structured argument. Do not reconstruct text through shell interpolation, pretty-print and paste file contents, normalize newlines, or split a scientific evidence file to satisfy upload limits. Temporary upload trees are only blob carriers; the final repository tree is the dependent SHA overlay chain starting from the immutable baseline tree.

The 3 MB cap is on the stored compact UTF-8 request JSON; transport wrappers may add overhead. Individual oversized text blobs deliberately exceed that inline cap and stay UTF-8. This avoids base64 expansion of the largest text request. Binary/base64 and individual large requests have no remotely verified size or rate guarantee. Retain a rejected request/result and use an independently authorized suitable transport if necessary; do not change evidence bytes.

After each actual connector call, save its entire JSON tool result outside the checkout, then record it. For example:

```bash
python -B /workspace/scratch/095cdac579b7/p310_publication_prepare.py record --plan /workspace/scratch/095cdac579b7/p310_publication_plan_v1 --phase upload --index 0 --result /absolute/path/to/actual_tool_result.json
python -B /workspace/scratch/095cdac579b7/p310_publication_prepare.py status --plan /workspace/scratch/095cdac579b7/p310_publication_plan_v1 --limit 4
```

Use `--result -` for exact JSON via stdin if convenient. Each call appends `receipts/<phase>/<index>/attempt_<n>/tool_result.json` and metadata. A mismatched SHA, error flag, or incomplete overlay dependency returns exit code 2 and remains recorded. Uploads may be processed in modest independent batches. Overlays are sequential and require all uploads plus each earlier overlay verified. `status` skips already verified receipts and returns the next payload paths; it never implies that a commit or ref has been published. A remote response lost before recording may be resubmitted to `record` when recovered; repeating a content-addressed object upload is byte-idempotent, but do not fabricate a receipt from an expected SHA.

Commit creation, fresh remote expected-head verification, `force:false` guarded ref update, and post-update remote readback are root's separate authorized publication phase. A stale remote head is a stop-and-inspect condition; the helper does not force an update or rebuild on another base silently.

## Materialize the identical API-created commit locally later

The connector's create-commit operation does not expose author/committer overrides. Obtain the returned commit's full Git-commit GET response and use:

```bash
python -B /workspace/scratch/095cdac579b7/p310_publication_prepare.py commit-payload --plan /workspace/scratch/095cdac579b7/p310_publication_plan_v1 --response /absolute/path/to/remote_commit_get.json --out /workspace/scratch/095cdac579b7/p310_local_materialization_v1
```

This command writes a raw payload and future instructions only. It first requires the intended final tree, sole baseline parent, and exact expected commit SHA. GitHub API dates may have lost the original numeric timezone. The helper checks the API offset, then shared minute-resolution offsets between -1400 and +1400, including signed zero; a candidate is accepted only if the complete commit object SHA matches. If the author/committer offsets differ, supply independently known values using `--author-offset=-0700 --committer-offset=+0000`, or obtain exact raw commit bytes. It checks the API message as supplied and with one terminal LF; unsupported encoding, headers, signatures, or different terminal bytes cause failure. It preserves every failed reconstruction attempt. The SHA is the acceptance condition, not a timezone guess.

The generated `local_materialization_instructions.json` describes these later authorized actions, without executing them:

1. Write each new exact blob snapshot with `git hash-object -w --no-filters --stdin`; verify each returned planned blob SHA.
2. Set `GIT_INDEX_FILE` to a separate, **initially nonexistent** path outside the checkout. `git read-tree` the baseline tree into that index. Do not use an existing empty file as a new index.
3. Feed `index_updates.z` to `git update-index -z --index-info` under that temporary index, then `git write-tree`. Require the expected final tree SHA. The normal index and working files stay unchanged.
4. Write the exact `commit.raw` with `git hash-object -t commit -w --stdin`; require the API commit SHA. Exact parent order, names, emails, timestamps, numeric offsets, and message bytes matter. A new commit made with local defaults need not have the same ID even when the tree matches.

These steps install objects and a separate index only. Moving local branch refs and synchronizing the normal index are separate operations after remote publication verification; they are not included or executed by this helper. Use the intended repository and clear any inherited Git environment overrides when executing future commands.

Primary documentation: [Git hash-object](https://git-scm.com/docs/git-hash-object), [Git write-tree](https://git-scm.com/docs/git-write-tree), [Git commit-tree](https://git-scm.com/docs/git-commit-tree), and [GitHub Git commits API](https://docs.github.com/en/rest/git/commits). The existing P3-09 payloads/receipts and the broker's `publication_preflight_v1/RECOMMENDATION.md` supplied the repository-specific reconstruction pattern.

## Scope of validation

The offline checks establish local serialization, hashing, exact-byte/tree reconstruction, and resumable receipt behavior on the prior complete publication plus synthetic edge cases. They do not establish current write authorization, credentials, remote quota, large-request acceptance, a final P3-10 inventory, successful upload, commit creation, or ref publication. No scientific experiment was rerun. The preparation and tests changed only new files outside the checkout; tests compared the real baseline HEAD and index identities before and after.
