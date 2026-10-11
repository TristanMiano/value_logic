# P3-10 read-only publication preparation

**Disposition: the captured evidence tree has a feasible content-addressed Git-data publication route, subject to final closure and one unverified large-request capacity boundary. No commit, upload, push, ref move, Git object write, index write, or scientific execution was performed by this review.**

Reviewer: `/root/freeze_review`. Principal Research90 and engagement credit from this delegation: **zero**. This is publication preparation within P3-10; it starts no contribution decision, P3-11 task, or author gate.

## Captured inventory

The inventory read ran from **2026-10-11 16:09:39.732346 to 16:09:43.430620 UTC**, RC0. Local HEAD was `ea3e20dd9889c2ee22141c17390595867d33d8ab` before and after. Git-reported path/status sets were unchanged; all individual file reads passed the recorded stat checks. This is an observed window without a global write lock, not a final closure or a promise that ongoing administrative files will remain unchanged.

`inventory.json` supplies the complete path inventory, mode, byte size, SHA-256, computed Git blob ID, and relevant baseline identity. `baseline_paths.json` binds the 8,373 base tracked paths. `summary.json`, `rollup.json`, the before/after statuses, and captured execution evidence give the supporting counts. The whole `publication_preflight_v1/` directory is explicitly excluded to avoid self-recursion. A final inventory must add this directory and every subsequent closure artifact.

| Captured group | Changed/new paths | Exact logical bytes |
|---|---:|---:|
| Original failed `final_v1/`, with its preserved completed work | 1,366 | 134,825,103 |
| `final_v1_amended_A1/` | 1,706 | 12,615,267 |
| Amendment definition and evidence | 11 | 409,070 |
| P3-10 session directory, excluding this preflight | 369 | 58,736,056 |
| Results, plan, and sibling session worklog | 3 | 69,553 |
| **Total** | **3,455** | **206,655,049** |

The statuses were **3,454 untracked paths and one modified tracked path**, `v3/plan.v1.json`; none was staged or deleted. All captured paths were regular files with Git mode `100644`. Three zero-byte lock paths are included exactly as Git reported them. This review did not delete them or infer lock ownership from their existence. Ignored files were not included and no ignore rules were changed.

There are **3,373 distinct changed blob identities**, of which 25 already occur in the base tree. Those reusable identities account for 56 changed/new paths. The remaining **3,348 new distinct blobs contain 186,379,689 bytes**, and every one decodes as UTF-8. Deduplication is against the known base tree and among new files; additional reusable historic objects were not assumed. The new content requires 201,245,026 bytes just for its JSON string representations with the specified UTF-8 serialization, before request metadata. Base64 would require 248,510,476 content characters. Native Git's independent per-blob zlib estimate is 20,147,201 bytes, but that is **not a measured Git pack size or tested push transport**.

The largest blob is `numeric_observation_A1/results.json`: **7,385,258 bytes**, Git ID `76d0ea8e3a7f7155afa9eab717a9bd743993bd50`, SHA-256 `8f7e34aef5060b43bccb2447f87238c3b3c864c5a2e375d317472827567da82f`. Its content string occupies 7,933,772 serialized bytes. Ten distinct new blobs exceed 1 MiB; none reaches 10 MiB. Repeated source/result snapshots need only one content upload per identical Git blob.

## Existing publication pattern and remote base

The prior P3-09 and Option B request payloads, indexes, upload receipts, tree receipts, and remote publication records remain outside the checkout under `/workspace/scratch/095cdac579b7/`. `prior_publication_pattern_review.v2.json` binds their exact bytes. The review independently reconstructed **all 20 P3-09 and 43 Option B content-request SHA results**, agreeing with both the saved expected values and receipts. P3-09 uploaded 164 distinct blobs; Option B uploaded 1,571. Those records describe completed remote publication and retain an expected-head guard with `force: false`.

The observed method is directly reusable in structure:

1. Deduplicate exact file bytes by Git blob ID and omit identities already known in the base tree.
2. Upload UTF-8 blobs in temporary content-addressed trees: each entry's path is the expected blob ID and its content is the exact file text. Such temporary upload trees are not the repository's published tree. Separate binary objects used `create_blob` with base64 in the earlier sessions; this captured P3-10 inventory has none.
3. Build the repository tree by applying **128-path SHA-only overlay batches**, each based on the preceding verified tree. P3-09 used three such batches; Option B used 19. Preserve the base tree rather than creating the published tree from an incomplete path list.
4. Create a commit with the freshly checked main head as parent. Update main using the same explicit expected head and `force: false`. Fetch and verify the resulting ref, commit parent, and exact tree afterward. A rejected lease requires fresh inspection; it does not authorize a force update.

The read-only remote main GET returned the same local base, `ea3e20dd9889c2ee22141c17390595867d33d8ab`. A Git-commit GET at **16:10:12 UTC** confirmed tree `3900e2333e1324af72b0b7f51764bfecc79794ba` and parent `f2a240b87d4df07ac91874b092db20b8c4378889`. The responses are saved here. No remote write permission or native Git push authentication was probed.

The older P3-07 portable ZIP helpers are useful design precedent for exact preimages, append-only time-ledger handling, preserved remote changes, and final tree verification. They are **not directly applicable executables for P3-10**: they bind a different base, task, schema, permitted path scope, and closure records. Reuse would require a separate versioned adaptation after principal closure. The current P3-09 Git-data pattern already avoids that unrelated package adaptation.

The first offline prior-receipt summary required an explicit per-receipt `verified` boolean which Option B did not store. It therefore reported a false summary flag despite matching every SHA. That initial JSON remains preserved. Version 2 distinguishes field absence from an identity mismatch; there was no failed upload or changed prior evidence.

## Recommended transport plan after principal closure

Use the established Git-data route, with **3,000,000-byte target caps for ordinary inline-content requests and at most 128 blobs per such request**. At the captured inventory this produces the following exact sizing model; it is a plan, and no upload payload was submitted:

| Ordinary request cap | Inline trees | Larger individual UTF-8 blobs | Content requests | 128-path overlay requests | Content + overlay requests |
|---|---:|---:|---:|---:|---:|
| 900,000 bytes | 206 | 24 | 230 | 27 | 257 |
| 2,000,000 bytes | 93 | 8 | 101 | 27 | 128 |
| **3,000,000 bytes** | **64** | **5** | **69** | **27** | **96** |
| 4,000,000 bytes | 46 | 5 | 51 | 27 | 78 |

`batch_plans.json` contains the exact blob assignments and sizes for each model. The recommended plan has **201,560,746 serialized content-request bytes**, before any connector-specific serialization overhead, and the largest individual `create_blob` request is **7,933,853 bytes**. Tree, commit, ref, and verification operations are additional. The ordinary request cap is an operational choice, not an asserted GitHub service limit.

The largest preserved successful P3-09 request was **6,372,377 bytes**; Option B's was 3,599,554. Thus prior evidence supports the ordinary batching route but does **not** demonstrate capacity for the new 7.93 MB individual request. Handle the five large objects independently and preserve each returned blob SHA. If a connector rejects an object's size, retain the failure and use an authorized native Git transport from the exact reviewed tree if that transport is available. A contents API call or base64 encoding does not establish a larger effective request allowance; splitting a frozen file would change its bytes and is not a suitable transport fix.

GitHub's official documentation confirms UTF-8/base64 blob creation and tree entries by content or SHA. It also explains that a base tree retains unrelated entries. The recursive tree GET limit is a **read-response** boundary, not proof of a write-request limit; inspect `truncated` and fetch needed subtrees when necessary. See the current [blob](https://docs.github.com/en/rest/git/blobs?apiVersion=2022-11-28) and [tree](https://docs.github.com/en/rest/git/trees?apiVersion=2022-11-28) documentation and `official_documentation_notes.json`.

Pace publication and respect returned throttling information. The [official secondary-rate guidance](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) gives general content-creation limits of 80 requests/minute and 500/hour, while allowing lower and undisclosed limits. This review did not inspect remaining shared quota. A small bounded upload queue with receipts, followed by sequential dependent tree operations, is appropriate; the principal should retain and resume verified identities rather than restart a partly completed upload.

`snapshot_tree_plan.json` independently rebuilds the known base tree and computes every 128-path overlay tree using only captured identities. Its final **snapshot-only** tree is `1d72c7ad56e40b0750d0495526366ddb64cf075a` over 11,827 tracked paths. This excludes the preflight itself and later closure edits and **must not be treated as the final deliverable tree**.

Before the first publication mutation, the principal should finish Research90/accounting and results closure, refresh the full path inventory, include the actual append-only ledger and control-file changes, and bind the final reviewed tree. Re-read remote main and its touched preimages immediately before creating the final parent/tree relationship. Preserve both the failed original lineage and the successful A1 composite without rewriting scientific bytes, failure markers, or their hashes. Publication creates no research credit and does not change the global unknown-prefix economic gate or the P3-11/author-gate status.

**Remaining publication uncertainties:** final closure bytes are still changing; the 7.93 MB connector request is untested; available write quota and native push authentication were not inspected. No numerical, protocol, or final-data rerun is required to resolve any of those operational questions.
