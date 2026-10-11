# Independent implementation review: retrospective report observer, first revision

Reviewer: **ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction**.
Scope: source-only review against the accepted derivation and frozen reporting
contracts. **No final-data access and no code execution.** Principal credit: **0**.
Disposition: **Mathematical computation passes inspection; two implementation
corrections requested before execution.** Exact files are bound in the manifest.

## What matches the derivation

The observer uses immutable `emitted_q`, `terminal_action`, and `selected` values.
Its `F`, unselected `V`, and actual `Z` constant/coefficient pairs are correct.
It groups the full serialized four-part claim key, so opaque query IDs do not
split logically identical keys. The public-bound computation never imports a
frozen worker, reporter or CNF evaluator.

Chronology uses a separate forward `prior` map, although the complete end map
has already been collected. In hard-disabled mode an earlier paid label does
not become an issued hard correction or an exact chronology summand; that label
can still tighten the retrospective end map. The resulting chronology rebuild
matches the frozen report's `F`/`V` envelopes and `[0,n_live]` for `Z`.

Within each unresolved key it accumulates the signed coefficient and the sum
of absolute coefficients. `absolute_sum-abs(coefficient)` is exactly the proven
cancellation gain. The position width, receipt gain and grouped width are
consistent, with both interval containment and telescoping checks. Delivered
sampling widths are recorded separately, including conflicts; no unjustified
containment inside the delivered sampling interval is imposed.

The optional private numeric file is first opened only after `public_bounds.json`
has been written and its digest retained. Private targets test the fixed bounds;
they do not feed into their creation. The write is exclusive and the bounds
are not overwritten. The post-validation unchanged-digest check is appropriate.
Aggregation uses per-scheduled-horizon quantities, equal seed slots within each
population, then equal population means, and retains identity mirrors.

## Concrete requested corrections

1. **Failure-path horizon access.** `audit()` builds `header` with
   `episode['contract']['horizon']` before testing whether the episode succeeded.
   Frozen `p309_broker.run` has an adapter/source-admission failure record that
   deliberately omits `contract`. That valid recorded failure would raise
   `KeyError`, instead of being retained as `status='unavailable'`. Read the
   scheduled horizon from the frozen unit's `whole` segment (`stop-start`),
   validate it against a successful episode's contract, and use it for every
   denominator. This also directly enforces the derivation's scheduled-T rule.

2. **Durable publication boundary.** `save()` flushes and `fsync`s the newly
   created file but does not sync its containing directory. The intended durable
   creation guarantee needs the directory entry synced as well before opening
   the optional private file. Add directory `fsync` after the completed file write,
   or use an equivalent durable publication helper confined to the observer.

Neither issue requires changing a frozen source, rerunning a paid service, or
altering any recorded scientific result. Both were identified before final-data
access. Runtime, command and final output/failure digests should be retained by
the surrounding observer execution receipt, as required by the derivation.

This note approves no unreviewed future code revision. Re-review the narrow
correction diff against this preserved snapshot before running it.
