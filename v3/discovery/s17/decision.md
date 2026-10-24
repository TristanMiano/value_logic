# One useful decision, with its information and price conditions

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT.
This is the decision consequence of [N16-C/v1](claim.md), not an empirical
performance result. It uses the existing s16 fixture and its chosen rational
parameters. All claims about actual systems remain conditional on truthful
old-value and edit warrants.

Assessment update: the stronger two-scalar control also settles the original
0.539 threshold. The preferred contribution example is now the separately
documented [0.5385 decision](two_scalar_control.md), which the rounded block
certifies and that two-scalar information class cannot certify. Preserve the
original result below as a valid but weaker comparison.

A later algebraic [cancellation example](cancellation_decision.md) gives a
larger capability separation: a rounded block certifies an upper value of
about 0.583119 below 0.6, while a full-rank source preserving the entire old
optimizer and residual permits value exactly one. It is a constructed
information comparison, with three old queries and their precision charged.
The original and tighter examples remain preserved, including the adverse
strong-control comparison and their distinct precision results.

## Decision and ambiguity from one old value

An edited service is admissible exactly when its reoptimized ridge objective
F(N;Wc) is strictly below tau=539/1000. A known alternative has objective tau;
any common execution costs can be added to both. This is a comparison of
objective values, not a claim that checking the certificate supplies the
new optimizer or pays the service's execution cost.

Let C=diag(1/10,9/10), c=(1,1)/sqrt(2), and e=1/10. The old target value
c^T Cc=1/2 alone cannot settle the comparison over its compatibility class.
Indeed, M=I and W=I give that same old value. For any unit c, edits
N=I+(1/10)cc^T and N=I-(1/10)cc^T have the allowed operator norm and give
respectively F=100/221<539/1000 and F=100/181>539/1000. The same dimensions
and target c can be used in both comparisons. Thus no sound rule using
only that old scalar and this norm warrant can always certify admissibility.

The richer block excludes those sources. The existing checker, at
t_lower=141/625 and t_upper=5211/21100, gives for exact C

    lower = 618573873750 / 1340748094907,
    upper = 867127945275459 / 1611861132384100 < 539/1000.

It therefore certifies every compatible edit as admissible without acquiring
its new objective value. The rounded s16 bracket C+/-10^-5 I also certifies
the same decision. The information gain is concrete, but it uses more
retained old information. A conventional implementation given the same
information and theorem returns the same answer.

## Acquisition and decision-specific precision

The three old queries q(e_1), q(e_2), q(e_1+e_2), with q(z)=z^T C z,
determine the block by polarization. The last is twice the target query.
Thus the block has three scalar observations versus one, with two additional
directions; costs of normalized and unnormalized queries must be stated by
the actual service. Retaining W, the error warrants and source identity also
costs resources. A vector-returning solver or a richer old receipt may supply
this information more cheaply, and is a necessary alternative in applications.

For uniform absolute half-width epsilon on these three queries, ordinary
polarization and the row-sum norm bound give a matrix half-width
delta=(5/2)epsilon. The earlier epsilon=4*10^-6 is sufficient but is not a
necessary precision for this particular threshold. With the same upper
parameter, the scalar bound for the diagonal upper bracket is

    U(delta) = (1+t)/2 * [ (1/10+delta)/(1+d(1/10+delta))
                         +(9/10+delta)/(1+d(9/10+delta)) ],
    d=t-E-E/t, t=5211/21100, E=1/100.

It is strictly increasing in delta while the bracket is in the domain.
Testing this rational expression at a declared delta is sufficient; a
certified scalar optimizer is unnecessary for the decision. The
[exact check](decision_check.py) and [result](decision_result.json) establish
that delta=2/3125, corresponding to epsilon=4/15625, still certifies it:

    upper = 3053006421894548945019 / 5668003681640145208100
          = 0.538638750674... < 0.539.

This is 64 times the old scalar half-width: six fewer binary precision bits
are sufficient in this example. At 128 times the old half-width this fixed
certificate is unresolved, with upper 0.539310439798...; that does not prove
every possible certificate would fail. No runtime or fee reduction follows
from the tolerance ratio alone. Its effect on actual acquisition cost must
be measured or warranted separately. The exact audit ran in 891,900 ns;
that one observed implementation run is not a service cost model.

## Conditional economics, with strong alternatives retained

Suppose the two extra old directions cost A each at the required precision,
retention costs S over the intended horizon, a certificate costs B per edit,
and obtaining a fresh new objective costs P. For J edits all satisfying the
same warrant and decision threshold, this route costs 2A+S+JB, versus JP
for the specified fresh-value policy. Its break-even condition is

    P>B and J > (2A+S)/(P-B).

This is an accounting identity under stated prices, not measured savings.
The oracle returning all three values at once, warm-started solves, storing
solution or residual vectors, direct robust optimization from known M, and
acquiring these same two directions only when needed are stronger practical
alternatives. Their information, precision, storage and cost must be compared
on the actual workload. The present bounded event establishes a new usable
information-conditioned guarantee only if its prior-art comparison survives;
it does not promise favorable economics on every interface.
