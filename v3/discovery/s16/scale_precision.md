# Rounded finite-scale receipts: a useful bound must pay for precision

Codex (GPT-6), October 23, 2026. DEVELOPMENT; extension of
[finite-scale acquisition](scale_receipts.md). Generic finite-difference
accuracy tradeoffs are conventional; this note retains the exact moment
information contract rather than assuming exact printed solver values.

First keep s exact, t=1+h>1, and suppose the second value r is only known
in a truthful interval[r_minus,r_plus]. Intersect that interval with
[s/(t-h*s),s]. If it is empty, the supplied receipts are inconsistent.
Let L(s,r),U(s,r) denote the moment endpoints in scale_receipts.md. Then

    dL/dr=t*(1-s)^2/[h*(1-r)^2]>0,
    dU/dr=s^2/[h*r^2]>0.

Consequently the sharp closure interval is

    L(s,r_minus)<=m<=U(s,r_plus),                         (1)

using the clipped endpoints. The endpoint witnesses from the exact-value
construction prove sharpness. This is an actual monotonicity argument;
it does not authorize checking corners of unrelated two-moment envelopes.

## A nonasymptotic noise-versus-spacing bound

Let epsilon be the TOTAL width of the clipped interval for r, not the
half-width of a printed plus/minus error bar. On the feasible interval
r>=s/t and r<=s, the two derivatives above are bounded by t/h and t^2/h.
For the actual r, the increase in width is at most
[t^2*(r_plus-r)+t*(r-r_minus)]/h<=t^2*epsilon/h.

The exact width itself admits a uniform bound. Put V=s*(1-s),
d=(s-r)/h and C=1+h*(1-s). The width formula becomes

    width_exact=h*d*(V-C*d)/[r*(1-r)].

Feasibility gives 0<=d<=V/C. Hence d*(V-C*d)<=V^2/(4*C), while
r*(1-r)>=(s/t)*(1-s)=V/t. Therefore

    width_exact<=h*t*V/(4*C)<=h*t/16,
    width_rounded<=min(V, h*t/16+t^2*epsilon/h).          (2)

For h<=1, the simpler bound h/8+4*epsilon/h follows. For sufficiently
small epsilon, choosing h proportional to sqrt(epsilon) gives a rigorous
O(sqrt(epsilon)) width bound. No work/precision price is implied by this
order statement. If the second solve's precision is fixed, taking h toward
zero makes the error bound worse; an exact derivative limit cannot be
obtained by ignoring rounding.

For a particular fixed spectrum, the exact width has the first-order term

    h*(s-m)*(m-s^2)/[s*(1-s)] + O(h^2).

This expansion helps forecast a useful spacing, but the unknown m cannot
be treated as verified input to a price claim. Use the exact interval or
the uniform bound for a certificate. More computation may buy a smaller
epsilon; any optimization of total cost must include that price and reuse
of factorizations by ordinary methods.

## If both old values are rounded

The exact feasible set is convex: r>=s/(t-h*s), r<=s and 0<s<1,
intersected with the two receipt intervals. In the transformed moments,
q0=(1+h*r)/t and H=(t*r-s)/h, the lower and upper endpoints are

    L=H+h*(r-H)^2/(q0-r),
    U=t*H-h*H^2/r.

The quadratic perspective makes L convex and U concave in(s,r) on the
positive-denominator domain. Minimizing L and maximizing U over the
compatible convex receipt set are constant-size convex problems, with
rotated-cone representations if desired. Supply certified bounds on those
optima; favorable feasible optimizer points have the wrong direction for
both ends. A new conic harness is not needed merely to state this reduction.

These guarantees concern uncertainty in retained numerical evidence. They
do not create probability information about a fixed unresolved theorem,
and they do not turn the cost of the original solves into a free resource.
