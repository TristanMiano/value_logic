# Final preservation audit plan

Contributor: ChatGPT (GPT-6 Astra Pro), ordinary-controls agent, October 10,
2026 UTC. Administrative observer work only; zero research-clock credit.

The parent requested a literal comparison against base commit
`33c6d6795aac894bd3cf8575e44f1d6f38f6ae56`, tree
`0dbec24dfc68172a31aaa4a524fd5d1f2c199b67`, containing 5,659 tracked files.
Only `TODO_v3.md`, `v3/plan.v1.json`, `v3/README.md`, `v3/claim_ledger.md`
and `v3/time_ledger.csv` may differ. Every other tracked blob must remain
byte-identical, and no baseline path may be deleted. Compare base object bytes
directly through read-only `git cat-file --batch`; save per-path hashes and
results without changing the index, branches, sources or status files.

Verify completed unit logs and every declared source copy for `primary_v5`
(317 records), `secondary_pruning_v1` (148), `actual_consumer_cap_v1` (288)
and `rational_service_v1_retry1` (30). Require the supplied completed digests,
summary/manifest agreement and declared row counts. Hash referenced packet
files as an artifact-integrity check; do not execute their contents.

Preserve the documented `rational_service_v1` exception: its current 29-row
log has digest
`df3e500eac31c649b9afa3fc285b3d5428ed157ced94e2a63c462ff6bc92f69f`,
while its unchanged summary declares 30 rows and another digest. Verify that
the independent `synthesis_review_v1` copies preserve those exact bytes and
the observation. Do not repair, replace or treat this original directory as
completed 30-unit evidence; the separate retry has its own seals.

Check that the baseline time ledger is an exact byte prefix of the current
ledger. At initial inspection, no new rows were appended; the parent is still
synchronizing the five permitted files. If the first scan precedes the append,
record that fact and save a separate ledger-only verification after the parent
signals completion. Preserve the first report. The audit will not alter or
assign any measured time, run a worker/checker/oracle, commit or push.
