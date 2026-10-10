# Structural DEVELOPMENT v4 — complete resource-failure receipt boundary

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.

This prospective repair follows the principal's review of v3. Preserve `run_v1`,
`run_v2`, `run_v3`, their source copies and verification records without edits.
The v3 source hash is
`4f61ecf8ffb6618225eb131f3a636a4c733161b53170bc22385415be1b4bf909`.

## Defect and exact admission contract

v3 caught budget exhaustion during solving but ran source and input admission
outside that handler. A budget denial during the second source enrollment could
therefore throw away the caller's access to the paid prefix invoice. Success
serialization and terminal-byte admission also lay outside the handler. No v3
statement required a budget large enough for complete setup and reporting, so
the tested post-admission failure did not establish the broader API claim.

v4 accepts an exact integer budget of at least `TERMINAL_RESERVE = 100000`.
A smaller or non-integer budget is rejected before any paid admission and has
no deployed receipt obligation. This resource-failure guarantee is for the nine
exact published fixture records returned by `fixtures()` under the sealed
source/runtime closure. It is not an all-path success bound for arbitrary
caller-created structural inputs. The fixed transport demonstration continues
to use its declared 50000000-unit account rather than accepting arbitrary
caller budgets.

## Repair and resource accounting

One handler covers source admission, input admission, worker execution, success
serialization and final report-byte admission. Source enrollment appends each
successfully paid entry to a list owned by the caller; the returned audit
wrapper records whether source and input admission completed. A denied charge
is not spent, and all previously admitted charges remain in the invoice.

Ordinary worker stages continue to protect the 100000-unit terminal reserve.
Normal terminal reporting additionally protects a separate 1024-unit failure
tranche, contained in that reserve. Only the failure handler may release this
tranche. The failure payload is a fixed 140-byte ASCII JSON literal with the
same UNKNOWN/no-answer/no-warrant service fields as before. Loading and returning
this literal is a bounded two-opcode worker operation in the declared CPython
runtime; its 140 report bytes are then charged. The 1024-unit tranche therefore
funds this receipt after any admitted-prefix denial, including denial during
an attempted success report. Failure details and invoices remain external
measurement records, consistently with the existing tariff contract.

No mathematical input, source rank, hypothetical interpretation, fixed action,
solver or checker changes. Source bytes and all actually executed worker costs
are remeasured in a fresh v4 run. The separate failure reserve changes budget
admissibility near exhaustion, not the meaning of a successful result.

## Prospective focused verification

1. Verify rejection before work for non-integer and below-reserve budgets.
2. Exercise denied first and second source enrollment and input admission,
   checking admitted source lists, partial admission flags, fixed failure
   payload, paid-prefix reconciliation and total spending within budget.
3. Preserve the existing genuine post-admission spent failure for both methods.
4. Exercise the two newly caught terminal boundaries with explicitly labelled
   meter fault injection: saturate the normal terminal allowance immediately
   before success serialization, and immediately before report-byte admission.
   These are API boundary probes, not additional structural performance cases.
   Verify that the protected tranche still returns the fixed failure payload.
5. Run the nine matched comparisons and transport once at their declared
   account, binding all results to a fresh v4 source manifest. Retain equality
   and any ordinary advantage. Reconcile source snapshots and invoice totals.
6. Ask the principal or integration reviewer to inspect the diff and the
   fixed failure-readout bound independently. Stop optional checks after the
   concrete boundary risks are resolved.

All work remains DEVELOPMENT, adds zero concurrent principal time credit,
does not create a final evaluation or freeze, and does not amend older evidence.
