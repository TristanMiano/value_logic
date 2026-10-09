# P3-07 acquisition planning v1.1: narrow repair review

## Disposition

**PASS. The identified v1 preflight boundary is repaired, and all 24 revised
core identities and construction bills verify. No further issue was found
in this narrow follow-up. The v1.1 source freeze may end.**

Source SHA-256:
`88c73b82ac2809da8f31a8dcb93237e732f93b73665a42f5ec180d6355c782b7`.
The current source, saved run source and reviewer snapshot agree.

This is same-model, nonblind internal review, DEVELOPMENT, unmeasured, with
zero principal-clock credit. It checks the changed preflight and revised
saved accounts only. The previous mathematical/theorem audit was not repeated.
The v1 review, snapshots, checks and original run remain preserved.

## 1. The changed admission path

The frozen diff moves the 96-unit admission payment before cap/horizon guards
or resource-price inspection. It then admits only an exact Fraction price,
checks numerator and denominator bit lengths against 256, and only afterwards
compares the price with the finite allowed-price tuple. The caller's negative
numerator is inspected with `.bit_length()` directly, without an `abs()` copy.
The exact meter-type check remains the prerequisite for making a payment.

The source separately prepays two profile units before the two source metadata
reads. Only after obtaining the bounded file sizes does it fund source-byte
reading and hashing. Thus the previously observed metadata reads at zero
charged units no longer occur.

Thirteen focused probes checked the actual frozen implementation. No probe
reached a Bellman numeric calculation, generated a profile observation or
executed a future deployment.

| Boundary | Verified behavior |
|---|---|
| Zero admission budget, valid inputs | Budget denial before price equality, metadata or source-byte reads |
| Zero admission budget, invalid supplied values | Same budget denial before those guards reject the values |
| Funded invalid cap or wrong price type | Value rejection after the 96 admission units remain charged |
| Exactly 96 units, valid parameters | Two-stat bundle denied; zero metadata reads |
| Exactly 98 units, valid parameters | Two metadata reads occur after 98 units are paid; source-byte bundle denied |
| Exactly 8178 units, valid parameters | Two source-byte reads occur after 8178 units are paid; first Bellman bundle denied before numeric work |
| 257-bit positive/negative price numerator or denominator | Bounded-domain rejection after 96 units, with zero Fraction equality calls |
| 256-bit boundary numerator or denominator | Reaches the bounded allowed-price comparisons, then rejects the unsupported price after 96 units |

A temporary process-local Fraction equality interceptor would fail if an
oversized component reached equality. All three oversized-price probes
rejected before that interceptor was called. At-cap probes exercised the
comparison path, confirming the admission boundary is inclusive at 256 bits.
Instrumentation was removed after each probe and changed no source file.

## 2. Revised construction arithmetic and core identity

The unchanged adapter has 22,795 bytes. The planner grows from 9,047 bytes in
v1 to 9,515 bytes in v1.1. Consequently its charged read/hash work is

```math
2\left(\left\lceil22795/8\right\rceil+
\left\lceil9515/8\right\rceil\right)=8080.
```

That is 118 more units than the v1 charge of 7962. Together with the two new
metadata units, every plan costs exactly 120 additional units. With
`m=(N+1)(N+2)/2` states and `w=1024+64m` core words, the new total is

```math
96+2+8080+128m+64m+2w+w=11250+384m.
```

| Profile cap | States | v1.1 construction units | Cost at price 1/1000 |
|---:|---:|---:|---:|
| 1 | 3 | 12402 | 12.402 |
| 12 | 91 | 46194 | 46.194 |

Across all 24 separately constructed tables, the verified total is 703152
units, an increase of 2880. The auxiliary audit independently reconstructed
the 24 canonical core identities, source-size/stat-derived operation bills,
category totals, construction-resource vectors, byte counts and envelopes.
All match the saved v1.1 records. These are the stipulated resource-account
quantities, not measurements of machine instructions or CPU time.

## 3. Mathematical evidence preserved without recomputation

The auxiliary directly compared the saved v1.1 and v1 data rather than
recomputing the dynamic program. All 1128 Bellman state rows, root actions
and values, conditional-law records, expected profile lengths, deployment
probabilities and operating gains are exactly unchanged. All 9763 comparisons
in that narrow audit pass with zero mismatches.

Construction changes therefore account for every all-in-value change:

```math
G_{\rm allin}^{v1.1}-G_{\rm allin}^{v1}=-120u.
```

The difference is zero at price zero, -0.012 at price 1/10000 and -0.120 at
price 1/1000. The Bellman and optional-stopping conclusions retain the scope
and proof established in the preserved v1 review; no new arithmetic/theorem
claim is inferred from this source revision.

## Evidence and limits

- [Narrow review plan](v1_1_review_plan.json)
- [Frozen v1.1 source](v1_1_frozen_07_acquisition_planning.py)
- [Preflight probe source](v1_1_preflight_check.py)
- [Preflight attempt](v1_1_preflight_attempt.json)
- [Preflight results](v1_1_preflight_result.json)
- [Auxiliary revised-core/accounting review](auxiliary/v1_1/review.md)
- [Auxiliary verification](auxiliary/v1_1/verification.json)
- [Preserved v1 review](review_v1.md)

This focused follow-up establishes the requested repair and its exact cost
consequences. It does not reopen the broader interface or mathematical audit,
turn stipulated service laws into empirical evidence, price human model
acquisition, or make a CPU guarantee. No root source, companion, original run,
clock, ledger, gate or publication file was edited by the reviewers.
