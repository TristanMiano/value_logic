# One paid value can bound a whole positive edit curve

Codex (GPT-6), DEVELOPMENT, October21,2026. A decision-directed adapter of
ordinary spectral representation, Jensen's inequality and secant bounds.
It deliberately avoids claiming full parameter recovery from one value.

Assume the exact mechanism y(t)=b^T(A+tUU^T)^(-1)b, A positive definite,
t>=0, and y0=y(0)>0. Unlike the general cross-response case, input and output
vectors are the same. Write v=A^(-1/2)b and M=A^(-1/2)UU^TA^(-1/2).
Diagonalization gives a probability measure nu on nonnegative eigenvalues
with y(t)/y0=E_nu[1/(1+t*lambda)]. Zero eigenvalues account for task components
unaffected by the edit. This is an ordinary positive spectral measure.

Purchase one response y(t0), t0>0, and put mu=y(t0)/y0. For s=t/t0>0,
set Z=1/(1+t0*lambda) and

    h_s(z) = z/[s+(1-s)z].

Then E[Z]=mu and y(t)/y0=E[h_s(Z)]. Its first derivative is positive and
its second derivative has the sign of s-1. Jensen's inequality and the
secant through z0,z1 therefore give

    s>=1:  h_s(mu) <= y(t)/y0 <= mu,
    0<s<=1: mu <= y(t)/y0 <= h_s(mu).

At s1 both bounds equal the purchased value. At t0 the baseline is separately
known exactly; do not substitute s0 into a formula at z0. The Jensen endpoint
is attained by a single eigenvalue. The other endpoint is approached by a
mixture of eigenvalue0 and an eigenvalue tending to infinity, with weights
chosen to preserve mu. Thus the bounds are sharp over the closure of this
unbounded spectral class, but the limiting endpoint need not have a finite
matrix realization. No small rank or parameter-identification premise is
needed for their validity.

If independently warranted spectral bounds l<=lambda<=u are available,
put a=1/(1+t0*u), b0=1/(1+t0*l), and require a<=mu<=b0. Let c_s be the
affine chord joining (a,h_s(a)) and (b0,h_s(b0)). For s>=1 the sharp bounds
are h_s(mu) and c_s(mu); for s<=1 they are c_s(mu) and h_s(mu). If a=b0 the
curve is fixed. The chord endpoint is attained by a two-point spectral law,
and the Jensen endpoint by one point, so rank at most2 suffices for the
extremizers when that rank is allowed. A stricter rank promise can tighten
the outer bounds but cannot invalidate them. Spectral bounds may be a paid
global duty; do not assume them from the one scalar receipt.

Interval measurements L<=mu<=U give bounds by evaluating the appropriate
lower function at L and upper function at U after intersecting with the
allowed interval [a,b0] (or [0,1] for the closure). Both h_s and its chord
are increasing. This makes a conservative threshold decision without
dividing by a near-zero observed difference or reconstructing a hidden
matrix. An empty measurement intersection signals incompatible premises.

Example: y0=1, t0=1, mu=3/4, and candidate edit t=2. Without spectral bounds,
the resulting value is in[3/5,3/4]. A requirement y(2)<=4/5 is certified;
a requirement y(2)<=7/10 is unresolved. If0<=lambda<=1 is warranted, the
upper bound improves to2/3, so the second requirement is certified too.
An arbitrary full model fitting only y0 and y1 may still predict the wrong
value inside this allowed interval. Task-level adequacy can nevertheless be
sufficient for a decision whose margin is wider than that interval.

Multiple purchased points yield intersections of these envelopes, which
are valid but generally not jointly sharp. Full Stieltjes interpolation and
moment optimization are the strong ordinary methods to compare before
claiming a new multipoint procedure. The present result is a compact useful
specialization, not new numerical analysis, a measured solve reduction, or
a proof that physical intervention semantics can be inferred from values.

The first robust_probe.py execution checked100 rational spectral panels,
1000 envelope inequalities,435 matching endpoint constructions and500 noisy-
interval checks. All passed, together with the displayed3/5-to2/3 example.
The shared tariff/spectral run took0.0502377seconds. This is finite algebraic
evidence, not a measured reduction in paid matrix solves.
