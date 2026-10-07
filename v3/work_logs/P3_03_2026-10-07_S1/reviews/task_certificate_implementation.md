# P3-03 terminal task certificate — implementation and development record

Contributor: **ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction
implementer**. October 7, 2026 UTC. **DEVELOPMENT**, with zero additional
concurrent research time credit. The principal owns the consolidated scientific
assessment; this is the implementer's record, not an independent review of
their own code.

## 1. Implemented service

[03_task_certificate.py](../../../checks/03_task_certificate.py) implements
`TaskCertificate(request)`. The request supplies scope, fixed query list,
conditional constraints, committed-cell cap, complete supplied action
catalogue, selected action and a nonnegative rational tolerance. Each action
has its original loss expression, unit and version. One to fifteen actions
leave room for the core's reserved sixteenth loss slot.

The wrapper compiles the maximum of
`resid(selected_loss, other_loss)` over all other supplied actions. A
one-action catalogue compiles directly to rational zero. Here the **local
kernel convention** is `resid(f,g)=max(0,f-g)`. Phase-two native `res` instead
requires the reversed arguments `res(g,f)`. The Boolean input coordinates are
answer indicators, not native formula-loss values with zero meaning true.

Original and compiled expressions are validated against the existing finite
syntax, node/depth and numerical admission limits. Common units are required;
the wrapper supplies no conversion oracle. The complete catalogue, its loss
versions, selected action, unit, tolerance and compiled term are bound to the
original request. Common-cost cancellation remains inherited ordinary/native
algebra. The new code supplies a checked construction and bound application
at this restricted interface; it does not claim new mathematics from that
identity.

## 2. Current-use and revision behavior

The wrapper retains immutable canonical copies of the original catalogue,
compiled core loss catalogue and query binding. Before core work or a new
certificate it checks the live catalogue, selection, tolerance, units, queries
and compiled expression against those originals. An altered comparison cannot
silently keep the old name and receive a new certificate.

`run`, `add_assumption` and `withdraw` delegate admitted source changes to the
existing core. Each certificate includes the core's active-source binding.
An old certificate becomes stale after source withdrawal or admission.
Further computation on the unchanged source can preserve an earlier, looser
warrant. A changed action objective or catalogue requires a newly validated
wrapper request. This implementation does not add transport of old compiled
proofs or excluded branches into that new instance.

`certificate()` returns `CERTIFIED_CONDITIONAL` only when a valid core outer
bound has an upper endpoint no greater than the bound tolerance. An excessive
upper endpoint produces `NOT_CERTIFIED_BY_THIS_BOUND`, which alone is not an
impossibility proof. Arithmetic refusal and detected finite conflict produce
no certificate. Unresolved feasibility retains the guarantee's conditional
meaning; the wrapper does not assert that an unchecked source is a complete
arithmetic model or that its premises describe the actual world.

`certificate_is_current()` checks identity and current applicability of genuine
historical outputs. It explicitly does **not** authenticate arbitrary fabricated
or modified JSON. Returned outputs are historical copies. The tested private
state fault injections are diagnostics of specific catalogue/compiled-term
guards, not a public arbitrary-memory-mutation interface.

## 3. Cost account

The wrapper records source/compiled node validation, expression copies,
catalogue scans, bounded input traversal and encoding, byte comparison
envelopes, hashing and tolerance comparisons. These are **boundary work outside
the core transaction allowance**. Its report and accounting calls keep those
counters separate from the core's own resource diagnostics. The embedded
boundary snapshot ends before that outer certificate's serialization; the
subsequent byte charge is retained in the live accounting record.

These diagnostics do not equate a compilation, hash, rational comparison or
core report to one CPU instruction. Host elapsed/process time are separately
recorded in the development summary. No fixed-total-RAM or physical CPU bound
is inferred from the transaction count.

## 4. Prospective execution and artifact bindings

The [prospective question and plan](../development/task_certificate_plan.md)
was saved before the first wrapper execution. The targeted
[check script](../../../checks/03_task_certificate_check.py) created a fresh
`task_certificate_attempt_1` directory and saved its complete deterministic
[inputs](../development/task_certificate_attempt_1/inputs.json) and
[manifest](../development/task_certificate_attempt_1/manifest.json) before
importing the wrapper. No earlier attempt was overwritten.

| Artifact | SHA-256 |
|---|---|
| Wrapper | `6735a7be6819d44ae9d05de497c613595ef7de212ed41f070354d6e0bc27ec75` |
| Targeted evaluator | `3adf6df4dc8aa77239572610ffc0f363dfef817ecbda99ce2d61d2d0821e45ba` |
| Unchanged core | `ae757bee58089b1229cdd2e123e4650be704f04729b2fff081238c988a916247` |
| Saved inputs | `ee97e5e4af63c49d84bdfbd90251fae6f14c0c8c24c61a8046d6cec7676a55f1` |
| Saved traces | `ac02a5fd040106e4fac7265e6c036acece577c0ecbc9e0bb669a6bbb204eea4a` |
| Saved manifest | `0d0abba12b40aa38b0635d97d88b76f2f546a482928c4dfa2064fd38a33babfc` |
| Saved summary | `be59fd40a025eee4947361435b85bfc2d0d50ddc76d5cf0105b966cc195b6db6` |

Read-only artifact checks confirmed these bindings, the plan's manifest hash,
and the per-suite assertion sum. The original kernel and generic harness were
not modified. The separate scalar evaluator computes the two Boolean cases
directly from the original supplied action catalogue; it does not call the
wrapper compiler or kernel's interval evaluator. Those reference values are
evaluator-only and are never injected into the opaque query or source.

## 5. Results

[Attempt 1](../development/task_certificate_attempt_1/summary.json) reports
**PASS: nine suites, 64 explicit assertions**. No rerun was performed.

| Question | Saved outcome |
|---|---|
| A=`10x`, B=`10x+1` | Regret upper bound nine initially, zero after one Boolean split. A receives a conditional zero-regret certificate; truth remains unresolved and the individual cost intervals remain `[0,10]` and `[1,11]`. |
| Replace B by `11-10x` | The same marginal intervals remain, but A's exact finite regret upper endpoint is nine, so no zero-tolerance certificate is issued. |
| A=`x`, B=`1-x` | Both selected pure actions have worst-case regret one after exact finite filtering and fail tolerance one half. |
| Withdraw `not x` | The old conditional certificate becomes stale; the recomputed regret interval reopens to `[0,1]`. Its historical bytes remain unchanged. |
| Different original tasks | Changed selected action, catalogue, tolerance or common unit does not inherit the prior task certificate. |
| Five meaning mutations | Altered selection, catalogue expression, catalogue membership, core action expression or reserved compiled expression is rejected before a new core report. |
| Reprice A to `20x`, version 2 | The original wrapper rejects the changed objective. A fresh request recomputes regret upper endpoint nine. |
| One-action and conflict cases | A one-action catalogue compiles to zero and certifies; detected finite conflict produces no certificate. |
| Admission | Mixed units, an absent selected action, negative tolerance and an oversized compiled expression receive typed refusals. |

The run's observed UTC interval was
`2026-10-07T15:58:01.624441+00:00` through
`2026-10-07T15:58:01.655335+00:00`. Recorded host elapsed time is
**30,887,562 ns** and process time **29,439,639 ns**. These are execution
diagnostics, not extra principal research credit; the manifest and summary
both record concurrent research credit as zero.

## 6. Scientific scope

This is a terminal, source-conditional certificate against the actions in one
supplied catalogue. It establishes neither a new policy for purchasing
computation nor a learned forecast, calibration guarantee, counterfactual
operator or performance advantage. The small cases show the implemented
binding/refinement behavior; the principal's proof supplies the general
conditional argument. P3-N01's contribution disposition is unchanged by
execution count or the familiar cancellation identity alone.
