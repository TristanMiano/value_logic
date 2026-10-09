# Raw selective-feedback evidence archive

The deterministic [raw_traces_v1.zip](raw_traces_v1.zip) preserves **99 exact
raw files**: 96 comparison JSONL transcripts, purchased per-call invoices,
private evaluator labels and annotations, plus the three large new-service
correctness `domain_checks.json` reports. Their total uncompressed size is
135,369,544 bytes. The archive is 3,029,601 bytes with SHA-256
`d3259d00110aa47f914af82c7d5151212938bda79250b5f16a8a5dc1517c7c23`.

The [manifest](raw_archive_manifest_v1.json) lists every exact repository path,
archive path, byte length and SHA-256. The same payload manifest appears
inside the ZIP as `RAW_EVIDENCE_MANIFEST.json`. All paths are relative to the
repository root. Extract to a separate inspection directory; compare hashes
before restoring anything into a repository that may have newer changes.

The [verification receipt](raw_archive_verification_v1.json) records a second
identical build, ZIP CRC verification, and a byte-for-byte comparison of every
archived payload with its original, in addition to matching both SHA-256
values to the manifest. Entry order, timestamps, Unix file metadata and deflate
level are fixed. Binary reproducibility was verified in the recorded
Python/zlib runtime.

This archive build did not delete any originals. The manifest identifies the
exact redundant raw files eligible for removal after rechecking the ZIP hash
and each original hash. No source, result, summary or clock file is a removal
candidate. The archival builder and saved-evidence audit source are retained
in `reviews/service_agent`.

The full `run_001/result.json`, arm/control summaries, aggregate deployment
and evaluator invoices, source-registry receipts, selector paths, environment,
commands, hashes and source snapshots remain directly readable. The three
correctness probes retain their result, plan and denial records outside the
archive. The [analysis](analysis.md) explains observed v1.1 results and the
separate [v1.2 registry-only transfer](current_registry_reprice_v1.json).

Archiving does not change the stage: all of this evidence remains
**DEVELOPMENT**, with no final evaluation or automatic next work item.
