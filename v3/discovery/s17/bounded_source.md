# Separate candidate: a retained block with a source-norm warrant

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; exploratory N17-K route.
This is an extension, not a prerequisite or added success metric for N16-C/v1.
It uses classical chord/Jensen bounds and the preceding endpoint constructions.
Its own close-prior and readiness assessment are outstanding.

Retain N16's C,c,e and additionally ||M||op<=K, with K>0. Put

    beta=1/(1+K^2), E=e^2, h=(E+sqrt(E^2+4E))/2, s=c^T Cc.

The information class is nonempty exactly when beta I<=C<I. Necessity
follows from S=(I+MM^T)^(-1)>=beta I, and the canonical source
M=(C^(-1)-I)^(1/2) proves sufficiency. The endpoint beta is permitted.

## Proposed exact piecewise families

As before a=1+t and d=t-E-E/t. Define

    lower_K(t) = c^T C(aI-dC)^(-1)c,                   t>=h;
                 (a*s-beta*d)/[(a-d)(a-beta*d)],        0<t<h.

For the upper endpoint define

    upper_K(t) = a*c^T C(I+dC)^(-1)c,                 t>=h;
                 a*(s+beta*d)/[(1+d)(1+beta*d)],        E<t<h.

The claim to develop is that the sharp lower endpoint is max_(t>0)
lower_K(t), and the sharp upper endpoint is inf_(t>E) upper_K(t), including
the upper limit 1 at t=infinity. If s=beta, the finite upper limit at t=E
is also included. If s>beta that boundary diverges and is irrelevant.
Both endpoints are finitely attained in unrestricted compatible dimensions.

## Validity: spectrum-bounded chord replacements

The spectrum of S lies in [beta,1]. For t>=h, the existing Jensen bounds
apply unchanged. For 0<t<h, d<0, and L_t(x)=x/(a-dx) is concave on this
interval. Its chord is

    L_t(x) >= (a*x-beta*d)/[(a-d)(a-beta*d)].

Functional calculus and compression then give lower_K(t). This uses the
pointwise scalar chord on the spectrum, not an unjustified scalar-to-operator
convexity inference. The Young lower inequality is valid for every t>0.

For E<t<h, -1<d<0 and U_t(x)=a*x/(1+d*x) is convex with positive
denominator. Its chord is

    U_t(x) <= a*(x+beta*d)/[(1+d)(1+beta*d)].

The Young upper inequality is valid on this domain because I+dS>0. This
gives upper_K(t). A parameter at or below E is not a uniform matrix inverse
witness when hidden eigenvalue-one directions are allowed.

## A compatible source attaining the chord families when stationary

Let D=(C-beta I)/(1-beta), so 0<=D<I. The block matrix

    P=[[D,sqrt(D(I-D))],[sqrt(D(I-D)),I-D]]

is an orthogonal projection. Put S=beta I+(1-beta)P, W=[I;0], and
M=(S^(-1)-I)^(1/2). It has norm K, compression C and

    Q=W^T S^2 W=(1+beta)C-beta I=:Q_max.

Every scalar function of S is its chord between beta and one, so the
piecewise chord expressions are the actual fixed-source scalar families
for this M. At a finite interior optimum, the normal-equation constructions
in proof.md apply to the full S rather than C. Their stationary derivative
again supplies the required norm ratio. The lower rank-one plus edit or
upper rank-one minus edit then attains the displayed family value. For
upper parameters it is convenient to use eta=E/(t-E)>0, as in the core
proof. No general robust-action/reoptimized-value interchange is assumed.

The relevant old coefficient norm is nonzero because s<1. A positive
interior upper minimizer also has nonzero residual, as follows directly
from its positive scalar stationarity relation. The old source can be
singular outside the retained space; the information contract permits that.

## Core-region and cap attainment

At an optimum strictly in t>h, the original canonical source S=C is
compatible with the norm warrant, so the core attainment proof still works.
For upper cancellation the same canonical source suffices.

At t=h the two families meet. Let m_min=c^T C^2c and
m_max=c^T Q_max c. A maximum of the lower piecewise family at the cap has
one-sided derivatives implying

    m_min <= s(1+h)/(2+h) <= m_max.

A minimum of the upper family there similarly implies

    m_min <= s/(2+h) <= m_max.

Choose Q on the line segment from C^2 to Q_max with the indicated target
second moment. The source M0=(W-R)(C-Q)^(-1/2) from second_block.md has
norm at most K by source_norm.md's feasibility characterization. The same
cap rank-one edit in proof.md attains the endpoint. This avoids assuming
that the original unrestricted dilation automatically respects the new norm.

## Boundary cases and existence

The lower family tends to zero at t=0 and infinity and is positive inside,
so its maximum is attained at a finite parameter. The upper family tends to
one at infinity. At t approaching E from above, it diverges when s>beta.
When s=beta, c lies in the beta eigenspace of C, and the limit is

    (1+E)/K^2.

This is exactly the zero-residual rotational regime in the s14 two-scalar
upper theorem. A source of norm K with target along its active direction,
plus one zero output row if needed, attains that value whenever this limit
is the minimizing branch. The other coordinates realizing C can be added
as a direct sum. Cancellation and the finite interior/cap cases cover the
other upper minima. Witness dimensions at most 2k+1 outputs and 2k inputs
suffice by these constructions; dimension optimality is not claimed.

## Relation to ordinary methods and the original goal

The exact conventional Gram SDP can add ||M||<=K through two bounded
interpolation LMIs, as in source_norm.md, without retaining Q. The proposed
delta is a further explicit analytic solution, not a new SDP principle.
The spectral chord is established matrix-inequality machinery. The useful
question is whether a readily available source-norm warrant changes a
decision after source information has been compressed. This extension must
be assessed separately; neither its apparent simplicity nor its development
checks establish moderate novelty or raise N16's current readiness forecast.

## Focused conventional comparison

[bounded_probe.py](bounded_probe.py) compares seven specified cases with the
same-information norm-constrained Gram SDP: a scalar rotational endpoint,
scalar and two-dimensional chord extrema, rotated core interiors, one upper
cap, cancellation and both caps. All fourteen endpoint comparisons passed
the prospective 1e-6 discrepancy and 5e-7 feasibility tolerances. The largest
endpoint discrepancy was 2.584e-8. [bounded_result.json](bounded_result.json)
preserves the matrices, solver states, warnings and Gram outputs. The loop
took 151,852,200 ns; no exact numerical certificate or speedup follows.
Three solves reported `optimal_inaccurate` with the solver's accuracy warning
(the two-chord upper and both endpoints of the both-cap case). Their recorded
violations and discrepancies still meet the prespecified screening tolerances.
The largest violation over all cases was 2.497e-9. The warnings are preserved;
no rerun was used to replace them with more favorable statuses.

## Prospective rounded-scalar decision

Take C=diag(1/10,11/100), c=(1,1)/sqrt(2), e=1 and a truthful K=3
source-norm warrant. The exact target value is s=21/200. Even a scalar
interval [s-1/1000,s+1/1000] can be used in the chord families. Choose
t_lower=1/3 and t_upper=13/10; both use negative d, with E<t_upper<h.
Use the lower scalar endpoint in the lower formula and the upper scalar
endpoint in the upper formula. The proposed decision is simultaneous strict
separation from lower threshold 1/20 and upper threshold 27/100.

Without K, the core C-only lower and upper extrema are both caps and straddle
those thresholds. Thus this tests what the additional norm warrant buys; it
does not assert that the scalar interval is more informative than the full
block or that acquiring K is free. The canonical source realizing this C has
norm three, so the strengthened information class is nonempty.

[bounded_decision.py](bounded_decision.py) and
[bounded_decision_result.json](bounded_decision_result.json) passed the exact
conditional calculation:

    lower = 379/6375 = 0.059450980392... > 1/20,
    upper = 1664/6195 = 0.268603712671... < 27/100.

Runtime was 85,000 ns. This is a check of the separate extension's formulas;
the original s16 checker is unchanged and correctly does not admit these
negative-d parameters without the new norm premise.

## No additional interaction beyond two sharp intervals

Let [L_C,U_C] be the original N16 interval for C,c,e, and let
[L_sK,U_sK] be this bounded-source theorem for the scalar block s=c^T Cc
and the same K,e. Then its full C,K interval is exactly

    [max(L_C,L_sK), min(U_C,U_sK)].

For t>=h, scalar Jensen gives c^T L_t(C)c>=L_t(s) and
c^T U_t(C)c<=U_t(s). For t<h the new chord expressions already depend
only on s,K,e. Taking the indicated scalar extrema proves the identity.
Thus this particular combination of information has no further improvement
beyond intersecting those two sharp intervals. The finite-attainment proof
is what establishes joint sharpness; intersections are not generally sharp
for arbitrary pairs of information contracts.

This is a useful acquisition/retention simplification and also a reason to
be cautious about treating N17-K as an independent novel mechanism. Its
standalone novelty is unassessed; retain it as a concrete adapter and a
possible mathematical extension, not as an automatic second promoted claim.
