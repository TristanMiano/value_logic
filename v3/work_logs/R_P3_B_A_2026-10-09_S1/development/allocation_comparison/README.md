# Adaptive DEVELOPMENT evidence

Start with [analysis.md](analysis.md). The three prospective arms completed
PASS under the pinned allocation/core/service/adapter closure. They produced
no new exact controls and did not repeat the initial probe.

- [Invocation and preflight](invocation_001.json)
- [Complete batch result](run_001/result.json)
- [Source snapshots and original plan](run_001/sources)
- [Source, command and environment manifest](run_001/manifest.json)
- [Read-only evidence/ZIP audit and exact archive index](saved_archive_audit.json)
- [Separately saved prospective analytic-null diagnostic note](postrun_null_diagnostic_plan_v1.json)
- [Analytic q=1/2 diagnostic; zero new runs](postrun_null_diagnostic_v1.json)

Each arm directory contains directly readable setup and aggregate invoices,
state, public-protocol audit, summary, and two small deterministic archives:
`public_raw.zip` and `evaluation_raw.zip`. The first contains allocation
records, public forecasts/actions and checked purchase receipts; it was
closed and verified before private evaluation. The second contains private
labels and postclosed annotations. Both carry an embedded `MANIFEST.json`
and a separate verification receipt beside the archive.

There are six ZIPs totaling 328,921 bytes, preserving 8,233,176 bytes of raw
JSONL. Every raw entry is SHA256-bound; complete deterministic ZIP rebuilds,
CRC checks, source hashes, invoice sums and transcript scores passed. Large
loose raw files were never written. `saved_archive_audit.json` gives the
exact repository-relative paths, sizes and hashes for packaging.

All work is DEVELOPMENT with zero principal-clock credit. The existing
uniform v1.1 observations and their separately derived v1.2 registry reprice
remain distinct from the adaptive v1.2 executions. The null diagnostic is
post-run algebra, separately announced before calculation, not an additional
scientific arm or a cheaper deployed null policy.
