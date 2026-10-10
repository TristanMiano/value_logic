# Consumer-cap interpretation before execution

Contributor: **ChatGPT (GPT-6 Astra Pro)**, principal, October 10, 2026 UTC.
Task R-P3-B-B. **Post-primary-exposure DEVELOPMENT analysis plan.**
This note precedes the selected actual cap run. It does not select a new
population, numerical threshold, method, horizon or final challenge.

The original service contract declared recipient thresholds $`2^{20}`$,
$`2^{22}`$ and $`2^{24}`$ units. The first is informative on the saved primary
invoices; the other two accommodate all successful primary bills plus the
1,024-unit protected failure reserve. The selected follow-up enforces exactly
the first threshold, keeps the original $`2^{27}`$ total request budget, and
attempts every one of the same 288 units in its original six-request session.
No price or cache-policy search is planned.

## Questions and possible directions

1. A primary successful path with consumer bill $`u`$ fits this account only
   if $`u+1024\le2^{20}`$. Is that static predicate still accurate when earlier
   rejected requests have evicted producer and recipient state?
2. An initial denial can force later resident portfolio requests to reconstruct
   and readmit their old warrants. Their primary resident invoices assumed that
   successful history. Losing it can make an otherwise affordable later request
   fail; a cheap incremental proof is not an independent bootstrap strategy.
3. Resetting a warm producer can also remove unused history from a later full
   export to a fresh recipient. Hence an earlier denial might make some later
   requests affordable that were not affordable on the primary path. The sign
   of the discrepancy is not fixed by cache eviction alone.
4. Source installation persists after a scientific failure that occurred after
   enrollment. Later rebuilding is therefore different from repeating the
   entire first request with its initial source fee. The observer must preserve
   the actual source and scientific-state distinctions.

These are explanatory hypotheses, not additional passing conditions or a
license to amend methods after seeing the results. The unchanged runner will
preserve completed units, current/stale receipt observations, failures and
their full bills. Independent scalar truths come from the 29 immutable primary
reference records and do not enter any worker.

## Comparison rule

For each six-request cell, report the exact delivered index set, charged cost
of every attempted request including failures, consumer cost and the mismatch
with each static predicate. Compare total costs as an equal-service ordering
only when the delivered request sets match. A lower total accompanied by fewer
delivered claims is not a cheaper complete service.

A useful separate partial order is coverage inclusion plus cost: method A
weakly dominates method B on these fixed attempts only if A delivers every
request delivered by B and A's total charged bill is no greater, with at least
one strict relation for strict dominance. Noncomparable pairs remain visible.
This order does not assign a utility to an omitted claim, choose an optimal
adaptive allocation policy or estimate a population success probability.

The fixed source and primary results imply all mathematical bounds are true.
An exhausted account must produce `NO_CURRENT_CERTIFICATE`, not a contrary
mathematical answer. Successful outputs must agree byte for byte with the
matching primary current output; a failed attempt must expose no current or
stale receipt and must evict the declared scientific caches.
