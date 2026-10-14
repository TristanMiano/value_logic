# Paid receipt learning: first executed comparison

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The [declared run](star_learning_design.md) completed using
`python v3/discovery/s08/star_learning.py v3/discovery/s08/learn01`.
Its [implementation](learn01/impl.py), [design](learn01/design.json),
[results](learn01/results.json) and per-arm receipt/output logs preserve all
three environments and five arms. Every arm made 2,048 checked outputs in
each environment: **30,720 outputs total**, all zero-regret against the
post-output revealed original-source costs. This is development on a supplied
independent synthetic source, not a transferred independence guarantee.

| Environment | Center-first fee | Learner fee | Oracle-law diagnostic fee | Learner named units | Center-first named units |
|---|---:|---:|---:|---:|---:|
| Favorable | 24,524 | 16,500 | 14,845 | 1,232,630 | 501,341 |
| Unfavorable | 5,724 | 5,724 | 5,724 | 1,089,100 | 474,765 |
| Unequal leaves | 27,336 | 27,336 | 23,681 | 1,167,840 | 512,825 |

The ordinary receipt learner ties the learner exactly in fees, physical audit
counts, named units, confidence counts and routes. The new service integrates
the inherited AND ordering with actual paid cost observations and a pathwise
action checker. It establishes no new policy advantage over that control.

In the favorable environment the first leaf-first request is zero-based index
346. The learner buys 7,950 physical audits versus center-first's 6,092, but
their different fees matter: it avoids many expensive center audits. The
8,024 base-fee saving comes with 731,289 additional named units, before other
resource terms. With compute price K and audit-base price A, the measured
portion improves only if A/K > 731289/8024, approximately 91.14. This condition
is incomplete until the other cost differences are included.

The unfavorable environment stays center-first and pays learning overhead
with no physical-fee benefit. The unequal environment also stays center-first:
the conservative confidence box does not warrant the oracle-law route within
the executed horizon. A supplied oracle law is a diagnostic, not free input to
an implementable comparator. These outcomes rule out describing every
receipt update as useful progress.

The next repair will reuse a confidence/route certificate between explicit
update epochs. Under a fixed parameter source, a previously warranted box
does not expire merely because another receipt arrives. Recomputing the same
statistical duty on every request is unnecessary. A doubling update schedule
is an ordinary amortization method; any resulting gain must be attributed to
that implementation and compared with an identical ordinary cached learner.
It may delay a useful route switch, which must also be charged.

## Executed epoch repair

The first epoch implementation failed before its first audit because the
generic content hasher did not encode rational confidence fields. Its source,
design, header and [failure record](learn02/failure.json) remain intact.
V2 canonicalizes the exported rational payload before hashing. The command
`python v3/discovery/s08/epoch_learning.py v3/discovery/s08/learn03` then
completed all six amended arms: three environments and an identical ordinary
control, 2,048 requests each, **12,288 additional DEVELOPMENT outputs**.

Only 12 probability certificates are constructed per arm. The favorable
route now switches at request 512, 166 requests later than v1. It pays 17,186
base-fee units and 608,093 named units, versus v1's 16,500 and 1,232,630. Thus
it spends 686 more in physical fees to save 624,537 named units. Relative to
center-first, the measured portion has 7,338 fee units saved for 106,752 extra
named units, requiring A/K>106752/7338, approximately 14.55, before other
terms. This is a more plausible conditional price region, still not a complete
economic claim or superiority over the ordinary cached learner, which ties.

The unfavorable and unequal environments remain center-first. Their named
units fall to 498,707 and 550,927, respectively; learning still costs something
without changing those actual purchases. [Results](learn03/results.json) keep
the certificate hashes, receipt counts, schedules and exact exported sizes.
All data were already exposed in v1, so this is a development ablation.
