# Uncertain query-cell probabilities without a free known sensor law

Codex (GPT-6), DEVELOPMENT extension of the query/flip regret construction.
The known cell-mass requirement can be weakened for one useful uncertainty set.
This is an elementary convex-extreme-point adaptation, not a generic robust
belief-update theorem or a new robust optimization principle.

Keep the conditional mean intervals for each cell, but only warrant
p_z>=L_z>=0 with sum_z L_z<=1. Let gamma=1-sum_z L_z. The admissible mass
vectors are exactly

```math
p=L+\gamma q,\qquad q\in\Delta_{2^r}.
```

Fix the proposed policy or private policy mixture before choosing p. Its
cellwise fees and expected terminal coefficients remain fixed. For any
competing policy, the mean-box maximization gives a fixed per-cell support
value; multiplying by nonnegative p_z and summing yields its regret. Thus the
worst regret R(p) is the maximum of linear functions of p, so is convex.
Its maximum over this simplex is achieved at one of the 2^r mass vectors
L+gamma e_z. Equivalently, the joint maxima over p, means and comparator can
be interchanged, and maximizing a fixed linear objective in p selects a vertex.

Run the existing exact regret oracle at each such mass vector and take the
largest result. Retain its mean witness and mass vector. This is exact for the
declared lower-mass/conditional-box source. It costs at most 2^r oracle calls,
still avoiding a distribution over all m hidden signs or all mean-box corners.
Gamma=0 requires one call. Gamma=1 allows concentration in a single cell and
usually makes the guarantee much weaker; this is real missing information.

One interpretation is a contamination model p=(1-epsilon)p0+epsilon q, with
known epsilon and a nominal p0, giving L=(1-epsilon)p0. A fallible model does
not establish that contamination bound by itself. Another interpretation uses
simultaneous lower confidence bounds for cell masses, with the actual risk
account and sampling semantics supplied separately. Unknown masses alone do
not warrant narrow conditional mean intervals in rare cells.

General two-sided bounds or coupled constraints on masses have different
extreme points; the 2^r formula is not valid for them. Its vertices may violate
those added upper constraints. They remain a conservative relaxation when the
lower source contains the actual source, but cannot be called attaining
witnesses for the more constrained source.

For mixed-scenario policy synthesis, the ordinary best response averages
unnormalized cell masses and moments: pbar_z=sum_k beta_k p_kz and
tbar_zi=sum_k beta_k p_kz mu_kzi. Where pbar_z>0 use mu_bar=tbar/pbar.
The source mean in the previous known-mass game is a special case. Arithmetic
averaging of conditional means when cell masses vary is generally wrong.

Prospective cheap screen: use the saved small four-cell instance and the large
sixteen-cell instance; compare epsilon=0,1/4,1. On the small case explicitly
enumerate all mean-box corners at each mass vertex. Check monotonicity under
increasing epsilon and keep one common attaining source for each result.

`mass_probe.py` and `mp01` complete the declared two-source screen on first
attempts. The small source checks 2,304 corner/vertex combinations in total
(one, four and four mass vertices times 256 corners). Every oracle bound
equals explicit corner optimization and has a single attaining common source.
The large source uses one, sixteen and sixteen oracle calls, with source
witness reconstruction at each. These are supplied-source checks; no estimated
contamination guarantee or physical acquisition saving is inferred.
