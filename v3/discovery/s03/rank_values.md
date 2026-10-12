# S18: exact value curves for rank-dependent decisions

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

S13Q is exact for a chosen coordinate query interface; it can miss cheaper
physical observations of equivalent facts. This branch admits an arbitrary
finite library of priced linear binary observations, but narrows the terminal
objective to one whose value depends only on remaining dimension.

## Full-assignment prediction

Let z be uniform on F_2^d. Query j reveals a_j z at fixed price q_j>=0. The
terminal action guesses the whole z, with utility one for an exact guess and
zero otherwise. After a history spanning rank r, the conditional law is uniform
on 2^(d-r) consistent assignments. Its optimal stopping value is

    v(r) = 2^(r-d).

The values of observed bits change the guessed assignment, but not v(r).
Dependent queries add no information and can be skipped. Every adaptive policy
therefore has expected net value E[v(rank S)-sum_{j in S}q_j], no greater than
the best fixed subset. A fixed best subset followed by any consistent guess
attains the bound. More generally this proof works for any declared terminal
decision problem whose optimal conditional value is a known v(r) independent
of observation outcomes. It does not hold for arbitrary coordinate-weighted
prediction objectives or nonuniform priors.

## Ordinary greedy cost profile

The independent query rows form a linear matroid. Sort by nondecreasing q and
append a row whenever it increases rank. Let the selected rows be g_1,...,g_R,
and K_r=sum_{i<=r}q_{g_i}. Each prefix is a minimum-cost rank-r independent set.
For a direct proof, before g_i is accepted, all strictly cheaper rows have rank
at most i-1. Any independent set of size r with sorted costs s_1,...,s_r must
therefore satisfy s_i>=q_{g_i}. Summing gives cost>=K_r, attained by the prefix.
Any dependent set contains a same-rank basis of no greater cost. Consequently

    optimal value at multiplier lambda = max_{0<=r<=R}[v(r)-lambda K_r].

One sorted elimination pass supplies all future price queries, all hard-budget
queries max_{r:K_r<=b}v(r), and (via the concave hull of (K_r,v(r))) expected-budget
lotteries. This is an ordinary matroid-greedy reduction, not a new optimization
algorithm. Exact arithmetic for the full-state objective has O(d)-bit dyadic
values. Returning an action also needs a consistent-completion solve, which
must be charged if the service promises executable decisions rather than values.

The classical antecedent is Edmonds, *Matroids and the greedy algorithm*,
Mathematical Programming 1 (1971), 127-136. A primary publisher's reference
was located through [An Exact Characterization of Greedy Structures](https://epubs.siam.org/doi/10.1137/0406021).
The original DOI and a course-hosted primary PDF were inaccessible in this
retrieval. The prefix-cost proof above is reconstructed directly; no unread
theorem hypotheses or claimed implementation speed are imported.

## Affine revisions and probability content

For a uniform consistent affine source x=x0+N z, map each physically available
query c_j x to row a_j=c_j N and phase c_j x0. A consistent right-hand-side
revision with fixed A changes phases but not rows, ranks, costs or the value
curve. Reuse the sorted rank profile; update action readout and reject
inconsistent revisions using the checked affine compiler. This removes the
free-coordinate access restriction for this full-assignment objective. A query
library with rank R<d can never reduce the residual uncertainty below d-R.

Here the value has explicit probabilistic content: v(r) is the mass of the most
likely assignment under a uniform remaining source. Knowing that scalar does
not identify which affine subspace or assignment is likely; the checked relation
and actual observed phases are still needed to choose an action. Value reuse
across revisions can coexist with a changed correct action.

If a fallible uniform model Q is only known to lie within total variation epsilon
of the true law P, and every policy's total cost is bounded by C, its net utility
lies in [-C,1]. The difference in its expected net value is at most (C+1)epsilon.
Thus the Q-optimal policy's regret under P is at most 2(C+1)epsilon, by applying
the bound to that policy and a P-optimal one. This is an ordinary robust bound,
conditional on a warranted epsilon; equal bit marginals do not warrant it.

Next check the rank planner against explicit adaptive beliefs for arbitrary
linear-query libraries. Keep the change of terminal objective visible: the
algorithm does not solve the general selected-coordinate value problem.

## Executable development and an objective limitation

[rank01.json](rank01.json) compares 36 arbitrary linear-query libraries with
explicit adaptive beliefs on 7,036 states and checks 4,780 query subsets.
All rank costs and net values agree. There are 1,024 consistent-guess checks,
including exact average success matching the declared value, and inconsistent
labels are rejected. On a supplied 128-dimensional, 512-query library,
construction takes 1.311 ms, the rank profile 2.238 ms, 129 naive price scans
23.390 ms, and an actual consistent completion 0.127 ms. Acquiring real query
labels is not timed; those observations are supplied.

The large price range [0,8] selects full rank throughout, so it is not evidence
for a diverse changing-rank workload. Full-assignment success grows exponentially
with rank; with equal query costs, convexity makes either no queries or maximum
available rank optimal. This terminal objective can therefore collapse to a
simple all-or-none choice. Preserve that limitation rather than presenting the
implicit world count as a standalone practical gain.

## Minimax reports need no uniform prior

Suppose only that the true assignment belongs to the current nonempty affine
source S. The action is a normalized probability report p on S, scored by
log_2 p(x) at the true x. Since min_{x in S}p(x)<=1/|S|, the best worst-case
score is -log_2|S|, uniquely attained by the uniform report. With h=d-r free
dimensions this is -h. The worst-case improvement after rank-r observations
is exactly r bits. This is an operational minimax report, not an assertion that
nature draws uniformly or that those probabilities are calibrated beliefs.

For fixed query prices in the same score units, maximize r-lambda K_r. Since
the ordinary greedy marginal costs are nondecreasing, accept independent rows
while their price is below 1/lambda (ties are indifferent). Any adaptive path
has a rank/cost pair no better than the corresponding cheapest prefix. To cover
arbitrary reports and randomized policies rigorously, average their score over
a hypothetical uniform true assignment. At every history, Jensen's inequality
gives the conditional average log score <=-log_2|S|. Hence their uniform-average
net score is no greater than the best rank prefix, and their worst-assignment
expected score cannot exceed that average. A fixed prefix with uniform reporting
attains the bound at every assignment. Uniform averaging is a proof device here,
not an adopted belief. The score is finite on the declared source; no guarantee
is made when the true assignment violates the premises.

This construction connects paid logical refinement to a probability-reporting
action without inventing a subjective prior. Its ingredients are standard
minimax logarithmic scoring, source cardinality and linear-matroid optimization.
Its expected-value analogue still needs a distribution. The two decision
criteria must not be silently interchanged.

## A bounded price for trusting a fallible model

Let f be any normalized forecast on S, and choose eta in [0,1). Report

    p_eta(x) = (1-eta)/|S| + eta f(x).

Then p_eta(x)>=(1-eta)/|S| for every x in S, so its log score loses at most
-log_2(1-eta) bits relative to the minimax uniform report, regardless of model
accuracy. At eta=1/2 the worst-case price is one bit. A good model can improve
the score sharply on the realized assignment; a wrong model cannot exceed the
declared loss bound. eta may be chosen from available information before the
unresolved assignment is scored; no calibration claim follows merely from it.

Normalization and support are real obligations. A convenient executable family
uses a product or autoregressive distribution over the remaining free binary
coordinates of a checked affine parameterization, then pushes it onto S. This
gives normalization by construction and avoids a general partition-function
oracle. Its factors must lie in [0,1]; exact evaluation and source mapping are
charged. A changed assumption may alter f and the action while the minimax rank
value remains unchanged. The protected uniform component still depends on a
correct nonempty source; it does not rescue an unsound logical premise.

The same guarantee is ordinary probability smoothing/mixture reasoning. The
developmental target is a small executable report/query interface with explicit
semantic revisions and costs, not a new foundational probability theorem.

## Conditioning spends the same trust budget differently

The protected uniform weight is not constant under Bayesian conditioning. If
an event E has probabilities u(E) and f(E), the model's conditional weight is

    eta_E = eta f(E) / [(1-eta)u(E)+eta f(E)].

Its future worst-case log-score surcharge is -log_2(1-eta_E), which can exceed
the original -log_2(1-eta). For two free bits, a point model at 00 and eta=1/2,
observing the first bit 0 has report mass 3/4 and changes eta to 2/3. Reporting
the wrong remaining bit then has probability 1/6, versus uniform 1/2: the
conditional surcharge is log_2 3, greater than one bit. The favorable prefix
already earned log_2(3/2), leaving the original whole-sequence one-bit bound
intact. Resetting eta to 1/2 after each observation gives a new per-step policy,
not the conditional law of the original report; its cumulative bill can grow.

[report01.json](report01.json) checks exact normalization on 32 affine sources
and 1,836 partial point-probability ranges/event probabilities. A separate
minimax log-score profile selects 23 distinct ranks across 128 prices; its
construction costs .793 ms and naive scans 12.024 ms. These are supplied kernel
examples. The first invocation failed with an unexplained integer-shift-by-tuple
TypeError; [failure](report01_failure.json) and logs are preserved. Source
inspection and a simple sanity check did not find a deterministic cause. The
one unchanged source/runtime/seed/output-artifact retry completed. The failure
is not erased, diagnosed as a runtime bug, or treated as independent replication.

Partial point-score receipts and event probabilities are different objects.
For a product model on remaining free coordinates, known coordinate values
give a product of their factors; unobserved factors range between their minimum
and maximum. Adding the protected uniform mass yields sharp point-probability
bounds, monotonically refined by more values. Summing over unknown coordinates
instead gives the event probability. Neither is automatically a confidence
statement about the adequacy of the forecast or source premises.
