# Value-only decision radii and retained anchors

Later same-session strengthening: finite_extremizers.md attains the first
distance branch with finite rank-one matrices. For positive values the
displayed infimum is therefore a minimum; the nonmetric conclusion remains.

Codex (GPT-6), DEVELOPMENT, October22,2026. This is a consequence of the
sharp response transport in finite_transport.md, using the same fixed v,
identity regularization and operator-norm distance interface.

For 0<t<s<=1, the infimum matrix distance needed to change an exact scalar
response s to t is

    d(s,t)=(s-t)/sqrt(s*t),                         s+t<=1;
           sqrt((1-t)/t)-sqrt((1-s)/s),           s+t>=1.

Extend by symmetry and d(s,s)=0. This inverts L_e(s)=t. The two expressions
agree at s+t=1. In the first region, the limiting two-dimensional examples
give an infimum; in the second, scalar matrices attain it. Values zero
require closure and infinite distance from a fixed positive response.

An old truthful interval[l,u] and threshold tau have the following duties.
If l>tau, every edit of norm at most d(l,tau) preserves response>=tau.
If u<tau, every edit of norm at most d(u,tau) preserves response<=tau.
Use strict inequality in the radius for a strict threshold conclusion.
For the original matrix update, divide the normalized radius by sqrt(t)
to obtain a bound on ||A^(-1/2)Delta||op at intervention strength t>0.
The old receipt radius, baseline normalization and edit-distance certificate
must all be accounted for before calling this a safe action.

This is a concrete partial-information service: retain a scalar numerical
receipt and an independently warranted distance, and certify a new threshold
decision without resolving the new full matrix or inverse. An ordinary
validated solver can implement exactly the same rule. Any usefulness claim
must compare direct recomputation and conventional perturbation certificates.

For a concrete same-duty comparison, an exact old response1/10 and an upper
decision threshold3/5 permit normalized edit radius5/sqrt(6)=2.041241...
with the sharp envelope. The earlier differential Phi rule permits only
1-sqrt(2/3)+log(5)=1.792941... . Both use the same scalar receipt and norm
premise. The comparison is a larger guaranteed perturbation radius, not a
runtime or audit-fee percentage, and the earlier rule is a restricted
comparator rather than the strongest ordinary implementation.

## Why the sharp scalar envelope is not a complete state

Do not call d a metric. For example,

    d(1/10,3/10)=2/sqrt(3)
       > d(1/10,1/5)+d(1/5,3/10)=1/sqrt(2)+1/sqrt(6).

Squaring the positive quantities proves the strict inequality. Pairwise
extremizers at the intermediate response need not be compatible matrices.
Thus applying sharp one-step envelopes repeatedly can be strictly looser
than applying one envelope from an original anchor with the sum of the
warranted edit lengths. No contradiction to the matrix triangle inequality
arises; the scalar response alone loses the geometry of the extremizers.

In the example, sequential upper envelopes allow1/5 after radius1/sqrt(2)
and then3/10 after an additional1/sqrt(6). The total-radius envelope from
the exact original1/10 is strictly below3/10. Keep the old receipt and its
origin even when a newer interval becomes available. A version change does
not erase the old information.

For several stored anchors i with truthful intervals[l_i,u_i] and independently
validated distances e_i to the current model, intersect

    [max_i L_(e_i)(l_i), min_i U_(e_i)(u_i)].

The intersection is sound. It is not in general the sharp joint-source band:
the anchors share one current matrix and impose compatibility constraints.
Independent extremizers cannot silently be combined. An empty intersection
indicates inconsistent premises or numerical certification and warrants no
decision. A graph of validated version distances can supply safe e_i via
path sums; direct difference bounds may be tighter when edits cancel.

This is an adapter for stored evidence, not a new caching principle. Its
specific benefit is keeping a demonstrably necessary anchor when scalar-only
one-step propagation loses information. A useful future screen would price
anchor retention, distance certification and target solves on a real version
stream; do not infer a net saving from the algebra alone.
