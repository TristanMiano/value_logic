# A decision-specific proof can bypass the raw parameter cap

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; a cheap consequence of
the existing N16 upper-endpoint proof, not a new generic proof system.

The [format counterexample](format_limits.md) is a limitation of a
particular rational-parameter receipt. It is not a lower bound on all
bounded reasoning. For a rank-one target and exact0<C<I, the core theorem
and its convex upper parameterization give

    upper(C,c,e)<1 iff c^T(C^(-1)-I)c>E.             (B1)

Indeed, in the compact parameter eta, g(0)=1 and
g'(0)=1-c^T(C^(-1)-I)c/E. A negative derivative supplies a strictly
smaller feasible value. If that derivative is nonnegative, convexity in
r=eta/(1+eta) makes0 a minimizer, so the endpoint equals1. Equivalently,
the cancellation construction attains1 exactly when the reverse weak
inequality holds. This uses the full sharp theorem only for necessity.

For a truthful upper bracket C_plus, the sufficient comparison

    tr(V*(C_plus^(-1)-I))>E

already proves every compatible edited value is strictly below1. It is
valid for any PSD trace-one V because the upper family's derivative is
linear in V; the exact iff characterization of the true optimized value
is asserted only for a rank-one target. Matrix inverse order transports
the sufficient condition to the unknown true C.

In the format example the difference is exactly

    1/C-1-E = 1/[v(v+1)] >0.

An exact symbolic comparison therefore settles the decision even though
no raw upper parameter within4096 bits can do so. Intermediate arithmetic
still has a cost and can exceed input bit lengths. The rule does not
provide the v1 schema's explicit rational upper endpoint below1; it
would be a separately specified qualitative decision certificate.

No implementation or new readiness forecast is attached. The useful
lesson is task-specific: a numeric interval representation can be more
demanding than the decision it supports. Ordinary boundary analysis
provides this shortcut. Future work should compare certificate formats
and actual arithmetic costs before calling a representation limit a
limit of bounded reasoning itself.

The4096-bit example has an extremely small strict margin. A positive cost
for acquiring, checking or using a solution can overwhelm that margin.
The qualitative rule alone does not prove positive net value at a charged
threshold1-minus-cost. Its role here is to separate representation limits
from intrinsic decision impossibility, not to supply an economic win.
