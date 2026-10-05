# F15 results draft: execution and scope review

Contributor: **delegated ChatGPT (GPT-6 Astra Pro), execution audit**.
Review observation: `2026-10-05T04:28:58.774472+00:00`.
Reviewed `results.md` introduction and sections 1, 2, 6 and 7 at SHA256
`ef97ee03d02d946896f9fa46f7373cf46bba0b5a57693ce3685f8b826a752ada`.
This is a collaborating F15 report check, not F16 or a Gate C/D assessment.
No report edit, generator, preparation/evaluation command, full rerun or
principal-clock credit was performed by this review.

## Disposition

**No blocking protocol, exposure, recovery or scientific-scope overclaim was
found in the requested sections.** The report accurately separates successful
experimental stages from the incomplete task accounting. It reports the
original aggregate failure, preserves its unknown cause, identifies the exact
separate recovery, and does not claim that all original hashes passed.
Two reporting/closure items below should be resolved before final handoff;
the remaining suggestions clarify wording without changing the experiment.

## Evidence checked

- The manifest remains
  `b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c`;
  a new read-only raw-byte comparison found 34 matching files and no mismatch.
- The only attempt directories remain `preparation_attempt_1` and
  `evaluation_attempt_1`. Their complete markers still record successful
  attempt 1, no unexplained retry, no reused units and no incomplete units.
- The original aggregate remains zero bytes. The recovered file remains
  15,833,616 bytes with SHA256
  `0b0d9f79a7e74ddecef52bf5d20654eb433a5472d66cc3df63f84ae27dd04691`.
- Reported preparation, validation, exposure and completion timestamps,
  model hashes/byte counts, pinned runtime and process costs agree with the
  existing execution audit and primary records.
- The 78 focused passes, 203,311 independent rational saved-output checks,
  and 560 independent interval checks agree with their respective saved
  audit reports. Section 6 keeps those checks distinct from a second native
  proof verification, raw-data replay, external peer review and F16.
- The current work log explicitly marks F15 **in progress**, with E60 and
  final handoff pending. Section 7 does not claim that the protected floor
  has already been met.
- All 39 local links in the reviewed portions resolve to existing files or
  directories. This is a file-existence check, not a new numerical rerun.

## Reporting and closure items

### R1. Consolidate both aggregate-read failures under F15-ART-01

Section 2.4 records the first independent retention-audit invocation's
`JSONDecodeError`. The execution auditor's own follow-up diagnostic parse
also raised `JSONDecodeError` before any comparisons; that read-only failure
is preserved in
[execution_audit_command_history.md](execution_audit_command_history.md),
section 3. The report currently does not explicitly identify this second
invocation. Both have the same already-disclosed aggregate-loss cause.

A compact complete wording would be:

> The execution-audit diagnostic read and the first independent retention-audit
> invocation both failed while parsing the zero-byte aggregate, before their
> numerical comparisons. Their preserved records are linked; neither wrote
> experimental inputs or repeated an experimental stage.

This can be consolidated into the existing failure table and F15-ART-01 rather
than given a new experimental failure category. It does not change the
unknown-cause disposition or the exact-recovery justification.

### R2. Synchronize task status at closure without an early E60 claim

The current `TODO_v2.md` still labels F15 selected/unstarted and retains the
old current-status statement that no F15 training/evaluation occurred. The
report and work log correctly record completed stages with the task still
in progress. Synchronize those descriptions before final handoff, preserving
the distinction between stage completion and the protected floor.

The final time section still needs the measured accounting and the explicit
assessment requested by the user: whether E60 was too high, too low or
appropriate, plus final POST-B-1 continuation and preservation/push status.
Those are expected pending items while the principal is below E60, not a
reason to treat the present stage-completion claim as false. No floor or
complete-task credit is assigned by this review.

## Small wording improvements

1. Section 2.1's runtime table says “binary64 numerical arithmetic.” Make its
   domain explicit: **neural binary64 arithmetic; retention exact rational
   arithmetic**. The current wording is recoverable from later sections, but
   the table alone could suggest that retention bounds were floating-point.
2. Section 2.2 attributes the external/internal timing difference to startup,
   imports and exit. The external scope also contains freeze/runtime checks,
   pre-exposure artifact loading/validation and marker/manifest I/O outside
   the runner's measured stage region. Mention those to avoid an overly narrow
   explanation of the difference.
3. Section 7.1 labels the table “F15-close disposition.” While task closure is
   pending, “Current F15 disposition” would match the work log more plainly.
   The substantive contribution assessment itself remains correctly bounded.

## Scope findings

The report does not convert ordinary-task learning into a causal-use claim,
does not label all unsupported identity MAE cells falsified, and does not
claim a unique utility representation. It retains ordinary controls and null
results, states the exact modest contribution type and comparison scope,
and declines worldwide priority. F15-ART-01 changes reporting/storage only;
the completed original units remain primary because no frozen scientific
dependency, criterion or population was changed.

F16 is recommended with a fresh D60 and an explicit reconstruction target,
but remains unstarted. The conditional recurrence instruction is appropriate
to an actually displaced or unsupported meaningful difference; this draft
does not manufacture one merely from the neural null. Gates C/D remain
unattempted and A/B retain their existing scoped passes. No further
experimental execution or forensic rerun is needed to resolve the wording
items identified here.
