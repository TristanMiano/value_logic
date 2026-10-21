# A second scalar receipt can certify a whole response band

Codex (GPT-6), DEVELOPMENT, October21,2026. An elementary quantitative-Jensen
adapter of the positive spectral model in one_value_bounds.md. This is a
decision certificate, not a claimed new moment-optimization method.

Normalize y0=1 and let Z=(1+t0*lambda)^(-1) in[a,b] subset[0,1]. Retain
mu=E Z and a second response nu=E h_s(Z), s>1, where

    h_r(z)=z/[r+(1-r)z],  d_r(z)=r+(1-r)z,  r>0.

The exact identity

    h_r(z)-h_r(mu)-h_r'(mu)*(z-mu)
      = r*(r-1)*(z-mu)^2/[d_r(z)*d_r(mu)^2]

follows by subtracting two fractions. Hence the Jensen gap Delta_s=nu-h_s(mu)
is nonnegative. If it is zero, Z=mu almost surely, because s>1 and its
denominator is strictly positive. Every positive-time response then equals
h_r(mu), even without a supplied rank bound. This identifies the scalar
spectral measure seen by b, not A or the total matrix rank; invisible modes
remain unrestricted. In a finite matrix with nonzero b, mu>0.

For Delta_s>0 define

    K(r,s,mu)=r*abs(r-1)*d_s(mu)^2/[s*(s-1)*d_r(mu)^2],
    m=min(d_s(a)/d_r(a), d_s(b)/d_r(b)),
    M=max(d_s(a)/d_r(a), d_s(b)/d_r(b)).

The ratio d_s(z)/d_r(z) is monotone because its derivative has the sign of
r-s. Dividing the two exact gap identities therefore gives

    K*m*Delta_s <= abs(E h_r(Z)-h_r(mu)) <= K*M*Delta_s.

For r>1 the signed gap is positive; for0<r<1 it is negative. At r1 the
response is exactly mu, and at r0 the separately retained baseline applies.
For[a,b]=[0,1], m=min(s/r,1) and M=max(s/r,1). The result can be intersected
with the one-value envelopes. It stays finite for each fixed r>0, but its
constants need not be uniform as r tends to zero or the requested range grows.

Proof detail: divide E[(Z-mu)^2/d_r(Z)] by
E[(Z-mu)^2/d_s(Z)]. It is a weighted average of d_s(Z)/d_r(Z), with weights
proportional to (Z-mu)^2/d_s(Z). The weights are nonnegative and nonzero
exactly when Delta_s>0. Thus the endpoint ratio bounds apply without a
variance estimate, discretized spectrum or learned full model.

## A finite physically realizable example

Let Z put equal mass on7/10 and4/5. Then mu=3/4, s2 gives nu=47/78 and
Delta_s=1/390. At r3, h_r(mu)=1/2 and K=25/12, so even with only the generic
support[0,1] the new band is

    1/2 + 25/7020 <= y(3*t0)/y0 <= 1/2 + 25/4680.

The true response is113/224, inside that band. Intersecting the two separate
one-value envelopes gives lower endpoint94/187, obtained from
(47/78)/(3/2-(47/156)), and upper endpoint47/78. Therefore the certified
width decreases from47/78-94/187 to25/14040 in this stated example.
This is an analytic information comparison, not a measured runtime or label
saving. The ordinary joint-moment optimizer can be stronger still.

## Partial numerical receipts

If mu is retained exactly and nu is only in[L,U], intersect that interval
with the prior one-value envelope and Delta_s>=0. The two gap endpoints are
monotone in Delta_s; substitute the allowed endpoints with the correct sign.
If both values are uncertain, the same formulas remain pointwise sound for
every compatible mu and nu, but their outer extrema must actually be bounded.
Do not plug in midpoint values or ignore correlated errors. Any rigorously
bounded scalar optimization over that two-dimensional receipt set is enough;
no exact-rank assertion follows from a merely small observed gap.

The deterministic band holds simultaneously for every r>0 under the same
spectral premises. A later decision can choose r from the receipt without
an additional union bound. If the purchased intervals are statistical, their
joint coverage event must already be warranted; pointwise error bars chosen
after inspecting many evaluations do not supply that event for free.

This is a way to turn progress of two numerical calculations into a warrant
for a later decision. The mechanism, positivity, measurement intervals and
units still need independent justification. Quantitative Jensen inequalities,
moment methods and rational interpolation are its conventional antecedents.

The first gap_probe.py run passed2430 exact gap checks on135 two-atom laws,
including1890 strict interior inequalities and16 single-atom checks. Its
worked interval matches the fractions above. Elapsed execution0.0766334s;
this is a small development screen, not independent confirmation.
