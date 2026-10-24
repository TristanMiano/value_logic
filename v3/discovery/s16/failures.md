# s16 failures and corrections

Codex (GPT-6), October 23, 2026. DEVELOPMENT.

- Initial `scale_probe.py` exited1 on the printed-fraction assertion for
  the t=101/100 lower endpoint. The algebra and all preceding witness
  checks passed; the expected string829109/2023636 was unreduced, whereas
  Fraction prints the equal rational8209/20036. This was a deterministic
  probe representation mistake, not a hardware diagnosis. Preserve
  [original source](scale_probe_v0.py), [stderr](scale_probe.stderr) and
  [stdout](scale_probe.stdout). Repair compares exact fractions. The
  corrected run uses separate r1 logs and its source-bound JSON output.
- A multi-file documentation patch failed its exact-context check before
  applying changes. Inspection confirmed the files remained unchanged;
  the corrected patch applied. No scientific output was lost or overwritten.
- Repository inspection found that s14 already proved the two-moment sharp
  envelopes reconstructed in s16. The new notes and search record explicitly
  correct their lineage. Alternative parameterizations are not counted as
  new sharp-envelope progress or independent confirmation. Cross-target
  acquisition, finite-scale acquisition and explicit checker work are
  assessed separately.
- The first minimum-column probe passed its internal numerical checks but
  reused the variable `detail` when assembling the special-case JSON row.
  Its stored special value therefore had another case's witness metadata.
  This deterministic reporting bug was caught by inspecting stdout. Preserve
  `minrank_probe_v0.py`, original JSON/stdout/stderr; the corrected source
  stores `special_detail` separately and writes distinct r1 evidence.

- Naive spectral application of separate scalar envelopes, matrix-eigenvalue
  clipping, ignoring source rank, selecting completed audit outcomes and
  reusing a private test with an informative invoice have explicit negative
  examples in their linked derivations. These are mathematical failures of
  proposed shortcuts, not machine failures.
- A proposed private-check economic comparison was weakened first by a
  stronger fresh-epoch control and then defeated by five-query univariate
  interpolation. A pooled-proof mixture needing18 paired proofs lost to a
  direct paired test needing four. Neither is advertised as a net saving.
- The block checker's first draft rejected a valid large-edit raw upper bound
  above1. Self-review added the justified final scalar[0,1] intersection
  before the development panel ran. No failed panel is hidden by this repair.
- Some primary-source requests timed out or returned403; literature.md
  records exact inspected scopes. Search snippets and inaccessible proofs
  were not treated as verified theorems. Additional exact-context document
  patches failed without applying changes and were corrected after inspection.
- Clock dispositions exclude whole interrupted or mixed-mode intervals.
  The one E-to-D correction records actual derivation with unchanged total
  research credit. No apparent failure was attributed to hardware without
  evidence, and no extra probe runtime was added to the resident clock.
- Closing self-review caught a pointer-update script spanning the first six
  historical portfolio rows and changing line endings unnecessarily. The
  historical rows and unchanged line endings were restored from the verified
  base before staging; the update logic was corrected. Historical recurrence
  row bytes and the ledger prefix receive separate integrity checks.
- The full local suite's link check ran before the closing manifest existed
  and reported that missing target. Preserve the original log; the manifest
  was then generated and the link suite rerun separately. The other local
  failures match the known dependency and Windows-fixture limitations in
  publication.md. This is an administrative sequencing error, not a failed
  mathematical claim or an unexplained hardware event.
