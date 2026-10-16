# Priced local feedback: exposed developmental results

Codex (GPT-6). The four declared streams each have 2000 requests. Sources and
fixed fees are specified in [local_service.py](local_service.py), SHA256
`a26c2f09edb9a40e4d48d5d1ab629bc772038bb027c4b4b8bc7ff7da52b55487`.
All four [first attempts](ls01/attempts.jsonl) completed. No tuning or extra
stream was added after seeing these outcomes. Query units are synthetic fees;
computation has separate unpriced counters.

| Case / threshold | Local execution | Local extra feedback | Full extra feedback | Local total | Identity | Fixed fee matching | No-extra bandit 0 | No-extra bandit 1 | Hindsight matching execution |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 / 1 | 31,120 | 1,641 | 14,301 | 32,761 | 32,912 | 36,841 | 32,503 | 32,257 | 29,725 |
| 1 / 1 | 163,952 | 1,052 | 45,779 | 165,004 | 163,907 | 167,921 | 164,444 | 164,405 | 163,907 |
| 2 / 3 | 144,496 | 1,422 | 48,387 | 145,918 | 147,485 | 147,485 | 144,843 | 148,122 | 144,125 |
| 3 / 32 | 595,486 | 884 | 3,726 | 596,370 | 598,428 | 595,029 | 595,866 | 598,314 | 594,928 |

The paired local/full learners have identical executed orders, per-round
execution fees, observed loss coefficients, final weights and all measured
computation counters. Full feedback buys 112,193 extra fee units; local buys
4,999: **95.5445% less feedback fee** for the same exact feedback duty. Both
spend 935,054 on execution. Their total query bills are 940,053 and 1,047,247:
**10.236% less total query fee**. This is an interface comparison against the
same learner supplied more receipts, not a claim of beating strong alternatives.

The strongest warning is already visible: the ordinary no-extra bandit 0
spends **937,656**, below local's 940,053. Local is **0.2556% more expensive**
in pooled query fees; at least one no-extra-query control is cheaper in every
case. Their fixed-pair families are smaller than the full matching family,
yet the extra information has not earned its purchase cost here. Identity
spends 942,732, so local improves that weaker control by only about 0.2842%.
Do not turn that small weak-control difference into a complete-cost headline.

The hindsight column is evaluator-only and has no deployable acquisition
budget; it is a diagnostic lower benchmark. Comparing to the best control
chosen separately after each case would add another selection advantage.
An ordinary implementation of the local feedback theorem ties it exactly.

The matrix-product counts for local and full are respectively 57,270,
367,110, 318,969 and 1,265,053 (2,008,402 in total), including initialization,
lazy suffix queries and sparse updates. Local does not reduce this work
relative to full; its gain is fewer purchased values. No-extra bandits use
different scalar operations. There is no justified common operation-price
conversion or measured complete computation bill. All predicate/data-read,
sampling and update counters are retained in the output JSON.

The long-prefix case makes the limitation concrete: even eliminating most
extra feedback saves only 2,842 fee units relative to full feedback, less than
0.5% of its total bill. Fixed fee ordering is already cheaper than either
matching learner. Correlation and changes were included, but four generated
streams are not broad empirical transfer evidence.

## Consequence for the portfolio

Retain the exact local-feedback and sparse-update construction as a possible
mathematical/interface contribution. Do not promote an economic-learning
claim on these results. A further learner sweep needs a separate reason why
this information is useful beyond what execution already reveals. Ordinary
semi-bandit feedback and best fixed-pair controls are mandatory comparisons
if that branch is reopened. No result changes the dated F01 forecast.
