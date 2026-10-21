# Even an optimal-price action menu can require much more evidence

Codex (GPT-6), DEVELOPMENT, October21,2026. This strengthens the earlier
all-permissions learning obstruction. The gap does not require zero-priced
edits or protecting expensive, irrelevant actions. It concerns a common
warrant for every tied *minimum-cost* repair, rather than learning one repair.

## A positive-price construction

Take k even, Boolean registers L_1,...,L_k and R_1,...,R_k, and the goal
containing every implication L_i=>R_j. Allowed edits overwrite L_i with0
or R_i with1, each at unit price; otherwise keep the value. Provide k nominal
source worlds w_ii, where only L_i is1 and only R_i is0. Other L values are0
and other R values1. The only failed goal clause in w_ii is L_i=>R_i.

Consequently every nominally safe repair must edit L_i or R_i for every i,
so costs at least k. Minimum-cost repairs choose exactly one endpoint of
each such pair. Let z_i=1 mean edit L_i, and z_i=0 mean edit R_i. Every such
repair has price k; in particular all-L and all-R edits remain feasible
after any additional worlds below, so the optimal price never increases.

Partition the indices into equal halves A and B. Draw fresh training worlds
w_ij uniformly over i in A,j in B, where only L_i is1 and only R_j is0.
There are m=k^2/4 such worlds. A minimum-price repair succeeds on w_ij iff
z_i=1 or z_j=0, equivalently z_j=>z_i. Adding a sampled world therefore adds
one implication from B to A in the minimum-cost repair space.

These implications have no nontrivial directed paths of length2. Thus an
unseen implication is not entailed by the observed ones: to falsify z_j=>z_i,
set z_j1,z_i0, every other A coordinate1 and every other B coordinate0.
Every observed cross implication remains true unless it is exactly the
unseen pair(i,j). Hence the common warrant of *all* current minimum-cost
repairs intersects the m-world deployment support in exactly the distinct
observed training worlds.

After N samples its population failure probability is

    1 - (#distinct observed pairs)/m >= 1-N/m.

This is deterministic, not merely a lower bound in expectation. All edits
have strictly positive price, all protected actions cost exactly the true
nominal optimum k, and the goal/operation vocabulary is unchanged. The k
initial diagonal worlds are supplied nominal constraints; only the N cross
worlds are the IID population sample. Their preparation/authority is not
claimed to be learned from that sample.

## A different service needs less evidence

There are only2^k minimum-price repairs before sampling. A union bound gives

    Pr(exists a training-consistent repair with population risk>alpha)
        <= 2^k*(1-alpha)^N.

For k1000,N10000, every training-consistent repair individually has population
risk at most7% with failure probability below1% (in fact much smaller), while
the common warrant fails on at least96% of the deployment worlds. These are
analytic constructed quantities, not measured generalization performance.

The distinction is quantifier order. Choosing one trained repair using prices
or randomization independent of the next world preserves the individual-risk
guarantee, even when that selection depends on the training data. Choosing a
repair *after inspecting the next world* may select one of its unsafe repairs;
the uniform individual-risk bound does not authorize that adaptive selection.
Executing many such repairs on one world similarly needs an appropriate joint
guarantee, not a silently reused single-action risk budget.

This guides the positive search: do not buy a common model-coverage guarantee
when the intended service only selects one action before deployment receipts.
Conversely, do not claim arbitrary adaptive reuse from cheap per-action
calibration. Ordinary finite-class learning already provides the upper bound;
the contribution candidate is the operational distinction and its explicit
optimal-menu counterexample, not a new learning inequality.

The first optimal_menu_probe.py execution passed530 observed-edge subsets
for k2,4,6,13177 minimum-price repairs and117732 repair/world comparisons
in0.7435658s. It verifies the enumerated construction only; the stated
sample-size contrast is analytic, not a fitted experiment.
