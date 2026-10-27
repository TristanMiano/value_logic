# Overlapping evidence: observed separators and a binary tree LP

Codex (GPT-6), October 26, 2026. DEVELOPMENT. New broad candidate prompted
by de Oliveira--Ishii--Lin2026 section7.1.2. No novelty or readiness claim
yet; compare robust classification with prescribed marginal distributions.

## Shared observed context

Suppose the known marginal channels are (S,X_i) conditional on a binary
state theta. They agree on the channel of S. All signals, including S,
are observed, and no other restrictions on dependence are imposed.
After observing S=s, the prior and marginal channels X_i|s,theta are
known. The compatible couplings are independent choices across s and
theta. Consequently the robust value is the S-weighted sum of the
conditional robust-fusion values. In the binary case the imported
Blackwell-supremum construction applies in each stratum. Its garblings
preserve s, so the conditional constructions glue into a compatible
joint channel. Zero-probability strata or states are omitted.

Treating the overlapping channels as unrelated black boxes can be strictly
weaker. Let S be a fair bit independent of theta, with prior theta1/2.
X reveals theta when S=0 and is an erasure otherwise; Y reveals theta
when S=1 and is an erasure otherwise. Each of (S,X) and (S,Y) alone has
prediction error1/4. Their ordinary unconditional Blackwell supremum is
the half-revealing experiment and also has error1/4. But compatibility
requires the shared S labels to agree, and the full signal always reveals
theta: error zero. Conditional specialization is the ordinary exact rule.
This is a constructed information consequence, not an empirical gain.

## Arbitrary junction-tree marginals, binary prediction

Let the full observed vector be Y. Known clique distributions
P_theta,C(y_C) for theta in{0,1} are mutually consistent on the separators
of a junction tree; the cliques satisfy the running-intersection property.
No conditional-independence restriction is imposed on a feasible full
distribution. Let p_theta be the prior and define weighted clique masses
M_theta,C=p_theta*P_theta,C. Consider binary 0/1 prediction.

Proposed exact LP for worst compatible Bayes error:

    maximize rho
    0 <= R_C(y_C) <= min(M_0,C(y_C), M_1,C(y_C))
    the R_C marginalize consistently on every tree separator
    sum_(y_C) R_C(y_C)=rho for every clique C.

There is one nonnegative table per clique. Empty separators enforce equal
total mass. Redundant rho equations may be removed. For a graph tree with
alphabet size q this has O(|edges|*q^2) entries, not q^|vertices|.
For a supplied width-w junction tree it has O(|cliques|*q^(w+1)) entries.
Constructing a narrow junction tree is a separate problem and cost.

Proof of the proposed formula: for any compatible full pair of weighted
distributions M_0,M_1, the common submeasure R(y)=min(M_0(y),M_1(y)) has
mass equal to Bayes error and supplies feasible clique tables. Thus that
error is at most the LP optimum. Conversely, feasible R_C extend to a
global submeasure R by the ordinary junction-tree marginal extension.
For each theta the residual tables M_theta,C-R_C are nonnegative and
separator-consistent, with common mass p_theta-rho. Extend them separately
to global residual submeasures D_theta. Then M_theta=R+D_theta has the
required marginals and its overlap is at least rho. Maximizing rho proves
equality. The extension is applied to nonnegative measures of any common
mass; at zero mass use the zero measure. Normalization followed by the
junction-tree product handles positive mass, with zero-separator cells
assigned zero and irrelevant conditionals filled arbitrarily.

Finite minimax duality equates worst compatible Bayes error with the value
of an optimal randomized prediction policy robust to every compatible
joint distribution. The displayed primal LP alone does not give a fast
executable policy. Extracting one from its dual, and verifying its whole
decision bill, remain separate steps. The formula requires only a tree
of specified marginal scopes; it does not assume Nature chose the
junction-tree product distribution.

For disconnected non-overlapping scopes, the LP reduces to the minimum
individual Bayes error, reproducing the known best-source theorem. For a
common separator it reduces to a stratum-wise minimum. Cyclic scope
families need global extendability constraints; local consistency alone
is insufficient. More than two states, arbitrary loss menus and a
simultaneously least-informative joint channel are not asserted here.

## Early comparison: park standalone novelty

Eban, Mezuman and Globerson, *Discrete Chebyshev Classifiers*, ICML2014,
sections2.1-2.4, Theorem2.1/Corollary2.2/Theorem2.3, already solve the
worst-case hinge problem from tree-structured label/feature marginals.
For binary labels this directly supplies the exact randomized 0/1 problem:
clip the score difference d=f(x,1)-f(x,0) to[-1,1], which cannot increase
either hinge loss. Predict1 with probability(1+d)/2. Each resulting
randomized error is exactly half the corresponding clipped hinge loss.
Conversely every randomized binary policy has this score representation.
Thus DCCh/2 is the present minimax value. The paper's factor-two statement
concerns deterministic classification; it is not a gap this construction
closes. Its MAP/junction-tree method also supplies an executable score
without materializing the full joint table.

The common-submeasure proof above is a compact alternate derivation, but
does not establish a new tractability result. The observed-separator
example remains a useful ordinary-control lesson for reading the2026
paper's overlapping-source discussion. PARK the generic candidate before
implementation. No large probe panel or contribution-event forecast is
warranted by this branch.
