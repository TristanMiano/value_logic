# Two old regularization values bound the missing moment sharply

Codex (GPT-6), October 23, 2026. DEVELOPMENT; new acquisition derivation.
s14 already related the extra moment to a value derivative. This note
uses two finite value observations instead, without assuming a derivative
oracle or retaining a solve vector. Moment-problem inequalities are the
ordinary ingredients; the exact application needs a primary comparison.

Let s=v^T(I+MM^T)^(-1)v, ||v||=1, and for a known t>1 retain

    r=v^T(I+t*M M^T)^(-1)v.

Both old objective values and the common operator/target identity must be
warranted. They cost two solves if not already available. We seek the
unobserved moment m=v^T(I+MM^T)^(-2)v used by the inherited edit envelope.

## Sharp moment interval from a transformed spectral measure

Let lambda in(0,1] have the spectral distribution of S=(I+MM^T)^(-1)
at v. Then E[lambda]=s, E[lambda^2]=m and
r=E[lambda/(t-(t-1)*lambda)]. Put a=t-1. Feasible finite nontrivial
receipts satisfy

    0<s<1,       s/(t-a*s)<=r<s.                         (1)

The lower r inequality is Jensen for a convex scalar function; the upper
is strict unless the target lies entirely in the eigenvalue-one space.
Introduce the positive measure dnu=dP/(t-a*lambda), with moments

    q0=(1+a*r)/t,       q1=r,       q2=h=(t*r-s)/a.

Writing q3=k, the desired moment is m=t*h-a*k. Cauchy-Schwarz with
the weights lambda and(1-lambda), respectively, gives

    h^2/r <= k <= h-(r-h)^2/(q0-r).

Therefore the exact closure interval is

    m_lo=s-t*(1-s)*(s-r)/[a*(1-r)],
    m_hi=s-s*(s-r)/(a*r).                                (2)

The proof is a moment calculation, not a finite-difference approximation.
Both endpoints lie between s^2 and s under(1).

## Matching source spectra and the closure qualification

For the lower endpoint, let

    c=t*(s-r)/[a*(1-r)].

A spectral distribution supported on{c,1}, with mass(1-s)/(1-c) at c,
has the required s,r and moment m_lo. Condition(1) gives 0<c<=s<1,
so a finite diagonal M realizes it. At Jensen equality c=s and the
distribution reduces to one point.

For the upper endpoint put d=(t*r-s)/(a*r). The measure on{0,d} with
mass s/d at d has the required s,r and moment m_hi. A positive mass at
zero is only a closure spectrum: finite M cannot have a zero resolvent
eigenvalue. For a small positive epsilon, replace the two support points
by epsilon and

    d_epsilon=(h-epsilon*r)/(r-epsilon*q0),

with mass(s-epsilon)/(d_epsilon-epsilon) at d_epsilon. For strict Jensen
inequality and sufficiently small epsilon these are feasible points in(0,1],
match s,r exactly and approach the upper endpoint. This follows also by
substituting the two support points into
h=(epsilon+d_epsilon)*r-epsilon*d_epsilon*q0. Degenerate single-point
receipts attain m=s^2 without this limiting construction.

## Price and precision consequences

The new information can be inserted as a JOINT moment interval into the
existing transport/checker. A value at tM M^T is not the same as an edit
bound on an unrelated matrix. The operator, target, norm and scale receipts
must match, and any later perturbation is still separately warranted.

The interval width is

    (s-r)/a * [r*(t-a*s)-s]/[r*(1-r)].                   (3)

For t approaching1, it shrinks to zero for a fixed finite spectrum, because
r=s-(t-1)*(s-m)+O((t-1)^2). This recovers s14's derivative relation in
the limit. It does not make close-scale measurements free: subtracting s-r
amplifies value uncertainty by about1/(t-1). Rounded inputs require an
optimization or outward bounds over all compatible(s,r), not substitution
of their printed midpoints. Nearby solves may share a factorization, which
the ordinary control must also be allowed to use.

For the earlier spectrum with equal masses at1/10 and9/10, s=1/2 and
m=41/100. At t=2 the second receipt is91/209, yielding

    91/236<=m<=155/364.

At t=101/100, r=504100/1010009 gives

    829109/2023636<=m<=8273/20164.

These intervals use two old scalar values rather than the three
cross-target values in the previous acquisition route. Their actual
precision/acquisition prices differ. They are not an economic superiority
claim, and an ordinary moment-bound implementation obtains the same result.

The [exact probe](scale_probe.py) checked18 receipt pairs, all lower
matching spectra and48 finite upper-approach witnesses. At t=1001/1000
the example's second value50041000/100100009 gives the moment interval
[82009/200036,82073/200164]. Both rational threshold checks pass for the
later edit e=1/10, certifying F_new in(.4608,.539) from these TWO old
values. The [output](scale_probe.json) binds the corrected source and
records3,552,700ns of execution. The initial string-format assertion
failure and original source are retained in[failures](failures.md).
This is same-model developmental arithmetic, not independent validation
or a measured saving in solve time or audit fees.
