# Source review of the first P3-10-A1 continuation draft

Contributor: **ChatGPT (GPT-6 Astra Pro)**, `/root/freeze_review`.
Signed UTC: **2026-10-11T15:31:24.427711+00:00**. Reviewed driver SHA-256: **8b9b05dcaa7d894ca048240bd50d3037be97ca9c7aec59101b0949176d5b6ede**.

**Status: CORE DESIGN PASSES STATIC REVIEW; TWO AUDIT GAPS REQUIRE CLOSURE.** This review is bound to the first unsealed draft, not to a future amendment manifest or execution. No driver, generator, worker, scorer, analyzer or observer was executed. No final payload was read. Zero principal Research90 minutes are claimed.

## Passed scoped checks

- The driver preserves the original freeze/protocol identity as an explicit part of a new binding containing `amendment_id` and `amendment_manifest_sha256`. Original records retain their original identities.
- The exact original verifier runs in a separate interpreter. The current driver is admitted separately through the expanded local-source closure, and the current process must match the exact original runtime record. The prospective new-source list and original evidence inventory are byte-bound by the amendment manifest.
- All 12 original inputs are reused. Exactly 440 old public records must resolve to broker/certificate units; exactly 60 remaining original-schedule units must all be conformance. Their rosters must match the prospective manifest.
- The new public stage schedules only those 60 units. The bootstrap calls the inherited initializer on the exact conformance module instance before the unchanged paid worker. There is no generator call or paid broker/certificate replay.
- The composite index requires exactly the full original 500-ID universe, rejects overlapping/duplicate new IDs, and stores ordered references to actual old/new seals and result hashes with explicit provenance labels. Private evaluation requires both the new 60-unit completion and equality with a freshly reconstructed composite reference index.
- Evaluation uses all 500 original unit configurations under the new binding. The unchanged analyzer's score-universe check remains applicable and requires all 500 scores before analysis.
- The merged audit explicitly includes the original unsealed prefix, requires an original unknown public attempt to remain present, and forces complete outer/physical accounting false. This retains the global economic gate and discloses the conformance/overall-orchestration amendment.
- `ROOT/orchestration.lock` serializes the approved new driver while `OLD/writer.lock` excludes an original writer. The inherited stage executor can acquire `ROOT/writer.lock` without a duplicate flock. The custom orchestration lock covers composite construction/verification between stage calls; the original lock remains held throughout.
- There is no retry option or hidden deletion. The immutable per-stage verification publication also makes a repeated command fail. Any intended continuation beyond one command/attempt must therefore be a further explicitly declared disposition, not an implicit unchanged retry.

## Gap 1: enforce read-only preconditions before inherited original-stage helpers

`inputs_stage.verify_complete()` and `inputs_stage.completed()` call `Stage._initialize()` through the inherited lifecycle. `_initialize()` publishes a schedule if it is absent. Thus the comment that the existing original schedule is never recreated is not enforced by this draft. If the prospective original inventory were captured with a missing input schedule but a complete index and valid unit seals, the driver could recreate that schedule inside the original root. The final `check_inventory` rechecks listed bytes, not the absence of newly added paths, so it would not necessarily expose that write.

Require both original `inputs/schedule.json` and `public/schedule.json` to exist and equal the exact expected stage schedule documents before calling any original `Stage` helper that can initialize. After that guard, `old_stage.completed(require_all=False)` can also reject unexpected old unit directories while retaining the same 440/60 derivation. This is a narrow fail-closed precondition, not a proposal to reconstruct any original record.

## Gap 2: preserve the complete verifier subprocess outcome before branching

The draft checks `child.returncode == 0` before publishing a receipt. Failure therefore loses the structured record of its command, raw stdout, stderr, return code and observation times. On success, it preserves the parsed verification object and stderr but not raw stdout or return code. Write an immutable command-attempt receipt immediately after the subprocess returns, before evaluating return code or JSON shape. Keep the existing prospective/source checks and the one-command-per-stage rule. Failure must remain a retained preflight outcome, not permit an unrecorded repeat.

## Limits and next step

No amendment manifest was available/sealed for this review. Its actual source roster, original evidence inventory, exact remaining/reuse lists, stated attempt rule and source hashes need their own bound check. This source pass cannot certify those future bytes or any final outcome. The current broker observer stays unchanged; its new A1 adaptation will be stored separately and will keep the explicit final-completion release requirement.
