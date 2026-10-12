# S11L: choose the value baseline for its continuation cost

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; Q2/Q3/Q4/Q5.
This derives a representation warning and constructive alternative. It is not
a novelty claim about belief compression or potential transformations.

## Conventional linear continuation, beyond state partitions

Poupart and Boutilier, [Value-directed Compression of POMDPs, §§3–3.2](https://www.cs.toronto.edu/~cebly/Papers/vdib.pdf),
give sufficient reward-preservation and compressed-transition identities;
§3.1 builds the smallest common invariant linear subspace containing rewards.
This is stronger than merging states with identical behavior. Section 3.2
also makes explicit the cost of finding the representation and the potential
absence of useful exact compression. These are direct antecedents, not new
results here. The present finite terminal-cost adaptation includes a constant
feature to recover observation probabilities; the paper's unnormalized
value recursion need not impose that stronger requirement.

In our deterministic finite system, let
K_eo f(x)=1[o(x,e)=o]*f(t(x,e)). For any potential b, transformed terminal
costs are r_a=c_a−b and charges q*_e=q_e+b∘t_e−b. If a feature matrix F spans
1, every r_a and q*_e, and K_eo F=F M_eo, then z=F^T p carries their expected
values and updates by z'_unnormalized=M_eo^T z. The constant coordinate gives
the observation probability. Normalize only nonzero-probability branches.
The same finite-horizon induction used for the partition proves equality of
optimal transformed values. Add the initial E[b] for absolute original cost.
The initial feature acquisition and operator construction remain paid duties.

If available deterministic observation histories identify every initial state,
closing a subspace containing 1 under all K_eo forces full rank: each identifying
history gives a product of K operators applied to 1 equal to that state's
indicator. This is a limit of this *observation-preserving closure*, not every
value representation. A zero-reward problem can ignore all such observations
and retain no state information for choosing its optimal policy.

## A baseline can create unnecessary exponential features

Take m=2n+1 Boolean signs x_i in {−1,+1}. All 2^m hidden assignments are possible;
the prior may have arbitrary correlations. Let S(x)=sum_i x_i. Two terminal
costs are c_0(x)=0 and c_1(x)=S(x). Operation i flips x_i at known nonnegative
price q_i, and produces a constant observation. At most H flips are allowed.
This is a stipulated finite intervention model, not a learned counterfactual
semantics or a free solver for unknown mathematical propositions.

With the fixed reference potential b=c_0=0, constant and coordinate functions
span all costs and are closed under each flip. The exact continuation space
has dimension m+1. A terminal-regret normalization instead chooses
b=min(0,S)=(S−|S|)/2, with r_0=(|S|−S)/2 and r_1=(|S|+S)/2. Preserving these
transformed values and their continuations requires dimension

    2^(m−1)+m,

even though both pipelines can ultimately choose the same optimal policy.

Here is a reconstructable proof. Walsh characters chi_A=product_{i in A} x_i
are an orthogonal basis under the uniform counting measure (used for algebra,
not as the controller's prior). A coordinate flip multiplies chi_A by −1 iff
its coordinate lies in A. Products of the operators (I±flip_i)/2 project onto
individual characters. Therefore the smallest flip-invariant subspace
containing given functions has dimension equal to their union of nonzero
Walsh supports.

Write M(x)=sign(S(x)). For a subset A of odd size 2k−1, choose i in A. The
discrete derivative of M in coordinate i is the indicator that the other 2n
signs sum to zero. Thus

    M_hat_(2k−1) = C * (−1)^(k−1) * binom(n,k−1)/binom(2n,2k−2),
    C = binom(2n,n)/2^(2n).

To see the conditional-product factor, a balanced vector has generating
polynomial product_j(1+t*x_j)=(1−t^2)^n. The coefficient of t^(2k−2), divided
by the number of subsets of that size, is its exchangeable product moment.
Even-degree coefficients of M vanish by sign symmetry.

Since |S|=S*M, its coefficient at degree 2k is
2k*M_hat_(2k−1)+(m−2k)*M_hat_(2k+1). Consecutive nonzero odd coefficients have
ratio −(2k−1)/(m−2k), so this equals M_hat_(2k−1), which is nonzero. The
degree-zero coefficient is m*C>0. Thus |S| contains every even-degree character,
2^(m−1) in total, and none at odd degree. S adds the m degree-one characters.
Both transformed terminal vectors generate this full union. Transformed flip
charges add no new support because they are differences of b and its flips
plus a constant. The stated dimension follows.

The regret-normalized representation is paying to preserve an avoidable common
component of all policy values. This is not a lower bound on choosing a policy,
nor a reason to abandon regret as a final certificate. The construction shows
why an action-comparison source and an absolute transformed-value source can
have sharply different continuation bills. A further potential change can
repair the bad pipeline; ordinary control theory permits that repair.

## Constructive controller using only marginal values

Let mu_i=E[x_i], obtained at an explicit acquisition cost. After flipping subset
J, the expected cost of terminal action 1 including computation is
sum_i mu_i + sum_(i in J)(q_i−2*mu_i). Repeated flips cannot help at nonnegative
prices: an even pair restores state, produces no information and wastes budget.
For action 0, doing no operation has cost zero and dominates any paid sequence
ending there. Therefore select up to H positive savings 2*mu_i−q_i, largest
first, and compare their total against immediate action 0. Correlations and the
remaining 2^m−m−1 prior parameters are unnecessary for this menu.

This exact special case is ordinary expected-cost optimization. Its relevance
is a concrete representation choice, not demonstrated advantage over a strong
conventional controller. Next: inexpensive exact spectral and policy checks,
then consider what survives genuinely informative or stateful observations.

## Sharp regret checking with uncertain marginal values

Suppose only l_i<=mu_i<=u_i is warranted, with −1<=l_i<=u_i<=1, and prices are
known. Every point in this box is realized by some distribution on the full
Boolean cube, so its bounds are sharp for this information. Correlations are
unrestricted. If another source restricts feasible worlds, the box remains a
relaxation and the following bounds remain conservative rather than sharp.
Acquiring a warranted box is an outstanding separate duty.

Let top_H(v) be the sum of at most H positive largest entries of v. For a fixed
deterministic plan J (flip J, then take terminal action 1), put q_J=sum_J q_i.
Its worst regret over the box, relative to every allowed deterministic plan
and immediate action 0, is exactly max(A_J,B_J), where

    A_J = sum_(i not in J) u_i − sum_(i in J) l_i + q_J,
    B_J = q_J − 2*sum_(i in J) l_i + top_H(v^J),
    v_i^J = 2*l_i−q_i if i in J, else 2*u_i−q_i.

Indeed, comparison with action 0 maximizes each coefficient of C_J separately,
giving A_J. For competitor K, C_J−C_K has coefficient −2 on J\K, +2 on K\J,
and zero elsewhere. Maximize it at l on J\K and u on K\J, then collect terms
depending on K; these are exactly v^J. Selecting the largest positive entries
solves the remaining cardinality constraint. Taking K=J shows B_J>=0.

Immediate action 0 has worst regret

    R_0 = max(0, −sum_i l_i + top_H(l_i+u_i−q_i)).

Here −C_K is maximized at u on K and l elsewhere. These derivations also give
explicit countermodels: retain the maximizing K and those endpoint means.
An independent-product Boolean distribution realizes the means. Thus a
proposed plan, a worst competitor and a box endpoint certify the exact bound
using O(m log m) rational comparisons/arithmetic, not 2^m probability entries.
This checks a proposed plan; it does not solve the general minimax choice of J
in that complexity, nor optimize randomized mixtures of plans.

For noisy point advice, baseline errors cancel when comparing two flip plans.
If |mu_i−mu_hat_i|<=epsilon_i, their cost-difference error is at most twice the
sum of epsilon_i on their symmetric difference. The selected plan need not
be trusted: the box oracle can certify its actual worst regret, give a concrete
obstruction, or recommend further acquisition. The uncertainty shared by all
action-1 plans still matters when comparing with action 0. This is a precise
instance of useful value refinement without recovering a full probability
distribution, using conventional robust decision methods as the comparator.

## Cheap executed check

[baseline01.json](baseline01.json), bound to [baseline_probe.py](baseline_probe.py)
and [flip_values.py](flip_values.py), checks the exact Walsh coefficients for
odd m from 1 through 11. At m=11 the fixed-reference dimension is 12 while
the regret-normalized dimension is 1,035 over 2,048 worlds. The finite
coefficients agree with the derivation; the derivation, not this finite test,
supplies the proposed arbitrary-odd-m statement.

The same run matches marginal advice to exhaustive allowed-plan costs for
72 explicitly saved correlated priors, and matches the proposed-plan regret
kernel and attaining countermodels against 31,676 box-corner/plan evaluations.
No sampling-risk guarantee or semantic model acquisition was tested. Exact
box certificates and representation consequences remain DEVELOPMENT; the
complete-cost benefit on a meaningful external task is still an open duty.
