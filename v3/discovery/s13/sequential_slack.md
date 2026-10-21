# Sequential acquisition of a fixed action-menu warrant

Codex (GPT-6), DEVELOPMENT, October21,2026. A small adapter of ordinary
time-uniform calibration, not a new statistical method or a measured saving.
It removes the fixed-N restriction in calibrated_slack.md under explicit
additional rules; it does not permit refitting the source on its audit data.

Keep the fixed independent score function Z, integer allowance domain,
i.i.d. stream of calibration worlds and truthful lower scores L_i<=Z_i.
Choose in advance increasing positive integers n_j and positive error
budgets delta_j with sum_j delta_j<=delta. For example n_j=2^j and
delta_j=delta/[j(j+1)] for j>=1. At checkpoint j choose the largest k_j with
Pr{Bin(n_j,alpha)<=k_j-1}<=delta_j. If there is no such rank, make no new
claim. Otherwise use epsilon_j=min(E_max,L_(k_j)-1) on the first n_j cases,
rejecting a negative result. Keep the largest previously accepted allowance.

For each fixed j, calibrated_slack.md's exact-score argument bounds the
event that its hypothetical allowance is unsafe by delta_j. A union bound
therefore makes every exact-score allowance safe simultaneously with
probability at least1-delta. At any time, any partial-score order statistic
is no larger than its exact counterpart. Thus arbitrary interleaving of
paid refinements across old cases, optional stopping of purchases, and
adaptive selection among already reached checkpoints preserve the same
event. Rechecking one checkpoint after refining its scores spends no new
statistical error budget. All original prefix cases must remain in the
denominator, including unfinished cases with their valid universal bounds.

This argument uses pathwise domination, so the lower scores need not form
an adapted or independent process. It does require the underlying original
Z_i to be the i.i.d. scores of the fixed task. Sampling new cases until they
look easy and discarding others, or changing the action source/goal/price
anchor in response to labels, is not licensed. Taking a maximum of safe
allowances is valid because the risk is nondecreasing in allowance and the
maximum is one of the accepted values. An unattained supremum needs its own
endpoint/tie treatment; use only finite recorded maxima.

The geometric checkpoints use log(j) error penalties, hence logarithms of
the sample-count logarithm in elementary tail approximations. No optimal
constant, sample-size guarantee, or equivalence to sharper confidence
sequences is claimed. Taking n_j=j with the same budgets is also valid and
potentially more conservative. If no checkpoint passes, the result is no
certificate; this task does not have a universally safe fallback for free.

This fills a concrete continuation duty: a bounded reasoner may retain and
gradually improve incomplete calibration work across sessions without fixing
its final audit budget. Cut/receipt costs and a useful economic comparison
remain open. Ordinary tolerance limits with error spending implement exactly
the same procedure. Hultberg, Zachariah and Ribeiro's
[Anytime-Valid Conformal Risk Control](https://arxiv.org/html/2602.04364v1)
already supplies stronger general sequential risk-control machinery; its
safe-endpoint assumption should not be silently copied to our no-certificate
case. No new simulation is needed for this immediate union-bound consequence.
