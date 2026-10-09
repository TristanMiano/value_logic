# Uniform paid-feedback DEVELOPMENT evidence

Start with [analysis.md](analysis.md), [the original planned batch result](run_001/result.json)
and [the separate current-core setup transfer](current_registry_reprice_v1.json).
Twenty learner arms and eight exact controls completed under the preserved
v1.1 controller; current v1.2 changes only version metadata and an initial
funding-failure annotation. It adds 26 source-registry units to those successful
cold bills, without rerunning or relabelling the observations.

## Raw evidence and a recorded packaging repair

[raw_traces_v1.zip](raw_traces_v1.zip) preserves 99 complete raw files and their
embedded original manifest: **135,369,544 uncompressed bytes**, stored in a
**3,105,040-byte** ZIP. SHA256:
`d3259d00110aa47f914af82c7d5151212938bda79250b5f16a8a5dc1517c7c23`.

Use the [authoritative v2 archive manifest](raw_archive_manifest_v2.json) and
[principal verification](principal_archive_verification.json). The principal
first found an incomplete 3,029,601-byte prefix where the complete archive was
expected, stopped before removing any original, and rebuilt the archive from
all 99 intact, hash-matching originals. The complete rebuild has exactly the
original expected SHA. CRC and every archived byte passed independent checking
before only the redundant raw originals were removed.

The [packaging correction](archive_packaging_correction_v2.json),
[first failed guard](principal_archive_guard_failure.json) and
[rebuild receipt](principal_archive_rebuild_receipt.json) preserve the event.
The historical v1 manifest/verification retain the older advertised incomplete
size; their scientific payload hashes are unchanged. The exact damaged prefix
can be reconstructed from the complete archive using the saved byte count and
verified damaged-file SHA. The cause of the incomplete container is unknown.
No scientific execution or label computation was repeated for this repair.

ZIP paths are repository-relative. Extract into a separate inspection directory;
check the manifest before replacing any existing repository path. Result,
summary, aggregate invoices, source snapshots and environment records remain
directly readable beside this archive.

## Reproduction scope

The top-level development driver intentionally pins controller v1.1. The
current top-level controller is v1.2, so the historical driver rejects that
combination rather than silently running a different closure. A complete
self-contained copy of the actual v1.1 dependency closure is in
[run_001/sources](run_001/sources). Its driver accepts `--plan` and `--out`;
its saved `run_plan_v1.json` declares the exact original grid. An output path
must not already exist. Reproducing the algorithm is a new DEVELOPMENT run,
not recovery of the old observations; source-path-dependent registry charges
and physical runtime may differ at another location or machine.

For a new current controller call, use the API documented in
[07_selective_feedback.py](../../../../checks/07_selective_feedback.py).
The source-known and tighter post-run numerical bounds are separate
[certificate calculations](../binary_potential_certificates.json). The
original batch certificates are preserved unchanged.
