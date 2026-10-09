# Independent review addendum: integrated scalar v2.1

Contributor: **ChatGPT (GPT-6 Astra Pro), independent implementation reviewer**.
October 9, 2026 UTC.

**Disposition: PASS within the declared finite-feature, binary-feedback
interface.** The current integrated source matches the independently tested
snapshot, and every issue identified in the preserved supplementary interface
has a checked repair. This is a development and implementation-correspondence
assessment, not a contribution gate or a general mathematical-reasoning claim.

## Exact reviewed version

| Artifact | SHA-256 |
| --- | --- |
| Production `v3/checks/06_defensive_forecasting.py`, version `p306-scalar-v2.1` | `b66af7ec64b7e690aaa15c0901b2ccb220f93f97962052607481ddd7ae240e07` |
| Superseded initial integrated version `scalar_v2_0.py` | `fafa3a07a3549f4c1faddcd5396bc50c38d7ed6fe2ff7a24727ecb4c0b3af5ef` |

The [`v2.1 snapshot`](../development/independent_audit_v2/scalar_v2_1.py),
[`audit source`](../development/independent_audit_v2/audit_integrated.py), and
[`complete result`](../development/independent_audit_v2/audit_result.json)
preserve the exact tested bytes and interpreter metadata. The result verifies
that production still matched the snapshot when the run completed.

## Checked repairs and two additional findings

The revised constructors detach expert names, validate scopes and configuration
immediately, and normalize malformed rational inputs to `ValueError`. Invalid
issues no longer allocate a live delayed copy. Predictions, action tables,
accumulators, observations and returned copy snapshots are immutable; mappings
returned for inspection are detached.

Inspection of the initial integrated v2.0 found two additional defects before
the main audit: `pool.copies` exposed live learner handles, and empty-pool audits
skipped validation of square-root precision. Calling `reveal` through a live
copy left the pool with one admitted query but reported counts settled one and
pending one. The principal preserved that exact version and repaired both
issues in v2.1. The
[`reproduction`](../development/independent_audit_v2/reproduce_v2_0_ownership.py)
and [`record`](../development/independent_audit_v2/v2_0_ownership_findings.json)
show the superseded failures rather than misrepresenting them as current
behavior. The reviewed version exposes frozen `CopySnapshot` objects without
`issue` or `reveal` methods, and validates precision even for an empty pool.

## Independent verification

The new audit passes **7,026 checks**:

- **Preserved baseline equivalence:** all 32 original binary-sequence cases,
  comprising 160 issuances, match the preserved algorithm's probabilities,
  features, expert values, weights, scores, allowances, root-work counts and
  accumulated statistics. Their probabilities and allowances also match the
  already saved result, not merely a second implementation run.
- **Input and ownership contract:** 110 failed-call or immutability probes
  verify unchanged state; 22 constructor cases check immediate validation.
  The probes cover invalid labels, scopes, queries, expert values, weights,
  tolerances, work caps, action inputs, duplicate feedback, detached caller
  configuration, public snapshots and empty-pool precision.
- **New decision features and root certificate:** 32 length-five outcome
  sequences use zero and nonunit weights, rational feature scales, changed
  action tables, negative loss entries, equal slopes, shared offsets and
  certified adaptive root budgets. External formulas reconstruct the
  feature/score and both possible next potential increments. All certified
  reports meet an endpoint condition or the requested residual tolerance.
  There are 2,912 score-difference probes spanning tent and smoothing
  breakpoints; each respects the announced Lipschitz bound.
- **Direct decision accounting:** independently computed mixture losses and
  fixed-action losses match the accumulator. The smoothing allowance and
  fixed-action regret certificate pass. A shared offset of order $`2^{128}`$
  changes absolute costs by the exact expected amount while leaving forecasts
  and features identical.
- **Delayed subsets and numerical enclosures:** a 24-query schedule has 48
  issuance/settlement cutoffs. At every cutoff, three square-root precisions
  are tested against independently rebuilt settled residuals, losses and
  weights. The square-root enclosure is reconstructed using integer interval
  search rather than the production `isqrt` formula. Increasing precision
  never loosens the reported bound. No pending answer appears in a history.

The final delayed state has 24 settled queries, zero pending queries, total
settled weight $`126/5`$, four allocated copies, and three copies with positive
certificate bounds. This explicitly exercises the zero-bound copy handling
in the revised aggregate inequality.

## Assessment and remaining scope

No further correctness defect was found within the audited public contract.
The source's exact identities and the independent reconstruction support its
finite-feature guarantees. The finite probes verify the enumerated execution
cases; they do not replace the derivation or prove correctness of an arbitrary
external answer-checking adapter.

The decision result concerns a fractional two-action mixture or its conditional
expected loss. It is not a bound for every realization of a sampled action.
Query semantics, proof admission and expert computation belong to the task
adapter. Arbitrary private-field mutation is outside the interface. Exact
arithmetic and retained histories still have the input-dependent storage and
bit costs discussed in the original review.

The finite-menu repricing extension has its own
[`separate reconstruction`](menu_extension_review.md). It is not functionality
silently added to this one-profile production module.

All these artifacts are development evidence. They preserve observed execution
runtimes but receive zero principal Research90 credit. The principal retains
responsibility for the final task integration, clock assessment and status.
