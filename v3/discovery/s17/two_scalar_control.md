# The original decision is also solved by a stronger two-scalar control

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; adverse comparison and repair.
This preserves rather than erases the original threshold example in
[decision.md](decision.md).

For the canonical source realizing C=diag(1/10,9/10) and c=(1,1)/sqrt(2),
the old value and residual moment are s=1/2 and m=41/100. The existing
[s14 two-scalar upper theorem](../s14/two_scalar_upper.md) uses the ordinary
robust residual expression

    J(alpha)=(sqrt(1-alpha+(41/100)alpha^2)+(3/100)alpha)^2
              +(9/100)alpha^2, alpha>=0.

At alpha=97/100, let R=415769/1000000. Expanding gives

    J(alpha)=50129681/100000000+(291/5000)sqrt(R).

An elementary outward square-root interval therefore proves J(97/100)<0.539.
This stronger control settles the original decision too. If the old solver
already returns its residual, retaining m can be cheaper than acquiring two
extra target directions. The original three-versus-one example is a valid
information separation, but not evidence that the sharp block formula is
needed at that threshold.

## A tighter developmental decision isolates additional block information

Use tau=1077/2000=0.5385 for a separate example. N16's existing rounded
upper certificate remains below this value. The two-scalar information
class, even with exact s=1/2 and m=41/100, has a worst value above it.
Here is an exact way to certify that latter comparison, without trusting a
floating scalar optimizer.

The robust norm-squared part of J is convex, and (9/100)alpha^2 gives
strong convexity constant mu=9/50. Hence for any alpha0>=0,

    min_(alpha>=0) J(alpha)
      >= J(alpha0)-[J'(alpha0)]^2/(2 mu).

At alpha0=97/100, the rational interval

    403/625=0.6448 < sqrt(R) < 64481/100000=0.64481

gives J(alpha0)>0.5388 and |J'(alpha0)|<1/800. Consequently

    min J > 0.5388-1/230400 > 0.5385.

The derivative used is

    J'(alpha0)=-14127/500000+(3/50)sqrt(R)
                       -(297693/50000000)/sqrt(R).

The s14 attainment argument supplies a compatible rank-one old source and
edit realizing min J for this two-scalar information class. Thus it cannot
certify the tighter decision, whereas the full block can. This is an
information-content comparison, not a same-information algorithm victory.
The [exact check](control_check.py) and [record](control_result.json) pass
these inequalities. The conservative lower certificate is 0.538795659722... .

An even simpler direct witness removes dependence on the general s14
attainment theorem for this comparison. Take v=(1,0),

    M=(5/3,-4/3)^T, N=(119/75,-209/150)^T.

The old residual is w=(1/2,2/5), giving s=1/2 and m=41/100.
The edit is (-2/25,-3/50), of squared norm 1/100. Direct inversion gives

    F(N;v)=66181/122825=229/425 > 1077/2000.

Pad both sources with a zero column and rotate the output basis if the
comparison requires the same 2-by-2 shape and target c=(1,1)/sqrt(2) as the
block example. These operations preserve every scalar receipt and the edit
norm. The source fails the additional full-block observations, as it must.
This finite feasible witness alone proves the two-scalar information cannot
certify the tighter decision. The convex lower bound above remains a useful
separate check, but is no longer a load-bearing dependency for that fact.
The [witness script](control_witness.py) and [record](control_witness.json)
verify its old residual, moment, edit norm and new objective exactly.

The tighter threshold was selected during this assessment after the stronger
control defeated the original separation. It is a mathematical development
example, not a fresh empirical evaluation or preregistered success metric.
The original 64-fold precision result remains true at 0.539. A separate
precision check at 0.5385 passes at 32 times the original half-width, with upper
0.538302847547... (see the exact fraction in the record), and is unresolved
at 64 times. Thus five fewer binary precision bits suffice for the tighter
decision with this fixed certificate. No fee or runtime gain is inferred.

The [same-vector comparison](vector_control.md) strengthens this further:
the ambiguous old source can preserve the entire optimizer and residual
in the same two-by-two dimensions, not only their two scalar summaries.
Using the full source or the actual edit direction remains a stronger,
separate ordinary option whose costs must be compared in an application.
