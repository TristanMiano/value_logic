# Independent public reporting implementation audit

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Task **P3-08**, **DEVELOPMENT**. Delegated reconstruction review; zero added
principal-clock credit. This review did not edit the reporter, obtain any
unpurchased truth labels, run a final evaluation, freeze a method, or publish.

## Finding and source boundary

**No load-bearing formula, chronology, selected-propensity, finite-width, or
report-funding defect was found in the reviewed source.** This is a bounded
implementation/algebra audit, separate from the integration review of the
probability theorem. It is not an authentication audit of arbitrary external
transcripts or empirical evidence of confidence coverage.

The subject is `p308-live-performance-v1.1`, **19,571 bytes**, SHA-256
`33ecde23b45ca9696da44ffb925797b52dc450d141e16b79fa17ec937fdb347d`.
Its executable closure, mathematical note, protocol, interpreter identity,
audit script hash, and input hash are in
[`run_v1/manifest_before.json`](run_v1/manifest_before.json). The saved closure
and working sources matched before and after execution; see
[`run_v1/manifest_after.json`](run_v1/manifest_after.json). The focused selector
extension used those same immutable subject bytes.

The independent expected-value routine `derive_public(episode)` takes only a
public episode, uses `Fraction`, and follows sections 3–5 of
[`08_live_hard_performance.md`](../../../../derivations/08_live_hard_performance.md).
It neither imports nor calls the production integer calculator. The subject
reporter receives an `IdentityOnly` provider exposing only provider identity
and version; asking it for a solver capability raises an error. Fresh broker
episodes use a separate public-service boundary that logs every paid selected
purchase. Those calls exactly matched the selected rows.

## Exact fixed-denominator algebra

Write D=2^h, P=B for uniform selection or 2B for tickets, and M=1 or B+1,
respectively. A position has multiplicity a in {1,M}, with actual probability
pi=a/P. The selected row has numerator n and purchased label y. Its centered
loss numerator is

```math
r_n=(n-D/2)(1-2y)=D\,[q+(1-2q)y-1/2].
```

The production accumulator `u_num` has denominator DM. Its initial value is
(T-m)DM/2; each selected update is (P-a)r_n(M/a). Dividing by DM gives exactly
the note's (1/pi-1)(d-1/2) update. Likewise `a_num` has denominator D²M:
it starts at TD²M/2, adds P r_n D(M/a) on each selected row, and subtracts
n(D-n)M on every row. It therefore equals the declared Brier center, with
the base forecast variance term retained over every position.

The block width numerator is

```math
w_k=\max_t |D-2n_t|\,P(M/a_t),\qquad
Q=\frac{\sum_k w_k^2}{D^2M^2}.
```

The reporter uses the **base** numerators n_t in this maximum. It does not
recompute a width from selector-dependent live forecasts. With
R=P ceil(sqrt(2m)), its common output denominator is 8RD²M² and its sampling
radius numerator is 8 sum(w_k²)+5R²D²M². The quotient is exactly Q/R+5R/8.

There is no accidental floor approximation in these divisions. D is even
because h>=1; a divides M; and the common denominator is a multiple of DM,
D²M, D, and D². The action-radius expression
`ceil_sqrt((5*n_live+1)//2)` is exactly ceil(sqrt(ceil(5*n_live/2))). Negative
center numerators do not change these divisibility facts.

The independent reconstruction compared both base centers, both live centers,
all three corrections, Q, R, both radii, every interval endpoint and conflict
flag, all deterministic envelopes, and all reported row/key counts. As an
additional public identity, it checked

```math
A'_c-U'_c
=\sum_{t\text{ selected}}(q'_t-y_t)^2
 -\sum_{t\text{ unselected}}q'_t(1-q'_t).
```

The right side needs only selected labels and retained forecasts. It does
not privately score the unselected rows.

## Chronology and exact-all-known behavior

The reporter looks up a complete key among **earlier** selected receipts
before it handles the current selected invoice. Thus the current purchase
cannot retroactively justify a hard correction of its own issued forecast.
Selected Brier corrections occur only when a prior answer already existed;
selected terminal actions are corrected regardless. The ordinary and live
unselected actions must retain their documented common-draw path unless a
prior current answer supplies the live override.

Focused mutations were rejected for a current receipt presented as a prior
hard answer, an incorrect hard forecast, a different complete key, a changed
scope epoch, stale provider version, false row or block probability, ticket
versus selection mismatch, incorrect selected terminal action, an unselected
claimed purchase, and a 129-character source tag. These are defensive checks
within the declared owned-transcript boundary; they do not make the record
cryptographically authenticated. The provider itself also rejected the
129-character source tag. Four complete 128-character-tag episodes passed.

When `n_live=0`, every unselected row has an earlier hard answer and every
remaining row was selected. Accordingly V and Z are exactly zero and every
issued Brier loss is public. The reporter returns these exact points, while
retaining its generic centers as audit information. The two hard-enabled
historical smoke episodes exercised this branch without any private labels.
On mixed-key episodes, hard-enabled `n_live` was positive; this exercised the
usual translated intervals rather than relying only on the exact exception.

The implementation preserves an empty interval intersection as
`confidence_conflict=true`. The small owned traces here did not produce an
empty intersection; that behavior was checked from the bounded min/max
construction, not inferred from a nonexistent sampled failure.

## Concrete finite checks

The initial run completed **38/38 checks** with **13 exact formula
comparisons**: the four old smoke reports, those same four episodes through
the current subject, four new mixed-key episodes, and one one-bit ticket
episode. The public tape encodings and all selected purchases are saved.

| Public episode | Selector / hard use | `n_live` | Report units |
|---|---|---:|---:|
| Repeated smoke | Uniform / off | 6 | 9,536 |
| Repeated smoke | Uniform / on | 0 | 9,004 |
| Repeated smoke | Tickets / off | 6 | 9,888 |
| Repeated smoke | Tickets / on | 0 | 9,382 |
| 128-character tag, mixed keys | Uniform / off | 9 | 15,292 |
| 128-character tag, mixed keys | Uniform / on | 8 | 15,382 |
| 128-character tag, mixed keys | Tickets / off | 9 | 15,879 |
| 128-character tag, mixed keys | Tickets / on | 8 | 15,975 |
| One action bit, B=2 | Tickets / on | 2 | 6,462 |
| Focused nonfavorite selection | Tickets / on | 6 | 16,229 |

The old/current smoke formula results and resource totals were equal. The
initial ticket samples selected only the favorite, including both its own
ordinary ticket and extra tickets. The prospective
[`selector_addendum.md`](selector_addendum.md) records this concrete gap and
one extra episode, chosen using only already public first-draw/favorite
information. Its first block selected offset 0 while the favorite was 3,
so its selected probability was 1/8 and multiplicity 1. Later blocks selected
the favorite through extra and ordinary tickets. The independent formulas
agreed throughout. This raises the total to **14 exact formula comparisons
and six fresh owned episodes**, without altering the first run or selecting
on unpurchased outcomes. The focused report used 16,229 units and at most
50 integer bits. See [`nonfavorite_v1/summary.json`](nonfavorite_v1/summary.json).

## Finite width and all-path report funding

The width audit uses the maximum admitted public contract: T<=8192,
B<=1024, m<=4096, h<=32, and <=1024 words per complete key. For a coarse
bound, T<=2^13, m<=2^12, D<=2^32, P<=2^11, M<2^11, and R<2^18. Summing
absolute terms bounds every prefix, without assuming favorable cancellation:

| Intermediate | Conservative absolute bound |
|---|---:|
| U numerator | <2^66 |
| A numerator | <2^98 |
| Width numerator | <2^54 |
| Q numerator / denominator | <2^120 / <2^86 |
| Common output denominator | <2^107 |
| Sampling-radius numerator | <2^125 |
| Each scaled base center | <2^130 |
| Each scaled correction | <=2^120 |
| Each live center | <2^131 |
| Action-plus-sampling radius numerator | <2^126 |
| Interval arithmetic endpoints | <2^132 |

For example, common/(DM)=8RDM and common/(D²M)=8RM; cancellation here is an
exact symbolic divisibility fact, not a numerical assumption. The action
radius is <=144<2^8. Every source arithmetic operation is covered by these
operand/product or prefix bounds. The meter's conservative pre-operation
bit count adds at most the operand-bit overhead; **134 bits** is a safe
coarse envelope, below its 256-bit contract. A separate exact upper-bound
table for the twenty (B, selector) maximum-T/maximum-D combinations has
largest named magnitude **115 bits**. The largest observed production
pre-operation value was **50 bits**; finite observations alone are not the
all-input proof. The direct overwidth probe also rejected its multiplication
before charging that rejected operation, preserving the prior paid operation.

For report cost, at most Tm retained-key comparisons cost <=4100 each; the
selected-key comparisons cost <=2052 each. Their combined upper bound is
137,581,576,192 units. Static source inspection finds 50 per-row integer
call sites when both mutually exclusive branches are counted; each costs
<=52 units at 256 bits. A deliberately loose 100,000-unit row allowance
covers those operations, row/key/shape reads, receipt binding, and storage.
The separately bounded block records and global square roots, exact output
pairs, and fixed metadata then yield total report cost at most
**138,434,527,232 units**, below 2^38. The declared 2^48 completion cap exceeds
this envelope by more than 2,000 times. Full arithmetic tables and source
counts are in [`run_v1/finite_bounds.json`](run_v1/finite_bounds.json).

This is a bound for the declared word-record service, including its priced
native integer/square-root and exact-output operations. It is **not** a CPU
cycle count, physical memory bound, or a price for audit JSON. Source
enrollment is a separate deployment charge and remains outside the report
cap, as specified by the broker/common interface.

The all-path flag was withheld from a successful report with limit 2^48-1,
and from a successful report whose broker funding premise was false. At
2^48 with the broker premise present it was eligible under the stated
mathematical assumptions. An actual late failure at limit 15,381 retained
**14,358 spent units**, including the prepared terminal status, denied the
last 1,024-unit bundle, returned `failed`, and suppressed every interval.
The successful version of that report costs 15,382. There is no refund of
the failed prefix and no confidence assertion conditional on its success.

## Limits and disposition

The reporter deliberately consumes a completed **trusted local broker**
record. It does not re-execute the learner, replay hidden supplied action
bits, derive the selector's favorite from the advice, independently prove
provider receipts, or authenticate caller-supplied data. It validates the
reported ticket law against the owned favorite and selection, and validates
hard usage against chronological checked receipts. The caller's owned
broker and sound provider remain load-bearing assumptions.

The `confidence_eligible` metadata is explicitly conditional on fresh fair
supplied bits, action-independent history, and all-path completion; the
development seeded generator does not establish those assumptions. The
report is per declared episode at a fixed endpoint, with no simultaneous
multi-arm or conditional-on-success coverage claim. Its exact identities
and exact-all-known outputs can still be checked without probabilistic
coverage. The existing empty-intersection flag is not a repair of a failed
probability event.

All public expected values, actual reports, failure records, source hashes,
and commands are retained under this directory. No reporter repair is
requested on this evidence. Any later source change needs an explicit
dependency disposition; these results bind to the SHA-256 above.
