# P3-06 final evidence integrity audit

Contributor: **ChatGPT (GPT-6 Astra Pro), independent implementation reviewer**.
October 9, 2026 UTC. Signed review by `/root/p306_implementation_review`.
This contribution is unmeasured and receives **zero principal Research90 credit**.

**Disposition: verified with one declared provenance limitation.** The audit
completed **6,705 integrity checks** over retained files and numerical records.
There are no failed numerical-equivalence, declared-byte-count, artifact-hash,
or current-module checks. One recorded hash names a former whole derivation
draft whose exact bytes were not located; its reviewed theorem section is
preserved separately. Section 3 states the limitation without replacing or
rewriting the original record.

The [machine-readable audit](final_evidence_audit.json) gives every observed
hash, resolution, count and exception. Its
[checker](../development/final_evidence_audit_v1/audit_evidence.py) reads files,
recomputes digests, and compares saved records. It imports no forecaster and
reruns no original scientific test suite. This review makes no phase, clock,
gate, ledger, publication or P3-07 decision.

## 1. Preservation and source binding

| Item | Verified result |
|---|---|
| Scientific manifest files inspected | 15 |
| File-hash declarations | 188; 187 resolve to exact retained bytes, with the single whole-draft exception below |
| Run-artifact hash declarations | All 30 match their declared artifact locations |
| Explicit byte-count declarations | All 35 match |
| Original checkpoint archive members | All seven preserved byte for byte; archive CRC check passes |
| Current `06_*.py` check modules | All six match retained source records |
| Existing scientific inputs checked again at scan end | All 142 unchanged during the scan |
| Local Markdown targets inspected | 105; all current targets resolve, with one dangling link inside a historical snapshot |

The supplied checkpoint ZIP has SHA-256
`220d850d8cedeac8488b68bbde6573e3f2900844f3504144a157474ddcee02b5`.
Every non-directory member matches its copy under
`recovery/checkpoint_original/`, including the surviving addendum, its source
and checker, its original development result, and the recovery metadata.
The saved fresh rerun's deterministic payload equals the original saved
payload after excluding its explicitly recorded environment and timing
fields. Its **1,510 original assertions** are retained historical evidence;
this audit does not count them as newly executed tests.

Of the 188 file-hash declarations, 129 resolve directly at a declared or
explicit snapshot location, and 58 resolve to exact source content elsewhere
in the retained evidence. The latter category includes bare source filenames
and intentional historical-version references. It does not mean that 58
artifacts changed. No strict run-artifact or review-manifest location has a
different payload from its recorded hash.

## 2. Current modules and historical versions

All hashes in this table are full SHA-256 values. They identify the source
bytes inspected by this audit, rather than claiming every older run used the
latest source.

| Current module under `v3/checks/` | Version | Bytes | SHA-256 |
|---|---|---:|---|
| `06_capital_development.py` | `p306-capital-development-v1` | 14,608 | `51aa7a4c684db60b277f070ad74d843d779b3902c087518521e6aff168fc87e6` |
| `06_capital_forecasting.py` | `p306-capital-enclosure-v1.1` | 16,461 | `2c04defb96a9a8f17ef5d32bacfeaadb70f5b981de3491f68eaba7461c1b5ecb` |
| `06_defensive_forecasting.py` | `p306-scalar-v2.1` | 22,638 | `b66af7ec64b7e690aaa15c0901b2ccb220f93f97962052607481ddd7ae240e07` |
| `06_forecast_transport_probe.py` | No `VERSION` constant | 7,453 | `e08035bd940e7d32299932b58203358387eba6263f65abcec3f4d5471f4ca080` |
| `06_mathematical_forecast_development.py` | `p306-modular-development-v3` | 50,110 | `7e19e1e0930cbcdea3637af16c1ade4e1f2099b615a3600821196c2c8c5cecd4` |
| `06_price_replay.py` | `p306-price-replay-v2` | 16,951 | `35addf6ddec8229d953608a5739179d44ac8f2e4121990d181c995aa9f74a9be` |

The mathematical-query v1 and v2 manifests still name the repository source
path, but their historical hashes differ from the current v3 bytes. Exact
copies exist in their respective
`mathematical_queries_v1/source_snapshot/v3/checks/` and
`mathematical_queries_v2/source_snapshot/v3/checks/` directories. The v1
saved-chronology review also correctly records the v1 source hash. These are
historical source references, not assertions that the live path still has
those bytes.

Likewise, the price-replay v1 source hash resolves to
`price_replay_v1/source_snapshot/v3/checks/06_price_replay.py`; the live file
is v2. The earlier scalar ownership defect, mathematical receipt-boundary
defect, and capital cached-input-validation defect retain their exact
reviewed source versions and reproduction results. Their repaired versions
remain distinct. Nothing in the integrity result erases those failures or
retroactively attributes old results to repaired code.

## 3. Explicit provenance and archive-context limitations

The one unresolved source declaration is
`development/independent_audit_v1/menu_extension_plan.json` field
`source_derivation_sha256`, whose value is
`2a6104638894de64ddafddf80a4e6b043d3802317cf1567d2427172511abd0f2`.
It describes the then-current **whole** cost-forecast derivation. No exact
whole-file match was located in the retained scientific inputs or the wider
workspace text search performed during this review. The original plan is
retained with that declaration intact; this audit does not claim the missing
whole draft has been recovered.

The actual [CF-7 theorem-section snapshot](../development/independent_audit_v1/menu_extension_theorem_snapshot.md)
does survive with SHA-256
`d52a000a5a25ba78ca14994e9cf8bc22d3f6dc57d5167952a2a821e6c3391bb1`.
Its binding in the extension result, the extension probe, and their covering
review-manifest entries all match. The limitation is therefore the recovery
of the surrounding whole draft, while the independently reviewed section
and executable extension evidence have exact retained identities.

Two further context limitations concern partial snapshots:

- The historical `independent_harness_review_v1/source_snapshot/06_forecast_transport.md`
  retains a relative link to a sibling `06_cost_forecast_refinement.md` that
  was not copied into that snapshot directory. The transport snapshot itself
  matches its recorded source hash. All corresponding current-document links
  resolve, including the readiness and final scientific review targets that
  were created while this audit was being prepared.
- The archived price-replay v1 script loads an adjacent
  `06_defensive_forecasting.py`, which its partial source folder does not
  contain. The exact required `b66af7ec...` dependency is retained elsewhere
  and is still the current scalar module. The snapshot preserves exact
  source-file bytes but is not a standalone executable source tree; an
  isolated replay must restore that matching dependency beside the script.

Neither issue was hidden by editing an archive or old manifest.

## 4. Frozen mathematical-query and repricing evidence

For every case, v1 and v2's complete saved `records` arrays are exactly
equal. Across v1, v2 and v3, the forecast metrics, full core-audit fields,
pending identities, input-generation counts, and shared-expert counters are
exactly equal. The v2 and v3 instrumentation traces are also exactly equal.

V3's immutable receipt-counter representation intentionally changes receipt
and linked report hashes. Comparing all remaining record and event content
requires converting the counter pair lists to mappings and separating those
versioned digest links from the semantic values. Cached source references
are compared by presence in that projection, then independently checked
against the exact previously admitted receipt for the same mathematical
claim and outcome.

The audit separately recomputed **1,536 report digests**, **1,524 receipt
representation digests**, **1,536 event-to-report links**, and **1,500
admission-event-to-receipt links**. All **12 cached-source checks** across the
four cases and three versions match a same-claim receipt admitted before the
cached issue. No changed label, event order, input, forecast, action mixture,
or numeric audit field was concealed by removing the versioned digests.

| Full mathematical case, in each version | Queries | Fresh issues | Cached issues | Fresh admissions | Settled including cache | Pending |
|---|---:|---:|---:|---:|---:|---:|
| `recurring_shortcuts` | 128 | 127 | 1 | 127 | 128 | 0 |
| `balanced_nonshortcut_null` | 128 | 127 | 1 | 127 | 128 | 0 |
| `delayed_pending_tail` | 128 | 127 | 1 | 119 | 120 | 8 |
| `varying_stakes_actions` | 128 | 127 | 1 | 127 | 128 | 0 |

The cached issue occurs at **tick 33 in every case**. Repeated numeric
equality establishes preservation across instrumentation and receipt
repairs; it is not an additional independent predictive experiment.

Price-replay v1 and v2's complete saved numerical content is equal after
excluding elapsed time and the deliberately revised
certificate-applicability metadata. The v2 metadata separates the rerun's
own certificate, the retained original cost certificate, and the retained
original Brier/calibration certificate. Public issue/admission tapes and
their digests are unchanged and match an independently reconstructed
projection of the v1 mathematical files. All three profiles retain 128
forecasts per method and the same admitted-label/pending partition.

## 5. Exact capital prefix and late targeted probe populations

Each capital case uses the public tape through **tick 32**, including only
admissions available at that cutoff. The audit compared the full saved tape,
report identities, labels, copy totals and all five comparator population
weights to that exact prefix.

| Capital case | Issues | Admitted | Pending | Settled weight | Copies | Allowance misses |
|---|---:|---:|---:|---:|---:|---:|
| `recurring_shortcuts` | 32 | 32 | 0 | 32 | 1 | 0 |
| `balanced_nonshortcut_null` | 32 | 32 | 0 | 32 | 1 | 0 |
| `delayed_pending_tail` | 32 | 29 | 3 | 109 | 4 | 0 |
| `varying_stakes_actions` | 32 | 32 | 0 | 120 | 1 | 0 |

The delayed pending identities are `:028`, `:029` and `:031`. There is no
cached round in any capital prefix, and no comparator receives an eventual
label from after the cutoff. These are 32-issue comparisons, separate from
the full 128-query population above.

The two later targeted probes are newly added evidence, not modifications
to previously frozen experiments. Their plan/probe hashes, declared inputs
and stored result identities match:

| Stored probe | Declared assertions | Saved population | Result SHA-256 |
|---|---:|---|---|
| `bria_constant_bound_v1` | 20,588 | 127 consecutive records | `3fa74aba49fb0c4e8e08845273e0d9bb5416b3d1f30fb4f6e35e6f52ede27ea5` |
| `unit_covariance_v1` | 3,522 | Two tick-16 prefixes, each under three announced profiles | `70dd26c4205892cc23e59770efcac2c4a1f97005c70828d0bf7569c8f5235a42` |

The unit-covariance input hashes match the original mathematical-query v1
files. Every balanced prefix has 16 issues, 16 admissions and no pending
query; every delayed prefix has 16 issues, 13 admissions and three pending
queries (`:009`, `:013`, `:014`). Across its three profiles, each case retains
identical saved capital forecasts and copy assignments. Totals are 96
capital report records and 87 admissions across the six case/profile rows.
The declared assertion counts equal the sums of their stored check groups.

These checks verify saved populations and source bindings. They do not
execute either probe or turn the BRIA actual-path monitor witness into a
production-trajectory or outcome-uniform allowance result.

## 6. Review coverage and the audit's own revisions

The current bytes of all six Markdown reviews covered by earlier independent
review manifests still match: `implementation_review.md`,
`implementation_review_v2.md`, `menu_extension_review.md`,
`transport_and_harness_review.md`, `capital_enclosure_review.md`, and
`fs_kernel_comparison_review.md`.

Other notes, including `independent_proof_review.md`, `literature_review.md`
and the newly created `final_scientific_integration_review.md`, are evolving
review documents rather than payloads covered by those earlier manifests.
The audit records the SHA-256 of their observed bytes and states which
earlier manifests, if any, cover them. A subsequent separately authored
addition does not acquire an older review's hash coverage. The observation
hashes identify this audit's file state; they do not purport to freeze other
contributors' subsequent work.

The audit checker also retains its own development evidence. Its first
draft omitted a versioned cached-report digest from the semantic
normalization and consequently produced a false equivalence alarm. That
checker and output are preserved. A second attempt stopped at its exclusive
output-creation guard, also documented. The next successful audit and its
source were preserved before the final addition of cached-receipt linkage
and the two late stored probes. The final checker verifies raw digests
separately instead of treating differing versioned hashes as differing
numerical records.

The final JSON has SHA-256
`1264c6ec7c62fdd73950ed7a0d0445a921131cb24d00e8a0c5a44df71f9f0156`,
and its checker has SHA-256
`1dee8b86fd3e85cc684f4b52fdeb7cf1d9cdd93973d3214a03d9b182232d7549`.
A separate manifest in `development/final_evidence_audit_v1/` binds these
final artifacts and this signed note without modifying earlier evidence.

**Signed:** `/root/p306_implementation_review`, ChatGPT (GPT-6 Astra Pro).
