# Receipt-learning star service: prospective development declaration

**Codex (GPT-6), October 14, 2026 UTC. DEVELOPMENT.**
Based on the [star derivation](star_audits.md), checked by
[star01](star01/results.json): 26 cases, 27,652 Bellman states and 789 leaf
orders. Three cases strictly favor leaf-first. The worked case has expected
fees 12 for center-first and 14317/2000 for the optimal route. These were
conditional calculations with zero acquisitions. Separately, the binary
minimax equality matched 144 information states and 7,560 action evaluations.

## Admitted source and evidence order

Use the original independent exactly-one CNF with a star of four leaves.
The source cost alphabet is now {0,1,2}; each positive unit edge contributes
two choices as in the derivation. Source factorization and the cost-map
alphabet must be checked anew. The request requires zero realized regret.
Every arm sees the same public source, sensor menu and physical audit fees.
The hidden law is independent across vertices and fresh requests. Parameter
values are withheld from all service controllers except the labelled oracle
diagnostic. This contract is supplied by the synthetic generator; deployed
source independence is not claimed to have been learned from finite data.

Before generating hidden rows, freeze implementations, source declarations,
arm rules, parameters, seeds and request counts. Buy receipts sequentially and
flush each prefix to disk before the next query. Stop only when every edge
has a known extreme endpoint or both endpoints are known. Construct and check
an actual original-source satisfying action and its exact local dominance.
Only after the output is durable may the diagnostic read the hidden full row.

## Policies and statistical rule

Compare center-first, full identification, a conservative receipt learner,
the same ordinary AND-ordering learner, and an oracle-law diagnostic. The
learner starts center-first with empty counts. Before each request it forms
one confidence interval for each extreme probability using **previous** paid
receipts only. Select the ratio-ordered leaf route when the lower savings
under leaf lower bounds and the center upper bound is positive; otherwise
use center-first. After the checked output, update counts from acquired
receipts. There are no free training audits or truth labels for unqueried
vertices. The ordinary learner has the identical information and kernel.

Use alpha=1/20 and m=5 coordinates. At each sample count n>=1, assign failure
alpha/(m*n*(n+1)). Let L be the least integer with
2^L >= 2*m*n*(n+1)/alpha. Choose the smallest nonnegative grid radius r=k/1024
with 2*n*r*r>=L. Since e>2, the two-sided Hoeffding tail is at most
2*2^(-L), which is no larger than the assigned failure allowance. All
rounding and comparisons in the implementation use integers/rationals.
The clipped empirical interval and [0,1] at n=0 are conservative. This is
deliberately simple and may learn slowly. The common event covers every
vertex, count and later policy choice; it does not license source changes.

## Fixed development matrix

Three 2,048-request environments, each with four leaves:

1. Favorable route: fees (10,1,1,1,1), extreme probabilities
   (1/2,9/10,9/10,9/10,9/10).
2. Unfavorable route: fees (2,1,1,1,1), extreme probabilities
   (4/5,1/2,1/2,1/2,1/2).
3. Unequal leaves: fees (9,1,2,1,3), extreme probabilities
   (2/5,19/20,4/5,9/10,3/5).

Split extreme probability equally between values 0 and 2. Use independent
Python pseudorandom streams with seeds 814140..814142; their reproducibility
is development evidence, not a proof of a physical sampler. Every arm receives
the same row values but buys its own receipts. Save each arm's complete
trace and post-output diagnostics, including every switch and confidence
state. No selection of a favorable subset after exposure.

## Resource and comparison scope

Charge source admission, actual audit base fees, receipt checking, policy
selection, confidence calculation, updates, action construction and checking
in named units; measure serialized bytes and whole-arm CPU/wall work. Provider
preparation, code admission, host work not represented by named units,
storage byte-time and external unit prices remain separate terms. Report
physical-fee savings and the compute/audit-price break-even relation, not a
complete economic win with unpriced terms silently zero. An identical ordinary
learner must tie; compare with that control before making a novelty claim.

The declared run is DEVELOPMENT, has no promotion event, and leaves F01 intact.
