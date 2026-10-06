# F16 saved-evidence integrity and status audit

**Disposition: preserved F14/ND01 freezes and local execution history pass the
bounded read-only audit. Current-status documentation needs synchronization.**

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, delegated integrity reviewer.
Session: F16-A1 / 2026-10-05-S1. Base and observed HEAD:
`6ef27f20e3ac0920953a27dd84d6c91a021ba58f`.
Recorded verification window: **2026-10-05 22:54:33–22:54:39 UTC**.
Principal credited minutes added: **zero**. This is a concurrent read-only
evidence audit, not a fresh F16 derivation-floor certification or gate decision.
All reviewer writes are confined to this file and `reviews/integrity/`.

## 1. Commands, attempts and frozen membership

The two read-only commands are documented in
`v2/experiments/F15_ND01_results.md`, **“Reproduction without another scientific
run”**. Their implementations were read before execution: F14 verification
checks registered bytes/configuration/import closure; ND01 `verify` reloads and
validates the existing preparations, completions and exposure binding.

| Command | Attempt | Exit | Wall seconds | Outcome |
|---|---:|---:|---:|---|
| `python -m v2.experiments.freeze verify` | 1 | 0 | 0.487022 | All 34 registered files verified. |
| `python -m v2.experiments.neural_diagnostic_v1.runner verify` | 1 | 0 | 3.474422 | 47 registered files, five original source preparations, 15 prepared units and 15 evaluation units verified. |

Both had empty stderr. Runtime was CPython 3.12.14 with NumPy 2.3.5. Each
process received `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`;
`PYTHONDONTWRITEBYTECODE=1` prevented import-cache writes. Full stdout, stderr,
argv, UTC starts/ends and exit codes are saved as
`integrity/f14_verify_attempt1.*` and `integrity/nd01_verify_attempt1.*`.
The containing audit also completed once, exit 0, with its own
`integrity/audit_attempt1.*` records. There was no prepare/evaluate invocation,
new population, model execution or generation, frozen-challenge rerun, or test
suite. Two preliminary inspection errors are disclosed separately in
`integrity/inspection_failures.md`; neither was a verifier/scientific attempt.

| Manifest | Current SHA256, equal to the preserved registration | Derivation 09 member? |
|---|---|---|
| `v2/experiments/freeze.v1.json` | `b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c` | No, among 34 dictionary entries. |
| `v2/experiments/neural_diagnostic_v1/freeze.json` | `9c15af55b83d7edf134542a9c70bcc0f087c6f4f6491f993361a27493b5cf24c` | No, among 47 file entries or five source preparations. |

**`v2/derivations/09_c4_price_revision.md` is outside both freezes.** A dated,
transparent correction to its §10 midpoint-coherence warning can therefore be
made without altering registered evidence. The present audit establishes that
permission boundary, not an independent proof of the mathematical correction.
The review supplied by the mathematical collaborators concerns exact A1:
`k=3`, equal old prices, `M>0`, all laws on eight worlds, and a single edited
price. Proposed correction: state that this family's revised-coordinate
midpoints admit a common law in the old-summary fiber, cite the F16 proof, and
retain the possibility of incoherence only for broader vector-query settings
where separately justified. Preserve the old warning as a dated correction
record and do not extend the new assertion to arbitrary k or arbitrary edits.

The frozen Markdown members are protocol/design/source-comparison documents,
including `v2/experiments/protocol.md` and the ND01 protocol. Those historical
contracts must remain unchanged. `integrity/integrity_result.json` records the
complete memberships, expected/actual SHA256 values and byte counts.

## 2. Saved reports, source hashes and execution continuity

A raw Git-blob comparison of **973 saved files** under `v2/experiments/`, both
registered F15/ND01 run directories, their two session directories and their
session Markdown logs found **zero additions, deletions or changed bytes
relative to the base commit**. Python import caches were excluded. Before/after
inventories are also identical. The checks use raw working-tree bytes, not
timestamp inference or an eol-normalized diff. They are retained in
`integrity/inventory_before.json` and `integrity/inventory_after.json`.

| Saved report | Current SHA256 | Comparison with base |
|---|---|---|
| `v2/experiments/results.md` | `333ef2b80b9108d288529d9bc0c7925c8c76471eb1a1ae4fc055d5d475341d74` | Byte-identical. |
| `v2/experiments/F15_ND01_results.md` | `e1aff33a3b59c9dc0c53e530e3b1c6305969a1c073814069e2ab824e6880ac6a` | Byte-identical. |

All **181** F15 reporting-input registrations and **nine** derived-output
registrations match their current files. Of 46 ND01 audit-input/preservation
registrations inspected, 44 match; the two exceptions are the explicitly
historical report snapshots bound by the earlier report review and addendum:
`2ba0372855335965d98e8514e4cb06556d41c86c2010ecf96676397d992de598` and
`19f6348fa965e8b52b6098a9dd3fd0e39dbfcbd65a877c0b310dc5e7f203ac71`.
The completed report differs from those intermediate snapshots but is already
present with its current bytes in the base commit. The older audits and their
hashes are preserved; this is not evidence of an F16-period report change or a
scientific rerun. Do not describe those older reviews as hash-verification of
the final report snapshot.

The registered hashes of `v2/experiments/summarize_f15.py`, F15's
`audit_saved_artifacts.py`, and ND01's `audit_final_report.py` and
`audit_report_addendum.py` also match. Exact values are in
`integrity/source_hashes.json`; their source files were inspected/hashed, not
executed again.

F15 has exactly the original `preparation_attempt_1` and
`evaluation_attempt_1` directories; ND01 has the same two attempt-1 directory
names. Both preparation/completion pairs, exposure/start markers and all
saved event records remain base-identical. F15's recorded evaluation ran from
**03:47:20.675387 to 03:50:24.452339 UTC**; ND01's from
**17:04:36.564386 to 17:04:57.737900 UTC**, on October 5. Both completions say
attempt 1 and no unchanged unexplained retry. ND01 records zero new ordinary
training steps and no retention execution. Its verifier rechecks the durable
15-unit preparation binding before accepting the saved exposure/completion.

F15 run sidecars match for **180/181** JSON files. The sole exception is the
already documented zero-byte
`v2/work_logs/F15_v1_run1/evaluation_attempt_1/retention_results.json`.
Its sidecar still expects
`0b0d9f79a7e74ddecef52bf5d20654eb433a5472d66cc3df63f84ae27dd04691`;
the separately preserved
`v2/work_logs/F15_2026-10-04_S1/retention_results_recovered.json` has exactly
that SHA256 and 15,833,616 bytes. No repair was attempted here. ND01 run
sidecars match **103/103** JSON files.

**Conclusion at this evidence scope:** there is no new recorded F15/ND01
execution after the base commit. Saved hashes and markers cannot prove that
no unrecorded, deleted, or external execution ever occurred.

## 3. Current-status corrections proposed to the principal

Line numbers below refer to the inspection snapshot, before the principal's
concurrent edits. The complete matched text and heading context are in
`integrity/status_inventory.json`. These are proposed corrections only; this
reviewer edited none of the documents listed here.

| Document and exact section | Stale statement/location | Proposed correction while F16 is active |
|---|---|---|
| `README.md`, opening status | Lines 13 and 26: F16 “next/unstarted” or “remains unattempted”. | State “F16 in progress, fresh D60”; keep optional ND02 deferred/unstarted and C/D unattempted. Explicitly date the F15-close sentence if preserving it as history. |
| `README.md`, opening completion summaries; “Current emphasis”; “Phase two” | Repeated F16 selected/unstarted at lines 63, 68, 78, 149, 184 and 186. | Synchronize the current F16 phrase or replace repetitive current-status tails with a pointer to authoritative TODO. |
| `v2/README.md`, opening and “Current status” | Lines 6 and 24 still say F16 selected/unstarted or recommended next. | State F16 in progress and link its fresh work record. |
| `v2/README.md`, “Preserved F15 completion” | Lines 43–44 call 801.130388 “Current POST-B-1” and F16 unattempted. | Label the amount “At ND01 close” until final F16 accounting; change the active F16 pointer or label it explicitly historical. |
| `v2/README.md`, repeated completion records and “Next task” paragraph | F16 unstarted at lines 125, 137, 189, 212, 227, 310–311. | The surrounding archive qualifier can preserve dated history, but the “Next task” paragraph must either reflect F16 in progress or explicitly say “At ND01 close”. Avoid unqualified present-tense stale pointers. |
| `v2/claim_ledger.md`, opening “Current status” | Line 6 says F16 selected/unstarted; line 13 calls it the fresh D60 priority. | Replace with F16 in progress; append the F16 disposition when complete. Preserve dated F15/ND01 claim rows as their original decisions, with a clear later-status pointer. |
| `v2/contribution_plan.md`, current opening | Line 10 says F16 selected/unstarted. | Update to F16 in progress. §15 line 719's recommendation should be explicitly labeled the ND01-close recommendation if preserved. |
| `v2/contribution_review.md`, “Current handoff” | Lines 11–12 say F16 selected/unstarted. | Update the current handoff. §9 line 431 and §10 line 467 can remain as dated F15/ND01 recommendations if explicitly framed that way. |
| `verification/README.md`, opening status | Lines 5–9 say complete only through F14 and F15 selected/unstarted. | State F15 and ND01 complete at their recorded scopes, F16 in progress, and retain historical validation counts/failure limits. |
| `v2/verification/README.md`, opening status and “Validation and limits” | Lines 18–24 say F15 selected/unstarted and no F15 execution; line 219 calls F15 next/unstarted. | Add present F15/ND01 completion/F16 status. Qualify “no F15 execution” as true at F14 development close, not today. Update the active pointer at §Validation and limits. |
| `TODO_v2.md`, numbered queue, completed F15 and ND01 entries | Lines 1354 and 1393 still call F16 unattempted or next/unstarted, while the header and F16 entry correctly say in progress. | Say “At F15/ND01 close, F16 was recommended next; it is now in progress”, or replace the trailing pointer with the current F16 queue entry. |

Historical statements should not be indiscriminately rewritten: the explicit
“At F14 close” paragraphs in both READMEs, the dated F14 claim-ledger entry,
`v2/checkpoints/POST_B_8H_1.md` §“Later pointer: F14 close”, and older dated
opportunity rankings are valid historical records. The two saved F15/ND01
reports are base-preserved study-close evidence; their next-step recommendations
can be superseded in current control documents without altering report bytes.
In particular, frozen `v2/experiments/protocol.md` §8 must retain its F14-time
statement that F15 had not yet begun.

**Signed:** ChatGPT (GPT-6 Astra Pro), delegated F16 integrity reviewer,
October 5, 2026 UTC. No principal time credit claimed.
