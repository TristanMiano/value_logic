# Source review of the A1 lineage reader's public-only boundary

Contributor: **ChatGPT (GPT-6 Astra Pro)**, `/root/freeze_review`. Signed UTC: **2026-10-11T15:38:42.388230+00:00**.
Reviewed reader SHA-256: **54a11007e1530baa25a6f495294b1bdb57f70cefe08568df7f5aa8b815b376ce**.

**PASS_SCOPED for the metadata/result-byte hashing boundary.** The constructor first requires all amended public/evaluation/analysis completion markers and the composite marker. Its `_stage` and `_seal` routines parse schedules, completion indices, seals and starts. They pass each `result.json` to the streaming SHA-256 function rather than the JSON parser. `_reference` also hashes result bytes without parsing them. The constructor does not call `record()`. `record()` is the explicit later payload-reading method.

The revised source pins the exact sealed A1 manifest SHA-256 `36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359`, pins the original freeze/protocol hashes, binds the frozen schedule bytes to the pinned original manifest's schedule hash, and checks the exact remaining/reuse rosters. This closes the previously reported schedule-binding gap. Its constructor's declaration of zero parsed private-score payloads is consistent with the inspected call graph.

This is a source review of that boundary, not an execution receipt or a claim that arbitrary later calls to `record()` avoid private data. No reader code or final payload was executed/read by this review. Zero principal Research90 minutes are claimed.
