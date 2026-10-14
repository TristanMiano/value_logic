# Learning the useful policy from compulsory receipts

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
This is an exposed-row mechanism ablation, not independent confirmation.

The initial [Markov service](ms01/results.json) completed 13,824 zero-regret
outputs across nine environments and six arms. Its partial-observation
likelihood learner retained only the true menu member in every environment,
but repeatedly processing full receipt patterns and growing integer weights
was expensive. The identical ordinary learner tied it. Learning did not
establish a new class advantage.

[The compulsory-pair derivation](forced_calibration.md) gives an ordinary
Bernoulli sample at no additional **physical** purchase: after the first
middle receipt, the next adjacent receipt is required by the action duty.
Under the stated stationary symmetric homogeneous Markov source, its repeat
probability is exactly rho even when the first query adapts across requests.
[cell01](cell01/results.json) verifies this law in 135 small cases. A loose
upper certificate passes the old fee checker but is rejected by the new
equality checker: exact values are necessary for the claimed policy-cell
stopping rule.

[pl01](pl01/results.json) completes another 13,824 zero-regret outputs, using
the same nine environments and rows as ms01. Six arms compare Hoeffding and
mixture-likelihood confidence sets, each with cell stopping, an ordinary
mirror, and a continue-to-singleton diagnostic. Every ordinary mirror ties
its corresponding candidate. No observed true-model exclusion occurred;
this single run is not a calibration experiment.

| Case | Static robust fee / units | Full likelihood fee / units | Pair-mixture cell fee / units | Pair samples / stop before row | Retained rho numerators |
|---|---:|---:|---:|---:|---|
| n6, rho=.1 | 6,463 / 179,927 | 5,715 / 1,781,012 | 5,755 / 167,169 | 8 / 11 | 1, 3 |
| n6, rho=.5 | 7,191 / 179,887 | 7,191 / 1,770,001 | 7,191 / 168,032 | 4 / 4 | 5, 7, 9 |
| n6, rho=.9 | 6,603 / 180,203 | 6,603 / 1,855,668 | 6,603 / 168,644 | 4 / 8 | 5, 7, 9 |
| n10, rho=.1 | 6,797 / 379,312 | 6,669 / 3,559,922 | 6,727 / 394,374 | 62 / 122 | 1 |
| n10, rho=.5 | 8,420 / 380,376 | 8,420 / 3,271,045 | 8,420 / 371,654 | 14 / 30 | 3, 5 |
| n10, rho=.9 | 7,860 / 379,370 | 7,860 / 3,337,383 | 7,860 / 367,286 | 2 / 3 | 3, 5, 7, 9 |
| n16, rho=.1 | 13,718 / 830,358 | 13,044 / 6,428,690 | 13,190 / 831,221 | 40 / 75 | 1 |
| n16, rho=.5 | 16,791 / 832,727 | 16,791 / 5,991,141 | 16,791 / 870,042 | 87 / 205 | 5 |
| n16, rho=.9 | 16,075 / 832,578 | 16,065 / 6,157,218 | 16,067 / 824,808 | 19 / 38 | 9 |

Rows are zero-indexed; all 256 requests per arm remain in each invoice.
Fees and named computation units are distinct quantities, not an established
exchange rate. Setup includes five policy proposals and 25 cross-model exact
value certificates per learning arm. Complete service costs are not supplied
by this partial operation model. Static robust selection is recomputed each
request in ms01 and can itself be cached, so its listed overhead is not a
strongest implementation lower bound.

Cell stopping avoids unnecessary inference: in n6/rho=.1, the mixture cell
arm stops after eight samples with {1,3}; singleton identification takes 51
samples, with the same physical fee but 17,565 more named units. The Hoeffding
cell arm stops after 36 samples; its singleton arm has not identified the
parameter after 134. Conversely, the n10 and n16 low-rho cases need a singleton
to share a minimizing bank policy. Stopping and sampling costs depend on the
actual decision geometry; the source parameter is not always disposable.

These certificates concern expected **future physical fee** within one fixed
policy bank and source family. Exact original-source output checks retain
zero realized action regret regardless of whether the learned model is right.
The statistical guarantee has explicit alpha=1/20 per deployed confidence
procedure. The finite model menu and stationarity remain assumptions.

**Constructive next move:** remove the arbitrary five-point menu premise for
rho while preserving receipt-only calibration and checked policy comparisons.
Do not relabel an off-menu source as a confidence failure of a theorem that
assumed menu membership. A continuum method must pay for its richer expected
fee certificates and retain comparisons with ordinary parametric verification.
