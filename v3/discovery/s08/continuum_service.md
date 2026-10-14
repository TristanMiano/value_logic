# Prospective continuum receipt-learning service

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
Follows the executed cont01 polynomial checks. Preserve all earlier exposed
records. This experiment uses the three fee vectors already exposed in ms01,
with new off-menu repeat probabilities 1/5, 2/5, 4/5 and 1,024 fresh requests
per environment. Seeds 8141470 through 8141478 are assigned size-major then
rho-major. No claim of held-out confirmation is attached to these new rows.

Prepare five interval policies at the old menu values, then certify each
policy's exact expected-fee polynomial over the entire rho continuum. The
menu selects a finite **policy bank**, not a restriction on the true source.
Compile a fixed partition of [0,1] into 64 rational bins. On each bin record
checked fee upper bounds and the policies whose expected fee is within
epsilon=1/10 audit-fee unit of every bank policy throughout that bin. The
partition may be inconclusive; uncovered acceptable regions are not invented.

Restrict each policy polynomial once per bin; differences of those restricted
coefficient vectors give the pairwise bounds. Independent checking validates
the source/roots, polynomial identities, exact interval endpoints, all 64 bins,
coefficient transformations, fee maxima and every claimed acceptable policy.
A runtime interval may intersect several bins. A policy is acceptable only
if it is in the intersection of all their certified masks. Scanning bins is
allowed in this first implementation but must be billed; faster range-query
structures remain a possible repair, not an unpriced assumption.

Five arms: full audit; cached static robust policy over [0,1]; continuum
Hoeffding learner; an identical ordinary learner; and a plug-in empirical-rho
policy at the same count epochs as a diagnostic. Each arm pays its own
admission, appropriate preparation, execution, proof checking and retention.
The static robust policy needs the same polynomial bank and fee bounds but
does not need pairwise decision-region masks; record the narrower setup bill.
The plug-in arm needs the polynomial bank but no bins; it makes no interval
fee-guarantee claim. All arms produce and check exact current-row actions.

The warranted learner maintains one cumulative intersection of time-uniform
Hoeffding intervals from first-middle/next-neighbor pairs, updating its
selection only at cumulative pair counts 0,1,2,4,...,512. It may retain a
count-epoch interval between updates. If a policy is certified epsilon-optimal
over that interval, freeze the interval and policy and stop statistical
updates. Otherwise choose the policy with the smallest maximum certified
fee across intersected bins. The plug-in arm does not permanently stop;
between epochs it reuses its selected bank policy. The actual horizon is
1,024, so a statistical stopping error is evaluated under that finite workload
rather than advertised as zero-error infinite-horizon identification.

Report every request, receipt, action, fee, setup and named operation invoice,
statistical samples/epochs, stopping interval and observed true-parameter
coverage. Compare expected bank fee at the true parameter only as a diagnostic
after execution. Record worst conditional expected excess, cumulative expected
physical-fee regret and realized fee separately. Hidden rows and true rho are
not inputs to the learner. Single-run timings and named units are partial
cost measurements; no complete-cost or independent-confirmation conclusion
follows from them alone.
