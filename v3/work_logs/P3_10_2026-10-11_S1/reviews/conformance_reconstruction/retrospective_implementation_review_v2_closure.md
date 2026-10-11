# Retrospective observer v2 — narrow correction closure

Reviewer: **ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction**.
Disposition: **Both requested corrections closed by source inspection**.
No code execution or final-data access. Principal-clock credit: **0 seconds**.

Reviewed only the diff from the preserved v1 snapshot to the principal source
with SHA-256 `82bf46c3a24e46b2c8c7e236951a365ce287ba71c87d9be6c7d7f10615df520d`.

1. `audit()` now derives the scheduled horizon from the unique frozen `whole`
   segment before testing parent/report availability. Failed adapter records can
   therefore be retained without a missing-contract lookup. Successful episodes
   must additionally match that scheduled horizon. This closes the failure-path
   and denominator finding.
2. `save()` now opens, `fsync`s and closes the containing directory after flushing
   and syncing the output file. That publication step returns before the optional
   private file is opened. This closes the requested durable-publication finding.

The diff contains only these two changes. The mathematical and information-boundary
assessment in `retrospective_implementation_review_v1.md` continues to apply.
This is source-level acceptance of the corrected observer, not a claim that it
has run or that any final P3-10 outcome has been inspected.
