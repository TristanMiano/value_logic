# Cheap scalar scores for paired latent costs

Codex (GPT-6), DEVELOPMENT, 2026-10-14.

The contraction inequality is inherited from [s08 scalar transport](../s08/box_transport.md).
It is not new. The present consequence is its score law under separately
observed true/false costs, a cheap conservative discretization, and an executable
prefix service that needs only one source-complete initial scalar bound.

For initial T_i,F_i in [0,H], m-copy count a_i and a checked initial regret
upper U, observing T_i=t guarantees contraction
g_T(t)=min(a_i(H-t),(m-a_i)t). Observing F_i=f guarantees
g_F(f)=min(a_i f,(m-a_i)(H-f)). Their sum is still a valid guaranteed contraction
when both are bought: each is the minimum of that query's nonnegative decrease
against the two possible competitor bits, and sum of minima <= minimum of sums.
Summing across coordinates yields R<=U-sum g, without a new source solve.
Pure action coordinates have zero guaranteed scalar score and can be omitted
from this particular score policy; source-aware ordinary controls may exploit them.

If a is interior and t is continuously uniform on [0,H], then

```math
\Pr[g_T(t)\ge s]=1-\frac{s}{aH}-\frac{s}{(m-a)H}
\quad(0\le s\le a(m-a)H/m).
```

Thus g is uniform on [0,a(m-a)H/m]. The two linear preimage branches prove the
identity. True/false observations are independent under the explicitly chosen
latent law, so scores from distinct latent queries are independent. This fails
for correlated costs without a new conditional-law analysis.

For the executed integer ticks0..24000, m=3 and a=1 or2, replace g by
6000*floor(g/6000). Both query kinds and both interior counts have exactly the
same score histogram: integer scores0,1,2 have counts9000,9000,6001 out of24001.
The discrete distribution is not the continuous uniform distribution; use its
exact counts. With quota Q=ceil((U-tau)/6000), capped convolution has only Q+1
states and three transitions per state, independent of the number of models.

For identical independent score distributions, sorting queries by nondecreasing
fee minimizes expected prefix cost at every fixed prefix length: exchanging two
out-of-order fees changes cost by (c_large-c_small) times the nonnegative drop
in survival probability. Repeated exchanges prove the sorted order. This does
not prove unrestricted adaptive optimality or account for exact source-based
stopping beyond the scalar certificate.

Use the inherited exact prefix formula F_k=sum_j c_j Pr(S_{j-1}<Q)+C Pr(S_k<Q),
including k=0. Choose the least F_k among prefixes with listed fee<=C. Expected
physical fee is <=C under the stated law; realized fee<=2C. A fallback that buys
the cheaper of remaining individual observations and the full bundle only
improves this physical bound. Pay source compilation, initial action search,
histogram/convolution, receipts, scalar updates and final source checks.

The initial action can come from a bounded ordinary witness proposal, and U
from a checked unit-propagated diagram. No complete model enumeration is needed.
The source is still exponential to compile in general. The resource claim must
face exact-threshold and exact one-query controls using the same source and
information menu, not just an expensive full-audit implementation.
